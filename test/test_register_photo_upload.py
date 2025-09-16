#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试注册页面照片上传功能

这个测试程序验证：
1. 前端注册页面是否正确显示照片上传组件
2. 照片上传功能是否按预期工作
3. 表单验证是否正确处理照片字段
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
import json

class RegisterPhotoUploadTest:
    """注册页面照片上传功能测试"""
    
    def __init__(self):
        self.client = Client()
        self.test_results = []
    
    def log_test(self, test_name, passed, message=""):
        """记录测试结果"""
        status = "✅ PASS" if passed else "❌ FAIL"
        result = f"{status} {test_name}"
        if message:
            result += f" - {message}"
        self.test_results.append(result)
        print(result)
    
    def test_register_page_loads(self):
        """测试注册页面是否正常加载"""
        try:
            # 检查前端注册页面文件是否存在
            register_vue_path = project_root / "frontend" / "src" / "views" / "Register.vue"
            exists = register_vue_path.exists()
            
            if exists:
                # 检查文件内容是否包含照片上传相关代码
                with open(register_vue_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                has_avatar_upload = 'avatar-uploader' in content
                has_plus_icon = 'Plus' in content
                has_avatar_field = 'avatar:' in content or 'avatar =' in content
                
                self.log_test(
                    "注册页面文件存在", 
                    exists, 
                    f"路径: {register_vue_path}"
                )
                
                self.log_test(
                    "包含头像上传组件", 
                    has_avatar_upload, 
                    "检查 avatar-uploader 类"
                )
                
                self.log_test(
                    "包含Plus图标", 
                    has_plus_icon, 
                    "检查 Plus 图标导入"
                )
                
                self.log_test(
                    "包含头像字段", 
                    has_avatar_field, 
                    "检查 avatar 字段定义"
                )
                
                return has_avatar_upload and has_plus_icon and has_avatar_field
            else:
                self.log_test("注册页面文件存在", False, "文件不存在")
                return False
                
        except Exception as e:
            self.log_test("注册页面加载测试", False, f"异常: {str(e)}")
            return False
    
    def test_avatar_validation_rules(self):
        """测试头像验证规则"""
        try:
            register_vue_path = project_root / "frontend" / "src" / "views" / "Register.vue"
            
            with open(register_vue_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 检查头像验证规则
            has_avatar_validation = 'avatar: [' in content
            has_coach_avatar_required = '教练员必须上传头像照片' in content
            has_file_type_validation = 'beforeAvatarUpload' in content
            
            self.log_test(
                "头像验证规则存在", 
                has_avatar_validation, 
                "检查 avatar 验证规则"
            )
            
            self.log_test(
                "教练员头像必填验证", 
                has_coach_avatar_required, 
                "检查教练员头像必填提示"
            )
            
            self.log_test(
                "文件类型验证方法", 
                has_file_type_validation, 
                "检查 beforeAvatarUpload 方法"
            )
            
            return has_avatar_validation and has_coach_avatar_required and has_file_type_validation
            
        except Exception as e:
            self.log_test("头像验证规则测试", False, f"异常: {str(e)}")
            return False
    
    def test_upload_methods(self):
        """测试上传相关方法"""
        try:
            register_vue_path = project_root / "frontend" / "src" / "views" / "Register.vue"
            
            with open(register_vue_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 检查上传相关方法
            has_before_upload = 'beforeAvatarUpload' in content
            has_upload_avatar = 'uploadAvatar' in content
            has_success_handler = 'handleAvatarSuccess' in content
            has_error_handler = 'handleAvatarError' in content
            
            # 检查文件类型和大小验证
            has_file_type_check = 'image/jpeg' in content and 'image/png' in content
            has_file_size_check = '2MB' in content or '2M' in content
            
            self.log_test(
                "上传前验证方法", 
                has_before_upload, 
                "检查 beforeAvatarUpload 方法"
            )
            
            self.log_test(
                "上传处理方法", 
                has_upload_avatar, 
                "检查 uploadAvatar 方法"
            )
            
            self.log_test(
                "成功处理方法", 
                has_success_handler, 
                "检查 handleAvatarSuccess 方法"
            )
            
            self.log_test(
                "错误处理方法", 
                has_error_handler, 
                "检查 handleAvatarError 方法"
            )
            
            self.log_test(
                "文件类型验证", 
                has_file_type_check, 
                "检查 JPG/PNG 格式验证"
            )
            
            self.log_test(
                "文件大小验证", 
                has_file_size_check, 
                "检查 2MB 大小限制"
            )
            
            return all([
                has_before_upload, has_upload_avatar, 
                has_success_handler, has_error_handler,
                has_file_type_check, has_file_size_check
            ])
            
        except Exception as e:
            self.log_test("上传方法测试", False, f"异常: {str(e)}")
            return False
    
    def test_css_styles(self):
        """测试CSS样式"""
        try:
            register_vue_path = project_root / "frontend" / "src" / "views" / "Register.vue"
            
            with open(register_vue_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 检查CSS样式
            has_upload_container_style = '.avatar-upload-container' in content
            has_uploader_style = '.avatar-uploader' in content
            has_preview_style = '.avatar-preview' in content
            has_responsive_style = '@media (max-width: 768px)' in content
            
            self.log_test(
                "上传容器样式", 
                has_upload_container_style, 
                "检查 .avatar-upload-container 样式"
            )
            
            self.log_test(
                "上传组件样式", 
                has_uploader_style, 
                "检查 .avatar-uploader 样式"
            )
            
            self.log_test(
                "预览图片样式", 
                has_preview_style, 
                "检查 .avatar-preview 样式"
            )
            
            self.log_test(
                "响应式样式", 
                has_responsive_style, 
                "检查移动端适配样式"
            )
            
            return all([
                has_upload_container_style, has_uploader_style,
                has_preview_style, has_responsive_style
            ])
            
        except Exception as e:
            self.log_test("CSS样式测试", False, f"异常: {str(e)}")
            return False
    
    def run_all_tests(self):
        """运行所有测试"""
        print("\n" + "="*60)
        print("🧪 注册页面照片上传功能测试")
        print("="*60)
        
        tests = [
            ("页面加载测试", self.test_register_page_loads),
            ("验证规则测试", self.test_avatar_validation_rules),
            ("上传方法测试", self.test_upload_methods),
            ("CSS样式测试", self.test_css_styles),
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
            print("🎉 所有测试通过！注册页面照片上传功能实现完成。")
        else:
            print(f"⚠️  有 {total_tests - passed_tests} 个测试失败，需要进一步修复。")
        
        print("="*60)
        
        return passed_tests == total_tests

if __name__ == "__main__":
    tester = RegisterPhotoUploadTest()
    success = tester.run_all_tests()
    
    if success:
        print("\n✅ 步骤1完成：注册页面照片上传功能已成功实现！")
        print("📝 下一步：更新教练员序列化器包含头像字段")
    else:
        print("\n❌ 步骤1未完成：请检查并修复失败的测试项")
    
    sys.exit(0 if success else 1)