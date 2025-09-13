#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
调试球台API问题的脚本
"""

import os
import sys
import django
import requests
from datetime import datetime, timedelta
import json

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'keshe.settings')
django.setup()

from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from campus.models import Campus
from reservations.models import Table, Booking

User = get_user_model()

def get_or_create_test_token():
    """获取或创建测试用户的token"""
    try:
        # 尝试获取现有的测试用户
        user = User.objects.filter(username='test_student').first()
        if not user:
            # 创建测试用户
            user = User.objects.create_user(
                username='test_student',
                email='test@example.com',
                password='testpass123',
                user_type='student',
                real_name='测试学员'
            )
            print(f"创建测试用户: {user.username}")
        
        # 获取或创建token
        token, created = Token.objects.get_or_create(user=user)
        if created:
            print(f"创建新token: {token.key}")
        else:
            print(f"使用现有token: {token.key}")
        
        return token.key
    except Exception as e:
        print(f"获取token失败: {e}")
        return None

def test_campus_api(token):
    """测试校区API"""
    print("\n=== 测试校区API ===")
    
    # 1. 测试数据库中的校区数据
    campuses_db = Campus.objects.all()
    print(f"数据库中的校区数量: {campuses_db.count()}")
    for campus in campuses_db:
        print(f"  - {campus.name} (ID: {campus.id})")
    
    # 2. 测试API响应
    headers = {
        'Authorization': f'Token {token}',
        'Content-Type': 'application/json'
    }
    
    try:
        response = requests.get('http://127.0.0.1:8000/api/campus/api/list/', headers=headers)
        print(f"\nAPI响应状态码: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"API响应数据结构: {type(data)}")
            print(f"API响应内容: {json.dumps(data, ensure_ascii=False, indent=2)}")
            
            # 检查数据结构
            if isinstance(data, dict) and 'data' in data:
                campuses = data['data']
                print(f"\n校区列表长度: {len(campuses)}")
                if campuses:
                    print(f"第一个校区数据: {json.dumps(campuses[0], ensure_ascii=False, indent=2)}")
            elif isinstance(data, list):
                print(f"\n校区列表长度: {len(data)}")
                if data:
                    print(f"第一个校区数据: {json.dumps(data[0], ensure_ascii=False, indent=2)}")
        else:
            print(f"API请求失败: {response.text}")
            
    except Exception as e:
        print(f"API请求异常: {e}")
    
    return campuses_db.first() if campuses_db.exists() else None

def test_table_api(token, campus):
    """测试球台API"""
    print("\n=== 测试球台API ===")
    
    if not campus:
        print("没有可用的校区，跳过球台测试")
        return
    
    # 1. 测试数据库中的球台数据
    tables_db = Table.objects.filter(campus=campus)
    print(f"校区 '{campus.name}' 中的球台数量: {tables_db.count()}")
    for table in tables_db:
        print(f"  - {table.number}号台 (ID: {table.id}, 状态: {table.status})")
    
    # 2. 测试API响应
    headers = {
        'Authorization': f'Token {token}',
        'Content-Type': 'application/json'
    }
    
    # 设置测试时间（明天10:00-12:00）
    tomorrow = datetime.now() + timedelta(days=1)
    start_time = tomorrow.replace(hour=10, minute=0, second=0, microsecond=0)
    end_time = tomorrow.replace(hour=12, minute=0, second=0, microsecond=0)
    
    # 测试不同的时间格式
    time_formats = [
        start_time.strftime('%Y-%m-%d %H:%M:%S'),  # 前端使用的格式
        start_time.strftime('%Y-%m-%dT%H:%M:%S'),  # ISO格式
        start_time.isoformat(),  # Python ISO格式
    ]
    
    for i, start_str in enumerate(time_formats):
        end_str = end_time.strftime('%Y-%m-%d %H:%M:%S') if i == 0 else (
            end_time.strftime('%Y-%m-%dT%H:%M:%S') if i == 1 else end_time.isoformat()
        )
        
        print(f"\n--- 测试时间格式 {i+1}: {start_str} ---")
        
        params = {
            'campus_id': campus.id,
            'start_time': start_str,
            'end_time': end_str
        }
        
        try:
            response = requests.get(
                'http://127.0.0.1:8000/api/reservations/tables/available/',
                headers=headers,
                params=params
            )
            
            print(f"请求URL: {response.url}")
            print(f"响应状态码: {response.status_code}")
            
            if response.status_code == 200:
                tables = response.json()
                print(f"可用球台数量: {len(tables)}")
                if tables:
                    print(f"第一个球台: {json.dumps(tables[0], ensure_ascii=False, indent=2)}")
                else:
                    print("⚠️  该时间段暂无可用球台")
            else:
                print(f"API请求失败: {response.text}")
                
        except Exception as e:
            print(f"API请求异常: {e}")

def check_existing_bookings(campus):
    """检查现有预约情况"""
    print("\n=== 检查现有预约 ===")
    
    if not campus:
        print("没有可用的校区")
        return
    
    # 查询该校区的所有预约
    bookings = Booking.objects.filter(table__campus=campus).order_by('-start_time')
    print(f"校区 '{campus.name}' 的预约数量: {bookings.count()}")
    
    # 显示最近的几个预约
    recent_bookings = bookings[:5]
    for booking in recent_bookings:
        print(f"  - {booking.start_time} - {booking.end_time}, {booking.table.number}号台, 状态: {booking.status}")
    
    # 检查明天的预约冲突
    tomorrow = datetime.now() + timedelta(days=1)
    start_of_day = tomorrow.replace(hour=0, minute=0, second=0, microsecond=0)
    end_of_day = tomorrow.replace(hour=23, minute=59, second=59, microsecond=999999)
    
    tomorrow_bookings = bookings.filter(
        start_time__gte=start_of_day,
        start_time__lte=end_of_day
    )
    
    print(f"\n明天的预约数量: {tomorrow_bookings.count()}")
    for booking in tomorrow_bookings:
        print(f"  - {booking.start_time.strftime('%H:%M')} - {booking.end_time.strftime('%H:%M')}, {booking.table.number}号台")

def main():
    print("🏓 开始调试球台API问题")
    
    # 1. 获取测试token
    token = get_or_create_test_token()
    if not token:
        print("无法获取有效token，退出")
        return
    
    # 2. 测试校区API
    campus = test_campus_api(token)
    
    # 3. 测试球台API
    test_table_api(token, campus)
    
    # 4. 检查现有预约
    check_existing_bookings(campus)
    
    print("\n🎯 调试完成")
    print("\n💡 建议检查项目:")
    print("1. 前端是否正确传递了校区ID")
    print("2. 时间格式是否匹配后端期望")
    print("3. 是否存在时区问题")
    print("4. 球台状态是否正确设置")
    print("5. 预约冲突检查逻辑是否正确")

if __name__ == '__main__':
    main()