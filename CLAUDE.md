# CLAUDE.md - Croupier Proto 规范文档

**重要：本文档定义了强制性规范，任何修改必须严格遵守！**

---

## ⚠️ 版本锁定警告 - 必读！

**禁止随意修改任何版本号！** 版本不匹配会导致所有 SDK 编译失败。

如果你（Claude）想要修改版本，**必须先询问用户确认**，并说明：
1. 为什么要改
2. 改动会影响哪些 SDK
3. 需要同步修改哪些文件

**历史教训**：版本问题已经反复出现三个多月，每次随意改版本都会导致 CI 失败。

---

## 核心版本锁定表（不可变更）

### Protobuf 生态版本 - 锁定 v25.1

| 组件 | 版本 | 说明 |
|------|------|------|
| wellknowntypes | v25.1 | buf.yaml deps |
| protoc (remote plugin) | v25.1 | buf.gen.yaml |
| grpc (remote plugin) | v1.71.0 | buf.gen.yaml |

### SDK Runtime 依赖版本对应表

| SDK | 依赖包 | 版本 | 配置文件 |
|-----|--------|------|----------|
| **Java** | protobuf-java | 3.25.1 | build.gradle |
| **Java** | grpc-* | 1.71.0 | build.gradle |
| **Go** | google.golang.org/protobuf | v1.36.11 | go.mod |
| **Go** | google.golang.org/grpc | v1.71.0 | go.mod |
| **Python** | protobuf | 4.25.1 | pyproject.toml |
| **Python** | grpcio | 1.71.0 | pyproject.toml |
| **C++** | protobuf (vcpkg) | 4.25.1 | vcpkg.json |
| **C++** | grpc (vcpkg) | 1.71.0 | vcpkg.json |
| **C++** | abseil (vcpkg) | 20240722.0 | vcpkg.json |
| **C#** | Google.Protobuf | 3.25.1 | *.csproj |
| **C#** | Grpc.Net.Client | 2.71.0 | *.csproj |
| **JS/TS** | @bufbuild/protobuf | 2.2.3 | package.json |
| **JS/TS** | @connectrpc/connect | 2.0.0 | package.json |

---

## buf.gen.yaml 模板（带固定版本）

### Go SDK / Server

```yaml
version: v2
plugins:
  - remote: buf.build/protocolbuffers/go:v1.36.11
    out: pkg/pb
    opt:
      - paths=source_relative
  - remote: buf.build/grpc/go:v1.5.1
    out: pkg/pb
    opt:
      - paths=source_relative
```

### Java SDK

```yaml
version: v2
plugins:
  - remote: buf.build/protocolbuffers/java:v25.1
    out: generated
  - remote: buf.build/grpc/java:v1.71.0
    out: generated
```

### Python SDK

```yaml
version: v2
plugins:
  - remote: buf.build/protocolbuffers/python:v25.1
    out: generated
  - remote: buf.build/grpc/python:v1.71.0
    out: generated
```

### C++ SDK

```yaml
version: v2
plugins:
  - remote: buf.build/protocolbuffers/cpp:v25.1
    out: generated
  - remote: buf.build/grpc/cpp:v1.71.0
    out: generated
```

### C# SDK

```yaml
version: v2
plugins:
  - remote: buf.build/protocolbuffers/csharp:v25.1
    out: generated
  - remote: buf.build/grpc/csharp:v1.71.0
    out: generated
```

### JavaScript/TypeScript SDK

JS/TS 使用 Connect-ES 2.0 架构，只需要 protoc-gen-es（版本由 package.json 控制）：

```yaml
version: v2
plugins:
  - local: protoc-gen-es
    out: src/gen
    opt:
      - target=ts
```

**注意**：Connect-ES 2.0 不再需要 protoc-gen-connect-es，service 定义由 protoc-gen-es 直接生成。

---

## buf.yaml 模板

```yaml
version: v2
modules:
  - path: .
deps:
  - buf.build/protocolbuffers/wellknowntypes:v25.1
```

---

## Buf 配置版本 - 强制 v2

**所有 buf.yaml 和 buf.gen.yaml 必须使用 `version: v2`，禁止使用 v1！**

```yaml
# 正确 ✅
version: v2

# 错误 ❌ - 禁止使用
version: v1
```

---

## 禁止事项

1. **禁止修改 remote plugin 版本**（除非用户明确要求升级）
2. **禁止修改 SDK runtime 依赖版本**（必须与 remote plugin 版本匹配）
3. **禁止使用不带版本号的 remote plugin**（如 `buf.build/protocolbuffers/java` 不带 `:v29.5`）
4. **禁止在任何 buf 配置文件中使用 `version: v1`**
5. **禁止混用 v1 和 v2 语法**

---

## 版本升级流程（仅当用户要求时）

如果需要升级版本，必须按以下步骤执行：

1. **确认新版本号**
   - 查看 buf.build registry 获取最新 remote plugin 版本
   - 查看各语言的 runtime 版本对应关系

2. **同步修改以下文件**
   - `croupier-proto/CLAUDE.md` - 更新版本对应表
   - `croupier-proto/.github/workflows/sync-sdks.yml` - 更新 remote plugin 版本
   - 各 SDK 的依赖配置文件

3. **测试验证**
   - 手动触发 sync-sdks workflow
   - 确认所有 SDK CI 通过

---

## Workflow 检查清单

修改 `.github/workflows/sync-sdks.yml` 前，检查：

- [ ] 所有 remote plugin 都带版本号（如 `:v25.1`）
- [ ] 版本号与本文档的版本对应表一致
- [ ] buf.yaml 的 deps 使用 `v25.1`
- [ ] 所有 buf.gen.yaml 使用 `version: v2`

---

## 快速验证命令

```bash
# 验证配置格式
buf config ls-modules

# 测试生成
buf generate --debug
```

---

**最后更新：2026-01-31**
**此文档为强制性规范，违反将导致 CI 失败**
**版本锁定：protoc v25.1 / grpc v1.71.0**
