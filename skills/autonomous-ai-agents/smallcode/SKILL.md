---
name: smallcode
category: autonomous-ai-agents
description: AI coding agent optimized for small LLMs (7B-20B parameters). Terminal-native, context-budget-aware, with forgiving tool call parsing, TODO-driven planning, and model escalation.
---

# SmallCode — AI Coding Agent for Small LLMs

**GitHub**: https://github.com/Doorman11991/smallcode
**Stars**: ⭐593 (as of 2026-05-19)
**License**: MIT
**Language**: JavaScript (Node.js)

## 项目简介

SmallCode 是一个专为**小参数本地模型（7B-20B）** 设计的终端 AI 编码代理。与 OpenCode/Claude Code 等需要前沿大模型（128K+ 上下文、完美工具调用）的工具不同，SmallCode 通过智能架构补偿小模型的局限性，在消费级硬件上就能运行。

**核心对比**：

| 特性 | OpenCode | SmallCode |
|------|----------|-----------|
| 目标模型 | 前沿模型（Claude, GPT-5） | 7B-20B 本地模型 |
| 上下文 | 全部倒入 | 预算管理、智能摘要 |
| 工具调用 | 假设可靠 JSON | 多格式容错解析器 |
| 规划 | 单次生成 | TODO 文件分解步骤 |
| 编辑 | 全文件写入 | 搜索替换式 patch |
| 隐私 | 云端 API | 完全本地，无需网络 |

## 安装方式

```bash
# 全局安装
npm install -g smallcode

# 或直接使用 npx
npx smallcode
```

**依赖**（随 smallcode 自动安装）：
- [BoneScript](https://github.com/Doorman11991/BoneScript) — 声明式后端代码生成
- [budget-aware-mcp](https://github.com/Doorman11991/budget-aware-mcp) — 上下文预算感知 MCP

**系统要求**：Node.js 18+（推荐 20.x/22.x LTS）

## 基本用法

### 1. 启动

```bash
cd my-project
smallcode
```

### 2. 配置 `.env`

```bash
# 必需
SMALLCODE_MODEL=your-model-name
SMALLCODE_BASE_URL=http://localhost:1234/v1

# 可选：失败时自动回退到云端模型
# ANTHROPIC_API_KEY=***
# OPENAI_API_KEY=***
# DEEPSEEK_API_KEY=***
```

### 3. 程序化 API

```javascript
const { SmallCode } = require('smallcode');

const agent = new SmallCode({
  model: 'gemma-4-e4b',
  baseUrl: 'http://localhost:1234/v1',
});

const result = await agent.run("create hello.py that prints hello world");
console.log(result.filesCreated);  // ['hello.py']
console.log(result.success);      // true

// 订阅事件
agent.on('tool_start', ({ name, args }) => console.log(`Using: ${name}`));
agent.on('tool_end', ({ name, ms }) => console.log(`Done: ${name} (${ms}ms)`));
```

## 核心功能

### MarrowScript 认知层
用声明式 `.marrow` 文件定义智能行为，编译为带缓存、重试、验证、追踪和预算执行的生产代码。

```marrow
prompt classify_task_type(user_message: string) {
  model: TinyClassifier
  timeout: 3s
  cache: { key: hash(user_message), ttl: 10m }
  constraints: [output in ["coding", "editing", "search", ...]]
}
```

### 上下文预算引擎
- 工具结果上限 4K 字符
- 中间轮次自动淘汰旧结果
- 语义压缩替代丢弃

### 2 阶段工具路由
模型先选类别（读/写/搜索/运行/规划），再加载相关工具模式。节省约 50% 上下文开销，对 8-16K 上下文的模型至关重要。

### 容错工具调用解析器
可解析 JSON、YAML、XML、Hermes 格式甚至纯文本中的工具调用。自动修复常见错误（参数名错误、类型不匹配）。

### Patch 优先编辑
搜索-替换作为主要编辑原语。小模型无法可靠重写完整文件（会截断、幻觉或偏移）。`patch` 更安全、更节省上下文。

### 模型升级（Escalation）
本地模型失败后可选择升级到云端模型：
- Claude Sonnet 4.5 / 4.6, Haiku 4.5
- GPT-5.4 Mini / Nano
- DeepSeek V4 / V4 Pro / V4 Flash

## 内置工具

| 工具 | 描述 |
|------|------|
| `bone_compile` | 编译 .bone 为完整后端项目 |
| `bone_check` | 校验 .bone 文件 |
| `graph_search` | 代码图符号搜索 |
| `explain_symbol` | 符号解析（调用者/被调用者） |
| `read_file` | 读取文件 |
| `write_file` | 创建/覆盖文件 |
| `patch` | 搜索-替换编辑 |
| `bash` | 运行命令 |
| `search` | 正则搜索（ripgrep） |
| `find_files` | 通配符文件搜索 |
| `memory_load` | 加载项目记忆 |
| `memory_remember` | 保存知识到记忆 |
| `web_search` | DuckDuckGo 网页搜索 |
| `web_fetch` | 获取 URL 文本内容 |

## 关键命令

| 命令 | 描述 |
|------|------|
| `/q`, `/quit` | 退出 |
| `/clear` | 重置对话 |
| `/stats` | 会话统计 |
| `/tokens` | Token 使用详情 |
| `/budget` | 上下文预算可视化 |
| `/trace` | 执行追踪 |
| `/memory` | 显示工作记忆 |
| `/plan` | 当前任务计划 |
| `/model` | 查看/切换模型 |
| `/eval` | 运行评估套件 |
| `/skill` | 管理可复用技能 |
| `/plugin` | 安装/管理插件 |

## 评估模式

```bash
# 从 CLI 运行评估
smallcode --eval classify_accuracy
smallcode --eval tool_selection
```

## 适用场景

1. **离线开发**：在无网络环境中用本地模型进行编码
2. **隐私敏感项目**：代码不离开本地机器
3. **低成本开发**：无需支付 API 费用，消费级 GPU 即可运行
4. **小型模型研究**：测试和对比 7B-20B 模型的编码能力
5. **CI/CD 自动化**：通过程序化 API 集成到流水线
6. **学习 AI Agent 架构**：研究小模型代理的优化策略
