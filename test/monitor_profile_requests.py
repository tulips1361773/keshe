#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
监控个人资料更新请求
"""

import os
import sys
import django
import json
from datetime import datetime

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'keshe.settings')
django.setup()

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from accounts.views import UserProfileUpdateView

# 创建一个监控装饰器
def monitor_request(original_method):
    def wrapper(self, request, *args, **kwargs):
        print(f"\n=== 个人资料更新请求监控 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ===")
        print(f"请求方法: {request.method}")
        print(f"请求路径: {request.path}")
        print(f"请求头: {dict(request.headers)}")
        
        if hasattr(request, 'body') and request.body:
            try:
                body_data = json.loads(request.body.decode('utf-8'))
                print(f"请求体: {json.dumps(body_data, indent=2, ensure_ascii=False)}")
            except:
                print(f"请求体（原始）: {request.body}")
        
        # 调用原始方法
        response = original_method(self, request, *args, **kwargs)
        
        print(f"响应状态码: {response.status_code}")
        if hasattr(response, 'content'):
            try:
                response_data = json.loads(response.content.decode('utf-8'))
                print(f"响应内容: {json.dumps(response_data, indent=2, ensure_ascii=False)}")
            except:
                print(f"响应内容（原始）: {response.content}")
        
        print("=" * 60)
        return response
    
    return wrapper

# 应用监控装饰器到原始视图
original_put = UserProfileUpdateView.put
UserProfileUpdateView.put = monitor_request(original_put)

print("个人资料更新请求监控已启动...")
print("现在可以在前端进行个人资料保存操作，所有请求将被记录。")
print("按 Ctrl+C 停止监控")

try:
    # 保持脚本运行
    import time
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\n监控已停止")