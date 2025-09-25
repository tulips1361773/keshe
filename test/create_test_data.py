#!/usr/bin/env python
"""
创建测试数据用于测试教练审核预约功能
"""
import os
import django

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'keshe.settings')
django.setup()

from accounts.models import User, Coach
from reservations.models import Booking, CoachStudentRelation, Table
from campus.models import Campus
from datetime import datetime, timedelta
from django.utils import timezone

def create_test_data():
    """创建测试数据"""
    print("=== 创建测试数据 ===\n")
    
    try:
        # 获取教练
        coach_user = User.objects.get(username='test_coach')
        coach = coach_user.coach_profile
        print(f"使用教练: {coach.user.real_name}")
        
        # 创建或获取学员账号
        student_user, created = User.objects.get_or_create(
            username='test_student',
            defaults={
                'real_name': '测试学员',
                'user_type': 'student',
                'email': 'student@test.com',
                'phone': '13800000002',
                'is_active': True,
                'is_active_member': True
            }
        )
        
        if created:
            student_user.set_password('123456')
            student_user.save()
            print(f"✅ 创建学员账号: {student_user.username}")
        else:
            print(f"📋 学员账号已存在: {student_user.username}")
        
        # 确保学员有足够余额（通过account_balance字段）
        if not hasattr(student_user, 'account_balance'):
            student_user.account_balance = 1000.00
            student_user.save()
            print(f"💰 设置学员余额: {student_user.account_balance}")
        elif student_user.account_balance < 100:
            student_user.account_balance = 1000.00
            student_user.save()
            print(f"💰 更新学员余额: {student_user.account_balance}")
        
        # 创建师生关系
        relation, created = CoachStudentRelation.objects.get_or_create(
            coach=coach.user,
            student=student_user,
            defaults={
                'status': 'approved',
                'applied_by': 'student',
                'applied_at': timezone.now(),
                'processed_at': timezone.now()
            }
        )
        
        if created:
            print(f"✅ 创建师生关系: {relation.coach.real_name} - {relation.student.real_name}")
        else:
            print(f"📋 师生关系已存在: {relation.coach.real_name} - {relation.student.real_name}")
            # 确保关系是已批准状态
            if relation.status != 'approved':
                relation.status = 'approved'
                relation.processed_at = timezone.now()
                relation.save()
                print(f"🔄 更新师生关系状态为approved")
        
        # 获取或创建球台
        campus = Campus.objects.first()
        if not campus:
            campus = Campus.objects.create(
                name='测试校区',
                code='TEST001',
                address='测试地址',
                phone='13800000000'
            )
            print(f"✅ 创建测试校区: {campus.name}")
        
        table, created = Table.objects.get_or_create(
            campus=campus,
            number='1',
            defaults={
                'name': '1号台',
                'status': 'available',
                'description': '测试球台',
                'is_active': True,
            }
        )
        
        if created:
            print(f"🏓 创建球台: {table}")
        else:
            print(f"🏓 球台已存在: {table}")
        
        # 创建待审核的预约
        tomorrow = timezone.now() + timedelta(days=1)
        start_time = tomorrow.replace(hour=10, minute=0, second=0, microsecond=0)
        end_time = start_time + timedelta(hours=1)
        
        booking, created = Booking.objects.get_or_create(
            relation=relation,
            table=table,
            start_time=start_time,
            defaults={
                'end_time': end_time,
                'duration_hours': 1.0,
                'total_fee': 50.00,
                'status': 'pending',
                'payment_status': 'unpaid'
            }
        )
        
        if created:
            print(f"✅ 创建待审核预约: ID={booking.id}")
        else:
            print(f"📋 预约已存在: ID={booking.id}, 状态={booking.status}")
            # 如果预约不是pending状态，重置为pending
            if booking.status != 'pending':
                booking.status = 'pending'
                booking.save()
                print(f"🔄 重置预约状态为pending")
        
        print(f"\n=== 测试数据准备完成 ===")
        print(f"教练: {coach.user.real_name} (ID: {coach.id})")
        print(f"学员: {student_user.real_name} (ID: {student_user.id}, 余额: {getattr(student_user, 'account_balance', '未设置')})")
        print(f"师生关系: ID={relation.id}, 状态={relation.status}")
        print(f"球台: {table.campus.name} - {table.number}号台")
        print(f"待审核预约: ID={booking.id}, 状态={booking.status}, 时间={booking.start_time}")
        
        return True
        
    except Exception as e:
        print(f"❌ 创建测试数据失败: {e}")
        return False

if __name__ == '__main__':
    create_test_data()