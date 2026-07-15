---
name: ai-daily-review-coach
description: Use when the user wants to do a daily review, generate weekly/monthly retrospectives, or reflect on their day with AI-driven deep questioning. Runs an interactive terminal session where AI asks 3 tailored follow-up questions based on the user's daily log, synthesizes insights, identifies patterns and blockers, and saves structured markdown reviews. Also supports --week and --month retrospectives that aggregate past reviews.
version: 1.0.0
author: AI个人系统实践课程
license: MIT
metadata:
  hermes:
    tags: [productivity, reflection, journaling, coaching, review]
    related_skills: []
---

# AI每日复盘教练 (AI Daily Review Coach)

## Overview

一个终端里的 AI 复盘教练。你描述今天发生了什么，AI 不会直接给结论，而是先问 3 个深度追问——帮你挖出自己都没想到的那一层。等你回答完，AI 再综合提炼：关键事件、卡点、模式、明天的 1 个行动建议。每次复盘自动存为 Markdown 日记，积累一周或一个月后可以生成周报/月报。

**AI 核心价值：** 没有 AI 这个功能根本做不到——只有大模型能基于你零散的日记录，提出有针对性、不重复、能击中盲区的追问，然后从中提炼模式和洞察。

## When to Use

- 每天晚上复盘今天的工作/学习/生活
- 想看清自己重复踩的坑和隐藏的卡点
- 需要周报/月报来回顾成长轨迹
- 写流水账复盘没效果，需要有人帮你"问对问题"

Don't use for:
- 简单的任务列表管理（用待办工具更合适）
- 需要实时协作的团队复盘

## Quick Start

### 1. 安装依赖

```bash
pip install openai
```

### 2. 设置 API Key

```bash
# DeepSeek（推荐，学生免费额度）
export DEEPSEEK_API_KEY="你的key"
# 或者用 OpenAI 兼容接口
export OPENAI_API_KEY="你的key"
export OPENAI_BASE_URL="https://api.deepseek.com"  # 可选
```

### 3. 运行

```bash
# 每日复盘（交互模式）
python skill/scripts/daily_review.py

# 生成周报
python skill/scripts/daily_review.py --week

# 生成月报
python skill/scripts/daily_review.py --month

# 查看所有记录
python skill/scripts/daily_review.py --list

# 查看某天记录
python skill/scripts/daily_review.py --read 2026-07-15
```

## Workflow

```
用户输入日记录
      ↓
AI 生成 3 个深度追问（基于具体内容，从情绪/动机、行为/决策、结果/影响三个角度）
      ↓
用户逐一回答
      ↓
AI 综合提炼：关键事件 + 模式识别 + 卡点 + 核心洞察 + 明天1个行动建议
      ↓
保存为 Markdown 日记（~/.daily-reviews/YYYY-MM-DD.md）
```

## 文件存储

所有复盘记录默认保存在 `~/.daily-reviews/` 目录下：

```
~/.daily-reviews/
├── 2026-07-15.md    # 每日复盘
├── 2026-07-16.md
├── week-2026-07-21.md  # 周报
└── month-2026-07-31.md # 月报
```

可通过 `REVIEW_DIR` 环境变量自定义路径。

## 配置参考

| 环境变量 | 说明 | 默认值 |
|----------|------|--------|
| `DEEPSEEK_API_KEY` | DeepSeek API密钥 | - |
| `OPENAI_API_KEY` | OpenAI API密钥（备选） | - |
| `DEEPSEEK_BASE_URL` | API地址（OpenAI兼容） | `https://api.deepseek.com` |
| `REVIEW_MODEL` | 模型名称 | `deepseek-chat` |
| `REVIEW_DIR` | 复盘文件存储目录 | `~/.daily-reviews` |

详见 `references/config_example.yaml`。

## Common Pitfalls

1. **API Key 没设** — 运行前确保设置了 `DEEPSEEK_API_KEY` 或 `OPENAI_API_KEY`。学生可去 platform.deepseek.com 免费领额度。
2. **输入太短** — 只写"今天很累"这种，AI 追问也会很浅。建议至少写 3-5 句，包含具体事件。
3. **跳过追问直接想要结论** — 这个工具的核心价值就在追问环节。认真回答追问，AI 的提炼才有质量。
4. **只在心情不好的时候用** — 好事也值得复盘。让 AI 帮你看到"做对了什么"和"为什么做对了"。
5. **数据攒不够就生成周报/月报** — 至少需要 5 天以上的每日复盘，周报才有意义。

## Verification Checklist

- [ ] `pip install openai` 安装成功
- [ ] API Key 环境变量已设置
- [ ] 运行 `python daily_review.py` 能进入交互模式
- [ ] 输入一段日记录后，AI 生成了 3 个追问
- [ ] 回答追问后，复盘 Markdown 文件正确保存到 `~/.daily-reviews/`
- [ ] `python daily_review.py --list` 能列出所有记录
- [ ] 积累 5+ 天记录后，`--week` 能生成有意义的周报
