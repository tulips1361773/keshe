#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试头像字段长度修复后的注册功能
"""

import os
import sys
import django
import requests
import json
from io import BytesIO
from PIL import Image
import base64

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'keshe.settings')
django.setup()

from django.contrib.auth import get_user_model
from accounts.models import Coach

User = get_user_model()

class AvatarFixTester:
    def __init__(self):
        self.base_url = 'http://localhost:8000'
        self.test_results = []
        
    def log_test(self, test_name, success, details=""):
        """记录测试结果"""
        status = "✓ 通过" if success else "✗ 失败"
        result = f"[{status}] {test_name}"
        if details:
            result += f" - {details}"
        print(result)
        self.test_results.append({
            'name': test_name,
            'success': success,
            'details': details
        })
        return success
    
    def create_test_image(self):
        """创建测试用的图片文件"""
        try:
            # 创建一个简单的测试图片
            img = Image.new('RGB', (100, 100), color='red')
            img_bytes = BytesIO()
            img.save(img_bytes, format='JPEG')
            img_bytes.seek(0)
            return img_bytes.getvalue()
        except Exception as e:
            print(f"创建测试图片失败: {e}")
            return None
    
    def test_database_avatar_field(self):
        """测试数据库avatar字段长度"""
        try:
            from django.db import connection
            cursor = connection.cursor()
            cursor.execute('DESCRIBE accounts_user')
            rows = cursor.fetchall()
            
            avatar_field = None
            for row in rows:
                if 'avatar' in str(row):
                    avatar_field = row
                    break
            
            if avatar_field:
                field_type = avatar_field[1]
                is_varchar_500 = 'varchar(500)' in field_type
                return self.log_test(
                    "数据库avatar字段长度检查",
                    is_varchar_500,
                    f"字段类型: {field_type}"
                )
            else:
                return self.log_test(
                    "数据库avatar字段长度检查",
                    False,
                    "未找到avatar字段"
                )
                
        except Exception as e:
            return self.log_test(
                "数据库avatar字段长度检查",
                False,
                f"异常: {str(e)}"
            )
    
    def test_coach_registration_with_avatar(self):
        """测试带头像的教练员注册"""
        try:
            # 创建测试图片
            img_data = self.create_test_image()
            if not img_data:
                return self.log_test(
                    "教练员注册（带头像）",
                    False,
                    "无法创建测试图片"
                )
            
            # 准备注册数据
            files = {
                'avatar': ('test_avatar.jpg', img_data, 'image/jpeg')
            }
            
            data = {
                'username': f'test_coach_avatar_{len(User.objects.all()) + 1}',
                'password': 'TestPass123!',
                'password_confirm': 'TestPass123!',
                'real_name': '测试教练员',
                'phone': f'1380000{len(User.objects.all()) + 1000:04d}',
                'email': f'test_coach_{len(User.objects.all()) + 1}@example.com',
                'user_type': 'coach',
                'achievements': '测试成绩描述' * 20  # 创建较长的成绩描述
            }
            
            # 发送注册请求
            response = requests.post(
                f'{self.base_url}/accounts/api/register/',
                data=data,
                files=files,
                timeout=10
            )
            
            success = response.status_code in [200, 201]
            details = f"状态码: {response.status_code}"
            
            if not success:
                try:
                    error_data = response.json()
                    details += f", 错误: {error_data}"
                except:
                    details += f", 响应: {response.text[:200]}"
            
            return self.log_test(
                "教练员注册（带头像）",
                success,
                details
            )
            
        except Exception as e:
            return self.log_test(
                "教练员注册（带头像）",
                False,
                f"异常: {str(e)}"
            )
    
    def test_long_filename_avatar(self):
        """测试长文件名头像上传"""
        try:
            # 创建测试图片
            img_data = self.create_test_image()
            if not img_data:
                return self.log_test(
                    "长文件名头像上传测试",
                    False,
                    "无法创建测试图片"
                )
            
            # 创建一个很长的文件名
            long_filename = 'very_long_filename_' + 'x' * 100 + '.jpg'
            
            files = {
                'avatar': (long_filename, img_data, 'image/jpeg')
            }
            
            data = {
                'username': f'test_long_filename_{len(User.objects.all()) + 1}',
                'password': 'TestPass123!',
                'password_confirm': 'TestPass123!',
                'real_name': '长文件名测试',
                'phone': f'1390000{len(User.objects.all()) + 1000:04d}',
                'email': f'test_long_{len(User.objects.all()) + 1}@example.com',
                'user_type': 'coach',
                'achievements': '长文件名测试成绩'
            }
            
            response = requests.post(
                f'{self.base_url}/accounts/api/register/',
                data=data,
                files=files,
                timeout=10
            )
            
            success = response.status_code in [200, 201]
            details = f"状态码: {response.status_code}, 文件名长度: {len(long_filename)}"
            
            if not success:
                try:
                    error_data = response.json()
                    details += f", 错误: {error_data}"
                except:
                    details += f", 响应: {response.text[:200]}"
            
            return self.log_test(
                "长文件名头像上传测试",
                success,
                details
            )
            
        except Exception as e:
            return self.log_test(
                "长文件名头像上传测试",
                False,
                f"异常: {str(e)}"
            )
    
    def run_all_tests(self):
        """运行所有测试"""
        print("=== 头像字段修复测试 ===")
        print()
        
        tests = [
            self.test_database_avatar_field,
            self.test_coach_registration_with_avatar,
            self.test_long_filename_avatar
        ]
        
        passed = 0
        total = len(tests)
        
        for test in tests:
            if test():
                passed += 1
            print()
        
        print(f"=== 测试完成: {passed}/{total} 通过 ===")
        
        if passed == total:
            print("🎉 所有测试通过！头像字段长度问题已修复。")
        else:
            print("⚠️  部分测试失败，请检查相关问题。")
        
        return passed == total

if __name__ == '__main__':
    tester = AvatarFixTester()
    tester.run_all_tests()