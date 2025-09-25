from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.conf import settings


class Notification(models.Model):
    """消息通知模型"""
    MESSAGE_TYPES = [
        ('system', '系统消息'),
        ('booking', '预约消息'),
        ('payment', '支付消息'),
        ('competition', '比赛消息'),
        ('evaluation', '评价消息'),
    ]
    
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='received_notifications',
        verbose_name='接收人'
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='sent_notifications',
        verbose_name='发送人'
    )
    title = models.CharField(max_length=200, verbose_name='消息标题')
    message = models.TextField(verbose_name='消息内容')
    message_type = models.CharField(
        max_length=20, 
        choices=MESSAGE_TYPES, 
        default='system',
        verbose_name='消息类型'
    )
    is_read = models.BooleanField(default=False, verbose_name='是否已读')
    data = models.JSONField(null=True, blank=True, verbose_name='附加数据')
    created_at = models.DateTimeField(default=timezone.now, verbose_name='创建时间')
    read_at = models.DateTimeField(null=True, blank=True, verbose_name='阅读时间')
    
    class Meta:
        db_table = 'notifications'
        verbose_name = '消息通知'
        verbose_name_plural = '消息通知'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['recipient', 'is_read']),
            models.Index(fields=['message_type']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f'{self.title} - {self.recipient.username}'
    
    def mark_as_read(self):
        """标记为已读"""
        if not self.is_read:
            self.is_read = True
            self.read_at = timezone.now()
            self.save(update_fields=['is_read', 'read_at'])
    
    @classmethod
    def create_notification(cls, recipient, title, message, message_type='system', sender=None, data=None):
        """创建通知的便捷方法"""
        return cls.objects.create(
            recipient=recipient,
            sender=sender,
            title=title,
            message=message,
            message_type=message_type,
            data=data
        )
    
    @classmethod
    def create_system_notification(cls, recipient, title, message, data=None):
        """创建系统通知"""
        return cls.create_notification(
            recipient=recipient,
            title=title,
            message=message,
            message_type='system',
            data=data
        )
    
    @classmethod
    def create_booking_notification(cls, recipient, title, message, sender=None, data=None):
        """创建预约通知"""
        return cls.create_notification(
            recipient=recipient,
            title=title,
            message=message,
            message_type='booking',
            sender=sender,
            data=data
        )
    
    @classmethod
    def create_payment_notification(cls, recipient, title, message, sender=None, data=None):
        """创建支付通知"""
        return cls.create_notification(
            recipient=recipient,
            title=title,
            message=message,
            message_type='payment',
            sender=sender,
            data=data
        )
    
    @classmethod
    def get_unread_count(cls, user):
        """获取用户未读消息数量"""
        return cls.objects.filter(recipient=user, is_read=False).count()
    
    @classmethod
    def get_stats(cls, user):
        """获取用户消息统计"""
        queryset = cls.objects.filter(recipient=user)
        return {
            'total': queryset.count(),
            'unread': queryset.filter(is_read=False).count(),
            'system': queryset.filter(message_type='system').count(),
            'booking': queryset.filter(message_type='booking').count(),
            'payment': queryset.filter(message_type='payment').count(),
            'competition': queryset.filter(message_type='competition').count(),
            'evaluation': queryset.filter(message_type='evaluation').count(),
        }
