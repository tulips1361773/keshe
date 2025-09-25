#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
前端登录API调试程序
检查登录API的请求和响应
"""

import os
import sys
import django
import requests
import json
from datetime import datetime

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'keshe.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
django.setup()

from django.contrib.auth.models import Group
from accounts.models import User, Coach
from campus.models import Campus, CampusCoach

class LoginAPIDebugger:
    def __init__(self):
        self.base_url = 'http://localhost:8000'
        self.frontend_url = 'http://localhost:3002'
        self.test_user = None
        self.coach_profile = None
        
    def check_services(self):
        """检查服务状态"""
        print("=== 检查服务状态 ===")
        
        # 检查后端服务
        try:
            response = requests.get(f'{self.base_url}/api/accounts/csrf-token/', timeout=5)
            if response.status_code == 200:
                print("✅ 后端服务运行正常")
            else:
                print(f"❌ 后端服务异常: {response.status_code}")
        except Exception as e:
            print(f"❌ 后端服务连接失败: {e}")
            return False
            
        # 检查前端服务
        try:
            response = requests.get(self.frontend_url, timeout=5)
            if response.status_code == 200:
                print("✅ 前端服务运行正常")
            else:
                print(f"❌ 前端服务异常: {response.status_code}")
        except Exception as e:
            print(f"❌ 前端服务连接失败: {e}")
            return False
            
        return True
    
    def create_test_data(self):
        """创建测试数据"""
        print("=== 创建测试数据 ===")
        
        try:
            # 创建或获取校区
            campus, created = Campus.objects.get_or_create(
                name='测试校区',
                defaults={
                    'code': 'TEST001',
                    'address': '测试地址',
                    'phone': '13800138000',
                    'contact_person': '测试联系人'
                }
            )
            
            # 创建唯一用户名和手机号
            timestamp = str(int(datetime.now().timestamp()))
            username = f'debug_coach_{timestamp}'
            phone = f'138{timestamp[-8:]}'
            
            # 删除可能存在的同名用户
            User.objects.filter(username=username).delete()
            User.objects.filter(phone=phone).delete()
            
            # 创建教练用户
            self.test_user = User.objects.create_user(
                username=username,
                password='testpass123',
                email=f'coach{timestamp}@test.com',
                real_name='测试教练',
                phone=phone,
                user_type='coach'
            )
            
            # 添加到教练组
            coach_group, created = Group.objects.get_or_create(name='教练员')
            self.test_user.groups.add(coach_group)
            
            # 创建教练资料
            self.coach_profile = Coach.objects.create(
                user=self.test_user,
                coach_level='senior',
                hourly_rate=200.00,
                achievements='专业网球教练，经验丰富',
                max_students=20,
                status='approved'
            )
            
            # 创建校区教练关联
            CampusCoach.objects.get_or_create(
                campus=campus,
                coach=self.test_user
            )
            
            print(f"✅ 创建测试用户: {username}")
            print(f"✅ 密码: testpass123")
            
            return True
            
        except Exception as e:
            print(f"❌ 创建测试数据失败: {e}")
            return False
    
    def test_csrf_token(self):
        """测试CSRF令牌获取"""
        print("\n=== 测试CSRF令牌 ===")
        
        try:
            response = requests.get(f'{self.base_url}/api/accounts/csrf-token/')
            print(f"CSRF API状态码: {response.status_code}")
            
            if response.status_code == 200:
                csrf_data = response.json()
                print(f"CSRF响应: {csrf_data}")
                return csrf_data.get('csrfToken')
            else:
                print(f"CSRF获取失败: {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ CSRF令牌获取异常: {e}")
            return None
    
    def test_login_api(self):
        """测试登录API"""
        print("\n=== 测试登录API ===")
        
        # 获取CSRF令牌
        csrf_token = self.test_csrf_token()
        if not csrf_token:
            print("❌ 无法获取CSRF令牌")
            return False
        
        # 准备登录数据
        login_data = {
            'username': self.test_user.username,
            'password': 'testpass123'
        }
        
        headers = {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrf_token,
            'Referer': f'{self.base_url}/'
        }
        
        print(f"登录数据: {login_data}")
        print(f"请求头: {headers}")
        
        try:
            # 发送登录请求
            response = requests.post(
                f'{self.base_url}/api/accounts/login/',
                json=login_data,
                headers=headers
            )
            
            print(f"登录API状态码: {response.status_code}")
            print(f"响应头: {dict(response.headers)}")
            
            if response.status_code == 200:
                login_result = response.json()
                print(f"✅ 登录成功: {login_result}")
                return True
            else:
                print(f"❌ 登录失败: {response.text}")
                try:
                    error_data = response.json()
                    print(f"错误详情: {error_data}")
                except:
                    pass
                return False
                
        except Exception as e:
            print(f"❌ 登录API请求异常: {e}")
            return False
    
    def test_user_info_api(self):
        """测试用户信息API"""
        print("\n=== 测试用户信息API ===")
        
        try:
            response = requests.get(f'{self.base_url}/api/accounts/profile/')
            print(f"用户信息API状态码: {response.status_code}")
            
            if response.status_code == 200:
                user_data = response.json()
                print(f"✅ 用户信息: {user_data}")
            else:
                print(f"❌ 用户信息获取失败: {response.text}")
                
        except Exception as e:
            print(f"❌ 用户信息API异常: {e}")
    
    def cleanup(self):
        """清理测试数据"""
        try:
            if self.test_user:
                # 删除关联的教练资料
                if hasattr(self.test_user, 'coach_profile'):
                    self.test_user.coach_profile.delete()
                
                # 删除校区关联
                CampusCoach.objects.filter(coach=self.test_user).delete()
                
                # 删除用户
                self.test_user.delete()
                print("✅ 清理测试数据完成")
        except Exception as e:
            print(f"❌ 清理测试数据失败: {e}")
    
    def run_debug(self):
        """运行调试"""
        print("🔍 前端登录API调试程序")
        print("=" * 50)
        
        try:
            # 检查服务状态
            if not self.check_services():
                return
            
            # 创建测试数据
            if not self.create_test_data():
                return
            
            # 测试登录API
            self.test_login_api()
            
            # 测试用户信息API
            self.test_user_info_api()
            
        except Exception as e:
            print(f"❌ 调试程序执行失败: {e}")
        finally:
            # 清理测试数据
            self.cleanup()
        
        print("\n🎉 前端登录API调试完成！")

if __name__ == '__main__':
    debugger = LoginAPIDebugger()
    debugger.run_debug()