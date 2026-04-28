#!/bin/bash
# 白圭自动备份脚本
# 备份 workspace（核心人格 + 记忆 + 工具配置）到 git

WORKSPACE="$HOME/.openclaw/workspace"
LOG="$WORKSPACE/.openclaw/backup.log"
DATE=$(date '+%Y-%m-%d %H:%M')

cd "$WORKSPACE" || exit 1

# 备份 openclaw 主配置
cp "$HOME/.openclaw/openclaw.json" "$WORKSPACE/.openclaw/config.json.backup" 2>/dev/null

# 检测是否有变更
if git status --porcelain | grep -q .; then
    git add -A
    git commit -m "🔄 自动备份 $DATE" >> "$LOG" 2>&1
    echo "[$DATE] ✅ 备份完成" >> "$LOG"
else
    echo "[$DATE] ⏭️ 无变更，跳过" >> "$LOG"
fi

# 保留最近 30 天日志
tail -n 100 "$LOG" > "$LOG.tmp" && mv "$LOG.tmp" "$LOG"
