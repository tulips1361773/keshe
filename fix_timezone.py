#!/usr/bin/env python
"""
修复时区问题的脚本
"""
import os
import sys
import django

# 设置Django环境
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'keshe.settings')
django.setup()

from django.db import connection
from django.conf import settings
from logs.models import LoginLog, SystemLog
from django.utils import timezone
import pytz

def check_mysql_timezone():
    """检查MySQL时区设置"""
    print("=== 检查MySQL时区设置 ===")
    with connection.cursor() as cursor:
        cursor.execute("SELECT @@global.time_zone, @@session.time_zone")
        result = cursor.fetchone()
        print(f"全局时区: {result[0]}")
        print(f"会话时区: {result[1]}")
        
        cursor.execute("SELECT NOW(), UTC_TIMESTAMP()")
        result = cursor.fetchone()
        print(f"当前时间: {result[0]}")
        print(f"UTC时间: {result[1]}")
        
        # 检查系统时区
        cursor.execute("SELECT @@system_time_zone")
        result = cursor.fetchone()
        print(f"系统时区: {result[0]}")

def fix_timezone_issue():
    """修复时区问题"""
    print("\n=== 修复时区问题 ===")
    
    # 设置MySQL会话时区
    with connection.cursor() as cursor:
        try:
            cursor.execute("SET time_zone = '+08:00'")
            print("✅ 设置MySQL会话时区为 +08:00")
        except Exception as e:
            print(f"❌ 设置时区失败: {e}")
            
    # 验证Django时区设置
    print(f"Django USE_TZ: {settings.USE_TZ}")
    print(f"Django TIME_ZONE: {settings.TIME_ZONE}")
    print(f"当前激活时区: {timezone.get_current_timezone()}")

def test_log_queries():
    """测试日志查询"""
    print("\n=== 测试日志查询 ===")
    
    try:
        # 测试登录日志查询
        login_logs = LoginLog.objects.all()[:5]
        print(f"登录日志查询成功，前5条记录:")
        for log in login_logs:
            print(f"  ID: {log.id}, 用户: {log.user.username}, 时间: {log.login_time}")
    except Exception as e:
        print(f"❌ 登录日志查询失败: {e}")
        
    try:
        # 测试系统日志查询
        system_logs = SystemLog.objects.all()[:5]
        print(f"系统日志查询成功，前5条记录:")
        for log in system_logs:
            print(f"  ID: {log.id}, 用户: {log.user.username}, 时间: {log.created_at}")
    except Exception as e:
        print(f"❌ 系统日志查询失败: {e}")

if __name__ == "__main__":
    print("开始修复时区问题...")
    check_mysql_timezone()
    fix_timezone_issue()
    test_log_queries()
    print("\n✅ 时区问题修复完成")