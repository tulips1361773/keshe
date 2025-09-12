#!/usr/bin/env python
"""
创建测试数据脚本
用于为乒乓球管理系统创建基础测试数据
"""

import os
import sys
import django
from datetime import datetime, timedelta
from decimal import Decimal

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'keshe.settings')
django.setup()

from accounts.models import User, UserProfile
from campus.models import Campus, CampusArea
from courses.models import Course, CourseEnrollment
from reservations.models import Table, Booking, CoachStudentRelation
from notifications.models import Notification

def create_test_data():
    """创建测试数据"""
    print("开始创建测试数据...")
    
    # 1. 创建用户
    print("1. 创建用户...")
    
    # 创建管理员用户
    admin_user, created = User.objects.get_or_create(
        username='admin01',
        defaults={
            'email': 'admin@example.com',
            'real_name': '系统管理员',
            'phone': '13800138000',
            'user_type': 'admin',
            'is_staff': True,
            'is_superuser': True
        }
    )
    if created:
        admin_user.set_password('admin123')
        admin_user.save()
        print(f"  创建管理员: {admin_user.username}")
    
    # 创建教练用户
    coach_user, created = User.objects.get_or_create(
        username='coach01',
        defaults={
            'email': 'coach01@example.com',
            'real_name': '张教练',
            'phone': '13800138001',
            'user_type': 'coach'
        }
    )
    if created:
        coach_user.set_password('coach123')
        coach_user.save()
        print(f"  创建教练: {coach_user.username}")
    
    # 创建学生用户
    student_user, created = User.objects.get_or_create(
        username='student01',
        defaults={
            'email': 'student01@example.com',
            'real_name': '李学员',
            'phone': '13800138002',
            'user_type': 'student'
        }
    )
    if created:
        student_user.set_password('student123')
        student_user.save()
        print(f"  创建学生: {student_user.username}")
    
    # 2. 创建用户资料
    print("2. 创建用户资料...")
    
    # 管理员资料
    admin_profile, created = UserProfile.objects.get_or_create(
        user=admin_user,
        defaults={
            'bio': '系统管理员，负责整体运营管理',
            'experience_years': 10
        }
    )
    if created:
        print(f"  创建管理员资料: {admin_user.real_name}")
    
    # 教练资料
    coach_profile, created = UserProfile.objects.get_or_create(
        user=coach_user,
        defaults={
            'bio': '专业乒乓球教练，擅长基础教学和技术指导',
            'experience_years': 5,
            'skills': '基础教学,正手攻球,发球技术'
        }
    )
    if created:
        print(f"  创建教练资料: {coach_user.real_name}")
    
    # 学生资料
    student_profile, created = UserProfile.objects.get_or_create(
        user=student_user,
        defaults={
            'bio': '乒乓球爱好者，希望提高技术水平',
            'experience_years': 1
        }
    )
    if created:
        print(f"  创建学生资料: {student_user.real_name}")
    
    # 3. 创建校区数据
    print("3. 创建校区数据...")
    
    campus, created = Campus.objects.get_or_create(
        name='主校区',
        defaults={
            'address': '北京市朝阳区体育大街123号',
            'phone': '010-12345678',
            'description': '主要校区，设施齐全'
        }
    )
    if created:
        print(f"  创建校区: {campus.name}")
    
    # 创建校区区域
    area1, created = CampusArea.objects.get_or_create(
        campus=campus,
        name='A区训练馆',
        defaults={
            'description': 'A区训练馆，适合基础训练',
            'capacity': 20
        }
    )
    if created:
        print(f"  创建区域: {area1.name}")
    
    # 4. 创建球台
    print("4. 创建球台...")
    
    for i in range(1, 6):
        table, created = Table.objects.get_or_create(
            campus=campus,
            number=f'T{i:02d}',
            defaults={
                'name': f'球台{i}号',
                'status': 'available'
            }
        )
        if created:
            print(f"  创建球台: {table.number}")
    
    # 5. 创建课程
    print("5. 创建课程...")
    
    course, created = Course.objects.get_or_create(
        name='乒乓球基础入门课程',
        defaults={
            'description': '适合零基础学员的入门课程，学习基本握拍、发球和接球技巧',
            'course_type': 'beginner',
            'campus': campus,
            'coach': coach_user,
            'area': area1,
            'max_students': 10,
            'duration_minutes': 90,
            'price_per_session': Decimal('100.00'),
            'total_sessions': 12,
            'status': 'published',
            'start_date': datetime.now().date(),
            'end_date': (datetime.now() + timedelta(days=90)).date(),
            'requirements': '无特殊要求，适合零基础学员',
            'equipment_needed': '球拍、乒乓球（场馆提供）'
        }
    )
    if created:
        print(f"  创建课程: {course.name}")
    
    # 6. 创建课程报名
    print("6. 创建课程报名...")
    
    enrollment, created = CourseEnrollment.objects.get_or_create(
        course=course,
        student=student_user,
        defaults={
            'status': 'confirmed',
            'payment_status': 'paid',
            'paid_amount': course.total_price,
            'notes': '测试报名数据'
        }
    )
    if created:
        print(f"  创建课程报名: {student_user.real_name} -> {course.name}")
    
    # 7. 创建师生关系
    print("7. 创建师生关系...")
    
    relation, created = CoachStudentRelation.objects.get_or_create(
        coach=coach_user,
        student=student_user,
        defaults={
            'status': 'approved',
            'applied_by': 'student',
            'notes': '基础课程师生关系'
        }
    )
    if created:
        print(f"  创建师生关系: {coach_user.real_name} -> {student_user.real_name}")
    
    # 8. 创建预约记录
    print("8. 创建预约记录...")
    
    table = Table.objects.first()
    if table:
        start_datetime = datetime.now().replace(hour=14, minute=0, second=0, microsecond=0)
        end_datetime = datetime.now().replace(hour=16, minute=0, second=0, microsecond=0)
        
        booking, created = Booking.objects.get_or_create(
            relation=relation,
            table=table,
            start_time=start_datetime,
            defaults={
                'end_time': end_datetime,
                'duration_hours': Decimal('2.0'),
                'total_fee': Decimal('100.00'),
                'status': 'confirmed',
                'notes': '测试预约数据'
            }
        )
        if created:
            print(f"  创建预约: {table.number} - {booking.start_time.date()}")
    
    # 9. 创建通知
    print("9. 创建通知...")
    
    # 给学生发送通知
    notification1, created = Notification.objects.get_or_create(
        recipient=student_user,
        title='欢迎加入乒乓球训练',
        defaults={
            'message': '欢迎您加入我们的乒乓球训练课程！请按时参加训练。',
            'message_type': 'system',
            'is_read': False
        }
    )
    if created:
        print(f"  创建通知: {notification1.title}")
    
    # 给教练发送通知
    notification2, created = Notification.objects.get_or_create(
        recipient=coach_user,
        title='新学员加入课程',
        defaults={
            'message': f'学员{student_user.real_name}已加入您的基础入门课程。',
            'message_type': 'system',
            'is_read': False
        }
    )
    if created:
        print(f"  创建通知: {notification2.title}")
    
    print("\n测试数据创建完成！")
    print("\n用户账号信息:")
    print(f"管理员: admin01 / admin123")
    print(f"教练: coach01 / coach123")
    print(f"学生: student01 / student123")
    print("\n可以使用这些账号登录系统进行测试。")

if __name__ == '__main__':
    try:
        create_test_data()
    except Exception as e:
        print(f"创建测试数据时出错: {e}")
        import traceback
        traceback.print_exc()