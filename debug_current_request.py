#!/usr/bin/env python
import os
import django

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'keshe.settings')
django.setup()

from accounts.models import User
from reservations.models import CoachStudentRelation

print("=== 当前请求调试 ===")

# 检查当前登录用户（假设是ID 4的huang用户）
try:
    student = User.objects.get(id=4)
    print(f"学员信息: {student.username} (ID: {student.id}, 姓名: {student.first_name})")
    print(f"用户类型: {student.user_type}")
except User.DoesNotExist:
    print("学员不存在！")

print("\n=== 可用教练列表 ===")
coaches = User.objects.filter(user_type='coach', is_active=True)
print(f"总教练数: {coaches.count()}")

# 显示前10个教练
for coach in coaches[:10]:
    # 检查是否已有关系
    existing = CoachStudentRelation.objects.filter(
        coach_id=coach.id, 
        student_id=4
    ).first()
    
    status = "无关系"
    if existing:
        status = f"已有关系({existing.status})"
    
    print(f"  教练: {coach.first_name} (ID: {coach.id}, 用户名: {coach.username}) - {status}")

print("\n=== 建议测试 ===")
# 找一个没有关系的教练
available_coach = None
for coach in coaches:
    if not CoachStudentRelation.objects.filter(coach_id=coach.id, student_id=4).exists():
        available_coach = coach
        break

if available_coach:
    print(f"建议选择教练: {available_coach.first_name} (ID: {available_coach.id})")
    print(f"前端应发送数据: {{'coach_id': {available_coach.id}, 'student_id': 4, 'notes': '测试选择'}}")
else:
    print("所有教练都已建立关系")