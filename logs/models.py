from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
import json

User = get_user_model()


class SystemLog(models.Model):
    """系统操作日志模型"""
    ACTION_TYPE_CHOICES = [
        ('create', '创建'),
        ('update', '更新'),
        ('delete', '删除'),
        ('login', '登录'),
        ('logout', '登出'),
        ('approve', '审核'),
        ('reject', '拒绝'),
        ('cancel', '取消'),
        ('confirm', '确认'),
        ('payment', '支付'),
        ('refund', '退款'),
        ('register', '注册'),
        ('other', '其他'),
    ]
    
    RESOURCE_TYPE_CHOICES = [
        ('user', '用户'),
        ('campus', '校区'),
        ('student', '学员'),
        ('coach', '教练'),
        ('booking', '预约'),
        ('course', '课程'),
        ('payment', '支付'),
        ('competition', '比赛'),
        ('notification', '通知'),
        ('system', '系统'),
        ('other', '其他'),
    ]
    
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='operation_logs',
        verbose_name='操作用户'
    )
    action_type = models.CharField(
        max_length=20,
        choices=ACTION_TYPE_CHOICES,
        verbose_name='操作类型'
    )
    resource_type = models.CharField(
        max_length=20,
        choices=RESOURCE_TYPE_CHOICES,
        verbose_name='资源类型'
    )
    resource_id = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name='资源ID'
    )
    resource_name = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        verbose_name='资源名称'
    )
    description = models.TextField(
        verbose_name='操作描述'
    )
    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True,
        verbose_name='IP地址'
    )
    user_agent = models.TextField(
        null=True,
        blank=True,
        verbose_name='用户代理'
    )
    extra_data = models.JSONField(
        default=dict,
        blank=True,
        verbose_name='额外数据'
    )
    campus = models.ForeignKey(
        'campus.Campus',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='operation_logs',
        verbose_name='所属校区'
    )
    created_at = models.DateTimeField(
        default=timezone.now,
        verbose_name='操作时间'
    )
    
    class Meta:
        verbose_name = '系统日志'
        verbose_name_plural = '系统日志'
        db_table = 'logs_system_log'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'created_at']),
            models.Index(fields=['action_type', 'created_at']),
            models.Index(fields=['resource_type', 'created_at']),
            models.Index(fields=['campus', 'created_at']),
        ]
    
    def __str__(self):
        user_name = self.user.real_name if self.user and self.user.real_name else (self.user.username if self.user else '系统')
        return f"{user_name} - {self.get_action_type_display()} - {self.description}"
    
    @classmethod
    def create_log(cls, user=None, action_type='other', resource_type='other', 
                   resource_id=None, resource_name=None, description='', 
                   ip_address=None, user_agent=None, extra_data=None, campus=None):
        """创建系统日志的便捷方法"""
        # 如果用户有校区信息且没有指定校区，自动设置校区
        if user and not campus:
            # 对于校区管理员，使用其管理的校区
            if user.user_type == 'campus_admin':
                managed_campus = user.managed_campus.first()
                if managed_campus:
                    campus = managed_campus
            # 对于学员，使用其所属的校区
            elif user.user_type == 'student':
                student_campus = user.campus_memberships.filter(is_active=True).first()
                if student_campus:
                    campus = student_campus.campus
            # 对于教练，使用其工作的校区
            elif user.user_type == 'coach':
                coach_campus = user.campus_assignments.filter(is_active=True).first()
                if coach_campus:
                    campus = coach_campus.campus
        
        return cls.objects.create(
            user=user,
            action_type=action_type,
            resource_type=resource_type,
            resource_id=str(resource_id) if resource_id else None,
            resource_name=resource_name,
            description=description,
            ip_address=ip_address,
            user_agent=user_agent,
            extra_data=extra_data or {},
            campus=campus
        )


class LoginLog(models.Model):
    """登录日志模型"""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='login_logs',
        verbose_name='用户'
    )
    login_time = models.DateTimeField(
        default=timezone.now,
        verbose_name='登录时间'
    )
    logout_time = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='登出时间'
    )
    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True,
        verbose_name='IP地址'
    )
    user_agent = models.TextField(
        null=True,
        blank=True,
        verbose_name='用户代理'
    )
    session_key = models.CharField(
        max_length=40,
        null=True,
        blank=True,
        verbose_name='会话密钥'
    )
    is_successful = models.BooleanField(
        default=True,
        verbose_name='是否成功'
    )
    failure_reason = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        verbose_name='失败原因'
    )
    
    class Meta:
        verbose_name = '登录日志'
        verbose_name_plural = '登录日志'
        db_table = 'logs_login_log'
        ordering = ['-login_time']
        indexes = [
            models.Index(fields=['user', 'login_time']),
            models.Index(fields=['ip_address', 'login_time']),
        ]
    
    def __str__(self):
        status = '成功' if self.is_successful else '失败'
        user_name = self.user.real_name if self.user.real_name else self.user.username
        return f"{user_name} - {self.login_time.strftime('%Y-%m-%d %H:%M:%S')} - {status}"
    
    @property
    def session_duration(self):
        """会话持续时间"""
        if self.logout_time:
            return self.logout_time - self.login_time
        return None