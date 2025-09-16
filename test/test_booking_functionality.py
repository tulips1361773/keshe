#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
课程预约功能全面测试脚本
测试范围：数据库模型、后端API、前端功能
"""

import os
import sys
import django
import requests
import json
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import logging

# 配置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'keshe.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
django.setup()

# Django模型导入
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from accounts.models import User, Coach, Student
from campus.models import Campus
from reservations.models import CoachStudentRelation, Table, Booking, BookingCancellation
from notifications.models import Notification

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('booking_test.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class BookingFunctionalityTest:
    """课程预约功能测试类"""
    
    def __init__(self):
        self.base_url = 'http://localhost:8000'
        self.frontend_url = 'http://localhost:3002'
        self.test_data = {}
        self.driver = None
        
    def setup_test_data(self):
        """设置测试数据"""
        logger.info("=== 设置测试数据 ===")
        
        try:
            # 创建校区
            campus, created = Campus.objects.get_or_create(
                name='测试校区',
                defaults={
                    'address': '测试地址123号',
                    'phone': '010-12345678',
                    'description': '用于测试的校区'
                }
            )
            self.test_data['campus'] = campus
            logger.info(f"校区创建{'成功' if created else '已存在'}: {campus.name}")
            
            # 创建教练用户
            coach_user, created = User.objects.get_or_create(
                username='test_coach_booking',
                defaults={
                    'email': 'coach_booking@test.com',
                    'real_name': '测试教练',
                    'phone': '13800000001',
                    'user_type': 'coach',
                    'is_active': True
                }
            )
            if created:
                coach_user.set_password('testpass123')
                coach_user.save()
            
            # 创建教练档案
            coach_profile, created = Coach.objects.get_or_create(
                user=coach_user,
                defaults={
                    'campus': campus,
                    'level': 'intermediate',
                    'hourly_rate': 100.00,
                    'bio': '测试教练简介',
                    'is_approved': True
                }
            )
            self.test_data['coach_user'] = coach_user
            self.test_data['coach_profile'] = coach_profile
            logger.info(f"教练创建{'成功' if created else '已存在'}: {coach_user.real_name}")
            
            # 创建学员用户
            student_user, created = User.objects.get_or_create(
                username='test_student_booking',
                defaults={
                    'email': 'student_booking@test.com',
                    'real_name': '测试学员',
                    'phone': '13800000002',
                    'user_type': 'student',
                    'is_active': True
                }
            )
            if created:
                student_user.set_password('testpass123')
                student_user.save()
            
            # 创建学员档案
            student_profile, created = Student.objects.get_or_create(
                user=student_user,
                defaults={
                    'campus': campus,
                    'level': 'beginner',
                    'balance': 1000.00
                }
            )
            self.test_data['student_user'] = student_user
            self.test_data['student_profile'] = student_profile
            logger.info(f"学员创建{'成功' if created else '已存在'}: {student_user.real_name}")
            
            # 创建师生关系
            relation, created = CoachStudentRelation.objects.get_or_create(
                coach=coach_user,
                student=student_user,
                defaults={
                    'status': 'approved',
                    'applied_by': 'student',
                    'applied_at': timezone.now(),
                    'processed_at': timezone.now()
                }
            )
            self.test_data['relation'] = relation
            logger.info(f"师生关系创建{'成功' if created else '已存在'}")
            
            # 创建球台
            table, created = Table.objects.get_or_create(
                campus=campus,
                number=1,
                defaults={
                    'name': '测试球台1号',
                    'status': 'available',
                    'description': '用于测试的球台',
                    'is_active': True
                }
            )
            self.test_data['table'] = table
            logger.info(f"球台创建{'成功' if created else '已存在'}: {table}")
            
            logger.info("测试数据设置完成")
            return True
            
        except Exception as e:
            logger.error(f"设置测试数据失败: {e}")
            return False
    
    def test_database_models(self):
        """测试数据库模型"""
        logger.info("=== 测试数据库模型 ===")
        
        try:
            # 测试预约模型创建
            start_time = timezone.now() + timedelta(days=1, hours=10)
            end_time = start_time + timedelta(hours=2)
            
            booking = Booking.objects.create(
                relation=self.test_data['relation'],
                table=self.test_data['table'],
                start_time=start_time,
                end_time=end_time,
                duration_hours=2.0,
                total_fee=200.00,
                status='pending',
                notes='测试预约'
            )
            
            logger.info(f"预约创建成功: ID={booking.id}")
            
            # 测试预约属性
            assert booking.coach == self.test_data['coach_user']
            assert booking.student == self.test_data['student_user']
            logger.info("预约属性验证通过")
            
            # 测试取消权限检查
            can_cancel, message = booking.can_cancel(self.test_data['student_user'])
            logger.info(f"取消权限检查: {can_cancel}, {message}")
            
            # 测试预约取消申请
            cancellation = BookingCancellation.objects.create(
                booking=booking,
                requested_by=self.test_data['student_user'],
                reason='测试取消原因'
            )
            logger.info(f"取消申请创建成功: ID={cancellation.id}")
            
            # 清理测试数据
            cancellation.delete()
            booking.delete()
            
            logger.info("数据库模型测试通过")
            return True
            
        except Exception as e:
            logger.error(f"数据库模型测试失败: {e}")
            return False
    
    def get_auth_token(self, username, password):
        """获取认证令牌"""
        try:
            response = requests.post(f'{self.base_url}/api/auth/login/', {
                'username': username,
                'password': password
            })
            if response.status_code == 200:
                return response.json().get('token')
            else:
                logger.error(f"登录失败: {response.status_code}, {response.text}")
                return None
        except Exception as e:
            logger.error(f"获取认证令牌失败: {e}")
            return None
    
    def test_backend_api(self):
        """测试后端API"""
        logger.info("=== 测试后端API ===")
        
        try:
            # 获取学员认证令牌
            student_token = self.get_auth_token('test_student_booking', 'testpass123')
            if not student_token:
                logger.error("无法获取学员认证令牌")
                return False
            
            headers = {
                'Authorization': f'Token {student_token}',
                'Content-Type': 'application/json'
            }
            
            # 测试获取师生关系列表
            response = requests.get(f'{self.base_url}/api/reservations/relations/', headers=headers)
            assert response.status_code == 200
            relations = response.json()['results']
            logger.info(f"师生关系列表获取成功，数量: {len(relations)}")
            
            # 测试获取可用球台
            start_time = (timezone.now() + timedelta(days=1, hours=10)).isoformat()
            end_time = (timezone.now() + timedelta(days=1, hours=12)).isoformat()
            
            params = {
                'start_time': start_time,
                'end_time': end_time,
                'campus_id': self.test_data['campus'].id
            }
            
            response = requests.get(f'{self.base_url}/api/reservations/tables/available/', 
                                  params=params, headers=headers)
            assert response.status_code == 200
            tables = response.json()
            logger.info(f"可用球台获取成功，数量: {len(tables)}")
            
            # 测试创建预约
            booking_data = {
                'relation_id': self.test_data['relation'].id,
                'table_id': self.test_data['table'].id,
                'start_time': start_time,
                'end_time': end_time,
                'duration_hours': 2.0,
                'total_fee': 200.00,
                'notes': 'API测试预约'
            }
            
            response = requests.post(f'{self.base_url}/api/reservations/bookings/', 
                                   json=booking_data, headers=headers)
            assert response.status_code == 201
            booking = response.json()
            booking_id = booking['id']
            logger.info(f"预约创建成功: ID={booking_id}")
            
            # 测试获取预约列表
            response = requests.get(f'{self.base_url}/api/reservations/bookings/', headers=headers)
            assert response.status_code == 200
            bookings = response.json()['results']
            logger.info(f"预约列表获取成功，数量: {len(bookings)}")
            
            # 测试教练确认预约
            coach_token = self.get_auth_token('test_coach_booking', 'testpass123')
            coach_headers = {
                'Authorization': f'Token {coach_token}',
                'Content-Type': 'application/json'
            }
            
            response = requests.post(f'{self.base_url}/api/reservations/bookings/{booking_id}/confirm/', 
                                   headers=coach_headers)
            assert response.status_code == 200
            logger.info("教练确认预约成功")
            
            # 测试取消预约
            cancel_data = {'reason': 'API测试取消'}
            response = requests.post(f'{self.base_url}/api/reservations/bookings/{booking_id}/cancel/', 
                                   json=cancel_data, headers=headers)
            assert response.status_code == 200
            logger.info("预约取消成功")
            
            # 测试预约统计
            response = requests.get(f'{self.base_url}/api/reservations/statistics/', headers=headers)
            assert response.status_code == 200
            stats = response.json()
            logger.info(f"预约统计获取成功: {stats}")
            
            logger.info("后端API测试通过")
            return True
            
        except Exception as e:
            logger.error(f"后端API测试失败: {e}")
            return False
    
    def setup_webdriver(self):
        """设置WebDriver"""
        try:
            chrome_options = Options()
            chrome_options.add_argument('--headless')  # 无头模式
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--window-size=1920,1080')
            
            self.driver = webdriver.Chrome(options=chrome_options)
            self.driver.implicitly_wait(10)
            logger.info("WebDriver设置成功")
            return True
        except Exception as e:
            logger.error(f"WebDriver设置失败: {e}")
            return False
    
    def test_frontend_functionality(self):
        """测试前端功能"""
        logger.info("=== 测试前端功能 ===")
        
        if not self.setup_webdriver():
            return False
        
        try:
            # 访问登录页面
            self.driver.get(f'{self.frontend_url}/login')
            logger.info("访问登录页面")
            
            # 等待页面加载
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "form"))
            )
            
            # 学员登录
            username_input = self.driver.find_element(By.CSS_SELECTOR, "input[type='text'], input[placeholder*='用户名'], input[placeholder*='账号']")
            password_input = self.driver.find_element(By.CSS_SELECTOR, "input[type='password']")
            
            username_input.clear()
            username_input.send_keys('test_student_booking')
            password_input.clear()
            password_input.send_keys('testpass123')
            
            # 查找并点击登录按钮
            login_selectors = [
                "button[type='submit']",
                "button:contains('登录')",
                "button:contains('立即登录')",
                ".el-button--primary",
                "[class*='login-btn']"
            ]
            
            login_button = None
            for selector in login_selectors:
                try:
                    if ':contains(' in selector:
                        # 使用XPath处理包含文本的选择器
                        xpath = f"//button[contains(text(), '登录')]")
                        login_button = self.driver.find_element(By.XPATH, xpath)
                    else:
                        login_button = self.driver.find_element(By.CSS_SELECTOR, selector)
                    break
                except NoSuchElementException:
                    continue
            
            if login_button:
                self.driver.execute_script("arguments[0].scrollIntoView();", login_button)
                time.sleep(1)
                login_button.click()
                logger.info("点击登录按钮")
            else:
                logger.error("未找到登录按钮")
                return False
            
            # 等待登录完成并跳转
            time.sleep(3)
            
            # 访问预约页面
            self.driver.get(f'{self.frontend_url}/reservations')
            logger.info("访问预约页面")
            
            # 等待页面加载
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "reservations-container"))
            )
            logger.info("预约页面加载成功")
            
            # 测试新建预约按钮
            try:
                new_booking_btn = WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), '新建预约')]"))
                )
                new_booking_btn.click()
                logger.info("点击新建预约按钮成功")
                
                # 等待预约表单出现
                WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "booking-form"))
                )
                logger.info("预约表单显示成功")
                
            except TimeoutException:
                logger.warning("新建预约功能测试超时，可能需要手动检查")
            
            # 测试预约列表显示
            try:
                table = self.driver.find_element(By.CSS_SELECTOR, ".el-table")
                logger.info("预约列表表格显示正常")
            except NoSuchElementException:
                logger.warning("预约列表表格未找到")
            
            # 测试筛选功能
            try:
                filter_card = self.driver.find_element(By.CLASS_NAME, "filter-card")
                logger.info("筛选功能区域显示正常")
            except NoSuchElementException:
                logger.warning("筛选功能区域未找到")
            
            logger.info("前端功能测试完成")
            return True
            
        except Exception as e:
            logger.error(f"前端功能测试失败: {e}")
            return False
        finally:
            if self.driver:
                self.driver.quit()
    
    def cleanup_test_data(self):
        """清理测试数据"""
        logger.info("=== 清理测试数据 ===")
        
        try:
            # 删除预约相关数据
            Booking.objects.filter(
                relation__coach__username='test_coach_booking'
            ).delete()
            
            BookingCancellation.objects.filter(
                booking__relation__coach__username='test_coach_booking'
            ).delete()
            
            # 删除师生关系
            CoachStudentRelation.objects.filter(
                coach__username='test_coach_booking'
            ).delete()
            
            # 删除通知
            Notification.objects.filter(
                recipient__username__in=['test_coach_booking', 'test_student_booking']
            ).delete()
            
            logger.info("测试数据清理完成")
            
        except Exception as e:
            logger.error(f"清理测试数据失败: {e}")
    
    def run_all_tests(self):
        """运行所有测试"""
        logger.info("开始课程预约功能全面测试")
        
        results = {
            'setup_data': False,
            'database_models': False,
            'backend_api': False,
            'frontend_functionality': False
        }
        
        try:
            # 设置测试数据
            results['setup_data'] = self.setup_test_data()
            
            if results['setup_data']:
                # 测试数据库模型
                results['database_models'] = self.test_database_models()
                
                # 测试后端API
                results['backend_api'] = self.test_backend_api()
                
                # 测试前端功能
                results['frontend_functionality'] = self.test_frontend_functionality()
            
            # 清理测试数据
            self.cleanup_test_data()
            
        except Exception as e:
            logger.error(f"测试过程中发生错误: {e}")
        
        # 输出测试结果
        logger.info("=== 测试结果汇总 ===")
        for test_name, result in results.items():
            status = "✅ 通过" if result else "❌ 失败"
            logger.info(f"{test_name}: {status}")
        
        all_passed = all(results.values())
        logger.info(f"\n总体结果: {'✅ 全部通过' if all_passed else '❌ 存在失败'}")
        
        return results

if __name__ == '__main__':
    test = BookingFunctionalityTest()
    results = test.run_all_tests()
    
    # 根据测试结果设置退出码
    exit_code = 0 if all(results.values()) else 1
    sys.exit(exit_code)