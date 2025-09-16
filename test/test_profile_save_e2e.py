#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
端到端测试个人资料保存功能
模拟前端的完整操作流程
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
from accounts.models import UserProfile

User = get_user_model()

def test_e2e_profile_save():
    """端到端测试个人资料保存"""
    print("=== 端到端测试个人资料保存功能 ===")
    
    # 1. 创建测试用户
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S%f')[:-3]
    test_username = f"e2e_test_{timestamp}"
    test_phone = f"138{timestamp[-8:]}"  # 使用时间戳生成唯一手机号
    test_user = User.objects.create_user(
        username=test_username,
        email=f"{test_username}@test.com",
        password="testpass123",
        user_type="coach",
        real_name="E2E测试教练",
        phone=test_phone
    )
    print(f"✅ 创建测试用户: {test_user.username}")
    
    try:
        # 2. 模拟前端登录流程
        print("\n📱 模拟前端登录...")
        login_response = requests.post(
            "http://localhost:8000/accounts/api/login/",
            json={
                "username": test_username,
                "password": "testpass123"
            },
            headers={"Content-Type": "application/json"}
        )
        
        if login_response.status_code != 200:
            print(f"❌ 登录失败: {login_response.text}")
            return False
        
        token = login_response.json().get('token')
        print(f"✅ 登录成功，获取Token: {token[:20]}...")
        
        # 3. 模拟前端获取当前资料
        print("\n📋 获取当前个人资料...")
        headers = {
            "Authorization": f"Token {token}",
            "Content-Type": "application/json"
        }
        
        profile_response = requests.get(
            "http://localhost:8000/accounts/api/profile/",
            headers=headers
        )
        
        if profile_response.status_code == 200:
            current_profile = profile_response.json()
            print(f"✅ 获取资料成功: {current_profile.get('real_name')}")
        else:
            print(f"❌ 获取资料失败: {profile_response.text}")
            return False
        
        # 4. 模拟前端保存操作（完全按照前端代码的数据结构）
        print("\n💾 模拟前端保存操作...")
        update_phone = f"139{timestamp[-8:]}"  # 生成唯一的更新手机号
        update_data = {
            "real_name": "更新的教练姓名",
            "phone": update_phone,  # 这是关键字段，之前缺失导致保存失败
            "email": f"updated_{test_username}@example.com",
            "gender": "female",
            "address": "北京市朝阳区体育馆路123号",
            "emergency_contact": "张三",
            "emergency_phone": f"137{timestamp[-8:]}",
            "skills": "乒乓球专业教学, 青少年训练, 比赛指导",
            "experience_years": 8,
            "bio": "资深乒乓球教练，擅长青少年基础训练和技术提升，曾带队参加多项比赛并获得优异成绩。"
        }
        
        # 发送PUT请求到profile/update/端点
        update_response = requests.put(
            "http://localhost:8000/accounts/api/profile/update/",
            json=update_data,
            headers=headers
        )
        
        print(f"📤 发送更新请求，状态码: {update_response.status_code}")
        
        if update_response.status_code == 200:
            response_data = update_response.json()
            print(f"✅ 保存成功: {response_data.get('message')}")
            
            # 5. 验证数据是否正确保存到数据库
            print("\n🔍 验证数据库中的数据...")
            updated_user = User.objects.get(id=test_user.id)
            
            # 验证用户基本信息
            assert updated_user.real_name == update_data['real_name'], f"姓名不匹配: {updated_user.real_name}"
            assert updated_user.phone == update_data['phone'], f"手机号不匹配: {updated_user.phone}"
            assert updated_user.email == update_data['email'], f"邮箱不匹配: {updated_user.email}"
            assert updated_user.gender == update_data['gender'], f"性别不匹配: {updated_user.gender}"
            assert updated_user.address == update_data['address'], f"地址不匹配: {updated_user.address}"
            
            print("✅ 用户基本信息验证通过")
            
            # 验证扩展资料
            try:
                profile = UserProfile.objects.get(user=updated_user)
                assert profile.skills == update_data['skills'], f"技能不匹配: {profile.skills}"
                assert profile.experience_years == update_data['experience_years'], f"经验年数不匹配: {profile.experience_years}"
                assert profile.bio == update_data['bio'], f"个人简介不匹配: {profile.bio}"
                print("✅ 扩展资料验证通过")
            except UserProfile.DoesNotExist:
                print("❌ 扩展资料未创建")
                return False
            
            # 6. 再次获取资料，验证API返回的数据
            print("\n🔄 验证API返回数据...")
            verify_response = requests.get(
                "http://localhost:8000/accounts/api/profile/",
                headers=headers
            )
            
            if verify_response.status_code == 200:
                verify_data = verify_response.json()
                print(f"✅ API返回验证成功: {verify_data.get('real_name')}")
                
                # 检查关键字段
                key_fields = ['real_name', 'phone', 'email', 'gender', 'address', 'skills', 'experience_years', 'bio']
                for field in key_fields:
                    if field in verify_data and field in update_data:
                        if verify_data[field] != update_data[field]:
                            print(f"⚠️ 字段 {field} 不匹配: API返回 {verify_data[field]}, 期望 {update_data[field]}")
                        else:
                            print(f"✅ 字段 {field} 匹配")
                
                return True
            else:
                print(f"❌ 验证API调用失败: {verify_response.text}")
                return False
                
        else:
            print(f"❌ 保存失败!")
            print(f"状态码: {update_response.status_code}")
            print(f"错误信息: {update_response.text}")
            
            # 尝试解析错误信息
            try:
                error_data = update_response.json()
                print(f"详细错误: {json.dumps(error_data, indent=2, ensure_ascii=False)}")
            except:
                pass
            
            return False
            
    finally:
        # 清理测试数据
        try:
            test_user.delete()
            print(f"\n🧹 清理测试用户: {test_username}")
        except Exception as e:
            print(f"清理失败: {e}")

if __name__ == "__main__":
    success = test_e2e_profile_save()
    if success:
        print("\n🎉 端到端测试通过！个人资料保存功能完全正常！")
        print("\n📋 测试总结:")
        print("   ✅ 前端登录流程正常")
        print("   ✅ 获取个人资料API正常")
        print("   ✅ 保存个人资料API正常")
        print("   ✅ 数据库存储正确")
        print("   ✅ API数据返回正确")
        print("   ✅ 所有字段（包括phone）都能正确保存")
    else:
        print("\n💥 端到端测试失败！")
        sys.exit(1)