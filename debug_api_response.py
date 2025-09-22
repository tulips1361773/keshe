#!/usr/bin/env python
"""
调试脚本：检查API响应的详细结构
"""
import os
import sys
import django
import requests
import json

# 设置Django环境
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'keshe.settings')
django.setup()

from django.contrib.auth import get_user_model
from accounts.serializers import UserSerializer

User = get_user_model()

def debug_api_response():
    """调试API响应结构"""
    print("=== 调试API响应结构 ===")
    
    # 1. 直接测试序列化器
    print("\n1. 直接测试序列化器:")
    try:
        user = User.objects.get(id=4)
        serializer = UserSerializer(user)
        serialized_data = serializer.data
        
        print(f"  序列化器返回的数据:")
        print(f"  用户ID: {serialized_data.get('id')}")
        print(f"  用户名: {serialized_data.get('username')}")
        print(f"  头像字段: {serialized_data.get('avatar')}")
        print(f"  头像字段类型: {type(serialized_data.get('avatar'))}")
        
        # 检查原始头像字段
        print(f"\n  原始用户对象:")
        print(f"  user.avatar: {user.avatar}")
        print(f"  user.avatar.name: {user.avatar.name if user.avatar else 'None'}")
        print(f"  user.avatar.url: {user.avatar.url if user.avatar else 'None'}")
        
    except User.DoesNotExist:
        print("  用户ID 4不存在")
        return
    except Exception as e:
        print(f"  序列化器测试异常: {e}")
    
    # 2. 测试完整API响应
    print("\n2. 测试完整API响应:")
    try:
        session = requests.Session()
        
        # 获取CSRF token
        csrf_response = session.get('http://127.0.0.1:8000/api/accounts/csrf-token/')
        if csrf_response.status_code == 200:
            csrf_token = csrf_response.json().get('csrfToken')
            session.headers.update({'X-CSRFToken': csrf_token})
        
        # 登录
        login_data = {'username': 'hhm', 'password': '123456'}
        login_response = session.post('http://127.0.0.1:8000/api/accounts/login/', json=login_data)
        
        if login_response.status_code == 200:
            # 获取用户资料
            profile_response = session.get('http://127.0.0.1:8000/api/accounts/profile/')
            if profile_response.status_code == 200:
                response_data = profile_response.json()
                print(f"  API响应结构:")
                print(f"  success: {response_data.get('success')}")
                
                user_data = response_data.get('user', {})
                print(f"  user.id: {user_data.get('id')}")
                print(f"  user.username: {user_data.get('username')}")
                print(f"  user.avatar: {user_data.get('avatar')}")
                print(f"  user.avatar类型: {type(user_data.get('avatar'))}")
                
                profile_data = response_data.get('profile', {})
                print(f"  profile.id: {profile_data.get('id')}")
                
                # 打印完整响应
                print(f"\n  完整API响应:")
                print(json.dumps(response_data, indent=2, ensure_ascii=False))
            else:
                print(f"  API调用失败: {profile_response.status_code}")
                print(f"  错误信息: {profile_response.text}")
        else:
            print(f"  登录失败: {login_response.status_code}")
            
    except Exception as e:
        print(f"  API测试异常: {e}")

if __name__ == '__main__':
    debug_api_response()