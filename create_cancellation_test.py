#!/usr/bin/env python
"""
创建取消申请测试数据
"""
import os
import django

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'keshe.settings')
django.setup()

from accounts.models import User
from reservations.models import Booking, BookingCancellation, CoachStudentRelation
from reservations.models import Table
from datetime import datetime, timedelta
from django.utils import timezone

def main():
    print('🔍 查找测试数据...')

    # 获取测试用户
    try:
        coach = User.objects.get(username='test_coach')
        student = User.objects.get(username='test_student')
        print(f'✅ 找到教练: {coach.username}')
        print(f'✅ 找到学员: {student.username}')
    except User.DoesNotExist:
        print('❌ 未找到测试用户')
        return

    # 获取师生关系
    try:
        relation = CoachStudentRelation.objects.get(coach=coach, student=student)
        print(f'✅ 找到师生关系: ID={relation.id}')
    except CoachStudentRelation.DoesNotExist:
        print('❌ 未找到师生关系')
        return

    # 获取球台
    try:
        table = Table.objects.first()
        print(f'✅ 找到球台: {table.name}')
    except:
        print('❌ 未找到球台')
        return

    # 创建一个已确认的预约
    start_time = timezone.now() + timedelta(days=2, hours=10)
    end_time = start_time + timedelta(hours=2)

    booking = Booking.objects.create(
        relation=relation,
        table=table,
        start_time=start_time,
        end_time=end_time,
        duration_hours=2.0,
        total_fee=160.0,
        status='confirmed',
        payment_status='paid'
    )
    print(f'✅ 创建预约: ID={booking.id}, 状态={booking.status}')

    # 学员申请取消预约
    cancellation = BookingCancellation.objects.create(
        booking=booking,
        requested_by=student,
        reason='临时有事，无法参加训练',
        status='pending'
    )
    print(f'✅ 创建取消申请: ID={cancellation.id}')

    # 更新预约状态为待审核取消
    booking.status = 'pending_cancellation'
    booking.save()
    print(f'✅ 更新预约状态为: {booking.status}')

    print(f'\n📋 测试数据创建完成:')
    print(f'   预约ID: {booking.id}')
    print(f'   状态: {booking.status}')
    print(f'   申请人: {student.username} ({student.get_full_name()})')
    print(f'   审核人: {coach.username} ({coach.get_full_name()})')
    print(f'   取消原因: {cancellation.reason}')
    print(f'\n🎯 现在教练可以在预约管理页面看到审核按钮了！')

if __name__ == '__main__':
    main()