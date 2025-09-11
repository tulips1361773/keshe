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