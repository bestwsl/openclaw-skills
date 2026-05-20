#!/usr/bin/env python3
"""Quectel technical support knowledge tracker - morning push + evening review."""
import os
import json
import sys
from datetime import datetime

STATE_FILE = os.path.expanduser("~/.hermes/cron/quectel_knowledge_state.json")

TOPICS = [
    {
        "day": 1,
        "title": "📡 4G/5G 通信协议基础",
        "content": (
            "**核心要点：**\n\n"
            "• **4G LTE**：峰值速率300Mbps（Cat.6），核心靠OFDMA+MIMO\n"
            "• **5G NR**：Sub-6GHz（FR1）和毫米波（FR2），核心靠更宽带宽+更高阶调制\n"
            "• **LTE Cat.1**：移远主打系列，10Mbps下行/5Mbps上行，替代3G的性价比之选\n"
            "• **NB-IoT**：窄带物联网，200kHz带宽，支持海量连接（10万+/小区）\n"
            "• **网络注册流程**：开机→搜网→PLMN选择→附着→PDN连接建立\n\n"
            "**面试常问：**\"客户模组一直搜不到网，你会怎么排查？\"\n"
            "→ 先查SIM卡状态(CCID/IMSI)，再看天线驻波比，抓空口log定位"
        ),
        "review": (
            "**今日复习 · 快速自测：**\n\n"
            "1️⃣ 4G LTE 的峰值速率是多少？（答：Cat.6 下 300Mbps）\n"
            "2️⃣ 5G NR 分为哪两个频段范围？（答：FR1 Sub-6GHz + FR2 毫米波）\n"
            "3️⃣ NB-IoT 的带宽和小区连接数？（答：200kHz，10万+/小区）\n"
            "4️⃣ LTE Cat.1 的上下行速率？（答：10Mbps下行 / 5Mbps上行）\n"
            "5️⃣ 网络注册流程有哪几步？（答：开机→搜网→PLMN选择→附着→PDN连接建立）\n"
            "6️⃣ 客户模组搜不到网，第一步查什么？（答：SIM卡状态 CCID/IMSI）\n\n"
            "**💡 一句话记住：** 搜网先查SIM卡，信号不好看天线"
        )
    },
    {
        "day": 2,
        "title": "🔌 AT 指令集详解",
        "content": (
            "**核心要点：**\n\n"
            "• AT = Attention，Hayes标准指令集，模组控制的基本语言\n"
            "• **基础指令**：AT（握手）、ATE（回显）、AT+CGMI（厂商）\n"
            "• **网络指令**：AT+CSQ（信号强度）、AT+COPS（运营商选择）、AT+CREG（网络注册）\n"
            "• **数据指令**：AT+CGATT（附着/分离）、AT+CGDCONT（PDP上下文）\n"
            "• **TCP/IP指令**：AT+QIOPEN（建立socket）、AT+QISEND（发数据）\n"
            "• **调试技巧**：AT+QCFG 系列是移远私有扩展指令，功能超丰富\n\n"
            "**常见问题：** AT 返回 ERROR → 检查波特率、硬件流控、模块供电是否稳定"
        ),
        "review": (
            "**今日复习 · 快速自测：**\n\n"
            "1️⃣ AT 全称是什么？（答：Attention）\n"
            "2️⃣ 查看信号强度用什么指令？（答：AT+CSQ）\n"
            "3️⃣ 查看运营商选择用什么指令？（答：AT+COPS）\n"
            "4️⃣ 建立TCP socket用移远哪条指令？（答：AT+QIOPEN）\n"
            "5️⃣ AT 返回 ERROR 可能是什么原因？（答：波特率不对、流控不匹配、供电不稳）\n"
            "6️⃣ 移远私有扩展指令以什么开头？（答：AT+QCFG）\n\n"
            "**💡 一句话记住：** AT+CSQ看信号，AT+QIOPEN建连接，ERROR先查波特率"
        )
    },
    {
        "day": 3,
        "title": "🧪 射频基础与信号测试",
        "content": (
            "**核心要点：**\n\n"
            "• **关键指标**：\n"
            "  - RSRP（参考信号接收功率）：-80~-120dBm，越小信号越差\n"
            "  - RSRQ（参考信号接收质量）：-3~-20dB，反映信噪比\n"
            "  - SINR（信干噪比）：>20dB优秀，<0dB很差\n"
            "  - RSSI（接收信号强度指示）：整体信号强度\n"
            "• **天线基础**：驻波比(VSWR)<2.0为合格，增益(dBi)越高覆盖越远\n"
            "• **干扰排查**：同频干扰→频点偏移；邻频干扰→滤波器/频段隔离\n"
            "• **测试工具**：频谱仪、综测仪(CMW500/MT8821)、QLog抓RF log\n\n"
            "**面试常问：** 客户反馈信号弱→先查天线类型/位置，用AT+CSQ看RSRP值，对比不同位置差异"
        ),
        "review": (
            "**今日复习 · 快速自测：**\n\n"
            "1️⃣ RSRP 正常范围是多少？（答：-80~-120dBm）\n"
            "2️⃣ RSRQ 与 RSRP 有什么区别？（答：RSRP看功率，RSRQ看信噪比）\n"
            "3️⃣ SINR 大于多少算优秀？（答：>20dB）\n"
            "4️⃣ 天线 VSWR 合格标准？（答：<2.0）\n"
            "5️⃣ 同频干扰和邻频干扰分别怎么处理？（答：同频→偏移频点；邻频→加滤波器）\n"
            "6️⃣ 信号弱第一步查什么？（答：天线类型/位置，AT+CSQ看RSRP）\n\n"
            "**💡 一句话记住：** 信号强度看RSRP，质量看SINR，天线VSWR<2才合格"
        )
    },
    {
        "day": 4,
        "title": "✅ 模组认证流程（CE/FCC/GCF）",
        "content": (
            "**核心要点：**\n\n"
            "• **CE认证**（欧洲）：RED指令2014/53/EU，含射频(EN 301 511)+EMC(EN 301 489)+安全(EN 62368)\n"
            "• **FCC认证**（美国）：Part 15/22/24/27，SAR测试(OET 65)\n"
            "• **GCF认证**（全球）：PTCRB(北美)+GCF(全球)，运营商准入必过\n"
            "• **CCC认证**（中国）：强制3C+SRRC（无线电）+CTA（入网）\n"
            "• **移远优势**：大部分模组已预认证，客户终端只需做终端级认证\n"
            "• **常见坑**：天线匹配不良导致FCC/CE辐射超标，PCB布局影响EMC\n\n"
            "**面试常问：** 客户问模组已经过认证了为什么他的产品还要再认证？\n"
            "→ 模组认证 ≠ 终端认证，终端需做EMC/SAR/安全等补充测试"
        ),
        "review": (
            "**今日复习 · 快速自测：**\n\n"
            "1️⃣ CE认证适用哪个地区？涵盖哪些方面？（答：欧洲，射频+EMC+安全）\n"
            "2️⃣ FCC认证适用哪个地区？（答：美国）\n"
            "3️⃣ GCF和PTCRB是什么关系？（答：GCF全球，PTCRB北美）\n"
            "4️⃣ 中国需要哪三个认证？（答：3C强制认证 + SRRC无线电 + CTA入网）\n"
            "5️⃣ 模组已认证，终端为什么还要认证？（答：终端要自己做EMC/SAR/安全测试）\n"
            "6️⃣ 认证中最常见的坑是什么？（答：天线匹配不良导致辐射超标）\n\n"
            "**💡 一句话记住：** 欧洲CE美国FCC，中国3C+SRRC+CTA，模组认证≠终端认证"
        )
    },
    {
        "day": 5,
        "title": "🐍 QuecPython 入门",
        "content": (
            "**核心要点：**\n\n"
            "• **QuecPython** = 移远自研的物联网Python开发框架，在模组上直接跑Python\n"
            "• **适用场景**：快速原型、简单IoT应用、减少MCU成本\n"
            "• **支持模组**：EC600x/EC800x等Cat.1/BIS系列\n"
            "• **核心API**：\n"
            "  - `quecIot`：连接飞鸢平台\n"
            "  - `dataCall`：数据拨号\n"
            "  - `net`：网络状态\n"
            "  - `sim`：SIM卡操作\n"
            "• **开发流程**：Python写代码→.py文件→QPYcom工具烧录→串口调试\n"
            "• **对比传统**：免C语言交叉编译，开发效率提升3-5倍\n\n"
            "**官网入口：** https://python.quectel.com/"
        ),
        "review": (
            "**今日复习 · 快速自测：**\n\n"
            "1️⃣ QuecPython 是什么？（答：移远自研的物联网Python开发框架）\n"
            "2️⃣ 哪些模组支持 QuecPython？（答：EC600x/EC800x等Cat.1/BIS系列）\n"
            "3️⃣ 连接飞鸢平台用哪个API？（答：quecIot）\n"
            "4️⃣ 数据拨号用哪个API？（答：dataCall）\n"
            "5️⃣ 开发流程是怎样的？（答：Python写代码→.py→QPYcom烧录→串口调试）\n"
            "6️⃣ 相比C语言开发有哪些优势？（答：免交叉编译，效率3-5倍）\n\n"
            "**💡 一句话记住：** QuecPython让模组直接跑Python，QPYcom烧录，quecIot连飞鸢"
        )
    },
    {
        "day": 6,
        "title": "🔍 问题排查方法论",
        "content": (
            "**核心要点：**\n\n"
            "**标准排查流程：**\n"
            "1. **确认现象**：能复现吗？什么条件下触发？\n"
            "2. **收集信息**：AT+CSQ信号、AT+CREG注册状态、供电电压\n"
            "3. **抓Log**：QLog（移远工具）抓模组log，Wireshark抓网络包\n"
            "4. **简化环境**：去掉客户外围电路，裸板+串口测试\n"
            "5. **对比测试**：同样的环境换一个模组/换SIM卡/换天线\n"
            "6. **看已知问题**：查Release Note、Known Issues、技术论坛\n\n"
            "**分类排查：**\n"
            "• **不上网** → 检查APN、SIM卡、网络覆盖\n"
            "• **掉线** → 检查电源纹波、天线驻波、温度\n"
            "• **功耗高** → PSM/eDRX配置、睡眠唤醒检查\n"
            "• **数据传不上** → MQTT/TCP参数、MTU、防火墙\n\n"
            "GitHub开源：https://github.com/QuecPython/"
        ),
        "review": (
            "**今日复习 · 快速自测：**\n\n"
            "1️⃣ 问题排查标准流程有哪几步？（答：确认现象→收集信息→抓Log→简化环境→对比→查已知问题）\n"
            "2️⃣ 抓Log用什么工具？（答：QLog抓模组log，Wireshark抓网络包）\n"
            "3️⃣ 不上网先查什么？（答：APN、SIM卡、网络覆盖）\n"
            "4️⃣ 掉线可能是什么原因？（答：电源纹波、天线驻波、温度）\n"
            "5️⃣ 功耗高要检查什么配置？（答：PSM/eDRX配置、睡眠唤醒）\n"
            "6️⃣ 数据传不上要检查什么？（答：MQTT/TCP参数、MTU、防火墙）\n\n"
            "**💡 一句话记住：** 排查六步走，确认→信息→Log→简化→对比→查已知"
        )
    },
    {
        "day": 7,
        "title": "🌐 物联网通信协议",
        "content": (
            "**核心要点：**\n\n"
            "• **MQTT**（最常用）：发布/订阅模式，QoS 0/1/2，轻量级\n"
            "  - 移远模组 AT+QMTCFG / AT+QMTOPEN / AT+QMTPUB\n"
            "  - 面试常问：MQTT保活心跳怎么设？→ KeepAlive建议60-300s\n"
            "• **CoAP**：UDP之上的RESTful协议，适合资源受限设备\n"
            "• **HTTP/HTTPS**：AT+QHTTPURL / AT+QHTTPGET/POST\n"
            "• **TCP/UDP**：底层传输，AT+QIOPEN直接操作socket\n"
            "• **LwM2M**：OMA标准设备管理协议，NB-IoT首选\n"
            "• **TLS/DTLS**：加密传输，需要预置证书→AT+QSSLCFG配置\n\n"
            "**面试常问：** MQTT断线重连机制怎么实现？\n"
            "→ Clean Session=true每次重连清扫，false则恢复之前的订阅和未确认消息"
        ),
        "review": (
            "**今日复习 · 快速自测：**\n\n"
            "1️⃣ IoT最常用的通信协议是什么？（答：MQTT，发布/订阅模式）\n"
            "2️⃣ MQTT 有哪三级 QoS？（答：0最多一次、1至少一次、2恰好一次）\n"
            "3️⃣ CoAP 基于什么传输层协议？（答：UDP）\n"
            "4️⃣ 移远模组建立TCP socket用什么指令？（答：AT+QIOPEN）\n"
            "5️⃣ 加密传输用什么协议？如何配置？（答：TLS/DTLS，AT+QSSLCFG配置证书）\n"
            "6️⃣ LwM2M 适合什么场景？（答：NB-IoT设备管理）\n\n"
            "**💡 一句话记住：** MQTT最常用，CoAP走UDP，TLS加密要配证书"
        )
    },
    {
        "day": 8,
        "title": "💻 嵌入式Linux驱动调试",
        "content": (
            "**核心要点：**\n\n"
            "• **驱动基础**：USB虚拟串口（CDC ACM/QMI/RNDIS/ECM）\n"
            "  - QMI_WWAN：高通方案，最稳定、功能最全\n"
            "  - ECM/RNDIS：简化网络连接，RNDIS是微软标准\n"
            "• **移远驱动**：GobiNet/QMI_WWAN驱动源码开源\n"
            "  - `qmi_wwan_q`：移远修改版，支持更多模组\n"
            "• **PPP拨号**：传统方式，`pppd call quectel-ppp`\n"
            "• **调试命令**：\n"
            "  - `lsusb` 看USB枚举\n"
            "  - `dmesg` 看驱动加载log\n"
            "  - `ifconfig wwan0` 看网络接口\n"
            "  - `udhcpc -i wwan0` 获取IP\n"
            "• **常见问题**：USB不通→检查硬件电源/复位；驱动不识别→检查内核版本\n\n"
            "GitHub驱动：https://github.com/quectel-open"
        ),
        "review": (
            "**今日复习 · 快速自测：**\n\n"
            "1️⃣ Linux下QMI_WWAN是什么？（答：高通方案USB网络驱动，最稳定功能最全）\n"
            "2️⃣ 移远模组在Linux下有哪些驱动方式？（答：QMI_WWAN、GobiNet、ECM/RNDIS、PPP）\n"
            "3️⃣ `lsusb` 看什么？（答：USB设备枚举情况）\n"
            "4️⃣ `dmesg` 看什么？（答：驱动加载日志）\n"
            "5️⃣ `udhcpc -i wwan0` 做什么？（答：通过DHCP获取IP地址）\n"
            "6️⃣ 驱动不识别先查什么？（答：内核版本）\n\n"
            "**💡 一句话记住：** QMI_WWAN最稳，PPPD也能用，USB不通先查电源复位"
        )
    },
    {
        "day": 9,
        "title": "📶 GNSS 定位技术基础",
        "content": (
            "**核心要点：**\n\n"
            "• **四大系统**：GPS（美国）+北斗（中国）+GLONASS（俄罗斯）+Galileo（欧盟）\n"
            "• **移远GNSS模组**：L76K/L26系列，支持多星座联合定位\n"
            "• **定位模式**：\n"
            "  - 单点定位：2-5米精度\n"
            "  - RTK差分定位：厘米级，需要CORS站/网络校正\n"
            "  - AGNSS辅助定位：利用基站/网络加速首次定位(TTFF)\n"
            "• **AT指令**：AT+QGPS=1（开启）、AT+QGPSLOC（获取定位）\n"
            "• **影响精度的因素**：天空视野、多径效应、电离层扰动\n"
            "• **常见问题**：\"定位不了\"→先确认天线位置（天面270°无遮挡），再查NMEA输出\n\n"
            "**面试常问：** 客户首次定位太慢怎么办？\n"
            "→ 开启AGNSS辅助，或者把星历/历书保存到Flash，下次冷启变成热启"
        ),
        "review": (
            "**今日复习 · 快速自测：**\n\n"
            "1️⃣ 全球四大卫星定位系统有哪些？（答：GPS+北斗+GLONASS+Galileo）\n"
            "2️⃣ 移远GNSS模组有哪些系列？（答：L76K/L26）\n"
            "3️⃣ RTK差分定位精度多少？（答：厘米级）\n"
            "4️⃣ AGNSS的作用是什么？（答：利用基站/网络加速首次定位）\n"
            "5️⃣ 开启GNSS用哪个AT指令？（答：AT+QGPS=1）\n"
            "6️⃣ 首次定位太慢怎么办？（答：开启AGNSS辅助或保存星历到Flash）\n\n"
            "**💡 一句话记住：** 四大系统联合定位，AGNSS加速冷启，RTK到厘米级"
        )
    },
    {
        "day": 10,
        "title": "🏗 飞鸢物联网平台",
        "content": (
            "**核心要点：**\n\n"
            "• **飞鸢=Quectal IoT Hub**：移远自有物联网云平台\n"
            "• **核心功能**：\n"
            "  - 设备管理：注册、在线/离线状态、OTA升级\n"
            "  - 数据采集：上行数据解析、告警规则\n"
            "  - 远程控制：下行指令、参数配置\n"
            "  - 规则引擎：数据流转到三方平台\n"
            "• **对接方式**：MQTT/CoAP/HTTP多种协议\n"
            "• **QuecPython集成**：`quecIot`库一行代码连接\n"
            "• **核心价值**：免去客户自建云平台，模组端+云+APP一站式\n"
            "• **竞品对比**：vs 阿里云IoT/华为IoT/AWS IoT\n\n"
            "**面试常问：** 客户用你们的模组一定要用飞鸢平台吗？\n"
            "→ 不一定，模组支持标准MQTT/HTTP，可以对接任何云平台"
        ),
        "review": (
            "**今日复习 · 快速自测：**\n\n"
            "1️⃣ 飞鸢平台是什么？（答：移远自有物联网云平台 Quectal IoT Hub）\n"
            "2️⃣ 飞鸢平台核心功能有哪些？（答：设备管理、数据采集、远程控制、规则引擎）\n"
            "3️⃣ 支持哪些协议接入？（答：MQTT/CoAP/HTTP）\n"
            "4️⃣ QuecPython如何集成飞鸢？（答：quecIot库一行代码连接）\n"
            "5️⃣ 飞鸢平台的竞品有哪些？（答：阿里云IoT、华为IoT、AWS IoT）\n"
            "6️⃣ 客户一定要用飞鸢平台吗？（答：不必，模组支持标准协议对接任何云平台）\n\n"
            "**💡 一句话记住：** 飞鸢一站式IoT云平台，QuecPython一行连，也可对接三方云"
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
    """Morning mode: advance to next topic."""
    state = load_state()
    today = datetime.now().strftime("%Y-%m-%d")
    
    # Don't advance if already ran this morning
    if state.get("last_morning_date") == today:
        return TOPICS[state["current_day"] - 1] if state["current_day"] > 0 else None
    
    state["current_day"] = state.get("current_day", 0) + 1
    state["last_morning_date"] = today
    if state.get("started_at") is None:
        state["started_at"] = today
    
    if state["current_day"] > len(TOPICS):
        state["current_day"] = 1  # restart
    
    topic = TOPICS[state["current_day"] - 1]
    save_state(state)
    return topic

def get_evening_topic():
    """Evening mode: review today's topic."""
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
        print(f"QUECTEL_DAY={topic['day']}")
        print(f"QUECTEL_TOTAL={total}")
        print(f"QUECTEL_TITLE={topic['title']}")
        if mode == "morning":
            print(f"QUECTEL_CONTENT={topic['content']}")
        else:
            print(f"QUECTEL_CONTENT={topic['review']}")
