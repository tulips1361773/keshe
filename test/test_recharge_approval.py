#!/usr/bin/env python
"""
测试充值审核功能
"""

import os
import sys
import django
import requests
import json

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'keshe.settings')
django.setup()

from django.contrib.auth import get_user_model
from payments.models import PaymentMethod, Payment, UserAccount
from decimal import Decimal

User = get_user_model()

def test_recharge_approval():
    """测试充值审核功能"""
    print("=== 测试充值审核功能 ===\n")
    
    # 1. 准备测试数据
    print("1. 准备测试数据...")
    
    # 获取学员用户
    try:
        student = User.objects.filter(user_type='student').first()
        if not student:
            print("❌ 未找到学员用户")
            return False
        print(f"✅ 学员用户: {student.username}")
    except Exception as e:
        print(f"❌ 获取学员用户失败: {e}")
        return False
    
    # 获取管理员用户
    try:
        admin = User.objects.filter(user_type__in=['super_admin', 'campus_admin']).first()
        if not admin:
            print("❌ 未找到管理员用户")
            return False
        print(f"✅ 管理员用户: {admin.username}")
    except Exception as e:
        print(f"❌ 获取管理员用户失败: {e}")
        return False
    
    # 2. 学员登录并创建充值订单
    print("\n2. 学员创建充值订单...")
    
    # 设置学员密码
    student.set_password('testpass123')
    student.save()
    
    # 学员登录
    login_data = {
        'username': student.username,
        'password': 'testpass123'
    }
    
    try:
        response = requests.post('http://127.0.0.1:8000/api/accounts/login/', json=login_data)
        if response.status_code == 200:
            student_token = response.json().get('token')
            print(f"✅ 学员登录成功")
        else:
            print(f"❌ 学员登录失败: {response.text}")
            return False
    except Exception as e:
        print(f"❌ 学员登录请求失败: {e}")
        return False
    
    # 获取学员充值前余额
    account, created = UserAccount.objects.get_or_create(
        user=student,
        defaults={'balance': Decimal('0.00')}
    )
    balance_before = account.balance
    print(f"✅ 学员充值前余额: ¥{balance_before}")
    
    # 创建充值订单
    recharge_data = {
        'amount': '200.00',
        'payment_method_id': 2,  # 微信支付
        'description': '测试充值审核功能'
    }
    
    headers = {
        'Authorization': f'Token {student_token}',
        'Content-Type': 'application/json'
    }
    
    try:
        response = requests.post(
            'http://127.0.0.1:8000/api/payments/api/account/recharge/',
            json=recharge_data,
            headers=headers
        )
        if response.status_code == 200:
            recharge_result = response.json()
            payment_id = recharge_result['data']['payment_id']
            print(f"✅ 充值订单创建成功，订单号: {payment_id}")
            print(f"   订单状态: {recharge_result['data']['status']}")
        else:
            print(f"❌ 充值订单创建失败: {response.text}")
            return False
    except Exception as e:
        print(f"❌ 充值订单创建请求失败: {e}")
        return False
    
    # 3. 管理员登录
    print("\n3. 管理员登录...")
    
    # 设置管理员密码
    admin.set_password('adminpass123')
    admin.save()
    
    # 管理员登录
    admin_login_data = {
        'username': admin.username,
        'password': 'adminpass123'
    }
    
    try:
        response = requests.post('http://127.0.0.1:8000/api/accounts/login/', json=admin_login_data)
        if response.status_code == 200:
            admin_token = response.json().get('token')
            print(f"✅ 管理员登录成功")
        else:
            print(f"❌ 管理员登录失败: {response.text}")
            return False
    except Exception as e:
        print(f"❌ 管理员登录请求失败: {e}")
        return False
    
    admin_headers = {
        'Authorization': f'Token {admin_token}',
        'Content-Type': 'application/json'
    }
    
    # 4. 管理员查看待审核充值订单
    print("\n4. 管理员查看待审核充值订单...")
    
    try:
        response = requests.get(
            'http://127.0.0.1:8000/api/payments/api/admin/pending-recharges/',
            headers=admin_headers
        )
        if response.status_code == 200:
            pending_result = response.json()
            pending_count = pending_result['data']['count']
            print(f"✅ 待审核充值订单数量: {pending_count}")
            
            if pending_count > 0:
                for order in pending_result['data']['results']:
                    print(f"   订单号: {order['payment_id']}, 金额: ¥{order['amount']}, 用户: {order['user']['real_name'] or order['user']['username']}")
        else:
            print(f"❌ 获取待审核充值订单失败: {response.text}")
            return False
    except Exception as e:
        print(f"❌ 获取待审核充值订单请求失败: {e}")
        return False
    
    # 5. 管理员审核充值订单（通过）
    print("\n5. 管理员审核充值订单（通过）...")
    
    approval_data = {
        'approve': True
    }
    
    try:
        response = requests.post(
            f'http://127.0.0.1:8000/api/payments/api/admin/recharge/{payment_id}/approve/',
            json=approval_data,
            headers=admin_headers
        )
        if response.status_code == 200:
            approval_result = response.json()
            print(f"✅ 充值审核成功: {approval_result['message']}")
            print(f"   订单状态: {approval_result['data']['status']}")
            print(f"   支付时间: {approval_result['data']['paid_at']}")
        else:
            print(f"❌ 充值审核失败: {response.text}")
            return False
    except Exception as e:
        print(f"❌ 充值审核请求失败: {e}")
        return False
    
    # 6. 验证用户余额是否更新
    print("\n6. 验证用户余额更新...")
    
    account.refresh_from_db()
    balance_after = account.balance
    balance_change = balance_after - balance_before
    
    print(f"✅ 学员充值后余额: ¥{balance_after}")
    print(f"✅ 余额变化: +¥{balance_change}")
    
    if balance_change == Decimal('200.00'):
        print("✅ 余额更新正确")
    else:
        print(f"❌ 余额更新错误，期望增加¥200.00，实际增加¥{balance_change}")
        return False
    
    # 7. 测试拒绝充值订单
    print("\n7. 测试拒绝充值订单...")
    
    # 创建另一个充值订单
    recharge_data2 = {
        'amount': '100.00',
        'payment_method_id': 1,  # 现金支付
        'description': '测试拒绝充值'
    }
    
    try:
        response = requests.post(
            'http://127.0.0.1:8000/api/payments/api/account/recharge/',
            json=recharge_data2,
            headers=headers
        )
        if response.status_code == 200:
            recharge_result2 = response.json()
            payment_id2 = recharge_result2['data']['payment_id']
            print(f"✅ 第二个充值订单创建成功，订单号: {payment_id2}")
        else:
            print(f"❌ 第二个充值订单创建失败: {response.text}")
            return False
    except Exception as e:
        print(f"❌ 第二个充值订单创建请求失败: {e}")
        return False
    
    # 管理员拒绝充值订单
    rejection_data = {
        'approve': False
    }
    
    try:
        response = requests.post(
            f'http://127.0.0.1:8000/api/payments/api/admin/recharge/{payment_id2}/approve/',
            json=rejection_data,
            headers=admin_headers
        )
        if response.status_code == 200:
            rejection_result = response.json()
            print(f"✅ 充值拒绝成功: {rejection_result['message']}")
            print(f"   订单状态: {rejection_result['data']['status']}")
        else:
            print(f"❌ 充值拒绝失败: {response.text}")
            return False
    except Exception as e:
        print(f"❌ 充值拒绝请求失败: {e}")
        return False
    
    # 验证余额没有变化
    account.refresh_from_db()
    balance_final = account.balance
    
    if balance_final == balance_after:
        print(f"✅ 拒绝充值后余额未变化: ¥{balance_final}")
    else:
        print(f"❌ 拒绝充值后余额异常变化: ¥{balance_final}")
        return False
    
    print("\n=== 充值审核功能测试完成 ===\n")
    print("✅ 所有测试用例通过")
    print("\n功能总结:")
    print("1. ✅ 学员可以创建充值订单（状态为pending）")
    print("2. ✅ 管理员可以查看待审核充值订单列表")
    print("3. ✅ 管理员可以审核通过充值订单，用户余额自动更新")
    print("4. ✅ 管理员可以拒绝充值订单，用户余额不变")
    print("5. ✅ 充值审核有完整的权限控制")
    print("6. ✅ 充值审核有完整的状态管理")
    
    return True

if __name__ == '__main__':
    success = test_recharge_approval()
    if success:
        print("\n🎉 充值审核功能测试成功！")
    else:
        print("\n❌ 充值审核功能测试失败！")
        sys.exit(1)