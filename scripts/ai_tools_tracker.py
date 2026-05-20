#!/usr/bin/env python3
"""AI Tools skills tracker - weekly lessons on Wed/Sat."""
import os
import json
import sys
from datetime import datetime

STATE_FILE = os.path.expanduser("~/.hermes/cron/ai_tools_state.json")

TOPICS = [
    {
        "day": 1,
        "title": "🤖 Prompt工程 — 让AI更懂你",
        "content": (
            "**核心：好的Prompt = 明确的角色 + 具体任务 + 输出格式**\n\n"
            "**公式：**\n"
            "```\n"
            "角色（你是谁） + 任务（要做什么） + 背景（上下文） + 格式（怎么输出）\n"
            "```\n\n"
            "**❌ 不好的Prompt：**\n"
            "> 帮我写个邮件\n\n"
            "**✅ 好的Prompt：**\n"
            "> 你是移远通信技术支持工程师，要给客户写一封邮件，\n"
            "> 告知模组无法注册的问题已定位到是SIM卡接触不良，\n"
            "> 建议客户检查SIM卡座焊接和触点清洁度。\n"
            "> 语气专业友善，中英文双语版本。\n\n"
            "**技巧1：Chain of Thought（思维链）**\n"
            "> 先在脑子里一步步想清楚，再给出答案\n\n"
            "**技巧2：Few-Shot（给例子）**\n"
            "> 参考这个格式：\n"
            "> 输入：xxx → 输出：yyy\n"
            "> 现在输入：zzz → 输出：\n\n"
            "**技巧3：否定指令**\n"
            "> 不要编造数据，如果没有准确信息就说不知道\n\n"
            "**每天练一练：** 下次用AI之前，先花10秒写一个结构化的Prompt"
        ),
        "practice": (
            "**🛠 今日练习：对比Prompt效果**\n\n"
            "分别用以下两种方式问AI，对比结果：\n\n"
            "**Prompt A（模糊）：**\n"
            "> 帮我分析一下这个数据\n"
            "> 数据：模组A卖了1000个，模组B卖了800个，模组C卖了1200个\n\n"
            "**Prompt B（结构化）：**\n"
            "> 你是数据分析师。\n"
            "> 请分析以下三个产品的销售数据，\n"
            "> 找出销量最高的产品和最低的产品，\n"
            "> 计算平均销量，给出改进建议。\n"
            "> 数据：\n"
            "> - 模组A：1000个\n"
            "> - 模组B：800个\n"
            "> - 模组C：1200个\n"
            "> 输出格式：\n"
            "> 📊 分析结论：\n"
            "> 🥇 冠军：\n"
            "> 📉 短板：\n"
            "> 💡 建议：\n\n"
            "💡 你会发现，同样的AI，Prompt不同效果天差地别"
        )
    },
    {
        "day": 2,
        "title": "🤖 AI辅助编程 — 你的免费结对编程搭档",
        "content": (
            "**场景：** 写代码卡住了、要查语法、要重构、要加注释\n\n"
            "**最佳实践：**\n\n"
            "**1. 写脚本**\n"
            "> 用Python写一个脚本：\n"
            "> - 读取当前目录下所有.xlsx文件\n"
            "> - 合并每个文件的第二个Sheet的数据\n"
            "> - 输出到一个新文件\n"
            "> 要有错误处理，打印进度\n\n"
            "**2. 调试错误**\n"
            "> 这段代码报错：\n"
            "> [粘贴错误信息]\n"
            "> 帮我分析原因并修复\n\n"
            "**3. 代码重构**\n"
            "> 这段代码太长了，帮我拆成函数：\n"
            "> [粘贴代码]\n\n"
            "**4. 加注释/写文档**\n"
            "> 给这段代码加中文注释，并生成README：\n"
            "> [粘贴代码]\n\n"
            "**5. 解释代码**\n"
            "> 我是一个Python新手，请用大白话解释这段代码在做什么：\n"
            "> [粘贴代码]\n\n"
            "**💡 把AI当成你的结对编程搭档，不是取代你，是加速你**"
        ),
        "practice": (
            "**🛠 今日练习：用AI解决实际问题**\n\n"
            "找一个你工作中遇到的重复性任务，用AI帮你写脚本解决：\n\n"
            "**步骤：**\n"
            "1️⃣ 描述任务：\"我每天要手动把10个Excel合并成一个\"\n"
            "2️⃣ 让AI写出脚本\n"
            "3️⃣ 运行试试，有问题继续问AI修bug\n"
            "4️⃣ 成功之后，把它加入你的toolkit.py\n\n"
            "**Prompt模板：**\n"
            "> 我是Python新手，需要写一个脚本：\n"
            "> [详细描述你要做什么]\n"
            "> 要求：\n"
            "> - 用Python3\n"
            "> - 有详细的注释\n"
            "> - 有错误处理\n"
            "> - 打印执行进度\n\n"
            "💡 亲身实测：用AI辅助编程，学习速度提升3倍"
        )
    },
    {
        "day": 3,
        "title": "🤖 AI处理文档 — 总结翻译提取一条龙",
        "content": (
            "**场景：** 英文技术文档看不懂、长文章没时间读、需要提取关键信息\n\n"
            "**实用Prompt模板：**\n\n"
            "**1. 文档总结**\n"
            "> 请用中文总结以下英文技术文档，\n"
            "> 只保留核心技术要点，去掉广告和废话：\n"
            "> [粘贴文档内容]\n\n"
            "**2. 翻译+保留格式**\n"
            "> 把以下英文翻译成中文，\n"
            "> 保留技术术语不翻译（如AT command、MQTT等），\n"
            "> 保持原格式：\n"
            "> [粘贴文档]\n\n"
            "**3. 提取行动项**\n"
            "> 从以下会议纪要中提取：\n"
            "> 1. 决策事项\n"
            "> 2. 待办任务（谁做、什么时候完成）\n"
            "> 3. 风险点\n"
            "> [粘贴会议纪要]\n\n"
            "**4. 简化技术内容**\n"
            "> 我是刚入职的技术支持工程师，\n"
            "> 请用大白话解释以下技术概念，\n"
            "> 让初中生也能听懂：\n"
            "> [粘贴技术文档]\n\n"
            "**💡 英文技术文档再也不怕了，先扔给AI翻译摘要再精读**"
        ),
        "practice": (
            "**🛠 今日练习：翻译英文技术文档**\n\n"
            "找一份移远模组的英文Datasheet或Application Note：\n"
            "https://www.quectel.com/product/\n\n"
            "用AI做以下处理：\n\n"
            "1️⃣ 全文翻译成中文（保留技术术语）\n"
            "2️⃣ 提取核心参数表\n"
            "3️⃣ 用三句话总结这个文档\n\n"
            "**Prompt示例：**\n"
            "> 请处理以下英文技术文档：\n"
            "> 1. 先翻译成中文，技术术语保留英文\n"
            "> 2. 提取所有关键参数到一个表格\n"
            "> 3. 用三句话总结核心内容\n"
            "> [粘贴文档]\n\n"
            "💡 以后看英文Datasheet，先过AI这一遍，效率翻倍"
        )
    },
    {
        "day": 4,
        "title": "🤖 AI分析数据 — 不用学pandas也能分析",
        "content": (
            "**场景：** 有一份Excel/CSV数据，想快速出分析报告\n\n"
            "**方法：把数据丢给AI，用自然语言分析**\n\n"
            "**Prompt模板：**\n"
            "> 我有一份销售数据，格式如下：\n"
            "> [粘贴CSV前20行]\n"
            ">\n"
            "> 请帮我：\n"
            "> 1. 哪个产品卖得最好？哪个最差？\n"
            "> 2. 每天的销售趋势是怎样的？\n"
            "> 3. 有没有异常数据？\n"
            "> 4. 给出3条可执行的建议\n\n"
            "**进阶：让AI帮你写分析代码**\n"
            "> 我有这份CSV数据：\n"
            "> [粘贴数据结构]\n"
            "> 请用Python+pandas写一段代码，\n"
            "> 做以下分析：\n"
            "> 1. 各产品销量占比（饼图）\n"
            "> 2. 每日销量趋势（折线图）\n"
            "> 3. 找出销售额最高的前3天\n"
            "> 保存为 analysis_report.xlsx\n\n"
            "**💡 不一定非要自己写pandas，让AI写你跑，学多了自然就会了**"
        ),
        "practice": (
            "**🛠 今日练习：让AI分析你的数据**\n\n"
            "找一份你工作中的真实数据（脱敏后），用AI分析：\n\n"
            "```\n"
            "日期,客户,问题类型,处理时长(小时),满意度\n"
            "2026-05-01,客户A,无法注册,2,5\n"
            "2026-05-01,客户B,信号弱,1.5,4\n"
            "2026-05-02,客户A,掉线,3,3\n"
            "2026-05-02,客户C,AT指令异常,0.5,5\n"
            "2026-05-03,客户B,功耗高,4,2\n"
            "```\n\n"
            "问AI：\n"
            "1. 哪种问题花的时间最多？\n"
            "2. 哪个客户的满意度最低？\n"
            "3. 建议如何改进？\n\n"
            "💡 以后日报不用手动分析，直接粘贴数据让AI出结论"
        )
    },
    {
        "day": 5,
        "title": "🤖 AI工具链 — 这些工具值得试试",
        "content": (
            "**实用AI工具推荐：**\n\n"
            "**🆓 免费好用：**\n"
            "• **DeepSeek**（deepseek.com）— 国产强模型，编程推理都很强\n"
            "• **Kimi**（kimi.moonshot.cn）— 长文档处理强，一次读20万字\n"
            "• **豆包**（doubao.com）— 字节出品，日常对话好用\n"
            "• **通义千问**（tongyi.aliyun.com）— 阿里出品，代码能力不错\n\n"
            "**💻 开发效率：**\n"
            "• **Cursor** — AI驱动的IDE，用自然语言写代码\n"
            "• **GitHub Copilot** — VS Code里的AI编程助手\n"
            "• **Claude Code / Codex CLI** — 终端里让AI直接写代码跑\n\n"
            "**🎨 创意工具：**\n"
            "• **Napkin AI** — 文字直接生成流程图/架构图\n"
            "• **Gamma** — AI生成PPT\n"
            "• **Notion AI** — 笔记+AI写作\n\n"
            "**🔧 办公提效：**\n"
            "• **讯飞听见** — 语音转文字，开会录音自动出纪要\n"
            "• **沉浸式翻译** — 浏览器插件，双语对照翻译\n\n"
            "**💡 建议：** 每周试一个新工具，不好用就换，找到最适合自己的组合"
        ),
        "practice": (
            "**🛠 今日练习：搭建你的AI工作流**\n\n"
            "选一个你每天重复做的任务，尝试用AI改造：\n\n"
            "**示例：技术支持日报工作流**\n"
            "1. 📝 记录问题 → 用语音转文字（讯飞听见）\n"
            "2. 🤖 分析数据 → 粘贴到AI分析趋势\n"
            "3. 📄 生成报告 → AI生成日报内容\n"
            "4. ✉️ 发送邮件 → 自动生成中英文邮件\n\n"
            "**你的任务：** 画一个流程图\n"
            "```\n"
            "日常工作 → 哪一步可以用AI？ → 用什么工具？ → 预期节省多少时间？\n"
            "```\n\n"
            "💡 目标是：每周至少找到一个可以用AI提效的环节"
        )
    },
    {
        "day": 6,
        "title": "🤖 AI写邮件 — 专业得体的沟通",
        "content": (
            "**场景：** 给客户/领导写邮件，不知道措辞是否合适\n\n"
            "**Prompt模板：**\n\n"
            "**1. 写邮件**\n"
            "> 以移远技术支持工程师的身份，给客户写一封邮件：\n"
            "> 背景：客户反馈EC600S模组在低温-20℃下无法正常工作\n"
            "> 我们已经复现并修复，新固件版本V2.1.3已发布\n"
            "> 附上固件下载链接和升级步骤文档\n"
            "> 语气：专业、友善\n"
            "> 语言：中英文双语\n\n"
            "**2. 回复投诉邮件**\n"
            "> 客户对处理速度不满意，写一封安抚邮件：\n"
            "> 承认问题、说明原因、给出解决方案和时间节点\n"
            "> 态度诚恳但不卑微\n\n"
            "**3. 简化/润色**\n"
            "> 帮我润色这段邮件，让它更专业简洁：\n"
            "> [粘贴你的草稿]\n\n"
            "**4. 回复英文邮件**\n"
            "> 客户发了一封英文邮件：\n"
            "> [粘贴英文邮件]\n"
            "> 请帮我用英文回复，专业礼貌，\n"
            "> 回复要点：\n"
            "> - 已收到反馈\n"
            "> - 正在排查\n"
            "> - 预计2个工作日内给结果\n\n"
            "**💡 英文不地道？让AI润色，学它的表达方式**"
        ),
        "practice": (
            "**🛠 今日练习：客户邮件实战**\n\n"
            "假设客户发来这样一封邮件：\n\n"
            "> Hi Team,\n"
            ">\n"
            "> We are having issues with the EC600S module.\n"
            "> It fails to register on the China Mobile network\n"
            "> after firmware upgrade from V2.0 to V2.1.\n"
            "> We have 2000 devices in the field affected.\n"
            "> Please advise ASAP.\n"
            ">\n"
            "> Best regards,\n"
            "> John\n\n"
            "请你用AI：\n"
            "1️⃣ 分析客户的关键诉求\n"
            "2️⃣ 写一封专业的英文回复\n"
            "3️⃣ 再用中文写一封同步给领导的内部邮件\n\n"
            "💡 这种场景在实际工作中每天都会遇到，AI帮你又快又专业"
        )
    },
    {
        "day": 7,
        "title": "🤖 AI查资料 — 快速调研和学习",
        "content": (
            "**场景：** 要快速了解一个新技术、做竞品分析、查解决方案\n\n"
            "**Prompt模板：**\n\n"
            "**1. 快速学习新技术**\n"
            "> 我想了解5G RedCap（轻量化5G），\n"
            "> 请用费曼学习法（Feynman Technique）解释：\n"
            "> 1. 用一句话说清楚它是什么\n"
            "> 2. 它和普通5G有什么不同\n"
            "> 3. 它的核心应用场景\n"
            "> 4. 移远有没有相关的模组产品\n\n"
            "**2. 竞品对比**\n"
            "> 对比移远EC600S和广和通L610，\n"
            "> 从以下维度分析：\n"
            "> - 频段支持\n"
            "> - 功耗\n"
            "> - 尺寸\n"
            "> - 认证情况\n"
            "> - 价格区间（大概）\n"
            "> - 各自的优势\n\n"
            "**3. 方案调研**\n"
            "> 客户要在农业大棚中部署温湿度传感器，\n"
            "> 使用NB-IoT通信。\n"
            "> 请列出推荐方案：\n"
            "> - 推荐模组型号\n"
            "> - 传感器选择建议\n"
            "> - 云平台对接方案\n"
            "> - 供电方案（大棚无市电）\n\n"
            "**💡 把AI当成你的技术顾问，不懂就问，问多了知识就积累起来了**"
        ),
        "practice": (
            "**🛠 今日练习：用AI做技术调研**\n\n"
            "选一个你想深入了解的物联网技术，用AI做调研：\n\n"
            "**推荐选题：**\n"
            "1. 5G LAN是什么？对工业互联网有什么价值？\n"
            "2. Matter协议是什么？和传统智能家居协议有什么区别？\n"
            "3. eSIM vs 传统SIM卡，有什么优劣势？\n"
            "4. 卫星物联网现在发展到什么程度了？\n\n"
            "**调研框架：**\n"
            "1. 一句话定义\n"
            "2. 核心技术原理（说人话版）\n"
            "3. 行业应用场景\n"
            "4. 和现有方案的对比\n"
            "5. 移远在这个领域的布局\n\n"
            "💡 每周调研一个新技术，半年后你就是团队里的技术百科全书"
        )
    },
    {
        "day": 8,
        "title": "🤖 AI最佳实践总结 — 成为AI高手",
        "content": (
            "**回顾+进阶技巧：**\n\n"
            "**1. 结构化提示**\n"
            "好的Prompt = 角色 + 背景 + 任务 + 格式 + 约束\n\n"
            "**2. 迭代优化**\n"
            "不要指望一次完美 → 先出结果 → 不满意再细化\n"
            "> \"不够详细，再展开说说第三点\"\n"
            "> \"换个角度分析\"\n"
            "> \"用表格展示\"\n\n"
            "**3. 上下文很重要**\n"
            "不要每次重新描述，保持对话上下文\n"
            "> 同一个对话里连续追问，AI会记住前面的内容\n\n"
            "**4. 验证结果**\n"
            "AI会犯错（幻觉），重要数据一定要验证\n"
            "> \"你这个数据来源是什么？\"\n"
            "> \"请列出具体引用\"\n\n"
            "**5. 组合使用**\n"
            "AI + Python脚本 + 自动化 = 超级生产力\n"
            "> AI写脚本 → 你调试 → 定时运行 → 每天自动产出\n\n"
            "**💡 AI不会取代你，会用AI的人会取代你**"
        ),
        "practice": (
            "**🛠 今日实战：设计你的AI工作流**\n\n"
            "画一张你的个人AI工作流：\n\n"
            "```\n"
            "📥 输入 → 🤖 AI处理 → 📤 输出\n"
            "--------------------------------\n"
            "客户问题 → AI分析根因+建议方案 → 回复邮件\n"
            "日报数据 → AI分析趋势+生成报告 → 发给领导\n"
            "英文文档 → AI翻译+摘要 → 存入知识库\n"
            "代码报错 → AI诊断+修复方案 → 修复bug\n"
            "新技术 → AI调研+总结 → 分享给团队\n"
            "```\n\n"
            "**行动清单：**\n"
            "✅ 本周用AI帮我做过什么？\n"
            "✅ 哪个环节最提效？\n"
            "✅ 下个想用AI解决什么问题？\n\n"
            "💡 建议你把常用的Prompt保存起来，建立自己的Prompt库"
        )
    }
]

