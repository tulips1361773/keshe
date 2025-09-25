# 前端 esbuild 平台不匹配错误修复文档

## 错误描述

在运行前端开发服务器时遇到以下错误：

```
Error:
You installed esbuild for another platform than the one you're currently using.
This won't work because esbuild is written with native code and needs to
install a platform-specific binary executable.

Specifically the "@esbuild/win32-x64" package is present but this platform
needs the "@esbuild/win32-ia32" package instead.
```

## 错误分析

### 根本原因
esbuild 是一个用原生代码编写的构建工具，需要安装特定平台的二进制可执行文件。错误发生的原因是：

1. **平台架构不匹配**：系统中安装了 `@esbuild/win32-x64` 包，但当前平台需要 `@esbuild/win32-ia32` 包
2. **依赖缓存问题**：npm 缓存中可能保存了错误平台的二进制文件
3. **node_modules 污染**：现有的 node_modules 目录包含了不兼容的平台特定文件

### 常见触发场景
- 在不同操作系统之间复制 node_modules 文件夹
- 在 Windows 和 WSL 环境之间共享项目文件
- 使用了不匹配当前平台架构的预编译二进制文件
- 从其他开发环境迁移项目时未重新安装依赖

## 解决方案

### 步骤 1：清理现有依赖
```powershell
# 进入前端项目目录
cd frontend

# 删除 node_modules 目录
Remove-Item -Recurse -Force node_modules
```

### 步骤 2：清理 npm 缓存
```powershell
# 强制清理 npm 缓存
npm cache clean --force
```

### 步骤 3：重新安装依赖
```powershell
# 重新安装所有依赖，让 npm 为当前平台安装正确的二进制文件
npm install
```

### 步骤 4：验证修复
```powershell
# 启动开发服务器验证问题已解决
npm run dev
```

## 预防措施

1. **避免跨平台复制 node_modules**
   - 在不同环境间迁移项目时，只复制源代码
   - 在目标环境重新运行 `npm install`

2. **使用 .gitignore 排除 node_modules**
   ```gitignore
   node_modules/
   ```
