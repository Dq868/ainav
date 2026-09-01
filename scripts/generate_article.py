#!/usr/bin/env python3
"""每日 AI 文章生成：仅使用免费模型，自动多供应商切换 + 质量校验"""

import os
import sys
import json
import re
import datetime
import urllib.request
import urllib.error

EXISTING_TOPICS = [
    "ChatGPT vs Claude vs Gemini", "AI代码助手对比", "免费AI工具推荐",
    "AI视频生成", "国产AI大模型", "Midjourney教程", "Cursor IDE",
    "AI营销工具", "AI语音合成", "AI视频创作流程", "Perplexity教程",
    "AI代码审查", "AI绘图工具对比", "AI学习工具", "AI工具价格大全",
    "Midjourney指南", "AI创作全流程", "Claude深度使用", "Gemini进阶技巧",
    "AI PPT工具", "AI搜索引擎", "Notion AI教程", "AI音乐生成",
    "AI设计工具推荐", "AI编程效率工具", "数据处理AI工具",
    "AI写作工作流", "AI提示词工程", "AI会议记录", "AI绘画风格一致性",
    "零代码AI智能体", "AI英文写作", "AI电商出图", "AI数据隐私",
    "AI行业资讯工作流",
]

VALID_CATS = {"chat", "code", "image", "video", "audio", "office", "search", "other"}
CAT_ALIASES = {
    "technology": "chat", "ai": "other", "tool": "other", "tools": "other",
    "workflow": "office", "productivity": "office", "writing": "chat",
    "3": "office", "2": "search", "1": "chat",
}

SYSTEM_PROMPT = """你是一个AI工具领域的专业写手。请生成一篇关于AI工具的原创实用文章。
要求：
1. 只输出JSON，不要任何其他文字，不要输出markdown代码块
2. JSON格式：{"title": "标题", "summary": "一句话摘要", "cat": "分类id", "icon": "emoji", "relatedTools": ["工具id"], "content": "文章HTML"}
3. content 用 HTML 格式，1200字左右，必须包含至少两个<h2>和若干<p><ul><li>
4. 分类id只能从 chat、code、image、video、audio、office、search、other 中选择
5. relatedTools 使用这些常见的工具id之一：chatgpt, claude, gemini, deepseek, kimi, doubao, tongyi, midjourney, dalle, flux, stable-diffusion, ideogram, recraft, leonardo, comfyui, copilot, cursor, windsurf, codex, v0, bolt, lovable, replit-agent, devin, tabnine, sora, runway, heygen, pika, jianying, capcut, kling, vidu, minimax, veed, elevenlabs, suno, udio, whisper, iflyrec, fish-audio, notion-ai, gamma, feishu, grammarly, beautiful-ai, wps-ai, otter, xinghuo, granica, microsoft-copilot, mieta, tiangong, consensus, elicit, scispace, check-ai, huggingface, replicate, poe, coze, dify, figma-ai, manus, autoai, grok
6. 不要写用户指定禁止的主题
7. 内容要具体、可操作、有真实场景，避免空话套话，不要在文章里提及“我是AI”或“由AI生成”"""


def build_user_prompt():
    return f"写一篇AI工具相关的原创实用文章。禁止写的主题：{'、'.join(EXISTING_TOPICS)}"


def post_json(url, key, payload, extra_headers=None):
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "ainav-bot/1.0",
    }
    if key:
        headers["Authorization"] = f"Bearer {key}"
    if extra_headers:
        headers.update(extra_headers)
    req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers=headers, method="POST")
    with urllib.request.urlopen(req, timeout=180) as resp:
        return json.loads(resp.read().decode("utf-8"))


def openai_chat(url, key, model):
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": build_user_prompt()},
        ],
        "temperature": 0.85,
        "max_tokens": 4096,
    }
    data = post_json(url, key, payload)
    return data["choices"][0]["message"]["content"].strip()


def gemini_chat(api_key, model="gemini-2.0-flash"):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
    payload = {
        "contents": [{"parts": [{"text": SYSTEM_PROMPT + "\n\n" + build_user_prompt()}]}],
        "generationConfig": {"temperature": 0.85, "maxOutputTokens": 8192},
    }
    data = post_json(url, None, payload)
    return data["candidates"][0]["content"]["parts"][0]["text"].strip()


