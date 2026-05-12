Hermes Agent 的记忆已备份到 GitHub: https://github.com/bestwsl/openclaw-skills
  - hermes-agent-IDENTITY.md — 身份
  - hermes-agent-SOUL.md — 人格
  - hermes-agent-MEMORY.md — 长期记忆
  - memory/2026-04-29-hermes-backup.md — 当日会话日志
  Git push 在大陆网络不稳定，改用 GitHub API PUT /contents/ 成功上传
§
每天 21:30 (晚上9:30) Asia/Shanghai
§
Check recent file writes and memory for context on "两份文件"
§
用户圭哥反映提取文件时我会卡死。
§
用户圭哥反馈我（Hermes Agent）会崩溃/卡死，需要自我修复检查。待排查根因。
§
圭哥触发 /repair 自我修复指令，需要全面诊断 Hermes Agent 状态
§
[修复] 2026-04-30 reasoning_content 400 错误修复：代码已补丁并 git commit 到仓库。根因：custom provider (10.0.2.3) 使用推理模型但 _supports_reasoning_extra_body() 返回 False。修复：在 _build_api_kwargs 中添加 `_has_reasoning_in_history()` 嵌套函数，检测历史消息有 reasoning_content 时自动添加 reasoning extra_body。`elif _has_reasoning_in_history(api_messages):` 分支已添加。Gateway 重启后生效（PID 17189→32062）。新增 reasoning_content 字段写入 assistant message，summary 路径也添加了 _summary_has_reasoning 处理。
§
2026-04-29 维修记录：reasoning_content 400 错误代码已修复，但 Gateway 进程未重启，导致旧代码仍在运行。通过 kill -TERM 优雅重启 Gateway（PID 521→17189），新代码生效。同时创建了每日 10:30 纳斯达克七姐妹涨跌播报定时任务。
§
圭哥触发 /repair 自我修复指令，需要全面诊断 Hermes Agent 状态。检查项：内存完整性、工具可用性、技能目录、近期错误、定时任务健康、GitHub 备份状态。
§
股票报告定时任务不能依赖AI模型知识（无搜索工具会编造数据），必须提供具体URL让浏览器访问新浪财经/Yahoo Finance获取实时数据，并在提示词中明确"不得编造任何数字"。
§
每天17:00 GitHub学习新技能后，必须将新创建的 skill 推送到 GitHub 仓库 (https://github.com/bestwsl/openclaw-skills)。使用 github-api-push skill 进行推送（因大陆 git push 不稳定）。更新 cron job prompt 增加此步骤。
§
移远通信产品系列介绍定时任务：每天12:00发一个系列，共10天。顺序：5G→4G/LTE→LPWA→智能→车载→GNSS→短距离→天线→卫星通信→3G/2G。脚本 ~/.hermes/scripts/quectel_tracker.py 管理进度。