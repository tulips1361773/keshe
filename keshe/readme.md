# 乒乓球培训管理系统

## 项目介绍
乒乓球培训管理系统是一个基于Django和Vue.js开发的全栈应用，用于管理乒乓球培训机构的日常运营，包括学员管理、教练管理、课程安排、预约系统、比赛管理等功能。

## 系统要求
- 数据库：MySQL
- 后端：Django框架
- 前端：Vue.js + Element Plus

## 部署指南

### 1. 环境准备

#### 1.1 安装必要软件
- Python 3.8+
- MySQL 8.0+
- Node.js 14+
- npm 6+

#### 1.2 安装Python依赖
```bash
# 创建并激活虚拟环境（可选但推荐）
conda create -n keshe_env python=3.8
conda activate keshe_env


# 安装依赖
pip install -r requirements.txt
```

#### 1.3 安装前端依赖
```bash
cd frontend
npm install
```

### 2. 数据库配置

#### 2.1 创建MySQL数据库
```sql
CREATE DATABASE keshe_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

#### 2.2 导入数据库备份
```bash
# 在项目根目录执行
mysql -u root -p keshe_db < keshe_db_backup.sql
```

#### 2.3 配置数据库连接
编辑 `keshe/settings.py` 文件，修改数据库配置：
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'keshe_db',
        'USER': 'root',
        'PASSWORD': '20040324',  # 替换为你的MySQL密码
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

### 3. 启动应用

#### 3.1 启动Django后端
```bash
# 在项目根目录执行
python manage.py runserver
```

#### 3.2 启动Vue前端（开发模式）
```bash
cd frontend
npm run dev
```

#### 3.3 构建前端生产版本（可选）
```bash
cd frontend
npm run build
```

### 4. 访问系统
- 前端访问地址：http://localhost:3001/
- 后台管理地址：http://localhost:8000/admin/

## 账号信息

### 管理员账号
- 超级管理员：admin01 / admin123
- 校区管理员：campus_admin / admin123

### 教练账号
- 测试教练1：test_coach1 / testpass123（初级教练）
- 测试教练2：test_coach2 / testpass123（中级教练）
- 王教练：王教练 / password123（高级教练）

### 学员账号
- 测试学员：test_student / testpass123
- 学员1：student1 / testpass123
- 学员2：student2 / testpass123
- 学员3：student3 / testpass123

## 常见问题

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

### 前端构建问题
- 确保Node.js和npm版本兼容
- 如遇到依赖问题，尝试删除`node_modules`文件夹并重新运行`npm install`

### 权限问题
- 确保上传的媒体文件目录（media）和静态文件目录（static）有正确的读写权限

## 文档资源
- 需求分析文档：`docs/需求分析_v2.md`
- 系统设计文档：`docs/系统设计文档.md`
- 开发进度：`docs/开发进度.md`


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

**注意**: 如果首次运行项目时logs目录不存在，可以运行以下命令创建：
```bash
python create_logs_directory.py
```
或者Django会在启动时自动创建logs目录。

### 数据库管理
```bash
# 进入Django shell
python manage.py shell

# 查看数据库状态
python manage.py dbshell
```