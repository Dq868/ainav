#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
国内化改造：移除被墙的 Google 脚本（GA4 / AdSense），植入百度统计与百度自动推送。

背景：站点面向国内用户，而 googletagmanager.com（GA4）与 pagead2.googlesyndication.com
（AdSense）在国内被墙，浏览器会持续尝试连接并超时，拖慢加载、影响百度 SEO。
国内站应改用百度统计（数据）与百度联盟（广告），并用百度自动推送加速收录。

用法：
  # 预览（不写盘）
  python3 scripts/migrate_to_domestic.py --baidu-tongji-id <ID>

  # 真正执行
  python3 scripts/migrate_to_domestic.py --baidu-tongji-id <ID> --apply

  # 暂未拿到统计 ID 时可用占位符（后续替换 BAIDU_TONGJI_ID 即可）
  python3 scripts/migrate_to_domestic.py --apply

处理的文件：根目录 .html + tool/*.html + blog/*.html
"""
import os
import re
import glob
import argparse

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ---- 需要移除的 Google 脚本 ----
GA4_LOADER_RE = re.compile(
    r'[ \t]*<script[^>]*src="https://www\.googletagmanager\.com/gtag/js\?id=[^"]*"[^>]*>\s*</script>\s*\n?',
    re.I,
)
# GA4 的配置块：包含 dataLayer 与 gtag('config' 的内联 script
GA4_CONFIG_RE = re.compile(
    r'[ \t]*<script>\s*\n(?=[^<]*dataLayer)(?=[^<]*gtag\()[^<]*</script>\s*\n?',
    re.I,
)
ADSENSE_LOADER_RE = re.compile(
    r'[ \t]*<script[^>]*src="https://pagead2\.googlesyndication\.com/[^"]*"[^>]*>\s*</script>\s*\n?',
    re.I,
)
# 兜底：任何指向 google 广告/统计域名的 script 标签
GOOGLE_ANY_RE = re.compile(
    r'[ \t]*<script[^>]*src="https://(?:www\.googletagmanager\.com|pagead2\.googlesyndication\.com|'
    r'www\.google-analytics\.com|googleads\.[^"]*)/[^"]*"[^>]*>\s*</script>\s*\n?',
    re.I,
)


def build_domestic_snippet(tongji_id):
    """生成百度统计 + 百度自动推送的 HTML 片段。"""
    tid = tongji_id or "BAIDU_TONGJI_ID"
    return f"""<!-- 百度统计（国内可用；把 BAIDU_TONGJI_ID 换成 tongji.baidu.com 里的 ID） -->
<script>
var _hmt = _hmt || [];
(function() {{
  var hm = document.createElement("script");
  hm.src = "https://hm.baidu.com/hm.js?{tid}";
  var s = document.getElementsByTagName("script")[0];
  s.parentNode.insertBefore(hm, s);
}})();
</script>
<!-- 百度自动推送：用户访问即向百度报备 URL，加速收录 -->
<script>
(function(){{
    var bp = document.createElement('script');
    var curProtocol = window.location.protocol.split(':')[0];
    if (curProtocol === 'https') {{
        bp.src = 'https://zz.bdstatic.com/linksubmit/push.js';
    }} else {{
        bp.src = 'http://push.zhanzhang.baidu.com/push.js';
    }}
    var s = document.getElementsByTagName("script")[0];
    s.parentNode.insertBefore(bp, s);
}})();
</script>
"""


def strip_google(html):
    """移除 Google 脚本，返回 (新html, 移除的标签数)。"""
    removed = 0
    for pat in (GA4_LOADER_RE, GA4_CONFIG_RE, ADSENSE_LOADER_RE):
        html, n = pat.subn("", html)
        removed += n
    html, n = GOOGLE_ANY_RE.subn("", html)
    removed += n
    return html, removed


def insert_domestic(html, snippet):
    """把国内脚本片段插到 </head> 之前（无 head 则插到 </body> 之前）。"""
    if "hm.baidu.com/hm.js" in html and "zz.bdstatic.com/linksubmit/push.js" in html:
        return html, False  # 已存在，避免重复注入
    if "</head>" in html:
        return html.replace("</head>", snippet + "</head>", 1), True
    if "</body>" in html:
        return html.replace("</body>", snippet + "</body>", 1), True
    return html, False


def target_files():
    files = [f for f in glob.glob(os.path.join(REPO_ROOT, "*.html"))]
    files += glob.glob(os.path.join(REPO_ROOT, "tool", "*.html"))
    files += glob.glob(os.path.join(REPO_ROOT, "blog", "*.html"))
    # 跳过搜索引擎验证文件（google*.html / baidu_verify_*.html 等），它们只需原样返回 token
    skip = re.compile(r"(?:^|/)(?:google[0-9a-f]+\.html|baidu_verify_[^/]*\.html)$", re.I)
    files = [f for f in files if not skip.search(f)]
    return sorted(files)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--baidu-tongji-id", default="", help="百度统计 ID（hm.js? 后面那串）")
    ap.add_argument("--apply", action="store_true", help="真正写盘")
    args = ap.parse_args()

    snippet = build_domestic_snippet(args.baidu_tongji_id)
    files = target_files()
    print(f"待处理 HTML 文件: {len(files)} 个")
    print(f"百度统计 ID: {args.baidu_tongji_id or '（未提供，将写入占位符 BAIDU_TONGJI_ID）'}")
    print()

    total_removed = 0
    touched = 0
    injected = 0
    for path in files:
        with open(path, encoding="utf-8") as f:
            html = f.read()
        orig = html
        html, removed = strip_google(html)
        html, did_inject = insert_domestic(html, snippet)
        if did_inject:
            injected += 1
        if html != orig:
            touched += 1
            total_removed += removed
            if args.apply:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(html)

    print(f"移除 Google 脚本标签: {total_removed} 个")
    print(f"注入百度统计+自动推送: {injected} 个页面")
    print(f"发生改动的文件: {touched} / {len(files)}")
    if not args.apply:
        print("\n[dry-run] 未写盘。确认后加 --apply 生效。")


if __name__ == "__main__":
    main()
