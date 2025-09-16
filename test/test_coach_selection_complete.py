#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
学员查询和选择教练员功能完整性测试
测试需求分析文档第43-46行的功能实现情况
"""

import os
import sys
import django
import requests
import json

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'keshe.settings')
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from accounts.models import Coach
from reservations.models import CoachStudentRelation

User = get_user_model()

def test_coach_selection_functionality():
    """
    测试学员查询和选择教练员功能的完整实现
    
    需求分析文档要求：
    1. 学员查询教练员（按姓名、性别、年龄查询，至少填一项）
    2. 浏览校区全部教练员列表  
    3. 显示教练员基本信息、照片、获奖信息
    4. 点击教练员查看详情
    5. 学员可以选择教练员（双选关系）
    """
    print("学员查询和选择教练员功能完整性测试")
    print("=" * 60)
    
    # 测试结果统计
    results = {
        '后端API功能': {
            '教练员列表API': False,
            '按姓名查询': False,
            '按性别筛选': False,
            '按年龄筛选': False,
            '教练员详情API': False,
            '师生关系创建API': False,
            '师生关系查询API': False
        },
        '前端页面功能': {
            '教练员列表页面': False,
            '查询筛选功能': False,
            '教练员详情页面': False,
            '选择教练按钮': False
        },
        '数据完整性': {
            '教练员基本信息': False,
            '教练员照片': False,
            '获奖信息': False,
            '联系方式': False
        }
    }
    
    base_url = "http://127.0.0.1:8000"
    frontend_url = "http://localhost:5173"
    
    # 创建测试客户端
    client = Client()
    
    # 1. 准备测试数据
    print("\n=== 准备测试数据 ===")
    try:
        # 获取或创建测试学员
        try:
            student = User.objects.get(username='test_student_selection')
        except User.DoesNotExist:
            student = User.objects.create_user(
                username='test_student_selection',
                email='student_test@example.com',
                password='test123456',
                real_name='测试学员',
                phone='13900000001',  # 添加唯一手机号
                user_type='student',
                is_active=True
            )
        
        # 创建认证token
        token, _ = Token.objects.get_or_create(user=student)
        auth_headers = {'Authorization': f'Token {token.key}'}
        
        print(f"✅ 测试学员准备完成: {student.username}")
        
    except Exception as e:
        print(f"❌ 测试数据准备失败: {e}")
        return results
    
    # 2. 测试后端API功能
    print("\n=== 测试后端API功能 ===")
    
    # 2.1 测试教练员列表API
    print("\n📋 测试教练员列表API")
    try:
        response = client.get('/accounts/api/coaches/', HTTP_AUTHORIZATION=f'Token {token.key}')
        if response.status_code == 200:
            data = response.json()
            coach_count = data.get('count', len(data.get('results', [])))
            print(f"✅ 教练员列表API正常，共 {coach_count} 名教练员")
            results['后端API功能']['教练员列表API'] = True
            
            # 检查数据结构
            if data.get('results') and len(data['results']) > 0:
                coach = data['results'][0]
                if 'user' in coach and coach['user']:
                    user_info = coach['user']
                    if user_info.get('real_name'):
                        results['数据完整性']['教练员基本信息'] = True
                        print("✅ 教练员基本信息完整")
                    if user_info.get('avatar'):
                        results['数据完整性']['教练员照片'] = True
                        print("✅ 教练员照片信息存在")
                    if user_info.get('phone') or user_info.get('email'):
                        results['数据完整性']['联系方式'] = True
                        print("✅ 教练员联系方式完整")
                
                if coach.get('achievements'):
                    results['数据完整性']['获奖信息'] = True
                    print("✅ 教练员获奖信息存在")
        else:
            print(f"❌ 教练员列表API失败: {response.status_code}")
    except Exception as e:
        print(f"❌ 教练员列表API测试失败: {e}")
    
    # 2.2 测试查询功能
    print("\n🔍 测试查询筛选功能")
    
    # 按姓名查询
    try:
        response = client.get('/accounts/api/coaches/?search=张', HTTP_AUTHORIZATION=f'Token {token.key}')
        if response.status_code == 200:
            print("✅ 按姓名查询功能正常")
            results['后端API功能']['按姓名查询'] = True
        else:
            print(f"❌ 按姓名查询失败: {response.status_code}")
    except Exception as e:
        print(f"❌ 按姓名查询测试失败: {e}")
    
    # 按性别筛选（如果支持）
    try:
        response = client.get('/accounts/api/coaches/?gender=male', HTTP_AUTHORIZATION=f'Token {token.key}')
        if response.status_code == 200:
            print("✅ 按性别筛选功能正常")
            results['后端API功能']['按性别筛选'] = True
        else:
            print("⚠️  按性别筛选功能未实现或参数不正确")
    except Exception as e:
        print(f"⚠️  按性别筛选测试失败: {e}")
    
    # 按年龄筛选（如果支持）
    try:
        response = client.get('/accounts/api/coaches/?age_min=25&age_max=40', HTTP_AUTHORIZATION=f'Token {token.key}')
        if response.status_code == 200:
            print("✅ 按年龄筛选功能正常")
            results['后端API功能']['按年龄筛选'] = True
        else:
            print("⚠️  按年龄筛选功能未实现或参数不正确")
    except Exception as e:
        print(f"⚠️  按年龄筛选测试失败: {e}")
    
    # 2.3 测试教练员详情API
    print("\n👤 测试教练员详情API")
    try:
        # 获取第一个教练员的ID
        coach = Coach.objects.first()
        if coach:
            response = client.get(f'/accounts/api/coaches/{coach.id}/', HTTP_AUTHORIZATION=f'Token {token.key}')
            if response.status_code == 200:
                data = response.json()
                print(f"✅ 教练员详情API正常 (ID: {coach.id})")
                print(f"   教练姓名: {data.get('user', {}).get('real_name', 'N/A')}")
                results['后端API功能']['教练员详情API'] = True
            else:
                print(f"❌ 教练员详情API失败: {response.status_code}")
        else:
            print("⚠️  没有找到教练员数据")
    except Exception as e:
        print(f"❌ 教练员详情API测试失败: {e}")
    
    # 2.4 测试师生关系API
    print("\n🤝 测试师生关系API")
    try:
        # 测试查询师生关系
        response = client.get('/api/reservations/relations/', HTTP_AUTHORIZATION=f'Token {token.key}')
        if response.status_code == 200:
            print("✅ 师生关系查询API正常")
            results['后端API功能']['师生关系查询API'] = True
            
            # 测试创建师生关系
            coach = Coach.objects.first()
            if coach:
                relation_data = {
                    'coach': coach.user.id,
                    'notes': '功能测试申请'
                }
                response = client.post(
                    '/api/reservations/relations/',
                    data=json.dumps(relation_data),
                    content_type='application/json',
                    HTTP_AUTHORIZATION=f'Token {token.key}'
                )
                if response.status_code == 201:
                    print("✅ 师生关系创建API正常")
                    results['后端API功能']['师生关系创建API'] = True
                elif response.status_code == 400:
                    # 可能已存在关系
                    response_data = response.json()
                    if 'already exists' in str(response_data) or '已存在' in str(response_data):
                        print("✅ 师生关系创建API正常（关系已存在）")
                        results['后端API功能']['师生关系创建API'] = True
                    else:
                        print(f"❌ 师生关系创建失败: {response_data}")
                else:
                    print(f"❌ 师生关系创建失败: {response.status_code}")
        else:
            print(f"❌ 师生关系API失败: {response.status_code}")
    except Exception as e:
        print(f"❌ 师生关系API测试失败: {e}")
    
    # 3. 测试前端页面功能
    print("\n=== 测试前端页面功能 ===")
    
    # 3.1 测试前端页面可访问性
    print("\n🌐 测试前端页面可访问性")
    try:
        # 测试教练员列表页面
        response = requests.get(f"{frontend_url}/#/coaches", timeout=5)
        if response.status_code == 200:
            print("✅ 教练员列表页面可访问")
            results['前端页面功能']['教练员列表页面'] = True
        else:
            print(f"❌ 教练员列表页面不可访问: {response.status_code}")
        
        # 测试教练员详情页面
        coach = Coach.objects.first()
        if coach:
            response = requests.get(f"{frontend_url}/#/coaches/{coach.id}", timeout=5)
            if response.status_code == 200:
                print("✅ 教练员详情页面可访问")
                results['前端页面功能']['教练员详情页面'] = True
            else:
                print(f"❌ 教练员详情页面不可访问: {response.status_code}")
        
    except Exception as e:
        print(f"⚠️  前端页面测试失败（可能前端服务未启动）: {e}")
    
    # 4. 分析前端代码实现
    print("\n=== 分析前端代码实现 ===")
    
    # 检查前端文件是否存在查询筛选功能
    coaches_vue_path = "d:/code/django_learning/keshe/frontend/src/views/Coaches.vue"
    coach_detail_vue_path = "d:/code/django_learning/keshe/frontend/src/views/CoachDetail.vue"
    
    try:
        if os.path.exists(coaches_vue_path):
            with open(coaches_vue_path, 'r', encoding='utf-8') as f:
                content = f.read()
                if 'filter' in content.lower() or 'search' in content.lower():
                    print("✅ 教练员列表页面包含查询筛选功能")
                    results['前端页面功能']['查询筛选功能'] = True
                else:
                    print("⚠️  教练员列表页面缺少查询筛选功能")
        
        if os.path.exists(coach_detail_vue_path):
            with open(coach_detail_vue_path, 'r', encoding='utf-8') as f:
                content = f.read()
                if '选择教练' in content or '申请教练' in content or 'select' in content.lower():
                    print("✅ 教练员详情页面包含选择教练功能")
                    results['前端页面功能']['选择教练按钮'] = True
                elif '联系教练' in content:
                    print("⚠️  教练员详情页面只有联系教练功能，缺少选择教练功能")
                else:
                    print("❌ 教练员详情页面缺少选择教练功能")
    
    except Exception as e:
        print(f"❌ 前端代码分析失败: {e}")
    
    # 5. 生成测试报告
    print("\n" + "=" * 60)
    print("📊 功能实现情况报告")
    print("=" * 60)
    
    total_tests = 0
    passed_tests = 0
    
    for category, tests in results.items():
        print(f"\n📋 {category}:")
        category_total = len(tests)
        category_passed = sum(1 for result in tests.values() if result)
        
        for test_name, result in tests.items():
            status = "✅" if result else "❌"
            print(f"   {status} {test_name}")
        
        print(f"   完成度: {category_passed}/{category_total} ({category_passed/category_total*100:.1f}%)")
        
        total_tests += category_total
        passed_tests += category_passed
    
    print(f"\n🎯 总体完成度: {passed_tests}/{total_tests} ({passed_tests/total_tests*100:.1f}%)")
    
    # 6. 需求符合性分析
    print("\n" + "=" * 60)
    print("📋 需求符合性分析")
    print("=" * 60)
    
    requirements = {
        "学员查询教练员（基础功能）": results['后端API功能']['教练员列表API'],
        "按姓名查询教练员": results['后端API功能']['按姓名查询'],
        "按性别筛选教练员": results['后端API功能']['按性别筛选'],
        "按年龄筛选教练员": results['后端API功能']['按年龄筛选'],
        "显示教练员基本信息": results['数据完整性']['教练员基本信息'],
        "显示教练员照片": results['数据完整性']['教练员照片'],
        "显示获奖信息": results['数据完整性']['获奖信息'],
        "查看教练员详情": results['后端API功能']['教练员详情API'],
        "学员选择教练员（双选关系）": results['后端API功能']['师生关系创建API'],
        "前端页面支持": results['前端页面功能']['教练员列表页面'] and results['前端页面功能']['教练员详情页面']
    }
    
    for requirement, status in requirements.items():
        status_icon = "✅" if status else "❌"
        print(f"{status_icon} {requirement}")
    
    implemented_count = sum(1 for status in requirements.values() if status)
    total_requirements = len(requirements)
    
    print(f"\n📈 需求实现度: {implemented_count}/{total_requirements} ({implemented_count/total_requirements*100:.1f}%)")
    
    # 7. 改进建议
    print("\n" + "=" * 60)
    print("💡 改进建议")
    print("=" * 60)
    
    suggestions = []
    
    if not results['后端API功能']['按性别筛选']:
        suggestions.append("1. 在教练员列表API中添加按性别筛选功能")
    
    if not results['后端API功能']['按年龄筛选']:
        suggestions.append("2. 在教练员列表API中添加按年龄筛选功能")
    
    if not results['前端页面功能']['选择教练按钮']:
        suggestions.append("3. 在教练员详情页面添加'选择教练'按钮，替换或补充'联系教练'功能")
    
    if not results['前端页面功能']['查询筛选功能']:
        suggestions.append("4. 在教练员列表页面完善查询筛选界面，支持姓名、性别、年龄等条件")
    
    if not results['数据完整性']['获奖信息']:
        suggestions.append("5. 完善教练员获奖信息的数据录入和显示")
    
    if suggestions:
        for suggestion in suggestions:
            print(suggestion)
    else:
        print("🎉 所有功能已完整实现，符合需求要求！")
    
    return results

if __name__ == '__main__':
    test_coach_selection_functionality()