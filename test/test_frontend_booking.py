#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
前端预约功能测试脚本
测试前端页面与后端API的集成情况
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

# 只导入必要的模块进行API测试
from django.contrib.auth.models import User

def test_frontend_api_integration():
    """
    测试前端API集成
    """
    print("\n=== 前端预约功能API集成测试 ===")
    
    # 1. 测试用户登录API
    print("\n1. 测试用户登录API")
    login_url = "http://127.0.0.1:8000/api/accounts/login/"
    login_data = {
        "username": "student1",
        "password": "testpass123"
    }
    
    try:
        response = requests.post(login_url, json=login_data)
        print(f"登录请求状态码: {response.status_code}")
        
        if response.status_code == 200:
            login_result = response.json()
            token = login_result.get('token')
            print(f"登录成功，获得token: {token[:20]}...")
            
            # 设置认证头
            headers = {
                'Authorization': f'Token {token}',
                'Content-Type': 'application/json'
            }
            
            # 2. 测试师生关系API
            print("\n2. 测试师生关系API")
            relations_url = "http://127.0.0.1:8000/api/reservations/relations/"
            relations_response = requests.get(relations_url, headers=headers)
            print(f"师生关系请求状态码: {relations_response.status_code}")
            
            if relations_response.status_code == 200:
                relations = relations_response.json()
                print(f"获取到 {len(relations)} 个师生关系")
                if relations:
                    print(f"第一个关系: {relations[0]}")
            
            # 3. 测试校区API
            print("\n3. 测试校区API")
            campuses_url = "http://127.0.0.1:8000/api/reservations/campuses/"
            campuses_response = requests.get(campuses_url, headers=headers)
            print(f"校区请求状态码: {campuses_response.status_code}")
            
            if campuses_response.status_code == 200:
                campuses = campuses_response.json()
                print(f"获取到 {len(campuses)} 个校区")
                if campuses:
                    print(f"第一个校区: {campuses[0]}")
            
            # 4. 测试球台API
            print("\n4. 测试球台API")
            if campuses_response.status_code == 200 and campuses:
                campus_id = campuses[0]['id']
                start_time = (datetime.now() + timedelta(hours=1)).strftime('%Y-%m-%d %H:%M:%S')
                end_time = (datetime.now() + timedelta(hours=2)).strftime('%Y-%m-%d %H:%M:%S')
                
                tables_url = f"http://127.0.0.1:8000/api/reservations/tables/available/"
                tables_params = {
                    'campus_id': campus_id,
                    'start_time': start_time,
                    'end_time': end_time
                }
                
                tables_response = requests.get(tables_url, headers=headers, params=tables_params)
                print(f"球台请求状态码: {tables_response.status_code}")
                
                if tables_response.status_code == 200:
                    tables = tables_response.json()
                    print(f"获取到 {len(tables)} 个可用球台")
                    if tables:
                        print(f"第一个球台: {tables[0]}")
            
            # 5. 测试预约列表API
            print("\n5. 测试预约列表API")
            bookings_url = "http://127.0.0.1:8000/api/reservations/bookings/"
            bookings_response = requests.get(bookings_url, headers=headers)
            print(f"预约列表请求状态码: {bookings_response.status_code}")
            
            if bookings_response.status_code == 200:
                bookings_data = bookings_response.json()
                if isinstance(bookings_data, dict) and 'results' in bookings_data:
                    bookings = bookings_data['results']
                    print(f"获取到 {len(bookings)} 个预约记录")
                else:
                    print(f"预约数据格式: {type(bookings_data)}")
            
            # 6. 测试创建预约API（如果有必要的数据）
            print("\n6. 测试创建预约API")
            if (relations_response.status_code == 200 and relations and 
                campuses_response.status_code == 200 and campuses and
                tables_response.status_code == 200 and tables):
                
                booking_data = {
                    'relation_id': relations[0]['id'],
                    'campus_id': campuses[0]['id'],
                    'table_id': tables[0]['id'],
                    'start_time': start_time,
                    'end_time': end_time,
                    'duration_hours': 1.0,
                    'notes': '前端API测试预约'
                }
                
                create_response = requests.post(bookings_url, headers=headers, json=booking_data)
                print(f"创建预约请求状态码: {create_response.status_code}")
                
                if create_response.status_code == 201:
                    booking_result = create_response.json()
                    print(f"预约创建成功: ID {booking_result.get('id')}")
                else:
                    print(f"创建预约失败: {create_response.text}")
            else:
                print("缺少必要数据，跳过创建预约测试")
                
        else:
            print(f"登录失败: {response.text}")
            
    except Exception as e:
        print(f"API测试出错: {e}")

def test_frontend_urls():
    """
    测试前端URL访问
    """
    print("\n=== 前端URL访问测试 ===")
    
    frontend_urls = [
        "http://localhost:3002/",
        "http://localhost:3002/login",
        "http://localhost:3002/reservations",
        "http://localhost:3002/courses"
    ]
    
    for url in frontend_urls:
        try:
            response = requests.get(url, timeout=5)
            print(f"{url}: {response.status_code}")
        except Exception as e:
            print(f"{url}: 连接失败 - {e}")

if __name__ == '__main__':
    print("开始前端预约功能测试...")
    
    # 测试API集成
    test_frontend_api_integration()
    
    # 测试前端URL
    test_frontend_urls()
    
    print("\n=== 测试完成 ===")
    print("\n建议：")
    print("1. 在浏览器中访问 http://localhost:3002/login 进行登录")
    print("2. 登录后访问 http://localhost:3002/reservations 测试预约功能")
    print("3. 尝试创建新预约，检查表单验证和API调用")
    print("4. 检查预约列表的显示和操作功能")