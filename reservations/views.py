from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.db import transaction, models
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from datetime import datetime

from .models import CoachStudentRelation, Table, Booking
from .coach_change_models import CoachChangeRequest
from .serializers import (
    CoachStudentRelationSerializer, 
    TableSerializer, 
    BookingSerializer,
    CoachChangeRequestSerializer,
    CoachChangeApprovalSerializer
)
from accounts.models import Coach

User = get_user_model()


class CoachStudentRelationListCreateView(generics.ListCreateAPIView):
    """师生关系列表和创建视图"""
    serializer_class = CoachStudentRelationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.user_type == 'coach':
            return CoachStudentRelation.objects.filter(coach=user)
        elif user.user_type == 'student':
            return CoachStudentRelation.objects.filter(student=user)
        else:
            return CoachStudentRelation.objects.none()


class CoachStudentRelationDetailView(generics.RetrieveUpdateDestroyAPIView):
    """师生关系详情视图"""
    serializer_class = CoachStudentRelationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.user_type == 'coach':
            return CoachStudentRelation.objects.filter(coach=user)
        elif user.user_type == 'student':
            return CoachStudentRelation.objects.filter(student=user)
        else:
            return CoachStudentRelation.objects.none()


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def approve_relation(request, relation_id):
    """审批师生关系"""
    try:
        relation = CoachStudentRelation.objects.get(id=relation_id)
    except CoachStudentRelation.DoesNotExist:
        return Response({'error': '师生关系不存在'}, status=status.HTTP_404_NOT_FOUND)
    
    user = request.user
    action = request.data.get('action')  # 'approve' 或 'reject'
    
    # 检查权限
    if user != relation.coach and user != relation.student:
        return Response({'error': '无权限操作此关系'}, status=status.HTTP_403_FORBIDDEN)
    
    if relation.status != 'pending':
        return Response({'error': '该关系已处理'}, status=status.HTTP_400_BAD_REQUEST)
    
    if action == 'approve':
        relation.status = 'approved'
        relation.processed_at = timezone.now()
        message = '师生关系已通过审核'
    elif action == 'reject':
        relation.status = 'rejected'
        relation.processed_at = timezone.now()
        message = '师生关系已拒绝'
    else:
        return Response({'error': '无效的操作'}, status=status.HTTP_400_BAD_REQUEST)
    
    relation.save()
    
    return Response({
        'message': message,
        'relation': CoachStudentRelationSerializer(relation).data
    })


