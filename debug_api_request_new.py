#!/usr/bin/env python
"""
调试前端API请求问题的脚本
模拟前端发送的完整请求
"""
import os
import django
import json
import requests
from django.test import Client
from django.contrib.auth import authenticate

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'keshe.settings')
django.setup()

from django.contrib.auth import get_user_model
from reservations.models import CoachStudentRelation

User = get_user_model()

def test_api_request():
    """测试API请求"""
    print("=== 调试前端API请求 ===")
    
    # 1. 检查用户状态
    try:
        student = User.objects.get(username='hhm')
        coach = User.objects.get(id=113)
        print(f"学员: {student.username} (ID: {student.id}, 类型: {student.user_type})")
        print(f"教练: {coach.username} (ID: {coach.id}, 类型: {coach.user_type})")
    except User.DoesNotExist as e:
        print(f"用户不存在: {e}")
        return
    
    # 2. 检查现有关系
    existing_relations = CoachStudentRelation.objects.filter(
        coach=coach, student=student
    )
    print(f"现有关系数量: {existing_relations.count()}")
    for rel in existing_relations:
        print(f"  - 关系ID: {rel.id}, 状态: {rel.status}")
    
    # 3. 使用Django测试客户端模拟请求
    client = Client()
    
    # 登录
    login_success = client.login(username='hhm', password='123456')
    print(f"登录状态: {login_success}")
    
    if not login_success:
        print("登录失败，无法继续测试")
        return
    
    # 4. 发送选择教练请求
    request_data = {
        'coach_id': coach.id,
        'student_id': student.id,
        'notes': '测试选择教练'
    }
    
    print(f"发送请求数据: {request_data}")
    
    response = client.post(
        '/api/reservations/relations/',
        data=json.dumps(request_data),
        content_type='application/json'
    )
    
    print(f"响应状态码: {response.status_code}")
    print(f"响应内容: {response.content.decode('utf-8')}")
    
    # 5. 如果创建成功，清理测试数据
    if response.status_code == 201:
        response_data = json.loads(response.content)
        relation_id = response_data.get('id')
        if relation_id:
            try:
                test_relation = CoachStudentRelation.objects.get(id=relation_id)
                test_relation.delete()
                print(f"已删除测试关系 ID: {relation_id}")
            except CoachStudentRelation.DoesNotExist:
                print("测试关系已不存在")

def test_with_requests():
    """使用requests库测试API"""
    print("\n=== 使用requests库测试 ===")
    
    # 1. 获取CSRF token
    session = requests.Session()
    csrf_response = session.get('http://localhost:8000/api/accounts/csrf-token/')
    
    if csrf_response.status_code == 200:
        csrf_token = csrf_response.json().get('csrfToken')
        print(f"CSRF Token: {csrf_token[:20]}...")
    else:
        print("获取CSRF token失败")
        return
    
    # 2. 登录
    login_data = {
        'username': 'hhm',
        'password': '123456'
    }
    
    headers = {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrf_token,
        'Referer': 'http://localhost:8000/'
    }
    
    login_response = session.post(
        'http://localhost:8000/api/accounts/login/',
        json=login_data,
        headers=headers
    )
    
    print(f"登录响应状态码: {login_response.status_code}")
    print(f"登录响应内容: {login_response.text}")
    
    if login_response.status_code != 200:
        print("登录失败，无法继续测试")
        return
    
    # 3. 发送选择教练请求
    request_data = {
        'coach_id': 113,
        'student_id': 4,
        'notes': '使用requests测试选择教练'
    }
    
    relation_response = session.post(
        'http://localhost:8000/api/reservations/relations/',
        json=request_data,
        headers=headers
    )
    
    print(f"选择教练响应状态码: {relation_response.status_code}")
    print(f"选择教练响应内容: {relation_response.text}")

if __name__ == '__main__':
    test_api_request()
    test_with_requests()