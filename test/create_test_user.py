#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import django

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'keshe.settings')
django.setup()

from accounts.models import User
from django.contrib.auth.hashers import make_password

def create_test_user():
    """创建测试用户"""
    print("=== 创建测试用户 ===")
    
    username = 'test_student'
    password = 'test123456'
    email = 'test_student@example.com'
    
    # 检查用户是否已存在
    if User.objects.filter(username=username).exists():
        print(f"用户 {username} 已存在")
        user = User.objects.get(username=username)
    else:
        # 创建新用户
        user = User.objects.create(
            username=username,
            email=email,
            password=make_password(password),
            user_type='student',
            is_active=True
        )
        print(f"✅ 创建用户成功: {username}")
    
    print(f"用户信息:")
    print(f"- 用户名: {user.username}")
    print(f"- 邮箱: {user.email}")
    print(f"- 用户类型: {user.user_type}")
    print(f"- 是否激活: {user.is_active}")
    print(f"- 密码: {password}")
    
    return username, password

if __name__ == '__main__':
    create_test_user()