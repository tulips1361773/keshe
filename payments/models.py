from django.db import models
from django.utils import timezone
from decimal import Decimal
from accounts.models import User
from courses.models import Course, CourseEnrollment


class PaymentMethod(models.Model):
    """支付方式模型"""
    METHOD_TYPE_CHOICES = [
        ('cash', '现金'),
        ('wechat', '微信支付'),
        ('alipay', '支付宝'),
        ('bank_card', '银行卡'),
        ('credit_card', '信用卡'),
        ('other', '其他'),
    ]
    
    name = models.CharField(
        max_length=50,
        verbose_name='支付方式名称'
    )
    method_type = models.CharField(
        max_length=20,
        choices=METHOD_TYPE_CHOICES,
        verbose_name='支付类型'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='是否启用'
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name='描述'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='创建时间'
    )
    
    class Meta:
        verbose_name = '支付方式'
        verbose_name_plural = '支付方式'
        db_table = 'payments_method'
    
    def __str__(self):
        return self.name


class Payment(models.Model):
    """支付记录模型"""
    PAYMENT_STATUS_CHOICES = [
        ('pending', '待支付'),
        ('processing', '处理中'),
        ('completed', '已完成'),
        ('failed', '支付失败'),
        ('cancelled', '已取消'),
        ('refunded', '已退款'),
    ]
    
    PAYMENT_TYPE_CHOICES = [
        ('course_fee', '课程费用'),
        ('registration_fee', '注册费'),
        ('equipment_fee', '器材费'),
        ('membership_fee', '会员费'),
        ('penalty_fee', '违约金'),
        ('other', '其他'),
    ]
    
    payment_id = models.CharField(
        max_length=50,
        unique=True,
        verbose_name='支付单号'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='payments',
        verbose_name='支付用户'
    )
    enrollment = models.ForeignKey(
        CourseEnrollment,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='payments',
        verbose_name='关联报名'
    )
    payment_type = models.CharField(
        max_length=20,
        choices=PAYMENT_TYPE_CHOICES,
        default='course_fee',
        verbose_name='支付类型'
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='支付金额'
    )
    payment_method = models.ForeignKey(
        PaymentMethod,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='支付方式'
    )
    status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS_CHOICES,
        default='pending',
        verbose_name='支付状态'
    )
    transaction_id = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='第三方交易号'
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name='支付描述'
    )
    paid_at = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='支付时间'
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
        verbose_name = '支付记录'
        verbose_name_plural = '支付记录'
        db_table = 'payments_payment'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.payment_id} - {self.user.real_name} - ¥{self.amount}"
    
    def save(self, *args, **kwargs):
        if not self.payment_id:
            # 生成支付单号
            import uuid
            self.payment_id = f"PAY{timezone.now().strftime('%Y%m%d')}{str(uuid.uuid4())[:8].upper()}"
        super().save(*args, **kwargs)


class Refund(models.Model):
    """退款记录模型"""
    REFUND_STATUS_CHOICES = [
        ('pending', '待处理'),
        ('approved', '已批准'),
        ('rejected', '已拒绝'),
        ('processing', '处理中'),
        ('completed', '已完成'),
        ('failed', '退款失败'),
    ]
    
    REFUND_REASON_CHOICES = [
        ('course_cancelled', '课程取消'),
        ('student_request', '学员申请'),
        ('schedule_conflict', '时间冲突'),
        ('quality_issue', '质量问题'),
        ('other', '其他原因'),
    ]
    
    refund_id = models.CharField(
        max_length=50,
        unique=True,
        verbose_name='退款单号'
    )
    payment = models.ForeignKey(
        Payment,
        on_delete=models.CASCADE,
        related_name='refunds',
        verbose_name='原支付记录'
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='退款金额'
    )
    reason = models.CharField(
        max_length=20,
        choices=REFUND_REASON_CHOICES,
        verbose_name='退款原因'
    )
    status = models.CharField(
        max_length=20,
        choices=REFUND_STATUS_CHOICES,
        default='pending',
        verbose_name='退款状态'
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name='退款说明'
    )
    approved_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={'user_type__in': ['super_admin', 'campus_admin']},
        related_name='approved_refunds',
        verbose_name='审批人'
    )
    approved_at = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='审批时间'
    )
    processed_at = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='处理时间'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='申请时间'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='更新时间'
    )
    
    class Meta:
        verbose_name = '退款记录'
        verbose_name_plural = '退款记录'
        db_table = 'payments_refund'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.refund_id} - ¥{self.amount}"
    
    def save(self, *args, **kwargs):
        if not self.refund_id:
            # 生成退款单号
            import uuid
            self.refund_id = f"REF{timezone.now().strftime('%Y%m%d')}{str(uuid.uuid4())[:8].upper()}"
        super().save(*args, **kwargs)


