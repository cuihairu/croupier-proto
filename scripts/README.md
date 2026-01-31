# Scripts 目录

此目录包含用于本地开发和维护的辅助脚本。

## sync-sdks.sh - 本地 SDK 同步脚本

当 GitHub Actions 卡住或需要快速本地测试时，可以使用此脚本手动同步 proto 文件到各个 SDK 仓库。

### 前置要求

1. 安装 [Buf CLI](https://docs.buf.build/installation)
2. 所有 SDK 仓库已克隆到本地（默认在 `../` 目录下）
3. 对于 JavaScript SDK，需要先安装依赖（`pnpm install`）

### 基本用法

```bash
# 从 croupier-proto 根目录执行
./scripts/sync-sdks.sh

# 同步所有 SDK 到默认路径 (../)
./scripts/sync-sdks.sh all

# 同步指定的 SDK
./scripts/sync-sdks.sh go
./scripts/sync-sdks.sh go,python,cpp

# 指定 SDK 仓库的基础路径
./scripts/sync-sdks.sh -p ~/Workspaces go

# 预演模式（不实际修改文件）
./scripts/sync-sdks.sh -d cpp
```

### 支持的 SDK

- `go` - croupier-sdk-go
- `python` - croupier-sdk-python
- `java` - croupier-sdk-java
- `js` - croupier-sdk-js
- `cpp` - croupier-sdk-cpp
- `csharp` - croupier-sdk-csharp
- `server` - croupier (主服务器仓库)
- `all` - 所有 SDK

### 示例

#### 1. 快速测试单个 SDK

```bash
# 只同步 Go SDK
./scripts/sync-sdks.sh go
```

#### 2. 同步多个 SDK

```bash
# 同步 Go 和 Python SDK
./scripts/sync-sdks.sh go,python
```

#### 3. 预演模式

```bash
# 查看 C++ SDK 同步会做什么，但不实际执行
./scripts/sync-sdks.sh -d cpp
```

#### 4. 自定义 SDK 路径

```bash
# 如果你的 SDK 仓库在其他位置
./scripts/sync-sdks.sh -p /path/to/workspaces all
```

### 脚本功能

- ✅ 自动检测 `buf` 命令是否安装
- ✅ 支持预演模式（dry-run）
- ✅ 彩色输出，易于阅读
- ✅ 错误处理和验证
- ✅ 显示生成的文件数量
- ✅ 与 GitHub Actions workflow 使用相同的配置

### 同步后操作

脚本执行完成后，生成的代码会自动提交到各个 SDK 仓库的本地 Git 仓库。你需要手动检查并推送：

```bash
# 进入 SDK 目录
cd ../croupier-sdk-go

# 检查改动
git status

# 如果满意，提交并推送
git add .
git commit -m "chore: sync proto from croupier-proto"
git push origin main
```

### 故障排除

#### buf 命令未找到

```bash
# macOS
brew install bufbuild/buf/buf

# Linux
curl -sSL https://github.com/bufbuild/buf/releases/latest/download/buf-Linux-x86_64 -o /usr/local/bin/buf
chmod +x /usr/local/bin/buf
```

#### SDK 仓库路径不存在

确保你的目录结构如下：

```
Workspaces/
├── croupier-proto/        # Proto 定义仓库
├── croupier-sdk-go/       # Go SDK
├── croupier-sdk-python/   # Python SDK
├── croupier-sdk-java/     # Java SDK
├── croupier-sdk-js/       # JavaScript SDK
├── croupier-sdk-cpp/      # C++ SDK
├── croupier-sdk-csharp/   # C# SDK
└── croupier/              # Server 仓库
```

如果在不同位置，使用 `-p` 参数指定：

```bash
./scripts/sync-sdks.sh -p /your/custom/path all
```

#### JavaScript SDK 失败

确保已安装 Node.js 依赖：

```bash
cd ../croupier-sdk-js
pnpm install
cd ../croupier-proto
./scripts/sync-sdks.sh js
```

### 版本配置

脚本使用的版本配置与 `.github/workflows/sync-sdks.yml` 一致：

- **Protobuf:** v25.1 (4.25.x)
- **gRPC:** v1.71.0
- **Go Plugin:** v1.36.11
- **Go gRPC Plugin:** v1.5.1

这些版本锁定确保所有 SDK 的一致性和兼容性。
