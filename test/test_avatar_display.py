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

def test_avatar_display():
    """测试头像显示"""
    print("=== 测试头像显示 ===")
    
    # 查找有头像的用户
    users_with_avatar = User.objects.exclude(avatar__isnull=True).exclude(avatar='')
    
    print(f"找到 {users_with_avatar.count()} 个有头像的用户")
    
    for user in users_with_avatar[:3]:  # 只测试前3个
        print(f"\n用户: {user.username}")
        print(f"头像路径: {user.avatar}")
        
        # 获取或创建token
        token, created = Token.objects.get_or_create(user=user)
        
        # 测试API
        headers = {'Authorization': f'Token {token.key}'}
        
        try:
            response = requests.get('http://localhost:8000/accounts/api/profile/', headers=headers)
            if response.status_code == 200:
                data = response.json()
                avatar_url = data.get('user', {}).get('avatar')
                print(f"API返回的头像URL: {avatar_url}")
                
                # 检查头像文件是否存在
                if avatar_url:
                    # 构建完整的头像URL
                    full_avatar_url = f"http://localhost:8000{avatar_url}"
                    print(f"完整头像URL: {full_avatar_url}")
                    
                    # 测试头像是否可访问
                    try:
                        avatar_response = requests.get(full_avatar_url)
                        print(f"头像访问状态: {avatar_response.status_code}")
                        if avatar_response.status_code == 200:
                            print(f"✅ 头像可正常访问")
                        else:
                            print(f"❌ 头像访问失败")
                    except Exception as e:
                        print(f"❌ 头像访问异常: {str(e)}")
                else:
                    print("❌ API未返回头像URL")
            else:
                print(f"❌ API请求失败: {response.status_code}")
                
        except Exception as e:
            print(f"❌ 请求异常: {str(e)}")
    
    if users_with_avatar.count() == 0:
        print("\n没有找到有头像的用户，创建一个测试用户...")
        # 这里可以创建一个测试用户并上传头像
        
if __name__ == '__main__':
    test_avatar_display()