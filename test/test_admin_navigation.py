#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import django

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'keshe.settings')
django.setup()

from payments.models import Payment

def show_admin_navigation():
    """显示Django Admin导航指南"""
    print("=== Django Admin 充值审核导航指南 ===")
    print()
    
    # 检查待审核订单
    pending_count = Payment.objects.filter(
        payment_type='recharge',
        status='pending'
    ).count()
    
    print(f"📊 当前待审核充值订单: {pending_count} 个")
    print()
    
    print("🔗 访问步骤:")
    print("1. 打开浏览器，访问: http://127.0.0.1:8000/admin/")
    print("2. 登录账户: admin / testpass123")
    print("3. 在主页面找到 '支付管理' 部分")
    print("4. 点击 'Payments' 链接")
    print("5. 在右侧筛选器中:")
    print("   - Payment type: 选择 'recharge'")
    print("   - Status: 选择 'pending'")
    print("6. 点击 '筛选' 按钮")
    print("7. 选择要审核的订单")
    print("8. 在页面底部 '操作' 下拉菜单选择:")
    print("   - '批准选中的充值订单' 或")
    print("   - '拒绝选中的充值订单'")
    print("9. 点击 '执行' 按钮")
    print()
    
    print("📋 预期看到的界面元素:")
    print("- 页面标题: 'Select payment to change'")
    print("- 右侧筛选器面板")
    print("- 订单列表（包含payment_id, 用户, 金额等）")
    print("- 页面底部的批量操作区域")
    print()
    
    if pending_count > 0:
        print("✅ 系统中有待审核订单，可以进行实际测试")
        
        # 显示具体订单信息
        pending_orders = Payment.objects.filter(
            payment_type='recharge',
            status='pending'
        ).order_by('-created_at')[:5]
        
        print("\n📋 待审核订单详情:")
        for order in pending_orders:
            print(f"  - {order.payment_id}: {order.user.username} ¥{order.amount}")
    else:
        print("⚠️  当前没有待审核订单，建议先创建测试订单")
        print("   运行: python create_pending_recharge.py")
    
    print()
    print("🎯 验证审核功能:")
    print("1. 选择一个待审核订单")
    print("2. 使用 '批准选中的充值订单' 操作")
    print("3. 检查订单状态是否变为 'completed'")
    print("4. 在 'User accounts' 中验证用户余额是否增加")
    print("5. 在 'Account transactions' 中查看交易记录")

def check_admin_urls():
    """检查管理后台相关URL"""
    print("\n=== 相关管理页面URL ===")
    print("🔗 主要页面:")
    print("- 管理后台首页: http://127.0.0.1:8000/admin/")
    print("- 支付记录管理: http://127.0.0.1:8000/admin/payments/payment/")
    print("- 用户账户管理: http://127.0.0.1:8000/admin/payments/useraccount/")
    print("- 交易记录管理: http://127.0.0.1:8000/admin/payments/accounttransaction/")
    print("- 退款记录管理: http://127.0.0.1:8000/admin/payments/refund/")
    print()
    print("💡 提示: 可以直接访问这些URL快速跳转到对应管理页面")

if __name__ == '__main__':
    show_admin_navigation()
    check_admin_urls()
    
    print("\n" + "="*60)
    print("🎉 如果按照上述步骤仍然找不到充值审核功能，")
    print("   请检查Django服务器是否正常运行，或联系技术支持。")
    print("="*60)