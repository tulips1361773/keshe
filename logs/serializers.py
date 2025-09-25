from rest_framework import serializers
from .models import SystemLog, LoginLog


class SystemLogSerializer(serializers.ModelSerializer):
    """系统日志序列化器"""
    user_name = serializers.SerializerMethodField()
    action_type_display = serializers.CharField(source='get_action_type_display', read_only=True)
    resource_type_display = serializers.CharField(source='get_resource_type_display', read_only=True)
    campus_name = serializers.CharField(source='campus.name', read_only=True)
    
    class Meta:
        model = SystemLog
        fields = [
            'id', 'user', 'user_name', 'action_type', 'action_type_display',
            'resource_type', 'resource_type_display', 'resource_id', 'resource_name',
            'description', 'ip_address', 'user_agent', 'extra_data',
            'campus', 'campus_name', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']
    
    def get_user_name(self, obj):
        if obj.user:
            return obj.user.real_name or obj.user.username
        return '系统'


class LoginLogSerializer(serializers.ModelSerializer):
    """登录日志序列化器"""
    user_name = serializers.SerializerMethodField()
    session_duration = serializers.SerializerMethodField()
    
    class Meta:
        model = LoginLog
        fields = [
            'id', 'user', 'user_name', 'login_time', 'logout_time',
            'ip_address', 'user_agent', 'session_key', 'is_successful',
            'failure_reason', 'session_duration'
        ]
        read_only_fields = ['id']
    
    def get_user_name(self, obj):
        return obj.user.real_name or obj.user.username
    
    def get_session_duration(self, obj):
        duration = obj.session_duration
        if duration:
            total_seconds = int(duration.total_seconds())
            hours = total_seconds // 3600
            minutes = (total_seconds % 3600) // 60
            seconds = total_seconds % 60
            return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        return None