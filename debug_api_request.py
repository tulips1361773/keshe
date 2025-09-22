#!/usr/bin/env python
import os
import django
import requests
import json

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'keshe.settings')
django.setup()

from accounts.models import User
from django.contrib.auth import authenticate
from django.contrib.sessions.models import Session
from django.test import Client

print("=== 模拟前端API请求 ===")

# 创建测试客户端
client = Client()

# 模拟登录获取session
print("1. 模拟用户登录...")
login_data = {
    'username': 'hhm',
    'password': 'hhm123456'
}

login_response = client.post('/api/accounts/login/', login_data, content_type='application/json')
print(f"登录响应状态: {login_response.status_code}")
print(f"登录响应内容: {login_response.content.decode()}")

if login_response.status_code == 200:
    print("✓ 登录成功")
    
    # 模拟选择教练请求
    print("\n2. 模拟选择教练请求...")
    coach_data = {
        'coach_id': 113,
        'student_id': 4,
        'notes': '测试选择教练'
    }
    
    # 使用相同的client发送请求（保持session）
    response = client.post('/api/reservations/relations/', 
                          json.dumps(coach_data), 
                          content_type='application/json')
    
    print(f"选择教练响应状态: {response.status_code}")
    print(f"选择教练响应内容: {response.content.decode()}")
    
    if response.status_code == 400:
        print("✗ 请求失败，分析错误...")
        try:
            error_data = json.loads(response.content.decode())
            print(f"错误详情: {error_data}")
        except:
            print(f"无法解析错误响应: {response.content.decode()}")
    elif response.status_code in [200, 201]:
        print("✓ 选择教练成功")
    else:
        print(f"✗ 未预期的响应状态: {response.status_code}")
        
else:
    print("✗ 登录失败，无法继续测试")

print("\n3. 直接检查数据库状态...")
try:
    coach = User.objects.get(id=113, user_type='coach')
    student = User.objects.get(id=4, user_type='student')
    print(f"✓ 教练存在: {coach.username}")
    print(f"✓ 学员存在: {student.username}")
except User.DoesNotExist as e:
    print(f"✗ 用户不存在: {e}")

# 检查现有关系
from reservations.models import CoachStudentRelation
existing = CoachStudentRelation.objects.filter(coach_id=113, student_id=4).first()
if existing:
    print(f"现有关系状态: {existing.status}")
else:
    print("无现有关系")