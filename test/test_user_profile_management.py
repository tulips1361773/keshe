#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
用户信息维护功能测试脚本
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
PROFILE_URL = f'{BASE_URL}/accounts/api/profile/'
UPDATE_PROFILE_URL = f'{BASE_URL}/accounts/api/profile/update/'
CHANGE_PASSWORD_URL = f'{BASE_URL}/accounts/api/change-password/'

def print_separator(title):
    print(f"\n{'='*50}")
    print(f"{title}")
    print(f"{'='*50}")

def create_test_user():
    """创建测试用户"""
    print("\n=== 创建测试用户 ===")
    
    # 生成唯一的测试数据
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S%f')[:-3]
    
    # 学员注册数据
    user_data = {
        'username': f'profile_test_{timestamp}',
        'password': 'TestPass123!',
        'password_confirm': 'TestPass123!',
        'real_name': '测试用户',
        'phone': f'139{timestamp[-8:]}',  # 生成11位手机号
        'email': f'profile_test_{timestamp}@test.com',
        'user_type': 'student',
        'gender': 'male'
    }
    
    try:
        response = requests.post(REGISTER_URL, data=user_data)
        if response.status_code == 201:
            result = response.json()
            print("✅ 测试用户创建成功")
            return user_data['username'], user_data['password']
        else:
            print(f"❌ 测试用户创建失败: {response.text}")
            return None, None
    except Exception as e:
        print(f"❌ 创建测试用户出错: {str(e)}")
        return None, None

def login_user(username, password):
    """用户登录获取token"""
    login_data = {
        'username': username,
        'password': password
    }
    
    try:
        response = requests.post(LOGIN_URL, data=login_data)
        if response.status_code == 200:
            result = response.json()
            return result.get('token')
        else:
            print(f"❌ 登录失败: {response.text}")
            return None
    except Exception as e:
        print(f"❌ 登录出错: {str(e)}")
        return None

def test_get_profile(token):
    """测试获取用户资料"""
    print("\n=== 测试获取用户资料 ===")
    
    headers = {'Authorization': f'Token {token}'}
    
    try:
        response = requests.get(PROFILE_URL, headers=headers)
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ 成功获取用户资料")
            print(f"用户名: {result.get('user', {}).get('username')}")
            print(f"真实姓名: {result.get('user', {}).get('real_name')}")
            print(f"邮箱: {result.get('user', {}).get('email')}")
            return True
        else:
            print(f"❌ 获取用户资料失败: {response.text}")
            return False
    except Exception as e:
        print(f"❌ 获取用户资料出错: {str(e)}")
        return False

def test_update_profile(token):
    """测试更新用户资料"""
    print("\n=== 测试更新用户资料 ===")
    
    headers = {
        'Authorization': f'Token {token}',
        'Content-Type': 'application/json'
    }
    
    # 更新数据 - 使用时间戳确保邮箱唯一性
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S%f')[:-3]
    update_data = {
        'real_name': '更新后的姓名',
        'email': f'updated_email_{timestamp}@test.com',
        'gender': 'female',
        'address': '北京市朝阳区',
        'emergency_contact': '紧急联系人',
        'emergency_phone': '13800138000',
        'bio': '这是更新后的个人简介',
        'skills': '乒乓球基础技能',
        'experience_years': 2
    }
    
    try:
        response = requests.put(UPDATE_PROFILE_URL, 
                              data=json.dumps(update_data), 
                              headers=headers)
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ 用户资料更新成功")
            print(f"更新后姓名: {result.get('user', {}).get('real_name')}")
            print(f"更新后邮箱: {result.get('user', {}).get('email')}")
            print(f"更新后地址: {result.get('user', {}).get('address')}")
            return True
        else:
            print(f"❌ 用户资料更新失败: {response.text}")
            return False
    except Exception as e:
        print(f"❌ 用户资料更新出错: {str(e)}")
        return False

def test_change_password(token, username, old_password):
    """测试修改密码"""
    print("\n=== 测试修改密码 ===")
    
    headers = {
        'Authorization': f'Token {token}',
        'Content-Type': 'application/json'
    }
    
    # 修改密码数据
    password_data = {
        'old_password': old_password,
        'new_password': 'NewPass456!',
        'confirm_password': 'NewPass456!'
    }
    
    try:
        response = requests.post(CHANGE_PASSWORD_URL, 
                               data=json.dumps(password_data), 
                               headers=headers)
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ 密码修改成功")
            
            # 验证新密码是否生效
            print("验证新密码是否生效...")
            new_token = login_user(username, 'NewPass456!')
            if new_token:
                print("✅ 新密码登录成功")
                return True, 'NewPass456!'
            else:
                print("❌ 新密码登录失败")
                return False, old_password
        else:
            print(f"❌ 密码修改失败: {response.text}")
            return False, old_password
    except Exception as e:
        print(f"❌ 密码修改出错: {str(e)}")
        return False, old_password

