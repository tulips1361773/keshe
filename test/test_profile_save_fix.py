#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试个人资料保存功能修复
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

def test_profile_save():
    """测试个人资料保存功能"""
    print("=== 测试个人资料保存功能 ===")
    
    # 1. 获取或创建测试用户
    test_username = f"profile_test_{datetime.now().strftime('%Y%m%d_%H%M%S%f')[:-3]}"
    test_user = User.objects.create_user(
        username=test_username,
        email=f"{test_username}@test.com",
        password="testpass123",
        user_type="student",
        real_name="测试用户",
        phone="13800138000"
    )
    print(f"创建测试用户: {test_user.username}")
    
    # 2. 获取登录Token
    login_data = {
        "username": test_username,
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
    
    # 3. 测试保存个人资料
    headers = {
        "Authorization": f"Token {token}",
        "Content-Type": "application/json"
    }
    
    update_data = {
        "real_name": "更新后的姓名",
        "phone": "13900139000",
        "email": f"updated_{test_username}@test.com",
        "gender": "male",
        "address": "测试地址123号",
        "emergency_contact": "紧急联系人",
        "emergency_phone": "13700137000",
        "skills": "Python, Django, Vue.js",
        "experience_years": 3,
        "bio": "这是一个测试用户的个人简介"
    }
    
    print("\n发送更新请求...")
    update_response = requests.put(
        "http://localhost:8000/accounts/api/profile/update/",
        json=update_data,
        headers=headers
    )
    
    print(f"更新响应状态码: {update_response.status_code}")
    
    if update_response.status_code == 200:
        response_data = update_response.json()
        print("✅ 个人资料保存成功!")
        print(f"响应消息: {response_data.get('message')}")
        
        # 验证数据是否正确保存
        updated_user = User.objects.get(id=test_user.id)
        print(f"\n验证保存的数据:")
        print(f"姓名: {updated_user.real_name}")
        print(f"手机: {updated_user.phone}")
        print(f"邮箱: {updated_user.email}")
        print(f"性别: {updated_user.gender}")
        print(f"地址: {updated_user.address}")
        
        # 检查扩展资料
        try:
            profile = UserProfile.objects.get(user=updated_user)
            print(f"技能: {profile.skills}")
            print(f"经验年数: {profile.experience_years}")
            print(f"个人简介: {profile.bio}")
        except UserProfile.DoesNotExist:
            print("⚠️ 扩展资料未找到")
        
        return True
    else:
        print(f"❌ 个人资料保存失败!")
        print(f"错误信息: {update_response.text}")
        return False
    
    # 4. 清理测试数据
    try:
        test_user.delete()
        print(f"\n清理测试用户: {test_username}")
    except:
        pass

if __name__ == "__main__":
    success = test_profile_save()
    if success:
        print("\n🎉 个人资料保存功能测试通过!")
    else:
        print("\n💥 个人资料保存功能测试失败!")
        sys.exit(1)