from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import CoachStudentRelation, Table, Booking
from .coach_change_models import CoachChangeRequest
from accounts.serializers import UserSerializer

User = get_user_model()


class CoachStudentRelationSerializer(serializers.ModelSerializer):
    coach_id = serializers.IntegerField(write_only=True)
    student_id = serializers.IntegerField(write_only=True)
    coach = UserSerializer(read_only=True)
    student = UserSerializer(read_only=True)
    
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
    
    def create(self, validated_data):
        coach_id = validated_data.pop('coach_id')
        student_id = validated_data.pop('student_id')
        
        try:
            coach = User.objects.get(id=coach_id, user_type='coach')
            student = User.objects.get(id=student_id, user_type='student')
        except User.DoesNotExist:
            raise serializers.ValidationError("指定的教练或学员不存在")
        
        # 检查是否已存在关系
        existing_relation = CoachStudentRelation.objects.filter(
            coach=coach,
            student=student
        ).first()
        
        if existing_relation:
            if existing_relation.status == 'approved':
                raise serializers.ValidationError("已经选择过这位教练了")
            elif existing_relation.status == 'pending':
                raise serializers.ValidationError("已经向该教练发送过申请，请等待审核")
            elif existing_relation.status == 'rejected':
                raise serializers.ValidationError("该教练已拒绝您的申请")
        
        validated_data['coach'] = coach
        validated_data['student'] = student
        validated_data['applied_by'] = 'student'
        
        return super().create(validated_data)


class TableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = '__all__'


