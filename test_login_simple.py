import requests
import json

def test_login():
    url = 'http://127.0.0.1:8000/api/accounts/login/'
    data = {
        'username': 'admin',
        'password': 'testpass123'
    }
    
    try:
        response = requests.post(url, json=data)
        print(f'状态码: {response.status_code}')
        print(f'响应头: {dict(response.headers)}')
        print(f'响应内容: {response.text}')
        
        if response.status_code == 200:
            result = response.json()
            print(f'登录成功!')
            print(f'Token: {result.get("token", "未找到token")}')
            print(f'用户信息: {result.get("user", "未找到用户信息")}')
        else:
            print(f'登录失败: {response.text}')
            
    except Exception as e:
        print(f'请求异常: {e}')

if __name__ == '__main__':
    test_login()