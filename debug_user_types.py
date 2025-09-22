#!/usr/bin/env python
import os
import django

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'keshe.settings')
django.setup()

from accounts.models import User, Coach

def check_user_types():
    """检查用户类型和教练关系"""
    print("=== 检查用户类型和教练关系 ===")
    
    # 检查学员hhm
    try:
        student = User.objects.get(username='hhm')
        print(f"✅ 学员 hhm:")
        print(f"   ID: {student.id}")
        print(f"   用户类型: {student.user_type}")
        print(f"   是否激活: {student.is_active}")
    except User.DoesNotExist:
        print("❌ 学员 hhm 不存在")
        return
    
    # 检查教练82
    try:
        coach_user = User.objects.get(id=82)
        print(f"\n✅ 用户 ID 82:")
        print(f"   用户名: {coach_user.username}")
        print(f"   用户类型: {coach_user.user_type}")
        print(f"   是否激活: {coach_user.is_active}")
        
        # 检查是否有对应的Coach记录
        try:
            coach_profile = Coach.objects.get(user_id=82)
            print(f"   教练档案存在: ID={coach_profile.id}, 等级={coach_profile.coach_level}")
        except Coach.DoesNotExist:
            print(f"   ❌ 没有对应的教练档案")
            
    except User.DoesNotExist:
        print("❌ 用户 ID 82 不存在")
    
    # 查找所有教练类型的用户
    print(f"\n=== 所有教练类型用户 ===")
    coach_users = User.objects.filter(user_type='coach')[:10]
    for user in coach_users:
        try:
            coach_profile = Coach.objects.get(user=user)
            print(f"ID: {user.id}, 用户名: {user.username}, 教练档案ID: {coach_profile.id}")
        except Coach.DoesNotExist:
            print(f"ID: {user.id}, 用户名: {user.username}, ❌ 无教练档案")
    
    # 查找所有Coach记录对应的用户
    print(f"\n=== 所有教练档案对应的用户 ===")
    coaches = Coach.objects.all()[:10]
    for coach in coaches:
        user = coach.user
        print(f"教练档案ID: {coach.id}, 用户ID: {user.id}, 用户名: {user.username}, 用户类型: {user.user_type}")

if __name__ == "__main__":
    check_user_types()