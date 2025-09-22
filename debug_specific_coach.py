#!/usr/bin/env python
import os
import django

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'keshe.settings')
django.setup()

from accounts.models import User
from reservations.models import CoachStudentRelation

print("=== 检查教练ID 113 ===")

try:
    coach = User.objects.get(id=113)
    print(f"教练存在: {coach.username} (ID: {coach.id})")
    print(f"姓名: '{coach.first_name}' (长度: {len(coach.first_name)})")
    print(f"用户类型: {coach.user_type}")
    print(f"是否激活: {coach.is_active}")
    # print(f"是否审核通过: {coach.is_approved}")  # User模型可能没有这个字段
except User.DoesNotExist:
    print("教练ID 113不存在！")
    
    # 查找其他可用教练
    print("\n查找其他可用教练:")
    coaches = User.objects.filter(user_type='coach', is_active=True)
    for coach in coaches[:5]:
        existing = CoachStudentRelation.objects.filter(coach_id=coach.id, student_id=4).exists()
        if not existing:
            print(f"  可选教练: {coach.first_name or '无姓名'} (ID: {coach.id}, 用户名: {coach.username})")

print("\n=== 检查学员ID 4 ===")
try:
    student = User.objects.get(id=4)
    print(f"学员存在: {student.username} (ID: {student.id})")
    print(f"姓名: '{student.first_name}' (长度: {len(student.first_name)})")
    print(f"用户类型: {student.user_type}")
    print(f"是否激活: {student.is_active}")
except User.DoesNotExist:
    print("学员ID 4不存在！")

print("\n=== 检查现有关系 ===")
if 'coach' in locals() and 'student' in locals():
    existing = CoachStudentRelation.objects.filter(coach_id=113, student_id=4).first()
    if existing:
        print(f"已存在关系: 状态={existing.status}, 创建时间={existing.created_at}")
    else:
        print("无现有关系，可以创建新关系")