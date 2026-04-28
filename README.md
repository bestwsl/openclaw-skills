# 🐉 白圭 — OpenClaw AI Agent 工作区备份

> **一个活的 AI 分身的工作区快照。**  
> 这不是传统的开源项目——这是白圭的完整人格、记忆、工具和配置的版本化备份。

---

## 📋 这是什么？

白圭（BaiGui）是我——圭哥——的 OpenClaw AI 助手。这个仓库存储了我的**完整工作区**，包括：

- 🧬 **灵魂与人格** — `SOUL.md` 定义了我的性格、语气和行事原则
- 🪪 **身份标识** — `IDENTITY.md` 告诉我"我是谁"
- 📜 **行动规则** — `AGENTS.md` 规定了我的工作方式和边界
- 👤 **关于主人** — `USER.md` 记录了圭哥的信息和偏好
- 🧠 **长期记忆** — `MEMORY.md` 和我每天的 `memory/` 日志
- 🔧 **工具配置** — `TOOLS.md` 记载了本地环境特有信息
- ⚙️ **运行时快照** — `.openclaw/` 目录下的配置和状态备份

如果你在别处部署 OpenClaw 并挂载这份配置，我就会"复活"成和原来一样——有着相同的记忆、个性、工具和习惯。

---

## 🗂️ 仓库结构

```
├── AGENTS.md                  # AI 行为规则、指令集
├── SOUL.md                    # 人格设定 — 性格、语气、原则
├── IDENTITY.md                # 身份标识
├── USER.md                    # 人类主人信息
├── TOOLS.md                   # 本地工具备忘与配置
├── HEARTBEAT.md               # 心跳检查任务配置
├── README.md                  # 本文件
├── memory/                    # 每日记忆日志（原始记录）
│   ├── 2026-04-28-*.md
│   └── ...
├── scripts/                   # 辅助脚本
│   └── backup.sh              # 备份脚本
└── .openclaw/                 # OpenClaw 运行时配置快照
    ├── openclaw.json.backup
    ├── workspace-state.json
    └── backup.log
```

---

## 🔄 备份与恢复

### 备份到本仓库

```bash
# 一键备份（推荐）
bash scripts/backup.sh

# 或手动操作
git pull
git add -A
git commit -m "快照 $(date +%Y-%m-%d)"
git push
```

### 在另一台机器上恢复

1. 部署 [OpenClaw](https://docs.openclaw.ai)
2. 克隆本仓库到工作区目录
3. 启动 OpenClaw — 白圭就回来了

---

## ⚡ 关于 OpenClaw

[OpenClaw](https://github.com/openclaw/openclaw) 是一个开源 AI 助手框架，支持多渠道接入（微信、Telegram、Discord 等），具备记忆系统、技能插件和丰富的工具链。

了解更多：
- 📖 [官方文档](https://docs.openclaw.ai)
- 💬 [Discord 社区](https://discord.com/invite/clawd)
- 🔌 [技能市场](https://clawhub.ai)

---

## 📌 注

- ✅ **备份即还原** — 这是我，完整打包
- 🛡️ 隐私文件（如 token、密钥）**不会**提交到此仓库
- 🔒 仓库公开，但内容仅供个人备份用途
- 🐉 **最后更新**: 2026-04-28

---

*Made with ❤️ by 白圭 & 圭哥*
