# CLAUDE.md - Croupier Proto 规范文档

**重要：本文档定义了强制性规范，任何修改必须严格遵守！**

## 核心规范（不可变更）

### 1. Buf 配置版本 - 强制 v2

**所有 buf.yaml 和 buf.gen.yaml 必须使用 `version: v2`，禁止使用 v1！**

```yaml
# 正确 ✅
version: v2

# 错误 ❌ - 禁止使用
version: v1
```

**原因：**
- v1 不支持 `remote:` 插件语法
- v1 的 `managed` 配置语法不同
- v2 是当前稳定版本，统一使用避免兼容性问题

### 2. Protobuf 依赖版本 - 固定 v29.3 (对应 protobuf 5.29.x)

```yaml
deps:
  - buf.build/protocolbuffers/wellknowntypes:v29.3
```

**禁止升级或降级此版本，除非经过完整的跨 SDK 兼容性测试。**

### 3. Buf CLI 版本 - 使用最新版本

GitHub Actions workflow 中使用最新版本即可：
```yaml
- uses: bufbuild/buf-setup-action@v1
  with:
    github_token: ${{ github.token }}
```

## buf.gen.yaml 模板

### Go SDK / Server

```yaml
version: v2
plugins:
  - remote: buf.build/protocolbuffers/go
    out: generated
  - remote: buf.build/grpc/go
    out: generated
```

或本地插件方式：
```yaml
version: v2
managed:
  enabled: true
  override:
    - file_option: go_package_prefix
      value: github.com/cuihairu/croupier/pkg/pb
plugins:
  - local: protoc-gen-go
    out: pkg/pb
    opt:
      - paths=source_relative
  - local: protoc-gen-go-grpc
    out: pkg/pb
    opt:
      - paths=source_relative
```

### Java SDK

```yaml
version: v2
plugins:
  - remote: buf.build/protocolbuffers/java
    out: generated
  - remote: buf.build/grpc/java
    out: generated
```

### Python SDK

```yaml
version: v2
plugins:
  - remote: buf.build/protocolbuffers/python
    out: croupier/pb
```

### C++ SDK

```yaml
version: v2
plugins:
  - remote: buf.build/protocolbuffers/cpp
    out: generated
  - remote: buf.build/grpc/cpp
    out: generated
```

### C# SDK

```yaml
version: v2
plugins:
  - remote: buf.build/protocolbuffers/csharp
    out: src/Gen
```

### JavaScript/TypeScript SDK

```yaml
version: v2
plugins:
  - local: protoc-gen-es
    out: src/gen
    opt:
      - target=ts
      - import_extension=.ts
  - local: protoc-gen-connect-es
    out: src/gen
    opt:
      - target=ts
      - import_extension=.ts
```

## buf.yaml 模板

```yaml
version: v2
modules:
  - path: .
deps:
  - buf.build/protocolbuffers/wellknowntypes:v29.3
```

## 禁止事项

1. **禁止在任何 buf 配置文件中使用 `version: v1`**
2. **禁止在 v1 格式中使用 `remote:` 语法**（v1 只支持 `name:` 和 `plugin:`）
3. **禁止混用 v1 和 v2 语法**
4. **禁止修改 wellknowntypes 版本**（锁定 v29.3）
5. ~~Buf CLI 版本不锁定，使用最新版即可~~

## Workflow 文件检查清单

修改 `.github/workflows/sync-sdks.yml` 前，检查：

- [ ] 所有生成的 buf.gen.yaml 使用 `version: v2`
- [ ] 使用 `remote:` 语法时必须是 v2 格式
- [ ] buf.yaml 的 deps 使用 `v29.3`
- [ ] bufbuild/buf-setup-action 使用最新版本（不指定 version）

## 快速验证命令

```bash
# 验证配置格式
buf config ls-modules

# 测试生成
buf generate --debug
```

---

**最后更新：2026-01-11**
**此文档为强制性规范，违反将导致 CI 失败**
