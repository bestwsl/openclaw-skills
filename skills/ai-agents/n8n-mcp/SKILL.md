---
title: n8n-mcp
name: n8n-mcp
description: MCP server that gives AI assistants (Claude, Cursor, Windsurf, Codex) comprehensive access to n8n's 1,650 workflow automation nodes for building workflows via natural language.
tags: [n8n, mcp, workflow-automation, claude, cursor, ai-agents]
---

# n8n-mcp — AI-Powered n8n Workflow Builder

## 项目简介

[n8n-mcp](https://github.com/czlonkowski/n8n-mcp) 是一个 Model Context Protocol (MCP) 服务器，它为 AI 助手（Claude Desktop/Code、Cursor、Windsurf、Codex 等）提供了对 n8n 工作流自动化平台的完整访问能力。通过它，AI 可以直接搜索 n8n 节点文档、查询模板、构建和验证工作流。

- **Stars:** 21,000+
- **License:** MIT
- **当前版本:** 2.52.x

## 核心功能

1. **1,650 个 n8n 节点全覆盖** — 820 个核心节点 + 830 个社区节点（741 已验证），含详细 Schema
2. **工作流模板库** — 2,352 个工作流模板，99.96% 有 AI 元数据覆盖
3. **节点验证** — 多级验证（minimal / full / strict），确保配置无误
4. **n8n API 管理** — 创建工作流、更新、删除、执行测试、凭证管理、安全审计
5. **多 IDE 支持** — Claude Code、VS Code、Cursor、Windsurf、Codex 均可接入

## 安装方式

### 最快方式（云端 SaaS，无需安装）

访问 [dashboard.n8n-mcp.com](https://dashboard.n8n-mcp.com)
- 免费层: 100 次工具调用/天
- 注册获取 API Key 即可连接 MCP 客户端

### npx 本地运行

```bash
# 直接通过 npx 运行
npx n8n-mcp

# 配置环境变量
export N8N_API_URL=https://your-n8n-instance.com
export N8N_API_KEY=your-api-key
```

### Docker

```bash
docker run -d \
  --name n8n-mcp \
  -p 3000:3000 \
  -e N8N_API_URL=https://your-n8n-instance.com \
  -e N8N_API_KEY=your-api-key \
  ghcr.io/czlonkowski/n8n-mcp:latest
```

## MCP 配置示例

### Claude Desktop

编辑 `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "n8n": {
      "command": "npx",
      "args": ["n8n-mcp"],
      "env": {
        "N8N_API_URL": "http://localhost:5678",
        "N8N_API_KEY": "your-api-key"
      }
    }
  }
}
```

### Cursor

在 Cursor Settings > MCP Servers 中添加:
```
Name: n8n
Type: command
Command: npx n8n-mcp
Environment variables:
  N8N_API_URL=http://localhost:5678
  N8N_API_KEY=your-api-key
```

## 核心 MCP 工具

### 搜索与文档 (7 个工具)
| 工具 | 功能 |
|------|------|
| `tools_documentation()` | 获取所有工具的文档（从这里开始！） |
| `search_nodes({query, includeExamples})` | 全文搜索所有节点 |
| `get_node({nodeType, detail, mode})` | 获取节点信息（minimal/standard/full/docs/versions） |
| `validate_node({nodeType, config, mode})` | 验证节点配置 |
| `validate_workflow(workflow)` | 完整工作流验证（含 AI Agent） |
| `search_templates({searchMode, ...})` | 模板搜索（5 种模式：keyword/by_nodes/by_task/by_metadata） |
| `get_template(templateId, {mode})` | 获取模板完整 JSON |

### n8n 管理 (13 个工具)
| 工具 | 功能 |
|------|------|
| `n8n_create_workflow` | 创建工作流 |
| `n8n_get_workflow` | 获取工作流 |
| `n8n_update_full_workflow` | 全量更新工作流 |
| `n8n_update_partial_workflow` | 增量更新（推荐，节省 Token） |
| `n8n_delete_workflow` | 删除工作流 |
| `n8n_list_workflows` | 列出工作流 |
| `n8n_validate_workflow` | 验证已部署的工作流 |
| `n8n_autofix_workflow` | 自动修复常见错误 |
| `n8n_workflow_versions` | 版本管理与回滚 |
| `n8n_deploy_template` | 从模板直接部署 |
| `n8n_test_workflow` | 测试/触发工作流执行 |
| `n8n_executions` | 执行管理（列表/查看/删除） |
| `n8n_manage_credentials` | 凭证管理 |
| `n8n_audit_instance` | 安全审计 |

## 注意事项

- **永远不要直接用 AI 编辑生产环境的工作流！** 先复制再测试
- 默认参数值是运行时失败的第一大原因 — 始终显式配置所有参数
- IF 节点有两个输出（TRUE/FALSE），需要使用 `branch` 参数路由
- 推荐工作流：模板优先 → 节点发现 → 验证 → 构建 → 多级验证 → 部署

## 适用场景

- 自动化日常工作流（通知、数据同步、审批）
- AI Agent 驱动的业务流程
- DevOps 监控与告警
- CRM/营销自动化
- 与 LLM 结合实现智能工作流编排
