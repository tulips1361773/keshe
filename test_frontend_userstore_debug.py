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

def test_complete_frontend_flow():
    """测试完整的前端认证流程"""
    print("=== 测试完整前端认证流程 ===")
    
    session = requests.Session()
    
    # 1. 获取CSRF token
    print("1. 获取CSRF token...")
    csrf_response = session.get('http://localhost:8000/api/accounts/csrf-token/')
    if csrf_response.status_code != 200:
        print(f"❌ 获取CSRF token失败: {csrf_response.status_code}")
        return None
    
    csrf_token = csrf_response.json().get('csrfToken')
    print(f"✅ CSRF Token: {csrf_token[:20]}...")
    
    # 2. 登录获取token
    print("\n2. 用户登录...")
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
    print(f"   用户信息: {user_info}")
    
    # 3. 模拟前端localStorage存储
    print(f"\n3. 模拟前端localStorage存储...")
    print(f"   localStorage.setItem('token', '{token}')")
    print(f"   localStorage.setItem('user', '{json.dumps(user_info)}')")
    
    # 4. 模拟前端initializeAuth过程
    print(f"\n4. 模拟前端initializeAuth过程...")
    
    # 4.1 从localStorage恢复token
    stored_token = token  # 模拟从localStorage获取
    print(f"   从localStorage恢复token: {stored_token[:20]}...")
    
    # 4.2 设置axios默认headers
    print(f"   设置axios.defaults.headers.common['Authorization'] = 'Token {stored_token}'")
    
    # 4.3 调用fetchProfile
    print(f"   调用fetchProfile...")
    profile_headers = {
        'Authorization': f'Token {stored_token}',
        'Content-Type': 'application/json'
    }
    
    profile_response = session.get(
        'http://localhost:8000/api/accounts/profile/',
        headers=profile_headers
    )
    
    if profile_response.status_code == 200:
        profile_data = profile_response.json()
        profile_user = profile_data.get('user', {})
        print(f"✅ fetchProfile成功")
        print(f"   Profile用户: {profile_user}")
        
        # 5. 模拟选择教练请求
        print(f"\n5. 模拟选择教练请求...")
        
        # 模拟前端CoachSelection组件中的逻辑
        coach = {'id': 113, 'real_name': '测试教练'}
        userStore_userInfo = profile_user  # 这是userStore.userInfo的值
        
        request_data = {
            'coach_id': coach['id'],
            'student_id': userStore_userInfo.get('id'),  # 对应前端的 userStore.userInfo?.id
            'notes': f'学员选择教练：{coach["real_name"]}'
        }
        
        print(f"   教练对象: {coach}")
        print(f"   userStore.userInfo: {userStore_userInfo}")
        print(f"   构造的请求数据: {request_data}")
        
        # 发送请求（需要CSRF token）
        coach_headers = {
            'Authorization': f'Token {stored_token}',
            'X-CSRFToken': csrf_token,
            'Content-Type': 'application/json'
        }
        
        coach_response = session.post(
            'http://localhost:8000/api/reservations/relations/',
            json=request_data,
            headers=coach_headers
        )
        
        print(f"   请求状态码: {coach_response.status_code}")
        
        if coach_response.status_code == 201:
            result_data = coach_response.json()
            relation_id = result_data.get('id')
            print(f"✅ 选择教练成功，关系ID: {relation_id}")
            
            # 清理测试数据
            try:
                from reservations.models import CoachStudentRelation
                CoachStudentRelation.objects.get(id=relation_id).delete()
                print(f"   已删除测试关系 {relation_id}")
            except:
                pass
        else:
            print(f"❌ 选择教练失败")
            try:
                error_data = coach_response.json()
                print(f"   错误信息: {error_data}")
            except:
                print(f"   响应文本: {coach_response.text}")
        
    else:
        print(f"❌ fetchProfile失败: {profile_response.status_code}")
        print(f"   响应: {profile_response.text}")
        print(f"   这会导致userStore.logout()被调用，用户信息被清除")

def test_userstore_edge_cases():
    """测试userStore的边缘情况"""
    print(f"\n=== 测试userStore边缘情况 ===")
    
    edge_cases = [
        {
            'name': 'localStorage中没有token',
            'token': None,
            'expected': 'initializeAuth不会调用fetchProfile'
        },
        {
            'name': 'token无效',
            'token': 'invalid_token_12345',
            'expected': 'fetchProfile返回401，调用logout()清除状态'
        },
        {
            'name': 'fetchProfile返回的user为空',
            'token': 'valid_token',
            'user_response': {'success': True, 'user': None},
            'expected': 'userStore.user为null，userInfo getter返回null'
        }
    ]
    
    for case in edge_cases:
        print(f"\n--- 场景: {case['name']} ---")
        print(f"预期结果: {case['expected']}")
        
        if case['name'] == 'localStorage中没有token':
            print("   userStore.userInfo?.id 将返回 undefined")
            print("   选择教练请求的student_id将为undefined")
            print("   后端将返回'指定的教练或学员不存在'错误")
        
        elif case['name'] == 'token无效':
            # 测试无效token
            session = requests.Session()
            headers = {
                'Authorization': f'Token {case["token"]}',
                'Content-Type': 'application/json'
            }
            
            response = session.get(
                'http://localhost:8000/api/accounts/profile/',
                headers=headers
            )
            
            print(f"   Profile API状态码: {response.status_code}")
            if response.status_code == 401:
                print("   ✅ 确认会返回401，触发logout()")
                print("   userStore.user将被设为null")
                print("   userStore.userInfo?.id 将返回 undefined")

def check_database_user_state():
    """检查数据库中的用户状态"""
    print(f"\n=== 检查数据库用户状态 ===")
    
    try:
        user = User.objects.get(username='hhm')
        print(f"用户信息:")
        print(f"   ID: {user.id}")
        print(f"   用户名: {user.username}")
        print(f"   真实姓名: {user.real_name}")
        print(f"   用户类型: {user.user_type}")
        print(f"   是否激活: {user.is_active}")
        print(f"   最后登录: {user.last_login}")
        
        # 检查用户的token
        from rest_framework.authtoken.models import Token
        try:
            token = Token.objects.get(user=user)
            print(f"   Token: {token.key[:20]}...")
        except Token.DoesNotExist:
            print(f"   Token: 不存在")
            
    except User.DoesNotExist:
        print("❌ 用户不存在")

def main():
    """主函数"""
    check_database_user_state()
    test_complete_frontend_flow()
    test_userstore_edge_cases()

if __name__ == '__main__':
    main()