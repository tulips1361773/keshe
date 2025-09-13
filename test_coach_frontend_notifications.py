#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试教练前端通知显示问题
检查教练登录后是否能在前端看到通知
"""

import os
import sys
import django
import requests
import json
from django.conf import settings

# 添加项目路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'keshe.settings')
django.setup()

from accounts.models import User, Coach
from notifications.models import Notification

def test_coach_frontend_notifications():
    """测试教练前端通知显示"""
    print("=== 教练前端通知显示测试 ===")
    
    # 1. 找到教练用户
    try:
        coach_obj = Coach.objects.first()
        if not coach_obj:
            print("❌ 未找到教练用户")
            return False
            
        coach_user = coach_obj.user
        print(f"✓ 找到教练: {coach_user.username} (ID: {coach_user.id})")
        
    except Exception as e:
        print(f"❌ 查找教练失败: {e}")
        return False
    
    # 2. 检查教练的通知数据
    print("\n=== 检查教练通知数据 ===")
    notifications = Notification.objects.filter(recipient=coach_user).order_by('-created_at')
    print(f"教练通知总数: {notifications.count()}")
    
    if notifications.exists():
        for i, notification in enumerate(notifications[:3], 1):
            print(f"{i}. [{notification.message_type}] {notification.title}")
            print(f"   内容: {notification.message}")
            print(f"   已读: {'是' if notification.is_read else '否'}")
            print(f"   数据: {notification.data}")
            print()
    else:
        print("❌ 教练没有任何通知")
        return False
    
    # 3. 测试教练登录API
    print("\n=== 测试教练登录API ===")
    login_url = 'http://127.0.0.1:8000/api/accounts/login/'
    login_data = {
        'username': coach_user.username,
        'password': 'testpass123'  # 假设密码
    }
    
    try:
        response = requests.post(login_url, json=login_data)
        print(f"登录API状态码: {response.status_code}")
        
        if response.status_code == 200:
            login_result = response.json()
            token = login_result.get('token')
            user_info = login_result.get('user', {})
            
            print(f"✓ 登录成功，Token: {token[:20]}...")
            print(f"✓ 用户类型: {user_info.get('user_type')}")
            print(f"✓ 用户ID: {user_info.get('id')}")
            
        else:
            print(f"❌ 登录失败: {response.text}")
            # 尝试使用其他可能的密码
            for password in ['123456', 'password', 'admin123']:
                login_data['password'] = password
                response = requests.post(login_url, json=login_data)
                if response.status_code == 200:
                    login_result = response.json()
                    token = login_result.get('token')
                    print(f"✓ 使用密码 '{password}' 登录成功，Token: {token[:20]}...")
                    break
            else:
                print("❌ 尝试多个密码都登录失败")
                return False
                
    except Exception as e:
        print(f"❌ 登录请求失败: {e}")
        return False
    
    # 4. 测试通知API
    print("\n=== 测试通知API ===")
    headers = {'Authorization': f'Token {token}'}
    
    # 测试通知列表API
    notifications_url = 'http://127.0.0.1:8000/api/notifications/list/'
    try:
        response = requests.get(notifications_url, headers=headers)
        print(f"通知列表API状态码: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            results = data.get('results', [])
            print(f"✓ API返回通知数量: {len(results)}")
            print(f"✓ 总数: {data.get('count', 0)}")
            
            for i, notification in enumerate(results[:3], 1):
                print(f"{i}. [{notification.get('message_type')}] {notification.get('title')}")
                print(f"   内容: {notification.get('message')}")
                print(f"   已读: {'是' if notification.get('is_read') else '否'}")
                print()
        else:
            print(f"❌ 通知API失败: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ 通知API请求失败: {e}")
        return False
    
    # 5. 测试统计API
    print("\n=== 测试统计API ===")
    stats_url = 'http://127.0.0.1:8000/api/notifications/stats/'
    try:
        response = requests.get(stats_url, headers=headers)
        print(f"统计API状态码: {response.status_code}")
        
        if response.status_code == 200:
            stats = response.json()
            print(f"✓ 总通知数: {stats.get('total', 0)}")
            print(f"✓ 未读通知数: {stats.get('unread', 0)}")
            print(f"✓ 系统通知数: {stats.get('system', 0)}")
            print(f"✓ 预约通知数: {stats.get('booking', 0)}")
        else:
            print(f"❌ 统计API失败: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ 统计API请求失败: {e}")
        return False
    
    # 6. 测试未读数量API
    print("\n=== 测试未读数量API ===")
    unread_url = 'http://127.0.0.1:8000/api/notifications/unread-count/'
    try:
        response = requests.get(unread_url, headers=headers)
        print(f"未读数量API状态码: {response.status_code}")
        
        if response.status_code == 200:
            unread_data = response.json()
            print(f"✓ 未读数量: {unread_data.get('count', 0)}")
        else:
            print(f"❌ 未读数量API失败: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ 未读数量API请求失败: {e}")
        return False
    
    print("\n=== 前端调试建议 ===")
    print("1. 检查前端是否正确保存了Token")
    print("2. 检查前端API请求是否包含正确的Authorization头")
    print("3. 检查前端是否在页面加载时调用了通知API")
    print("4. 检查浏览器控制台是否有JavaScript错误")
    print("5. 检查网络面板中的API请求和响应")
    
    print(f"\n=== 测试Token信息 ===")
    print(f"Token: {token}")
    print(f"教练用户名: {coach_user.username}")
    print(f"教练ID: {coach_user.id}")
    
    return True

if __name__ == '__main__':
    test_coach_frontend_notifications()