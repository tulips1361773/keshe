#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
获取所有学员和教练的账号密码信息
"""

import os
import django

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'keshe.settings')
django.setup()

from accounts.models import User, UserProfile

def get_all_user_accounts():
    """
    获取所有用户账号信息
    """
    print("=== 乒乓球培训管理系统 - 用户账号信息 ===")
    print()
    
    users = User.objects.all().order_by('id')
    
    if not users:
        print("数据库中没有用户数据")
        return
    
    print(f"共找到 {users.count()} 个用户账号：")
    print()
    
    # 分类显示
    admins = []
    students = []
    coaches = []
    others = []
    
    for user in users:
        user_info = {
            'username': user.username,
            'password': 'testpass123',  # 测试系统统一密码
            'name': user.first_name or user.username,
            'email': user.email or '未设置',
            'role': '未设置',
            'is_active': user.is_active
        }
        
        # 获取用户角色
        if user.is_superuser:
            user_info['role'] = '超级管理员'
            admins.append(user_info)
        elif hasattr(user, 'userprofile'):
            role = user.userprofile.role
            if role == 'student':
                user_info['role'] = '学员'
                students.append(user_info)
            elif role == 'coach':
                user_info['role'] = '教练'
                coaches.append(user_info)
            else:
                user_info['role'] = role or '未设置'
                others.append(user_info)
        else:
            others.append(user_info)
    
    # 显示管理员账号
    if admins:
        print("📋 管理员账号：")
        for admin in admins:
            print(f"  用户名: {admin['username']}")
            print(f"  密码: {admin['password']}")
            print(f"  姓名: {admin['name']}")
            print(f"  角色: {admin['role']}")
            print(f"  状态: {'激活' if admin['is_active'] else '未激活'}")
            print()
    
    # 显示学员账号
    if students:
        print("🎓 学员账号：")
        for i, student in enumerate(students, 1):
            print(f"  {i}. 用户名: {student['username']}")
            print(f"     密码: {student['password']}")
            print(f"     姓名: {student['name']}")
            print(f"     邮箱: {student['email']}")
            print(f"     状态: {'激活' if student['is_active'] else '未激活'}")
            print()
    
    # 显示教练账号
    if coaches:
        print("🏓 教练账号：")
        for i, coach in enumerate(coaches, 1):
            print(f"  {i}. 用户名: {coach['username']}")
            print(f"     密码: {coach['password']}")
            print(f"     姓名: {coach['name']}")
            print(f"     邮箱: {coach['email']}")
            print(f"     状态: {'激活' if coach['is_active'] else '未激活'}")
            print()
    
    # 显示其他账号
    if others:
        print("❓ 其他账号：")
        for other in others:
            print(f"  用户名: {other['username']}")
            print(f"  密码: {other['password']}")
            print(f"  姓名: {other['name']}")
            print(f"  角色: {other['role']}")
            print(f"  状态: {'激活' if other['is_active'] else '未激活'}")
            print()
    
    # 统计信息
    print("📊 统计信息：")
    print(f"  管理员: {len(admins)} 个")
    print(f"  学员: {len(students)} 个")
    print(f"  教练: {len(coaches)} 个")
    print(f"  其他: {len(others)} 个")
    print(f"  总计: {len(admins) + len(students) + len(coaches) + len(others)} 个")
    
    print()
    print("💡 使用说明：")
    print("  1. 所有测试账号的密码都是: testpass123")
    print("  2. 管理员可以访问Django后台管理")
    print("  3. 学员和教练可以登录前端系统")
    print("  4. 前端登录地址: http://localhost:3002/login")
    print("  5. 后台管理地址: http://127.0.0.1:8000/admin/")

if __name__ == '__main__':
    get_all_user_accounts()