from django.contrib import admin
from .models import Table, Booking, CoachStudentRelation


@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    """球台管理"""
    list_display = ('campus', 'number', 'name', 'status', 'is_active', 'created_at')
    list_filter = ('campus', 'status', 'is_active', 'created_at')
    search_fields = ('number', 'name', 'description')
    ordering = ('campus', 'number')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('基本信息', {
            'fields': ('campus', 'number', 'name', 'description')
        }),
        ('状态设置', {
            'fields': ('status', 'is_active')
        }),
        ('时间信息', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def get_queryset(self, request):
        """根据用户权限过滤球台"""
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        # 校区管理员只能看到自己校区的球台
        if hasattr(request.user, 'managed_campus'):
            return qs.filter(campus=request.user.managed_campus)
        return qs.none()


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    """预约管理"""
    list_display = ('relation', 'table', 'start_time', 'end_time', 'status', 'total_fee', 'created_at')
    list_filter = ('status', 'table__campus', 'start_time', 'created_at')
    search_fields = ('relation__student__username', 'relation__coach__username', 'table__number')
    ordering = ('-start_time',)
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('预约信息', {
            'fields': ('relation', 'table', 'start_time', 'end_time', 'duration_hours')
        }),
        ('费用信息', {
            'fields': ('total_fee', 'payment_status')
        }),
        ('状态信息', {
            'fields': ('status', 'notes')
        }),
        ('时间信息', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )


@admin.register(CoachStudentRelation)
class CoachStudentRelationAdmin(admin.ModelAdmin):
    """师生关系管理"""
    list_display = ('coach', 'student', 'status', 'applied_by', 'applied_at', 'processed_at')
    list_filter = ('status', 'applied_by', 'applied_at', 'processed_at')
    search_fields = ('coach__username', 'student__username', 'coach__real_name', 'student__real_name')
    ordering = ('-applied_at',)
    readonly_fields = ('applied_at', 'processed_at')
    
    fieldsets = (
        ('关系信息', {
            'fields': ('coach', 'student', 'status')
        }),
        ('申请信息', {
            'fields': ('applied_by', 'applied_at', 'processed_at')
        })
    )
