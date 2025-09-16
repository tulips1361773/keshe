#!/usr/bin/env python
import os
import sys
import django

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'keshe.settings')
django.setup()

from django.db import connection

def check_coach_change_table():
    """检查CoachChangeRequest表结构"""
    cursor = connection.cursor()
    
    try:
        # 检查表是否存在
        cursor.execute("SHOW TABLES LIKE 'reservations_coach_change_request'")
        table_exists = cursor.fetchone()
        
        if not table_exists:
            print("❌ 表 'reservations_coach_change_request' 不存在")
            return
        
        print("✅ 表 'reservations_coach_change_request' 存在")
        
        # 获取表结构
        cursor.execute("DESCRIBE reservations_coach_change_request")
        columns = cursor.fetchall()
        
        print("\n📋 表结构:")
        for column in columns:
            print(f"  - {column[0]} ({column[1]})")
        
        # 检查是否有target_coach_id字段
        column_names = [col[0] for col in columns]
        if 'target_coach_id' in column_names:
            print("\n✅ target_coach_id 字段存在")
        else:
            print("\n❌ target_coach_id 字段不存在")
            
        # 检查其他关键字段
        required_fields = ['student_id', 'current_coach_id', 'target_coach_id', 'reason', 'status']
        missing_fields = [field for field in required_fields if field not in column_names]
        
        if missing_fields:
            print(f"\n❌ 缺少字段: {missing_fields}")
        else:
            print("\n✅ 所有必需字段都存在")
            
    except Exception as e:
        print(f"❌ 检查表结构时出错: {e}")
    finally:
        cursor.close()

if __name__ == '__main__':
    check_coach_change_table()