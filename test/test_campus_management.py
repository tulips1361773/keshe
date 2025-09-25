#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
校区管理模块功能测试脚本
测试校区管理是否符合需求分析_v2.md中L33-36的要求
"""

import os
import sys
import django
from django.test import TestCase
from django.contrib.auth import get_user_model
import json

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'keshe.settings')
django.setup()

from rest_framework.test import APIClient
from rest_framework import status

from campus.models import Campus
from accounts.models import User

class CampusManagementTest:
    """校区管理功能测试类"""
    
    def __init__(self):
        self.client = APIClient()
        self.setup_test_data()
    
    def setup_test_data(self):
        """设置测试数据"""
        print("=== 设置测试数据 ===")
        
        # 先清理可能存在的测试数据
        self.cleanup_existing_data()
        
        # 创建超级管理员
        self.super_admin, created = User.objects.get_or_create(
            username='super_admin_test',
            defaults={
                'password': 'test123456',
                'real_name': '超级管理员',
                'user_type': 'super_admin',
                'phone': '13800000001',
                'email': 'super@test.com'
            }
        )
        if created:
            self.super_admin.set_password('test123456')
            self.super_admin.save()
        print(f"✓ 创建超级管理员: {self.super_admin.real_name}")
        
        # 创建校区管理员
        self.campus_admin, created = User.objects.get_or_create(
            username='campus_admin_test',
            defaults={
                'password': 'test123456',
                'real_name': '校区管理员',
                'user_type': 'campus_admin',
                'phone': '13800000002',
                'email': 'campus@test.com'
            }
        )
        if created:
            self.campus_admin.set_password('test123456')
            self.campus_admin.save()
        print(f"✓ 创建校区管理员: {self.campus_admin.real_name}")
        
        # 创建测试校区
        self.campus, created = Campus.objects.get_or_create(
            name='测试校区',
            defaults={
                'code': 'TEST001',
                'campus_type': 'center',
                'address': '测试地址123号',
                'contact_person': '联系人',
                'phone': '13800000003',
                'email': 'campus@example.com'
            }
        )
        print(f"✓ 创建测试校区: {self.campus.name}")
    
    def cleanup_existing_data(self):
        """清理现有测试数据"""
        try:
            Campus.objects.filter(name__contains='测试').delete()
            Campus.objects.filter(name__contains='新校区').delete()
            User.objects.filter(username__contains='test').delete()
        except Exception as e:
            pass  # 忽略清理错误
    
    def test_campus_creation_by_super_admin(self):
        """测试超级管理员创建校区功能"""
        print("\n=== 测试1: 超级管理员录入校区信息 ===")
        
        # 超级管理员登录
        self.client.force_authenticate(user=self.super_admin)
        
        campus_data = {
            'name': '新校区',
            'code': 'NEW001',
            'campus_type': 'branch',
            'address': '新校区地址456号',
            'contact_person': '新联系人',
            'phone': '13800000004',
            'email': 'new@example.com',
            'parent_campus': self.campus.id,
            'description': '这是一个新的分校区'
        }
        
        response = self.client.post('/campus/api/create/', campus_data, format='json')
        
        if response.status_code == 201:
            print("✓ 超级管理员成功创建校区")
            print(f"  - 校区名称: {response.data['data']['name']}")
            print(f"  - 校区编码: {response.data['data']['code']}")
            print(f"  - 校区地址: {response.data['data']['address']}")
            return True
        else:
            print(f"✗ 创建校区失败: {response.data}")
            return False
    
    def test_assign_campus_manager(self):
        """测试超级管理员指定校区负责人功能"""
        print("\n=== 测试2: 超级管理员指定分校区负责人 ===")
        
        # 超级管理员登录
        self.client.force_authenticate(user=self.super_admin)
        
        # 获取可用管理员列表
        response = self.client.get('/campus/api/available-managers/')
        if response.status_code == 200:
            print("✓ 成功获取可用管理员列表")
            managers = response.data['data']
            for manager in managers:
                print(f"  - {manager['real_name']} (ID: {manager['id']})")
        
        # 为校区指定管理员
        assign_data = {
            'manager_id': self.campus_admin.id
        }
        
        response = self.client.post(f'/campus/api/{self.campus.id}/assign-manager/', assign_data, format='json')
        
        if response.status_code == 200:
            print("✓ 超级管理员成功指定校区负责人")
            print(f"  - 校区: {response.data['data']['campus_name']}")
            print(f"  - 新管理员: {response.data['data']['new_manager']}")
            return True
        else:
            print(f"✗ 指定负责人失败: {response.data}")
            return False
    
    def test_campus_admin_permissions(self):
        """测试校区管理员权限"""
        print("\n=== 测试3: 校区管理员权限验证 ===")
        
        # 校区管理员登录
        self.client.force_authenticate(user=self.campus_admin)
        
        # 测试校区管理员不能创建校区
        campus_data = {
            'name': '非法校区',
            'code': 'ILLEGAL001',
            'campus_type': 'center',
            'address': '非法地址',
            'contact_person': '非法联系人',
            'phone': '13800000005',
            'email': 'illegal@example.com'
        }
        
        response = self.client.post('/campus/api/create/', campus_data, format='json')
        
        if response.status_code == 403:
            print("✓ 校区管理员正确被禁止创建校区")
        else:
            print(f"✗ 权限控制失败: {response.data}")
            return False
        
        # 测试校区管理员不能指定其他校区的负责人
        assign_data = {
            'manager_id': self.campus_admin.id
        }
        
        response = self.client.post(f'/campus/api/{self.campus.id}/assign-manager/', assign_data, format='json')
        
        if response.status_code == 403:
            print("✓ 校区管理员正确被禁止指定校区负责人")
            return True
        else:
            print(f"✗ 权限控制失败: {response.data}")
            return False
    
    def test_super_admin_full_permissions(self):
        """测试超级管理员的完整权限"""
        print("\n=== 测试4: 超级管理员完整权限验证 ===")
        
        # 超级管理员登录
        self.client.force_authenticate(user=self.super_admin)
        
        # 测试查看所有校区
        response = self.client.get('/campus/api/list/')
        
        if response.status_code == 200:
            print("✓ 超级管理员可以查看所有校区")
            print(f"  - 校区数量: {response.data['count']}")
            
            # 检查权限标识
            permissions = response.data.get('user_permissions', {})
            if permissions.get('can_create') and permissions.get('is_super_admin'):
                print("✓ 超级管理员权限标识正确")
                return True
            else:
                print(f"✗ 权限标识错误: {permissions}")
                return False
        else:
            print(f"✗ 获取校区列表失败: {response.data}")
            return False
    
    def run_all_tests(self):
        """运行所有测试"""
        print("\n" + "="*50)
        print("开始校区管理模块功能测试")
        print("测试需求: 需求分析_v2.md L33-36")
        print("="*50)
        
        tests = [
            self.test_campus_creation_by_super_admin,
            self.test_assign_campus_manager,
            self.test_campus_admin_permissions,
            self.test_super_admin_full_permissions
        ]
        
        passed = 0
        total = len(tests)
        
        for test in tests:
            try:
                if test():
                    passed += 1
            except Exception as e:
                print(f"✗ 测试执行出错: {e}")
        
        print("\n" + "="*50)
        print(f"测试结果: {passed}/{total} 通过")
        
        if passed == total:
            print("🎉 所有测试通过！校区管理模块符合需求。")
        else:
            print("⚠️  部分测试失败，需要进一步检查。")
        
        print("="*50)
        
        return passed == total
    
    def cleanup(self):
        """清理测试数据"""
        print("\n=== 清理测试数据 ===")
        try:
            # 删除创建的测试数据
            Campus.objects.filter(name__contains='测试').delete()
            Campus.objects.filter(name__contains='新校区').delete()
            User.objects.filter(username__contains='test').delete()
            print("✓ 测试数据清理完成")
        except Exception as e:
            print(f"✗ 清理数据时出错: {e}")

def main():
    """主函数"""
    tester = CampusManagementTest()
    
    try:
        success = tester.run_all_tests()
        return success
    finally:
        tester.cleanup()

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)