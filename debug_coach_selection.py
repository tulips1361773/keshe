#!/usr/bin/env python
"""
调试教练选择API问题的脚本
"""
import os
import django
import json
import requests

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'keshe.settings')
django.setup()

from django.contrib.auth import get_user_model
from reservations.models import CoachStudentRelation

User = get_user_model()

def debug_coach_selection():
    print("=== 调试教练选择API问题 ===\n")
    
    # 1. 检查用户数据
    print("1. 检查用户数据:")
    coaches = User.objects.filter(user_type='coach')[:5]
    students = User.objects.filter(user_type='student')[:5]
    
    print(f"教练数量: {User.objects.filter(user_type='coach').count()}")
    print(f"学员数量: {User.objects.filter(user_type='student').count()}")
    
    print("\n前5个教练:")
    for coach in coaches:
        print(f"  ID: {coach.id}, 用户名: {coach.username}, 姓名: {coach.real_name}")
    
    print("\n前5个学员:")
    for student in students:
        print(f"  ID: {student.id}, 用户名: {student.username}, 姓名: {student.real_name}")
    
    # 2. 模拟前端请求
    if coaches and students:
        coach = coaches[0]
        student = students[0]
        
        print(f"\n2. 模拟API请求:")
        print(f"选择教练: {coach.real_name} (ID: {coach.id})")
        print(f"学员: {student.real_name} (ID: {student.id})")
        
        # 模拟前端发送的数据
        data = {
            'coach_id': coach.id,
            'student_id': student.id,
            'notes': f'学员选择教练：{coach.real_name}'
        }
        
        print(f"发送数据: {json.dumps(data, ensure_ascii=False)}")
        
        # 检查用户是否存在
        try:
            coach_obj = User.objects.get(id=coach.id, user_type='coach')
            student_obj = User.objects.get(id=student.id, user_type='student')
            print(f"✓ 教练存在: {coach_obj.real_name}")
            print(f"✓ 学员存在: {student_obj.real_name}")
        except User.DoesNotExist as e:
            print(f"✗ 用户不存在: {e}")
        
        # 检查是否已有关系
        existing = CoachStudentRelation.objects.filter(
            coach=coach,
            student=student
        ).first()
        
        if existing:
            print(f"✗ 已存在关系: 状态={existing.status}")
        else:
            print("✓ 无现有关系")
    
    print("\n=== 调试完成 ===")

if __name__ == '__main__':
    debug_coach_selection()