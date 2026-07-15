#!/usr/bin/env python3
"""
AI每日复盘教练 — Daily Review Coach
=====================================
A terminal-based AI coach that asks deep questions about your day,
synthesizes insights, and maintains a review journal.

Usage:
    python daily_review.py                  # Interactive mode
    python daily_review.py --week           # Weekly retrospective
    python daily_review.py --month          # Monthly retrospective
    python daily_review.py --list           # List all saved reviews
    python daily_review.py --read 2026-07-15 # Read a specific day's review

Requirements:
    pip install openai
    Set OPENAI_API_KEY or DEEPSEEK_API_KEY environment variable.
"""

import argparse
import json
import os
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

# ── Config ──────────────────────────────────────────────────────────
API_KEY = os.environ.get("DEEPSEEK_API_KEY") or os.environ.get("OPENAI_API_KEY")
API_BASE = os.environ.get("DEEPSEEK_BASE_URL") or "https://api.deepseek.com"
MODEL = os.environ.get("REVIEW_MODEL") or "deepseek-chat"

REVIEW_DIR = Path(os.environ.get("REVIEW_DIR") or Path.home() / ".daily-reviews")
REVIEW_DIR.mkdir(parents=True, exist_ok=True)


def get_client():
    """Lazy-import OpenAI client with configured base URL."""
    from openai import OpenAI
    if not API_KEY:
        print("错误：请设置 DEEPSEEK_API_KEY 或 OPENAI_API_KEY 环境变量")
        print("      学生可免费领取 DeepSeek API 额度：https://platform.deepseek.com")
        sys.exit(1)
    return OpenAI(api_key=API_KEY, base_url=API_BASE)


# ── Prompts ──────────────────────────────────────────────────────────
SYSTEM_PROMPT = """你是一位专业的每日复盘教练。你的职责是：
1. 根据用户的日记录，提出3个有深度、有针对性的追问
2. 综合用户的回答，提炼关键事件、识别卡点、给出明天最重要的1个行动建议
3. 永远保持好奇、不评判、帮助用户看到自己忽略的点

追问原则：
- 不问泛泛的问题（如"今天感觉怎么样"），而是基于用户具体描述深挖
- 每次追问一个方向：情绪/动机、行为/决策、结果/影响
- 帮用户发现重复模式和盲区

输出格式（严格JSON）：
对于提问阶段：
{"questions": ["问题1", "问题2", "问题3"]}

对于合成阶段：
{
  "key_events": ["事件1", "事件2"],
  "patterns": "识别到的模式或盲区",
  "blockers": ["卡点1"],
  "tomorrow_focus": "明天最重要的1个行动建议",
  "insight": "今天的核心洞察（一句话）"
}
"""

WEEKLY_PROMPT = """你是一位复盘教练。以下是用户过去一周的每日复盘记录。
请综合这些记录，生成一份周报。

输出格式（严格JSON）：
{
  "weekly_theme": "本周的核心主题（一句话）",
  "highlights": ["本周亮点1", "本周亮点2"],
  "challenges": ["持续遇到的挑战"],
  "patterns_weekly": "本周发现的重复模式",
  "next_week_focus": "下周最重要的1个方向",
  "growth_moment": "本周最值得记住的成长瞬间"
}
"""

MONTHLY_PROMPT = """你是一位复盘教练。以下是用户过去一个月的每日复盘记录和周报。
请综合这些记录，生成一份月报。

输出格式（严格JSON）：
{
  "monthly_theme": "本月的核心主题",
  "biggest_win": "本月最大成就",
  "biggest_lesson": "本月最大教训",
  "habit_trends": "习惯和模式的变化趋势",
  "next_month_goal": "下个月最重要的1个目标",
  "personal_growth": "本月个人成长总结（2-3句话）"
}
"""


# ── Core Functions ───────────────────────────────────────────────────
def ask_ai(client, system_prompt: str, user_prompt: str) -> str:
    """Send a prompt to the AI and return the response text."""
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.7,
        max_tokens=2000,
    )
    return response.choices[0].message.content.strip()


def parse_json_response(text: str) -> dict:
    """Try to parse AI response as JSON, falling back to cleaning markdown fences."""
    text = text.strip()
    if text.startswith("```"):
        text = text.split("\n", 1)[-1]
        if text.endswith("```"):
            text = text[:-3]
    return json.loads(text)


