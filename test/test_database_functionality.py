#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
数据库功能测试程序
测试各个应用的数据模型和API功能是否正常
"""

import os
import sys
import django
from datetime import datetime, timedelta

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'keshe.settings')
django.setup()

from accounts.models import User, UserProfile
from notifications.models import Notification
from campus.models import Campus, CampusArea
from courses.models import Course
from reservations.models import Booking, Table, CoachStudentRelation
from payments.models import Payment

def test_user_and_profile():
    """测试用户和用户资料功能"""
    print("\n=== 测试用户和用户资料功能 ===")
    
    try:
        # 检查是否有用户
        users = User.objects.all()
        print(f"用户总数: {users.count()}")
        
        if users.exists():
            user = users.first()
            print(f"第一个用户: {user.username} ({user.email})")
            
            # 检查用户资料
            try:
                profile = user.profile
                print(f"用户资料: 技能={profile.skills}, 经验年数={profile.experience_years}")
            except UserProfile.DoesNotExist:
                print("用户资料不存在，创建默认资料")
                profile = UserProfile.objects.create(
                    user=user,
                    skills="乒乓球基础",
                    experience_years=1
                )
                print(f"已创建用户资料: {profile.skills}")
        else:
            print("没有用户，创建测试用户")
            user = User.objects.create_user(
                username='testuser',
                email='test@example.com',
                password='testpass123'
            )
            profile = UserProfile.objects.create(
                user=user,
                skills="乒乓球基础",
                experience_years=1
            )
            print(f"已创建测试用户: {user.username}")
            
        return True
    except Exception as e:
        print(f"用户测试失败: {e}")
        return False

def test_notifications():
    """测试通知功能"""
    print("\n=== 测试通知功能 ===")
    
    try:
        # 获取用户
        user = User.objects.first()
        if not user:
            print("没有用户，跳过通知测试")
            return False
            
        # 检查通知数量
        notifications = Notification.objects.filter(recipient=user)
        print(f"用户 {user.username} 的通知总数: {notifications.count()}")
        
        # 检查未读通知
        unread_count = notifications.filter(is_read=False).count()
        print(f"未读通知数量: {unread_count}")
        
        # 如果没有通知，创建一些测试通知
        if notifications.count() == 0:
            print("创建测试通知...")
            Notification.objects.create(
                recipient=user,
                title="欢迎使用系统",
                message="这是一条测试通知",
                message_type="system"
            )
            Notification.objects.create(
                recipient=user,
                title="预约提醒",
                message="您有一个预约即将到期",
                message_type="booking"
            )
            print("已创建测试通知")
            
        return True
    except Exception as e:
        print(f"通知测试失败: {e}")
        return False

def test_campus_data():
    """测试校园数据"""
    print("\n=== 测试校园数据 ===")
    
    try:
        # 检查校区
        campuses = Campus.objects.all()
        print(f"校区总数: {campuses.count()}")
        
        if campuses.count() == 0:
            print("创建测试校区...")
            campus = Campus.objects.create(
                name="中心校区",
                code="CENTER",
                campus_type="center",
                address="北京市海淀区",
                phone="010-12345678"
            )
            print(f"已创建校区: {campus.name}")
        else:
            campus = campuses.first()
            print(f"第一个校区: {campus.name}")
            
        # 检查校区分区
        areas = CampusArea.objects.all()
        print(f"校区分区总数: {areas.count()}")
        
        if areas.count() == 0:
            print("创建测试分区...")
            area = CampusArea.objects.create(
                campus=campus,
                name="训练区A",
                area_type="training",
                description="主要训练区域",
                capacity=50
            )
            print(f"已创建分区: {area.name}")
            
        return True
    except Exception as e:
        print(f"校园数据测试失败: {e}")
        return False

def test_courses():
    """测试课程数据"""
    print("\n=== 测试课程数据 ===")
    
    try:
        courses = Course.objects.all()
        print(f"课程总数: {courses.count()}")
        
        if courses.count() == 0:
            print("创建测试课程...")
            user = User.objects.first()
            if user:
                course = Course.objects.create(
                    name="Python程序设计",
                    code="CS101",
                    description="Python编程基础课程",
                    instructor=user,
                    credits=3
                )
                print(f"已创建课程: {course.name}")
            else:
                print("没有用户，无法创建课程")
                
        return True
    except Exception as e:
        print(f"课程测试失败: {e}")
        return False

def test_reservations():
    """测试预约数据"""
    print("\n=== 测试预约数据 ===")
    
    try:
        bookings = Booking.objects.all()
        print(f"预约总数: {bookings.count()}")
        
        # 检查今天的预约
        today_bookings = bookings.filter(
            start_time__date=datetime.now().date()
        )
        print(f"今天的预约数量: {today_bookings.count()}")
        
        # 检查球台数量
        tables = Table.objects.all()
        print(f"球台总数: {tables.count()}")
        
        # 检查师生关系
        relations = CoachStudentRelation.objects.all()
        print(f"师生关系总数: {relations.count()}")
        
        return True
    except Exception as e:
        print(f"预约测试失败: {e}")
        return False

def test_api_endpoints():
    """测试API端点"""
    print("\n=== 测试API端点可访问性 ===")
    
    try:
        from django.test import Client
        from django.contrib.auth import authenticate
        
        client = Client()
        
        # 测试用户登录
        user = User.objects.first()
        if user:
            # 设置用户密码（如果需要）
            user.set_password('testpass123')
            user.save()
            
            # 登录
            login_success = client.login(username=user.username, password='testpass123')
            print(f"用户登录测试: {'成功' if login_success else '失败'}")
            
            if login_success:
                # 测试各个API端点
                endpoints = [
                    '/accounts/api/profile/',
                    '/accounts/api/stats/',
                    '/api/notifications/unread-count/',
                    '/api/notifications/list/',
                ]
                
                for endpoint in endpoints:
                    try:
                        response = client.get(endpoint)
                        print(f"{endpoint}: 状态码 {response.status_code}")
                        if response.status_code == 200:
                            print(f"  响应内容长度: {len(response.content)} 字节")
                    except Exception as e:
                        print(f"{endpoint}: 错误 - {e}")
        
        return True
    except Exception as e:
        print(f"API测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("开始数据库功能测试...")
    print("=" * 50)
    
    tests = [
        test_user_and_profile,
        test_notifications,
        test_campus_data,
        test_courses,
        test_reservations,
        test_api_endpoints
    ]
    
    results = []
    for test_func in tests:
        try:
            result = test_func()
            results.append(result)
        except Exception as e:
            print(f"测试 {test_func.__name__} 出现异常: {e}")
            results.append(False)
    
    print("\n" + "=" * 50)
    print("测试结果汇总:")
    for i, (test_func, result) in enumerate(zip(tests, results)):
        status = "✓ 通过" if result else "✗ 失败"
        print(f"{i+1}. {test_func.__name__}: {status}")
    
    success_count = sum(results)
    total_count = len(results)
    print(f"\n总体结果: {success_count}/{total_count} 个测试通过")
    
    if success_count == total_count:
        print("🎉 所有测试都通过了！")
    else:
        print("⚠️  有测试失败，请检查相关功能")

if __name__ == '__main__':
    main()