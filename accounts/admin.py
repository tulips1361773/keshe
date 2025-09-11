from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User, UserProfile


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