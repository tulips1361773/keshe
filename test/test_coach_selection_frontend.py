#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试前端教练选择功能
"""

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import os
import sys
import django

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'keshe.settings')
django.setup()

from accounts.models import User

def test_coach_selection_error():
    print("=== 测试前端教练选择错误 ===")
    
    # 获取测试用户
    try:
        student = User.objects.filter(user_type='student').first()
        if not student:
            print("❌ 没有找到学员用户")
            return
        print(f"✅ 找到学员: {student.username}")
    except Exception as e:
        print(f"❌ 获取用户失败: {e}")
        return
    
    # 设置Chrome选项
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # 无头模式
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1920,1080')
    
    driver = None
    try:
        # 启动浏览器
        driver = webdriver.Chrome(options=chrome_options)
        driver.implicitly_wait(10)
        
        print("✅ 浏览器启动成功")
        
        # 1. 访问登录页面
        login_url = 'http://localhost:3002/login'
        driver.get(login_url)
        print(f"✅ 访问登录页面: {login_url}")
        
        # 等待页面加载
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "form"))
        )
        
        # 2. 填写登录信息
        username_input = driver.find_element(By.CSS_SELECTOR, "input[type='text'], input[placeholder*='用户名'], input[placeholder*='账号']")
        password_input = driver.find_element(By.CSS_SELECTOR, "input[type='password']")
        
        username_input.clear()
        username_input.send_keys(student.username)
        password_input.clear()
        password_input.send_keys('testpass123')
        
        print(f"✅ 填写登录信息: {student.username}")
        
        # 3. 点击登录按钮
        login_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit'], .el-button--primary")
        login_button.click()
        
        print("✅ 点击登录按钮")
        
        # 等待登录完成
        time.sleep(3)
        
        # 4. 访问教练选择页面
        coach_selection_url = 'http://localhost:3002/coach-selection'
        driver.get(coach_selection_url)
        print(f"✅ 访问教练选择页面: {coach_selection_url}")
        
        # 等待页面加载
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "coach-card"))
        )
        
        # 5. 查找并点击选择教练按钮
        try:
            select_buttons = driver.find_elements(By.CSS_SELECTOR, ".el-button--primary")
            if select_buttons:
                select_button = select_buttons[0]  # 选择第一个教练
                print("✅ 找到选择教练按钮")
                
                # 点击选择按钮
                driver.execute_script("arguments[0].click();", select_button)
                print("✅ 点击选择教练按钮")
                
                # 等待确认对话框
                time.sleep(2)
                
                # 查找并点击确认按钮
                try:
                    confirm_button = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, ".el-button--primary"))
                    )
                    confirm_button.click()
                    print("✅ 点击确认按钮")
                    
                    # 等待响应
                    time.sleep(3)
                    
                    # 6. 检查错误消息
                    try:
                        # 查找错误消息元素
                        error_elements = driver.find_elements(By.CSS_SELECTOR, ".el-message--error, .el-message.el-message--error")
                        if error_elements:
                            error_text = error_elements[0].text
                            print(f"✅ 捕获到错误消息: {error_text}")
                        else:
                            print("❌ 没有找到错误消息元素")
                            
                        # 检查控制台错误
                        logs = driver.get_log('browser')
                        console_errors = [log for log in logs if log['level'] == 'SEVERE']
                        if console_errors:
                            print("控制台错误:")
                            for error in console_errors:
                                print(f"  - {error['message']}")
                        else:
                            print("✅ 没有控制台错误")
                            
                    except Exception as e:
                        print(f"❌ 检查错误消息失败: {e}")
                        
                except TimeoutException:
                    print("❌ 没有找到确认按钮")
                    
            else:
                print("❌ 没有找到选择教练按钮")
                
        except Exception as e:
            print(f"❌ 选择教练过程失败: {e}")
        
        # 7. 截图保存
        try:
            screenshot_path = 'coach_selection_error_test.png'
            driver.save_screenshot(screenshot_path)
            print(f"✅ 截图已保存: {screenshot_path}")
        except Exception as e:
            print(f"❌ 截图失败: {e}")
            
    except Exception as e:
        print(f"❌ 测试过程中出现错误: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        if driver:
            driver.quit()
            print("✅ 浏览器已关闭")

if __name__ == '__main__':
    test_coach_selection_error()