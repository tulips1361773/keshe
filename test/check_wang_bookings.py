#!/usr/bin/env python
import os
import django

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'keshe.settings')
django.setup()

from reservations.models import Booking
from accounts.models import User
from datetime import datetime, timedelta

# 获取王教练信息
wang_coach = User.objects.get(id=224)
print(f'王教练信息: 用户名={wang_coach.username}, 真实姓名={wang_coach.real_name}')

# 检查预约数据
bookings = Booking.objects.filter(relation__coach=wang_coach)
print(f'王教练的预约总数: {bookings.count()}')

# 检查未来一周的预约
today = datetime.now().date()
next_week = today + timedelta(days=7)
future_bookings = bookings.filter(start_time__date__gte=today, start_time__date__lte=next_week)
print(f'未来一周的预约数: {future_bookings.count()}')

if future_bookings.exists():
    print('\n未来一周的预约详情:')
    for booking in future_bookings[:5]:
        print(f'  - {booking.start_time} | 学生: {booking.relation.student.real_name} | 球台: {booking.table.name} | 状态: {booking.status}')
else:
    print('\n没有找到未来一周的预约数据')
    print('\n检查所有预约:')
    for booking in bookings[:5]:
        print(f'  - {booking.start_time} | 学生: {booking.relation.student.real_name} | 球台: {booking.table.name} | 状态: {booking.status}')

# 重置密码
print('\n重置王教练密码...')
wang_coach.set_password('password123')
wang_coach.save()
print('密码重置完成')