#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
检查教练API返回的数据结构
"""

import os
import sys
import django
import json
from datetime import datetime

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'keshe.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
django.setup()

from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from accounts.serializers import CoachSerializer

User = get_user_model()

def check_coach_api_response():
    """检查教练API返回的数据结构"""
    print("=== 检查教练API返回的数据结构 ===")
    
    try:
        # 获取一个学员用户进行测试
        student = User.objects.filter(user_type='student', is_active=True).first()
        if not student:
            print("❌ 没有可用的学员用户")
            return False
        
        print(f"使用学员用户: {student.username} (ID: {student.id})")
        
        # 创建API客户端
        client = APIClient()
        client.force_authenticate(user=student)
        
        # 请求教练列表
        response = client.get('/accounts/api/coaches/')
        print(f"\nAPI响应状态码: {response.status_code}")
        
        if response.status_code == 200:
            data = response.data
            print(f"响应数据类型: {type(data)}")
            print(f"响应数据键: {list(data.keys()) if isinstance(data, dict) else 'Not a dict'}")
            
            if 'results' in data and data['results']:
                coach_data = data['results'][0]
                print(f"\n第一个教练数据结构:")
                print(json.dumps(coach_data, indent=2, ensure_ascii=False, default=str))
                
                # 检查ID字段
                print(f"\n教练ID字段分析:")
                print(f"  id: {coach_data.get('id')}")
                print(f"  user_id: {coach_data.get('user_id')}")
                print(f"  pk: {coach_data.get('pk')}")
                
                return True
            else:
                print("❌ 没有教练数据")
                return False
        else:
            print(f"❌ API请求失败: {response.data}")
            return False
            
    except Exception as e:
        print(f"❌ 检查API响应时出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def check_coach_serializer():
    """检查教练序列化器"""
    print("\n=== 检查教练序列化器 ===")
    
    try:
        # 获取一个教练用户
        coach = User.objects.filter(user_type='coach', is_active=True).first()
        if not coach:
            print("❌ 没有可用的教练用户")
            return False
        
        print(f"使用教练用户: {coach.username} (ID: {coach.id})")
        
        # 使用序列化器
        serializer = CoachSerializer(coach)
        serialized_data = serializer.data
        
        print(f"\n序列化后的教练数据:")
        print(json.dumps(serialized_data, indent=2, ensure_ascii=False, default=str))
        
        # 检查ID字段
        print(f"\n序列化器ID字段分析:")
        print(f"  id: {serialized_data.get('id')}")
        print(f"  user_id: {serialized_data.get('user_id')}")
        print(f"  pk: {serialized_data.get('pk')}")
        
        return True
        
    except Exception as e:
        print(f"❌ 检查序列化器时出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_coach_selection_with_correct_id():
    """使用正确的ID测试选择教练"""
    print("\n=== 使用正确的ID测试选择教练 ===")
    
    try:
        student = User.objects.filter(user_type='student', is_active=True).first()
        coach = User.objects.filter(user_type='coach', is_active=True).first()
        
        if not student or not coach:
            print("❌ 缺少测试用户")
            return False
        
        client = APIClient()
        client.force_authenticate(user=student)
        
        # 先获取教练数据
        coaches_response = client.get('/accounts/api/coaches/')
        if coaches_response.status_code == 200 and coaches_response.data.get('results'):
            coach_from_api = coaches_response.data['results'][0]
            coach_id = coach_from_api.get('id') or coach_from_api.get('user_id')
            
            print(f"从API获取的教练ID: {coach_id}")
            print(f"教练数据: {coach_from_api.get('real_name')} ({coach_from_api.get('username')})")
            
            # 清理现有关系
            from reservations.models import CoachStudentRelation
            CoachStudentRelation.objects.filter(
                coach_id=coach_id,
                student=student
            ).delete()
            
            # 测试选择教练
            data = {
                'coach_id': coach_id,
                'notes': f'学员选择教练：{coach_from_api.get("real_name")}'
            }
            
            print(f"\n发送选择教练请求: {data}")
            response = client.post('/api/reservations/relations/', data, format='json')
            print(f"响应状态码: {response.status_code}")
            print(f"响应数据: {response.data}")
            
            if response.status_code == 201:
                print("✅ 选择教练成功")
                return True
            else:
                print(f"❌ 选择教练失败")
                return False
        else:
            print("❌ 无法获取教练数据")
            return False
            
    except Exception as e:
        print(f"❌ 测试选择教练时出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """主函数"""
    print("开始检查教练API数据结构...")
    print(f"检查时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    tests = [
        ("检查教练API响应", check_coach_api_response),
        ("检查教练序列化器", check_coach_serializer),
        ("测试正确ID选择教练", test_coach_selection_with_correct_id)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n{'='*50}")
        print(f"执行: {test_name}")
        result = test_func()
        results.append((test_name, result))
    
    # 输出结果摘要
    print(f"\n{'='*50}")
    print("检查结果摘要:")
    
    all_passed = True
    for test_name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"  {test_name}: {status}")
        if not result:
            all_passed = False
    
    if all_passed:
        print("\n✅ 所有检查通过")
    else:
        print("\n⚠️  发现问题，需要修复")
    
    return all_passed

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)