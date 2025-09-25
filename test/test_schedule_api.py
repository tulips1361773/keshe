import requests
import json

# 测试学员课表查询API
def test_schedule_api():
    # 1. 登录获取token
    login_data = {'username': 'hhm', 'password': 'testpass123'}
    login_response = requests.post('http://127.0.0.1:8000/api/accounts/login/', json=login_data)
    print(f'登录状态: {login_response.status_code}')
    
    if login_response.status_code != 200:
        print('登录失败，详细信息:')
        print(login_response.text)
        return
    
    token = login_response.json().get('token')
    if not token:
        print('未获取到token')
        return
    
    print(f'获取到token: {token[:20]}...')
    
    # 2. 测试课表查询API
    headers = {'Authorization': f'Token {token}'}
    schedule_response = requests.get('http://127.0.0.1:8000/api/reservations/bookings/my_schedule/', headers=headers)
    
    print(f'课表查询状态: {schedule_response.status_code}')
    
    if schedule_response.status_code == 200:
        data = schedule_response.json()
        print('课表查询成功:')
        print(json.dumps(data, indent=2, ensure_ascii=False))
    else:
        print('课表查询失败:')
        print(schedule_response.text)

if __name__ == '__main__':
    test_schedule_api()