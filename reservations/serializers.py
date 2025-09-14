from rest_framework import serializers
from django.utils import timezone
from datetime import datetime, timedelta

from .models import CoachStudentRelation, Table, Booking, BookingCancellation
from accounts.models import User
from campus.models import Campus


class UserSimpleSerializer(serializers.ModelSerializer):
    """用户简单信息序列化器"""
    class Meta:
        model = User
        fields = ['id', 'username', 'real_name', 'phone', 'email', 'user_type']
        read_only_fields = ['id', 'username', 'user_type']


class CampusSimpleSerializer(serializers.ModelSerializer):
    """校区简单信息序列化器"""
    class Meta:
        model = Campus
        fields = ['id', 'name', 'address', 'phone']
        read_only_fields = ['id']


class CoachStudentRelationSerializer(serializers.ModelSerializer):
    """师生关系序列化器"""
    coach = UserSimpleSerializer(read_only=True)
    student = UserSimpleSerializer(read_only=True)
    coach_id = serializers.IntegerField(write_only=True, required=False)
    student_id = serializers.IntegerField(write_only=True, required=False)
    
    class Meta:
        model = CoachStudentRelation
        fields = [
            'id', 'coach', 'student', 'coach_id', 'student_id',
            'status', 'applied_by', 'applied_at', 'processed_at',
            'terminated_at', 'notes', 'created_at'
        ]
        read_only_fields = [
            'id', 'status', 'applied_by', 'applied_at',
            'processed_at', 'terminated_at', 'created_at'
        ]
    
    def validate(self, data):
        request = self.context.get('request')
        if not request:
            return data
        
        user = request.user
        
        # 根据用户类型验证数据
        if user.user_type == 'coach':
            if 'student_id' not in data:
                raise serializers.ValidationError('教练申请时必须指定学员')
            
            # 验证学员存在且为学员类型
            try:
                student = User.objects.get(id=data['student_id'], user_type='student')
                data['student'] = student
            except User.DoesNotExist:
                raise serializers.ValidationError('指定的学员不存在')
            
            # 检查是否已存在师生关系
            existing_relation = CoachStudentRelation.objects.filter(
                coach=user,
                student=student
            ).first()
            
            if existing_relation:
                if existing_relation.status == 'pending':
                    raise serializers.ValidationError('您已经向该学员发送过申请，请等待处理')
                elif existing_relation.status == 'approved':
                    raise serializers.ValidationError('您与该学员已经建立了师生关系')
                elif existing_relation.status == 'rejected':
                    raise serializers.ValidationError('该学员已拒绝您的申请，暂时无法重新申请')
        
        elif user.user_type == 'student':
            if 'coach_id' not in data:
                raise serializers.ValidationError('学员申请时必须指定教练')
            
            # 验证教练是否存在 - 支持Coach模型ID和User模型ID
            coach = None
            try:
                # 首先尝试通过Coach模型ID查找
                from accounts.models import Coach
                coach_profile = Coach.objects.select_related('user').get(id=data['coach_id'])
                coach = coach_profile.user
            except Coach.DoesNotExist:
                try:
                    # 如果Coach模型ID不存在，尝试User模型ID
                    coach = User.objects.get(id=data['coach_id'], user_type='coach')
                except User.DoesNotExist:
                    raise serializers.ValidationError('指定的教练不存在')
            
            if not coach or coach.user_type != 'coach':
                raise serializers.ValidationError('指定的教练不存在')
            
            data['coach'] = coach
            
            # 检查是否已存在师生关系
            existing_relation = CoachStudentRelation.objects.filter(
                coach=coach,
                student=user
            ).first()
            
            if existing_relation:
                if existing_relation.status == 'pending':
                    raise serializers.ValidationError('您已经向该教练发送过申请，请等待处理')
                elif existing_relation.status == 'approved':
                    raise serializers.ValidationError('您已经选择过这位教练了')
                elif existing_relation.status == 'rejected':
                    raise serializers.ValidationError('该教练已拒绝您的申请，暂时无法重新申请')
        
        else:
            raise serializers.ValidationError('只有教练和学员可以创建师生关系')
        
        return data
    
    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user if request else None
        
        # 根据用户类型设置关系
        if user and user.user_type == 'coach':
            validated_data['coach'] = user
            # student已在validate中设置
        elif user and user.user_type == 'student':
            validated_data['student'] = user
            # coach已在validate中设置
        
        # 移除临时字段
        validated_data.pop('coach_id', None)
        validated_data.pop('student_id', None)
        
        # 创建师生关系
        relation = super().create(validated_data)
        
        # 创建通知
        from notifications.models import Notification
        
        if user and user.user_type == 'student':
            # 学员申请教练时，通知教练
            Notification.create_system_notification(
                recipient=relation.coach,
                title="新的学员申请",
                message=f"学员 {user.real_name or user.username} 申请选择您为教练",
                data={
                    'relation_id': relation.id,
                    'type': 'relation_request',
                    'student_name': user.real_name or user.username,
                    'student_id': user.id
                }
            )
        elif user and user.user_type == 'coach':
            # 教练申请学员时，通知学员
            Notification.create_system_notification(
                recipient=relation.student,
                title="教练申请",
                message=f"教练 {user.real_name or user.username} 申请指导您",
                data={
                    'relation_id': relation.id,
                    'type': 'coach_request',
                    'coach_name': user.real_name or user.username,
                    'coach_id': user.id
                }
            )
        
        return relation


