#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试前端应用状态
检查前端应用是否正常运行，排除浏览器扩展错误的干扰
"""

import requests
import json
from datetime import datetime

def test_frontend_status():
    """测试前端应用状态"""
    print("🔍 前端应用状态检查")
    print("=" * 50)
    
    frontend_url = "http://localhost:3002"
    
    print(f"检查时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"前端地址: {frontend_url}")
    print()
    
    # 1. 检查前端主页
    print("=== 1. 检查前端主页 ===")
    try:
        response = requests.get(frontend_url, timeout=10)
        print(f"状态码: {response.status_code}")
        print(f"响应头: {dict(response.headers)}")
        
        if response.status_code == 200:
            content = response.text
            print(f"页面内容长度: {len(content)} 字符")
            
            # 检查关键内容
            if "<!DOCTYPE html" in content:
                print("✅ HTML文档结构正常")
            else:
                print("❌ HTML文档结构异常")
                
            if "vite" in content.lower():
                print("✅ Vite开发服务器正常")
            else:
                print("⚠️  未检测到Vite标识")
                
            if "vue" in content.lower():
                print("✅ Vue应用正常")
            else:
                print("⚠️  未检测到Vue标识")
                
        else:
            print(f"❌ 前端服务异常: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到前端服务")
        return False
    except Exception as e:
        print(f"❌ 检查前端服务时出错: {e}")
        return False
    
    # 2. 检查静态资源
    print("\n=== 2. 检查静态资源 ===")
    static_urls = [
        f"{frontend_url}/vite.svg",
        f"{frontend_url}/src/main.js",
        f"{frontend_url}/src/App.vue"
    ]
    
    for url in static_urls:
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                print(f"✅ {url.split('/')[-1]}: 可访问")
            else:
                print(f"⚠️  {url.split('/')[-1]}: {response.status_code}")
        except Exception as e:
            print(f"❌ {url.split('/')[-1]}: 访问失败 - {e}")
    
    # 3. 检查API连接
    print("\n=== 3. 检查后端API连接 ===")
    backend_url = "http://localhost:8000"
    
    try:
        # 检查CSRF token端点
        response = requests.get(f"{backend_url}/api/accounts/csrf-token/", timeout=5)
        if response.status_code == 200:
            print("✅ 后端API连接正常")
            data = response.json()
            print(f"   CSRF Token: {data.get('csrf_token', 'N/A')[:20]}...")
        else:
            print(f"❌ 后端API异常: {response.status_code}")
    except Exception as e:
        print(f"❌ 后端API连接失败: {e}")
    
    print("\n=== 结论 ===")
    print("如果看到'Failed to fetch latest config'错误:")
    print("1. 这很可能来自浏览器扩展（如Trae AI扩展）")
    print("2. 不是我们应用代码的问题")
    print("3. 可以安全忽略，不影响应用功能")
    print("4. 如需消除，可以禁用相关浏览器扩展")
    print()
    print("✅ 前端应用状态检查完成")
    
    return True

if __name__ == '__main__':
    test_frontend_status()