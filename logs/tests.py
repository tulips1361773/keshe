from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from rest_framework.test import APITestCase
from rest_framework import status
from campus.models import Campus, CampusStudent
from .models import SystemLog, LoginLog
from .utils import log_user_action, get_client_ip, get_user_agent

User = get_user_model()


class SystemLogModelTest(TestCase):
    """系统日志模型测试"""
    
    def setUp(self):
        """设置测试数据"""
        self.campus = Campus.objects.create(
            name='测试校区',
            code='TEST001',
            address='测试地址',
            phone='13800138000'
        )
        
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            real_name='测试用户',
            phone='13800138001',
            user_type='student'
        )
        
        # 创建用户和校区的关联关系
        CampusStudent.objects.create(
            campus=self.campus,
            student=self.user
        )
        
        self.campus_admin = User.objects.create_user(
            username='admin',
            password='adminpass123',
            real_name='校区管理员',
            phone='13800138002',
            user_type='campus_admin'
        )
        
        # 设置校区管理员
        self.campus.manager = self.campus_admin
        self.campus.save()
        
        self.student = User.objects.create_user(
            username='student',
            password='testpass123',
            real_name='学员',
            phone='13800138003',
            user_type='student'
        )
        
        # 创建学员和校区的关联关系
        CampusStudent.objects.create(
            campus=self.campus,
            student=self.student
        )
    
    def test_create_system_log(self):
        """测试创建系统日志"""
        log = SystemLog.create_log(
            user=self.campus_admin,
            action_type='create',
            resource_type='student',
            resource_id='123',
            resource_name='测试学员',
            description='创建学员账户',
            ip_address='127.0.0.1',
            campus=self.campus
        )
        
        self.assertEqual(log.user, self.campus_admin)
        self.assertEqual(log.action_type, 'create')
        self.assertEqual(log.resource_type, 'student')
        self.assertEqual(log.resource_id, '123')
        self.assertEqual(log.resource_name, '测试学员')
        self.assertEqual(log.description, '创建学员账户')
        self.assertEqual(log.ip_address, '127.0.0.1')
        self.assertEqual(log.campus, self.campus)
    
    def test_system_log_str(self):
        """测试系统日志字符串表示"""
        log = SystemLog.create_log(
            user=self.campus_admin,
            action_type='update',
            resource_type='campus',
            description='更新校区信息'
        )
        
        expected = f"{self.campus_admin.real_name} - 更新 - 更新校区信息"
        self.assertEqual(str(log), expected)
    
    def test_auto_set_campus(self):
        """测试自动设置校区"""
        # 获取用户关联的校区
        user_campus = self.user.campus_memberships.first().campus
        
        log = SystemLog.create_log(
            user=self.user,
            action_type='create',
            resource_type='student',
            description='创建学员'
        )
        
        # 应该自动设置为用户的校区
        self.assertEqual(log.campus, user_campus)


class LoginLogModelTest(TestCase):
    """登录日志模型测试"""
    
    def setUp(self):
        """设置测试数据"""
        self.campus = Campus.objects.create(
            name='测试校区',
            code='TEST002',
            address='测试地址',
            phone='13800138010'
        )
        
        self.user = User.objects.create_user(
            username='testuser2',
            password='testpass123',
            real_name='测试用户2',
            phone='13800138011'
        )
    
    def test_create_login_log(self):
        """测试创建登录日志"""
        login_log = LoginLog.objects.create(
            user=self.user,
            ip_address='127.0.0.1',
            user_agent='Test Browser',
            session_key='test_session_key'
        )
        
        self.assertEqual(login_log.user, self.user)
        self.assertEqual(login_log.ip_address, '127.0.0.1')
        self.assertEqual(login_log.user_agent, 'Test Browser')
        self.assertEqual(login_log.session_key, 'test_session_key')
        self.assertTrue(login_log.is_successful)
    
    def test_session_duration(self):
        """测试会话持续时间计算"""
        login_time = timezone.now()
        logout_time = login_time + timezone.timedelta(hours=2, minutes=30)
        
        login_log = LoginLog.objects.create(
            user=self.user,
            login_time=login_time,
            logout_time=logout_time
        )
        
        duration = login_log.session_duration
        self.assertIsNotNone(duration)
        self.assertEqual(duration.total_seconds(), 2.5 * 3600)  # 2.5小时
    
    def test_login_log_str(self):
        """测试登录日志字符串表示"""
        login_log = LoginLog.objects.create(
            user=self.user,
            is_successful=True
        )
        
        expected = f"{self.user.real_name} - {login_log.login_time.strftime('%Y-%m-%d %H:%M:%S')} - 成功"
        self.assertEqual(str(login_log), expected)


