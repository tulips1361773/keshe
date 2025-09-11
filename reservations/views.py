from django.shortcuts import render
from django.utils import timezone
from django.db.models import Q
from rest_framework import status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from datetime import datetime, timedelta

from .models import CoachStudentRelation, Table, Booking, BookingCancellation
from .serializers import (
    CoachStudentRelationSerializer,
    TableSerializer,
    BookingSerializer,
    BookingCancellationSerializer,
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
        
        # 验证师生关系
        relation_id = self.request.data.get('relation_id')
        try:
            relation = CoachStudentRelation.objects.get(
                id=relation_id,
                status='approved'
            )
            if user not in [relation.coach, relation.student]:
                raise ValueError('无权限创建此预约')
        except CoachStudentRelation.DoesNotExist:
            raise ValueError('师生关系不存在或未通过审核')
        
        serializer.save()
    
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