def generate_questions(client, daily_log: str) -> list:
    """Generate 3 deep follow-up questions based on the daily log."""
    prompt = f"""用户今天的记录：
{daily_log}

请根据以上内容，生成3个深度追问。要求：
1. 每个问题都要基于用户的具体描述来深挖
2. 从不同角度追问：情绪/动机、行为/决策、结果/影响
3. 问题要有启发性，帮用户看到自己可能忽略的点

只返回JSON，不要其他内容。"""
    response = ask_ai(client, SYSTEM_PROMPT, prompt)
    data = parse_json_response(response)
    return data.get("questions", [])


def synthesize_review(client, daily_log: str, qa_pairs: list) -> dict:
    """Synthesize the daily log + Q&A into a structured review."""
    qa_text = "\n".join(f"追问{i+1}: {q}\n回答: {a}" for i, (q, a) in enumerate(qa_pairs))
    prompt = f"""用户今天的记录：
{daily_log}

追问与回答：
{qa_text}

请综合以上内容，生成今日复盘。只返回JSON，不要其他内容。"""
    response = ask_ai(client, SYSTEM_PROMPT, prompt)
    return parse_json_response(response)


def format_review_markdown(day: str, daily_log: str, qa_pairs: list, synthesis: dict) -> str:
    """Format a daily review as a Markdown document."""
    qa_md = "\n\n".join(
        f"### 追问 {i+1}\n> {q}\n\n**我的回答：** {a}"
        for i, (q, a) in enumerate(qa_pairs)
    )
    events_md = "\n".join(f"- {e}" for e in synthesis.get("key_events", []))
    blockers_md = "\n".join(f"- {b}" for b in synthesis.get("blockers", []))

    return f"""# 每日复盘 — {day}

## 原始记录
{daily_log}

## 深度追问
{qa_md}

## AI 综合分析

### 关键事件
{events_md}

### 识别到的模式/盲区
{synthesis.get("patterns", "")}

### 卡点
{blockers_md}

### 今日核心洞察
> {synthesis.get("insight", "")}

### 明天最重要的1件事
🎯 **{synthesis.get("tomorrow_focus", "")}**

---
*由 AI每日复盘教练 自动生成*
"""


def interactive_review(client):
    """Run an interactive daily review session."""
    print("\n" + "=" * 50)
    print("  🤖 AI 每日复盘教练")
    print("=" * 50)
    print("\n今天发生了什么？做了什么？有什么感受？")
    print("（输入完成后，空行按 Enter 即可）\n")

    # Read input until empty line
    lines = []
    while True:
        try:
            line = input()
        except EOFError:
            break
        if line.strip() == "":
            if lines:
                break
        else:
            lines.append(line)
    daily_log = "\n".join(lines)

    if not daily_log.strip():
        print("没有输入内容，退出。")
        return

    today = date.today().isoformat()

    print("\n⏳ AI 正在分析你的记录，生成深度追问...\n")
    questions = generate_questions(client, daily_log)

    qa_pairs = []
    for i, q in enumerate(questions, 1):
        print(f"💬 追问 {i}：{q}")
        answer = input("你的回答：").strip()
        qa_pairs.append((q, answer))
        print()

    print("⏳ AI 正在综合复盘...\n")
    synthesis = synthesize_review(client, daily_log, qa_pairs)

    # Build markdown
    md_content = format_review_markdown(today, daily_log, qa_pairs, synthesis)
    filepath = REVIEW_DIR / f"{today}.md"
    filepath.write_text(md_content, encoding="utf-8")

    print("=" * 50)
    print(f"📝 复盘已保存: {filepath}")
    print("=" * 50)
    print(f"\n🎯 明天最重要的1件事：")
    print(f"   {synthesis.get('tomorrow_focus', '继续加油！')}")
    print(f"\n💡 今日核心洞察：")
    print(f"   {synthesis.get('insight', '每一天都值得记录。')}")
    print()


