#!/usr/bin/env python
import os
import django

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'keshe.settings')
django.setup()

from reservations.models import Booking
from accounts.models import User
from datetime import datetime, timedelta
from django.utils import timezone

# 获取王教练信息
wang_coach = User.objects.get(id=224)
print(f'王教练信息: 用户名={wang_coach.username}, 真实姓名={wang_coach.real_name}')

# 获取所有王教练的预约
bookings = Booking.objects.filter(relation__coach=wang_coach)
print(f'王教练的预约总数: {bookings.count()}')

# 更新预约日期到未来
today = timezone.now().date()
print(f'今天日期: {today}')

for i, booking in enumerate(bookings):
    # 将预约日期更新到今天之后的几天
    new_date = today + timedelta(days=i % 7 + 1)  # 分布在未来7天内
    
    # 保持原来的时间，只更新日期
    original_time = booking.start_time.time()
    new_start_time = timezone.make_aware(datetime.combine(new_date, original_time))
    
    # 计算结束时间
    duration = timedelta(hours=float(booking.duration_hours))
    new_end_time = new_start_time + duration
    
    # 更新预约
    booking.start_time = new_start_time
    booking.end_time = new_end_time
    booking.save()
    
    print(f'更新预约 {booking.id}: {new_start_time} | 学生: {booking.relation.student.real_name} | 球台: {booking.table.name}')

print('\n预约日期更新完成！')

# 验证更新结果
future_bookings = bookings.filter(start_time__date__gte=today)
print(f'\n未来的预约数: {future_bookings.count()}')