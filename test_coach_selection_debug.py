#!/usr/bin/env python
"""
教练选择功能调试脚本
基于登录API和CSP错误修复文档的经验，调试教练选择中的"指定的教练或学员不存在"错误
"""
import os
import sys
import django
import requests
import json

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'keshe.settings')
django.setup()

from accounts.models import User
from accounts.models import Coach
from reservations.models import CoachStudentRelation

def check_database_state():
    """检查数据库中教练和学员的状态"""
    print("=== 检查数据库状态 ===")
    
    # 检查学员用户
    student = User.objects.filter(username='hhm').first()
    if student:
        print(f"✅ 学员用户存在: {student.username} (ID: {student.id})")
        print(f"   用户类型: {student.user_type}")
        print(f"   是否激活: {student.is_active}")
    else:
        print("❌ 学员用户不存在")
        return False
    
    # 检查教练
    coaches = Coach.objects.all()[:5]
    print(f"✅ 教练总数: {Coach.objects.count()}")
    for coach in coaches:
        print(f"   教练ID: {coach.id}, 姓名: {coach.user.real_name or coach.user.username}, 用户ID: {coach.user.id if coach.user else 'None'}")
    
    # 检查现有关系
    relations = CoachStudentRelation.objects.filter(student=student)
    print(f"✅ 学员现有教练关系数: {relations.count()}")
    for relation in relations:
        print(f"   关系ID: {relation.id}, 教练: {relation.coach.real_name or relation.coach.username}, 状态: {relation.status}")
    
    return True, student, coaches[0] if coaches else None

def test_api_with_correct_data():
    """使用正确的数据测试API"""
    print("\n=== 测试API调用 ===")
    
    # 先登录获取token
    login_response = requests.post('http://127.0.0.1:8000/api/accounts/login/', 
                                 json={'username': 'hhm', 'password': '123456'})
    
    if login_response.status_code != 200:
        print(f"❌ 登录失败: {login_response.status_code}")
        print(f"   响应: {login_response.text}")
        return False
    
    login_data = login_response.json()
    token = login_data['token']
    user_id = login_data['user']['id']
    print(f"✅ 登录成功, 用户ID: {user_id}, Token: {token[:20]}...")
    
    # 获取CSRF token
    csrf_response = requests.get('http://127.0.0.1:8000/api/accounts/csrf-token/')
    if csrf_response.status_code == 200:
        try:
            csrf_token = csrf_response.json()['csrfToken']
            print(f"✅ CSRF Token: {csrf_token[:20]}...")
        except:
            print(f"❌ CSRF token响应格式错误: {csrf_response.text}")
            return
    else:
        print(f"❌ 获取CSRF token失败: {csrf_response.status_code}")
        return False
    
    # 获取一个教练ID
    coach = Coach.objects.first()
    if not coach:
        print("❌ 没有可用的教练")
        return False
    
    # 使用教练对应的用户ID，而不是Coach模型的ID
    coach_user_id = coach.user.id
    print(f"✅ 使用教练: ID={coach_user_id}, 姓名={coach.user.real_name or coach.user.username}")
    
    # 测试选择教练API
    headers = {
        'Authorization': f'Token {token}',
        'X-CSRFToken': csrf_token,
        'Content-Type': 'application/json'
    }
    
    request_data = {
        'coach_id': coach_user_id,  # 使用用户ID而不是Coach模型ID
        'student_id': user_id,
        'notes': '调试测试选择教练'
    }
    
    print(f"✅ 请求数据: {request_data}")
    print(f"✅ 请求头: Authorization=Token ***, X-CSRFToken={csrf_token[:10]}...")
    
    response = requests.post('http://127.0.0.1:8000/api/reservations/relations/', 
                           json=request_data, headers=headers)
    
    print(f"✅ 响应状态码: {response.status_code}")
    print(f"✅ 响应内容: {response.text}")
    
    if response.status_code == 201:
        print("✅ 选择教练成功!")
        return True
    else:
        print(f"❌ 选择教练失败: {response.status_code}")
        try:
            error_data = response.json()
            print(f"   错误详情: {error_data}")
        except:
            print(f"   原始响应: {response.text}")
        return False

