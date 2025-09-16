# 教练员查询与选择功能 - 测试文档

## 概述

本文档描述了教练员查询与选择功能的全面测试方案，包括后端API测试、前端功能测试和端到端集成测试。

## 测试架构

```
测试体系
├── 后端API测试 (test_coach_selection_backend.py)
│   ├── 教练员列表查询API
│   ├── 教练员筛选和搜索API
│   └── 师生关系管理API
├── 前端功能测试 (frontend/test_coach_selection_frontend.html)
│   ├── 组件渲染测试
│   ├── 用户交互测试
│   └── API集成测试
├── 端到端测试 (test_coach_selection_e2e.py)
│   ├── 页面导航测试
│   ├── 完整流程测试
│   └── 数据一致性验证
└── 测试执行器 (run_all_tests.py)
    └── 统一执行和报告生成
```

## 测试文件说明

### 1. 后端API测试 (`test_coach_selection_backend.py`)

**功能**: 测试Django后端API接口的功能和性能

**测试内容**:
- 教练员列表查询API (`/accounts/api/coaches/`)
- 教练员筛选功能（性别、年龄、等级等）
- 教练员搜索功能（姓名关键词）
- 师生关系创建API (`/api/reservations/relations/`)
- 师生关系删除API
- 权限验证和错误处理

**运行方式**:
```bash
python test_coach_selection_backend.py
```

**输出**: `test_coach_selection_backend_report.json`

### 2. 前端功能测试 (`frontend/test_coach_selection_frontend.html`)

**功能**: 测试Vue.js前端组件的渲染和交互

**测试内容**:
- 教练员选择组件渲染
- 搜索框和筛选器交互
- 教练员卡片显示
- 选择/取消选择功能
- API调用和响应处理
- 错误处理和用户反馈

**运行方式**:
1. 确保前端服务器运行在 `http://localhost:5173`
2. 在浏览器中打开 `frontend/test_coach_selection_frontend.html`
3. 点击测试按钮执行各项测试

**特点**:
- 可视化测试界面
- 实时测试进度显示
- 详细的测试结果报告

### 3. 端到端测试 (`test_coach_selection_e2e.py`)

**功能**: 使用Selenium模拟真实用户操作流程

**测试内容**:
- 页面导航和加载
- 教练员列表显示
- 搜索功能完整流程
- 筛选功能完整流程
- 教练员选择完整流程
- 我的教练员管理
- 前后端数据一致性验证

**运行方式**:
```bash
python test_coach_selection_e2e.py
```

**依赖**:
- Chrome浏览器
- ChromeDriver
- Selenium库

**输出**: 
- `test_coach_selection_e2e_report.json`
- 截图文件（测试过程中的关键页面）

### 4. 测试执行器 (`run_all_tests.py`)

**功能**: 统一执行所有测试并生成综合报告

**运行方式**:
```bash
python run_all_tests.py
```

**输出**: `comprehensive_test_report.json`

## 测试环境要求

### 服务器要求
- **后端服务器**: Django运行在 `http://localhost:8000`
- **前端服务器**: Vue.js运行在 `http://localhost:5173`

### 启动服务器
```bash
# 启动后端服务器
python manage.py runserver

# 启动前端服务器（在frontend目录下）
npm run dev
```

### 依赖安装
```bash
# Python依赖
pip install requests selenium

# 前端依赖
cd frontend
npm install
```

### 浏览器要求
- Chrome浏览器（用于端到端测试）
- ChromeDriver（需要与Chrome版本匹配）

## 测试数据准备

### 数据库要求
1. **用户组**: 确保存在"学员"和"教练员"用户组
2. **教练员数据**: 至少5个教练员记录，包含不同性别、年龄、等级
3. **学员数据**: 至少1个测试学员账户

### 测试用户
测试会自动创建以下测试用户：
- 后端测试用户: `backend_test_student`
- 端到端测试用户: `e2e_test_student`

## 执行测试

### 快速开始
1. 确保服务器运行
2. 执行统一测试脚本：
```bash
python run_all_tests.py
```

### 单独执行测试
```bash
# 只执行后端测试
python test_coach_selection_backend.py

# 只执行端到端测试
python test_coach_selection_e2e.py

# 前端测试需要在浏览器中手动执行
```

## 测试报告

### 报告文件
- `comprehensive_test_report.json`: 综合测试报告
- `test_coach_selection_backend_report.json`: 后端API测试详细报告
- `test_coach_selection_e2e_report.json`: 端到端测试详细报告

### 报告内容
每个报告包含：
- 测试摘要（通过率、执行时间等）
- 详细测试结果
- 错误信息和调试信息
- 性能数据（响应时间等）
- 改进建议

## 常见问题

### 1. 端到端测试失败
**可能原因**:
- Chrome浏览器或ChromeDriver未安装
- 前后端服务器未运行
- 网络连接问题

**解决方案**:
```bash
# 安装ChromeDriver（Windows）
# 下载对应版本的ChromeDriver并添加到PATH

# 检查服务器状态
curl http://localhost:8000/accounts/api/coaches/
curl http://localhost:5173
```

### 2. 后端API测试失败
**可能原因**:
- Django服务器未运行
- 数据库连接问题
- 权限配置错误

**解决方案**:
```bash
# 检查Django服务器
python manage.py runserver

# 检查数据库迁移
python manage.py migrate

# 创建测试数据
python manage.py shell
```

### 3. 前端测试无法访问
**可能原因**:
- 前端服务器未运行
- 端口被占用
- 构建失败

**解决方案**:
```bash
# 重新启动前端服务器
cd frontend
npm run dev

# 检查端口占用
netstat -ano | findstr :5173
```

## 测试最佳实践

### 1. 测试前准备
- 确保数据库有足够的测试数据
- 清理之前的测试用户和关系记录
- 检查服务器日志确保无错误

### 2. 测试执行
- 按顺序执行：后端 → 前端 → 端到端
- 保存测试日志和截图
- 记录测试环境信息

### 3. 结果分析
- 查看详细的JSON报告
- 分析失败原因
- 检查性能指标
- 根据建议进行优化

## 扩展测试

### 性能测试
可以扩展后端测试以包含：
- 并发用户测试
- 大数据量测试
- 响应时间基准测试

### 安全测试
可以添加：
- SQL注入测试
- XSS攻击测试
- 权限绕过测试

### 兼容性测试
可以扩展端到端测试以支持：
- 多浏览器测试（Firefox, Safari等）
- 移动端测试
- 不同屏幕分辨率测试

## 维护和更新

### 定期维护
- 更新测试数据
- 检查依赖版本
- 更新测试用例

### 版本控制
- 测试脚本纳入版本控制
- 记录测试结果历史
- 跟踪性能变化趋势

---

**最后更新**: 2024年1月
**维护者**: 开发团队
**联系方式**: 项目仓库Issues