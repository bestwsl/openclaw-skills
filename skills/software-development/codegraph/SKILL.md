---
name: codegraph
title: CodeGraph — Pre-indexed Code Knowledge Graph for AI Coding Agents
description: Supercharge AI coding agents with a pre-indexed knowledge graph — symbol relationships, call graphs, and code structure. 94% fewer tool calls, 77% faster exploration, 100% local.
tags: [claude-code, code-intelligence, mcp, code-graph, developer-tools]
created: 2026-05-17
---

# CodeGraph — Pre-indexed Code Knowledge Graph

> **GitHub**: https://github.com/colbymchenry/codegraph  
> **Stars**: ⭐ 2.8k | **Fork**: 231 | **License**: MIT  
> **Author**: @colbymchenry  

## 简介

CodeGraph 是一个本地代码知识图谱工具，专为 AI 编程助手（如 Claude Code）设计。它通过 tree-sitter 解析源码生成 AST，构建包含符号关系、调用图、代码结构的知识图谱，存储在本地 SQLite 数据库中。AI 代理可以瞬间查询图谱，无需逐个扫描文件。

**基准测试**（6 个真实项目）：
- 平均减少 **92%** 的 tool 调用
- 平均 **71%** 更快的探索速度

## 核心功能

1. **智能上下文构建** — 一次 tool 调用获取入口点、相关符号和代码片段
2. **全文搜索** — 基于 FTS5 的即时符号搜索
3. **影响分析** — 追踪调用者/被调用者，分析变更的影响范围
4. **自动同步** — 使用原生 OS 文件事件（FSEvents/inotify）监听文件变更，自动增量更新
5. **19+ 语言支持** — TypeScript, JavaScript, Python, Go, Rust, Java, C#, PHP, Ruby, C, C++, Swift, Kotlin, Dart, Svelte, Liquid, Pascal/Delphi, Vue, Scala
6. **框架感知路由** — 自动识别 Django, Flask, FastAPI, Express, Laravel, Rails, Spring 等 13+ 框架的路由文件
7. **100% 本地** — 数据不离开本机，无 API Key，使用 SQLite 存储

## 安装

### 一键安装（推荐）

```bash
npx @colbymchenry/codegraph
```

安装器会自动：
- 全局安装 codegraph（MCP server 需要）
- 配置 MCP server 到 ~/.claude.json
- 添加全局指令到 ~/.claude/CLAUDE.md
- 可选初始化当前项目

### 手动安装 & 初始化

```bash
# 安装
npm install -g @colbymchenry/codegraph

# 在项目中初始化
cd your-project
codegraph init -i

# 重启 Claude Code 即可使用
```

## 基本用法

### CLI 命令

```bash
codegraph                         # 运行交互式安装器
codegraph install                 # 运行安装器（显式）
codegraph init [path]             # 在项目中初始化（--index 同时索引）
codegraph uninit [path]           # 移除 CodeGraph
codegraph index [path]            # 完整索引（--force 强制重索引）
codegraph sync [path]             # 增量更新
codegraph status [path]           # 查看统计信息
codegraph query <search>          # 搜索符号（--kind, --limit, --json）
codegraph files [path]            # 显示文件结构
codegraph context <task>          # 为 AI 构建上下文
codegraph affected [files...]     # 查找受变更影响的测试文件
codegraph serve --mcp             # 启动 MCP server
```

### 查找受影响测试文件

```bash
# 直接传文件
codegraph affected src/utils.ts src/api.ts

# 从 git diff 管道获取
git diff --name-only | codegraph affected --stdin

# CI hook 示例
#!/usr/bin/env bash
AFFECTED=$(git diff --name-only HEAD | codegraph affected --stdin --quiet)
if [ -n "$AFFECTED" ]; then
  npx vitest run $AFFECTED
fi
```

### MCP Tools（供 Claude Code 使用）

| Tool | 用途 |
|------|------|
| `codegraph_search` | 按名称搜索符号 |
| `codegraph_context` | 为任务构建相关代码上下文 |
| `codegraph_callers` | 查找函数的调用者 |
| `codegraph_callees` | 查找函数调用的子函数 |
| `codegraph_impact` | 分析修改符号的影响范围 |
| `codegraph_node` | 获取符号详情（含源码） |
| `codegraph_files` | 获取索引文件结构 |
| `codegraph_status` | 查看索引健康状态 |

### 库方式使用（Node.js API）

```typescript
import CodeGraph from '@colbymchenry/codegraph';

const cg = await CodeGraph.init('/path/to/project');
await cg.indexAll({ onProgress: (p) => console.log(`${p.phase}: ${p.current}/${p.total}`) });

const results = cg.searchNodes('UserService');
const callers = cg.getCallers(results[0].node.id);
const context = await cg.buildContext('fix login bug', { maxNodes: 20, includeCode: true, format: 'markdown' });
cg.watch();  // auto-sync on file changes
```

## 配置

`.codegraph/config.json`：

```json
{
  "version": 1,
  "languages": ["typescript", "javascript"],
  "exclude": ["node_modules/**", "dist/**", "build/**", "*.min.js"],
  "frameworks": [],
  "maxFileSize": 1048576,
  "extractDocstrings": true,
  "trackCallSites": true
}
```

## 适用场景

- **使用 Claude Code 或类似 AI 编码助手的开发者** — 大幅提升代码理解速度
- **大型代码库探索** — 快速理解项目结构和符号关系
- **代码审查** — 分析变更影响范围，找到受影响的测试文件
- **重构/技术债务清理** — 通过影响分析安全地进行大规模代码变更
- **CI/CD 流水线** — 自动运行受变更影响的测试文件

## 故障排除

1. **索引慢** — 检查 node_modules 等大目录是否被排除
2. **WASM 回退（性能差）** — 运行 `codegraph status` 查看 Backend 行：
   - `Backend: native` — 正常
   - `Backend: wasm` — 需安装 C 编译器后 `npm rebuild better-sqlite3`

## 工作原理

```
tree-sitter 解析源码 → AST → 提取节点（函数、类、方法）和边（调用、导入、继承）
→ 存入 SQLite（FTS5 全文搜索）→ 引用解析 → 文件监听自动同步
```
