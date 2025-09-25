from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.contrib import messages
from django.db import transaction, models
from .models import Table, Booking, CoachStudentRelation
from .coach_change_models import CoachChangeRequest
from logs.utils import log_user_action


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


@admin.register(CoachChangeRequest)
class CoachChangeRequestAdmin(admin.ModelAdmin):
    """教练更换申请管理"""
    list_display = (
        'id', 'student', 'current_coach', 'target_coach', 'status', 
        'current_coach_approval_display', 'target_coach_approval_display', 
        'campus_admin_approval_display', 'created_at'
    )
    list_filter = (
        'status', 'current_coach_approval', 'target_coach_approval', 
        'campus_admin_approval', 'created_at'
    )
    search_fields = (
        'student__username', 'student__real_name',
        'current_coach__username', 'current_coach__real_name',
        'target_coach__username', 'target_coach__real_name',
        'reason'
    )
    ordering = ('-created_at',)
    readonly_fields = (
        'created_at', 'updated_at', 'processed_at', 'processed_by',
        'current_coach_approved_at', 'current_coach_approved_by',
        'target_coach_approved_at', 'target_coach_approved_by',
        'campus_admin_approved_at', 'campus_admin_approved_by'
    )
    
    fieldsets = (
        ('基本信息', {
            'fields': ('student', 'current_coach', 'target_coach', 'reason')
        }),
        ('当前教练审核', {
            'fields': (
                'current_coach_approval', 'current_coach_notes',
                'current_coach_approved_by', 'current_coach_approved_at'
            )
        }),
        ('目标教练审核', {
            'fields': (
                'target_coach_approval', 'target_coach_notes',
                'target_coach_approved_by', 'target_coach_approved_at'
            )
        }),
        ('校区管理员审核', {
            'fields': (
                'campus_admin_approval', 'campus_admin_notes',
                'campus_admin_approved_by', 'campus_admin_approved_at'
            )
        }),
        ('状态信息', {
            'fields': ('status', 'processed_by', 'processed_at')
        }),
        ('时间信息', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    actions = ['approve_by_admin', 'reject_by_admin']
    
    def current_coach_approval_display(self, obj):
        """显示当前教练审核状态"""
        status_colors = {
            'pending': 'orange',
            'approved': 'green',
            'rejected': 'red'
        }
        status_text = {
            'pending': '待审核',
            'approved': '已通过',
            'rejected': '已拒绝'
        }
        color = status_colors.get(obj.current_coach_approval, 'gray')
        text = status_text.get(obj.current_coach_approval, obj.current_coach_approval)
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color, text
        )
    current_coach_approval_display.short_description = '当前教练审核'
    
    def target_coach_approval_display(self, obj):
        """显示目标教练审核状态"""
        status_colors = {
            'pending': 'orange',
            'approved': 'green',
            'rejected': 'red'
        }
        status_text = {
            'pending': '待审核',
            'approved': '已通过',
            'rejected': '已拒绝'
        }
        color = status_colors.get(obj.target_coach_approval, 'gray')
        text = status_text.get(obj.target_coach_approval, obj.target_coach_approval)
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color, text
        )
    target_coach_approval_display.short_description = '目标教练审核'
    
    def campus_admin_approval_display(self, obj):
        """显示校区管理员审核状态"""
        status_colors = {
            'pending': 'orange',
            'approved': 'green',
            'rejected': 'red'
        }
        status_text = {
            'pending': '待审核',
            'approved': '已通过',
            'rejected': '已拒绝'
        }
        color = status_colors.get(obj.campus_admin_approval, 'gray')
        text = status_text.get(obj.campus_admin_approval, obj.campus_admin_approval)
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color, text
        )
    campus_admin_approval_display.short_description = '校区管理员审核'
    
    def approve_by_admin(self, request, queryset):
        """批量通过申请（管理员操作）"""
        approved_count = 0
        failed_count = 0
        
        for obj in queryset:
            try:
                with transaction.atomic():
                    # 只有校区管理员或超级管理员可以审核
                    if not (request.user.is_superuser or 
                           (request.user.user_type == 'campus_admin' and 
                            obj.student.campus == request.user.managed_campus)):
                        failed_count += 1
                        continue
                    
                    # 使用模型的审核方法
                    if obj.campus_admin_approval == 'pending':
                        obj.approve_by_campus_admin(request.user, "管理员批量审核通过")
                        approved_count += 1
                        
                        # 记录操作日志
                        log_user_action(
                            user=request.user,
                            action_type='approve',
                            resource_type='coach_change_request',
                            resource_id=obj.id,
                            description=f'管理员批量审核通过教练更换申请: 学员 {obj.student.username} 从 {obj.current_coach.username} 更换到 {obj.target_coach.username}',
                            request=request
                        )
                    else:
                        failed_count += 1
                        
            except Exception as e:
                failed_count += 1
                messages.error(request, f'审核申请 {obj.id} 失败: {str(e)}')
        
        if approved_count > 0:
            messages.success(request, f'成功审核通过 {approved_count} 个申请')
        if failed_count > 0:
            messages.warning(request, f'{failed_count} 个申请审核失败')
    
    approve_by_admin.short_description = "批量通过选中的申请"
    
    def reject_by_admin(self, request, queryset):
        """批量拒绝申请（管理员操作）"""
        rejected_count = 0
        failed_count = 0
        
        for obj in queryset:
            try:
                with transaction.atomic():
                    # 只有校区管理员或超级管理员可以审核
                    if not (request.user.is_superuser or 
                           (request.user.user_type == 'campus_admin' and 
                            obj.student.campus == request.user.managed_campus)):
                        failed_count += 1
                        continue
                    
                    # 使用模型的审核方法
                    if obj.campus_admin_approval == 'pending':
                        obj.reject_by_campus_admin(request.user, "管理员批量审核拒绝")
                        rejected_count += 1
                        
                        # 记录操作日志
                        log_user_action(
                            user=request.user,
                            action_type='reject',
                            resource_type='coach_change_request',
                            resource_id=obj.id,
                            description=f'管理员批量审核拒绝教练更换申请: 学员 {obj.student.username} 从 {obj.current_coach.username} 更换到 {obj.target_coach.username}',
                            request=request
                        )
                    else:
                        failed_count += 1
                        
            except Exception as e:
                failed_count += 1
                messages.error(request, f'审核申请 {obj.id} 失败: {str(e)}')
        
        if rejected_count > 0:
            messages.success(request, f'成功拒绝 {rejected_count} 个申请')
        if failed_count > 0:
            messages.warning(request, f'{failed_count} 个申请审核失败')
    
    reject_by_admin.short_description = "批量拒绝选中的申请"
    
    def get_queryset(self, request):
        """根据用户权限过滤教练更换申请"""
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        # 校区管理员只能看到自己校区学员的申请
        if hasattr(request.user, 'managed_campus') and request.user.user_type == 'campus_admin':
            return qs.filter(student__campus=request.user.managed_campus)
        return qs.none()
    
    def save_model(self, request, obj, form, change):
        """保存教练更换申请时记录日志"""
        action_type = 'update' if change else 'create'
        
        # 如果是管理员在修改审核状态
        if change and (request.user.user_type in ['campus_admin', 'super_admin'] or request.user.is_superuser):
            original = CoachChangeRequest.objects.get(pk=obj.pk)
            
            # 检查是否修改了校区管理员审核状态
            if (original.campus_admin_approval != obj.campus_admin_approval and 
                obj.campus_admin_approval in ['approved', 'rejected']):
                
                # 使用模型的审核方法而不是直接保存
                try:
                    if obj.campus_admin_approval == 'approved':
                        original.approve_by_campus_admin(
                            request.user, 
                            obj.campus_admin_notes or "管理员审核通过"
                        )
                    else:
                        original.reject_by_campus_admin(
                            request.user, 
                            obj.campus_admin_notes or "管理员审核拒绝"
                        )
                    
                    # 记录操作日志
                    log_user_action(
                        user=request.user,
                        action_type='approve' if obj.campus_admin_approval == 'approved' else 'reject',
                        resource_type='coach_change_request',
                        resource_id=obj.id,
                        description=f'管理员{"通过" if obj.campus_admin_approval == "approved" else "拒绝"}教练更换申请: 学员 {obj.student.username} 从 {obj.current_coach.username} 更换到 {obj.target_coach.username}',
                        request=request
                    )
                    return  # 不需要调用super().save_model
                    
                except Exception as e:
                    messages.error(request, f'审核操作失败: {str(e)}')
                    return
        
        # 对于管理员界面的其他修改，允许保护字段更新
        if change and (request.user.user_type in ['campus_admin', 'super_admin'] or request.user.is_superuser):
            obj.save(allow_protected_update=True)
            
            # 记录普通操作日志
            log_user_action(
                user=request.user,
                action_type='update',
                resource_type='coach_change_request',
                resource_id=obj.id,
                description=f'管理员更新教练更换申请: 学员 {obj.student.username} 从 {obj.current_coach.username} 更换到 {obj.target_coach.username}',
                request=request
            )
        else:
            super().save_model(request, obj, form, change)
            
            # 记录普通操作日志
            if action_type == 'create':
                log_user_action(
                    user=request.user,
                    action_type=action_type,
                    resource_type='coach_change_request',
                    resource_id=obj.id,
                    description=f'{"更新" if change else "创建"}教练更换申请: 学员 {obj.student.username} 从 {obj.current_coach.username} 更换到 {obj.target_coach.username}',
                    request=request
                )
    
    def get_queryset(self, request):
        """根据用户权限过滤教练更换申请"""
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        # 校区管理员只能看到自己校区学员的申请
        if hasattr(request.user, 'managed_campus') and request.user.user_type == 'campus_admin':
            return qs.filter(student__campus=request.user.managed_campus)
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
    list_display = ('id', 'coach_display', 'student_display', 'status_display', 'applied_by_display', 'applied_at', 'processed_at')
    list_filter = ('status', 'applied_by', 'applied_at', 'processed_at')
    search_fields = ('coach__username', 'student__username', 'coach__real_name', 'student__real_name')
    ordering = ('-applied_at',)
    readonly_fields = ('applied_at', 'processed_at', 'terminated_at', 'created_at')
    
    fieldsets = (
        ('关系信息', {
            'fields': ('coach', 'student', 'status')
        }),
        ('申请信息', {
            'fields': ('applied_by', 'applied_at', 'processed_at', 'terminated_at')
        }),
        ('其他信息', {
            'fields': ('notes', 'created_at'),
            'classes': ('collapse',)
        })
    )
    
    def coach_display(self, obj):
        """显示教练信息"""
        if obj.coach:
            # 获取教练所属校区
            coach_campus = None
            if hasattr(obj.coach, 'campus_assignments') and obj.coach.campus_assignments.exists():
                coach_campus = obj.coach.campus_assignments.first().campus.name
            campus_info = f" ({coach_campus})" if coach_campus else " (未分配校区)"
            return f"{obj.coach.real_name or obj.coach.username}{campus_info}"
        return "无"
    coach_display.short_description = "教练"
    
    def student_display(self, obj):
        """显示学员信息"""
        if obj.student:
            # 获取学员所属校区
            student_campus = None
            if hasattr(obj.student, 'campus_memberships') and obj.student.campus_memberships.exists():
                student_campus = obj.student.campus_memberships.first().campus.name
            campus_info = f" ({student_campus})" if student_campus else " (未分配校区)"
            return f"{obj.student.real_name or obj.student.username}{campus_info}"
        return "无"
    student_display.short_description = "学员"
    
    def status_display(self, obj):
        """显示状态"""
        status_colors = {
            'pending': '#ffc107',  # 黄色
            'approved': '#28a745',  # 绿色
            'rejected': '#dc3545',  # 红色
            'terminated': '#6c757d'  # 灰色
        }
        color = status_colors.get(obj.status, '#000')
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color,
            obj.get_status_display()
        )
    status_display.short_description = "状态"
    
    def applied_by_display(self, obj):
        """显示申请方"""
        return obj.get_applied_by_display()
    applied_by_display.short_description = "申请方"
    
    def save_model(self, request, obj, form, change):
        """保存师生关系时记录日志"""
        action_type = 'update' if change else 'create'
        super().save_model(request, obj, form, change)
        
        # 记录操作日志
        description = f'{"更新" if change else "创建"}师生关系: {obj.coach.real_name or obj.coach.username} - {obj.student.real_name or obj.student.username} (状态: {obj.get_status_display()})'
        log_user_action(
            user=request.user,
            action_type=action_type,
            resource_type='coach_student_relation',
            resource_id=obj.id,
            description=description,
            request=request
        )
    
    def delete_model(self, request, obj):
        """删除师生关系时记录日志"""
        relation_info = f'{obj.coach.real_name or obj.coach.username} - {obj.student.real_name or obj.student.username}'
        relation_id = obj.id
        super().delete_model(request, obj)
        
        # 记录删除日志
        log_user_action(
            user=request.user,
            action_type='delete',
            resource_type='coach_student_relation',
            resource_id=relation_id,
            description=f'删除师生关系: {relation_info}',
            request=request
        )
    
    def get_queryset(self, request):
        """根据用户权限过滤师生关系"""
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        # 校区管理员只能看到自己校区的师生关系
        if hasattr(request.user, 'managed_campus') and request.user.user_type == 'campus_admin':
            managed_campus = request.user.managed_campus.first()
            if managed_campus:
                return qs.filter(
                    models.Q(coach__campus_assignments__campus=managed_campus) |
                    models.Q(student__campus_memberships__campus=managed_campus)
                )
        return qs.none()
