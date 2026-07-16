# AI每日复盘教练 (AI Daily Review Coach)

> AI个人系统实践课程 — 结课项目

一个终端里的 AI 复盘教练。你说说今天发生了什么，AI 不会直接给你结论，而是先问 3 个深度追问——帮你挖出自己都没看到的那一层。等你回答完，AI 再综合提炼，帮你看见模式、卡点和明天的方向。

## 为什么选这个题目

复盘这件事，大多数人都做成"流水账"——记了等于没记。真正的深度复盘需要一个"会追问"的教练，而老师/朋友不可能每天都陪你做这件事。

**AI 的核心价值：** 只有大模型能基于你零散的日记录，提出有针对性、不重复、能击中盲区的追问，然后从多天数据中提炼模式和洞察。这不是"给传统工具套个 AI 壳"，而是 AI 让深度复盘这件事第一次变得可能。

## 功能

- 🎯 **每日复盘**：描述今天 → AI 追问 3 个深度问题 → 综合提炼
- 📊 **周报生成**：综合过去 7 天复盘，发现模式和趋势
- 📈 **月报生成**：综合过去 30 天数据，回顾成长轨迹
- 📝 **Markdown 存档**：所有复盘自动保存为结构化日记

## 快速开始

### 1. 安装

```bash
pip install openai
```

### 2. 配置 API Key

```bash
# DeepSeek（学生免费额度：https://platform.deepseek.com）
export DEEPSEEK_API_KEY="sk-your-key"
```

### 3. 运行

```bash
# 每日复盘
python skill/scripts/daily_review.py

# 周报
python skill/scripts/daily_review.py --week

# 月报
python skill/scripts/daily_review.py --month

# 查看记录
python skill/scripts/daily_review.py --list
python skill/scripts/daily_review.py --read 2026-07-15
```

## 项目结构

```
ai-daily-review-coach/
├── skill/                          # Skill 文件
│   ├── SKILL.md                    # 技能定义（Hermes Skill 格式）
│   ├── scripts/
│   │   └── daily_review.py         # 核心脚本
│   └── references/
│       ├── prompt_templates.md     # 提示词模板参考
│       └── config_example.yaml     # 配置示例
├── data/
│   └── sample_review.md            # 测试样例数据
├── tests/
│   └── test_record.md              # 测试记录
├── iteration/
│   └── iteration_log.md            # 迭代升级说明
└── README.md
```

## 选题来源

选自 `AI实践场景清单.xlsx` 第 9 号场景：**AI每日复盘教练**

## 落地难度

★★★ 零门槛 — 仅需 Python + 免费大模型 API

## 课程信息

- 课程：AI个人系统实践
- 仓库地址：https://github.com/r1454/ai-daily-review-coach
- 提交：https://www.kdocs.cn/l/cldE5GnPASi5
