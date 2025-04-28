from collections import defaultdict
import os
import re

input_path = "weibo_originals.txt"
output_dir = "year_chunks"
os.makedirs(output_dir, exist_ok=True)

# ===== 你的分析 Prompt =====
prompt = """下面是一个人一年内所有的微博发言（不含转发内容、图片或链接，只保留了他自己写下的话），请你根据这些发言，尽可能细致地描绘出这个人给你的印象。

不要分析时间趋势，也不需要列出兴趣分类；而是从你读完这些发言后，对“这个人是怎样的”所产生的整体感受来写。

你可以从他的表达方式、情绪节奏、用词偏好、在意的东西、说话的方式、避而不谈的事物等方面切入。

写作方式上，请不要使用列表，而是用自然段落来书写。

你的目标不是总结内容，而是描摹出一个人。

你可以像一个敏感的读者、也像一个擅长心理描写的作家。带点判断，但不需要断言；带点感情，但不必评价；尽量丰富、细腻、有温度。

最后，请你尝试根据这些发言的语言方式、表达倾向与思维特征，推测这个人的 MBTI 类型，并自然地融入描述之中。你不需要将其作为一个分析模块独立列出，而是像一位理解深刻的读者，顺势地说出“我觉得他/她可能是……”并进一步解释原因。请让这个人格推测成为对这个人整体描写的有机延伸，而不是附加标签。
"""

# 新增日期模式
date_pattern = re.compile(r'^\d{4}-\d{2}-\d{2}\s')

def is_valid_weibo_line(line):
    """判断是否是有效的微博条目"""
    return bool(date_pattern.match(line))

def build_chunks(input_path):
    lines_by_year = defaultdict(list)

    with open(input_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or not is_valid_weibo_line(line):
                continue
            year = line[:4]
            content = line[11:].strip()
            if content:
                lines_by_year[year].append(content)

    for year, entries in sorted(lines_by_year.items()):
        filename = os.path.join(output_dir, f"{year}.txt")
        with open(filename, "w", encoding="utf-8") as f:
            f.write(prompt.strip() + "\n\n")
            f.write("\n".join(entries))

        print(f"✅ 写入 {filename}，共 {len(entries)} 条微博")

if __name__ == "__main__":
    build_chunks(input_path)

