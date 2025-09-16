#!/usr/bin/env python
"""
最终通知系统测试
验证教练能否实时看到学员申请通知
"""

import os
import sys
import django
import time
import requests
from datetime import datetime

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'keshe.settings')
django.setup()

from django.contrib.auth.models import Group
from accounts.models import User
from accounts.models import Coach
from campus.models import Campus, CampusCoach
from reservations.models import CoachStudentRelation
from notifications.models import Notification

class FinalNotificationTest:
    def __init__(self):
        self.base_url = 'http://127.0.0.1:8000'
        self.frontend_url = 'http://localhost:3002'
        
    def cleanup_test_data(self):
        """清理测试数据"""
        print("=== 清理测试数据 ===")
        
        # 删除测试用户
        test_users = User.objects.filter(username__startswith='final_test_')
        for user in test_users:
            print(f"删除测试用户: {user.username}")
            user.delete()
            
        # 删除测试通知
        test_notifications = Notification.objects.filter(
            title__contains='最终测试'
        )
        for notification in test_notifications:
            notification.delete()
            
        print("✅ 测试数据清理完成")
        
    def create_test_users(self):
        """创建测试用户"""
        print("\n=== 创建测试用户 ===")
        
        timestamp = str(int(time.time()))
        
        # 创建教练组
        coach_group, _ = Group.objects.get_or_create(name='教练员')
        
        # 创建测试教练
        self.coach_user = User.objects.create_user(
            username=f'final_test_coach_{timestamp}',
            email=f'coach_{timestamp}@test.com',
            password='testpass123',
            real_name='最终测试教练',
            phone=f'138{timestamp[-8:]}',
            user_type='coach'
        )
        self.coach_user.groups.add(coach_group)
        
        # 创建教练资料
        self.coach_profile = Coach.objects.create(
            user=self.coach_user,
            coach_level='senior',
            hourly_rate=200.00,
            status='approved'
        )
        
        print(f"✅ 教练档案创建成功，Coach ID: {self.coach_profile.id}, User ID: {self.coach_user.id}")
        
        # 创建测试学员
        self.student_user = User.objects.create_user(
            username=f'final_test_student_{timestamp}',
            email=f'student_{timestamp}@test.com',
            password='testpass123',
            real_name='最终测试学员',
            phone=f'139{timestamp[-8:]}',
            user_type='student'
        )
        
        print(f"✅ 创建教练: {self.coach_user.username}")
        print(f"✅ 创建学员: {self.student_user.username}")
        
    def get_auth_token(self, username, password):
        """获取认证token"""
        response = requests.post(f'{self.base_url}/api/accounts/login/', {
            'username': username,
            'password': password
        })
        
        if response.status_code == 200:
            return response.json().get('token')
        else:
            print(f"登录失败: {response.text}")
            return None
            
    def test_student_application(self):
        """测试学员申请流程"""
        print("\n=== 测试学员申请流程 ===")
        
        # 学员登录
        student_token = self.get_auth_token(
            self.student_user.username, 'testpass123'
        )
        
        if not student_token:
            print("❌ 学员登录失败")
            return False
            
        # 学员申请选择教练
        headers = {'Authorization': f'Token {student_token}'}
        application_data = {
            'coach_id': self.coach_profile.id,
            'student_name': self.student_user.real_name,
            'student_phone': self.student_user.phone,
            'student_email': self.student_user.email,
            'preferred_time': '周末上午',
            'learning_goals': '提高驾驶技能',
            'reason': '最终测试 - 申请选择教练'
        }
        response = requests.post(
            f'{self.base_url}/api/reservations/relations/',
            application_data,
            headers=headers
        )
        
        if response.status_code == 201:
            self.relation_id = response.json().get('id')
            print(f"✅ 学员申请成功，关系ID: {self.relation_id}")
            return True
        else:
            print(f"❌ 学员申请失败: {response.text}")
            return False
            
    def test_coach_notifications(self):
        """测试教练通知接收"""
        print("\n=== 测试教练通知接收 ===")
        
        # 教练登录
        coach_token = self.get_auth_token(
            self.coach_user.username, 'testpass123'
        )
        
        if not coach_token:
            print("❌ 教练登录失败")
            return False
            
        headers = {'Authorization': f'Token {coach_token}'}
        
        # 检查通知列表
        response = requests.get(
            f'{self.base_url}/api/notifications/list/',
            headers=headers
        )
        
        if response.status_code == 200:
            notifications = response.json().get('results', [])
            print(f"✅ 教练收到通知数量: {len(notifications)}")
            
            # 查找相关通知
            relation_notifications = [
                n for n in notifications 
                if 'relation_request' in str(n.get('data', {}))
            ]
            
            if relation_notifications:
                print("✅ 找到师生关系申请通知")
                for notification in relation_notifications:
                    print(f"  - {notification['title']}: {notification.get('message', notification.get('content', '无内容'))}")
                return True
            else:
                print("❌ 未找到师生关系申请通知")
                return False
        else:
            print(f"❌ 获取通知失败: {response.text}")
            return False
            
    def test_notification_stats(self):
        """测试通知统计"""
        print("\n=== 测试通知统计 ===")
        
        coach_token = self.get_auth_token(
            self.coach_user.username, 'testpass123'
        )
        
        headers = {'Authorization': f'Token {coach_token}'}
        
        # 检查统计数据
        response = requests.get(
            f'{self.base_url}/api/notifications/stats/',
            headers=headers
        )
        
        if response.status_code == 200:
            stats = response.json()
            print(f"✅ 通知统计:")
            print(f"  - 总通知数: {stats.get('total', 0)}")
            print(f"  - 未读通知数: {stats.get('unread', 0)}")
            print(f"  - 系统通知数: {stats.get('system', 0)}")
            return True
        else:
            print(f"❌ 获取统计失败: {response.text}")
            return False
            
    def test_unread_count(self):
        """测试未读通知数量"""
        print("\n=== 测试未读通知数量 ===")
        
        coach_token = self.get_auth_token(
            self.coach_user.username, 'testpass123'
        )
        
        headers = {'Authorization': f'Token {coach_token}'}
        
        # 检查未读数量
        response = requests.get(
            f'{self.base_url}/api/notifications/unread-count/',
            headers=headers
        )
        
        if response.status_code == 200:
            data = response.json()
            unread_count = data.get('count', 0)
            print(f"✅ 未读通知数量: {unread_count}")
            return unread_count > 0
        else:
            print(f"❌ 获取未读数量失败: {response.text}")
            return False
            
    def check_frontend_accessibility(self):
        """检查前端页面可访问性"""
        print("\n=== 检查前端页面可访问性 ===")
        
        try:
            response = requests.get(self.frontend_url, timeout=5)
            if response.status_code == 200:
                print(f"✅ 前端页面可访问: {self.frontend_url}")
                return True
            else:
                print(f"❌ 前端页面状态码: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ 前端页面连接失败: {e}")
            print("ℹ️  前端服务可能未启动或端口不正确")
            return False
            
    def run_complete_test(self):
        """运行完整测试"""
        print("🚀 开始最终通知系统测试")
        print(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        try:
            # 清理旧数据
            self.cleanup_test_data()
            
            # 创建测试用户
            self.create_test_users()
            
            # 测试学员申请
            if not self.test_student_application():
                print("❌ 学员申请测试失败")
                return False
                
            # 等待通知处理
            print("⏳ 等待通知处理...")
            time.sleep(2)
            
            # 测试教练通知接收
            if not self.test_coach_notifications():
                print("❌ 教练通知接收测试失败")
                return False
                
            # 测试通知统计
            if not self.test_notification_stats():
                print("❌ 通知统计测试失败")
                return False
                
            # 测试未读数量
            if not self.test_unread_count():
                print("❌ 未读数量测试失败")
                return False
                
            # 检查前端可访问性
            if not self.check_frontend_accessibility():
                print("❌ 前端可访问性测试失败")
                return False
                
            print("\n🎉 最终通知系统测试全部通过！")
            print("\n=== 测试结果总结 ===")
            print("✅ 学员申请功能正常")
            print("✅ 教练通知接收正常")
            print("✅ 通知统计功能正常")
            print("✅ 未读数量统计正常")
            print("✅ 前端页面可访问")
            print("\n📋 修复内容:")
            print("1. 添加了Dashboard页面定时刷新机制（每30秒）")
            print("2. 添加了手动刷新按钮")
            print("3. 修复了用户认证状态初始化问题")
            print("4. 确保了路由认证守卫正常工作")
            print("\n🔧 建议:")
            print("- 教练登录后会自动每30秒刷新通知")
            print("- 可以点击刷新按钮立即更新通知")
            print("- 页面刷新后认证状态会自动恢复")
            
            return True
            
        except Exception as e:
            print(f"❌ 测试过程中发生错误: {e}")
            import traceback
            traceback.print_exc()
            return False
        finally:
            # 清理测试数据
            self.cleanup_test_data()

if __name__ == '__main__':
    tester = FinalNotificationTest()
    success = tester.run_complete_test()
    sys.exit(0 if success else 1)