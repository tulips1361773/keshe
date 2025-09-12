from rest_framework import serializers
from .models import Campus, CampusArea, CampusStudent, CampusCoach
from accounts.serializers import UserSerializer


class CampusSerializer(serializers.ModelSerializer):
    """校区序列化器"""
    manager_name = serializers.CharField(source='manager.real_name', read_only=True)
    current_students_count = serializers.ReadOnlyField()
    current_coaches_count = serializers.ReadOnlyField()
    campus_type_display = serializers.CharField(source='get_campus_type_display', read_only=True)
    parent_campus_name = serializers.CharField(source='parent_campus.name', read_only=True)
    is_center_campus = serializers.ReadOnlyField()
    branch_campuses_count = serializers.ReadOnlyField()
    
    class Meta:
        model = Campus
        fields = [
            'id', 'name', 'code', 'campus_type', 'campus_type_display',
            'address', 'contact_person', 'phone', 'email',
            'manager', 'manager_name', 'parent_campus', 'parent_campus_name',
            'description', 'facilities', 'operating_hours', 'capacity',
            'is_active', 'is_center_campus', 'branch_campuses_count',
            'current_students_count', 'current_coaches_count',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def validate_code(self, value):
        """验证校区编码唯一性"""
        if self.instance:
            # 更新时排除当前实例
            if Campus.objects.exclude(pk=self.instance.pk).filter(code=value).exists():
                raise serializers.ValidationError("校区编码已存在")
        else:
            # 创建时检查唯一性
            if Campus.objects.filter(code=value).exists():
                raise serializers.ValidationError("校区编码已存在")
        return value

    def validate_name(self, value):
        """验证校区名称唯一性"""
        if self.instance:
            # 更新时排除当前实例
            if Campus.objects.exclude(pk=self.instance.pk).filter(name=value).exists():
                raise serializers.ValidationError("校区名称已存在")
        else:
            # 创建时检查唯一性
            if Campus.objects.filter(name=value).exists():
                raise serializers.ValidationError("校区名称已存在")
        return value
    
    def validate(self, data):
        """验证校区数据"""
        campus_type = data.get('campus_type')
        parent_campus = data.get('parent_campus')
        
        # 分校区必须有上级校区
        if campus_type == 'branch' and not parent_campus:
            raise serializers.ValidationError("分校区必须指定上级校区")
        
        # 中心校区不能有上级校区
        if campus_type == 'center' and parent_campus:
            raise serializers.ValidationError("中心校区不能指定上级校区")
        
        # 上级校区必须是中心校区
        if parent_campus and parent_campus.campus_type != 'center':
            raise serializers.ValidationError("上级校区必须是中心校区")
        
        return data


class CampusAreaSerializer(serializers.ModelSerializer):
    """校区分区序列化器"""
    campus_name = serializers.CharField(source='campus.name', read_only=True)
    area_type_display = serializers.CharField(source='get_area_type_display', read_only=True)
    
    class Meta:
        model = CampusArea
        fields = [
            'id', 'campus', 'campus_name', 'name', 'area_type',
            'area_type_display', 'description', 'capacity',
            'equipment_list', 'is_available', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def validate(self, data):
        """验证分区名称在同一校区内唯一"""
        campus = data.get('campus')
        name = data.get('name')
        
        if campus and name:
            queryset = CampusArea.objects.filter(campus=campus, name=name)
            if self.instance:
                queryset = queryset.exclude(pk=self.instance.pk)
            
            if queryset.exists():
                raise serializers.ValidationError("该校区已存在同名分区")
        
        return data


class CampusStudentSerializer(serializers.ModelSerializer):
    """校区学员序列化器"""
    campus_name = serializers.CharField(source='campus.name', read_only=True)
    student_name = serializers.CharField(source='student.real_name', read_only=True)
    student_phone = serializers.CharField(source='student.phone', read_only=True)
    student_info = UserSerializer(source='student', read_only=True)
    
    class Meta:
        model = CampusStudent
        fields = [
            'id', 'campus', 'campus_name', 'student', 'student_name',
            'student_phone', 'student_info', 'enrollment_date',
            'is_active', 'notes', 'created_at'
        ]
        read_only_fields = ['created_at']

    def validate(self, data):
        """验证学员不能重复加入同一校区"""
        campus = data.get('campus')
        student = data.get('student')
        
        if campus and student:
            # 检查学员类型
            if student.user_type != 'student':
                raise serializers.ValidationError("只能添加学员类型的用户")
            
            # 检查是否已存在
            queryset = CampusStudent.objects.filter(campus=campus, student=student)
            if self.instance:
                queryset = queryset.exclude(pk=self.instance.pk)
            
            if queryset.exists():
                raise serializers.ValidationError("该学员已在此校区")
        
        return data


class CampusCoachSerializer(serializers.ModelSerializer):
    """校区教练序列化器"""
    campus_name = serializers.CharField(source='campus.name', read_only=True)
    coach_name = serializers.CharField(source='coach.real_name', read_only=True)
    coach_phone = serializers.CharField(source='coach.phone', read_only=True)
    coach_info = UserSerializer(source='coach', read_only=True)
    current_students_count = serializers.ReadOnlyField()
    
    class Meta:
        model = CampusCoach
        fields = [
            'id', 'campus', 'campus_name', 'coach', 'coach_name',
            'coach_phone', 'coach_info', 'hire_date', 'is_active',
            'specialties', 'max_students', 'hourly_rate',
            'current_students_count', 'notes', 'created_at'
        ]
        read_only_fields = ['created_at']

    def validate(self, data):
        """验证教练不能重复加入同一校区"""
        campus = data.get('campus')
        coach = data.get('coach')
        
        if campus and coach:
            # 检查教练类型
            if coach.user_type != 'coach':
                raise serializers.ValidationError("只能添加教练类型的用户")
            
            # 检查是否已存在
            queryset = CampusCoach.objects.filter(campus=campus, coach=coach)
            if self.instance:
                queryset = queryset.exclude(pk=self.instance.pk)
            
            if queryset.exists():
                raise serializers.ValidationError("该教练已在此校区")
        
        return data

    def validate_hourly_rate(self, value):
        """验证时薪"""
        if value < 0:
            raise serializers.ValidationError("时薪不能为负数")
        return value

    def validate_max_students(self, value):
        """验证最大学员数"""
        if value <= 0:
            raise serializers.ValidationError("最大学员数必须大于0")
        return value