from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from logs.utils import log_user_action
from django.db import transaction, models
from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, timedelta
from django.utils import timezone
from .models import CoachStudentRelation, Table, Booking, CoachChangeRequest
from .serializers import (
    CoachStudentRelationSerializer, 
    TableSerializer, 
    BookingSerializer, 
    CoachChangeRequestSerializer,
    CoachChangeApprovalSerializer
)
from payments.models import UserAccount, AccountTransaction
from notifications.models import Notification

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
        notification_title = "师生关系申请通过"
        notification_message = f"恭喜！教练 {relation.coach.real_name or relation.coach.username} 已同意您的申请。"
    elif action == 'reject':
        relation.status = 'rejected'
        relation.processed_at = timezone.now()
        message = '师生关系已拒绝'
        notification_title = "师生关系申请被拒绝"
        notification_message = f"很抱歉，教练 {relation.coach.real_name or relation.coach.username} 拒绝了您的申请。"
    else:
        return Response({'error': '无效的操作'}, status=status.HTTP_400_BAD_REQUEST)
    
    relation.save()
    
    # 发送通知给学员
    from notifications.models import Notification
    try:
        Notification.create_notification(
            recipient=relation.student,
            sender=relation.coach,
            title=notification_title,
            message=notification_message,
            message_type="system",
            data={
                'relation_id': relation.id,
                'coach_id': relation.coach.id,
                'coach_name': relation.coach.real_name or relation.coach.username,
                'action': 'relation_' + action,
                'status': relation.status
            }
        )
    except Exception as e:
        # 通知发送失败不应影响主要业务逻辑
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Failed to send notification to student {relation.student.id}: {str(e)}")
    
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
            return Booking.objects.filter(relation__coach=user).select_related(
                'relation__coach', 'relation__student', 'table__campus', 'cancellation'
            )
        elif user.user_type == 'student':
            return Booking.objects.filter(relation__student=user).select_related(
                'relation__coach', 'relation__student', 'table__campus', 'cancellation'
            )
        else:
            return Booking.objects.none()
    
    def create(self, request, *args, **kwargs):
        """创建预约，包含余额检查"""
        try:
            with transaction.atomic():
                # 获取学员账户（只有学员可以创建预约）
                if request.user.user_type != 'student':
                    return Response({
                        'error': '只有学员可以创建预约'
                    }, status=status.HTTP_403_FORBIDDEN)
                
                # 获取或创建学员账户
                student_account, created = UserAccount.objects.get_or_create(
                    user=request.user,
                    defaults={'balance': 0.00}
                )
                
                # 获取预约费用
                total_fee = float(request.data.get('total_fee', 0))
                if total_fee <= 0:
                    return Response({
                        'error': '预约费用必须大于0'
                    }, status=status.HTTP_400_BAD_REQUEST)
                
                # 检查账户余额
                if student_account.balance < total_fee:
                    return Response({
                        'error': f'账户余额不足。当前余额：¥{student_account.balance:.2f}，需要：¥{total_fee:.2f}，请先充值'
                    }, status=status.HTTP_400_BAD_REQUEST)
                
                # 创建预约
                serializer = self.get_serializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                booking = serializer.save()
                
                # 预约创建成功，但费用暂不扣除（等待教练确认）
                return Response({
                    'message': '预约创建成功，等待教练确认',
                    'booking': serializer.data
                }, status=status.HTTP_201_CREATED)
                
        except Exception as e:
            return Response({
                'error': f'创建预约失败: {str(e)}'
            }, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request, *args, **kwargs):
        """处理GET请求，支持my_schedule端点的日期过滤"""
        # 检查是否是my_schedule端点
        if 'my_schedule' in request.path:
            return self.get_my_schedule(request)
        return super().get(request, *args, **kwargs)
    
    def get_my_schedule(self, request):
        """获取我的课表"""
        from datetime import datetime, time
        from django.utils import timezone
        
        # 获取日期参数
        date_from = request.GET.get('date_from')
        date_to = request.GET.get('date_to')
        
        queryset = self.get_queryset()
        
        # 应用日期过滤 - 使用时间范围而不是日期过滤
        if date_from:
            try:
                date_from_obj = datetime.strptime(date_from, '%Y-%m-%d').date()
                # 转换为当天开始时间
                start_datetime = timezone.make_aware(
                    datetime.combine(date_from_obj, time.min)
                )
                queryset = queryset.filter(start_time__gte=start_datetime)
            except ValueError:
                return Response({'error': '日期格式错误'}, status=400)
        
        if date_to:
            try:
                date_to_obj = datetime.strptime(date_to, '%Y-%m-%d').date()
                # 转换为当天结束时间
                end_datetime = timezone.make_aware(
                    datetime.combine(date_to_obj, time.max)
                )
                queryset = queryset.filter(start_time__lte=end_datetime)
            except ValueError:
                return Response({'error': '日期格式错误'}, status=400)
        
        # 序列化数据
        serializer = self.get_serializer(queryset, many=True)
        return Response({'bookings': serializer.data})


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def confirm_booking(request, booking_id):
    """教练确认预约并扣除学员费用"""
    try:
        with transaction.atomic():
            # 获取预约
            booking = get_object_or_404(Booking, id=booking_id)
            
            # 权限检查：只有教练可以确认预约
            if request.user.user_type != 'coach':
                return Response({
                    'error': '只有教练可以确认预约'
                }, status=status.HTTP_403_FORBIDDEN)
            
            # 检查是否是该教练的预约
            if booking.relation.coach != request.user:
                return Response({
                    'error': '您只能确认自己的预约'
                }, status=status.HTTP_403_FORBIDDEN)
            
            # 检查预约状态
            if booking.status != 'pending':
                return Response({
                    'error': f'预约状态不允许确认，当前状态：{booking.get_status_display()}'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # 获取学员账户
            student = booking.relation.student
            try:
                student_account = UserAccount.objects.get(user=student)
            except UserAccount.DoesNotExist:
                return Response({
                    'error': '学员账户不存在'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # 再次检查余额（防止并发问题）
            if student_account.balance < booking.total_fee:
                return Response({
                    'error': f'学员账户余额不足。当前余额：¥{student_account.balance:.2f}，需要：¥{booking.total_fee:.2f}'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # 扣除费用
            student_account.balance -= booking.total_fee
            student_account.save()
            
            # 获取教练账户并增加收入
            coach = booking.relation.coach
            try:
                coach_account = UserAccount.objects.get(user=coach)
            except UserAccount.DoesNotExist:
                # 如果教练账户不存在，创建一个
                coach_account = UserAccount.objects.create(user=coach)
            
            # 增加教练账户余额
            coach_account.balance += booking.total_fee
            coach_account.save()
            
            # 创建学员支付交易记录
            AccountTransaction.objects.create(
                account=student_account,
                transaction_type='payment',
                amount=booking.total_fee,
                balance_before=student_account.balance + booking.total_fee,
                balance_after=student_account.balance,
                description=f'预约课程费用 - 教练：{booking.relation.coach.real_name}，时间：{booking.start_time.strftime("%Y-%m-%d %H:%M")}'
            )
            
            # 创建教练收入交易记录
            AccountTransaction.objects.create(
                account=coach_account,
                transaction_type='income',
                amount=booking.total_fee,
                balance_before=coach_account.balance - booking.total_fee,
                balance_after=coach_account.balance,
                description=f'课程收入 - 学员：{booking.relation.student.real_name}，时间：{booking.start_time.strftime("%Y-%m-%d %H:%M")}'
            )
            
            # 更新预约状态
            booking.status = 'confirmed'
            booking.payment_status = 'paid'
            booking.save()
            
            # 发送通知给学员
            from notifications.models import Notification
            try:
                Notification.create_notification(
                    recipient=student,
                    sender=request.user,
                    title="预约已确认",
                    message=f"您的预约已被教练 {request.user.real_name or request.user.username} 确认，费用 ¥{booking.total_fee:.2f} 已扣除。",
                    message_type="booking",
                    data={
                        'booking_id': booking.id,
                        'coach_id': request.user.id,
                        'coach_name': request.user.real_name or request.user.username,
                        'amount': float(booking.total_fee),
                        'start_time': booking.start_time.isoformat(),
                        'end_time': booking.end_time.isoformat(),
                        'action': 'booking_confirmed'
                    }
                )
            except Exception as e:
                # 通知发送失败不应影响主要业务逻辑
                import logging
                logger = logging.getLogger(__name__)
                logger.error(f"Failed to send booking confirmation notification to student {student.id}: {str(e)}")
            
            # 记录操作日志
            log_user_action(
                user=request.user,
                action_type='confirm',
                resource_type='booking',
                resource_id=booking.id,
                resource_name=f"预约 {booking.id}",
                description=f"确认了与学员 {student.real_name} 的预约，获得收入 ¥{booking.total_fee}",
                request=request,
                extra_data={
                    'student_id': student.id,
                    'student_name': student.real_name,
                    'amount': float(booking.total_fee),
                    'student_balance_after': float(student_account.balance),
                    'coach_balance_after': float(coach_account.balance),
                    'start_time': booking.start_time.isoformat(),
                    'end_time': booking.end_time.isoformat()
                }
            )
            
            # 返回成功响应
            serializer = BookingSerializer(booking)
            return Response({
                'message': '预约确认成功，费用已扣除，收入已到账',
                'booking': serializer.data,
                'student_balance': float(student_account.balance),
                'coach_balance': float(coach_account.balance)
            }, status=status.HTTP_200_OK)
            
    except Exception as e:
        return Response({
            'error': f'确认预约失败: {str(e)}'
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def reject_booking(request, booking_id):
    """教练拒绝预约"""
    try:
        with transaction.atomic():
            # 获取预约
            booking = get_object_or_404(Booking, id=booking_id)
            
            # 权限检查：只有教练可以拒绝预约
            if request.user.user_type != 'coach':
                return Response({
                    'error': '只有教练可以拒绝预约'
                }, status=status.HTTP_403_FORBIDDEN)
            
            # 检查是否是该教练的预约
            if booking.relation.coach != request.user:
                return Response({
                    'error': '您只能拒绝自己的预约'
                }, status=status.HTTP_403_FORBIDDEN)
            
            # 检查预约状态
            if booking.status != 'pending':
                return Response({
                    'error': f'预约状态不允许拒绝，当前状态：{booking.get_status_display()}'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # 获取拒绝原因
            reason = request.data.get('reason', '教练拒绝了预约')
            
            # 更新预约状态
            booking.status = 'cancelled'
            booking.cancelled_at = timezone.now()
            booking.cancelled_by = request.user
            booking.cancel_reason = reason
            booking.save()
            
            # 发送通知给学员
            from notifications.models import Notification
            try:
                Notification.create_notification(
                    recipient=booking.relation.student,
                    sender=request.user,
                    title="预约被拒绝",
                    message=f"很抱歉，教练 {request.user.real_name or request.user.username} 拒绝了您的预约申请。原因：{reason}",
                    message_type="booking",
                    data={
                        'booking_id': booking.id,
                        'coach_id': request.user.id,
                        'coach_name': request.user.real_name or request.user.username,
                        'reason': reason,
                        'start_time': booking.start_time.isoformat(),
                        'end_time': booking.end_time.isoformat(),
                        'action': 'booking_rejected'
                    }
                )
            except Exception as e:
                # 通知发送失败不应影响主要业务逻辑
                import logging
                logger = logging.getLogger(__name__)
                logger.error(f"Failed to send booking rejection notification to student {booking.relation.student.id}: {str(e)}")
            
            # 记录操作日志
            log_user_action(
                user=request.user,
                action_type='reject',
                resource_type='booking',
                resource_id=booking.id,
                resource_name=f"预约 {booking.id}",
                description=f"拒绝了学员 {booking.relation.student.real_name} 的预约申请",
                request=request,
                extra_data={
                    'student_id': booking.relation.student.id,
                    'student_name': booking.relation.student.real_name,
                    'reason': reason,
                    'start_time': booking.start_time.isoformat(),
                    'end_time': booking.end_time.isoformat()
                }
            )
            
            return Response({
                'message': '预约已拒绝',
                'booking_id': booking.id,
                'status': 'cancelled',
                'reason': reason
            }, status=status.HTTP_200_OK)
            
    except Exception as e:
        return Response({
            'error': f'拒绝预约失败: {str(e)}'
        }, status=status.HTTP_400_BAD_REQUEST)


class BookingDetailView(generics.RetrieveUpdateDestroyAPIView):
    """预约详情视图"""
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.user_type == 'student':
            return Booking.objects.filter(relation__student=user)
        elif user.user_type == 'coach':
            return Booking.objects.filter(relation__coach=user)
        return Booking.objects.none()
    
    def post(self, request, *args, **kwargs):
        """处理POST请求的取消预约"""
        return self.cancel_booking(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        """取消预约并处理退费"""
        return self.cancel_booking(request, *args, **kwargs)
    
    def cancel_booking(self, request, *args, **kwargs):
        """创建取消申请的方法"""
        try:
            with transaction.atomic():
                booking = self.get_object()
                
                # 检查预约状态
                if booking.status == 'cancelled':
                    return Response({
                        'error': '预约已经被取消'
                    }, status=status.HTTP_400_BAD_REQUEST)
                
                # 检查是否已有待处理的取消申请
                from .models import BookingCancellation
                if BookingCancellation.objects.filter(booking=booking, status='pending').exists():
                    return Response({
                        'error': '已有待处理的取消申请'
                    }, status=status.HTTP_400_BAD_REQUEST)
                
                # 检查是否可以取消（传入用户参数）
                can_cancel, reason = booking.can_cancel(request.user)
                if not can_cancel:
                    return Response({
                        'error': reason
                    }, status=status.HTTP_400_BAD_REQUEST)
                
                # 创建取消申请
                cancellation = BookingCancellation.objects.create(
                    booking=booking,
                    requested_by=request.user,
                    reason=request.data.get('reason', ''),
                    status='pending'
                )
                
                # 更新预约状态为待审核取消
                booking.status = 'pending_cancellation'
                booking.save()
                
                return Response({
                    'message': '取消申请已提交，等待教练审核',
                    'cancellation_id': cancellation.id,
                    'status': 'pending_cancellation'
                }, status=status.HTTP_201_CREATED)
                
        except Exception as e:
            return Response({
                'error': f'提交取消申请失败: {str(e)}'
            }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def complete_booking(request, booking_id):
    """完成预约"""
    try:
        with transaction.atomic():
            # 获取预约
            booking = get_object_or_404(Booking, id=booking_id)
            
            # 权限检查：只有教练可以完成预约
            if request.user.user_type != 'coach':
                return Response({
                    'error': '只有教练可以完成预约'
                }, status=status.HTTP_403_FORBIDDEN)
            
            # 检查是否是该教练的预约
            if booking.relation.coach != request.user:
                return Response({
                    'error': '您只能完成自己的预约'
                }, status=status.HTTP_403_FORBIDDEN)
            
            # 检查预约状态
            if booking.status != 'confirmed':
                return Response({
                    'error': f'预约状态不允许完成，当前状态：{booking.get_status_display()}'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # 更新预约状态为已完成
            booking.status = 'completed'
            booking.save()
            
            # 返回成功响应
            serializer = BookingSerializer(booking)
            return Response({
                'message': '预约已完成',
                'booking': serializer.data
            }, status=status.HTTP_200_OK)
            
    except Exception as e:
        return Response({
            'error': f'完成预约失败: {str(e)}'
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def approve_cancellation(request, cancellation_id):
    """审核取消申请（支持双向审核）"""
    try:
        from .models import BookingCancellation
        from payments.models import UserAccount, AccountTransaction
        
        # 获取取消申请
        try:
            cancellation = BookingCancellation.objects.get(id=cancellation_id)
        except BookingCancellation.DoesNotExist:
            return Response({
                'error': '取消申请不存在'
            }, status=status.HTTP_404_NOT_FOUND)
        
        booking = cancellation.booking
        
        # 检查权限：只有对方可以审核取消申请
        if cancellation.requested_by == request.user:
            return Response({
                'error': '不能审核自己的取消申请'
            }, status=status.HTTP_403_FORBIDDEN)
        
        # 教练只能审核学员的取消申请，学员只能审核教练的取消申请
        if request.user.user_type == 'coach':
            if booking.relation.coach != request.user or cancellation.requested_by.user_type != 'student':
                return Response({
                    'error': '只能审核自己学员的取消申请'
                }, status=status.HTTP_403_FORBIDDEN)
        elif request.user.user_type == 'student':
            if booking.relation.student != request.user or cancellation.requested_by.user_type != 'coach':
                return Response({
                    'error': '只能审核自己教练的取消申请'
                }, status=status.HTTP_403_FORBIDDEN)
        else:
            return Response({
                'error': '权限不足'
            }, status=status.HTTP_403_FORBIDDEN)
        
        # 检查申请状态
        if cancellation.status != 'pending':
            return Response({
                'error': '该申请已经被处理过了'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        with transaction.atomic():
            # 在事务内部再次检查预约状态，确保数据一致性
            # 允许 pending_cancellation 状态，因为这表示已有待处理的取消申请
            if booking.status not in ['confirmed', 'pending', 'pending_cancellation']:
                return Response({
                    'error': '预约状态不允许取消'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # 获取审核结果
            action = request.data.get('action')  # 'approve' 或 'reject'
            response_message = request.data.get('comment', '')
            
            if action == 'approve':
                # 批准取消申请
                
                # 处理退款逻辑（在状态更新之前处理）
                refund_processed = False
                
                # 检查是否需要退款：
                # 1. 预约支付状态为 'paid'
                # 2. 或者存在支付交易记录但预约状态未更新（数据不一致情况）
                should_refund = False
                
                if booking.payment_status == 'paid':
                    should_refund = True
                elif booking.payment_status in ['unpaid', 'pending']:
                    # 检查是否存在实际的支付交易记录
                    from payments.models import Payment
                    payment_exists = Payment.objects.filter(
                        booking_id=booking.id,
                        status='approved'
                    ).exists()
                    
                    if payment_exists:
                        should_refund = True
                        print(f"发现数据不一致：预约{booking.id}存在已批准的支付记录但payment_status为{booking.payment_status}")
                
                if should_refund:
                    # 处理学员退款
                    student_account = UserAccount.objects.get(user=booking.relation.student)
                    
                    # 直接退还金额到账户余额
                    # 注意：对于已确认的预约，金额已经从冻结转为实际扣费，所以只需要增加余额
                    student_account.balance += booking.total_fee
                    student_account.save()
                    
                    # 创建学员退款交易记录
                    AccountTransaction.objects.create(
                        account=student_account,
                        transaction_type='refund',
                        amount=booking.total_fee,
                        balance_before=student_account.balance - booking.total_fee,
                        balance_after=student_account.balance,
                        description=f'预约取消退款 - 预约ID: {booking.id}'
                    )
                    
                    # 处理教练收入扣除
                    coach_account = UserAccount.objects.get(user=booking.relation.coach)
                    
                    # 从教练账户扣除收入
                    coach_account.balance -= booking.total_fee
                    coach_account.save()
                    
                    # 创建教练收入扣除交易记录
                    AccountTransaction.objects.create(
                        account=coach_account,
                        transaction_type='refund',
                        amount=-booking.total_fee,  # 负数表示扣除
                        balance_before=coach_account.balance + booking.total_fee,
                        balance_after=coach_account.balance,
                        description=f'预约取消收入扣除 - 预约ID: {booking.id}'
                    )
                    
                    # 更新预约支付状态
                    booking.payment_status = 'refunded'
                    refund_processed = True
                
                # 更新取消申请状态
                cancellation.status = 'approved'
                cancellation.processed_by = request.user
                cancellation.processed_at = timezone.now()
                cancellation.response_message = response_message
                cancellation.save()
                
                # 更新预约状态为已取消
                booking.status = 'cancelled'
                booking.cancelled_at = timezone.now()
                booking.cancelled_by = request.user
                booking.save()
                
                # 记录操作日志
                log_user_action(
                    user=request.user,
                    action_type='approve',
                    resource_type='booking',
                    resource_id=booking.id,
                    resource_name=f"预约取消申请",
                    description=f"批准了{cancellation.requested_by.real_name}的预约取消申请，预约ID: {booking.id}",
                    request=request,
                    extra_data={
                        'cancellation_id': cancellation.id,
                        'refund_processed': refund_processed,
                        'refund_amount': float(booking.total_fee) if refund_processed else 0.0
                    }
                )
                
                # 发送通知给申请人
                from notifications.models import Notification
                try:
                    Notification.create_notification(
                        recipient=cancellation.requested_by,
                        sender=request.user,
                        title="取消申请已批准",
                        message=f"您的预约取消申请已被批准。{f'退款 ¥{booking.total_fee:.2f} 已到账。' if refund_processed else ''}",
                        message_type="booking",
                        data={
                            'booking_id': booking.id,
                            'cancellation_id': cancellation.id,
                            'refund_processed': refund_processed,
                            'refund_amount': float(booking.total_fee) if refund_processed else 0.0,
                            'action': 'cancellation_approved'
                        }
                    )
                except Exception as e:
                    # 通知发送失败不应影响主要业务逻辑
                    import logging
                    logger = logging.getLogger(__name__)
                    logger.error(f"Failed to send cancellation approval notification to user {cancellation.requested_by.id}: {str(e)}")
                
                return Response({
                    'message': '取消申请已批准，预约已取消',
                    'refund_processed': refund_processed,
                    'refund_amount': float(booking.total_fee) if refund_processed else 0.0
                }, status=status.HTTP_200_OK)
                
            elif action == 'reject':
                # 拒绝取消申请
                
                # 更新取消申请状态
                cancellation.status = 'rejected'
                cancellation.processed_by = request.user
                cancellation.processed_at = timezone.now()
                cancellation.response_message = response_message
                cancellation.save()
                
                # 记录操作日志
                log_user_action(
                    user=request.user,
                    action_type='reject',
                    resource_type='booking',
                    resource_id=booking.id,
                    resource_name=f"预约取消申请",
                    description=f"拒绝了{cancellation.requested_by.real_name}的预约取消申请，预约ID: {booking.id}",
                    request=request,
                    extra_data={
                        'cancellation_id': cancellation.id,
                        'reason': response_message
                    }
                )
                
                # 发送通知给申请人
                from notifications.models import Notification
                try:
                    Notification.create_notification(
                        recipient=cancellation.requested_by,
                        sender=request.user,
                        title="取消申请被拒绝",
                        message=f"很抱歉，您的预约取消申请被拒绝。{f'原因：{response_message}' if response_message else ''}",
                        message_type="booking",
                        data={
                            'booking_id': booking.id,
                            'cancellation_id': cancellation.id,
                            'reason': response_message,
                            'action': 'cancellation_rejected'
                        }
                    )
                except Exception as e:
                    # 通知发送失败不应影响主要业务逻辑
                    import logging
                    logger = logging.getLogger(__name__)
                    logger.error(f"Failed to send cancellation rejection notification to user {cancellation.requested_by.id}: {str(e)}")
                
                return Response({
                    'message': '取消申请已拒绝'
                }, status=status.HTTP_200_OK)
                
            else:
                return Response({
                    'error': '无效的操作，请选择 approve 或 reject'
                }, status=status.HTTP_400_BAD_REQUEST)
                
    except Exception as e:
        return Response({
            'error': f'处理取消申请失败: {str(e)}'
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def pending_cancellations(request):
    """获取待审核的取消申请列表（教练用）"""
    try:
        from .models import BookingCancellation
        
        # 检查权限：只有教练可以查看
        if not hasattr(request.user, 'coach_profile'):
            return Response({
                'error': '只有教练可以查看待审核的取消申请'
            }, status=status.HTTP_403_FORBIDDEN)
        
        # 获取该教练的待审核取消申请
        cancellations = BookingCancellation.objects.filter(
            booking__relation__coach__user=request.user,
            status='pending'
        ).select_related(
            'booking__relation__student',
            'booking__relation__coach',
            'requested_by'
        ).order_by('-created_at')
        
        cancellation_list = []
        for cancellation in cancellations:
            booking = cancellation.booking
            cancellation_list.append({
                'id': cancellation.id,
                'booking_id': booking.id,
                'student_name': booking.relation.student.real_name,
                'start_time': booking.start_time.strftime('%Y-%m-%d %H:%M'),
                'end_time': booking.end_time.strftime('%Y-%m-%d %H:%M'),
                'total_fee': float(booking.total_fee),
                'payment_status': booking.payment_status,
                'reason': cancellation.reason,
                'requested_at': cancellation.created_at.strftime('%Y-%m-%d %H:%M'),
                'requested_by': cancellation.requested_by.real_name
            })
        
        return Response({
            'cancellations': cancellation_list,
            'count': len(cancellation_list)
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'error': f'获取待审核取消申请失败: {str(e)}'
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def cancel_stats(request):
    """获取用户的取消统计信息"""
    user = request.user
    
    # 获取当前月份的开始时间
    current_month = timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    
    # 统计本月取消次数
    from django.db.models import Q
    monthly_cancel_count = Booking.objects.filter(
        Q(relation__coach=user) | Q(relation__student=user),
        cancelled_at__gte=current_month,
        cancelled_by=user
    ).count()
    
    # 最大取消次数限制
    max_monthly_cancels = 3
    
    # 是否还能取消
    can_cancel_more = monthly_cancel_count < max_monthly_cancels
    
    return Response({
        'monthly_cancel_count': monthly_cancel_count,
        'max_monthly_cancels': max_monthly_cancels,
        'can_cancel_more': can_cancel_more,
        'remaining_cancels': max_monthly_cancels - monthly_cancel_count
    })

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def coach_list(request):
    """获取教练列表"""
    try:
        from accounts.models import Coach
        
        coaches = User.objects.filter(user_type='coach', is_active=True)
        
        coach_data = []
        for coach in coaches:
            try:
                coach_profile = Coach.objects.get(user=coach)
                # 安全地获取current_students_count
                try:
                    current_students = coach_profile.current_students_count
                except Exception as e:
                    print(f"获取教练 {coach.real_name} 的学员数量失败: {e}")
                    current_students = 0
                
                coach_info = {
                    'id': coach.id,
                    'username': coach.username,
                    'real_name': coach.real_name,
                    'phone': coach.phone,
                    'email': coach.email,
                    'level': coach_profile.coach_level,
                    'hourly_rate': float(coach_profile.hourly_rate) if coach_profile.hourly_rate else 0.0,
                    'max_students': coach_profile.max_students,
                    'current_students': current_students,
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
                    'hourly_rate': 0.0,
                    'max_students': None,
                    'current_students': 0,
                    'bio': None,
                    'specialties': None,
                    'is_available': True
                }
            except Exception as e:
                print(f"处理教练 {coach.real_name} 信息时出错: {e}")
                continue
            
            coach_data.append(coach_info)
        
        return Response(coach_data)
        
    except Exception as e:
        print(f"获取教练列表失败: {e}")
        return Response({
            'error': f'获取教练列表失败: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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
        coach_change_request = serializer.save()
        
        # 发送通知给相关人员
        try:
            # 通知当前教练
            Notification.create_notification(
                recipient=coach_change_request.current_coach,
                sender=coach_change_request.student,
                title="教练更换申请",
                message=f"学员 {coach_change_request.student.real_name or coach_change_request.student.username} 申请更换教练，目标教练：{coach_change_request.target_coach.real_name or coach_change_request.target_coach.username}",
                message_type="system",
                data={
                    'request_id': coach_change_request.id,
                    'student_name': coach_change_request.student.real_name or coach_change_request.student.username,
                    'target_coach_name': coach_change_request.target_coach.real_name or coach_change_request.target_coach.username,
                    'reason': coach_change_request.reason
                }
            )
            
            # 通知目标教练
            Notification.create_notification(
                recipient=coach_change_request.target_coach,
                sender=coach_change_request.student,
                title="教练更换申请",
                message=f"学员 {coach_change_request.student.real_name or coach_change_request.student.username} 申请将您设为新教练，当前教练：{coach_change_request.current_coach.real_name or coach_change_request.current_coach.username}",
                message_type="system",
                data={
                    'request_id': coach_change_request.id,
                    'student_name': coach_change_request.student.real_name or coach_change_request.student.username,
                    'current_coach_name': coach_change_request.current_coach.real_name or coach_change_request.current_coach.username,
                    'reason': coach_change_request.reason
                }
            )
            
            # 通知校区管理员
            campus_admins = User.objects.filter(user_type='campus_admin')
            for admin in campus_admins:
                Notification.create_notification(
                    recipient=admin,
                    sender=coach_change_request.student,
                    title="教练更换申请待审核",
                    message=f"学员 {coach_change_request.student.real_name or coach_change_request.student.username} 申请更换教练，从 {coach_change_request.current_coach.real_name or coach_change_request.current_coach.username} 更换到 {coach_change_request.target_coach.real_name or coach_change_request.target_coach.username}",
                    message_type="system",
                    data={
                        'request_id': coach_change_request.id,
                        'student_name': coach_change_request.student.real_name or coach_change_request.student.username,
                        'current_coach_name': coach_change_request.current_coach.real_name or coach_change_request.current_coach.username,
                        'target_coach_name': coach_change_request.target_coach.real_name or coach_change_request.target_coach.username,
                        'reason': coach_change_request.reason
                    }
                )
        except Exception as e:
            # 通知发送失败不影响主流程
            print(f"发送教练更换申请通知失败: {e}")
        
        return coach_change_request


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
    
    user = request.user
    
    # 严格的权限验证
    has_permission = False
    approval_type = None
    
    # 检查用户是否有权限审批此请求
    if user == coach_change_request.current_coach and user.user_type == 'coach':
        # 当前教练审批 - 验证是否真的是当前教练
        if coach_change_request.current_coach_approval == 'pending':
            has_permission = True
            approval_type = 'current_coach'
        else:
            return Response({'error': '您已经审批过此请求'}, status=status.HTTP_400_BAD_REQUEST)
            
    elif user == coach_change_request.target_coach and user.user_type == 'coach':
        # 目标教练审批 - 验证是否真的是目标教练
        if coach_change_request.target_coach_approval == 'pending':
            has_permission = True
            approval_type = 'target_coach'
        else:
            return Response({'error': '您已经审批过此请求'}, status=status.HTTP_400_BAD_REQUEST)
            
    elif user.user_type == 'campus_admin' or user.is_superuser:
        # 校区管理员或超级管理员审批
        from campus.models import CampusStudent
        try:
            student_campus = CampusStudent.objects.get(student=coach_change_request.student).campus
            # 超级管理员可以审批所有申请，校区管理员只能审批本校区的申请
            if user.is_superuser or user == student_campus.manager:
                if coach_change_request.campus_admin_approval == 'pending':
                    has_permission = True
                    approval_type = 'campus_admin'
                else:
                    return Response({'error': '您已经审批过此请求'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'error': '您只能审批本校区学员的请求'}, status=status.HTTP_403_FORBIDDEN)
        except CampusStudent.DoesNotExist:
            return Response({'error': '学员校区信息不存在'}, status=status.HTTP_400_BAD_REQUEST)
    
    # 如果没有权限，拒绝访问
    if not has_permission:
        return Response({'error': '您没有权限审批此请求'}, status=status.HTTP_403_FORBIDDEN)
    
    # 检查请求状态
    if coach_change_request.status != 'pending':
        return Response({'error': '该请求已处理，无法再次审批'}, status=status.HTTP_400_BAD_REQUEST)
    
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
    
    with transaction.atomic():
        # 根据审批类型进行审批，使用模型的专用方法
        try:
            if approval_type == 'current_coach':
                # 当前教练审批
                if action == 'approve':
                    coach_change_request.approve_by_current_coach(user, notes)
                else:
                    coach_change_request.reject_by_current_coach(user, notes)
                
            elif approval_type == 'target_coach':
                # 目标教练审批
                if action == 'approve':
                    coach_change_request.approve_by_target_coach(user, notes)
                else:
                    coach_change_request.reject_by_target_coach(user, notes)
                
            elif approval_type == 'campus_admin':
                # 校区管理员审批
                if action == 'approve':
                    coach_change_request.approve_by_campus_admin(user, notes)
                else:
                    coach_change_request.reject_by_campus_admin(user, notes)
        
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        # 发送通知
        if coach_change_request.has_rejection:
            # 发送拒绝通知
            try:
                Notification.create_notification(
                    recipient=coach_change_request.student,
                    sender=user,
                    title="教练更换申请被拒绝",
                    message=f"您的教练更换申请已被 {user.real_name or user.username} 拒绝。拒绝原因：{notes or '无'}",
                    message_type="system",
                    data={
                        'request_id': coach_change_request.id,
                        'rejected_by': user.real_name or user.username,
                        'rejection_reason': notes or '无'
                    }
                )
            except Exception as e:
                print(f"发送教练更换拒绝通知失败: {e}")
            
        elif coach_change_request.is_all_approved:
            # 执行教练更换逻辑
            try:
                coach_change_request.execute_change()
            except ValueError as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
            
            # 发送成功通知
            try:
                Notification.create_notification(
                    recipient=coach_change_request.student,
                    sender=user,
                    title="教练更换申请已通过",
                    message=f"您的教练更换申请已通过所有审批，教练已从 {coach_change_request.current_coach.real_name or coach_change_request.current_coach.username} 更换为 {coach_change_request.target_coach.real_name or coach_change_request.target_coach.username}",
                    message_type="system",
                    data={
                        'request_id': coach_change_request.id,
                        'old_coach': coach_change_request.current_coach.real_name or coach_change_request.current_coach.username,
                        'new_coach': coach_change_request.target_coach.real_name or coach_change_request.target_coach.username
                    }
                )
            except Exception as e:
                print(f"发送教练更换成功通知失败: {e}")
        else:
            # 还有待审批的，发送进度通知
            try:
                # 通知学员审批进度
                approver_name = user.real_name or user.username
                Notification.create_notification(
                    recipient=coach_change_request.student,
                    sender=user,
                    title="教练更换申请审批进度",
                    message=f"{approver_name} 已{('同意' if action == 'approve' else '拒绝')}您的教练更换申请，请等待其他审批人员处理。",
                    message_type="system",
                    data={
                        'request_id': coach_change_request.id,
                        'approver': approver_name,
                        'action': action,
                        'notes': notes
                    }
                )
            except Exception as e:
                print(f"发送教练更换进度通知失败: {e}")
    
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
        
    elif user.user_type == 'campus_admin' or user.is_superuser:
        # 校区管理员或超级管理员查看待审批的请求
        requests = CoachChangeRequest.objects.filter(
            campus_admin_approval='pending',
            status='pending'
        ).order_by('-created_at')
        
        # 校区管理员只能看到本校区的申请，超级管理员可以看到所有申请
        if user.user_type == 'campus_admin' and not user.is_superuser:
            from campus.models import CampusStudent
            # 过滤出本校区学员的申请
            campus_students = CampusStudent.objects.filter(
                campus__manager=user, is_active=True
            ).values_list('student_id', flat=True)
            requests = requests.filter(student_id__in=campus_students)
        
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
