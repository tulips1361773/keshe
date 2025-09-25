from django.contrib import admin
from .models import Campus, CampusArea, CampusStudent, CampusCoach


@admin.register(Campus)
class CampusAdmin(admin.ModelAdmin):
    """校区管理"""
    list_display = ('name', 'code', 'manager', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at', 'updated_at')
    search_fields = ('name', 'code', 'address', 'manager__username')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('基本信息', {
            'fields': ('name', 'code', 'description')
        }),
        ('联系信息', {
            'fields': ('address', 'phone', 'email')
        }),
        ('管理信息', {
            'fields': ('manager', 'is_active')
        }),
        ('时间信息', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def get_queryset(self, request):
        """根据用户权限过滤校区"""
        qs = super().get_queryset(request)
        if request.user.is_superuser or request.user.is_super_admin:
            return qs
        # 普通管理员只能看到自己管理的校区
        return qs.filter(manager=request.user)


@admin.register(CampusArea)
class CampusAreaAdmin(admin.ModelAdmin):
    """校区分区管理"""
    list_display = ('name', 'campus', 'area_type', 'capacity', 'is_available')
    list_filter = ('area_type', 'is_available', 'campus')
    search_fields = ('name', 'campus__name', 'description')
    ordering = ('campus', 'name')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('基本信息', {
            'fields': ('campus', 'name', 'area_type', 'description')
        }),
        ('容量信息', {
            'fields': ('capacity', 'equipment_list', 'is_available')
        }),
        ('时间信息', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def get_queryset(self, request):
        """根据用户权限过滤分区"""
        qs = super().get_queryset(request)
        if request.user.is_superuser or request.user.is_super_admin:
            return qs
        # 普通管理员只能看到自己管理校区的分区
        return qs.filter(campus__manager=request.user)


class CampusStudentInline(admin.TabularInline):
    """校区学员内联"""
    model = CampusStudent
    extra = 0
    readonly_fields = ('enrollment_date', 'created_at')
    fields = ('student', 'is_active', 'enrollment_date', 'notes')


class CampusCoachInline(admin.TabularInline):
    """校区教练内联"""
    model = CampusCoach
    extra = 0
    readonly_fields = ('hire_date', 'created_at')
    fields = ('coach', 'is_active', 'hire_date', 'notes')


@admin.register(CampusStudent)
class CampusStudentAdmin(admin.ModelAdmin):
    """校区学员管理"""
    list_display = ('student', 'campus', 'is_active', 'enrollment_date')
    list_filter = ('is_active', 'campus', 'enrollment_date')
    search_fields = ('student__username', 'student__first_name', 'student__last_name', 'campus__name')
    ordering = ('-enrollment_date',)
    readonly_fields = ('enrollment_date', 'created_at')
    
    fieldsets = (
        ('关联信息', {
            'fields': ('campus', 'student')
        }),
        ('状态信息', {
            'fields': ('is_active', 'enrollment_date', 'notes')
        }),
        ('时间信息', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        })
    )
    
    def get_queryset(self, request):
        """根据用户权限过滤学员"""
        qs = super().get_queryset(request)
        if request.user.is_superuser or request.user.is_super_admin:
            return qs
        # 普通管理员只能看到自己管理校区的学员
        return qs.filter(campus__manager=request.user)


@admin.register(CampusCoach)
class CampusCoachAdmin(admin.ModelAdmin):
    """校区教练管理"""
    list_display = ('coach', 'campus', 'is_active', 'hire_date')
    list_filter = ('is_active', 'campus', 'hire_date')
    search_fields = ('coach__username', 'coach__first_name', 'coach__last_name', 'campus__name')
    ordering = ('-hire_date',)
    readonly_fields = ('hire_date', 'created_at')
    
    fieldsets = (
        ('关联信息', {
            'fields': ('campus', 'coach')
        }),
        ('职业信息', {
            'fields': ('specialties', 'max_students', 'hourly_rate')
        }),
        ('状态信息', {
            'fields': ('is_active', 'hire_date', 'notes')
        }),
        ('时间信息', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        })
    )
    
    def get_queryset(self, request):
        """根据用户权限过滤教练"""
        qs = super().get_queryset(request)
        if request.user.is_superuser or request.user.is_super_admin:
            return qs
        # 普通管理员只能看到自己管理校区的教练
        return qs.filter(campus__manager=request.user)


# 将内联添加到Campus管理中
CampusAdmin.inlines = [CampusStudentInline, CampusCoachInline]