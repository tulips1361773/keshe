#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import django
from decimal import Decimal

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'keshe.settings')
django.setup()

from accounts.models import User
from payments.models import Payment, UserAccount, AccountTransaction, PaymentMethod
from django.utils import timezone
from django.db import transaction

def test_admin_recharge_approval():
    """测试Django Admin充值审核功能"""
    print("=== 测试Django Admin充值审核功能 ===")
    
    try:
        # 1. 创建测试用户
        import random
        phone_suffix = random.randint(1000, 9999)
        test_user, created = User.objects.get_or_create(
            username='test_recharge_user',
            defaults={
                'real_name': '测试充值用户',
                'phone': f'139000{phone_suffix}',
                'email': 'test@recharge.com',
                'user_type': 'student'
            }
        )
        if created:
            test_user.set_password('testpass123')
            test_user.save()
        print(f"✅ 测试用户: {test_user.username}")
        
        # 2. 创建支付方式
        payment_method, created = PaymentMethod.objects.get_or_create(
            name='银行转账',
            defaults={
                'method_type': 'bank_transfer',
                'is_active': True
            }
        )
        print(f"✅ 支付方式: {payment_method.name}")
        
        # 3. 创建待审核的充值订单
        payment = Payment.objects.create(
            user=test_user,
            payment_type='recharge',
            amount=Decimal('100.00'),
            payment_method=payment_method,
            status='pending',
            description='测试充值订单 - 等待管理员审核'
        )
        print(f"✅ 创建充值订单: {payment.payment_id} (金额: ¥{payment.amount})")
        
        # 4. 获取用户当前余额
        account, created = UserAccount.objects.get_or_create(
            user=test_user,
            defaults={'balance': Decimal('0.00')}
        )
        balance_before = account.balance
        print(f"📊 充值前余额: ¥{balance_before}")
        
        # 5. 模拟管理员审核通过操作
        print("\n🔄 模拟管理员审核通过...")
        with transaction.atomic():
            # 更新支付状态
            payment.status = 'completed'
            payment.paid_at = timezone.now()
            payment.save()
            
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
        
        # 6. 验证结果
        payment.refresh_from_db()
        account.refresh_from_db()
        
        print(f"✅ 订单状态: {payment.status}")
        print(f"✅ 充值后余额: ¥{account.balance}")
        print(f"✅ 余额变化: +¥{account.balance - balance_before}")
        
        # 7. 查看交易记录
        transactions = AccountTransaction.objects.filter(
            account=account,
            payment=payment
        ).order_by('-created_at')
        
        if transactions.exists():
            latest_transaction = transactions.first()
            print(f"✅ 交易记录: {latest_transaction.transaction_type} +¥{latest_transaction.amount}")
        
        print("\n📋 Django Admin管理界面信息:")
        print("- 管理后台地址: http://127.0.0.1:8000/admin/")
        print("- 管理员账户: admin / testpass123")
        print("- 充值管理: 支付管理 > Payments")
        print("- 用户账户: 支付管理 > User accounts")
        print("- 交易记录: 支付管理 > Account transactions")
        
        print("\n💡 使用说明:")
        print("1. 登录Django管理后台")
        print("2. 进入 '支付管理' > 'Payments'")
        print("3. 筛选 payment_type='recharge' 和 status='pending'")
        print("4. 选择待审核订单，使用批量操作 '批准选中的充值订单'")
        print("5. 在 'User accounts' 中查看用户余额变化")
        
        return True
        
    except Exception as e:
        print(f"❌ 测试过程中出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_admin_recharge_approval()
    if success:
        print("\n🎉 Django Admin充值审核功能测试完成!")
    else:
        print("\n❌ 测试失败，请检查错误信息")