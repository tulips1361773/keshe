#!/usr/bin/env python
import os
import sys
import django
import requests
import json

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'keshe.settings')
django.setup()

from accounts.models import User
from django.conf import settings

def debug_vue_avatar_detailed():
    """详细调试Vue应用头像显示问题"""
    print("=== 详细调试Vue应用头像显示问题 ===")
    
    # 1. 检查用户数据和头像文件
    try:
        user = User.objects.get(username='hhm')
        print(f"✅ 用户存在: {user.username} (ID: {user.id})")
        print(f"   头像字段: {user.avatar}")
        print(f"   头像URL: {user.avatar.url}")
        
        # 检查头像文件
        avatar_name = str(user.avatar)
        full_path = os.path.join(settings.MEDIA_ROOT, avatar_name)
        print(f"   文件路径: {full_path}")
        print(f"   文件存在: {os.path.exists(full_path)}")
        
        if os.path.exists(full_path):
            file_size = os.path.getsize(full_path)
            print(f"   文件大小: {file_size} bytes")
            
    except User.DoesNotExist:
        print("❌ 用户不存在")
        return False
    
    # 2. 测试不同的URL访问方式
    print(f"\n=== 测试不同URL访问方式 ===")
    
    urls_to_test = [
        "http://127.0.0.1:8000/media/avatars/avatar_4_8f901e9d.jpg",
        "http://localhost:8000/media/avatars/avatar_4_8f901e9d.jpg",
        f"http://127.0.0.1:8000{user.avatar.url}",
        f"http://localhost:8000{user.avatar.url}"
    ]
    
    for url in urls_to_test:
        print(f"\n测试URL: {url}")
        try:
            response = requests.get(url, timeout=5)
            print(f"  状态码: {response.status_code}")
            if response.status_code == 200:
                print(f"  ✅ 访问成功")
                print(f"  Content-Type: {response.headers.get('Content-Type')}")
                print(f"  Content-Length: {response.headers.get('Content-Length')}")
            else:
                print(f"  ❌ 访问失败: {response.text[:100]}")
        except Exception as e:
            print(f"  ❌ 请求异常: {e}")
    
    # 3. 检查CORS头部
    print(f"\n=== 检查CORS头部 ===")
    try:
        response = requests.get("http://127.0.0.1:8000/media/avatars/avatar_4_8f901e9d.jpg")
        cors_headers = {
            'Access-Control-Allow-Origin': response.headers.get('Access-Control-Allow-Origin'),
            'Access-Control-Allow-Credentials': response.headers.get('Access-Control-Allow-Credentials'),
            'Access-Control-Allow-Methods': response.headers.get('Access-Control-Allow-Methods'),
            'Access-Control-Allow-Headers': response.headers.get('Access-Control-Allow-Headers'),
        }
        print("CORS头部:")
        for key, value in cors_headers.items():
            print(f"  {key}: {value}")
    except Exception as e:
        print(f"❌ 获取CORS头部失败: {e}")
    
    # 4. 模拟浏览器请求
    print(f"\n=== 模拟浏览器请求 ===")
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Referer': 'http://localhost:3002/',
        'Origin': 'http://localhost:3002'
    }
    
    try:
        response = requests.get(
            "http://127.0.0.1:8000/media/avatars/avatar_4_8f901e9d.jpg",
            headers=headers,
            timeout=5
        )
        print(f"浏览器模拟请求状态码: {response.status_code}")
        if response.status_code == 200:
            print("✅ 浏览器模拟请求成功")
        else:
            print(f"❌ 浏览器模拟请求失败: {response.text[:100]}")
    except Exception as e:
        print(f"❌ 浏览器模拟请求异常: {e}")
    
    # 5. 检查Django媒体文件设置
    print(f"\n=== 检查Django媒体文件设置 ===")
    print(f"MEDIA_URL: {settings.MEDIA_URL}")
    print(f"MEDIA_ROOT: {settings.MEDIA_ROOT}")
    print(f"DEBUG: {settings.DEBUG}")
    
    # 6. 检查URL配置
    print(f"\n=== 检查URL配置 ===")
    from django.urls import reverse
    from django.conf.urls.static import static
    
    # 检查是否有媒体文件URL配置
    try:
        from keshe.urls import urlpatterns
        media_patterns = [p for p in urlpatterns if hasattr(p, 'pattern') and 'media' in str(p.pattern)]
        print(f"媒体文件URL模式: {len(media_patterns)} 个")
        for pattern in media_patterns:
            print(f"  {pattern}")
    except Exception as e:
        print(f"检查URL配置失败: {e}")
    
    # 7. 生成测试HTML页面
    print(f"\n=== 生成测试HTML页面 ===")
    html_content = f'''<!DOCTYPE html>
<html>
<head>
    <title>头像加载测试</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .test-item {{ margin: 20px 0; padding: 10px; border: 1px solid #ccc; }}
        img {{ max-width: 200px; max-height: 200px; border: 1px solid #ddd; }}
        .error {{ color: red; }}
        .success {{ color: green; }}
    </style>
</head>
<body>
    <h1>头像加载测试页面</h1>
    
    <div class="test-item">
        <h3>测试1: 127.0.0.1:8000</h3>
        <img src="http://127.0.0.1:8000/media/avatars/avatar_4_8f901e9d.jpg" 
             onload="document.getElementById('result1').innerHTML='✅ 加载成功'; document.getElementById('result1').className='success';"
             onerror="document.getElementById('result1').innerHTML='❌ 加载失败'; document.getElementById('result1').className='error';">
        <p id="result1">加载中...</p>
    </div>
    
    <div class="test-item">
        <h3>测试2: localhost:8000</h3>
        <img src="http://localhost:8000/media/avatars/avatar_4_8f901e9d.jpg" 
             onload="document.getElementById('result2').innerHTML='✅ 加载成功'; document.getElementById('result2').className='success';"
             onerror="document.getElementById('result2').innerHTML='❌ 加载失败'; document.getElementById('result2').className='error';">
        <p id="result2">加载中...</p>
    </div>
    
    <div class="test-item">
        <h3>测试3: 相对路径</h3>
        <img src="/media/avatars/avatar_4_8f901e9d.jpg" 
             onload="document.getElementById('result3').innerHTML='✅ 加载成功'; document.getElementById('result3').className='success';"
             onerror="document.getElementById('result3').innerHTML='❌ 加载失败'; document.getElementById('result3').className='error';">
        <p id="result3">加载中...</p>
    </div>
    
    <script>
        console.log('页面加载完成，开始测试头像加载');
        
        // 监听所有图片加载事件
        document.querySelectorAll('img').forEach((img, index) => {{
            img.addEventListener('load', () => {{
                console.log(`图片${{index + 1}}加载成功:`, img.src);
            }});
            
            img.addEventListener('error', (e) => {{
                console.error(`图片${{index + 1}}加载失败:`, img.src, e);
            }});
        }});
    </script>
</body>
</html>'''
    
    test_file_path = os.path.join(os.getcwd(), 'test_avatar_loading.html')
    with open(test_file_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✅ 测试页面已生成: {test_file_path}")
    print(f"   访问地址: http://localhost:8080/test_avatar_loading.html")
    
    return True

if __name__ == '__main__':
    debug_vue_avatar_detailed()