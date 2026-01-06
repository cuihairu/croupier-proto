# Protobuf 版本对应关系

本文档记录各语言 SDK 的 protobuf 版本对应关系，确保跨语言兼容性。

## 目标版本

所有 SDK 应基于 **protoc v29.x** 生成代码，确保二进制格式兼容。

## 版本对应表

| 语言 | SDK 版本 | 对应 protoc | 证据来源 |
|------|---------|-------------|---------|
| **C++** | 5.29.5 | v29.x | [protobuf.dev 版本支持表](https://protobuf.dev/support/version-support/) |
| **Java** | 4.29.1 | v29.x | [protobuf.dev 版本支持表](https://protobuf.dev/support/version-support/) |
| **Go** | v1.36.0 | v29.1 | [GitHub Release Notes](https://github.com/protocolbuffers/protobuf-go/releases/tag/v1.36.0) |
| **Python** | Buf CLI v1.28.1 | v29.x | Buf 远程插件 |
| **JavaScript/TypeScript** | Buf CLI v1.28.1 | v29.x | Buf 远程插件 |

## 官方证据

### C++ 和 Java 版本对应

根据 [protobuf.dev 官方版本支持文档](https://protobuf.dev/support/version-support/)：

```
Release support chart

| Protobuf C++ | protoc | 24Q1 | 24Q2 | 24Q3 | 24Q4 |
|--------------|--------|------|------|------|------|
| 5.x          | 26.x-29.x | 5.26 | 5.27 | 5.28 | 5.29 |

| Protobuf Java | protoc | 24Q1 | 24Q2 | 24Q3 | 24Q4 |
|---------------|--------|------|------|------|------|
| 4.x           | 26.x-33.x | 4.26 | 4.27 | 4.28 | 4.29 |
```

**关键规则**：protoc 版本可以从 Protobuf C++ 的次版本号推断。
例如：Protobuf C++ 5.29.x 使用 protoc 29.x。

### Go 版本对应

根据 [protobuf-go GitHub Releases](https://github.com/protocolbuffers/protobuf-go/releases)：

| protoc-gen-go 版本 | 对应 protoc | Release Notes |
|-------------------|-------------|---------------|
| v1.34.2 | v27.0 | `types/descriptorpb: regenerate using latest protobuf v27.0 release` |
| v1.35.x | v28.x | intermediate versions |
| v1.36.0 | v29.1 | `types/descriptorpb: regenerate using latest protobuf v29.1 release` |
| v1.37.x | v30.x+ | future versions |

## 为什么版本需要匹配

1. **二进制兼容性**：虽然 protobuf 的二进制格式在不同版本间保持兼容，但生成的代码 API 可能不同
2. **描述符兼容性**：`descriptor.pb` 文件在不同 protoc 版本间可能不兼容
3. **编译错误**：使用不匹配的版本会导致如 `SetHasBit`、`CheckHasBit` 等函数未声明的编译错误

## 历史问题

之前 CI 使用 `apt-get install protobuf-compiler` 安装的 protoc 版本是 **3.21.x**（Ubuntu 系统仓库版本），与 vcpkg 的 protobuf 5.29.5 运行时版本不兼容，导致：

```
error: "Protobuf C++ gencode is built with an incompatible version of"
error: "Protobuf C++ headers/runtime"
error: use of undeclared identifier 'SetHasBit'
```

## 版本锁定策略

### CI/CD 配置

所有 SDK 的 CI 工作流锁定到固定版本：

- **C++**: vcpkg 分支 `2025.01.13`（确保 protobuf 5.29.5）
- **Go**: `protoc-gen-go@v1.36.0`, `protoc-gen-go-grpc@v1.3.0`
- **Python/JS**: Buf CLI `v1.28.1`
- **Java**: Gradle protobuf plugin `0.9.4` with protoc `4.29.1`

### 升级流程

当需要升级 protobuf 版本时：

1. 查阅 [protobuf.dev 版本支持文档](https://protobuf.dev/support/version-support/)
2. 查阅各语言的 GitHub Releases 页面找到对应版本
3. 同步更新所有 SDK 的 CI 配置
4. 更新本文档

## 参考链接

- [Protobuf 官方版本支持](https://protobuf.dev/support/version-support/)
- [protobuf-go Releases](https://github.com/protocolbuffers/protobuf-go/releases)
- [protobuf C++ Releases](https://github.com/protocolbuffers/protobuf/releases)
- [Buf CLI 版本发布](https://github.com/bufbuild/buf/releases)
