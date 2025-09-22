#!/usr/bin/env python
import os
import django

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'keshe.settings')
django.setup()

from accounts.models import User
from accounts.serializers import UserSerializer

print("=== 检查教练数据结构 ===")

# 获取教练ID 113
coach = User.objects.get(id=113)
print(f"数据库中的教练: {coach}")
print(f"教练ID: {coach.id}")
print(f"教练用户名: {coach.username}")

# 使用序列化器获取前端会收到的数据
serializer = UserSerializer(coach)
coach_data = serializer.data
print(f"\n前端收到的教练数据: {coach_data}")

# 检查是否有user_id字段
if 'user_id' in coach_data:
    print(f"user_id字段存在: {coach_data['user_id']}")
else:
    print("user_id字段不存在")

print(f"id字段: {coach_data.get('id')}")

# 模拟前端的逻辑
coach_id_used = coach_data.get('user_id') or coach_data.get('id')
print(f"\n前端使用的coach_id: {coach_id_used}")

# 检查这个ID是否存在
try:
    check_coach = User.objects.get(id=coach_id_used, user_type='coach')
    print(f"✓ 使用的coach_id有效: {check_coach.username}")
except User.DoesNotExist:
    print(f"✗ 使用的coach_id无效: {coach_id_used}")

print("\n=== 检查所有教练的数据结构 ===")
coaches = User.objects.filter(user_type='coach')[:3]
for coach in coaches:
    serializer = UserSerializer(coach)
    data = serializer.data
    print(f"教练 {coach.username}: id={data.get('id')}, user_id={data.get('user_id', '不存在')}")