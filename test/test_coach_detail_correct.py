#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
教练详情功能正确测试脚本
测试教练选择页面的教练详情功能是否正常工作
"""

import requests
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException

def test_coach_detail_functionality():
    """
    测试教练详情功能
    """
    print("教练详情功能测试")
    print("=" * 50)
    
    results = {
        '后端API测试': False,
        '前端页面访问': False,
        '教练详情功能': False
    }
    
    # 1. 测试后端API
    print("\n=== 1. 测试后端API ===")
    try:
        # 测试教练列表API
        response = requests.get('http://127.0.0.1:8000/api/reservations/coaches/', timeout=10)
        if response.status_code == 200:
            coaches_data = response.json()
            print(f"✅ 教练列表API正常，返回{len(coaches_data.get('results', []))}个教练")
            
            # 如果有教练数据，测试教练详情API
            if coaches_data.get('results'):
                coach_id = coaches_data['results'][0]['id']
                detail_response = requests.get(f'http://127.0.0.1:8000/api/accounts/coaches/{coach_id}/', timeout=10)
                if detail_response.status_code == 200:
                    print(f"✅ 教练详情API正常，教练ID: {coach_id}")
                    results['后端API测试'] = True
                else:
                    print(f"❌ 教练详情API失败: {detail_response.status_code}")
            else:
                print("⚠️  没有教练数据")
        else:
            print(f"❌ 教练列表API失败: {response.status_code}")
    except Exception as e:
        print(f"❌ 后端API测试失败: {e}")
    
    # 2. 测试前端页面
    print("\n=== 2. 测试前端页面 ===")
    driver = None
    try:
        # 设置Chrome选项
        chrome_options = Options()
        chrome_options.add_argument('--headless')  # 无头模式
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')
        
        driver = webdriver.Chrome(options=chrome_options)
        wait = WebDriverWait(driver, 10)
        
        # 访问前端页面
        frontend_url = 'http://localhost:3002'
        driver.get(frontend_url)
        time.sleep(2)
        
        # 检查页面是否加载
        if "乒乓球" in driver.title or len(driver.title) > 0:
            print(f"✅ 前端页面加载成功: {driver.title}")
            results['前端页面访问'] = True
            
            # 尝试访问Dashboard页面
            dashboard_url = f"{frontend_url}/#/dashboard"
            driver.get(dashboard_url)
            time.sleep(3)
            
            # 检查是否需要登录
            current_url = driver.current_url
            if 'login' in current_url:
                print("⚠️  需要登录才能访问Dashboard")
                # 尝试简单登录（如果有测试账号）
                try:
                    username_input = driver.find_element(By.CSS_SELECTOR, "input[type='text'], input[placeholder*='用户名'], input[placeholder*='账号']")
                    password_input = driver.find_element(By.CSS_SELECTOR, "input[type='password']")
                    login_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit'], .login-btn, .el-button--primary")
                    
                    username_input.send_keys("test_student")
                    password_input.send_keys("test123456")
                    login_button.click()
                    time.sleep(3)
                    
                    # 登录后再次访问Dashboard
                    driver.get(dashboard_url)
                    time.sleep(3)
                except Exception as login_error:
                    print(f"⚠️  自动登录失败: {login_error}")
            
            # 查找教练选择菜单项
            try:
                coach_selection_menu = wait.until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "[index='coach-selection'], .el-menu-item[index='coach-selection']"))
                )
                coach_selection_menu.click()
                time.sleep(3)
                print("✅ 成功点击教练选择菜单")
                
                # 查找教练卡片和详情按钮
                coach_cards = driver.find_elements(By.CSS_SELECTOR, ".coach-card, .el-card")
                if coach_cards:
                    print(f"✅ 找到{len(coach_cards)}个教练卡片")
                    
                    # 查找详情按钮
                    detail_buttons = driver.find_elements(By.CSS_SELECTOR, "button:contains('查看详情'), .detail-btn, button[onclick*='detail'], button[onclick*='Detail']")
                    if not detail_buttons:
                        # 尝试其他选择器
                        detail_buttons = driver.find_elements(By.XPATH, "//button[contains(text(), '查看详情') or contains(text(), '详情')]")
                    
                    if detail_buttons:
                        print(f"✅ 找到{len(detail_buttons)}个详情按钮")
                        
                        # 点击第一个详情按钮
                        detail_buttons[0].click()
                        time.sleep(3)
                        
                        # 检查是否跳转到详情页面
                        current_url = driver.current_url
                        if '/coaches/' in current_url:
                            print("✅ 成功跳转到教练详情页面")
                            
                            # 检查详情页面内容
                            page_content = driver.page_source
                            if any(keyword in page_content for keyword in ['教练', '联系方式', '基本信息', '成就']):
                                print("✅ 教练详情页面内容正常")
                                results['教练详情功能'] = True
                            else:
                                print("⚠️  教练详情页面内容可能不完整")
                        else:
                            print(f"⚠️  未跳转到详情页面，当前URL: {current_url}")
                    else:
                        print("❌ 未找到详情按钮")
                else:
                    print("❌ 未找到教练卡片")
                    
            except TimeoutException:
                print("❌ 未找到教练选择菜单项")
                
        else:
            print("❌ 前端页面加载失败")
            
    except Exception as e:
        print(f"❌ 前端测试失败: {e}")
    finally:
        if driver:
            driver.quit()
    
    # 3. 输出测试结果
    print("\n=== 测试结果汇总 ===")
    passed_tests = sum(results.values())
    total_tests = len(results)
    
    for test_name, result in results.items():
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{test_name}: {status}")
    
    print(f"\n总体结果: {passed_tests}/{total_tests} 通过")
    
    if results['教练详情功能']:
        print("\n🎉 教练详情功能测试通过！")
    else:
        print("\n⚠️  教练详情功能需要进一步检查")
    
    return results

if __name__ == '__main__':
    test_coach_detail_functionality()