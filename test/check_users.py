#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import django

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'keshe.settings')
django.setup()

from accounts.models import User

def check_users():
    """检查数据库中的用户"""
    print("=== 检查数据库中的用户 ===")
    
    users = User.objects.all()
    print(f"总用户数: {users.count()}")
    
    print("\n用户列表:")
    for user in users[:10]:  # 只显示前10个用户
        print(f"- 用户名: {user.username}, 邮箱: {user.email}, 用户类型: {user.user_type}, 是否超级用户: {user.is_superuser}")
    
    # 检查是否有超级用户
    superusers = User.objects.filter(is_superuser=True)
    print(f"\n超级用户数: {superusers.count()}")
    if superusers.exists():
        for su in superusers:
            print(f"- 超级用户: {su.username}")
    
    # 检查是否有学员用户
    students = User.objects.filter(user_type='student')
    print(f"\n学员用户数: {students.count()}")
    if students.exists():
        for student in students[:3]:
            print(f"- 学员: {student.username}")

if __name__ == '__main__':
    check_users()