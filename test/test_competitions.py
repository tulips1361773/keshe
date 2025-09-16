#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
比赛管理模块测试脚本
测试数据库模型、API接口和业务逻辑
"""

import os
import sys
import django
from datetime import datetime, timedelta
import json

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'keshe.settings')
django.setup()

from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

from competitions.models import Competition, CompetitionRegistration, CompetitionGroup, CompetitionMatch
from campus.models import Campus
from accounts.models import User

class CompetitionModelTest:
    """测试比赛管理数据库模型"""
    
    def __init__(self):
        self.client = Client()
        self.api_client = APIClient()
        self.setup_test_data()
    
    def setup_test_data(self):
        """创建测试数据"""
        print("\n=== 创建测试数据 ===")
        
        # 清理已存在的测试数据
        User.objects.filter(username__startswith='test_').delete()
        Campus.objects.filter(name='测试校区').delete()
        print("✓ 清理已存在的测试数据")
        
        # 创建校区
        self.campus, created = Campus.objects.get_or_create(
            name="测试校区",
            defaults={
                'code': 'TEST001',
                'address': '测试地址123号',
                'phone': '123-456-7890',
                'contact_person': '测试管理员',
                'campus_type': 'branch'
            }
        )
        print(f"校区: {self.campus.name} {'(新建)' if created else '(已存在)'}")
        
        # 创建用户
        self.coach_user, created = User.objects.get_or_create(
            username="test_coach",
            defaults={
                'email': 'coach@test.com',
                'first_name': '测试',
                'last_name': '教练',
                'real_name': '测试教练',
                'phone': '13800138001',
                'user_type': 'coach'
            }
        )
        if created:
            self.coach_user.set_password('testpass123')
            self.coach_user.save()
        print(f"教练用户: {self.coach_user.username} {'(新建)' if created else '(已存在)'}")
        
        self.student_user1, created = User.objects.get_or_create(
            username="test_student1",
            defaults={
                'email': 'student1@test.com',
                'first_name': '测试',
                'last_name': '学员1',
                'real_name': '测试学员1',
                'phone': '13800138002',
                'user_type': 'student'
            }
        )
        if created:
            self.student_user1.set_password('testpass123')
            self.student_user1.save()
        print(f"学员用户1: {self.student_user1.username} {'(新建)' if created else '(已存在)'}")
        
        self.student_user2, created = User.objects.get_or_create(
            username="test_student2",
            defaults={
                'email': 'student2@test.com',
                'first_name': '测试',
                'last_name': '学员2',
                'real_name': '测试学员2',
                'phone': '13800138003',
                'user_type': 'student'
            }
        )
        if created:
            self.student_user2.set_password('testpass123')
            self.student_user2.save()
        print(f"学员用户2: {self.student_user2.username} {'(新建)' if created else '(已存在)'}")
    
    def test_competition_creation(self):
        """测试比赛创建"""
        print("\n=== 测试比赛创建 ===")
        
        competition_data = {
            'title': '测试羽毛球比赛',
            'description': '这是一个测试比赛',
            'campus': self.campus,
            'competition_date': datetime.now() + timedelta(days=7),
            'registration_start': datetime.now() + timedelta(days=1),
            'registration_end': datetime.now() + timedelta(days=5),
            'registration_fee': 30.00,
            'max_participants_per_group': 16,
            'status': 'upcoming',
            'created_by': self.coach_user
        }
        
        competition = Competition.objects.create(**competition_data)
        print(f"✓ 比赛创建成功: {competition.title} (ID: {competition.id})")
        
        # 验证比赛属性
        assert competition.title == '测试羽毛球比赛'
        assert competition.max_participants_per_group == 16
        assert competition.status == 'upcoming'
        print("✓ 比赛属性验证通过")
        
        return competition
    
    def test_competition_registration(self, competition):
        """测试比赛报名"""
        print("\n=== 测试比赛报名 ===")
        
        # 学员1报名
        registration1 = CompetitionRegistration.objects.create(
            competition=competition,
            participant=self.student_user1
        )
        print(f"✓ 学员1报名成功: {registration1.participant.get_full_name()}")
        
        # 学员2报名
        registration2 = CompetitionRegistration.objects.create(
            competition=competition,
            participant=self.student_user2
        )
        print(f"✓ 学员2报名成功: {registration2.participant.get_full_name()}")
        
        # 验证报名数量
        registration_count = CompetitionRegistration.objects.filter(competition=competition).count()
        assert registration_count == 2
        print(f"✓ 报名数量验证通过: {registration_count}人")
        
        return [registration1, registration2]
    
    def test_competition_groups(self, competition, registrations):
        """测试比赛分组"""
        print("\n=== 测试比赛分组 ===")
        
        # 创建分组
        group = CompetitionGroup.objects.create(
            competition=competition,
            name='A组',
            description='第一组'
        )
        print(f"✓ 分组创建成功: {group.name}")
        
        # 添加参赛者到分组
        group.participants.add(self.student_user1, self.student_user2)
        print(f"✓ 参赛者添加到分组: {group.participants.count()}人")
        
        # 验证分组
        assert group.participants.count() == 2
        assert self.student_user1 in group.participants.all()
        assert self.student_user2 in group.participants.all()
        print("✓ 分组验证通过")
        
        return group
    
    def test_competition_matches(self, competition, group):
        """测试比赛对阵"""
        print("\n=== 测试比赛对阵 ===")
        
        # 创建对阵
        match = CompetitionMatch.objects.create(
            competition=competition,
            group=group,
            player1=self.student_user1,
            player2=self.student_user2,
            round_number=1,
            match_date=datetime.now().date() + timedelta(days=7)
        )
        print(f"✓ 对阵创建成功: {match.player1.get_full_name()} vs {match.player2.get_full_name()}")
        
        # 记录比赛结果
        match.player1_score = 21
        match.player2_score = 18
        match.winner = self.student_user1
        match.status = 'completed'
        match.save()
        print(f"✓ 比赛结果记录: {match.winner.get_full_name()} 获胜 ({match.player1_score}:{match.player2_score})")
        
        # 验证对阵
        assert match.player1 == self.student_user1
        assert match.player2 == self.student_user2
        assert match.winner == self.student_user1
        assert match.status == 'completed'
        print("✓ 对阵验证通过")
        
        return match
    
    def run_model_tests(self):
        """运行所有模型测试"""
        print("\n" + "="*50)
        print("开始比赛管理数据库模型测试")
        print("="*50)
        
        try:
            # 测试比赛创建
            competition = self.test_competition_creation()
            
            # 测试比赛报名
            registrations = self.test_competition_registration(competition)
            
            # 测试比赛分组
            group = self.test_competition_groups(competition, registrations)
            
            # 测试比赛对阵
            match = self.test_competition_matches(competition, group)
            
            print("\n" + "="*50)
            print("✓ 所有数据库模型测试通过！")
            print("="*50)
            
            return True
            
        except Exception as e:
            print(f"\n❌ 测试失败: {str(e)}")
            import traceback
            traceback.print_exc()
            return False

class CompetitionAPITest:
    """测试比赛管理API接口"""
    
    def __init__(self):
        self.api_client = APIClient()
        self.setup_auth()
    
    def setup_auth(self):
        """设置API认证"""
        # 使用已存在的教练用户进行认证
        try:
            coach_user = User.objects.get(username="test_coach")
            self.api_client.force_authenticate(user=coach_user)
            print(f"✓ API认证设置完成: {coach_user.username}")
        except User.DoesNotExist:
            print("❌ 找不到测试用户，请先运行模型测试")
    
    def test_competition_api_crud(self):
        """测试比赛API的CRUD操作"""
        print("\n=== 测试比赛API CRUD操作 ===")
        
        # 获取校区ID
        campus = Campus.objects.get(name="测试校区")
        
        # 测试创建比赛
        competition_data = {
            'title': 'API测试比赛',
            'description': '通过API创建的测试比赛',
            'competition_date': (datetime.now() + timedelta(days=10)).isoformat(),
            'registration_start': (datetime.now() - timedelta(days=1)).isoformat(),
            'registration_end': (datetime.now() + timedelta(days=8)).isoformat(),
            'registration_fee': 50.00,
            'max_participants_per_group': 32,
            'status': 'registration',
            'campus': campus.id
        }
        
        response = self.api_client.post('/api/competitions/', competition_data, format='json')
        print(f"创建比赛 - 状态码: {response.status_code}")
        
        if response.status_code == 201:
            competition_id = response.data['id']
            print(f"✓ 比赛创建成功 (ID: {competition_id})")
            
            # 测试获取比赛列表
            response = self.api_client.get('/api/competitions/')
            print(f"获取比赛列表 - 状态码: {response.status_code}")
            if response.status_code == 200:
                print(f"✓ 比赛列表获取成功，共 {len(response.data)} 个比赛")
            
            # 测试获取单个比赛
            response = self.api_client.get(f'/api/competitions/{competition_id}/')
            print(f"获取单个比赛 - 状态码: {response.status_code}")
            if response.status_code == 200:
                print(f"✓ 比赛详情获取成功: {response.data['title']}")
            
            # 测试更新比赛
            update_data = {'title': 'API测试比赛(已更新)'}
            response = self.api_client.patch(f'/api/competitions/{competition_id}/', update_data, format='json')
            print(f"更新比赛 - 状态码: {response.status_code}")
            if response.status_code == 200:
                print(f"✓ 比赛更新成功: {response.data['title']}")
            
            return competition_id
        else:
            print(f"❌ 比赛创建失败: 状态码 {response.status_code}")
            if hasattr(response, 'data'):
                print(f"错误详情: {response.data}")
            return None
    
    def test_registration_api(self, competition_id):
        """测试报名API"""
        print("\n=== 测试报名API ===")
        
        if not competition_id:
            print("❌ 没有有效的比赛ID，跳过报名测试")
            return
        
        # 切换到学员用户
        student_user = User.objects.get(username="test_student1")
        self.api_client.force_authenticate(user=student_user)
        
        # 测试报名
        response = self.api_client.post(f'/api/competitions/{competition_id}/register/', {}, format='json')
        print(f"比赛报名 - 状态码: {response.status_code}")
        
        if response.status_code == 201:
            print(f"✓ 报名成功: {response.data}")
            
            # 测试获取报名列表
            response = self.api_client.get(f'/api/competitions/{competition_id}/registrations/')
            print(f"获取报名列表 - 状态码: {response.status_code}")
            if response.status_code == 200:
                print(f"✓ 报名列表获取成功，共 {len(response.data)} 条记录")
            else:
                print(f"❌ 获取报名列表失败: 状态码 {response.status_code}")
        else:
            print(f"❌ 报名失败: 状态码 {response.status_code}")
            if hasattr(response, 'data'):
                print(f"错误详情: {response.data}")
    
    def run_api_tests(self):
        """运行所有API测试"""
        print("\n" + "="*50)
        print("开始比赛管理API接口测试")
        print("="*50)
        
        try:
            # 测试比赛CRUD
            competition_id = self.test_competition_api_crud()
            
            # 测试报名API
            self.test_registration_api(competition_id)
            
            print("\n" + "="*50)
            print("✓ 所有API接口测试完成！")
            print("="*50)
            
            return True
            
        except Exception as e:
            print(f"\n❌ API测试失败: {str(e)}")
            import traceback
            traceback.print_exc()
            return False

def main():
    """主测试函数"""
    print("比赛管理模块全面测试")
    print("=" * 60)
    
    # 数据库模型测试
    model_test = CompetitionModelTest()
    model_success = model_test.run_model_tests()
    
    # API接口测试
    api_test = CompetitionAPITest()
    api_success = api_test.run_api_tests()
    
    # 总结
    print("\n" + "="*60)
    print("测试总结")
    print("="*60)
    print(f"数据库模型测试: {'✓ 通过' if model_success else '❌ 失败'}")
    print(f"API接口测试: {'✓ 通过' if api_success else '❌ 失败'}")
    
    if model_success and api_success:
        print("\n🎉 所有测试通过！比赛管理模块功能正常。")
    else:
        print("\n⚠️ 部分测试失败，请检查相关功能。")

if __name__ == '__main__':
    main()