#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import django

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'keshe.settings')
django.setup()

from accounts.models import User, Coach

print('=== 当前数据库中的教练员数据 ===')
coaches = Coach.objects.select_related('user').all()
print(f'总教练员数量: {coaches.count()}')

for coach in coaches:
    print(f'- {coach.user.real_name} ({coach.user.gender}, {coach.coach_level}, {coach.status})')

print('\n=== 按姓名搜索"张"的结果 ===')
zhang_coaches = Coach.objects.select_related('user').filter(
    user__real_name__icontains='张'
)
print(f'找到 {zhang_coaches.count()} 个包含"张"的教练员:')
for coach in zhang_coaches:
    print(f'- {coach.user.real_name}')

print('\n=== 按性别筛选男性的结果 ===')
male_coaches = Coach.objects.select_related('user').filter(
    user__gender='male'
)
print(f'找到 {male_coaches.count()} 个男性教练员:')
for coach in male_coaches:
    print(f'- {coach.user.real_name} ({coach.user.gender})')