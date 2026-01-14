# Security Policy

## Supported Versions

Croupier Proto 作为 gRPC/Protobuf 契约定义库，与主项目版本同步维护：

| Version | Supported          |
| ------- | ------------------ |
| main    | :white_check_mark: |

## Reporting a Vulnerability

如果您发现安全漏洞（如契约定义中的敏感信息泄露风险），请通过以下方式负责任地披露：

1. **请勿** 在公开的 GitHub Issues 中报告安全漏洞
2. 发送邮件至项目维护者，或通过 [GitHub Security Advisories](https://github.com/cuihairu/croupier-proto/security/advisories/new) 提交报告
3. 请在报告中包含：
   - 漏洞描述
   - 复现步骤
   - 潜在影响
   - 如有可能，提供修复建议

## Response Timeline

- **确认收到**：48 小时内
- **初步评估**：7 个工作日内
- **修复发布**：视漏洞严重程度而定，高危漏洞优先处理

## Security Considerations

Proto 定义相关的安全注意事项：

- 避免在 proto 文件中硬编码敏感信息
- 使用 `bytes` 类型传输敏感数据，便于加密处理
- 字段编号设计考虑向后兼容性
- 定期更新 Buf 工具链和依赖版本
