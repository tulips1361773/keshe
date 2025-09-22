#!/usr/bin/env python
"""
检查可用教练和现有师生关系的脚本
"""
import os
import django

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'keshe.settings')
django.setup()

from django.contrib.auth import get_user_model
from reservations.models import CoachStudentRelation

User = get_user_model()

def check_available_coaches():
    print("=== 检查可用教练和师生关系 ===\n")
    
    # 获取一个测试学员
    student = User.objects.filter(user_type='student').first()
    if not student:
        print("没有找到学员用户")
        return
    
    print(f"测试学员: {student.real_name} (ID: {student.id})")
    
    # 检查该学员的现有关系
    existing_relations = CoachStudentRelation.objects.filter(student=student)
    print(f"\n该学员现有的师生关系数量: {existing_relations.count()}")
    
    for relation in existing_relations:
        print(f"  - 教练: {relation.coach.real_name} (ID: {relation.coach.id}), 状态: {relation.status}")
    
    # 获取所有教练
    all_coaches = User.objects.filter(user_type='coach')
    print(f"\n所有教练数量: {all_coaches.count()}")
    
    # 找出该学员可以选择的教练（没有关系或关系已终止的）
    available_coaches = []
    for coach in all_coaches:
        existing = CoachStudentRelation.objects.filter(
            coach=coach,
            student=student
        ).first()
        
        if not existing:
            available_coaches.append((coach, "无关系"))
        elif existing.status == 'terminated':
            available_coaches.append((coach, "关系已终止"))
        else:
            print(f"  不可选择: {coach.real_name} (ID: {coach.id}) - 状态: {existing.status}")
    
    print(f"\n可选择的教练数量: {len(available_coaches)}")
    for coach, reason in available_coaches[:5]:  # 只显示前5个
        print(f"  ✓ {coach.real_name} (ID: {coach.id}) - {reason}")
    
    # 建议测试数据
    if available_coaches:
        coach, _ = available_coaches[0]
        print(f"\n建议测试数据:")
        print(f"  coach_id: {coach.id}")
        print(f"  student_id: {student.id}")
        print(f"  教练姓名: {coach.real_name}")
        print(f"  学员姓名: {student.real_name}")
    
    print("\n=== 检查完成 ===")

if __name__ == '__main__':
    check_available_coaches()