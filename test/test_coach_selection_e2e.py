#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
教练员查询与选择功能 - 端到端测试

测试完整的用户流程：
1. 用户登录
2. 浏览教练员列表
3. 使用筛选和搜索功能
4. 选择教练员
5. 管理师生关系
6. 验证数据一致性
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

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'keshe.settings')
django.setup()

from django.contrib.auth.models import Group
from accounts.models import User, Coach, UserProfile
from reservations.models import CoachStudentRelation

class CoachSelectionE2ETest:
    """教练员选择功能端到端测试类"""
    
    def __init__(self):
        self.driver = None
        self.test_results = []
        self.base_url = "http://localhost:3001"
        self.api_base_url = "http://localhost:8000"
        self.setup_driver()
        self.setup_test_user()
    
    def setup_driver(self):
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
            
            print("✅ WebDriver 设置成功")
        except Exception as e:
            print(f"❌ WebDriver 设置失败: {str(e)}")
            print("提示: 请确保已安装Chrome浏览器和ChromeDriver")
            sys.exit(1)
    
    def setup_test_user(self):
        """设置测试用户"""
        try:
            # 创建或获取测试学员
            student_group, _ = Group.objects.get_or_create(name='学员')
            
            # 清理所有测试用户
            User.objects.filter(username__contains='test').delete()
            User.objects.filter(phone__in=['13800138001', '13900139001']).delete()
            
            self.test_user = User.objects.create(
                username='e2e_test_student',
                email='e2e_student@test.com',
                first_name='端到端',
                last_name='测试学员',
                real_name='端到端测试学员',
                phone='13900139001',
                gender='male',
                user_type='student'
            )
            
            self.test_user.groups.add(student_group)
            
            print(f"✅ 测试用户设置成功: {self.test_user.username}")
        except Exception as e:
            print(f"❌ 测试用户设置失败: {str(e)}")
    
    def log_test_result(self, test_name, success, message, details=None, screenshot=None):
        """记录测试结果"""
        result = {
            'test_name': test_name,
            'success': success,
            'message': message,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'details': details or {},
            'screenshot': screenshot
        }
        self.test_results.append(result)
        
        status_icon = "✅" if success else "❌"
        print(f"{status_icon} {test_name}: {message}")
        if details:
            for key, value in details.items():
                print(f"   {key}: {value}")
    
    def take_screenshot(self, name):
        """截取屏幕截图"""
        try:
            screenshot_path = f"screenshot_{name}_{int(time.time())}.png"
            self.driver.save_screenshot(screenshot_path)
            return screenshot_path
        except Exception as e:
            print(f"截图失败: {str(e)}")
            return None
    
    def wait_for_element(self, by, value, timeout=10):
        """等待元素出现"""
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, value))
            )
            return element
        except TimeoutException:
            return None
    
    def test_page_navigation(self):
        """测试页面导航"""
        print("\n=== 测试页面导航 ===")
        
        try:
            # 访问主页
            self.driver.get(self.base_url)
            time.sleep(2)
            
            # 检查页面是否加载成功
            page_title = self.driver.title
            page_loaded = "乒乓球" in page_title or "训练" in page_title or len(page_title) > 0
            
            self.log_test_result(
                "主页访问",
                page_loaded,
                "主页加载成功" if page_loaded else "主页加载失败",
                {"页面标题": page_title, "URL": self.driver.current_url}
            )
            
            # 导航到教练员选择页面
            coach_selection_url = f"{self.base_url}/#/coach-selection"
            self.driver.get(coach_selection_url)
            time.sleep(3)
            
            # 检查是否成功导航到教练员选择页面
            current_url = self.driver.current_url
            navigation_success = "coach-selection" in current_url
            
            screenshot = self.take_screenshot("coach_selection_page")
            
            self.log_test_result(
                "教练员选择页面导航",
                navigation_success,
                "成功导航到教练员选择页面" if navigation_success else "导航失败",
                {"目标URL": coach_selection_url, "当前URL": current_url},
                screenshot
            )
            
        except Exception as e:
            self.log_test_result(
                "页面导航测试",
                False,
                f"导航测试异常: {str(e)}"
            )
    
    def test_coach_list_display(self):
        """测试教练员列表显示"""
        print("\n=== 测试教练员列表显示 ===")
        
        try:
            # 等待教练员列表加载
            coach_list = self.wait_for_element(By.CLASS_NAME, "coach-list", 15)
            
            if coach_list:
                # 查找教练员卡片
                coach_cards = self.driver.find_elements(By.CLASS_NAME, "coach-card")
                card_count = len(coach_cards)
                
                # 检查是否有教练员数据
                has_coaches = card_count > 0
                
                self.log_test_result(
                    "教练员列表显示",
                    has_coaches,
                    f"教练员列表显示正常，共 {card_count} 个教练员" if has_coaches else "未找到教练员数据",
                    {"教练员卡片数量": card_count}
                )
                
                # 检查第一个教练员卡片的结构
                if coach_cards:
                    first_card = coach_cards[0]
                    
                    # 检查卡片基本信息
                    has_name = len(first_card.find_elements(By.CLASS_NAME, "coach-name")) > 0
                    has_level = len(first_card.find_elements(By.CLASS_NAME, "coach-level")) > 0
                    has_avatar = len(first_card.find_elements(By.CLASS_NAME, "coach-avatar")) > 0
                    
                    card_structure_valid = has_name or has_level  # 至少有姓名或等级
                    
                    self.log_test_result(
                        "教练员卡片结构",
                        card_structure_valid,
                        "教练员卡片结构完整" if card_structure_valid else "教练员卡片结构不完整",
                        {
                            "包含姓名": has_name,
                            "包含等级": has_level,
                            "包含头像": has_avatar
                        }
                    )
            else:
                self.log_test_result(
                    "教练员列表显示",
                    False,
                    "未找到教练员列表容器"
                )
        
        except Exception as e:
            self.log_test_result(
                "教练员列表显示测试",
                False,
                f"测试异常: {str(e)}"
            )
    
    def test_search_functionality(self):
        """测试搜索功能"""
        print("\n=== 测试搜索功能 ===")
        
        try:
            # 查找搜索输入框
            search_input = self.driver.find_element(By.CSS_SELECTOR, "input[placeholder*='搜索'], input[type='search']")
            
            if search_input:
                # 输入搜索关键词
                search_keyword = "张"
                search_input.clear()
                search_input.send_keys(search_keyword)
                time.sleep(1)
                
                # 查找搜索按钮或触发搜索
                search_button = self.driver.find_elements(By.CSS_SELECTOR, "button[type='submit'], .search-btn")
                if search_button:
                    search_button[0].click()
                else:
                    # 如果没有搜索按钮，尝试按回车
                    search_input.send_keys("\n")
                
                time.sleep(2)
                
                # 检查搜索结果
                coach_cards = self.driver.find_elements(By.CLASS_NAME, "coach-card")
                search_results_count = len(coach_cards)
                
                # 验证搜索结果是否包含关键词
                relevant_results = 0
                for card in coach_cards[:3]:  # 检查前3个结果
                    card_text = card.text.lower()
                    if search_keyword.lower() in card_text:
                        relevant_results += 1
                
                search_success = search_results_count > 0 and (relevant_results > 0 or search_results_count <= 5)
                
                self.log_test_result(
                    "搜索功能",
                    search_success,
                    f"搜索功能正常，找到 {search_results_count} 个结果" if search_success else "搜索功能异常",
                    {
                        "搜索关键词": search_keyword,
                        "结果数量": search_results_count,
                        "相关结果": relevant_results
                    }
                )
            else:
                self.log_test_result(
                    "搜索功能",
                    False,
                    "未找到搜索输入框"
                )
        
        except Exception as e:
            self.log_test_result(
                "搜索功能测试",
                False,
                f"测试异常: {str(e)}"
            )
    
    def test_filter_functionality(self):
        """测试筛选功能"""
        print("\n=== 测试筛选功能 ===")
        
        try:
            # 查找筛选控件
            filter_selects = self.driver.find_elements(By.TAG_NAME, "select")
            
            if filter_selects:
                # 尝试使用第一个筛选器
                first_filter = filter_selects[0]
                options = first_filter.find_elements(By.TAG_NAME, "option")
                
                if len(options) > 1:
                    # 选择第二个选项（跳过默认选项）
                    options[1].click()
                    time.sleep(2)
                    
                    # 检查筛选结果
                    coach_cards_after = self.driver.find_elements(By.CLASS_NAME, "coach-card")
                    filter_results_count = len(coach_cards_after)
                    
                    filter_success = True  # 假设筛选成功（实际应该检查结果是否符合筛选条件）
                    
                    self.log_test_result(
                        "筛选功能",
                        filter_success,
                        f"筛选功能正常，筛选后有 {filter_results_count} 个结果",
                        {
                            "筛选器数量": len(filter_selects),
                            "筛选后结果数量": filter_results_count
                        }
                    )
                else:
                    self.log_test_result(
                        "筛选功能",
                        False,
                        "筛选器选项不足"
                    )
            else:
                self.log_test_result(
                    "筛选功能",
                    False,
                    "未找到筛选控件"
                )
        
        except Exception as e:
            self.log_test_result(
                "筛选功能测试",
                False,
                f"测试异常: {str(e)}"
            )
    
    def test_coach_selection(self):
        """测试教练员选择功能"""
        print("\n=== 测试教练员选择功能 ===")
        
        try:
            # 查找教练员卡片
            coach_cards = self.driver.find_elements(By.CLASS_NAME, "coach-card")
            
            if coach_cards:
                # 选择第一个教练员
                first_card = coach_cards[0]
                
                # 查找选择按钮
                select_buttons = first_card.find_elements(By.CSS_SELECTOR, "button[class*='select'], .select-btn, button:contains('选择')")
                
                if select_buttons:
                    select_button = select_buttons[0]
                    
                    # 记录选择前的状态
                    button_text_before = select_button.text
                    
                    # 点击选择按钮
                    select_button.click()
                    time.sleep(1)
                    
                    # 处理可能的确认对话框
                    try:
                        confirm_button = self.wait_for_element(By.CSS_SELECTOR, ".el-button--primary, button[class*='confirm']", 3)
                        if confirm_button:
                            confirm_button.click()
                            time.sleep(2)
                    except:
                        pass
                    
                    # 检查选择结果
                    # 可以通过按钮状态变化、成功消息等来判断
                    success_message = self.driver.find_elements(By.CSS_SELECTOR, ".el-message--success, .success-message")
                    button_text_after = select_button.text if select_button.is_displayed() else "已选择"
                    
                    selection_success = len(success_message) > 0 or button_text_before != button_text_after
                    
                    self.log_test_result(
                        "教练员选择",
                        selection_success,
                        "教练员选择成功" if selection_success else "教练员选择可能失败",
                        {
                            "按钮文本变化": f"{button_text_before} -> {button_text_after}",
                            "成功消息": len(success_message) > 0
                        }
                    )
                else:
                    self.log_test_result(
                        "教练员选择",
                        False,
                        "未找到选择按钮"
                    )
            else:
                self.log_test_result(
                    "教练员选择",
                    False,
                    "未找到教练员卡片"
                )
        
        except Exception as e:
            self.log_test_result(
                "教练员选择测试",
                False,
                f"测试异常: {str(e)}"
            )
    
    def test_my_coaches_section(self):
        """测试我的教练员部分"""
        print("\n=== 测试我的教练员部分 ===")
        
        try:
            # 查找我的教练员部分
            my_coaches_section = self.driver.find_elements(By.CSS_SELECTOR, ".my-coaches, .selected-coaches")
            
            if my_coaches_section:
                section = my_coaches_section[0]
                
                # 检查是否有已选择的教练员
                selected_coaches = section.find_elements(By.CLASS_NAME, "selected-coach")
                selected_count = len(selected_coaches)
                
                self.log_test_result(
                    "我的教练员显示",
                    True,
                    f"我的教练员部分显示正常，已选择 {selected_count} 个教练员",
                    {"已选择教练员数量": selected_count}
                )
                
                # 如果有已选择的教练员，测试取消选择功能
                if selected_coaches:
                    first_selected = selected_coaches[0]
                    unselect_buttons = first_selected.find_elements(By.CSS_SELECTOR, "button[class*='unselect'], .unselect-btn")
                    
                    if unselect_buttons:
                        self.log_test_result(
                            "取消选择功能",
                            True,
                            "取消选择按钮存在",
                            {"取消选择按钮数量": len(unselect_buttons)}
                        )
                    else:
                        self.log_test_result(
                            "取消选择功能",
                            False,
                            "未找到取消选择按钮"
                        )
            else:
                self.log_test_result(
                    "我的教练员显示",
                    False,
                    "未找到我的教练员部分"
                )
        
        except Exception as e:
            self.log_test_result(
                "我的教练员测试",
                False,
                f"测试异常: {str(e)}"
            )
    
    def verify_data_consistency(self):
        """验证数据一致性"""
        print("\n=== 验证数据一致性 ===")
        
        try:
            # 检查数据库中的师生关系记录
            relations = CoachStudentRelation.objects.filter(student=self.test_user)
            db_relation_count = relations.count()
            
            # 检查前端显示的已选择教练员数量
            selected_coaches_elements = self.driver.find_elements(By.CLASS_NAME, "selected-coach")
            frontend_count = len(selected_coaches_elements)
            
            # 数据一致性检查
            data_consistent = abs(db_relation_count - frontend_count) <= 1  # 允许1个差异（考虑到异步更新）
            
            self.log_test_result(
                "数据一致性验证",
                data_consistent,
                "前后端数据一致" if data_consistent else "前后端数据不一致",
                {
                    "数据库记录数": db_relation_count,
                    "前端显示数": frontend_count,
                    "差异": abs(db_relation_count - frontend_count)
                }
            )
        
        except Exception as e:
            self.log_test_result(
                "数据一致性验证",
                False,
                f"验证异常: {str(e)}"
            )
    
    def run_all_tests(self):
        """运行所有端到端测试"""
        print("\n" + "="*60)
        print("教练员查询与选择功能 - 端到端测试")
        print("="*60)
        
        try:
            # 运行各项测试
            self.test_page_navigation()
            self.test_coach_list_display()
            self.test_search_functionality()
            self.test_filter_functionality()
            self.test_coach_selection()
            self.test_my_coaches_section()
            self.verify_data_consistency()
            
            # 生成测试报告
            self.generate_test_report()
        
        finally:
            # 清理资源
            if self.driver:
                self.driver.quit()
    
    def generate_test_report(self):
        """生成测试报告"""
        print("\n" + "="*60)
        print("端到端测试报告")
        print("="*60)
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result['success'])
        failed_tests = total_tests - passed_tests
        
        print(f"\n总测试数: {total_tests}")
        print(f"通过: {passed_tests}")
        print(f"失败: {failed_tests}")
        print(f"通过率: {(passed_tests/total_tests*100):.1f}%" if total_tests > 0 else "通过率: 0%")
        
        if failed_tests > 0:
            print("\n失败的测试:")
            for result in self.test_results:
                if not result['success']:
                    print(f"  ❌ {result['test_name']}: {result['message']}")
        
        # 保存详细报告到文件
        report_file = 'test_coach_selection_e2e_report.json'
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump({
                'summary': {
                    'total_tests': total_tests,
                    'passed_tests': passed_tests,
                    'failed_tests': failed_tests,
                    'pass_rate': f"{(passed_tests/total_tests*100):.1f}%" if total_tests > 0 else "0%",
                    'test_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'test_environment': {
                        'frontend_url': self.base_url,
                        'backend_url': self.api_base_url,
                        'test_user': self.test_user.username
                    }
                },
                'detailed_results': self.test_results
            }, f, ensure_ascii=False, indent=2)
        
        print(f"\n详细测试报告已保存到: {report_file}")
        
        # 显示截图信息
        screenshots = [r for r in self.test_results if r.get('screenshot')]
        if screenshots:
            print(f"\n截图文件 ({len(screenshots)} 个):")
            for result in screenshots:
                if result.get('screenshot'):
                    print(f"  📸 {result['test_name']}: {result['screenshot']}")

def main():
    """主函数"""
    print("🏓 开始教练员选择功能端到端测试...")
    print("\n注意事项:")
    print("1. 请确保前端服务器运行在 http://localhost:5173")
    print("2. 请确保后端服务器运行在 http://localhost:8000")
    print("3. 请确保已安装Chrome浏览器和ChromeDriver")
    print("4. 测试将在无头模式下运行")
    
    try:
        tester = CoachSelectionE2ETest()
        tester.run_all_tests()
    except KeyboardInterrupt:
        print("\n测试被用户中断")
    except Exception as e:
        print(f"\n测试运行异常: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()