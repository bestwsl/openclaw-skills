#!/bin/bash
# 白圭自动备份脚本
# 备份 workspace（核心人格 + 记忆 + 工具配置）到 git 并推送远程

WORKSPACE="$HOME/.openclaw/workspace"
LOG="$WORKSPACE/.openclaw/backup.log"
DATE=$(date '+%Y-%m-%d %H:%M')

cd "$WORKSPACE" || exit 1

# 先拉取远程最新（避免冲突）
git pull --rebase origin main >> "$LOG" 2>&1

# 检测是否有变更
if git status --porcelain | grep -q .; then
    git add -A
    git commit -m "🔄 自动备份 $DATE" >> "$LOG" 2>&1
    git push origin main >> "$LOG" 2>&1
    echo "[$DATE] ✅ 备份并推送完成" >> "$LOG"
else
    echo "[$DATE] ⏭️ 无变更，跳过" >> "$LOG"
fi

# 保留最近 100 行日志
tail -n 100 "$LOG" > "$LOG.tmp" && mv "$LOG.tmp" "$LOG"
