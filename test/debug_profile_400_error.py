#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
调试个人资料保存400错误
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

def debug_profile_update_error():
    """调试个人资料更新400错误"""
    print("=== 调试个人资料保存400错误 ===")
    
    # 1. 使用现有用户进行测试
    try:
        # 尝试获取一个现有用户
        test_user = User.objects.filter(user_type='student').first()
        if not test_user:
            # 如果没有学生用户，创建一个
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S%f')[:-3]
            test_user = User.objects.create_user(
                username=f"debug_user_{timestamp}",
                email=f"debug_{timestamp}@test.com",
                password="testpass123",
                user_type="student",
                real_name="调试用户",
                phone=f"138{timestamp[-8:]}"
            )
            print(f"创建调试用户: {test_user.username}")
        else:
            print(f"使用现有用户: {test_user.username}")
        
        # 2. 获取登录Token
        login_data = {
            "username": test_user.username,
            "password": "testpass123"
        }
        
        # 如果是现有用户，可能密码不是testpass123，我们重置一下
        test_user.set_password("testpass123")
        test_user.save()
        
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
        
        # 3. 获取当前资料
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
            print(f"当前资料: {json.dumps(current_profile, indent=2, ensure_ascii=False)}")
        else:
            print(f"获取资料失败: {profile_response.text}")
            return False
        
        # 4. 测试各种更新数据组合，找出导致400错误的原因
        test_cases = [
            {
                "name": "最小数据集",
                "data": {
                    "real_name": "测试姓名"
                }
            },
            {
                "name": "包含手机号",
                "data": {
                    "real_name": "测试姓名",
                    "phone": "13900139000"
                }
            },
            {
                "name": "包含邮箱",
                "data": {
                    "real_name": "测试姓名",
                    "email": "test@example.com"
                }
            },
            {
                "name": "完整数据（模拟前端）",
                "data": {
                    "real_name": "完整测试姓名",
                    "phone": "13900139001",
                    "email": "complete@example.com",
                    "gender": "male",
                    "address": "测试地址",
                    "emergency_contact": "紧急联系人",
                    "emergency_phone": "13700137000",
                    "skills": "测试技能",
                    "experience_years": 5,
                    "bio": "测试简介"
                }
            },
            {
                "name": "包含无效字段",
                "data": {
                    "real_name": "测试姓名",
                    "invalid_field": "无效数据"
                }
            },
            {
                "name": "空字符串测试",
                "data": {
                    "real_name": "",
                    "phone": "",
                    "email": ""
                }
            },
            {
                "name": "无效手机号",
                "data": {
                    "real_name": "测试姓名",
                    "phone": "123456789"
                }
            },
            {
                "name": "无效邮箱",
                "data": {
                    "real_name": "测试姓名",
                    "email": "invalid-email"
                }
            }
        ]
        
        for i, test_case in enumerate(test_cases, 1):
            print(f"\n--- 测试用例 {i}: {test_case['name']} ---")
            print(f"发送数据: {json.dumps(test_case['data'], indent=2, ensure_ascii=False)}")
            
            update_response = requests.put(
                "http://localhost:8000/accounts/api/profile/update/",
                json=test_case['data'],
                headers=headers
            )
            
            print(f"响应状态码: {update_response.status_code}")
            
            if update_response.status_code == 200:
                response_data = update_response.json()
                print(f"✅ 成功: {response_data.get('message')}")
            else:
                print(f"❌ 失败: {update_response.text}")
                try:
                    error_data = update_response.json()
                    print(f"详细错误: {json.dumps(error_data, indent=2, ensure_ascii=False)}")
                except:
                    pass
        
        return True
        
    except Exception as e:
        print(f"调试过程中发生错误: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    debug_profile_update_error()