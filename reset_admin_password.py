#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import django

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'keshe.settings')
django.setup()

from accounts.models import User
from django.contrib.auth import authenticate

def reset_admin_password():
    """重置管理员密码"""
    print("=== 重置管理员密码 ===")
    
    try:
        # 查找admin账户
        admin = User.objects.get(username='admin')
        print(f"✅ 找到admin账户: {admin.username}")
        print(f"   当前密码哈希: {admin.password[:50]}...")
        
        # 重置密码为testpass123
        admin.set_password('testpass123')
        admin.save()
        print("✅ 密码已重置为: testpass123")
        
        # 验证新密码
        auth_result = authenticate(username='admin', password='testpass123')
        if auth_result:
            print("✅ 新密码验证成功")
            print("\n管理员登录信息:")
            print("- 用户名: admin")
            print("- 密码: testpass123")
            print("- 前端登录: http://localhost:3002/login")
            print("- 后台管理: http://127.0.0.1:8000/admin/")
        else:
            print("❌ 新密码验证失败")
            
    except User.DoesNotExist:
        print("❌ 未找到admin账户")
    except Exception as e:
        print(f"❌ 重置过程中出错: {str(e)}")

if __name__ == '__main__':
    reset_admin_password()