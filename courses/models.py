from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from accounts.models import User
from campus.models import Campus, CampusArea


class Course(models.Model):
    """课程模型"""
    COURSE_TYPE_CHOICES = [
        ('beginner', '初级课程'),
        ('intermediate', '中级课程'),
        ('advanced', '高级课程'),
        ('private', '私教课程'),
        ('group', '团体课程'),
    ]
    
    COURSE_STATUS_CHOICES = [
        ('draft', '草稿'),
        ('published', '已发布'),
        ('suspended', '暂停'),
        ('cancelled', '已取消'),
    ]
    
    name = models.CharField(
        max_length=100,
        verbose_name='课程名称'
    )
    description = models.TextField(
        verbose_name='课程描述'
    )
    course_type = models.CharField(
        max_length=20,
        choices=COURSE_TYPE_CHOICES,
        verbose_name='课程类型'
    )
    campus = models.ForeignKey(
        Campus,
        on_delete=models.CASCADE,
        related_name='courses',
        verbose_name='所属校区'
    )
    coach = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'user_type': 'coach'},
        related_name='teaching_courses',
        verbose_name='授课教练'
    )
    area = models.ForeignKey(
        CampusArea,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='courses',
        verbose_name='上课区域'
    )
    max_students = models.PositiveIntegerField(
        default=10,
        verbose_name='最大学员数'
    )
    duration_minutes = models.PositiveIntegerField(
        default=60,
        verbose_name='课程时长(分钟)'
    )
    price_per_session = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=0.00,
        verbose_name='单次课程价格'
    )
    total_sessions = models.PositiveIntegerField(
        default=1,
        verbose_name='总课时数'
    )
    status = models.CharField(
        max_length=20,
        choices=COURSE_STATUS_CHOICES,
        default='draft',
        verbose_name='课程状态'
    )
    start_date = models.DateField(
        verbose_name='开始日期'
    )
    end_date = models.DateField(
        verbose_name='结束日期'
    )
    requirements = models.TextField(
        blank=True,
        null=True,
        verbose_name='课程要求'
    )
    equipment_needed = models.TextField(
        blank=True,
        null=True,
        verbose_name='所需器材'
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
        verbose_name = '课程'
        verbose_name_plural = '课程'
        db_table = 'courses_course'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.coach.real_name}"
    
    @property
    def current_enrollments_count(self):
        """当前报名人数"""
        return self.enrollments.filter(is_active=True).count()
    
    @property
    def available_spots(self):
        """剩余名额"""
        return self.max_students - self.current_enrollments_count
    
    @property
    def is_full(self):
        """是否已满员"""
        return self.current_enrollments_count >= self.max_students
    
    @property
    def total_price(self):
        """课程总价"""
        return self.price_per_session * self.total_sessions


class CourseSchedule(models.Model):
    """课程时间表模型"""
    WEEKDAY_CHOICES = [
        (0, '周一'),
        (1, '周二'),
        (2, '周三'),
        (3, '周四'),
        (4, '周五'),
        (5, '周六'),
        (6, '周日'),
    ]
    
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='schedules',
        verbose_name='课程'
    )
    weekday = models.IntegerField(
        choices=WEEKDAY_CHOICES,
        verbose_name='星期'
    )
    start_time = models.TimeField(
        verbose_name='开始时间'
    )
    end_time = models.TimeField(
        verbose_name='结束时间'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='是否启用'
    )
    
    class Meta:
        verbose_name = '课程时间表'
        verbose_name_plural = '课程时间表'
        db_table = 'courses_schedule'
        unique_together = ['course', 'weekday', 'start_time']
    
    def __str__(self):
        return f"{self.course.name} - {self.get_weekday_display()} {self.start_time}-{self.end_time}"


