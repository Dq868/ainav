#!/usr/bin/env python3
import sys, json, re, datetime

def escape_js(s):
    s = s.replace('\\', '\\\\')
    s = s.replace('`', '\\`')
    s = s.replace('${', '\\${')
    return s

def main():
    raw = sys.stdin.read().strip()
    try:
        article = json.loads(raw)
    except json.JSONDecodeError as e:
        print(f"JSON parse error: {e}", file=sys.stderr)
        sys.exit(1)

    for field in ['title', 'content']:
        if field not in article or not article[field]:
            print(f"Missing: {field}", file=sys.stderr)
            sys.exit(1)

    today = datetime.date.today().isoformat()
    article.setdefault('id', 'auto-' + today)
    article.setdefault('date', today)
    article.setdefault('cat', 'other')
    article.setdefault('icon', '🤖')
    article.setdefault('summary', '')
    article.setdefault('relatedTools', [])
    article['id'] = re.sub(r'[^a-z0-9\-]', '', article['id'].lower().replace(' ', '-'))

    with open('articles.js', 'r', encoding='utf-8') as f:
        js = f.read()

    last_idx = js.rfind('\n];')
    if last_idx == -1:
        print("No array end found", file=sys.stderr)
        sys.exit(1)

    fields = []
    for key, val in article.items():
        if key == 'content':
            fields.append(f"    content: `\n{escape_js(val)}\n    `")
        elif key == 'relatedTools' and val:
            fields.append(f"    relatedTools: [{', '.join(repr(v) for v in val)}]")
        elif isinstance(val, str):
            fields.append(f"    {key}: '{escape_js(val)}'")
        elif isinstance(val, list):
            fields.append(f"    {key}: [{', '.join(repr(v) for v in val)}]")

    entry = "  {\n" + ",\n".join(fields) + "\n  },\n"
    js = js[:last_idx] + entry + js[last_idx:]

    with open('articles.js', 'w', encoding='utf-8') as f:
        f.write(js)

    print(f"OK: {article['title']}")

if __name__ == '__main__':
    main()
