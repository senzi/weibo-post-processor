# 微博人格年度总结生成器

本项目帮助你从自己的微博导出数据，经过清洗和处理，最终生成一份【可浏览的年度人格变化总结网页】，并可进一步分析跨年份的人格变化轨迹。

---

## 0. 前置准备

首先，需要使用 [Weibo-archiver](https://github.com/Chilfish/Weibo-archiver) 项目导出你的微博数据。

### 导出设置参考

在 Weibo-archiver 中导出微博时，请注意选择以下选项：

- ✅ **导出全部微博**（不限制时间）
- ✅ **只导出微博**（不要勾选只导出关注列表）
- ❌ **不包含转发**（可以关闭）
- ❌ **不包含转发的图片**（可以关闭）
- ❌ **不包含评论**（可以关闭）

导出后，得到一个名为：

```
weibo-data.json
```
的文件。

---

## 1. 准备数据

将刚才导出的 `weibo-data.json` **复制到本项目根目录下**。

---

## 2. 清洗微博文本

执行：

```bash
python extract_weibo_texts.py
```

这一步会生成：

```
weibo_originals.txt
weibo_retweets.txt
```

后续主要使用 `weibo_originals.txt`。

---

## 3. 按年份切分原始发言并附加分析提示

执行：

```bash
python prepare_yearly_profiles.py
```

这一步会在 `year_chunks/` 目录下，生成每年一个 `.txt` 文件，每个文件前面包含了分析提示（Prompt）。

---

## 4. 使用你喜欢的 LLM 进行逐年人格分析

- 将 `year_chunks/` 中每个年份的 `.txt` 文件分别输入给你喜欢的大模型（如 GPT-4o、Claude-3、DeepSeek 等）。
- 注意根据 LLM 支持的最大上下文长度，合理控制输入量（若年份太长，可手动分段）。
- **分析结果请保存为纯文本 `.txt` 文件**，放入：

```
result/
```

> 📌 **注意事项：**
> - `result/` 目录下只能放 LLM 分析输出的 `.txt` 文件，**不要混入其他文件**。
> - 每个文件建议以年份命名，如 `2022.txt`、`2023.txt`；
> - 若有整体总结，可命名为 `all_years.txt` 或 `summary.txt`。

---

## 5. 生成跨年份变化分析提示（可选，但推荐）

在完成逐年分析后，执行：

```bash
python generate_all_prompt.py
```

这一步会根据 `result/` 里的所有 `.txt` 文件，自动生成一份整合分析提示：

```
all_combined_prompt.txt
```

- 内容包括四年（或更多年）的人格素描；
- 可输入给 LLM，得到【跨年份人格变化分析】的完整回答。

---

## 6. 自动生成完整网页

执行：

```bash
python generate_index.py
```

- 会读取 `template.html`；
- 将 `result/` 中每个 `.txt` 文件作为一个 Tab 页面；
- 最终生成美观可交互的网页：

```
www/index.html
```

打开即可查看你的微博年度人格总结。

---

## 📌 小提示

- 不限制年份数量，可任意增加/减少年份或总结文件。
- 自动识别文件名，无需修改模板。
- 每段发言自动加段落缩进，保证良好阅读体验。
- 所有生成的 HTML 页面本地浏览，无需联网，无隐私泄露风险。
- 跨年份综合分析步骤（`generate_all_prompt.py`）是可选但推荐的，用于深入洞察变化轨迹。

---

# 🎉 享受探索自己的轨迹吧！