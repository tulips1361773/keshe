#!/usr/bin/env python
import os
import sys
import django

# 设置Django环境
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'keshe.settings')
django.setup()

from accounts.models import User
from accounts.serializers import UserSerializer

def debug_serializer_issue():
    """调试序列化器问题"""
    print("=== 调试序列化器头像字段问题 ===")
    
    try:
        user = User.objects.get(id=4)
        print(f"\n1. 用户对象检查:")
        print(f"  用户ID: {user.id}")
        print(f"  用户名: {user.username}")
        print(f"  头像字段: {user.avatar}")
        print(f"  头像字段类型: {type(user.avatar)}")
        print(f"  头像字段bool值: {bool(user.avatar)}")
        
        # 检查头像字段的属性
        if user.avatar:
            print(f"  头像name: {user.avatar.name}")
            print(f"  头像url: {user.avatar.url}")
            print(f"  头像path: {user.avatar.path}")
            print(f"  头像size: {user.avatar.size}")
        
        print(f"\n2. 序列化器测试:")
        serializer = UserSerializer(user)
        data = serializer.data
        
        print(f"  序列化后的数据类型: {type(data)}")
        print(f"  序列化后的头像字段: {data.get('avatar')}")
        print(f"  序列化后的头像字段类型: {type(data.get('avatar'))}")
        
        # 手动调用get_avatar方法
        print(f"\n3. 手动调用get_avatar方法:")
        avatar_url = serializer.get_avatar(user)
        print(f"  get_avatar返回值: {avatar_url}")
        print(f"  get_avatar返回值类型: {type(avatar_url)}")
        
        # 检查所有序列化字段
        print(f"\n4. 所有序列化字段:")
        for key, value in data.items():
            print(f"  {key}: {value} ({type(value)})")
            
    except User.DoesNotExist:
        print("用户ID 4不存在")
    except Exception as e:
        print(f"调试过程中发生异常: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    debug_serializer_issue()