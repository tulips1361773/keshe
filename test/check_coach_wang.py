import os
import django

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'keshe.settings')
django.setup()

from accounts.models import User

# 查询王教练信息
coach = User.objects.filter(username='王教练').first()
if coach:
    print(f'王教练ID: {coach.id}')
    print(f'用户类型: {coach.user_type}')
    print(f'姓名: {coach.first_name}')
    print(f'邮箱: {coach.email}')
    print(f'是否激活: {coach.is_active}')
else:
    print('未找到王教练用户')
    # 查看所有教练用户
    coaches = User.objects.filter(user_type='coach')
    print(f'\n系统中的教练用户数量: {coaches.count()}')
    for c in coaches:
        print(f'- {c.username} (ID: {c.id}, 姓名: {c.first_name})')