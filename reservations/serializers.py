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
        
        elif user.user_type == 'student':
            if 'coach_id' not in data:
                raise serializers.ValidationError('学员申请时必须指定教练')
            
            # 验证教练存在且为教练类型
            try:
                coach = User.objects.get(id=data['coach_id'], user_type='coach')
                data['coach'] = coach
            except User.DoesNotExist:
                raise serializers.ValidationError('指定的教练不存在')
        
        else:
            raise serializers.ValidationError('只有教练和学员可以创建师生关系')
        
        return data
    
    def create(self, validated_data):
        # 移除临时字段
        validated_data.pop('coach_id', None)
        validated_data.pop('student_id', None)
        return super().create(validated_data)


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
    
    class Meta:
        model = Booking
        fields = [
            'id', 'relation', 'table', 'coach', 'student',
            'start_time', 'end_time', 'duration_hours', 'total_fee',
            'status', 'confirmed_at', 'cancelled_at', 'cancel_reason',
            'cancelled_by', 'notes', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'coach', 'student', 'confirmed_at', 'cancelled_at',
            'cancelled_by', 'created_at', 'updated_at'
        ]


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