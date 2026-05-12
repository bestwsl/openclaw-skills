---
name: react-doctor
category: software-development
description: Scan your React/Next.js codebase with one command for AI-generated bad code — scores 0-100, catches state, performance, security, accessibility, and dead code issues. By Million (millionco).
---

# react-doctor

**Your agent writes bad React. This catches it.**

One command scans your React/Next.js/Vite/React Native codebase and outputs a **0–100 health score** with actionable diagnostics. Built by [Million](https://github.com/millionco/react-doctor).

- **GitHub:** https://github.com/millionco/react-doctor
- **Stars:** 8.4k+
- **Language:** TypeScript

## Quick Start

```bash
# Scan your project
npx -y react-doctor@latest .

# Install for your coding agent (Claude Code, Cursor, Codex, etc.)
npx -y react-doctor@latest install
```

## Score Ranges

| Score | Meaning |
|-------|---------|
| 75+   | ✅ Great |
| 50–74 | ⚠️ Needs work |
| <50   | 🔴 Critical |

## Categories Checked

- **State & Effects** — cascading setState, derived useState, missing deps
- **Performance** — unnecessary re-renders, heavy computations in render
- **Architecture** — component coupling, prop drilling, file organization
- **Security** — dangerouslySetInnerHTML, XSS vectors
- **Accessibility** — missing ARIA labels, keyboard navigation
- **Dead Code** — unused imports, variables, exports

## GitHub Actions

Add `.github/workflows/react-doctor.yml` to your repo:

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

## Configuration

Create `react-doctor.config.json`:

```json
{
  "ignore": {
    "rules": ["react/no-danger"],
    "files": ["src/generated/**"],
    "overrides": [
      {
        "files": ["components/diff/**"],
        "rules": ["react-doctor/no-array-index-as-key"]
      }
    ]
  }
}
```

## Inline Suppressions

```jsx
// react-doctor-disable-next-line react-doctor/no-cascading-set-state
useEffect(() => {
  setA(value);
  setB(value);
}, [value]);
```

## Caveats

- Requires Node.js (uses npx)
- First run downloads the package; subsequent runs are cached
- Respects `.gitignore`, `.eslintignore`, `.prettierignore`
- Honors `// eslint-disable*` and `// oxlint-disable*` comments