def strip_fence(content):
    content = content.strip()
    if content.startswith("```"):
        lines = content.split("\n", 1)
        if len(lines) > 1:
            content = lines[1]
        content = re.sub(r"```[a-zA-Z]*\s*$", "", content).strip()
    return content


def parse_article(content):
    content = strip_fence(content)
    try:
        return json.loads(content)
    except Exception:
        pass
    m = re.search(r"\{[\s\S]*\}", content)
    if m:
        try:
            return json.loads(m.group(0))
        except Exception:
            pass
    raise ValueError("模型输出不是合法 JSON")


def normalize_cat(cat):
    cat = (cat or "").strip().lower()
    if cat in VALID_CATS:
        return cat
    if cat in CAT_ALIASES:
        return CAT_ALIASES[cat]
    return "other"


def plain_text_len(html):
    return len(re.sub(r"<[^>]+>", "", html or "").strip())


def validate_article(art):
    if not isinstance(art, dict):
        return False, "不是对象"
    title = str(art.get("title") or "").strip()
    summary = str(art.get("summary") or "").strip()
    content = str(art.get("content") or "").strip()
    cat = normalize_cat(art.get("cat"))
    art["cat"] = cat
    if len(title) < 6:
        return False, "标题过短"
    if len(summary) < 10:
        return False, "摘要过短"
    if plain_text_len(content) < 600:
        return False, "正文少于600字"
    if content.count("<h2") < 2:
        return False, "缺少至少两个 h2 小节"
    if not art.get("icon"):
        art["icon"] = "🤖"
    if not isinstance(art.get("relatedTools"), list):
        art["relatedTools"] = []
    return True, ""


def escape_js(s):
    s = s.replace("\\", "\\\\")
    s = s.replace("`", "\\`")
    s = s.replace("${", "\\${")
    return s


def append_article(article):
    today = datetime.date.today().isoformat()
    article.setdefault("id", "auto-" + today.replace("-", ""))
    article.setdefault("date", today)
    article.setdefault("summary", "")
    article.setdefault("relatedTools", [])
    article["id"] = re.sub(r"[^a-z0-9\-]", "", article["id"].lower().replace(" ", "-"))

    with open("articles.js", "r", encoding="utf-8") as f:
        js = f.read()

    existing_ids = set(re.findall(r"id: '([^']+)'", js))
    base_id = article["id"]
    i = 2
    while article["id"] in existing_ids:
        article["id"] = f"{base_id}-{i}"
        i += 1

    last_idx = js.rfind("\n];")
    if last_idx == -1:
        raise RuntimeError("No array end found in articles.js")

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


def providers():
    gh_token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_MODEL_TOKEN")
    if gh_token:
        for model in ("gpt-4o-mini", "gpt-4.1-mini", "gpt-4o"):
            yield f"github:{model}", lambda m=model: openai_chat(
                "https://models.inference.ai.azure.com/chat/completions", gh_token, m
            )
    if os.environ.get("GROQ_API_KEY"):
        yield "groq:llama-3.3-70b-versatile", lambda: openai_chat(
            "https://api.groq.com/openai/v1/chat/completions",
            os.environ["GROQ_API_KEY"], "llama-3.3-70b-versatile"
        )
    if os.environ.get("OPENROUTER_API_KEY"):
        yield "openrouter:deepseek-chat-free", lambda: openai_chat(
            "https://openrouter.ai/api/v1/chat/completions",
            os.environ["OPENROUTER_API_KEY"], "deepseek-chat:free"
        )
    if os.environ.get("GEMINI_KEY"):
        yield "gemini:flash", lambda: gemini_chat(os.environ["GEMINI_KEY"])


def main():
    attempts = []
    found = False
    for name, fn in providers():
        try:
            raw = fn()
            art = parse_article(raw)
            ok, reason = validate_article(art)
            if not ok:
                attempts.append(f"{name}: 质量校验未通过({reason})")
                continue
            print(f"provider={name}")
            append_article(art)
            found = True
            break
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", errors="replace")[:200]
            attempts.append(f"{name}: HTTP {e.code} {body}")
        except Exception as e:
            attempts.append(f"{name}: {type(e).__name__} {str(e)[:120]}")
    if not found:
        print("ALL FREE PROVIDERS FAILED: " + "; ".join(attempts), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
