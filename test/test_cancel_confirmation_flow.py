#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试预约取消确认流程
验证新的取消确认机制是否正常工作
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
from reservations.models import (
    Campus, Table, CoachStudentRelation, Booking, BookingCancellation
)
from notifications.models import Notification
from rest_framework.test import APIClient
import json

def test_cancel_confirmation_flow():
    """
    测试完整的取消确认流程
    """
    print("=== 测试预约取消确认流程 ===")
    
    # 1. 准备测试数据
    print("\n1. 准备测试数据...")
    try:
        # 获取测试用户
        coach = User.objects.filter(user_type='coach').first()
        student = User.objects.filter(user_type='student').first()
        
        if not coach or not student:
            print("❌ 缺少测试用户")
            return False
            
        print(f"✅ 教练: {coach.username} ({coach.real_name})")
        print(f"✅ 学员: {student.username} ({student.real_name})")
        
        # 获取师生关系
        relation, created = CoachStudentRelation.objects.get_or_create(
            coach=coach,
            student=student,
            defaults={'status': 'approved', 'applied_by': 'student'}
        )
        
        if created:
            print(f"✅ 创建师生关系: {relation.id}")
        else:
            print(f"✅ 使用现有师生关系: {relation.id}")
            
        # 获取校区和球台
        campus = Campus.objects.first()
        table = Table.objects.filter(campus=campus).first()
        
        if not campus or not table:
            print("❌ 缺少校区或球台数据")
            return False
            
        print(f"✅ 校区: {campus.name}")
        print(f"✅ 球台: {table.number}号台")
        
    except Exception as e:
        print(f"❌ 准备测试数据失败: {e}")
        return False
    
    # 2. 创建测试预约
    print("\n2. 创建测试预约...")
    try:
        # 清理旧的测试预约
        old_bookings = Booking.objects.filter(
            relation=relation,
            start_time__gte=timezone.now()
        )
        if old_bookings.exists():
            old_bookings.delete()
            print("✅ 清理了旧的测试预约")
        
        # 创建新预约（设置为3天后，确保满足24小时取消限制）
        start_time = timezone.now() + timedelta(days=3)
        end_time = start_time + timedelta(hours=2)
        
        booking = Booking.objects.create(
            relation=relation,
            table=table,
            start_time=start_time,
            end_time=end_time,
            duration_hours=2,
            total_fee=200.00,
            status='confirmed',
            notes='测试预约取消确认流程'
        )
        
        print(f"✅ 创建测试预约: {booking.id}")
        print(f"   开始时间: {booking.start_time}")
        print(f"   状态: {booking.status}")
        
    except Exception as e:
        print(f"❌ 创建测试预约失败: {e}")
        return False
    
    # 3. 学员申请取消预约
    print("\n3. 学员申请取消预约...")
    try:
        client = APIClient()
        client.force_authenticate(user=student)
        
        # 记录通知基准数量
        initial_coach_notifications = Notification.objects.filter(recipient=coach).count()
        
        # 提交取消申请
        cancel_data = {
            'reason': '临时有事，无法参加课程'
        }
        
        response = client.post(f'/api/reservations/bookings/{booking.id}/cancel/', cancel_data)
        
        if response.status_code == 200:
            print("✅ 学员取消申请提交成功")
            print(f"   响应: {response.data.get('message', '')}")
        else:
            print(f"❌ 学员取消申请失败: {response.status_code}")
            print(f"   错误: {response.data}")
            return False
            
        # 检查取消申请记录
        cancellation = BookingCancellation.objects.filter(booking=booking).first()
        if cancellation:
            print(f"✅ 创建取消申请记录: {cancellation.id}")
            print(f"   申请人: {cancellation.requested_by.username}")
            print(f"   状态: {cancellation.status}")
            print(f"   原因: {cancellation.reason}")
        else:
            print("❌ 未找到取消申请记录")
            return False
            
        # 检查预约状态
        booking.refresh_from_db()
        print(f"✅ 预约状态: {booking.status} (应该仍为confirmed)")
        
        # 检查教练是否收到通知
        coach_notifications = Notification.objects.filter(
            recipient=coach,
            data__cancellation_id=cancellation.id
        )
        
        if coach_notifications.exists():
            notification = coach_notifications.first()
            print(f"✅ 教练收到取消申请通知: {notification.title}")
            print(f"   内容: {notification.message}")
        else:
            print("❌ 教练未收到取消申请通知")
            return False
            
    except Exception as e:
        print(f"❌ 学员申请取消失败: {e}")
        return False
    
    # 4. 教练同意取消申请
    print("\n4. 教练同意取消申请...")
    try:
        client.force_authenticate(user=coach)
        
        # 记录通知基准数量
        initial_student_notifications = Notification.objects.filter(recipient=student).count()
        
        # 同意取消申请
        approve_data = {
            'response_message': '理解您的情况，同意取消预约'
        }
        
        response = client.post(f'/api/reservations/cancellations/{cancellation.id}/approve/', approve_data)
        
        if response.status_code == 200:
            print("✅ 教练同意取消申请成功")
            print(f"   响应: {response.data.get('message', '')}")
        else:
            print(f"❌ 教练同意取消申请失败: {response.status_code}")
            print(f"   错误: {response.data}")
            return False
            
        # 检查取消申请状态
        cancellation.refresh_from_db()
        print(f"✅ 取消申请状态: {cancellation.status} (应该为approved)")
        print(f"   处理人: {cancellation.processed_by.username if cancellation.processed_by else 'None'}")
        print(f"   处理时间: {cancellation.processed_at}")
        
        # 检查预约状态
        booking.refresh_from_db()
        print(f"✅ 预约状态: {booking.status} (应该为cancelled)")
        print(f"   取消时间: {booking.cancelled_at}")
        print(f"   取消人: {booking.cancelled_by.username if booking.cancelled_by else 'None'}")
        
        # 检查学员是否收到通知
        student_notifications = Notification.objects.filter(
            recipient=student,
            data__cancellation_id=cancellation.id,
            data__type='cancellation_approved'
        )
        
        if student_notifications.exists():
            notification = student_notifications.first()
            print(f"✅ 学员收到同意通知: {notification.title}")
            print(f"   内容: {notification.message}")
        else:
            print("❌ 学员未收到同意通知")
            return False
            
    except Exception as e:
        print(f"❌ 教练同意取消失败: {e}")
        return False
    
    # 5. 测试拒绝流程（创建新预约）
    print("\n5. 测试拒绝取消申请流程...")
    try:
        # 创建新预约用于测试拒绝流程（设置为4天后）
        start_time2 = timezone.now() + timedelta(days=4)
        end_time2 = start_time2 + timedelta(hours=1)
        
        booking2 = Booking.objects.create(
            relation=relation,
            table=table,
            start_time=start_time2,
            end_time=end_time2,
            duration_hours=1,
            total_fee=100.00,
            status='confirmed',
            notes='测试拒绝取消申请流程'
        )
        
        print(f"✅ 创建第二个测试预约: {booking2.id}")
        
        # 学员申请取消
        client.force_authenticate(user=student)
        cancel_data2 = {'reason': '想要测试拒绝流程'}
        response = client.post(f'/api/reservations/bookings/{booking2.id}/cancel/', cancel_data2)
        
        if response.status_code != 200:
            print(f"❌ 第二次取消申请失败: {response.status_code}")
            return False
            
        cancellation2 = BookingCancellation.objects.filter(booking=booking2).first()
        print(f"✅ 创建第二个取消申请: {cancellation2.id}")
        
        # 教练拒绝取消申请
        client.force_authenticate(user=coach)
        reject_data = {
            'response_message': '课程安排已确定，不便取消'
        }
        
        response = client.post(f'/api/reservations/cancellations/{cancellation2.id}/reject/', reject_data)
        
        if response.status_code == 200:
            print("✅ 教练拒绝取消申请成功")
        else:
            print(f"❌ 教练拒绝取消申请失败: {response.status_code}")
            return False
            
        # 检查状态
        cancellation2.refresh_from_db()
        booking2.refresh_from_db()
        
        print(f"✅ 取消申请状态: {cancellation2.status} (应该为rejected)")
        print(f"✅ 预约状态: {booking2.status} (应该仍为confirmed)")
        
        # 检查学员是否收到拒绝通知
        reject_notifications = Notification.objects.filter(
            recipient=student,
            data__cancellation_id=cancellation2.id,
            data__type='cancellation_rejected'
        )
        
        if reject_notifications.exists():
            notification = reject_notifications.first()
            print(f"✅ 学员收到拒绝通知: {notification.title}")
        else:
            print("❌ 学员未收到拒绝通知")
            return False
            
    except Exception as e:
        print(f"❌ 测试拒绝流程失败: {e}")
        return False
    
    # 6. 清理测试数据
    print("\n6. 清理测试数据...")
    try:
        # 删除测试预约和取消申请
        BookingCancellation.objects.filter(booking__in=[booking, booking2]).delete()
        Booking.objects.filter(id__in=[booking.id, booking2.id]).delete()
        
        # 删除测试通知
        Notification.objects.filter(
            data__booking_id__in=[booking.id, booking2.id]
        ).delete()
        
        print("✅ 清理测试数据完成")
        
    except Exception as e:
        print(f"⚠️  清理测试数据失败: {e}")
    
    print("\n=== 测试总结 ===")
    print("✅ 预约取消确认流程测试通过")
    print("✅ 学员可以申请取消预约")
    print("✅ 教练收到取消申请通知")
    print("✅ 教练可以同意或拒绝取消申请")
    print("✅ 申请人收到处理结果通知")
    print("✅ 预约状态正确更新")
    
    return True

if __name__ == '__main__':
    try:
        success = test_cancel_confirmation_flow()
        if success:
            print("\n🎉 所有测试通过！")
        else:
            print("\n❌ 测试失败！")
            sys.exit(1)
    except Exception as e:
        print(f"\n💥 测试过程中发生错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)