---
name: react-doctor
category: software-development
description: Scan React/Next.js codebases for AI-generated bad code — one command gives a 0-100 health score with actionable diagnostics. Works with 50+ coding agents.
---

# React Doctor — AI-Generated React Code Quality Scanner

**GitHub**: https://github.com/millionco/react-doctor
**Author**: millionco (by aidenybai)
**Stars**: 9,500+ | **License**: MIT | **Language**: TypeScript

## 简介

React Doctor 是一款专门扫描 React/Next.js 代码库中常见问题的 CLI 工具，尤其擅长检测 AI 编码助手（如 Claude Code、Cursor、Codex、OpenCode 等）生成的糟糕代码。一条命令即可输出 0-100 的健康评分和可操作的诊断建议。

## 核心功能

1. **一键扫描评分** — 输出 0-100 健康分（75+ 优秀，50-74 需改进，<50 严重）
2. **六大检查维度** — State & Effects、Performance、Architecture、Security、Accessibility、Dead Code
3. **AI Agent 集成** — 自动检测 50+ 编码助手并为它们安装最佳实践规则文件
4. **GitHub Actions 支持** — 可在 PR 中自动评论发现问题，支持 diff 模式只扫描变更文件
5. **可配置规则** — 支持忽略规则、文件、特定覆盖；兼容 ESLint/Oxlint 规则继承
6. **Node.js API** — 提供编程接口 `diagnose()` 用于脚本集成

## 安装

```bash
# 扫描项目
npx -y react-doctor@latest .

# 为 AI 编码助手安装最佳实践规则
npx -y react-doctor@latest install
```

## 评分公式

```
分数 = 100 - (unique_error_rules × 1.5) - (unique_warning_rules × 0.75)
```

分数按"规则种类"而非"违规次数"计算，修复同一规则的多次违规只会扣一次分。

| 分数 | 等级 |
|------|------|
| 75+  | ✅ 优秀 |
| 50–74 | ⚠️ 需改进 |
| <50  | 🔴 严重 |

## CLI 命令参考

```bash
# 扫描指定目录
react-doctor .

# 仅扫描变更的文件（对比 main 分支）
react-doctor --diff main

# 仅扫描暂存区文件（用于 pre-commit hook）
react-doctor --staged

# 仅输出分数（用于 CI 阈值检查）
react-doctor --score

# JSON 格式输出（所有人类可读输出都被抑制）
react-doctor --json

# 详细输出（显示每个规则和文件详情）
react-doctor --verbose

# 诊断某个诊断为何触发/为何抑制不生效
react-doctor --explain src/App.tsx:10
# 或使用别名
react-doctor --why src/App.tsx:10

# 设置失败级别（error / warning / none）
react-doctor --fail-on warning

# 输出 GitHub Actions annotations 格式
react-doctor --annotations

# 跳过 linting
react-doctor --no-lint

# 跳过死代码检测
react-doctor --no-dead-code
```

## GitHub Actions 配置

```yaml
name: React Doctor
on:
  pull_request:
  push:
    branches: [main]
permissions:
  contents: read
  pull-requests: write
jobs:
  react-doctor:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v5
        with:
          fetch-depth: 0
      - uses: millionco/react-doctor@main
        with:
          diff: main
          github-token: ${{ secrets.GITHUB_TOKEN }}
```

## 配置文件 `react-doctor.config.json`

```json
{
  "ignore": {
    "rules": ["react/no-danger"],
    "files": ["src/generated/**"],
    "overrides": [
      {
        "files": ["components/diff/**"],
        "rules": ["react-doctor/no-array-index-as-key"]
      },
      {
        "files": ["components/search/HighlightedSnippet.tsx"],
        "rules": ["react/no-danger"]
      }
    ]
  }
}
```

三个层级：`ignore.rules`（全局忽略规则）、`ignore.files`（全局忽略文件）、`ignore.overrides`（按文件覆盖特定规则）。

配置文件也可写在 `package.json` 的 `"reactDoctor"` 键中。CLI 标志始终优先于配置文件。

## 内联抑制

```jsx
// react-doctor-disable-next-line react-doctor/no-cascading-set-state
useEffect(() => {
  setA(value);
  setB(value);
}, [value]);
```

单行多规则：
```jsx
// react-doctor-disable-next-line react-doctor/rerender-state-only-in-handlers, react-doctor/no-derived-useState
const [localSearch, setLocalSearch] = useState(searchQuery);
```

JSX 中（花括号注释）：
```jsx
{/* react-doctor-disable-next-line react/no-danger */}
<div dangerouslySetInnerHTML={{ __html }} />
```

## Node.js API

```typescript
import { diagnose, toJsonReport, summarizeDiagnostics } from "react-doctor/api";

const result = await diagnose("./path/to/project");
console.log(result.score); // { score: 82, label: "Great" } or null
console.log(result.diagnostics); // Diagnostic[]
console.log(result.project); // detected framework, React version

const report = toJsonReport(result, { version: "1.0.0" });
const counts = summarizeDiagnostics(result.diagnostics);
```

## 可选插件

| 插件 | 说明 |
|------|------|
| eslint-plugin-react-hooks (v6/v7) | React Compiler 前端的正确性规则 |
| eslint-plugin-react-you-might-not-need-an-effect (v0.10+) | 补充的 Effects 反模式规则 |

## 支持框架

- Next.js
- Vite (React)
- React Native
- TanStack Start
- TanStack Query

## 检查规则类别

| 类别 | 示例规则 |
|------|---------|
| State & Effects | `no-fetch-in-effect`, `no-derived-state-effect`, `no-cascading-set-state` |
| Performance | `no-array-index-as-key`, `no-barrel-import`, `no-render-in-render` |
| Architecture | `no-direct-effect-ref-act`, `no-default-export-arrow` |
| Security | `no-danger` (dangerouslySetInnerHTML) |
| Accessibility | `no-autofocus`, `no-missing-alt` |
| Dead Code | 未使用的导出、组件、文件 |

## 注意事项

- 需要 Node.js（使用 npx）
- 首次运行会下载包，后续运行有缓存
- 尊重 `.gitignore`, `.eslintignore`, `.oxlintignore`, `.prettierignore`
- 尊重 `// eslint-disable*` 和 `// oxlint-disable*` 注释
- 支持 `.gitattributes` 中的 `linguist-vendored` / `linguist-generated` 注解
- 如果项目有 `.oxlintrc.json` 或 `.eslintrc.json` 配置，会自动合并其规则
- `--staged` 和 `--diff` 不能同时使用，且两种模式都会跳过死代码检测
- 不同版本间分数可能下降（新规则加入），建议在 CI 中固定版本
