#!/usr/bin/env python
import os
import django

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'keshe.settings')
django.setup()

from django.utils import timezone
from datetime import timedelta
from reservations.models import Booking
from notifications.models import Notification

def test_reminder_function():
    """测试上课提醒功能"""
    print("=== 测试上课提醒功能 ===")
    
    # 1. 查找现有预约
    booking = Booking.objects.filter(relation__student__username='hhm').first()
    if not booking:
        print("❌ 未找到预约记录")
        return False
    
    print(f"✅ 找到预约记录: ID={booking.id}")
    print(f"   学员: {booking.relation.student.username}")
    print(f"   教练: {booking.relation.coach.username}")
    print(f"   原始时间: {booking.start_time}")
    
    # 2. 设置预约时间为1小时后
    now = timezone.now()
    future_time = now + timedelta(hours=1, minutes=2)
    
    booking.start_time = future_time
    booking.end_time = future_time + timedelta(hours=1)
    booking.save()
    
    print(f"✅ 已将预约时间设置为: {future_time}")
    
    # 3. 检查现有通知数量
    before_count = Notification.objects.filter(
        recipient=booking.relation.student,
        message_type='booking'
    ).count()
    print(f"设置前通知数量: {before_count}")
    
    # 4. 运行提醒命令
    from django.core.management import call_command
    print("\n=== 执行提醒命令 ===")
    call_command('send_class_reminders')
    
    # 5. 检查通知是否创建
    after_count = Notification.objects.filter(
        recipient=booking.relation.student,
        message_type='booking'
    ).count()
    print(f"设置后通知数量: {after_count}")
    
    if after_count > before_count:
        print("✅ 提醒功能正常工作，已创建新通知")
        
        # 显示最新通知
        latest_notification = Notification.objects.filter(
            recipient=booking.relation.student,
            message_type='booking'
        ).order_by('-created_at').first()
        
        if latest_notification:
            print(f"最新通知标题: {latest_notification.title}")
            print(f"最新通知内容: {latest_notification.message}")
        
        return True
    else:
        print("❌ 提醒功能可能存在问题，未创建新通知")
        return False

if __name__ == '__main__':
    test_reminder_function()