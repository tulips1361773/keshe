#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
调试教练选择失败的问题
"""

import os
import sys
import django
import requests
import json
from datetime import datetime

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'keshe.settings')
django.setup()

from accounts.models import User
from reservations.models import CoachStudentRelation

def debug_coach_selection():
    print("=== 调试教练选择失败问题 ===")
    
    # 1. 获取测试用户
    try:
        student = User.objects.filter(user_type='student').first()
        coach = User.objects.filter(user_type='coach').first()
        
        if not student:
            print("❌ 没有找到学员用户")
            return
        if not coach:
            print("❌ 没有找到教练用户")
            return
            
        print(f"✅ 找到学员: {student.username} (ID: {student.id})")
        print(f"✅ 找到教练: {coach.username} (ID: {coach.id})")
        
    except Exception as e:
        print(f"❌ 获取用户失败: {e}")
        return
    
    # 2. 检查现有师生关系
    existing_relations = CoachStudentRelation.objects.filter(
        coach=coach, student=student
    )
    print(f"\n现有师生关系数量: {existing_relations.count()}")
    for relation in existing_relations:
        print(f"  - 状态: {relation.status}, 申请方: {relation.applied_by}")
    
    # 3. 模拟学员登录获取token
    login_url = 'http://localhost:8000/api/accounts/login/'
    login_data = {
        'username': student.username,
        'password': 'testpass123'  # 假设密码
    }
    
    try:
        login_response = requests.post(login_url, json=login_data)
        print(f"\n登录响应状态: {login_response.status_code}")
        
        if login_response.status_code == 200:
            token_data = login_response.json()
            print(f"登录响应数据: {token_data}")
            token = token_data.get('access') or token_data.get('token')
            if token:
                print(f"✅ 获取到token: {token[:20]}...")
            else:
                print(f"❌ 响应中没有找到token: {token_data}")
                return
        else:
            print(f"❌ 登录失败: {login_response.text}")
            return
            
    except Exception as e:
        print(f"❌ 登录请求失败: {e}")
        return
    
    # 4. 测试师生关系创建API
    relations_url = 'http://localhost:8000/api/reservations/relations/'
    headers = {
        'Authorization': f'Token {token}',
        'Content-Type': 'application/json'
    }
    
    # 测试不同的请求数据格式
    test_cases = [
        {
            'name': '使用coach_id',
            'data': {
                'coach_id': coach.id,
                'notes': f'学员选择教练：{coach.real_name}'
            }
        },
        {
            'name': '使用coach_id (user_id)',
            'data': {
                'coach_id': coach.user_id if hasattr(coach, 'user_id') else coach.id,
                'notes': f'学员选择教练：{coach.real_name}'
            }
        },
        {
            'name': '使用student_id和coach_id',
            'data': {
                'student_id': student.id,
                'coach_id': coach.id,
                'notes': f'学员选择教练：{coach.real_name}'
            }
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n=== 测试 {i}: {test_case['name']} ===")
        print(f"请求数据: {json.dumps(test_case['data'], indent=2, ensure_ascii=False)}")
        
        try:
            response = requests.post(relations_url, json=test_case['data'], headers=headers)
            print(f"响应状态: {response.status_code}")
            print(f"响应内容: {response.text}")
            
            if response.status_code in [200, 201]:
                print("✅ 请求成功")
                break
            else:
                print("❌ 请求失败")
                
        except Exception as e:
            print(f"❌ 请求异常: {e}")
    
    # 5. 检查API端点是否存在
    print("\n=== 检查API端点 ===")
    try:
        options_response = requests.options(relations_url, headers=headers)
        print(f"OPTIONS响应状态: {options_response.status_code}")
        print(f"允许的方法: {options_response.headers.get('Allow', 'N/A')}")
    except Exception as e:
        print(f"❌ OPTIONS请求失败: {e}")
    
    # 6. 检查数据库约束
    print("\n=== 检查数据库约束 ===")
    try:
        # 尝试直接创建师生关系
        relation = CoachStudentRelation(
            coach=coach,
            student=student,
            applied_by='student',
            notes='测试创建'
        )
        relation.full_clean()  # 验证模型
        print("✅ 模型验证通过")
        
        # 不实际保存，只是验证
        print("模型字段:")
        print(f"  - coach: {relation.coach}")
        print(f"  - student: {relation.student}")
        print(f"  - applied_by: {relation.applied_by}")
        print(f"  - status: {relation.status}")
        
    except Exception as e:
        print(f"❌ 模型验证失败: {e}")

if __name__ == '__main__':
    debug_coach_selection()