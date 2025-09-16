#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试球台API调用
模拟前端调用，检查为什么显示暂无可用球台
"""

import os
import sys
import django
import requests
import json
from datetime import datetime, timedelta

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'keshe.settings')
django.setup()

from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from reservations.models import Table, Campus, Booking
from django.utils import timezone

User = get_user_model()

def test_table_api():
    """测试球台API"""
    print("=== 球台API测试 ===")
    
    # 1. 检查数据库中的球台数据
    print("\n1. 检查数据库球台数据：")
    total_tables = Table.objects.count()
    available_tables = Table.objects.filter(is_active=True, status='available').count()
    print(f"总球台数量: {total_tables}")
    print(f"可用球台数量: {available_tables}")
    
    for table in Table.objects.all():
        print(f"  - {table.campus.name} {table.number}号台: {table.get_status_display()}, 启用:{table.is_active}")
    
    # 2. 检查校区数据
    print("\n2. 检查校区数据：")
    campuses = Campus.objects.all()
    for campus in campuses:
        table_count = Table.objects.filter(campus=campus).count()
        print(f"  - {campus.name} (ID: {campus.id}): {table_count}个球台")
    
    # 3. 获取测试用户token
    print("\n3. 获取测试用户token：")
    try:
        # 尝试获取一个测试用户
        test_user = User.objects.filter(is_active=True).first()
        if not test_user:
            print("没有找到可用的测试用户")
            return
        
        token, created = Token.objects.get_or_create(user=test_user)
        print(f"用户: {test_user.username}, Token: {token.key[:10]}...")
        
    except Exception as e:
        print(f"获取token失败: {e}")
        return
    
    # 4. 测试API调用
    print("\n4. 测试API调用：")
    base_url = "http://127.0.0.1:8000"
    
    # 设置测试时间（明天10:00-12:00）
    tomorrow = datetime.now() + timedelta(days=1)
    start_time = tomorrow.replace(hour=10, minute=0, second=0, microsecond=0)
    end_time = tomorrow.replace(hour=12, minute=0, second=0, microsecond=0)
    
    print(f"查询时间段: {start_time} - {end_time}")
    
    # 测试不同的时间格式
    time_formats = [
        (start_time.isoformat(), end_time.isoformat(), "ISO格式"),
        (start_time.strftime('%Y-%m-%dT%H:%M:%S'), end_time.strftime('%Y-%m-%dT%H:%M:%S'), "标准格式"),
        (start_time.strftime('%Y-%m-%d %H:%M:%S'), end_time.strftime('%Y-%m-%d %H:%M:%S'), "空格格式")
    ]
    
    headers = {
        'Authorization': f'Token {token.key}',
        'Content-Type': 'application/json'
    }
    
    for start_str, end_str, format_name in time_formats:
        print(f"\n测试 {format_name}:")
        print(f"  开始时间: {start_str}")
        print(f"  结束时间: {end_str}")
        
        # 测试不同校区
        for campus in campuses:
            params = {
                'start_time': start_str,
                'end_time': end_str,
                'campus_id': campus.id
            }
            
            try:
                response = requests.get(
                    f"{base_url}/api/reservations/tables/available/",
                    params=params,
                    headers=headers,
                    timeout=10
                )
                
                print(f"  校区 {campus.name} (ID:{campus.id}): 状态码 {response.status_code}")
                
                if response.status_code == 200:
                    data = response.json()
                    print(f"    返回 {len(data)} 个可用球台")
                    for table in data:
                        print(f"      - {table.get('name', table.get('number'))}")
                else:
                    print(f"    错误: {response.text}")
                    
            except Exception as e:
                print(f"    请求失败: {e}")
    
    # 5. 检查是否有冲突的预约
    print("\n5. 检查预约冲突：")
    conflicting_bookings = Booking.objects.filter(
        start_time__lt=end_time,
        end_time__gt=start_time,
        status__in=['pending', 'confirmed']
    )
    
    print(f"冲突预约数量: {conflicting_bookings.count()}")
    for booking in conflicting_bookings:
        print(f"  - {booking.table.campus.name} {booking.table.number}号台: {booking.start_time} - {booking.end_time} ({booking.status})")

if __name__ == '__main__':
    test_table_api()