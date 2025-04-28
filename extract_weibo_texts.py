import json
import re
from datetime import datetime

path = "weibo-data.json"
output_originals = "weibo_originals.txt"
output_retweets = "weibo_retweets.txt"

def ts_to_day(ts):
    """只保留日期：2024-06-29"""
    if isinstance(ts, int):
        return datetime.fromtimestamp(ts / 1000).strftime("%Y-%m-%d")
    elif isinstance(ts, str):
        try:
            dt = datetime.strptime(ts, "%a %b %d %H:%M:%S %z %Y")
            return dt.strftime("%Y-%m-%d")
        except Exception:
            return "[InvalidDate]"
    else:
        return "[NoTime]"

def clean_html_links(text):
    """删除所有<a href=...>标签"""
    return re.sub(r'<a .*?href=.*?>|</a>', '', text)

def remove_urls(text):
    """删除所有 URL，包括 http(s)://，weibo.com，短链"""
    url_pattern = r'(https?://\S+|www\.\S+|weibo\.com/\S+)'
    return re.sub(url_pattern, '', text)

def replace_html_breaks(text):
    """把 <br> <br/> <br /> 转成换行符"""
    return re.sub(r'(?i)<br\s*/?>', '\n', text)

def extract_my_text(s):
    if not isinstance(s, str):
        return ""

    # 清除图片、换行、零宽字符
    s = re.sub(r'\[img://.*?\]', '', s)
    s = s.replace("\n", " ").replace("\u200b", "").strip()

    # 删除 HTML 标签
    s = clean_html_links(s)

    # 删除 URL
    s = remove_urls(s)

    # 判断是否是纯转发（开头是 // 或其 HTML 变体）
    if re.match(r'^//(\s|<a|@|http|weibo\.com)', s):
        return ""

    # 回复微博：直接取冒号后的内容
    if s.startswith("回复"):
        parts = s.split(":", 1)
        if len(parts) == 2:
            s = parts[1].strip()

    # 去除后续转发链
    if "//<a" in s:
        s = s.split("//<a", 1)[0].strip()
    elif "//@" in s:
        s = s.split("//@", 1)[0].strip()
    elif "//weibo.com" in s:
        s = s.split("//weibo.com", 1)[0].strip()

    # 无效模板内容过滤
    if s in {"转发微博", "图片评论", "分享图片", "转发视频"}:
        return ""

    return s.strip()

with open(path, "r", encoding="utf-8") as f:
    data = json.load(f)

weibo_list = data.get("weibo", [])

originals = []
retweets = []

for w in weibo_list:
    day = ts_to_day(w.get("created_at"))
    raw = w.get("text", "")
    cleaned = extract_my_text(raw)

    if not cleaned:
        continue

    line = f"{day} {cleaned}"
    if "retweeted_status" not in w:
        originals.append(line)
    else:
        retweets.append(line)

with open(output_originals, "w", encoding="utf-8") as f:
    for line in originals:
        line = replace_html_breaks(line)
        f.write(line + "\n")

with open(output_retweets, "w", encoding="utf-8") as f:
    for line in retweets:
        line = replace_html_breaks(line)
        f.write(line + "\n")

print(f"✅ 已输出 {len(originals)} 条原创 到 {output_originals}")
print(f"✅ 已输出 {len(retweets)} 条转发/回复 到 {output_retweets}")
