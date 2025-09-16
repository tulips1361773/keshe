#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试教练详情功能是否正常工作
"""

import time
import requests
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
    print("=== 测试教练详情功能 ===")
    
    # 配置Chrome选项
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # 无头模式
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1920,1080')
    
    driver = None
    test_results = []
    
    try:
        # 启动浏览器
        driver = webdriver.Chrome(options=chrome_options)
        wait = WebDriverWait(driver, 10)
        
        frontend_url = "http://localhost:3002"
        backend_url = "http://127.0.0.1:8000"
        
        print(f"前端地址: {frontend_url}")
        print(f"后端地址: {backend_url}")
        
        # 测试1: 检查后端教练详情API
        print("\n=== 测试1: 后端教练详情API ===")
        try:
            # 先获取教练列表，找到一个教练ID
            response = requests.get(f"{backend_url}/accounts/api/coaches/", timeout=5)
            if response.status_code == 200:
                data = response.json()
                coaches = data.get('results', [])
                if coaches:
                    coach_id = coaches[0]['id']
                    print(f"✅ 找到教练ID: {coach_id}")
                    
                    # 测试教练详情API
                    detail_response = requests.get(f"{backend_url}/accounts/coaches/{coach_id}/", timeout=5)
                    if detail_response.status_code == 200:
                        detail_data = detail_response.json()
                        print(f"✅ 教练详情API正常")
                        print(f"   教练姓名: {detail_data.get('user', {}).get('real_name', 'N/A')}")
                        print(f"   教练等级: {detail_data.get('coach_level', 'N/A')}")
                        print(f"   状态: {detail_data.get('status', 'N/A')}")
                        test_results.append(('后端教练详情API', True, '正常'))
                    else:
                        print(f"❌ 教练详情API失败: {detail_response.status_code}")
                        test_results.append(('后端教练详情API', False, f'状态码: {detail_response.status_code}'))
                else:
                    print("❌ 没有找到教练数据")
                    test_results.append(('后端教练详情API', False, '没有教练数据'))
            else:
                print(f"❌ 获取教练列表失败: {response.status_code}")
                test_results.append(('后端教练详情API', False, f'获取教练列表失败: {response.status_code}'))
        except Exception as e:
            print(f"❌ 后端API测试异常: {e}")
            test_results.append(('后端教练详情API', False, f'异常: {e}'))
        
        # 测试2: 前端页面访问
        print("\n=== 测试2: 前端页面访问 ===")
        try:
            # 访问首页
            driver.get(frontend_url)
            time.sleep(2)
            
            # 检查页面是否加载成功
            page_title = driver.title
            print(f"✅ 页面标题: {page_title}")
            
            # 尝试访问教练选择页面（如果有的话）
            coach_selection_url = f"{frontend_url}/coach-selection"
            driver.get(coach_selection_url)
            time.sleep(3)
            
            # 检查是否有教练卡片
            coach_cards = driver.find_elements(By.CSS_SELECTOR, ".coach-card, .el-card, .coach-item")
            if coach_cards:
                print(f"✅ 找到 {len(coach_cards)} 个教练卡片")
                
                # 查找查看详情按钮
                first_card = coach_cards[0]
                detail_buttons = first_card.find_elements(By.CSS_SELECTOR, "button")
                
                detail_button = None
                for btn in detail_buttons:
                    if "详情" in btn.text:
                        detail_button = btn
                        break
                
                if detail_button:
                    print("✅ 找到查看详情按钮")
                    
                    # 点击查看详情按钮
                    detail_button.click()
                    time.sleep(3)
                    
                    # 检查是否跳转到详情页面
                    current_url = driver.current_url
                    if '/coaches/' in current_url:
                        print(f"✅ 成功跳转到教练详情页面: {current_url}")
                        
                        # 检查详情页面内容
                        coach_name = driver.find_elements(By.CSS_SELECTOR, ".coach-name, h1, h2")
                        if coach_name:
                            print(f"✅ 详情页面显示教练姓名: {coach_name[0].text}")
                        
                        contact_info = driver.find_elements(By.CSS_SELECTOR, ".contact-info, .phone, .email")
                        if contact_info:
                            print("✅ 详情页面显示联系信息")
                        
                        achievements = driver.find_elements(By.CSS_SELECTOR, ".achievements, .成就")
                        if achievements:
                            print("✅ 详情页面显示成就信息")
                        
                        test_results.append(('前端教练详情页面', True, '功能正常'))
                    else:
                        print(f"❌ 未跳转到详情页面，当前URL: {current_url}")
                        test_results.append(('前端教练详情页面', False, '未跳转到详情页面'))
                else:
                    print("❌ 未找到查看详情按钮")
                    test_results.append(('前端教练详情页面', False, '未找到详情按钮'))
            else:
                print("❌ 未找到教练卡片")
                test_results.append(('前端教练详情页面', False, '未找到教练卡片'))
                
        except Exception as e:
            print(f"❌ 前端页面测试异常: {e}")
            test_results.append(('前端教练详情页面', False, f'异常: {e}'))
        
        # 测试3: 直接访问教练详情页面
        print("\n=== 测试3: 直接访问教练详情页面 ===")
        try:
            # 使用一个测试ID直接访问详情页面
            test_coach_id = 1
            detail_url = f"{frontend_url}/coaches/{test_coach_id}"
            driver.get(detail_url)
            time.sleep(3)
            
            # 检查页面是否正常加载
            page_source = driver.page_source
            if "教练员详情" in page_source or "coach-detail" in page_source:
                print("✅ 教练详情页面正常加载")
                test_results.append(('直接访问详情页面', True, '页面正常加载'))
            else:
                print("❌ 教练详情页面加载异常")
                test_results.append(('直接访问详情页面', False, '页面加载异常'))
                
        except Exception as e:
            print(f"❌ 直接访问详情页面测试异常: {e}")
            test_results.append(('直接访问详情页面', False, f'异常: {e}'))
        
    except Exception as e:
        print(f"❌ 测试过程中发生异常: {e}")
        test_results.append(('整体测试', False, f'异常: {e}'))
    
    finally:
        if driver:
            driver.quit()
    
    # 输出测试结果
    print("\n" + "=" * 60)
    print("📊 测试结果汇总")
    print("=" * 60)
    
    passed_tests = 0
    total_tests = len(test_results)
    
    for test_name, passed, message in test_results:
        status_icon = "✅" if passed else "❌"
        print(f"{status_icon} {test_name}: {message}")
        if passed:
            passed_tests += 1
    
    print(f"\n📈 测试通过率: {passed_tests}/{total_tests} ({passed_tests/total_tests*100:.1f}%)")
    
    if passed_tests == total_tests:
        print("🎉 所有测试通过！教练详情功能正常工作。")
        return True
    else:
        print("⚠️  部分测试失败，请检查相关功能。")
        return False

if __name__ == "__main__":
    test_coach_detail_functionality()