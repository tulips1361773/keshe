#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试教练详情API修复
"""

import requests
import json

def test_coach_detail_api():
    """
    测试教练详情API
    """
    print("测试教练详情API修复")
    print("=" * 40)
    
    base_url = "http://127.0.0.1:8000"
    
    # 1. 先获取教练列表，找到一个有效的教练ID
    print("\n1. 获取教练列表...")
    try:
        response = requests.get(f"{base_url}/api/reservations/coaches/", timeout=10)
        if response.status_code == 200:
            coaches_data = response.json()
            coaches = coaches_data.get('results', [])
            if coaches:
                coach_id = coaches[0]['id']
                coach_name = coaches[0].get('real_name', '未知教练')
                print(f"✅ 找到教练: {coach_name} (ID: {coach_id})")
                
                # 2. 测试教练详情API
                print(f"\n2. 测试教练详情API (ID: {coach_id})...")
                detail_response = requests.get(f"{base_url}/api/accounts/coaches/{coach_id}/", timeout=10)
                
                if detail_response.status_code == 200:
                    detail_data = detail_response.json()
                    print("✅ 教练详情API调用成功")
                    print(f"教练姓名: {detail_data.get('user', {}).get('real_name', '未知')}")
                    print(f"教练等级: {detail_data.get('coach_level', '未知')}")
                    print(f"认证状态: {detail_data.get('status', '未知')}")
                    print(f"评分: {detail_data.get('rating', 0)}")
                    print(f"学员数量: {detail_data.get('student_count', 0)}")
                    
                    # 检查必要字段
                    required_fields = ['id', 'user', 'coach_level', 'status']
                    missing_fields = [field for field in required_fields if field not in detail_data]
                    
                    if not missing_fields:
                        print("✅ 所有必要字段都存在")
                        return True
                    else:
                        print(f"⚠️  缺少字段: {missing_fields}")
                        return False
                        
                elif detail_response.status_code == 404:
                    print(f"❌ 教练不存在 (ID: {coach_id})")
                    return False
                elif detail_response.status_code == 403:
                    print("❌ 权限不足，需要登录")
                    return False
                else:
                    print(f"❌ 教练详情API失败: {detail_response.status_code}")
                    print(f"响应内容: {detail_response.text}")
                    return False
            else:
                print("❌ 没有找到教练数据")
                return False
        else:
            print(f"❌ 获取教练列表失败: {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ 网络请求失败: {e}")
        return False
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False

def test_frontend_api_path():
    """
    测试前端API路径是否正确
    """
    print("\n3. 测试前端API路径...")
    
    # 检查修复后的API路径
    coach_detail_file = "D:/code/django_learning/keshe/frontend/src/views/CoachDetail.vue"
    try:
        with open(coach_detail_file, 'r', encoding='utf-8') as f:
            content = f.read()
            if '/api/accounts/coaches/' in content:
                print("✅ 前端API路径已修复为 /api/accounts/coaches/")
                return True
            else:
                print("❌ 前端API路径未正确修复")
                return False
    except Exception as e:
        print(f"❌ 检查前端文件失败: {e}")
        return False

if __name__ == '__main__':
    print("教练详情功能修复测试")
    print("=" * 50)
    
    results = []
    
    # 测试后端API
    api_result = test_coach_detail_api()
    results.append(('后端API测试', api_result))
    
    # 测试前端路径修复
    frontend_result = test_frontend_api_path()
    results.append(('前端路径修复', frontend_result))
    
    # 输出总结
    print("\n=== 测试结果总结 ===")
    passed = 0
    for test_name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n总体结果: {passed}/{len(results)} 通过")
    
    if passed == len(results):
        print("\n🎉 教练详情功能修复成功！")
    else:
        print("\n⚠️  还有问题需要解决")