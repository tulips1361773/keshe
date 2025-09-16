#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
调试"指定的教练不存在"错误
检查教练数据和验证逻辑
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

def check_coach_data():
    """检查教练数据"""
    print("\n=== 检查教练数据 ===")
    
    try:
        # 获取所有教练
        coaches = User.objects.filter(user_type='coach')
        print(f"数据库中教练总数: {coaches.count()}")
        
        if coaches.count() == 0:
            print("❌ 数据库中没有教练用户")
            return False
        
        print("\n教练列表:")
        for coach in coaches[:10]:  # 只显示前10个
            print(f"  ID: {coach.id}, 用户名: {coach.username}, 姓名: {coach.real_name}, 状态: {coach.is_active}")
        
        # 检查活跃教练
        active_coaches = coaches.filter(is_active=True)
        print(f"\n活跃教练数量: {active_coaches.count()}")
        
        if active_coaches.count() == 0:
            print("❌ 没有活跃的教练用户")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ 检查教练数据时出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def check_student_data():
    """检查学员数据"""
    print("\n=== 检查学员数据 ===")
    
    try:
        # 获取所有学员
        students = User.objects.filter(user_type='student')
        print(f"数据库中学员总数: {students.count()}")
        
        if students.count() == 0:
            print("❌ 数据库中没有学员用户")
            return False
        
        print("\n学员列表:")
        for student in students[:5]:  # 只显示前5个
            print(f"  ID: {student.id}, 用户名: {student.username}, 姓名: {student.real_name}, 状态: {student.is_active}")
        
        # 检查活跃学员
        active_students = students.filter(is_active=True)
        print(f"\n活跃学员数量: {active_students.count()}")
        
        return True
        
    except Exception as e:
        print(f"❌ 检查学员数据时出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_coach_validation():
    """测试教练验证逻辑"""
    print("\n=== 测试教练验证逻辑 ===")
    
    try:
        student = User.objects.filter(user_type='student', is_active=True).first()
        coach = User.objects.filter(user_type='coach', is_active=True).first()
        
        if not student:
            print("❌ 没有可用的学员用户")
            return False
        
        if not coach:
            print("❌ 没有可用的教练用户")
            return False
        
        print(f"测试学员: {student.username} (ID: {student.id})")
        print(f"测试教练: {coach.username} (ID: {coach.id})")
        
        # 创建模拟请求
        factory = RequestFactory()
        request = factory.post('/api/reservations/relations/')
        request.user = student
        
        # 测试有效的教练ID
        print("\n测试有效的教练ID...")
        data = {
            'coach_id': coach.id,
            'notes': f'学员选择教练：{coach.real_name}'
        }
        
        serializer = CoachStudentRelationSerializer(
            data=data,
            context={'request': request}
        )
        
        if serializer.is_valid():
            print("✅ 有效教练ID验证通过")
        else:
            print(f"❌ 有效教练ID验证失败: {serializer.errors}")
            return False
        
        # 测试无效的教练ID
        print("\n测试无效的教练ID...")
        invalid_data = {
            'coach_id': 99999,  # 不存在的ID
            'notes': '测试无效教练ID'
        }
        
        invalid_serializer = CoachStudentRelationSerializer(
            data=invalid_data,
            context={'request': request}
        )
        
        if not invalid_serializer.is_valid():
            error_msg = invalid_serializer.errors.get('non_field_errors', [''])[0]
            print(f"✅ 无效教练ID验证失败（符合预期）: {error_msg}")
            
            if '指定的教练不存在' in str(error_msg):
                print("✅ 错误消息正确")
                return True
            else:
                print(f"❌ 错误消息不符合预期: {error_msg}")
                return False
        else:
            print("❌ 无效教练ID应该验证失败")
            return False
            
    except Exception as e:
        print(f"❌ 测试教练验证时出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_api_request():
    """测试API请求"""
    print("\n=== 测试API请求 ===")
    
    try:
        student = User.objects.filter(user_type='student', is_active=True).first()
        coach = User.objects.filter(user_type='coach', is_active=True).first()
        
        if not student or not coach:
            print("❌ 缺少测试用户")
            return False
        
        client = APIClient()
        client.force_authenticate(user=student)
        
        # 清理现有关系
        CoachStudentRelation.objects.filter(
            coach=coach,
            student=student
        ).delete()
        
        # 测试有效请求
        print(f"\n测试选择教练 ID: {coach.id}")
        data = {
            'coach_id': coach.id,
            'notes': f'学员选择教练：{coach.real_name}'
        }
        
        response = client.post('/api/reservations/relations/', data, format='json')
        print(f"响应状态码: {response.status_code}")
        print(f"响应数据: {response.data}")
        
        if response.status_code == 201:
            print("✅ 有效请求成功")
        else:
            print(f"❌ 有效请求失败")
            return False
        
        # 测试无效教练ID请求
        print("\n测试无效教练ID请求...")
        invalid_data = {
            'coach_id': 99999,
            'notes': '测试无效教练ID'
        }
        
        invalid_response = client.post('/api/reservations/relations/', invalid_data, format='json')
        print(f"响应状态码: {invalid_response.status_code}")
        print(f"响应数据: {invalid_response.data}")
        
        if invalid_response.status_code == 400:
            error_msg = invalid_response.data.get('non_field_errors', [''])[0]
            if '指定的教练不存在' in str(error_msg):
                print("✅ 无效教练ID请求正确返回错误")
                return True
            else:
                print(f"❌ 错误消息不符合预期: {error_msg}")
                return False
        else:
            print(f"❌ 无效教练ID请求应该返回400错误")
            return False
            
    except Exception as e:
        print(f"❌ 测试API请求时出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def check_frontend_request_data():
    """检查前端可能发送的数据格式"""
    print("\n=== 检查前端请求数据格式 ===")
    
    try:
        student = User.objects.filter(user_type='student', is_active=True).first()
        
        if not student:
            print("❌ 没有可用的学员用户")
            return False
        
        client = APIClient()
        client.force_authenticate(user=student)
        
        # 测试可能的错误数据格式
        test_cases = [
            {'coach_id': None, 'notes': '测试null值'},
            {'coach_id': '', 'notes': '测试空字符串'},
            {'coach_id': 'invalid', 'notes': '测试非数字字符串'},
            {'coach_id': 0, 'notes': '测试0值'},
            {'coach_id': -1, 'notes': '测试负数'},
        ]
        
        for i, test_data in enumerate(test_cases, 1):
            print(f"\n测试用例 {i}: {test_data}")
            response = client.post('/api/reservations/relations/', test_data, format='json')
            print(f"  状态码: {response.status_code}")
            print(f"  响应: {response.data}")
        
        return True
        
    except Exception as e:
        print(f"❌ 检查前端请求数据时出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """主函数"""
    print("开始调试'指定的教练不存在'错误...")
    print(f"调试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    tests = [
        ("检查教练数据", check_coach_data),
        ("检查学员数据", check_student_data),
        ("测试教练验证逻辑", test_coach_validation),
        ("测试API请求", test_api_request),
        ("检查前端请求数据格式", check_frontend_request_data)
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
    
    all_passed = True
    for test_name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"  {test_name}: {status}")
        if not result:
            all_passed = False
    
    if all_passed:
        print("\n✅ 所有检查通过，教练验证逻辑正常")
        print("\n可能的问题原因:")
        print("1. 前端发送的coach_id格式不正确")
        print("2. 前端发送的coach_id对应的教练不存在或不活跃")
        print("3. 网络请求中数据丢失或格式错误")
        print("4. 前端JavaScript代码中的数据处理问题")
    else:
        print("\n⚠️  发现问题，请检查相关配置")
    
    return all_passed

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)