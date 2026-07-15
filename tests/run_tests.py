"""自动化测试脚本 - 模拟完整每日复盘流程"""
import os
import sys

os.environ["DEEPSEEK_API_KEY"] = "sk-8088f62929604a8981f347141be5a70f"

sys.path.insert(0, r"C:\Users\ASUS\ai-daily-review-coach\skill\scripts")
from daily_review import get_client, generate_questions, synthesize_review, format_review_markdown

client = get_client()

# 测试样例1
daily_log = """今天上午去上了大数据课，讲了 Spark 的 RDD 转换操作，半懂不懂的。
下午在图书馆复习，试着写了一个简单的 WordCount，跑通了但不太理解原理。
晚上和室友打了两把游戏，然后看了一会儿 B 站就睡了。"""

print("=" * 50)
print("测试1: 生成追问")
print("=" * 50)
print(f"输入: {daily_log[:50]}...\n")

questions = generate_questions(client, daily_log)
for i, q in enumerate(questions, 1):
    print(f"追问{i}: {q}")

# 模拟回答
mock_answers = [
    "老师讲得太快了，而且我Python基础一般，跟不上思路",
    "我照着教程敲的，但RDD的转换逻辑不理解，比如map和flatMap的区别",
    "确实会滚雪球，我觉得应该课后花30分钟看官方文档的第一个例子"
]
qa_pairs = list(zip(questions, mock_answers))

print("\n" + "=" * 50)
print("测试2: 综合复盘")
print("=" * 50)

synthesis = synthesize_review(client, daily_log, qa_pairs)
print(f"关键事件: {synthesis.get('key_events')}")
print(f"模式识别: {synthesis.get('patterns')}")
print(f"卡点: {synthesis.get('blockers')}")
print(f"核心洞察: {synthesis.get('insight')}")
print(f"明天焦点: {synthesis.get('tomorrow_focus')}")

print("\n" + "=" * 50)
print("测试3: 生成 Markdown")
print("=" * 50)

md = format_review_markdown("2026-07-15", daily_log, qa_pairs, synthesis)
print(md[:500])
print("...\n")

# 保存到测试目录
from pathlib import Path
test_dir = Path(r"C:\Users\ASUS\ai-daily-review-coach\tests\output")
test_dir.mkdir(exist_ok=True)
(test_dir / "test_review_2026-07-15.md").write_text(md, encoding="utf-8")

print("测试完成！复盘文件已保存到 tests/output/test_review_2026-07-15.md")
