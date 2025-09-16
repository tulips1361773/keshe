#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试教练通知功能
检查教练是否能正确接收到学员申请的通知
"""

import os
import sys
import django
from django.conf import settings

# 添加项目路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'keshe.settings')
django.setup()

from accounts.models import User, Coach
from notifications.models import Notification
from reservations.models import CoachStudentRelation
from rest_framework.test import APIClient

def test_coach_notifications():
    """测试教练通知功能"""
    print("=== 教练通知功能测试 ===")
    
    # 1. 查找现有的教练和学员
    try:
        # 查找教练用户（通过Coach模型）
        coach_obj = Coach.objects.first()
        if coach_obj:
            coach_user = coach_obj.user
        else:
            coach_user = None
            
        # 查找学员用户（非教练用户）
        if coach_user:
            student_user = User.objects.exclude(id=coach_user.id).first()
        else:
            student_user = User.objects.first()
        
        if not coach_user:
            print("❌ 未找到教练用户")
            return False
            
        if not student_user:
            print("❌ 未找到学员用户")
            return False
            
        print(f"✓ 找到教练: {coach_user.username} (ID: {coach_user.id})")
        print(f"✓ 找到学员: {student_user.username} (ID: {student_user.id})")
        
    except Exception as e:
        print(f"❌ 查找用户失败: {e}")
        return False
    
    # 2. 检查教练的当前通知
    print("\n=== 检查教练当前通知 ===")
    coach_notifications = Notification.objects.filter(recipient=coach_user).order_by('-created_at')
    print(f"教练当前通知总数: {coach_notifications.count()}")
    
    for i, notification in enumerate(coach_notifications[:5], 1):
        print(f"{i}. [{notification.message_type}] {notification.title}")
        print(f"   内容: {notification.message}")
        print(f"   时间: {notification.created_at}")
        print(f"   已读: {'是' if notification.is_read else '否'}")
        if notification.data:
            print(f"   数据: {notification.data}")
        print()
    
    # 3. 检查学员的当前通知
    print("\n=== 检查学员当前通知 ===")
    student_notifications = Notification.objects.filter(recipient=student_user).order_by('-created_at')
    print(f"学员当前通知总数: {student_notifications.count()}")
    
    for i, notification in enumerate(student_notifications[:5], 1):
        print(f"{i}. [{notification.message_type}] {notification.title}")
        print(f"   内容: {notification.message}")
        print(f"   时间: {notification.created_at}")
        print(f"   已读: {'是' if notification.is_read else '否'}")
        if notification.data:
            print(f"   数据: {notification.data}")
        print()
    
    # 4. 检查师生关系申请记录
    print("\n=== 检查师生关系申请记录 ===")
    relations = CoachStudentRelation.objects.filter(
        coach=coach_user,
        student=student_user
    ).order_by('-created_at')
    
    print(f"师生关系记录总数: {relations.count()}")
    for i, relation in enumerate(relations[:3], 1):
        print(f"{i}. 状态: {relation.status}")
        print(f"   申请时间: {relation.created_at}")
        print(f"   备注: {relation.notes or '无'}")
        print()
    
    # 5. 测试API接口
    print("\n=== 测试通知API接口 ===")
    
    # 测试教练通知API
    client = APIClient()
    client.force_authenticate(user=coach_user)
    
    try:
        response = client.get('/api/notifications/list/')
        print(f"教练通知API状态码: {response.status_code}")
        if response.status_code == 200:
            data = response.data
            print(f"API返回通知数量: {len(data.get('results', []))}")
            print(f"总数: {data.get('count', 0)}")
            
            # 显示前3条通知
            for i, notification in enumerate(data.get('results', [])[:3], 1):
                print(f"{i}. [{notification.get('message_type')}] {notification.get('title')}")
                print(f"   内容: {notification.get('message')}")
                print(f"   已读: {'是' if notification.get('is_read') else '否'}")
                print()
        else:
            print(f"API请求失败: {response.data}")
            
    except Exception as e:
        print(f"❌ API测试失败: {e}")
    
    # 6. 测试统计API
    try:
        response = client.get('/api/notifications/stats/')
        print(f"\n统计API状态码: {response.status_code}")
        if response.status_code == 200:
            stats = response.data
            print(f"总通知数: {stats.get('total', 0)}")
            print(f"未读通知数: {stats.get('unread', 0)}")
            print(f"系统通知数: {stats.get('system', 0)}")
            print(f"预约通知数: {stats.get('booking', 0)}")
        else:
            print(f"统计API请求失败: {response.data}")
            
    except Exception as e:
        print(f"❌ 统计API测试失败: {e}")
    
    return True

if __name__ == '__main__':
    test_coach_notifications()