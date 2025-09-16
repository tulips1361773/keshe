#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
前端注册上传照片功能测试脚本
测试前端注册页面的头像上传功能是否正常工作
"""

import os
import sys
import django
import requests
import base64
from io import BytesIO
from PIL import Image
import json

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'keshe.settings')
django.setup()

from accounts.models import User

class FrontendPhotoUploadTester:
    def __init__(self):
        self.base_url = 'http://localhost:8000'
        self.test_results = []
        
    def create_test_image(self, format='JPEG', filename='test_avatar', size=(100, 100)):
        """创建测试图片并转换为base64格式"""
        # 创建一个简单的测试图片
        img = Image.new('RGB', size, color='red')
        
        # 保存到内存
        buffer = BytesIO()
        img.save(buffer, format=format)
        buffer.seek(0)
        
        # 转换为base64
        image_data = buffer.getvalue()
        base64_data = base64.b64encode(image_data).decode('utf-8')
        
        # 构造data URL
        mime_type = f'image/{format.lower()}'
        if format.upper() == 'JPEG':
            mime_type = 'image/jpeg'
        
        data_url = f'data:{mime_type};base64,{base64_data}'
        
        return data_url, len(filename)
    
    def test_coach_registration_with_avatar(self):
        """测试教练员注册（带头像）"""
        print("\n[测试] 教练员注册（带头像）")
        
        try:
            # 创建测试图片
            avatar_data, _ = self.create_test_image('JPEG', 'coach_avatar')
            
            # 准备注册数据
            data = {
                'username': 'test_coach_frontend',
                'password': 'testpass123!',
                'password_confirm': 'testpass123!',
                'email': 'coach_frontend@test.com',
                'real_name': '测试教练',
                'user_type': 'coach',
                'avatar': avatar_data,
                'phone': '13800138001',
                'achievements': '全国游泳比赛第一名',
                'specialties': '游泳,健身',
                'experience_years': 5,
                'hourly_rate': 100.00,
                'bio': '专业游泳教练'
            }
            
            # 模拟前端FormData发送方式
            # 将base64转换为文件
            base64_data = avatar_data.split(',')[1]
            mime_type = avatar_data.split(',')[0].split(':')[1].split(';')[0]
            image_bytes = base64.b64decode(base64_data)
            
            # 准备FormData
            files = {
                'avatar': ('coach_avatar.jpg', BytesIO(image_bytes), mime_type)
            }
            
            # 移除avatar字段，因为它现在在files中
            form_data = {k: v for k, v in data.items() if k != 'avatar'}
            
            # 发送注册请求
            response = requests.post(
                f'{self.base_url}/accounts/api/register/',
                data=form_data,
                files=files
            )
            
            if response.status_code == 201:
                print(f"[✓ 通过] 教练员注册（带头像） - 状态码: {response.status_code}")
                
                # 验证用户是否创建成功
                user = User.objects.filter(username='test_coach_frontend').first()
                if user and user.avatar:
                    print(f"[✓ 通过] 头像文件已保存: {user.avatar.name}")
                    return True
                else:
                    print(f"[✗ 失败] 用户创建成功但头像未保存")
                    return False
            else:
                print(f"[✗ 失败] 教练员注册失败 - 状态码: {response.status_code}")
                print(f"错误信息: {response.text}")
                return False
                
        except Exception as e:
            print(f"[✗ 失败] 教练员注册异常: {str(e)}")
            return False
    
    def test_different_image_formats(self):
        """测试不同格式图片上传"""
        print("\n[测试] 不同格式图片上传")
        
        formats = ['JPEG', 'PNG']
        success_count = 0
        
        for format_type in formats:
            try:
                # 创建测试图片
                avatar_data, _ = self.create_test_image(format_type, f'test_{format_type.lower()}')
                
                # 准备注册数据
                data = {
                    'username': f'test_user_{format_type.lower()}',
                    'password': 'testpass123!',
                    'password_confirm': 'testpass123!',
                    'email': f'{format_type.lower()}@test.com',
                    'real_name': f'测试用户{format_type}',
                    'user_type': 'coach',
                    'avatar': avatar_data,
                    'phone': f'1380013800{2 + formats.index(format_type)}',
                    'achievements': f'{format_type}格式测试成绩',
                    'specialties': '测试',
                    'experience_years': 1,
                    'hourly_rate': 50.00,
                    'bio': f'{format_type}格式测试'
                }
                
                # 模拟前端FormData发送方式
                base64_data = avatar_data.split(',')[1]
                mime_type = avatar_data.split(',')[0].split(':')[1].split(';')[0]
                image_bytes = base64.b64decode(base64_data)
                
                # 准备FormData
                files = {
                    'avatar': (f'{format_type.lower()}_avatar.jpg', BytesIO(image_bytes), mime_type)
                }
                
                # 移除avatar字段
                form_data = {k: v for k, v in data.items() if k != 'avatar'}
                
                # 发送注册请求
                response = requests.post(
                    f'{self.base_url}/accounts/api/register/',
                    data=form_data,
                    files=files
                )
                
                if response.status_code == 201:
                    print(f"[✓ 通过] {format_type}格式图片上传成功")
                    success_count += 1
                else:
                    print(f"[✗ 失败] {format_type}格式图片上传失败 - 状态码: {response.status_code}")
                    
            except Exception as e:
                print(f"[✗ 失败] {format_type}格式测试异常: {str(e)}")
        
        return success_count == len(formats)
    
    def test_long_filename_upload(self):
        """测试长文件名图片上传"""
        print("\n[测试] 长文件名图片上传")
        
        try:
            # 创建长文件名
            long_filename = 'very_long_filename_for_testing_avatar_upload_functionality_with_extremely_long_names_that_might_cause_issues'
            avatar_data, filename_length = self.create_test_image('JPEG', long_filename)
            
            # 准备注册数据
            data = {
                'username': 'test_long_filename',
                'password': 'testpass123!',
                'password_confirm': 'testpass123!',
                'email': 'longfilename@test.com',
                'real_name': '长文件名测试用户',
                'user_type': 'coach',
                'avatar': avatar_data,
                'phone': '13800138005',
                'achievements': '长文件名测试成绩',
                'specialties': '测试',
                'experience_years': 1,
                'hourly_rate': 50.00,
                'bio': '长文件名测试'
            }
            
            # 模拟前端FormData发送方式
            base64_data = avatar_data.split(',')[1]
            mime_type = avatar_data.split(',')[0].split(':')[1].split(';')[0]
            image_bytes = base64.b64decode(base64_data)
            
            # 准备FormData
            files = {
                'avatar': (f'{long_filename}.jpg', BytesIO(image_bytes), mime_type)
            }
            
            # 移除avatar字段
            form_data = {k: v for k, v in data.items() if k != 'avatar'}
            
            # 发送注册请求
            response = requests.post(
                f'{self.base_url}/accounts/api/register/',
                data=form_data,
                files=files
            )
            
            if response.status_code == 201:
                print(f"[✓ 通过] 长文件名图片上传成功 - 文件名长度: {filename_length}")
                return True
            else:
                print(f"[✗ 失败] 长文件名图片上传失败 - 状态码: {response.status_code}")
                print(f"错误信息: {response.text}")
                return False
                
        except Exception as e:
            print(f"[✗ 失败] 长文件名测试异常: {str(e)}")
            return False
    
    def test_avatar_display_and_storage(self):
        """测试头像显示和存储"""
        print("\n[测试] 头像显示和存储验证")
        
        try:
            # 查找已创建的测试用户
            test_users = User.objects.filter(username__startswith='test_').exclude(avatar='')
            
            if not test_users.exists():
                print("[✗ 失败] 没有找到带头像的测试用户")
                return False
            
            success_count = 0
            total_count = test_users.count()
            
            for user in test_users:
                if user.avatar and user.avatar.name:
                    # 检查文件是否存在
                    avatar_path = user.avatar.path
                    if os.path.exists(avatar_path):
                        print(f"[✓ 通过] 用户 {user.username} 的头像文件存在: {user.avatar.name}")
                        success_count += 1
                    else:
                        print(f"[✗ 失败] 用户 {user.username} 的头像文件不存在: {avatar_path}")
                else:
                    print(f"[✗ 失败] 用户 {user.username} 没有头像数据")
            
            print(f"\n头像存储验证: {success_count}/{total_count} 通过")
            return success_count == total_count
            
        except Exception as e:
            print(f"[✗ 失败] 头像显示和存储验证异常: {str(e)}")
            return False
    
    def cleanup_test_data(self):
        """清理测试数据"""
        print("\n[清理] 删除测试数据")
        try:
            # 删除测试用户
            test_users = User.objects.filter(username__startswith='test_')
            deleted_count = 0
            
            for user in test_users:
                # 删除头像文件
                if user.avatar:
                    try:
                        if os.path.exists(user.avatar.path):
                            os.remove(user.avatar.path)
                    except:
                        pass
                
                user.delete()
                deleted_count += 1
            
            print(f"[✓ 完成] 已删除 {deleted_count} 个测试用户")
            
        except Exception as e:
            print(f"[警告] 清理测试数据时出现异常: {str(e)}")
    
    def run_all_tests(self):
        """运行所有测试"""
        print("=== 前端注册上传照片功能测试 ===")
        
        # 清理之前的测试数据
        self.cleanup_test_data()
        
        tests = [
            ('教练员注册（带头像）', self.test_coach_registration_with_avatar),
            ('不同格式图片上传', self.test_different_image_formats),
            ('长文件名图片上传', self.test_long_filename_upload),
            ('头像显示和存储验证', self.test_avatar_display_and_storage),
        ]
        
        passed_tests = 0
        total_tests = len(tests)
        
        for test_name, test_func in tests:
            try:
                if test_func():
                    passed_tests += 1
            except Exception as e:
                print(f"[✗ 失败] {test_name} - 异常: {str(e)}")
        
        print(f"\n=== 测试完成: {passed_tests}/{total_tests} 通过 ===")
        
        if passed_tests == total_tests:
            print("🎉 所有测试通过！前端注册上传照片功能正常工作。")
        else:
            print("⚠️ 部分测试失败，请检查相关功能。")
        
        # 清理测试数据
        self.cleanup_test_data()
        
        return passed_tests == total_tests

if __name__ == '__main__':
    tester = FrontendPhotoUploadTester()
    tester.run_all_tests()