#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
最终测试：验证选择教练功能完全修复
模拟前端实际使用场景
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
from accounts.models import Coach
from reservations.models import CoachStudentRelation

User = get_user_model()

class CoachSelectionFinalTest:
    """选择教练功能最终测试"""
    
    def __init__(self):
        self.client = APIClient()
        self.test_results = []
        
    def setup_test_user(self):
        """设置测试用户"""
        print("\n=== 设置测试用户 ===")
        
        # 获取现有学员用户
        try:
            self.student = User.objects.get(username='hhm')
            print(f"使用现有学员用户: {self.student.username} ({self.student.real_name})")
        except User.DoesNotExist:
            print("❌ 未找到测试学员用户")
            return False
            
        # 登录学员用户
        self.client.force_authenticate(user=self.student)
        print(f"✅ 学员用户登录成功")
        return True
    
    def test_get_coaches_api(self):
        """测试获取教练列表API"""
        print("\n=== 测试获取教练列表API ===")
        
        try:
            response = self.client.get('/accounts/api/coaches/')
            
            if response.status_code == 200:
                coaches_data = response.json()
                print(f"✅ 获取教练列表成功，共 {coaches_data.get('count', 0)} 个教练")
                
                coaches = coaches_data.get('results', [])
                if coaches:
                    first_coach = coaches[0]
                    print(f"第一个教练: {first_coach.get('real_name')} (ID: {first_coach.get('id')})")
                    return first_coach
                else:
                    print("❌ 教练列表为空")
                    return None
            else:
                print(f"❌ 获取教练列表失败: {response.status_code}")
                print(f"错误信息: {response.data}")
                return None
                
        except Exception as e:
            print(f"❌ 获取教练列表异常: {str(e)}")
            return None
    
    def test_select_coach(self, coach_data):
        """测试选择教练功能"""
        print("\n=== 测试选择教练功能 ===")
        
        if not coach_data:
            print("❌ 没有教练数据可供测试")
            return False
            
        coach_id = coach_data.get('id')
        coach_name = coach_data.get('real_name', '未知教练')
        
        print(f"尝试选择教练: {coach_name} (ID: {coach_id})")
        
        # 清理可能存在的关系
        try:
            existing_relations = CoachStudentRelation.objects.filter(
                student=self.student
            )
            if existing_relations.exists():
                print(f"清理现有关系: {existing_relations.count()} 个")
                existing_relations.delete()
        except Exception as e:
            print(f"清理关系时出错: {str(e)}")
        
        # 发送选择教练请求
        request_data = {
            'coach_id': coach_id,
            'notes': f'学员选择教练：{coach_name}'
        }
        
        try:
            response = self.client.post('/api/reservations/relations/', request_data)
            
            print(f"请求数据: {request_data}")
            print(f"响应状态码: {response.status_code}")
            
            if response.status_code == 201:
                response_data = response.json()
                print(f"✅ 选择教练成功")
                print(f"师生关系ID: {response_data.get('id')}")
                print(f"状态: {response_data.get('status')}")
                return True
            else:
                print(f"❌ 选择教练失败")
                print(f"错误信息: {response.data}")
                return False
                
        except Exception as e:
            print(f"❌ 选择教练异常: {str(e)}")
            return False
    
    def test_duplicate_selection(self, coach_data):
        """测试重复选择教练"""
        print("\n=== 测试重复选择教练 ===")
        
        if not coach_data:
            print("❌ 没有教练数据可供测试")
            return False
            
        coach_id = coach_data.get('id')
        coach_name = coach_data.get('real_name', '未知教练')
        
        request_data = {
            'coach_id': coach_id,
            'notes': f'重复选择教练：{coach_name}'
        }
        
        try:
            response = self.client.post('/api/reservations/relations/', request_data)
            
            print(f"请求数据: {request_data}")
            print(f"响应状态码: {response.status_code}")
            
            if response.status_code == 400:
                error_message = response.data
                print(f"✅ 正确拦截重复选择")
                print(f"错误信息: {error_message}")
                return True
            else:
                print(f"❌ 未正确拦截重复选择")
                print(f"响应数据: {response.data}")
                return False
                
        except Exception as e:
            print(f"❌ 测试重复选择异常: {str(e)}")
            return False
    
    def test_invalid_coach_id(self):
        """测试无效教练ID"""
        print("\n=== 测试无效教练ID ===")
        
        invalid_ids = [99999, 0, -1, 'invalid']
        
        for invalid_id in invalid_ids:
            print(f"\n测试无效ID: {invalid_id}")
            
            request_data = {
                'coach_id': invalid_id,
                'notes': f'测试无效教练ID：{invalid_id}'
            }
            
            try:
                response = self.client.post('/api/reservations/relations/', request_data)
                
                print(f"响应状态码: {response.status_code}")
                
                if response.status_code == 400:
                    error_message = response.data
                    print(f"✅ 正确拦截无效ID")
                    print(f"错误信息: {error_message}")
                else:
                    print(f"❌ 未正确拦截无效ID")
                    print(f"响应数据: {response.data}")
                    
            except Exception as e:
                print(f"测试无效ID异常: {str(e)}")
    
    def run_all_tests(self):
        """运行所有测试"""
        print("\n" + "="*50)
        print("选择教练功能最终测试")
        print("="*50)
        
        # 设置测试用户
        if not self.setup_test_user():
            print("\n❌ 测试用户设置失败，终止测试")
            return
        
        # 获取教练列表
        coach_data = self.test_get_coaches_api()
        
        # 测试选择教练
        if coach_data:
            success = self.test_select_coach(coach_data)
            
            if success:
                # 测试重复选择
                self.test_duplicate_selection(coach_data)
        
        # 测试无效教练ID
        self.test_invalid_coach_id()
        
        print("\n" + "="*50)
        print("测试完成")
        print("="*50)

def main():
    """主函数"""
    test = CoachSelectionFinalTest()
    test.run_all_tests()

if __name__ == '__main__':
    main()