class LogUtilsTest(TestCase):
    """日志工具函数测试"""
    
    def setUp(self):
        """设置测试数据"""
        self.campus = Campus.objects.create(
            name='测试校区',
            code='TEST003',
            address='测试地址',
            phone='13800138020'
        )
        
        self.user = User.objects.create_user(
            username='testuser3',
            password='testpass123',
            real_name='测试用户3',
            phone='13800138021'
        )
        
        self.client = Client()
    
    def test_get_client_ip(self):
        """测试获取客户端IP"""
        from django.test import RequestFactory
        from .utils import get_client_ip
        
        factory = RequestFactory()
        
        # 测试普通IP
        request = factory.get('/')
        request.META['REMOTE_ADDR'] = '192.168.1.1'
        self.assertEqual(get_client_ip(request), '192.168.1.1')
        
        # 测试X-Forwarded-For头
        request = factory.get('/')
        request.META['HTTP_X_FORWARDED_FOR'] = '203.0.113.1, 192.168.1.1'
        request.META['REMOTE_ADDR'] = '192.168.1.1'
        self.assertEqual(get_client_ip(request), '203.0.113.1')
    
    def test_log_user_action(self):
        """测试记录用户操作"""
        # 创建用户和校区的关联关系
        CampusStudent.objects.create(
            campus=self.campus,
            student=self.user
        )
        
        from django.test import RequestFactory
        
        factory = RequestFactory()
        request = factory.post('/')
        request.META['REMOTE_ADDR'] = '127.0.0.1'
        request.META['HTTP_USER_AGENT'] = 'Test Browser'
        
        log = log_user_action(
            user=self.user,
            action_type='create',
            resource_type='student',
            resource_id='123',
            resource_name='测试学员',
            description='创建学员账户',
            request=request
        )
        
        self.assertEqual(log.user, self.user)
        self.assertEqual(log.action_type, 'create')
        self.assertEqual(log.resource_type, 'student')
        self.assertEqual(log.ip_address, '127.0.0.1')
        self.assertEqual(log.user_agent, 'Test Browser')
        # 验证校区是否正确设置
        user_campus = self.user.campus_memberships.first().campus
        self.assertEqual(log.campus, user_campus)


