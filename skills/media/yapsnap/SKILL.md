---
name: yapsnap
description: Snap any video URL or audio file into plaintext. No GPU. No cloud. One command. CPU-only offline transcription with speaker diarization.
category: media
---

# yapsnap — CPU-only 离线音视频转文字工具

> 项目地址：<https://github.com/kouhxp/yapsnap>
> 只需一行命令，将任何视频链接或音频文件转成纯文本。全程运行在 CPU 上，无需 GPU，无需云端 API。

## 项目简介

yapsnap 是一个基于 `sherpa-onnx` 的离线音视频转写工具。它使用 **Streaming Zipformer2 转导器**（Kroko 模型）在 CPU 上实时流式识别语音，速度快于原时长播放。支持：

- **在线视频 URL**：YouTube、X/Twitter、TikTok、Instagram Reels、直接媒体链接
- **本地文件**：`.mp3`、`.mp4`、`.wav`、`.m4a`、`.webm`、`.mkv` 等常见格式
- **离线运行**：首次运行下载 ~80MB 模型后完全离线，无 API Key、无配额限制
- **说话人标记**（可选）：`--diarize` 参数标记每句话是谁说的
- **多语言**：英语为主，支持法语、德语、西班牙语、意大利语等 10+ 语言

## 安装

### 1. 安装 ffmpeg

| 系统 | 命令 |
|------|------|
| macOS | `brew install ffmpeg` |
| Linux | `sudo apt install ffmpeg` 或 `sudo dnf install ffmpeg` |
| Windows | `winget install ffmpeg` 或 `choco install ffmpeg` |

### 2. 安装 yapsnap

```bash
pip install yapsnap
```

安装后提供两个命令：`yapsnap` 和别名 `transcribe`。

## 基本用法

```bash
# 转写本地音频文件
yapsnap audio.mp3

# 转写 YouTube 视频
yapsnap "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

# 带时间戳
yapsnap meeting.mp4 --timestamps

# 说话人标记
yapsnap interview.mp3 --diarize

# 指定说话人数（比自动检测更准确）
yapsnap call.mp3 --diarize --num-speakers 2

# 自定义输出路径
yapsnap input.mp4 -o ~/notes/transcript.txt

# 保持原速（默认 1.5x 加速以缩短时间）
yapsnap input.mp4 --speed 1.0
```

## 常用选项

| 参数 | 说明 |
|------|------|
| `-o, --output` | 输出 `.txt` 路径，默认 `./transcripts/<input>_transcript.txt` |
| `--timestamps` | 每句话前加 `[MM:SS]` 时间戳 |
| `--diarize` | 标记说话人（`SPEAKER_00 [MM:SS]: ...`），隐含 `--timestamps` |
| `--diarize-model` | 分段模型：`pyannote`（默认）或 `reverb`（更准但非商业许可） |
| `--num-speakers` | 已知说话人数，默认 `-1`（自动检测） |
| `--speed` | 加速倍数，默认 `1.5`（音调保持） |
| `--keep-audio` | 保留下载的音频（仅 URL 输入） |
| `--model` | 覆盖模型目录，也读取 `KROKO_MODEL` 环境变量 |

## 输出示例

**无时间戳：**
```
Welcome to the show. Today we're talking about transcription.
```

**带时间戳：**
```
[00:00] Welcome to the show.
[00:03] Today we're talking about transcription.
```

**带说话人标记：**
```
SPEAKER_00 [00:00]: Welcome to the show.
SPEAKER_01 [00:03]: Glad to be here, thanks for having me.
```

## 多语言支持

默认模型为英语。其他语言需下载对应 Kroko 模型：

```bash
# 下载法语模型后
yapsnap interview.mp3 --model /path/to/kroko-french
# 或设置环境变量
export KROKO_MODEL=/path/to/kroko-french
yapsnap interview.mp3
```

支持的语言：法语、德语、西班牙语、意大利语、葡萄牙语、荷兰语、瑞典语、瑞士德语、希伯来语、土耳其语。

模型下载：[HuggingFace - Banafo/Kroko-ASR](https://huggingface.co/Banafo/Kroko-ASR/tree/main)

## 工作原理

1. **获取**：URL 输入通过 `yt-dlp` 下载最佳音频流
2. **解码**：`ffmpeg` 转为 16kHz 单声道 PCM，可选的 `atempo` 滤镜加速不失真
3. **识别**：Streaming Zipformer2 转导器（Kroko，INT8 ONNX，~80MB）流式处理 PCM
4. **格式化**：默认纯文本，`--timestamps` 分组为句子加时间戳
5. **说话人标记**：额外运行说话人分割+嵌入模型，聚类声纹标记每句话

全程 CPU，无网络请求（首次之后），无数据离机。

## 适用场景

- **会议录音转文字**：快速将会议录音转为可搜索的文本
- **视频内容整理**：将 YouTube/TikTok 教程视频转写为笔记
- **播客笔记**：提取播客核心内容
- **采访/访谈处理**：带说话人标记的访谈记录
- **语言学习**：将外语视频转写为文本辅助学习
- **媒体归档**：为视频/音频文件建立可搜索的文字索引

## 注意事项

- 默认模型为英语，其他语言需手动下载模型
- `--speed 1.5` 可大幅缩短转写时间，对嘈杂/快速语音建议 `--speed 1.0`
- 输出默认保存到 `./transcripts/` 目录
- 首次运行需下载模型（~80MB），之后完全离线
- 使用 `--diarize` 时若说话人超过 ~7 位，建议指定 `--num-speakers`
- 说话人标记仅单次运行内稳定，不同文件间 SPEAKER_00 没有关联

## 许可证

- 项目本身：Apache-2.0
- Kroko 模型：见 [HuggingFace 许可](https://huggingface.co/Banafo/Kroko-ASR)
- 可选 diarization 模型：pyannote（CC-BY-4.0）、reverb（非商业许可）
