#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试选择教练功能的错误处理
验证重复关系检查和友好错误消息
"""

import os
import sys
import django
from datetime import datetime

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'keshe.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
django.setup()

from django.contrib.auth import get_user_model
from reservations.models import CoachStudentRelation
from reservations.serializers import CoachStudentRelationSerializer
from rest_framework.test import APIClient
from django.test import RequestFactory

User = get_user_model()

def test_duplicate_relation_handling():
    """测试重复关系处理"""
    print("\n=== 测试重复关系处理 ===")
    
    try:
        # 获取测试用户
        student = User.objects.filter(user_type='student').first()
        coach = User.objects.filter(user_type='coach').first()
        
        if not student or not coach:
            print("❌ 缺少测试用户")
            return False
        
        print(f"✅ 学员: {student.username} (ID: {student.id})")
        print(f"✅ 教练: {coach.username} (ID: {coach.id})")
        
        # 清理现有关系
        CoachStudentRelation.objects.filter(
            coach=coach,
            student=student
        ).delete()
        print("✅ 清理现有关系")
        
        # 使用APIClient进行测试
        client = APIClient()
        client.force_authenticate(user=student)
        
        data = {
            'coach_id': coach.id,
            'notes': f'学员选择教练：{coach.real_name}'
        }
        
        # 第一次请求 - 应该成功
        print("\n第一次选择教练...")
        response1 = client.post('/api/reservations/relations/', data, format='json')
        print(f"响应状态码: {response1.status_code}")
        
        if response1.status_code == 201:
            print("✅ 第一次选择成功")
        else:
            print(f"❌ 第一次选择失败: {response1.data}")
            return False
        
        # 第二次请求 - 应该失败并返回友好错误消息
        print("\n第二次选择同一教练...")
        response2 = client.post('/api/reservations/relations/', data, format='json')
        print(f"响应状态码: {response2.status_code}")
        print(f"响应数据: {response2.data}")
        
        if response2.status_code == 400:
            error_msg = None
            if 'non_field_errors' in response2.data:
                error_msg = response2.data['non_field_errors'][0]
            
            if error_msg and '已经向该教练发送过申请' in str(error_msg):
                print("✅ 重复关系检查正常工作")
                print(f"✅ 友好错误消息: {error_msg}")
                return True
            else:
                print(f"❌ 错误消息不符合预期: {error_msg}")
                return False
        else:
            print(f"❌ 第二次请求应该返回400状态码")
            return False
            
    except Exception as e:
        print(f"❌ 测试过程中出现错误: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_different_relation_statuses():
    """测试不同关系状态的处理"""
    print("\n=== 测试不同关系状态处理 ===")
    
    try:
        student = User.objects.filter(user_type='student').first()
        coach = User.objects.filter(user_type='coach').first()
        
        if not student or not coach:
            print("❌ 缺少测试用户")
            return False
        
        client = APIClient()
        client.force_authenticate(user=student)
        
        data = {
            'coach_id': coach.id,
            'notes': f'学员选择教练：{coach.real_name}'
        }
        
        # 测试不同状态
        statuses = ['pending', 'approved', 'rejected']
        expected_messages = [
            '已经向该教练发送过申请',
            '已经选择过这位教练了',
            '已拒绝您的申请'
        ]
        
        for status, expected_msg in zip(statuses, expected_messages):
            print(f"\n测试状态: {status}")
            
            # 清理并创建指定状态的关系
            CoachStudentRelation.objects.filter(
                coach=coach,
                student=student
            ).delete()
            
            CoachStudentRelation.objects.create(
                coach=coach,
                student=student,
                status=status,
                applied_by='student',
                notes='测试关系'
            )
            
            # 尝试再次创建关系
            response = client.post('/api/reservations/relations/', data, format='json')
            
            if response.status_code == 400:
                error_msg = response.data.get('non_field_errors', [''])[0]
                if expected_msg in str(error_msg):
                    print(f"✅ {status}状态检查正常: {error_msg}")
                else:
                    print(f"❌ {status}状态错误消息不符合预期: {error_msg}")
                    return False
            else:
                print(f"❌ {status}状态应该返回400错误")
                return False
        
        return True
        
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
        
        # 清理现有关系
        CoachStudentRelation.objects.filter(
            coach=coach,
            student=student
        ).delete()
        
        # 创建模拟请求
        factory = RequestFactory()
        request = factory.post('/api/reservations/relations/')
        request.user = student
        
        # 测试正常情况
        data = {
            'coach_id': coach.id,
            'notes': f'学员选择教练：{coach.real_name}'
        }
        
        serializer = CoachStudentRelationSerializer(
            data=data,
            context={'request': request}
        )
        
        if serializer.is_valid():
            print("✅ 正常数据验证通过")
            
            # 创建关系
            relation = serializer.save()
            print(f"✅ 关系创建成功: {relation}")
            
            # 再次验证相同数据 - 应该失败
            serializer2 = CoachStudentRelationSerializer(
                data=data,
                context={'request': request}
            )
            
            if not serializer2.is_valid():
                error_msg = serializer2.errors.get('non_field_errors', [''])[0]
                print(f"✅ 重复关系验证失败（符合预期）: {error_msg}")
                return True
            else:
                print("❌ 重复关系验证应该失败")
                return False
        else:
            print(f"❌ 正常数据验证失败: {serializer.errors}")
            return False
            
    except Exception as e:
        print(f"❌ 测试过程中出现错误: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """主测试函数"""
    print("开始测试选择教练功能的错误处理...")
    print(f"测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    tests = [
        ("重复关系处理", test_duplicate_relation_handling),
        ("不同关系状态处理", test_different_relation_statuses),
        ("序列化器验证", test_serializer_validation)
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
        print("\n🎉 所有测试通过！错误处理功能正常工作！")
        print("\n修复内容:")
        print("1. ✅ 前端增强错误处理，提供友好的错误消息")
        print("2. ✅ 后端序列化器增加重复关系检查")
        print("3. ✅ 不同关系状态的友好错误提示")
        print("4. ✅ 400错误的详细分类处理")
        
        print("\n用户操作建议:")
        print("1. 访问前端页面: http://localhost:3001")
        print("2. 登录学员账户")
        print("3. 尝试选择同一个教练两次")
        print("4. 应该看到友好的错误提示")
    else:
        print("\n⚠️  部分测试失败，请检查相关问题")
    
    return all_passed

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)