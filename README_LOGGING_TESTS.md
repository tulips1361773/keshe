# 日志功能测试脚本使用说明

## 概述

本测试套件用于全面验证乒乓球预约系统的日志记录功能，包括比赛管理、球台管理和API操作的日志记录。

## 测试脚本列表

### 1. `test_logging_setup.py` - 环境准备脚本
**功能**: 创建测试用户、校区、教练等基础数据，清理测试日志
**用途**: 为其他测试脚本准备必要的测试环境

**创建的测试数据**:
- 管理员用户: `test_admin` / `admin123456`
- 学生用户: `test_student` / `test123456`  
- 教练用户: `test_coach` / `coach123456`
- 测试校区: `测试校区`
- 测试教练: `测试教练`

### 2. `test_competition_logging.py` - 比赛管理日志测试
**功能**: 测试比赛创建、更新、删除操作的日志记录
**测试内容**:
- API创建比赛的日志记录
- API更新比赛的日志记录  
- API删除比赛的日志记录
- Django Admin比赛操作的日志记录

### 3. `test_table_logging.py` - 球台管理日志测试
**功能**: 测试球台创建、更新、删除操作的日志记录
**测试内容**:
- Django Admin创建球台的日志记录
- Django Admin更新球台的日志记录
- Django Admin删除球台的日志记录
- 多球台批量操作的日志记录
- 球台状态变更的日志记录

### 4. `test_api_logging.py` - API接口日志测试
**功能**: 测试各种API操作的日志记录
**测试内容**:
- 用户资料更新的日志记录
- 预约操作的日志记录
- 比赛报名的日志记录
- 用户认证的日志记录
- 教练操作的日志记录

### 5. `run_all_logging_tests.py` - 综合测试脚本
**功能**: 统一运行所有测试并生成详细报告
**特性**:
- 自动运行所有测试脚本
- 生成详细的测试报告
- 提供日志统计信息
- 保存报告到文件

## 使用方法

### 前置条件

1. **启动Django开发服务器**:
   ```bash
   python manage.py runserver
   ```

2. **确保数据库正常**:
   ```bash
   python manage.py migrate
   ```

### 运行方式

#### 方式一: 运行综合测试 (推荐)
```bash
python run_all_logging_tests.py
```
这将自动运行所有测试并生成完整报告。

#### 方式二: 单独运行测试
```bash
# 1. 首先准备测试环境
python test_logging_setup.py

# 2. 运行具体测试
python test_competition_logging.py
python test_table_logging.py  
python test_api_logging.py
```

### 测试输出

每个测试脚本都会输出详细的测试过程和结果:

```
✓ 日志记录成功:
  - 操作类型: create
  - 资源类型: competition
  - 资源ID: 123
  - 描述: 创建比赛: API测试比赛
  - 操作时间: 2024-01-20 10:30:45
```

### 测试报告

综合测试会生成包含以下信息的报告:
- 测试执行时间和耗时
- 各个测试的通过/失败状态
- 日志统计信息 (按操作类型、资源类型、用户统计)
- 最近的日志记录
- 测试建议和故障排除指导

## 验证日志记录

### 通过Django Admin查看
1. 访问 `http://localhost:8000/admin/`
2. 登录管理员账户
3. 进入 "Logs" -> "System logs" 查看日志记录

### 通过数据库查看
```sql
SELECT * FROM logs_systemlog ORDER BY created_at DESC LIMIT 10;
```

### 通过API查看 (如果有相应端点)
```bash
curl -H "Authorization: Token <admin_token>" \
     http://localhost:8000/api/logs/system-logs/
```

## 故障排除

### 常见问题

1. **API请求失败**
   - 确保Django开发服务器正在运行
   - 检查端口是否为8000
   - 验证API端点是否存在

2. **数据库连接失败**
   - 检查数据库配置
   - 确保数据库服务正在运行
   - 验证数据库权限

3. **测试用户不存在**
   - 先运行 `test_logging_setup.py` 创建测试用户
   - 检查用户创建是否成功

4. **日志记录失败**
   - 检查日志模型是否正确迁移
   - 验证日志装饰器和函数是否正确导入
   - 确认IP地址获取功能正常

### 调试技巧

1. **查看详细错误信息**:
   每个测试脚本都会输出详细的错误信息，包括HTTP状态码和响应内容。

2. **检查日志数据库**:
   ```python
   from logs.models import SystemLog
   print(SystemLog.objects.count())  # 查看日志总数
   print(SystemLog.objects.latest('created_at'))  # 查看最新日志
   ```

3. **手动测试API**:
   使用Postman或curl手动测试API端点，确认功能正常。

## 扩展测试

### 添加新的测试用例

1. **创建新的测试脚本**:
   参考现有脚本的结构，创建新的测试文件。

2. **更新综合测试脚本**:
   在 `run_all_logging_tests.py` 中添加新的测试脚本。

### 自定义测试数据

修改 `test_logging_setup.py` 中的数据创建逻辑，添加更多测试数据。

## 注意事项

1. **测试环境隔离**: 测试会创建和删除数据，建议在开发环境中运行。

2. **数据清理**: 测试脚本会自动清理创建的测试数据，但建议定期清理测试日志。

3. **并发测试**: 避免同时运行多个测试脚本，可能会导致数据冲突。

4. **权限要求**: 某些测试需要管理员权限，确保测试用户具有相应权限。

## 联系支持

如果在使用测试脚本过程中遇到问题，请检查:
1. Django项目配置是否正确
2. 数据库连接是否正常  
3. 相关模型和视图是否正确实现
4. API端点是否存在并可访问