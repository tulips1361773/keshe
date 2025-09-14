#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import django
from decimal import Decimal

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'keshe.settings')
django.setup()

from accounts.models import User
from payments.models import Payment, UserAccount, PaymentMethod

def create_pending_recharge():
    """创建待审核的充值订单供管理员测试"""
    print("=== 创建待审核充值订单 ===")
    
    try:
        # 1. 获取或创建测试用户
        import random
        phone_suffix = random.randint(1000, 9999)
        test_user, created = User.objects.get_or_create(
            username='pending_recharge_user',
            defaults={
                'real_name': '待审核充值用户',
                'phone': f'138000{phone_suffix}',
                'email': 'pending@recharge.com',
                'user_type': 'student'
            }
        )
        if created:
            test_user.set_password('testpass123')
            test_user.save()
        print(f"✅ 测试用户: {test_user.username} ({test_user.real_name})")
        
        # 2. 获取支付方式
        payment_method, created = PaymentMethod.objects.get_or_create(
            name='银行转账',
            defaults={
                'method_type': 'bank_transfer',
                'is_active': True
            }
        )
        print(f"✅ 支付方式: {payment_method.name}")
        
        # 3. 创建多个待审核的充值订单
        amounts = [Decimal('50.00'), Decimal('100.00'), Decimal('200.00')]
        created_payments = []
        
        for amount in amounts:
            payment = Payment.objects.create(
                user=test_user,
                payment_type='recharge',
                amount=amount,
                payment_method=payment_method,
                status='pending',
                description=f'用户充值 ¥{amount} - 等待管理员审核'
            )
            created_payments.append(payment)
            print(f"✅ 创建充值订单: {payment.payment_id} (¥{amount})")
        
        # 4. 获取用户当前余额
        account, created = UserAccount.objects.get_or_create(
            user=test_user,
            defaults={'balance': Decimal('0.00')}
        )
        print(f"📊 用户当前余额: ¥{account.balance}")
        
        print("\n📋 Django Admin操作指南:")
        print("1. 访问管理后台: http://127.0.0.1:8000/admin/")
        print("2. 使用管理员账户登录: admin / testpass123")
        print("3. 进入 '支付管理' > 'Payments'")
        print("4. 筛选条件设置:")
        print("   - Payment type: recharge")
        print("   - Status: pending")
        print("5. 选择待审核订单")
        print("6. 在 '操作' 下拉菜单选择 '批准选中的充值订单'")
        print("7. 点击 '执行' 按钮")
        print("8. 在 'User accounts' 中查看余额变化")
        
        print("\n🎯 测试目标:")
        print(f"- 用户: {test_user.username}")
        print(f"- 待审核订单数量: {len(created_payments)}")
        print(f"- 总充值金额: ¥{sum(amounts)}")
        print(f"- 预期审核后余额: ¥{account.balance + sum(amounts)}")
        
        return True
        
    except Exception as e:
        print(f"❌ 创建过程中出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = create_pending_recharge()
    if success:
        print("\n🎉 待审核充值订单创建完成! 请在Django Admin中进行审核测试。")
    else:
        print("\n❌ 创建失败，请检查错误信息")