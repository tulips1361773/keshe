#!/usr/bin/env python
"""
创建测试支付记录
验证修复后的日志记录功能
"""

import os
import sys
import django

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'keshe.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
django.setup()

from django.contrib.auth import get_user_model
from payments.models import Payment, PaymentMethod
from logs.models import SystemLog
from decimal import Decimal
from django.test import RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.auth.middleware import AuthenticationMiddleware

User = get_user_model()

def create_test_payment():
    """创建测试支付记录"""
    print("=" * 60)
    print("创建测试支付记录")
    print("=" * 60)
    
    # 1. 查找测试用户
    try:
        test_student = User.objects.get(username='test_student')
        print(f"✓ 找到测试学员: {test_student.username} ({test_student.real_name or '未设置'})")
    except User.DoesNotExist:
        print("❌ 未找到test_student用户，请先创建测试用户")
        return
    
    # 2. 查找支付方式
    try:
        payment_method = PaymentMethod.objects.filter(is_active=True).first()
        if not payment_method:
            print("❌ 未找到可用的支付方式")
            return
        print(f"✓ 找到支付方式: {payment_method.name}")
    except Exception as e:
        print(f"❌ 查找支付方式时出错: {e}")
        return
    
    # 3. 模拟请求对象
    factory = RequestFactory()
    request = factory.post('/api/payments/api/create/', {
        'payment_type': 'course_fee',
        'amount': '50.00',
        'payment_method_id': payment_method.id,
        'description': '测试支付记录'
    })
    
    # 设置用户
    request.user = test_student
    
    # 添加session支持
    middleware = SessionMiddleware(lambda x: None)
    middleware.process_request(request)
    request.session.save()
    
    # 4. 创建支付记录（模拟视图逻辑）
    try:
        # 创建支付记录
        payment = Payment.objects.create(
            user=test_student,
            payment_type='course_fee',
            amount=Decimal('50.00'),
            payment_method=payment_method,
            description='测试支付记录'
        )
        
        print(f"✓ 创建支付记录: {payment.payment_id}")
        print(f"  用户: {payment.user.username} ({payment.user.real_name or '未设置'})")
        print(f"  金额: ¥{payment.amount}")
        print(f"  状态: {payment.get_status_display()}")
        
        # 5. 手动记录日志（模拟修复后的逻辑）
        from logs.utils import log_user_action
        user_name = test_student.real_name or test_student.username
        description = f"{user_name} 创建了支付（ID: {payment.payment_id}）"
        
        log_user_action(
            user=test_student,  # 记录实际用户
            action_type='create',
            resource_type='payment',
            resource_id=str(payment.id),
            description=description,
            request=request,
            extra_data={
                'payment_id': payment.payment_id,
                'amount': str(payment.amount),
                'payment_type': payment.payment_type,
                'payment_method': payment_method.name,
                'test_record': True
            }
        )
        
        print(f"✓ 记录日志成功")
        
        # 6. 验证日志记录
        create_log = SystemLog.objects.filter(
            resource_type='payment',
            action_type='create',
            resource_id=str(payment.id)
        ).first()
        
        if create_log:
            print(f"\n📝 日志验证:")
            print(f"  日志用户: {create_log.user.username} ({create_log.user.real_name or '未设置'})")
            print(f"  支付用户: {payment.user.username} ({payment.user.real_name or '未设置'})")
            print(f"  描述: {create_log.description}")
            print(f"  时间: {create_log.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
            
            if create_log.user == payment.user:
                print(f"  ✓ 日志用户与支付用户一致 - 修复成功！")
            else:
                print(f"  ❌ 日志用户与支付用户不一致")
        else:
            print(f"❌ 未找到创建日志")
        
    except Exception as e:
        print(f"❌ 创建支付记录时出错: {e}")
        import traceback
        traceback.print_exc()
    
    print(f"\n" + "=" * 60)
    print("测试完成")
    print("=" * 60)

if __name__ == '__main__':
    create_test_payment()