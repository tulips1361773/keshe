#!/usr/bin/env python
import os
import sys
import django

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'keshe.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
django.setup()

from accounts.models import User
from reservations.models import CoachStudentRelation

def check_current_state():
    print("=== 检查当前系统状态 ===")
    
    # 1. 检查用户状态
    print("\n1. 检查用户状态:")
    try:
        student = User.objects.get(username='hhm')
        print(f"学员: {student.username} (ID: {student.id}, 激活: {student.is_active})")
        
        coach = User.objects.get(id=113)
        print(f"教练: {coach.username} (ID: {coach.id}, 激活: {coach.is_active})")
        
    except User.DoesNotExist as e:
        print(f"❌ 用户不存在: {e}")
        return
    
    # 2. 检查现有关系
    print("\n2. 检查现有关系:")
    relations = CoachStudentRelation.objects.filter(
        coach_id=113, student_id=4
    ).order_by('-created_at')
    
    print(f"关系总数: {relations.count()}")
    for i, relation in enumerate(relations[:5]):  # 显示最近5个
        print(f"  {i+1}. ID: {relation.id}, 状态: {relation.status}, 创建时间: {relation.created_at}")
    
    # 3. 检查所有教练数据结构
    print("\n3. 检查教练数据结构:")
    coaches = User.objects.filter(user_type='coach', is_active=True)[:3]
    for coach in coaches:
        print(f"教练 {coach.id}: username={coach.username}, user_type={coach.user_type}")
    
    # 4. 模拟前端可能发送的数据
    print("\n4. 模拟前端数据:")
    print("前端应该发送的数据格式:")
    print({
        'coach_id': 113,
        'student_id': 4,
        'notes': '学员选择教练：haunghm1'
    })
    
    # 5. 检查是否有其他pending关系
    print("\n5. 检查所有pending关系:")
    pending_relations = CoachStudentRelation.objects.filter(status='pending')
    print(f"系统中pending关系总数: {pending_relations.count()}")
    for relation in pending_relations:
        print(f"  - 教练ID: {relation.coach_id}, 学员ID: {relation.student_id}, 创建时间: {relation.created_at}")

if __name__ == "__main__":
    check_current_state()