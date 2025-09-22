#!/usr/bin/env python
import os
import sys
import django
import requests
from django.conf import settings

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'keshe.settings')
django.setup()

def test_csrf_endpoint():
    """测试CSRF token端点"""
    print("=== 测试CSRF token端点 ===")
    
    # 测试CSRF token API
    session = requests.Session()
    csrf_response = session.get('http://localhost:8000/api/accounts/csrf-token/')
    
    print(f"CSRF端点状态码: {csrf_response.status_code}")
    if csrf_response.status_code == 200:
        csrf_data = csrf_response.json()
        print(f"CSRF响应数据: {csrf_data}")
        csrf_token = csrf_data.get('csrfToken')
        print(f"获取到的CSRF token: {csrf_token[:20]}..." if csrf_token else "未获取到CSRF token")
        
        # 测试使用CSRF token发送请求
        print("\n=== 测试使用CSRF token发送请求 ===")
        
        # 先登录
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
        
        print(f"登录状态码: {login_response.status_code}")
        if login_response.status_code == 200:
            login_result = login_response.json()
            print(f"登录成功，用户: {login_result.get('user', {}).get('username')}")
            
            # 测试选择教练
            coach_data = {
                'coach_id': 113,
                'student_id': 4,
                'notes': '测试选择教练'
            }
            
            # 更新headers，可能需要新的CSRF token
            cookies = session.cookies.get_dict()
            print(f"当前cookies: {cookies}")
            
            # 从cookies中获取CSRF token
            csrf_from_cookie = cookies.get('csrftoken')
            if csrf_from_cookie:
                headers['X-CSRFToken'] = csrf_from_cookie
                print(f"使用cookie中的CSRF token: {csrf_from_cookie[:20]}...")
            
            coach_response = session.post(
                'http://localhost:8000/api/reservations/relations/',
                json=coach_data,
                headers=headers
            )
            
            print(f"选择教练状态码: {coach_response.status_code}")
            print(f"选择教练响应: {coach_response.text}")
            
            if coach_response.status_code == 201:
                result = coach_response.json()
                relation_id = result.get('id')
                print(f"成功创建关系，ID: {relation_id}")
                
                # 清理测试数据
                from reservations.models import CoachStudentRelation
                if relation_id:
                    try:
                        relation = CoachStudentRelation.objects.get(id=relation_id)
                        relation.delete()
                        print(f"已删除测试关系 ID: {relation_id}")
                    except CoachStudentRelation.DoesNotExist:
                        pass
        else:
            print(f"登录失败: {login_response.text}")
    else:
        print(f"获取CSRF token失败: {csrf_response.text}")

if __name__ == '__main__':
    test_csrf_endpoint()