#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试管理员线下支付录入功能的前端API接口
"""

import os
import sys
import django
import requests
import json
from decimal import Decimal

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'keshe.settings')
django.setup()

from accounts.models import User, UserProfile
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from payments.models import PaymentMethod, UserAccount

def test_admin_frontend_apis():
    """
    测试管理员前端API接口
    """
    print("=== 测试管理员线下支付录入前端API接口 ===")
    
    base_url = 'http://127.0.0.1:8000'
    
    # 1. 创建或获取测试用户
    print("\n1. 准备测试数据...")
    
    # 获取或创建管理员用户
    try:
        admin_user = User.objects.get(username='test_admin')
        print(f"使用现有管理员用户: {admin_user.username}")
    except User.DoesNotExist:
        admin_user = User.objects.create(
            username='test_admin',
            real_name='测试管理员',
            user_type='campus_admin',
            phone='13800001001',
            email='admin_offline@test.com',
            is_active=True
        )
        admin_user.set_password('admin123')
        admin_user.save()
        print(f"创建管理员用户: {admin_user.username}")
    
    # 获取或创建学员用户
    try:
        student_user = User.objects.get(username='test_student_offline')
        print(f"使用现有学员用户: {student_user.username}")
    except User.DoesNotExist:
        student_user = User.objects.create(
            username='test_student_offline',
            real_name='测试学员线下',
            user_type='student',
            phone='13800001002',
            email='student_offline@test.com',
            is_active=True
        )
        student_user.set_password('student123')
        student_user.save()
        print(f"创建学员用户: {student_user.username}")
    
    # 获取管理员Token
    admin_token, _ = Token.objects.get_or_create(user=admin_user)
    print(f"✓ 获取管理员Token成功: {admin_token.key[:20]}...")
    headers = {
        'Authorization': f'Token {admin_token.key}',
        'Content-Type': 'application/json'
    }
    
    # 2. 测试学员搜索API
    print("\n--- 测试学员搜索API ---")
    try:
        response = requests.get(
            f'{base_url}/api/payments/api/admin/students/',
            headers=headers
        )
        
        if response.status_code == 200:
            data = response.json()
            students_data = data.get('data', {}).get('students', [])
            print(f"✓ 学员搜索API测试成功")
            print(f"  - 返回学员数量: {len(students_data)}")
            if students_data:
                student = students_data[0]
                print(f"  - 示例学员: {student.get('real_name')} ({student.get('username')})")
                student_id = student.get('id')
            else:
                print("  - 未找到学员数据")
                student_id = None
        else:
            print(f"✗ 学员搜索API测试失败: {response.status_code}")
            print(f"  响应内容: {response.text}")
            return False
    except Exception as e:
        print(f"✗ 学员搜索API请求异常: {e}")
        return False
    
    # 3. 测试线下支付录入API
    print("\n--- 测试线下支付录入API ---")
    if 'student_id' in locals() and student_id is not None:
        try:
            payment_data = {
                'student_id': student_id,
                'amount': 500.00,
                'payment_type': 'course_fee',
                'description': '前端测试 - 线下现金支付课程费用'
            }
            
            response = requests.post(
                f'{base_url}/api/payments/api/admin/offline-payment/',
                headers=headers,
                json=payment_data
            )
            
            if response.status_code == 200:
                response_data = response.json()
                if response_data.get('code') == 200:
                    data = response_data.get('data', {})
                    print(f"✓ 线下支付录入API测试成功")
                    print(f"  - 支付记录ID: {data.get('id')}")
                    print(f"  - 支付金额: ¥{data.get('amount')}")
                    print(f"  - 支付状态: {data.get('status')}")
                else:
                    print(f"✗ 线下支付录入API业务失败: {response_data.get('message')}")
                    return False
            else:
                print(f"✗ 线下支付录入API测试失败: {response.status_code}")
                print(f"  响应内容: {response.text}")
                return False
        except Exception as e:
            print(f"✗ 线下支付录入API请求异常: {e}")
            return False
    else:
        print("✗ 无法测试线下支付录入API，未找到学员")
        return False
    
    # 4. 测试权限验证（使用学员Token）
    print("\n--- 测试权限验证 ---")
    try:
        student_user = User.objects.get(username='test_student_offline')
        student_token, _ = Token.objects.get_or_create(user=student_user)
        
        student_headers = {
            'Authorization': f'Token {student_token.key}',
            'Content-Type': 'application/json'
        }
        
        # 尝试用学员Token访问管理员API
        response = requests.get(
            f'{base_url}/api/payments/api/admin/students/',
            headers=student_headers
        )
        
        if response.status_code == 403:
            print("✓ 权限验证测试成功 - 学员无法访问管理员API")
        else:
            print(f"✗ 权限验证测试失败 - 学员可以访问管理员API: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"✗ 权限验证测试异常: {e}")
        return False
    
    print("\n=== 所有前端API测试完成 ===")
    return True

if __name__ == '__main__':
    success = test_admin_frontend_apis()
    if success:
        print("\n🎉 管理员线下支付录入前端API功能测试通过！")
        sys.exit(0)
    else:
        print("\n❌ 管理员线下支付录入前端API功能测试失败！")
        sys.exit(1)