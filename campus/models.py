from django.db import models
from django.utils import timezone
from accounts.models import User


class Campus(models.Model):
    """校区模型"""
    CAMPUS_TYPE_CHOICES = [
        ('center', '中心校区'),
        ('branch', '分校区'),
    ]
    
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='校区名称'
    )
    code = models.CharField(
        max_length=20,
        unique=True,
        verbose_name='校区编码'
    )
    campus_type = models.CharField(
        max_length=10,
        choices=CAMPUS_TYPE_CHOICES,
        default='branch',
        verbose_name='校区类型'
    )
    address = models.TextField(
        verbose_name='校区地址'
    )
    contact_person = models.CharField(
        max_length=50,
        default='待填写',
        verbose_name='联系人'
    )
    phone = models.CharField(
        max_length=20,
        verbose_name='联系电话'
    )
    email = models.EmailField(
        blank=True,
        null=True,
        verbose_name='邮箱'
    )
    manager = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={'user_type__in': ['campus_admin', 'super_admin']},
        related_name='managed_campus',
        verbose_name='校区管理员'
    )
    parent_campus = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={'campus_type': 'center'},
        related_name='branch_campuses',
        verbose_name='上级校区'
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name='校区描述'
    )
    facilities = models.TextField(
        blank=True,
        null=True,
        verbose_name='设施介绍'
    )
    operating_hours = models.CharField(
        max_length=100,
        default='09:00-21:00',
        verbose_name='营业时间'
    )
    capacity = models.PositiveIntegerField(
        default=100,
        verbose_name='容纳人数'
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
        verbose_name = '校区'
        verbose_name_plural = '校区'
        db_table = 'campus_campus'
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name}({self.get_campus_type_display()})"

    @property
    def current_students_count(self):
        """当前学员数量"""
        return self.students.filter(is_active=True).count()

    @property
    def current_coaches_count(self):
        """当前教练数量"""
        return self.coaches.filter(is_active=True).count()
    
    @property
    def is_center_campus(self):
        """是否为中心校区"""
        return self.campus_type == 'center'
    
    @property
    def branch_campuses_count(self):
        """分校区数量（仅对中心校区有效）"""
        if self.is_center_campus:
            return self.branch_campuses.filter(is_active=True).count()
        return 0
    
    def can_manage_by_user(self, user):
        """检查用户是否可以管理此校区"""
        if user.user_type == 'super_admin':
            return True
        if user.user_type == 'campus_admin' and self.manager == user:
            return True
        return False
    
    def get_all_managed_campuses(self):
        """获取用户可管理的所有校区（包括分校区）"""
        campuses = [self]
        if self.is_center_campus:
            campuses.extend(list(self.branch_campuses.filter(is_active=True)))
        return campuses


class CampusArea(models.Model):
    """校区分区模型"""
    AREA_TYPE_CHOICES = [
        ('training', '训练区'),
        ('rest', '休息区'),
        ('equipment', '器材区'),
        ('office', '办公区'),
        ('reception', '接待区'),
        ('other', '其他'),
    ]
    
    campus = models.ForeignKey(
        Campus,
        on_delete=models.CASCADE,
        related_name='areas',
        verbose_name='所属校区'
    )
    name = models.CharField(
        max_length=50,
        verbose_name='分区名称'
    )
    area_type = models.CharField(
        max_length=20,
        choices=AREA_TYPE_CHOICES,
        verbose_name='分区类型'
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name='分区描述'
    )
    capacity = models.PositiveIntegerField(
        default=10,
        verbose_name='容纳人数'
    )
    equipment_list = models.TextField(
        blank=True,
        null=True,
        verbose_name='设备清单'
    )
    is_available = models.BooleanField(
        default=True,
        verbose_name='是否可用'
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
        verbose_name = '校区分区'
        verbose_name_plural = '校区分区'
        db_table = 'campus_area'
        unique_together = ['campus', 'name']
    
    def __str__(self):
        return f"{self.campus.name} - {self.name}"


class CampusStudent(models.Model):
    """校区学员关联模型"""
    campus = models.ForeignKey(
        Campus,
        on_delete=models.CASCADE,
        related_name='students',
        verbose_name='校区'
    )
    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'user_type': 'student'},
        related_name='campus_memberships',
        verbose_name='学员'
    )
    enrollment_date = models.DateTimeField(
        default=timezone.now,
        verbose_name='入学时间'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='是否活跃'
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
        verbose_name = '校区学员'
        verbose_name_plural = '校区学员'
        db_table = 'campus_student'
        unique_together = ['campus', 'student']
    
    def __str__(self):
        return f"{self.campus.name} - {self.student.real_name}"


class CampusCoach(models.Model):
    """校区教练关联模型"""
    campus = models.ForeignKey(
        Campus,
        on_delete=models.CASCADE,
        related_name='coaches',
        verbose_name='校区'
    )
    coach = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'user_type': 'coach'},
        related_name='campus_assignments',
        verbose_name='教练'
    )
    hire_date = models.DateTimeField(
        default=timezone.now,
        verbose_name='入职时间'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='是否在职'
    )
    specialties = models.TextField(
        blank=True,
        null=True,
        verbose_name='专业特长'
    )
    max_students = models.PositiveIntegerField(
        default=20,
        verbose_name='最大学员数'
    )
    hourly_rate = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=0.00,
        verbose_name='时薪'
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
        verbose_name = '校区教练'
        verbose_name_plural = '校区教练'
        db_table = 'campus_coach'
        unique_together = ['campus', 'coach']
    
    def __str__(self):
        return f"{self.campus.name} - {self.coach.real_name}"
    
    @property
    def current_students_count(self):
        """当前学员数量"""
        from courses.models import CourseEnrollment
        return CourseEnrollment.objects.filter(
            course__coach=self.coach,
            course__campus=self.campus,
            is_active=True
        ).count()