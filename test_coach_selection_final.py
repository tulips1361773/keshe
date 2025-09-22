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

def test_coach_selection():
    print("=== 测试选择教练功能 ===")
    
    # 检查用户
    try:
        coach = User.objects.get(id=113)
        student = User.objects.get(id=4)
        print(f"教练: {coach.username} (ID: {coach.id}, 类型: {coach.user_type})")
        print(f"学员: {student.username} (ID: {student.id}, 类型: {student.user_type})")
    except User.DoesNotExist as e:
        print(f"用户不存在: {e}")
        return
    
    # 检查现有关系
    existing_relations = CoachStudentRelation.objects.filter(
        coach_id=113, student_id=4
    )
    print(f"\n现有关系数量: {existing_relations.count()}")
    for relation in existing_relations:
        print(f"- 状态: {relation.status}, 创建时间: {relation.created_at}")
    
    # 模拟创建新关系
    if existing_relations.count() == 0:
        print("\n✅ 可以创建新的教练-学员关系")
        try:
            # 创建测试关系
            relation = CoachStudentRelation.objects.create(
                coach_id=113,
                student_id=4,
                notes="测试选择教练",
                status='pending'
            )
            print(f"✅ 成功创建关系 ID: {relation.id}")
            
            # 立即删除测试关系
            relation.delete()
            print("✅ 测试关系已删除")
            
        except Exception as e:
            print(f"❌ 创建关系失败: {e}")
    else:
        print("\n❌ 已存在关系，无法创建新关系")
        print("建议删除现有关系后重试")

if __name__ == "__main__":
    test_coach_selection()