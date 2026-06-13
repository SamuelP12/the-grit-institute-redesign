#!/usr/bin/env python3
"""Phase 2+3: download all assets, then rewrite pages/CSS to a local static site."""
import os, re, json, time, urllib.parse, urllib.request, html

OUT = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(OUT, "_raw")
ASSET_HOSTS = {
    "cdn.prod.website-files.com", "d3e54v103j8qbb.cloudfront.net",
    "ajax.googleapis.com", "uploads-ssl.webflow.com",
    "assets.website-files.com", "assets-global.website-files.com",
}
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36"

with open(os.path.join(OUT, "_pages.json")) as f:
    meta = json.load(f)
page_paths = meta["pages"]
assets = set(meta["assets"])

CSS_URL_RE = re.compile(r'url\(\s*["\']?([^"\')]+)["\']?\s*\)')

def fetch_bin(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                return r.read(), r.headers.get("Content-Type", "")
        except Exception as e:
            if attempt == 2:
                print(f"  FAIL {url} :: {e}")
                return None, ""
            time.sleep(2)

def url_to_fs(url):
    """Map an asset URL to a local filesystem relative path (decoded)."""
    p = urllib.parse.urlparse(url)
    path = urllib.parse.unquote(p.path).lstrip("/")
    if p.query:
        # keep query-distinct files unique (e.g. jquery ?site=...)
        import hashlib
        path += "_" + hashlib.md5(p.query.encode()).hexdigest()[:8]
    return os.path.join("assets", p.netloc, path)

def fs_to_href(fs_rel):
    """Filesystem rel path -> URL-safe href from site root."""
    return urllib.parse.quote(fs_rel, safe="/")

# ---- Phase 2: download assets (with one level of CSS url() expansion) ----
print("== Phase 2: downloading assets ==")
url_map = {}      # asset url -> fs rel path
css_files = []    # (url, fs_rel) for css to post-process
to_get = set(assets)
done = set()

def download(url):
    if url in done:
        return url_map.get(url)
    done.add(url)
    fs_rel = url_to_fs(url)
    fs_abs = os.path.join(OUT, fs_rel)
    os.makedirs(os.path.dirname(fs_abs), exist_ok=True)
    data, ctype = fetch_bin(url)
    if data is None:
        return None
    with open(fs_abs, "wb") as f:
        f.write(data)
    url_map[url] = fs_rel
    if "css" in ctype.lower() or fs_rel.endswith(".css"):
        css_files.append((url, fs_rel, data))
    return fs_rel

n = 0
for url in sorted(to_get):
    n += 1
    download(url)
    if n % 25 == 0:
        print(f"  {n}/{len(to_get)} assets...")
    time.sleep(0.05)
print(f"Downloaded {len(url_map)} assets.")

# expand CSS url() refs (fonts/images) -> download + record per-css rewrites
print("== Phase 2b: expanding CSS url() references ==")
css_rewrites = {}   # css_fs_rel -> list[(orig_token, new_rel_from_css)]
for url, fs_rel, data in list(css_files):
    text = data.decode("utf-8", "replace")
    css_dir = os.path.dirname(os.path.join(OUT, fs_rel))
    rewrites = []
    for m in CSS_URL_RE.finditer(text):
        token = m.group(1).strip()
        if token.startswith(("data:", "#")):
            continue
        abs_u = urllib.parse.urljoin(url, html.unescape(token))
        host = urllib.parse.urlparse(abs_u).netloc
        if host not in ASSET_HOSTS:
            continue
        dl = download(abs_u)
        if dl:
            rel_from_css = os.path.relpath(os.path.join(OUT, dl), css_dir)
            rewrites.append((token, fs_to_href(rel_from_css)))
    if rewrites:
        css_rewrites[fs_rel] = rewrites

# apply CSS rewrites
for fs_rel, rewrites in css_rewrites.items():
    fp = os.path.join(OUT, fs_rel)
    with open(fp, "r", encoding="utf-8", errors="replace") as f:
        text = f.read()
    for token, newref in rewrites:
        text = text.replace("url(" + token + ")", "url(" + newref + ")")
        text = text.replace('url("' + token + '")', 'url("' + newref + '")')
        text = text.replace("url('" + token + "')", "url('" + newref + "')")
    with open(fp, "w", encoding="utf-8") as f:
        f.write(text)
print(f"Rewrote url() in {len(css_rewrites)} CSS files.")

# ---- Phase 3: rewrite & write pages ----
print("== Phase 3: rewriting pages ==")

def page_to_local(path):
    """site path -> local file rel path (dir/index.html)."""
    if path == "/":
        return "index.html"
    return path.strip("/") + "/index.html"

page_local = {p: page_to_local(p) for p in page_paths}
SITE = "the-grit-institute.webflow.io"

def rewrite_page(path, doc):
    local = page_local[path]
    depth = local.count("/")          # dir/index.html -> depth=1 ; index.html -> 0
    prefix = "../" * depth
    # 1) asset absolute URLs -> local
    for url, fs_rel in url_map.items():
        if url in doc:
            doc = doc.replace(url, prefix + fs_to_href(fs_rel))
        esc = html.escape(url)
        if esc != url and esc in doc:
            doc = doc.replace(esc, prefix + fs_to_href(fs_rel))
    # 2) protocol-relative forms
    for url, fs_rel in url_map.items():
        pr = url.replace("https:", "", 1) if url.startswith("https:") else None
        if pr and pr in doc:
            doc = doc.replace(pr, prefix + fs_to_href(fs_rel))
    # 3) internal page links (href="/about" etc.) -> local relative
    def repl_href(m):
        attr, q, val = m.group(1), m.group(2), m.group(3)
        raw = val
        v = val.split("#")[0].split("?")[0]
        frag = val[len(v):]
        # normalize
        vv = v
        if vv != "/" and vv.endswith("/"):
            vv = vv.rstrip("/")
        target = None
        if vv in page_local:
            target = page_local[vv]
        elif vv == "" and raw.startswith("#"):
            return m.group(0)
        if target is None:
            return m.group(0)
        return f'{attr}={q}{prefix}{target}{frag}{q}'
    doc = re.sub(r'(href)=(["\'])([^"\']*)\2', repl_href, doc)
    # 4) absolute self-domain links -> local (https://site/about)
    def repl_abs(m):
        attr, q, val = m.group(1), m.group(2), m.group(3)
        p = urllib.parse.urlparse(val)
        if p.netloc != SITE:
            return m.group(0)
        vv = p.path or "/"
        if vv != "/" and vv.endswith("/"):
            vv = vv.rstrip("/")
        if vv in page_local:
            frag = ("#" + p.fragment) if p.fragment else ""
            return f'{attr}={q}{prefix}{page_local[vv]}{frag}{q}'
        return m.group(0)
    doc = re.sub(r'(href)=(["\'])(https?://[^"\']*)\2', repl_abs, doc)
    return doc

for path in page_paths:
    fn = "index" if path == "/" else path.strip("/").replace("/", "__")
    with open(os.path.join(RAW, fn + ".html"), encoding="utf-8") as f:
        doc = f.read()
    out_doc = rewrite_page(path, doc)
    dest = os.path.join(OUT, page_local[path])
    os.makedirs(os.path.dirname(dest) or OUT, exist_ok=True)
    with open(dest, "w", encoding="utf-8") as f:
        f.write(out_doc)
    print(f"  wrote {page_local[path]}")

print("\nDone. Open with: cd ~/grit-institute && python3 -m http.server 8099")
