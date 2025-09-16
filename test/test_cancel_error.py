#!/usr/bin/env python
"""
测试取消预约错误的脚本
"""

import os
import django
import requests
import json
from datetime import datetime, timedelta

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'keshe.settings')
django.setup()

from accounts.models import User
from rest_framework.authtoken.models import Token
from reservations.models import Booking, CoachStudentRelation
from django.db.models import Q

def test_cancel_booking():
    """测试取消预约功能"""
    print("=== 测试取消预约功能 ===")
    
    # 获取用户和token
    user = User.objects.get(username='hhm')
    token, created = Token.objects.get_or_create(user=user)
    
    headers = {
        'Authorization': f'Token {token.key}',
        'Content-Type': 'application/json'
    }
    
    # 1. 测试获取取消统计
    print("\n1. 测试获取取消统计API")
    try:
        response = requests.get('http://127.0.0.1:8000/api/reservations/bookings/cancel_stats/', headers=headers)
        print(f"状态码: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"取消统计: {json.dumps(data, indent=2, ensure_ascii=False)}")
        else:
            print(f"错误: {response.text}")
    except Exception as e:
        print(f"请求错误: {e}")
    
    # 2. 获取用户的预约
    print("\n2. 获取用户预约")
    relations = CoachStudentRelation.objects.filter(
        Q(coach=user) | Q(student=user),
        status='approved'
    )
    
    bookings = Booking.objects.filter(
        relation__in=relations,
        status='confirmed'
    )[:5]  # 只取前5个
    
    print(f"找到 {bookings.count()} 个确认状态的预约")
    
    for booking in bookings:
        print(f"预约ID: {booking.id}, 状态: {booking.status}, 开始时间: {booking.start_time}")
        
        # 3. 测试取消预约
        print(f"\n3. 测试取消预约 ID: {booking.id}")
        cancel_url = f'http://127.0.0.1:8000/api/reservations/bookings/{booking.id}/cancel/'
        cancel_data = {'reason': '测试取消原因'}
        
        try:
            response = requests.post(cancel_url, headers=headers, json=cancel_data)
            print(f"状态码: {response.status_code}")
            print(f"响应: {response.text}")
            
            if response.status_code == 400:
                print("✓ 正确返回月取消次数限制错误")
                break
            elif response.status_code == 200:
                print("✓ 取消成功")
                break
        except Exception as e:
            print(f"请求错误: {e}")
        
        print("-" * 50)

if __name__ == '__main__':
    test_cancel_booking()