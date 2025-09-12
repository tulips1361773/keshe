#!/usr/bin/env python
"""
测试API端点的脚本
使用token认证测试各个API是否正常工作
"""

import requests
import json

# 配置
BASE_URL = 'http://127.0.0.1:8000'
TOKEN = '2f4e9746ba1c15900dd4df0858e5dd67a099a79e'

# 请求头
headers = {
    'Authorization': f'Token {TOKEN}',
    'Content-Type': 'application/json',
}

def test_api_endpoint(url, method='GET', data=None):
    """测试API端点"""
    try:
        full_url = f"{BASE_URL}{url}"
        print(f"\n测试: {method} {full_url}")
        
        if method == 'GET':
            response = requests.get(full_url, headers=headers)
        elif method == 'POST':
            response = requests.post(full_url, headers=headers, json=data)
        
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            try:
                result = response.json()
                print(f"响应: {json.dumps(result, indent=2, ensure_ascii=False)[:200]}...")
            except:
                print(f"响应: {response.text[:200]}...")
        else:
            print(f"错误: {response.text}")
            
        return response.status_code == 200
        
    except Exception as e:
        print(f"请求失败: {e}")
        return False

def main():
    """主测试函数"""
    print("开始测试API端点...")
    
    # 测试的API端点
    test_endpoints = [
        '/accounts/api/profile/',
        '/accounts/api/stats/',
        '/api/notifications/list/?page=1&page_size=5',
        '/api/notifications/unread-count/',
        '/payments/api/account/',
        '/payments/api/account/transactions/',
        '/api/reservations/bookings/?page=1&page_size=10',
    ]
    
    success_count = 0
    total_count = len(test_endpoints)
    
    for endpoint in test_endpoints:
        if test_api_endpoint(endpoint):
            success_count += 1
    
    print(f"\n测试完成: {success_count}/{total_count} 个端点成功")
    
    if success_count == total_count:
        print("✅ 所有API端点都正常工作!")
    else:
        print("❌ 部分API端点存在问题")

if __name__ == '__main__':
    main()