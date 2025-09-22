#!/usr/bin/env python
"""
调试脚本：检查教练列表API的响应数据结构
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
from accounts.models import Coach

User = get_user_model()

def debug_coach_api_response():
    """调试教练列表API响应"""
    print("=== 调试教练列表API响应数据结构 ===")
    
    # 1. 检查数据库中的教练数据
    print("\n1. 数据库中的教练数据:")
    coaches = Coach.objects.filter(status='approved').select_related('user')[:3]
    for coach in coaches:
        print(f"  Coach ID: {coach.id}, User ID: {coach.user.id}, Name: {coach.user.real_name}")
    
    # 2. 模拟API请求
    print("\n2. 模拟API请求:")
    try:
        # 先登录获取session
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
            print(f"  CSRF Token获取成功: {csrf_token[:20]}...")
        
        # 登录
        login_response = session.post('http://127.0.0.1:8000/api/accounts/login/', json=login_data)
        if login_response.status_code == 200:
            print("  登录成功")
        else:
            print(f"  登录失败: {login_response.status_code}")
            return
        
        # 获取教练列表
        coaches_response = session.get('http://127.0.0.1:8000/api/accounts/coaches/')
        if coaches_response.status_code == 200:
            data = coaches_response.json()
            print(f"  教练列表API调用成功")
            print(f"  总数: {data.get('count', 0)}")
            
            # 检查返回的教练数据结构
            if data.get('results'):
                print("\n3. API返回的教练数据结构:")
                first_coach = data['results'][0]
                print(f"  第一个教练的数据字段:")
                for key, value in first_coach.items():
                    if key == 'user_info':
                        print(f"    {key}: {type(value)} (包含用户详细信息)")
                        if isinstance(value, dict):
                            print(f"      user_info.id: {value.get('id')}")
                            print(f"      user_info.real_name: {value.get('real_name')}")
                    else:
                        print(f"    {key}: {value} ({type(value).__name__})")
                
                print(f"\n  关键字段对比:")
                print(f"    coach.id (Coach模型ID): {first_coach.get('id')}")
                print(f"    coach.user (User模型ID): {first_coach.get('user')}")
                print(f"    coach.user_info.id (用户详细信息中的ID): {first_coach.get('user_info', {}).get('id')}")
                
        else:
            print(f"  教练列表API调用失败: {coaches_response.status_code}")
            print(f"  响应内容: {coaches_response.text}")
            
    except Exception as e:
        print(f"  API请求异常: {e}")

if __name__ == '__main__':
    debug_coach_api_response()