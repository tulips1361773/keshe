#!/usr/bin/env python
import os
import django

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'keshe.settings')
django.setup()

from accounts.models import User
from reservations.serializers import CoachStudentRelationSerializer

print("=== 模拟后端验证过程 ===")

# 模拟前端发送的数据
data = {
    'coach_id': 113,
    'student_id': 4,
    'notes': '测试选择教练'
}

print(f"前端发送数据: {data}")

# 手动验证教练和学员是否存在
print("\n=== 手动验证 ===")
try:
    coach = User.objects.get(id=113, user_type='coach')
    print(f"✓ 教练存在: {coach.username} (ID: {coach.id}, 类型: {coach.user_type})")
except User.DoesNotExist:
    print("✗ 教练不存在")

try:
    student = User.objects.get(id=4, user_type='student')
    print(f"✓ 学员存在: {student.username} (ID: {student.id}, 类型: {student.user_type})")
except User.DoesNotExist:
    print("✗ 学员不存在")

# 使用serializer验证
print("\n=== Serializer验证 ===")
serializer = CoachStudentRelationSerializer(data=data)
if serializer.is_valid():
    print("✓ 数据验证通过")
    try:
        instance = serializer.save()
        print(f"✓ 关系创建成功: {instance}")
    except Exception as e:
        print(f"✗ 创建失败: {e}")
else:
    print("✗ 数据验证失败")
    print(f"错误详情: {serializer.errors}")

print("\n=== 检查User模型字段 ===")
user_fields = [field.name for field in User._meta.fields]
print(f"User模型字段: {user_fields}")

# 检查是否有其他过滤条件
print("\n=== 检查教练和学员的详细信息 ===")
coach = User.objects.get(id=113)
student = User.objects.get(id=4)

print(f"教练详情:")
for field in ['id', 'username', 'user_type', 'is_active', 'is_staff', 'is_superuser']:
    if hasattr(coach, field):
        print(f"  {field}: {getattr(coach, field)}")

print(f"学员详情:")
for field in ['id', 'username', 'user_type', 'is_active', 'is_staff', 'is_superuser']:
    if hasattr(student, field):
        print(f"  {field}: {getattr(student, field)}")