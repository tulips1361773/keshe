from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
import json
from .models import SystemLog, LoginLog


@admin.register(SystemLog)
class SystemLogAdmin(admin.ModelAdmin):
    """系统日志管理"""
    list_display = [
        'id', 'user_link', 'action_type_badge', 'resource_type_badge',
        'resource_name', 'description_short', 'campus_link', 'created_at'
    ]
    list_filter = [
        'action_type', 'resource_type', 'campus', 'created_at',
        ('user', admin.RelatedOnlyFieldListFilter),
    ]
    search_fields = [
        'user__username', 'user__real_name', 'description',
        'resource_name', 'ip_address'
    ]
    readonly_fields = [
        'user', 'action_type', 'resource_type', 'resource_id',
        'resource_name', 'description', 'ip_address', 'user_agent',
        'extra_data_formatted', 'campus', 'created_at'
    ]
    date_hierarchy = 'created_at'
    ordering = ['-created_at']
    list_per_page = 50
    
    def get_queryset(self, request):
        """根据用户权限过滤日志"""
        qs = super().get_queryset(request)
        if request.user.is_super_admin:
            return qs
        elif request.user.is_campus_admin and request.user.campus:
            return qs.filter(campus=request.user.campus)
        else:
            return qs.filter(user=request.user)
    
    def user_link(self, obj):
        """用户链接"""
        if obj.user:
            url = reverse('admin:accounts_user_change', args=[obj.user.pk])
            name = obj.user.real_name or obj.user.username
            return format_html('<a href="{}">{}</a>', url, name)
        return '系统'
    user_link.short_description = '操作用户'
    
    def campus_link(self, obj):
        """校区链接"""
        if obj.campus:
            url = reverse('admin:campus_campus_change', args=[obj.campus.pk])
            return format_html('<a href="{}">{}</a>', url, obj.campus.name)
        return '-'
    campus_link.short_description = '所属校区'
    
    def action_type_badge(self, obj):
        """操作类型徽章"""
        color_map = {
            'create': 'success',
            'update': 'info',
            'delete': 'danger',
            'login': 'primary',
            'logout': 'secondary',
            'approve': 'success',
            'reject': 'warning',
            'cancel': 'warning',
            'confirm': 'info',
            'payment': 'success',
            'refund': 'warning',
            'register': 'primary',
            'other': 'secondary',
        }
        color = color_map.get(obj.action_type, 'secondary')
        return format_html(
            '<span class="badge badge-{}">{}</span>',
            color, obj.get_action_type_display()
        )
    action_type_badge.short_description = '操作类型'
    
    def resource_type_badge(self, obj):
        """资源类型徽章"""
        return format_html(
            '<span class="badge badge-outline-primary">{}</span>',
            obj.get_resource_type_display()
        )
    resource_type_badge.short_description = '资源类型'
    
    def description_short(self, obj):
        """简短描述"""
        if len(obj.description) > 50:
            return obj.description[:50] + '...'
        return obj.description
    description_short.short_description = '操作描述'
    
    def extra_data_formatted(self, obj):
        """格式化额外数据"""
        if obj.extra_data:
            return format_html(
                '<pre>{}</pre>',
                json.dumps(obj.extra_data, indent=2, ensure_ascii=False)
            )
        return '-'
    extra_data_formatted.short_description = '额外数据'
    
    def has_add_permission(self, request):
        """禁止添加日志"""
        return False
    
    def has_change_permission(self, request, obj=None):
        """禁止修改日志"""
        return False
    
    def has_delete_permission(self, request, obj=None):
        """只有超级管理员可以删除日志"""
        return request.user.is_super_admin


@admin.register(LoginLog)
class LoginLogAdmin(admin.ModelAdmin):
    """登录日志管理"""
    list_display = [
        'id', 'user_link', 'login_time', 'logout_time',
        'session_duration_display', 'ip_address', 'status_badge'
    ]
    list_filter = [
        'is_successful', 'login_time', 'logout_time',
        ('user', admin.RelatedOnlyFieldListFilter),
    ]
    search_fields = [
        'user__username', 'user__real_name', 'ip_address',
        'user_agent', 'failure_reason'
    ]
    readonly_fields = [
        'user', 'login_time', 'logout_time', 'ip_address',
        'user_agent', 'session_key', 'is_successful', 'failure_reason'
    ]
    date_hierarchy = 'login_time'
    ordering = ['-login_time']
    list_per_page = 50
    
    def get_queryset(self, request):
        """根据用户权限过滤登录日志"""
        qs = super().get_queryset(request)
        if request.user.is_super_admin:
            return qs
        elif request.user.is_campus_admin and request.user.campus:
            campus_users = request.user.campus.users.all()
            return qs.filter(user__in=campus_users)
        else:
            return qs.filter(user=request.user)
    
    def user_link(self, obj):
        """用户链接"""
        url = reverse('admin:accounts_user_change', args=[obj.user.pk])
        name = obj.user.real_name or obj.user.username
        return format_html('<a href="{}">{}</a>', url, name)
    user_link.short_description = '用户'
    
    def status_badge(self, obj):
        """状态徽章"""
        if obj.is_successful:
            return format_html('<span class="badge badge-success">成功</span>')
        else:
            return format_html(
                '<span class="badge badge-danger" title="{}">失败</span>',
                obj.failure_reason or '未知原因'
            )
    status_badge.short_description = '登录状态'
    
    def session_duration_display(self, obj):
        """会话持续时间显示"""
        duration = obj.session_duration
        if duration:
            total_seconds = int(duration.total_seconds())
            hours = total_seconds // 3600
            minutes = (total_seconds % 3600) // 60
            return f"{hours}小时{minutes}分钟"
        return '-'
    session_duration_display.short_description = '会话时长'
    
    def has_add_permission(self, request):
        """禁止添加登录日志"""
        return False
    
    def has_change_permission(self, request, obj=None):
        """禁止修改登录日志"""
        return False
    
    def has_delete_permission(self, request, obj=None):
        """只有超级管理员可以删除登录日志"""
        return request.user.is_super_admin