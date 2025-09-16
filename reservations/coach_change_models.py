from django.db import models
from django.utils import timezone
from accounts.models import User


class CoachChangeRequest(models.Model):
    """教练员更换请求模型"""
    
    REQUEST_STATUS_CHOICES = [
        ('pending', '待审核'),
        ('approved', '已通过'),
        ('rejected', '已拒绝'),
        ('cancelled', '已取消'),
    ]
    
    APPROVAL_STATUS_CHOICES = [
        ('pending', '待审核'),
        ('approved', '同意'),
        ('rejected', '拒绝'),
    ]
    
    # 基本信息
    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'user_type': 'student'},
        related_name='coach_change_requests',
        verbose_name='学员'
    )
    current_coach = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'user_type': 'coach'},
        related_name='current_coach_change_requests',
        verbose_name='当前教练'
    )
    target_coach = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'user_type': 'coach'},
        related_name='target_coach_change_requests',
        verbose_name='目标教练'
    )
    
    # 申请信息
    reason = models.TextField(
        verbose_name='更换原因',
        help_text='学员申请更换教练的原因'
    )
    request_date = models.DateTimeField(
        default=timezone.now,
        verbose_name='申请时间'
    )
    
    # 审批状态
    status = models.CharField(
        max_length=20,
        choices=REQUEST_STATUS_CHOICES,
        default='pending',
        verbose_name='请求状态'
    )
    
    # 三方审批状态
    current_coach_approval = models.CharField(
        max_length=20,
        choices=APPROVAL_STATUS_CHOICES,
        default='pending',
        verbose_name='当前教练审批状态'
    )
    target_coach_approval = models.CharField(
        max_length=20,
        choices=APPROVAL_STATUS_CHOICES,
        default='pending',
        verbose_name='目标教练审批状态'
    )
    campus_admin_approval = models.CharField(
        max_length=20,
        choices=APPROVAL_STATUS_CHOICES,
        default='pending',
        verbose_name='校区管理员审批状态'
    )
    
    # 审批人和时间
    current_coach_approved_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='current_coach_approvals',
        verbose_name='当前教练审批人'
    )
    current_coach_approved_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='当前教练审批时间'
    )
    
    target_coach_approved_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='target_coach_approvals',
        verbose_name='目标教练审批人'
    )
    target_coach_approved_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='目标教练审批时间'
    )
    
    campus_admin_approved_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={'user_type': 'campus_admin'},
        related_name='campus_admin_approvals',
        verbose_name='校区管理员审批人'
    )
    campus_admin_approved_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='校区管理员审批时间'
    )
    
    # 审批备注
    current_coach_notes = models.TextField(
        blank=True,
        null=True,
        verbose_name='当前教练备注'
    )
    target_coach_notes = models.TextField(
        blank=True,
        null=True,
        verbose_name='目标教练备注'
    )
    campus_admin_notes = models.TextField(
        blank=True,
        null=True,
        verbose_name='校区管理员备注'
    )
    
    # 处理结果
    processed_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='处理完成时间'
    )
    processed_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='processed_coach_changes',
        verbose_name='处理人'
    )
    
    # 时间戳
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='创建时间'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='更新时间'
    )
    
    class Meta:
        verbose_name = '教练员更换请求'
        verbose_name_plural = '教练员更换请求'
        db_table = 'reservations_coach_change_request'
        ordering = ['-created_at']
        
        # 确保学员不能同时有多个待处理的更换请求
        constraints = [
            models.UniqueConstraint(
                fields=['student'],
                condition=models.Q(status='pending'),
                name='unique_pending_coach_change_per_student'
            )
        ]
    
    def __str__(self):
        return f"{self.student.real_name} 申请从 {self.current_coach.real_name} 更换到 {self.target_coach.real_name}"
    
    @property
    def is_all_approved(self):
        """检查是否三方都已同意"""
        return (
            self.current_coach_approval == 'approved' and
            self.target_coach_approval == 'approved' and
            self.campus_admin_approval == 'approved'
        )
    
    @property
    def has_rejection(self):
        """检查是否有任何一方拒绝"""
        return (
            self.current_coach_approval == 'rejected' or
            self.target_coach_approval == 'rejected' or
            self.campus_admin_approval == 'rejected'
        )
    
    def update_status(self):
        """根据三方审批状态更新总体状态"""
        if self.has_rejection:
            self.status = 'rejected'
            if not self.processed_at:
                self.processed_at = timezone.now()
        elif self.is_all_approved:
            self.status = 'approved'
            if not self.processed_at:
                self.processed_at = timezone.now()
        else:
            self.status = 'pending'
        
        self.save()
    
    def approve_by_current_coach(self, user, notes=None):
        """当前教练审批"""
        self.current_coach_approval = 'approved'
        self.current_coach_approved_by = user
        self.current_coach_approved_at = timezone.now()
        if notes:
            self.current_coach_notes = notes
        self.save()
        self.update_status()
    
    def reject_by_current_coach(self, user, notes=None):
        """当前教练拒绝"""
        self.current_coach_approval = 'rejected'
        self.current_coach_approved_by = user
        self.current_coach_approved_at = timezone.now()
        if notes:
            self.current_coach_notes = notes
        self.save()
        self.update_status()
    
    def approve_by_target_coach(self, user, notes=None):
        """目标教练审批"""
        self.target_coach_approval = 'approved'
        self.target_coach_approved_by = user
        self.target_coach_approved_at = timezone.now()
        if notes:
            self.target_coach_notes = notes
        self.save()
        self.update_status()
    
    def reject_by_target_coach(self, user, notes=None):
        """目标教练拒绝"""
        self.target_coach_approval = 'rejected'
        self.target_coach_approved_by = user
        self.target_coach_approved_at = timezone.now()
        if notes:
            self.target_coach_notes = notes
        self.save()
        self.update_status()
    
    def approve_by_campus_admin(self, user, notes=None):
        """校区管理员审批"""
        self.campus_admin_approval = 'approved'
        self.campus_admin_approved_by = user
        self.campus_admin_approved_at = timezone.now()
        if notes:
            self.campus_admin_notes = notes
        self.save()
        self.update_status()
    
    def reject_by_campus_admin(self, user, notes=None):
        """校区管理员拒绝"""
        self.campus_admin_approval = 'rejected'
        self.campus_admin_approved_by = user
        self.campus_admin_approved_at = timezone.now()
        if notes:
            self.campus_admin_notes = notes
        self.save()
        self.update_status()
    
    def execute_change(self):
        """执行教练更换（在三方都同意后调用）"""
        if not self.is_all_approved:
            raise ValueError("只有在三方都同意后才能执行更换")
        
        from .models import CoachStudentRelation
        
        # 终止当前师生关系
        try:
            current_relation = CoachStudentRelation.objects.get(
                coach=self.current_coach,
                student=self.student,
                status='approved'
            )
            current_relation.status = 'terminated'
            current_relation.terminated_at = timezone.now()
            current_relation.save()
        except CoachStudentRelation.DoesNotExist:
            pass  # 如果当前关系不存在，继续执行
        
        # 创建新的师生关系
        new_relation, created = CoachStudentRelation.objects.get_or_create(
            coach=self.target_coach,
            student=self.student,
            defaults={
                'status': 'approved',
                'applied_by': 'student',
                'notes': f'通过教练更换请求建立的师生关系 (请求ID: {self.id})',
                'processed_at': timezone.now()
            }
        )
        
        if not created and new_relation.status != 'approved':
            new_relation.status = 'approved'
            new_relation.processed_at = timezone.now()
            new_relation.save()
        
        # 标记更换请求为已处理
        self.processed_at = timezone.now()
        self.save()
        
        return new_relation