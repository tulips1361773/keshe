#!/usr/bin/env python
"""
前端教练更换功能测试脚本
测试前端表单提交和用户交互
"""

import requests
import json
import re
from datetime import datetime

class FrontendCoachChangeTest:
    def __init__(self):
        self.base_url = "http://localhost:8000"
        self.frontend_url = "http://localhost:3001"
        self.session = requests.Session()
        self.test_results = []
        
    def log_test(self, test_name, status, message="", details=None):
        """记录测试结果"""
        result = {
            'test': test_name,
            'status': status,
            'message': message,
            'details': details,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        self.test_results.append(result)
        status_symbol = "✅" if status == "PASS" else "❌" if status == "FAIL" else "⚠️"
        print(f"{status_symbol} {test_name}: {message}")
        if details:
            print(f"   详情: {details}")
    
    def get_csrf_token(self):
        """获取CSRF token"""
        try:
            response = self.session.get(f"{self.base_url}/api/accounts/csrf-token/")
            if response.status_code == 200:
                data = response.json()
                return data.get('csrfToken')
            else:
                print(f"获取CSRF token失败，状态码: {response.status_code}")
                return None
        except Exception as e:
            print(f"获取CSRF token异常: {e}")
            return None
    
    def login_as_student(self):
        """以学员身份登录"""
        print("\n=== 学员登录测试 ===")
        
        # 先获取CSRF token
        csrf_token = self.get_csrf_token()
        
        login_data = {
            'username': 'hhm',  # 使用真实的学员用户名
            'password': 'testpass123'
        }
        
        # 添加CSRF token到请求头
        headers = {
            'Content-Type': 'application/json'
        }
        if csrf_token:
            headers['X-CSRFToken'] = csrf_token
        
        try:
            response = self.session.post(
                f"{self.base_url}/api/accounts/login/", 
                json=login_data,
                headers=headers
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success') and 'token' in data:
                    # 设置认证头
                    self.session.headers.update({
                        'Authorization': f'Token {data["token"]}',
                        'Content-Type': 'application/json'
                    })
                    if csrf_token:
                        self.session.headers['X-CSRFToken'] = csrf_token
                    self.log_test("学员登录", "PASS", f"登录成功，用户类型: {data.get('user', {}).get('user_type', 'unknown')}")
                    return True
                else:
                    self.log_test("学员登录", "FAIL", f"登录响应格式错误: {data}")
                    return False
            else:
                self.log_test("学员登录", "FAIL", f"登录失败，状态码: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("学员登录", "FAIL", f"登录异常: {str(e)}")
            return False
    
    def test_get_coach_relations(self):
        """测试获取教练关系列表"""
        print("\n=== 测试教练关系列表API ===")
        
        try:
            response = self.session.get(f"{self.base_url}/api/reservations/relations/")
            
            if response.status_code == 200:
                data = response.json()
                self.log_test("教练关系列表", "PASS", 
                             f"获取成功，数据类型: {type(data)}")
                
                if isinstance(data, dict) and 'results' in data:
                    self.log_test("分页数据格式", "PASS", 
                                 f"包含字段: {list(data.keys())}")
                    
                    if data['results']:
                        sample_relation = data['results'][0]
                        self.log_test("关系数据结构", "PASS", 
                                     f"示例关系字段: {list(sample_relation.keys())}")
                    else:
                        self.log_test("关系数据内容", "WARN", "关系列表为空")
                        
                else:
                    self.log_test("分页数据格式", "FAIL", 
                                 f"数据格式不正确: {type(data)}")
                    
            else:
                self.log_test("教练关系列表", "FAIL", 
                             f"请求失败，状态码: {response.status_code}")
                
        except Exception as e:
            self.log_test("教练关系列表", "FAIL", f"请求异常: {str(e)}")
    
    def test_coach_change_request_submission(self):
        """测试教练更换请求提交"""
        print("\n=== 测试教练更换请求提交 ===")
        
        # 测试数据
        test_data = {
            'current_coach_id': 102,  # coach08
            'target_coach_id': 113,   # coach10
            'reason': '前端测试教练更换申请'
        }
        
        try:
            # 获取CSRF token
            csrf_token = self.get_csrf_token()
            
            # 设置请求头
            headers = {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrf_token,
                'Referer': self.base_url
            }
            
            response = self.session.post(
                f"{self.base_url}/api/reservations/coach-change-requests/", 
                json=test_data,
                headers=headers
            )
            
            if response.status_code == 201:
                data = response.json()
                self.log_test("教练更换请求提交", "PASS", 
                             f"提交成功，请求ID: {data.get('id', 'unknown')}")
                
                # 检查返回数据结构
                expected_fields = ['id', 'student', 'current_coach', 'target_coach', 'reason', 'status']
                actual_fields = list(data.keys())
                
                missing_fields = [f for f in expected_fields if f not in actual_fields]
                if not missing_fields:
                    self.log_test("响应数据结构", "PASS", "包含所有必要字段")
                else:
                    self.log_test("响应数据结构", "WARN", 
                                 f"缺少字段: {missing_fields}")
                
            elif response.status_code == 400:
                try:
                    error_data = response.json()
                    self.log_test("教练更换请求提交", "FAIL", 
                                 f"验证错误: {error_data}")
                except:
                    self.log_test("教练更换请求提交", "FAIL", 
                                 f"400错误，无法解析响应: {response.text}")
                    
            else:
                self.log_test("教练更换请求提交", "FAIL", 
                             f"提交失败，状态码: {response.status_code}, 响应: {response.text}")
                
        except Exception as e:
            self.log_test("教练更换请求提交", "FAIL", f"请求异常: {str(e)}")
    
    def test_invalid_data_submission(self):
        """测试无效数据提交"""
        print("\n=== 测试无效数据提交 ===")
        
        # 测试相同教练ID
        invalid_data = {
            'current_coach_id': 102,
            'target_coach_id': 102,  # 相同教练
            'reason': '测试相同教练'
        }
        
        try:
            # 获取CSRF token
            csrf_token = self.get_csrf_token()
            
            # 设置请求头
            headers = {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrf_token,
                'Referer': self.base_url
            }
            
            response = self.session.post(
                f"{self.base_url}/api/reservations/coach-change-requests/", 
                json=invalid_data,
                headers=headers
            )
            
            if response.status_code == 400:
                self.log_test("相同教练验证", "PASS", "正确拒绝相同教练的请求")
            else:
                self.log_test("相同教练验证", "FAIL", 
                             f"应该返回400错误，实际状态码: {response.status_code}")
                
        except Exception as e:
            self.log_test("相同教练验证", "FAIL", f"请求异常: {str(e)}")
        
        # 测试缺少必填字段
        incomplete_data = {
            'current_coach_id': 102,
            # 缺少 target_coach_id
            'reason': '测试缺少字段'
        }
        
        try:
            # 获取CSRF token
            csrf_token = self.get_csrf_token()
            
            # 设置请求头
            headers = {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrf_token,
                'Referer': self.base_url
            }
            
            response = self.session.post(
                f"{self.base_url}/api/reservations/coach-change-requests/", 
                json=incomplete_data,
                headers=headers
            )
            
            if response.status_code == 400:
                self.log_test("必填字段验证", "PASS", "正确拒绝缺少必填字段的请求")
            else:
                self.log_test("必填字段验证", "FAIL", 
                             f"应该返回400错误，实际状态码: {response.status_code}")
                
        except Exception as e:
            self.log_test("必填字段验证", "FAIL", f"请求异常: {str(e)}")
    
    def test_get_my_requests(self):
        """测试获取我的申请列表"""
        print("\n=== 测试我的申请列表 ===")
        
        try:
            response = self.session.get(f"{self.base_url}/api/reservations/coach-change-requests/")
            
            if response.status_code == 200:
                data = response.json()
                
                # 检查是否是分页格式
                if isinstance(data, dict) and 'results' in data:
                    requests_list = data['results']
                    self.log_test("我的申请列表", "PASS", 
                                 f"获取成功，申请数量: {len(requests_list)}")
                    
                    if requests_list:
                        sample_request = requests_list[0]
                        self.log_test("申请数据结构", "PASS", 
                                     f"示例申请字段: {list(sample_request.keys())}")
                    else:
                        self.log_test("申请数据内容", "WARN", "申请列表为空")
                        
                elif isinstance(data, list):
                    self.log_test("我的申请列表", "PASS", 
                                 f"获取成功，申请数量: {len(data)}")
                    
                    if data:
                        sample_request = data[0]
                        self.log_test("申请数据结构", "PASS", 
                                     f"示例申请字段: {list(sample_request.keys())}")
                    else:
                        self.log_test("申请数据内容", "WARN", "申请列表为空")
                else:
                    self.log_test("申请数据格式", "FAIL", 
                                 f"数据格式不正确: {type(data)}")
                    
            else:
                self.log_test("我的申请列表", "FAIL", 
                             f"请求失败，状态码: {response.status_code}")
                
        except Exception as e:
            self.log_test("我的申请列表", "FAIL", f"请求异常: {str(e)}")
    
    def run_all_tests(self):
        """运行所有测试"""
        print("🚀 开始前端教练更换功能测试")
        print("=" * 50)
        
        # 先登录
        if not self.login_as_student():
            print("❌ 登录失败，无法继续测试")
            return False
        
        # 运行各项测试
        self.test_get_coach_relations()
        self.test_coach_change_request_submission()
        self.test_invalid_data_submission()
        self.test_get_my_requests()
        
        # 生成测试报告
        print("\n" + "=" * 50)
        print("📊 前端测试结果汇总")
        print("=" * 50)
        
        pass_count = sum(1 for r in self.test_results if r['status'] == 'PASS')
        fail_count = sum(1 for r in self.test_results if r['status'] == 'FAIL')
        warn_count = sum(1 for r in self.test_results if r['status'] == 'WARN')
        
        print(f"✅ 通过: {pass_count}")
        print(f"❌ 失败: {fail_count}")
        print(f"⚠️  警告: {warn_count}")
        print(f"📈 总计: {len(self.test_results)}")
        
        if fail_count > 0:
            print("\n❌ 失败的测试:")
            for result in self.test_results:
                if result['status'] == 'FAIL':
                    print(f"  - {result['test']}: {result['message']}")
        
        return fail_count == 0

if __name__ == "__main__":
    tester = FrontendCoachChangeTest()
    success = tester.run_all_tests()
    
    if success:
        print("\n🎉 前端测试通过!")
    else:
        print("\n⚠️  前端测试存在问题，需要修复")