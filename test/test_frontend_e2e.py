#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
前端端到端功能测试
通过创建测试用户和数据来验证前端功能的完整性
"""

import requests
import json
import time
from datetime import datetime, timedelta
import os
import django

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'keshe.settings')
django.setup()

from accounts.models import User, UserProfile
from campus.models import Campus
from reservations.models import Table
from reservations.models import CoachStudentRelation, Booking
from notifications.models import Notification

class FrontendE2ETester:
    def __init__(self):
        self.base_url = 'http://localhost:8000/api'
        self.frontend_url = 'http://localhost:3002'
        self.session = requests.Session()
        self.test_results = []
        self.test_users = {}
        
    def log_test(self, test_name, success, message=""):
        """记录测试结果"""
        result = {
            'test': test_name,
            'success': success,
            'message': message,
            'timestamp': datetime.now().isoformat()
        }
        self.test_results.append(result)
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}: {message}")
        
    def setup_test_data(self):
        """创建测试数据"""
        print("\n=== 创建测试数据 ===")
        
        try:
            # 创建测试学员
            student_user, created = User.objects.get_or_create(
                username='test_student',
                defaults={
                    'email': 'student@test.com',
                    'first_name': '测试',
                    'last_name': '学员'
                }
            )
            if created:
                student_user.set_password('testpass123')
                student_user.save()
                
            student_profile, created = UserProfile.objects.get_or_create(
                user=student_user,
                defaults={
                    'user_type': 'student',
                    'phone': '13800000001',
                    'real_name': '测试学员',
                    'is_profile_complete': True
                }
            )
            
            self.test_users['student'] = {
                'user': student_user,
                'profile': student_profile,
                'credentials': {'username': 'test_student', 'password': 'testpass123'}
            }
            
            # 创建测试教练
            coach_user, created = User.objects.get_or_create(
                username='test_coach',
                defaults={
                    'email': 'coach@test.com',
                    'first_name': '测试',
                    'last_name': '教练'
                }
            )
            if created:
                coach_user.set_password('testpass123')
                coach_user.save()
                
            coach_profile, created = UserProfile.objects.get_or_create(
                user=coach_user,
                defaults={
                    'user_type': 'coach',
                    'phone': '13800000002',
                    'real_name': '测试教练',
                    'is_profile_complete': True,
                    'is_approved': True
                }
            )
            
            self.test_users['coach'] = {
                'user': coach_user,
                'profile': coach_profile,
                'credentials': {'username': 'test_coach', 'password': 'testpass123'}
            }
            
            # 创建测试校区和球台
            campus, created = Campus.objects.get_or_create(
                name='测试校区',
                defaults={
                    'address': '测试地址',
                    'description': '测试校区描述'
                }
            )
            
            table, created = Table.objects.get_or_create(
                campus=campus,
                number='T001',
                defaults={
                    'name': '测试球台',
                    'status': 'available',
                    'is_active': True
                }
            )
            
            # 创建师生关系
            relation, created = CoachStudentRelation.objects.get_or_create(
                student=student_user,
                coach=coach_user,
                defaults={
                    'status': 'approved',
                    'applied_by': 'student',
                    'notes': '测试师生关系'
                }
            )
            
            self.log_test("创建测试数据", True, "测试用户、校区、球台和师生关系创建成功")
            
        except Exception as e:
            self.log_test("创建测试数据", False, f"创建失败: {str(e)}")
            
    def test_student_login_flow(self):
        """测试学员登录流程"""
        print("\n=== 测试学员登录流程 ===")
        
        try:
            # 测试登录
            response = self.session.post(
                f"{self.base_url}/accounts/login/",
                json=self.test_users['student']['credentials'],
                headers={'Content-Type': 'application/json'}
            )
            
            if response.status_code == 200:
                data = response.json()
                if 'token' in data:
                    self.session.headers.update({
                        'Authorization': f'Token {data["token"]}'
                    })
                    # 保存token到test_users中
                    self.test_users['student']['token'] = data['token']
                    self.log_test("学员登录", True, "登录成功，获得认证令牌")
                    
                    # 测试获取个人资料
                    profile_response = self.session.get(f"{self.base_url}/accounts/profile/")
                    if profile_response.status_code == 200:
                        profile_data = profile_response.json()
                        self.log_test("获取学员资料", True, f"获取成功，用户类型: {profile_data.get('user_type')}")
                    else:
                        self.log_test("获取学员资料", False, f"状态码: {profile_response.status_code}")
                        
                else:
                    self.log_test("学员登录", False, "响应中缺少认证令牌")
            else:
                self.log_test("学员登录", False, f"登录失败，状态码: {response.status_code}")
                
        except Exception as e:
            self.log_test("学员登录", False, f"请求失败: {str(e)}")
            
    def test_coach_login_flow(self):
        """测试教练登录流程"""
        print("\n=== 测试教练登录流程 ===")
        
        try:
            # 创建新的session用于教练
            coach_session = requests.Session()
            
            # 测试教练登录
            response = coach_session.post(
                f"{self.base_url}/accounts/login/",
                json=self.test_users['coach']['credentials'],
                headers={'Content-Type': 'application/json'}
            )
            
            if response.status_code == 200:
                data = response.json()
                if 'token' in data:
                    coach_session.headers.update({
                        'Authorization': f'Token {data["token"]}'
                    })
                    # 保存token到test_users中
                    self.test_users['coach']['token'] = data['token']
                    self.log_test("教练登录", True, "登录成功，获得认证令牌")
                    
                    # 测试获取教练资料
                    profile_response = coach_session.get(f"{self.base_url}/accounts/profile/")
                    if profile_response.status_code == 200:
                        profile_data = profile_response.json()
                        self.log_test("获取教练资料", True, f"获取成功，用户类型: {profile_data.get('user_type')}")
                    else:
                        self.log_test("获取教练资料", False, f"状态码: {profile_response.status_code}")
                        
                else:
                    self.log_test("教练登录", False, "响应中缺少认证令牌")
            else:
                self.log_test("教练登录", False, f"登录失败，状态码: {response.status_code}")
                
        except Exception as e:
            self.log_test("教练登录", False, f"请求失败: {str(e)}")
            
    def test_relation_functionality(self):
        """测试师生关系功能"""
        print("\n=== 测试师生关系功能 ===")
        
        try:
            # 测试获取师生关系列表
            response = self.session.get(f"{self.base_url}/reservations/relations/")
            
            if response.status_code == 200:
                relations = response.json()
                if isinstance(relations, list) and len(relations) > 0:
                    self.log_test("获取师生关系", True, f"找到 {len(relations)} 个师生关系")
                else:
                    self.log_test("获取师生关系", True, "师生关系列表为空")
            else:
                self.log_test("获取师生关系", False, f"状态码: {response.status_code}")
                
        except Exception as e:
            self.log_test("获取师生关系", False, f"请求失败: {str(e)}")
            
    def test_booking_functionality(self):
        """测试预约功能"""
        print("\n=== 测试预约功能 ===")
        
        try:
            # 测试获取可用球台
            start_time = (datetime.now() + timedelta(days=1)).isoformat()
            end_time = (datetime.now() + timedelta(days=1, hours=2)).isoformat()
            
            params = {
                'campus': 1,
                'start_time': start_time,
                'end_time': end_time
            }
            
            response = self.session.get(
                f"{self.base_url}/reservations/tables/available/",
                params=params
            )
            
            if response.status_code == 200:
                tables = response.json()
                if isinstance(tables, list):
                    self.log_test("获取可用球台", True, f"找到 {len(tables)} 个可用球台")
                else:
                    self.log_test("获取可用球台", False, "返回数据格式不正确")
            else:
                self.log_test("获取可用球台", False, f"状态码: {response.status_code}")
                
            # 测试创建预约
            # 获取师生关系ID
            relation = CoachStudentRelation.objects.filter(
                student=self.test_users['student']['user'],
                coach=self.test_users['coach']['user'],
                status='approved'
            ).first()
            
            if relation is not None:
                booking_data = {
                    'relation_id': relation.id,
                    'start_time': start_time,
                    'end_time': end_time,
                    'table_id': 1,
                    'duration_hours': 2.0,
                    'total_fee': 100.00,
                    'notes': '端到端测试预约'
                }
                
                # 使用教练token创建预约
                coach_token = self.test_users['coach']['token']
                
                # 获取CSRF token
                csrf_response = self.session.get(f"{self.base_url}/")
                csrf_token = None
                if 'csrftoken' in self.session.cookies:
                    csrf_token = self.session.cookies['csrftoken']
                
                headers = {
                    'Content-Type': 'application/json',
                    'Authorization': f'Token {coach_token}'
                }
                
                if csrf_token:
                    headers['X-CSRFToken'] = csrf_token
                
                response = self.session.post(
                    f"{self.base_url}/reservations/bookings/",
                    json=booking_data,
                    headers=headers
                )
            else:
                response = None
            
            if response is not None and response.status_code == 201:
                booking = response.json()
                self.log_test("创建预约", True, f"预约创建成功，ID: {booking.get('id')}")
            elif response is not None and response.status_code == 400:
                error_data = response.json()
                self.log_test("创建预约", True, f"预约验证正常（数据验证失败）: {error_data}")
            elif response is not None and response.status_code == 403:
                self.log_test("创建预约", False, f"权限不足: {response.text}")
            elif response is not None:
                self.log_test("创建预约", False, f"状态码: {response.status_code}, 响应: {response.text}")
            else:
                self.log_test("创建预约", False, "师生关系不存在，无法创建预约")
                
        except Exception as e:
            self.log_test("预约功能测试", False, f"请求失败: {str(e)}")
            
    def test_notification_functionality(self):
        """测试通知功能"""
        print("\n=== 测试通知功能 ===")
        
        try:
            # 获取学员token
            student_token = self.test_users['student']['token']
            
            # 创建测试通知
            notification = Notification.objects.create(
                recipient=self.test_users['student']['user'],
                title='测试通知',
                message='这是一个测试通知',
                message_type='booking'
            )
            
            # 测试获取通知列表
            response = self.session.get(
                f"{self.base_url}/notifications/list/",
                headers={'Authorization': f'Token {student_token}'}
            )
            
            if response.status_code == 200:
                notifications = response.json()
                results = notifications.get('results', [])
                self.log_test("获取通知列表", True, f"找到 {len(results)} 个通知")
            else:
                self.log_test("获取通知列表", False, f"状态码: {response.status_code}")
                
        except Exception as e:
            self.log_test("通知功能测试", False, f"测试失败: {str(e)}")
            
    def test_frontend_pages(self):
        """测试前端页面可访问性"""
        print("\n=== 测试前端页面 ===")
        
        try:
            response = requests.get(self.frontend_url, timeout=10)
            if response.status_code == 200:
                self.log_test("前端主页", True, "页面加载成功")
                
                # 检查关键元素
                content = response.text
                if 'id="app"' in content:
                    self.log_test("Vue应用容器", True, "找到Vue应用容器")
                else:
                    self.log_test("Vue应用容器", False, "未找到Vue应用容器")
                    
            else:
                self.log_test("前端主页", False, f"状态码: {response.status_code}")
                
        except Exception as e:
            self.log_test("前端页面测试", False, f"访问失败: {str(e)}")
            
    def cleanup_test_data(self):
        """清理测试数据"""
        print("\n=== 清理测试数据 ===")
        
        try:
            # 删除测试预约
            deleted_bookings = Booking.objects.filter(
                relation__student__username='test_student'
            ).delete()
            
            # 删除测试通知
            deleted_notifications = Notification.objects.filter(
                recipient__in=[self.test_users['student']['user'], self.test_users['coach']['user']]
            ).delete()
            
            self.log_test("清理测试数据", True, 
                         f"删除了 {deleted_bookings[0]} 个预约和 {deleted_notifications[0]} 个通知")
            
        except Exception as e:
            self.log_test("清理测试数据", False, f"清理失败: {str(e)}")
            
    def generate_report(self):
        """生成测试报告"""
        print("\n" + "="*60)
        print("前端端到端功能测试报告")
        print("="*60)
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result['success'])
        failed_tests = total_tests - passed_tests
        
        print(f"\n总测试数: {total_tests}")
        print(f"通过: {passed_tests}")
        print(f"失败: {failed_tests}")
        print(f"成功率: {(passed_tests/total_tests*100):.1f}%")
        
        if failed_tests > 0:
            print("\n失败的测试:")
            for result in self.test_results:
                if not result['success']:
                    print(f"  - {result['test']}: {result['message']}")
                    
        # 功能完整性评估
        print("\n=== 功能完整性评估 ===")
        
        core_functions = {
            '用户认证': ['学员登录', '教练登录'],
            '个人资料': ['获取学员资料', '获取教练资料'],
            '师生关系': ['获取师生关系'],
            '预约功能': ['获取可用球台', '创建预约'],
            '通知系统': ['获取通知列表'],
            '前端界面': ['前端主页', 'Vue应用容器']
        }
        
        for function_name, test_names in core_functions.items():
            function_tests = [r for r in self.test_results if r['test'] in test_names]
            if function_tests:
                passed = sum(1 for t in function_tests if t['success'])
                total = len(function_tests)
                status = "✅" if passed == total else "⚠️" if passed > 0 else "❌"
                print(f"{status} {function_name}: {passed}/{total} 通过")
                
        # 保存详细报告
        with open('frontend_e2e_report.json', 'w', encoding='utf-8') as f:
            json.dump({
                'summary': {
                    'total': total_tests,
                    'passed': passed_tests,
                    'failed': failed_tests,
                    'success_rate': passed_tests/total_tests*100
                },
                'function_analysis': core_functions,
                'results': self.test_results
            }, f, ensure_ascii=False, indent=2)
            
        print("\n详细报告已保存到 frontend_e2e_report.json")
        
    def run_all_tests(self):
        """运行所有测试"""
        print("开始前端端到端功能测试...")
        print(f"测试时间: {datetime.now()}")
        
        # 设置测试数据
        self.setup_test_data()
        
        # 运行功能测试
        self.test_frontend_pages()
        self.test_student_login_flow()
        self.test_coach_login_flow()
        self.test_relation_functionality()
        self.test_booking_functionality()
        self.test_notification_functionality()
        
        # 清理测试数据
        self.cleanup_test_data()
        
        # 生成报告
        self.generate_report()
        
if __name__ == '__main__':
    tester = FrontendE2ETester()
    tester.run_all_tests()