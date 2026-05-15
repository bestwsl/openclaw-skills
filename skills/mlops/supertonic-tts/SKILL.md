---
name: supertonic-tts
category: mlops
description: "Supertonic — Lightning Fast, On-Device, Multilingual TTS. ONNX Runtime based TTS system supporting 31 languages, capable of running on CPU, browser, mobile, and edge devices."
---

# Supertonic TTS Skill

## 项目简介

[Supertonic](https://github.com/supertone-inc/supertonic) 是由 Supertone Inc. 开发的极速本地文字转语音（TTS）系统。基于 ONNX Runtime，它完全在设备端运行——无需云端、无需 API 调用、无隐私泄露。支持 **31 种语言**，模型仅约 **99M 参数**，能在 CPU、树莓派、浏览器上流畅运行。

## 核心特性

- 🚀 **极速推理**：优化低延迟，桌面/浏览器/边缘设备均可运行
- 🔒 **完全本地**：零网络依赖，数据不出设备，隐私有保障
- 🌍 **31 语言支持**：含中、英、日、韩、法、德等主流语言
- 🎭 **情感标签**：支持 `<laugh>`、`<breath>`、`<sigh>` 等语音表情标签
- 📦 **轻量模型**：约 99M 参数，远小于 0.7B~2B 级别的 TTS 模型
- 🎯 **准确朗读**：改进的阅读稳定性，减少重复/跳过失败
- 💻 **多平台 SDK**：Python、Node.js、Java、C++、C#、Go、Swift、iOS、Rust、Flutter、浏览器 WebGPU/WASM

## 安装方式

### Python SDK（推荐快速体验）

```bash
pip install supertonic
```

### 完整仓库克隆

```bash
git clone https://github.com/supertone-inc/supertonic.git
cd supertonic
```

### 下载模型资产（使用 Git LFS）

```bash
# macOS
brew install git-lfs && git lfs install

# 通用安装：https://git-lfs.com
git lfs install
git clone https://huggingface.co/Supertone/supertonic-3 assets
```

## 基本用法

### Python 快速使用

```python
from supertonic import TTS

# 首次运行自动从 Hugging Face 下载模型
tts = TTS(auto_download=True)

style = tts.get_voice_style(voice_name="M1")

text = "A gentle breeze moved through the open window while everyone listened to the story."
wav, duration = tts.synthesize(text, voice_style=style, lang="en")

tts.save_audio(wav, "output.wav")
print(f"Generated {duration:.2f}s of audio")
```

### Python 完整示例（含 uv 包管理器）

```bash
cd py
uv sync
uv run example_onnx.py
```

### 浏览器体验

直接访问 [Interactive Demo](https://supertone-inc.github.io/supertonic/) 即可在线体验。

## 可用语言（31种）

| 代码 | 语言 | 代码 | 语言 | 代码 | 语言 |
|------|------|------|------|------|------|
| en | English | ko | Korean | ja | Japanese |
| ar | Arabic | bg | Bulgarian | cs | Czech |
| da | Danish | de | German | el | Greek |
| es | Spanish | et | Estonian | fi | Finnish |
| fr | French | hi | Hindi | hr | Croatian |
| hu | Hungarian | id | Indonesian | it | Italian |
| lt | Lithuanian | lv | Latvian | nl | Dutch |
| pl | Polish | pt | Portuguese | ro | Romanian |
| ru | Russian | sk | Slovak | sl | Slovenian |
| sv | Swedish | tr | Turkish | uk | Ukrainian |
| vi | Vietnamese |   |   |   |   |

## 预设语音风格

提供多种语音风格：M1~M5（男声）、F1~F5（女声）等。

```python
# 查看所有可用语音
style = tts.get_voice_style(voice_name="M1")
```

## 关键 API

| API | 说明 |
|-----|------|
| `TTS(auto_download=True)` | 初始化 TTS 引擎，自动下载模型 |
| `tts.get_voice_style(voice_name)` | 获取指定语音风格 |
| `tts.synthesize(text, voice_style, lang)` | 合成语音，返回 (wav, duration_seconds) |
| `tts.save_audio(wav, path)` | 将音频数据保存为 WAV 文件 |

## 适用场景

1. **智能语音助手**：本地 TTS 实现语音交互，无需联网
2. **阅读辅助工具**：如 Chrome 扩展 TLDRL，将网页转为音频
3. **电子书朗读**：在电子书阅读器上实现零网络依赖朗读（实测 0.3× RTF）
4. **无障碍应用**：为视障用户提供高质量本地语音合成
5. **游戏/VR 场景**：低延迟语音反馈，适合交互式应用
6. **IoT/边缘设备**：树莓派等设备上实时 TTS
7. **多语言内容创作**：31 种语言覆盖全球化需求
8. **隐私敏感场景**：医疗、金融等数据不可出站的场景

## 与主流 TTS 对比

| 特性 | Supertonic | ElevenLabs | OpenAI TTS |
|------|-----------|------------|------------|
| 本地运行 | ✅ | ❌ | ❌ |
| 免费 | ✅ | ❌ | ❌ |
| 31 语言 | ✅ | ✅ | ✅ |
| 情感标签 | ✅ | ❌ | ❌ |
| 模型大小 | 99M | N/A | N/A |

## 参考文献

- [SupertonicTTS: Main Architecture](https://arxiv.org/abs/2503.23108)
- [Length-Aware RoPE for Text-Speech Alignment](https://arxiv.org/abs/2509.11084)
- [Self-Purifying Flow Matching](https://arxiv.org/abs/2509.19091)

## 许可证

- 示例代码：MIT License
- 模型资产：OpenRAIL-M License
