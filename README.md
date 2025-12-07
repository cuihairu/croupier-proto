# croupier-proto

[![Sync SDKs](https://github.com/cuihairu/croupier-proto/actions/workflows/sync-sdks.yml/badge.svg)](https://github.com/cuihairu/croupier-proto/actions/workflows/sync-sdks.yml)

> Croupier 平台所有 gRPC/Protobuf 契约的唯一来源（source of truth）。  
> The canonical home for every Croupier gRPC/Protobuf contract.

## 🧭 目录结构 / Layout

| 路径 | 说明 |
| --- | --- |
| `croupier/common/*` | 共享基础类型（身份、UI、权限等） |
| `croupier/{agent,edge,server,...}` | 各个服务或 SDK 专属的 RPC/消息定义 |
| `examples/` | 演示如何使用特定 proto 的最小样例 |
| `buf.yaml`, `buf.lock` | Buf workspace 声明、依赖锁 |

该仓库通常以 Git submodule 形式被挂载到 [`cuihairu/croupier`](https://github.com/cuihairu/croupier) 主仓库、各 SDK 仓库（Go/Java/JS/Python/C++），以及第三方扩展中。

## 🚀 快速开始 / Quick Start

1. 安装依赖
   - [Buf CLI](https://buf.build/docs/installation) ≥ 1.30
   - `protoc` ≥ 3.21（仅在本地需要直接调用 `protoc` 时）
2. 校验
   ```bash
   buf lint
   buf breaking --against buf.build/cuihairu/croupier-proto
   ```
3. 生成代码（根据需要选择模板）
   ```bash
   # 默认模板（生成 Go + gRPC）
   buf generate --template buf.gen.yaml

   # 本地预览额外语言
   buf generate --template buf.gen.local.yaml
   ```

> 所有 SDK 仓库都直接提交生成后的代码文件，因此 CI 只需要 `go test`/`npm test` 等常规步骤，不再重复下载 proto。

## 🔁 自动同步 / Automation

- `proto/.github/workflows/sync-sdks.yml` 会在 `main` 推送后触发，拉取各 SDK 仓库，运行对应的生成脚本，并推送更新的 `.pb.*` 文件。
- 需要在本仓库设置 `SDK_SYNC_TOKEN`，一个有写各 SDK 仓库权限的 PAT。
- 若要扩展到新的语言，只需在同一个 workflow 新增 job，并在目标 SDK 仓库实现 `scripts/generate_proto.*`（或其他约定脚本）。

当前自动同步的仓库：

| 语言 | 仓库 | 入口 |
| --- | --- | --- |
| Server / Agent / Edge（主仓） | [cuihairu/croupier](https://github.com/cuihairu/croupier) | 直接引用 `proto/` 子模块（需手动 `git submodule update`） |
| Go | [cuihairu/croupier-sdk-go](https://github.com/cuihairu/croupier-sdk-go) | `sdks/go/scripts/generate_proto.go`（workflow 自动运行） |
| C++ | [cuihairu/croupier-sdk-cpp](https://github.com/cuihairu/croupier-sdk-cpp) | CMake `ProtoGeneration.cmake`（CI 模式，workflow 自动运行） |
| Java | [cuihairu/croupier-sdk-java](https://github.com/cuihairu/croupier-sdk-java) | `./gradlew --no-daemon clean build`（workflow 自动运行并提交） |
| JS/TS | [cuihairu/croupier-sdk-js](https://github.com/cuihairu/croupier-sdk-js) | `pnpm install && pnpm run generate && pnpm run build`（workflow 自动运行） |
| Python | [cuihairu/croupier-sdk-python](https://github.com/cuihairu/croupier-sdk-python) | `uv pip install --system ".[dev]" && uv run --system pytest`（workflow 自动运行） |

> Workflow 目前会在 proto 变更后自动同步主仓以及五个 SDK，保持多语言实现一致。

## 🧱 贡献流程 / Contributing

1. 修改 `croupier/` 下的 `.proto` 文件。
2. 运行 `buf lint` 与相关 `buf generate` 命令，确保没有 breaking change 或 lint 错误。
3. 更新示例/文档（若接口有新增字段或语义变更）。
4. 提交 PR，说明影响范围和版本规划（默认沿用语义化版本，必要时更新 SDK README 中的兼容矩阵）。

## ❓ 常见问题 / FAQ

- **为什么用 Buf？** Buf 提供 lint、breaking change 检查、统一生成配置，可避免多语言 SDK 之间的不一致。
- **如何引用特定版本？** 以 Git tag（例如 `proto/v2024.12.0`）标记，每个 SDK 再根据 tag 进行升级。
- **可以直接在 SDK 仓库修改 proto 吗？** 不建议。请在这里修改然后依赖自动同步；手动改动很容易与主仓库脱节。

欢迎提 Issue 或 PR，一起维护 Croupier 协议生态。💕
