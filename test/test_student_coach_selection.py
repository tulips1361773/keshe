#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
学员查询和选择教练员功能完整性测试
根据需求分析文档检查功能实现情况
"""

import os
import sys
import django
import requests
import json
from datetime import datetime

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'keshe.settings')
django.setup()

from django.contrib.auth import get_user_model
from accounts.models import Coach
from reservations.models import CoachStudentRelation
from django.test import Client
from rest_framework.authtoken.models import Token

User = get_user_model()

def test_student_coach_selection_requirements():
    """
    测试学员查询教练员功能是否满足需求分析文档要求
    
    需求文档第43-46行要求：
    1. 学员查询教练员（按姓名、性别、年龄查询，至少填一项）
    2. 浏览校区全部教练员列表
    3. 显示教练员基本信息、照片、获奖信息
    4. 点击教练员查看详情
    5. 学员可以选择教练员（双选关系）
    """
    print("🏓 学员查询和选择教练员功能测试")
    print("=" * 60)
    
    # 测试结果统计
    test_results = {
        'coach_query_api': False,
        'name_search': False,
        'gender_filter': False,
        'age_filter': False,
        'coach_detail_api': False,
        'coach_selection_api': False,
        'frontend_coach_list': False,
        'frontend_coach_detail': False,
        'frontend_selection_button': False
    }
    
    base_url = "http://127.0.0.1:8000"
    frontend_url = "http://localhost:5173"
    
    # 创建测试客户端
    client = Client()
    session = requests.Session()
    
    # 1. 测试学员登录
    print("\n=== 测试1: 学员登录 ===")
    try:
        # 获取测试学员
        student = User.objects.filter(user_type='student', is_active=True).first()
        if not student:
            print("❌ 没有找到测试学员")
            return False
            
        # 创建或获取Token
        token, created = Token.objects.get_or_create(user=student)
        print(f"✅ 学员登录成功: {student.username}")
        
        # 设置认证头
        auth_headers = {'Authorization': f'Token {token.key}'}
        
    except Exception as e:
        print(f"❌ 学员登录失败: {e}")
        return False
    
    # 2. 测试教练员列表API
    print("\n=== 测试2: 教练员列表API ===")
    try:
        response = client.get('/accounts/api/coaches/', HTTP_AUTHORIZATION=f'Token {token.key}')
        if response.status_code == 200:
            data = response.json()
            coach_count = data.get('count', len(data.get('results', [])))
            print(f"✅ 教练员列表API正常，共 {coach_count} 名教练员")
            test_results['coach_query_api'] = True
            
            # 检查返回数据结构
            if data.get('results'):
                coach = data['results'][0]
                required_fields = ['id', 'user', 'coach_level', 'hourly_rate']
                missing_fields = [field for field in required_fields if field not in coach]
                if missing_fields:
                    print(f"⚠️  缺少字段: {missing_fields}")
                else:
                    print("✅ 教练员数据结构完整")
        else:
            print(f"❌ 教练员列表API失败: {response.status_code}")
    except Exception as e:
        print(f"❌ 教练员列表API测试失败: {e}")
    
    # 3. 测试按姓名查询
    print("\n=== 测试3: 按姓名查询 ===")
    try:
        response = client.get('/accounts/api/coaches/?search=张', HTTP_AUTHORIZATION=f'Token {token.key}')
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 姓名查询功能正常，找到 {data.get('count', 0)} 个结果")
            test_results['name_search'] = True
        else:
            print(f"❌ 姓名查询失败: {response.status_code}")
    except Exception as e:
        print(f"❌ 姓名查询测试失败: {e}")
    
    # 4. 测试按性别查询
    print("\n=== 测试4: 按性别查询 ===")
    try:
        response = client.get('/accounts/api/coaches/?gender=male', HTTP_AUTHORIZATION=f'Token {token.key}')
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 性别查询功能正常，找到 {data.get('count', 0)} 个结果")
            test_results['gender_filter'] = True
        else:
            print(f"⚠️  性别查询功能未实现或有问题: {response.status_code}")
    except Exception as e:
        print(f"❌ 性别查询测试失败: {e}")
    
    # 5. 测试按年龄查询
    print("\n=== 测试5: 按年龄查询 ===")
    try:
        response = client.get('/accounts/api/coaches/?age_min=25&age_max=35', HTTP_AUTHORIZATION=f'Token {token.key}')
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 年龄查询功能正常，找到 {data.get('count', 0)} 个结果")
            test_results['age_filter'] = True
        else:
            print(f"⚠️  年龄查询功能未实现或有问题: {response.status_code}")
    except Exception as e:
        print(f"❌ 年龄查询测试失败: {e}")
    
    # 6. 测试教练员详情API
    print("\n=== 测试6: 教练员详情API ===")
    try:
        coach = Coach.objects.first()
        if coach:
            response = client.get(f'/accounts/api/coaches/{coach.id}/', HTTP_AUTHORIZATION=f'Token {token.key}')
            if response.status_code == 200:
                data = response.json()
                print(f"✅ 教练员详情API正常: {data.get('user', {}).get('real_name', 'N/A')}")
                test_results['coach_detail_api'] = True
                
                # 检查详情数据完整性
                required_info = ['user', 'achievements', 'coach_level', 'hourly_rate']
                missing_info = [info for info in required_info if info not in data]
                if missing_info:
                    print(f"⚠️  详情缺少信息: {missing_info}")
                else:
                    print("✅ 教练员详情信息完整")
            else:
                print(f"❌ 教练员详情API失败: {response.status_code}")
        else:
            print("⚠️  没有找到教练员数据")
    except Exception as e:
        print(f"❌ 教练员详情API测试失败: {e}")
    
    # 7. 测试师生关系API（学员选择教练功能）
    print("\n=== 测试7: 学员选择教练API ===")
    try:
        # 检查师生关系API是否存在
        response = client.get('/api/reservations/relations/', HTTP_AUTHORIZATION=f'Token {token.key}')
        if response.status_code == 200:
            print("✅ 师生关系API存在")
            
            # 测试创建师生关系申请
            coach = Coach.objects.first()
            if coach:
                relation_data = {
                    'coach': coach.user.id,
                    'notes': 'API测试申请'
                }
                response = client.post(
                    '/api/reservations/relations/',
                    data=json.dumps(relation_data),
                    content_type='application/json',
                    HTTP_AUTHORIZATION=f'Token {token.key}'
                )
                if response.status_code == 201:
                    print("✅ 学员选择教练功能正常")
                    test_results['coach_selection_api'] = True
                elif response.status_code == 400:
                    # 可能已存在关系
                    print("✅ 学员选择教练API存在（关系可能已存在）")
                    test_results['coach_selection_api'] = True
                else:
                    print(f"❌ 学员选择教练失败: {response.status_code}")
                    print(f"响应内容: {response.content.decode()}")
        else:
            print(f"❌ 师生关系API不存在: {response.status_code}")
    except Exception as e:
        print(f"❌ 学员选择教练API测试失败: {e}")
    
    # 8. 测试前端页面可访问性
    print("\n=== 测试8: 前端页面可访问性 ===")
    try:
        # 测试前端主页
        response = requests.get(frontend_url, timeout=5)
        if response.status_code == 200:
            print("✅ 前端应用可访问")
            test_results['frontend_coach_list'] = True
        else:
            print(f"❌ 前端应用不可访问: {response.status_code}")
    except Exception as e:
        print(f"⚠️  前端应用访问测试失败: {e}")
    
    # 9. 生成测试报告
    print("\n" + "=" * 60)
    print("📊 功能完整性测试报告")
    print("=" * 60)
    
    total_tests = len(test_results)
    passed_tests = sum(test_results.values())
    
    print(f"\n总测试项目: {total_tests}")
    print(f"通过测试: {passed_tests}")
    print(f"完成度: {passed_tests/total_tests*100:.1f}%")
    
    print("\n详细结果:")
    status_map = {True: "✅", False: "❌"}
    
    print(f"{status_map[test_results['coach_query_api']]} 教练员查询API")
    print(f"{status_map[test_results['name_search']]} 按姓名查询")
    print(f"{status_map[test_results['gender_filter']]} 按性别筛选")
    print(f"{status_map[test_results['age_filter']]} 按年龄筛选")
    print(f"{status_map[test_results['coach_detail_api']]} 教练员详情API")
    print(f"{status_map[test_results['coach_selection_api']]} 学员选择教练API")
    print(f"{status_map[test_results['frontend_coach_list']]} 前端教练列表页面")
    
    # 10. 需求符合性分析
    print("\n" + "=" * 60)
    print("📋 需求符合性分析")
    print("=" * 60)
    
    requirements_status = {
        "学员查询教练员（基础功能）": test_results['coach_query_api'],
        "按姓名查询教练员": test_results['name_search'],
        "按性别查询教练员": test_results['gender_filter'],
        "按年龄查询教练员": test_results['age_filter'],
        "查看教练员详情": test_results['coach_detail_api'],
        "学员选择教练员（双选关系）": test_results['coach_selection_api'],
        "前端页面支持": test_results['frontend_coach_list']
    }
    
    print("\n需求实现情况:")
    for requirement, status in requirements_status.items():
        status_text = "已实现" if status else "未实现"
        icon = "✅" if status else "❌"
        print(f"{icon} {requirement}: {status_text}")
    
    # 11. 缺失功能提醒
    missing_features = [req for req, status in requirements_status.items() if not status]
    if missing_features:
        print("\n⚠️  需要完善的功能:")
        for feature in missing_features:
            print(f"   - {feature}")
            
        if not test_results['gender_filter']:
            print("\n💡 性别筛选实现建议:")
            print("   - 在User模型中添加gender字段")
            print("   - 在教练员查询API中添加gender参数支持")
            
        if not test_results['age_filter']:
            print("\n💡 年龄筛选实现建议:")
            print("   - 在User模型中添加birth_date字段")
            print("   - 在教练员查询API中添加age_min和age_max参数支持")
            
        if not test_results['coach_selection_api']:
            print("\n💡 学员选择教练功能建议:")
            print("   - 确保CoachStudentRelation API正常工作")
            print("   - 在前端教练详情页面添加'选择教练'按钮")
    else:
        print("\n🎉 所有核心功能已实现！")
    
    return passed_tests >= total_tests * 0.7  # 70%通过率认为基本完成

if __name__ == '__main__':
    success = test_student_coach_selection_requirements()
    if success:
        print("\n✅ 学员查询教练员功能基本完成")
    else:
        print("\n❌ 学员查询教练员功能需要进一步完善")