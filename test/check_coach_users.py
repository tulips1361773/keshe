#!/usr/bin/env python
import os
import django

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'keshe.settings')
django.setup()

from accounts.models import User

print('所有教练用户:')
coaches = User.objects.filter(user_type='coach')
for coach in coaches:
    print(f'ID: {coach.id}, 用户名: {coach.username}, 真实姓名: {coach.real_name}, 邮箱: {coach.email}')

print('\n重置王教练密码:')
try:
    wang_coach = User.objects.get(real_name='王教练')
    print(f'找到王教练: 用户名={wang_coach.username}, ID={wang_coach.id}')
    wang_coach.set_password('password123')
    wang_coach.save()
    print('密码重置完成')
except User.DoesNotExist:
    print('未找到真实姓名为王教练的用户')
    # 尝试通过用户名查找
    try:
        wang_coach = User.objects.get(username='王教练')
        print(f'通过用户名找到: 用户名={wang_coach.username}, 真实姓名={wang_coach.real_name}, ID={wang_coach.id}')
        wang_coach.set_password('password123')
        wang_coach.save()
        print('密码重置完成')
    except User.DoesNotExist:
        print('也未找到用户名为王教练的用户')