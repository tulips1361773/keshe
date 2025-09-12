from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User, UserProfile, Coach


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = '用户资料'


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)
    list_display = ('username', 'real_name', 'phone', 'user_type', 'is_active', 'registration_date')
    list_filter = ('user_type', 'is_active', 'is_staff', 'registration_date')
    search_fields = ('username', 'real_name', 'phone', 'email')
    ordering = ('-registration_date',)
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('个人信息'), {'fields': ('real_name', 'phone', 'email', 'avatar', 'gender', 'birth_date', 'id_card')}),
        (_('联系信息'), {'fields': ('address', 'emergency_contact', 'emergency_phone')}),
        (_('权限'), {'fields': ('user_type', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('重要日期'), {'fields': ('last_login', 'date_joined', 'registration_date')}),
        (_('其他信息'), {'fields': ('is_active_member', 'last_login_ip')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'real_name', 'phone', 'user_type', 'password1', 'password2'),
        }),
    )
    
    readonly_fields = ('registration_date', 'last_login_ip')


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'experience_years', 'created_at', 'updated_at')
    list_filter = ('experience_years', 'created_at')
    search_fields = ('user__username', 'user__real_name', 'bio', 'skills')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Coach)
class CoachAdmin(admin.ModelAdmin):
    """教练员管理"""
    list_display = ('user', 'coach_level', 'status', 'hourly_rate', 'approved_by', 'created_at')
    list_filter = ('status', 'coach_level', 'created_at', 'approved_at')
    search_fields = ('user__username', 'user__real_name', 'user__phone', 'achievements')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at', 'approved_at')
    
    fieldsets = (
        ('基本信息', {
            'fields': ('user', 'coach_level', 'hourly_rate', 'max_students')
        }),
        ('成绩描述', {
            'fields': ('achievements',)
        }),
        ('审核信息', {
            'fields': ('status', 'approved_by', 'approved_at')
        }),
        ('时间信息', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def get_queryset(self, request):
        """根据用户权限过滤教练"""
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        # 校区管理员只能看到自己校区的教练
        if request.user.user_type == 'campus_admin':
            return qs.filter(user__campus=request.user.campus)
        return qs
    
    def save_model(self, request, obj, form, change):
        """保存教练模型时的自定义逻辑"""
        if change:  # 如果是更新操作
            # 记录审核人和审核时间
            if 'status' in form.changed_data:
                obj.approved_by = request.user
                from django.utils import timezone
                obj.approved_at = timezone.now()
                
                # 如果审核通过，激活用户账户并设置会员状态
                if obj.status == 'approved':
                    obj.user.is_active = True
                    obj.user.is_active_member = True  # 关键修复：设置会员激活状态
                    obj.user.save()
                    
                    # 记录审核日志
                    from django.contrib.admin.models import LogEntry, CHANGE
                    from django.contrib.contenttypes.models import ContentType
                    LogEntry.objects.log_action(
                        user_id=request.user.id,
                        content_type_id=ContentType.objects.get_for_model(obj.user).pk,
                        object_id=obj.user.pk,
                        object_repr=str(obj.user),
                        action_flag=CHANGE,
                        change_message=f'教练审核通过，激活用户账户和会员状态'
                    )
                elif obj.status == 'rejected':
                    # 如果审核拒绝，确保用户无法登录
                    obj.user.is_active_member = False
                    obj.user.save()
        
        super().save_model(request, obj, form, change)
    
    def has_change_permission(self, request, obj=None):
        """权限控制"""
        if request.user.is_superuser:
            return True
        if request.user.user_type == 'campus_admin':
            if obj and obj.user.campus != request.user.campus:
                return False
            return True
        return False