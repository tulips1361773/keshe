from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from accounts.models import User
from campus.models import Campus

# 导入教练更换模型
from .coach_change_models import CoachChangeRequest


class CoachStudentRelation(models.Model):
    """师生关系模型"""
    RELATION_STATUS_CHOICES = [
        ('pending', '待审核'),
        ('approved', '已通过'),
        ('rejected', '已拒绝'),
        ('terminated', '已终止'),
    ]
    
    APPLIED_BY_CHOICES = [
        ('student', '学员申请'),
        ('coach', '教练申请'),
    ]
    
    coach = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'user_type': 'coach'},
        related_name='student_relations',
        verbose_name='教练'
    )
    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'user_type': 'student'},
        related_name='coach_relations',
        verbose_name='学员'
    )
    status = models.CharField(
        max_length=20,
        choices=RELATION_STATUS_CHOICES,
        default='pending',
        verbose_name='关系状态'
    )
    applied_by = models.CharField(
        max_length=20,
        choices=APPLIED_BY_CHOICES,
        verbose_name='申请方'
    )
    applied_at = models.DateTimeField(
        default=timezone.now,
        verbose_name='申请时间'
    )
    processed_at = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='处理时间'
    )
    terminated_at = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='终止时间'
    )
    notes = models.TextField(
        blank=True,
        null=True,
        verbose_name='备注'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='创建时间'
    )
    
    class Meta:
        verbose_name = '师生关系'
        verbose_name_plural = '师生关系'
        db_table = 'reservations_coach_student_relation'
        unique_together = ['coach', 'student']
    
    def __str__(self):
        return f"{self.coach.real_name} - {self.student.real_name}"


class Table(models.Model):
    """球台模型"""
    TABLE_STATUS_CHOICES = [
        ('available', '可用'),
        ('occupied', '占用中'),
        ('maintenance', '维护中'),
        ('disabled', '停用'),
    ]
    
    campus = models.ForeignKey(
        Campus,
        on_delete=models.CASCADE,
        related_name='tables',
        verbose_name='所属校区'
    )
    number = models.CharField(
        max_length=10,
        verbose_name='球台编号'
    )
    name = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name='球台名称'
    )
    status = models.CharField(
        max_length=20,
        choices=TABLE_STATUS_CHOICES,
        default='available',
        verbose_name='球台状态'
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name='球台描述'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='是否启用'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='创建时间'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='更新时间'
    )
    
    class Meta:
        verbose_name = '球台'
        verbose_name_plural = '球台'
        db_table = 'reservations_table'
        unique_together = ['campus', 'number']
        ordering = ['campus', 'number']
    
    def __str__(self):
        return f"{self.campus.name} - {self.number}号台"


class Booking(models.Model):
    """预约模型"""
    BOOKING_STATUS_CHOICES = [
        ('pending', '待确认'),
        ('confirmed', '已确认'),
        ('completed', '已完成'),
        ('cancelled', '已取消'),
    ]
    
    relation = models.ForeignKey(
        CoachStudentRelation,
        on_delete=models.CASCADE,
        related_name='bookings',
        verbose_name='师生关系'
    )
    table = models.ForeignKey(
        Table,
        on_delete=models.CASCADE,
        related_name='bookings',
        verbose_name='球台'
    )
    start_time = models.DateTimeField(
        verbose_name='开始时间'
    )
    end_time = models.DateTimeField(
        verbose_name='结束时间'
    )
    duration_hours = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        verbose_name='时长(小时)'
    )
    total_fee = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='总费用'
    )
    status = models.CharField(
        max_length=20,
        choices=BOOKING_STATUS_CHOICES,
        default='pending',
        verbose_name='预约状态'
    )
    confirmed_at = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='确认时间'
    )
    cancelled_at = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='取消时间'
    )
    cancel_reason = models.TextField(
        blank=True,
        null=True,
        verbose_name='取消原因'
    )
    cancelled_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='cancelled_bookings',
        verbose_name='取消人'
    )
    notes = models.TextField(
        blank=True,
        null=True,
        verbose_name='备注'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='创建时间'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='更新时间'
    )
    
    class Meta:
        verbose_name = '预约'
        verbose_name_plural = '预约'
        db_table = 'reservations_booking'
        ordering = ['-start_time']
    
    def __str__(self):
        return f"{self.relation} - {self.start_time.strftime('%Y-%m-%d %H:%M')}"
    
    @property
    def coach(self):
        """获取教练"""
        return self.relation.coach
    
    @property
    def student(self):
        """获取学员"""
        return self.relation.student
    
    def can_cancel(self, user):
        """检查是否可以取消预约"""
        if self.status not in ['pending', 'confirmed']:
            return False, '预约状态不允许取消'
        
        # 检查是否在24小时内
        from django.utils import timezone
        time_diff = self.start_time - timezone.now()
        if time_diff.total_seconds() < 24 * 3600:
            return False, '距离上课时间不足24小时，无法取消'
        
        # 检查用户权限
        if user not in [self.coach, self.student]:
            return False, '只有教练或学员可以取消预约'
        
        # 检查本月取消次数
        from django.db.models import Q
        current_month = timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        cancel_count = Booking.objects.filter(
            Q(relation__coach=user) | Q(relation__student=user),
            cancelled_at__gte=current_month,
            cancelled_by=user
        ).count()
        
        if cancel_count >= 3:
            return False, '本月取消次数已达上限(3次)'
        
        return True, '可以取消'
    
    def has_pending_cancellation(self):
        """检查是否有待处理的取消申请"""
        return hasattr(self, 'cancellation') and self.cancellation.status == 'pending'
    
    def get_cancellation_status(self):
        """获取取消申请状态"""
        if hasattr(self, 'cancellation'):
            return self.cancellation.status
        return None
    
    def can_be_cancelled_by(self, user):
        """检查指定用户是否可以取消此预约（考虑取消申请流程）"""
        # 基本的取消检查
        can_cancel, message = self.can_cancel(user)
        if not can_cancel:
            return False, message
        
        # 检查是否已有待处理的取消申请
        if self.has_pending_cancellation():
            return False, '该预约已有待处理的取消申请'
        
        return True, '可以申请取消'


class BookingCancellation(models.Model):
    """预约取消申请模型"""
    CANCELLATION_STATUS_CHOICES = [
        ('pending', '待确认'),
        ('approved', '已同意'),
        ('rejected', '已拒绝'),
    ]
    
    booking = models.OneToOneField(
        Booking,
        on_delete=models.CASCADE,
        related_name='cancellation',
        verbose_name='预约'
    )
    requested_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='requested_cancellations',
        verbose_name='申请人'
    )
    reason = models.TextField(
        verbose_name='取消原因'
    )
    status = models.CharField(
        max_length=20,
        choices=CANCELLATION_STATUS_CHOICES,
        default='pending',
        verbose_name='申请状态'
    )
    processed_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='processed_cancellations',
        verbose_name='处理人'
    )
    processed_at = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='处理时间'
    )
    response_message = models.TextField(
        blank=True,
        null=True,
        verbose_name='回复消息'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='申请时间'
    )
    
    class Meta:
        verbose_name = '预约取消申请'
        verbose_name_plural = '预约取消申请'
        db_table = 'reservations_booking_cancellation'
    
    def __str__(self):
        return f"预约{self.booking.id} - 取消申请"
