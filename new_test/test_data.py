# -*- coding: utf-8 -*-
"""
乒乓球培训管理系统 - 测试数据管理

功能：
- 测试数据创建：创建各种测试用的模型实例
- 测试数据清理：清理测试后的数据
- 测试数据工厂：批量生成测试数据
- 测试数据验证：验证测试数据的完整性
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from decimal import Decimal
from datetime import datetime, timedelta
import random
import string

# 导入模型
from accounts.models import User, UserProfile, Coach
from campus.models import Campus, CampusArea
from reservations.models import CoachStudentRelation, Table, Booking, CoachChangeRequest
from payments.models import UserAccount, AccountTransaction, Payment
from competitions.models import Competition, CompetitionRegistration
from notifications.models import Notification
from logs.models import SystemLog

User = get_user_model()


class TestDataManager:
    """测试数据管理器"""
    
    def __init__(self):
        """初始化测试数据管理器"""
        self.created_objects = {
            'users': [],
            'campuses': [],
            'tables': [],
            'bookings': [],
            'accounts': [],
            'transactions': [],
            'notifications': [],
            'logs': [],
            'relations': [],
            'competitions': []
        }
    
    def generate_random_string(self, length=8):
        """生成随机字符串"""
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in range(length))
    
    def generate_random_phone(self):
        """生成随机手机号"""
        return f"138{random.randint(10000000, 99999999)}"
    
    def create_test_campus(self, name=None, **kwargs):
        """创建测试校区"""
        if name is None:
            name = f"测试校区_{self.generate_random_string(4)}"
        
        # 检查是否已存在同名校区
        existing_campus = Campus.objects.filter(name=name).first()
        if existing_campus:
            safe_print(f"校区已存在: {existing_campus.name}", "pass")
            return existing_campus
        
        # 生成唯一的校区编码
        code = kwargs.get('code', f"TEST_{self.generate_random_string(4).upper()}")
        while Campus.objects.filter(code=code).exists():
            code = f"TEST_{self.generate_random_string(4).upper()}"
        
        campus_data = {
            'name': name,
            'code': code,
            'address': kwargs.get('address', f'测试地址{random.randint(1, 999)}号'),
            'phone': kwargs.get('phone', self.generate_random_phone()),
            'description': kwargs.get('description', '这是一个测试校区'),
            'is_active': kwargs.get('is_active', True)
        }
        
        campus = Campus.objects.create(**campus_data)
        self.created_objects['campuses'].append(campus)
        
        safe_print(f"创建测试校区: {campus.name} (编码: {campus.code})", "pass")
        return campus
    
    def create_test_user(self, user_type='student', campus=None, **kwargs):
        """创建测试用户"""
        username = kwargs.get('username', f'test_{user_type}_{self.generate_random_string(6)}')
        
        # 检查用户名是否已存在，如果存在则生成新的用户名
        while User.objects.filter(username=username).exists():
            username = f'test_{user_type}_{self.generate_random_string(8)}'
        
        user_data = {
            'username': username,
            'password': kwargs.get('password', 'test123456'),
            'user_type': user_type,
            'real_name': kwargs.get('real_name', f'测试{user_type}_{self.generate_random_string(3)}'),
            'phone': kwargs.get('phone', self.generate_random_phone()),
            'email': kwargs.get('email', f'{username}@test.com'),
            'is_active': kwargs.get('is_active', True)
        }
        
        if user_type == 'admin':
            user_data['is_staff'] = True
            user_data['is_superuser'] = kwargs.get('is_superuser', False)
        
        user = User.objects.create_user(**user_data)
        self.created_objects['users'].append(user)
        
        # 如果指定了校区，创建校区关联关系
        if campus:
            if user_type == 'student':
                from campus.models import CampusStudent
                CampusStudent.objects.create(campus=campus, student=user)
            elif user_type == 'coach':
                from campus.models import CampusCoach
                CampusCoach.objects.create(campus=campus, coach=user)
        
        safe_print(f"创建测试用户: {user.username} ({user_type})", "pass")
        return user
    
    def create_test_table(self, campus=None, **kwargs):
        """创建测试球台"""
        if campus is None:
            campus = self.create_test_campus()
        
        # 生成唯一的球台编号
        number = kwargs.get('number', str(random.randint(1, 20)))
        while Table.objects.filter(campus=campus, number=number).exists():
            number = str(random.randint(1, 999))
        
        table_data = {
            'number': number,
            'name': kwargs.get('name', f'{number}号台'),
            'campus': campus,
            'status': kwargs.get('status', 'available'),
            'is_active': kwargs.get('is_active', True),
            'description': kwargs.get('description', '测试球台')
        }
        
        table = Table.objects.create(**table_data)
        self.created_objects['tables'].append(table)
        
        safe_print(f"创建测试球台: {table.name}", "pass")
        return table
    
    def create_test_coach_student_relation(self, student=None, coach=None, **kwargs):
        """创建测试师生关系"""
        if student is None:
            student = self.create_test_user('student')
        if coach is None:
            coach = self.create_test_user('coach', campus=student.campus)
        
        relation_data = {
            'student': student,
            'coach': coach,
            'status': kwargs.get('status', 'approved'),
            'applied_by': kwargs.get('applied_by', 'student'),
            'notes': kwargs.get('notes', '测试师生关系')
        }
        
        relation = CoachStudentRelation.objects.create(**relation_data)
        self.created_objects['relations'].append(relation)
        
        safe_print(f"创建师生关系: {student.real_name} - {coach.real_name}", "pass")
        return relation
    
    def create_test_booking(self, student=None, coach=None, table=None, **kwargs):
        """创建测试预约"""
        if student is None:
            student = self.create_test_user('student')
        if coach is None:
            coach = self.create_test_user('coach', campus=student.campus)
        if table is None:
            table = self.create_test_table(campus=student.campus)
        
        # 确保师生关系存在
        relation, created = CoachStudentRelation.objects.get_or_create(
            student=student,
            coach=coach,
            defaults={'status': 'active'}
        )
        if created:
            self.created_objects['relations'].append(relation)
        
        # 设置预约时间
        start_time = kwargs.get('start_time', timezone.now() + timedelta(days=random.randint(1, 7)))
        end_time = kwargs.get('end_time', start_time + timedelta(hours=random.randint(1, 3)))
        duration_hours = (end_time - start_time).total_seconds() / 3600
        
        booking_data = {
            'relation': relation,
            'table': table,
            'start_time': start_time,
            'end_time': end_time,
            'duration_hours': duration_hours,
            'total_fee': kwargs.get('total_fee', duration_hours * 100),  # 默认每小时100元
            'status': kwargs.get('status', 'confirmed'),
            'notes': kwargs.get('notes', '测试预约'),
            'payment_status': kwargs.get('payment_status', 'pending')
        }
        
        booking = Booking.objects.create(**booking_data)
        self.created_objects['bookings'].append(booking)
        
        safe_print(f"创建测试预约: {student.real_name} - {coach.real_name} ({start_time.strftime('%Y-%m-%d %H:%M')})", "pass")
        return booking
    
    def create_test_user_account(self, user=None, **kwargs):
        """创建测试用户账户"""
        if user is None:
            user = self.create_test_user('student')
        
        account_data = {
            'user': user,
            'balance': kwargs.get('balance', Decimal(str(random.randint(0, 1000))))
        }
        
        account = UserAccount.objects.create(**account_data)
        self.created_objects['accounts'].append(account)
        
        safe_print(f"创建测试账户: {user.real_name} (余额: {account.balance})", "pass")
        return account
    
    def create_test_transaction(self, account=None, **kwargs):
        """创建测试交易记录"""
        if account is None:
            user = self.create_test_user('student')
            account = self.create_test_user_account(user)
        
        transaction_types = ['recharge', 'payment', 'refund', 'freeze', 'unfreeze', 'adjustment']
        
        # 获取当前余额作为交易前余额
        balance_before = account.balance
        amount = kwargs.get('amount', Decimal(str(random.randint(1, 500))))
        
        # 根据交易类型计算交易后余额
        if kwargs.get('transaction_type', random.choice(transaction_types)) in ['recharge', 'refund', 'unfreeze']:
            balance_after = balance_before + amount
        else:
            balance_after = balance_before - amount
        
        transaction_data = {
            'account': account,
            'transaction_type': kwargs.get('transaction_type', random.choice(transaction_types)),
            'amount': amount,
            'balance_before': balance_before,
            'balance_after': balance_after,
            'description': kwargs.get('description', '测试交易')
        }
        
        transaction = AccountTransaction.objects.create(**transaction_data)
        self.created_objects['transactions'].append(transaction)
        
        safe_print(f"创建测试交易: {transaction.transaction_type} {transaction.amount}", "pass")
        return transaction
    
    def create_test_notification(self, recipient=None, **kwargs):
        """创建测试通知"""
        if recipient is None:
            recipient = self.create_test_user('student')
        
        message_types = ['system', 'booking', 'payment', 'competition']
        
        notification_data = {
            'recipient': recipient,
            'title': kwargs.get('title', f'测试通知_{self.generate_random_string(4)}'),
            'message': kwargs.get('message', '这是一条测试通知消息'),
            'message_type': kwargs.get('message_type', random.choice(message_types)),
            'is_read': kwargs.get('is_read', False)
        }
        
        notification = Notification.objects.create(**notification_data)
        self.created_objects['notifications'].append(notification)
        
        safe_print(f"创建测试通知: {notification.title}", "pass")
        return notification
    
    def create_test_system_log(self, user=None, **kwargs):
        """创建测试系统日志"""
        if user is None:
            user = self.create_test_user('student')
        
        action_types = ['login', 'logout', 'create', 'update', 'delete', 'view']
        resource_types = ['user', 'booking', 'payment', 'notification']
        
        log_data = {
            'user': user,
            'action_type': kwargs.get('action_type', random.choice(action_types)),
            'resource_type': kwargs.get('resource_type', random.choice(resource_types)),
            'resource_id': kwargs.get('resource_id', str(random.randint(1, 1000))),
            'description': kwargs.get('description', '测试系统日志'),
            'ip_address': kwargs.get('ip_address', f'192.168.1.{random.randint(1, 254)}')
        }
        
        log = SystemLog.objects.create(**log_data)
        self.created_objects['logs'].append(log)
        
        safe_print(f"创建测试日志: {log.action_type} - {log.resource_type}", "pass")
        return log
    
    def create_test_competition(self, **kwargs):
        """创建测试比赛"""
        # 获取或创建一个校区
        campus = kwargs.get('campus')
        if not campus:
            campus = self.create_test_campus("测试校区")
        
        # 获取或创建一个创建者
        created_by = kwargs.get('created_by')
        if not created_by:
            created_by = self.create_test_user('admin')
        
        # 设置时间
        now = timezone.now()
        registration_start = kwargs.get('registration_start', now + timedelta(days=1))
        registration_end = kwargs.get('registration_end', now + timedelta(days=7))
        competition_date = kwargs.get('competition_date', now + timedelta(days=14))
        
        competition_data = {
            'title': kwargs.get('title', f'测试比赛_{self.generate_random_string(4)}'),
            'name': kwargs.get('name', f'测试比赛_{self.generate_random_string(4)}'),
            'description': kwargs.get('description', '这是一个测试比赛'),
            'campus': campus,
            'created_by': created_by,
            'competition_date': competition_date,
            'registration_start': registration_start,
            'registration_end': registration_end,
            'registration_fee': kwargs.get('registration_fee', Decimal(str(random.randint(0, 200)))),
            'max_participants_per_group': kwargs.get('max_participants_per_group', random.randint(10, 20)),
            'status': kwargs.get('status', 'upcoming')
        }
        
        competition = Competition.objects.create(**competition_data)
        self.created_objects['competitions'].append(competition)
        
        safe_print(f"创建测试比赛: {competition.title}", "pass")
        return competition
    
    def create_complete_test_scenario(self):
        """创建完整的测试场景"""
        safe_print("开始创建完整测试场景", "test")
        
        # 创建校区
        campus1 = self.create_test_campus("主校区")
        campus2 = self.create_test_campus("分校区")
        
        # 创建用户
        admin = self.create_test_user('admin', campus1, username='test_admin')
        
        students = []
        coaches = []
        
        for i in range(5):
            student = self.create_test_user('student', campus1, username=f'test_student_{i+1}')
            students.append(student)
            
        for i in range(3):
            coach = self.create_test_user('coach', campus1, username=f'test_coach_{i+1}')
            coaches.append(coach)
        
        # 创建球台
        tables = []
        for i in range(6):
            table = self.create_test_table(campus1, name=f'{i+1}号台')
            tables.append(table)
        
        # 创建师生关系
        relations = []
        for i, student in enumerate(students):
            coach = coaches[i % len(coaches)]
            relation = self.create_test_coach_student_relation(student, coach)
            relations.append(relation)
        
        # 创建用户账户和交易
        for student in students:
            account = self.create_test_user_account(student, balance=Decimal('500.00'))
            
            # 创建一些交易记录
            for j in range(3):
                self.create_test_transaction(account)
        
        # 创建预约
        for i in range(10):
            student = random.choice(students)
            # 找到该学员的教练
            relation = CoachStudentRelation.objects.filter(student=student, status='active').first()
            if relation:
                coach = relation.coach
                table = random.choice(tables)
                self.create_test_booking(student, coach, table)
        
        # 创建通知
        for student in students:
            for j in range(2):
                self.create_test_notification(student)
        
        # 创建系统日志
        all_users = [admin] + students + coaches
        for user in all_users:
            for j in range(3):
                self.create_test_system_log(user)
        
        # 创建比赛
        for i in range(2):
            self.create_test_competition()
        
        safe_print("完整测试场景创建完成", "pass")
        return {
            'campus': [campus1, campus2],
            'admin': admin,
            'students': students,
            'coaches': coaches,
            'tables': tables,
            'relations': relations
        }
    
    def cleanup_test_data(self):
        """清理测试数据"""
        safe_print("开始清理测试数据", "test")
        
        cleanup_count = 0
        
        # 按依赖关系顺序删除
        for booking in self.created_objects['bookings']:
            try:
                booking.delete()
                cleanup_count += 1
            except Exception as e:
                safe_print(f"删除预约失败: {str(e)}", "fail")
        
        for transaction in self.created_objects['transactions']:
            try:
                transaction.delete()
                cleanup_count += 1
            except Exception as e:
                safe_print(f"删除交易记录失败: {str(e)}", "fail")
        
        for account in self.created_objects['accounts']:
            try:
                account.delete()
                cleanup_count += 1
            except Exception as e:
                safe_print(f"删除账户失败: {str(e)}", "fail")
        
        for notification in self.created_objects['notifications']:
            try:
                notification.delete()
                cleanup_count += 1
            except Exception as e:
                safe_print(f"删除通知失败: {str(e)}", "fail")
        
        for log in self.created_objects['logs']:
            try:
                log.delete()
                cleanup_count += 1
            except Exception as e:
                safe_print(f"删除日志失败: {str(e)}", "fail")
        
        for relation in self.created_objects['relations']:
            try:
                relation.delete()
                cleanup_count += 1
            except Exception as e:
                safe_print(f"删除师生关系失败: {str(e)}", "fail")
        
        for competition in self.created_objects['competitions']:
            try:
                competition.delete()
                cleanup_count += 1
            except Exception as e:
                safe_print(f"删除比赛失败: {str(e)}", "fail")
        
        for table in self.created_objects['tables']:
            try:
                table.delete()
                cleanup_count += 1
            except Exception as e:
                safe_print(f"删除球台失败: {str(e)}", "fail")
        
        for user in self.created_objects['users']:
            try:
                user.delete()
                cleanup_count += 1
            except Exception as e:
                safe_print(f"删除用户失败: {str(e)}", "fail")
        
        for campus in self.created_objects['campuses']:
            try:
                campus.delete()
                cleanup_count += 1
            except Exception as e:
                safe_print(f"删除校区失败: {str(e)}", "fail")
        
        safe_print(f"测试数据清理完成，共清理 {cleanup_count} 个对象", "pass")
        
        # 重置创建对象记录
        for key in self.created_objects:
            self.created_objects[key] = []
    
    def validate_test_data(self):
        """验证测试数据完整性"""
        safe_print("开始验证测试数据完整性", "test")
        
        validation_results = {
            'users': 0,
            'campuses': 0,
            'tables': 0,
            'bookings': 0,
            'accounts': 0,
            'transactions': 0,
            'notifications': 0,
            'logs': 0,
            'relations': 0,
            'competitions': 0
        }
        
        # 统计各类对象数量
        validation_results['users'] = User.objects.count()
        validation_results['campuses'] = Campus.objects.count()
        validation_results['tables'] = Table.objects.count()
        validation_results['bookings'] = Booking.objects.count()
        validation_results['accounts'] = UserAccount.objects.count()
        validation_results['transactions'] = AccountTransaction.objects.count()
        validation_results['notifications'] = Notification.objects.count()
        validation_results['logs'] = SystemLog.objects.count()
        validation_results['relations'] = CoachStudentRelation.objects.count()
        validation_results['competitions'] = Competition.objects.count()
        
        safe_print("数据统计结果:", "test")
        for key, count in validation_results.items():
            safe_print(f"- {key}: {count} 个")
        
        # 验证数据关系完整性
        integrity_issues = []
        
        # 检查用户是否都有校区
        users_without_campus = User.objects.filter(campus__isnull=True).count()
        if users_without_campus > 0:
            integrity_issues.append(f"{users_without_campus} 个用户没有关联校区")
        
        # 检查预约是否都有有效的师生关系
        bookings_without_relation = 0
        for booking in Booking.objects.all():
            if not CoachStudentRelation.objects.filter(
                student=booking.student,
                coach=booking.coach,
                status='active'
            ).exists():
                bookings_without_relation += 1
        
        if bookings_without_relation > 0:
            integrity_issues.append(f"{bookings_without_relation} 个预约没有有效的师生关系")
        
        if integrity_issues:
            safe_print("发现数据完整性问题:", "fail")
            for issue in integrity_issues:
                safe_print(f"- {issue}", "fail")
        else:
            safe_print("数据完整性验证通过", "pass")
        
        return validation_results, integrity_issues


class TestDataFactory:
    """测试数据工厂"""
    
    @staticmethod
    def create_batch_users(count=10, user_type='student', campus=None):
        """批量创建用户"""
        manager = TestDataManager()
        if campus is None:
            campus = manager.create_test_campus()
        
        users = []
        for i in range(count):
            user = manager.create_test_user(user_type, campus)
            users.append(user)
        
        safe_print(f"批量创建 {count} 个 {user_type} 用户", "pass")
        return users
    
    @staticmethod
    def create_batch_bookings(count=20, students=None, coaches=None, tables=None):
        """批量创建预约"""
        manager = TestDataManager()
        
        if students is None:
            students = TestDataFactory.create_batch_users(5, 'student')
        if coaches is None:
            coaches = TestDataFactory.create_batch_users(3, 'coach', students[0].campus)
        if tables is None:
            tables = []
            for i in range(6):
                table = manager.create_test_table(students[0].campus)
                tables.append(table)
        
        bookings = []
        for i in range(count):
            student = random.choice(students)
            coach = random.choice(coaches)
            table = random.choice(tables)
            
            # 确保师生关系存在
            relation, created = CoachStudentRelation.objects.get_or_create(
                student=student,
                coach=coach,
                defaults={'status': 'active'}
            )
            
            booking = manager.create_test_booking(student, coach, table)
            bookings.append(booking)
        
        safe_print(f"批量创建 {count} 个预约", "pass")
        return bookings


def safe_print(message, status=None):
    """安全的打印函数，避免Unicode编码错误"""
    if status == 'pass':
        print(f"[PASS] {message}")
    elif status == 'fail':
        print(f"[FAIL] {message}")
    elif status == 'test':
        print(f"[TEST] {message}")
    else:
        print(message)


# 全局测试数据管理器实例
test_data_manager = TestDataManager()


# 测试运行时的输出
if __name__ == '__main__':
    safe_print("测试数据管理模块加载完成", "test")
    safe_print("包含以下功能:", "test")
    safe_print("- TestDataManager: 测试数据管理器")
    safe_print("- TestDataFactory: 测试数据工厂")
    safe_print("- 支持创建完整测试场景")
    safe_print("- 支持批量数据创建和清理")
    safe_print("- 支持数据完整性验证")