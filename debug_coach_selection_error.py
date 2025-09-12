#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
调试选择教练功能错误
详细检查API请求和响应
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
from django.test import RequestFactory, Client
from django.contrib.auth.models import AnonymousUser
from rest_framework.test import APIClient
from django.contrib.auth import authenticate

User = get_user_model()

def test_api_with_authentication():
    """测试带认证的API请求"""
    print("\n=== 测试带认证的API请求 ===")
    
    try:
        # 获取测试用户
        student = User.objects.filter(user_type='student').first()
        coach = User.objects.filter(user_type='coach').first()
        
        if not student or not coach:
            print("❌ 缺少测试用户")
            return False
        
        print(f"✅ 学员: {student.username} (ID: {student.id})")
        print(f"✅ 教练: {coach.username} (ID: {coach.id})")
        
        # 使用APIClient进行测试
        client = APIClient()
        client.force_authenticate(user=student)
        
        # 测试POST请求
        data = {
            'coach_id': coach.id,
            'notes': f'学员选择教练：{coach.real_name}'
        }
        
        print(f"\n发送数据: {data}")
        
        response = client.post('/api/reservations/relations/', data, format='json')
        
        print(f"响应状态码: {response.status_code}")
        print(f"响应数据: {response.data}")
        
        if response.status_code == 201:
            print("✅ API请求成功")
            return True
        else:
            print(f"❌ API请求失败: {response.data}")
            return False
            
    except Exception as e:
        print(f"❌ 测试过程中出现错误: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_serializer_validation():
    """测试序列化器验证"""
    print("\n=== 测试序列化器验证 ===")
    
    try:
        student = User.objects.filter(user_type='student').first()
        coach = User.objects.filter(user_type='coach').first()
        
        if not student or not coach:
            print("❌ 缺少测试用户")
            return False
        
        # 创建模拟请求
        factory = RequestFactory()
        request = factory.post('/api/reservations/relations/')
        request.user = student
        
        # 测试数据
        test_cases = [
            {
                'name': '正确格式 - coach_id',
                'data': {
                    'coach_id': coach.id,
                    'notes': f'学员选择教练：{coach.real_name}'
                }
            },
            {
                'name': '错误格式 - coach',
                'data': {
                    'coach': coach.id,
                    'notes': f'学员选择教练：{coach.real_name}'
                }
            },
            {
                'name': '缺少coach_id',
                'data': {
                    'notes': f'学员选择教练：{coach.real_name}'
                }
            },
            {
                'name': '无效coach_id',
                'data': {
                    'coach_id': 99999,
                    'notes': f'学员选择教练：{coach.real_name}'
                }
            }
        ]
        
        for test_case in test_cases:
            print(f"\n测试: {test_case['name']}")
            print(f"数据: {test_case['data']}")
            
            serializer = CoachStudentRelationSerializer(
                data=test_case['data'],
                context={'request': request}
            )
            
            if serializer.is_valid():
                print("✅ 验证通过")
            else:
                print(f"❌ 验证失败: {serializer.errors}")
        
        return True
        
    except Exception as e:
        print(f"❌ 测试过程中出现错误: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def check_existing_relations():
    """检查现有师生关系"""
    print("\n=== 检查现有师生关系 ===")
    
    try:
        relations = CoachStudentRelation.objects.all()
        print(f"总关系数: {relations.count()}")
        
        for relation in relations[:5]:  # 只显示前5个
            print(f"ID: {relation.id}, 教练: {relation.coach.username}, 学员: {relation.student.username}, 状态: {relation.status}")
        
        return True
        
    except Exception as e:
        print(f"❌ 检查关系时出现错误: {str(e)}")
        return False

def test_duplicate_relation():
    """测试重复关系检查"""
    print("\n=== 测试重复关系检查 ===")
    
    try:
        student = User.objects.filter(user_type='student').first()
        coach = User.objects.filter(user_type='coach').first()
        
        if not student or not coach:
            print("❌ 缺少测试用户")
            return False
        
        # 检查是否已存在关系
        existing = CoachStudentRelation.objects.filter(
            coach=coach,
            student=student
        ).first()
        
        if existing:
            print(f"⚠️  已存在关系: ID={existing.id}, 状态={existing.status}")
            print("这可能是导致400错误的原因")
        else:
            print("✅ 不存在重复关系")
        
        return True
        
    except Exception as e:
        print(f"❌ 检查重复关系时出现错误: {str(e)}")
        return False

def main():
    """主测试函数"""
    print("开始调试选择教练功能错误...")
    print(f"调试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    tests = [
        ("检查现有师生关系", check_existing_relations),
        ("测试重复关系检查", test_duplicate_relation),
        ("测试序列化器验证", test_serializer_validation),
        ("测试带认证的API请求", test_api_with_authentication)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n{'='*50}")
        print(f"执行测试: {test_name}")
        result = test_func()
        results.append((test_name, result))
    
    # 输出测试结果摘要
    print(f"\n{'='*50}")
    print("调试结果摘要:")
    
    for test_name, result in results:
        status = "✅ 成功" if result else "❌ 失败"
        print(f"  {test_name}: {status}")
    
    print("\n💡 可能的问题原因:")
    print("1. 重复的师生关系申请")
    print("2. 用户认证问题")
    print("3. 数据验证失败")
    print("4. 权限检查失败")
    
    return True

if __name__ == '__main__':
    main()