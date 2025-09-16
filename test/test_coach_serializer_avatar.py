#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试教练员序列化器头像字段更新

这个测试程序验证：
1. UserRegistrationSerializer是否正确处理头像字段
2. CoachSerializer是否包含头像相关字段
3. 注册流程是否正确保存头像数据
"""

import os
import sys
import django
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'keshe.settings')
django.setup()

from django.test import TestCase, Client
from django.urls import reverse
from accounts.models import User, Coach
from accounts.serializers import UserRegistrationSerializer, CoachSerializer
import json

class CoachSerializerAvatarTest:
    """教练员序列化器头像字段测试"""
    
    def __init__(self):
        self.test_results = []
    
    def log_test(self, test_name, passed, message=""):
        """记录测试结果"""
        status = "✅ PASS" if passed else "❌ FAIL"
        result = f"{status} {test_name}"
        if message:
            result += f" - {message}"
        self.test_results.append(result)
        print(result)
    
    def test_user_registration_serializer_fields(self):
        """测试用户注册序列化器字段"""
        try:
            # 检查UserRegistrationSerializer是否包含avatar字段
            serializer = UserRegistrationSerializer()
            fields = serializer.fields
            
            has_avatar_field = 'avatar' in fields
            has_achievements_field = 'achievements' in fields
            
            # 检查Meta.fields是否包含avatar
            meta_fields = UserRegistrationSerializer.Meta.fields
            avatar_in_meta = 'avatar' in meta_fields
            
            self.log_test(
                "注册序列化器包含avatar字段", 
                has_avatar_field, 
                "检查serializer.fields中的avatar"
            )
            
            self.log_test(
                "注册序列化器包含achievements字段", 
                has_achievements_field, 
                "检查serializer.fields中的achievements"
            )
            
            self.log_test(
                "Meta.fields包含avatar", 
                avatar_in_meta, 
                "检查Meta.fields列表"
            )
            
            return has_avatar_field and has_achievements_field and avatar_in_meta
            
        except Exception as e:
            self.log_test("注册序列化器字段测试", False, f"异常: {str(e)}")
            return False
    
    def test_coach_serializer_fields(self):
        """测试教练员序列化器字段"""
        try:
            # 检查CoachSerializer是否包含头像相关字段
            serializer = CoachSerializer()
            fields = serializer.fields
            
            has_avatar_field = 'avatar' in fields
            has_real_name_field = 'real_name' in fields
            has_phone_field = 'phone' in fields
            has_user_info_field = 'user_info' in fields
            
            # 检查Meta.fields是否包含这些字段
            meta_fields = CoachSerializer.Meta.fields
            avatar_in_meta = 'avatar' in meta_fields
            real_name_in_meta = 'real_name' in meta_fields
            phone_in_meta = 'phone' in meta_fields
            
            self.log_test(
                "教练序列化器包含avatar字段", 
                has_avatar_field, 
                "检查serializer.fields中的avatar"
            )
            
            self.log_test(
                "教练序列化器包含real_name字段", 
                has_real_name_field, 
                "检查serializer.fields中的real_name"
            )
            
            self.log_test(
                "教练序列化器包含phone字段", 
                has_phone_field, 
                "检查serializer.fields中的phone"
            )
            
            self.log_test(
                "教练序列化器包含user_info字段", 
                has_user_info_field, 
                "检查serializer.fields中的user_info"
            )
            
            self.log_test(
                "Meta.fields包含avatar", 
                avatar_in_meta, 
                "检查Meta.fields列表"
            )
            
            self.log_test(
                "Meta.fields包含real_name", 
                real_name_in_meta, 
                "检查Meta.fields列表"
            )
            
            self.log_test(
                "Meta.fields包含phone", 
                phone_in_meta, 
                "检查Meta.fields列表"
            )
            
            return all([
                has_avatar_field, has_real_name_field, has_phone_field,
                has_user_info_field, avatar_in_meta, real_name_in_meta, phone_in_meta
            ])
            
        except Exception as e:
            self.log_test("教练序列化器字段测试", False, f"异常: {str(e)}")
            return False
    
    def test_registration_validation(self):
        """测试注册验证逻辑"""
        try:
            # 测试教练员注册时缺少头像的验证
            import random
            random_suffix = random.randint(1000, 9999)
            coach_data_without_avatar = {
                'username': f'test_coach_{random_suffix}',
                'password': 'TestPass123!',
                'password_confirm': 'TestPass123!',
                'real_name': '测试教练',
                'user_type': 'coach',
                'phone': f'138{random.randint(10000000, 99999999)}',
                'email': f'coach{random_suffix}@test.com',
                'achievements': '获得过全国乒乓球比赛冠军',
                # 缺少avatar字段
            }
            
            serializer = UserRegistrationSerializer(data=coach_data_without_avatar)
            is_valid_without_avatar = serializer.is_valid()
            
            # 测试教练员注册时包含头像的验证
            random_suffix2 = random.randint(1000, 9999)
            coach_data_with_avatar = {
                'username': f'test_coach_with_avatar_{random_suffix2}',
                'password': 'TestPass123!',
                'password_confirm': 'TestPass123!',
                'real_name': '测试教练2',
                'user_type': 'coach',
                'phone': f'139{random.randint(10000000, 99999999)}',
                'email': f'coach_with_avatar_{random_suffix2}@test.com',
                'achievements': '获得过全国乒乓球比赛冠军',
                'avatar': 'data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD...'
            }
            
            serializer_with_avatar = UserRegistrationSerializer(data=coach_data_with_avatar)
            is_valid_with_avatar = serializer_with_avatar.is_valid()
            
            # 测试学员注册（不需要头像）
            import random
            random_phone = f'138{random.randint(10000000, 99999999)}'
            student_data = {
                'username': f'test_student_{random.randint(1000, 9999)}',
                'password': 'TestPass123!',
                'password_confirm': 'TestPass123!',
                'real_name': '测试学员',
                'user_type': 'student',
                'phone': random_phone,
                'email': f'student{random.randint(1000, 9999)}@test.com',
                # 学员不需要avatar和achievements
            }
            
            student_serializer = UserRegistrationSerializer(data=student_data)
            is_valid_student = student_serializer.is_valid()
            
            self.log_test(
                "教练员缺少头像验证失败", 
                not is_valid_without_avatar, 
                "应该验证失败"
            )
            
            if not is_valid_without_avatar:
                errors = serializer.errors
                has_avatar_error = any('头像' in str(error) for error in errors.get('non_field_errors', []))
                self.log_test(
                    "包含头像错误信息", 
                    has_avatar_error, 
                    f"错误信息: {errors}"
                )
            
            self.log_test(
                "教练员包含头像验证通过", 
                is_valid_with_avatar, 
                f"验证结果: {serializer_with_avatar.errors if not is_valid_with_avatar else '通过'}"
            )
            
            self.log_test(
                "学员注册验证通过", 
                is_valid_student, 
                f"验证结果: {student_serializer.errors if not is_valid_student else '通过'}"
            )
            
            return (not is_valid_without_avatar) and is_valid_with_avatar and is_valid_student
            
        except Exception as e:
            self.log_test("注册验证逻辑测试", False, f"异常: {str(e)}")
            return False
    
    def test_serializer_source_fields(self):
        """测试序列化器source字段配置"""
        try:
            # 检查CoachSerializer中的source配置
            serializer = CoachSerializer()
            
            # 检查avatar字段的source
            avatar_field = serializer.fields.get('avatar')
            avatar_source_correct = hasattr(avatar_field, 'source') and avatar_field.source == 'user.avatar'
            
            # 检查real_name字段的source
            real_name_field = serializer.fields.get('real_name')
            real_name_source_correct = hasattr(real_name_field, 'source') and real_name_field.source == 'user.real_name'
            
            # 检查phone字段的source
            phone_field = serializer.fields.get('phone')
            phone_source_correct = hasattr(phone_field, 'source') and phone_field.source == 'user.phone'
            
            self.log_test(
                "avatar字段source配置正确", 
                avatar_source_correct, 
                f"source: {getattr(avatar_field, 'source', 'None')}"
            )
            
            self.log_test(
                "real_name字段source配置正确", 
                real_name_source_correct, 
                f"source: {getattr(real_name_field, 'source', 'None')}"
            )
            
            self.log_test(
                "phone字段source配置正确", 
                phone_source_correct, 
                f"source: {getattr(phone_field, 'source', 'None')}"
            )
            
            return avatar_source_correct and real_name_source_correct and phone_source_correct
            
        except Exception as e:
            self.log_test("序列化器source字段测试", False, f"异常: {str(e)}")
            return False
    
    def run_all_tests(self):
        """运行所有测试"""
        print("\n" + "="*60)
        print("🧪 教练员序列化器头像字段测试")
        print("="*60)
        
        tests = [
            ("注册序列化器字段测试", self.test_user_registration_serializer_fields),
            ("教练序列化器字段测试", self.test_coach_serializer_fields),
            ("注册验证逻辑测试", self.test_registration_validation),
            ("序列化器source字段测试", self.test_serializer_source_fields),
        ]
        
        passed_tests = 0
        total_tests = len(tests)
        
        for test_name, test_func in tests:
            print(f"\n📋 {test_name}:")
            if test_func():
                passed_tests += 1
        
        print("\n" + "="*60)
        print(f"📊 测试结果汇总: {passed_tests}/{total_tests} 通过")
        
        if passed_tests == total_tests:
            print("🎉 所有测试通过！教练员序列化器头像字段更新完成。")
        else:
            print(f"⚠️  有 {total_tests - passed_tests} 个测试失败，需要进一步修复。")
        
        print("="*60)
        
        return passed_tests == total_tests

if __name__ == "__main__":
    tester = CoachSerializerAvatarTest()
    success = tester.run_all_tests()
    
    if success:
        print("\n✅ 步骤2完成：教练员序列化器头像字段更新成功！")
        print("📝 下一步：创建教练员列表页面")
    else:
        print("\n❌ 步骤2未完成：请检查并修复失败的测试项")
    
    sys.exit(0 if success else 1)