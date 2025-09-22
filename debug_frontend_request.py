#!/usr/bin/env python
import os
import sys
import django
import requests
import json

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'keshe.settings')
django.setup()

from accounts.models import User
from reservations.models import CoachStudentRelation

def check_user_login_status():
    """检查用户登录状态和session"""
    print("=== 检查用户登录状态 ===")
    
    # 模拟前端的完整登录流程
    session = requests.Session()
    
    # 1. 获取CSRF token
    csrf_response = session.get('http://localhost:8000/api/accounts/csrf-token/')
    if csrf_response.status_code != 200:
        print(f"❌ 获取CSRF token失败: {csrf_response.status_code}")
        return None
    
    csrf_token = csrf_response.json().get('csrfToken')
    print(f"✅ CSRF Token: {csrf_token[:20]}...")
    
    # 2. 登录
    login_data = {
        'username': 'hhm',
        'password': '123456'
    }
    
    headers = {
        'X-CSRFToken': csrf_token,
        'Content-Type': 'application/json'
    }
    
    login_response = session.post(
        'http://localhost:8000/api/accounts/login/',
        json=login_data,
        headers=headers
    )
    
    if login_response.status_code != 200:
        print(f"❌ 登录失败: {login_response.status_code}")
        print(f"   响应: {login_response.text}")
        return None
    
    login_result = login_response.json()
    user_info = login_result.get('user', {})
    print(f"✅ 登录成功")
    print(f"   用户ID: {user_info.get('id')}")
    print(f"   用户名: {user_info.get('username')}")
    print(f"   用户类型: {user_info.get('user_type')}")
    
    # 3. 检查cookies和session
    cookies = session.cookies.get_dict()
    print(f"   Cookies: {list(cookies.keys())}")
    
    return session, user_info

def test_different_request_formats(session, user_info):
    """测试不同的请求数据格式"""
    print("\n=== 测试不同请求格式 ===")
    
    # 更新CSRF token
    cookies = session.cookies.get_dict()
    csrf_token = cookies.get('csrftoken')
    
    headers = {
        'X-CSRFToken': csrf_token,
        'Content-Type': 'application/json'
    }
    
    # 测试用例1: 正常格式
    test_cases = [
        {
            'name': '正常格式',
            'data': {
                'coach_id': 113,
                'student_id': user_info.get('id'),
                'notes': '学员选择教练：测试'
            }
        },
        {
            'name': '字符串ID格式',
            'data': {
                'coach_id': '113',
                'student_id': str(user_info.get('id')),
                'notes': '学员选择教练：测试'
            }
        },
        {
            'name': '不存在的教练ID',
            'data': {
                'coach_id': 99999,
                'student_id': user_info.get('id'),
                'notes': '学员选择教练：测试'
            }
        },
        {
            'name': '不存在的学员ID',
            'data': {
                'coach_id': 113,
                'student_id': 99999,
                'notes': '学员选择教练：测试'
            }
        }
    ]
    
    for test_case in test_cases:
        print(f"\n--- 测试: {test_case['name']} ---")
        print(f"请求数据: {json.dumps(test_case['data'], indent=2, ensure_ascii=False)}")
        
        response = session.post(
            'http://localhost:8000/api/reservations/relations/',
            json=test_case['data'],
            headers=headers
        )
        
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 201:
            result = response.json()
            relation_id = result.get('id')
            print(f"✅ 成功创建关系，ID: {relation_id}")
            
            # 清理测试数据
            if relation_id:
                try:
                    relation = CoachStudentRelation.objects.get(id=relation_id)
                    relation.delete()
                    print(f"✅ 已删除测试关系 ID: {relation_id}")
                except CoachStudentRelation.DoesNotExist:
                    pass
        else:
            print(f"❌ 请求失败")
            try:
                error_data = response.json()
                print(f"错误详情: {error_data}")
            except:
                print(f"原始响应: {response.text}")

def check_frontend_userstore():
    """检查前端可能的用户状态问题"""
    print("\n=== 检查可能的前端问题 ===")
    
    # 检查用户数据
    try:
        student = User.objects.get(username='hhm')
        print(f"数据库中的学员信息:")
        print(f"   ID: {student.id}")
        print(f"   用户名: {student.username}")
        print(f"   真实姓名: {student.real_name}")
        print(f"   用户类型: {student.user_type}")
        print(f"   是否激活: {student.is_active}")
        print(f"   最后登录: {student.last_login}")
    except User.DoesNotExist:
        print("❌ 学员不存在")
        return
    
    # 检查教练数据
    try:
        coach = User.objects.get(id=113)
        print(f"\n数据库中的教练信息:")
        print(f"   ID: {coach.id}")
        print(f"   用户名: {coach.username}")
        print(f"   真实姓名: {coach.real_name}")
        print(f"   用户类型: {coach.user_type}")
        print(f"   是否激活: {coach.is_active}")
    except User.DoesNotExist:
        print("❌ 教练不存在")
        return
    
    # 检查现有关系
    existing_relations = CoachStudentRelation.objects.filter(
        coach_id=113,
        student_id=student.id
    )
    print(f"\n现有关系:")
    print(f"   数量: {existing_relations.count()}")
    for rel in existing_relations:
        print(f"   ID: {rel.id}, 状态: {rel.status}, 申请者: {rel.applied_by}")

def main():
    """主函数"""
    result = check_user_login_status()
    if result:
        session, user_info = result
        test_different_request_formats(session, user_info)
    
    check_frontend_userstore()

if __name__ == '__main__':
    main()