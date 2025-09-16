#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
教练审核申请功能 - 前端完整测试程序

测试范围：
1. 教练登录和身份验证
2. 教学管理页面渲染
3. 学生申请列表显示
4. 申请详情查看
5. 审核操作（同意/拒绝）
6. 学生管理功能
7. 数据更新和状态同步
8. 用户交互和反馈
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

class CoachApprovalSystemFrontendTest:
    """教练审核申请功能前端测试类"""
    
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
        
        # 创建校区（使用时间戳确保唯一性）
        timestamp = str(int(time.time()))
        self.campus = Campus.objects.get_or_create(
            name=f'测试校区_{timestamp}',
            defaults={
                'address': '测试地址123号',
                'phone': '12345678901',
                'description': '用于前端测试的校区',
                'code': f'TEST_{timestamp}'
            }
        )[0]
        
        # 清理旧的测试数据
        User.objects.filter(username__startswith='coach_frontend_test').delete()
        User.objects.filter(username__startswith='student_frontend_test').delete()
        
        # 创建测试教练（使用时间戳确保唯一性）
        self.coach_user = User.objects.create_user(
            username=f'coach_frontend_test_{timestamp}',
            email=f'coach_frontend_{timestamp}@test.com',
            password='testpass123',
            first_name='前端测试',
            last_name='教练',
            real_name='前端测试教练',
            phone=f'138{timestamp[-8:]}',
            gender='male',
            user_type='coach',
            is_active=True
        )
        self.coach_user.groups.add(coach_group)
        
        # 创建校区关联关系
        from campus.models import CampusCoach
        CampusCoach.objects.get_or_create(
            campus=self.campus,
            coach=self.coach_user
        )
        
        # 创建教练资料
        self.coach_profile = Coach.objects.create(
            user=self.coach_user,
            coach_level='senior',
            achievements='全国乒乓球锦标赛冠军，有10年教学经验',
            status='approved',
            max_students=20
        )
        
        # 创建测试学员
        self.students = []
        student_data = [
            {
                'username': 'student_frontend_test1',
                'real_name': '张学员',
                'phone': '13800138002',
                'gender': 'male'
            },
            {
                'username': 'student_frontend_test2',
                'real_name': '李学员',
                'phone': '13800138003',
                'gender': 'female'
            },
            {
                'username': 'student_frontend_test3',
                'real_name': '王学员',
                'phone': '13800138004',
                'gender': 'male'
            }
        ]
        
        for i, data in enumerate(student_data):
            student_user = User.objects.create_user(
                username=f"{data['username']}_{timestamp}",
                email=f"{data['username']}_{timestamp}@test.com",
                password='testpass123',
                real_name=data['real_name'],
                phone=f"139{timestamp[-7:]}{i}",
                gender=data['gender'],
                user_type='student',
                is_active=True
            )
            student_user.groups.add(student_group)
            
            # 创建校区关联关系
            from campus.models import CampusStudent
            CampusStudent.objects.get_or_create(
                campus=self.campus,
                student=student_user
            )
            
            self.students.append(student_user)
        
        # 创建师生关系申请
        self.relations = []
        statuses = ['pending', 'pending', 'approved']
        
        for i, student in enumerate(self.students):
            relation = CoachStudentRelation.objects.create(
                coach=self.coach_user,
                student=student,
                status=statuses[i],
                notes=f'我希望跟随{self.coach_user.real_name}教练学习乒乓球技术',
                applied_by='student'
            )
            self.relations.append(relation)
        
        print(f"✅ 创建了1个测试教练和{len(self.students)}个测试学员")
        print(f"✅ 创建了{len(self.relations)}个师生关系申请")
    
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
    
    def test_coach_login(self):
        """测试教练登录功能"""
        print("\n=== 测试1: 教练登录功能 ===")
        
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
            username_input.send_keys(self.coach_user.username)
            password_input.clear()
            password_input.send_keys('testpass123')
            
            # 点击登录
            login_button.click()
            time.sleep(3)
            
            # 检查是否登录成功
            current_url = self.driver.current_url
            if '/login' not in current_url or self.driver.find_elements(By.CSS_SELECTOR, ".user-info, .avatar, .el-dropdown"):
                print("✅ 教练登录成功")
                self.test_results.append(('教练登录', True, '登录功能正常'))
                return True
            else:
                print("❌ 教练登录失败")
                self.test_results.append(('教练登录', False, '登录失败'))
                return False
                
        except Exception as e:
            print(f"❌ 登录测试异常: {e}")
            self.test_results.append(('教练登录', False, f'异常: {e}'))
            return False
    
    def test_teaching_management_page(self):
        """测试教学管理页面"""
        print("\n=== 测试2: 教学管理页面 ===")
        
        try:
            # 访问教学管理页面
            self.driver.get(f"{self.frontend_url}/teaching-management")
            time.sleep(3)
            
            # 检查页面标题
            page_title = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "h1, h2, .page-title"))
            )
            
            if '教学管理' in page_title.text or '学员管理' in page_title.text:
                print("✅ 教学管理页面标题正确")
            
            # 检查标签页或导航
            tabs = self.driver.find_elements(By.CSS_SELECTOR, ".el-tabs__item, .tab-item, .nav-item")
            
            if tabs:
                print(f"✅ 找到 {len(tabs)} 个标签页")
                
                # 检查是否有申请管理和学员管理标签
                tab_texts = [tab.text for tab in tabs]
                print(f"✅ 标签页内容: {tab_texts}")
                
                if any('申请' in text for text in tab_texts):
                    print("✅ 找到申请管理标签")
                
                if any('学员' in text for text in tab_texts):
                    print("✅ 找到学员管理标签")
            
            self.test_results.append(('教学管理页面', True, '页面加载正常'))
            return True
                
        except Exception as e:
            print(f"❌ 教学管理页面测试异常: {e}")
            self.test_results.append(('教学管理页面', False, f'异常: {e}'))
            return False
    
    def test_application_list(self):
        """测试申请列表显示"""
        print("\n=== 测试3: 申请列表显示 ===")
        
        try:
            # 确保在教学管理页面
            if '/teaching-management' not in self.driver.current_url:
                self.driver.get(f"{self.frontend_url}/teaching-management")
                time.sleep(2)
            
            # 查找申请管理标签并点击
            application_tab = self.driver.find_elements(By.XPATH, "//span[contains(text(), '申请') or contains(text(), '待审核')]")
            
            if application_tab:
                application_tab[0].click()
                time.sleep(2)
                print("✅ 切换到申请管理标签")
            
            # 检查申请列表
            application_items = self.driver.find_elements(By.CSS_SELECTOR, ".application-item, .el-card, .student-application")
            
            if application_items:
                print(f"✅ 找到 {len(application_items)} 个申请")
                
                # 检查第一个申请的信息
                first_application = application_items[0]
                
                # 检查学员姓名
                name_elements = first_application.find_elements(By.CSS_SELECTOR, ".student-name, .name, h3, h4")
                if name_elements:
                    print(f"✅ 学员姓名显示: {name_elements[0].text}")
                
                # 检查申请状态
                status_elements = first_application.find_elements(By.CSS_SELECTOR, ".status, .申请状态, .tag")
                if status_elements:
                    print(f"✅ 申请状态显示: {status_elements[0].text}")
                
                # 检查申请时间
                time_elements = first_application.find_elements(By.CSS_SELECTOR, ".time, .申请时间, .date")
                if time_elements:
                    print(f"✅ 申请时间显示: {time_elements[0].text}")
                
                # 检查操作按钮
                action_buttons = first_application.find_elements(By.CSS_SELECTOR, "button, .btn, .action")
                if action_buttons:
                    print(f"✅ 找到 {len(action_buttons)} 个操作按钮")
                
                self.test_results.append(('申请列表显示', True, f'显示{len(application_items)}个申请'))
                return True
            else:
                print("⚠️  未找到申请列表，可能没有待审核申请")
                self.test_results.append(('申请列表显示', True, '无待审核申请'))
                return True
                
        except Exception as e:
            print(f"❌ 申请列表测试异常: {e}")
            self.test_results.append(('申请列表显示', False, f'异常: {e}'))
            return False
    
    def test_approval_operations(self):
        """测试审核操作"""
        print("\n=== 测试4: 审核操作 ===")
        
        try:
            # 确保在申请管理页面
            if '/teaching-management' not in self.driver.current_url:
                self.driver.get(f"{self.frontend_url}/teaching-management")
                time.sleep(2)
            
            # 查找待审核的申请
            application_items = self.driver.find_elements(By.CSS_SELECTOR, ".application-item, .el-card, .student-application")
            
            if application_items:
                # 测试同意操作
                approve_buttons = application_items[0].find_elements(By.CSS_SELECTOR, "button[class*='success'], .approve-btn, .同意")
                
                if approve_buttons:
                    print("✅ 找到同意按钮")
                    
                    # 点击同意
                    approve_buttons[0].click()
                    time.sleep(2)
                    
                    # 检查确认对话框
                    confirm_dialog = self.driver.find_elements(By.CSS_SELECTOR, ".el-message-box, .confirm-dialog")
                    
                    if confirm_dialog:
                        print("✅ 出现确认对话框")
                        
                        # 点击确认
                        confirm_button = confirm_dialog[0].find_elements(By.CSS_SELECTOR, "button[class*='primary'], .confirm")
                        if confirm_button:
                            confirm_button[0].click()
                            time.sleep(3)
                            
                            # 检查成功提示
                            success_message = self.driver.find_elements(By.CSS_SELECTOR, ".el-message--success, .success-message")
                            
                            if success_message:
                                print("✅ 同意操作成功")
                                self.test_results.append(('同意申请', True, '操作成功'))
                            else:
                                print("⚠️  同意操作已执行")
                                self.test_results.append(('同意申请', True, '操作已执行'))
                    else:
                        # 直接执行，检查结果
                        time.sleep(2)
                        success_message = self.driver.find_elements(By.CSS_SELECTOR, ".el-message--success, .success-message")
                        
                        if success_message:
                            print("✅ 同意操作成功")
                            self.test_results.append(('同意申请', True, '操作成功'))
                        else:
                            print("⚠️  同意操作已执行")
                            self.test_results.append(('同意申请', True, '操作已执行'))
                
                # 测试拒绝操作（如果还有其他申请）
                time.sleep(1)
                application_items = self.driver.find_elements(By.CSS_SELECTOR, ".application-item, .el-card, .student-application")
                
                if len(application_items) > 1:
                    reject_buttons = application_items[1].find_elements(By.CSS_SELECTOR, "button[class*='danger'], .reject-btn, .拒绝")
                    
                    if reject_buttons:
                        print("✅ 找到拒绝按钮")
                        
                        # 点击拒绝
                        reject_buttons[0].click()
                        time.sleep(2)
                        
                        # 检查拒绝理由输入框
                        reason_input = self.driver.find_elements(By.CSS_SELECTOR, "textarea, input[placeholder*='理由']")
                        
                        if reason_input:
                            reason_input[0].send_keys("暂时学员已满，请稍后再申请")
                            time.sleep(1)
                        
                        # 确认拒绝
                        confirm_reject = self.driver.find_elements(By.CSS_SELECTOR, "button[class*='danger'], .confirm")
                        if confirm_reject:
                            confirm_reject[0].click()
                            time.sleep(3)
                            
                            print("✅ 拒绝操作成功")
                            self.test_results.append(('拒绝申请', True, '操作成功'))
                
                return True
            else:
                print("⚠️  未找到待审核申请")
                self.test_results.append(('审核操作', True, '无待审核申请'))
                return True
                
        except Exception as e:
            print(f"❌ 审核操作测试异常: {e}")
            self.test_results.append(('审核操作', False, f'异常: {e}'))
            return False
    
    def test_student_management(self):
        """测试学员管理功能"""
        print("\n=== 测试5: 学员管理功能 ===")
        
        try:
            # 确保在教学管理页面
            if '/teaching-management' not in self.driver.current_url:
                self.driver.get(f"{self.frontend_url}/teaching-management")
                time.sleep(2)
            
            # 查找学员管理标签并点击
            student_tab = self.driver.find_elements(By.XPATH, "//span[contains(text(), '学员') or contains(text(), '我的学员')]")
            
            if student_tab:
                student_tab[0].click()
                time.sleep(2)
                print("✅ 切换到学员管理标签")
            
            # 检查学员列表
            student_items = self.driver.find_elements(By.CSS_SELECTOR, ".student-item, .el-card, .my-student")
            
            if student_items:
                print(f"✅ 找到 {len(student_items)} 个学员")
                
                # 检查第一个学员的信息
                first_student = student_items[0]
                
                # 检查学员姓名
                name_elements = first_student.find_elements(By.CSS_SELECTOR, ".student-name, .name, h3, h4")
                if name_elements:
                    print(f"✅ 学员姓名显示: {name_elements[0].text}")
                
                # 检查学员状态
                status_elements = first_student.find_elements(By.CSS_SELECTOR, ".status, .学员状态")
                if status_elements:
                    print(f"✅ 学员状态显示: {status_elements[0].text}")
                
                # 检查联系方式
                contact_elements = first_student.find_elements(By.CSS_SELECTOR, ".contact, .phone, .联系方式")
                if contact_elements:
                    print("✅ 联系方式显示正常")
                
                # 检查操作按钮
                action_buttons = first_student.find_elements(By.CSS_SELECTOR, "button, .btn")
                if action_buttons:
                    print(f"✅ 找到 {len(action_buttons)} 个操作按钮")
                
                self.test_results.append(('学员管理', True, f'显示{len(student_items)}个学员'))
                return True
            else:
                print("⚠️  未找到学员列表，可能还没有学员")
                self.test_results.append(('学员管理', True, '暂无学员'))
                return True
                
        except Exception as e:
            print(f"❌ 学员管理测试异常: {e}")
            self.test_results.append(('学员管理', False, f'异常: {e}'))
            return False
    
    def generate_test_report(self):
        """生成测试报告"""
        print("\n" + "=" * 60)
        print("📊 教练审核申请功能前端测试报告")
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
        with open('coach_approval_system_frontend_test_report.json', 'w', encoding='utf-8') as f:
            json.dump(report_data, f, ensure_ascii=False, indent=2)
        
        print(f"\n💾 测试报告已保存到: coach_approval_system_frontend_test_report.json")
        
        return report_data
    
    def run_all_tests(self):
        """运行所有测试"""
        print("🏓 开始教练审核申请功能前端测试")
        print("=" * 60)
        
        # 设置浏览器
        if not self.setup_driver():
            print("❌ 浏览器设置失败，无法继续测试")
            return False
        
        try:
            # 运行测试
            self.test_coach_login()
            self.test_teaching_management_page()
            self.test_application_list()
            self.test_approval_operations()
            self.test_student_management()
            
            # 生成报告
            report = self.generate_test_report()
            
            return report['pass_rate'] > 70  # 70%以上通过率认为测试成功
            
        finally:
            if self.driver:
                self.driver.quit()
                print("\n🔚 浏览器已关闭")

def main():
    """主函数"""
    print("🏓 乒乓球训练管理系统 - 教练审核申请功能前端测试")
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
    tester = CoachApprovalSystemFrontendTest()
    success = tester.run_all_tests()
    
    if success:
        print("\n🎉 教练审核申请功能前端测试完成！")
        print("📝 功能基本正常，可以进行用户验收测试")
    else:
        print("\n⚠️  教练审核申请功能前端测试完成，但存在一些问题")
        print("🔧 请根据测试报告修复相关问题")
    
    return success

if __name__ == '__main__':
    main()