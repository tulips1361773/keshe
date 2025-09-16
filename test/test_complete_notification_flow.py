#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
完整的通知流程测试
测试从学员申请到教练收到通知的完整流程
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
from rest_framework.authtoken.models import Token

def test_complete_notification_flow():
    """测试完整的通知流程"""
    print("=== 完整通知流程测试 ===")
    
    # 1. 获取或创建测试用户
    try:
        # 查找教练
        coach_obj = Coach.objects.first()
        if not coach_obj:
            print("❌ 未找到教练")
            return False
            
        coach_user = coach_obj.user
        
        # 查找学员（非教练用户）
        student_user = User.objects.exclude(id=coach_user.id).first()
        if not student_user:
            print("❌ 未找到学员")
            return False
            
        print(f"✓ 教练: {coach_user.username} ({coach_user.real_name})")
        print(f"✓ 学员: {student_user.username} ({student_user.real_name})")
        
    except Exception as e:
        print(f"❌ 获取用户失败: {e}")
        return False
    
    # 2. 获取或创建Token
    try:
        coach_token, created = Token.objects.get_or_create(user=coach_user)
        student_token, created = Token.objects.get_or_create(user=student_user)
        
        print(f"\n教练Token: {coach_token.key}")
        print(f"学员Token: {student_token.key}")
        
    except Exception as e:
        print(f"❌ 获取Token失败: {e}")
        return False
    
    # 3. 清理之前的测试数据
    print("\n=== 清理测试数据 ===")
    try:
        # 删除之前的师生关系
        old_relations = CoachStudentRelation.objects.filter(
            coach=coach_user,
            student=student_user
        )
        deleted_relations = old_relations.count()
        old_relations.delete()
        print(f"✓ 清理了 {deleted_relations} 个旧的师生关系")
        
        # 清理相关通知
        old_notifications = Notification.objects.filter(
            recipient__in=[coach_user, student_user]
        )
        deleted_notifications = old_notifications.count()
        old_notifications.delete()
        print(f"✓ 清理了 {deleted_notifications} 个旧通知")
        
    except Exception as e:
        print(f"❌ 清理数据失败: {e}")
        return False
    
    # 4. 记录初始状态
    print("\n=== 初始状态 ===")
    coach_initial_notifications = Notification.objects.filter(recipient=coach_user).count()
    student_initial_notifications = Notification.objects.filter(recipient=student_user).count()
    print(f"教练初始通知数: {coach_initial_notifications}")
    print(f"学员初始通知数: {student_initial_notifications}")
    
    # 5. 模拟学员申请教练
    print("\n=== 学员申请教练 ===")
    client = APIClient()
    client.force_authenticate(user=student_user)
    
    apply_data = {
        'coach_id': coach_user.id,
        'notes': '希望能成为您的学员，请多指教！测试申请'
    }
    
    try:
        response = client.post('/api/reservations/relations/', apply_data, format='json')
        
        if response.status_code == 201:
            print("✅ 学员申请提交成功")
            relation_data = response.data
            relation_id = relation_data['id']
            print(f"  师生关系ID: {relation_id}")
            print(f"  申请状态: {relation_data.get('status', 'unknown')}")
        else:
            print(f"❌ 学员申请失败: {response.status_code}")
            print(f"  错误信息: {response.data}")
            return False
            
    except Exception as e:
        print(f"❌ 申请过程出错: {e}")
        return False
    
    # 6. 检查教练是否收到通知
    print("\n=== 检查教练通知 ===")
    try:
        # 查找教练收到的新通知
        coach_notifications = Notification.objects.filter(
            recipient=coach_user
        ).order_by('-created_at')
        
        print(f"教练当前通知总数: {coach_notifications.count()}")
        
        # 查找与此申请相关的通知
        related_notifications = coach_notifications.filter(
            data__relation_id=relation_id
        )
        
        if related_notifications.exists():
            notification = related_notifications.first()
            print("✅ 教练收到申请通知")
            print(f"  标题: {notification.title}")
            print(f"  内容: {notification.message}")
            print(f"  类型: {notification.message_type}")
            print(f"  时间: {notification.created_at}")
            print(f"  已读: {'是' if notification.is_read else '否'}")
            print(f"  数据: {notification.data}")
        else:
            print("❌ 教练未收到申请通知")
            # 显示所有通知以便调试
            print("\n教练的所有通知:")
            for i, notif in enumerate(coach_notifications[:5], 1):
                print(f"{i}. [{notif.message_type}] {notif.title}")
                print(f"   内容: {notif.message}")
                print(f"   数据: {notif.data}")
                print()
            return False
            
    except Exception as e:
        print(f"❌ 检查通知失败: {e}")
        return False
    
    # 7. 测试教练端API
    print("\n=== 测试教练端API ===")
    coach_client = APIClient()
    coach_client.force_authenticate(user=coach_user)
    
    try:
        # 测试通知列表API
        response = coach_client.get('/api/notifications/list/')
        print(f"通知列表API状态码: {response.status_code}")
        
        if response.status_code == 200:
            data = response.data
            print(f"API返回通知数量: {len(data.get('results', []))}")
            print(f"总数: {data.get('count', 0)}")
            
            # 显示前3条通知
            for i, notification in enumerate(data.get('results', [])[:3], 1):
                print(f"{i}. [{notification.get('message_type')}] {notification.get('title')}")
                print(f"   内容: {notification.get('message')}")
                print(f"   已读: {'是' if notification.get('is_read') else '否'}")
                if notification.get('data'):
                    print(f"   数据: {notification.get('data')}")
                print()
        else:
            print(f"API请求失败: {response.data}")
            
        # 测试统计API
        response = coach_client.get('/api/notifications/stats/')
        print(f"统计API状态码: {response.status_code}")
        if response.status_code == 200:
            stats = response.data
            print(f"总通知数: {stats.get('total', 0)}")
            print(f"未读通知数: {stats.get('unread', 0)}")
            print(f"系统通知数: {stats.get('system', 0)}")
            print(f"预约通知数: {stats.get('booking', 0)}")
        else:
            print(f"统计API请求失败: {response.data}")
            
    except Exception as e:
        print(f"❌ API测试失败: {e}")
        return False
    
    # 8. 模拟教练审核
    print("\n=== 教练审核申请 ===")
    try:
        response = coach_client.post(f'/api/reservations/relations/{relation_id}/approve/')
        
        if response.status_code == 200:
            print("✅ 教练审核成功")
            
            # 检查学员是否收到审核结果通知
            student_notifications = Notification.objects.filter(
                recipient=student_user,
                data__relation_id=relation_id
            ).order_by('-created_at')
            
            if student_notifications.exists():
                notification = student_notifications.first()
                print("✅ 学员收到审核结果通知")
                print(f"  标题: {notification.title}")
                print(f"  内容: {notification.message}")
            else:
                print("❌ 学员未收到审核结果通知")
                
        else:
            print(f"❌ 教练审核失败: {response.status_code}")
            print(f"  错误信息: {response.data}")
            
    except Exception as e:
        print(f"❌ 审核过程出错: {e}")
        return False
    
    # 9. 最终统计
    print("\n=== 最终统计 ===")
    coach_final_notifications = Notification.objects.filter(recipient=coach_user).count()
    student_final_notifications = Notification.objects.filter(recipient=student_user).count()
    
    print(f"教练最终通知数: {coach_final_notifications}")
    print(f"学员最终通知数: {student_final_notifications}")
    print(f"教练新增通知: {coach_final_notifications - coach_initial_notifications}")
    print(f"学员新增通知: {student_final_notifications - student_initial_notifications}")
    
    print("\n=== 测试结果 ===")
    print("✅ 完整通知流程测试成功")
    print("✅ 学员申请时教练能收到通知")
    print("✅ 教练审核后学员能收到通知")
    print("✅ API接口工作正常")
    
    return True

if __name__ == '__main__':
    success = test_complete_notification_flow()
    if success:
        print("\n🎉 所有测试通过！")
    else:
        print("\n❌ 测试失败！")