#!/usr/bin/env python
"""
创建测试预约数据脚本
为课程表功能生成测试数据
"""

import os
import sys
import django
from datetime import datetime, timedelta

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'keshe.settings')
django.setup()

from django.contrib.auth import get_user_model
from reservations.models import Booking, CoachStudentRelation, Table
from campus.models import Campus
from django.utils import timezone

User = get_user_model()

def create_test_bookings():
    """创建测试预约数据"""
    print("=== 创建测试预约数据 ===\n")
    
    # 1. 获取测试用户
    try:
        student = User.objects.filter(user_type='student').first()
        coach = User.objects.filter(user_type='coach').first()
        
        if not student or not coach:
            print("❌ 缺少测试用户，请先创建学员和教练用户")
            return
        
        print(f"学员: {student.username}")
        print(f"教练: {coach.username}")
        
    except Exception as e:
        print(f"❌ 获取用户失败: {str(e)}")
        return
    
    # 2. 获取或创建师生关系
    try:
        relation, created = CoachStudentRelation.objects.get_or_create(
            coach=coach,
            student=student,
            defaults={
                'status': 'approved',
                'applied_by': 'student'
            }
        )
        
        if created:
            print(f"✅ 创建师生关系: {coach.username} - {student.username}")
        else:
            print(f"✅ 师生关系已存在: {coach.username} - {student.username}")
            
    except Exception as e:
        print(f"❌ 创建师生关系失败: {str(e)}")
        return
    
    # 3. 获取或创建球台
    try:
        campus = Campus.objects.first()
        if not campus:
            print("❌ 没有找到校区，请先创建校区")
            return
        
        table, created = Table.objects.get_or_create(
            campus=campus,
            number='1',
            defaults={
                'is_active': True,
                'status': 'available'
            }
        )
        
        if created:
            print(f"✅ 创建球台: {table.number}")
        else:
            print(f"✅ 球台已存在: {table.number}")
            
    except Exception as e:
        print(f"❌ 获取球台失败: {str(e)}")
        return
    
    # 4. 创建本周的测试预约
    try:
        now = timezone.now()
        today = now.date()
        
        # 删除现有的未来预约（避免重复）
        future_bookings = Booking.objects.filter(
            relation=relation,
            start_time__date__gte=today
        )
        deleted_count = future_bookings.count()
        future_bookings.delete()
        print(f"✅ 删除了 {deleted_count} 个未来预约")
        
        # 创建从今天开始的预约
        bookings_created = 0
        for i in range(7):  # 创建一周的预约
            booking_date = today + timedelta(days=i)
            
            # 创建当天的预约时间（使用当前时区）
            booking_datetime = datetime.combine(booking_date, datetime.min.time().replace(hour=14, minute=0))
            booking_time = timezone.make_aware(booking_datetime)
            
            # 创建预约
            booking = Booking.objects.create(
                relation=relation,
                table=table,
                start_time=booking_time,
                end_time=booking_time + timedelta(hours=1),
                duration_hours=1.0,
                status='confirmed',
                total_fee=50.00,
                notes=f'测试预约 - {booking_date.strftime("%Y-%m-%d")}'
            )
            
            bookings_created += 1
            print(f"✅ 创建预约: {booking_date} 14:00-15:00")
        
        print(f"\n✅ 总共创建了 {bookings_created} 个测试预约")
        
    except Exception as e:
        print(f"❌ 创建预约失败: {str(e)}")
        return
    
    # 5. 验证创建的数据
    try:
        total_bookings = Booking.objects.filter(relation=relation).count()
        future_bookings = Booking.objects.filter(
            relation=relation,
            start_time__date__gte=today
        ).count()
        
        print(f"\n=== 数据验证 ===")
        print(f"学员总预约数: {total_bookings}")
        print(f"未来预约数: {future_bookings}")
        
        # 显示本周预约详情
        week_bookings = Booking.objects.filter(
            relation=relation,
            start_time__date__gte=today,
            start_time__date__lt=today + timedelta(days=7)
        ).order_by('start_time')
        
        print(f"\n本周预约详情:")
        for booking in week_bookings:
            print(f"  - {booking.start_time.strftime('%Y-%m-%d %H:%M')} - {booking.get_status_display()}")
        
        print(f"\n✅ 测试数据创建完成！")
        
    except Exception as e:
        print(f"❌ 数据验证失败: {str(e)}")

if __name__ == '__main__':
    create_test_bookings()