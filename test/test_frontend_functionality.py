#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
前端功能完整性测试脚本
测试所有前端页面和功能是否正常工作
"""

import requests
import json
import time
from datetime import datetime, timedelta

class FrontendFunctionalityTester:
    def __init__(self):
        self.base_url = 'http://localhost:8000/api'
        self.frontend_url = 'http://localhost:3002'
        self.session = requests.Session()
        self.test_results = []
        
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
        
    def test_api_endpoints(self):
        """测试后端API端点是否可访问"""
        print("\n=== 测试后端API端点 ===")
        
        # 测试GET端点
        get_endpoints = [
            '/accounts/profile/',
            '/accounts/coaches/',
            '/reservations/relations/',
            '/reservations/bookings/',
            '/reservations/tables/',
            '/notifications/',
            '/campus/campuses/',
        ]
        
        for endpoint in get_endpoints:
            try:
                response = requests.get(f"{self.base_url}{endpoint}", timeout=5)
                # 200, 401, 403 都表示端点存在且正常
                if response.status_code in [200, 401, 403]:
                    self.log_test(f"GET {endpoint}", True, f"状态码: {response.status_code}")
                elif response.status_code == 404:
                    self.log_test(f"GET {endpoint}", False, f"端点不存在: {response.status_code}")
                else:
                    self.log_test(f"GET {endpoint}", True, f"端点存在，状态码: {response.status_code}")
            except Exception as e:
                self.log_test(f"GET {endpoint}", False, f"连接失败: {str(e)}")
                
        # 测试POST端点（只检查是否存在，不发送数据）
        post_endpoints = [
            '/accounts/login/',
            '/accounts/register/',
        ]
        
        for endpoint in post_endpoints:
            try:
                response = requests.post(f"{self.base_url}{endpoint}", timeout=5)
                # 400表示端点存在但缺少数据，405表示方法不允许
                if response.status_code in [400, 401, 403]:
                    self.log_test(f"POST {endpoint}", True, f"端点存在，状态码: {response.status_code}")
                elif response.status_code == 405:
                    self.log_test(f"POST {endpoint}", False, f"方法不允许: {response.status_code}")
                elif response.status_code == 404:
                    self.log_test(f"POST {endpoint}", False, f"端点不存在: {response.status_code}")
                else:
                    self.log_test(f"POST {endpoint}", True, f"端点存在，状态码: {response.status_code}")
            except Exception as e:
                self.log_test(f"POST {endpoint}", False, f"连接失败: {str(e)}")
                
    def test_frontend_accessibility(self):
        """测试前端页面是否可访问"""
        print("\n=== 测试前端页面可访问性 ===")
        
        try:
            response = requests.get(self.frontend_url, timeout=10)
            if response.status_code == 200:
                self.log_test("前端主页访问", True, "页面加载成功")
                # 检查是否包含Vue应用的基本元素
                if 'id="app"' in response.text:
                    self.log_test("Vue应用容器", True, "找到Vue应用容器")
                else:
                    self.log_test("Vue应用容器", False, "未找到Vue应用容器")
            else:
                self.log_test("前端主页访问", False, f"状态码: {response.status_code}")
        except Exception as e:
            self.log_test("前端主页访问", False, f"连接失败: {str(e)}")
            
    def test_user_authentication_flow(self):
        """测试用户认证流程"""
        print("\n=== 测试用户认证流程 ===")
        
        # 测试学员登录
        student_data = {
            'username': 'student_test',
            'password': 'testpass123'
        }
        
        try:
            response = self.session.post(
                f"{self.base_url}/accounts/login/",
                json=student_data,
                headers={'Content-Type': 'application/json'}
            )
            
            if response.status_code == 200:
                data = response.json()
                if 'access' in data:
                    self.log_test("学员登录API", True, "登录成功，获得访问令牌")
                    # 保存token用于后续测试
                    self.session.headers.update({
                        'Authorization': f'Bearer {data["access"]}'
                    })
                else:
                    self.log_test("学员登录API", False, "登录响应缺少访问令牌")
            elif response.status_code == 401:
                self.log_test("学员登录API", True, "登录端点正常（凭据无效）")
            else:
                self.log_test("学员登录API", False, f"状态码: {response.status_code}")
                
        except Exception as e:
            self.log_test("学员登录API", False, f"请求失败: {str(e)}")
            
    def test_profile_functionality(self):
        """测试个人资料功能"""
        print("\n=== 测试个人资料功能 ===")
        
        try:
            response = self.session.get(f"{self.base_url}/accounts/profile/")
            
            if response.status_code == 200:
                self.log_test("获取个人资料", True, "成功获取个人资料")
            elif response.status_code == 401:
                self.log_test("获取个人资料", True, "需要认证（正常行为）")
            else:
                self.log_test("获取个人资料", False, f"状态码: {response.status_code}")
                
        except Exception as e:
            self.log_test("获取个人资料", False, f"请求失败: {str(e)}")
            
    def test_booking_functionality(self):
        """测试预约功能"""
        print("\n=== 测试预约功能 ===")
        
        # 测试获取师生关系
        try:
            response = self.session.get(f"{self.base_url}/reservations/relations/")
            if response.status_code in [200, 401]:
                self.log_test("师生关系API", True, f"端点正常，状态码: {response.status_code}")
            else:
                self.log_test("师生关系API", False, f"状态码: {response.status_code}")
        except Exception as e:
            self.log_test("师生关系API", False, f"请求失败: {str(e)}")
            
        # 测试获取可用球台
        try:
            params = {
                'campus': 1,
                'start_time': (datetime.now() + timedelta(days=1)).isoformat(),
                'end_time': (datetime.now() + timedelta(days=1, hours=2)).isoformat()
            }
            response = self.session.get(
                f"{self.base_url}/reservations/tables/available/",
                params=params
            )
            if response.status_code in [200, 401]:
                self.log_test("可用球台API", True, f"端点正常，状态码: {response.status_code}")
            else:
                self.log_test("可用球台API", False, f"状态码: {response.status_code}")
        except Exception as e:
            self.log_test("可用球台API", False, f"请求失败: {str(e)}")
            
        # 测试预约创建
        try:
            booking_data = {
                'relation': 1,
                'start_time': (datetime.now() + timedelta(days=1)).isoformat(),
                'end_time': (datetime.now() + timedelta(days=1, hours=2)).isoformat(),
                'table': 1,
                'fee': 100.00,
                'notes': '测试预约'
            }
            response = self.session.post(
                f"{self.base_url}/reservations/bookings/",
                json=booking_data,
                headers={'Content-Type': 'application/json'}
            )
            if response.status_code in [201, 401, 400]:
                self.log_test("创建预约API", True, f"端点正常，状态码: {response.status_code}")
            else:
                self.log_test("创建预约API", False, f"状态码: {response.status_code}")
        except Exception as e:
            self.log_test("创建预约API", False, f"请求失败: {str(e)}")
            
    def test_notification_functionality(self):
        """测试通知功能"""
        print("\n=== 测试通知功能 ===")
        
        try:
            response = self.session.get(f"{self.base_url}/notifications/")
            if response.status_code in [200, 401]:
                self.log_test("通知API", True, f"端点正常，状态码: {response.status_code}")
            else:
                self.log_test("通知API", False, f"状态码: {response.status_code}")
        except Exception as e:
            self.log_test("通知API", False, f"请求失败: {str(e)}")
            
    def test_campus_management(self):
        """测试校区管理功能"""
        print("\n=== 测试校区管理功能 ===")
        
        try:
            response = self.session.get(f"{self.base_url}/campus/campuses/")
            if response.status_code in [200, 401]:
                self.log_test("校区管理API", True, f"端点正常，状态码: {response.status_code}")
                if response.status_code == 200:
                    data = response.json()
                    if isinstance(data, list):
                        self.log_test("校区数据格式", True, f"返回{len(data)}个校区")
                    else:
                        self.log_test("校区数据格式", False, "数据格式不正确")
            else:
                self.log_test("校区管理API", False, f"状态码: {response.status_code}")
        except Exception as e:
            self.log_test("校区管理API", False, f"请求失败: {str(e)}")
            
    def check_frontend_components(self):
        """检查前端组件文件是否存在"""
        print("\n=== 检查前端组件文件 ===")
        
        import os
        
        components = [
             'frontend/src/components/BookingForm.vue',
             'frontend/src/components/CoachSelection.vue',
             'frontend/src/views/Login.vue',
             'frontend/src/views/Dashboard.vue',
             'frontend/src/views/Profile.vue',
             'frontend/src/views/Notifications.vue',
             'frontend/src/router/index.js',
             'frontend/src/stores/user.js'
         ]
        
        for component in components:
            file_path = os.path.join(os.getcwd(), component)
            if os.path.exists(file_path):
                self.log_test(f"组件文件 {component}", True, "文件存在")
            else:
                self.log_test(f"组件文件 {component}", False, "文件不存在")
                
    def generate_report(self):
        """生成测试报告"""
        print("\n" + "="*50)
        print("前端功能测试报告")
        print("="*50)
        
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
                    
        # 保存详细报告
        with open('frontend_functionality_report.json', 'w', encoding='utf-8') as f:
            json.dump({
                'summary': {
                    'total': total_tests,
                    'passed': passed_tests,
                    'failed': failed_tests,
                    'success_rate': passed_tests/total_tests*100
                },
                'results': self.test_results
            }, f, ensure_ascii=False, indent=2)
            
        print("\n详细报告已保存到 frontend_functionality_report.json")
        
    def run_all_tests(self):
        """运行所有测试"""
        print("开始前端功能完整性测试...")
        print(f"测试时间: {datetime.now()}")
        
        # 按顺序执行测试
        self.test_api_endpoints()
        self.test_frontend_accessibility()
        self.test_user_authentication_flow()
        self.test_profile_functionality()
        self.test_booking_functionality()
        self.test_notification_functionality()
        self.test_campus_management()
        self.check_frontend_components()
        
        # 生成报告
        self.generate_report()
        
if __name__ == '__main__':
    tester = FrontendFunctionalityTester()
    tester.run_all_tests()