#!/usr/bin/env python
"""
创建logs目录和初始日志文件
确保Django日志系统正常工作
"""
import os
from pathlib import Path

def create_logs_directory():
    """创建logs目录和必要的日志文件"""
    # 获取项目根目录
    base_dir = Path(__file__).resolve().parent
    logs_dir = base_dir / 'logs'
    
    # 创建logs目录（如果不存在）
    logs_dir.mkdir(exist_ok=True)
    print(f"✅ 创建logs目录: {logs_dir}")
    
    # 需要创建的日志文件列表
    log_files = [
        'django.log',
        'api.log', 
        'error.log',
        'performance.log'
    ]
    
    # 创建空的日志文件（如果不存在）
    for log_file in log_files:
        log_path = logs_dir / log_file
        if not log_path.exists():
            log_path.touch()
            print(f"✅ 创建日志文件: {log_path}")
        else:
            print(f"📄 日志文件已存在: {log_path}")
    
    print("\n🎉 logs目录和日志文件创建完成！")
    print("现在Django可以正常写入日志了。")

if __name__ == '__main__':
    create_logs_directory()