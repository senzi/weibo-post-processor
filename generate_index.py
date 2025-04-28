import os

template_path = "template.html"
result_dir = "result"
output_dir = "www"
output_file = os.path.join(output_dir, "index.html")

def load_text(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read().strip()

def slugify(name):
    """转成适合 HTML ID 的安全字符串"""
    return name.lower().replace(" ", "_").replace(".", "_")

def format_text_to_html(text):
    """把纯文本根据空行分段，生成<p>段落"""
    paragraphs = [f"<p>{para.strip()}</p>" for para in text.split("\n\n") if para.strip()]
    return "\n".join(paragraphs)

def main():
    template_path = "template.html"
    result_dir = "result"
    output_dir = "www"
    output_file = os.path.join(output_dir, "index.html")

    if not os.path.exists(result_dir):
        print(f"❌ 错误：未找到 result/ 目录。请先准备好 .txt 文件！")
        return

    if not os.path.exists(template_path):
        print(f"❌ 错误：未找到 template.html。请确认模板文件存在！")
        return

    with open(template_path, "r", encoding="utf-8") as f:
        template_html = f.read()

    txt_files = sorted([f for f in os.listdir(result_dir) if f.endswith(".txt")])

    if not txt_files:
        print(f"⚠️ result/ 目录下没有找到任何 .txt 文件。")
        return

    tabs_html = []
    sections_html = []

    for idx, filename in enumerate(txt_files):
        title = filename[:-4]  # 去掉 .txt
        safe_id = slugify(title)

        # 导航按钮
        btn_class = "active" if idx == 0 else ""
        tabs_html.append(f'<button onclick="show(\'{safe_id}\')" class="{btn_class}">{title}</button>')

        # 内容区
        section_class = "section active" if idx == 0 else "section"
        raw_text = load_text(os.path.join(result_dir, filename))
        html_text = format_text_to_html(raw_text)

        section_html = f"""
        <div id="{safe_id}" class="{section_class}">
          <div class="year-title">✨ {title} ✨</div>
          {html_text}
        </div>
        """
        sections_html.append(section_html.strip())

    # 替换模板
    final_html = template_html.replace("<!-- inject_tabs_here -->", "\n".join(tabs_html))
    final_html = final_html.replace("<!-- inject_sections_here -->", "\n".join(sections_html))

    os.makedirs(output_dir, exist_ok=True)
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(final_html)

    print(f"\n🎉 已成功生成：{output_file}")

if __name__ == "__main__":
    main()
