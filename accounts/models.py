from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    """自定义用户模型"""
    USER_TYPE_CHOICES = [
        ('super_admin', '超级管理员'),
        ('campus_admin', '校区管理员'),
        ('student', '学员'),
        ('coach', '教练员'),
    ]
    
    user_type = models.CharField(
        max_length=20,
        choices=USER_TYPE_CHOICES,
        default='student',
        verbose_name='用户类型'
    )
    phone = models.CharField(
        max_length=11,
        unique=True,
        verbose_name='手机号码'
    )
    avatar = models.ImageField(
        upload_to='avatars/',
        blank=True,
        null=True,
        verbose_name='头像'
    )
    real_name = models.CharField(
        max_length=50,
        verbose_name='真实姓名'
    )
    id_card = models.CharField(
        max_length=18,
        blank=True,
        null=True,
        verbose_name='身份证号'
    )
    birth_date = models.DateField(
        blank=True,
        null=True,
        verbose_name='出生日期'
    )
    gender = models.CharField(
        max_length=10,
        choices=[('male', '男'), ('female', '女')],
        blank=True,
        null=True,
        verbose_name='性别'
    )
    address = models.TextField(
        blank=True,
        null=True,
        verbose_name='地址'
    )
    emergency_contact = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name='紧急联系人'
    )
    emergency_phone = models.CharField(
        max_length=11,
        blank=True,
        null=True,
        verbose_name='紧急联系电话'
    )
    is_active_member = models.BooleanField(
        default=True,
        verbose_name='是否活跃用户'
    )
    registration_date = models.DateTimeField(
        default=timezone.now,
        verbose_name='注册时间'
    )
    last_login_ip = models.GenericIPAddressField(
        blank=True,
        null=True,
        verbose_name='最后登录IP'
    )
    
    class Meta:
        verbose_name = '用户'
        verbose_name_plural = '用户'
        db_table = 'accounts_user'
    
    def __str__(self):
        return f"{self.real_name}({self.username})"
    
    @property
    def is_super_admin(self):
        return self.user_type == 'super_admin'
    
    @property
    def is_campus_admin(self):
        return self.user_type == 'campus_admin'
    
    @property
    def is_student(self):
        return self.user_type == 'student'
    
    @property
    def is_coach(self):
        return self.user_type == 'coach'


class UserProfile(models.Model):
    """用户扩展信息"""
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name='用户'
    )
    bio = models.TextField(
        blank=True,
        null=True,
        verbose_name='个人简介'
    )
    skills = models.TextField(
        blank=True,
        null=True,
        verbose_name='技能特长'
    )
    experience_years = models.PositiveIntegerField(
        default=0,
        verbose_name='经验年数'
    )
    certification = models.TextField(
        blank=True,
        null=True,
        verbose_name='资格证书'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='创建时间'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='更新时间'
    )
    
    class Meta:
        verbose_name = '用户资料'
        verbose_name_plural = '用户资料'
        db_table = 'accounts_user_profile'
    
    def __str__(self):
        return f"{self.user.real_name}的资料"


class Coach(models.Model):
    """教练员扩展模型"""
    COACH_LEVEL_CHOICES = [
        ('junior', '初级教练员'),
        ('intermediate', '中级教练员'),
        ('senior', '高级教练员'),
    ]
    
    STATUS_CHOICES = [
        ('pending', '待审核'),
        ('approved', '已通过'),
        ('rejected', '已拒绝'),
    ]
    
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'user_type': 'coach'},
        related_name='coach_profile',
        verbose_name='用户'
    )
    coach_level = models.CharField(
        max_length=20,
        choices=COACH_LEVEL_CHOICES,
        default='junior',
        verbose_name='教练级别'
    )
    hourly_rate = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=80.00,
        verbose_name='时薪（元/小时）'
    )
    achievements = models.TextField(
        blank=True,
        null=True,
        verbose_name='比赛成绩描述'
    )
    max_students = models.PositiveIntegerField(
        default=20,
        verbose_name='最大学员数'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name='审核状态'
    )
    approved_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={'user_type': 'campus_admin'},
        related_name='approved_coaches',
        verbose_name='审核人'
    )
    approved_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='审核时间'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='创建时间'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='更新时间'
    )
    
    class Meta:
        verbose_name = '教练员'
        verbose_name_plural = '教练员'
        db_table = 'accounts_coach'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.real_name} - {self.get_coach_level_display()}"
    
    @property
    def current_students_count(self):
        """当前学员数量"""
        from reservations.models import CoachStudentRelation
        return CoachStudentRelation.objects.filter(
            coach=self.user,
            status='approved'
        ).count()
    
    @property
    def is_approved(self):
        """是否已审核通过"""
        return self.status == 'approved'
    
    def save(self, *args, **kwargs):
        # 根据教练级别设置时薪
        if self.coach_level == 'junior':
            self.hourly_rate = 80.00
        elif self.coach_level == 'intermediate':
            self.hourly_rate = 150.00
        elif self.coach_level == 'senior':
            self.hourly_rate = 200.00
        
        super().save(*args, **kwargs)