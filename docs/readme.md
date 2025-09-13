# 乒乓球培训管理系统

## 项目简介

这是一个基于Django + Vue3的乒乓球培训管理系统，提供用户注册、教练选择、课程预约、校区管理、支付管理等功能。

## 技术栈

### 后端
- Django 4.2.24
- Django REST Framework 3.14.0
- MySQL 数据库
- Redis 缓存
- JWT 认证

### 前端
- Vue 3.3.4
- Element Plus 2.3.8
- Vue Router 4.2.4
- Axios 1.4.0
- Vite 4.4.5

## 环境要求

- Python 3.8+
- Node.js 16+
- MySQL 5.7+
- Redis (可选，用于缓存)

## 安装和启动指南

### 1. 克隆项目

```bash
git clone <项目地址>
cd keshe
```

### 2. 后端环境配置

#### 2.1 创建虚拟环境

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

#### 2.2 安装Python依赖

```bash
pip install -r requirements.txt
```

#### 2.3 数据库配置

1. 创建MySQL数据库：
```sql
CREATE DATABASE keshe_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

2. 修改 `keshe/settings.py` 中的数据库配置：
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'keshe_db',
        'USER': 'your_username',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {
            'charset': 'utf8mb4',
        },
    }
}
```

#### 2.4 数据库迁移

```bash
python manage.py makemigrations
python manage.py migrate
```

#### 2.5 创建超级用户

```bash
python manage.py createsuperuser
```

#### 2.6 创建测试数据（可选）

```bash
# 创建基础测试数据
python create_test_data.py

# 创建教练审核测试数据
python create_test_approval_data.py
```

#### 2.7 启动后端服务

```bash
python manage.py runserver
```

后端服务将在 `http://127.0.0.1:8000` 启动

### 3. 前端环境配置

#### 3.1 进入前端目录

```bash
cd frontend
```

#### 3.2 安装Node.js依赖

```bash
npm install
```

#### 3.3 启动前端开发服务器

```bash
npm run dev
```

前端服务将在 `http://127.0.0.1:3001` 启动

## 快速启动脚本

### Windows PowerShell

创建 `start.ps1` 文件：
```powershell
# 启动后端
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD'; venv\Scripts\activate; python manage.py runserver"

# 启动前端
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD\frontend'; npm run dev"

Write-Host "系统启动中..."
Write-Host "后端地址: http://127.0.0.1:8000"
Write-Host "前端地址: http://127.0.0.1:3001"
```

### Linux/Mac Bash

创建 `start.sh` 文件：
```bash
#!/bin/bash

# 启动后端
gnome-terminal -- bash -c "source venv/bin/activate; python manage.py runserver; exec bash"

# 启动前端
gnome-terminal -- bash -c "cd frontend; npm run dev; exec bash"

echo "系统启动中..."
echo "后端地址: http://127.0.0.1:8000"
echo "前端地址: http://127.0.0.1:3001"
```

## 测试账号

### 管理员账号
- 用户名: `admin01`
- 密码: `admin123`

### 教练账号
- 用户名: `test_coach`
- 密码: `testpass123`

### 学员账号
- 用户名: `student01`
- 密码: `student123`

## 主要功能模块

### 1. 用户管理 (`/accounts/`)
- 用户注册和登录
- 个人资料管理
- 头像上传
- 用户类型管理（学员/教练/管理员）

### 2. 校区管理 (`/campus/`)
- 校区信息管理
- 区域管理
- 设施管理

### 3. 课程管理 (`/courses/`)
- 课程创建和管理
- 课程报名
- 课程评价

### 4. 预约管理 (`/reservations/`)
- 球台预约
- 教练选择
- 师生关系管理
- 预约审核

### 5. 支付管理 (`/payments/`)
- 订单管理
- 支付记录
- 退款处理

### 6. 通知系统 (`/notifications/`)
- 系统通知
- 消息推送
- 通知历史

### 7. 比赛管理 (`/competitions/`)
- 比赛创建
- 报名管理
- 成绩记录

## API文档

启动后端服务后，可以访问以下地址查看API文档：
- Django Admin: `http://127.0.0.1:8000/admin/`
- API浏览器: `http://127.0.0.1:8000/api/`

## 开发工具

### 日志查看
项目日志存储在 `logs/` 目录下：
- `django.log`: 应用日志
- `api.log`: API请求日志
- `error.log`: 错误日志
- `performance.log`: 性能日志

### 数据库管理
```bash
# 进入Django shell
python manage.py shell

# 查看数据库状态
python manage.py dbshell
```

### 测试运行
```bash
# 运行所有测试
python manage.py test

# 运行特定应用测试
python manage.py test accounts
```

## 常见问题解决

### 1. 数据库连接错误
- 检查MySQL服务是否启动
- 确认数据库配置信息正确
- 检查数据库用户权限

### 2. 前端无法访问后端API
- 确认后端服务正在运行
- 检查CORS配置
- 确认代理配置正确

### 3. 静态文件无法加载
```bash
python manage.py collectstatic
```

### 4. 权限错误
- 检查用户是否已登录
- 确认用户类型和权限
- 检查Token是否有效

### 5. 端口占用
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:8000 | xargs kill -9
```

## 部署说明

### 生产环境配置
1. 修改 `settings.py` 中的 `DEBUG = False`
2. 配置 `ALLOWED_HOSTS`
3. 设置环境变量存储敏感信息
4. 使用 Gunicorn 或 uWSGI 部署后端
5. 使用 Nginx 代理和静态文件服务

### 前端构建
```bash
cd frontend
npm run build
```

## 项目结构

```
keshe/
├── accounts/          # 用户管理应用
├── campus/            # 校区管理应用
├── courses/           # 课程管理应用
├── reservations/      # 预约管理应用
├── payments/          # 支付管理应用
├── notifications/     # 通知系统应用
├── competitions/      # 比赛管理应用
├── frontend/          # Vue前端项目
│   ├── src/
│   │   ├── components/
│   │   ├── views/
│   │   ├── router/
│   │   └── stores/
│   └── public/
├── keshe/             # Django项目配置
├── static/            # 静态文件
├── media/             # 媒体文件
├── logs/              # 日志文件
├── docs/              # 项目文档
└── requirements.txt   # Python依赖
```

## 贡献指南

1. Fork 项目
2. 创建功能分支
3. 提交更改
4. 推送到分支
5. 创建 Pull Request

## 许可证

本项目采用 MIT 许可证。

## 联系方式

如有问题，请联系开发团队或提交 Issue。

---

**最后更新时间**: 2024年12月
**版本**: v1.0.0