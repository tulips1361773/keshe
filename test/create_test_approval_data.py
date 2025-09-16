#!/usr/bin/env python
"""
创建教练审核测试数据
"""

import os
import sys
import django
from datetime import datetime, timedelta

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'keshe.settings')
django.setup()

from django.contrib.auth import get_user_model
from accounts.models import Coach
from reservations.models import CoachStudentRelation
from notifications.models import Notification

User = get_user_model()

def create_test_data():
    print("=== 创建教练审核测试数据 ===")
    
    # 1. 创建测试教练
    try:
        coach_user = User.objects.get(username='test_coach')
        print(f"✅ 教练用户已存在: {coach_user.username}")
    except User.DoesNotExist:
        coach_user = User.objects.create_user(
            username='test_coach',
            email='coach@test.com',
            password='testpass123',
            user_type='coach',
            real_name='测试教练',
            phone='13800000001'
        )
        print(f"✅ 创建教练用户: {coach_user.username}")
    
    # 创建教练档案
    coach, created = Coach.objects.get_or_create(
        user=coach_user,
        defaults={
            'coach_level': 'intermediate',
            'hourly_rate': 200.00,
            'achievements': '拥有5年教学经验的专业乒乓球教练',
            'max_students': 30,
            'status': 'approved'
        }
    )
    if created:
        print(f"✅ 创建教练档案: {coach.user.real_name}")
    else:
        print(f"✅ 教练档案已存在: {coach.user.real_name}")
    
    # 2. 创建测试学员
    students_data = [
        {'username': 'student1', 'real_name': '张三', 'email': 'student1@test.com', 'phone': '13800000002'},
        {'username': 'student2', 'real_name': '李四', 'email': 'student2@test.com', 'phone': '13800000003'},
        {'username': 'student3', 'real_name': '王五', 'email': 'student3@test.com', 'phone': '13800000004'},
        {'username': 'student4', 'real_name': '赵六', 'email': 'student4@test.com', 'phone': '13800000005'},
    ]
    
    students = []
    for student_data in students_data:
        try:
            student_user = User.objects.get(username=student_data['username'])
            print(f"✅ 学员用户已存在: {student_user.username}")
        except User.DoesNotExist:
            student_user = User.objects.create_user(
                username=student_data['username'],
                email=student_data['email'],
                password='testpass123',
                user_type='student',
                real_name=student_data['real_name'],
                phone=student_data['phone']
            )
            print(f"✅ 创建学员用户: {student_user.username}")
        
            # 学员信息直接使用User模型
        students.append(student_user)
    
    # 3. 创建师生关系申请（不同状态）
    relations_data = [
        {'student': students[0], 'status': 'pending', 'notes': '希望能够提高发球技术'},
        {'student': students[1], 'status': 'pending', 'notes': '想学习正手攻球'},
        {'student': students[2], 'status': 'approved', 'notes': '已经有一些基础，希望进一步提高'},
        {'student': students[3], 'status': 'rejected', 'notes': '时间安排有冲突'},
    ]
    
    for i, relation_data in enumerate(relations_data):
        # 检查是否已存在
        existing_relation = CoachStudentRelation.objects.filter(
            coach=coach.user,
            student=relation_data['student']
        ).first()
        
        if existing_relation:
            # 更新状态
            existing_relation.status = relation_data['status']
            existing_relation.notes = relation_data['notes']
            existing_relation.save()
            print(f"✅ 更新师生关系: {relation_data['student'].real_name} - {relation_data['status']}")
        else:
            # 创建新关系
            relation = CoachStudentRelation.objects.create(
                coach=coach.user,
                student=relation_data['student'],
                status=relation_data['status'],
                notes=relation_data['notes'],
                applied_at=datetime.now() - timedelta(days=i+1)
            )
            
            # 如果已处理，设置处理时间
            if relation_data['status'] in ['approved', 'rejected']:
                relation.processed_at = datetime.now() - timedelta(hours=i*2)
                relation.save()
            
            print(f"✅ 创建师生关系: {relation_data['student'].real_name} - {relation_data['status']}")
    
    # 4. 创建相关通知
    pending_relations = CoachStudentRelation.objects.filter(
        coach=coach.user,
        status='pending'
    )
    
    for relation in pending_relations:
        # 为教练创建通知
        notification, created = Notification.objects.get_or_create(
            recipient=coach.user,
            title='新的学员申请',
            message=f'{relation.student.real_name} 申请选择您为教练',
            message_type='relation_request',
            defaults={
                'data': {
                'relation_id': relation.id,
                'student_name': relation.student.real_name
            }
            }
        )
        if created:
            print(f"✅ 创建通知: {notification.title}")
    
    print("\n=== 测试数据创建完成 ===")
    print(f"教练: {coach.user.real_name} ({coach.user.username})")
    print(f"学员数量: {len(students)}")
    
    # 统计师生关系
    total_relations = CoachStudentRelation.objects.filter(coach=coach.user).count()
    pending_count = CoachStudentRelation.objects.filter(coach=coach.user, status='pending').count()
    approved_count = CoachStudentRelation.objects.filter(coach=coach.user, status='approved').count()
    rejected_count = CoachStudentRelation.objects.filter(coach=coach.user, status='rejected').count()
    
    print(f"师生关系总数: {total_relations}")
    print(f"待审核: {pending_count}")
    print(f"已通过: {approved_count}")
    print(f"已拒绝: {rejected_count}")
    
    # 通知统计
    notification_count = Notification.objects.filter(recipient=coach.user).count()
    print(f"通知数量: {notification_count}")
    
    print("\n🎉 测试数据准备就绪！")
    print("\n📋 测试说明:")
    print("1. 使用教练账号登录: test_coach / testpass123")
    print("2. 进入教学管理页面查看学员申请")
    print("3. 测试审核功能（同意/拒绝申请）")
    print("4. 查看通知系统是否正常工作")

if __name__ == '__main__':
    create_test_data()