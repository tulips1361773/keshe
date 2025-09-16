#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
教练员注册和审核流程测试脚本
"""

import os
import sys
import django
import requests
import json
from datetime import datetime

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'keshe.settings')
django.setup()

from django.contrib.auth import get_user_model
from accounts.models import User

User = get_user_model()

# 测试配置
BASE_URL = 'http://127.0.0.1:8000'
REGISTER_URL = f'{BASE_URL}/accounts/api/register/'
LOGIN_URL = f'{BASE_URL}/accounts/api/login/'

def print_separator(title):
    print(f"\n{'='*50}")
    print(f"{title}")
    print(f"{'='*50}")

def test_coach_registration():
    """测试教练员注册流程"""
    print("\n=== 测试教练员注册流程 ===")
    
    # 生成唯一的测试数据
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S%f')[:-3]
    
    # 教练员注册数据
    coach_data = {
        'username': f'coach_test_{timestamp}',
        'password': 'TestPass123!',
        'password_confirm': 'TestPass123!',
        'real_name': '李教练',
        'phone': f'138{timestamp[-8:]}',  # 生成11位手机号
        'email': f'coach_test_{timestamp}@test.com',
        'user_type': 'coach',
        'gender': 'male',
        'achievements': '国家一级教练员，10年教学经验'
    }
    
    try:
        response = requests.post(REGISTER_URL, data=coach_data)
        print(f"状态码: {response.status_code}")
        print(f"响应内容: {response.text}")
        
        if response.status_code == 201:
            result = response.json()
            print("✅ 教练员注册成功")
            user_id = result.get('user', {}).get('id')
            username = result.get('user', {}).get('username')
            print(f"用户ID: {user_id}")
            print(f"用户名: {username}")
            
            # 检查用户状态
            if user_id:
                user = User.objects.get(id=user_id)
                print(f"用户激活状态: {user.is_active}")
                print(f"会员激活状态: {user.is_active_member}")
                
                # 教练员应该默认未激活，需要审核
                if user.user_type == 'coach' and not user.is_active_member:
                    print("✅ 教练员注册后正确设置为待审核状态")
                    return user_id, username
                else:
                    print("❌ 教练员注册后状态设置不正确")
            
            return user_id, username
        else:
            print(f"❌ 教练员注册失败: {response.text}")
            return None, None
            
    except Exception as e:
        print(f"❌ 教练员注册测试出错: {str(e)}")
        return None, None

def test_coach_login_before_approval(username):
    """测试教练员审核前登录"""
    print("\n=== 测试教练员审核前登录 ===")
    
    login_data = {
        'username': username,
        'password': 'TestPass123!'
    }
    
    try:
        response = requests.post(LOGIN_URL, data=login_data)
        print(f"状态码: {response.status_code}")
        print(f"响应内容: {response.text}")
        
        if response.status_code == 400:
            print("✅ 正确拒绝未审核教练员登录")
            return True
        else:
            print("❌ 应该拒绝未审核教练员登录")
            return False
            
    except Exception as e:
        print(f"❌ 教练员登录测试出错: {str(e)}")
        return False

def test_coach_approval(user_id):
    """测试教练员审核流程"""
    print("\n=== 测试教练员审核流程 ===")
    
    try:
        # 模拟管理员审核通过
        user = User.objects.get(id=user_id)
        print(f"审核前状态: is_active={user.is_active}, is_active_member={user.is_active_member}")
        
        # 审核通过
        user.is_active_member = True
        user.save()
        
        print(f"审核后状态: is_active={user.is_active}, is_active_member={user.is_active_member}")
        print("✅ 教练员审核通过")
        return True
        
    except Exception as e:
        print(f"❌ 教练员审核测试出错: {str(e)}")
        return False

def test_coach_login_after_approval(username):
    """测试教练员审核后登录"""
    print("\n=== 测试教练员审核后登录 ===")
    
    login_data = {
        'username': username,
        'password': 'TestPass123!'
    }
    
    try:
        response = requests.post(LOGIN_URL, data=login_data)
        print(f"状态码: {response.status_code}")
        print(f"响应内容: {response.text}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ 审核后教练员登录成功")
            print(f"获得Token: {result.get('token', 'N/A')[:20]}...")
            return True
        else:
            print(f"❌ 审核后教练员登录失败: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ 教练员登录测试出错: {str(e)}")
        return False

def test_coach_required_fields():
    """测试教练员注册必填字段"""
    print("\n=== 测试教练员注册必填字段 ===")
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S%f')[:-3]
    base_data = {
        'username': f'coach_test_{timestamp}',
        'password': 'TestPass123!',
        'password_confirm': 'TestPass123!',
        'real_name': '李教练',
        'phone': f'138{timestamp[-8:]}',
        'email': f'coach_test_{timestamp}@test.com',
        'user_type': 'coach',
        'gender': 'male',
        'achievements': '国家一级教练员'
    }
    
    # 测试缺少成就描述
    test_cases = [
        ('缺少成就描述', 'achievements'),
    ]
    
    passed = 0
    total = len(test_cases)
    
    for test_name, missing_field in test_cases:
        print(f"\n测试: {test_name}")
        test_data = base_data.copy()
        del test_data[missing_field]
        
        try:
            response = requests.post(REGISTER_URL, data=test_data)
            if response.status_code == 400:
                print(f"✅ 正确拒绝: {response.json().get('error', response.text)}")
                passed += 1
            else:
                print(f"❌ 应该拒绝但通过了: {response.text}")
        except Exception as e:
            print(f"❌ 测试出错: {str(e)}")
    
    print(f"\n教练员必填字段验证测试结果: {passed}/{total} 通过")
    return passed == total

def main():
    """主测试函数"""
    print_separator("教练员注册和审核流程测试")
    
    results = {
        'registration': False,
        'login_before_approval': False,
        'approval': False,
        'login_after_approval': False,
        'required_fields': False
    }
    
    # 1. 测试教练员注册
    user_id, username = test_coach_registration()
    if user_id and username:
        results['registration'] = True
        
        # 2. 测试审核前登录
        results['login_before_approval'] = test_coach_login_before_approval(username)
        
        # 3. 测试审核流程
        if test_coach_approval(user_id):
            results['approval'] = True
            
            # 4. 测试审核后登录
            results['login_after_approval'] = test_coach_login_after_approval(username)
    
    # 5. 测试必填字段
    results['required_fields'] = test_coach_required_fields()
    
    # 输出测试结果
    print_separator("测试结果汇总")
    print(f"教练员注册: {'✅ 通过' if results['registration'] else '❌ 失败'}")
    print(f"审核前登录拒绝: {'✅ 通过' if results['login_before_approval'] else '❌ 失败'}")
    print(f"审核流程: {'✅ 通过' if results['approval'] else '❌ 失败'}")
    print(f"审核后登录: {'✅ 通过' if results['login_after_approval'] else '❌ 失败'}")
    print(f"必填字段验证: {'✅ 通过' if results['required_fields'] else '❌ 失败'}")
    
    passed = sum(results.values())
    total = len(results)
    print(f"\n总体结果: {passed}/{total} 测试通过")
    
    if passed == total:
        print("🎉 所有测试都通过了！")
    else:
        print("⚠️ 部分测试失败，需要检查相关功能")

if __name__ == '__main__':
    main()