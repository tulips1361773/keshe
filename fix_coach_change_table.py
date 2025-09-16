#!/usr/bin/env python
import os
import sys
import django

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'keshe.settings')
django.setup()

from django.db import connection

def fix_coach_change_table():
    """修复CoachChangeRequest表结构"""
    cursor = connection.cursor()
    
    try:
        # 删除旧表
        cursor.execute("DROP TABLE IF EXISTS reservations_coach_change_request")
        print("✅ 删除旧表成功")
        
        # 创建新表
        create_table_sql = """
        CREATE TABLE `reservations_coach_change_request` (
            `id` bigint NOT NULL AUTO_INCREMENT,
            `reason` longtext NOT NULL,
            `request_date` datetime(6) NOT NULL,
            `status` varchar(20) NOT NULL,
            `current_coach_approval` varchar(20) NOT NULL,
            `target_coach_approval` varchar(20) NOT NULL,
            `campus_admin_approval` varchar(20) NOT NULL,
            `current_coach_approved_at` datetime(6) DEFAULT NULL,
            `target_coach_approved_at` datetime(6) DEFAULT NULL,
            `campus_admin_approved_at` datetime(6) DEFAULT NULL,
            `current_coach_notes` longtext,
            `target_coach_notes` longtext,
            `campus_admin_notes` longtext,
            `processed_at` datetime(6) DEFAULT NULL,
            `created_at` datetime(6) NOT NULL,
            `updated_at` datetime(6) NOT NULL,
            `campus_admin_approved_by_id` bigint DEFAULT NULL,
            `current_coach_id` bigint NOT NULL,
            `current_coach_approved_by_id` bigint DEFAULT NULL,
            `processed_by_id` bigint DEFAULT NULL,
            `student_id` bigint NOT NULL,
            `target_coach_id` bigint NOT NULL,
            `target_coach_approved_by_id` bigint DEFAULT NULL,
            PRIMARY KEY (`id`),
            KEY `reservations_coach_ch_campus_admin_approve_b8b8b8b8_fk_accounts_` (`campus_admin_approved_by_id`),
            KEY `reservations_coach_ch_current_coach_id_b8b8b8b8_fk_accounts_` (`current_coach_id`),
            KEY `reservations_coach_ch_current_coach_approv_b8b8b8b8_fk_accounts_` (`current_coach_approved_by_id`),
            KEY `reservations_coach_ch_processed_by_id_b8b8b8b8_fk_accounts_` (`processed_by_id`),
            KEY `reservations_coach_ch_student_id_b8b8b8b8_fk_accounts_` (`student_id`),
            KEY `reservations_coach_ch_target_coach_id_b8b8b8b8_fk_accounts_` (`target_coach_id`),
            KEY `reservations_coach_ch_target_coach_approve_b8b8b8b8_fk_accounts_` (`target_coach_approved_by_id`),
            CONSTRAINT `reservations_coach_ch_campus_admin_approve_b8b8b8b8_fk_accounts_` FOREIGN KEY (`campus_admin_approved_by_id`) REFERENCES `accounts_user` (`id`),
            CONSTRAINT `reservations_coach_ch_current_coach_approv_b8b8b8b8_fk_accounts_` FOREIGN KEY (`current_coach_approved_by_id`) REFERENCES `accounts_user` (`id`),
            CONSTRAINT `reservations_coach_ch_current_coach_id_b8b8b8b8_fk_accounts_` FOREIGN KEY (`current_coach_id`) REFERENCES `accounts_user` (`id`),
            CONSTRAINT `reservations_coach_ch_processed_by_id_b8b8b8b8_fk_accounts_` FOREIGN KEY (`processed_by_id`) REFERENCES `accounts_user` (`id`),
            CONSTRAINT `reservations_coach_ch_student_id_b8b8b8b8_fk_accounts_` FOREIGN KEY (`student_id`) REFERENCES `accounts_user` (`id`),
            CONSTRAINT `reservations_coach_ch_target_coach_approve_b8b8b8b8_fk_accounts_` FOREIGN KEY (`target_coach_approved_by_id`) REFERENCES `accounts_user` (`id`),
            CONSTRAINT `reservations_coach_ch_target_coach_id_b8b8b8b8_fk_accounts_` FOREIGN KEY (`target_coach_id`) REFERENCES `accounts_user` (`id`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
        """
        
        cursor.execute(create_table_sql)
        print("✅ 创建新表成功")
        
        # 验证表结构
        cursor.execute("DESCRIBE reservations_coach_change_request")
        columns = cursor.fetchall()
        
        print("\n📋 新表结构:")
        for column in columns:
            print(f"  - {column[0]} ({column[1]})")
        
        # 检查关键字段
        column_names = [col[0] for col in columns]
        required_fields = ['student_id', 'current_coach_id', 'target_coach_id', 'reason', 'status']
        
        if all(field in column_names for field in required_fields):
            print("\n✅ 所有必需字段都存在")
        else:
            missing = [field for field in required_fields if field not in column_names]
            print(f"\n❌ 缺少字段: {missing}")
            
    except Exception as e:
        print(f"❌ 修复表结构时出错: {e}")
    finally:
        cursor.close()

if __name__ == '__main__':
    fix_coach_change_table()