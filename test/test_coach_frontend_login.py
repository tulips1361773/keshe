#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试教练前端登录和通知显示
使用Selenium模拟教练登录前端查看通知
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

# 设置Django环境
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'keshe.settings')
django.setup()

from accounts.models import User, Coach
from notifications.models import Notification

class CoachFrontendLoginTest:
    def __init__(self):
        self.frontend_url = 'http://localhost:3002'
        self.driver = None
        self.wait = None
        
    def setup_driver(self):
        """设置浏览器驱动"""
        print("=== 设置浏览器驱动 ===")
        
        try:
            chrome_options = Options()
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--window-size=1920,1080')
            # chrome_options.add_argument('--headless')  # 注释掉以便观察
            
            self.driver = webdriver.Chrome(options=chrome_options)
            self.wait = WebDriverWait(self.driver, 10)
            
            print("✓ 浏览器驱动设置成功")
            return True
            
        except Exception as e:
            print(f"❌ 浏览器驱动设置失败: {e}")
            return False
    
    def get_coach_info(self):
        """获取教练信息"""
        print("\n=== 获取教练信息 ===")
        
        try:
            coach_obj = Coach.objects.first()
            if not coach_obj:
                print("❌ 未找到教练用户")
                return None
                
            coach_user = coach_obj.user
            print(f"✓ 找到教练: {coach_user.username} (ID: {coach_user.id})")
            
            # 检查通知
            notifications = Notification.objects.filter(recipient=coach_user)
            print(f"✓ 教练通知数量: {notifications.count()}")
            
            return {
                'username': coach_user.username,
                'user_id': coach_user.id,
                'notification_count': notifications.count()
            }
            
        except Exception as e:
            print(f"❌ 获取教练信息失败: {e}")
            return None
    
    def test_frontend_login(self, coach_info):
        """测试前端登录"""
        print("\n=== 测试前端登录 ===")
        
        try:
            # 访问登录页面
            self.driver.get(f"{self.frontend_url}/login")
            print(f"访问登录页面: {self.frontend_url}/login")
            
            # 等待页面加载
            time.sleep(3)
            
            # 截图
            self.driver.save_screenshot('coach_login_page.png')
            print("📸 登录页面截图: coach_login_page.png")
            
            # 查找用户名输入框
            username_selectors = [
                "input[placeholder*='用户名']",
                "input[placeholder*='账号']",
                "input[type='text']",
                ".el-input__inner[type='text']"
            ]
            
            username_input = None
            for selector in username_selectors:
                try:
                    username_input = self.driver.find_element(By.CSS_SELECTOR, selector)
                    print(f"✓ 找到用户名输入框: {selector}")
                    break
                except NoSuchElementException:
                    continue
            
            if not username_input:
                print("❌ 未找到用户名输入框")
                return False
            
            # 查找密码输入框
            password_input = self.driver.find_element(By.CSS_SELECTOR, "input[type='password']")
            print("✓ 找到密码输入框")
            
            # 输入登录信息
            username_input.clear()
            username_input.send_keys(coach_info['username'])
            print(f"✓ 输入用户名: {coach_info['username']}")
            
            password_input.clear()
            password_input.send_keys('testpass123')
            print("✓ 输入密码")
            
            # 查找登录按钮
            login_selectors = [
                "button[type='submit']",
                ".el-button--primary",
                "button:contains('登录')",
                ".login-btn"
            ]
            
            login_button = None
            for selector in login_selectors:
                try:
                    login_button = self.driver.find_element(By.CSS_SELECTOR, selector)
                    print(f"✓ 找到登录按钮: {selector}")
                    break
                except NoSuchElementException:
                    continue
            
            if not login_button:
                print("❌ 未找到登录按钮")
                return False
            
            # 点击登录
            login_button.click()
            print("✓ 点击登录按钮")
            
            # 等待登录处理
            time.sleep(5)
            
            # 检查登录结果
            current_url = self.driver.current_url
            print(f"登录后URL: {current_url}")
            
            if '/login' not in current_url:
                print("✅ 登录成功")
                return True
            else:
                print("❌ 登录失败，仍在登录页面")
                # 检查错误信息
                try:
                    error_elements = self.driver.find_elements(By.CSS_SELECTOR, ".el-message--error, .error-message")
                    for error in error_elements:
                        if error.is_displayed():
                            print(f"错误信息: {error.text}")
                except:
                    pass
                return False
                
        except Exception as e:
            print(f"❌ 前端登录测试失败: {e}")
            return False
    
    def test_notifications_page(self):
        """测试通知页面"""
        print("\n=== 测试通知页面 ===")
        
        try:
            # 访问通知页面
            self.driver.get(f"{self.frontend_url}/notifications")
            print(f"访问通知页面: {self.frontend_url}/notifications")
            
            # 等待页面加载
            time.sleep(5)
            
            # 截图
            self.driver.save_screenshot('coach_notifications_page.png')
            print("📸 通知页面截图: coach_notifications_page.png")
            
            # 检查页面标题
            try:
                title_element = self.driver.find_element(By.CSS_SELECTOR, "h1, .header h1")
                print(f"✓ 页面标题: {title_element.text}")
            except:
                print("⚠️ 未找到页面标题")
            
            # 检查统计信息
            try:
                stat_cards = self.driver.find_elements(By.CSS_SELECTOR, ".stat-card, .el-card")
                print(f"✓ 找到统计卡片数量: {len(stat_cards)}")
                
                for i, card in enumerate(stat_cards[:4]):
                    try:
                        number = card.find_element(By.CSS_SELECTOR, ".stat-number")
                        label = card.find_element(By.CSS_SELECTOR, ".stat-label")
                        print(f"  统计{i+1}: {label.text} = {number.text}")
                    except:
                        print(f"  统计{i+1}: 无法读取")
                        
            except Exception as e:
                print(f"⚠️ 统计信息检查失败: {e}")
            
            # 检查通知列表
            try:
                notification_items = self.driver.find_elements(By.CSS_SELECTOR, ".notification-item")
                print(f"✓ 找到通知项数量: {len(notification_items)}")
                
                if len(notification_items) > 0:
                    for i, item in enumerate(notification_items[:3]):
                        try:
                            title = item.find_element(By.CSS_SELECTOR, ".notification-title")
                            message = item.find_element(By.CSS_SELECTOR, ".notification-message")
                            type_tag = item.find_element(By.CSS_SELECTOR, ".el-tag")
                            print(f"  通知{i+1}:")
                            print(f"    标题: {title.text}")
                            print(f"    内容: {message.text}")
                            print(f"    类型: {type_tag.text}")
                        except Exception as e:
                            print(f"  通知{i+1}: 读取详情失败 - {e}")
                            # 尝试获取整个通知项的文本
                            try:
                                print(f"    完整文本: {item.text[:100]}...")
                            except:
                                print(f"    无法读取任何文本")
                else:
                    print("⚠️ 未找到通知项")
                    
            except Exception as e:
                print(f"⚠️ 通知列表检查失败: {e}")
            
            # 检查是否有空状态提示
            try:
                empty_state = self.driver.find_elements(By.CSS_SELECTOR, ".empty-state, .no-data")
                if empty_state:
                    print("⚠️ 显示空状态提示")
            except:
                pass
            
            # 检查控制台错误
            logs = self.driver.get_log('browser')
            js_errors = [log for log in logs if log['level'] == 'SEVERE']
            if js_errors:
                print("⚠️ JavaScript错误:")
                for error in js_errors:
                    print(f"  {error['message']}")
            else:
                print("✓ 无JavaScript错误")
            
            return True
            
        except Exception as e:
            print(f"❌ 通知页面测试失败: {e}")
            return False
    
    def run_test(self):
        """运行测试"""
        print("🏓 教练前端登录和通知显示测试")
        print("=" * 50)
        
        try:
            # 获取教练信息
            coach_info = self.get_coach_info()
            if not coach_info:
                return False
            
            # 设置浏览器
            if not self.setup_driver():
                return False
            
            # 测试登录
            login_success = self.test_frontend_login(coach_info)
            if not login_success:
                return False
            
            # 测试通知页面
            notifications_success = self.test_notifications_page()
            
            if login_success and notifications_success:
                print("\n🎉 测试完成！请查看截图了解详细情况")
            else:
                print("\n❌ 测试发现问题，请检查截图和日志")
            
            # 保持浏览器打开一段时间以便观察
            print("\n⏳ 保持浏览器打开10秒以便观察...")
            time.sleep(10)
            
            return True
            
        except Exception as e:
            print(f"❌ 测试执行失败: {e}")
            return False
        finally:
            if self.driver:
                self.driver.quit()
                print("🔚 浏览器已关闭")

if __name__ == '__main__':
    test = CoachFrontendLoginTest()
    test.run_test()