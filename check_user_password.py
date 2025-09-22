#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'keshe.settings')
django.setup()

from accounts.models import User

user = User.objects.get(username='hhm')
print(f'用户: {user.username}')
print(f'密码哈希: {user.password[:50]}...')
print(f'检查密码hhm123456: {user.check_password("hhm123456")}')
print(f'检查密码123456: {user.check_password("123456")}')

# 检查现有关系
from reservations.models import CoachStudentRelation
relations = CoachStudentRelation.objects.filter(student_id=4)
print(f'\n学员的所有关系:')
for rel in relations:
    print(f'  教练: {rel.coach.username} (ID: {rel.coach.id}), 状态: {rel.status}')