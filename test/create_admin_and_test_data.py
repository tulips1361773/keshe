#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
创建管理员账户和测试数据脚本
"""

import os
import sys
import django
from django.contrib.auth import get_user_model

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'keshe.settings')
django.setup()

from accounts.models import User, Coach
from campus.models import Campus

def create_admin_user():
    """创建管理员用户"""
    print("=== 创建管理员用户 ===")
    
    # 创建超级管理员
    if not User.objects.filter(username='admin').exists():
        # 检查手机号是否已存在
        if User.objects.filter(phone='13800000000').exists():
            print("手机号13800000000已存在，跳过创建超级管理员")
        else:
            admin_user = User.objects.create_superuser(
                username='admin',
                email='admin@example.com',
                password='admin123',
                real_name='系统管理员',
                phone='13800000000',
                user_type='super_admin'
            )
            print(f"✅ 创建超级管理员: {admin_user.username}")
    else:
        print("超级管理员已存在")
    
    # 创建校区
    campus, created = Campus.objects.get_or_create(
        name='测试校区',
        defaults={
            'address': '北京市朝阳区测试街道123号',
            'phone': '010-12345678',
            'description': '用于测试的校区'
        }
    )
    if created:
        print(f"✅ 创建校区: {campus.name}")
    else:
        print(f"校区已存在: {campus.name}")
    
    # 创建校区管理员
    if not User.objects.filter(username='campus_admin').exists():
        # 检查手机号是否已存在
        if User.objects.filter(phone='13800000001').exists():
            print("手机号13800000001已存在，跳过创建校区管理员")
        else:
            campus_admin = User.objects.create_user(
                username='campus_admin',
                email='campus_admin@example.com',
                password='admin123',
                real_name='校区管理员',
                phone='13800000001',
                user_type='campus_admin',
                campus=campus,
                is_active=True
            )
            print(f"✅ 创建校区管理员: {campus_admin.username}")
    else:
        print("校区管理员已存在")

def create_test_coach():
    """创建测试教练"""
    print("\n=== 创建测试教练 ===")
    
    campus = Campus.objects.get(name='测试校区')
    
    # 创建待审核的教练
    if not User.objects.filter(username='test_coach').exists():
        # 检查手机号是否已存在
        if User.objects.filter(phone='13800000002').exists():
            print("手机号13800000002已存在，跳过创建测试教练")
            return
            
        coach_user = User.objects.create_user(
            username='test_coach',
            email='coach@example.com',
            password='coach123',
            real_name='测试教练',
            phone='13800000002',
            user_type='coach',
            campus=campus,
            is_active=False  # 待审核状态
        )
        
        # 创建教练资料
        coach_profile = Coach.objects.create(
            user=coach_user,
            coach_level='intermediate',
            hourly_rate=150.00,
            achievements='2023年全国游泳锦标赛第三名，2022年省级比赛冠军',
            max_students=15,
            status='pending'
        )
        
        print(f"✅ 创建待审核教练: {coach_user.username}")
        print(f"   教练级别: {coach_profile.get_coach_level_display()}")
        print(f"   审核状态: {coach_profile.get_status_display()}")
    else:
        print("测试教练已存在")

def main():
    """主函数"""
    try:
        create_admin_user()
        create_test_coach()
        
        print("\n=== 创建完成 ===")
        print("管理员登录信息:")
        print("- 超级管理员: admin / admin123")
        print("- 校区管理员: campus_admin / admin123")
        print("\n测试教练信息:")
        print("- 用户名: test_coach")
        print("- 状态: 待审核")
        print("\n请访问 http://localhost:8000/admin 进行管理")
        
    except Exception as e:
        print(f"❌ 创建过程中出错: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()