#!/usr/bin/env python
"""
预约API测试脚本
"""

import os
import sys
import django
from django.test import Client
from django.contrib.auth import authenticate
from django.urls import reverse
import json
from datetime import datetime, timedelta
from django.utils import timezone

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'keshe.settings')
django.setup()

from accounts.models import User
from campus.models import Campus
from reservations.models import Table, CoachStudentRelation, Booking
from rest_framework.authtoken.models import Token

def test_booking_api():
    """测试预约API功能"""
    print("=== 预约API测试开始 ===")
    
    # 创建测试客户端
    client = Client()
    
    # 获取测试用户
    try:
        coach = User.objects.get(username='coach1')
        student = User.objects.get(username='huanghm')
        print(f"✓ 获取测试用户成功: 教练={coach.real_name}, 学员={student.username}")
    except User.DoesNotExist:
        print("✗ 测试用户不存在")
        return False
    
    # 获取或创建Token
    coach_token, created = Token.objects.get_or_create(user=coach)
    student_token, created = Token.objects.get_or_create(user=student)
    
    print(f"✓ 获取认证Token: 教练Token={coach_token.key[:10]}..., 学员Token={student_token.key[:10]}...")
    
    # 测试1: 获取球台列表
    print("\n--- 测试1: 获取球台列表 ---")
    response = client.get(
        '/api/reservations/tables/',
        HTTP_AUTHORIZATION=f'Token {coach_token.key}'
    )
    print(f"状态码: {response.status_code}")
    if response.status_code == 200:
        tables = response.json()
        print(f"✓ 获取到 {len(tables['results']) if 'results' in tables else len(tables)} 个球台")
        if tables.get('results'):
            print(f"  第一个球台: {tables['results'][0]['name']}")
    else:
        print(f"✗ 获取球台列表失败: {response.content.decode()}")
    
    # 测试2: 获取师生关系列表
    print("\n--- 测试2: 获取师生关系列表 ---")
    response = client.get(
        '/api/reservations/relations/',
        HTTP_AUTHORIZATION=f'Token {coach_token.key}'
    )
    print(f"状态码: {response.status_code}")
    if response.status_code == 200:
        relations = response.json()
        print(f"✓ 获取到 {len(relations['results']) if 'results' in relations else len(relations)} 个师生关系")
    else:
        print(f"✗ 获取师生关系列表失败: {response.content.decode()}")
    
    # 测试3: 获取预约列表
    print("\n--- 测试3: 获取预约列表 ---")
    response = client.get(
        '/api/reservations/bookings/',
        HTTP_AUTHORIZATION=f'Token {coach_token.key}'
    )
    print(f"状态码: {response.status_code}")
    if response.status_code == 200:
        bookings = response.json()
        print(f"✓ 获取到 {len(bookings['results']) if 'results' in bookings else len(bookings)} 个预约")
        if bookings.get('results'):
            booking = bookings['results'][0]
            print(f"  第一个预约: ID={booking['id']}, 状态={booking['status']}")
    else:
        print(f"✗ 获取预约列表失败: {response.content.decode()}")
    
    # 测试4: 创建新预约
    print("\n--- 测试4: 创建新预约 ---")
    try:
        # 获取师生关系和球台
        relation = CoachStudentRelation.objects.filter(coach=coach, student=student, status='approved').first()
        table = Table.objects.filter(is_active=True).first()
        
        if not relation:
            print("✗ 没有找到已审核的师生关系")
            return False
        
        if not table:
            print("✗ 没有找到可用的球台")
            return False
        
        # 创建预约数据
        start_time = timezone.now() + timedelta(hours=2)
        end_time = start_time + timedelta(hours=1)
        
        booking_data = {
            'relation_id': relation.id,
            'table_id': table.id,
            'start_time': start_time.isoformat(),
            'end_time': end_time.isoformat(),
            'duration_hours': 1.0,
            'total_fee': 50.00,
            'notes': 'API测试预约'
        }
        
        response = client.post(
            '/api/reservations/bookings/',
            data=json.dumps(booking_data),
            content_type='application/json',
            HTTP_AUTHORIZATION=f'Token {coach_token.key}'
        )
        
        print(f"状态码: {response.status_code}")
        if response.status_code == 201:
            new_booking = response.json()
            print(f"✓ 创建预约成功: ID={new_booking['id']}")
            
            # 测试5: 确认预约
            print("\n--- 测试5: 确认预约 ---")
            response = client.post(
                f'/api/reservations/bookings/{new_booking["id"]}/confirm/',
                HTTP_AUTHORIZATION=f'Token {coach_token.key}'
            )
            print(f"状态码: {response.status_code}")
            if response.status_code == 200:
                print("✓ 预约确认成功")
            else:
                print(f"✗ 预约确认失败: {response.content.decode()}")
            
        else:
            print(f"✗ 创建预约失败: {response.content.decode()}")
            
    except Exception as e:
        print(f"✗ 创建预约时发生错误: {e}")
    
    print("\n=== 预约API测试完成 ===")
    return True

if __name__ == '__main__':
    test_booking_api()