#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
教练员查询与选择功能 - 测试执行器

统一执行所有测试并生成综合报告
"""

import os
import sys
import subprocess
import json
import time
from datetime import datetime

class TestRunner:
    """测试执行器"""
    
    def __init__(self):
        self.test_results = {}
        self.start_time = datetime.now()
    
    def run_backend_tests(self):
        """运行后端API测试"""
        print("\n🔧 运行后端API测试...")
        try:
            result = subprocess.run(
                [sys.executable, 'test_coach_selection_backend.py'],
                capture_output=True,
                text=True,
                timeout=300  # 5分钟超时
            )
            
            self.test_results['backend'] = {
                'success': result.returncode == 0,
                'output': result.stdout,
                'error': result.stderr,
                'return_code': result.returncode
            }
            
            if result.returncode == 0:
                print("✅ 后端API测试完成")
            else:
                print(f"❌ 后端API测试失败 (退出码: {result.returncode})")
                if result.stderr:
                    print(f"错误信息: {result.stderr[:500]}...")
        
        except subprocess.TimeoutExpired:
            print("❌ 后端API测试超时")
            self.test_results['backend'] = {
                'success': False,
                'output': '',
                'error': '测试执行超时',
                'return_code': -1
            }
        except Exception as e:
            print(f"❌ 后端API测试异常: {str(e)}")
            self.test_results['backend'] = {
                'success': False,
                'output': '',
                'error': str(e),
                'return_code': -1
            }
    
    def check_frontend_tests(self):
        """检查前端测试文件"""
        print("\n🌐 检查前端测试...")
        
        frontend_test_file = 'frontend/test_coach_selection_frontend.html'
        
        if os.path.exists(frontend_test_file):
            print("✅ 前端测试文件存在")
            print(f"📁 测试文件位置: {os.path.abspath(frontend_test_file)}")
            print("💡 请在浏览器中打开该文件进行前端测试")
            
            self.test_results['frontend'] = {
                'success': True,
                'file_exists': True,
                'file_path': os.path.abspath(frontend_test_file),
                'note': '需要在浏览器中手动执行'
            }
        else:
            print("❌ 前端测试文件不存在")
            self.test_results['frontend'] = {
                'success': False,
                'file_exists': False,
                'error': '测试文件不存在'
            }
    
    def run_e2e_tests(self):
        """运行端到端测试"""
        print("\n🔄 运行端到端测试...")
        print("注意: 端到端测试需要Chrome浏览器和ChromeDriver")
        
        try:
            result = subprocess.run(
                [sys.executable, 'test_coach_selection_e2e.py'],
                capture_output=True,
                text=True,
                timeout=600  # 10分钟超时
            )
            
            self.test_results['e2e'] = {
                'success': result.returncode == 0,
                'output': result.stdout,
                'error': result.stderr,
                'return_code': result.returncode
            }
            
            if result.returncode == 0:
                print("✅ 端到端测试完成")
            else:
                print(f"❌ 端到端测试失败 (退出码: {result.returncode})")
                if result.stderr:
                    print(f"错误信息: {result.stderr[:500]}...")
        
        except subprocess.TimeoutExpired:
            print("❌ 端到端测试超时")
            self.test_results['e2e'] = {
                'success': False,
                'output': '',
                'error': '测试执行超时',
                'return_code': -1
            }
        except Exception as e:
            print(f"❌ 端到端测试异常: {str(e)}")
            self.test_results['e2e'] = {
                'success': False,
                'output': '',
                'error': str(e),
                'return_code': -1
            }
    
    def check_test_reports(self):
        """检查测试报告文件"""
        print("\n📊 检查测试报告...")
        
        report_files = [
            'test_coach_selection_backend_report.json',
            'test_coach_selection_e2e_report.json'
        ]
        
        found_reports = []
        for report_file in report_files:
            if os.path.exists(report_file):
                found_reports.append(report_file)
                print(f"✅ 找到报告: {report_file}")
            else:
                print(f"❌ 未找到报告: {report_file}")
        
        self.test_results['reports'] = {
            'found_reports': found_reports,
            'total_expected': len(report_files),
            'success': len(found_reports) > 0
        }
    
    def generate_comprehensive_report(self):
        """生成综合测试报告"""
        print("\n📋 生成综合测试报告...")
        
        end_time = datetime.now()
        duration = end_time - self.start_time
        
        # 统计测试结果
        total_tests = len([k for k in self.test_results.keys() if k != 'reports'])
        passed_tests = sum(1 for k, v in self.test_results.items() 
                          if k != 'reports' and v.get('success', False))
        
        # 生成综合报告
        comprehensive_report = {
            'test_summary': {
                'test_suite': '教练员查询与选择功能测试',
                'start_time': self.start_time.strftime('%Y-%m-%d %H:%M:%S'),
                'end_time': end_time.strftime('%Y-%m-%d %H:%M:%S'),
                'duration': str(duration),
                'total_test_categories': total_tests,
                'passed_categories': passed_tests,
                'failed_categories': total_tests - passed_tests,
                'overall_success_rate': f"{(passed_tests/total_tests*100):.1f}%" if total_tests > 0 else "0%"
            },
            'test_categories': {
                'backend_api': {
                    'name': '后端API测试',
                    'status': '通过' if self.test_results.get('backend', {}).get('success') else '失败',
                    'description': '测试教练员列表、筛选、搜索和师生关系管理API',
                    'details': self.test_results.get('backend', {})
                },
                'frontend': {
                    'name': '前端功能测试',
                    'status': '可用' if self.test_results.get('frontend', {}).get('success') else '不可用',
                    'description': '测试前端组件渲染、交互和API集成',
                    'details': self.test_results.get('frontend', {})
                },
                'e2e': {
                    'name': '端到端测试',
                    'status': '通过' if self.test_results.get('e2e', {}).get('success') else '失败',
                    'description': '测试完整的用户操作流程',
                    'details': self.test_results.get('e2e', {})
                }
            },
            'test_environment': {
                'python_version': sys.version,
                'operating_system': os.name,
                'working_directory': os.getcwd(),
                'test_files': [
                    'test_coach_selection_backend.py',
                    'frontend/test_coach_selection_frontend.html',
                    'test_coach_selection_e2e.py'
                ]
            },
            'recommendations': self._generate_recommendations()
        }
        
        # 保存综合报告
        report_file = 'comprehensive_test_report.json'
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(comprehensive_report, f, ensure_ascii=False, indent=2)
        
        print(f"✅ 综合测试报告已保存: {report_file}")
        
        # 显示摘要
        self._print_summary(comprehensive_report)
        
        return comprehensive_report
    
    def _generate_recommendations(self):
        """生成测试建议"""
        recommendations = []
        
        # 检查后端测试
        if not self.test_results.get('backend', {}).get('success'):
            recommendations.append({
                'category': '后端API',
                'issue': '后端API测试失败',
                'suggestion': '检查Django服务器是否运行，数据库连接是否正常，API接口是否正确实现'
            })
        
        # 检查前端测试
        if not self.test_results.get('frontend', {}).get('success'):
            recommendations.append({
                'category': '前端功能',
                'issue': '前端测试文件不可用',
                'suggestion': '确保前端测试文件存在，在浏览器中打开进行手动测试'
            })
        
        # 检查端到端测试
        if not self.test_results.get('e2e', {}).get('success'):
            recommendations.append({
                'category': '端到端测试',
                'issue': '端到端测试失败',
                'suggestion': '确保Chrome浏览器和ChromeDriver已安装，前后端服务器都在运行'
            })
        
        # 通用建议
        recommendations.extend([
            {
                'category': '测试环境',
                'issue': '测试环境准备',
                'suggestion': '确保前端服务器运行在 http://localhost:5173，后端服务器运行在 http://localhost:8000'
            },
            {
                'category': '数据准备',
                'issue': '测试数据',
                'suggestion': '确保数据库中有足够的教练员和学员测试数据'
            },
            {
                'category': '权限设置',
                'issue': '用户权限',
                'suggestion': '确保测试用户具有正确的权限组设置（学员组）'
            }
        ])
        
        return recommendations
    
    def _print_summary(self, report):
        """打印测试摘要"""
        print("\n" + "="*80)
        print("🏓 教练员查询与选择功能 - 综合测试报告")
        print("="*80)
        
        summary = report['test_summary']
        print(f"\n📅 测试时间: {summary['start_time']} - {summary['end_time']}")
        print(f"⏱️  测试耗时: {summary['duration']}")
        print(f"📊 测试结果: {summary['passed_categories']}/{summary['total_test_categories']} 通过 ({summary['overall_success_rate']})")
        
        print("\n📋 测试分类结果:")
        for category, details in report['test_categories'].items():
            status_icon = "✅" if details['status'] in ['通过', '可用'] else "❌"
            print(f"  {status_icon} {details['name']}: {details['status']}")
            print(f"     {details['description']}")
        
        # 显示建议
        if report['recommendations']:
            print("\n💡 改进建议:")
            for i, rec in enumerate(report['recommendations'][:5], 1):  # 显示前5个建议
                print(f"  {i}. [{rec['category']}] {rec['suggestion']}")
        
        print("\n" + "="*80)
    
    def run_all_tests(self):
        """运行所有测试"""
        print("🏓 开始教练员查询与选择功能全面测试")
        print("\n测试包括:")
        print("  1. 后端API接口测试")
        print("  2. 前端功能测试检查")
        print("  3. 端到端集成测试")
        print("  4. 综合测试报告生成")
        
        print("\n⚠️  注意事项:")
        print("  - 确保Django后端服务器运行在 http://localhost:8000")
        print("  - 确保Vue前端服务器运行在 http://localhost:5173")
        print("  - 端到端测试需要Chrome浏览器和ChromeDriver")
        
        input("\n按回车键开始测试...")
        
        try:
            # 运行各类测试
            self.run_backend_tests()
            self.check_frontend_tests()
            self.run_e2e_tests()
            self.check_test_reports()
            
            # 生成综合报告
            self.generate_comprehensive_report()
            
            print("\n🎉 所有测试执行完成！")
            print("\n📁 生成的文件:")
            print("  - comprehensive_test_report.json (综合测试报告)")
            print("  - test_coach_selection_backend_report.json (后端测试报告)")
            print("  - test_coach_selection_e2e_report.json (端到端测试报告)")
            print("  - frontend/test_coach_selection_frontend.html (前端测试页面)")
        
        except KeyboardInterrupt:
            print("\n测试被用户中断")
        except Exception as e:
            print(f"\n测试执行异常: {str(e)}")
            import traceback
            traceback.print_exc()

def main():
    """主函数"""
    runner = TestRunner()
    runner.run_all_tests()

if __name__ == '__main__':
    main()