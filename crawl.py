#!/usr/bin/env python3
"""Mirror the-grit-institute.webflow.io into a local, editable static site."""
import os, re, sys, time, json, html, urllib.parse, urllib.request, hashlib

SITE = "the-grit-institute.webflow.io"
BASE = f"https://{SITE}"
OUT = os.path.dirname(os.path.abspath(__file__))
ASSET_HOSTS = {
    "cdn.prod.website-files.com",
    "d3e54v103j8qbb.cloudfront.net",
    "ajax.googleapis.com",
    "uploads-ssl.webflow.com",
    "assets.website-files.com",
    "assets-global.website-files.com",
}
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36"

# Seed pages from nav/footer (CMS pages get discovered by crawling)
SEEDS = ["/", "/about", "/speaking", "/courses", "/transcend-mastermind",
         "/offerings-for-schools", "/powrpack", "/the-grit-factor",
         "/other-books-writing", "/podcast", "/blog", "/media", "/contact",
         "/privacy-policy", "/404"]

pages = {}        # path -> raw html
assets = set()    # absolute asset urls to download
visited = set()
queue = list(dict.fromkeys(SEEDS))

def fetch(url, binary=False):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=45) as r:
                data = r.read()
                ctype = r.headers.get("Content-Type", "")
                return data if binary else data.decode("utf-8", "replace"), ctype
        except Exception as e:
            if attempt == 2:
                print(f"  FAIL {url} :: {e}")
                return (None, "") if not binary else None
            time.sleep(2)

def norm_page(href):
    """Return a clean site path for an internal page link, or None."""
    href = href.strip()
    if not href or href.startswith(("#", "mailto:", "tel:", "javascript:")):
        return None
    p = urllib.parse.urlparse(href)
    if p.scheme in ("http", "https"):
        if p.netloc != SITE:
            return None
        path = p.path
    elif p.scheme == "":
        path = p.path
    else:
        return None
    if not path:
        return None
    # strip query/fragment, drop trailing slash (except root)
    path = path.split("#")[0].split("?")[0]
    if path != "/" and path.endswith("/"):
        path = path.rstrip("/")
    # skip obvious asset paths
    if re.search(r"\.(css|js|png|jpe?g|webp|svg|gif|ico|json|pdf|mp4|webm|woff2?|ttf|eot|xml|txt|zip)$", path, re.I):
        return None
    if not path.startswith("/"):
        return None
    return path

ASSET_ATTR_RE = re.compile(r'(?:src|href|content|data-src|poster)\s*=\s*["\']([^"\']+)["\']', re.I)
SRCSET_RE = re.compile(r'srcset\s*=\s*["\']([^"\']+)["\']', re.I)
CSS_URL_RE = re.compile(r'url\(\s*["\']?([^"\')]+)["\']?\s*\)')

def collect_assets_from_html(doc):
    urls = set()
    for m in ASSET_ATTR_RE.finditer(doc):
        urls.add(m.group(1))
    for m in SRCSET_RE.finditer(doc):
        for part in m.group(1).split(","):
            u = part.strip().split(" ")[0]
            if u:
                urls.add(u)
    for m in CSS_URL_RE.finditer(doc):
        urls.add(m.group(1))
    out = set()
    for u in urls:
        u = html.unescape(u.strip())
        if u.startswith("//"):
            u = "https:" + u
        if not u.startswith("http"):
            continue
        host = urllib.parse.urlparse(u).netloc
        if host in ASSET_HOSTS:
            out.add(u)
    return out

def collect_links(doc):
    links = set()
    for m in re.finditer(r'href\s*=\s*["\']([^"\']+)["\']', doc, re.I):
        p = norm_page(m.group(1))
        if p:
            links.add(p)
    return links

# ---- Phase 1: crawl pages ----
print("== Phase 1: crawling pages ==")
while queue:
    path = queue.pop(0)
    if path in visited:
        continue
    visited.add(path)
    url = BASE + (path if path != "/" else "/")
    res = fetch(url)
    if not res or res[0] is None:
        continue
    doc, ctype = res
    if "html" not in ctype.lower():
        continue
    pages[path] = doc
    assets |= collect_assets_from_html(doc)
    for link in collect_links(doc):
        if link not in visited:
            queue.append(link)
    print(f"  page [{len(pages)}] {path}  (+{len(assets)} assets known, {len(queue)} queued)")
    time.sleep(0.25)

print(f"\nTotal pages: {len(pages)}")
with open(os.path.join(OUT, "_pages.json"), "w") as f:
    json.dump({"pages": sorted(pages.keys()), "assets": sorted(assets)}, f, indent=2)
# stash raw html
raw_dir = os.path.join(OUT, "_raw")
os.makedirs(raw_dir, exist_ok=True)
for path, doc in pages.items():
    fn = "index" if path == "/" else path.strip("/").replace("/", "__")
    with open(os.path.join(raw_dir, fn + ".html"), "w") as f:
        f.write(doc)
print(f"Saved raw HTML to {raw_dir}")
print("Run crawl_assets.py next.")
