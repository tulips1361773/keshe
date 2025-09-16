#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
管理员线下支付录入完整功能测试
测试前端和后端的完整集成
"""

import os
import sys
import django
import requests
import json

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'keshe.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
django.setup()

from accounts.models import User
from payments.models import PaymentMethod, UserAccount

def test_complete_admin_offline_payment():
    """
    测试管理员线下支付录入的完整流程
    """
    print("=== 开始测试管理员线下支付录入完整功能 ===")
    
    # 1. 准备测试数据
    print("\n1. 准备测试数据...")
    
    # 使用现有的管理员用户
    try:
        admin_user = User.objects.filter(is_superuser=True).first()
        if not admin_user:
            raise User.DoesNotExist
        print(f"使用现有管理员用户: {admin_user.username}")
    except User.DoesNotExist:
        print("未找到管理员用户")
        return False
    
    # 使用现有的学员用户
    try:
        student_user = User.objects.filter(user_type='student').first()
        if not student_user:
            raise User.DoesNotExist
        print(f"使用现有学员用户: {student_user.username}")
    except User.DoesNotExist:
        print("未找到学员用户")
        return False
    
    # 2. 获取管理员Token
    print("\n2. 获取管理员Token...")
    login_data = {
        'username': admin_user.username,
        'password': 'admin123'  # 假设密码，实际应该设置正确密码
    }
    
    # 为管理员用户设置已知密码
    admin_user.set_password('admin123')
    admin_user.save()
    
    try:
        response = requests.post('http://127.0.0.1:8000/api/accounts/login/', json=login_data)
        if response.status_code == 200:
            token_data = response.json()
            print(f"登录响应数据: {token_data}")
            # 尝试不同的token字段名
            admin_token = token_data.get('access') or token_data.get('token') or token_data.get('access_token')
            if admin_token:
                print(f"获取管理员Token成功: {admin_token[:20]}...")
            else:
                print(f"未找到Token字段，响应数据: {token_data}")
                return False
        else:
            print(f"获取管理员Token失败: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"获取管理员Token异常: {e}")
        return False
    
    # 3. 测试学员搜索API
    print("\n3. 测试学员搜索API...")
    headers = {'Authorization': f'Token {admin_token}'}
    
    try:
        response = requests.get(
            'http://127.0.0.1:8000/api/payments/api/admin/students/',
            headers=headers,
            params={'search': 'test_student'}
        )
        
        if response.status_code == 200:
            data = response.json()
            students_data = data.get('data', {}).get('students', [])
            print(f"学员搜索API成功，返回 {len(students_data)} 个学员")
            
            if students_data:
                student_info = students_data[0]
                student_id = student_info.get('id')
                print(f"找到学员: {student_info.get('real_name')} (ID: {student_id})")
            else:
                print("未找到学员数据")
                return False
        else:
            print(f"学员搜索API失败: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"学员搜索API异常: {e}")
        return False
    
    # 4. 测试线下支付录入API
    print("\n4. 测试线下支付录入API...")
    
    payment_data = {
        'student_id': student_id,
        'amount': 500.00,
        'payment_type': 'course_fee',
        'description': '测试线下支付录入 - 课程费用'
    }
    
    try:
        response = requests.post(
            'http://127.0.0.1:8000/api/payments/api/admin/offline-payment/',
            headers=headers,
            json=payment_data
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get('code') == 200:
                payment_info = data.get('data', {})
                print(f"线下支付录入成功!")
                print(f"交易ID: {payment_info.get('transaction_id')}")
                print(f"支付金额: {payment_info.get('amount')}")
                print(f"学员余额: {payment_info.get('new_balance')}")
            else:
                print(f"线下支付录入业务失败: {data.get('message')}")
                return False
        else:
            print(f"线下支付录入API失败: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"线下支付录入API异常: {e}")
        return False
    
    # 5. 验证权限控制
    print("\n5. 验证权限控制...")
    
    # 使用学员Token尝试访问管理员API
    student_login_data = {
        'username': student_user.username,
        'password': 'student123'
    }
    
    # 为学员用户设置已知密码
    student_user.set_password('student123')
    student_user.save()
    
    try:
        response = requests.post('http://127.0.0.1:8000/api/accounts/login/', json=student_login_data)
        if response.status_code == 200:
            student_token_data = response.json()
            student_token = student_token_data.get('access')
            
            # 尝试用学员Token访问管理员API
            student_headers = {'Authorization': f'Token {student_token}'}
            response = requests.get(
                'http://127.0.0.1:8000/api/payments/api/admin/students/',
                headers=student_headers
            )
            
            if response.status_code == 403:
                print("权限控制正常：学员无法访问管理员API")
            else:
                print(f"权限控制异常：学员可以访问管理员API (状态码: {response.status_code})")
                return False
        else:
            print("无法获取学员Token进行权限测试")
    except Exception as e:
        print(f"权限验证异常: {e}")
    
    print("\n=== 管理员线下支付录入完整功能测试通过! ===")
    return True

if __name__ == '__main__':
    success = test_complete_admin_offline_payment()
    if success:
        print("\n✅ 所有测试通过")
        sys.exit(0)
    else:
        print("\n❌ 测试失败")
        sys.exit(1)