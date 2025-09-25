from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
import random

from accounts.models import User
from campus.models import Campus, CampusStudent, CampusCoach
from logs.models import SystemLog, LoginLog


class Command(BaseCommand):
    help = '创建演示日志数据'

    def add_arguments(self, parser):
        parser.add_argument(
            '--days',
            type=int,
            default=30,
            help='生成多少天的日志数据（默认30天）'
        )
        parser.add_argument(
            '--logs-per-day',
            type=int,
            default=10,
            help='每天生成多少条日志（默认10条）'
        )

    def handle(self, *args, **options):
        days = options['days']
        logs_per_day = options['logs_per_day']
        
        self.stdout.write(f'开始创建 {days} 天的演示日志数据，每天 {logs_per_day} 条...')
        
        # 获取现有用户和校区
        users = list(User.objects.all())
        campuses = list(Campus.objects.all())
        
        if not users:
            self.stdout.write(self.style.ERROR('没有找到用户，请先创建用户数据'))
            return
            
        if not campuses:
            self.stdout.write(self.style.ERROR('没有找到校区，请先创建校区数据'))
            return
        
        # 定义操作类型和资源类型
        action_types = ['CREATE', 'UPDATE', 'DELETE', 'VIEW', 'LOGIN', 'LOGOUT']
        resource_types = ['USER', 'CAMPUS', 'COURSE', 'SCHEDULE', 'SYSTEM']
        
        # 生成系统日志
        system_logs_created = 0
        for day in range(days):
            date = timezone.now() - timedelta(days=day)
            
            for _ in range(logs_per_day):
                user = random.choice(users)
                action_type = random.choice(action_types)
                resource_type = random.choice(resource_types)
                
                # 根据用户类型确定校区
                campus = None
                if user.is_campus_admin:
                    managed_campuses = user.managed_campus.all()
                    if managed_campuses:
                        campus = random.choice(list(managed_campuses))
                elif hasattr(user, 'campus_memberships'):
                    memberships = user.campus_memberships.filter(is_active=True)
                    if memberships:
                        campus = random.choice(list(memberships)).campus
                elif hasattr(user, 'campus_assignments'):
                    assignments = user.campus_assignments.filter(is_active=True)
                    if assignments:
                        campus = random.choice(list(assignments)).campus
                
                if not campus and campuses:
                    campus = random.choice(campuses)
                
                # 生成描述
                descriptions = {
                    'CREATE': f'创建了新的{resource_type.lower()}',
                    'UPDATE': f'更新了{resource_type.lower()}信息',
                    'DELETE': f'删除了{resource_type.lower()}',
                    'VIEW': f'查看了{resource_type.lower()}列表',
                    'LOGIN': '登录系统',
                    'LOGOUT': '退出系统',
                }
                
                SystemLog.objects.create(
                    user=user,
                    campus=campus,
                    action_type=action_type,
                    resource_type=resource_type,
                    description=descriptions.get(action_type, f'执行了{action_type}操作'),
                    ip_address=f'192.168.1.{random.randint(1, 254)}',
                    user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                    created_at=date - timedelta(
                        hours=random.randint(0, 23),
                        minutes=random.randint(0, 59)
                    )
                )
                system_logs_created += 1
        
        # 生成登录日志
        login_logs_created = 0
        for day in range(days):
            date = timezone.now() - timedelta(days=day)
            
            # 每天随机选择一些用户登录
            daily_users = random.sample(users, min(len(users), random.randint(3, 8)))
            
            for user in daily_users:
                login_time = date - timedelta(
                    hours=random.randint(8, 18),
                    minutes=random.randint(0, 59)
                )
                
                # 90% 的登录是成功的
                is_successful = random.random() < 0.9
                
                login_log = LoginLog.objects.create(
                    user=user,
                    ip_address=f'192.168.1.{random.randint(1, 254)}',
                    user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                    login_time=login_time,
                    is_successful=is_successful
                )
                
                # 如果登录成功，添加登出时间
                if is_successful and random.random() < 0.8:  # 80% 的成功登录会有登出记录
                    logout_time = login_time + timedelta(
                        hours=random.randint(1, 8),
                        minutes=random.randint(0, 59)
                    )
                    login_log.logout_time = logout_time
                    login_log.save()
                
                login_logs_created += 1
        
        self.stdout.write(
            self.style.SUCCESS(
                f'成功创建演示数据：\n'
                f'- 系统日志：{system_logs_created} 条\n'
                f'- 登录日志：{login_logs_created} 条'
            )
        )