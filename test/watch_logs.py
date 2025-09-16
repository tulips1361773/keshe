#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
实时监控Django日志文件
"""

import time
import os

def watch_log_file(log_file_path):
    """实时监控日志文件"""
    print(f"开始监控日志文件: {log_file_path}")
    print("等待新的日志记录...")
    print("按 Ctrl+C 停止监控\n")
    
    # 获取文件当前大小
    if os.path.exists(log_file_path):
        with open(log_file_path, 'r', encoding='utf-8', errors='ignore') as f:
            f.seek(0, 2)  # 移动到文件末尾
            last_position = f.tell()
    else:
        print(f"日志文件不存在: {log_file_path}")
        return
    
    try:
        while True:
            with open(log_file_path, 'r', encoding='utf-8', errors='ignore') as f:
                f.seek(last_position)
                new_lines = f.readlines()
                
                if new_lines:
                    for line in new_lines:
                        line = line.strip()
                        if line:
                            # 高亮显示包含特定关键词的行
                            if any(keyword in line for keyword in ['个人资料', 'profile', 'PUT', '400', 'ERROR', 'WARNING']):
                                print(f"🔍 {line}")
                            else:
                                print(line)
                    
                    last_position = f.tell()
                
            time.sleep(1)  # 每秒检查一次
            
    except KeyboardInterrupt:
        print("\n监控已停止")
    except Exception as e:
        print(f"监控过程中发生错误: {e}")

if __name__ == "__main__":
    log_file = "D:\\code\\django_learning\\keshe\\logs\\django.log"
    watch_log_file(log_file)