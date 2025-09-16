#!/usr/bin/env python
import os
import sys
import django
import requests
import json

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'keshe.settings')
django.setup()

from accounts.models import User
from rest_framework.authtoken.models import Token

def test_profile_api():
    """测试个人资料API"""
    print("=== 测试个人资料API ===")
    
    # 获取一个测试用户
    user = User.objects.filter(user_type='coach').first()
    if not user:
        print("❌ 没有找到测试用户")
        return
    
    print(f"测试用户: {user.username}")
    print(f"用户头像字段: {user.avatar}")
    
    # 获取或创建token
    token, created = Token.objects.get_or_create(user=user)
    print(f"用户Token: {token.key}")
    
    # 测试API
    headers = {'Authorization': f'Token {token.key}'}
    
    try:
        response = requests.get('http://localhost:8000/accounts/api/profile/', headers=headers)
        print(f"\n响应状态码: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("\n=== API返回数据结构 ===")
            print(json.dumps(data, indent=2, ensure_ascii=False))
            
            # 检查头像字段
            if 'user' in data:
                user_data = data['user']
                print(f"\n用户数据中的头像: {user_data.get('avatar', '未找到avatar字段')}")
            else:
                print(f"\n直接返回的头像: {data.get('avatar', '未找到avatar字段')}")
        else:
            print(f"❌ API请求失败: {response.text}")
            
    except Exception as e:
        print(f"❌ 请求异常: {str(e)}")

if __name__ == '__main__':
    test_profile_api()