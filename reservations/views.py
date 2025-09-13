from django.shortcuts import render
from django.utils import timezone
from django.db.models import Q
from rest_framework import status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from datetime import datetime, timedelta
from notifications.models import Notification
import logging

# 导入错误处理工具
from keshe.utils import APIErrorHandler, BusinessLogicError, log_user_action, PerformanceMonitor

logger = logging.getLogger(__name__)

from .models import CoachStudentRelation, Table, Booking, BookingCancellation
from .serializers import (
    CoachStudentRelationSerializer,
    TableSerializer,
    BookingSerializer,
    BookingCancellationSerializer,
    BookingCancellationCreateSerializer,
    BookingCreateSerializer
)
from accounts.models import User
from campus.models import Campus


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class CoachStudentRelationViewSet(viewsets.ModelViewSet):
    """师生关系管理"""
    serializer_class = CoachStudentRelationSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    
    def get_queryset(self):
        user = self.request.user
        if user.user_type == 'coach':
            return CoachStudentRelation.objects.filter(coach=user)
        elif user.user_type == 'student':
            return CoachStudentRelation.objects.filter(student=user)
        else:
            return CoachStudentRelation.objects.none()
    
    def perform_create(self, serializer):
        user = self.request.user
        if user.user_type == 'coach':
            serializer.save(coach=user, applied_by='coach')
        elif user.user_type == 'student':
            serializer.save(student=user, applied_by='student')
    
    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        """同意师生关系申请"""
        relation = self.get_object()
        user = request.user
        
        # 检查权限
        if user not in [relation.coach, relation.student]:
            return Response(
                {'error': '只有相关的教练或学员可以处理申请'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        if relation.status != 'pending':
            return Response(
                {'error': '申请状态不正确'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        relation.status = 'approved'
        relation.processed_at = timezone.now()
        relation.save()
        
        # 创建通知
        if user == relation.coach:
            # 教练同意申请，通知学员
            recipient = relation.student
            message = f"教练 {user.username} 已同意您的师生关系申请"
        else:
            # 学员同意申请，通知教练
            recipient = relation.coach
            message = f"学员 {user.username} 已同意您的师生关系申请"
        
        Notification.create_system_notification(
            recipient=recipient,
            title="师生关系审核结果",
            message=message,
            data={'relation_id': relation.id, 'type': 'relation_approved'}
        )
        
        return Response({'message': '申请已同意'})
    
    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        """拒绝师生关系申请"""
        relation = self.get_object()
        user = request.user
        
        # 检查权限
        if user not in [relation.coach, relation.student]:
            return Response(
                {'error': '只有相关的教练或学员可以处理申请'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        if relation.status != 'pending':
            return Response(
                {'error': '申请状态不正确'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        relation.status = 'rejected'
        relation.processed_at = timezone.now()
        relation.save()
        
        # 创建通知
        if user == relation.coach:
            # 教练拒绝申请，通知学员
            recipient = relation.student
            message = f"教练 {user.username} 已拒绝您的师生关系申请"
        else:
            # 学员拒绝申请，通知教练
            recipient = relation.coach
            message = f"学员 {user.username} 已拒绝您的师生关系申请"
        
        Notification.create_system_notification(
            recipient=recipient,
            title="师生关系审核结果",
            message=message,
            data={'relation_id': relation.id, 'type': 'relation_rejected'}
        )
        
        return Response({'message': '申请已拒绝'})


class TableViewSet(viewsets.ReadOnlyModelViewSet):
    """球台信息查看"""
    serializer_class = TableSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = Table.objects.filter(is_active=True)
        campus_id = self.request.query_params.get('campus_id')
        if campus_id:
            queryset = queryset.filter(campus_id=campus_id)
        return queryset
    
    @action(detail=False, methods=['get'])
    def available(self, request):
        """获取可用球台"""
        start_time = request.query_params.get('start_time')
        end_time = request.query_params.get('end_time')
        campus_id = request.query_params.get('campus_id')
        
        if not all([start_time, end_time]):
            return Response(
                {'error': '请提供开始时间和结束时间'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            start_dt = datetime.fromisoformat(start_time.replace('Z', '+00:00'))
            end_dt = datetime.fromisoformat(end_time.replace('Z', '+00:00'))
        except ValueError:
            return Response(
                {'error': '时间格式不正确'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # 获取基础查询集
        queryset = Table.objects.filter(is_active=True, status='available')
        if campus_id:
            queryset = queryset.filter(campus_id=campus_id)
        
        # 排除已被预约的球台
        occupied_tables = Booking.objects.filter(
            start_time__lt=end_dt,
            end_time__gt=start_dt,
            status__in=['pending', 'confirmed']
        ).values_list('table_id', flat=True)
        
        available_tables = queryset.exclude(id__in=occupied_tables)
        serializer = self.get_serializer(available_tables, many=True)
        
        return Response(serializer.data)


class BookingViewSet(viewsets.ModelViewSet):
    """预约管理"""
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    
    def get_serializer_class(self):
        if self.action == 'create':
            return BookingCreateSerializer
        return BookingSerializer
    
    def get_queryset(self):
        user = self.request.user
        queryset = Booking.objects.all()
        
        if user.user_type == 'coach':
            queryset = queryset.filter(relation__coach=user)
        elif user.user_type == 'student':
            queryset = queryset.filter(relation__student=user)
        else:
            return Booking.objects.none()
        
        # 过滤参数
        status_filter = self.request.query_params.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        date_from = self.request.query_params.get('date_from')
        if date_from:
            try:
                date_from = datetime.fromisoformat(date_from)
                queryset = queryset.filter(start_time__gte=date_from)
            except ValueError:
                pass
        
        date_to = self.request.query_params.get('date_to')
        if date_to:
            try:
                date_to = datetime.fromisoformat(date_to)
                queryset = queryset.filter(start_time__lte=date_to)
            except ValueError:
                pass
        
        return queryset.order_by('-start_time')
    
    def perform_create(self, serializer):
        user = self.request.user
        
        try:
            logger.info(f"User {user.username} attempting to create booking")
            
            # 验证师生关系
            relation_id = self.request.data.get('relation_id')
            if not relation_id:
                raise BusinessLogicError("师生关系ID不能为空", "missing_relation_id")
            
            try:
                relation = CoachStudentRelation.objects.get(
                    id=relation_id,
                    status='approved'
                )
                if user not in [relation.coach, relation.student]:
                    raise BusinessLogicError('无权限创建此预约', 'permission_denied', 403)
            except CoachStudentRelation.DoesNotExist:
                raise BusinessLogicError('师生关系不存在或未通过审核', 'relation_not_found', 404)
            
            # 检查时间冲突
            start_time = serializer.validated_data.get('start_time')
            end_time = serializer.validated_data.get('end_time')
            table_id = serializer.validated_data.get('table_id')
            
            if start_time and end_time and table_id:
                conflicting_bookings = Booking.objects.filter(
                    table_id=table_id,
                    status__in=['pending', 'confirmed'],
                    start_time__lt=end_time,
                    end_time__gt=start_time
                )
                
                if conflicting_bookings.exists():
                    raise BusinessLogicError('该时间段已被预约', 'time_conflict', 409)
            
            # 保存预约
            booking = serializer.save()
            
            # 记录用户操作
            log_user_action(
                user, 
                'create_booking', 
                f'booking_{booking.id}',
                {
                    'relation_id': relation_id,
                    'table_id': table_id,
                    'start_time': str(start_time),
                    'end_time': str(end_time)
                }
            )
            
            # 创建通知
            try:
                if user == relation.coach:
                    # 教练创建预约，通知学员
                    recipient = relation.student
                    message = f"教练 {relation.coach.username} 为您创建了一个新的预约"
                else:
                    # 学员创建预约，通知教练
                    recipient = relation.coach
                    message = f"学员 {relation.student.username} 创建了一个新的预约"
                
                Notification.objects.create(
                    recipient=recipient,
                    sender=user,
                    message=message,
                    notification_type='booking_created',
                    related_object_id=booking.id
                )
                
                logger.info(f"Notification created for booking {booking.id}")
                
            except Exception as e:
                logger.warning(f"Failed to create notification for booking {booking.id}: {e}")
                # 通知创建失败不应该影响预约创建
            
            logger.info(f"Booking {booking.id} created successfully by user {user.username}")
            
        except BusinessLogicError:
            # 重新抛出业务逻辑错误，让DRF处理
            raise
        except Exception as e:
            logger.error(f"Unexpected error creating booking for user {user.username}: {e}")
            raise BusinessLogicError('创建预约时发生错误', 'creation_failed', 500)
    
    @action(detail=True, methods=['post'])
    def confirm(self, request, pk=None):
        """确认预约"""
        booking = self.get_object()
        user = request.user
        
        # 检查权限（通常是教练确认）
        if user != booking.coach:
            return Response(
                {'error': '只有教练可以确认预约'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        if booking.status != 'pending':
            return Response(
                {'error': '预约状态不正确'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        booking.status = 'confirmed'
        booking.confirmed_at = timezone.now()
        booking.save()
        
        # 创建通知
        Notification.objects.create(
            recipient=booking.relation.student,
            sender=request.user,
            message=f"您的预约已被教练 {request.user.username} 确认",
            notification_type='booking_confirmed',
            related_object_id=booking.id
        )
        
        return Response({'message': '预约已确认'})
    
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """取消预约"""
        booking = self.get_object()
        user = request.user
        reason = request.data.get('reason', '')
        
        # 检查是否可以取消
        can_cancel, message = booking.can_cancel(user)
        if not can_cancel:
            return Response(
                {'error': message},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        booking.status = 'cancelled'
        booking.cancelled_at = timezone.now()
        booking.cancelled_by = user
        booking.cancel_reason = reason
        booking.save()
        
        # 创建通知
        if user == booking.relation.coach:
            # 教练取消，通知学员
            recipient = booking.relation.student
            message = f"教练 {user.username} 取消了您的预约"
        else:
            # 学员取消，通知教练
            recipient = booking.relation.coach
            message = f"学员 {user.username} 取消了预约"
        
        Notification.objects.create(
            recipient=recipient,
            sender=user,
            message=message,
            notification_type='booking_cancelled',
            related_object_id=booking.id
        )
        
        return Response({'message': '预约已取消'})
    
    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        """完成预约"""
        booking = self.get_object()
        user = request.user
        
        # 检查权限
        if user not in [booking.coach, booking.student]:
            return Response(
                {'error': '只有相关的教练或学员可以标记完成'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        if booking.status != 'confirmed':
            return Response(
                {'error': '只有已确认的预约可以标记完成'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # 检查时间（只能在课程结束后标记完成）
        if timezone.now() < booking.end_time:
            return Response(
                {'error': '课程尚未结束，无法标记完成'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        booking.status = 'completed'
        booking.save()
        
        return Response({'message': '预约已完成'})
    
    @action(detail=False, methods=['get'])
    def my_schedule(self, request):
        """获取我的课表"""
        user = request.user
        
        # 获取日期范围参数
        date_from = request.query_params.get('date_from')
        date_to = request.query_params.get('date_to')
        
        # 如果没有指定日期范围，默认获取本周的课表
        if not date_from or not date_to:
            from datetime import datetime, timedelta
            today = datetime.now().date()
            # 获取本周一
            monday = today - timedelta(days=today.weekday())
            # 获取本周日
            sunday = monday + timedelta(days=6)
            date_from = monday.isoformat()
            date_to = sunday.isoformat()
        
        try:
            from datetime import datetime as dt
            start_date = dt.strptime(date_from, '%Y-%m-%d')
            end_date = dt.strptime(date_to, '%Y-%m-%d')
            # 设置结束日期为当天的23:59:59
            end_date = end_date.replace(hour=23, minute=59, second=59)
        except ValueError:
            return Response(
                {'error': '日期格式不正确，请使用YYYY-MM-DD格式'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # 获取用户的预约记录
        queryset = self.get_queryset().filter(
            start_time__gte=start_date,
            start_time__lte=end_date
        ).order_by('start_time')
        
        serializer = self.get_serializer(queryset, many=True)
        
        return Response({
            'date_from': date_from,
            'date_to': date_to,
            'bookings': serializer.data,
            'total_count': queryset.count()
        })


class BookingCancellationViewSet(viewsets.ModelViewSet):
    """预约取消申请管理"""
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    
    def get_serializer_class(self):
        if self.action == 'create':
            return BookingCancellationCreateSerializer
        return BookingCancellationSerializer
    
    def get_queryset(self):
        user = self.request.user
        queryset = BookingCancellation.objects.all()
        
        if user.user_type == 'coach':
            # 教练可以看到自己相关的取消申请
            queryset = queryset.filter(
                Q(booking__relation__coach=user) |
                Q(requested_by=user)
            )
        elif user.user_type == 'student':
            # 学员只能看到自己的申请
            queryset = queryset.filter(
                Q(booking__relation__student=user) |
                Q(requested_by=user)
            )
        else:
            return BookingCancellation.objects.none()
        
        return queryset.order_by('-created_at')
    
    def create(self, request, *args, **kwargs):
        """创建取消申请"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # 获取预约对象
        booking_id = serializer.validated_data['booking_id']
        booking = Booking.objects.get(id=booking_id)
        
        # 检查权限：只有相关的教练或学员可以申请取消
        if request.user not in [booking.relation.coach, booking.relation.student]:
            return Response(
                {'error': '只有相关的教练或学员可以申请取消'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # 创建取消申请
        cancellation = BookingCancellation.objects.create(
            booking=booking,
            requested_by=request.user,
            reason=serializer.validated_data['reason']
        )
        
        # 返回详细信息
        response_serializer = BookingCancellationSerializer(cancellation)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        """同意取消申请"""
        cancellation = self.get_object()
        user = request.user
        response_message = request.data.get('response_message', '')
        
        # 检查权限（通常是教练处理学员的申请，或管理员处理）
        booking = cancellation.booking
        if user != booking.coach and not user.is_staff:
            return Response(
                {'error': '只有教练或管理员可以处理取消申请'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        if cancellation.status != 'pending':
            return Response(
                {'error': '申请状态不正确'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # 更新取消申请状态
        cancellation.status = 'approved'
        cancellation.processed_by = user
        cancellation.processed_at = timezone.now()
        cancellation.response_message = response_message
        cancellation.save()
        
        # 更新预约状态
        booking.status = 'cancelled'
        booking.cancelled_at = timezone.now()
        booking.cancelled_by = cancellation.requested_by
        booking.cancel_reason = cancellation.reason
        booking.save()
        
        # 创建通知
        Notification.objects.create(
            recipient=cancellation.requested_by,
            sender=user,
            message=f"您的预约取消申请已被 {user.username} 同意",
            notification_type='cancellation_approved',
            related_object_id=cancellation.id
        )
        
        return Response({'message': '取消申请已同意，预约已取消'})
    
    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        """拒绝取消申请"""
        cancellation = self.get_object()
        user = request.user
        response_message = request.data.get('response_message', '')
        
        # 检查权限
        booking = cancellation.booking
        if user != booking.coach and not user.is_staff:
            return Response(
                {'error': '只有教练或管理员可以处理取消申请'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        if cancellation.status != 'pending':
            return Response(
                {'error': '申请状态不正确'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # 更新取消申请状态
        cancellation.status = 'rejected'
        cancellation.processed_by = user
        cancellation.processed_at = timezone.now()
        cancellation.response_message = response_message
        cancellation.save()
        
        # 创建通知
        Notification.objects.create(
            recipient=cancellation.requested_by,
            sender=user,
            message=f"您的预约取消申请已被 {user.username} 拒绝",
            notification_type='cancellation_rejected',
            related_object_id=cancellation.id
        )
        
        return Response({'message': '取消申请已拒绝'})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_coaches(request):
    """获取教练列表"""
    coaches = User.objects.filter(user_type='coach', is_active=True)
    data = [{
        'id': coach.id,
        'real_name': coach.real_name,
        'phone': coach.phone,
        'email': coach.email
    } for coach in coaches]
    
    return Response(data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_students(request):
    """获取学员列表（仅教练可用）"""
    if request.user.user_type != 'coach':
        return Response(
            {'error': '只有教练可以查看学员列表'},
            status=status.HTTP_403_FORBIDDEN
        )
    
    students = User.objects.filter(user_type='student', is_active=True)
    data = [{
        'id': student.id,
        'real_name': student.real_name,
        'phone': student.phone,
        'email': student.email
    } for student in students]
    
    return Response(data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def booking_statistics(request):
    """预约统计"""
    user = request.user
    
    # 基础查询
    if user.user_type == 'coach':
        bookings = Booking.objects.filter(relation__coach=user)
    elif user.user_type == 'student':
        bookings = Booking.objects.filter(relation__student=user)
    else:
        return Response({'error': '权限不足'}, status=status.HTTP_403_FORBIDDEN)
    
    # 统计数据
    total_bookings = bookings.count()
    pending_bookings = bookings.filter(status='pending').count()
    confirmed_bookings = bookings.filter(status='confirmed').count()
    completed_bookings = bookings.filter(status='completed').count()
    cancelled_bookings = bookings.filter(status='cancelled').count()
    
    # 本月统计
    current_month = timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    month_bookings = bookings.filter(created_at__gte=current_month).count()
    month_completed = bookings.filter(
        status='completed',
        created_at__gte=current_month
    ).count()
    
    return Response({
        'total_bookings': total_bookings,
        'pending_bookings': pending_bookings,
        'confirmed_bookings': confirmed_bookings,
        'completed_bookings': completed_bookings,
        'cancelled_bookings': cancelled_bookings,
        'month_bookings': month_bookings,
        'month_completed': month_completed,
    })
