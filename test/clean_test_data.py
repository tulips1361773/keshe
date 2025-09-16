#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import django

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'keshe.settings')
django.setup()

from accounts.models import User, Coach
from django.contrib.auth.models import Group

print('=== 清理重复的测试数据 ===')

# 删除所有测试相关的用户和教练员
test_users = User.objects.filter(
    username__in=['coach1', 'coach2', 'coach3', 'backend_test_student']
)
print(f'删除测试用户: {test_users.count()} 个')
test_users.delete()

# 删除重复的张教练（保留一个有完整信息的）
zhang_coaches = Coach.objects.filter(user__real_name='张教练')
print(f'找到张教练: {zhang_coaches.count()} 个')

# 保留第一个有完整gender信息的张教练，删除其他的
valid_zhang = None
for coach in zhang_coaches:
    if coach.user.gender and not valid_zhang:
        valid_zhang = coach
        print(f'保留张教练: {coach.user.username} (gender: {coach.user.gender})')
    else:
        print(f'删除重复张教练: {coach.user.username}')
        coach.user.delete()  # 删除用户会级联删除教练记录

print('\n=== 重新创建标准测试数据 ===')

# 创建用户组
student_group, _ = Group.objects.get_or_create(name='学员')
coach_group, _ = Group.objects.get_or_create(name='教练员')

# 创建测试学员
student_user = User.objects.create(
    username='backend_test_student',
    email='backend_student@test.com',
    first_name='后端',
    last_name='测试学员',
    real_name='后端测试学员',
    phone='13800138001',
    gender='male',
    user_type='student'
)
student_user.groups.add(student_group)
print(f'创建测试学员: {student_user.username}')

# 创建标准测试教练员（如果不存在）
coach_data = [
    {'username': 'test_coach_zhang', 'real_name': '张教练', 'gender': 'male', 'level': 'senior', 'phone': '13800138002'},
    {'username': 'test_coach_li', 'real_name': '李教练', 'gender': 'female', 'level': 'intermediate', 'phone': '13800138003'},
    {'username': 'test_coach_wang', 'real_name': '王教练', 'gender': 'male', 'level': 'junior', 'phone': '13800138004'},
]

for data in coach_data:
    # 检查是否已存在
    existing_user = User.objects.filter(username=data['username']).first()
    if existing_user:
        print(f'教练员 {data["username"]} 已存在，跳过创建')
        continue
        
    # 创建用户
    coach_user = User.objects.create(
        username=data['username'],
        email=f"{data['username']}@test.com",
        first_name=data['real_name'][:1],
        last_name=data['real_name'][1:],
        phone=data['phone'],
        real_name=data['real_name'],
        gender=data['gender'],
        user_type='coach'
    )
    coach_user.set_password('testpass123')
    coach_user.save()
    coach_user.groups.add(coach_group)
    
    # 创建教练档案
    coach, created = Coach.objects.get_or_create(
        user=coach_user,
        defaults={
            'coach_level': data['level'],
            'achievements': '乒乓球基础训练',
            'status': 'approved'
        }
    )
    
    print(f'创建教练员: {coach_user.real_name} ({coach_user.gender}, {coach.coach_level})')

print('\n=== 数据清理完成，验证结果 ===')
coaches = Coach.objects.select_related('user').filter(status='approved')
print(f'总教练员数量: {coaches.count()}')

for coach in coaches:
    print(f'- {coach.user.real_name} ({coach.user.gender}, {coach.coach_level})')

print('\n=== 验证搜索结果 ===')
zhang_coaches = Coach.objects.select_related('user').filter(
    user__real_name__icontains='张',
    status='approved'
)
print(f'搜索"张"的结果: {zhang_coaches.count()} 个')

male_coaches = Coach.objects.select_related('user').filter(
    user__gender='male',
    status='approved'
)
print(f'男性教练员: {male_coaches.count()} 个')