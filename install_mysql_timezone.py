#!/usr/bin/env python
"""
安装MySQL时区数据的脚本
"""
import os
import sys
import django
from django.db import connection
from django.conf import settings

# 设置Django环境
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'keshe.settings')
django.setup()

def install_basic_timezone_data():
    """安装基本的时区数据"""
    print("=== 安装基本时区数据 ===")
    
    timezone_data = [
        # 时区名称数据
        ("INSERT IGNORE INTO mysql.time_zone_name (Name, Time_zone_id) VALUES "
         "('UTC', 1), ('Asia/Shanghai', 2), ('GMT', 1), ('CST', 2)"),
        
        # 时区数据
        ("INSERT IGNORE INTO mysql.time_zone (Time_zone_id, Use_leap_seconds) VALUES "
         "(1, 'N'), (2, 'N')"),
        
        # 时区转换数据 - UTC
        ("INSERT IGNORE INTO mysql.time_zone_transition_type "
         "(Time_zone_id, Transition_type_id, Offset, Is_DST, Abbreviation) VALUES "
         "(1, 0, 0, 'N', 'UTC')"),
        
        # 时区转换数据 - Asia/Shanghai (+8小时)
        ("INSERT IGNORE INTO mysql.time_zone_transition_type "
         "(Time_zone_id, Transition_type_id, Offset, Is_DST, Abbreviation) VALUES "
         "(2, 0, 28800, 'N', 'CST')"),
    ]
    
    with connection.cursor() as cursor:
        try:
            for sql in timezone_data:
                cursor.execute(sql)
                print(f"✅ 执行: {sql[:50]}...")
            
            # 提交事务
            connection.commit()
            print("✅ 基本时区数据安装完成")
            return True
            
        except Exception as e:
            print(f"❌ 安装时区数据失败: {e}")
            connection.rollback()
            return False

def verify_timezone_installation():
    """验证时区安装"""
    print("\n=== 验证时区安装 ===")
    
    with connection.cursor() as cursor:
        try:
            # 检查时区名称表
            cursor.execute("SELECT COUNT(*) FROM mysql.time_zone_name")
            count = cursor.fetchone()[0]
            print(f"时区名称表记录数: {count}")
            
            # 测试时区转换
            cursor.execute("SELECT CONVERT_TZ('2025-09-22 12:00:00', 'UTC', 'Asia/Shanghai')")
            result = cursor.fetchone()[0]
            print(f"时区转换测试: UTC 12:00 -> Asia/Shanghai {result}")
            
            if result is not None:
                print("✅ 时区转换功能正常")
                return True
            else:
                print("❌ 时区转换仍然失败")
                return False
                
        except Exception as e:
            print(f"❌ 验证失败: {e}")
            return False

def set_mysql_timezone():
    """设置MySQL时区"""
    print("\n=== 设置MySQL时区 ===")
    
    with connection.cursor() as cursor:
        try:
            # 设置全局时区（需要SUPER权限）
            try:
                cursor.execute("SET GLOBAL time_zone = '+08:00'")
                print("✅ 设置全局时区为 +08:00")
            except Exception as e:
                print(f"⚠️  设置全局时区失败（可能需要SUPER权限）: {e}")
            
            # 设置会话时区
            cursor.execute("SET time_zone = '+08:00'")
            print("✅ 设置会话时区为 +08:00")
            
            # 验证设置
            cursor.execute("SELECT @@time_zone")
            tz = cursor.fetchone()[0]
            print(f"当前时区设置: {tz}")
            
        except Exception as e:
            print(f"❌ 设置时区失败: {e}")

if __name__ == "__main__":
    print("开始安装MySQL时区数据...")
    
    # 安装基本时区数据
    install_success = install_basic_timezone_data()
    
    if install_success:
        # 验证安装
        verify_success = verify_timezone_installation()
        
        if verify_success:
            print("\n✅ MySQL时区数据安装成功")
        else:
            print("\n❌ 时区数据安装可能不完整")
    
    # 设置时区
    set_mysql_timezone()
    
    print("\n完成安装过程")