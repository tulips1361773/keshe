from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    """消息通知序列化器"""
    sender_name = serializers.SerializerMethodField()
    recipient_name = serializers.CharField(source='recipient.username', read_only=True)
    message_type_display = serializers.CharField(source='get_message_type_display', read_only=True)
    
    class Meta:
        model = Notification
        fields = [
            'id', 'recipient', 'recipient_name', 'sender', 'sender_name',
            'title', 'message', 'message_type', 'message_type_display',
            'is_read', 'data', 'created_at', 'read_at'
        ]
        read_only_fields = ['id', 'created_at', 'read_at']
    
    def get_sender_name(self, obj):
        """获取发送人姓名"""
        if obj.sender:
            return getattr(obj.sender, 'real_name', None) or obj.sender.username
        return '系统'


class NotificationCreateSerializer(serializers.ModelSerializer):
    """消息通知创建序列化器"""
    
    class Meta:
        model = Notification
        fields = ['recipient', 'title', 'message', 'message_type', 'data']
    
    def validate_recipient(self, value):
        """验证接收人"""
        if not value.is_active:
            raise serializers.ValidationError('接收人账户未激活')
        return value
    
    def create(self, validated_data):
        """创建通知"""
        # 设置发送人为当前用户（如果有的话）
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            validated_data['sender'] = request.user
        
        return super().create(validated_data)


class NotificationStatsSerializer(serializers.Serializer):
    """消息统计序列化器"""
    total = serializers.IntegerField()
    unread = serializers.IntegerField()
    system = serializers.IntegerField()
    booking = serializers.IntegerField()
    payment = serializers.IntegerField()
    competition = serializers.IntegerField()
    evaluation = serializers.IntegerField()


class BulkNotificationSerializer(serializers.Serializer):
    """批量通知序列化器"""
    recipients = serializers.ListField(
        child=serializers.IntegerField(),
        help_text='接收人ID列表'
    )
    title = serializers.CharField(max_length=200)
    message = serializers.CharField()
    message_type = serializers.ChoiceField(
        choices=Notification.MESSAGE_TYPES,
        default='system'
    )
    data = serializers.JSONField(required=False, allow_null=True)
    
    def validate_recipients(self, value):
        """验证接收人列表"""
        if not value:
            raise serializers.ValidationError('接收人列表不能为空')
        
        # 检查用户是否存在且激活
        users = User.objects.filter(id__in=value, is_active=True)
        if users.count() != len(value):
            raise serializers.ValidationError('部分接收人不存在或未激活')
        
        return value
    
    def create(self, validated_data):
        """批量创建通知"""
        recipients = validated_data.pop('recipients')
        request = self.context.get('request')
        sender = request.user if request and request.user.is_authenticated else None
        
        notifications = []
        for recipient_id in recipients:
            notification = Notification(
                recipient_id=recipient_id,
                sender=sender,
                **validated_data
            )
            notifications.append(notification)
        
        return Notification.objects.bulk_create(notifications)