#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
为全部文章生成静态 HTML 页面：/blog/<id>.html
- 正文（article.content）直接写入 HTML 源码，Googlebot 不执行 JS 也能读取。
- 静态写入 Article JSON-LD、canonical、title、description、og 标记。
- 相关的“相关工具”卡片（relatedTools）也静态渲染，风格与 JS 版一致。
- 保留与 article.html 一致的样式与顶部导航/页脚。

用法：
  python3 scripts/generate_article_pages.py
  （读取 ./articles.js 与 ./tools.js，输出到 ./blog/<id>.html；重复运行会覆盖）
"""
import os
import re
import sys
import json
import subprocess

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BLOG_DIR = os.path.join(REPO_ROOT, "blog")
SITE = "https://jzzai.cn"


def parse_js_array(var_name, filename):
    """通过 Node 解析某个 const 数组并返回 Python 列表。"""
    code = (
        "const fs=require('fs');const vm=require('vm');"
        f"const s=fs.readFileSync({json.dumps(filename)},'utf8');const sb={{}};"
        "vm.createContext(sb);"
        f"vm.runInContext(s+';globalThis.__out={var_name};',sb);"
        "console.log(JSON.stringify(sb.__out));"
    )
    out = subprocess.run(
        ["node", "-e", code], capture_output=True, text=True, timeout=30,
        check=True, cwd=REPO_ROOT,
    )
    return json.loads(out.stdout)


def esc(s):
    """HTML 转义（用于 meta/JSON-LD 里嵌入的文本）。"""
    return (str(s or "")
            .replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            .replace('"', "&quot;"))


def js_str(s):
    """JS 字符串转义（用于 JSON-LD 的 JSON 值，不能带未转义换行）。"""
    return json.dumps(str(s or ""), ensure_ascii=False)


def article_json_ld(art):
    """构造 Article 结构化数据。键顺序固定，使用 json.dumps 保证合法。"""
    return {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": art["title"],
        "description": art["summary"],
        "datePublished": art["date"],
        "dateModified": art["date"],
        "author": {"@type": "Organization", "name": "酱肘AI"},
        "publisher": {"@type": "Organization", "name": "酱肘AI", "url": SITE},
        "mainEntityOfPage": f"{SITE}/blog/{art['id']}",
    }


def related_tools_html(art, tool_by_id):
    """根据 relatedTools 生成相关工具卡片，与 JS 版结构一致。"""
    ids = (art.get("relatedTools") or [])[:4]
    cards = []
    for tid in ids:
        t = tool_by_id.get(tid)
        if not t:
            continue
        cards.append(
            f'<a class="related-card" href="/tool/{t["id"]}">'
            f'<div class="r-icon">{t.get("icon","🤖")}</div>'
            f'<div class="r-name">{esc(t.get("name",""))}</div>'
            f'<div class="r-desc">{esc(t.get("desc",""))}</div>'
            f"</a>"
        )
    if not cards:
        return ""
    return (
        '<div class="related-section">\n'
        '  <h3>🔗 相关工具</h3>\n'
        f'  <div class="related-grid">{"".join(cards)}</div>\n'
        "</div>"
    )


def render_article(art, tool_by_id, cat_label):
    """生成单个文章静态页的完整 HTML。"""
    title = f"{art['title']} — 酱肘AI"
    canonical = f"{SITE}/blog/{art['id']}"
    icon = art.get("icon") or "🤖"
    cat_text = f"{cat_label}" if cat_label else ""
    related = related_tools_html(art, tool_by_id)

    ld = article_json_ld(art)
    ld_str = json.dumps(ld, ensure_ascii=False)

    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<link rel="icon" type="image/svg+xml" href="/favicon.svg">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="robots" content="index, follow">
<meta property="og:type" content="article">
<meta property="og:site_name" content="酱肘AI">
<meta name="twitter:card" content="summary_large_image">
<meta name="google-site-verification" content="uKC3K2ArEDrW3FQkAgbXPG5RfJnbqdBkfNCckyB49ok" />
<meta name="google-site-verification" content="Wsq4c3zO5bibhXAw6kxO56XsaFS0xb9nKduMqGakfOY" />
<meta name="description" content="{esc(art["summary"])}">
<link rel="canonical" href="{canonical}" />
<title>{esc(title)}</title>
<meta property="og:title" content="{esc(art["title"])}">
<meta property="og:description" content="{esc(art["summary"])}">
<meta property="og:url" content="{canonical}">
<script type="application/ld+json">
{ld_str}
</script>
<style>
  *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
  :root {{
    --bg: #f7f8fa;
    --surface: #ffffff;
    --border: #e6e8ec;
    --text: #1a1d26;
    --text-secondary: #6b7280;
    --primary: #4f6cf7;
    --primary-light: #eef1ff;
    --primary-dark: #3b55d6;
    --ad-label: #9ca3af;
    --radius: 12px;
    --radius-sm: 8px;
    --max-w: 800px;
    --header-h: 64px;
  }}
  html {{ font-size: 16px; }}
  body {{
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, "Noto Sans SC", sans-serif;
    background: var(--bg); color: var(--text); line-height: 1.8;
  }}
  header {{
    position: sticky; top: 0; z-index: 100;
    background: rgba(255,255,255,.85); backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border-bottom: 1px solid var(--border);
    height: var(--header-h); display: flex; align-items: center;
  }}
  header .inner {{
    max-width: var(--max-w); margin: 0 auto; padding: 0 24px;
    width: 100%; display: flex; align-items: center; gap: 12px;
  }}
  .back-link {{
    display: flex; align-items: center; gap: 6px;
    color: var(--text-secondary); font-size: .9rem; font-weight: 500;
    text-decoration: none; padding: 6px 12px; border-radius: var(--radius-sm);
    transition: background .15s, color .15s;
  }}
  .back-link:hover {{ background: var(--primary-light); color: var(--primary); }}
  .container {{ max-width: var(--max-w); margin: 0 auto; padding: 32px 24px 60px; }}
  .article-content {{
    background: var(--surface); border: 1px solid var(--border);
    border-radius: var(--radius); padding: 40px 44px;
  }}
  .article-content .icon-wrap {{
    width: 56px; height: 56px; border-radius: 14px;
    background: var(--primary-light); display: flex; align-items: center;
    justify-content: center; font-size: 2rem; margin-bottom: 16px;
  }}
  .article-content h1 {{ font-size: 1.6rem; font-weight: 700; margin-bottom: 8px; line-height: 1.4; }}
  .article-meta {{
    color: var(--text-secondary); font-size: .85rem; margin-bottom: 24px;
    display: flex; gap: 16px; align-items: center;
  }}
  .article-content h2 {{
    font-size: 1.2rem; font-weight: 600; margin: 32px 0 12px; padding-bottom: 8px;
    border-bottom: 1px solid var(--border);
  }}
  .article-content h3 {{ font-size: 1.05rem; font-weight: 600; margin: 24px 0 8px; }}
  .article-content p {{ margin-bottom: 16px; color: var(--text); }}
  .article-content table {{ width: 100%; border-collapse: collapse; margin: 16px 0; font-size: .9rem; }}
  .article-content th, .article-content td {{ padding: 10px 14px; border: 1px solid var(--border); text-align: left; }}
  .article-content th {{ background: var(--bg); font-weight: 600; }}
  .related-section {{ margin-top: 24px; padding-top: 24px; border-top: 1px solid var(--border); }}
  .related-section h3 {{ font-size: 1rem; font-weight: 600; margin-bottom: 12px; }}
  .related-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(180px, 1fr)); gap: 12px; }}
  .related-card {{
    background: var(--bg); border: 1px solid var(--border);
    border-radius: var(--radius-sm); padding: 14px; cursor: pointer; text-decoration: none;
    color: inherit; display: block; transition: box-shadow .2s;
  }}
  .related-card:hover {{ box-shadow: 0 2px 8px rgba(0,0,0,.06); }}
  .related-card .r-icon {{ width: 32px; height: 32px; border-radius: 8px; background: var(--primary-light); display: flex; align-items: center; justify-content: center; font-size: 1rem; margin-bottom: 6px; }}
  .related-card .r-name {{ font-weight: 600; font-size: .88rem; }}
  .related-card .r-desc {{ font-size: .78rem; color: var(--text-secondary); }}
  footer {{ text-align: center; padding: 32px 24px; border-top: 1px solid var(--border); color: var(--text-secondary); font-size: .82rem; }}
  footer a {{ color: var(--primary); text-decoration: none; }}
  @media (max-width: 640px) {{
    .article-content {{ padding: 24px 20px; }}
    .article-content table {{ font-size: .78rem; }}
    .article-content th, .article-content td {{ padding: 6px 8px; }}
  }}
</style>
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-9519141393679331" crossorigin="anonymous"></script>
<script async src="https://www.googletagmanager.com/gtag/js?id=G-006K3L3V06"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());
  gtag('config', 'G-006K3L3V06');
</script>
</head>
<body>

<header>
  <div class="inner">
    <a class="back-link" href="/">
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="15 18 9 12 15 6"/></svg>
      返回首页
    </a>
  </div>
</header>

<div class="container">
  <div id="content">
    <div class="article-content">
      <div class="icon-wrap">{icon}</div>
      <h1>{esc(art["title"])}</h1>
      <div class="article-meta">
        <span>📅 {esc(art["date"])}</span>
        <span>📂 {esc(cat_text)}</span>
      </div>
      {art["content"]}
      {related}
    </div>
  </div>
</div>

<footer>© 2026 酱肘AI &mdash; <a href="/">发现最好的 AI 工具</a> &nbsp;·&nbsp;
  <a href="/about">关于我们</a> &nbsp;·&nbsp;
  <a href="/contact">联系我们</a> &nbsp;·&nbsp;
  <a href="/privacy">隐私政策</a> &nbsp;·&nbsp;
  <a href="/terms">服务条款</a> &nbsp;·&nbsp;
  <a href="/editorial">编辑准则</a>
</footer>

</body>
</html>
"""


def main():
    articles = parse_js_array("ARTICLES", "articles.js")
    tools = parse_js_array("TOOLS", "tools.js")
    cats = parse_js_array("CATEGORIES", "tools.js")

    tool_by_id = {t["id"]: t for t in tools}
    cat_label = {c["id"]: c.get("label", "") for c in cats}

    os.makedirs(BLOG_DIR, exist_ok=True)
    written = []
    skipped = []
    for art in articles:
        if not art.get("id") or not art.get("title") or not art.get("content"):
            skipped.append(art.get("id", "?"))
            continue
        html = render_article(art, tool_by_id, cat_label.get(art.get("cat"), ""))
        path = os.path.join(BLOG_DIR, f"{art['id']}.html")
        with open(path, "w", encoding="utf-8") as f:
            f.write(html)
        written.append(art["id"])

    # 可选：生成 /blog/index 列表页（所有文章卡片），便于直接访问
    print(f"已生成 {len(written)} 篇文章静态页 -> {BLOG_DIR}")
    if skipped:
        print("跳过(缺字段):", skipped)
    print("工具条目: %d, 分类: %d" % (len(tools), len(cats)))


if __name__ == "__main__":
    main()
