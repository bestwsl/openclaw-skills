# agentmemory — Persistent Memory for AI Coding Agents

## 项目简介

[agentmemory](https://github.com/rohitg00/agentmemory) 是专为 AI 编码代理设计的持久化内存系统。它能够自动捕获代理在每个会话中的操作、决策和上下文，并将其压缩为可搜索的结构化记忆，在下个会话开始时自动注入最相关的上下文。

- **GitHub**: https://github.com/rohitg00/agentmemory
- **Stars**: 6,425+
- **License**: Apache-2.0
- **语言**: TypeScript (基于 iii-engine)

## 核心亮点

| 指标 | 数据 |
|------|------|
| 检索精度 R@5 | **95.2%** (LongMemEval-S) |
| Token 节省 | **92% 更少** (年约 $10) |
| MCP 工具 | **51 个** |
| 自动 Hook | **12 个**生命周期钩子 |
| 外部依赖 | **零** (SQLite + iii-engine) |

## 快速开始

### 30 秒体验

```bash
# 终端 1：启动内存服务器
npx @agentmemory/agentmemory

# 终端 2：填充示例数据
npx @agentmemory/agentmemory demo
```

打开 `http://localhost:3113` 查看实时内存面板。

### MCP 服务器集成

在任何支持 MCP 的代理配置中添加：

```json
{
  "mcpServers": {
    "agentmemory": {
      "command": "npx",
      "args": ["-y", "@agentmemory/mcp"],
      "env": {
        "AGENTMEMORY_URL": "http://localhost:3111"
      }
    }
  }
}
```

支持：Claude Code、Cursor、Codex CLI、Gemini CLI、Cline、Roo Code、Windsurf、OpenClaw、Hermes Agent、Aider、Goose 等。

### 从源码安装

```bash
git clone https://github.com/rohitg00/agentmemory.git
cd agentmemory
npm install
npm run build
npm start
```

## 各代理集成

### Claude Code (一键粘贴)

```
Install agentmemory: run `npx @agentmemory/agentmemory` in a separate terminal to start the memory server. Then run `/plugin marketplace add rohitg00/agentmemory` and `/plugin install agentmemory`.
```

### Codex CLI

```bash
npx @agentmemory/agentmemory
codex plugin marketplace add rohitg00/agentmemory
codex plugin install agentmemory
```

### Hermes Agent

```yaml
mcp_servers:
  agentmemory:
    command: npx
    args: ["-y", "@agentmemory/mcp"]

memory:
  provider: agentmemory
```

## 核心 MCP 工具

### 核心工具 (始终可用)
| 工具 | 描述 |
|------|------|
| `memory_recall` | 搜索历史观察记录 |
| `memory_save` | 保存洞察、决策或模式 |
| `memory_smart_search` | 混合语义 + 关键词搜索 |
| `memory_sessions` | 列出最近会话 |
| `memory_timeline` | 按时间线查看 |
| `memory_profile` | 项目画像 |

### 高级工具 (AGENTMEMORY_TOOLS=all)
| 工具 | 描述 |
|------|------|
| `memory_graph_query` | 知识图谱遍历 |
| `memory_snapshot_create` | Git 版本化快照 |
| `memory_signal_send` | 代理间消息传递 |
| `memory_lease` | 多代理排他操作锁 |
| `memory_diagnose` | 健康检查 |
| `memory_heal` | 自动修复卡住状态 |
| `memory_governance_delete` | 审计删除 |

## 内存架构

PostToolUse hook -> SHA-256 去重(5min) -> 隐私过滤器 -> 存储原始观察
-> LLM 压缩 -> 结构化事实+概念 -> 向量嵌入 -> BM25+向量索引

4 层整合：
- **Working**: 原始工具调用 (短期记忆)
- **Episodic**: 会话摘要 ("发生了什么")
- **Semantic**: 事实和模式 ("我知道什么")
- **Procedural**: 工作流和决策模式 ("怎么做")

## 嵌入提供商

```bash
npm install @xenova/transformers   # 推荐：本地离线免费嵌入
```

| 提供商 | 模型 | 成本 |
|--------|------|------|
| Local (推荐) | all-MiniLM-L6-v2 | 免费 |
| Gemini | text-embedding-004 | 免费额度 |
| OpenAI | text-embedding-3-small | $0.02/1M |
| Voyage AI | voyage-code-3 | 付费 |

## 适用场景

1. **多代理协作**: 多个代理共享同一记忆库
2. **大型项目**: 记住架构、约定、历史决策
3. **长周期任务**: 跨越数天的开发无需重复学习
4. **团队知识管理**: 跨团队共享经验

## 关键命令

```bash
npx @agentmemory/agentmemory          # 启动服务器
npx @agentmemory/agentmemory demo     # 演示模式
npx @agentmemory/agentmemory upgrade  # 升级
npx @agentmemory/mcp                  # 独立 MCP 模式
curl http://localhost:3111/agentmemory/health  # 健康检查
open http://localhost:3113             # 实时查看器
```

## vs 竞品

| 维度 | agentmemory | mem0 | Letta/MemGPT | CLAUDE.md |
|------|------------|------|-------------|-----------|
| R@5 | **95.2%** | 68.5% | 83.2% | N/A |
| 自动捕获 | 12 hooks | 手动 | 自编辑 | 手动 |
| 搜索 | BM25+向量+图谱 | 向量+图谱 | 向量 | 全加载 |
| 外依赖 | 无 (SQLite) | Qdrant | Postgres+向量 | 无 |
| Token | ~1900/会话 | 不定 | Core mem | 22K+ |