class SystemLogAPITest(APITestCase):
    """系统日志API测试"""
    
    def setUp(self):
        """设置测试数据"""
        self.campus1 = Campus.objects.create(
            name='校区1',
            code='TEST004',
            address='地址1',
            phone='13800138031'
        )
        
        self.campus2 = Campus.objects.create(
            name='校区2',
            code='TEST005',
            address='地址2',
            phone='13800138032'
        )
        
        self.super_admin = User.objects.create_user(
            username='super_admin',
            password='testpass123',
            real_name='超级管理员',
            phone='13800138030',
            user_type='super_admin'
        )
        
        self.campus_admin1 = User.objects.create_user(
            username='campus_admin1',
            password='testpass123',
            real_name='校区管理员1',
            phone='13800138033',
            user_type='campus_admin'
        )
        
        # 设置校区1管理员
        self.campus1.manager = self.campus_admin1
        self.campus1.save()
        
        self.campus_admin2 = User.objects.create_user(
            username='campus_admin2',
            password='testpass123',
            real_name='校区管理员2',
            phone='13800138034',
            user_type='campus_admin'
        )
        
        # 设置校区2管理员
        self.campus2.manager = self.campus_admin2
        self.campus2.save()
        
        self.student = User.objects.create_user(
            username='student',
            password='testpass123',
            real_name='学员',
            phone='13800138035',
            user_type='student'
        )
        
        # 创建学员和校区1的关联关系
        CampusStudent.objects.create(
            campus=self.campus1,
            student=self.student
        )
        
        # 创建测试日志
        SystemLog.create_log(
            user=self.campus_admin1,
            action_type='create',
            resource_type='student',
            description='校区1管理员创建学员',
            campus=self.campus1
        )
        
        SystemLog.create_log(
            user=self.campus_admin2,
            action_type='update',
            resource_type='campus',
            description='校区2管理员更新校区',
            campus=self.campus2
        )
        
        SystemLog.create_log(
            user=self.student,
            action_type='login',
            resource_type='system',
            description='学员登录',
            campus=self.campus1
        )
    
    def test_super_admin_can_view_all_logs(self):
        """测试超级管理员可以查看所有日志"""
        self.client.force_authenticate(user=self.super_admin)
        
        url = reverse('logs:systemlog-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 3)  # 所有日志
    
    def test_campus_admin_can_only_view_own_campus_logs(self):
        """测试校区管理员只能查看自己校区的日志"""
        self.client.force_authenticate(user=self.campus_admin1)
        
        url = reverse('logs:systemlog-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)  # 只有校区1的日志
        
        # 验证返回的日志都属于校区1
        for log in response.data['results']:
            self.assertEqual(log['campus'], self.campus1.id)
    
    def test_student_can_only_view_own_logs(self):
        """测试学员只能查看自己的日志"""
        self.client.force_authenticate(user=self.student)
        
        url = reverse('logs:systemlog-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)  # 只有自己的日志
        self.assertEqual(response.data['results'][0]['user'], self.student.id)
    
    def test_log_statistics(self):
        """测试日志统计功能"""
        self.client.force_authenticate(user=self.super_admin)
        
        url = reverse('logs:systemlog-statistics')
        response = self.client.get(url, {'days': 7})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('total_count', response.data)
        self.assertIn('action_statistics', response.data)
        self.assertIn('resource_statistics', response.data)
        self.assertEqual(response.data['total_count'], 3)
    
    def test_recent_activities(self):
        """测试最近活动功能"""
        self.client.force_authenticate(user=self.super_admin)
        
        url = reverse('logs:systemlog-recent-activities')
        response = self.client.get(url, {'limit': 5})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertLessEqual(len(response.data), 5)
    
    def test_unauthorized_access(self):
        """测试未授权访问"""
        url = reverse('logs:systemlog-list')
        response = self.client.get(url)
        
        # Django REST framework 默认返回 403 Forbidden 而不是 401 Unauthorized
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class LoginLogAPITest(APITestCase):
    """登录日志API测试"""
    
    def setUp(self):
        """设置测试数据"""
        self.campus = Campus.objects.create(
            name='测试校区',
            code='TEST006',
            address='测试地址',
            phone='13800138040'
        )
        
        self.super_admin = User.objects.create_user(
            username='super_admin2',
            password='testpass123',
            real_name='超级管理员2',
            phone='13800138041',
            user_type='super_admin'
        )
        
        self.campus_admin = User.objects.create_user(
            username='campus_admin3',
            password='testpass123',
            real_name='校区管理员3',
            phone='13800138042',
            user_type='campus_admin'
        )
        
        # 设置校区管理员
        self.campus.manager = self.campus_admin
        self.campus.save()
        
        self.student = User.objects.create_user(
            username='student2',
            password='testpass123',
            real_name='学员2',
            phone='13800138043',
            user_type='student'
        )
        
        # 创建学员和校区的关联关系
        CampusStudent.objects.create(
            campus=self.campus,
            student=self.student
        )
        
        # 创建测试登录日志
        LoginLog.objects.create(
            user=self.campus_admin,
            ip_address='127.0.0.1',
            is_successful=True
        )
        
        LoginLog.objects.create(
            user=self.student,
            ip_address='127.0.0.1',
            is_successful=True
        )
    
    def test_campus_admin_can_view_campus_user_login_logs(self):
        """测试校区管理员可以查看校区用户的登录日志"""
        self.client.force_authenticate(user=self.campus_admin)
        
        url = reverse('logs:loginlog-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)  # 校区管理员和学员的日志
    
    def test_login_statistics(self):
        """测试登录统计功能"""
        self.client.force_authenticate(user=self.super_admin)
        
        url = reverse('logs:loginlog-login-statistics')
        response = self.client.get(url, {'days': 7})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('total_logins', response.data)
        self.assertIn('successful_logins', response.data)
        self.assertIn('failed_logins', response.data)
        self.assertIn('success_rate', response.data)