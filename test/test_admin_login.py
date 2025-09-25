#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import django

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'keshe.settings')
django.setup()

from accounts.models import User
from django.contrib.auth import authenticate

def test_admin_login():
    """测试管理员登录"""
    print("=== 测试管理员账户 ===")
    
    try:
        # 查找admin账户
        admin = User.objects.get(username='admin')
        print(f"✅ 找到admin账户")
        print(f"   用户名: {admin.username}")
        print(f"   真实姓名: {admin.real_name}")
        print(f"   超级用户: {admin.is_superuser}")
        print(f"   激活状态: {admin.is_active}")
        print(f"   用户类型: {admin.user_type}")
        
        # 测试密码验证
        auth_result = authenticate(username='admin', password='testpass123')
        if auth_result:
            print("✅ 密码验证成功")
            print("\n管理员登录信息:")
            print("- 用户名: admin")
            print("- 密码: testpass123")
            print("- 前端登录: http://localhost:3002/login")
            print("- 管理后台: http://localhost:8000/admin")
        else:
            print("❌ 密码验证失败")
            
    except User.DoesNotExist:
        print("❌ 未找到admin账户")
        
        # 查看所有超级用户
        superusers = User.objects.filter(is_superuser=True)
        print(f"\n当前超级用户列表 ({superusers.count()}个):")
        for user in superusers:
            print(f"- {user.username} ({user.real_name})")
    
    except Exception as e:
        print(f"❌ 测试过程中出错: {str(e)}")

if __name__ == '__main__':
    test_admin_login()