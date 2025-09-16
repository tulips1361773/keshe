#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import django

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'keshe.settings')
django.setup()

from django.contrib import admin
from payments.models import Payment
from payments.admin import PaymentAdmin

def check_admin_actions():
    """检查Django Admin中的批量操作配置"""
    print("=== 检查Django Admin充值审核配置 ===")
    
    try:
        # 1. 检查PaymentAdmin是否注册
        if Payment in admin.site._registry:
            payment_admin = admin.site._registry[Payment]
            print(f"✅ Payment模型已注册到Admin: {payment_admin.__class__.__name__}")
            
            # 2. 检查批量操作
            actions = payment_admin.get_actions(None)
            print(f"\n📋 可用的批量操作 ({len(actions)}个):")
            for action_name, action_func in actions.items():
                if hasattr(action_func[0], 'short_description'):
                    description = action_func[0].short_description
                else:
                    description = action_name
                print(f"  - {action_name}: {description}")
            
            # 3. 检查特定的充值审核操作
            recharge_actions = ['approve_recharge', 'reject_recharge']
            print(f"\n🔍 充值审核相关操作:")
            for action in recharge_actions:
                if action in actions:
                    func = actions[action][0]
                    desc = getattr(func, 'short_description', action)
                    print(f"  ✅ {action}: {desc}")
                else:
                    print(f"  ❌ {action}: 未找到")
            
            # 4. 检查列表显示字段
            print(f"\n📊 列表显示字段:")
            list_display = payment_admin.list_display
            for field in list_display:
                print(f"  - {field}")
            
            # 5. 检查筛选字段
            print(f"\n🔍 筛选字段:")
            list_filter = payment_admin.list_filter
            for field in list_filter:
                print(f"  - {field}")
            
            # 6. 检查搜索字段
            print(f"\n🔎 搜索字段:")
            search_fields = payment_admin.search_fields
            for field in search_fields:
                print(f"  - {field}")
            
            return True
        else:
            print("❌ Payment模型未注册到Django Admin")
            return False
            
    except Exception as e:
        print(f"❌ 检查过程中出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def check_pending_payments():
    """检查是否有待审核的充值订单"""
    print("\n=== 检查待审核充值订单 ===")
    
    try:
        from payments.models import Payment
        
        # 查询待审核的充值订单
        pending_recharges = Payment.objects.filter(
            payment_type='recharge',
            status='pending'
        ).order_by('-created_at')
        
        print(f"📊 待审核充值订单数量: {pending_recharges.count()}")
        
        if pending_recharges.exists():
            print("\n📋 待审核订单列表:")
            for payment in pending_recharges[:5]:  # 显示前5个
                print(f"  - {payment.payment_id}: {payment.user.username} ¥{payment.amount} ({payment.created_at.strftime('%Y-%m-%d %H:%M')})")
            
            if pending_recharges.count() > 5:
                print(f"  ... 还有 {pending_recharges.count() - 5} 个订单")
        else:
            print("💡 当前没有待审核的充值订单")
            
        return True
        
    except Exception as e:
        print(f"❌ 查询过程中出错: {str(e)}")
        return False

if __name__ == '__main__':
    print("Django Admin充值审核功能检查")
    print("=" * 50)
    
    success1 = check_admin_actions()
    success2 = check_pending_payments()
    
    if success1 and success2:
        print("\n🎯 访问指南:")
        print("1. 打开浏览器访问: http://127.0.0.1:8000/admin/")
        print("2. 使用管理员账户登录: admin / testpass123")
        print("3. 点击 '支付管理' 部分")
        print("4. 点击 'Payments' 进入支付记录管理")
        print("5. 使用右侧筛选器:")
        print("   - Payment type: recharge")
        print("   - Status: pending")
        print("6. 选择要审核的订单")
        print("7. 在页面底部 '操作' 下拉菜单选择审核操作")
        print("8. 点击 '执行' 按钮")
        
        print("\n🎉 检查完成!")
    else:
        print("\n❌ 检查过程中发现问题，请查看上述错误信息")