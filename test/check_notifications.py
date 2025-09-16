#!/usr/bin/env python
import os
import django

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'keshe.settings')
django.setup()

from notifications.models import Notification
from accounts.models import User

def check_notifications():
    """检查通知是否创建成功"""
    print("=== 检查通知创建情况 ===")
    
    # 查找学员
    try:
        student = User.objects.get(username='hhm')
        print(f"✅ 找到学员: {student.username}")
    except User.DoesNotExist:
        print("❌ 未找到学员")
        return
    
    # 查找预约相关通知
    notifications = Notification.objects.filter(
        recipient=student,
        message_type='booking'
    ).order_by('-created_at')
    
    print(f"学员预约通知总数: {notifications.count()}")
    
    if notifications.exists():
        print("\n=== 最新通知详情 ===")
        latest = notifications.first()
        print(f"标题: {latest.title}")
        print(f"内容: {latest.message}")
        print(f"创建时间: {latest.created_at}")
        print(f"是否已读: {latest.is_read}")
        
        # 检查是否是上课提醒
        if latest.data and 'class_reminder' in str(latest.data):
            print("✅ 确认是上课提醒通知")
        else:
            print("⚠️ 不是上课提醒通知")
            
        return True
    else:
        print("❌ 未找到任何预约通知")
        return False

if __name__ == '__main__':
    check_notifications()