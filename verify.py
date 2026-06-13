#!/usr/bin/env python3
"""Verify every relative asset/page reference in built HTML resolves to a real file."""
import os, re, glob, urllib.parse

OUT = os.path.dirname(os.path.abspath(__file__))
missing = {}
remote = {}
checked = 0

REF_RE = re.compile(r'(?:src|href|content|poster|data-src)\s*=\s*["\']([^"\']+)["\']')
SRCSET_RE = re.compile(r'srcset\s*=\s*["\']([^"\']+)["\']')

def refs_in(text):
    out = []
    for m in REF_RE.finditer(text):
        out.append(m.group(1))
    for m in SRCSET_RE.finditer(text):
        for part in m.group(1).split(","):
            u = part.strip().split(" ")[0]
            if u:
                out.append(u)
    return out

for html_path in glob.glob(os.path.join(OUT, "**", "*.html"), recursive=True):
    if "/_raw/" in html_path:
        continue
    rel_page = os.path.relpath(html_path, OUT)
    page_dir = os.path.dirname(html_path)
    with open(html_path, encoding="utf-8", errors="replace") as f:
        text = f.read()
    for ref in refs_in(text):
        if ref.startswith(("data:", "mailto:", "tel:", "#", "javascript:")):
            continue
        if ref.startswith(("http://", "https://", "//")):
            host = urllib.parse.urlparse(ref if "//" in ref else "//"+ref).netloc
            remote.setdefault(host, 0)
            remote[host] += 1
            continue
        checked += 1
        clean = urllib.parse.unquote(ref.split("#")[0].split("?")[0])
        target = os.path.normpath(os.path.join(page_dir, clean))
        if not os.path.exists(target):
            missing.setdefault(rel_page, []).append(ref)

print(f"Local refs checked: {checked}")
print(f"Pages with missing local files: {len(missing)}")
for page, refs in list(missing.items())[:20]:
    print(f"  {page}:")
    for r in refs[:8]:
        print(f"     MISSING {r}")
print("\nRemaining REMOTE hosts referenced (expected: fonts/typekit/analytics):")
for host, n in sorted(remote.items(), key=lambda x: -x[1]):
    print(f"  {n:4d}  {host}")
