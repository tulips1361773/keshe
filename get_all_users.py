#!/usr/bin/env python
import os
import django

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'keshe.settings')
django.setup()

from accounts.models import User
from campus.models import CampusStudent, CampusCoach
from django.contrib.auth.hashers import make_password

def get_all_users_info():
    print('=== 所有用户信息 ===')
    users = User.objects.all().order_by('user_type', 'username')
    
    user_info_list = []
    
    for user in users:
        user_info = {
            'username': user.username,
            'real_name': user.real_name or "未设置",
            'user_type': user.get_user_type_display(),
            'phone': user.phone or "未设置",
            'is_superuser': user.is_superuser,
            'is_active': user.is_active,
        }
        
        print(f'用户名: {user_info["username"]}')
        print(f'真实姓名: {user_info["real_name"]}')
        print(f'用户类型: {user_info["user_type"]}')
        print(f'手机号: {user_info["phone"]}')
        print(f'是否超级用户: {user_info["is_superuser"]}')
        print(f'是否激活: {user_info["is_active"]}')
        print('---')
        
        user_info_list.append(user_info)
    
    print(f'总用户数: {users.count()}')
    return user_info_list

def reset_all_passwords():
    print('\n=== 重置所有用户密码为 "password" ===')
    users = User.objects.all()
    
    for user in users:
        user.set_password('password')
        user.save()
        print(f'已重置用户 {user.username} 的密码')
    
    print(f'共重置了 {users.count()} 个用户的密码')

def generate_markdown_report(user_info_list):
    markdown_content = """# 系统账号信息

注意：所有密码已统一重置为 "password"

"""
    
    # 按用户类型分组
    superusers = [u for u in user_info_list if u['is_superuser']]
    coaches = [u for u in user_info_list if u['user_type'] == '教练员']
    students = [u for u in user_info_list if u['user_type'] == '学员']
    admins = [u for u in user_info_list if u['user_type'] == '管理员' and not u['is_superuser']]
    
    if superusers:
        markdown_content += "## 超级管理员\n\n"
        for user in superusers:
            markdown_content += f"- {user['real_name']}：{user['username']} / password（超级管理员）\n"
        markdown_content += "\n"
    
    if admins:
        markdown_content += "## 管理员\n\n"
        for user in admins:
            markdown_content += f"- {user['real_name']}：{user['username']} / password（管理员）\n"
        markdown_content += "\n"
    
    if coaches:
        markdown_content += "## 教练\n\n"
        for user in coaches:
            markdown_content += f"- {user['real_name']}：{user['username']} / password（教练员）\n"
        markdown_content += "\n"
    
    if students:
        markdown_content += "## 学员\n\n"
        for user in students:
            markdown_content += f"- {user['real_name']}：{user['username']} / password（学员）\n"
        markdown_content += "\n"
    
    markdown_content += f"## 统计信息\n\n"
    markdown_content += f"- 总用户数：{len(user_info_list)}\n"
    markdown_content += f"- 超级管理员：{len(superusers)}\n"
    markdown_content += f"- 管理员：{len(admins)}\n"
    markdown_content += f"- 教练：{len(coaches)}\n"
    markdown_content += f"- 学员：{len(students)}\n"
    
    return markdown_content

if __name__ == '__main__':
    # 获取用户信息
    user_info_list = get_all_users_info()
    
    # 重置所有密码
    reset_all_passwords()
    
    # 生成Markdown报告
    markdown_content = generate_markdown_report(user_info_list)
    
    # 写入文件
    with open('系统账号信息.md', 'w', encoding='utf-8') as f:
        f.write(markdown_content)
    
    print('\n✅ 系统账号信息已更新到 系统账号信息.md 文件')