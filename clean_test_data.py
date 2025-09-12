#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
清理测试数据脚本
"""

import os
import sys
import django

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'keshe.settings')
django.setup()

from accounts.models import User
from campus.models import Campus
from competitions.models import Competition, CompetitionRegistration, CompetitionGroup, CompetitionMatch

def clean_test_data():
    """清理所有测试数据"""
    print("开始清理测试数据...")
    
    # 清理比赛相关数据
    test_competitions = Competition.objects.filter(title__contains='测试')
    CompetitionMatch.objects.filter(competition__in=test_competitions).delete()
    CompetitionGroup.objects.filter(competition__in=test_competitions).delete()
    CompetitionRegistration.objects.filter(competition__in=test_competitions).delete()
    test_competitions.delete()
    print("✓ 清理比赛数据")
    
    # 清理用户数据
    User.objects.filter(username__startswith='test_').delete()
    User.objects.filter(phone__in=['13800138001', '13800138002', '13800138003']).delete()
    print("✓ 清理用户数据")
    
    # 清理校区数据
    Campus.objects.filter(name='测试校区').delete()
    Campus.objects.filter(code='TEST001').delete()
    print("✓ 清理校区数据")
    
    print("测试数据清理完成！")

if __name__ == '__main__':
    clean_test_data()