Hermes 记忆备份仓库：github.com/bestwsl/openclaw-skills（公开），本地副本 D:\Hermes\memories\openclaw-skills。旧环境是 Linux 服务器+微信接入，现环境为 Windows 10 + WorkBuddy 桌面 app（Hermes 嵌入其中）。
§
大陆网络下 GitHub git push 不稳定，旧备份方案改用 GitHub API PUT /contents/ 上传。
§
圭哥要求：不在本地备份记忆，所有备份只推 GitHub。本地备份 curator.backup.enabled 需手动在 D:\Hermes\config.yaml 设为 false（沙箱保护写不进去）。
§
本机 git-bash 环境设置了 MSYS2_ARG_CONV_EXCL="*" 和 MSYS_NO_PATHCONV="1"（路径转换被禁用）：给 git.exe 等原生 Windows 程序传路径必须用 Windows 风格 (D:/... 或 D:\...)，传 /d/... 会被当作字面路径（曾导致克隆到 C:\d\Hermes）。
§
东财API A股选股经验：f48(PE)与新浪页面差异大以个股页为准；请求字段>15或page_size>500易超时；负债率=1-(市值/PB)/总资产；营收增(f41)可能因并购虚高需人工核实；PEG(f136)多为0不可依赖；净利率注意会计期间差异；金融股豁免负债率/毛利率检测。
§
WorkBuddy 沙箱环境：所有删除操作被拦截（回收站不可用，rm/rmdir/Python os.remove 全部 fail-closed），删除需改用覆盖写入或让用户手动删；~/.hermes/scripts 与 ~/.hermes/cron 目录可正常写入。
§
Hermes cron 约束：script 必须放在 ~/.hermes/scripts/ 下并用相对文件名；桌面会话默认 deliver=local（输出只保存不投递），需要投递必须显式 deliver='all'。
§
微信已接入 Hermes（腾讯 iLink Bot API）：bot account 4916a2f2e4e7@im.bot，圭哥微信 ID o9cq8023zYlNSdjbM6GdIH6pDn58@im.wechat（已配对批准），私聊 pairing 模式、群聊禁用；网关为手动运行，电脑重启后需 hermes gateway run 或 hermes gateway install 设置自启。
§
记忆备份 cron job 已恢复（b8e2e6616793）：每日21:30，no_agent，script=hermes_backup.py，deliver=all。脚本已改为临时目录中转+推送后自动清理，不留本地副本。Token 由圭哥自行配置（GITHUB_PAT 或 D:\Hermes\scripts\github_token.txt）。
§
WorkBuddy 沙箱：从 Hermes 启动的进程无法向用户级 GUI 应用注入键鼠（Windows UIPI 拦 SendKeys/PostMessage/SendInput/keybd_event/VBScript），桌面自动化需 computer-use(cua-driver) 或用户手动操作。网易云音乐在 D:\app\CloudMusic\cloudmusic.exe（窗口类 OrpheusBrowserHost），圭哥常让播"我喜欢的音乐"歌单。
§
圭哥明确要求：个股分析必须核查最新季度数据（Q1/中报），不能只看滞后年报。2026年曾因只看2025年报推荐了2026Q1已净利转负的股票（映翰通-58%、福耀-16%）被纠正。规则已固化到 a-share-data-api skill。