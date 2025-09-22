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

def check_current_data():
    """检查当前的教练和学员数据"""
    print("=== 检查当前数据状态 ===")
    
    # 检查学员hhm
    try:
        student = User.objects.get(username='hhm')
        print(f"✅ 学员 hhm 存在:")
        print(f"   ID: {student.id}")
        print(f"   用户名: {student.username}")
        print(f"   用户类型: {student.user_type}")
        print(f"   是否激活: {student.is_active}")
    except User.DoesNotExist:
        print("❌ 学员 hhm 不存在")
        return False
    
    # 检查教练113
    try:
        coach = User.objects.get(id=113)
        print(f"✅ 教练 ID 113 存在:")
        print(f"   ID: {coach.id}")
        print(f"   用户名: {coach.username}")
        print(f"   用户类型: {coach.user_type}")
        print(f"   是否激活: {coach.is_active}")
    except User.DoesNotExist:
        print("❌ 教练 ID 113 不存在")
        
        # 查找其他教练
        coaches = User.objects.filter(user_type='coach', is_active=True)[:5]
        print(f"可用教练列表 (前5个):")
        for c in coaches:
            print(f"   ID: {c.id}, 用户名: {c.username}, 真实姓名: {c.real_name}")
        return False
    
    # 检查现有关系
    existing_relations = CoachStudentRelation.objects.filter(
        coach_id=113, 
        student_id=student.id
    )
    print(f"现有关系数量: {existing_relations.count()}")
    for rel in existing_relations:
        print(f"   关系ID: {rel.id}, 状态: {rel.status}, 创建时间: {rel.created_at}")
    
    return True

def simulate_frontend_request():
    """模拟前端请求"""
    print("\n=== 模拟前端请求 ===")
    
    # 获取学员信息
    try:
        student = User.objects.get(username='hhm')
        student_id = student.id
    except User.DoesNotExist:
        print("❌ 无法获取学员信息")
        return
    
    # 模拟前端发送的数据
    request_data = {
        'coach_id': 113,
        'student_id': student_id,
        'notes': '学员选择教练：测试'
    }
    
    print(f"请求数据: {json.dumps(request_data, indent=2, ensure_ascii=False)}")
    
    # 使用requests发送请求
    session = requests.Session()
    
    # 获取CSRF token
    csrf_response = session.get('http://localhost:8000/api/accounts/csrf-token/')
    if csrf_response.status_code == 200:
        csrf_token = csrf_response.json().get('csrfToken')
        print(f"CSRF Token: {csrf_token[:20]}...")
    else:
        print(f"❌ 获取CSRF token失败: {csrf_response.status_code}")
        return
    
    # 登录
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
    
    if login_response.status_code == 200:
        print("✅ 登录成功")
        login_result = login_response.json()
        user_info = login_result.get('user', {})
        print(f"   用户ID: {user_info.get('id')}")
        print(f"   用户名: {user_info.get('username')}")
    else:
        print(f"❌ 登录失败: {login_response.status_code}")
        print(f"   响应: {login_response.text}")
        return
    
    # 发送选择教练请求
    # 更新CSRF token（可能在登录后有变化）
    cookies = session.cookies.get_dict()
    csrf_from_cookie = cookies.get('csrftoken')
    if csrf_from_cookie:
        headers['X-CSRFToken'] = csrf_from_cookie
    
    coach_response = session.post(
        'http://localhost:8000/api/reservations/relations/',
        json=request_data,
        headers=headers
    )
    
    print(f"\n选择教练请求结果:")
    print(f"   状态码: {coach_response.status_code}")
    print(f"   响应内容: {coach_response.text}")
    
    if coach_response.status_code == 201:
        result = coach_response.json()
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
            error_data = coach_response.json()
            print(f"   错误详情: {error_data}")
        except:
            print(f"   原始响应: {coach_response.text}")

def check_serializer_validation():
    """检查序列化器验证逻辑"""
    print("\n=== 检查序列化器验证 ===")
    
    from reservations.serializers import CoachStudentRelationSerializer
    
    # 获取学员信息
    try:
        student = User.objects.get(username='hhm')
        student_id = student.id
    except User.DoesNotExist:
        print("❌ 无法获取学员信息")
        return
    
    # 测试数据
    test_data = {
        'coach_id': 113,
        'student_id': student_id,
        'notes': '测试验证'
    }
    
    print(f"测试数据: {test_data}")
    
    # 创建序列化器实例
    serializer = CoachStudentRelationSerializer(data=test_data)
    
    if serializer.is_valid():
        print("✅ 数据验证通过")
        try:
            instance = serializer.save()
            print(f"✅ 成功创建关系，ID: {instance.id}")
            # 清理测试数据
            instance.delete()
            print(f"✅ 已删除测试关系")
        except Exception as e:
            print(f"❌ 创建失败: {e}")
    else:
        print("❌ 数据验证失败")
        print(f"   错误: {serializer.errors}")

if __name__ == '__main__':
    if check_current_data():
        simulate_frontend_request()
        check_serializer_validation()