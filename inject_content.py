import os

html_path = "www/index.html"
result_dir = "result"

year_files = {
    "2022": "2022.txt",
    "2023": "2023.txt",
    "2024": "2024.txt",
    "2025": "2025.txt",
    "summary": "all_years.txt"
}

def load_text(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        # 只去除首尾的空白，但保留内部的空行格式
        return f.read().strip()

def inject_into_html(template, marker, content):
    return template.replace(marker, content)

def main():
    with open(html_path, "r", encoding="utf-8") as f:
        html = f.read()

    for key, filename in year_files.items():
        path = os.path.join(result_dir, filename)
        marker = f"（请在此处粘贴 {filename} 的内容）"
        if os.path.exists(path):
            text = load_text(path)
            html = inject_into_html(html, marker, text)
        else:
            print(f"⚠️  未找到文件：{path}")

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)

    print("✅ 所有内容已成功注入到 index.html")

if __name__ == "__main__":
    main()