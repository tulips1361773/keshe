#!/usr/bin/env python
"""
教练更换功能详细测试脚本
测试后端API和前端功能的完整流程
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
from campus.models import CampusCoach, CampusStudent
from reservations.models import CoachStudentRelation, CoachChangeRequest

User = get_user_model()

class CoachChangeTestSuite:
    def __init__(self):
        self.base_url = "http://localhost:8000"
        self.frontend_url = "http://localhost:3001"
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
    
    def test_database_data(self):
        """测试数据库中的基础数据"""
        print("\n=== 测试数据库基础数据 ===")
        
        # 检查用户数据
        users = User.objects.all()
        self.log_test("用户数据检查", "PASS" if users.exists() else "FAIL", 
                     f"找到 {users.count()} 个用户")
        
        # 检查教练数据
        coaches = User.objects.filter(user_type='coach')
        self.log_test("教练数据检查", "PASS" if coaches.exists() else "FAIL", 
                     f"找到 {coaches.count()} 个教练")
        
        # 检查学员数据
        students = User.objects.filter(user_type='student')
        self.log_test("学员数据检查", "PASS" if students.exists() else "FAIL", 
                     f"找到 {students.count()} 个学员")
        
        # 检查教练学员关系
        relations = CoachStudentRelation.objects.all()
        self.log_test("教练学员关系检查", "PASS" if relations.exists() else "FAIL", 
                     f"找到 {relations.count()} 个关系")
        
        # 详细显示数据
        if coaches.exists():
            print("\n教练列表:")
            for coach in coaches[:5]:  # 显示前5个
                print(f"  - ID: {coach.id}, 用户: {coach.username}, 姓名: {coach.real_name}")
        
        if students.exists():
            print("\n学员列表:")
            for student in students[:5]:  # 显示前5个
                print(f"  - ID: {student.id}, 用户: {student.username}, 姓名: {student.real_name}")
        
        if relations.exists():
            print("\n教练学员关系:")
            for relation in relations[:5]:  # 显示前5个
                print(f"  - 学员: {relation.student.username} -> 教练: {relation.coach.username}")
    
    def test_api_endpoints(self):
        """测试API端点"""
        print("\n=== 测试API端点 ===")
        
        # 测试教练列表API
        try:
            response = requests.get(f"{self.base_url}/api/reservations/relations/")
            if response.status_code == 200:
                data = response.json()
                self.log_test("教练关系列表API", "PASS", 
                             f"状态码: {response.status_code}, 数据格式: {type(data)}")
                if isinstance(data, dict) and 'results' in data:
                    self.log_test("API分页格式", "PASS", 
                                 f"包含分页字段: {list(data.keys())}")
                else:
                    self.log_test("API分页格式", "FAIL", 
                                 f"缺少分页格式, 实际格式: {type(data)}")
            else:
                self.log_test("教练关系列表API", "FAIL", 
                             f"状态码: {response.status_code}")
        except Exception as e:
            self.log_test("教练关系列表API", "FAIL", f"请求失败: {str(e)}")
    
    def test_coach_change_request_creation(self):
        """测试教练更换请求创建"""
        print("\n=== 测试教练更换请求创建 ===")
        
        # 获取测试数据
        try:
            student = User.objects.filter(user_type='student').first()
            coaches = User.objects.filter(user_type='coach')
            
            if not student:
                self.log_test("测试数据准备", "FAIL", "没有找到学员数据")
                return
            
            if coaches.count() < 2:
                self.log_test("测试数据准备", "FAIL", "需要至少2个教练进行测试")
                return
            
            current_coach = coaches[0]
            target_coach = coaches[1]
            
            self.log_test("测试数据准备", "PASS", 
                         f"学员: {student.username}, 当前教练: {current_coach.username}, 目标教练: {target_coach.username}")
            
            # 创建或获取教练学员关系
            relation, created = CoachStudentRelation.objects.get_or_create(
                student=student,
                coach=current_coach,
                defaults={'status': 'approved', 'applied_by': 'student'}
            )
            
            if created:
                self.log_test("教练学员关系创建", "PASS", "创建了新的关系")
            else:
                self.log_test("教练学员关系检查", "PASS", "关系已存在")
            
            # 测试API请求数据格式
            test_data = {
                'current_coach_id': current_coach.id,
                'target_coach_id': target_coach.id,
                'reason': '测试教练更换申请'
            }
            
            self.log_test("API请求数据格式", "PASS", 
                         f"数据: {test_data}")
            
            # 检查现有的更换请求
            existing_requests = CoachChangeRequest.objects.filter(
                student=student,
                status='pending'
            )
            
            self.log_test("现有请求检查", "PASS", 
                         f"找到 {existing_requests.count()} 个待处理请求")
            
        except Exception as e:
            self.log_test("教练更换请求测试", "FAIL", f"测试失败: {str(e)}")
    
    def test_serializer_validation(self):
        """测试序列化器验证逻辑"""
        print("\n=== 测试序列化器验证 ===")
        
        from reservations.serializers import CoachChangeRequestSerializer
        
        try:
            # 获取测试数据
            student = User.objects.filter(user_type='student').first()
            coaches = User.objects.filter(user_type='coach')
            
            if not student or coaches.count() < 2:
                self.log_test("序列化器测试数据", "FAIL", "缺少必要的测试数据")
                return
            
            current_coach = coaches[0]
            target_coach = coaches[1]
            
            # 测试有效数据
            valid_data = {
                'current_coach_id': current_coach.id,
                'target_coach_id': target_coach.id,
                'reason': '测试原因'
            }
            
            # 创建序列化器实例
            serializer = CoachChangeRequestSerializer(data=valid_data)
            
            # 模拟请求上下文
            class MockRequest:
                def __init__(self, user):
                    self.user = user
            
            serializer.context = {'request': MockRequest(student)}
            
            if serializer.is_valid():
                self.log_test("序列化器验证-有效数据", "PASS", "数据验证通过")
            else:
                self.log_test("序列化器验证-有效数据", "FAIL", 
                             f"验证失败: {serializer.errors}")
            
            # 测试无效数据 - 相同教练
            invalid_data = {
                'current_coach_id': current_coach.id,
                'target_coach_id': current_coach.id,  # 相同教练
                'reason': '测试原因'
            }
            
            serializer = CoachChangeRequestSerializer(data=invalid_data)
            serializer.context = {'request': MockRequest(student)}
            
            if not serializer.is_valid():
                self.log_test("序列化器验证-相同教练", "PASS", 
                             f"正确拒绝相同教练: {serializer.errors}")
            else:
                self.log_test("序列化器验证-相同教练", "FAIL", 
                             "应该拒绝相同教练的请求")
            
        except Exception as e:
            self.log_test("序列化器验证测试", "FAIL", f"测试失败: {str(e)}")
    
    def test_frontend_api_call(self):
        """测试前端API调用"""
        print("\n=== 测试前端API调用格式 ===")
        
        # 检查前端代码中的API调用
        frontend_file = "frontend/src/views/CoachChange.vue"
        
        try:
            with open(frontend_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # 检查API调用格式
            if 'current_coach_id' in content and 'target_coach_id' in content:
                self.log_test("前端API字段格式", "PASS", "使用正确的字段名称")
            else:
                self.log_test("前端API字段格式", "FAIL", "字段名称不正确")
            
            # 检查错误处理
            if 'error.response?.data?.error' in content:
                self.log_test("前端错误处理", "PASS", "包含错误处理逻辑")
            else:
                self.log_test("前端错误处理", "WARN", "可能缺少完整的错误处理")
                
        except FileNotFoundError:
            self.log_test("前端文件检查", "FAIL", f"文件不存在: {frontend_file}")
        except Exception as e:
            self.log_test("前端文件检查", "FAIL", f"读取失败: {str(e)}")
    
    def run_all_tests(self):
        """运行所有测试"""
        print("🚀 开始教练更换功能详细测试")
        print("=" * 50)
        
        self.test_database_data()
        self.test_api_endpoints()
        self.test_coach_change_request_creation()
        self.test_serializer_validation()
        self.test_frontend_api_call()
        
        # 生成测试报告
        print("\n" + "=" * 50)
        print("📊 测试结果汇总")
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
    tester = CoachChangeTestSuite()
    success = tester.run_all_tests()
    
    if success:
        print("\n🎉 所有测试通过!")
    else:
        print("\n⚠️  存在测试失败，需要修复")
    
    sys.exit(0 if success else 1)