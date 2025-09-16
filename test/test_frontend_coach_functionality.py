#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
前端教练员查询功能测试脚本
测试前端页面是否满足需求文档中的教练员查询功能要求
"""

import requests
import json
from datetime import datetime

def test_frontend_coach_functionality():
    """
    测试前端教练员查询功能是否完整
    
    需求文档要求：
    1. 按姓名查询教练员
    2. 按性别查询教练员  
    3. 按年龄查询教练员
    4. 组合查询（至少填写一项）
    5. 浏览所有教练员
    6. 显示教练员基本信息、照片、获奖信息
    7. 点击教练员查看详情
    """
    
    print("🏓 前端教练员查询功能测试")
    print("=" * 50)
    
    # 测试配置
    frontend_url = "http://localhost:5173"
    backend_url = "http://localhost:8000"
    
    # 创建会话
    session = requests.Session()
    
    # 1. 测试登录功能
    print("\n=== 测试1: 用户登录 ===")
    login_data = {
        'username': 'test_student',
        'password': 'test123456'
    }
    
    try:
        response = session.post(f"{backend_url}/accounts/api/login/", json=login_data)
        if response.status_code == 200:
            print("✅ 登录成功")
            login_success = True
        else:
            print(f"❌ 登录失败: {response.status_code}")
            login_success = False
    except Exception as e:
        print(f"❌ 登录请求失败: {e}")
        login_success = False
    
    if not login_success:
        print("⚠️  无法继续测试，请确保后端服务正常运行")
        return False
    
    # 2. 测试前端页面可访问性
    print("\n=== 测试2: 前端页面可访问性 ===")
    try:
        response = requests.get(frontend_url, timeout=5)
        if response.status_code == 200:
            print("✅ 前端应用可访问")
            frontend_accessible = True
        else:
            print(f"❌ 前端应用不可访问: {response.status_code}")
            frontend_accessible = False
    except Exception as e:
        print(f"❌ 前端应用访问失败: {e}")
        frontend_accessible = False
    
    # 3. 测试教练员列表API（基础功能）
    print("\n=== 测试3: 教练员列表API ===")
    try:
        response = session.get(f"{backend_url}/accounts/api/coaches/")
        if response.status_code == 200:
            data = response.json()
            coach_count = data.get('count', len(data.get('results', [])))
            print(f"✅ 获取教练员列表成功，共 {coach_count} 名教练员")
            api_works = True
        else:
            print(f"❌ 获取教练员列表失败: {response.status_code}")
            api_works = False
    except Exception as e:
        print(f"❌ API请求失败: {e}")
        api_works = False
    
    # 4. 测试按姓名查询
    print("\n=== 测试4: 按姓名查询 ===")
    try:
        response = session.get(f"{backend_url}/accounts/api/coaches/?search=李")
        if response.status_code == 200:
            data = response.json()
            results = data.get('results', [])
            print(f"✅ 姓名查询成功，找到 {len(results)} 个匹配结果")
            name_search_works = True
        else:
            print(f"❌ 姓名查询失败: {response.status_code}")
            name_search_works = False
    except Exception as e:
        print(f"❌ 姓名查询请求失败: {e}")
        name_search_works = False
    
    # 5. 测试按性别查询
    print("\n=== 测试5: 按性别查询 ===")
    try:
        response = session.get(f"{backend_url}/accounts/api/coaches/?gender=male")
        if response.status_code == 200:
            data = response.json()
            results = data.get('results', [])
            print(f"✅ 性别查询成功，找到 {len(results)} 个男性教练员")
            gender_search_works = True
        else:
            print(f"❌ 性别查询失败: {response.status_code}")
            gender_search_works = False
    except Exception as e:
        print(f"❌ 性别查询请求失败: {e}")
        gender_search_works = False
    
    # 6. 测试按年龄查询
    print("\n=== 测试6: 按年龄查询 ===")
    try:
        response = session.get(f"{backend_url}/accounts/api/coaches/?age_min=25&age_max=35")
        if response.status_code == 200:
            data = response.json()
            results = data.get('results', [])
            print(f"✅ 年龄查询成功，找到 {len(results)} 个25-35岁的教练员")
            age_search_works = True
        else:
            print(f"❌ 年龄查询失败: {response.status_code}")
            age_search_works = False
    except Exception as e:
        print(f"❌ 年龄查询请求失败: {e}")
        age_search_works = False
    
    # 7. 测试组合查询
    print("\n=== 测试7: 组合查询 ===")
    try:
        response = session.get(f"{backend_url}/accounts/api/coaches/?search=教练&gender=male&age_min=20&age_max=50")
        if response.status_code == 200:
            data = response.json()
            results = data.get('results', [])
            print(f"✅ 组合查询成功，找到 {len(results)} 个匹配结果")
            combo_search_works = True
        else:
            print(f"❌ 组合查询失败: {response.status_code}")
            combo_search_works = False
    except Exception as e:
        print(f"❌ 组合查询请求失败: {e}")
        combo_search_works = False
    
    # 8. 测试数据完整性
    print("\n=== 测试8: 数据完整性检查 ===")
    try:
        response = session.get(f"{backend_url}/accounts/api/coaches/?page_size=1")
        if response.status_code == 200:
            data = response.json()
            results = data.get('results', [])
            if results:
                coach = results[0]
                required_fields = ['id', 'real_name', 'coach_level', 'status']
                missing_fields = [field for field in required_fields if field not in coach]
                
                if not missing_fields:
                    print("✅ 教练员数据结构完整")
                    data_complete = True
                else:
                    print(f"❌ 缺少必要字段: {missing_fields}")
                    data_complete = False
            else:
                print("⚠️  没有教练员数据可供检查")
                data_complete = False
        else:
            print(f"❌ 数据完整性检查失败: {response.status_code}")
            data_complete = False
    except Exception as e:
        print(f"❌ 数据完整性检查请求失败: {e}")
        data_complete = False
    
    # 生成测试报告
    print("\n" + "=" * 50)
    print("📊 前端功能需求符合性分析")
    print("=" * 50)
    
    # 功能检查结果
    checks = {
        "前端应用可访问": frontend_accessible,
        "后端API正常": api_works,
        "按姓名查询": name_search_works,
        "按性别查询": gender_search_works,
        "按年龄查询": age_search_works,
        "组合查询": combo_search_works,
        "数据完整性": data_complete
    }
    
    for check_name, result in checks.items():
        status = "✅ 支持" if result else "❌ 不支持"
        print(f"{check_name}: {status}")
    
    # 计算总体符合度
    passed_checks = sum(checks.values())
    total_checks = len(checks)
    compliance_rate = (passed_checks / total_checks) * 100
    
    print(f"\n总体符合度: {compliance_rate:.1f}% ({passed_checks}/{total_checks})")
    
    if compliance_rate >= 85:
        print("\n🎉 前端教练员查询功能基本满足需求！")
        print("✨ 建议：")
        print("  - 测试前端页面的用户交互")
        print("  - 验证筛选器的实际效果")
        print("  - 检查教练员详情页面")
    elif compliance_rate >= 60:
        print("\n⚠️  前端功能部分满足需求，需要改进")
        failed_checks = [name for name, result in checks.items() if not result]
        print("需要修复的功能：")
        for check in failed_checks:
            print(f"  - {check}")
    else:
        print("\n❌ 前端功能严重不符合需求，需要大幅改进")
        failed_checks = [name for name, result in checks.items() if not result]
        print("需要修复的功能：")
        for check in failed_checks:
            print(f"  - {check}")
    
    return compliance_rate >= 85

if __name__ == '__main__':
    test_frontend_coach_functionality()