class TableListView(generics.ListAPIView):
    """球台列表视图"""
    queryset = Table.objects.filter(is_active=True)
    serializer_class = TableSerializer
    permission_classes = [permissions.IsAuthenticated]


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def available_tables(request):
    """获取可用球台"""
    try:
        # 获取查询参数
        start_time_str = request.GET.get('start_time')
        end_time_str = request.GET.get('end_time')
        campus_id = request.GET.get('campus_id')
        
        # 验证必需参数
        if not all([start_time_str, end_time_str, campus_id]):
            return Response({
                'error': '缺少必需参数: start_time, end_time, campus_id'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # 解析时间参数
        try:
            # 处理URL编码的时间格式
            start_time_str = start_time_str.replace(' ', '+')
            end_time_str = end_time_str.replace(' ', '+')
            
            # 解析时间
            start_time = datetime.strptime(start_time_str, '%Y-%m-%d+%H:%M:%S')
            end_time = datetime.strptime(end_time_str, '%Y-%m-%d+%H:%M:%S')
        except ValueError:
            return Response({
                'error': '时间格式错误，请使用 YYYY-MM-DD+HH:MM:SS 格式'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # 验证时间逻辑
        if start_time >= end_time:
            return Response({
                'error': '开始时间必须早于结束时间'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # 获取指定校区的所有可用球台
        all_tables = Table.objects.filter(
            campus_id=campus_id,
            is_active=True,
            status='available'
        )
        
        # 查找在指定时间段内有预约的球台
        occupied_table_ids = Booking.objects.filter(
            table__campus_id=campus_id,
            status__in=['pending', 'confirmed'],
            start_time__lt=end_time,
            end_time__gt=start_time
        ).values_list('table_id', flat=True)
        
        # 过滤出可用的球台
        available_tables_queryset = all_tables.exclude(id__in=occupied_table_ids)
        
        # 序列化数据
        serializer = TableSerializer(available_tables_queryset, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'error': f'服务器内部错误: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class BookingListCreateView(generics.ListCreateAPIView):
    """预约列表和创建视图"""
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.user_type == 'coach':
            return Booking.objects.filter(relation__coach=user)
        elif user.user_type == 'student':
            return Booking.objects.filter(relation__student=user)
        else:
            return Booking.objects.none()
    
    def get(self, request, *args, **kwargs):
        """处理GET请求，支持my_schedule端点的日期过滤"""
        # 检查是否是my_schedule端点
        if 'my_schedule' in request.path:
            return self.get_my_schedule(request)
        return super().get(request, *args, **kwargs)
    
    def get_my_schedule(self, request):
        """获取我的课表"""
        from datetime import datetime
        
        # 获取日期参数
        date_from = request.GET.get('date_from')
        date_to = request.GET.get('date_to')
        
        queryset = self.get_queryset()
        
        # 应用日期过滤
        if date_from:
            try:
                date_from_obj = datetime.strptime(date_from, '%Y-%m-%d').date()
                queryset = queryset.filter(start_time__date__gte=date_from_obj)
            except ValueError:
                return Response({'error': '日期格式错误'}, status=400)
        
        if date_to:
            try:
                date_to_obj = datetime.strptime(date_to, '%Y-%m-%d').date()
                queryset = queryset.filter(start_time__date__lte=date_to_obj)
            except ValueError:
                return Response({'error': '日期格式错误'}, status=400)
        
        # 序列化数据
        serializer = self.get_serializer(queryset, many=True)
        return Response({'bookings': serializer.data})


class BookingDetailView(generics.RetrieveUpdateDestroyAPIView):
    """预约详情视图"""
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.user_type == 'coach':
            return Booking.objects.filter(relation__coach=user)
        elif user.user_type == 'student':
            return Booking.objects.filter(relation__student=user)
        else:
            return Booking.objects.none()


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def coach_list(request):
    """获取教练列表"""
    coaches = User.objects.filter(user_type='coach', is_active=True)
    
    coach_data = []
    for coach in coaches:
        try:
            coach_profile = Coach.objects.get(user=coach)
            coach_info = {
                'id': coach.id,
                'username': coach.username,
                'real_name': coach.real_name,
                'phone': coach.phone,
                'email': coach.email,
                'level': coach_profile.coach_level,
                'hourly_rate': coach_profile.hourly_rate,
                'max_students': coach_profile.max_students,
                'current_students': coach_profile.current_students_count,
                'bio': coach_profile.achievements,
                'specialties': None,
                'is_available': True
            }
        except Coach.DoesNotExist:
            coach_info = {
                'id': coach.id,
                'username': coach.username,
                'real_name': coach.real_name,
                'phone': coach.phone,
                'email': coach.email,
                'level': None,
                'hourly_rate': None,
                'max_students': None,
                'current_students': 0,
                'bio': None,
                'specialties': None,
                'is_available': True
            }
        
        coach_data.append(coach_info)
    
    return Response(coach_data)


# ==================== 教练更换相关视图 ====================

@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(csrf_exempt, name='post')
class CoachChangeRequestListCreateView(generics.ListCreateAPIView):
    """教练更换请求列表和创建视图"""
    serializer_class = CoachChangeRequestSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        
        if user.user_type == 'student':
            # 学员只能看到自己的更换请求
            return CoachChangeRequest.objects.filter(student=user)
        elif user.user_type == 'coach':
            # 教练可以看到与自己相关的更换请求（作为当前教练或目标教练）
            return CoachChangeRequest.objects.filter(
                models.Q(current_coach=user) | models.Q(target_coach=user)
            )
        elif user.user_type == 'campus_admin':
            # 校区管理员可以看到所有更换请求
            return CoachChangeRequest.objects.all()
        else:
            return CoachChangeRequest.objects.none()
    
    def perform_create(self, serializer):
        """创建教练更换请求"""
        serializer.save()


class CoachChangeRequestDetailView(generics.RetrieveAPIView):
    """教练更换请求详情视图"""
    serializer_class = CoachChangeRequestSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        
        if user.user_type == 'student':
            return CoachChangeRequest.objects.filter(student=user)
        elif user.user_type == 'coach':
            return CoachChangeRequest.objects.filter(
                models.Q(current_coach=user) | models.Q(target_coach=user)
            )
        elif user.user_type == 'campus_admin':
            return CoachChangeRequest.objects.all()
        else:
            return CoachChangeRequest.objects.none()


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def approve_coach_change(request, request_id):
    """审批教练更换请求"""
    try:
        coach_change_request = CoachChangeRequest.objects.get(id=request_id)
    except CoachChangeRequest.DoesNotExist:
        return Response({'error': '教练更换请求不存在'}, status=status.HTTP_404_NOT_FOUND)
    
    # 创建审批序列化器
    serializer = CoachChangeApprovalSerializer(
        data=request.data,
        context={
            'request': request,
            'coach_change_request': coach_change_request
        }
    )
    
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    action = serializer.validated_data['action']
    notes = serializer.validated_data.get('notes', '')
    user = request.user
    
    with transaction.atomic():
        # 根据用户身份进行审批
        if user == coach_change_request.current_coach:
            # 当前教练审批
            if action == 'approve':
                coach_change_request.current_coach_approval = 'approved'
            else:
                coach_change_request.current_coach_approval = 'rejected'
            
            coach_change_request.current_coach_approved_by = user
            coach_change_request.current_coach_approved_at = timezone.now()
            coach_change_request.current_coach_notes = notes
            
        elif user == coach_change_request.target_coach:
            # 目标教练审批
            if action == 'approve':
                coach_change_request.target_coach_approval = 'approved'
            else:
                coach_change_request.target_coach_approval = 'rejected'
            
            coach_change_request.target_coach_approved_by = user
            coach_change_request.target_coach_approved_at = timezone.now()
            coach_change_request.target_coach_notes = notes
            
        elif user.user_type == 'campus_admin':
            # 校区管理员审批
            if action == 'approve':
                coach_change_request.campus_admin_approval = 'approved'
            else:
                coach_change_request.campus_admin_approval = 'rejected'
            
            coach_change_request.campus_admin_approved_by = user
            coach_change_request.campus_admin_approved_at = timezone.now()
            coach_change_request.campus_admin_notes = notes
        
        # 检查是否所有审批都完成
        if coach_change_request.has_rejection:
            # 有拒绝，直接设为拒绝状态
            coach_change_request.status = 'rejected'
            coach_change_request.processed_at = timezone.now()
            coach_change_request.processed_by = user
            
        elif coach_change_request.is_all_approved:
            # 所有审批都通过，执行教练更换
            coach_change_request.status = 'approved'
            coach_change_request.processed_at = timezone.now()
            coach_change_request.processed_by = user
            
            # 执行教练更换逻辑
            coach_change_request.execute_coach_change()
        
        coach_change_request.save()
    
    # 返回更新后的请求信息
    response_serializer = CoachChangeRequestSerializer(coach_change_request)
    
    return Response({
        'message': f'审批成功：{action}',
        'request': response_serializer.data
    })


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def my_coach_change_requests(request):
    """获取我的教练更换请求"""
    user = request.user
    
    if user.user_type != 'student':
        return Response({'error': '只有学员可以查看自己的更换请求'}, status=status.HTTP_403_FORBIDDEN)
    
    requests = CoachChangeRequest.objects.filter(student=user).order_by('-created_at')
    serializer = CoachChangeRequestSerializer(requests, many=True)
    
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def pending_coach_change_approvals(request):
    """获取待我审批的教练更换请求"""
    user = request.user
    
    if user.user_type == 'coach':
        # 教练查看待审批的请求
        requests = CoachChangeRequest.objects.filter(
            models.Q(current_coach=user, current_coach_approval='pending') |
            models.Q(target_coach=user, target_coach_approval='pending'),
            status='pending'
        ).order_by('-created_at')
        
    elif user.user_type == 'campus_admin':
        # 校区管理员查看待审批的请求
        requests = CoachChangeRequest.objects.filter(
            campus_admin_approval='pending',
            status='pending'
        ).order_by('-created_at')
        
    else:
        return Response({'error': '无权限查看审批列表'}, status=status.HTTP_403_FORBIDDEN)
    
    serializer = CoachChangeRequestSerializer(requests, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def coach_change_statistics(request):
    """获取教练更换统计信息"""
    user = request.user
    
    if user.user_type == 'campus_admin':
        # 管理员可以查看全部统计
        total_requests = CoachChangeRequest.objects.count()
        pending_requests = CoachChangeRequest.objects.filter(status='pending').count()
        approved_requests = CoachChangeRequest.objects.filter(status='approved').count()
        rejected_requests = CoachChangeRequest.objects.filter(status='rejected').count()
        
    elif user.user_type == 'coach':
        # 教练查看与自己相关的统计
        related_requests = CoachChangeRequest.objects.filter(
            models.Q(current_coach=user) | models.Q(target_coach=user)
        )
        total_requests = related_requests.count()
        pending_requests = related_requests.filter(status='pending').count()
        approved_requests = related_requests.filter(status='approved').count()
        rejected_requests = related_requests.filter(status='rejected').count()
        
    elif user.user_type == 'student':
        # 学员查看自己的统计
        my_requests = CoachChangeRequest.objects.filter(student=user)
        total_requests = my_requests.count()
        pending_requests = my_requests.filter(status='pending').count()
        approved_requests = my_requests.filter(status='approved').count()
        rejected_requests = my_requests.filter(status='rejected').count()
        
    else:
        return Response({'error': '无权限查看统计信息'}, status=status.HTTP_403_FORBIDDEN)
    
    return Response({
        'total_requests': total_requests,
        'pending_requests': pending_requests,
        'approved_requests': approved_requests,
        'rejected_requests': rejected_requests,
        'approval_rate': round(approved_requests / total_requests * 100, 2) if total_requests > 0 else 0
    })
