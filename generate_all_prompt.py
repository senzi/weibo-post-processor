import os
import re

result_dir = "result"
output_file = "all_combined_prompt.txt"

# 开头的指引
prompt_header = """以下是一个人从 xxxx 年到 xxxx 年连续x年人格描写的分析文字，内容是他每年微博发言背后所展现出的性格与心理状态侧写（包括 MBTI 推测）。 

请你阅读这几年的人格素描，试着从中看出这个人正在经历什么变化，或者正在哪些方面维持着一种长期的稳定。

你可以关注他的：

情绪表达密度是否有变化？

语言节奏与思维风格是否趋于某种极端或趋向融合？

兴趣重心是否发生了转移？

表达欲、社交姿态、自我意识、内耗机制是否发生过结构性调整？

是否变得更主动？更谨慎？更讽刺或更柔软？

如果你在不同年份里感受到人格某种功能的加强或退潮，请试着将这些变化串联起来，像在观察一个人慢慢转身的过程。

最终写作请使用自然段，不要列表，不要年份标题，不要分类。请你用一种叙事性的语言，把这几年里这个人留下的文字轨迹，写成一段有情绪、有轮廓、有时间张力的心理画像。

如果你愿意，也可以最后尝试重新判断他在最近的 MBTI 类型，并对比早期分析，看看这是否代表了一种人格功能的转化、强化或抑制。请用缓慢自然的方式写出这种推测，而不是强行标注类型变化。

"""

def slug_sort_key(name):
    """排序用，优先年份"""
    match = re.match(r'^(\d{4})', name)
    if match:
        return int(match.group(1))
    return 9999  # summary.txt等放到最后

def load_text(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read().strip()

def main():
    if not os.path.exists(result_dir):
        print(f"❌ 错误：未找到 result/ 目录。")
        return

    txt_files = [f for f in os.listdir(result_dir) if f.endswith(".txt") and f != "all_combined_prompt.txt"]
    if not txt_files:
        print(f"⚠️ 结果目录下没有找到可用的 .txt 文件。")
        return

    # 排序
    txt_files = sorted(txt_files, key=lambda x: slug_sort_key(x))

    years = []
    combined = []

    for filename in txt_files:
        year = filename[:-4]  # 去掉 .txt
        years.append(year)
        content = load_text(os.path.join(result_dir, filename))
        combined.append(f"{year}(年)\n{content}")

    # 填补年份
    if years:
        first_year = years[0]
        last_year = years[-1]
        year_span = f"{first_year} 年到 {last_year} 年连续{len(years)}年"
    else:
        year_span = "未知年份"

    final_prompt = prompt_header.replace("xxxx 年到 xxxx 年连续x年", year_span)

    # 组合输出
    final_text = final_prompt.strip() + "\n\n" + "\n\n".join(combined)

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(final_text)

    print(f"✅ 已生成完整变化分析 Prompt：{output_file}")

if __name__ == "__main__":
    main()
