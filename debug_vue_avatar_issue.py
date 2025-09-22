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

def debug_vue_avatar_issue():
    """调试Vue应用头像显示问题"""
    print("=== 调试Vue应用头像显示问题 ===")
    
    # 1. 检查用户数据
    try:
        user = User.objects.get(username='hhm')
        print(f"✅ 用户存在: {user.username} (ID: {user.id})")
        print(f"   头像字段: {user.avatar}")
        print(f"   头像类型: {type(user.avatar)}")
        
        # 检查头像文件是否存在
        if user.avatar:
            from django.conf import settings
            import os
            
            # 获取头像文件的相对路径
            avatar_name = str(user.avatar)  # 转换为字符串
            print(f"   头像文件名: {avatar_name}")
            
            # 构建完整文件路径
            full_path = os.path.join(settings.MEDIA_ROOT, avatar_name)
            print(f"   文件路径: {full_path}")
            print(f"   文件存在: {os.path.exists(full_path)}")
            
            if os.path.exists(full_path):
                file_size = os.path.getsize(full_path)
                print(f"   文件大小: {file_size} bytes")
                
            # 获取头像的URL
            avatar_url = user.avatar.url
            print(f"   头像URL: {avatar_url}")
            
    except User.DoesNotExist:
        print("❌ 用户不存在")
        return False
    
    # 2. 测试完整的Vue应用认证流程
    session = requests.Session()
    
    # 2.1 获取CSRF token
    print("\n=== 测试Vue应用认证流程 ===")
    csrf_response = session.get('http://localhost:8000/api/accounts/csrf-token/')
    if csrf_response.status_code != 200:
        print(f"❌ 获取CSRF token失败: {csrf_response.status_code}")
        return False
    
    csrf_token = csrf_response.json().get('csrfToken')
    print(f"✅ CSRF Token: {csrf_token[:20]}...")
    
    # 2.2 登录
    login_data = {
        'username': 'hhm',
        'password': '123456'
    }
    
    headers = {
        'X-CSRFToken': csrf_token,
        'Content-Type': 'application/json'
    }
    
    login_response = session.post(
        'http://localhost:8000/api/accounts/login/',
        json=login_data,
        headers=headers
    )
    
    if login_response.status_code != 200:
        print(f"❌ 登录失败: {login_response.status_code}")
        print(f"   响应: {login_response.text}")
        return False
    
    login_result = login_response.json()
    user_info = login_result.get('user', {})
    token = login_result.get('token')
    
    print(f"✅ 登录成功")
    print(f"   Token: {token[:20] if token else 'None'}...")
    print(f"   用户头像: {user_info.get('avatar')}")
    
    # 2.3 使用Token测试Profile API
    print("\n=== 测试Profile API (使用Token认证) ===")
    profile_headers = {
        'Authorization': f'Token {token}',
        'Content-Type': 'application/json'
    }
    
    profile_response = session.get(
        'http://localhost:8000/api/accounts/profile/',
        headers=profile_headers
    )
    
    print(f"Profile API状态码: {profile_response.status_code}")
    if profile_response.status_code == 200:
        profile_data = profile_response.json()
        print(f"✅ Profile API成功")
        print(f"   用户头像: {profile_data.get('user', {}).get('avatar')}")
        
        # 测试头像URL访问
        avatar_path = profile_data.get('user', {}).get('avatar')
        if avatar_path:
            print(f"\n=== 测试头像URL访问 ===")
            
            # 测试相对路径拼接
            if avatar_path.startswith('/media/'):
                avatar_url = f"http://localhost:8000{avatar_path}"
            else:
                avatar_url = f"http://localhost:8000/media/{avatar_path}"
            
            print(f"头像URL: {avatar_url}")
            
            # 测试直接访问头像URL
            avatar_response = requests.get(avatar_url)
            print(f"头像访问状态码: {avatar_response.status_code}")
            
            if avatar_response.status_code == 200:
                print(f"✅ 头像文件可以正常访问")
                print(f"   Content-Type: {avatar_response.headers.get('Content-Type')}")
                print(f"   Content-Length: {avatar_response.headers.get('Content-Length')}")
            else:
                print(f"❌ 头像文件访问失败")
                print(f"   响应内容: {avatar_response.text[:200]}")
        else:
            print("❌ Profile API响应中没有头像字段")
    else:
        print(f"❌ Profile API失败: {profile_response.text}")
    
    # 3. 检查CORS设置
    print(f"\n=== 检查CORS设置 ===")
    from django.conf import settings
    print(f"CORS_ALLOWED_ORIGINS: {settings.CORS_ALLOWED_ORIGINS}")
    print(f"CORS_ALLOW_CREDENTIALS: {settings.CORS_ALLOW_CREDENTIALS}")
    
    # 4. 模拟前端getAvatarUrl函数
    print(f"\n=== 模拟前端getAvatarUrl函数 ===")
    avatar_path = user_info.get('avatar', '')
    print(f"输入参数: {avatar_path}")
    
    if not avatar_path:
        print("头像为空，返回空字符串")
        final_url = ''
    elif avatar_path.startswith('http'):
        print("头像是完整URL，直接返回")
        final_url = avatar_path
    else:
        print("头像是相对路径，拼接完整URL")
        final_url = f"http://localhost:8000{avatar_path}"
    
    print(f"最终URL: {final_url}")
    
    return True

if __name__ == '__main__':
    debug_vue_avatar_issue()