def do_retrospective(client, period: str):
    """Generate a weekly or monthly retrospective."""
    today = date.today()

    if period == "week":
        days_back = 7
        prompt_template = WEEKLY_PROMPT
        title_prefix = "周报"
    else:
        days_back = 30
        prompt_template = MONTHLY_PROMPT
        title_prefix = "月报"

    # Collect reviews from the period
    reviews = []
    for i in range(days_back):
        day = today - timedelta(days=i)
        review_path = REVIEW_DIR / f"{day.isoformat()}.md"
        if review_path.exists():
            reviews.append(f"--- {day.isoformat()} ---\n{review_path.read_text(encoding='utf-8')}")

    if not reviews:
        print(f"过去{days_back}天内没有找到复盘记录。先做几次每日复盘吧！")
        return

    combined = "\n\n".join(reviews)
    print(f"⏳ AI 正在综合过去 {len(reviews)} 天的复盘记录...\n")
    response = ask_ai(client, prompt_template, combined)
    data = parse_json_response(response)

    # Write the retrospective
    period_key = today.isoformat()
    filepath = REVIEW_DIR / f"{period}-{period_key}.md"

    md = format_retrospective_markdown(period, title_prefix, data)
    filepath.write_text(md, encoding="utf-8")

    print("=" * 50)
    print(f"📝 {title_prefix}已保存: {filepath}")
    print("=" * 50)
    print(md)


def format_retrospective_markdown(period: str, title: str, data: dict) -> str:
    """Format weekly/monthly retrospective as Markdown."""
    if period == "week":
        highlights = "\n".join(f"- {h}" for h in data.get("highlights", []))
        return f"""# {title} — {date.today().isoformat()}

## 本周主题
{data.get("weekly_theme", "")}

## 亮点
{highlights}

## 挑战
{chr(10).join(f"- {c}" for c in data.get("challenges", []))}

## 重复模式
{data.get("patterns_weekly", "")}

## 下周方向
🎯 {data.get("next_week_focus", "")}

## 最值得记住的成长瞬间
✨ {data.get("growth_moment", "")}

---
*由 AI每日复盘教练 自动生成*
"""
    else:
        return f"""# {title} — {date.today().isoformat()}

## 本月主题
{data.get("monthly_theme", "")}

## 最大成就
🏆 {data.get("biggest_win", "")}

## 最大教训
📖 {data.get("biggest_lesson", "")}

## 习惯与模式变化趋势
{data.get("habit_trends", "")}

## 下月目标
🎯 {data.get("next_month_goal", "")}

## 个人成长总结
{data.get("personal_growth", "")}

---
*由 AI每日复盘教练 自动生成*
"""


def list_reviews():
    """List all saved review files."""
    files = sorted(REVIEW_DIR.glob("*.md"), reverse=True)
    if not files:
        print("还没有任何复盘记录。运行一次每日复盘吧！")
        return
    print(f"\n📚 复盘记录（共 {len(files)} 条）:\n")
    for f in files:
        size = f.stat().st_size
        print(f"  {f.stem}  ({size}B)")


def read_review(day_str: str):
    """Read a specific day's review."""
    filepath = REVIEW_DIR / f"{day_str}.md"
    if not filepath.exists():
        # Try with hyphens
        filepath = REVIEW_DIR / f"{day_str.replace('-', '-')}.md"
    if not filepath.exists():
        print(f"未找到 {day_str} 的复盘记录。")
        # Suggest similar dates
        files = sorted(REVIEW_DIR.glob("*.md"))
        matching = [f for f in files if day_str in f.stem]
        if matching:
            print(f"你是不是要找：{', '.join(f.stem for f in matching[:5])}")
        return
    print(filepath.read_text(encoding="utf-8"))


# ── Main ─────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(
        description="AI每日复盘教练 — 帮你看清每一天",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python daily_review.py              # 开始今日复盘
  python daily_review.py --week       # 生成本周周报
  python daily_review.py --month      # 生成本月月报
  python daily_review.py --list       # 查看所有复盘记录
  python daily_review.py --read 2026-07-15  # 查看某天复盘
        """,
    )
    parser.add_argument("--week", action="store_true", help="生成本周周报")
    parser.add_argument("--month", action="store_true", help="生成本月月报")
    parser.add_argument("--list", action="store_true", help="列出所有复盘记录")
    parser.add_argument("--read", type=str, metavar="DATE", help="查看指定日期的复盘")
    parser.add_argument("--model", type=str, help="指定模型（覆盖环境变量）")
    args = parser.parse_args()

    global MODEL
    if args.model:
        MODEL = args.model

    if args.list:
        list_reviews()
    elif args.read:
        read_review(args.read)
    else:
        client = get_client()
        if args.week:
            do_retrospective(client, "week")
        elif args.month:
            do_retrospective(client, "month")
        else:
            # Loop mode: keep reviewing until user quits
            while True:
                interactive_review(client)
                print("\n再来一次？(y/n): ", end="")
                again = input().strip().lower()
                if again not in ("y", "yes", ""):
                    print("再见！👋")
                    break


if __name__ == "__main__":
    main()
