---
name: ppt-master
description: AI generates natively editable PPTX from any document — real PowerPoint shapes, text boxes, charts, animations, NOT images
category: productivity
---

# PPT Master (hugohe3/ppt-master)

> GitHub: https://github.com/hugohe3/ppt-master  
> Stars: 14.4k ⭐  
> Author: Hugo He (finance professional, CPA · CPV)

## 概述

PPT Master 是一个 AI 工作流（"skill"），运行在 Claude Code、Cursor、VS Code Copilot 等 AI IDE 中。输入 PDF、DOCX、URL、或 Markdown，AI 自动生成**原生可编辑**的 PPTX 文件——每个形状、文本框、图表都是真实可点击编辑的 DrawingML 元素，不是图片。

## 核心特性

1. **原生可编辑 PPTX** — 不是图片拼凑，所有元素在 PowerPoint 中可直接点击编辑
2. **支持多种输入** — PDF、DOCX、URL（文章链接）、Markdown、直接粘贴文本
3. **模板复制** — 给 AI 一个 .pptx 模板，它能提取主题色、字体、母版布局
4. **动画与转场** — 支持真实 OOXML 动画，PowerPoint / Keynote 原生播放
5. **语音旁白** — edge-tts / 云 TTS 生成旁白，嵌入 PPTX，可导出 MP4 视频
6. **声音克隆** — 支持 ElevenLabs / MiniMax / Qwen / CosyVoice 克隆声音
7. **数据本地化** — 除了 AI 模型通信，整个流程在本地运行
8. **无平台锁定** — 支持 Claude、GPT、Gemini、Kimi 等多种模型

## 快速开始

### 1. 环境要求
- Python 3.10+

### 2. 安装
```bash
git clone https://github.com/hugohe3/ppt-master.git
cd ppt-master
pip install -r requirements.txt
```

或通过 skill marketplace 安装：
```bash
npx skills add hugohe3/ppt-master
```

### 3. 使用方式
将源文件放入 `projects/` 目录，然后在 AI 聊天中告诉它：
```
请根据 projects/q3-report/sources/report.pdf 制作一份 PPT
```

或直接粘贴文本：
```
请将以下内容制作成 PPT：[粘贴内容...]
```

AI 会先确认设计规格（模板、格式、页数等），然后自动完成内容分析、视觉设计、SVG 生成和 PPTX 导出。

### 4. 输出
- 主文件：`exports/<name>_<timestamp>.pptx`（原生可编辑）
- 快照备份：`backup/<timestamp>/`（含 SVG 版参考）

## 模型推荐

- **最佳**：Claude Opus/Sonnet（大上下文窗口）+ gpt-image-2 生成图片
- 其他模型也能跑，但质量上限取决于模型能力

## 适用场景

- 论文/报告转 PPT
- 公众号文章做演示
- 季度汇报自动生成
- 学术汇报、产品发布等
- 从零快速制作专业演示文稿

## 注意事项

- AI 失去上下文时，告诉它 `read skills/ppt-master/SKILL.md`
- Windows 安装需要额外步骤（PATH 设置、执行策略等）
- 需要 Office 2016+
- 项目是开源免费的，唯一成本是 AI 模型调用费
