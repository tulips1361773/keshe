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

def check_user_authentication_flow():
    """检查完整的用户认证流程"""
    print("=== 检查用户认证流程 ===")
    
    session = requests.Session()
    
    # 1. 获取CSRF token
    csrf_response = session.get('http://localhost:8000/api/accounts/csrf-token/')
    if csrf_response.status_code != 200:
        print(f"❌ 获取CSRF token失败: {csrf_response.status_code}")
        return None
    
    csrf_token = csrf_response.json().get('csrfToken')
    print(f"✅ CSRF Token获取成功: {csrf_token[:20]}...")
    
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
    token = login_result.get('token')
    
    print(f"✅ 登录成功")
    print(f"   Token: {token[:20] if token else 'None'}...")
    print(f"   用户ID: {user_info.get('id')}")
    print(f"   用户名: {user_info.get('username')}")
    print(f"   真实姓名: {user_info.get('real_name')}")
    print(f"   用户类型: {user_info.get('user_type')}")
    
    # 3. 测试profile API
    profile_headers = {
        'Authorization': f'Token {token}',
        'X-CSRFToken': csrf_token,
        'Content-Type': 'application/json'
    }
    
    profile_response = session.get(
        'http://localhost:8000/api/accounts/profile/',
        headers=profile_headers
    )
    
    if profile_response.status_code == 200:
        profile_data = profile_response.json()
        profile_user = profile_data.get('user', {})
        print(f"✅ Profile API成功")
        print(f"   Profile用户ID: {profile_user.get('id')}")
        print(f"   Profile用户名: {profile_user.get('username')}")
    else:
        print(f"❌ Profile API失败: {profile_response.status_code}")
        print(f"   响应: {profile_response.text}")
    
    return session, user_info, token

def test_coach_selection_with_different_data():
    """测试不同数据格式的教练选择请求"""
    print("\n=== 测试教练选择请求 ===")
    
    result = check_user_authentication_flow()
    if not result:
        return
    
    session, user_info, token = result
    
    # 准备请求头
    headers = {
        'Authorization': f'Token {token}',
        'Content-Type': 'application/json'
    }
    
    # 测试数据集
    test_cases = [
        {
            'name': '正常数据（从登录响应获取）',
            'data': {
                'coach_id': 113,
                'student_id': user_info.get('id'),
                'notes': f'学员选择教练测试'
            }
        },
        {
            'name': '用户ID为None的情况',
            'data': {
                'coach_id': 113,
                'student_id': None,
                'notes': f'学员选择教练测试'
            }
        },
        {
            'name': '用户ID为undefined的情况',
            'data': {
                'coach_id': 113,
                'student_id': 'undefined',
                'notes': f'学员选择教练测试'
            }
        },
        {
            'name': '缺少student_id字段',
            'data': {
                'coach_id': 113,
                'notes': f'学员选择教练测试'
            }
        }
    ]
    
    for test_case in test_cases:
        print(f"\n--- 测试: {test_case['name']} ---")
        print(f"请求数据: {test_case['data']}")
        
        try:
            response = session.post(
                'http://localhost:8000/api/reservations/relations/',
                json=test_case['data'],
                headers=headers
            )
            
            print(f"状态码: {response.status_code}")
            
            if response.status_code == 201:
                result_data = response.json()
                relation_id = result_data.get('id')
                print(f"✅ 成功创建关系，ID: {relation_id}")
                
                # 删除测试数据
                if relation_id:
                    try:
                        CoachStudentRelation.objects.get(id=relation_id).delete()
                        print(f"   已删除测试关系 {relation_id}")
                    except:
                        pass
            else:
                print(f"❌ 请求失败")
                try:
                    error_data = response.json()
                    print(f"   错误信息: {error_data}")
                except:
                    print(f"   响应文本: {response.text}")
                    
        except Exception as e:
            print(f"❌ 请求异常: {str(e)}")

def check_frontend_userstore_simulation():
    """模拟前端userStore可能的状态"""
    print("\n=== 模拟前端userStore状态 ===")
    
    # 模拟不同的userStore状态
    scenarios = [
        {
            'name': '正常登录状态',
            'userInfo': {'id': 4, 'username': 'hhm', 'user_type': 'student'},
            'token': 'valid_token_here'
        },
        {
            'name': 'userInfo为null',
            'userInfo': None,
            'token': 'valid_token_here'
        },
        {
            'name': 'userInfo为空对象',
            'userInfo': {},
            'token': 'valid_token_here'
        },
        {
            'name': 'userInfo.id为undefined',
            'userInfo': {'username': 'hhm', 'user_type': 'student'},
            'token': 'valid_token_here'
        }
    ]
    
    for scenario in scenarios:
        print(f"\n--- 场景: {scenario['name']} ---")
        userInfo = scenario['userInfo']
        
        # 模拟前端代码：userStore.userInfo?.id
        student_id = userInfo.get('id') if userInfo else None
        
        print(f"userInfo: {userInfo}")
        print(f"student_id (userInfo?.id): {student_id}")
        
        request_data = {
            'coach_id': 113,
            'student_id': student_id,
            'notes': '学员选择教练测试'
        }
        
        print(f"构造的请求数据: {request_data}")
        
        # 判断这种情况下后端会如何响应
        if student_id is None:
            print("❌ 这种情况会导致'指定的教练或学员不存在'错误")
        elif not isinstance(student_id, int):
            print("❌ 这种情况可能导致类型错误")
        else:
            print("✅ 这种情况应该正常工作")

def main():
    """主函数"""
    check_user_authentication_flow()
    test_coach_selection_with_different_data()
    check_frontend_userstore_simulation()

if __name__ == '__main__':
    main()