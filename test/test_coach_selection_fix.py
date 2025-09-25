#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试选择教练功能修复
验证前后端数据格式匹配
"""

import os
import sys
import django
import requests
import json
from datetime import datetime

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'keshe.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
django.setup()

from django.contrib.auth import get_user_model
from reservations.models import CoachStudentRelation
from reservations.serializers import CoachStudentRelationSerializer
from django.test import RequestFactory
from django.contrib.auth.models import AnonymousUser

User = get_user_model()

def test_coach_selection_data_format():
    """测试选择教练的数据格式"""
    print("\n=== 测试选择教练数据格式 ===")
    
    try:
        # 创建测试用户
        coach = User.objects.filter(user_type='coach').first()
        student = User.objects.filter(user_type='student').first()
        
        if not coach or not student:
            print("❌ 缺少测试用户（教练或学员）")
            return False
        
        print(f"✅ 找到测试教练: {coach.real_name} (ID: {coach.id})")
        print(f"✅ 找到测试学员: {student.real_name} (ID: {student.id})")
        
        # 测试序列化器验证
        factory = RequestFactory()
        request = factory.post('/api/reservations/relations/')
        request.user = student
        
        # 测试正确的数据格式 (coach_id)
        correct_data = {
            'coach_id': coach.id,
            'notes': f'学员选择教练：{coach.real_name}'
        }
        
        serializer = CoachStudentRelationSerializer(
            data=correct_data,
            context={'request': request}
        )
        
        if serializer.is_valid():
            print("✅ 正确数据格式验证通过 (coach_id)")
            print(f"   数据: {correct_data}")
        else:
            print(f"❌ 正确数据格式验证失败: {serializer.errors}")
            return False
        
        # 测试错误的数据格式 (coach)
        wrong_data = {
            'coach': coach.id,  # 错误的字段名
            'notes': f'学员选择教练：{coach.real_name}'
        }
        
        wrong_serializer = CoachStudentRelationSerializer(
            data=wrong_data,
            context={'request': request}
        )
        
        if not wrong_serializer.is_valid():
            print("✅ 错误数据格式正确被拒绝 (coach)")
            print(f"   错误: {wrong_serializer.errors}")
        else:
            print("❌ 错误数据格式未被拒绝")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ 测试过程中出现错误: {str(e)}")
        return False

def test_api_endpoint_accessibility():
    """测试API端点可访问性"""
    print("\n=== 测试API端点可访问性 ===")
    
    try:
        # 测试后端服务器
        backend_url = "http://127.0.0.1:8000/api/reservations/relations/"
        
        response = requests.get(backend_url, timeout=5)
        print(f"✅ 后端API可访问 - 状态码: {response.status_code}")
        
        if response.status_code == 401:
            print("   (401状态码正常 - 需要认证)")
            return True
        elif response.status_code == 200:
            print("   (200状态码 - API正常响应)")
            return True
        else:
            print(f"   警告: 意外的状态码 {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到后端服务器")
        return False
    except Exception as e:
        print(f"❌ 测试API时出现错误: {str(e)}")
        return False

def test_frontend_backend_integration():
    """测试前后端集成"""
    print("\n=== 测试前后端集成 ===")
    
    try:
        # 测试前端服务器
        frontend_url = "http://localhost:3001"
        
        response = requests.get(frontend_url, timeout=5)
        if response.status_code == 200:
            print("✅ 前端服务器运行正常")
        else:
            print(f"❌ 前端服务器状态异常: {response.status_code}")
            return False
        
        # 检查数据库中的师生关系
        relations_count = CoachStudentRelation.objects.count()
        print(f"✅ 数据库中现有师生关系数量: {relations_count}")
        
        return True
        
    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到前端服务器")
        return False
    except Exception as e:
        print(f"❌ 测试集成时出现错误: {str(e)}")
        return False

def main():
    """主测试函数"""
    print("开始测试选择教练功能修复...")
    print(f"测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    tests = [
        ("数据格式验证", test_coach_selection_data_format),
        ("API端点可访问性", test_api_endpoint_accessibility),
        ("前后端集成", test_frontend_backend_integration)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n{'='*50}")
        print(f"执行测试: {test_name}")
        result = test_func()
        results.append((test_name, result))
    
    # 输出测试结果摘要
    print(f"\n{'='*50}")
    print("测试结果摘要:")
    
    all_passed = True
    for test_name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"  {test_name}: {status}")
        if not result:
            all_passed = False
    
    if all_passed:
        print("\n🎉 所有测试通过！选择教练功能修复成功！")
        print("\n用户操作建议:")
        print("1. 访问前端页面: http://localhost:3001")
        print("2. 登录学员账户")
        print("3. 进入教练选择页面")
        print("4. 尝试选择一个教练")
        print("5. 检查是否成功创建师生关系")
    else:
        print("\n⚠️  部分测试失败，请检查相关问题")
    
    return all_passed

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)