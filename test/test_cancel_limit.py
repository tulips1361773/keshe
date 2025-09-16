#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试预约取消次数限制功能
"""

import os
import sys
import django
from datetime import datetime, timedelta
from django.utils import timezone

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'keshe.settings')
django.setup()

from accounts.models import User
from reservations.models import Booking, CoachStudentRelation
from campus.models import Campus, Table

def test_monthly_cancel_limit():
    """
    测试每月取消次数限制功能
    """
    print("\n=== 测试每月取消次数限制功能 ===")
    
    try:
        # 1. 创建测试用户
        coach = User.objects.filter(user_type='coach').first()
        student = User.objects.filter(user_type='student').first()
        
        if not coach or not student:
            print("❌ 缺少测试用户，请先创建教练和学员用户")
            return False
            
        print(f"✅ 使用测试用户: 教练={coach.username}, 学员={student.username}")
        
        # 2. 创建师生关系
        relation, created = CoachStudentRelation.objects.get_or_create(
            coach=coach,
            student=student,
            defaults={
                'status': 'approved',
                'applied_by': 'student'
            }
        )
        print(f"✅ 师生关系: {'创建' if created else '已存在'}")
        
        # 3. 获取球台
        campus = Campus.objects.first()
        table = Table.objects.filter(campus=campus).first()
        
        if not table:
            print("❌ 缺少测试球台")
            return False
            
        print(f"✅ 使用球台: {campus.name} - {table.number}号台")
        
        # 4. 清理本月的取消记录
        current_month = timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        cancelled_bookings = Booking.objects.filter(
            relation__student=student,
            cancelled_at__gte=current_month,
            cancelled_by=student
        )
        print(f"✅ 清理本月已有的 {cancelled_bookings.count()} 条取消记录")
        cancelled_bookings.delete()
        
        # 5. 创建4个预约并测试取消
        bookings = []
        for i in range(4):
            start_time = timezone.now() + timedelta(days=i+2, hours=10)  # 确保超过24小时
            end_time = start_time + timedelta(hours=1)
            
            booking = Booking.objects.create(
                relation=relation,
                table=table,
                start_time=start_time,
                end_time=end_time,
                duration_hours=1.0,
                total_fee=100.00,
                status='confirmed'
            )
            bookings.append(booking)
            print(f"✅ 创建预约 {i+1}: {start_time.strftime('%Y-%m-%d %H:%M')}")
        
        # 6. 测试前3次取消（应该成功）
        for i in range(3):
            booking = bookings[i]
            can_cancel, message = booking.can_cancel(student)
            
            if can_cancel:
                booking.status = 'cancelled'
                booking.cancelled_at = timezone.now()
                booking.cancelled_by = student
                booking.cancel_reason = f'测试取消 {i+1}'
                booking.save()
                print(f"✅ 第 {i+1} 次取消成功: {message}")
            else:
                print(f"❌ 第 {i+1} 次取消失败: {message}")
                return False
        
        # 7. 测试第4次取消（应该失败）
        booking = bookings[3]
        can_cancel, message = booking.can_cancel(student)
        
        if not can_cancel and '本月取消次数已达上限' in message:
            print(f"✅ 第4次取消正确被拒绝: {message}")
        else:
            print(f"❌ 第4次取消应该被拒绝，但实际结果: can_cancel={can_cancel}, message={message}")
            return False
        
        # 8. 验证取消次数统计
        from django.db.models import Q
        cancel_count = Booking.objects.filter(
            Q(relation__coach=student) | Q(relation__student=student),
            cancelled_at__gte=current_month,
            cancelled_by=student
        ).count()
        
        if cancel_count == 3:
            print(f"✅ 取消次数统计正确: {cancel_count} 次")
        else:
            print(f"❌ 取消次数统计错误: 期望3次，实际{cancel_count}次")
            return False
        
        print("\n🎉 每月取消次数限制功能测试通过！")
        return True
        
    except Exception as e:
        print(f"❌ 测试过程中出现错误: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_24_hour_limit():
    """
    测试24小时取消限制功能
    """
    print("\n=== 测试24小时取消限制功能 ===")
    
    try:
        # 获取测试用户和关系
        coach = User.objects.filter(user_type='coach').first()
        student = User.objects.filter(user_type='student').first()
        relation = CoachStudentRelation.objects.filter(coach=coach, student=student).first()
        table = Table.objects.first()
        
        # 测试1: 创建一个24小时内的预约（应该不能取消）
        start_time = timezone.now() + timedelta(hours=12)  # 12小时后
        end_time = start_time + timedelta(hours=1)
        
        booking1 = Booking.objects.create(
            relation=relation,
            table=table,
            start_time=start_time,
            end_time=end_time,
            duration_hours=1.0,
            total_fee=100.00,
            status='confirmed'
        )
        
        can_cancel, message = booking1.can_cancel(student)
        if not can_cancel and '距离上课时间不足24小时' in message:
            print(f"✅ 24小时内预约正确被拒绝取消: {message}")
        else:
            print(f"❌ 24小时内预约应该被拒绝取消，但实际: can_cancel={can_cancel}")
            return False
        
        # 测试2: 创建一个24小时外的预约（应该可以取消）
        start_time = timezone.now() + timedelta(hours=48)  # 48小时后
        end_time = start_time + timedelta(hours=1)
        
        booking2 = Booking.objects.create(
            relation=relation,
            table=table,
            start_time=start_time,
            end_time=end_time,
            duration_hours=1.0,
            total_fee=100.00,
            status='confirmed'
        )
        
        can_cancel, message = booking2.can_cancel(student)
        if can_cancel:
            print(f"✅ 24小时外预约可以取消: {message}")
        else:
            print(f"❌ 24小时外预约应该可以取消，但被拒绝: {message}")
            return False
        
        print("\n🎉 24小时取消限制功能测试通过！")
        return True
        
    except Exception as e:
        print(f"❌ 测试过程中出现错误: {str(e)}")
        return False

if __name__ == '__main__':
    print("🏓 开始测试预约取消限制功能")
    
    # 运行测试
    test1_result = test_24_hour_limit()
    test2_result = test_monthly_cancel_limit()
    
    print("\n" + "="*50)
    print("📊 测试结果汇总:")
    print(f"  - 24小时取消限制: {'✅ 通过' if test1_result else '❌ 失败'}")
    print(f"  - 每月取消次数限制: {'✅ 通过' if test2_result else '❌ 失败'}")
    
    if test1_result and test2_result:
        print("\n🎉 所有测试通过！预约取消限制功能正常工作。")
    else:
        print("\n❌ 部分测试失败，请检查相关功能实现。")
        sys.exit(1)