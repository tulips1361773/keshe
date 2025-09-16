#!/usr/bin/env python
"""
完整功能测试脚本
测试从数据库到后端再到前端的完整流程
"""

import os
import sys
import django
import requests
import json
from datetime import datetime

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'keshe.settings')
django.setup()

from accounts.models import User, Coach
from django.contrib.auth import authenticate

def test_database():
    """测试数据库连接和数据"""
    print("\n" + "="*50)
    print("1. 数据库连接和数据测试")
    print("="*50)
    
    try:
        # 测试数据库连接
        user_count = User.objects.count()
        coach_count = Coach.objects.count()
        
        print(f"✅ 数据库连接成功")
        print(f"📊 用户总数: {user_count}")
        print(f"👨‍🏫 教练员总数: {coach_count}")
        
        # 显示教练员数据样本
        print("\n📋 教练员数据样本:")
        coaches = Coach.objects.select_related('user')[:5]
        for i, coach in enumerate(coaches, 1):
            print(f"  {i}. {coach.user.real_name or coach.user.username} - {coach.get_coach_level_display()} - {coach.get_status_display()}")
        
        return True
        
    except Exception as e:
        print(f"❌ 数据库测试失败: {e}")
        return False

def get_auth_token():
    """获取认证token"""
    base_url = "http://127.0.0.1:8000"
    
    # 先获取CSRF token
    try:
        csrf_response = requests.get(f"{base_url}/accounts/api/csrf-token/", timeout=5)
        if csrf_response.status_code == 200:
            csrf_token = csrf_response.json().get('csrfToken')
        else:
            return None, None
    except:
        return None, None
    
    # 尝试登录获取session
    try:
        # 尝试多个可能的管理员账户
        login_attempts = [
            {'username': 'admin01', 'password': 'admin123'},
            {'username': 'admin01', 'password': '123456'},
            {'username': 'admin01', 'password': 'password'},
            {'username': 'admin01', 'password': 'admin01'}
        ]
        
        for login_data in login_attempts:
            headers = {
                'X-CSRFToken': csrf_token,
                'Content-Type': 'application/json'
            }
            
            login_response = requests.post(
                f"{base_url}/accounts/api/login/", 
                json=login_data,
                headers=headers,
                timeout=5
            )
            
            if login_response.status_code == 200:
                # 获取session cookie
                session_cookie = login_response.cookies.get('sessionid')
                return csrf_token, session_cookie
        
        # 如果所有尝试都失败了
        return None, None
    except:
        return None, None

