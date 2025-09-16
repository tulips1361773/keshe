#!/usr/bin/env python
"""
创建教练更换系统测试数据
"""

import os
import sys
import django

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'keshe.settings')
django.setup()

from django.contrib.auth import get_user_model
from reservations.models import CoachStudentRelation

User = get_user_model()

def create_test_data():
    """创建测试数据"""
    print("开始创建测试数据...")
    
    # 创建测试学员
    student, created = User.objects.get_or_create(
        username='test_student',
        defaults={
            'user_type': 'student',
            'first_name': '测试',
            'last_name': '学员',
            'email': 'test_student@example.com',
            'phone': '13800000001'
        }
    )
    if created:
        student.set_password('testpass123')
        student.save()
        print(f'✅ 创建测试学员: {student.username}')
    else:
        print(f'ℹ️ 测试学员已存在: {student.username}')
    
    # 创建测试教练1（当前教练）
    coach1, created = User.objects.get_or_create(
        username='test_coach1',
        defaults={
            'user_type': 'coach',
            'first_name': '测试',
            'last_name': '教练1',
            'email': 'test_coach1@example.com',
            'phone': '13800000002'
        }
    )
    if created:
        coach1.set_password('testpass123')
        coach1.save()
        print(f'✅ 创建测试教练1: {coach1.username}')
    else:
        print(f'ℹ️ 测试教练1已存在: {coach1.username}')
    
    # 创建测试教练2（目标教练）
    coach2, created = User.objects.get_or_create(
        username='test_coach2',
        defaults={
            'user_type': 'coach',
            'first_name': '测试',
            'last_name': '教练2',
            'email': 'test_coach2@example.com',
            'phone': '13800000003'
        }
    )
    if created:
        coach2.set_password('testpass123')
        coach2.save()
        print(f'✅ 创建测试教练2: {coach2.username}')
    else:
        print(f'ℹ️ 测试教练2已存在: {coach2.username}')
    
    # 创建管理员
    admin, created = User.objects.get_or_create(
        username='test_admin',
        defaults={
            'user_type': 'campus_admin',
            'first_name': '测试',
            'last_name': '管理员',
            'email': 'test_admin@example.com',
            'phone': '13800000004',
            'is_staff': True,
            'is_superuser': True
        }
    )
    if created:
        admin.set_password('testpass123')
        admin.save()
        print(f'✅ 创建测试管理员: {admin.username}')
    else:
        print(f'ℹ️ 测试管理员已存在: {admin.username}')
    
    # 创建师生关系
    relation, created = CoachStudentRelation.objects.get_or_create(
        student=student,
        coach=coach1,
        defaults={'status': 'approved'}
    )
    if created:
        print(f'✅ 创建师生关系: {student.username} -> {coach1.username}')
    else:
        print(f'ℹ️ 师生关系已存在: {student.username} -> {coach1.username}')
    
    print("测试数据创建完成！")
    print("\n测试账号信息:")
    print(f"学员: test_student / testpass123")
    print(f"教练1: test_coach1 / testpass123")
    print(f"教练2: test_coach2 / testpass123")
    print(f"管理员: test_admin / testpass123")

if __name__ == '__main__':
    create_test_data()