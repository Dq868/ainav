#!/usr/bin/env python3
"""AI 文章生成：仅使用免费模型，自动多供应商切换 + 质量校验 + 标题去重。

注意（2026-09-02 复盘）：模板兜底已移除。模板基于站内已有数据生成，
与工具页内容重复（实测相似度 ~72%），会构成“规模化内容滥用”。
没有可用 AI 供应商时，本脚本不生成任何文章。
"""

import os
import sys
import json
import re
import datetime
import urllib.request
import urllib.error

# 仓库根目录：脚本位于 scripts/ 下，数据文件（tools.js/tool-content.js/articles.js）在仓库根。
# 无论从仓库根还是 scripts/ 目录运行，都能定位到正确路径。
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

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

CAT_LABELS = {
    "chat": "对话助手", "code": "编程开发", "image": "图像生成",
    "video": "视频创作", "audio": "音频处理", "office": "办公效率",
    "search": "搜索工具", "other": "其他工具",
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


# 低质量模板填充文的特征短语：一旦命中即判定为低价值内容并拒绝。
# 这些短语来自此前“两个工具二选一/工作流/避坑”模板，正是 AdSense 判低价值内容的典型样本。
LOW_QUALITY_MARKERS = [
    "先选哪一个，还是两个一起用",
    "这篇文章从定位、场景、功能、成本",
    "从定位、场景、功能、成本",
    "五个角度给出可执行的判断方法",
    "先明确你的使用场景",
    "选工具之前先回答三个问题",
    "很多用户在第一次接触时都会纠结",
    "核心价值在于",
    "更强调：",
    "值得注意的功能点",
    "工具没有绝对的好坏，只有适不适合",
    "把上面的方法执行一遍",
    "两者恰好覆盖流程的不同环节",
    "可以重点使用的能力",
]


def text_stats(html):
    """返回 (纯文本, 去标签后长度, 句子数)。"""
    txt = re.sub(r"<[^>]+>", " ", html or "")
    txt = re.sub(r"\s+", " ", txt).strip()
    sentences = re.split(r"[。！？\n]+", txt)
    sentences = [s.strip() for s in sentences if len(s.strip()) >= 8]
    return txt, len(txt), len(sentences)


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
    txt, tl, sn = text_stats(content)
    # 质量关卡（区分真实内容与低质模板填充文）
    # 字数下限设 600：足够高的信息密度，同时不会误杀基于真实深度数据的合理工具指南。
    # 真正识别“低价值内容”靠的是下方的模板特征检测与结构检查。
    if tl < 600:
        return False, f"正文少于600字(当前{tl})"
    if content.count("<h2") < 3:
        return False, "缺少至少三个 h2 小节"
    if sn < 6:
        return False, "有效句子过少，疑似碎片堆砌"
    # 模板填充特征检测：命中即判定为低价值内容
    for mk in LOW_QUALITY_MARKERS:
        if mk in content:
            return False, f"命中低质模板特征: {mk}"
    if not art.get("icon"):
        art["icon"] = "🤖"
    if not isinstance(art.get("relatedTools"), list):
        art["relatedTools"] = []
    return True, ""


def _norm_title(s):
    """标题归一化：去掉标点与空白，便于去重比较。"""
    return re.sub(r"[\s，。、：；！？·\-—/\\()（）【】\[\]“”\"'’]+", "", str(s or ""))


def load_existing_titles():
    """读取 articles.js 中已有文章的标题列表。"""
    try:
        path = os.path.join(REPO_ROOT, "articles.js")
        with open(path, encoding="utf-8") as f:
            js = f.read()
        return re.findall(r"title: '([^']+)'", js)
    except Exception as e:
        print(f"load_existing_titles failed: {e}", file=sys.stderr)
        return []


def check_duplicate(title, existing_titles, threshold=0.55):
    """检查标题与已有文章是否过于相似，避免产出重复内容。

    用 difflib 比较归一化标题；阈值 0.55 时，像
    “AI写作辅助工具实战：从选题到成稿的高效工作流” 与
    “AI写作辅助工具深度使用指南：从大纲到终稿的高效工作流”
    这类高度雷同的标题会被拦下。
    """
    import difflib
    nt = _norm_title(title)
    if not nt:
        return True, ""
    for old in existing_titles:
        no = _norm_title(old)
        if not no:
            continue
        r = difflib.SequenceMatcher(None, nt, no).ratio()
        if r >= threshold:
            return True, f"与已有文章过于相似({r:.2f}): {old}"
    return False, ""


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

    with open(os.path.join(REPO_ROOT, "articles.js"), "r", encoding="utf-8") as f:
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

    entry = "  {\n" + ",\n".join(fields) + "\n  },"
    prefix = js[:last_idx].rstrip()
    if not prefix.endswith(","):
        prefix += ","
    js = prefix + "\n" + entry + "\n" + js[last_idx:].lstrip("\n")

    with open(os.path.join(REPO_ROOT, "articles.js"), "w", encoding="utf-8") as f:
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
    existing_titles = load_existing_titles()
    for name, fn in providers():
        try:
            raw = fn()
            art = parse_article(raw)
            ok, reason = validate_article(art)
            if not ok:
                attempts.append(f"{name}: 质量校验未通过({reason})")
                continue
            dup, why = check_duplicate(art.get("title", ""), existing_titles)
            if dup:
                attempts.append(f"{name}: 内容重复({why})")
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
        # 重要：不再使用“模板兜底”生成文章。
        # 原因（2026-09-02 复盘）：此前的模板兜底基于 tool-content.js 的数据生成
        # “<工具名> 深度使用指南”，与站内已有的 /tool/<id> 工具页内容高度重复
        # （实测相似度 ~72%），且每天生成一篇、结构与标题几乎一致，属于 Google
        # 垃圾内容政策中的“规模化内容滥用（scaled content abuse）”，是 AdSense
        # 反复判定“低价值内容”的直接来源。模板天然无法产出独特内容，因此：
        #   —— 没有可用的真实 AI 供应商时，本次不生成任何文章（安全退出）。
        print("FREE PROVIDERS FAILED, 本次不生成文章（已禁用模板兜底以避免重复内容）: "
              + "; ".join(attempts), file=sys.stderr)
        sys.exit(0)


if __name__ == "__main__":
    main()
