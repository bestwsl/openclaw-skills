---
name: github-headroom
title: Headroom - Context Compression Layer for AI Agents
description: "Headroom compresses tool outputs, logs, files, and RAG chunks before they reach the LLM. 60-95% fewer tokens, same answers. Library, proxy, MCP server — supports Claude Code, Codex, Cursor, Aider, Copilot CLI and more."
tags:
  - ai-agents
  - token-compression
  - context-optimization
  - mcp
  - llm
  - proxy
  - productivity
created: 2026-06-21
author: chopratejas
repo: https://github.com/chopratejas/headroom
category: autonomous-ai-agents
---

# Headroom — The Context Compression Layer for AI Agents

**Repo:** https://github.com/chopratejas/headroom  
**Stars:** 42,600+ (June 2026)  
**License:** Apache 2.0  
**Author:** [chopratejas](https://github.com/chopratejas)

## What Is It?

Headroom compresses everything your AI agent reads — tool outputs, logs, RAG chunks, files, and conversation history — **before** it reaches the LLM. Same answers, fraction of the tokens.

> **60–95% fewer tokens** · library · proxy · MCP · 6 algorithms · local-first · reversible

## Key Features

| Feature | Description |
|---------|-------------|
| **Library** | `compress(messages)` in Python or TypeScript, inline in any app |
| **Proxy** | `headroom proxy --port 8787` — zero code changes, any language |
| **Agent Wrap** | `headroom wrap claude \| codex \| cursor \| aider \| copilot` in one command |
| **MCP Server** | Tools: `headroom_compress`, `headroom_retrieve`, `headroom_stats` for any MCP client |
| **Cross-agent Memory** | Shared store across Claude, Codex, Gemini — auto-dedup |
| **headroom learn** | Mines failed sessions, writes corrections to `CLAUDE.md` / `AGENTS.md` |
| **Output Token Reduction** | Trims what the model writes back — drops ceremony/restated code |
| **Reversible (CCR)** | Originals cached for retrieval on demand |

## Architecture

```
Your agent/app → Headroom (local) → Compressed prompt → LLM provider
                     │
    CacheAligner → ContentRouter → SmartCrusher (JSON)
                                     CodeCompressor (AST)
                                     Kompress-base (text)
```

- **ContentRouter** — detects content type, selects the right compressor
- **SmartCrusher / CodeCompressor / Kompress-base** — compress JSON, AST, or prose
- **CacheAligner** — stabilizes prefixes so provider KV caches actually hit
- **CCR** — stores originals locally; LLM calls `headroom_retrieve` if needed

## Quick Start

```bash
# Install
pip install "headroom-ai[all]"          # Python
npm install headroom-ai                 # Node / TypeScript

# Pick your mode
headroom wrap claude                    # wrap a coding agent
headroom proxy --port 8787              # drop-in proxy
# or: from headroom import compress      # inline library

# See the savings
headroom perf
```

## Token Savings (Proven)

| Workload | Before | After | Savings |
|----------|-------:|------:|--------:|
| Code search (100 results) | 17,765 | 1,408 | **92%** |
| SRE incident debugging | 65,694 | 5,118 | **92%** |
| GitHub issue triage | 54,174 | 14,761 | **73%** |
| Codebase exploration | 78,502 | 41,254 | **47%** |

**Accuracy preserved:** GSM8K ±0.000, TruthfulQA +0.030

## Agent Compatibility

| Agent | `headroom wrap` | Notes |
|-------|:---------------:|-------|
| Claude Code | ✅ | `--memory` · `--code-graph` |
| Codex | ✅ | shares memory with Claude |
| Cursor | ✅ | prints config — paste once |
| Aider | ✅ | starts proxy + launches |
| Copilot CLI | ✅ | starts proxy + launches |
| OpenClaw | ✅ | installs as ContextEngine plugin |

Any OpenAI-compatible client works via `headroom proxy`. MCP-native: `headroom mcp install`.

## Integrations

| Setup | Hook |
|-------|------|
| Any Python app | `compress(messages, model=…)` |
| Any TypeScript app | `await compress(messages, { model })` |
| Anthropic / OpenAI SDK | `withHeadroom(new Anthropic())` |
| Vercel AI SDK | `wrapLanguageModel({ middleware: headroomMiddleware() })` |
| LiteLLM | `litellm.callbacks = [HeadroomCallback()]` |
| LangChain | `HeadroomChatModel(your_llm)` |
| Agno | `HeadroomAgnoModel(your_model)` |
| ASGI apps | `app.add_middleware(CompressionMiddleware)` |

## Why This Matters for AI Agents

Every token sent to an LLM costs money and context window space. Headroom lets you:

1. **Work with larger contexts** — fit more information into the same window
2. **Reduce costs** — 60-95% fewer tokens = 60-95% lower API costs
3. **Speed up agents** — less tokens to process = faster responses
4. **Cross-agent memory** — one agent's learnings available to another
5. **No code changes** — the proxy mode transparently compresses everything

## Usage Patterns

### Pattern 1: Wrap a coding agent
```bash
headroom wrap claude --memory
# Claude now gets compressed context automatically
```

### Pattern 2: Proxy mode (zero code change)
```bash
headroom proxy --port 8787
# Point any OpenAI-compatible client at localhost:8787
```

### Pattern 3: Library mode (inline)
```python
from headroom import compress

compressed = compress(messages)
```

### Pattern 4: MCP integration
```bash
headroom mcp install
# Adds headroom_compress, headroom_retrieve, headroom_stats tools
```

## When to Use

**Great for:**
- Daily AI coding agent usage
- Multi-agent workflows needing shared memory
- Reversible compression needs (CCR)
- Cost reduction on large-scale LLM usage

**Skip if:**
- Using a single provider's native compaction
- Working in sandboxed environments where local processes can't run

## Learned

Using Headroom can dramatically improve agent efficiency and reduce costs. The proxy mode is the most frictionless — zero code changes. The `headroom learn` feature is particularly powerful for iterative improvement.