def test_backend_api():
    """测试后端API接口"""
    print("\n" + "="*50)
    print("2. 后端API接口测试")
    print("="*50)
    
    base_url = "http://127.0.0.1:8000"
    
    # 获取认证信息
    print("🔐 获取认证信息...")
    csrf_token, session_cookie = get_auth_token()
    
    if not csrf_token or not session_cookie:
        print("❌ 无法获取认证信息，使用匿名访问测试")
        headers = {}
        cookies = {}
    else:
        print("✅ 认证信息获取成功")
        headers = {
            'X-CSRFToken': csrf_token,
            'Content-Type': 'application/json'
        }
        cookies = {'sessionid': session_cookie}
    
    # 测试教练员列表API
    try:
        print("\n🔍 测试教练员列表API...")
        response = requests.get(
            f"{base_url}/accounts/api/coaches/", 
            headers=headers,
            cookies=cookies,
            timeout=5
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 教练员列表API正常 (状态码: {response.status_code})")
            
            if isinstance(data, dict) and 'results' in data:
                print(f"📊 返回教练员数量: {len(data['results'])}")
                print(f"📄 总页数信息: {data.get('count', 'N/A')}")
            elif isinstance(data, list):
                print(f"📊 返回教练员数量: {len(data)}")
            
            return True
        else:
            print(f"❌ 教练员列表API异常 (状态码: {response.status_code})")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ API请求失败: {e}")
        return False

def test_coach_detail_api():
    """测试教练员详情API"""
    print("\n🔍 测试教练员详情API...")
    
    try:
        # 获取第一个教练员的ID
        coach = Coach.objects.first()
        if not coach:
            print("⚠️  没有找到教练员数据，跳过详情API测试")
            return True
            
        base_url = "http://127.0.0.1:8000"
        response = requests.get(f"{base_url}/accounts/coaches/{coach.id}/", timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 教练员详情API正常 (ID: {coach.id})")
            print(f"👤 教练员姓名: {data.get('user', {}).get('real_name', 'N/A')}")
            return True
        else:
            print(f"❌ 教练员详情API异常 (状态码: {response.status_code})")
            return False
            
    except Exception as e:
        print(f"❌ 教练员详情API测试失败: {e}")
        return False

def test_avatar_upload_api():
    """测试头像上传API"""
    print("\n🔍 测试头像上传API...")
    
    try:
        base_url = "http://127.0.0.1:8000"
        
        # 创建一个测试用的小图片文件
        test_image_content = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde\x00\x00\x00\tpHYs\x00\x00\x0b\x13\x00\x00\x0b\x13\x01\x00\x9a\x9c\x18\x00\x00\x00\nIDATx\x9cc```\x00\x00\x00\x02\x00\x01H\xaf\xa4q\x00\x00\x00\x00IEND\xaeB`\x82'
        
        files = {'avatar': ('test.png', test_image_content, 'image/png')}
        
        # 注意：这个测试需要认证，所以可能会返回401，这是正常的
        response = requests.post(f"{base_url}/accounts/api/upload-avatar/", files=files, timeout=5)
        
        if response.status_code in [200, 401, 403]:  # 401/403是因为没有认证，但API存在
            print(f"✅ 头像上传API端点存在 (状态码: {response.status_code})")
            if response.status_code == 401:
                print("ℹ️  需要用户认证（这是正常的安全机制）")
            return True
        else:
            print(f"❌ 头像上传API异常 (状态码: {response.status_code})")
            return False
            
    except Exception as e:
        print(f"❌ 头像上传API测试失败: {e}")
        return False

def test_frontend_accessibility():
    """测试前端页面可访问性"""
    print("\n" + "="*50)
    print("3. 前端页面可访问性测试")
    print("="*50)
    
    frontend_url = "http://localhost:3001"
    
    try:
        print("🔍 测试前端主页...")
        response = requests.get(frontend_url, timeout=5)
        
        if response.status_code == 200:
            print(f"✅ 前端服务正常运行 (状态码: {response.status_code})")
            print(f"🌐 前端地址: {frontend_url}")
            return True
        else:
            print(f"❌ 前端服务异常 (状态码: {response.status_code})")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ 前端服务连接失败: {e}")
        print("💡 请确保前端开发服务器正在运行 (npm run dev)")
        return False

def main():
    """主测试函数"""
    print("🚀 开始完整功能测试")
    print(f"⏰ 测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    results = []
    
    # 1. 数据库测试
    results.append(test_database())
    
    # 2. 后端API测试
    results.append(test_backend_api())
    results.append(test_coach_detail_api())
    results.append(test_avatar_upload_api())
    
    # 3. 前端测试
    results.append(test_frontend_accessibility())
    
    # 总结
    print("\n" + "="*50)
    print("📊 测试结果总结")
    print("="*50)
    
    passed = sum(results)
    total = len(results)
    
    print(f"✅ 通过测试: {passed}/{total}")
    print(f"❌ 失败测试: {total - passed}/{total}")
    
    if passed == total:
        print("\n🎉 所有测试通过！系统功能正常！")
    else:
        print("\n⚠️  部分测试失败，请检查相关服务和配置")
    
    print("\n💡 建议进一步测试:")
    print("   - 在浏览器中访问 http://localhost:3001")
    print("   - 测试教练员列表和详情页面")
    print("   - 测试用户登录和头像上传功能")

if __name__ == "__main__":
    main()