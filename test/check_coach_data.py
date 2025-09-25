#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import django

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'keshe.settings')
django.setup()

from accounts.models import Coach, User

def check_coach_data():
    print("=== 检查教练员数据完整性 ===")
    
    # 获取所有教练员
    coaches = Coach.objects.all()
    print(f"教练员总数: {coaches.count()}")
    
    if coaches.count() == 0:
        print("❌ 数据库中没有教练员数据")
        return
    
    print("\n=== 教练员详细信息 ===")
    for i, coach in enumerate(coaches, 1):
        print(f"\n教练员 {i}:")
        print(f"  用户名: {coach.user.username}")
        print(f"  真实姓名: {coach.user.real_name}")
        print(f"  性别: {coach.user.gender}")
        print(f"  出生日期: {coach.user.birth_date}")
        print(f"  头像: {coach.user.avatar}")
        print(f"  教练级别: {coach.coach_level}")
        print(f"  比赛成绩: {coach.achievements}")
        print(f"  审核状态: {coach.status}")
        print(f"  时薪: {coach.hourly_rate}")
        
    # 检查数据完整性
    print("\n=== 数据完整性检查 ===")
    missing_data = []
    
    for coach in coaches:
        issues = []
        if not coach.user.real_name:
            issues.append("缺少真实姓名")
        if not coach.user.gender:
            issues.append("缺少性别信息")
        if not coach.user.birth_date:
            issues.append("缺少出生日期")
        if not coach.user.avatar:
            issues.append("缺少头像")
        if not coach.achievements:
            issues.append("缺少比赛成绩信息")
        if not coach.user.phone:
            issues.append("缺少手机号码")
            
        if issues:
            missing_data.append({
                'coach': coach.user.username,
                'issues': issues
            })
    
    if missing_data:
        print("❌ 发现数据不完整的教练员:")
        for item in missing_data:
            print(f"  {item['coach']}: {', '.join(item['issues'])}")
    else:
        print("✅ 所有教练员数据完整")
    
    # 检查审核状态
    approved_coaches = coaches.filter(status='approved').count()
    pending_coaches = coaches.filter(status='pending').count()
    rejected_coaches = coaches.filter(status='rejected').count()
    
    print(f"\n=== 审核状态统计 ===")
    print(f"已审核通过: {approved_coaches}")
    print(f"待审核: {pending_coaches}")
    print(f"已拒绝: {rejected_coaches}")

if __name__ == '__main__':
    check_coach_data()