#!/usr/bin/env python
"""
上课提醒定时任务脚本

使用方法：
1. 直接运行：python run_reminders.py
2. 使用Windows任务计划程序定期执行此脚本
3. 或者使用cron（Linux/Mac）定期执行

建议每10分钟执行一次，确保不会错过提醒时间
"""

import os
import sys
import django
from datetime import datetime

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'keshe.settings')
django.setup()

from django.core.management import call_command

def main():
    """主函数"""
    try:
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 开始执行上课提醒任务...")
        
        # 调用Django管理命令
        call_command('send_class_reminders')
        
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 上课提醒任务执行完成")
        
    except Exception as e:
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 执行上课提醒任务时出错: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main()