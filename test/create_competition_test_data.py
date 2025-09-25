#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
创建比赛对战生成功能测试数据
"""

import os
import sys
import django
from datetime import datetime, timedelta

# 添加项目路径到sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(current_dir)
sys.path.insert(0, project_dir)

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'keshe.settings')
django.setup()

from django.contrib.auth import get_user_model
from competitions.models import Competition, CompetitionRegistration
from campus.models import Campus
from django.utils import timezone

User = get_user_model()

def create_competition_test_data():
    """创建比赛测试数据"""
    print("=== 创建比赛对战生成测试数据 ===\n")
    
    try:
        # 1. 创建或获取管理员用户
        admin_user, created = User.objects.get_or_create(
            username='test_admin',
            defaults={
                'real_name': '测试管理员',
                'user_type': 'super_admin',
                'email': 'admin@test.com',
                'phone': '13800000001',
                'is_active': True,
                'is_superuser': True,
                'is_staff': True
            }
        )
        
        if created:
            admin_user.set_password('admin123')
            admin_user.save()
            print(f"✅ 创建管理员账号: {admin_user.username}")
        else:
            print(f"📋 管理员账号已存在: {admin_user.username}")
        
        # 2. 获取或创建校区
        campus = Campus.objects.first()
        if not campus:
            campus = Campus.objects.create(
                name='测试校区',
                address='测试地址',
                description='用于测试的校区'
            )
            print(f"✅ 创建校区: {campus.name}")
        else:
            print(f"📋 使用校区: {campus.name}")
        
        # 3. 创建测试学员（参赛者）
        students_data = [
            {'username': 'student1', 'real_name': '张三'},
            {'username': 'student2', 'real_name': '李四'},
            {'username': 'student3', 'real_name': '王五'},
            {'username': 'student4', 'real_name': '赵六'},
            {'username': 'student5', 'real_name': '钱七'},
            {'username': 'student6', 'real_name': '孙八'},
            {'username': 'student7', 'real_name': '周九'},
            {'username': 'student8', 'real_name': '吴十'},
        ]
        
        students = []
        for i, data in enumerate(students_data, 1):
            student, created = User.objects.get_or_create(
                username=data['username'],
                defaults={
                    'real_name': data['real_name'],
                    'user_type': 'student',
                    'email': f"{data['username']}@test.com",
                    'phone': f'1380000000{i+1}',
                    'is_active': True,
                    'is_active_member': True
                }
            )
            
            if created:
                student.set_password('123456')
                student.save()
                print(f"✅ 创建学员: {student.real_name}")
            else:
                print(f"📋 学员已存在: {student.real_name}")
            
            students.append(student)
        
        # 4. 创建测试比赛（循环赛）
        competition_date = timezone.now() + timedelta(days=7)
        registration_start = timezone.now() - timedelta(days=3)
        registration_end = timezone.now() + timedelta(days=2)
        
        round_robin_competition, created = Competition.objects.get_or_create(
            name='测试循环赛',
            defaults={
                'title': '测试循环赛比赛',
                'competition_type': 'individual',
                'description': '用于测试循环赛对战生成的比赛',
                'campus': campus,
                'competition_date': competition_date,
                'registration_start': registration_start,
                'registration_end': registration_end,
                'registration_fee': 50.00,
                'max_participants_per_group': 20,
                'status': 'registration',
                'created_by': admin_user
            }
        )
        
        if created:
            print(f"✅ 创建循环赛: {round_robin_competition.name}")
        else:
            print(f"📋 循环赛已存在: {round_robin_competition.name}")
        
        # 5. 创建测试比赛（分组淘汰赛）
        group_knockout_competition, created = Competition.objects.get_or_create(
            name='测试分组淘汰赛',
            defaults={
                'title': '测试分组淘汰赛比赛',
                'competition_type': 'individual',
                'description': '用于测试分组淘汰赛对战生成的比赛',
                'campus': campus,
                'competition_date': competition_date,
                'registration_start': registration_start,
                'registration_end': registration_end,
                'registration_fee': 80.00,
                'max_participants_per_group': 20,
                'status': 'registration',
                'created_by': admin_user
            }
        )
        
        if created:
            print(f"✅ 创建分组淘汰赛: {group_knockout_competition.name}")
        else:
            print(f"📋 分组淘汰赛已存在: {group_knockout_competition.name}")
        
        # 6. 为循环赛创建报名记录（4名参赛者）
        for student in students[:4]:
            registration, created = CompetitionRegistration.objects.get_or_create(
                competition=round_robin_competition,
                participant=student,
                defaults={
                    'registration_time': timezone.now() - timedelta(days=1),
                    'status': 'confirmed',
                    'payment_status': True  # 布尔值而不是字符串
                }
            )
            
            if created:
                print(f"✅ 循环赛报名: {student.real_name}")
            else:
                print(f"📋 循环赛报名已存在: {student.real_name}")
        
        # 7. 为分组淘汰赛创建报名记录（8名参赛者）
        for student in students:
            registration, created = CompetitionRegistration.objects.get_or_create(
                competition=group_knockout_competition,
                participant=student,
                defaults={
                    'registration_time': timezone.now() - timedelta(days=1),
                    'status': 'confirmed',
                    'payment_status': True  # 布尔值而不是字符串
                }
            )
            
            if created:
                print(f"✅ 分组淘汰赛报名: {student.real_name}")
            else:
                print(f"📋 分组淘汰赛报名已存在: {student.real_name}")
        
        print(f"\n=== 测试数据创建完成 ===")
        print(f"管理员: {admin_user.real_name} (用户名: {admin_user.username}, 密码: admin123)")
        print(f"校区: {campus.name}")
        print(f"循环赛: {round_robin_competition.name} (ID: {round_robin_competition.id})")
        print(f"  - 参赛人数: {CompetitionRegistration.objects.filter(competition=round_robin_competition, status='confirmed').count()}")
        print(f"分组淘汰赛: {group_knockout_competition.name} (ID: {group_knockout_competition.id})")
        print(f"  - 参赛人数: {CompetitionRegistration.objects.filter(competition=group_knockout_competition, status='confirmed').count()}")
        
        return {
            'admin_user': admin_user,
            'round_robin_competition': round_robin_competition,
            'group_knockout_competition': group_knockout_competition,
            'students': students
        }
        
    except Exception as e:
        print(f"❌ 创建测试数据失败: {e}")
        import traceback
        traceback.print_exc()
        return None

def print_test_instructions():
    """打印测试说明"""
    print(f"\n{'='*60}")
    print("🏓 对战生成功能测试说明")
    print(f"{'='*60}")
    
    print("\n📋 测试步骤:")
    print("1. 使用管理员账号登录: test_admin / admin123")
    print("2. 访问 Django Admin: http://127.0.0.1:8000/admin/")
    print("3. 进入 Competitions > Competitions")
    print("4. 选择要测试的比赛")
    
    print("\n🔧 API测试方法:")
    print("使用以下API端点生成对战:")
    print("- 循环赛: POST /api/competitions/{competition_id}/generate_matches/")
    print("- 请求体: {\"match_format\": \"round_robin\"}")
    print("- 分组淘汰赛: POST /api/competitions/{competition_id}/generate_matches/")
    print("- 请求体: {\"match_format\": \"group_knockout\"}")
    
    print("\n✅ 验证要点:")
    print("- 循环赛应生成 C(4,2) = 6 场比赛")
    print("- 分组淘汰赛应生成分组赛 + 淘汰赛比赛")
    print("- 每场比赛都有正确的时间安排和球台分配")
    print("- 比赛状态应更新为 'in_progress'")
    
    print(f"\n{'='*60}")

if __name__ == '__main__':
    result = create_competition_test_data()
    if result:
        print_test_instructions()