#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
学员注册流程测试脚本
测试学员注册的必填字段验证和注册流程
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
from django.urls import reverse
from accounts.models import User, UserProfile, Coach
from campus.models import Campus

class StudentRegistrationTest:
    def __init__(self):
        self.client = Client()
        self.base_url = 'http://127.0.0.1:8000'
        self.api_url = f'{self.base_url}/accounts/api'
        
    def setup_test_data(self):
        """设置测试数据"""
        print("\n=== 设置测试数据 ===")
        
        # 创建测试校区
        campus, created = Campus.objects.get_or_create(
            name='测试校区',
            defaults={
                'code': 'TEST001',
                'address': '测试地址123号',
                'phone': '13800138000',
                'campus_type': 'branch'
            }
        )
        print(f"测试校区: {campus.name} ({'创建' if created else '已存在'})")
        return campus
    
    def test_student_registration_success(self, campus):
        """测试学员注册成功案例"""
        print("\n=== 测试学员注册成功案例 ===")
        
        # 使用微秒级时间戳确保唯一性
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S%f")
        
        # 准备有效的学员注册数据
        student_data = {
            'username': f'student_test_{timestamp}',
            'password': 'Test123!@#',
            'password_confirm': 'Test123!@#',
            'real_name': '张三',
            'phone': f'139{timestamp[-8:]}',  # 使用时间戳后8位确保11位手机号
            'email': f'student_test_{timestamp}@test.com',
            'user_type': 'student',
            'gender': 'male'
        }
        
        try:
            response = requests.post(
                f'{self.api_url}/register/',
                json=student_data,
                headers={'Content-Type': 'application/json'}
            )
            
            print(f"响应状态码: {response.status_code}")
            print(f"响应内容: {response.text}")
            
            if response.status_code == 201:
                result = response.json()
                if result.get('success'):
                    print("✅ 学员注册成功")
                    print(f"用户ID: {result.get('user_id')}")
                    print(f"用户名: {result.get('username')}")
                    return True
                else:
                    print(f"❌ 注册失败: {result.get('message')}")
                    return False
            else:
                print(f"❌ HTTP错误: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ 请求异常: {str(e)}")
            return False
    
    def test_required_fields_validation(self, campus):
        """测试必填字段验证"""
        print("\n=== 测试必填字段验证 ===")
        
        # 测试缺少必填字段的情况
        test_cases = [
            {
                'name': '缺少用户名',
                'data': {
                    'password': 'Test123!@#',
                    'password_confirm': 'Test123!@#',
                    'real_name': '张三',
                    'phone': '13800138001',
                    'user_type': 'student',
                    'campus': campus.id
                },
                'expected_error': 'username'
            },
            {
                'name': '缺少密码',
                'data': {
                    'username': 'test_no_password',
                    'real_name': '张三',
                    'phone': '13800138002',
                    'user_type': 'student',
                    'campus': campus.id
                },
                'expected_error': 'password'
            },
            {
                'name': '缺少真实姓名',
                'data': {
                    'username': 'test_no_realname',
                    'password': 'Test123!@#',
                    'password_confirm': 'Test123!@#',
                    'phone': '13800138003',
                    'user_type': 'student',
                    'campus': campus.id
                },
                'expected_error': 'real_name'
            },
            {
                'name': '缺少手机号',
                'data': {
                    'username': 'test_no_phone',
                    'password': 'Test123!@#',
                    'password_confirm': 'Test123!@#',
                    'real_name': '张三',
                    'user_type': 'student',
                    'campus': campus.id
                },
                'expected_error': 'phone'
            },
            {
                'name': '缺少用户类型',
                'data': {
                    'username': 'test_no_usertype',
                    'password': 'Test123!@#',
                    'password_confirm': 'Test123!@#',
                    'real_name': '张三',
                    'phone': '13800138004'
                },
                'expected_error': 'user_type'
            }
        ]
        
        success_count = 0
        for test_case in test_cases:
            print(f"\n测试: {test_case['name']}")
            
            try:
                response = requests.post(
                    f'{self.api_url}/register/',
                    json=test_case['data'],
                    headers={'Content-Type': 'application/json'}
                )
                
                if response.status_code == 400:
                    result = response.json()
                    if not result.get('success'):
                        print(f"✅ 正确拒绝: {result.get('message')}")
                        success_count += 1
                    else:
                        print(f"❌ 应该拒绝但通过了")
                else:
                    print(f"❌ 期望400错误，实际: {response.status_code}")
                    
            except Exception as e:
                print(f"❌ 请求异常: {str(e)}")
        
        print(f"\n必填字段验证测试结果: {success_count}/{len(test_cases)} 通过")
        return success_count == len(test_cases)
    
    def test_password_complexity_validation(self, campus):
        """测试密码复杂度验证"""
        print("\n=== 测试密码复杂度验证 ===")
        
        password_test_cases = [
            {
                'name': '密码太短',
                'password': '123',
                'should_fail': True
            },
            {
                'name': '密码太长',
                'password': '1234567890123456789',
                'should_fail': True
            },
            {
                'name': '只有数字',
                'password': '12345678',
                'should_fail': True
            },
            {
                'name': '只有字母',
                'password': 'abcdefgh',
                'should_fail': True
            },
            {
                'name': '缺少特殊字符',
                'password': 'Test1234',
                'should_fail': True
            },
            {
                'name': '符合要求的密码',
                'password': 'Test123!@#',
                'should_fail': False
            }
        ]
        
        success_count = 0
        for i, test_case in enumerate(password_test_cases):
            print(f"\n测试: {test_case['name']}")
            
            timestamp = datetime.now().strftime("%H%M%S%f")[:8]  # 包含微秒确保唯一性
            test_data = {
                'username': f'pwd_test_{i}_{timestamp}',
                'password': test_case['password'],
                'password_confirm': test_case['password'],
                'real_name': '测试用户',
                'phone': f'138{timestamp[-6:]}{i:02d}',  # 确保11位手机号
                'user_type': 'student'
            }
            
            try:
                response = requests.post(
                    f'{self.api_url}/register/',
                    json=test_data,
                    headers={'Content-Type': 'application/json'}
                )
                
                if test_case['should_fail']:
                    if response.status_code == 400:
                        result = response.json()
                        print(f"✅ 正确拒绝: {result.get('message')}")
                        success_count += 1
                    else:
                        print(f"❌ 应该拒绝但通过了")
                else:
                    if response.status_code == 201:
                        result = response.json()
                        if result.get('success'):
                            print(f"✅ 正确通过")
                            success_count += 1
                        else:
                            print(f"❌ 应该通过但被拒绝: {result.get('message')}")
                    else:
                        print(f"❌ 应该通过但返回错误: {response.status_code}")
                        
            except Exception as e:
                print(f"❌ 请求异常: {str(e)}")
        
        print(f"\n密码复杂度验证测试结果: {success_count}/{len(password_test_cases)} 通过")
        return success_count == len(password_test_cases)
    
    def test_duplicate_validation(self, campus):
        """测试重复数据验证"""
        print("\n=== 测试重复数据验证 ===")
        
        # 先创建一个用户
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S%f")
        base_data = {
            'username': f'duplicate_test_{timestamp}',
            'password': 'Test123!@#',
            'password_confirm': 'Test123!@#',
            'real_name': '重复测试用户',
            'phone': f'137{timestamp[-8:]}',  # 使用时间戳确保11位手机号
            'email': f'duplicate_test_{timestamp}@test.com',
            'user_type': 'student'
        }
        
        # 创建第一个用户
        response1 = requests.post(
            f'{self.api_url}/register/',
            json=base_data,
            headers={'Content-Type': 'application/json'}
        )
        
        if response1.status_code != 201:
            print(f"❌ 创建第一个用户失败: {response1.text}")
            return False
        
        print("✅ 第一个用户创建成功")
        
        # 测试重复用户名
        timestamp2 = datetime.now().strftime("%Y%m%d_%H%M%S%f")
        duplicate_username_data = base_data.copy()
        duplicate_username_data['phone'] = f'136{timestamp2[-8:]}'
        duplicate_username_data['email'] = f'duplicate_test2_{timestamp2}@test.com'
        
        response2 = requests.post(
            f'{self.api_url}/register/',
            json=duplicate_username_data,
            headers={'Content-Type': 'application/json'}
        )
        
        if response2.status_code == 400:
            result = response2.json()
            print(f"✅ 正确拒绝重复用户名: {result.get('message')}")
            username_test_passed = True
        else:
            print(f"❌ 重复用户名应该被拒绝")
            username_test_passed = False
        
        # 测试重复手机号
        timestamp3 = datetime.now().strftime("%Y%m%d_%H%M%S%f")
        duplicate_phone_data = base_data.copy()
        duplicate_phone_data['username'] = f'duplicate_test2_{timestamp3}'
        duplicate_phone_data['email'] = f'duplicate_test3_{timestamp3}@test.com'
        
        response3 = requests.post(
            f'{self.api_url}/register/',
            json=duplicate_phone_data,
            headers={'Content-Type': 'application/json'}
        )
        
        if response3.status_code == 400:
            result = response3.json()
            print(f"✅ 正确拒绝重复手机号: {result.get('message')}")
            phone_test_passed = True
        else:
            print(f"❌ 重复手机号应该被拒绝")
            phone_test_passed = False
        
        return username_test_passed and phone_test_passed
    
    def run_all_tests(self):
        """运行所有测试"""
        print("\n" + "="*50)
        print("开始学员注册流程测试")
        print("="*50)
        
        # 设置测试数据
        campus = self.setup_test_data()
        
        # 运行各项测试
        test_results = {
            '学员注册成功': self.test_student_registration_success(campus),
            '必填字段验证': self.test_required_fields_validation(campus),
            '密码复杂度验证': self.test_password_complexity_validation(campus),
            '重复数据验证': self.test_duplicate_validation(campus)
        }
        
        # 输出测试结果
        print("\n" + "="*50)
        print("测试结果汇总")
        print("="*50)
        
        passed_count = 0
        total_count = len(test_results)
        
        for test_name, result in test_results.items():
            status = "✅ 通过" if result else "❌ 失败"
            print(f"{test_name}: {status}")
            if result:
                passed_count += 1
        
        print(f"\n总体结果: {passed_count}/{total_count} 测试通过")
        
        if passed_count == total_count:
            print("🎉 所有测试都通过了！")
        else:
            print("⚠️  部分测试失败，请检查相关功能")
        
        return passed_count == total_count

if __name__ == '__main__':
    tester = StudentRegistrationTest()
    tester.run_all_tests()