#!/usr/bin/env python
"""
分析系统日志中用户信息的准确性和分布情况
"""

import os
import sys
import django
from datetime import datetime, timedelta
from collections import Counter

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'keshe.settings')
django.setup()

from django.contrib.auth import get_user_model
from logs.models import SystemLog, LoginLog

User = get_user_model()

def analyze_user_logs():
    """分析用户日志的详细情况"""
    print("=" * 70)
    print("系统日志用户信息准确性分析")
    print("=" * 70)
    
    # 1. 总体统计
    total_system_logs = SystemLog.objects.count()
    total_login_logs = LoginLog.objects.count()
    total_users = User.objects.count()
    
    print(f"\n1. 总体统计:")
    print(f"   系统日志总数: {total_system_logs}")
    print(f"   登录日志总数: {total_login_logs}")
    print(f"   用户总数: {total_users}")
    
    # 2. 按用户类型分析系统日志
    print(f"\n2. 按用户类型分析系统日志:")
    
    user_type_stats = {}
    for user_type, user_type_name in User.USER_TYPE_CHOICES:
        users_of_type = User.objects.filter(user_type=user_type)
        logs_of_type = SystemLog.objects.filter(user__user_type=user_type).count()
        user_type_stats[user_type] = {
            'name': user_type_name,
            'user_count': users_of_type.count(),
            'log_count': logs_of_type,
            'avg_logs_per_user': logs_of_type / max(1, users_of_type.count())
        }
        print(f"   {user_type_name}:")
        print(f"     用户数量: {user_type_stats[user_type]['user_count']}")
        print(f"     日志数量: {user_type_stats[user_type]['log_count']}")
        print(f"     平均每用户日志数: {user_type_stats[user_type]['avg_logs_per_user']:.1f}")
    
    # 3. 按具体用户分析
    print(f"\n3. 按具体用户分析 (前10名活跃用户):")
    user_log_counts = SystemLog.objects.values('user__username', 'user__first_name', 'user__user_type').annotate(
        log_count=models.Count('id')
    ).order_by('-log_count')[:10]
    
    for i, user_stat in enumerate(user_log_counts, 1):
        username = user_stat['user__username']
        first_name = user_stat['user__first_name'] or '未设置'
        user_type = user_stat['user__user_type']
        log_count = user_stat['log_count']
        
        # 获取用户类型中文名
        user_type_name = dict(User.USER_TYPE_CHOICES).get(user_type, user_type)
        
        print(f"   {i:2d}. {username} ({first_name}) - {user_type_name}: {log_count} 条日志")
    
    # 4. 操作类型分析
    print(f"\n4. 操作类型分析:")
    action_stats = SystemLog.objects.values('action_type').annotate(
        count=models.Count('id')
    ).order_by('-count')
    
    for action_stat in action_stats:
        action_type = action_stat['action_type']
        count = action_stat['count']
        action_name = dict(SystemLog.ACTION_TYPE_CHOICES).get(action_type, action_type)
        percentage = (count / total_system_logs) * 100
        print(f"   {action_name}: {count} 条 ({percentage:.1f}%)")
    
    # 5. 资源类型分析
    print(f"\n5. 资源类型分析:")
    resource_stats = SystemLog.objects.values('resource_type').annotate(
        count=models.Count('id')
    ).order_by('-count')
    
    for resource_stat in resource_stats:
        resource_type = resource_stat['resource_type']
        count = resource_stat['count']
        resource_name = dict(SystemLog.RESOURCE_TYPE_CHOICES).get(resource_type, resource_type)
        percentage = (count / total_system_logs) * 100
        print(f"   {resource_name}: {count} 条 ({percentage:.1f}%)")
    
    # 6. 时间分布分析
    print(f"\n6. 时间分布分析 (最近7天):")
    now = datetime.now()
    for i in range(7):
        date = now - timedelta(days=i)
        start_of_day = date.replace(hour=0, minute=0, second=0, microsecond=0)
        end_of_day = date.replace(hour=23, minute=59, second=59, microsecond=999999)
        
        daily_logs = SystemLog.objects.filter(
            created_at__range=[start_of_day, end_of_day]
        ).count()
        
        print(f"   {date.strftime('%Y-%m-%d')}: {daily_logs} 条日志")
    
    # 7. 验证日志记录的完整性
    print(f"\n7. 日志记录完整性验证:")
    
    # 检查是否有用户为空的日志
    null_user_logs = SystemLog.objects.filter(user__isnull=True).count()
    print(f"   用户为空的日志: {null_user_logs} 条")
    
    # 检查是否有描述为空的日志
    empty_description_logs = SystemLog.objects.filter(description__isnull=True).count() + \
                           SystemLog.objects.filter(description='').count()
    print(f"   描述为空的日志: {empty_description_logs} 条")
    
    # 检查最近的日志是否正确记录了用户信息
    recent_logs = SystemLog.objects.select_related('user').order_by('-created_at')[:20]
    correct_user_info = 0
    
    for log in recent_logs:
        if log.user and log.user.username:
            correct_user_info += 1
    
    accuracy_rate = (correct_user_info / len(recent_logs)) * 100 if recent_logs else 0
    print(f"   最近20条日志用户信息准确率: {accuracy_rate:.1f}%")
    
    # 8. 非admin用户活跃度分析
    print(f"\n8. 非admin用户活跃度分析:")
    
    non_admin_users = User.objects.exclude(username='admin')
    active_non_admin_users = non_admin_users.filter(operation_logs__isnull=False).distinct()
    
    print(f"   非admin用户总数: {non_admin_users.count()}")
    print(f"   有日志记录的非admin用户: {active_non_admin_users.count()}")
    
    if non_admin_users.count() > 0:
        activity_rate = (active_non_admin_users.count() / non_admin_users.count()) * 100
        print(f"   非admin用户活跃率: {activity_rate:.1f}%")
    
    # 9. 最新的非admin用户操作
    print(f"\n9. 最新的非admin用户操作 (最近10条):")
    recent_non_admin_logs = SystemLog.objects.exclude(user__username='admin').select_related('user').order_by('-created_at')[:10]
    
    for log in recent_non_admin_logs:
        user_info = f"{log.user.username} ({log.user.first_name or '未设置'})" if log.user else "未知用户"
        user_type = dict(User.USER_TYPE_CHOICES).get(log.user.user_type, log.user.user_type) if log.user else "未知"
        action_name = dict(SystemLog.ACTION_TYPE_CHOICES).get(log.action_type, log.action_type)
        resource_name = dict(SystemLog.RESOURCE_TYPE_CHOICES).get(log.resource_type, log.resource_type)
        
        print(f"   [{log.created_at.strftime('%m-%d %H:%M')}] {user_info} ({user_type}) - {action_name} {resource_name}")
    
    print("\n" + "=" * 70)
    print("分析完成！")
    print("=" * 70)
    
    return {
        'total_logs': total_system_logs,
        'user_type_stats': user_type_stats,
        'null_user_logs': null_user_logs,
        'accuracy_rate': accuracy_rate,
        'non_admin_activity_rate': activity_rate if non_admin_users.count() > 0 else 0
    }

if __name__ == '__main__':
    from django.db import models  # 需要在这里导入models
    result = analyze_user_logs()
    
    print(f"\n关键指标摘要:")
    print(f"- 总日志数: {result['total_logs']}")
    print(f"- 用户信息准确率: {result['accuracy_rate']:.1f}%")
    print(f"- 非admin用户活跃率: {result['non_admin_activity_rate']:.1f}%")
    print(f"- 用户为空的日志: {result['null_user_logs']} 条")