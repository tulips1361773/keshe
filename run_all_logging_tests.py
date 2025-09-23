#!/usr/bin/env python
"""
日志功能综合测试脚本
统一运行所有日志功能测试并生成详细报告
"""

import os
import sys
import django
import subprocess
import time
from datetime import datetime

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'keshe.settings')
django.setup()

from logs.models import SystemLog
from django.contrib.auth import get_user_model

User = get_user_model()

class ComprehensiveLoggingTest:
    def __init__(self):
        self.test_scripts = [
            ('test_logging_setup.py', '环境准备'),
            ('test_competition_logging.py', '比赛管理日志测试'),
            ('test_table_logging.py', '球台管理日志测试'),
            ('test_api_logging.py', 'API接口日志测试')
        ]
        self.results = {}
        self.start_time = None
        self.end_time = None
        
    def check_environment(self):
        """检查测试环境"""
        print("检查测试环境...")
        print("="*60)
        
        # 检查数据库连接
        try:
            from django.db import connection
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
            print("✓ 数据库连接正常")
        except Exception as e:
            print(f"❌ 数据库连接失败: {e}")
            return False
        
        # 检查日志模型
        try:
            SystemLog.objects.count()
            print("✓ 日志模型可用")
        except Exception as e:
            print(f"❌ 日志模型不可用: {e}")
            return False
        
        # 检查测试脚本是否存在
        missing_scripts = []
        for script, description in self.test_scripts:
            if not os.path.exists(script):
                missing_scripts.append(script)
        
        if missing_scripts:
            print(f"❌ 缺少测试脚本: {', '.join(missing_scripts)}")
            return False
        else:
            print("✓ 所有测试脚本存在")
        
        print("✓ 测试环境检查通过\n")
        return True
    
    def run_script(self, script_name, description):
        """运行单个测试脚本"""
        print(f"运行 {description} ({script_name})...")
        print("-" * 50)
        
        try:
            # 运行测试脚本
            result = subprocess.run(
                [sys.executable, script_name],
                capture_output=True,
                text=True,
                timeout=300  # 5分钟超时
            )
            
            success = result.returncode == 0
            
            print(f"脚本输出:")
            print(result.stdout)
            
            if result.stderr:
                print(f"错误输出:")
                print(result.stderr)
            
            status = "✓ 通过" if success else "❌ 失败"
            print(f"\n{description} 结果: {status}")
            print("=" * 50)
            
            return {
                'success': success,
                'stdout': result.stdout,
                'stderr': result.stderr,
                'returncode': result.returncode
            }
            
        except subprocess.TimeoutExpired:
            print(f"❌ {description} 超时")
            return {
                'success': False,
                'stdout': '',
                'stderr': '测试超时',
                'returncode': -1
            }
        except Exception as e:
            print(f"❌ 运行 {description} 时出错: {e}")
            return {
                'success': False,
                'stdout': '',
                'stderr': str(e),
                'returncode': -1
            }
    
    def get_log_statistics(self):
        """获取日志统计信息"""
        print("获取日志统计信息...")
        print("-" * 50)
        
        try:
            # 总日志数量
            total_logs = SystemLog.objects.count()
            print(f"总日志数量: {total_logs}")
            
            # 按操作类型统计
            from django.db.models import Count
            action_stats = SystemLog.objects.values('action_type').annotate(
                count=Count('id')
            ).order_by('-count')
            
            print("\n按操作类型统计:")
            for stat in action_stats:
                print(f"  {stat['action_type']}: {stat['count']} 条")
            
            # 按资源类型统计
            resource_stats = SystemLog.objects.values('resource_type').annotate(
                count=Count('id')
            ).order_by('-count')
            
            print("\n按资源类型统计:")
            for stat in resource_stats:
                resource_type = stat['resource_type'] or '未指定'
                print(f"  {resource_type}: {stat['count']} 条")
            
            # 按用户统计
            user_stats = SystemLog.objects.values('user__username').annotate(
                count=Count('id')
            ).order_by('-count')
            
            print("\n按用户统计:")
            for stat in user_stats:
                username = stat['user__username'] or '未知用户'
                print(f"  {username}: {stat['count']} 条")
            
            # 最近的日志
            recent_logs = SystemLog.objects.order_by('-created_at')[:5]
            print("\n最近5条日志:")
            for log in recent_logs:
                print(f"  [{log.created_at}] {log.user.username if log.user else '未知'} "
                      f"{log.action_type} {log.resource_type or ''} - {log.description}")
            
            return {
                'total_logs': total_logs,
                'action_stats': list(action_stats),
                'resource_stats': list(resource_stats),
                'user_stats': list(user_stats),
                'recent_logs': [
                    {
                        'created_at': log.created_at.isoformat(),
                        'user': log.user.username if log.user else None,
                        'action_type': log.action_type,
                        'resource_type': log.resource_type,
                        'description': log.description
                    }
                    for log in recent_logs
                ]
            }
            
        except Exception as e:
            print(f"❌ 获取日志统计信息失败: {e}")
            return None
    
    def generate_report(self):
        """生成测试报告"""
        print("\n" + "="*60)
        print("日志功能测试报告")
        print("="*60)
        
        print(f"测试开始时间: {self.start_time}")
        print(f"测试结束时间: {self.end_time}")
        
        if self.start_time and self.end_time:
            duration = self.end_time - self.start_time
            print(f"测试总耗时: {duration}")
        
        print(f"\n测试结果汇总:")
        print("-" * 30)
        
        passed = 0
        total = len(self.results)
        
        for script, description in self.test_scripts:
            if script in self.results:
                result = self.results[script]
                status = "✓ 通过" if result['success'] else "❌ 失败"
                print(f"{description}: {status}")
                if result['success']:
                    passed += 1
                elif result['stderr']:
                    print(f"  错误: {result['stderr'][:100]}...")
        
        print(f"\n总体结果: {passed}/{total} 个测试通过")
        
        # 获取并显示日志统计
        print("\n" + "="*60)
        print("日志统计信息")
        print("="*60)
        
        log_stats = self.get_log_statistics()
        
        # 生成建议
        print("\n" + "="*60)
        print("测试建议")
        print("="*60)
        
        if passed == total:
            print("🎉 恭喜！所有日志功能测试都通过了！")
            print("\n建议:")
            print("1. 定期运行这些测试以确保日志功能正常")
            print("2. 监控日志数据库的大小，定期清理旧日志")
            print("3. 考虑添加日志分析和报警功能")
        else:
            print("⚠️  部分测试失败，需要检查以下方面:")
            print("1. 确保Django开发服务器正在运行 (python manage.py runserver)")
            print("2. 检查数据库连接和权限")
            print("3. 验证日志相关的模型和视图是否正确配置")
            print("4. 检查API端点是否存在并正常工作")
        
        # 保存报告到文件
        self.save_report_to_file(log_stats)
    
    def save_report_to_file(self, log_stats):
        """保存报告到文件"""
        report_filename = f"logging_test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        try:
            with open(report_filename, 'w', encoding='utf-8') as f:
                f.write("日志功能测试报告\n")
                f.write("="*60 + "\n")
                f.write(f"生成时间: {datetime.now()}\n")
                f.write(f"测试开始时间: {self.start_time}\n")
                f.write(f"测试结束时间: {self.end_time}\n\n")
                
                f.write("测试结果:\n")
                f.write("-" * 30 + "\n")
                
                for script, description in self.test_scripts:
                    if script in self.results:
                        result = self.results[script]
                        status = "通过" if result['success'] else "失败"
                        f.write(f"{description}: {status}\n")
                        
                        if not result['success'] and result['stderr']:
                            f.write(f"  错误: {result['stderr']}\n")
                
                if log_stats:
                    f.write(f"\n日志统计:\n")
                    f.write("-" * 30 + "\n")
                    f.write(f"总日志数量: {log_stats['total_logs']}\n")
                    
                    f.write("\n按操作类型统计:\n")
                    for stat in log_stats['action_stats']:
                        f.write(f"  {stat['action_type']}: {stat['count']} 条\n")
                    
                    f.write("\n按资源类型统计:\n")
                    for stat in log_stats['resource_stats']:
                        resource_type = stat['resource_type'] or '未指定'
                        f.write(f"  {resource_type}: {stat['count']} 条\n")
            
            print(f"\n✓ 测试报告已保存到: {report_filename}")
            
        except Exception as e:
            print(f"❌ 保存报告失败: {e}")
    
    def run_all_tests(self):
        """运行所有测试"""
        print("开始日志功能综合测试")
        print("="*60)
        
        self.start_time = datetime.now()
        
        # 检查环境
        if not self.check_environment():
            print("❌ 环境检查失败，无法继续测试")
            return False
        
        # 运行所有测试脚本
        for script, description in self.test_scripts:
            result = self.run_script(script, description)
            self.results[script] = result
            
            # 如果环境准备失败，停止后续测试
            if script == 'test_logging_setup.py' and not result['success']:
                print("❌ 环境准备失败，停止后续测试")
                break
            
            # 短暂暂停，避免测试冲突
            time.sleep(1)
        
        self.end_time = datetime.now()
        
        # 生成报告
        self.generate_report()
        
        # 返回总体测试结果
        passed = sum(1 for result in self.results.values() if result['success'])
        total = len(self.results)
        
        return passed == total

def main():
    """主函数"""
    print("日志功能综合测试工具")
    print("="*60)
    print("此工具将运行所有日志功能测试并生成详细报告")
    print("请确保:")
    print("1. Django开发服务器正在运行 (python manage.py runserver)")
    print("2. 数据库连接正常")
    print("3. 所有测试脚本文件存在")
    print("="*60)
    
    input("按回车键开始测试...")
    
    tester = ComprehensiveLoggingTest()
    success = tester.run_all_tests()
    
    return success

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)