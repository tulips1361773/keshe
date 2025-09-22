#!/usr/bin/env python
import requests
import json

def debug_frontend_api_issue():
    """调试前端API访问问题"""
    print("=== 调试前端API访问问题 ===")
    
    session = requests.Session()
    
    # 1. 测试CSRF Token获取
    print("\n1. 测试CSRF Token获取:")
    try:
        csrf_response = session.get('http://127.0.0.1:8000/api/accounts/csrf-token/')
        print(f"  状态码: {csrf_response.status_code}")
        print(f"  响应头: {dict(csrf_response.headers)}")
        
        if csrf_response.status_code == 200:
            csrf_data = csrf_response.json()
            csrf_token = csrf_data.get('csrfToken')
            print(f"  CSRF Token: {csrf_token[:20]}..." if csrf_token else "  CSRF Token: None")
            session.headers.update({'X-CSRFToken': csrf_token})
        else:
            print(f"  响应内容: {csrf_response.text}")
            
    except Exception as e:
        print(f"  CSRF Token获取异常: {e}")
        return
    
    # 2. 测试登录
    print("\n2. 测试登录:")
    try:
        login_data = {'username': 'hhm', 'password': '123456'}
        login_response = session.post('http://127.0.0.1:8000/api/accounts/login/', json=login_data)
        print(f"  状态码: {login_response.status_code}")
        print(f"  响应头: {dict(login_response.headers)}")
        
        if login_response.status_code == 200:
            login_result = login_response.json()
            print(f"  登录成功: {login_result.get('success')}")
            print(f"  用户信息: {login_result.get('user', {}).get('username')}")
            
            # 检查cookies
            print(f"  Session Cookies: {dict(session.cookies)}")
        else:
            print(f"  登录失败响应: {login_response.text}")
            return
            
    except Exception as e:
        print(f"  登录异常: {e}")
        return
    
    # 3. 测试Profile API - 不同的请求方式
    print("\n3. 测试Profile API:")
    
    # 3.1 使用session cookies
    try:
        print("  3.1 使用session cookies:")
        profile_response = session.get('http://127.0.0.1:8000/api/accounts/profile/')
        print(f"    状态码: {profile_response.status_code}")
        print(f"    响应头: {dict(profile_response.headers)}")
        
        if profile_response.status_code == 200:
            profile_data = profile_response.json()
            print(f"    成功获取Profile数据")
            print(f"    用户头像: {profile_data.get('user', {}).get('avatar')}")
        else:
            print(f"    失败响应: {profile_response.text}")
            
    except Exception as e:
        print(f"    Session方式异常: {e}")
    
    # 3.2 检查跨域设置
    print("\n  3.2 检查跨域请求:")
    try:
        # 模拟浏览器跨域请求
        headers = {
            'Origin': 'http://localhost:8080',
            'Referer': 'http://localhost:8080/',
            'X-CSRFToken': session.headers.get('X-CSRFToken', ''),
        }
        
        cors_response = session.get('http://127.0.0.1:8000/api/accounts/profile/', headers=headers)
        print(f"    跨域请求状态码: {cors_response.status_code}")
        print(f"    CORS响应头: {dict(cors_response.headers)}")
        
        if cors_response.status_code == 200:
            print(f"    跨域请求成功")
        else:
            print(f"    跨域请求失败: {cors_response.text}")
            
    except Exception as e:
        print(f"    跨域请求异常: {e}")
    
    # 4. 检查Django服务器状态
    print("\n4. 检查Django服务器状态:")
    try:
        health_response = session.get('http://127.0.0.1:8000/admin/')
        print(f"  Admin页面状态码: {health_response.status_code}")
        
        api_root_response = session.get('http://127.0.0.1:8000/api/')
        print(f"  API根路径状态码: {api_root_response.status_code}")
        
    except Exception as e:
        print(f"  服务器状态检查异常: {e}")

if __name__ == '__main__':
    debug_frontend_api_issue()