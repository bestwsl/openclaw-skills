---
name: auto-identity-remove
description: "Automated data broker opt-out runner - removes personal info from 500+ people-search sites"
category: devops
created: 2026-05-20
---

# auto-identity-remove

自动化的数据经纪商退出运行器，每月自动从 500+ 个人搜索网站上删除你的个人信息。
支持 macOS、Linux、Windows，自动处理验证码，支持 iMessage/Discord/Slack 通知。

**GitHub:** https://github.com/stephenlthorn/auto-identity-remove
**Stars:** 557+
**语言:** JavaScript / Node.js

## 核心功能

1. **自动化数据删除** — 每月自动搜索并提交删除请求到 30+ 主流数据经纪商
2. **500+ 站点覆盖** — 通用运行器处理 490+ 额外经纪商站点（来自 The Markup 数据集）
3. **CAPTCHA 自动解决** — 通过 CapSolver API（约 $0.001/次）
4. **状态跟踪** — 90 天重检窗口，避免重复提交
5. **多平台通知** — iMessage / ntfy.sh / Slack / Discord webhook
6. **Docker 支持** — 无头运行，挂载 config.json/state.json
7. **验证模式** — `--verify` 只读检查删除是否生效

## 安装

```bash
# 1. 克隆仓库
git clone https://github.com/stephenlthorn/auto-identity-remove.git
cd auto-identity-remove

# 2. 安装依赖
npm install

# 3. 安装 Playwright 浏览器
npx playwright install chromium

# 4. 运行交互式设置（创建 config.json 并注册月度任务）
node setup.js
```

## 基本用法

```bash
# 手动运行
./run.sh

# 预览模式（不提交任何表单）
node watcher.js --dry-run

# 验证之前删除是否生效
node watcher.js --verify

# 后台运行
./run.sh >> logs/manual-run.log 2>&1 &
```

## Docker 使用

```bash
# 构建
docker build -t auto-identity-remove .

# 预览运行
echo '{}' > state.json
docker run --rm \
  -v $(pwd)/config.json:/app/config.json \
  -v $(pwd)/state.json:/app/state.json \
  auto-identity-remove node watcher.js --dry-run

# 正式运行
docker run --rm \
  -v $(pwd)/config.json:/app/config.json \
  -v $(pwd)/state.json:/app/state.json \
  auto-identity-remove
```

## 配置示例 (config.json)

```json
{
  "firstName": "John",
  "lastName": "Doe",
  "state": "CA",
  "city": "Los Angeles",
  "zip": "90001",
  "email": "john@example.com",
  "phone": "213-555-0100",
  "aliases": ["Jon Doe", "Johnny Doe"],
  "capsolver": {
    "apiKey": "CAP-xxxxxxxxxxxx"
  },
  "notify": {
    "textTo": "+1234567890",
    "webhook": "https://ntfy.sh/my-channel"
  }
}
```

## 关键命令

| 命令 | 说明 |
|------|------|
| `node setup.js` | 交互式设置向导 |
| `node watcher.js` | 主运行器 |
| `node watcher.js --dry-run` | 预览不提交 |
| `node watcher.js --verify` | 验证删除效果 |
| `node watcher.js --pollute N` | 实验：提交 N 条虚假记录 |
| `./run.sh` | 手动触发 |
| `node scripts/prune-dead.js` | 清理失效 URL |

## 支持的数据经纪商（30+ 自动删除）

Spokeo, WhitePages, FastPeopleSearch, TruePeopleSearch, BeenVerified, Intelius, PeopleFinders, MyLife, Nuwber, Acxiom, LexisNexis, ZoomInfo, Clearbit 等。

## 适用场景

- **隐私保护** — 定期从数据经纪商处删除个人信息
- **反身份盗用** — 减少个人信息被滥用的风险
- **DevOps 自动化** — 可部署为 Docker 容器定时运行
- **跨国使用** — 支持非美国用户（自动跳过美国专属站点）

## 状态图标说明

| 图标 | 含义 |
|------|------|
| ✅ Submitted | 表单已提交 |
| 📧 Awaiting email confirm | 等待邮件确认 |
| ⏭ Skipped (fresh) | 最近已移除，暂不重复 |
| 🔍 Not listed | 未找到记录 |
| 📋 Manual needed | 需要手动操作 |
| ❌ Error | 网络/超时错误 |
| 💀 Dead (stale URL) | 经纪商 URL 已失效 |
