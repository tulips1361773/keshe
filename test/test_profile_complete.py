#!/usr/bin/env python
import os
import sys
import django
import requests
import json
from datetime import datetime

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'keshe.settings')
django.setup()

from accounts.models import User, UserProfile
from rest_framework.authtoken.models import Token

def test_profile_completeness():
    """测试个人信息展示页面的完整性"""
    print("=== 测试个人信息展示页面完整性 ===")
    
    # 查找一个有完整信息的用户，或创建一个
    user = User.objects.filter(user_type='coach').first()
    if not user:
        print("❌ 没有找到测试用户")
        return
    
    # 确保用户有完整的资料
    user.real_name = "张教练"
    user.phone = "13800138001"
    user.email = "zhang.coach@example.com"
    user.gender = "male"
    user.address = "北京市朝阳区体育馆路1号"
    user.emergency_contact = "张太太"
    user.emergency_phone = "13800138002"
    user.save()
    
    # 确保用户有UserProfile
    profile, created = UserProfile.objects.get_or_create(user=user)
    profile.bio = "专业乒乓球教练，拥有10年教学经验，曾获得全国比赛冠军。"
    profile.skills = "乒乓球基础技能、高级技巧、战术指导"
    profile.experience_years = 10
    profile.save()
    
    print(f"测试用户: {user.username}")
    print(f"真实姓名: {user.real_name}")
    print(f"用户类型: {user.user_type}")
    print(f"头像: {user.avatar or '无'}")
    
    # 获取token
    token, created = Token.objects.get_or_create(user=user)
    
    # 测试API
    headers = {'Authorization': f'Token {token.key}'}
    
    try:
        response = requests.get('http://localhost:8000/accounts/api/profile/', headers=headers)
        print(f"\nAPI响应状态: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            
            print("\n=== 检查返回的字段完整性 ===")
            
            # 检查用户基本信息
            user_data = data.get('user', {})
            profile_data = data.get('profile', {})
            
            fields_to_check = {
                '用户名': user_data.get('username'),
                '真实姓名': user_data.get('real_name'),
                '手机号码': user_data.get('phone'),
                '邮箱地址': user_data.get('email'),
                '性别': user_data.get('gender'),
                '地址': user_data.get('address'),
                '紧急联系人': user_data.get('emergency_contact'),
                '紧急联系电话': user_data.get('emergency_phone'),
                '用户类型': user_data.get('user_type'),
                '注册时间': user_data.get('registration_date'),
                '头像': user_data.get('avatar'),
                '个人简介': profile_data.get('bio'),
                '技能': profile_data.get('skills'),
                '经验年数': profile_data.get('experience_years')
            }
            
            for field_name, field_value in fields_to_check.items():
                status = "✅" if field_value else "❌"
                print(f"{status} {field_name}: {field_value or '未填写'}")
            
            # 检查头像访问
            avatar_url = user_data.get('avatar')
            if avatar_url:
                try:
                    full_url = f"http://localhost:8000{avatar_url}"
                    avatar_response = requests.get(full_url)
                    if avatar_response.status_code == 200:
                        print(f"✅ 头像可正常访问: {full_url}")
                    else:
                        print(f"❌ 头像访问失败: {avatar_response.status_code}")
                except Exception as e:
                    print(f"❌ 头像访问异常: {str(e)}")
            
            print("\n=== 完整性检查总结 ===")
            filled_fields = sum(1 for v in fields_to_check.values() if v)
            total_fields = len(fields_to_check)
            completeness = (filled_fields / total_fields) * 100
            
            print(f"已填写字段: {filled_fields}/{total_fields}")
            print(f"完整度: {completeness:.1f}%")
            
            if completeness >= 80:
                print("✅ 个人信息展示较为完整")
            elif completeness >= 60:
                print("⚠️ 个人信息展示基本完整，建议补充更多信息")
            else:
                print("❌ 个人信息展示不够完整，需要补充更多信息")
                
        else:
            print(f"❌ API请求失败: {response.text}")
            
    except Exception as e:
        print(f"❌ 请求异常: {str(e)}")

if __name__ == '__main__':
    test_profile_completeness()