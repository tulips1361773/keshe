#!/usr/bin/env python
"""
修复admin用户权限问题
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'keshe.settings')
django.setup()

from accounts.models import User

def fix_admin_permissions():
    """修复admin用户权限"""
    print("=" * 60)
    print("修复admin用户权限问题")
    print("=" * 60)
    
    try:
        admin = User.objects.get(username='admin')
        
        print(f"修复前的admin用户信息:")
        print(f"  - 用户名: {admin.username}")
        print(f"  - 用户类型: {admin.user_type}")
        print(f"  - is_superuser: {admin.is_superuser}")
        print(f"  - is_super_admin: {admin.is_super_admin}")
        print(f"  - is_campus_admin: {admin.is_campus_admin}")
        
        # 修改用户类型为超级管理员
        admin.user_type = 'super_admin'
        admin.save()
        
        print(f"\n修复后的admin用户信息:")
        print(f"  - 用户名: {admin.username}")
        print(f"  - 用户类型: {admin.user_type}")
        print(f"  - is_superuser: {admin.is_superuser}")
        print(f"  - is_super_admin: {admin.is_super_admin}")
        print(f"  - is_campus_admin: {admin.is_campus_admin}")
        
        print(f"\n✅ admin用户权限修复成功！")
        
    except User.DoesNotExist:
        print("❌ admin用户不存在")
    except Exception as e:
        print(f"❌ 修复失败: {e}")

if __name__ == "__main__":
    fix_admin_permissions()