def test_edge_cases():
    """测试边缘情况"""
    print("\n=== 测试边缘情况 ===")
    
    # 登录获取token
    login_response = requests.post('http://127.0.0.1:8000/api/accounts/login/', 
                                 json={'username': 'hhm', 'password': '123456'})
    
    if login_response.status_code != 200:
        print("❌ 登录失败，跳过边缘情况测试")
        return
    
    token = login_response.json()['token']
    csrf_response = requests.get('http://127.0.0.1:8000/api/accounts/csrf-token/')
    if csrf_response.status_code == 200:
        try:
            csrf_token = csrf_response.json()['csrfToken']
        except:
            print(f"❌ CSRF token响应格式错误: {csrf_response.text}")
            return
    else:
        print(f"❌ 获取CSRF token失败: {csrf_response.status_code}")
        return
    
    headers = {
        'Authorization': f'Token {token}',
        'X-CSRFToken': csrf_token,
        'Content-Type': 'application/json'
    }
    
    # 测试1: 不存在的教练ID
    print("\n--- 测试: 不存在的教练ID ---")
    response = requests.post('http://127.0.0.1:8000/api/reservations/relations/', 
                           json={'coach_id': 99999, 'student_id': 4, 'notes': '测试'}, 
                           headers=headers)
    print(f"状态码: {response.status_code}, 响应: {response.text}")
    
    # 测试2: 不存在的学员ID
    print("\n--- 测试: 不存在的学员ID ---")
    coach = Coach.objects.first()
    coach_user_id = coach.user.id  # 使用用户ID
    response = requests.post('http://127.0.0.1:8000/api/reservations/relations/', 
                           json={'coach_id': coach_user_id, 'student_id': 99999, 'notes': '测试'}, 
                           headers=headers)
    print(f"状态码: {response.status_code}, 响应: {response.text}")
    
    # 测试3: 缺少必要字段
    print("\n--- 测试: 缺少必要字段 ---")
    response = requests.post('http://127.0.0.1:8000/api/reservations/relations/', 
                           json={'coach_id': coach_user_id}, 
                           headers=headers)
    print(f"状态码: {response.status_code}, 响应: {response.text}")

def check_serializer_validation():
    """检查序列化器验证逻辑"""
    print("\n=== 检查序列化器验证逻辑 ===")
    
    from reservations.serializers import CoachStudentRelationSerializer
    
    # 获取有效的教练和学员
    coach = Coach.objects.first()
    student = User.objects.filter(username='hhm').first()
    
    if not coach or not student:
        print("❌ 缺少测试数据")
        return
    
    # 测试有效数据
    coach_user_id = coach.user.id  # 使用用户ID
    valid_data = {
        'coach_id': coach_user_id,
        'student_id': student.id,
        'notes': '序列化器测试'
    }
    
    serializer = CoachStudentRelationSerializer(data=valid_data)
    if serializer.is_valid():
        print(f"✅ 有效数据验证通过: {valid_data}")
    else:
        print(f"❌ 有效数据验证失败: {serializer.errors}")
    
    # 测试无效教练ID
    invalid_coach_data = {
        'coach_id': 99999,
        'student_id': student.id,
        'notes': '测试'
    }
    
    serializer = CoachStudentRelationSerializer(data=invalid_coach_data)
    if not serializer.is_valid():
        print(f"✅ 无效教练ID正确被拒绝: {serializer.errors}")
    else:
        print(f"❌ 无效教练ID未被拒绝")

def main():
    """主函数"""
    print("教练选择功能调试脚本")
    print("=" * 50)
    
    # 检查数据库状态
    db_ok, student, coach = check_database_state()
    if not db_ok:
        print("❌ 数据库状态检查失败，退出")
        return
    
    # 测试API调用
    api_ok = test_api_with_correct_data()
    
    # 测试边缘情况
    test_edge_cases()
    
    # 检查序列化器
    check_serializer_validation()
    
    print("\n" + "=" * 50)
    if api_ok:
        print("✅ 教练选择功能正常")
    else:
        print("❌ 教练选择功能存在问题，需要进一步调试")

if __name__ == '__main__':
    main()