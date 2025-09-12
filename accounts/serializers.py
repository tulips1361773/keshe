from rest_framework import serializers
from .models import User, UserProfile, Coach


class UserSerializer(serializers.ModelSerializer):
    """用户序列化器"""
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'real_name', 'phone', 'user_type',
            'avatar', 'gender', 'birth_date', 'address', 'emergency_contact',
            'emergency_phone', 'is_active', 'is_active_member', 'registration_date',
            'last_login', 'password'
        ]
        extra_kwargs = {
            'password': {'write_only': True},
            'last_login': {'read_only': True},
            'registration_date': {'read_only': True},
        }
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user
    
    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        if password:
            instance.set_password(password)
        
        instance.save()
        return instance


class UserProfileSerializer(serializers.ModelSerializer):
    """用户资料序列化器"""
    user_info = UserSerializer(source='user', read_only=True)
    
    class Meta:
        model = UserProfile
        fields = [
            'id', 'user', 'user_info', 'bio', 'skills', 'experience_years',
            'certification', 'created_at', 'updated_at'
        ]
        extra_kwargs = {
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
        }


class UserRegistrationSerializer(serializers.ModelSerializer):
    """用户注册序列化器"""
    password = serializers.CharField(write_only=True, min_length=8, max_length=16)
    password_confirm = serializers.CharField(write_only=True)
    achievements = serializers.CharField(required=False, allow_blank=True, write_only=True, help_text='教练员比赛成绩描述')
    avatar = serializers.ImageField(required=False, allow_null=True, write_only=True, help_text='教练员头像照片')
    
    class Meta:
        model = User
        fields = [
            'username', 'password', 'password_confirm', 'real_name',
            'user_type', 'phone', 'email', 'gender', 'achievements', 'avatar'
        ]
        extra_kwargs = {
            'password': {'write_only': True, 'min_length': 8, 'max_length': 16},
            'user_type': {'required': True},
            'real_name': {'required': True},
            'phone': {'required': True},
        }
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("两次输入的密码不一致")
        
        # 教练员必须填写成就描述和上传头像
        if attrs.get('user_type') == 'coach':
            achievements = attrs.get('achievements', '').strip()
            if not achievements:
                raise serializers.ValidationError("教练员必须填写比赛成绩描述")
            
            avatar = attrs.get('avatar')
            if not avatar:
                raise serializers.ValidationError("教练员必须上传头像照片")
        
        return attrs
    
    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("用户名已存在")
        return value
    
    def validate_phone(self, value):
        if User.objects.filter(phone=value).exists():
            raise serializers.ValidationError("手机号已被注册")
        return value
    
    def validate_email(self, value):
        if value and User.objects.filter(email=value).exists():
            raise serializers.ValidationError("该邮箱已被注册")
        return value
    
    def validate_password(self, value):
        import re
        
        # 检查密码长度
        if len(value) < 8 or len(value) > 16:
            raise serializers.ValidationError('密码长度必须为8-16位')
        
        # 检查是否包含字母
        if not re.search(r'[a-zA-Z]', value):
            raise serializers.ValidationError('密码必须包含字母')
        
        # 检查是否包含数字
        if not re.search(r'\d', value):
            raise serializers.ValidationError('密码必须包含数字')
        
        # 检查是否包含特殊字符
        if not re.search(r'[!@#$%^&*(),.?":{}|<>_~`\-+=\[\]\\;/]', value):
            raise serializers.ValidationError('密码必须包含特殊字符')
        
        return value
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        achievements = validated_data.pop('achievements', '')  # 移除achievements字段
        avatar = validated_data.pop('avatar', None)  # 移除avatar字段
        
        # 手动验证密码复杂度（确保验证生效）
        self.validate_password(password)
        
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        
        # 如果是教练员且有头像，保存头像
        if user.user_type == 'coach' and avatar:
            user.avatar = avatar
        
        user.save()
        
        # 创建用户资料
        UserProfile.objects.create(user=user)
        
        # 如果是教练员，创建教练员记录
        if user.user_type == 'coach':
            from .models import Coach
            Coach.objects.create(
                user=user,
                achievements=achievements,
                status='pending'  # 默认待审核状态
            )
            # 教练员默认需要审核，设置为未激活会员
            user.is_active_member = False
            user.save()
        
        return user