def test_change_password_validation(token):
    """测试修改密码验证"""
    print("\n=== 测试修改密码验证 ===")
    
    headers = {
        'Authorization': f'Token {token}',
        'Content-Type': 'application/json'
    }
    
    test_cases = [
        {
            'name': '旧密码错误',
            'data': {
                'old_password': 'WrongPassword',
                'new_password': 'NewPass789!',
                'confirm_password': 'NewPass789!'
            }
        },
        {
            'name': '新密码确认不匹配',
            'data': {
                'old_password': 'NewPass456!',
                'new_password': 'NewPass789!',
                'confirm_password': 'DifferentPass!'
            }
        },
        {
            'name': '新密码太简单',
            'data': {
                'old_password': 'NewPass456!',
                'new_password': '123456',
                'confirm_password': '123456'
            }
        }
    ]
    
    passed = 0
    total = len(test_cases)
    
    for test_case in test_cases:
        print(f"\n测试: {test_case['name']}")
        try:
            response = requests.post(CHANGE_PASSWORD_URL, 
                                   data=json.dumps(test_case['data']), 
                                   headers=headers)
            if response.status_code == 400:
                print(f"✅ 正确拒绝: {response.json().get('message', response.text)}")
                passed += 1
            else:
                print(f"❌ 应该拒绝但通过了: {response.text}")
        except Exception as e:
            print(f"❌ 测试出错: {str(e)}")
    
    print(f"\n密码修改验证测试结果: {passed}/{total} 通过")
    return passed == total

def test_profile_field_validation(token):
    """测试资料字段验证"""
    print("\n=== 测试资料字段验证 ===")
    
    headers = {
        'Authorization': f'Token {token}',
        'Content-Type': 'application/json'
    }
    
    test_cases = [
        {
            'name': '邮箱格式错误',
            'data': {'email': 'invalid-email'}
        },
        {
            'name': '手机号格式错误',
            'data': {'emergency_phone': '123'}
        }
    ]
    
    passed = 0
    total = len(test_cases)
    
    for test_case in test_cases:
        print(f"\n测试: {test_case['name']}")
        try:
            response = requests.put(UPDATE_PROFILE_URL, 
                                  data=json.dumps(test_case['data']), 
                                  headers=headers)
            if response.status_code == 400:
                print(f"✅ 正确拒绝: {response.json().get('message', response.text)}")
                passed += 1
            else:
                print(f"❌ 应该拒绝但通过了: {response.text}")
        except Exception as e:
            print(f"❌ 测试出错: {str(e)}")
    
    print(f"\n资料字段验证测试结果: {passed}/{total} 通过")
    return passed == total

def main():
    """主测试函数"""
    print_separator("用户信息维护功能测试")
    
    results = {
        'get_profile': False,
        'update_profile': False,
        'change_password': False,
        'password_validation': False,
        'field_validation': False
    }
    
    # 1. 创建测试用户
    username, password = create_test_user()
    if not username:
        print("❌ 无法创建测试用户，测试终止")
        return
    
    # 2. 登录获取token
    token = login_user(username, password)
    if not token:
        print("❌ 无法获取登录token，测试终止")
        return
    
    # 3. 测试获取用户资料
    results['get_profile'] = test_get_profile(token)
    
    # 4. 测试更新用户资料
    results['update_profile'] = test_update_profile(token)
    
    # 5. 测试修改密码
    success, new_password = test_change_password(token, username, password)
    results['change_password'] = success
    
    # 6. 重新获取token（密码已更改）
    if success:
        token = login_user(username, new_password)
        if not token:
            print("❌ 无法使用新密码获取token")
            return
    
    # 7. 测试密码修改验证
    results['password_validation'] = test_change_password_validation(token)
    
    # 8. 测试资料字段验证
    results['field_validation'] = test_profile_field_validation(token)
    
    # 输出测试结果
    print_separator("测试结果汇总")
    print(f"获取用户资料: {'✅ 通过' if results['get_profile'] else '❌ 失败'}")
    print(f"更新用户资料: {'✅ 通过' if results['update_profile'] else '❌ 失败'}")
    print(f"修改密码: {'✅ 通过' if results['change_password'] else '❌ 失败'}")
    print(f"密码修改验证: {'✅ 通过' if results['password_validation'] else '❌ 失败'}")
    print(f"资料字段验证: {'✅ 通过' if results['field_validation'] else '❌ 失败'}")
    
    passed = sum(results.values())
    total = len(results)
    print(f"\n总体结果: {passed}/{total} 测试通过")
    
    if passed == total:
        print("🎉 所有测试都通过了！")
    else:
        print("⚠️ 部分测试失败，需要检查相关功能")

if __name__ == '__main__':
    main()