class CourseEnrollment(models.Model):
    """课程报名模型"""
    ENROLLMENT_STATUS_CHOICES = [
        ('pending', '待确认'),
        ('confirmed', '已确认'),
        ('cancelled', '已取消'),
        ('completed', '已完成'),
    ]
    
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='enrollments',
        verbose_name='课程'
    )
    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'user_type': 'student'},
        related_name='course_enrollments',
        verbose_name='学员'
    )
    enrollment_date = models.DateTimeField(
        default=timezone.now,
        verbose_name='报名时间'
    )
    status = models.CharField(
        max_length=20,
        choices=ENROLLMENT_STATUS_CHOICES,
        default='pending',
        verbose_name='报名状态'
    )
    payment_status = models.CharField(
        max_length=20,
        choices=[
            ('unpaid', '未支付'),
            ('partial', '部分支付'),
            ('paid', '已支付'),
            ('refunded', '已退款'),
        ],
        default='unpaid',
        verbose_name='支付状态'
    )
    paid_amount = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=0.00,
        verbose_name='已支付金额'
    )
    notes = models.TextField(
        blank=True,
        null=True,
        verbose_name='备注'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='是否活跃'
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
        verbose_name = '课程报名'
        verbose_name_plural = '课程报名'
        db_table = 'courses_enrollment'
        unique_together = ['course', 'student']
    
    def __str__(self):
        return f"{self.student.real_name} - {self.course.name}"
    
    @property
    def remaining_amount(self):
        """剩余应付金额"""
        return self.course.total_price - self.paid_amount


class CourseSession(models.Model):
    """课程课时模型"""
    SESSION_STATUS_CHOICES = [
        ('scheduled', '已安排'),
        ('in_progress', '进行中'),
        ('completed', '已完成'),
        ('cancelled', '已取消'),
        ('postponed', '已延期'),
    ]
    
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='sessions',
        verbose_name='课程'
    )
    session_number = models.PositiveIntegerField(
        verbose_name='课时编号'
    )
    scheduled_date = models.DateField(
        verbose_name='计划日期'
    )
    scheduled_time = models.TimeField(
        verbose_name='计划时间'
    )
    actual_start_time = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='实际开始时间'
    )
    actual_end_time = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='实际结束时间'
    )
    status = models.CharField(
        max_length=20,
        choices=SESSION_STATUS_CHOICES,
        default='scheduled',
        verbose_name='课时状态'
    )
    content = models.TextField(
        blank=True,
        null=True,
        verbose_name='课程内容'
    )
    homework = models.TextField(
        blank=True,
        null=True,
        verbose_name='课后作业'
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
        verbose_name = '课程课时'
        verbose_name_plural = '课程课时'
        db_table = 'courses_session'
        unique_together = ['course', 'session_number']
        ordering = ['course', 'session_number']
    
    def __str__(self):
        return f"{self.course.name} - 第{self.session_number}课时"


class CourseAttendance(models.Model):
    """课程考勤模型"""
    ATTENDANCE_STATUS_CHOICES = [
        ('present', '出席'),
        ('absent', '缺席'),
        ('late', '迟到'),
        ('leave_early', '早退'),
        ('excused', '请假'),
    ]
    
    session = models.ForeignKey(
        CourseSession,
        on_delete=models.CASCADE,
        related_name='attendances',
        verbose_name='课时'
    )
    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'user_type': 'student'},
        related_name='course_attendances',
        verbose_name='学员'
    )
    status = models.CharField(
        max_length=20,
        choices=ATTENDANCE_STATUS_CHOICES,
        default='present',
        verbose_name='考勤状态'
    )
    check_in_time = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='签到时间'
    )
    check_out_time = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='签退时间'
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
        verbose_name = '课程考勤'
        verbose_name_plural = '课程考勤'
        db_table = 'courses_attendance'
        unique_together = ['session', 'student']
    
    def __str__(self):
        return f"{self.student.real_name} - {self.session} - {self.get_status_display()}"


class CourseEvaluation(models.Model):
    """课程评价模型"""
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='evaluations',
        verbose_name='课程'
    )
    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'user_type': 'student'},
        related_name='course_evaluations',
        verbose_name='学员'
    )
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name='评分(1-5)'
    )
    comment = models.TextField(
        blank=True,
        null=True,
        verbose_name='评价内容'
    )
    coach_rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name='教练评分(1-5)'
    )
    facility_rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name='设施评分(1-5)'
    )
    is_anonymous = models.BooleanField(
        default=False,
        verbose_name='是否匿名'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='评价时间'
    )
    
    class Meta:
        verbose_name = '课程评价'
        verbose_name_plural = '课程评价'
        db_table = 'courses_evaluation'
        unique_together = ['course', 'student']
    
    def __str__(self):
        return f"{self.student.real_name} - {self.course.name} - {self.rating}星"