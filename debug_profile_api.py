#!/usr/bin/env python
import os
import sys
import django
import requests
import json

# 设置Django环境
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'keshe.settings')
django.setup()

from accounts.models import User, UserProfile
from accounts.serializers import UserSerializer, UserProfileSerializer

def debug_profile_api():
    """调试Profile API响应"""
    print("=== 调试Profile API响应 ===")
    
    # 1. 直接测试序列化器
    print("\n1. 直接测试序列化器:")
    try:
        user = User.objects.get(id=4)
        profile, created = UserProfile.objects.get_or_create(user=user)
        
        user_serializer = UserSerializer(user)
        profile_serializer = UserProfileSerializer(profile)
        
        user_data = user_serializer.data
        profile_data = profile_serializer.data
        
        print(f"  用户序列化数据:")
        print(f"    ID: {user_data.get('id')}")
        print(f"    用户名: {user_data.get('username')}")
        print(f"    头像: {user_data.get('avatar')}")
        
        print(f"  资料序列化数据:")
        print(f"    ID: {profile_data.get('id')}")
        print(f"    用户ID: {profile_data.get('user')}")
        
        # 模拟API响应结构
        api_response = {
            'success': True,
            'user': user_data,
            'profile': profile_data
        }
        
        print(f"\n  模拟API响应:")
        print(f"    success: {api_response.get('success')}")
        print(f"    user.avatar: {api_response.get('user', {}).get('avatar')}")
        
    except Exception as e:
        print(f"  序列化器测试异常: {e}")
        import traceback
        traceback.print_exc()
    
    # 2. 测试实际API调用
    print("\n2. 测试实际API调用:")
    try:
        session = requests.Session()
        
        # 获取CSRF token
        csrf_response = session.get('http://127.0.0.1:8000/api/accounts/csrf-token/')
        if csrf_response.status_code == 200:
            csrf_token = csrf_response.json().get('csrfToken')
            session.headers.update({'X-CSRFToken': csrf_token})
            print(f"  CSRF Token获取成功")
        
        # 登录
        login_data = {'username': 'hhm', 'password': '123456'}
        login_response = session.post('http://127.0.0.1:8000/api/accounts/login/', json=login_data)
        if login_response.status_code == 200:
            print("  登录成功")
        else:
            print(f"  登录失败: {login_response.status_code}")
            return
        
        # 获取用户资料
        profile_response = session.get('http://127.0.0.1:8000/api/accounts/profile/')
        if profile_response.status_code == 200:
            profile_data = profile_response.json()
            print(f"  Profile API调用成功")
            print(f"  完整响应: {json.dumps(profile_data, indent=2, ensure_ascii=False)}")
            
            user_data = profile_data.get('user', {})
            print(f"\n  用户数据检查:")
            print(f"    用户ID: {user_data.get('id')}")
            print(f"    用户名: {user_data.get('username')}")
            print(f"    头像字段: {user_data.get('avatar')}")
            print(f"    头像字段类型: {type(user_data.get('avatar'))}")
            
        else:
            print(f"  Profile API调用失败: {profile_response.status_code}")
            print(f"  响应内容: {profile_response.text}")
            
    except Exception as e:
        print(f"  API测试异常: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    debug_profile_api()