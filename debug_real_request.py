#!/usr/bin/env python
import os
import sys
import django
import requests
import json

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'keshe.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
django.setup()

from accounts.models import User
from reservations.models import CoachStudentRelation
from django.contrib.auth import authenticate
from django.test import Client

def test_real_api_request():
    print("=== 模拟真实前端API请求 ===")
    
    # 使用Django测试客户端
    client = Client()
    
    # 1. 先登录获取session
    print("\n1. 尝试登录...")
    login_data = {
        'username': 'hhm',
        'password': '123456'
    }
    
    login_response = client.post('/api/accounts/login/', 
                                json.dumps(login_data), 
                                content_type='application/json')
    
    print(f"登录响应状态: {login_response.status_code}")
    if login_response.status_code == 200:
        print("✅ 登录成功")
        login_result = json.loads(login_response.content)
        print(f"用户信息: {login_result}")
    else:
        print(f"❌ 登录失败: {login_response.content}")
        return
    
    # 2. 检查用户和教练数据
    print("\n2. 检查数据库中的用户和教练...")
    try:
        student = User.objects.get(username='hhm')
        coach = User.objects.get(id=113)
        print(f"学员: {student.username} (ID: {student.id})")
        print(f"教练: {coach.username} (ID: {coach.id})")
        
        # 检查现有关系
        existing_relations = CoachStudentRelation.objects.filter(
            coach_id=coach.id, student_id=student.id
        )
        print(f"现有关系数量: {existing_relations.count()}")
        for relation in existing_relations:
            print(f"- 关系ID: {relation.id}, 状态: {relation.status}")
            
    except User.DoesNotExist as e:
        print(f"❌ 用户不存在: {e}")
        return
    
    # 3. 发送选择教练请求
    print("\n3. 发送选择教练请求...")
    request_data = {
        'coach_id': coach.id,  # 使用教练的实际ID
        'student_id': student.id,  # 使用学员的实际ID
        'notes': '测试选择教练'
    }
    
    print(f"请求数据: {request_data}")
    
    response = client.post('/api/reservations/relations/', 
                          json.dumps(request_data), 
                          content_type='application/json')
    
    print(f"响应状态码: {response.status_code}")
    print(f"响应内容: {response.content.decode('utf-8')}")
    
    if response.status_code == 201:
        print("✅ 选择教练成功!")
        result = json.loads(response.content)
        print(f"创建的关系: {result}")
    else:
        print(f"❌ 选择教练失败")
        try:
            error_data = json.loads(response.content)
            print(f"错误详情: {error_data}")
        except:
            print(f"原始错误内容: {response.content}")

if __name__ == "__main__":
    test_real_api_request()