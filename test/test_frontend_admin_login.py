#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import django
import requests
import json

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'keshe.settings')
django.setup()

def test_frontend_admin_login():
    """测试前端管理员登录"""
    print("=== 测试前端管理员登录 ===")
    
    # API登录地址
    login_url = 'http://127.0.0.1:8000/api/accounts/login/'
    
    # 登录数据
    login_data = {
        'username': 'admin',
        'password': 'testpass123'
    }
    
    try:
        print(f"🔗 请求URL: {login_url}")
        print(f"📝 登录数据: {login_data}")
        
        # 发送登录请求
        response = requests.post(
            login_url,
            data=json.dumps(login_data),
            headers={'Content-Type': 'application/json'}
        )
        
        print(f"📊 响应状态码: {response.status_code}")
        
        if response.status_code == 200:
            response_data = response.json()
            print(f"📋 响应数据: {json.dumps(response_data, indent=2, ensure_ascii=False)}")
            
            if response_data.get('success'):
                print("✅ 管理员前端登录成功")
                print(f"🎫 Token: {response_data.get('token', 'N/A')[:50]}...")
                print(f"👤 用户信息: {response_data.get('user', {})}")
                
                # 测试获取用户资料
                token = response_data.get('token')
                if token:
                    profile_url = 'http://127.0.0.1:8000/api/accounts/profile/'
                    profile_response = requests.get(
                        profile_url,
                        headers={'Authorization': f'Token {token}'}
                    )
                    
                    print(f"\n📋 用户资料请求状态: {profile_response.status_code}")
                    if profile_response.status_code == 200:
                        profile_data = profile_response.json()
                        print(f"✅ 用户资料获取成功: {json.dumps(profile_data, indent=2, ensure_ascii=False)}")
                    else:
                        print(f"❌ 用户资料获取失败: {profile_response.text}")
                        
            else:
                print(f"❌ 登录失败: {response_data.get('message', '未知错误')}")
        else:
            print(f"❌ 请求失败: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ 连接失败: 请确保Django服务器正在运行 (python manage.py runserver)")
    except Exception as e:
        print(f"❌ 测试过程中出错: {str(e)}")
    
    print("\n💡 使用说明:")
    print("1. 确保Django服务器运行: python manage.py runserver")
    print("2. 前端登录地址: http://localhost:3002/login")
    print("3. 管理员账户: admin / testpass123")
    print("4. 后台管理: http://127.0.0.1:8000/admin/")

if __name__ == '__main__':
    test_frontend_admin_login()