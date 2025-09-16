#!/usr/bin/env python
"""
教练更换系统测试脚本
测试完整的教练更换流程，包括：
1. 学员申请更换教练
2. 当前教练审批
3. 目标教练审批
4. 校区管理员审批
5. 系统自动更新师生关系
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

from django.contrib.auth import get_user_model
from reservations.models import CoachStudentRelation
from reservations.coach_change_models import CoachChangeRequest

User = get_user_model()

class CoachChangeSystemTester:
    def __init__(self):
        self.base_url = 'http://127.0.0.1:8000'
        self.session = requests.Session()
        self.test_results = []
        
    def log_result(self, test_name, success, message="", data=None):
        """记录测试结果"""
        result = {
            'test_name': test_name,
            'success': success,
            'message': message,
            'timestamp': datetime.now().isoformat(),
            'data': data
        }
        self.test_results.append(result)
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}: {message}")
        if data:
            print(f"   Data: {json.dumps(data, indent=2, ensure_ascii=False)}")
        print()

    def login_user(self, username, password):
        """用户登录"""
        try:
            response = self.session.post(f'{self.base_url}/api/accounts/login/', {
                'username': username,
                'password': password
            })
            
            if response.status_code == 200:
                data = response.json()
                token = data.get('access_token')
                if token:
                    self.session.headers.update({'Authorization': f'Bearer {token}'})
                    return True, data
                else:
                    return False, "No access token in response"
            else:
                return False, f"Login failed: {response.status_code} - {response.text}"
        except Exception as e:
            return False, f"Login error: {str(e)}"

    def test_student_create_change_request(self):
        """测试学员创建教练更换请求"""
        print("=== 测试学员创建教练更换请求 ===")
        
        # 登录学员账号 - 使用实际存在的测试用户
        success, result = self.login_user('test_student', 'testpass123')
        if not success:
            self.log_result("学员登录", False, result)
            return False
        
        self.log_result("学员登录", True, "登录成功", result)
        
        # 获取学员的教练关系
        try:
            response = self.session.get(f'{self.base_url}/api/reservations/relations/')
            if response.status_code == 200:
                relations = response.json()
                approved_relations = [r for r in relations if r['status'] == 'approved']
                
                if not approved_relations:
                    self.log_result("获取师生关系", False, "学员没有已批准的教练关系")
                    return False
                
                current_coach_id = approved_relations[0]['coach']
                self.log_result("获取师生关系", True, f"当前教练ID: {current_coach_id}")
            else:
                self.log_result("获取师生关系", False, f"请求失败: {response.status_code}")
                return False
        except Exception as e:
            self.log_result("获取师生关系", False, f"请求异常: {str(e)}")
            return False
        
        # 获取可用教练列表
        try:
            response = self.session.get(f'{self.base_url}/api/reservations/coaches/')
            if response.status_code == 200:
                coaches = response.json()
                available_coaches = [c for c in coaches if c['id'] != current_coach_id]
                
                if not available_coaches:
                    self.log_result("获取教练列表", False, "没有可选择的其他教练")
                    return False
                
                target_coach_id = available_coaches[0]['id']
                self.log_result("获取教练列表", True, f"目标教练ID: {target_coach_id}")
            else:
                self.log_result("获取教练列表", False, f"请求失败: {response.status_code}")
                return False
        except Exception as e:
            self.log_result("获取教练列表", False, f"请求异常: {str(e)}")
            return False
        
        # 创建更换请求
        change_data = {
            'current_coach': current_coach_id,
            'target_coach': target_coach_id,
            'reason': '希望更换到更适合的教练，提高学习效果。'
        }
        
        try:
            response = self.session.post(
                f'{self.base_url}/api/reservations/coach-change-requests/',
                json=change_data
            )
            
            if response.status_code == 201:
                request_data = response.json()
                self.log_result("创建更换请求", True, "请求创建成功", request_data)
                return request_data['id']
            else:
                self.log_result("创建更换请求", False, f"请求失败: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            self.log_result("创建更换请求", False, f"请求异常: {str(e)}")
            return False

    def test_coach_approval(self, request_id, coach_username, action='approve'):
        """测试教练审批"""
        print(f"=== 测试教练审批 ({coach_username}) ===")
        
        # 登录教练账号
        success, result = self.login_user(coach_username, 'testpass123')
        if not success:
            self.log_result(f"{coach_username}登录", False, result)
            return False
        
        self.log_result(f"{coach_username}登录", True, "登录成功")
        
        # 获取待审批请求
        try:
            response = self.session.get(f'{self.base_url}/api/reservations/pending-coach-change-approvals/')
            if response.status_code == 200:
                pending_requests = response.json()
                target_request = None
                
                for req in pending_requests:
                    if req['id'] == request_id:
                        target_request = req
                        break
                
                if not target_request:
                    self.log_result("获取待审批请求", False, f"未找到请求ID {request_id}")
                    return False
                
                self.log_result("获取待审批请求", True, "找到待审批请求", target_request)
            else:
                self.log_result("获取待审批请求", False, f"请求失败: {response.status_code}")
                return False
        except Exception as e:
            self.log_result("获取待审批请求", False, f"请求异常: {str(e)}")
            return False
        
        # 提交审批
        approval_data = {
            'action': action,
            'notes': f'教练{coach_username}的审批意见：{"同意" if action == "approve" else "拒绝"}更换请求。'
        }
        
        try:
            response = self.session.post(
                f'{self.base_url}/api/reservations/coach-change-requests/{request_id}/approve/',
                json=approval_data
            )
            
            if response.status_code == 200:
                approval_result = response.json()
                self.log_result(f"{coach_username}审批", True, f"审批成功: {action}", approval_result)
                return True
            else:
                self.log_result(f"{coach_username}审批", False, f"审批失败: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            self.log_result(f"{coach_username}审批", False, f"审批异常: {str(e)}")
            return False

    def test_admin_approval(self, request_id, action='approve'):
        """测试管理员审批"""
        print("=== 测试管理员审批 ===")
        
        # 登录管理员账号 - 使用现有的管理员账号
        success, result = self.login_user('test_admin', 'testpass123')
        if not success:
            self.log_result("管理员登录", False, result)
            return False
        
        self.log_result("管理员登录", True, "登录成功")
        
        # 获取待审批请求
        try:
            response = self.session.get(f'{self.base_url}/api/reservations/pending-coach-change-approvals/')
            if response.status_code == 200:
                pending_requests = response.json()
                target_request = None
                
                for req in pending_requests:
                    if req['id'] == request_id:
                        target_request = req
                        break
                
                if not target_request:
                    self.log_result("获取待审批请求", False, f"未找到请求ID {request_id}")
                    return False
                
                self.log_result("获取待审批请求", True, "找到待审批请求", target_request)
            else:
                self.log_result("获取待审批请求", False, f"请求失败: {response.status_code}")
                return False
        except Exception as e:
            self.log_result("获取待审批请求", False, f"请求异常: {str(e)}")
            return False
        
        # 提交审批
        approval_data = {
            'action': action,
            'notes': f'管理员审批意见：{"同意" if action == "approve" else "拒绝"}更换请求。'
        }
        
        try:
            response = self.session.post(
                f'{self.base_url}/api/reservations/coach-change-requests/{request_id}/approve/',
                json=approval_data
            )
            
            if response.status_code == 200:
                approval_result = response.json()
                self.log_result("管理员审批", True, f"审批成功: {action}", approval_result)
                return True
            else:
                self.log_result("管理员审批", False, f"审批失败: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            self.log_result("管理员审批", False, f"审批异常: {str(e)}")
            return False

    def test_request_status(self, request_id):
        """测试请求状态查询"""
        print("=== 测试请求状态查询 ===")
        
        try:
            response = self.session.get(f'{self.base_url}/api/reservations/coach-change-requests/{request_id}/')
            if response.status_code == 200:
                request_data = response.json()
                self.log_result("查询请求状态", True, "状态查询成功", request_data)
                return request_data
            else:
                self.log_result("查询请求状态", False, f"查询失败: {response.status_code}")
                return None
        except Exception as e:
            self.log_result("查询请求状态", False, f"查询异常: {str(e)}")
            return None

    def verify_relation_update(self, student_username, expected_coach_id):
        """验证师生关系是否已更新"""
        print("=== 验证师生关系更新 ===")
        
        try:
            # 获取学员用户
            student = User.objects.get(username=student_username)
            
            # 查询当前的师生关系
            current_relations = CoachStudentRelation.objects.filter(
                student=student,
                status='approved'
            )
            
            if current_relations.exists():
                current_coach_id = current_relations.first().coach.id
                if current_coach_id == expected_coach_id:
                    self.log_result("验证关系更新", True, f"师生关系已正确更新，当前教练ID: {current_coach_id}")
                    return True
                else:
                    self.log_result("验证关系更新", False, f"师生关系未正确更新，期望教练ID: {expected_coach_id}，实际教练ID: {current_coach_id}")
                    return False
            else:
                self.log_result("验证关系更新", False, "未找到已批准的师生关系")
                return False
        except Exception as e:
            self.log_result("验证关系更新", False, f"验证异常: {str(e)}")
            return False

    def run_complete_test(self):
        """运行完整的教练更换流程测试"""
        print("🚀 开始教练更换系统完整流程测试")
        print("=" * 60)
        
        # 1. 学员创建更换请求
        request_id = self.test_student_create_change_request()
        if not request_id:
            print("❌ 测试失败：无法创建更换请求")
            return False
        
        # 2. 查询请求详情
        request_data = self.test_request_status(request_id)
        if not request_data:
            print("❌ 测试失败：无法查询请求状态")
            return False
        
        current_coach_id = request_data['current_coach']
        target_coach_id = request_data['target_coach']
        
        # 获取教练用户名
        try:
            current_coach = User.objects.get(id=current_coach_id)
            target_coach = User.objects.get(id=target_coach_id)
            current_coach_username = current_coach.username
            target_coach_username = target_coach.username
        except User.DoesNotExist:
            print("❌ 测试失败：无法找到教练用户")
            return False
        
        # 3. 当前教练审批
        if not self.test_coach_approval(request_id, current_coach_username, 'approve'):
            print("❌ 测试失败：当前教练审批失败")
            return False
        
        # 4. 目标教练审批
        if not self.test_coach_approval(request_id, target_coach_username, 'approve'):
            print("❌ 测试失败：目标教练审批失败")
            return False
        
        # 5. 管理员审批
        if not self.test_admin_approval(request_id, 'approve'):
            print("❌ 测试失败：管理员审批失败")
            return False
        
        # 6. 验证最终状态
        final_request_data = self.test_request_status(request_id)
        if not final_request_data:
            print("❌ 测试失败：无法查询最终状态")
            return False
        
        if final_request_data['status'] != 'approved':
            self.log_result("验证最终状态", False, f"请求状态不正确，期望: approved，实际: {final_request_data['status']}")
            return False
        
        # 7. 验证师生关系更新
        if not self.verify_relation_update('test_student', target_coach_id):
            print("❌ 测试失败：师生关系未正确更新")
            return False
        
        print("🎉 教练更换系统完整流程测试成功！")
        return True

    def generate_test_report(self):
        """生成测试报告"""
        print("\n" + "=" * 60)
        print("📊 测试报告")
        print("=" * 60)
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result['success'])
        failed_tests = total_tests - passed_tests
        
        print(f"总测试数: {total_tests}")
        print(f"通过测试: {passed_tests}")
        print(f"失败测试: {failed_tests}")
        print(f"通过率: {passed_tests/total_tests*100:.1f}%")
        
        if failed_tests > 0:
            print("\n❌ 失败的测试:")
            for result in self.test_results:
                if not result['success']:
                    print(f"  - {result['test_name']}: {result['message']}")
        
        # 保存详细报告
        report_file = 'coach_change_test_report.json'
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(self.test_results, f, indent=2, ensure_ascii=False)
        
        print(f"\n📄 详细测试报告已保存到: {report_file}")

def main():
    """主函数"""
    tester = CoachChangeSystemTester()
    
    try:
        # 运行完整测试
        success = tester.run_complete_test()
        
        # 生成测试报告
        tester.generate_test_report()
        
        if success:
            print("\n✅ 教练更换系统测试完成，所有功能正常！")
            sys.exit(0)
        else:
            print("\n❌ 教练更换系统测试失败，请检查相关功能！")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n⚠️ 测试被用户中断")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 测试过程中发生异常: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main()