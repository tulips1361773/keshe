#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试教练员API修复
验证前端数据结构问题是否已解决
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

from django.contrib.auth import get_user_model
from accounts.models import Coach
from django.test import RequestFactory
from rest_framework.test import force_authenticate
from accounts.views import coach_list

User = get_user_model()

def test_coach_api_response_structure():
    """测试教练员API响应结构"""
    print("\n🔍 测试教练员API响应结构...")
    
    try:
        # 创建测试请求
        factory = RequestFactory()
        request = factory.get('/accounts/api/coaches/')
        
        # 获取一个学生用户进行认证
        student = User.objects.filter(user_type='student').first()
        if not student:
            print("⚠️  没有找到学生用户，创建测试用户")
            student = User.objects.create_user(
                username='test_student_api',
                password='testpass123',
                user_type='student',
                real_name='测试学生'
            )
        
        force_authenticate(request, user=student)
        
        # 调用API视图
        response = coach_list(request)
        response_data = response.data
        
        print(f"✅ API响应状态码: {response.status_code}")
        print(f"📊 响应数据结构:")
        print(f"   - success: {response_data.get('success')}")
        print(f"   - results: {'存在' if 'results' in response_data else '不存在'}")
        print(f"   - count: {response_data.get('count', 'N/A')}")
        print(f"   - num_pages: {response_data.get('num_pages', 'N/A')}")
        
        if 'results' in response_data:
            results = response_data['results']
            print(f"   - results长度: {len(results)}")
            if results:
                print(f"   - 第一个教练数据键: {list(results[0].keys())}")
        
        # 验证前端期望的数据结构
        expected_structure = {
            'success': True,
            'results': [],
            'count': 0
        }
        
        structure_ok = True
        for key in expected_structure.keys():
            if key not in response_data:
                print(f"❌ 缺少字段: {key}")
                structure_ok = False
        
        if structure_ok:
            print("✅ API响应结构符合前端期望")
        else:
            print("❌ API响应结构不符合前端期望")
            
        return structure_ok
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False

def test_frontend_backend_integration():
    """测试前后端集成"""
    print("\n🔗 测试前后端集成...")
    
    try:
        # 检查后端服务器
        backend_url = "http://127.0.0.1:8000"
        response = requests.get(f"{backend_url}/accounts/api/coaches/", timeout=5)
        
        if response.status_code == 401:
            print("⚠️  需要认证，这是正常的")
            return True
        elif response.status_code == 200:
            data = response.json()
            print(f"✅ 后端API可访问")
            print(f"📊 响应数据: {json.dumps(data, ensure_ascii=False, indent=2)[:200]}...")
            return True
        else:
            print(f"❌ 后端API异常，状态码: {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到后端服务器 (http://127.0.0.1:8000)")
        return False
    except Exception as e:
        print(f"❌ 集成测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("🚀 开始教练员API修复验证测试")
    print("=" * 50)
    
    results = []
    
    # 测试API响应结构
    results.append(test_coach_api_response_structure())
    
    # 测试前后端集成
    results.append(test_frontend_backend_integration())
    
    print("\n" + "=" * 50)
    print("📋 测试结果总结:")
    
    if all(results):
        print("✅ 所有测试通过！教练员API修复成功")
        print("🎉 前端应该能够正常获取教练员列表了")
        exit_code = 0
    else:
        print("❌ 部分测试失败，需要进一步检查")
        exit_code = 1
    
    print(f"\n测试完成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    return exit_code

if __name__ == '__main__':
    exit_code = main()
    sys.exit(exit_code)