from django.contrib import admin
from logs.utils import log_user_action
from .models import (
    Competition, 
    CompetitionRegistration, 
    CompetitionGroup, 
    CompetitionGroupMember,
    CompetitionMatch, 
    CompetitionResult
)

@admin.register(Competition)
class CompetitionAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'campus', 'competition_date', 'status', 
        'total_registrations', 'registration_fee', 'created_by'
    ]
    list_filter = ['status', 'campus', 'competition_date', 'created_at']
    search_fields = ['title', 'description', 'campus__name']
    readonly_fields = ['created_at', 'updated_at', 'total_registrations']
    date_hierarchy = 'competition_date'
    
    fieldsets = (
        ('基本信息', {
            'fields': ('title', 'description', 'campus', 'created_by')
        }),
        ('时间设置', {
            'fields': ('competition_date', 'registration_start', 'registration_end')
        }),
        ('比赛设置', {
            'fields': ('registration_fee', 'max_participants_per_group', 'status')
        }),
        ('系统信息', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def save_model(self, request, obj, form, change):
        """保存比赛模型时记录日志"""
        action_type = 'update' if change else 'create'
        super().save_model(request, obj, form, change)
        
        # 记录操作日志
        description = f'{"更新" if change else "创建"}比赛: {obj.title} ({obj.campus.name})'
        log_user_action(
            user=request.user,
            action_type=action_type,
            resource_type='competition',
            resource_id=obj.id,
            description=description,
            request=request
        )
    
    def delete_model(self, request, obj):
        """删除比赛时记录日志"""
        competition_info = f'{obj.title} ({obj.campus.name})'
        competition_id = obj.id
        super().delete_model(request, obj)
        
        # 记录删除日志
        log_user_action(
            user=request.user,
            action_type='delete',
            resource_type='competition',
            resource_id=competition_id,
            description=f'删除比赛: {competition_info}',
            request=request
        )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('campus', 'created_by')

@admin.register(CompetitionRegistration)
class CompetitionRegistrationAdmin(admin.ModelAdmin):
    list_display = [
        'participant', 'competition', 'group', 'status', 
        'payment_status', 'registration_time'
    ]
    list_filter = ['status', 'group', 'payment_status', 'registration_time']
    search_fields = [
        'participant__username', 'participant__real_name', 
        'competition__title'
    ]
    readonly_fields = ['registration_time']
    
    fieldsets = (
        ('报名信息', {
            'fields': ('competition', 'participant', 'group')
        }),
        ('状态信息', {
            'fields': ('status', 'payment_status', 'registration_time')
        }),
        ('备注', {
            'fields': ('notes',)
        })
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'competition', 'participant'
        )

@admin.register(CompetitionGroup)
class CompetitionGroupAdmin(admin.ModelAdmin):
    list_display = ['group_name', 'competition', 'group_type', 'created_at']
    list_filter = ['group_type', 'created_at']
    search_fields = ['group_name', 'competition__title']
    readonly_fields = ['created_at']
    filter_horizontal = ['participants']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('competition')

@admin.register(CompetitionGroupMember)
class CompetitionGroupMemberAdmin(admin.ModelAdmin):
    list_display = ['group', 'participant', 'seed_number']
    list_filter = ['group__group_type']
    search_fields = ['participant__username', 'group__group_name']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'group', 'participant'
        )

@admin.register(CompetitionMatch)
class CompetitionMatchAdmin(admin.ModelAdmin):
    list_display = [
        'competition', 'player1', 'player2', 'match_type', 
        'round_number', 'status', 'winner', 'scheduled_time'
    ]
    list_filter = [
        'match_type', 'status', 'round_number', 
        'scheduled_time', 'competition'
    ]
    search_fields = [
        'player1__username', 'player2__username', 
        'competition__title'
    ]
    readonly_fields = ['created_at', 'duration']
    date_hierarchy = 'scheduled_time'
    
    fieldsets = (
        ('比赛信息', {
            'fields': ('competition', 'group', 'match_type', 'round_number')
        }),
        ('对战选手', {
            'fields': ('player1', 'player2')
        }),
        ('时间安排', {
            'fields': (
                'scheduled_time', 'actual_start_time', 
                'actual_end_time', 'table_number'
            )
        }),
        ('比赛结果', {
            'fields': (
                'player1_score', 'player2_score', 
                'winner', 'status'
            )
        }),
        ('其他信息', {
            'fields': ('notes', 'created_at'),
            'classes': ('collapse',)
        })
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'competition', 'group', 'player1', 'player2', 'winner'
        )

@admin.register(CompetitionResult)
class CompetitionResultAdmin(admin.ModelAdmin):
    list_display = [
        'participant', 'competition', 'group', 'group_rank', 
        'matches_played', 'matches_won', 'win_rate', 'award'
    ]
    list_filter = ['group', 'competition', 'award']
    search_fields = [
        'participant__username', 'participant__real_name', 
        'competition__title'
    ]
    readonly_fields = [
        'created_at', 'updated_at', 'win_rate', 'score_difference'
    ]
    
    fieldsets = (
        ('基本信息', {
            'fields': ('competition', 'participant', 'group')
        }),
        ('比赛统计', {
            'fields': (
                'matches_played', 'matches_won', 'matches_lost',
                'total_score_for', 'total_score_against'
            )
        }),
        ('排名和奖项', {
            'fields': ('group_rank', 'overall_rank', 'award')
        }),
        ('系统信息', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'competition', 'participant'
        )
