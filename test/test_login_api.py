#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json

def test_login_api():
    """测试登录API的各种情况"""
    login_url = 'http://127.0.0.1:8000/api/accounts/login/'
    
    # 测试用例
    test_cases = [
        {'username': 'admin', 'password': 'testpass123', 'desc': '管理员正确登录'},
        {'username': 'wronguser', 'password': 'wrongpass', 'desc': '错误用户名密码'},
        {'username': '', 'password': 'testpass123', 'desc': '空用户名'},
        {'username': 'admin', 'password': '', 'desc': '空密码'},
        {'username': '', 'password': '', 'desc': '空用户名和密码'}
    ]
    
    print("=== 登录API测试报告 ===\n")
    
    for i, case in enumerate(test_cases, 1):
        print(f"{i}. 测试: {case['desc']}")
        print(f"   数据: username='{case['username']}', password='{case['password']}'")
        
        try:
            response = requests.post(
                login_url, 
                json={'username': case['username'], 'password': case['password']}, 
                headers={'Content-Type': 'application/json'}
            )
            
            print(f"   状态码: {response.status_code}")
            
            try:
                data = response.json()
                print(f"   响应: {data}")
                
                if response.status_code == 200 and data.get('success'):
                    token = data.get('token', 'N/A')
                    user_info = data.get('user', {})
                    print(f"   ✅ 登录成功 - Token: {token[:20]}...")
                    print(f"   用户类型: {user_info.get('user_type')}")
                else:
                    print(f"   ❌ 登录失败 - {data.get('message', '未知错误')}")
                    
            except json.JSONDecodeError:
                print(f"   响应内容: {response.text}")
                
        except Exception as e:
            print(f"   ❌ 请求异常: {e}")
        
        print()

if __name__ == '__main__':
    test_login_api()