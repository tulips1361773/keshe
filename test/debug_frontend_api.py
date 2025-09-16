#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
调试前端API调用
检查教练登录后API返回的数据格式
"""

import os
import sys
import django
import requests
import json

# 设置Django环境
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'keshe.settings')
django.setup()

from accounts.models import User, Coach
from notifications.models import Notification

def debug_frontend_api():
    """调试前端API"""
    print("=== 调试前端API调用 ===")
    
    # 1. 获取教练信息
    try:
        coach_obj = Coach.objects.first()
        if not coach_obj:
            print("❌ 未找到教练用户")
            return
            
        coach_user = coach_obj.user
        print(f"✓ 教练: {coach_user.username} (ID: {coach_user.id})")
        
    except Exception as e:
        print(f"❌ 获取教练信息失败: {e}")
        return
    
    # 2. 教练登录获取Token
    print("\n=== 教练登录获取Token ===")
    login_url = 'http://127.0.0.1:8000/api/accounts/login/'
    login_data = {
        'username': coach_user.username,
        'password': 'testpass123'
    }
    
    try:
        response = requests.post(login_url, json=login_data)
        if response.status_code == 200:
            login_result = response.json()
            token = login_result.get('token')
            print(f"✓ 登录成功，Token: {token[:20]}...")
        else:
            print(f"❌ 登录失败: {response.text}")
            return
    except Exception as e:
        print(f"❌ 登录请求失败: {e}")
        return
    
    # 3. 调用通知列表API
    print("\n=== 调用通知列表API ===")
    headers = {'Authorization': f'Token {token}'}
    
    notifications_url = 'http://127.0.0.1:8000/api/notifications/list/'
    try:
        response = requests.get(notifications_url, headers=headers)
        print(f"API状态码: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✓ 响应数据结构:")
            print(f"  - count: {data.get('count')}")
            print(f"  - results数量: {len(data.get('results', []))}")
            
            results = data.get('results', [])
            if results:
                print("\n✓ 通知详细数据:")
                for i, notification in enumerate(results, 1):
                    print(f"  通知{i}:")
                    print(f"    - id: {notification.get('id')}")
                    print(f"    - title: {notification.get('title')}")
                    print(f"    - message: {notification.get('message')}")
                    print(f"    - message_type: {notification.get('message_type')}")
                    print(f"    - is_read: {notification.get('is_read')}")
                    print(f"    - created_at: {notification.get('created_at')}")
                    print(f"    - data: {notification.get('data')}")
                    print()
            else:
                print("⚠️ results为空")
                
            # 完整响应数据
            print("\n=== 完整API响应 ===")
            print(json.dumps(data, indent=2, ensure_ascii=False))
            
        else:
            print(f"❌ API调用失败: {response.text}")
            
    except Exception as e:
        print(f"❌ API请求失败: {e}")
    
    # 4. 调用统计API
    print("\n=== 调用统计API ===")
    stats_url = 'http://127.0.0.1:8000/api/notifications/stats/'
    try:
        response = requests.get(stats_url, headers=headers)
        print(f"统计API状态码: {response.status_code}")
        
        if response.status_code == 200:
            stats = response.json()
            print("✓ 统计数据:")
            print(json.dumps(stats, indent=2, ensure_ascii=False))
        else:
            print(f"❌ 统计API失败: {response.text}")
            
    except Exception as e:
        print(f"❌ 统计API请求失败: {e}")
    
    # 5. 检查数据库中的通知
    print("\n=== 检查数据库通知 ===")
    notifications = Notification.objects.filter(recipient=coach_user).order_by('-created_at')
    print(f"数据库中教练通知数量: {notifications.count()}")
    
    for i, notification in enumerate(notifications, 1):
        print(f"通知{i}:")
        print(f"  - ID: {notification.id}")
        print(f"  - 标题: {notification.title}")
        print(f"  - 内容: {notification.message}")
        print(f"  - 类型: {notification.message_type}")
        print(f"  - 已读: {notification.is_read}")
        print(f"  - 创建时间: {notification.created_at}")
        print(f"  - 数据: {notification.data}")
        print()
    
    # 6. 模拟前端请求
    print("\n=== 模拟前端请求 ===")
    
    # 模拟前端的axios请求
    frontend_headers = {
        'Authorization': f'Token {token}',
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    
    # 带参数的请求
    params = {
        'page': 1,
        'page_size': 10
    }
    
    try:
        response = requests.get(notifications_url, headers=frontend_headers, params=params)
        print(f"前端模拟请求状态码: {response.status_code}")
        print(f"请求URL: {response.url}")
        print(f"请求头: {dict(response.request.headers)}")
        
        if response.status_code == 200:
            data = response.json()
            print("✓ 前端模拟请求成功")
            print(f"返回通知数量: {len(data.get('results', []))}")
        else:
            print(f"❌ 前端模拟请求失败: {response.text}")
            
    except Exception as e:
        print(f"❌ 前端模拟请求异常: {e}")

if __name__ == '__main__':
    debug_frontend_api()