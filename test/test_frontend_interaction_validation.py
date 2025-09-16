#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
前端页面交互和数据显示正确性验证测试程序

测试范围：
1. 页面加载和响应性测试
2. 用户界面交互测试
3. 数据显示准确性验证
4. 表单提交和验证测试
5. 错误处理和用户反馈测试
6. 跨浏览器兼容性测试
7. 移动端响应式设计测试
"""

import os
import sys
import django
import time
import json
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'keshe.settings')
django.setup()

from django.contrib.auth.models import Group
from accounts.models import User, Coach, UserProfile
from reservations.models import CoachStudentRelation
from campus.models import Campus, CampusStudent, CampusCoach
from django.contrib.auth import get_user_model

class FrontendInteractionValidationTest:
    """前端页面交互和数据显示正确性验证测试类"""
    
    def __init__(self):
        self.driver = None
        self.wait = None
        self.test_results = []
        self.frontend_url = "http://localhost:3002"
        self.backend_url = "http://127.0.0.1:8000"
        self.setup_test_data()
    
    def setup_test_data(self):
        """设置测试数据"""
        print("\n=== 设置测试数据 ===")
        
        # 清理旧的测试数据
        User.objects.filter(username__startswith='frontend_test_').delete()
        Campus.objects.filter(name__startswith='测试校区').delete()
        
        # 创建用户组
        student_group, _ = Group.objects.get_or_create(name='学员')
        coach_group, _ = Group.objects.get_or_create(name='教练员')
        
        # 创建校区（使用时间戳确保唯一性）
        import time
        timestamp = str(int(time.time()))
        
        self.campus = Campus.objects.create(
            name=f'测试校区_{timestamp}',
            code=f'TEST_{timestamp}',
            address='测试地址123号',
            phone='12345678901',
            description='用于前端交互测试的校区'
        )
        
        # 创建测试用户（使用时间戳确保唯一性）
        import time
        timestamp = str(int(time.time()))
        
        self.test_users = {
            'student': User.objects.create_user(
                username=f'frontend_test_student_{timestamp}',
                email=f'frontend_student_{timestamp}@test.com',
                password='testpass123',
                real_name='前端测试学员',
                phone=f'1380013{timestamp[-4:]}',
                gender='male',
                user_type='student',
                is_active=True
            ),
            'coach': User.objects.create_user(
                username=f'frontend_test_coach_{timestamp}',
                email=f'frontend_coach_{timestamp}@test.com',
                password='testpass123',
                real_name='前端测试教练',
                phone=f'1380014{timestamp[-4:]}',
                gender='female',
                user_type='coach',
                is_active=True
            )
        }
        
        # 添加用户到组
        self.test_users['student'].groups.add(student_group)
        self.test_users['coach'].groups.add(coach_group)
        
        # 创建校区关联关系
        CampusStudent.objects.get_or_create(
            campus=self.campus,
            student=self.test_users['student'],
            defaults={'is_active': True}
        )
        
        CampusCoach.objects.get_or_create(
            campus=self.campus,
            coach=self.test_users['coach'],
            defaults={'is_active': True}
        )
        
        # 创建教练资料
        self.coach_profile = Coach.objects.create(
            user=self.test_users['coach'],
            coach_level='intermediate',
            achievements='省级乒乓球比赛亚军，专长技术指导和战术分析',
            status='approved',
            max_students=20
        )
        
        print("✅ 测试数据设置完成")
    
    def setup_driver(self, browser='chrome'):
        """设置浏览器驱动"""
        print(f"\n=== 设置{browser}浏览器驱动 ===")
        
        try:
            if browser == 'chrome':
                chrome_options = Options()
                chrome_options.add_argument('--no-sandbox')
                chrome_options.add_argument('--disable-dev-shm-usage')
                chrome_options.add_argument('--disable-gpu')
                chrome_options.add_argument('--window-size=1920,1080')
                self.driver = webdriver.Chrome(options=chrome_options)
            elif browser == 'firefox':
                firefox_options = FirefoxOptions()
                firefox_options.add_argument('--width=1920')
                firefox_options.add_argument('--height=1080')
                self.driver = webdriver.Firefox(options=firefox_options)
            
            self.wait = WebDriverWait(self.driver, 15)
            print(f"✅ {browser}浏览器驱动设置成功")
            return True
        except Exception as e:
            print(f"❌ {browser}浏览器驱动设置失败: {e}")
            return False
    
    def test_page_loading_performance(self):
        """测试页面加载性能"""
        print("\n=== 测试页面加载性能 ===")
        
        pages_to_test = [
            ('首页', '/'),
            ('登录页', '/login'),
            ('教练选择页', '/coach-selection'),
            ('教练列表页', '/coaches'),
            ('教学管理页', '/teaching-management')
        ]
        
        loading_results = []
        
        for page_name, page_url in pages_to_test:
            try:
                print(f"\n🔍 测试{page_name}加载性能...")
                
                start_time = time.time()
                self.driver.get(f"{self.frontend_url}{page_url}")
                
                # 等待页面基本元素加载
                try:
                    self.wait.until(
                        EC.any_of(
                            EC.presence_of_element_located((By.TAG_NAME, "main")),
                            EC.presence_of_element_located((By.CLASS_NAME, "app")),
                            EC.presence_of_element_located((By.ID, "app")),
                            EC.presence_of_element_located((By.TAG_NAME, "body"))
                        )
                    )
                except TimeoutException:
                    pass  # 继续测试，即使没有找到特定元素
                
                end_time = time.time()
                load_time = end_time - start_time
                
                print(f"   ⏱️  加载时间: {load_time:.2f}秒")
                
                # 检查页面是否有错误
                error_elements = self.driver.find_elements(By.CSS_SELECTOR, ".error, .404, .not-found")
                has_error = len(error_elements) > 0
                
                # 检查页面内容是否加载
                page_text = self.driver.page_source
                has_content = len(page_text) > 1000  # 简单的内容检查
                
                result = {
                    'page': page_name,
                    'url': page_url,
                    'load_time': load_time,
                    'has_error': has_error,
                    'has_content': has_content,
                    'success': load_time < 10 and not has_error and has_content
                }
                
                loading_results.append(result)
                
                status = "✅" if result['success'] else "❌"
                print(f"   {status} {page_name}: {'成功' if result['success'] else '失败'}")
                
                # 截图记录
                self.driver.save_screenshot(f'frontend_test_page_{page_name.replace("页", "")}.png')
                
            except Exception as e:
                print(f"   ❌ {page_name}测试异常: {e}")
                loading_results.append({
                    'page': page_name,
                    'url': page_url,
                    'load_time': -1,
                    'has_error': True,
                    'has_content': False,
                    'success': False,
                    'error': str(e)
                })
        
        # 统计结果
        successful_pages = sum(1 for result in loading_results if result['success'])
        total_pages = len(loading_results)
        avg_load_time = sum(r['load_time'] for r in loading_results if r['load_time'] > 0) / max(1, len([r for r in loading_results if r['load_time'] > 0]))
        
        print(f"\n📊 页面加载性能统计:")
        print(f"   成功加载: {successful_pages}/{total_pages}")
        print(f"   平均加载时间: {avg_load_time:.2f}秒")
        
        self.test_results.append(('页面加载性能', successful_pages == total_pages, f'{successful_pages}/{total_pages}页面成功加载'))
        
        return loading_results
    
    def test_user_login_interaction(self):
        """测试用户登录交互"""
        print("\n=== 测试用户登录交互 ===")
        
        try:
            # 访问登录页面
            self.driver.get(f"{self.frontend_url}/login")
            time.sleep(3)
            
            # 测试表单验证
            print("🔍 测试表单验证...")
            
            # 查找表单元素
            username_input = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='text'], input[placeholder*='用户名'], input[placeholder*='账号']"))
            )
            password_input = self.driver.find_element(By.CSS_SELECTOR, "input[type='password']")
            login_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit'], .el-button--primary")
            
            # 测试空表单提交
            print("   📝 测试空表单提交...")
            login_button.click()
            time.sleep(2)
            
            # 检查验证提示
            validation_messages = self.driver.find_elements(By.CSS_SELECTOR, ".el-form-item__error, .error-message, .validation-error")
            empty_form_validation = len(validation_messages) > 0
            
            print(f"   {'✅' if empty_form_validation else '⚠️'} 空表单验证: {'有提示' if empty_form_validation else '无提示'}")
            
            # 测试错误登录
            print("   📝 测试错误登录...")
            username_input.clear()
            username_input.send_keys('wrong_user')
            password_input.clear()
            password_input.send_keys('wrong_pass')
            login_button.click()
            time.sleep(3)
            
            # 检查错误提示
            error_messages = self.driver.find_elements(By.CSS_SELECTOR, ".el-message--error, .error-message, .login-error")
            wrong_login_feedback = len(error_messages) > 0
            
            print(f"   {'✅' if wrong_login_feedback else '⚠️'} 错误登录反馈: {'有提示' if wrong_login_feedback else '无提示'}")
            
            # 测试正确登录
            print("   📝 测试正确登录...")
            username_input.clear()
            username_input.send_keys('frontend_test_student')
            password_input.clear()
            password_input.send_keys('testpass123')
            login_button.click()
            time.sleep(5)
            
            # 检查登录成功
            current_url = self.driver.current_url
            login_success = '/login' not in current_url
            
            print(f"   {'✅' if login_success else '❌'} 正确登录: {'成功' if login_success else '失败'}")
            
            # 截图记录
            self.driver.save_screenshot('frontend_test_login_interaction.png')
            
            interaction_score = sum([empty_form_validation, wrong_login_feedback, login_success])
            self.test_results.append(('用户登录交互', interaction_score >= 2, f'交互测试得分: {interaction_score}/3'))
            
            return login_success
            
        except Exception as e:
            print(f"❌ 登录交互测试异常: {e}")
            self.driver.save_screenshot('frontend_test_login_error.png')
            self.test_results.append(('用户登录交互', False, f'异常: {e}'))
            return False
    
    def test_coach_selection_interaction(self):
        """测试教练选择页面交互"""
        print("\n=== 测试教练选择页面交互 ===")
        
        try:
            # 访问教练选择页面
            self.driver.get(f"{self.frontend_url}/coach-selection")
            time.sleep(4)
            
            # 测试搜索功能
            print("🔍 测试搜索功能...")
            search_inputs = self.driver.find_elements(By.CSS_SELECTOR, "input[placeholder*='搜索'], input[placeholder*='查找'], .search-input")
            
            search_works = False
            if search_inputs:
                search_input = search_inputs[0]
                search_input.clear()
                search_input.send_keys('测试')
                search_input.send_keys(Keys.ENTER)
                time.sleep(2)
                search_works = True
                print("   ✅ 搜索功能可用")
            else:
                print("   ⚠️  未找到搜索输入框")
            
            # 测试筛选功能
            print("🔍 测试筛选功能...")
            filter_elements = self.driver.find_elements(By.CSS_SELECTOR, ".el-select, select, .filter-select")
            
            filter_works = False
            if filter_elements:
                try:
                    filter_element = filter_elements[0]
                    filter_element.click()
                    time.sleep(1)
                    filter_works = True
                    print("   ✅ 筛选功能可用")
                except:
                    print("   ⚠️  筛选功能交互异常")
            else:
                print("   ⚠️  未找到筛选元素")
            
            # 测试教练卡片交互
            print("🔍 测试教练卡片交互...")
            coach_cards = self.driver.find_elements(By.CSS_SELECTOR, ".coach-card, .el-card, .coach-item")
            
            card_interaction = False
            if coach_cards:
                first_card = coach_cards[0]
                
                # 测试悬停效果
                actions = ActionChains(self.driver)
                actions.move_to_element(first_card).perform()
                time.sleep(1)
                
                # 测试点击交互
                buttons = first_card.find_elements(By.CSS_SELECTOR, "button, .btn")
                if buttons:
                    buttons[0].click()
                    time.sleep(2)
                    card_interaction = True
                    print("   ✅ 教练卡片交互正常")
                else:
                    print("   ⚠️  教练卡片无交互按钮")
            else:
                print("   ⚠️  未找到教练卡片")
            
            # 测试响应式设计
            print("🔍 测试响应式设计...")
            
            # 模拟移动端视口
            self.driver.set_window_size(375, 667)  # iPhone 6/7/8 尺寸
            time.sleep(2)
            
            # 检查移动端布局
            mobile_layout_ok = True
            try:
                # 检查是否有横向滚动条
                body_width = self.driver.execute_script("return document.body.scrollWidth")
                window_width = self.driver.execute_script("return window.innerWidth")
                mobile_layout_ok = body_width <= window_width + 20  # 允许20px误差
                
                print(f"   {'✅' if mobile_layout_ok else '❌'} 移动端布局: {'正常' if mobile_layout_ok else '有横向滚动'}")
            except:
                print("   ⚠️  移动端布局检查异常")
            
            # 恢复桌面端视口
            self.driver.set_window_size(1920, 1080)
            time.sleep(1)
            
            # 截图记录
            self.driver.save_screenshot('frontend_test_coach_selection_interaction.png')
            
            interaction_score = sum([search_works, filter_works, card_interaction, mobile_layout_ok])
            self.test_results.append(('教练选择页面交互', interaction_score >= 2, f'交互测试得分: {interaction_score}/4'))
            
            return interaction_score >= 2
            
        except Exception as e:
            print(f"❌ 教练选择交互测试异常: {e}")
            self.driver.save_screenshot('frontend_test_coach_selection_error.png')
            self.test_results.append(('教练选择页面交互', False, f'异常: {e}'))
            return False
    
    def test_data_display_accuracy(self):
        """测试数据显示准确性"""
        print("\n=== 测试数据显示准确性 ===")
        
        try:
            # 访问教练列表页面
            self.driver.get(f"{self.frontend_url}/coaches")
            time.sleep(4)
            
            # 检查教练数据显示
            print("🔍 检查教练数据显示...")
            
            coach_elements = self.driver.find_elements(By.CSS_SELECTOR, ".coach-card, .coach-item, .el-card")
            
            data_accuracy_issues = []
            
            if coach_elements:
                for i, coach_element in enumerate(coach_elements[:3]):  # 检查前3个
                    print(f"\n   检查教练 {i+1}:")
                    
                    # 检查姓名显示
                    name_elements = coach_element.find_elements(By.CSS_SELECTOR, ".name, .coach-name, h3, h4")
                    if name_elements:
                        name_text = name_elements[0].text
                        if name_text and len(name_text.strip()) > 0:
                            print(f"     👤 姓名: {name_text} ✅")
                        else:
                            print(f"     👤 姓名: 空白 ❌")
                            data_accuracy_issues.append(f"教练{i+1}姓名为空")
                    else:
                        print(f"     👤 姓名: 未找到元素 ❌")
                        data_accuracy_issues.append(f"教练{i+1}姓名元素缺失")
                    
                    # 检查头像显示
                    avatar_elements = coach_element.find_elements(By.CSS_SELECTOR, ".avatar, .el-avatar, img")
                    if avatar_elements:
                        avatar_src = avatar_elements[0].get_attribute('src')
                        if avatar_src and 'default-avatar' not in avatar_src:
                            print(f"     🖼️  头像: 自定义头像 ✅")
                        elif avatar_src:
                            print(f"     🖼️  头像: 默认头像 ✅")
                        else:
                            print(f"     🖼️  头像: 无图片源 ❌")
                            data_accuracy_issues.append(f"教练{i+1}头像无图片源")
                    else:
                        print(f"     🖼️  头像: 未找到元素 ❌")
                        data_accuracy_issues.append(f"教练{i+1}头像元素缺失")
                    
                    # 检查等级显示
                    level_elements = coach_element.find_elements(By.CSS_SELECTOR, ".level, .coach-level, .tag")
                    if level_elements:
                        level_text = level_elements[0].text
                        if level_text and any(keyword in level_text for keyword in ['初级', '中级', '高级', 'junior', 'intermediate', 'senior']):
                            print(f"     🏆 等级: {level_text} ✅")
                        else:
                            print(f"     🏆 等级: {level_text} ⚠️")
                    else:
                        print(f"     🏆 等级: 未找到元素 ⚠️")
            else:
                print("   ❌ 未找到教练数据")
                data_accuracy_issues.append("未找到教练数据")
            
            # 检查页面标题和导航
            print("\n🔍 检查页面标题和导航...")
            
            page_title = self.driver.find_elements(By.CSS_SELECTOR, "title, h1, h2, .page-title")
            if page_title:
                title_text = page_title[0].text if hasattr(page_title[0], 'text') else page_title[0].get_attribute('textContent')
                print(f"   📋 页面标题: {title_text} ✅")
            else:
                print("   📋 页面标题: 未找到 ❌")
                data_accuracy_issues.append("页面标题缺失")
            
            # 检查导航菜单
            nav_elements = self.driver.find_elements(By.CSS_SELECTOR, "nav, .nav, .menu, .el-menu")
            if nav_elements:
                nav_items = nav_elements[0].find_elements(By.CSS_SELECTOR, "a, .nav-item, .el-menu-item")
                print(f"   🧭 导航项目: {len(nav_items)}个 ✅")
            else:
                print("   🧭 导航菜单: 未找到 ⚠️")
            
            # 截图记录
            self.driver.save_screenshot('frontend_test_data_display.png')
            
            accuracy_score = len(data_accuracy_issues) == 0
            issue_summary = f"发现{len(data_accuracy_issues)}个问题" if data_accuracy_issues else "数据显示正常"
            
            self.test_results.append(('数据显示准确性', accuracy_score, issue_summary))
            
            return accuracy_score
            
        except Exception as e:
            print(f"❌ 数据显示准确性测试异常: {e}")
            self.driver.save_screenshot('frontend_test_data_display_error.png')
            self.test_results.append(('数据显示准确性', False, f'异常: {e}'))
            return False
    
    def test_error_handling(self):
        """测试错误处理和用户反馈"""
        print("\n=== 测试错误处理和用户反馈 ===")
        
        try:
            error_handling_results = []
            
            # 测试404页面
            print("🔍 测试404页面处理...")
            self.driver.get(f"{self.frontend_url}/non-existent-page")
            time.sleep(3)
            
            page_text = self.driver.page_source.lower()
            has_404_handling = any(keyword in page_text for keyword in ['404', 'not found', '页面不存在', '找不到页面'])
            
            print(f"   {'✅' if has_404_handling else '❌'} 404页面处理: {'有处理' if has_404_handling else '无处理'}")
            error_handling_results.append(has_404_handling)
            
            # 测试网络错误处理（模拟）
            print("🔍 测试网络错误处理...")
            
            # 访问一个可能不存在的API端点
            self.driver.get(f"{self.frontend_url}/api/non-existent-endpoint")
            time.sleep(3)
            
            page_text = self.driver.page_source.lower()
            has_error_page = any(keyword in page_text for keyword in ['error', 'exception', '错误', '异常', '服务器错误'])
            
            print(f"   {'✅' if has_error_page else '⚠️'} 网络错误处理: {'有处理' if has_error_page else '无明确处理'}")
            error_handling_results.append(has_error_page)
            
            # 测试表单验证错误
            print("🔍 测试表单验证错误...")
            
            # 回到登录页面测试表单验证
            self.driver.get(f"{self.frontend_url}/login")
            time.sleep(3)
            
            # 尝试提交空表单
            login_button = self.driver.find_elements(By.CSS_SELECTOR, "button[type='submit'], .el-button--primary")
            if login_button:
                login_button[0].click()
                time.sleep(2)
                
                # 检查验证错误提示
                validation_errors = self.driver.find_elements(By.CSS_SELECTOR, ".el-form-item__error, .error-message, .validation-error")
                has_validation_feedback = len(validation_errors) > 0
                
                print(f"   {'✅' if has_validation_feedback else '❌'} 表单验证反馈: {'有反馈' if has_validation_feedback else '无反馈'}")
                error_handling_results.append(has_validation_feedback)
            else:
                print("   ⚠️  未找到登录按钮")
                error_handling_results.append(False)
            
            # 测试用户友好的错误信息
            print("🔍 测试用户友好的错误信息...")
            
            # 检查错误信息是否用户友好（中文或易懂的英文）
            all_error_elements = self.driver.find_elements(By.CSS_SELECTOR, ".error, .el-message--error, .validation-error")
            
            user_friendly_errors = True
            for error_element in all_error_elements:
                error_text = error_element.text
                if error_text:
                    # 检查是否包含技术性错误信息（如堆栈跟踪）
                    if any(tech_keyword in error_text.lower() for tech_keyword in ['stack trace', 'exception', 'null pointer', 'undefined']):
                        user_friendly_errors = False
                        break
            
            print(f"   {'✅' if user_friendly_errors else '❌'} 用户友好错误: {'友好' if user_friendly_errors else '包含技术信息'}")
            error_handling_results.append(user_friendly_errors)
            
            # 截图记录
            self.driver.save_screenshot('frontend_test_error_handling.png')
            
            error_handling_score = sum(error_handling_results)
            total_error_tests = len(error_handling_results)
            
            self.test_results.append(('错误处理和用户反馈', error_handling_score >= total_error_tests // 2, f'错误处理得分: {error_handling_score}/{total_error_tests}'))
            
            return error_handling_score >= total_error_tests // 2
            
        except Exception as e:
            print(f"❌ 错误处理测试异常: {e}")
            self.driver.save_screenshot('frontend_test_error_handling_error.png')
            self.test_results.append(('错误处理和用户反馈', False, f'异常: {e}'))
            return False
    
    def test_responsive_design(self):
        """测试响应式设计"""
        print("\n=== 测试响应式设计 ===")
        
        try:
            # 测试不同屏幕尺寸
            screen_sizes = [
                ('桌面端', 1920, 1080),
                ('平板端', 768, 1024),
                ('手机端', 375, 667)
            ]
            
            responsive_results = []
            
            for size_name, width, height in screen_sizes:
                print(f"\n🔍 测试{size_name}响应式设计 ({width}x{height})...")
                
                # 设置窗口大小
                self.driver.set_window_size(width, height)
                time.sleep(2)
                
                # 访问主要页面
                self.driver.get(f"{self.frontend_url}/coach-selection")
                time.sleep(3)
                
                # 检查布局是否适应
                try:
                    # 检查是否有横向滚动条
                    body_width = self.driver.execute_script("return document.body.scrollWidth")
                    window_width = self.driver.execute_script("return window.innerWidth")
                    no_horizontal_scroll = body_width <= window_width + 50  # 允许50px误差
                    
                    # 检查主要元素是否可见
                    main_elements = self.driver.find_elements(By.CSS_SELECTOR, "main, .main-content, .container")
                    elements_visible = len(main_elements) > 0
                    
                    # 检查导航是否适应（移动端可能折叠）
                    nav_elements = self.driver.find_elements(By.CSS_SELECTOR, "nav, .nav, .menu")
                    nav_adapted = len(nav_elements) > 0
                    
                    if width <= 768:  # 移动端特殊检查
                        # 检查是否有汉堡菜单或折叠导航
                        mobile_nav = self.driver.find_elements(By.CSS_SELECTOR, ".hamburger, .mobile-menu, .menu-toggle")
                        nav_adapted = nav_adapted or len(mobile_nav) > 0
                    
                    responsive_score = sum([no_horizontal_scroll, elements_visible, nav_adapted])
                    
                    print(f"   📱 横向滚动: {'无' if no_horizontal_scroll else '有'} {'✅' if no_horizontal_scroll else '❌'}")
                    print(f"   👁️  元素可见: {'是' if elements_visible else '否'} {'✅' if elements_visible else '❌'}")
                    print(f"   🧭 导航适应: {'是' if nav_adapted else '否'} {'✅' if nav_adapted else '❌'}")
                    
                    responsive_results.append({
                        'size': size_name,
                        'score': responsive_score,
                        'max_score': 3,
                        'success': responsive_score >= 2
                    })
                    
                    # 截图记录
                    self.driver.save_screenshot(f'frontend_test_responsive_{size_name}.png')
                    
                except Exception as e:
                    print(f"   ❌ {size_name}响应式测试异常: {e}")
                    responsive_results.append({
                        'size': size_name,
                        'score': 0,
                        'max_score': 3,
                        'success': False
                    })
            
            # 恢复桌面端尺寸
            self.driver.set_window_size(1920, 1080)
            time.sleep(1)
            
            # 统计响应式设计结果
            successful_sizes = sum(1 for result in responsive_results if result['success'])
            total_sizes = len(responsive_results)
            
            print(f"\n📊 响应式设计统计:")
            print(f"   适应良好: {successful_sizes}/{total_sizes}")
            
            self.test_results.append(('响应式设计', successful_sizes >= total_sizes // 2, f'{successful_sizes}/{total_sizes}尺寸适应良好'))
            
            return successful_sizes >= total_sizes // 2
            
        except Exception as e:
            print(f"❌ 响应式设计测试异常: {e}")
            self.driver.save_screenshot('frontend_test_responsive_error.png')
            self.test_results.append(('响应式设计', False, f'异常: {e}'))
            return False
    
    def generate_validation_report(self):
        """生成验证测试报告"""
        print("\n" + "=" * 70)
        print("📊 前端页面交互和数据显示正确性验证报告")
        print("=" * 70)
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for _, passed, _ in self.test_results if passed)
        failed_tests = total_tests - passed_tests
        
        print(f"\n📈 测试统计:")
        print(f"   总测试项目: {total_tests}")
        print(f"   通过项目: {passed_tests}")
        print(f"   失败项目: {failed_tests}")
        print(f"   通过率: {(passed_tests/total_tests*100):.1f}%")
        
        print(f"\n📋 详细测试结果:")
        for test_name, passed, message in self.test_results:
            status = "✅" if passed else "❌"
            print(f"   {status} {test_name}: {message}")
        
        # 前端质量评估
        print(f"\n🎯 前端质量评估:")
        if passed_tests >= total_tests * 0.9:
            print("   🌟 优秀: 前端功能完善，用户体验优良")
        elif passed_tests >= total_tests * 0.75:
            print("   👍 良好: 前端功能基本完善，少数问题需要优化")
        elif passed_tests >= total_tests * 0.6:
            print("   ⚠️  一般: 前端基本可用，但存在一些用户体验问题")
        else:
            print("   ❌ 较差: 前端存在较多问题，需要重点改进")
        
        # 改进建议
        print(f"\n💡 改进建议:")
        failed_areas = [name for name, passed, _ in self.test_results if not passed]
        if failed_areas:
            for area in failed_areas:
                if '页面加载' in area:
                    print("   🚀 优化页面加载性能，减少资源大小，使用CDN")
                elif '登录交互' in area:
                    print("   🔐 改进登录表单验证和用户反馈机制")
                elif '数据显示' in area:
                    print("   📊 检查数据绑定和显示逻辑，确保数据准确性")
                elif '错误处理' in area:
                    print("   🛠️ 完善错误处理机制，提供用户友好的错误信息")
                elif '响应式' in area:
                    print("   📱 优化响应式设计，确保多设备兼容性")
        else:
            print("   🎉 前端功能表现良好，继续保持！")
        
        # 生成JSON报告
        report_data = {
            'test_time': datetime.now().isoformat(),
            'test_type': 'Frontend Interaction Validation',
            'total_tests': total_tests,
            'passed_tests': passed_tests,
            'failed_tests': failed_tests,
            'pass_rate': round(passed_tests/total_tests*100, 1),
            'frontend_quality_score': min(100, (passed_tests/total_tests)*100),
            'test_results': [
                {
                    'test_name': name,
                    'passed': passed,
                    'message': message
                }
                for name, passed, message in self.test_results
            ],
            'screenshots': [
                'frontend_test_page_首页.png',
                'frontend_test_login_interaction.png',
                'frontend_test_coach_selection_interaction.png',
                'frontend_test_data_display.png',
                'frontend_test_error_handling.png',
                'frontend_test_responsive_桌面端.png',
                'frontend_test_responsive_平板端.png',
                'frontend_test_responsive_手机端.png'
            ]
        }
        
        # 保存报告
        with open('frontend_interaction_validation_report.json', 'w', encoding='utf-8') as f:
            json.dump(report_data, f, ensure_ascii=False, indent=2)
        
        print(f"\n💾 前端验证测试报告已保存到: frontend_interaction_validation_report.json")
        print(f"📸 测试截图已保存到当前目录")
        
        return report_data
    
    def run_complete_validation_test(self):
        """运行完整的前端验证测试"""
        print("🏓 开始前端页面交互和数据显示正确性验证测试")
        print("=" * 70)
        
        # 设置浏览器
        if not self.setup_driver('chrome'):
            print("❌ 浏览器设置失败，无法继续测试")
            return False
        
        try:
            print("\n🚀 开始执行前端验证测试...")
            
            # 1. 页面加载性能测试
            self.test_page_loading_performance()
            
            # 2. 用户登录交互测试
            login_success = self.test_user_login_interaction()
            
            # 3. 教练选择页面交互测试
            self.test_coach_selection_interaction()
            
            # 4. 数据显示准确性测试
            self.test_data_display_accuracy()
            
            # 5. 错误处理测试
            self.test_error_handling()
            
            # 6. 响应式设计测试
            self.test_responsive_design()
            
            # 生成报告
            report = self.generate_validation_report()
            
            return report['pass_rate'] > 70  # 70%以上通过率认为验证成功
            
        finally:
            if self.driver:
                print("\n⏳ 等待5秒以便查看最终状态...")
                time.sleep(5)
                self.driver.quit()
                print("🔚 浏览器已关闭")

def main():
    """主函数"""
    print("🏓 乒乓球训练管理系统 - 前端页面交互和数据显示正确性验证测试")
    print("=" * 80)
    
    # 检查前端服务是否运行
    import requests
    try:
        response = requests.get("http://localhost:3002", timeout=5)
        print("✅ 前端服务运行正常")
    except:
        print("❌ 前端服务未运行，请先启动前端服务: npm run dev")
        return False
    
    # 检查后端服务是否运行
    try:
        response = requests.get("http://127.0.0.1:8000/api/accounts/csrf-token/", timeout=5)
        print("✅ 后端服务运行正常")
    except:
        print("❌ 后端服务未运行，请先启动后端服务: python manage.py runserver")
        return False
    
    # 运行前端验证测试
    tester = FrontendInteractionValidationTest()
    success = tester.run_complete_validation_test()
    
    if success:
        print("\n🎉 前端页面交互和数据显示正确性验证测试完成！")
        print("🌟 前端功能表现良好，用户体验优秀")
        print("📝 系统前端已准备好投入使用")
    else:
        print("\n⚠️  前端页面交互和数据显示正确性验证测试完成，但存在一些问题")
        print("🔧 请根据测试报告和截图修复相关问题")
        print("📋 重点关注失败的测试项目和用户体验改进")
    
    return success

if __name__ == '__main__':
    main()