#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
教练员查询与选择功能 - 后端API接口测试

测试范围：
1. 教练员列表查询API
2. 教练员筛选和搜索API
3. 师生关系创建和管理API
4. 权限验证和错误处理
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

from django.test import TestCase, Client
from django.contrib.auth.models import Group
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from accounts.models import User, Coach, UserProfile
from reservations.models import CoachStudentRelation
from campus.models import Campus

class CoachSelectionBackendTest:
    """教练员选择功能后端测试类"""
    
    def __init__(self):
        self.client = APIClient()
        self.test_results = []
        self.setup_test_data()
    
    def setup_test_data(self):
        """设置测试数据"""
        print("\n=== 设置测试数据 ===")
        
        # 创建用户组
        student_group, _ = Group.objects.get_or_create(name='学员')
        coach_group, _ = Group.objects.get_or_create(name='教练员')
        
        # 创建校区
        self.campus = Campus.objects.get_or_create(
            name='测试校区',
            defaults={
                'address': '测试地址',
                'phone': '12345678901',
                'description': '测试校区描述'
            }
        )[0]
        
        # 创建测试学员
        # 清理测试数据
        User.objects.filter(username__contains='test').delete()
        User.objects.filter(username__in=['coach1', 'coach2', 'coach3']).delete()
        User.objects.filter(phone__startswith='138001380').delete()
        
        self.student_user = User.objects.create(
            username='backend_test_student',
            email='backend_student@test.com',
            first_name='后端',
            last_name='测试学员',
            real_name='后端测试学员',
            phone='13800138001',
            gender='male',
            user_type='student'
        )
        self.student_user.groups.add(student_group)
        
        # 创建测试教练员
        self.coaches = []
        coach_data = [
            {'username': 'coach1', 'real_name': '张教练', 'gender': 'male', 'age': 30, 'level': 'senior', 'phone': '13800138002'},
            {'username': 'coach2', 'real_name': '李教练', 'gender': 'female', 'age': 28, 'level': 'intermediate', 'phone': '13800138003'},
            {'username': 'coach3', 'real_name': '王教练', 'gender': 'male', 'age': 35, 'level': 'junior', 'phone': '13800138004'},
        ]
        
        for data in coach_data:
            # 创建用户
            coach_user = User.objects.create(
                username=data['username'],
                email=f"{data['username']}@test.com",
                first_name=data['real_name'][:1],
                last_name=data['real_name'][1:],
                phone=data['phone'],
                real_name=data['real_name'],
                gender=data['gender'],
                user_type='coach'
            )
            coach_user.set_password('testpass123')
            coach_user.save()
            coach_user.groups.add(coach_group)
            
            # 教练员信息已在User模型中设置，无需单独的UserProfile
            
            # 创建教练档案
            coach, _ = Coach.objects.get_or_create(
                user=coach_user,
                defaults={
                    'coach_level': data['level'],
                    'achievements': '乒乓球基础训练',  # 使用achievements字段存储专长
                    'status': 'approved'
                }
            )
            
            self.coaches.append(coach)
        
        print(f"创建了 {len(self.coaches)} 个测试教练员")
        print(f"创建了测试学员: {self.student_user.username}")
    
    def authenticate_as_student(self):
        """以学员身份认证"""
        self.client.force_authenticate(user=self.student_user)
    
    def log_test_result(self, test_name, success, message, details=None):
        """记录测试结果"""
        result = {
            'test_name': test_name,
            'success': success,
            'message': message,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'details': details or {}
        }
        self.test_results.append(result)
        
        status_icon = "✅" if success else "❌"
        print(f"{status_icon} {test_name}: {message}")
        if details:
            for key, value in details.items():
                print(f"   {key}: {value}")
    
    def test_coach_list_api(self):
        """测试教练员列表API"""
        print("\n=== 测试教练员列表API ===")
        
        self.authenticate_as_student()
        
        try:
            # 测试基本列表查询
            response = self.client.get('/accounts/api/coaches/')
            
            if response.status_code == 200:
                data = response.json()
                coach_count = len(data.get('results', []))
                
                self.log_test_result(
                    "教练员列表基本查询",
                    True,
                    f"成功获取教练员列表，共 {coach_count} 个教练员",
                    {
                        "状态码": response.status_code,
                        "教练员数量": coach_count,
                        "响应字段": list(data.keys()) if data else []
                    }
                )
            else:
                self.log_test_result(
                    "教练员列表基本查询",
                    False,
                    f"API调用失败，状态码: {response.status_code}",
                    {"响应内容": response.content.decode()}
                )
        
        except Exception as e:
            self.log_test_result(
                "教练员列表基本查询",
                False,
                f"测试异常: {str(e)}"
            )
    
    def test_coach_filter_api(self):
        """测试教练员筛选和搜索API"""
        print("\n=== 测试教练员筛选和搜索API ===")
        
        self.authenticate_as_student()
        
        # 测试用例
        test_cases = [
            {
                'name': '按姓名搜索',
                'params': {'search': '张'},
                'expected_count': 1
            },
            {
                'name': '按性别筛选',
                'params': {'gender': 'male'},
                'expected_count': 3
            },
            {
                'name': '按等级筛选',
                'params': {'level': 'senior'},
                'expected_count': 1
            },
            {
                'name': '组合筛选',
                'params': {'gender': 'male', 'search': '王'},
                'expected_count': 1
            },
            {
                'name': '分页测试',
                'params': {'page': 1, 'page_size': 2},
                'expected_count': 2
            }
        ]
        
        for case in test_cases:
            try:
                response = self.client.get('/accounts/api/coaches/', case['params'])
                
                if response.status_code == 200:
                    data = response.json()
                    results = data.get('results', [])
                    actual_count = len(results)
                    
                    success = actual_count == case['expected_count']
                    message = f"预期 {case['expected_count']} 个结果，实际 {actual_count} 个"
                    
                    self.log_test_result(
                        case['name'],
                        success,
                        message,
                        {
                            "查询参数": case['params'],
                            "状态码": response.status_code,
                            "结果数量": actual_count
                        }
                    )
                else:
                    self.log_test_result(
                        case['name'],
                        False,
                        f"API调用失败，状态码: {response.status_code}",
                        {"查询参数": case['params']}
                    )
            
            except Exception as e:
                self.log_test_result(
                    case['name'],
                    False,
                    f"测试异常: {str(e)}",
                    {"查询参数": case['params']}
                )
    
    def test_coach_student_relation_api(self):
        """测试师生关系创建和管理API"""
        print("\n=== 测试师生关系创建和管理API ===")
        
        self.authenticate_as_student()
        
        if not self.coaches:
            self.log_test_result(
                "师生关系测试",
                False,
                "没有可用的测试教练员"
            )
            return
        
        test_coach = self.coaches[0]
        
        try:
            # 测试创建师生关系
            relation_data = {
                'coach_id': test_coach.user.id,
                'notes': '测试选择教练'
            }
            
            response = self.client.post(
                '/api/reservations/relations/', 
                data=json.dumps(relation_data),
                content_type='application/json'
            )
            
            if response.status_code in [200, 201]:
                self.log_test_result(
                        "创建师生关系",
                        True,
                        "成功创建师生关系",
                        {
                            "状态码": response.status_code,
                            "教练员": test_coach.user.real_name,
                            "响应数据": response.json() if response.content else "无内容"
                        }
                    )
                
                # 测试查询师生关系
                response = self.client.get('/api/reservations/relations/')
                
                if response.status_code == 200:
                    relations = response.json()
                    relation_count = len(relations) if isinstance(relations, list) else 0
                    
                    self.log_test_result(
                        "查询师生关系",
                        True,
                        f"成功查询师生关系，共 {relation_count} 条记录",
                        {
                            "状态码": response.status_code,
                            "关系数量": relation_count
                        }
                    )
                else:
                    self.log_test_result(
                        "查询师生关系",
                        False,
                        f"查询失败，状态码: {response.status_code}"
                    )
            
            else:
                self.log_test_result(
                    "创建师生关系",
                    False,
                    f"创建失败，状态码: {response.status_code}",
                    {"响应内容": response.content.decode()}
                )
        
        except Exception as e:
            self.log_test_result(
                "师生关系API测试",
                False,
                f"测试异常: {str(e)}"
            )
    
    def test_authentication_and_permissions(self):
        """测试认证和权限"""
        print("\n=== 测试认证和权限 ===")
        
        # 测试未认证访问
        self.client.force_authenticate(user=None)
        
        try:
            response = self.client.get('/accounts/api/coaches/')
            
            if response.status_code in [401, 403]:
                self.log_test_result(
                    "未认证访问控制",
                    True,
                    f"正确拒绝未认证用户访问，状态码: {response.status_code}",
                    {"状态码": response.status_code}
                )
            else:
                self.log_test_result(
                    "未认证访问控制",
                    False,
                    f"未正确拒绝未认证访问，状态码: {response.status_code}"
                )
        
        except Exception as e:
            self.log_test_result(
                "认证测试",
                False,
                f"测试异常: {str(e)}"
            )
    
    def run_all_tests(self):
        """运行所有测试"""
        print("\n" + "="*50)
        print("教练员查询与选择功能 - 后端API接口测试")
        print("="*50)
        
        # 运行各项测试
        self.test_coach_list_api()
        self.test_coach_filter_api()
        self.test_coach_student_relation_api()
        self.test_authentication_and_permissions()
        
        # 生成测试报告
        self.generate_test_report()
    
    def generate_test_report(self):
        """生成测试报告"""
        print("\n" + "="*50)
        print("测试报告")
        print("="*50)
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result['success'])
        failed_tests = total_tests - passed_tests
        
        print(f"\n总测试数: {total_tests}")
        print(f"通过: {passed_tests}")
        print(f"失败: {failed_tests}")
        print(f"通过率: {(passed_tests/total_tests*100):.1f}%" if total_tests > 0 else "通过率: 0%")
        
        if failed_tests > 0:
            print("\n失败的测试:")
            for result in self.test_results:
                if not result['success']:
                    print(f"  ❌ {result['test_name']}: {result['message']}")
        
        # 保存详细报告到文件
        report_file = 'test_coach_selection_backend_report.json'
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump({
                'summary': {
                    'total_tests': total_tests,
                    'passed_tests': passed_tests,
                    'failed_tests': failed_tests,
                    'pass_rate': f"{(passed_tests/total_tests*100):.1f}%" if total_tests > 0 else "0%",
                    'test_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                },
                'detailed_results': self.test_results
            }, f, ensure_ascii=False, indent=2)
        
        print(f"\n详细测试报告已保存到: {report_file}")

def main():
    """主函数"""
    try:
        tester = CoachSelectionBackendTest()
        tester.run_all_tests()
    except Exception as e:
        print(f"测试运行异常: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()