def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, 'r') as f:
            return json.load(f)
    return {"current_day": 0, "started_at": None, "last_morning_date": None}

def save_state(state):
    os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f, indent=2)

def get_morning_topic():
    state = load_state()
    today = datetime.now().strftime("%Y-%m-%d")
    
    if state.get("last_morning_date") == today:
        return TOPICS[state["current_day"] - 1] if state["current_day"] > 0 else None
    
    state["current_day"] = state.get("current_day", 0) + 1
    state["last_morning_date"] = today
    if state.get("started_at") is None:
        state["started_at"] = today
    
    if state["current_day"] > len(TOPICS):
        state["current_day"] = 1
    
    topic = TOPICS[state["current_day"] - 1]
    save_state(state)
    return topic

def get_evening_topic():
    state = load_state()
    if state.get("current_day", 0) == 0:
        return None
    return TOPICS[state["current_day"] - 1]

if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "morning"
    
    if mode == "morning":
        topic = get_morning_topic()
    else:
        topic = get_evening_topic()
    
    if topic:
        total = len(TOPICS)
        print(f"LESSON_DAY={topic['day']}")
        print(f"LESSON_TOTAL={total}")
        print(f"LESSON_TITLE={topic['title']}")
        if mode == "morning":
            print(f"LESSON_CONTENT={topic['content']}")
        else:
            print(f"LESSON_CONTENT={topic['practice']}")
