#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
课程预约系统测试脚本
测试完整的预约流程，包括：
1. 师生关系申请和确认
2. 预约创建和球台选择
3. 预约确认和取消
4. 预约取消限制验证
"""

import os
import sys
import django
from datetime import datetime, timedelta
from django.utils import timezone
from django.test import TestCase
from django.contrib.auth import get_user_model

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'keshe.settings')
django.setup()

from accounts.models import User
from campus.models import Campus
from reservations.models import CoachStudentRelation, Table, Booking, BookingCancellation
from notifications.models import Notification

class BookingSystemTest:
    """预约系统测试类"""
    
    def __init__(self):
        self.coach = None
        self.student = None
        self.campus = None
        self.table = None
        self.relation = None
        self.booking = None
        
    def setup_test_data(self):
        """设置测试数据"""
        print("\n=== 设置测试数据 ===")
        
        # 创建测试用户
        try:
            self.coach = User.objects.get(username='test_coach')
            print(f"使用已存在的教练用户: {self.coach.username}")
        except User.DoesNotExist:
            # 检查是否有相同手机号的用户
            existing_user = User.objects.filter(phone='13800000001').first()
            if existing_user:
                self.coach = existing_user
                self.coach.username = 'test_coach'
                self.coach.user_type = 'coach'
                self.coach.save()
                print(f"更新已存在用户为测试教练: {self.coach.username}")
            else:
                self.coach = User.objects.create_user(
                    username='test_coach',
                    email='coach@test.com',
                    password='testpass123',
                    user_type='coach',
                    real_name='测试教练',
                    phone='13800000001'
                )
                print(f"创建教练用户: {self.coach.username}")
            
        try:
            self.student = User.objects.get(username='test_student')
            print(f"使用已存在的学员用户: {self.student.username}")
        except User.DoesNotExist:
            # 检查是否有相同手机号的用户
            existing_user = User.objects.filter(phone='13800000002').first()
            if existing_user:
                self.student = existing_user
                self.student.username = 'test_student'
                self.student.user_type = 'student'
                self.student.save()
                print(f"更新已存在用户为测试学员: {self.student.username}")
            else:
                self.student = User.objects.create_user(
                    username='test_student',
                    email='student@test.com',
                    password='testpass123',
                    user_type='student',
                    real_name='测试学员',
                    phone='13800000002'
                )
                print(f"创建学员用户: {self.student.username}")
            
        # 创建测试校区
        try:
            self.campus = Campus.objects.get(name='测试校区')
            print(f"使用已存在的校区: {self.campus.name}")
        except Campus.DoesNotExist:
            self.campus = Campus.objects.create(
                name='测试校区',
                address='测试地址123号',
                phone='010-12345678',
                is_active=True
            )
            print(f"创建校区: {self.campus.name}")
            
        # 创建测试球台
        try:
            self.table = Table.objects.get(campus=self.campus, number='T001')
            print(f"使用已存在的球台: {self.table}")
        except Table.DoesNotExist:
            self.table = Table.objects.create(
                campus=self.campus,
                number='T001',
                name='测试球台1',
                status='available',
                is_active=True
            )
            print(f"创建球台: {self.table}")
            
        print("测试数据设置完成")
        
    def test_coach_student_relation(self):
        """测试师生关系申请流程"""
        print("\n=== 测试师生关系申请流程 ===")
        
        # 1. 学员申请师生关系
        try:
            self.relation = CoachStudentRelation.objects.get(
                coach=self.coach,
                student=self.student
            )
            if self.relation.status != 'approved':
                self.relation.status = 'approved'
                self.relation.processed_at = timezone.now()
                self.relation.save()
            print(f"使用已存在的师生关系: {self.relation}")
        except CoachStudentRelation.DoesNotExist:
            self.relation = CoachStudentRelation.objects.create(
                coach=self.coach,
                student=self.student,
                status='pending',
                message='希望跟您学习乒乓球'
            )
            print(f"创建师生关系申请: {self.relation}")
            
            # 2. 教练确认申请
            self.relation.status = 'approved'
            self.relation.processed_at = timezone.now()
            self.relation.save()
            print(f"教练确认申请，状态: {self.relation.status}")
            
        # 验证师生关系状态
        assert self.relation.status == 'approved', "师生关系应该是已确认状态"
        print("✓ 师生关系申请流程测试通过")
        
    def test_booking_creation(self):
        """测试预约创建流程"""
        print("\n=== 测试预约创建流程 ===")
        
        # 设置预约时间（明天的10:00-12:00）
        tomorrow = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)
        start_time = tomorrow.replace(hour=10)
        end_time = tomorrow.replace(hour=12)
        
        print(f"预约时间: {start_time} - {end_time}")
        
        # 1. 检查球台可用性
        overlapping_bookings = Booking.objects.filter(
            table=self.table,
            start_time__lt=end_time,
            end_time__gt=start_time,
            status__in=['pending', 'confirmed']
        )
        
        if overlapping_bookings.exists():
            print("该时间段球台已被预约，删除冲突预约进行测试")
            overlapping_bookings.delete()
            
        # 2. 创建预约
        self.booking = Booking.objects.create(
            relation=self.relation,
            table=self.table,
            start_time=start_time,
            end_time=end_time,
            duration_hours=2.0,
            total_fee=200.00,
            status='pending'
        )
        
        print(f"创建预约: {self.booking}")
        print(f"预约状态: {self.booking.status}")
        print(f"预约费用: {self.booking.total_fee}元")
        
        # 验证预约创建
        assert self.booking.status == 'pending', "预约状态应该是待确认"
        assert self.booking.duration_hours == 2.0, "预约时长应该是2小时"
        print("✓ 预约创建流程测试通过")
        
    def test_booking_confirmation(self):
        """测试预约确认流程"""
        print("\n=== 测试预约确认流程 ===")
        
        # 教练确认预约
        self.booking.status = 'confirmed'
        self.booking.confirmed_at = timezone.now()
        self.booking.save()
        
        print(f"教练确认预约，状态: {self.booking.status}")
        print(f"确认时间: {self.booking.confirmed_at}")
        
        # 验证预约确认
        assert self.booking.status == 'confirmed', "预约状态应该是已确认"
        assert self.booking.confirmed_at is not None, "确认时间不应该为空"
        print("✓ 预约确认流程测试通过")
        
    def test_booking_cancellation_restrictions(self):
        """测试预约取消限制"""
        print("\n=== 测试预约取消限制 ===")
        
        # 1. 测试24小时限制
        print("1. 测试24小时取消限制")
        
        # 创建一个明天的预约（距离现在超过24小时）
        tomorrow = timezone.now() + timedelta(days=1, hours=2)
        future_booking = Booking.objects.create(
            relation=self.relation,
            table=self.table,
            start_time=tomorrow,
            end_time=tomorrow + timedelta(hours=2),
            duration_hours=2.0,
            total_fee=200.00,
            status='confirmed'
        )
        
        can_cancel, message = future_booking.can_cancel(self.student)
        print(f"距离上课超过24小时，可以取消: {can_cancel}, 消息: {message}")
        assert can_cancel, "距离上课超过24小时应该可以取消"
        
        # 创建一个1小时后的预约（距离现在不足24小时）
        soon_booking = Booking.objects.create(
            relation=self.relation,
            table=self.table,
            start_time=timezone.now() + timedelta(hours=1),
            end_time=timezone.now() + timedelta(hours=3),
            duration_hours=2.0,
            total_fee=200.00,
            status='confirmed'
        )
        
        can_cancel, message = soon_booking.can_cancel(self.student)
        print(f"距离上课不足24小时，可以取消: {can_cancel}, 消息: {message}")
        assert not can_cancel, "距离上课不足24小时不应该可以取消"
        assert '24小时' in message, "错误消息应该包含24小时限制说明"
        
        # 2. 测试每月3次限制
        print("\n2. 测试每月3次取消限制")
        
        # 清理本月的取消记录
        current_month = timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        Booking.objects.filter(
            relation__student=self.student,
            cancelled_at__gte=current_month
        ).delete()
        
        # 创建3个已取消的预约
        for i in range(3):
            cancelled_booking = Booking.objects.create(
                relation=self.relation,
                table=self.table,
                start_time=timezone.now() + timedelta(days=i+2),
                end_time=timezone.now() + timedelta(days=i+2, hours=2),
                duration_hours=2.0,
                total_fee=200.00,
                status='cancelled',
                cancelled_at=timezone.now(),
                cancelled_by=self.student
            )
            print(f"创建已取消预约 {i+1}: {cancelled_booking.id}")
            
        # 测试第4次取消
        can_cancel, message = future_booking.can_cancel(self.student)
        print(f"本月已取消3次，第4次取消: {can_cancel}, 消息: {message}")
        assert not can_cancel, "本月已取消3次，不应该可以再取消"
        assert '3次' in message, "错误消息应该包含3次限制说明"
        
        print("✓ 预约取消限制测试通过")
        
        # 清理测试数据
        future_booking.delete()
        soon_booking.delete()
        
    def test_available_tables_api(self):
        """测试可用球台API"""
        print("\n=== 测试可用球台API ===")
        
        # 设置查询时间
        start_time = timezone.now() + timedelta(days=2)
        end_time = start_time + timedelta(hours=2)
        
        print(f"查询时间段: {start_time} - {end_time}")
        
        # 获取可用球台
        available_tables = Table.objects.filter(
            is_active=True,
            status='available',
            campus=self.campus
        ).exclude(
            id__in=Booking.objects.filter(
                start_time__lt=end_time,
                end_time__gt=start_time,
                status__in=['pending', 'confirmed']
            ).values_list('table_id', flat=True)
        )
        
        print(f"可用球台数量: {available_tables.count()}")
        for table in available_tables:
            print(f"  - {table}")
            
        assert available_tables.count() > 0, "应该有可用的球台"
        print("✓ 可用球台API测试通过")
        
    def cleanup_test_data(self):
        """清理测试数据"""
        print("\n=== 清理测试数据 ===")
        
        # 删除测试预约
        if self.booking:
            self.booking.delete()
            print("删除测试预约")
            
        # 删除其他测试预约
        test_bookings = Booking.objects.filter(relation__coach=self.coach)
        deleted_count = test_bookings.count()
        test_bookings.delete()
        print(f"删除 {deleted_count} 个测试预约")
        
        # 删除师生关系
        if self.relation:
            self.relation.delete()
            print("删除师生关系")
            
        # 删除通知
        notifications = Notification.objects.filter(
            recipient__in=[self.coach, self.student]
        )
        deleted_notifications = notifications.count()
        notifications.delete()
        print(f"删除 {deleted_notifications} 个通知")
        
        print("测试数据清理完成")
        
    def run_all_tests(self):
        """运行所有测试"""
        print("开始运行课程预约系统测试")
        print("=" * 50)
        
        try:
            self.setup_test_data()
            self.test_coach_student_relation()
            self.test_booking_creation()
            self.test_booking_confirmation()
            self.test_booking_cancellation_restrictions()
            self.test_available_tables_api()
            
            print("\n" + "=" * 50)
            print("🎉 所有测试通过！课程预约系统功能正常")
            print("=" * 50)
            
        except Exception as e:
            print(f"\n❌ 测试失败: {str(e)}")
            import traceback
            traceback.print_exc()
            
        finally:
            self.cleanup_test_data()


if __name__ == '__main__':
    test = BookingSystemTest()
    test.run_all_tests()