class BookingSerializer(serializers.ModelSerializer):
    coach_name = serializers.CharField(source='relation.coach.real_name', read_only=True)
    student_name = serializers.CharField(source='relation.student.real_name', read_only=True)
    table_number = serializers.CharField(source='table.number', read_only=True)
    coach_id = serializers.IntegerField(source='relation.coach.id', read_only=True)
    student_id = serializers.IntegerField(source='relation.student.id', read_only=True)
    
    # 添加前端兼容字段
    relation_id = serializers.IntegerField(write_only=True, required=False)
    table_id = serializers.IntegerField(write_only=True, required=False)
    
    # 取消申请相关字段
    has_pending_cancellation = serializers.SerializerMethodField()
    cancellation_info = serializers.SerializerMethodField()
    
    # 用于返回的嵌套对象
    relation = serializers.SerializerMethodField()
    table = serializers.SerializerMethodField()
    
    def get_relation(self, obj):
        """返回包含coach和student信息的relation对象"""
        return {
            'id': obj.relation.id,
            'coach': {
                'id': obj.relation.coach.id,
                'real_name': obj.relation.coach.real_name,
                'username': obj.relation.coach.username,
            },
            'student': {
                'id': obj.relation.student.id,
                'real_name': obj.relation.student.real_name,
                'username': obj.relation.student.username,
            }
        }
    
    def get_table(self, obj):
        """返回包含campus信息的table对象"""
        return {
            'id': obj.table.id,
            'number': obj.table.number,
            'campus': {
                'id': obj.table.campus.id,
                'name': obj.table.campus.name,
            }
        }
    
    def get_has_pending_cancellation(self, obj):
        """检查是否有待处理的取消申请"""
        return hasattr(obj, 'cancellation') and obj.cancellation.status == 'pending'
    
    def get_cancellation_info(self, obj):
        """获取取消申请信息"""
        if hasattr(obj, 'cancellation') and obj.cancellation.status == 'pending':
            return {
                'id': obj.cancellation.id,
                'reason': obj.cancellation.reason,
                'requested_by_id': obj.cancellation.requested_by.id,
                'requested_by_name': obj.cancellation.requested_by.real_name or obj.cancellation.requested_by.username,
                'requested_at': obj.cancellation.created_at.strftime('%Y-%m-%d %H:%M'),
                'status': obj.cancellation.status
            }
        return None
    
    def create(self, validated_data):
        # 处理前端字段映射
        if 'relation_id' in validated_data:
            validated_data['relation_id'] = validated_data.pop('relation_id')
        if 'table_id' in validated_data:
            validated_data['table_id'] = validated_data.pop('table_id')
        
        return super().create(validated_data)
    
    class Meta:
        model = Booking
        fields = [
            'id', 'relation', 'table', 'relation_id', 'table_id', 'start_time', 'end_time',
            'duration_hours', 'total_fee', 'status',
            'notes', 'created_at', 'updated_at',
            'coach_id', 'coach_name', 'student_id', 'student_name', 'table_number',
            'has_pending_cancellation', 'cancellation_info'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class CoachChangeRequestSerializer(serializers.ModelSerializer):
    """教练更换请求序列化器"""
    
    # 只写字段
    current_coach_id = serializers.IntegerField(write_only=True, required=False)
    target_coach_id = serializers.IntegerField(write_only=True)
    
    # 只读字段 - 用户信息
    student = UserSerializer(read_only=True)
    current_coach = UserSerializer(read_only=True)
    target_coach = UserSerializer(read_only=True)
    
    # 只读字段 - 审批人信息
    current_coach_approved_by = UserSerializer(read_only=True)
    target_coach_approved_by = UserSerializer(read_only=True)
    campus_admin_approved_by = UserSerializer(read_only=True)
    processed_by = UserSerializer(read_only=True)
    
    # 状态显示字段
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    current_coach_approval_display = serializers.CharField(source='get_current_coach_approval_display', read_only=True)
    target_coach_approval_display = serializers.CharField(source='get_target_coach_approval_display', read_only=True)
    campus_admin_approval_display = serializers.CharField(source='get_campus_admin_approval_display', read_only=True)
    
    # 计算字段
    is_all_approved = serializers.BooleanField(read_only=True)
    has_rejection = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = CoachChangeRequest
        fields = [
            'id', 'student', 'current_coach', 'target_coach',
            'current_coach_id', 'target_coach_id',
            'reason', 'request_date', 'status', 'status_display',
            
            # 审批状态
            'current_coach_approval', 'current_coach_approval_display',
            'target_coach_approval', 'target_coach_approval_display', 
            'campus_admin_approval', 'campus_admin_approval_display',
            
            # 审批人和时间
            'current_coach_approved_by', 'current_coach_approved_at',
            'target_coach_approved_by', 'target_coach_approved_at',
            'campus_admin_approved_by', 'campus_admin_approved_at',
            
            # 审批备注
            'current_coach_notes', 'target_coach_notes', 'campus_admin_notes',
            
            # 处理信息
            'processed_at', 'processed_by',
            
            # 计算字段
            'is_all_approved', 'has_rejection',
            
            # 时间戳
            'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'student', 'status', 'request_date',
            'current_coach_approval', 'target_coach_approval', 'campus_admin_approval',
            'current_coach_approved_by', 'current_coach_approved_at',
            'target_coach_approved_by', 'target_coach_approved_at',
            'campus_admin_approved_by', 'campus_admin_approved_at',
            'current_coach_notes', 'target_coach_notes', 'campus_admin_notes',
            'processed_at', 'processed_by', 'created_at', 'updated_at'
        ]
    
    def validate(self, data):
        """验证数据"""
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            raise serializers.ValidationError("用户未认证")
        
        # 验证用户类型
        if request.user.user_type != 'student':
            raise serializers.ValidationError("只有学员可以申请更换教练")
        
        # 获取目标教练
        target_coach_id = data.get('target_coach_id')
        if not target_coach_id:
            raise serializers.ValidationError("必须指定目标教练")
        
        try:
            target_coach = User.objects.get(id=target_coach_id, user_type='coach')
        except User.DoesNotExist:
            raise serializers.ValidationError("指定的目标教练不存在")
        
        # 获取当前教练
        current_coach_id = data.get('current_coach_id')
        if current_coach_id:
            try:
                current_coach = User.objects.get(id=current_coach_id, user_type='coach')
            except User.DoesNotExist:
                raise serializers.ValidationError("指定的当前教练不存在")
        else:
            # 自动获取学员当前的教练
            current_relation = CoachStudentRelation.objects.filter(
                student=request.user,
                status='approved'
            ).first()
            
            if not current_relation:
                raise serializers.ValidationError("您当前没有教练，无法申请更换")
            
            current_coach = current_relation.coach
            data['current_coach_id'] = current_coach.id
        
        # 验证不能更换为同一个教练
        if current_coach.id == target_coach.id:
            raise serializers.ValidationError("不能更换为当前教练")
        
        # 检查是否已有待处理的更换请求
        existing_request = CoachChangeRequest.objects.filter(
            student=request.user,
            status='pending'
        ).first()
        
        if existing_request:
            raise serializers.ValidationError("您已有待处理的教练更换请求，请等待审核完成")
        
        return data
    
    def create(self, validated_data):
        """创建教练更换请求"""
        request = self.context.get('request')
        
        # 获取教练对象
        current_coach_id = validated_data.pop('current_coach_id')
        target_coach_id = validated_data.pop('target_coach_id')
        
        current_coach = User.objects.get(id=current_coach_id)
        target_coach = User.objects.get(id=target_coach_id)
        
        # 创建请求
        coach_change_request = CoachChangeRequest.objects.create(
            student=request.user,
            current_coach=current_coach,
            target_coach=target_coach,
            **validated_data
        )
        
        return coach_change_request


class CoachChangeApprovalSerializer(serializers.Serializer):
    """教练更换审批序列化器"""
    
    action = serializers.ChoiceField(choices=['approve', 'reject'])
    notes = serializers.CharField(required=False, allow_blank=True, max_length=500)
    
    def validate(self, data):
        """验证审批数据"""
        request = self.context.get('request')
        coach_change_request = self.context.get('coach_change_request')
        
        if not request or not request.user.is_authenticated:
            raise serializers.ValidationError("用户未认证")
        
        if not coach_change_request:
            raise serializers.ValidationError("未找到教练更换请求")
        
        # 检查请求状态
        if coach_change_request.status != 'pending':
            raise serializers.ValidationError("该请求已处理，无法再次审批")
        
        # 检查用户权限
        user = request.user
        if user == coach_change_request.current_coach:
            # 当前教练审批
            if coach_change_request.current_coach_approval != 'pending':
                raise serializers.ValidationError("您已经审批过此请求")
        elif user == coach_change_request.target_coach:
            # 目标教练审批
            if coach_change_request.target_coach_approval != 'pending':
                raise serializers.ValidationError("您已经审批过此请求")
        elif user.user_type == 'campus_admin':
            # 校区管理员审批
            if coach_change_request.campus_admin_approval != 'pending':
                raise serializers.ValidationError("您已经审批过此请求")
        else:
            raise serializers.ValidationError("您没有权限审批此请求")
        
        return data