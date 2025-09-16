#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
调试当前用户的个人资料保存问题
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
from accounts.models import UserProfile

User = get_user_model()

def debug_current_user_profile():
    """调试当前用户的个人资料保存问题"""
    print("=== 调试当前用户个人资料保存问题 ===")
    
    # 1. 获取一个现有用户（模拟前端当前登录用户）
    try:
        # 使用一个真实存在的用户
        test_user = User.objects.filter(username='hhm').first()
        if not test_user:
            print("用户 'hhm' 不存在，使用其他用户")
            test_user = User.objects.filter(user_type='student').first()
            if not test_user:
                print("没有找到合适的测试用户")
                return False
        
        print(f"使用用户: {test_user.username}")
        print(f"当前手机号: {test_user.phone}")
        print(f"当前邮箱: {test_user.email}")
        print(f"当前真实姓名: {test_user.real_name}")
        
        # 2. 重置密码以便登录
        test_user.set_password("testpass123")
        test_user.save()
        
        # 3. 获取登录Token
        login_data = {
            "username": test_user.username,
            "password": "testpass123"
        }
        
        login_response = requests.post(
            "http://localhost:8000/accounts/api/login/",
            json=login_data,
            headers={"Content-Type": "application/json"}
        )
        
        if login_response.status_code != 200:
            print(f"登录失败: {login_response.text}")
            return False
        
        token = login_response.json().get('token')
        print(f"获取Token成功: {token[:20]}...")
        
        # 4. 获取当前资料（模拟前端loadProfile）
        headers = {
            "Authorization": f"Token {token}",
            "Content-Type": "application/json"
        }
        
        profile_response = requests.get(
            "http://localhost:8000/accounts/api/profile/",
            headers=headers
        )
        
        if profile_response.status_code == 200:
            current_profile = profile_response.json()
            print(f"\n当前资料API返回: {json.dumps(current_profile, indent=2, ensure_ascii=False)}")
            
            # 提取用户和资料数据
            user_data = current_profile.get('user', {})
            profile_data = current_profile.get('profile', {})
            
            # 5. 模拟前端的保存操作（使用当前数据）
            print("\n=== 测试1: 使用当前数据保存（应该成功） ===")
            update_data_current = {
                "real_name": user_data.get('real_name', ''),
                "phone": user_data.get('phone', ''),
                "email": user_data.get('email', ''),
                "gender": user_data.get('gender', 'unknown'),
                "address": user_data.get('address', ''),
                "emergency_contact": user_data.get('emergency_contact', ''),
                "emergency_phone": user_data.get('emergency_phone', ''),
                "skills": profile_data.get('skills', ''),
                "experience_years": profile_data.get('experience_years', 0),
                "bio": profile_data.get('bio', '')
            }
            
            print(f"发送数据: {json.dumps(update_data_current, indent=2, ensure_ascii=False)}")
            
            update_response = requests.put(
                "http://localhost:8000/accounts/api/profile/update/",
                json=update_data_current,
                headers=headers
            )
            
            print(f"响应状态码: {update_response.status_code}")
            if update_response.status_code == 200:
                print(f"✅ 成功: {update_response.json().get('message')}")
            else:
                print(f"❌ 失败: {update_response.text}")
            
            # 6. 测试修改手机号的情况
            print("\n=== 测试2: 修改手机号为已存在的号码（应该失败） ===")
            update_data_duplicate = update_data_current.copy()
            update_data_duplicate['phone'] = '13900139001'  # admin01的手机号
            
            print(f"发送数据: {json.dumps(update_data_duplicate, indent=2, ensure_ascii=False)}")
            
            update_response2 = requests.put(
                "http://localhost:8000/accounts/api/profile/update/",
                json=update_data_duplicate,
                headers=headers
            )
            
            print(f"响应状态码: {update_response2.status_code}")
            if update_response2.status_code == 200:
                print(f"✅ 成功: {update_response2.json().get('message')}")
            else:
                print(f"❌ 失败: {update_response2.text}")
            
            # 7. 测试空字段的情况
            print("\n=== 测试3: 真实姓名为空（应该失败） ===")
            update_data_empty = update_data_current.copy()
            update_data_empty['real_name'] = ''
            
            print(f"发送数据: {json.dumps(update_data_empty, indent=2, ensure_ascii=False)}")
            
            update_response3 = requests.put(
                "http://localhost:8000/accounts/api/profile/update/",
                json=update_data_empty,
                headers=headers
            )
            
            print(f"响应状态码: {update_response3.status_code}")
            if update_response3.status_code == 200:
                print(f"✅ 成功: {update_response3.json().get('message')}")
            else:
                print(f"❌ 失败: {update_response3.text}")
            
            # 8. 测试无效手机号格式
            print("\n=== 测试4: 无效手机号格式（应该失败） ===")
            update_data_invalid_phone = update_data_current.copy()
            update_data_invalid_phone['phone'] = '123456789'
            
            print(f"发送数据: {json.dumps(update_data_invalid_phone, indent=2, ensure_ascii=False)}")
            
            update_response4 = requests.put(
                "http://localhost:8000/accounts/api/profile/update/",
                json=update_data_invalid_phone,
                headers=headers
            )
            
            print(f"响应状态码: {update_response4.status_code}")
            if update_response4.status_code == 200:
                print(f"✅ 成功: {update_response4.json().get('message')}")
            else:
                print(f"❌ 失败: {update_response4.text}")
                
        else:
            print(f"获取资料失败: {profile_response.text}")
            return False
        
        return True
        
    except Exception as e:
        print(f"调试过程中发生错误: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    debug_current_user_profile()