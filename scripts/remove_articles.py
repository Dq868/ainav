#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
按 id 批量下架文章：从 articles.js 删除对象、删除对应静态页、同步 sitemap.xml。

用法：
  # 预览（只打印将执行的动作，不写文件）
  python3 scripts/remove_articles.py --ids a,b,c

  # 从文件读取 id 列表（每行一个，# 开头为注释）
  python3 scripts/remove_articles.py --file removed_ids.txt --apply

  # 直接指定并执行
  python3 scripts/remove_articles.py --ids a,b,c --apply

特性：
- 感知 JS 模板字符串与引号字符串，精确删除整个文章对象（不会误删 content 内容）。
- 同步删除 blog/<id>.html 静态页。
- 同步从 sitemap.xml 移除对应 <url> 块（若存在）。
- 默认 dry-run，加 --apply 才写盘。
"""
import os
import re
import sys
import argparse

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARTICLES = os.path.join(REPO_ROOT, "articles.js")
BLOG_DIR = os.path.join(REPO_ROOT, "blog")
SITEMAP = os.path.join(REPO_ROOT, "sitemap.xml")


def _skip_forward(text, i):
    """从 i 处跳过字符串/模板字符串，返回结束后的位置。"""
    ch = text[i]
    if ch in ("'", '"'):
        q = ch
        i += 1
        while i < len(text):
            if text[i] == "\\":
                i += 2
                continue
            if text[i] == q:
                return i + 1
            i += 1
        return i
    if ch == "`":
        i += 1
        while i < len(text):
            c = text[i]
            if c == "\\":
                i += 2
                continue
            if c == "`":
                return i + 1
            if c == "$" and i + 1 < len(text) and text[i + 1] == "{":
                i += 2
                depth = 1
                while i < len(text) and depth > 0:
                    if text[i] == "{":
                        depth += 1
                    elif text[i] == "}":
                        depth -= 1
                    i += 1
                continue
            i += 1
        return i
    return i + 1


def find_object_bounds(text, pos):
    """给定对象内部任意位置，返回包裹它的 { 与 } 的下标。"""
    # 向右找 '}'
    depth = 0
    j = pos
    end = None
    while j < len(text):
        c = text[j]
        if c in ("'", '"', "`"):
            j = _skip_forward(text, j)
            continue
        if c == "{":
            depth += 1
        elif c == "}":
            if depth == 0:
                end = j
                break
            depth -= 1
        j += 1
    if end is None:
        return None, None
    # 向左找 '{'
    depth = 0
    j = pos
    start = None
    while j >= 0:
        c = text[j]
        if c in ("'", '"', "`"):
            # 向左跨过字符串：找其起始引号
            k = j
            found = False
            while k >= 0:
                if text[k] in ("'", '"', "`"):
                    back = k - 1
                    esc = 0
                    while back >= 0 and text[back] == "\\":
                        esc += 1
                        back -= 1
                    if esc % 2 == 0:
                        j = k - 1
                        found = True
                        break
                k -= 1
            if not found:
                j -= 1
            continue
        if c == "}":
            depth += 1
        elif c == "{":
            if depth == 0:
                start = j
                break
            depth -= 1
        j -= 1
    return start, end


def remove_ids(ids, apply=False):
    with open(ARTICLES, encoding="utf-8") as f:
        text = f.read()

    spans = []
    for aid in ids:
        pat = re.compile(r"^\s*id:\s*'" + re.escape(aid) + r"',?\s*$", re.M)
        m = pat.search(text)
        if not m:
            print(f"  [跳过] articles.js 中未找到 id: {aid}")
            continue
        s, e = find_object_bounds(text, m.start())
        if s is None:
            print(f"  [跳过] 无法定位对象边界: {aid}")
            continue
        spans.append((s, e, aid))

    if not spans:
        print("没有可删除的对象。")
        return []

    spans.sort()
    # 合并重叠/相邻
    merged = []
    for s, e, aid in spans:
        if merged and s <= merged[-1][1]:
            merged[-1] = (merged[-1][0], max(e, merged[-1][1]), merged[-1][2] + "," + aid)
        else:
            merged.append((s, e, aid))

    print(f"== articles.js: 将删除 {len(merged)} 个对象区间 ==")
    for s, e, aid in merged:
        print(f"   行 {text[:s].count(chr(10))+1}-{text[:e].count(chr(10))+1}: {aid}")

    deleted = []
    for _, _, aids in merged:
        deleted.extend(aids.split(","))

    if not apply:
        print("[dry-run] 未写盘。")
        return deleted

    for s, e, aid in reversed(merged):
        # 连同对象后的逗号一并删除，保持数组语法
        tail = e + 1
        while tail < len(text) and text[tail] in " \t":
            tail += 1
        if tail < len(text) and text[tail] == ",":
            tail += 1
        if tail < len(text) and text[tail] == "\n":
            tail += 1
        text = text[:s] + text[tail:]

    with open(ARTICLES, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"[apply] 已更新 {ARTICLES}")
    return deleted


def remove_static_pages(ids, apply=False):
    removed = []
    for aid in ids:
        p = os.path.join(BLOG_DIR, f"{aid}.html")
        if os.path.exists(p):
            removed.append(aid)
            if apply:
                os.remove(p)
    print(f"== blog 静态页: {'删除' if apply else '将删除'} {len(removed)} 个 ==")
    return removed


def remove_from_sitemap(ids, apply=False):
    with open(SITEMAP, encoding="utf-8") as f:
        xml = f.read()
    removed = []
    for aid in ids:
        loc = f"https://jzzai.cn/blog/{aid}"
        # 匹配整个 <url>...</url> 块
        pat = re.compile(r"\s*<url>\s*<loc>" + re.escape(loc) + r"</loc>.*?</url>", re.S)
        if pat.search(xml):
            removed.append(aid)
            if apply:
                xml = pat.sub("", xml, count=1)
    # 清理连续空行
    if apply:
        xml = re.sub(r"\n{3,}", "\n\n", xml)
        with open(SITEMAP, "w", encoding="utf-8") as f:
            f.write(xml)
    print(f"== sitemap.xml: {'移除' if apply else '将移除'} {len(removed)} 个 URL ==")
    return removed


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ids", help="逗号分隔的文章 id")
    ap.add_argument("--file", help="每行一个 id 的文件")
    ap.add_argument("--apply", action="store_true", help="真正写盘")
    args = ap.parse_args()

    ids = []
    if args.ids:
        ids = [x.strip() for x in args.ids.split(",") if x.strip()]
    if args.file:
        with open(args.file, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    ids.append(line)
    if not ids:
        print("未提供 id，使用 --ids 或 --file")
        sys.exit(1)

    print(f"待处理 {len(ids)} 个 id: {', '.join(ids)}\n")
    deleted = remove_ids(ids, args.apply)
    pages = remove_static_pages(deleted, args.apply)
    urls = remove_from_sitemap(deleted, args.apply)
    print(f"\n汇总: articles.js 删除 {len(deleted)} 篇 | 静态页 {len(pages)} 个 | sitemap {len(urls)} 个")
    if not args.apply:
        print("（dry-run，未写盘；加 --apply 生效）")


if __name__ == "__main__":
    main()
