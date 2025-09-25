#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试校区管理员线下支付录入功能
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

from accounts.models import User
from payments.models import PaymentMethod, UserAccount
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

def test_admin_offline_payment():
    """测试管理员线下支付录入功能"""
    print("=== 测试校区管理员线下支付录入功能 ===")
    
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
    
    # 确保现金支付方式存在
    cash_method, created = PaymentMethod.objects.get_or_create(
        method_type='cash',
        defaults={
            'name': '现金支付',
            'is_active': True,
            'description': '线下现金支付'
        }
    )
    if created:
        print(f"创建现金支付方式: {cash_method.name}")
    else:
        print(f"使用现有现金支付方式: {cash_method.name}")
    
    # 2. 获取管理员Token
    print("\n2. 获取管理员认证Token...")
    token, created = Token.objects.get_or_create(user=admin_user)
    print(f"管理员Token: {token.key[:10]}...")
    
    # 3. 测试获取学员列表API
    print("\n3. 测试获取学员列表API...")
    headers = {
        'Authorization': f'Token {token.key}',
        'Content-Type': 'application/json'
    }
    
    try:
        response = requests.get(
            'http://127.0.0.1:8000/payments/api/admin/students/',
            headers=headers
        )
        print(f"学员列表API状态码: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"获取到 {len(data['data']['students'])} 个学员")
            for student in data['data']['students'][:3]:  # 只显示前3个
                print(f"  - {student['real_name']} ({student['username']})")
        else:
            print(f"获取学员列表失败: {response.text}")
    except Exception as e:
        print(f"请求学员列表API失败: {e}")
    
    # 4. 测试线下支付录入API
    print("\n4. 测试线下支付录入API...")
    
    # 获取学员充值前的余额
    account, created = UserAccount.objects.get_or_create(
        user=student_user,
        defaults={'balance': Decimal('0.00')}
    )
    balance_before = account.balance
    print(f"学员充值前余额: ¥{balance_before}")
    
    # 发送线下支付录入请求
    payment_data = {
        'student_id': student_user.id,
        'amount': '100.00',
        'payment_type': 'course_fee',
        'description': '线下现金充值测试'
    }
    
    try:
        response = requests.post(
            'http://127.0.0.1:8000/payments/api/admin/offline-payment/',
            headers=headers,
            json=payment_data
        )
        print(f"线下支付录入API状态码: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"录入成功: {data['message']}")
            payment_info = data['data']
            print(f"支付单号: {payment_info['payment_id']}")
            print(f"支付金额: ¥{payment_info['amount']}")
            print(f"支付状态: {payment_info['status']}")
            
            # 验证账户余额是否更新
            account.refresh_from_db()
            balance_after = account.balance
            print(f"学员充值后余额: ¥{balance_after}")
            print(f"余额变化: +¥{balance_after - balance_before}")
            
        else:
            print(f"线下支付录入失败: {response.text}")
    except Exception as e:
        print(f"请求线下支付录入API失败: {e}")
    
    # 5. 测试权限验证
    print("\n5. 测试权限验证...")
    
    # 创建普通学员Token
    student_token, created = Token.objects.get_or_create(user=student_user)
    student_headers = {
        'Authorization': f'Token {student_token.key}',
        'Content-Type': 'application/json'
    }
    
    try:
        response = requests.post(
            'http://127.0.0.1:8000/payments/api/admin/offline-payment/',
            headers=student_headers,
            json=payment_data
        )
        print(f"学员访问管理员API状态码: {response.status_code}")
        if response.status_code == 403:
            print("权限验证正常: 学员无法访问管理员API")
        else:
            print(f"权限验证异常: {response.text}")
    except Exception as e:
        print(f"权限验证测试失败: {e}")
    
    print("\n=== 测试完成 ===")

if __name__ == '__main__':
    test_admin_offline_payment()