class TableSerializer(serializers.ModelSerializer):
    """球台序列化器"""
    campus = CampusSimpleSerializer(read_only=True)
    
    class Meta:
        model = Table
        fields = [
            'id', 'campus', 'number', 'name', 'status',
            'description', 'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class BookingSerializer(serializers.ModelSerializer):
    """预约序列化器"""
    relation = CoachStudentRelationSerializer(read_only=True)
    table = TableSerializer(read_only=True)
    coach = UserSimpleSerializer(read_only=True)
    student = UserSimpleSerializer(read_only=True)
    cancelled_by = UserSimpleSerializer(read_only=True)
    
    # 取消申请相关字段
    has_pending_cancellation = serializers.SerializerMethodField()
    cancellation_status = serializers.SerializerMethodField()
    cancellation_info = serializers.SerializerMethodField()
    
    class Meta:
        model = Booking
        fields = [
            'id', 'relation', 'table', 'coach', 'student',
            'start_time', 'end_time', 'duration_hours', 'total_fee',
            'status', 'confirmed_at', 'cancelled_at', 'cancel_reason',
            'cancelled_by', 'notes', 'created_at', 'updated_at',
            'has_pending_cancellation', 'cancellation_status', 'cancellation_info'
        ]
        read_only_fields = [
            'id', 'coach', 'student', 'confirmed_at', 'cancelled_at',
            'cancelled_by', 'created_at', 'updated_at'
        ]
    
    def get_has_pending_cancellation(self, obj):
        """获取是否有待处理的取消申请"""
        return obj.has_pending_cancellation()
    
    def get_cancellation_status(self, obj):
        """获取取消申请状态"""
        return obj.get_cancellation_status()
    
    def get_cancellation_info(self, obj):
        """获取取消申请详细信息"""
        if hasattr(obj, 'cancellation'):
            cancellation = obj.cancellation
            return {
                'id': cancellation.id,
                'requested_by': {
                    'id': cancellation.requested_by.id,
                    'username': cancellation.requested_by.username,
                    'real_name': cancellation.requested_by.real_name
                },
                'reason': cancellation.reason,
                'status': cancellation.status,
                'created_at': cancellation.created_at,
                'processed_by': {
                    'id': cancellation.processed_by.id,
                    'username': cancellation.processed_by.username,
                    'real_name': cancellation.processed_by.real_name
                } if cancellation.processed_by else None,
                'processed_at': cancellation.processed_at,
                'response_message': cancellation.response_message
            }
        return None


class BookingCreateSerializer(serializers.ModelSerializer):
    """创建预约序列化器"""
    relation_id = serializers.IntegerField()
    table_id = serializers.IntegerField()
    
    class Meta:
        model = Booking
        fields = [
            'relation_id', 'table_id', 'start_time', 'end_time',
            'duration_hours', 'total_fee', 'notes'
        ]
    
    def validate_relation_id(self, value):
        """验证师生关系"""
        try:
            relation = CoachStudentRelation.objects.get(id=value, status='approved')
            return value
        except CoachStudentRelation.DoesNotExist:
            raise serializers.ValidationError('师生关系不存在或未通过审核')
    
    def validate_table_id(self, value):
        """验证球台"""
        try:
            table = Table.objects.get(id=value, is_active=True)
            return value
        except Table.DoesNotExist:
            raise serializers.ValidationError('球台不存在或不可用')
    
    def validate(self, data):
        """验证预约数据"""
        start_time = data.get('start_time')
        end_time = data.get('end_time')
        table_id = data.get('table_id')
        
        # 验证时间
        if start_time >= end_time:
            raise serializers.ValidationError('开始时间必须早于结束时间')
        
        # 验证预约时间不能是过去时间
        if start_time <= timezone.now():
            raise serializers.ValidationError('预约时间不能是过去时间')
        
        # 验证预约时长
        duration = (end_time - start_time).total_seconds() / 3600
        if duration < 0.5:
            raise serializers.ValidationError('预约时长不能少于30分钟')
        if duration > 8:
            raise serializers.ValidationError('预约时长不能超过8小时')
        
        # 验证球台在该时间段是否可用
        overlapping_bookings = Booking.objects.filter(
            table_id=table_id,
            start_time__lt=end_time,
            end_time__gt=start_time,
            status__in=['pending', 'confirmed']
        )
        
        if overlapping_bookings.exists():
            raise serializers.ValidationError('该时间段球台已被预约')
        
        # 自动计算时长
        data['duration_hours'] = round(duration, 1)
        
        return data
    
    def create(self, validated_data):
        """创建预约"""
        relation_id = validated_data.pop('relation_id')
        table_id = validated_data.pop('table_id')
        
        relation = CoachStudentRelation.objects.get(id=relation_id)
        table = Table.objects.get(id=table_id)
        
        booking = Booking.objects.create(
            relation=relation,
            table=table,
            **validated_data
        )
        
        return booking


class BookingCancellationSerializer(serializers.ModelSerializer):
    """预约取消申请序列化器"""
    booking = BookingSerializer(read_only=True)
    requested_by = UserSimpleSerializer(read_only=True)
    processed_by = UserSimpleSerializer(read_only=True)
    
    class Meta:
        model = BookingCancellation
        fields = [
            'id', 'booking', 'requested_by', 'reason', 'status',
            'processed_by', 'processed_at', 'response_message', 'created_at'
        ]
        read_only_fields = [
            'id', 'requested_by', 'status', 'processed_by',
            'processed_at', 'response_message', 'created_at'
        ]


class BookingCancellationCreateSerializer(serializers.ModelSerializer):
    """创建预约取消申请序列化器"""
    booking_id = serializers.IntegerField()
    
    class Meta:
        model = BookingCancellation
        fields = ['booking_id', 'reason']
    
    def validate_booking_id(self, value):
        """验证预约ID"""
        try:
            booking = Booking.objects.get(id=value)
        except Booking.DoesNotExist:
            raise serializers.ValidationError('预约不存在')
        
        # 检查预约状态
        if booking.status not in ['pending', 'confirmed']:
            raise serializers.ValidationError('预约状态不允许申请取消')
        
        # 检查是否已有取消申请
        if hasattr(booking, 'cancellation'):
            raise serializers.ValidationError('该预约已有取消申请')
        
        return value


class BookingListSerializer(serializers.ModelSerializer):
    """预约列表序列化器（简化版）"""
    coach_name = serializers.CharField(source='relation.coach.real_name', read_only=True)
    student_name = serializers.CharField(source='relation.student.real_name', read_only=True)
    table_info = serializers.CharField(source='table.__str__', read_only=True)
    campus_name = serializers.CharField(source='table.campus.name', read_only=True)
    
    class Meta:
        model = Booking
        fields = [
            'id', 'coach_name', 'student_name', 'table_info', 'campus_name',
            'start_time', 'end_time', 'duration_hours', 'total_fee',
            'status', 'created_at'
        ]
        read_only_fields = fields