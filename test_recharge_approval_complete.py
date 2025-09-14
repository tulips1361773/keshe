#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
充值审核功能完整测试脚本
测试从学员充值申请到管理员审核的完整流程
"""

import os
import sys
import django
import json
from decimal import Decimal
from datetime import datetime
import random

# 设置Django环境
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'keshe.settings')
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model
from payments.models import Payment, PaymentMethod, UserAccount
from accounts.models import User

User = get_user_model()

def test_complete_recharge_approval_flow():
    """
    测试完整的充值审核流程
    1. 学员创建充值订单
    2. 管理员查看待审核订单
    3. 管理员审核通过订单
    4. 验证余额更新
    5. 管理员拒绝订单
    6. 验证权限控制
    """
    print("\n=== 充值审核功能完整测试 ===")
    
    client = Client()
    
    # 1. 准备测试数据
    print("\n1. 准备测试数据...")
    
    # 创建学员用户
    student_username = f'test_student_recharge_{random.randint(1000, 9999)}'
    student_phone = f'138{random.randint(10000000, 99999999)}'
    
    # 删除可能存在的同名用户
    User.objects.filter(username__startswith='test_student_recharge').delete()
    
    student_user = User.objects.create_user(
        username=student_username,
        email=f'student_recharge_{random.randint(1000, 9999)}@test.com',
        password='testpass123',
        user_type='student',
        real_name='测试学员充值',
        phone=student_phone
    )
    print(f"   创建学员用户: {student_user.username}")
    
    # 创建管理员用户
    admin_username = f'test_admin_approval_{random.randint(1000, 9999)}'
    admin_phone = f'139{random.randint(10000000, 99999999)}'
    
    # 删除可能存在的同名用户
    User.objects.filter(username__startswith='test_admin_approval').delete()
    
    admin_user = User.objects.create_user(
        username=admin_username,
        email=f'admin_approval_{random.randint(1000, 9999)}@test.com',
        password='testpass123',
        user_type='campus_admin',
        real_name='测试管理员审核',
        phone=admin_phone
    )
    print(f"   创建管理员用户: {admin_user.username}")
    
    # 确保用户账户存在
    student_account, created = UserAccount.objects.get_or_create(
        user=student_user,
        defaults={'balance': Decimal('0.00')}
    )
    if created:
        print(f"   创建学员账户: 初始余额 ¥{student_account.balance}")
    else:
        print(f"   学员账户余额: ¥{student_account.balance}")
    
    # 获取支付方式
    try:
        payment_method = PaymentMethod.objects.filter(is_active=True).first()
        if not payment_method:
            payment_method = PaymentMethod.objects.create(
                name='微信支付',
                method_type='wechat',
                is_active=True
            )
        print(f"   支付方式: {payment_method.name}")
    except Exception as e:
        print(f"   支付方式获取失败: {e}")
        return False
    
    # 2. 学员登录并创建充值订单
    print("\n2. 学员登录并创建充值订单...")
    
    # 学员登录
    login_response = client.post('/api/accounts/login/', {
        'username': student_username,
        'password': 'testpass123'
    })
    
    if login_response.status_code == 200:
        login_data = json.loads(login_response.content)
        if login_data.get('success'):
            student_token = login_data['token']
            print(f"   ✅ 学员登录成功")
        else:
            print(f"   ❌ 学员登录失败: {login_data.get('message')}")
            return False
    else:
        print(f"   ❌ 学员登录失败: HTTP状态码 {login_response.status_code}")
        return False
    
    # 创建充值订单
    recharge_data = {
        'amount': '100.00',
        'payment_method_id': payment_method.id,
        'description': '测试充值审核流程'
    }
    
    recharge_response = client.post(
        '/api/payments/api/account/recharge/',
        json.dumps(recharge_data),
        content_type='application/json',
        HTTP_AUTHORIZATION=f'Bearer {student_token}'
    )
    
    if recharge_response.status_code == 200:
        recharge_result = json.loads(recharge_response.content)
        if recharge_result.get('code') == 200:
            payment_id = recharge_result['data']['payment_id']
            print(f"   ✅ 充值订单创建成功: {payment_id}")
        else:
            print(f"   ❌ 充值订单创建失败: {recharge_result.get('message')}")
            return False
    else:
        print(f"   ❌ 充值订单创建请求失败: {recharge_response.status_code}")
        return False
    
    # 3. 管理员登录
    print("\n3. 管理员登录...")
    
    admin_login_response = client.post('/api/accounts/login/', {
        'username': admin_username,
        'password': 'testpass123'
    })
    
    if admin_login_response.status_code == 200:
        admin_login_data = json.loads(admin_login_response.content)
        if admin_login_data.get('success'):
            admin_token = admin_login_data['token']
            print(f"   ✅ 管理员登录成功")
        else:
            print(f"   ❌ 管理员登录失败: {admin_login_data.get('message')}")
            return False
    else:
        print(f"   ❌ 管理员登录失败: HTTP状态码 {admin_login_response.status_code}")
        return False
    
    # 4. 管理员查看待审核订单
    print("\n4. 管理员查看待审核订单...")
    
    pending_response = client.get(
        '/api/payments/api/admin/pending-recharges/',
        HTTP_AUTHORIZATION=f'Bearer {admin_token}'
    )
    
    if pending_response.status_code == 200:
        pending_data = json.loads(pending_response.content)
        if pending_data.get('code') == 200:
            pending_orders = pending_data['data']['results']
            print(f"   ✅ 获取待审核订单成功: {len(pending_orders)}个订单")
            
            # 查找我们创建的订单
            target_order = None
            for order in pending_orders:
                if order['payment_id'] == payment_id:
                    target_order = order
                    break
            
            if target_order:
                print(f"   📋 找到目标订单: {target_order['payment_id']}")
                print(f"      用户: {target_order['user']['real_name']}")
                print(f"      金额: ¥{target_order['amount']}")
                print(f"      状态: {target_order['status']}")
            else:
                print(f"   ❌ 未找到目标订单: {payment_id}")
                return False
        else:
            print(f"   ❌ 获取待审核订单失败: {pending_data.get('message')}")
            return False
    else:
        print(f"   ❌ 获取待审核订单请求失败: {pending_response.status_code}")
        return False
    
    # 5. 管理员审核通过订单
    print("\n5. 管理员审核通过订单...")
    
    # 记录审核前的余额
    student_account.refresh_from_db()
    balance_before = student_account.balance
    print(f"   审核前余额: ¥{balance_before}")
    
    approve_response = client.post(
        f'/api/payments/api/admin/recharge/{payment_id}/approve/',
        json.dumps({'approve': True}),
        content_type='application/json',
        HTTP_AUTHORIZATION=f'Bearer {admin_token}'
    )
    
    if approve_response.status_code == 200:
        approve_data = json.loads(approve_response.content)
        if approve_data.get('code') == 200:
            print(f"   ✅ 订单审核通过成功: {approve_data.get('message')}")
            
            # 验证余额更新
            student_account.refresh_from_db()
            balance_after = student_account.balance
            print(f"   审核后余额: ¥{balance_after}")
            
            expected_balance = balance_before + Decimal('100.00')
            if balance_after == expected_balance:
                print(f"   ✅ 余额更新正确: +¥100.00")
            else:
                print(f"   ❌ 余额更新错误: 期望¥{expected_balance}, 实际¥{balance_after}")
                return False
            
            # 验证订单状态
            payment = Payment.objects.get(payment_id=payment_id)
            if payment.status == 'completed':
                print(f"   ✅ 订单状态更新正确: {payment.status}")
            else:
                print(f"   ❌ 订单状态更新错误: {payment.status}")
                return False
        else:
            print(f"   ❌ 订单审核失败: {approve_data.get('message')}")
            return False
    else:
        print(f"   ❌ 订单审核请求失败: {approve_response.status_code}")
        return False
    
    # 6. 测试拒绝订单功能
    print("\n6. 测试拒绝订单功能...")
    
    # 创建另一个充值订单用于拒绝测试
    recharge_data_2 = {
        'amount': '50.00',
        'payment_method_id': payment_method.id,
        'description': '测试拒绝功能'
    }
    
    recharge_response_2 = client.post(
        '/api/payments/api/account/recharge/',
        json.dumps(recharge_data_2),
        content_type='application/json',
        HTTP_AUTHORIZATION=f'Bearer {student_token}'
    )
    
    if recharge_response_2.status_code == 200:
        recharge_result_2 = json.loads(recharge_response_2.content)
        if recharge_result_2.get('code') == 200:
            payment_id_2 = recharge_result_2['data']['payment_id']
            print(f"   创建第二个充值订单: {payment_id_2}")
        else:
            print(f"   ❌ 第二个充值订单创建失败")
            return False
    else:
        print(f"   ❌ 第二个充值订单创建请求失败")
        return False
    
    # 拒绝订单
    reject_response = client.post(
        f'/api/payments/api/admin/recharge/{payment_id_2}/approve/',
        json.dumps({
            'approve': False,
            'reason': '测试拒绝原因'
        }),
        content_type='application/json',
        HTTP_AUTHORIZATION=f'Bearer {admin_token}'
    )
    
    if reject_response.status_code == 200:
        reject_data = json.loads(reject_response.content)
        if reject_data.get('code') == 200:
            print(f"   ✅ 订单拒绝成功: {reject_data.get('message')}")
            
            # 验证订单状态
            payment_2 = Payment.objects.get(payment_id=payment_id_2)
            if payment_2.status == 'failed':
                print(f"   ✅ 拒绝订单状态正确: {payment_2.status}")
            else:
                print(f"   ❌ 拒绝订单状态错误: {payment_2.status}")
                return False
            
            # 验证余额未变化
            student_account.refresh_from_db()
            if student_account.balance == balance_after:
                print(f"   ✅ 拒绝后余额未变化: ¥{student_account.balance}")
            else:
                print(f"   ❌ 拒绝后余额异常变化")
                return False
        else:
            print(f"   ❌ 订单拒绝失败: {reject_data.get('message')}")
            return False
    else:
        print(f"   ❌ 订单拒绝请求失败: {reject_response.status_code}")
        return False
    
    # 7. 测试权限控制
    print("\n7. 测试权限控制...")
    
    # 重新用学员身份登录
    student_login_again = client.post('/api/accounts/login/', {
        'username': student_username,
        'password': 'testpass123'
    })
    
    if student_login_again.status_code == 200:
        student_login_data = json.loads(student_login_again.content)
        if student_login_data.get('success'):
            student_token_fresh = student_login_data['token']
        else:
            print(f"   ❌ 学员重新登录失败: {student_login_data.get('message')}")
            return False
    else:
        print(f"   ❌ 学员重新登录失败: HTTP状态码 {student_login_again.status_code}")
        return False
    
    # 学员尝试访问管理员API
    unauthorized_response = client.get(
        '/api/payments/api/admin/pending-recharges/',
        HTTP_AUTHORIZATION=f'Bearer {student_token_fresh}'
    )
    
    if unauthorized_response.status_code == 403:
        print(f"   ✅ 权限控制正常: 学员无法访问管理员API")
    else:
        unauthorized_data = json.loads(unauthorized_response.content)
        if unauthorized_data.get('code') == 403:
            print(f"   ✅ 权限控制正常: {unauthorized_data.get('message')}")
        else:
            print(f"   ❌ 权限控制异常: 学员可以访问管理员API")
            return False
    
    print("\n=== 充值审核功能测试完成 ===")
    print("\n📊 测试结果汇总:")
    print("   ✅ 学员充值订单创建")
    print("   ✅ 管理员查看待审核订单")
    print("   ✅ 管理员审核通过订单")
    print("   ✅ 余额正确更新")
    print("   ✅ 管理员拒绝订单")
    print("   ✅ 权限控制正常")
    print("\n🎉 所有测试通过！充值审核功能运行正常！")
    
    return True

if __name__ == '__main__':
    try:
        success = test_complete_recharge_approval_flow()
        if success:
            print("\n✅ 充值审核功能测试成功！")
        else:
            print("\n❌ 充值审核功能测试失败！")
            sys.exit(1)
    except Exception as e:
        print(f"\n💥 测试过程中发生异常: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)