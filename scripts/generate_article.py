#!/usr/bin/env python3
"""Generate a daily AI tool article via DeepSeek API and append to articles.js"""

import os, sys, json, re, datetime, urllib.request, urllib.error

EXISTING_TOPICS = [
    "ChatGPT vs Claude vs Gemini", "AI代码助手对比", "免费AI工具推荐",
    "AI视频生成", "国产AI大模型", "Midjourney教程", "Cursor IDE",
    "AI营销工具", "AI语音合成", "AI视频创作流程", "Perplexity教程",
    "AI代码审查", "AI绘图工具对比", "AI学习工具", "AI工具价格大全",
    "Midjourney指南", "AI创作全流程", "Claude深度使用", "Gemini进阶技巧",
    "AI PPT工具", "AI搜索引擎", "Notion AI教程", "AI音乐生成",
    "AI设计工具推荐", "AI编程效率工具", "数据处理AI工具",
]

CATEGORIES = {
    "chat": "对话助手", "code": "编程开发", "image": "图像生成",
    "video": "视频创作", "audio": "音频处理", "office": "办公效率",
    "search": "搜索工具", "other": "其他工具",
}

SYSTEM_PROMPT = """你是一个AI工具领域的专业写手。请生成一篇关于AI工具的原创文章。
要求：
1. 只输出JSON，不要任何其他文字
2. JSON格式：{"title": "标题", "summary": "一句话摘要", "cat": "分类id", "icon": "emoji", "relatedTools": ["id1", "id2"], "content": "文章HTML"}
3. content 用 HTML 格式，1000-1500字，用<h2><h3><p><ul><li>标签
4. 不要写用户指定禁止的主题
5. 要实用、有深度，适合中文读者"""


def call_deepseek(api_key: str) -> dict:
    payload = json.dumps({
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"写一篇AI工具相关的原创实用文章。禁止写的主题：{'、'.join(EXISTING_TOPICS)}"}
        ],
        "temperature": 0.85,
        "max_tokens": 4096,
    }).encode("utf-8")

    req = urllib.request.Request(
        "https://api.deepseek.com/v1/chat/completions",
        data=payload,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
            "User-Agent": "ainav-bot/1.0",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        print(f"API HTTP {e.code}: {body}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"API error: {e}", file=sys.stderr)
        sys.exit(1)

    content = data["choices"][0]["message"]["content"].strip()
    # Strip code fences if present
    if content.startswith("```"):
        lines = content.split("\n", 1)
        if len(lines) > 1:
            content = lines[1]
        if content.endswith("```"):
            content = content[:-3].strip()
        elif "```" in content:
            content = content.rsplit("```", 1)[0].strip()

    return json.loads(content)


def escape_js(s: str) -> str:
    s = s.replace("\\", "\\\\")
    s = s.replace("`", "\\`")
    s = s.replace("${", "\\${")
    return s


def append_article(article: dict):
    today = datetime.date.today().isoformat()
    article.setdefault("id", "auto-" + today.replace("-", ""))
    article.setdefault("date", today)
    article.setdefault("summary", "")
    article.setdefault("relatedTools", [])
    article["id"] = re.sub(r"[^a-z0-9\-]", "", article["id"].lower().replace(" ", "-"))

    with open("articles.js", "r", encoding="utf-8") as f:
        js = f.read()

    last_idx = js.rfind("\n];")
    if last_idx == -1:
        print("No array end found in articles.js", file=sys.stderr)
        sys.exit(1)

    fields = []
    for key, val in article.items():
        if key == "content":
            fields.append(f"    content: `\n{escape_js(val)}\n    `")
        elif key == "relatedTools" and val:
            fields.append(f"    relatedTools: [{', '.join(repr(v) for v in val)}]")
        elif isinstance(val, str):
            fields.append(f"    {key}: '{escape_js(val)}'")
        elif isinstance(val, list):
            fields.append(f"    {key}: [{', '.join(repr(v) for v in val)}]")

    entry = "  {\n" + ",\n".join(fields) + "\n  },\n"
    js = js[:last_idx] + entry + js[last_idx:]

    with open("articles.js", "w", encoding="utf-8") as f:
        f.write(js)

    print(f"OK: {article['title']}")


def main():
    api_key = os.environ.get("DEEPSEEK_KEY")
    if not api_key:
        print("DEEPSEEK_KEY not set", file=sys.stderr)
        sys.exit(1)

    article = call_deepseek(api_key)
    append_article(article)


if __name__ == "__main__":
    main()
