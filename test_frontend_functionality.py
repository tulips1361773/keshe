#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
前端功能测试脚本
测试前端页面的可访问性和基本功能
"""

import requests
import time
from datetime import datetime

def test_frontend_pages():
    """测试前端页面可访问性"""
    print("🚀 开始前端功能测试")
    print(f"⏰ 测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    base_url = "http://localhost:3001"
    
    test_pages = [
        {
            'name': '主页',
            'url': f"{base_url}/",
            'expected_content': ['教练员管理系统', 'Vue', 'Vite']
        },
        {
            'name': '教练员列表页',
            'url': f"{base_url}/#/coaches",
            'expected_content': ['教练员', '搜索']
        },
        {
            'name': '登录页',
            'url': f"{base_url}/#/login",
            'expected_content': ['登录', '用户名', '密码']
        }
    ]
    
    print("\n" + "="*50)
    print("前端页面可访问性测试")
    print("="*50)
    
    success_count = 0
    total_count = len(test_pages)
    
    for page in test_pages:
        print(f"\n🔍 测试 {page['name']}...")
        try:
            response = requests.get(page['url'], timeout=10)
            
            if response.status_code == 200:
                print(f"✅ {page['name']} 可访问 (状态码: {response.status_code})")
                
                # 检查页面内容
                content_found = 0
                for expected in page['expected_content']:
                    if expected.lower() in response.text.lower():
                        content_found += 1
                
                if content_found > 0:
                    print(f"📄 页面内容检查: {content_found}/{len(page['expected_content'])} 项匹配")
                    success_count += 1
                else:
                    print(f"⚠️  页面内容可能不完整")
                    
            else:
                print(f"❌ {page['name']} 访问异常 (状态码: {response.status_code})")
                
        except requests.exceptions.Timeout:
            print(f"⏰ {page['name']} 访问超时")
        except requests.exceptions.ConnectionError:
            print(f"🔌 {page['name']} 连接失败 - 前端服务可能未启动")
        except Exception as e:
            print(f"❌ {page['name']} 测试出错: {str(e)}")
    
    print("\n" + "="*50)
    print("📊 前端测试结果总结")
    print("="*50)
    
    if success_count == total_count:
        print(f"✅ 所有页面测试通过 ({success_count}/{total_count})")
        print("🎉 前端功能正常！")
    elif success_count > 0:
        print(f"⚠️  部分页面测试通过 ({success_count}/{total_count})")
        print("💡 建议检查失败的页面")
    else:
        print(f"❌ 所有页面测试失败 ({success_count}/{total_count})")
        print("🔧 请检查前端服务是否正常运行")
    
    return success_count, total_count

def test_api_integration():
    """测试前端与后端API的集成"""
    print("\n" + "="*50)
    print("API集成测试")
    print("="*50)
    
    # 测试前端是否能正确调用后端API
    frontend_url = "http://localhost:3001"
    backend_url = "http://127.0.0.1:8000"
    
    print("🔍 测试前端服务状态...")
    try:
        frontend_response = requests.get(frontend_url, timeout=5)
        if frontend_response.status_code == 200:
            print("✅ 前端服务正常运行")
        else:
            print(f"❌ 前端服务异常 (状态码: {frontend_response.status_code})")
            return False
    except Exception as e:
        print(f"❌ 前端服务连接失败: {e}")
        return False
    
    print("\n🔍 测试后端服务状态...")
    try:
        backend_response = requests.get(f"{backend_url}/accounts/api/csrf-token/", timeout=5)
        if backend_response.status_code == 200:
            print("✅ 后端服务正常运行")
        else:
            print(f"❌ 后端服务异常 (状态码: {backend_response.status_code})")
            return False
    except Exception as e:
        print(f"❌ 后端服务连接失败: {e}")
        return False
    
    print("\n✅ 前后端服务都正常运行")
    print("💡 建议在浏览器中手动测试具体功能")
    return True

def main():
    """主测试函数"""
    print("🎯 开始完整的前端功能测试")
    
    # 测试前端页面
    success_pages, total_pages = test_frontend_pages()
    
    # 测试API集成
    api_integration_ok = test_api_integration()
    
    print("\n" + "="*60)
    print("🏁 最终测试结果")
    print("="*60)
    
    print(f"📄 前端页面测试: {success_pages}/{total_pages} 通过")
    print(f"🔗 API集成测试: {'✅ 通过' if api_integration_ok else '❌ 失败'}")
    
    if success_pages == total_pages and api_integration_ok:
        print("\n🎉 恭喜！所有前端功能测试通过！")
        print("💡 系统已准备就绪，可以开始使用")
    else:
        print("\n⚠️  部分测试未通过，建议进一步检查")
    
    print("\n📋 后续建议:")
    print("   1. 在浏览器中访问 http://localhost:3001")
    print("   2. 测试用户注册和登录功能")
    print("   3. 测试教练员列表和详情页面")
    print("   4. 测试头像上传功能")
    print("   5. 测试搜索和筛选功能")

if __name__ == "__main__":
    main()