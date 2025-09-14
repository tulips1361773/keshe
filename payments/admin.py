from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils import timezone
from .models import PaymentMethod, Payment, Refund, UserAccount, AccountTransaction, Invoice


@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = ['name', 'method_type', 'is_active', 'created_at']
    list_filter = ['method_type', 'is_active']
    search_fields = ['name']
    ordering = ['-created_at']


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    change_list_template = 'admin/payments/payment/change_list.html'
    list_display = [
        'payment_id', 'user_link', 'payment_type', 'amount', 
        'payment_method', 'status', 'created_at', 'paid_at'
    ]
    list_filter = ['payment_type', 'status', 'payment_method', 'created_at']
    search_fields = ['payment_id', 'user__username', 'user__real_name', 'description']
    readonly_fields = ['payment_id', 'user', 'enrollment', 'payment_type', 'amount', 
                      'payment_method', 'status', 'transaction_id', 'description',
                      'paid_at', 'created_at', 'updated_at']
    ordering = ['-created_at']
    
    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['pending_payments_url'] = reverse('payments:pending_payments')
        return super().changelist_view(request, extra_context=extra_context)
    
    def get_urls(self):
        from django.urls import path
        urls = super().get_urls()
        custom_urls = [
            path('pending-review/', self.admin_site.admin_view(self.pending_review_redirect), name='payments_payment_pending_review'),
        ]
        return custom_urls + urls
    
    def pending_review_redirect(self, request):
        from django.shortcuts import redirect
        return redirect('payments:pending_payments')
    
    def has_add_permission(self, request):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False
    
    def has_change_permission(self, request, obj=None):
        # 只允许查看，不允许修改
        return False
    
    fieldsets = (
        ('基本信息', {
            'fields': ('payment_id', 'user', 'enrollment', 'payment_type', 'amount')
        }),
        ('支付信息', {
            'fields': ('payment_method', 'status', 'transaction_id', 'description')
        }),
        ('时间信息', {
            'fields': ('paid_at', 'created_at', 'updated_at')
        }),
    )
    
    def user_link(self, obj):
        """用户链接"""
        if obj.user:
            url = reverse('admin:accounts_user_change', args=[obj.user.id])
            return format_html('<a href="{}">{}</a>', url, obj.user.real_name or obj.user.username)
        return '-'
    user_link.short_description = '用户'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'payment_method', 'enrollment')
    
    actions = ['approve_recharge', 'reject_recharge']
    
    def approve_recharge(self, request, queryset):
        """批准充值"""
        from django.db import transaction
        from decimal import Decimal
        
        updated = 0
        for payment in queryset.filter(payment_type='recharge', status='pending'):
            with transaction.atomic():
                # 更新支付状态
                payment.status = 'completed'
                payment.paid_at = timezone.now()
                payment.save()
                
                # 更新用户账户余额
                account, created = UserAccount.objects.get_or_create(
                    user=payment.user,
                    defaults={'balance': Decimal('0.00')}
                )
                
                # 记录账户交易
                AccountTransaction.objects.create(
                    account=account,
                    transaction_type='recharge',
                    amount=payment.amount,
                    balance_before=account.balance,
                    balance_after=account.balance + payment.amount,
                    payment=payment,
                    description=f'管理员审核通过充值: {payment.description}'
                )
                
                # 更新账户余额
                account.balance += payment.amount
                account.total_paid += payment.amount
                account.save()
                
                updated += 1
        
        self.message_user(request, f'成功批准 {updated} 个充值订单')
    approve_recharge.short_description = '批准选中的充值订单'
    
    def reject_recharge(self, request, queryset):
        """拒绝充值"""
        updated = queryset.filter(payment_type='recharge', status='pending').update(
            status='failed',
            paid_at=timezone.now()
        )
        self.message_user(request, f'成功拒绝 {updated} 个充值订单')
    reject_recharge.short_description = '拒绝选中的充值订单'


@admin.register(Refund)
class RefundAdmin(admin.ModelAdmin):
    list_display = [
        'refund_id', 'payment_link', 'amount', 'reason', 
        'status', 'approved_by', 'created_at', 'approved_at'
    ]
    list_filter = ['reason', 'status', 'created_at']
    search_fields = ['refund_id', 'payment__payment_id', 'description']
    readonly_fields = ['refund_id', 'created_at', 'updated_at']
    ordering = ['-created_at']
    
    def payment_link(self, obj):
        """支付记录链接"""
        if obj.payment:
            url = reverse('admin:payments_payment_change', args=[obj.payment.id])
            return format_html('<a href="{}">{}</a>', url, obj.payment.payment_id)
        return '-'
    payment_link.short_description = '原支付记录'


@admin.register(UserAccount)
class UserAccountAdmin(admin.ModelAdmin):
    list_display = [
        'user_link', 'balance', 'frozen_amount', 'available_balance_display',
        'total_paid', 'total_refunded', 'created_at'
    ]
    search_fields = ['user__username', 'user__real_name']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-balance']
    
    def user_link(self, obj):
        """用户链接"""
        if obj.user:
            url = reverse('admin:accounts_user_change', args=[obj.user.id])
            return format_html('<a href="{}">{}</a>', url, obj.user.real_name or obj.user.username)
        return '-'
    user_link.short_description = '用户'
    
    def available_balance_display(self, obj):
        """可用余额"""
        return f'¥{obj.available_balance:.2f}'
    available_balance_display.short_description = '可用余额'


@admin.register(AccountTransaction)
class AccountTransactionAdmin(admin.ModelAdmin):
    list_display = [
        'account_user', 'transaction_type', 'amount_display', 
        'balance_before', 'balance_after', 'payment_link', 'created_at'
    ]
    list_filter = ['transaction_type', 'created_at']
    search_fields = ['account__user__username', 'account__user__real_name', 'description']
    readonly_fields = ['created_at']
    ordering = ['-created_at']
    
    def account_user(self, obj):
        """账户用户"""
        return obj.account.user.real_name or obj.account.user.username
    account_user.short_description = '用户'
    
    def amount_display(self, obj):
        """金额显示"""
        if obj.transaction_type in ['recharge', 'refund', 'unfreeze']:
            return format_html('<span style="color: green;">+¥{:.2f}</span>', obj.amount)
        else:
            return format_html('<span style="color: red;">-¥{:.2f}</span>', obj.amount)
    amount_display.short_description = '交易金额'
    
    def payment_link(self, obj):
        """支付记录链接"""
        if obj.payment:
            url = reverse('admin:payments_payment_change', args=[obj.payment.id])
            return format_html('<a href="{}">{}</a>', url, obj.payment.payment_id)
        return '-'
    payment_link.short_description = '关联支付'


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = [
        'invoice_number', 'payment_link', 'invoice_type', 
        'title', 'amount', 'status', 'created_at', 'issued_at'
    ]
    list_filter = ['invoice_type', 'status', 'created_at']
    search_fields = ['invoice_number', 'title', 'tax_number']
    readonly_fields = ['invoice_number', 'created_at']
    ordering = ['-created_at']
    
    def payment_link(self, obj):
        """支付记录链接"""
        if obj.payment:
            url = reverse('admin:payments_payment_change', args=[obj.payment.id])
            return format_html('<a href="{}">{}</a>', url, obj.payment.payment_id)
        return '-'
    payment_link.short_description = '关联支付'