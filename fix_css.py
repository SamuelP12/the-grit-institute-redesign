#!/usr/bin/env python3
"""Patch CSS url() refs still pointing remote (filenames with escaped parens)."""
import os, re, urllib.parse, urllib.request

OUT = os.path.dirname(os.path.abspath(__file__))
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/124 Safari/537.36"
# CSS url(...) honoring backslash escapes like \( \)
URL_RE = re.compile(r'url\(\s*(["\']?)((?:\\.|[^)"\'\\])*)\1\s*\)')

cache = {}
def fetch(url):
    if url in cache:
        return cache[url]
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Referer": "https://the-grit-institute.webflow.io/"})
    data = urllib.request.urlopen(req, timeout=60).read()
    cache[url] = data
    return data

def url_to_fs(url):
    p = urllib.parse.urlparse(url)
    return os.path.join("assets", p.netloc, urllib.parse.unquote(p.path).lstrip("/"))

css_root = os.path.join(OUT, "assets", "cdn.prod.website-files.com", "692709e75138a09dc8a4f247", "css")
fixed = 0
for fn in sorted(os.listdir(css_root)):
    if not fn.endswith(".css"):
        continue
    fp = os.path.join(css_root, fn)
    with open(fp, encoding="utf-8", errors="replace") as f:
        text = f.read()
    css_dir = os.path.dirname(fp)
    out = text
    for m in URL_RE.finditer(text):
        token = m.group(2)
        if "website-files.com" not in token:
            continue
        real = token.replace("\\(", "(").replace("\\)", ")").replace("\\,", ",").replace("\\", "")
        if not real.startswith("http"):
            continue
        try:
            data = fetch(real)
        except Exception as e:
            print(f"  FAIL {real} :: {e}")
            continue
        fs_rel = url_to_fs(real)
        fs_abs = os.path.join(OUT, fs_rel)
        os.makedirs(os.path.dirname(fs_abs), exist_ok=True)
        with open(fs_abs, "wb") as f:
            f.write(data)
        rel = urllib.parse.quote(os.path.relpath(fs_abs, css_dir), safe="/")
        out = out.replace(m.group(0), f'url("{rel}")')
        fixed += 1
        print(f"  fixed {os.path.basename(real)}")
    if out != text:
        with open(fp, "w", encoding="utf-8") as f:
            f.write(out)
print(f"Done. Fixed {fixed} CSS background refs.")
