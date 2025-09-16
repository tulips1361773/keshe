#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
修复后的前端登录功能调试程序
基于API调试结果修复前端登录测试
"""

import os
import sys
import django
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'keshe.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
django.setup()

from django.contrib.auth.models import Group
from accounts.models import User, Coach
from campus.models import Campus, CampusCoach
import requests

class FixedFrontendLoginDebugger:
    def __init__(self):
        self.base_url = 'http://localhost:8000'
        self.frontend_url = 'http://localhost:3002'
        self.driver = None
        self.test_user = None
        self.coach_profile = None
        
    def check_services(self):
        """检查服务状态"""
        print("=== 检查服务状态 ===")
        
        # 检查前端服务
        try:
            response = requests.get(self.frontend_url, timeout=5)
            if response.status_code == 200:
                print("✅ 前端服务运行正常")
            else:
                print(f"❌ 前端服务异常: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ 前端服务连接失败: {e}")
            return False
            
        # 检查后端服务
        try:
            response = requests.get(f'{self.base_url}/api/accounts/csrf-token/', timeout=5)
            if response.status_code == 200:
                print("✅ 后端服务运行正常")
            else:
                print(f"❌ 后端服务异常: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ 后端服务连接失败: {e}")
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
    
    def setup_driver(self):
        """设置浏览器驱动"""
        print("\n=== 设置浏览器驱动 ===")
        
        try:
            chrome_options = Options()
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--window-size=1920,1080')
            
            self.driver = webdriver.Chrome(options=chrome_options)
            self.driver.implicitly_wait(10)
            
            print("✅ 浏览器驱动设置成功")
            return True
            
        except Exception as e:
            print(f"❌ 浏览器驱动设置失败: {e}")
            return False
    
    def debug_login_page(self):
        """调试登录页面"""
        print("\n=== 调试登录页面 ===")
        
        try:
            # 访问登录页面
            login_url = f'{self.frontend_url}/login'
            print(f"访问登录页面: {login_url}")
            self.driver.get(login_url)
            
            # 等待页面加载
            time.sleep(3)
            
            # 截图
            self.driver.save_screenshot('debug_login_page_fixed.png')
            print("📸 登录页面截图已保存: debug_login_page_fixed.png")
            
            # 获取页面信息
            print(f"页面标题: {self.driver.title}")
            print(f"当前URL: {self.driver.current_url}")
            
            # 等待登录表单加载
            wait = WebDriverWait(self.driver, 10)
            
            # 查找用户名输入框 - 尝试多种选择器
            username_selectors = [
                "input[placeholder*='用户名']",
                "input[placeholder*='username']",
                "input[type='text']",
                ".el-input__inner[placeholder*='用户名']",
                "#username",
                "[name='username']"
            ]
            
            username_input = None
            for selector in username_selectors:
                try:
                    username_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
                    print(f"✅ 找到用户名输入框: {selector}")
                    break
                except TimeoutException:
                    continue
            
            if not username_input:
                print("❌ 未找到用户名输入框")
                return False
            
            # 查找密码输入框
            password_selectors = [
                "input[type='password']",
                "input[placeholder*='密码']",
                "input[placeholder*='password']",
                ".el-input__inner[type='password']",
                "#password",
                "[name='password']"
            ]
            
            password_input = None
            for selector in password_selectors:
                try:
                    password_input = self.driver.find_element(By.CSS_SELECTOR, selector)
                    print(f"✅ 找到密码输入框: {selector}")
                    break
                except NoSuchElementException:
                    continue
            
            if not password_input:
                print("❌ 未找到密码输入框")
                return False
            
            # 查找登录按钮
            login_button_selectors = [
                "button[type='submit']",
                "button:contains('登录')",
                "button:contains('立即登录')",
                ".login-button",
                ".el-button--primary",
                "[type='submit']"
            ]
            
            login_button = None
            for selector in login_button_selectors:
                try:
                    if ':contains(' in selector:
                        # 使用XPath处理包含文本的选择器
                        xpath = f"//button[contains(text(), '登录')]"
                        login_button = self.driver.find_element(By.XPATH, xpath)
                    else:
                        login_button = self.driver.find_element(By.CSS_SELECTOR, selector)
                    print(f"✅ 找到登录按钮: {selector}")
                    break
                except NoSuchElementException:
                    continue
            
            if not login_button:
                print("❌ 未找到登录按钮")
                return False
            
            return True
            
        except Exception as e:
            print(f"❌ 调试登录页面失败: {e}")
            return False
    
    def test_login_flow(self):
        """测试登录流程"""
        print("\n=== 测试登录流程 ===")
        
        try:
            # 清空输入框并输入用户名
            username_input = self.driver.find_element(By.CSS_SELECTOR, "input[placeholder*='用户名'], input[type='text']")
            username_input.clear()
            username_input.send_keys(self.test_user.username)
            print(f"输入用户名: {self.test_user.username}")
            
            # 清空输入框并输入密码
            password_input = self.driver.find_element(By.CSS_SELECTOR, "input[type='password']")
            password_input.clear()
            password_input.send_keys('testpass123')
            print("输入密码: testpass123")
            
            # 等待一下确保输入完成
            time.sleep(1)
            
            # 点击登录按钮 - 使用更精确的选择器
            login_button_selectors = [
                "button.login-button",
                "button[native-type='submit']",
                "button.el-button--primary",
                "//button[contains(text(), '立即登录')]",
                "//button[contains(text(), '登录中')]"
            ]
            
            login_button = None
            for selector in login_button_selectors:
                try:
                    if selector.startswith('//'):
                        login_button = self.driver.find_element(By.XPATH, selector)
                    else:
                        login_button = self.driver.find_element(By.CSS_SELECTOR, selector)
                    print(f"✅ 找到登录按钮: {selector}")
                    break
                except NoSuchElementException:
                    continue
            
            if not login_button:
                print("❌ 未找到登录按钮")
                return False
            
            # 确保按钮可点击
            self.driver.execute_script("arguments[0].scrollIntoView(true);", login_button)
            time.sleep(0.5)
            
            # 点击登录按钮
            login_button.click()
            print("点击登录按钮...")
            
            # 等待登录处理
            time.sleep(5)
            
            # 截图
            self.driver.save_screenshot('debug_after_login_fixed.png')
            print("📸 登录后截图已保存: debug_after_login_fixed.png")
            
            # 检查登录结果
            current_url = self.driver.current_url
            print(f"登录后URL: {current_url}")
            
            # 检查是否跳转到其他页面（不再是登录页面）
            if '/login' not in current_url:
                print("✅ 登录成功，已跳转到其他页面")
                return True
            else:
                # 检查是否有错误消息
                try:
                    error_elements = self.driver.find_elements(By.CSS_SELECTOR, ".el-message--error, .error-message, .alert-danger")
                    if error_elements:
                        for error in error_elements:
                            if error.is_displayed():
                                print(f"❌ 登录错误信息: {error.text}")
                    else:
                        print("❌ 登录失败，仍在登录页面，但未找到错误信息")
                except:
                    print("❌ 登录失败，仍在登录页面")
                return False
                
        except Exception as e:
            print(f"❌ 登录流程测试失败: {e}")
            return False
    
    def cleanup(self):
        """清理资源"""
        try:
            if self.driver:
                self.driver.quit()
                print("🔚 关闭浏览器")
        except:
            pass
        
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
        print("🔍 修复后的前端登录功能调试程序")
        print("=" * 50)
        
        try:
            # 检查服务状态
            if not self.check_services():
                return
            
            # 创建测试数据
            if not self.create_test_data():
                return
            
            # 设置浏览器驱动
            if not self.setup_driver():
                return
            
            # 调试登录页面
            if not self.debug_login_page():
                return
            
            # 测试登录流程
            login_success = self.test_login_flow()
            
            if login_success:
                print("\n🎉 前端登录功能测试通过！")
            else:
                print("\n❌ 前端登录功能仍有问题，需要进一步调试")
            
        except Exception as e:
            print(f"❌ 调试程序执行失败: {e}")
        finally:
            # 清理资源
            self.cleanup()
        
        print("\n🎉 修复后的前端登录调试完成！")

if __name__ == '__main__':
    debugger = FixedFrontendLoginDebugger()
    debugger.run_debug()