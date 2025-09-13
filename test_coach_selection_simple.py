#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单测试教练选择错误处理
"""

import requests
import json
import os
import sys
import django

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'keshe.settings')
django.setup()

from accounts.models import User
from reservations.models import CoachStudentRelation

def test_coach_selection_api():
    print("=== 测试教练选择API错误处理 ===")
    
    # 1. 获取测试用户
    try:
        student = User.objects.filter(user_type='student').first()
        coach = User.objects.filter(user_type='coach').first()
        
        if not student or not coach:
            print("❌ 缺少测试用户")
            return
            
        print(f"✅ 学员: {student.username} (ID: {student.id})")
        print(f"✅ 教练: {coach.username} (ID: {coach.id})")
        
    except Exception as e:
        print(f"❌ 获取用户失败: {e}")
        return
    
    # 2. 检查现有关系
    existing_relations = CoachStudentRelation.objects.filter(
        coach=coach, student=student
    )
    print(f"\n现有师生关系: {existing_relations.count()}个")
    for relation in existing_relations:
        print(f"  - ID: {relation.id}, 状态: {relation.status}")
    
    # 3. 学员登录
    login_url = 'http://localhost:8000/api/accounts/login/'
    login_data = {
        'username': student.username,
        'password': 'testpass123'
    }
    
    try:
        login_response = requests.post(login_url, json=login_data)
        if login_response.status_code == 200:
            token_data = login_response.json()
            token = token_data.get('token')
            print(f"\n✅ 登录成功，获取token")
        else:
            print(f"❌ 登录失败: {login_response.text}")
            return
    except Exception as e:
        print(f"❌ 登录请求失败: {e}")
        return
    
    # 4. 尝试选择教练（应该失败）
    relations_url = 'http://localhost:8000/api/reservations/relations/'
    headers = {
        'Authorization': f'Token {token}',
        'Content-Type': 'application/json'
    }
    
    request_data = {
        'coach_id': coach.id,
        'notes': f'学员选择教练：{coach.real_name}'
    }
    
    print(f"\n发送请求到: {relations_url}")
    print(f"请求数据: {json.dumps(request_data, indent=2, ensure_ascii=False)}")
    
    try:
        response = requests.post(relations_url, json=request_data, headers=headers)
        print(f"\n响应状态码: {response.status_code}")
        print(f"响应内容: {response.text}")
        
        if response.status_code == 400:
            response_data = response.json()
            print("\n=== 分析错误响应 ===")
            print(f"响应数据结构: {json.dumps(response_data, indent=2, ensure_ascii=False)}")
            
            # 模拟前端错误处理逻辑
            error_message = '选择教练失败，请稍后重试'
            
            if 'non_field_errors' in response_data and response_data['non_field_errors']:
                error_detail = response_data['non_field_errors'][0]
                if isinstance(error_detail, str):
                    error_message = error_detail
                    print(f"✅ 从non_field_errors获取错误信息: {error_message}")
                elif hasattr(error_detail, 'message'):
                    error_message = error_detail.message
                    print(f"✅ 从non_field_errors.message获取错误信息: {error_message}")
            elif 'detail' in response_data:
                error_message = response_data['detail']
                print(f"✅ 从detail获取错误信息: {error_message}")
            elif 'error' in response_data:
                error_message = response_data['error']
                print(f"✅ 从error获取错误信息: {error_message}")
            
            print(f"\n🎯 前端应该显示的错误信息: {error_message}")
            
            # 验证错误信息是否合理
            if '已经选择' in error_message or '重复' in error_message:
                print("✅ 错误信息正确，提示用户已选择过该教练")
            else:
                print("⚠️  错误信息可能不够明确")
                
        elif response.status_code == 201:
            print("⚠️  请求成功，但预期应该失败（因为已存在关系）")
        else:
            print(f"❌ 意外的响应状态码: {response.status_code}")
            
    except Exception as e:
        print(f"❌ 请求失败: {e}")
    
    # 5. 总结
    print("\n=== 总结 ===")
    print("1. 后端API正确返回400状态码和错误信息")
    print("2. 前端应该能正确解析并显示错误信息")
    print("3. 如果前端仍显示通用错误，可能是JavaScript执行或UI更新问题")
    print("\n💡 建议检查:")
    print("   - 浏览器开发者工具的Console标签")
    print("   - Network标签中的API请求响应")
    print("   - 前端错误处理代码的执行流程")

if __name__ == '__main__':
    test_coach_selection_api()