class UserAccount(models.Model):
    """用户账户模型"""
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='account',
        verbose_name='用户'
    )
    balance = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00'),
        verbose_name='账户余额'
    )
    frozen_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00'),
        verbose_name='冻结金额'
    )
    total_paid = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00'),
        verbose_name='累计支付'
    )
    total_refunded = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00'),
        verbose_name='累计退款'
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
        verbose_name = '用户账户'
        verbose_name_plural = '用户账户'
        db_table = 'payments_user_account'
    
    def __str__(self):
        return f"{self.user.real_name}的账户"
    
    @property
    def available_balance(self):
        """可用余额"""
        return self.balance - self.frozen_amount


class AccountTransaction(models.Model):
    """账户交易记录模型"""
    TRANSACTION_TYPE_CHOICES = [
        ('recharge', '充值'),
        ('payment', '支付'),
        ('refund', '退款'),
        ('freeze', '冻结'),
        ('unfreeze', '解冻'),
        ('adjustment', '调整'),
    ]
    
    account = models.ForeignKey(
        UserAccount,
        on_delete=models.CASCADE,
        related_name='transactions',
        verbose_name='账户'
    )
    transaction_type = models.CharField(
        max_length=20,
        choices=TRANSACTION_TYPE_CHOICES,
        verbose_name='交易类型'
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='交易金额'
    )
    balance_before = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='交易前余额'
    )
    balance_after = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='交易后余额'
    )
    payment = models.ForeignKey(
        Payment,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='account_transactions',
        verbose_name='关联支付'
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name='交易描述'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='交易时间'
    )
    
    class Meta:
        verbose_name = '账户交易记录'
        verbose_name_plural = '账户交易记录'
        db_table = 'payments_account_transaction'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.account.user.real_name} - {self.get_transaction_type_display()} - ¥{self.amount}"


class Invoice(models.Model):
    """发票模型"""
    INVOICE_TYPE_CHOICES = [
        ('personal', '个人'),
        ('company', '企业'),
    ]
    
    INVOICE_STATUS_CHOICES = [
        ('pending', '待开具'),
        ('issued', '已开具'),
        ('sent', '已发送'),
        ('cancelled', '已作废'),
    ]
    
    invoice_number = models.CharField(
        max_length=50,
        unique=True,
        verbose_name='发票号码'
    )
    payment = models.ForeignKey(
        Payment,
        on_delete=models.CASCADE,
        related_name='invoices',
        verbose_name='关联支付'
    )
    invoice_type = models.CharField(
        max_length=20,
        choices=INVOICE_TYPE_CHOICES,
        verbose_name='发票类型'
    )
    title = models.CharField(
        max_length=200,
        verbose_name='发票抬头'
    )
    tax_number = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name='税号'
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='发票金额'
    )
    status = models.CharField(
        max_length=20,
        choices=INVOICE_STATUS_CHOICES,
        default='pending',
        verbose_name='发票状态'
    )
    issued_at = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='开具时间'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='申请时间'
    )
    
    class Meta:
        verbose_name = '发票'
        verbose_name_plural = '发票'
        db_table = 'payments_invoice'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.invoice_number} - {self.title}"
    
    def save(self, *args, **kwargs):
        if not self.invoice_number:
            # 生成发票号码
            import uuid
            self.invoice_number = f"INV{timezone.now().strftime('%Y%m%d')}{str(uuid.uuid4())[:8].upper()}"
        super().save(*args, **kwargs)