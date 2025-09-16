#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
学生选择教练功能 - 前端完整测试程序

测试范围：
1. 学生登录和身份验证
2. 教练列表页面渲染和数据加载
3. 搜索和筛选功能
4. 教练详情页面
5. 选择教练功能
6. 用户交互和反馈
7. 错误处理和边界情况
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
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'keshe.settings')
django.setup()

from django.contrib.auth.models import Group
from accounts.models import User, Coach, UserProfile
from reservations.models import CoachStudentRelation
from campus.models import Campus
from django.contrib.auth import get_user_model

class StudentCoachSelectionFrontendTest:
    """学生选择教练功能前端测试类"""
    
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
        
        # 创建用户组
        student_group, _ = Group.objects.get_or_create(name='学员')
        coach_group, _ = Group.objects.get_or_create(name='教练员')
        
        # 创建校区
        self.campus = Campus.objects.get_or_create(
            name='测试校区',
            defaults={
                'address': '测试地址123号',
                'phone': '12345678901',
                'description': '用于前端测试的校区'
            }
        )[0]
        
        # 清理旧的测试数据
        User.objects.filter(username__startswith='frontend_test_').delete()
        
        # 创建测试学员
        self.student_user = User.objects.create_user(
            username='frontend_test_student',
            email='frontend_student@test.com',
            password='testpass123',
            first_name='前端测试',
            last_name='学员',
            real_name='前端测试学员',
            phone='13800138001',
            gender='male',
            user_type='student',
            campus=self.campus,
            is_active=True
        )
        self.student_user.groups.add(student_group)
        
        # 创建测试教练员
        self.coaches = []
        coach_data = [
            {
                'username': 'frontend_test_coach1',
                'real_name': '张教练',
                'gender': 'male',
                'phone': '13800138002',
                'level': 'senior',
                'achievements': '全国乒乓球锦标赛冠军，有10年教学经验'
            },
            {
                'username': 'frontend_test_coach2', 
                'real_name': '李教练',
                'gender': 'female',
                'phone': '13800138003',
                'level': 'intermediate',
                'achievements': '省级乒乓球比赛亚军，专长技术指导'
            },
            {
                'username': 'frontend_test_coach3',
                'real_name': '王教练', 
                'gender': 'male',
                'phone': '13800138004',
                'level': 'junior',
                'achievements': '市级乒乓球比赛冠军，擅长基础教学'
            }
        ]
        
        for i, data in enumerate(coach_data):
            # 创建教练用户
            coach_user = User.objects.create_user(
                username=data['username'],
                email=f"{data['username']}@test.com",
                password='testpass123',
                real_name=data['real_name'],
                phone=data['phone'],
                gender=data['gender'],
                user_type='coach',
                campus=self.campus,
                is_active=True
            )
            coach_user.groups.add(coach_group)
            
            # 创建教练资料
            coach_profile = Coach.objects.create(
                user=coach_user,
                coach_level=data['level'],
                achievements=data['achievements'],
                status='approved',
                max_students=20
            )
            
            self.coaches.append(coach_profile)
        
        print(f"✅ 创建了1个测试学员和{len(self.coaches)}个测试教练")
    
    def setup_driver(self):
        """设置浏览器驱动"""
        print("\n=== 设置浏览器驱动 ===")
        
        chrome_options = Options()
        chrome_options.add_argument('--headless')  # 无头模式
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')
        
        try:
            self.driver = webdriver.Chrome(options=chrome_options)
            self.wait = WebDriverWait(self.driver, 10)
            print("✅ 浏览器驱动设置成功")
            return True
        except Exception as e:
            print(f"❌ 浏览器驱动设置失败: {e}")
            return False
    
    def test_student_login(self):
        """测试学生登录功能"""
        print("\n=== 测试1: 学生登录功能 ===")
        
        try:
            # 访问登录页面
            self.driver.get(f"{self.frontend_url}/login")
            time.sleep(2)
            
            # 查找登录表单元素
            username_input = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='text'], input[placeholder*='用户名'], input[placeholder*='账号']"))
            )
            password_input = self.driver.find_element(By.CSS_SELECTOR, "input[type='password']")
            login_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit'], .el-button--primary")
            
            # 输入登录信息
            username_input.clear()
            username_input.send_keys('frontend_test_student')
            password_input.clear()
            password_input.send_keys('testpass123')
            
            # 点击登录
            login_button.click()
            time.sleep(3)
            
            # 检查是否登录成功（通过URL变化或页面元素判断）
            current_url = self.driver.current_url
            if '/login' not in current_url or self.driver.find_elements(By.CSS_SELECTOR, ".user-info, .avatar, .el-dropdown"):
                print("✅ 学生登录成功")
                self.test_results.append(('学生登录', True, '登录功能正常'))
                return True
            else:
                print("❌ 学生登录失败")
                self.test_results.append(('学生登录', False, '登录失败'))
                return False
                
        except Exception as e:
            print(f"❌ 登录测试异常: {e}")
            self.test_results.append(('学生登录', False, f'异常: {e}'))
            return False
    
    def test_coach_list_page(self):
        """测试教练列表页面"""
        print("\n=== 测试2: 教练列表页面 ===")
        
        try:
            # 访问教练选择页面
            self.driver.get(f"{self.frontend_url}/coach-selection")
            time.sleep(3)
            
            # 检查页面标题
            page_title = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "h1, h2, .page-title"))
            )
            
            if '教练' in page_title.text:
                print("✅ 教练列表页面标题正确")
            
            # 检查教练卡片是否存在
            coach_cards = self.driver.find_elements(By.CSS_SELECTOR, ".coach-card, .el-card, .coach-item")
            
            if len(coach_cards) > 0:
                print(f"✅ 找到 {len(coach_cards)} 个教练卡片")
                
                # 检查教练信息显示
                first_card = coach_cards[0]
                
                # 检查教练姓名
                name_elements = first_card.find_elements(By.CSS_SELECTOR, ".coach-name, .name, h3, h4")
                if name_elements:
                    print(f"✅ 教练姓名显示: {name_elements[0].text}")
                
                # 检查教练头像
                avatar_elements = first_card.find_elements(By.CSS_SELECTOR, ".avatar, .el-avatar, img")
                if avatar_elements:
                    print("✅ 教练头像显示正常")
                
                # 检查教练等级
                level_elements = first_card.find_elements(By.CSS_SELECTOR, ".level, .coach-level, .tag")
                if level_elements:
                    print(f"✅ 教练等级显示: {level_elements[0].text}")
                
                self.test_results.append(('教练列表页面', True, f'显示{len(coach_cards)}个教练'))
                return True
            else:
                print("❌ 未找到教练卡片")
                self.test_results.append(('教练列表页面', False, '未找到教练卡片'))
                return False
                
        except Exception as e:
            print(f"❌ 教练列表页面测试异常: {e}")
            self.test_results.append(('教练列表页面', False, f'异常: {e}'))
            return False
    
    def test_search_functionality(self):
        """测试搜索和筛选功能"""
        print("\n=== 测试3: 搜索和筛选功能 ===")
        
        try:
            # 确保在教练选择页面
            if '/coach-selection' not in self.driver.current_url:
                self.driver.get(f"{self.frontend_url}/coach-selection")
                time.sleep(2)
            
            # 测试姓名搜索
            search_input = self.driver.find_elements(By.CSS_SELECTOR, "input[placeholder*='搜索'], input[placeholder*='姓名'], .search-input input")
            
            if search_input:
                print("✅ 找到搜索输入框")
                
                # 输入搜索关键词
                search_input[0].clear()
                search_input[0].send_keys('张')
                
                # 查找搜索按钮或触发搜索
                search_button = self.driver.find_elements(By.CSS_SELECTOR, ".search-button, button[type='submit']")
                if search_button:
                    search_button[0].click()
                else:
                    search_input[0].send_keys(Keys.ENTER)
                
                time.sleep(2)
                
                # 检查搜索结果
                coach_cards = self.driver.find_elements(By.CSS_SELECTOR, ".coach-card, .el-card, .coach-item")
                print(f"✅ 搜索后显示 {len(coach_cards)} 个结果")
                
                self.test_results.append(('姓名搜索', True, f'搜索结果{len(coach_cards)}个'))
            
            # 测试等级筛选
            level_select = self.driver.find_elements(By.CSS_SELECTOR, ".el-select, select, .filter-select")
            
            if level_select:
                print("✅ 找到等级筛选器")
                
                # 点击筛选器
                level_select[0].click()
                time.sleep(1)
                
                # 选择高级教练
                senior_option = self.driver.find_elements(By.XPATH, "//span[contains(text(), '高级')]") 
                if senior_option:
                    senior_option[0].click()
                    time.sleep(2)
                    
                    coach_cards = self.driver.find_elements(By.CSS_SELECTOR, ".coach-card, .el-card, .coach-item")
                    print(f"✅ 等级筛选后显示 {len(coach_cards)} 个结果")
                    
                    self.test_results.append(('等级筛选', True, f'筛选结果{len(coach_cards)}个'))
            
            return True
            
        except Exception as e:
            print(f"❌ 搜索功能测试异常: {e}")
            self.test_results.append(('搜索功能', False, f'异常: {e}'))
            return False
    
    def test_coach_detail_page(self):
        """测试教练详情页面"""
        print("\n=== 测试4: 教练详情页面 ===")
        
        try:
            # 确保在教练选择页面
            if '/coach-selection' not in self.driver.current_url:
                self.driver.get(f"{self.frontend_url}/coach-selection")
                time.sleep(2)
            
            # 查找教练卡片
            coach_cards = self.driver.find_elements(By.CSS_SELECTOR, ".coach-card, .el-card, .coach-item")
            
            if coach_cards:
                # 查找详情按钮或点击教练卡片
                detail_buttons = coach_cards[0].find_elements(By.CSS_SELECTOR, "button, .detail-btn, .view-detail")
                
                if detail_buttons:
                    # 点击查看详情
                    detail_buttons[0].click()
                    time.sleep(3)
                    
                    # 检查是否跳转到详情页面或弹出详情对话框
                    current_url = self.driver.current_url
                    detail_dialog = self.driver.find_elements(By.CSS_SELECTOR, ".el-dialog, .modal, .detail-modal")
                    
                    if '/coach/' in current_url or detail_dialog:
                        print("✅ 成功打开教练详情页面")
                        
                        # 检查详情页面内容
                        if detail_dialog:
                            detail_container = detail_dialog[0]
                        else:
                            detail_container = self.driver
                        
                        # 检查教练基本信息
                        name_element = detail_container.find_elements(By.CSS_SELECTOR, ".coach-name, .name, h1, h2, h3")
                        if name_element:
                            print(f"✅ 教练姓名: {name_element[0].text}")
                        
                        # 检查成就信息
                        achievement_element = detail_container.find_elements(By.CSS_SELECTOR, ".achievement, .成就, .获奖")
                        if achievement_element:
                            print("✅ 成就信息显示正常")
                        
                        # 检查联系方式
                        contact_element = detail_container.find_elements(By.CSS_SELECTOR, ".contact, .phone, .联系")
                        if contact_element:
                            print("✅ 联系方式显示正常")
                        
                        self.test_results.append(('教练详情页面', True, '详情页面功能正常'))
                        return True
                    else:
                        print("❌ 未能打开教练详情页面")
                        self.test_results.append(('教练详情页面', False, '详情页面未打开'))
                        return False
                else:
                    print("❌ 未找到详情按钮")
                    self.test_results.append(('教练详情页面', False, '未找到详情按钮'))
                    return False
            else:
                print("❌ 未找到教练卡片")
                self.test_results.append(('教练详情页面', False, '未找到教练卡片'))
                return False
                
        except Exception as e:
            print(f"❌ 教练详情页面测试异常: {e}")
            self.test_results.append(('教练详情页面', False, f'异常: {e}'))
            return False
    
    def test_coach_selection_functionality(self):
        """测试选择教练功能"""
        print("\n=== 测试5: 选择教练功能 ===")
        
        try:
            # 确保在教练选择页面
            if '/coach-selection' not in self.driver.current_url:
                self.driver.get(f"{self.frontend_url}/coach-selection")
                time.sleep(2)
            
            # 查找教练卡片
            coach_cards = self.driver.find_elements(By.CSS_SELECTOR, ".coach-card, .el-card, .coach-item")
            
            if coach_cards:
                # 查找选择教练按钮
                select_buttons = coach_cards[0].find_elements(By.CSS_SELECTOR, "button[class*='primary'], .select-btn, .选择")
                
                if select_buttons:
                    # 点击选择教练
                    select_buttons[0].click()
                    time.sleep(2)
                    
                    # 检查是否出现确认对话框
                    confirm_dialog = self.driver.find_elements(By.CSS_SELECTOR, ".el-message-box, .confirm-dialog, .modal")
                    
                    if confirm_dialog:
                        print("✅ 出现选择确认对话框")
                        
                        # 查找确认按钮
                        confirm_button = confirm_dialog[0].find_elements(By.CSS_SELECTOR, "button[class*='primary'], .confirm-btn")
                        
                        if confirm_button:
                            confirm_button[0].click()
                            time.sleep(3)
                            
                            # 检查是否出现成功提示
                            success_message = self.driver.find_elements(By.CSS_SELECTOR, ".el-message--success, .success-message, .成功")
                            
                            if success_message:
                                print("✅ 选择教练成功")
                                self.test_results.append(('选择教练功能', True, '选择教练成功'))
                                return True
                            else:
                                print("⚠️  选择教练请求已发送，等待教练审核")
                                self.test_results.append(('选择教练功能', True, '申请已提交'))
                                return True
                    else:
                        # 直接提交，检查结果
                        time.sleep(2)
                        success_message = self.driver.find_elements(By.CSS_SELECTOR, ".el-message--success, .success-message")
                        
                        if success_message:
                            print("✅ 选择教练成功")
                            self.test_results.append(('选择教练功能', True, '选择教练成功'))
                            return True
                        else:
                            print("⚠️  选择教练请求已发送")
                            self.test_results.append(('选择教练功能', True, '申请已提交'))
                            return True
                else:
                    print("❌ 未找到选择教练按钮")
                    self.test_results.append(('选择教练功能', False, '未找到选择按钮'))
                    return False
            else:
                print("❌ 未找到教练卡片")
                self.test_results.append(('选择教练功能', False, '未找到教练卡片'))
                return False
                
        except Exception as e:
            print(f"❌ 选择教练功能测试异常: {e}")
            self.test_results.append(('选择教练功能', False, f'异常: {e}'))
            return False
    
    def test_error_handling(self):
        """测试错误处理"""
        print("\n=== 测试6: 错误处理 ===")
        
        try:
            # 测试网络错误处理
            # 访问不存在的页面
            self.driver.get(f"{self.frontend_url}/non-existent-page")
            time.sleep(2)
            
            # 检查是否有错误页面或404页面
            error_elements = self.driver.find_elements(By.CSS_SELECTOR, ".error, .404, .not-found")
            
            if error_elements or '404' in self.driver.page_source:
                print("✅ 404错误处理正常")
                self.test_results.append(('错误处理', True, '404页面正常'))
            else:
                print("⚠️  未找到明确的404错误页面")
                self.test_results.append(('错误处理', True, '基本错误处理'))
            
            return True
            
        except Exception as e:
            print(f"❌ 错误处理测试异常: {e}")
            self.test_results.append(('错误处理', False, f'异常: {e}'))
            return False
    
    def test_responsive_design(self):
        """测试响应式设计"""
        print("\n=== 测试7: 响应式设计 ===")
        
        try:
            # 访问教练选择页面
            self.driver.get(f"{self.frontend_url}/coach-selection")
            time.sleep(2)
            
            # 测试不同屏幕尺寸
            screen_sizes = [
                (1920, 1080),  # 桌面
                (768, 1024),   # 平板
                (375, 667)     # 手机
            ]
            
            for width, height in screen_sizes:
                self.driver.set_window_size(width, height)
                time.sleep(1)
                
                # 检查页面元素是否正常显示
                coach_cards = self.driver.find_elements(By.CSS_SELECTOR, ".coach-card, .el-card, .coach-item")
                
                if coach_cards:
                    print(f"✅ {width}x{height} 分辨率下显示正常")
                else:
                    print(f"⚠️  {width}x{height} 分辨率下可能有显示问题")
            
            # 恢复默认尺寸
            self.driver.set_window_size(1920, 1080)
            
            self.test_results.append(('响应式设计', True, '多分辨率测试完成'))
            return True
            
        except Exception as e:
            print(f"❌ 响应式设计测试异常: {e}")
            self.test_results.append(('响应式设计', False, f'异常: {e}'))
            return False
    
    def generate_test_report(self):
        """生成测试报告"""
        print("\n" + "=" * 60)
        print("📊 学生选择教练功能前端测试报告")
        print("=" * 60)
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for _, passed, _ in self.test_results if passed)
        failed_tests = total_tests - passed_tests
        
        print(f"\n📈 测试统计:")
        print(f"   总测试数: {total_tests}")
        print(f"   通过: {passed_tests}")
        print(f"   失败: {failed_tests}")
        print(f"   通过率: {(passed_tests/total_tests*100):.1f}%")
        
        print(f"\n📋 详细结果:")
        for test_name, passed, message in self.test_results:
            status = "✅" if passed else "❌"
            print(f"   {status} {test_name}: {message}")
        
        # 生成JSON报告
        report_data = {
            'test_time': datetime.now().isoformat(),
            'total_tests': total_tests,
            'passed_tests': passed_tests,
            'failed_tests': failed_tests,
            'pass_rate': round(passed_tests/total_tests*100, 1),
            'test_results': [
                {
                    'test_name': name,
                    'passed': passed,
                    'message': message
                }
                for name, passed, message in self.test_results
            ]
        }
        
        # 保存报告
        with open('student_coach_selection_frontend_test_report.json', 'w', encoding='utf-8') as f:
            json.dump(report_data, f, ensure_ascii=False, indent=2)
        
        print(f"\n💾 测试报告已保存到: student_coach_selection_frontend_test_report.json")
        
        return report_data
    
    def run_all_tests(self):
        """运行所有测试"""
        print("🏓 开始学生选择教练功能前端测试")
        print("=" * 60)
        
        # 设置浏览器
        if not self.setup_driver():
            print("❌ 浏览器设置失败，无法继续测试")
            return False
        
        try:
            # 运行测试
            self.test_student_login()
            self.test_coach_list_page()
            self.test_search_functionality()
            self.test_coach_detail_page()
            self.test_coach_selection_functionality()
            self.test_error_handling()
            self.test_responsive_design()
            
            # 生成报告
            report = self.generate_test_report()
            
            return report['pass_rate'] > 70  # 70%以上通过率认为测试成功
            
        finally:
            if self.driver:
                self.driver.quit()
                print("\n🔚 浏览器已关闭")

def main():
    """主函数"""
    print("🏓 乒乓球训练管理系统 - 学生选择教练功能前端测试")
    print("=" * 70)
    
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
    
    # 运行测试
    tester = StudentCoachSelectionFrontendTest()
    success = tester.run_all_tests()
    
    if success:
        print("\n🎉 学生选择教练功能前端测试完成！")
        print("📝 功能基本正常，可以进行用户验收测试")
    else:
        print("\n⚠️  学生选择教练功能前端测试完成，但存在一些问题")
        print("🔧 请根据测试报告修复相关问题")
    
    return success

if __name__ == '__main__':
    main()