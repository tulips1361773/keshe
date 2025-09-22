#!/usr/bin/env python
"""
调试脚本：检查头像上传和显示问题
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
from django.conf import settings

User = get_user_model()

def debug_avatar_issue():
    """调试头像问题"""
    print("=== 调试头像上传和显示问题 ===")
    
    # 1. 检查用户ID为4的头像数据
    print("\n1. 检查用户头像数据:")
    try:
        user = User.objects.get(id=4)
        print(f"  用户ID: {user.id}")
        print(f"  用户名: {user.username}")
        print(f"  真实姓名: {user.real_name}")
        print(f"  头像字段: {user.avatar}")
        print(f"  头像类型: {type(user.avatar)}")
        
        # 检查头像文件是否存在
        if user.avatar:
            avatar_path = os.path.join(settings.MEDIA_ROOT, str(user.avatar))
            print(f"  头像文件路径: {avatar_path}")
            print(f"  文件是否存在: {os.path.exists(avatar_path)}")
            if os.path.exists(avatar_path):
                print(f"  文件大小: {os.path.getsize(avatar_path)} bytes")
        
    except User.DoesNotExist:
        print("  用户ID 4不存在")
        return
    
    # 2. 测试API返回的用户数据
    print("\n2. 测试API返回的用户数据:")
    try:
        # 先登录
        login_data = {
            'username': 'hhm',
            'password': '123456'
        }
        
        session = requests.Session()
        
        # 获取CSRF token
        csrf_response = session.get('http://127.0.0.1:8000/api/accounts/csrf-token/')
        if csrf_response.status_code == 200:
            csrf_token = csrf_response.json().get('csrfToken')
            session.headers.update({'X-CSRFToken': csrf_token})
            print(f"  CSRF Token获取成功")
        
        # 登录
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
            print(f"  用户资料API调用成功")
            print(f"  返回的头像字段: {profile_data.get('avatar')}")
            print(f"  头像字段类型: {type(profile_data.get('avatar'))}")
            
            # 检查头像URL格式
            avatar_url = profile_data.get('avatar')
            if avatar_url:
                print(f"  头像URL: {avatar_url}")
                if avatar_url.startswith('/media/'):
                    full_url = f"http://127.0.0.1:8000{avatar_url}"
                    print(f"  完整头像URL: {full_url}")
                    
                    # 测试头像文件访问
                    try:
                        avatar_response = session.get(full_url)
                        print(f"  头像文件访问状态: {avatar_response.status_code}")
                        if avatar_response.status_code == 200:
                            print(f"  头像文件大小: {len(avatar_response.content)} bytes")
                            print(f"  Content-Type: {avatar_response.headers.get('Content-Type')}")
                        else:
                            print(f"  头像文件访问失败: {avatar_response.text}")
                    except Exception as e:
                        print(f"  头像文件访问异常: {e}")
            else:
                print("  用户没有设置头像")
        else:
            print(f"  用户资料API调用失败: {profile_response.status_code}")
            
    except Exception as e:
        print(f"  API测试异常: {e}")
    
    # 3. 检查媒体文件配置
    print("\n3. 检查媒体文件配置:")
    print(f"  MEDIA_URL: {settings.MEDIA_URL}")
    print(f"  MEDIA_ROOT: {settings.MEDIA_ROOT}")
    print(f"  DEBUG模式: {settings.DEBUG}")
    
    # 4. 检查头像目录
    print("\n4. 检查头像目录:")
    avatars_dir = os.path.join(settings.MEDIA_ROOT, 'avatars')
    print(f"  头像目录: {avatars_dir}")
    print(f"  目录是否存在: {os.path.exists(avatars_dir)}")
    
    if os.path.exists(avatars_dir):
        files = os.listdir(avatars_dir)
        print(f"  目录中的文件数量: {len(files)}")
        for file in files:
            if 'avatar_4_' in file:
                file_path = os.path.join(avatars_dir, file)
                print(f"    用户4的头像文件: {file} (大小: {os.path.getsize(file_path)} bytes)")

if __name__ == '__main__':
    debug_avatar_issue()