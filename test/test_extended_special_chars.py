#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试扩展特殊字符的密码验证
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

from accounts.models import User
from accounts.serializers import UserRegistrationSerializer

def test_extended_special_chars():
    """
    测试包含扩展特殊字符的密码验证
    """
    print("=== 测试扩展特殊字符密码验证 ===")
    print()
    
    # 测试用例：包含不同特殊字符的密码
    test_cases = [
        {
            'password': 'Abc12345_',
            'description': '包含下划线(_)',
            'should_pass': True
        },
        {
            'password': 'Abc12345~',
            'description': '包含波浪号(~)',
            'should_pass': True
        },
        {
            'password': 'Abc12345`',
            'description': '包含反引号(`)',
            'should_pass': True
        },
        {
            'password': 'Abc12345-',
            'description': '包含连字符(-)',
            'should_pass': True
        },
        {
            'password': 'Abc12345+',
            'description': '包含加号(+)',
            'should_pass': True
        },
        {
            'password': 'Abc12345=',
            'description': '包含等号(=)',
            'should_pass': True
        },
        {
            'password': 'Abc12345[',
            'description': '包含左方括号([)',
            'should_pass': True
        },
        {
            'password': 'Abc12345]',
            'description': '包含右方括号(])',
            'should_pass': True
        },
        {
            'password': 'Abc12345\\',
            'description': '包含反斜杠(\\)',
            'should_pass': True
        },
        {
            'password': 'Abc12345;',
            'description': '包含分号(;)',
            'should_pass': True
        },
        {
            'password': 'Abc12345/',
            'description': '包含斜杠(/)',
            'should_pass': True
        },
        {
            'password': 'Abc12345中',
            'description': '包含中文字符',
            'should_pass': False
        }
    ]
    
    passed_tests = 0
    total_tests = len(test_cases)
    
    for i, test_case in enumerate(test_cases, 1):
        password = test_case['password']
        description = test_case['description']
        should_pass = test_case['should_pass']
        
        print(f"测试 {i}: {description}")
        print(f"密码: {password}")
        
        # 构造测试数据
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S%f")
        test_data = {
            'username': f'test_user_{timestamp}_{i}',
            'password': password,
            'password_confirm': password,
            'real_name': '测试用户',
            'phone': f'139{timestamp[-8:]}',
            'email': f'test_{timestamp}_{i}@test.com',
            'user_type': 'student'
        }
        
        try:
            # 使用序列化器验证
            serializer = UserRegistrationSerializer(data=test_data)
            is_valid = serializer.is_valid()
            
            if should_pass:
                if is_valid:
                    print("✅ 正确通过验证")
                    passed_tests += 1
                    # 清理创建的用户
                    try:
                        user = serializer.save()
                        user.delete()
                    except:
                        pass
                else:
                    errors = serializer.errors
                    password_errors = errors.get('password', ['未知错误'])
                    print(f"❌ 应该通过但被拒绝: {password_errors[0]}")
                    print(f"   完整错误信息: {errors}")
            else:
                if not is_valid:
                    errors = serializer.errors
                    password_errors = errors.get('password', ['未知错误'])
                    print(f"✅ 正确拒绝: {password_errors[0]}")
                    if 'password' not in errors:
                        print(f"   完整错误信息: {errors}")
                    passed_tests += 1
                else:
                    print("❌ 应该被拒绝但通过了验证")
                    # 清理意外创建的用户
                    try:
                        user = serializer.save()
                        user.delete()
                    except:
                        pass
                        
        except Exception as e:
            if should_pass:
                print(f"❌ 验证过程出错: {str(e)}")
            else:
                print(f"✅ 正确拒绝: {str(e)}")
                passed_tests += 1
        
        print()
    
    print("=" * 50)
    print("扩展特殊字符测试结果汇总")
    print("=" * 50)
    print(f"通过测试: {passed_tests}/{total_tests}")
    
    if passed_tests == total_tests:
        print("🎉 所有扩展特殊字符测试都通过了！")
        return True
    else:
        print(f"⚠️  有 {total_tests - passed_tests} 个测试失败")
        return False

if __name__ == '__main__':
    success = test_extended_special_chars()
    sys.exit(0 if success else 1)