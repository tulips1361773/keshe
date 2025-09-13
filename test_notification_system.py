#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
师生关系申请通知功能测试脚本
测试学员申请教练时是否会通知教练
"""

import os
import sys
import django

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'keshe.settings')
django.setup()

from django.test import Client
from rest_framework.test import APIClient
from accounts.models import User
from reservations.models import CoachStudentRelation
from notifications.models import Notification

def test_notification_system():
    """
    测试师生关系申请通知系统
    """
    print("=== 师生关系申请通知系统测试 ===")
    
    # 1. 获取测试用户
    print("\n1. 获取测试用户...")
    try:
        # 使用现有的测试用户
        student = User.objects.get(username='student1757668378102')
        coach = User.objects.get(username='coach08')
        print(f"✓ 学员: {student.username} ({student.real_name})")
        print(f"✓ 教练: {coach.username} ({coach.real_name})")
    except User.DoesNotExist as e:
        print(f"✗ 获取测试用户失败: {e}")
        return False
    
    # 2. 清理之前的测试数据
    print("\n2. 清理测试数据...")
    old_relations = CoachStudentRelation.objects.filter(student=student, coach=coach)
    if old_relations.exists():
        old_relations.delete()
        print("✓ 清理了之前的师生关系")
    
    old_notifications = Notification.objects.filter(
        recipient=coach,
        data__student_id=student.id
    )
    if old_notifications.exists():
        old_notifications.delete()
        print("✓ 清理了之前的通知")
    
    # 3. 记录通知基准数量
    initial_coach_notifications = Notification.objects.filter(recipient=coach).count()
    initial_student_notifications = Notification.objects.filter(recipient=student).count()
    print(f"✓ 教练初始通知数: {initial_coach_notifications}")
    print(f"✓ 学员初始通知数: {initial_student_notifications}")
    
    # 4. 模拟学员申请教练
    print("\n3. 模拟学员申请教练...")
    
    client = APIClient()
    client.force_authenticate(user=student)
    
    # 申请数据
    apply_data = {
        'coach_id': coach.id,
        'notes': '希望能成为您的学员，请多指教！'
    }
    
    # 发送申请请求
    response = client.post('/api/reservations/relations/', apply_data, format='json')
    
    if response.status_code == 201:
        print("✓ 学员申请提交成功")
        relation_data = response.data
        relation_id = relation_data['id']
        print(f"  师生关系ID: {relation_id}")
        print(f"  申请状态: {relation_data.get('status', 'unknown')}")
    else:
        print(f"✗ 学员申请失败: {response.status_code}")
        if hasattr(response, 'data'):
            print(f"  错误信息: {response.data}")
        return False
    
    # 5. 检查教练是否收到通知
    print("\n4. 检查教练通知...")
    
    # 查找教练收到的新通知
    coach_notifications = Notification.objects.filter(
        recipient=coach,
        data__relation_id=relation_id
    )
    
    if coach_notifications.exists():
        notification = coach_notifications.first()
        print("✅ 教练收到申请通知")
        print(f"  标题: {notification.title}")
        print(f"  内容: {notification.message}")
        print(f"  类型: {notification.message_type}")
        print(f"  时间: {notification.created_at}")
        print(f"  已读: {'是' if notification.is_read else '否'}")
        
        if notification.data:
            print(f"  数据: {notification.data}")
    else:
        print("❌ 教练未收到申请通知")
        # 检查是否有其他相关通知
        all_coach_notifications = Notification.objects.filter(recipient=coach).order_by('-created_at')[:3]
        print("  教练最近的通知:")
        for notif in all_coach_notifications:
            print(f"    - {notif.title}: {notif.message}")
    
    # 6. 测试教练审核功能
    print("\n5. 测试教练审核...")
    
    client.force_authenticate(user=coach)
    approve_response = client.post(f'/api/reservations/relations/{relation_id}/approve/')
    
    if approve_response.status_code == 200:
        print("✓ 教练审核成功")
        
        # 检查学员是否收到审核结果通知
        student_notifications = Notification.objects.filter(
            recipient=student,
            data__relation_id=relation_id,
            data__type='relation_approved'
        )
        
        if student_notifications.exists():
            student_notif = student_notifications.first()
            print("✅ 学员收到审核结果通知")
            print(f"  标题: {student_notif.title}")
            print(f"  内容: {student_notif.message}")
        else:
            print("❌ 学员未收到审核结果通知")
    else:
        print(f"✗ 教练审核失败: {approve_response.status_code}")
        if hasattr(approve_response, 'data'):
            print(f"  错误信息: {approve_response.data}")
    
    # 7. 最终统计
    print("\n6. 通知统计...")
    
    final_coach_notifications = Notification.objects.filter(recipient=coach).count()
    final_student_notifications = Notification.objects.filter(recipient=student).count()
    
    coach_new_count = final_coach_notifications - initial_coach_notifications
    student_new_count = final_student_notifications - initial_student_notifications
    
    print(f"  教练新增通知: {coach_new_count}")
    print(f"  学员新增通知: {student_new_count}")
    
    # 8. 显示测试结果
    print("\n=== 测试结果 ===")
    
    if coach_new_count > 0:
        print("✅ 学员申请教练时，教练能收到通知 - 功能正常")
    else:
        print("❌ 学员申请教练时，教练未收到通知 - 功能异常")
    
    if student_new_count > 0:
        print("✅ 教练审核后，学员能收到通知 - 功能正常")
    else:
        print("❌ 教练审核后，学员未收到通知 - 功能异常")
    
    return True

if __name__ == '__main__':
    try:
        test_notification_system()
    except Exception as e:
        print(f"\n❌ 测试过程中发生错误: {e}")
        import traceback
        traceback.print_exc()