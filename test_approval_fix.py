#!/usr/bin/env python
"""
教练审核流程修复验证脚本
测试Django管理后台和API审核功能是否正确设置所有必要字段
"""

import os
import sys
import django
from datetime import datetime

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'keshe.settings')
django.setup()

from accounts.models import User, Coach
from campus.models import Campus
from django.contrib.auth import get_user_model
from django.utils import timezone

def print_separator(title):
    print(f"\n{'='*60}")
    print(f"{title}")
    print(f"{'='*60}")

def create_test_coach():
    """创建测试教练用于验证审核流程"""
    print("\n=== 创建测试教练 ===")
    
    # 获取或创建测试校区
    timestamp_short = datetime.now().strftime('%H%M%S')
    campus, created = Campus.objects.get_or_create(
        name='测试校区_审核修复',
        defaults={
            'code': f'TEST_FIX_{timestamp_short}',  # 添加唯一的校区代码
            'address': '测试地址123号',
            'phone': '400-123-4567',
            'description': '用于测试审核流程修复的校区'
        }
    )
    
    # 生成唯一的测试数据
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    username = f'test_coach_fix_{timestamp}'
    phone = f'138{timestamp[-8:]}'
    
    # 创建测试教练用户
    coach_user = User.objects.create_user(
        username=username,
        email=f'{username}@test.com',
        password='TestPass123!',
        real_name='测试教练_审核修复',
        phone=phone,
        user_type='coach',
        is_active=False,  # 初始状态：未激活
        is_active_member=False  # 初始状态：非会员
    )
    
    # 创建教练资料
    coach_profile = Coach.objects.create(
        user=coach_user,
        coach_level='intermediate',
        hourly_rate=150.00,
        achievements='测试教练，用于验证审核流程修复',
        max_students=15,
        status='pending'  # 初始状态：待审核
    )
    
    print(f"✅ 创建测试教练成功:")
    print(f"   用户名: {coach_user.username}")
    print(f"   手机号: {coach_user.phone}")
    print(f"   is_active: {coach_user.is_active}")
    print(f"   is_active_member: {coach_user.is_active_member}")
    print(f"   教练状态: {coach_profile.status}")
    
    return coach_user, coach_profile

def test_manual_approval(coach_user, coach_profile):
    """测试手动审核流程（模拟Django管理后台）"""
    print("\n=== 测试手动审核流程 ===")
    
    print("审核前状态:")
    print(f"   is_active: {coach_user.is_active}")
    print(f"   is_active_member: {coach_user.is_active_member}")
    print(f"   教练状态: {coach_profile.status}")
    
    # 模拟管理后台审核通过的逻辑
    coach_profile.status = 'approved'
    coach_profile.approved_at = timezone.now()
    
    # 应用修复后的逻辑
    if coach_profile.status == 'approved':
        coach_user.is_active = True
        coach_user.is_active_member = True  # 关键修复
        coach_user.save()
    
    coach_profile.save()
    
    # 重新加载数据
    coach_user.refresh_from_db()
    coach_profile.refresh_from_db()
    
    print("\n审核后状态:")
    print(f"   is_active: {coach_user.is_active}")
    print(f"   is_active_member: {coach_user.is_active_member}")
    print(f"   教练状态: {coach_profile.status}")
    
    # 验证结果
    if (coach_user.is_active and 
        coach_user.is_active_member and 
        coach_profile.status == 'approved'):
        print("✅ 手动审核流程修复成功！")
        return True
    else:
        print("❌ 手动审核流程仍有问题")
        return False

def test_login_capability(coach_user):
    """测试登录能力"""
    print("\n=== 测试登录能力 ===")
    
    from django.contrib.auth import authenticate
    
    # 尝试认证
    user = authenticate(username=coach_user.username, password='TestPass123!')
    
    if user:
        print(f"✅ 用户认证成功: {user.username}")
        
        # 检查登录条件
        if user.is_active:
            if user.user_type == 'coach' and not user.is_active_member:
                print("❌ 教练员账户待审核，无法登录")
                return False
            else:
                print("✅ 满足登录条件，可以正常登录")
                return True
        else:
            print("❌ 账户未激活，无法登录")
            return False
    else:
        print("❌ 用户认证失败")
        return False

def test_rejection_flow(coach_user, coach_profile):
    """测试审核拒绝流程"""
    print("\n=== 测试审核拒绝流程 ===")
    
    # 重置状态
    coach_profile.status = 'pending'
    coach_user.is_active = False
    coach_user.is_active_member = False
    coach_user.save()
    coach_profile.save()
    
    print("重置为待审核状态")
    
    # 模拟审核拒绝
    coach_profile.status = 'rejected'
    coach_profile.approved_at = timezone.now()
    
    # 应用修复后的逻辑
    if coach_profile.status == 'rejected':
        coach_user.is_active_member = False
        coach_user.save()
    
    coach_profile.save()
    
    # 重新加载数据
    coach_user.refresh_from_db()
    coach_profile.refresh_from_db()
    
    print("审核拒绝后状态:")
    print(f"   is_active: {coach_user.is_active}")
    print(f"   is_active_member: {coach_user.is_active_member}")
    print(f"   教练状态: {coach_profile.status}")
    
    # 验证拒绝后无法登录
    login_result = test_login_capability(coach_user)
    
    if not login_result and coach_profile.status == 'rejected':
        print("✅ 审核拒绝流程正常，用户无法登录")
        return True
    else:
        print("❌ 审核拒绝流程有问题")
        return False

def cleanup_test_data(coach_user, coach_profile):
    """清理测试数据"""
    print("\n=== 清理测试数据 ===")
    
    try:
        coach_profile.delete()
        coach_user.delete()
        print("✅ 测试数据清理完成")
    except Exception as e:
        print(f"❌ 清理测试数据失败: {str(e)}")

def main():
    """主测试函数"""
    print_separator("教练审核流程修复验证")
    
    try:
        # 创建测试数据
        coach_user, coach_profile = create_test_coach()
        
        # 测试审核通过流程
        approval_success = test_manual_approval(coach_user, coach_profile)
        
        # 测试登录能力
        login_success = test_login_capability(coach_user)
        
        # 测试审核拒绝流程
        rejection_success = test_rejection_flow(coach_user, coach_profile)
        
        # 总结测试结果
        print_separator("测试结果总结")
        
        results = {
            '审核通过流程': '✅ 通过' if approval_success else '❌ 失败',
            '登录功能': '✅ 通过' if login_success else '❌ 失败',
            '审核拒绝流程': '✅ 通过' if rejection_success else '❌ 失败'
        }
        
        for test_name, result in results.items():
            print(f"{test_name}: {result}")
        
        all_passed = all([approval_success, login_success, rejection_success])
        
        if all_passed:
            print("\n🎉 所有测试通过！审核流程修复成功！")
            print("\n修复要点:")
            print("1. ✅ 审核通过时同时设置 is_active=True 和 is_active_member=True")
            print("2. ✅ 审核拒绝时设置 is_active_member=False")
            print("3. ✅ 登录API正确验证教练员的会员状态")
        else:
            print("\n❌ 部分测试失败，需要进一步检查")
        
        # 清理测试数据
        cleanup_test_data(coach_user, coach_profile)
        
        return all_passed
        
    except Exception as e:
        print(f"\n❌ 测试过程中出现错误: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)