class UserLoginSerializer(serializers.Serializer):
    """用户登录序列化器"""
    username = serializers.CharField()
    password = serializers.CharField()
    
    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        
        if username and password:
            from django.contrib.auth import authenticate
            user = authenticate(username=username, password=password)
            
            if not user:
                raise serializers.ValidationError('用户名或密码错误')
            
            if not user.is_active:
                raise serializers.ValidationError('账户已被禁用')
            
            attrs['user'] = user
            return attrs
        else:
            raise serializers.ValidationError('用户名和密码不能为空')


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    """用户资料更新序列化器"""
    bio = serializers.CharField(required=False, allow_blank=True)
    skills = serializers.CharField(required=False, allow_blank=True)
    experience_years = serializers.IntegerField(required=False, min_value=0)
    certification = serializers.CharField(required=False, allow_blank=True)
    
    class Meta:
        model = User
        fields = [
            'real_name', 'email', 'gender', 'birth_date', 'address',
            'emergency_contact', 'emergency_phone', 'bio', 'skills',
            'experience_years', 'certification'
        ]
        extra_kwargs = {
            'real_name': {'required': False},
            'email': {'required': False},
            'gender': {'required': False},
            'birth_date': {'required': False},
            'address': {'required': False},
            'emergency_contact': {'required': False},
            'emergency_phone': {'required': False},
        }
    
    def validate_email(self, value):
        """验证邮箱格式"""
        if value:
            import re
            email_pattern = r'^[^\s@]+@[^\s@]+\.[^\s@]+$'
            if not re.match(email_pattern, value):
                raise serializers.ValidationError('邮箱格式不正确')
            
            # 检查邮箱是否已被其他用户使用
            user = self.context.get('request').user if self.context.get('request') else None
            if user and User.objects.filter(email=value).exclude(id=user.id).exists():
                raise serializers.ValidationError('该邮箱已被其他用户使用')
        return value
    
    def validate_emergency_phone(self, value):
        """验证紧急联系电话格式"""
        if value:
            import re
            phone_pattern = r'^1[3-9]\d{9}$'
            if not re.match(phone_pattern, value):
                raise serializers.ValidationError('手机号格式不正确')
        return value
    
    def update(self, instance, validated_data):
        """更新用户资料"""
        # 分离用户基本信息和扩展资料
        profile_fields = ['bio', 'skills', 'experience_years', 'certification']
        profile_data = {}
        
        for field in profile_fields:
            if field in validated_data:
                profile_data[field] = validated_data.pop(field)
        
        # 更新用户基本信息
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        # 更新用户扩展资料
        if profile_data:
            profile, created = UserProfile.objects.get_or_create(user=instance)
            for attr, value in profile_data.items():
                setattr(profile, attr, value)
            profile.save()
        
        return instance


class PasswordChangeSerializer(serializers.Serializer):
    """密码修改序列化器"""
    old_password = serializers.CharField()
    new_password = serializers.CharField(min_length=6)
    new_password_confirm = serializers.CharField()
    
    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError('原密码错误')
        return value
    
    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError('两次输入的新密码不一致')
        return attrs
    
    def save(self):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user


class CoachSerializer(serializers.ModelSerializer):
    """教练员序列化器"""
    user_info = UserSerializer(source='user', read_only=True)
    coach_level_display = serializers.CharField(source='get_coach_level_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    approved_by_name = serializers.CharField(source='approved_by.real_name', read_only=True)
    current_students_count = serializers.ReadOnlyField()
    is_approved = serializers.ReadOnlyField()
    avatar = serializers.CharField(source='user.avatar', read_only=True)
    real_name = serializers.CharField(source='user.real_name', read_only=True)
    phone = serializers.CharField(source='user.phone', read_only=True)
    
    class Meta:
        model = Coach
        fields = [
            'id', 'user', 'user_info', 'coach_level', 'coach_level_display',
            'hourly_rate', 'achievements', 'max_students', 'status', 'status_display',
            'approved_by', 'approved_by_name', 'approved_at', 'current_students_count',
            'is_approved', 'avatar', 'real_name', 'phone', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'user', 'hourly_rate', 'approved_by', 'approved_at',
            'created_at', 'updated_at'
        ]


class CoachApprovalSerializer(serializers.ModelSerializer):
    """教练员审核序列化器"""
    
    class Meta:
        model = Coach
        fields = ['coach_level', 'status']
    
    def validate_status(self, value):
        if value not in ['approved', 'rejected']:
            raise serializers.ValidationError('状态只能是已通过或已拒绝')
        return value
    
    def update(self, instance, validated_data):
        from django.utils import timezone
        
        # 设置审核人和审核时间
        request = self.context.get('request')
        if request and request.user:
            instance.approved_by = request.user
            instance.approved_at = timezone.now()
        
        return super().update(instance, validated_data)