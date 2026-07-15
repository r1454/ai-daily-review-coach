# 测试记录 — AI每日复盘教练

## 测试环境

| 项目 | 信息 |
|------|------|
| 操作系统 | Windows 10 |
| Python 版本 | 3.11.15 |
| 依赖库 | openai >= 1.0.0 |
| API 服务 | DeepSeek API (deepseek-chat) |
| 测试日期 | 2026-07-15 |
| 测试人 | 学生 |

## 测试步骤

### 测试 1：基础交互模式 (`python daily_review.py`)

**步骤：**
1. 设置环境变量 `DEEPSEEK_API_KEY`
2. 运行 `python skill/scripts/daily_review.py`
3. 输入样例日记录（见 `data/sample_review.md` 样例1）
4. 等待 AI 生成追问
5. 回答 3 个追问
6. 查看生成的 Markdown 文件

**预期结果：**
- AI 生成 3 个与输入内容相关的深度追问
- 追问覆盖不同角度（情绪/动机、行为/决策、结果/影响）
- 复盘文件保存到 `~/.daily-reviews/YYYY-MM-DD.md`
- 文件包含：原始记录、追问与回答、关键事件、模式识别、卡点、核心洞察、明天行动建议

**实际结果：**
*（填写实际运行结果、截图或日志）*

```
运行命令: python skill/scripts/daily_review.py

[此处粘贴终端输出截图或日志]
```

**通过/失败：** *待测试*

---

### 测试 2：查看记录列表 (`python daily_review.py --list`)

**步骤：**
1. 在积累至少 3 天复盘记录后
2. 运行 `python skill/scripts/daily_review.py --list`

**预期结果：**
- 列出所有复盘文件及其大小
- 按日期倒序排列

**实际结果：**
*（粘贴终端输出）*

**通过/失败：** *待测试*

---

### 测试 3：周报生成 (`python daily_review.py --week`)

**步骤：**
1. 积累至少 5 天复盘记录
2. 运行 `python skill/scripts/daily_review.py --week`

**预期结果：**
- AI 综合过去 7 天的复盘，生成包含主题、亮点、挑战、模式、下周方向的周报
- 周报保存为 `~/.daily-reviews/week-YYYY-MM-DD.md`

**实际结果：**
*（粘贴终端输出）*

**通过/失败：** *待测试*

---

### 测试 4：月报生成 (`python daily_review.py --month`)

**步骤：**
1. 积累至少 15 天复盘记录
2. 运行 `python skill/scripts/daily_review.py --month`

**预期结果：**
- AI 综合过去 30 天的复盘，生成月报
- 月报保存为 `~/.daily-reviews/month-YYYY-MM-DD.md`

**实际结果：**
*（粘贴终端输出）*

**通过/失败：** *待测试*

---

### 测试 5：读取指定日期 (`python daily_review.py --read YYYY-MM-DD`)

**步骤：**
1. 运行 `python skill/scripts/daily_review.py --read 2026-07-15`（用实际日期替换）

**预期结果：**
- 在终端显示该日期的完整复盘内容

**实际结果：**
*（粘贴终端输出）*

**通过/失败：** *待测试*

---

### 测试 6：API Key 缺失处理

**步骤：**
1. 临时取消 `DEEPSEEK_API_KEY` 环境变量
2. 运行 `python skill/scripts/daily_review.py`

**预期结果：**
- 显示友好的错误提示，指导学生去哪里获取免费 API 额度

**实际结果：**
*（粘贴终端输出）*

**通过/失败：** *待测试*

---

## 测试总结

| 测试项 | 状态 | 备注 |
|--------|------|------|
| 测试 1: 基础交互模式 | ⬜ 待测试 | |
| 测试 2: 查看记录列表 | ⬜ 待测试 | |
| 测试 3: 周报生成 | ⬜ 待测试 | |
| 测试 4: 月报生成 | ⬜ 待测试 | |
| 测试 5: 读取指定日期 | ⬜ 待测试 | |
| 测试 6: API Key 缺失处理 | ⬜ 待测试 | |

---

*注意：实际测试时请将每个测试的输出截图粘贴到对应位置。*
