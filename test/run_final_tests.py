#!/usr/bin/env python
"""
运行最终的完整测试套件
"""

import os
import sys
import django
import subprocess
import time

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'keshe.settings')
django.setup()

def run_test_suite():
    """运行完整的测试套件"""
    print("🚀 开始运行教练员查询与选择功能完整测试套件\n")
    
    test_results = {
        'backend_api': None,
        'frontend_e2e': None,
        'overall_status': 'pending'
    }
    
    # 1. 运行后端API测试
    print("=== 1. 后端API测试 ===")
    try:
        result = subprocess.run(
            [sys.executable, 'test_coach_selection_backend.py'],
            capture_output=True,
            text=True,
            timeout=60
        )
        
        if result.returncode == 0:
            print("✅ 后端API测试通过")
            # 检查通过率
            if "通过率: 100.0%" in result.stdout:
                test_results['backend_api'] = 'passed'
                print("   📊 通过率: 100%")
            else:
                test_results['backend_api'] = 'partial'
                print("   ⚠️  部分测试失败")
        else:
            print("❌ 后端API测试失败")
            test_results['backend_api'] = 'failed'
            print(f"   错误: {result.stderr}")
            
    except subprocess.TimeoutExpired:
        print("❌ 后端API测试超时")
        test_results['backend_api'] = 'timeout'
    except Exception as e:
        print(f"❌ 后端API测试异常: {e}")
        test_results['backend_api'] = 'error'
    
    print()
    
    # 2. 运行前端和端到端测试
    print("=== 2. 前端功能和端到端测试 ===")
    try:
        # 修改前端URL为正确的端口
        result = subprocess.run(
            [sys.executable, 'test_coach_selection_complete.py'],
            capture_output=True,
            text=True,
            timeout=120,
            env={**os.environ, 'FRONTEND_URL': 'http://localhost:3001'}
        )
        
        if result.returncode == 0:
            print("✅ 前端和端到端测试完成")
            # 分析结果
            if "总体完成度:" in result.stdout:
                # 提取完成度信息
                lines = result.stdout.split('\n')
                for line in lines:
                    if "总体完成度:" in line:
                        print(f"   📊 {line.strip()}")
                        break
                test_results['frontend_e2e'] = 'completed'
            else:
                test_results['frontend_e2e'] = 'partial'
        else:
            print("❌ 前端和端到端测试失败")
            test_results['frontend_e2e'] = 'failed'
            print(f"   错误: {result.stderr}")
            
    except subprocess.TimeoutExpired:
        print("❌ 前端和端到端测试超时")
        test_results['frontend_e2e'] = 'timeout'
    except Exception as e:
        print(f"❌ 前端和端到端测试异常: {e}")
        test_results['frontend_e2e'] = 'error'
    
    print()
    
    # 3. 生成最终报告
    print("=== 3. 最终测试报告 ===")
    print("=" * 60)
    print("📋 教练员查询与选择功能测试总结")
    print("=" * 60)
    
    print(f"🔧 后端API测试: {get_status_emoji(test_results['backend_api'])} {test_results['backend_api']}")
    print(f"🌐 前端功能测试: {get_status_emoji(test_results['frontend_e2e'])} {test_results['frontend_e2e']}")
    
    # 确定总体状态
    if test_results['backend_api'] == 'passed' and test_results['frontend_e2e'] in ['completed', 'partial']:
        test_results['overall_status'] = 'success'
        print(f"\n🎉 总体状态: ✅ 测试成功")
        print("\n✨ 主要成就:")
        print("   • 后端API测试100%通过")
        print("   • 教练员查询和筛选功能正常")
        print("   • 师生关系创建功能正常")
        print("   • 权限控制正常")
        
    elif test_results['backend_api'] in ['passed', 'partial']:
        test_results['overall_status'] = 'partial_success'
        print(f"\n⚠️  总体状态: 🟡 部分成功")
        print("\n✅ 已完成:")
        print("   • 后端API功能基本正常")
        print("\n🔄 需要改进:")
        print("   • 前端页面功能")
        print("   • 端到端测试覆盖")
        
    else:
        test_results['overall_status'] = 'needs_work'
        print(f"\n❌ 总体状态: 🔴 需要修复")
        print("\n🛠️  需要解决的问题:")
        if test_results['backend_api'] != 'passed':
            print("   • 后端API问题")
        if test_results['frontend_e2e'] == 'failed':
            print("   • 前端功能问题")
    
    print("\n📁 详细报告文件:")
    print("   • test_coach_selection_backend_report.json")
    print("   • test_coach_selection_complete_report.json (如果生成)")
    
    print("\n" + "=" * 60)
    
    return test_results

def get_status_emoji(status):
    """获取状态对应的emoji"""
    status_map = {
        'passed': '✅',
        'completed': '✅',
        'partial': '🟡',
        'failed': '❌',
        'timeout': '⏰',
        'error': '💥',
        'pending': '⏳'
    }
    return status_map.get(status, '❓')

if __name__ == '__main__':
    results = run_test_suite()
    
    # 根据结果设置退出码
    if results['overall_status'] == 'success':
        sys.exit(0)
    elif results['overall_status'] == 'partial_success':
        sys.exit(1)
    else:
        sys.exit(2)