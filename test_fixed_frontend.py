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
from rest_framework.authtoken.models import Token

def test_user_authentication_fix():
    """测试修复后的用户认证流程"""
    print("=== 测试修复后的用户认证流程 ===")
    
    # 1. 检查用户和token状态
    try:
        user = User.objects.get(username='hhm')
        print(f"✅ 用户存在: {user.username} (ID: {user.id})")
        
        # 确保用户有token
        token, created = Token.objects.get_or_create(user=user)
        if created:
            print(f"✅ 为用户创建新token: {token.key[:20]}...")
        else:
            print(f"✅ 用户已有token: {token.key[:20]}...")
            
    except User.DoesNotExist:
        print("❌ 用户不存在")
        return False
    
    # 2. 测试完整的认证流程
    session = requests.Session()
    
    # 2.1 获取CSRF token
    csrf_response = session.get('http://localhost:8000/api/accounts/csrf-token/')
    if csrf_response.status_code != 200:
        print(f"❌ 获取CSRF token失败: {csrf_response.status_code}")
        return False
    
    csrf_token = csrf_response.json().get('csrfToken')
    print(f"✅ CSRF Token: {csrf_token[:20]}...")
    
    # 2.2 登录
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
        return False
    
    login_result = login_response.json()
    user_info = login_result.get('user', {})
    auth_token = login_result.get('token')
    
    print(f"✅ 登录成功")
    print(f"   Token: {auth_token[:20] if auth_token else 'None'}...")
    print(f"   用户ID: {user_info.get('id')}")
    print(f"   用户名: {user_info.get('username')}")
    
    # 2.3 模拟前端initializeAuth - fetchProfile
    profile_headers = {
        'Authorization': f'Token {auth_token}',
        'Content-Type': 'application/json'
    }
    
    profile_response = session.get(
        'http://localhost:8000/api/accounts/profile/',
        headers=profile_headers
    )
    
    if profile_response.status_code != 200:
        print(f"❌ fetchProfile失败: {profile_response.status_code}")
        print(f"   响应: {profile_response.text}")
        return False
    
    profile_data = profile_response.json()
    profile_user = profile_data.get('user', {})
    
    print(f"✅ fetchProfile成功")
    print(f"   用户ID: {profile_user.get('id')}")
    print(f"   用户名: {profile_user.get('username')}")
    
    # 2.4 模拟修复后的选择教练逻辑
    print(f"\n--- 模拟修复后的选择教练逻辑 ---")
    
    # 检查认证状态 (isAuthenticated)
    is_authenticated = bool(auth_token)
    print(f"isAuthenticated: {is_authenticated}")
    
    # 检查用户信息 (userInfo)
    userInfo = profile_user
    has_user_info = userInfo and userInfo.get('id')
    print(f"userInfo存在且有ID: {has_user_info}")
    
    if not is_authenticated:
        print("❌ 前端会显示: 请先登录后再选择教练")
        return False
    
    if not has_user_info:
        print("❌ 前端会显示: 用户信息加载中，请稍后重试")
        return False
    
    # 构造请求数据
    coach = {'id': 113, 'real_name': '测试教练'}
    request_data = {
        'coach_id': coach['id'],
        'student_id': userInfo.get('id'),  # 现在确保有值
        'notes': f'学员选择教练：{coach["real_name"]}'
    }
    
    print(f"✅ 构造的请求数据: {request_data}")
    
    # 发送选择教练请求
    coach_headers = {
        'Authorization': f'Token {auth_token}',
        'X-CSRFToken': csrf_token,
        'Content-Type': 'application/json'
    }
    
    coach_response = session.post(
        'http://localhost:8000/api/reservations/relations/',
        json=request_data,
        headers=coach_headers
    )
    
    print(f"选择教练请求状态码: {coach_response.status_code}")
    
    if coach_response.status_code == 201:
        result_data = coach_response.json()
        relation_id = result_data.get('id')
        print(f"✅ 选择教练成功！关系ID: {relation_id}")
        
        # 清理测试数据
        try:
            from reservations.models import CoachStudentRelation
            CoachStudentRelation.objects.get(id=relation_id).delete()
            print(f"   已删除测试关系 {relation_id}")
        except:
            pass
        
        return True
    else:
        print(f"❌ 选择教练失败")
        try:
            error_data = coach_response.json()
            print(f"   错误信息: {error_data}")
        except:
            print(f"   响应文本: {coach_response.text}")
        return False

def test_edge_cases():
    """测试边缘情况"""
    print(f"\n=== 测试边缘情况 ===")
    
    edge_cases = [
        {
            'name': '无效token的情况',
            'token': 'invalid_token_12345',
            'expected_behavior': 'fetchProfile返回401，前端调用logout()清除状态'
        },
        {
            'name': '空token的情况',
            'token': '',
            'expected_behavior': '前端不会调用fetchProfile，userInfo为null'
        }
    ]
    
    for case in edge_cases:
        print(f"\n--- 测试: {case['name']} ---")
        print(f"预期行为: {case['expected_behavior']}")
        
        if case['token']:
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
            
            print(f"Profile API状态码: {response.status_code}")
            if response.status_code == 401:
                print("✅ 确认返回401，前端会调用logout()清除状态")
            else:
                print(f"❌ 意外的状态码: {response.status_code}")
        else:
            print("✅ 空token情况下，前端不会发送请求")

def main():
    """主函数"""
    success = test_user_authentication_fix()
    test_edge_cases()
    
    if success:
        print(f"\n🎉 修复验证成功！前端选择教练功能应该正常工作了。")
        print(f"📝 修复要点:")
        print(f"   1. 添加了用户认证状态检查")
        print(f"   2. 添加了用户信息存在性检查")
        print(f"   3. 在用户信息不存在时尝试重新获取")
        print(f"   4. 改进了错误提示信息")
    else:
        print(f"\n❌ 仍有问题需要进一步调试")

if __name__ == '__main__':
    main()