#!/usr/bin/env python
"""
测试充值功能修复
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
from payments.models import PaymentMethod

User = get_user_model()

def test_recharge_api():
    """测试充值API"""
    print("=== 测试充值功能修复 ===")
    
    # 1. 准备测试数据
    print("\n1. 准备测试数据...")
    
    # 获取测试用户
    try:
        user = User.objects.filter(user_type='student').first()
        if not user:
            print("❌ 未找到学员用户")
            return False
        print(f"✅ 使用测试用户: {user.username}")
    except Exception as e:
        print(f"❌ 获取用户失败: {e}")
        return False
    
    # 检查支付方式
    payment_methods = PaymentMethod.objects.filter(is_active=True)
    print(f"✅ 可用支付方式: {[f'{pm.id}-{pm.name}' for pm in payment_methods]}")
    
    # 2. 用户登录获取token
    print("\n2. 用户登录获取token...")
    
    # 设置用户密码
    user.set_password('testpass123')
    user.save()
    
    login_data = {
        'username': user.username,
        'password': 'testpass123'
    }
    
    try:
        response = requests.post('http://127.0.0.1:8000/api/accounts/login/', json=login_data)
        if response.status_code == 200:
            token = response.json().get('token')
            print(f"✅ 登录成功，获取token: {token[:20]}...")
        else:
            print(f"❌ 登录失败: {response.text}")
            return False
    except Exception as e:
        print(f"❌ 登录请求失败: {e}")
        return False
    
    # 3. 测试充值API
    print("\n3. 测试充值API...")
    
    headers = {
        'Authorization': f'Token {token}',
        'Content-Type': 'application/json'
    }
    
    # 测试不同的充值数据
    test_cases = [
        {
            'name': '正常充值 - 现金支付',
            'data': {
                'amount': '100.00',
                'payment_method_id': 1,
                'description': '测试充值'
            }
        },
        {
            'name': '正常充值 - 微信支付',
            'data': {
                'amount': '50.00',
                'payment_method_id': 2,
                'description': '微信充值测试'
            }
        },
        {
            'name': '异常充值 - 无效支付方式',
            'data': {
                'amount': '30.00',
                'payment_method_id': 999,
                'description': '无效支付方式测试'
            }
        },
        {
            'name': '异常充值 - 金额过大',
            'data': {
                'amount': '20000.00',
                'payment_method_id': 1,
                'description': '金额过大测试'
            }
        }
    ]
    
    success_count = 0
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n  测试 {i}: {test_case['name']}")
        
        try:
            response = requests.post(
                'http://127.0.0.1:8000/api/payments/api/account/recharge/',
                json=test_case['data'],
                headers=headers
            )
            
            print(f"    状态码: {response.status_code}")
            print(f"    响应: {response.text[:200]}...")
            
            if i <= 2:  # 前两个应该成功
                if response.status_code == 200:
                    print("    ✅ 测试通过")
                    success_count += 1
                else:
                    print("    ❌ 测试失败")
            else:  # 后两个应该失败
                if response.status_code != 200:
                    print("    ✅ 正确处理异常情况")
                    success_count += 1
                else:
                    print("    ❌ 应该失败但成功了")
                    
        except Exception as e:
            print(f"    ❌ 请求异常: {e}")
    
    print(f"\n=== 测试结果: {success_count}/{len(test_cases)} 通过 ===")
    return success_count == len(test_cases)

if __name__ == '__main__':
    success = test_recharge_api()
    sys.exit(0 if success else 1)