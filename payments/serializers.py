from rest_framework import serializers
from .models import Payment, PaymentMethod, UserAccount, AccountTransaction, Refund, Invoice
from accounts.serializers import UserSerializer
from courses.serializers import CourseEnrollmentSerializer


class PaymentMethodSerializer(serializers.ModelSerializer):
    """支付方式序列化器"""
    
    class Meta:
        model = PaymentMethod
        fields = ['id', 'name', 'method_type', 'is_active', 'description', 'created_at']
        read_only_fields = ['id', 'created_at']


class PaymentSerializer(serializers.ModelSerializer):
    """支付记录序列化器"""
    user = UserSerializer(read_only=True)
    enrollment = CourseEnrollmentSerializer(read_only=True)
    payment_method = PaymentMethodSerializer(read_only=True)
    payment_type_display = serializers.CharField(source='get_payment_type_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Payment
        fields = [
            'id', 'payment_id', 'user', 'enrollment', 'payment_type', 'payment_type_display',
            'amount', 'payment_method', 'status', 'status_display', 'transaction_id',
            'description', 'paid_at', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'payment_id', 'created_at', 'updated_at']


class UserAccountSerializer(serializers.ModelSerializer):
    """用户账户序列化器"""
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = UserAccount
        fields = [
            'id', 'user', 'balance', 'frozen_amount', 'total_recharge',
            'total_consumption', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class AccountTransactionSerializer(serializers.ModelSerializer):
    """账户交易记录序列化器"""
    account = UserAccountSerializer(read_only=True)
    payment = PaymentSerializer(read_only=True)
    transaction_type_display = serializers.CharField(source='get_transaction_type_display', read_only=True)
    
    class Meta:
        model = AccountTransaction
        fields = [
            'id', 'account', 'transaction_type', 'transaction_type_display',
            'amount', 'balance_before', 'balance_after', 'payment',
            'description', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class RefundSerializer(serializers.ModelSerializer):
    """退款记录序列化器"""
    payment = PaymentSerializer(read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Refund
        fields = [
            'id', 'refund_id', 'payment', 'refund_amount', 'reason',
            'status', 'status_display', 'processed_at', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'refund_id', 'created_at', 'updated_at']


class InvoiceSerializer(serializers.ModelSerializer):
    """发票序列化器"""
    payment = PaymentSerializer(read_only=True)
    invoice_type_display = serializers.CharField(source='get_invoice_type_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Invoice
        fields = [
            'id', 'invoice_number', 'payment', 'invoice_type', 'invoice_type_display',
            'title', 'tax_number', 'amount', 'status', 'status_display',
            'issued_at', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'invoice_number', 'created_at', 'updated_at']


class RechargeSerializer(serializers.Serializer):
    """充值请求序列化器"""
    amount = serializers.DecimalField(max_digits=10, decimal_places=2, min_value=0.01)
    payment_method_id = serializers.IntegerField()
    description = serializers.CharField(max_length=500, required=False, allow_blank=True)
    
    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("充值金额必须大于0")
        if value > 10000:
            raise serializers.ValidationError("单次充值金额不能超过10000元")
        return value
    
    def validate_payment_method_id(self, value):
        try:
            payment_method = PaymentMethod.objects.get(id=value, is_active=True)
        except PaymentMethod.DoesNotExist:
            raise serializers.ValidationError("支付方式不存在或已禁用")
        return value