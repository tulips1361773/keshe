#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
前端登录功能调试程序
用于分析和修复前端登录测试中的问题
"""

import os
import sys
import django
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import json
from datetime import datetime

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'keshe.settings')
django.setup()

from django.contrib.auth.models import Group
from accounts.models import User, Coach
from campus.models import Campus, CampusCoach

class FrontendLoginDebugger:
    def __init__(self):
        self.frontend_url = "http://localhost:3002"
        self.backend_url = "http://127.0.0.1:8000"
        self.driver = None
        self.wait = None
        self.test_user = None
        
    def setup_test_data(self):
        """创建测试数据"""
        print("=== 创建测试数据 ===")
        
        # 清理旧数据
        timestamp = str(int(time.time()))
        
        # 创建校区
        self.campus = Campus.objects.get_or_create(
            name=f'调试校区_{timestamp}',
            defaults={
                'address': '调试地址123号',
                'phone': '12345678901',
                'description': '用于调试的校区',
                'code': f'DEBUG_{timestamp}'
            }
        )[0]
        
        # 创建教练组
        coach_group, _ = Group.objects.get_or_create(name='教练员')
        
        # 创建测试教练用户
        self.test_user = User.objects.create_user(
            username=f'debug_coach_{timestamp}',
            email=f'debug_{timestamp}@test.com',
            password='testpass123',
            first_name='调试',
            last_name='教练',
            real_name='调试教练',
            phone=f'138{timestamp[-8:]}',
            gender='male',
            user_type='coach',
            is_active=True
        )
        self.test_user.groups.add(coach_group)
        
        # 创建校区关联关系
        CampusCoach.objects.get_or_create(
            campus=self.campus,
            coach=self.test_user
        )
        
        # 创建教练资料
        self.coach_profile = Coach.objects.create(
            user=self.test_user,
            coach_level='senior',
            hourly_rate=200.00,
            achievements='专业网球教练，经验丰富',
            max_students=20,
            status='approved'
        )
        
        print(f"✅ 创建测试用户: {self.test_user.username}")
        print(f"✅ 密码: testpass123")
        
    def setup_driver(self):
        """设置浏览器驱动"""
        print("\n=== 设置浏览器驱动 ===")
        
        chrome_options = Options()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')
        
        try:
            self.driver = webdriver.Chrome(options=chrome_options)
            self.wait = WebDriverWait(self.driver, 10)
            print("✅ 浏览器驱动设置成功")
        except Exception as e:
            print(f"❌ 浏览器驱动设置失败: {e}")
            return False
        return True
        
    def check_services(self):
        """检查前后端服务状态"""
        print("\n=== 检查服务状态 ===")
        
        import requests
        
        # 检查前端服务
        try:
            response = requests.get(self.frontend_url, timeout=5)
            if response.status_code == 200:
                print("✅ 前端服务运行正常")
            else:
                print(f"⚠️ 前端服务响应异常: {response.status_code}")
        except Exception as e:
            print(f"❌ 前端服务连接失败: {e}")
            
        # 检查后端服务
        try:
            response = requests.get(f"{self.backend_url}/api/accounts/csrf-token/", timeout=5)
            if response.status_code == 200:
                print("✅ 后端服务运行正常")
            else:
                print(f"⚠️ 后端服务响应异常: {response.status_code}")
        except Exception as e:
            print(f"❌ 后端服务连接失败: {e}")
            
    def debug_login_page(self):
        """调试登录页面"""
        print("\n=== 调试登录页面 ===")
        
        try:
            # 访问登录页面
            print(f"访问登录页面: {self.frontend_url}/login")
            self.driver.get(f"{self.frontend_url}/login")
            time.sleep(3)
            
            # 保存页面截图
            self.driver.save_screenshot('debug_login_page.png')
            print("📸 登录页面截图已保存: debug_login_page.png")
            
            # 检查页面标题
            page_title = self.driver.title
            print(f"页面标题: {page_title}")
            
            # 检查页面URL
            current_url = self.driver.current_url
            print(f"当前URL: {current_url}")
            
            # 查找所有输入框
            print("\n--- 查找页面元素 ---")
            inputs = self.driver.find_elements(By.TAG_NAME, "input")
            print(f"找到 {len(inputs)} 个输入框:")
            for i, input_elem in enumerate(inputs):
                input_type = input_elem.get_attribute('type')
                placeholder = input_elem.get_attribute('placeholder')
                name = input_elem.get_attribute('name')
                class_name = input_elem.get_attribute('class')
                print(f"  输入框{i+1}: type={input_type}, placeholder={placeholder}, name={name}, class={class_name}")
            
            # 查找所有按钮
            buttons = self.driver.find_elements(By.TAG_NAME, "button")
            print(f"\n找到 {len(buttons)} 个按钮:")
            for i, button in enumerate(buttons):
                button_type = button.get_attribute('type')
                button_text = button.text
                class_name = button.get_attribute('class')
                print(f"  按钮{i+1}: type={button_type}, text={button_text}, class={class_name}")
                
            return True
            
        except Exception as e:
            print(f"❌ 调试登录页面失败: {e}")
            return False
            
    def test_login_process(self):
        """测试登录流程"""
        print("\n=== 测试登录流程 ===")
        
        try:
            # 尝试多种方式定位用户名输入框
            username_input = None
            username_selectors = [
                "input[placeholder*='用户名']",
                "input[placeholder*='账号']", 
                "input[type='text']",
                ".el-input__inner[placeholder*='用户名']",
                "input[name='username']"
            ]
            
            for selector in username_selectors:
                try:
                    username_input = self.wait.until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                    )
                    print(f"✅ 找到用户名输入框: {selector}")
                    break
                except TimeoutException:
                    print(f"⚠️ 未找到用户名输入框: {selector}")
                    continue
                    
            if not username_input:
                print("❌ 无法找到用户名输入框")
                return False
                
            # 尝试多种方式定位密码输入框
            password_input = None
            password_selectors = [
                "input[type='password']",
                "input[placeholder*='密码']",
                ".el-input__inner[type='password']"
            ]
            
            for selector in password_selectors:
                try:
                    password_input = self.driver.find_element(By.CSS_SELECTOR, selector)
                    print(f"✅ 找到密码输入框: {selector}")
                    break
                except NoSuchElementException:
                    print(f"⚠️ 未找到密码输入框: {selector}")
                    continue
                    
            if not password_input:
                print("❌ 无法找到密码输入框")
                return False
                
            # 输入登录信息
            print(f"输入用户名: {self.test_user.username}")
            username_input.clear()
            username_input.send_keys(self.test_user.username)
            
            print("输入密码: testpass123")
            password_input.clear()
            password_input.send_keys('testpass123')
            
            # 保存输入后的截图
            self.driver.save_screenshot('debug_login_input.png')
            print("📸 输入信息后截图已保存: debug_login_input.png")
            
            # 查找登录按钮
            login_button = None
            button_selectors = [
                "button[type='submit']",
                ".el-button--primary",
                "button:contains('登录')",
                ".login-button",
                "button.gradient-button"
            ]
            
            for selector in button_selectors:
                try:
                    if 'contains' in selector:
                        # 使用XPath查找包含文本的按钮
                        login_button = self.driver.find_element(By.XPATH, "//button[contains(text(), '登录')]")
                    else:
                        login_button = self.driver.find_element(By.CSS_SELECTOR, selector)
                    print(f"✅ 找到登录按钮: {selector}")
                    break
                except NoSuchElementException:
                    print(f"⚠️ 未找到登录按钮: {selector}")
                    continue
                    
            if not login_button:
                print("❌ 无法找到登录按钮")
                return False
                
            # 点击登录按钮
            print("点击登录按钮...")
            login_button.click()
            time.sleep(5)
            
            # 保存登录后的截图
            self.driver.save_screenshot('debug_after_login.png')
            print("📸 登录后截图已保存: debug_after_login.png")
            
            # 检查登录结果
            current_url = self.driver.current_url
            print(f"登录后URL: {current_url}")
            
            # 检查是否有错误信息
            try:
                error_elements = self.driver.find_elements(By.CSS_SELECTOR, ".el-message--error, .error-message, .alert-danger")
                if error_elements:
                    for error in error_elements:
                        if error.is_displayed():
                            print(f"❌ 发现错误信息: {error.text}")
            except:
                pass
                
            # 检查是否登录成功
            if '/login' not in current_url:
                print("✅ 登录成功，页面已跳转")
                return True
            else:
                print("❌ 登录失败，仍在登录页面")
                return False
                
        except Exception as e:
            print(f"❌ 登录流程测试失败: {e}")
            return False
            
    def run_debug(self):
        """运行调试程序"""
        print("🔍 前端登录功能调试程序")
        print("=" * 50)
        
        try:
            # 检查服务状态
            self.check_services()
            
            # 创建测试数据
            self.setup_test_data()
            
            # 设置浏览器驱动
            if not self.setup_driver():
                return
                
            # 调试登录页面
            if not self.debug_login_page():
                return
                
            # 测试登录流程
            self.test_login_process()
            
        except Exception as e:
            print(f"❌ 调试程序执行失败: {e}")
        finally:
            if self.driver:
                print("\n🔚 关闭浏览器")
                self.driver.quit()
                
        print("\n🎉 前端登录调试完成！")
        
def main():
    debugger = FrontendLoginDebugger()
    debugger.run_debug()
    
if __name__ == '__main__':
    main()