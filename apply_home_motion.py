#!/usr/bin/env python3
"""Homepage motion upgrade: replace Webflow IX2 content reveals with the
lightweight scroll-reveal, scoped to <main> (nav untouched). Plus LCP perf.
Idempotent."""
import re

p = "index.html"
d = open(p, encoding="utf-8").read()

m = re.search(r'<main class="main-wrapper">.*?</main>', d, re.S)
main = m.group(0)

# 1) neutralize IX2 on CONTENT: drop data-w-id + inline entrance styles (opacity:0 / translate3d)
main = re.sub(r'\sdata-w-id="[^"]*"', '', main)
main = re.sub(r'\sstyle="[^"]*(?:opacity:0|translate3d)[^"]*"', '', main)

# 2) add lightweight reveal to non-hero top-level sections
def add_reveal(mm):
    tag, cls = mm.group(0), mm.group(1)
    if 'hero_section' in cls or ' reveal' in (' ' + cls):
        return tag
    return tag.replace('class="' + cls + '"', 'class="' + cls + ' reveal"', 1)
main = re.sub(r'<section[^>]*\bclass="([^"]*)"[^>]*>', add_reveal, main)

d = d[:m.start()] + main + d[m.end():]

# 3) remove the head style that hides hero elements until IX2 inits
d = re.sub(r'<style>@media \(min-width:992px\) \{html\.w-mod-js:not\(\.w-mod-ix\).*?</style>', '', d, flags=re.S)

# 4) LCP perf: make the first hero slide eager + high priority, and preload it
mimg = re.search(r'<img src="([^"]+_hero-slide-1\.webp)"[^>]*class="slider-image[^"]*"', d)
if not mimg:
    mimg = re.search(r'<img src="([^"]+)"[^>]*class="slider-image[^"]*"', d)
if mimg:
    src = mimg.group(1)
    first = mimg.group(0)
    eager = first.replace('loading="lazy"', 'loading="eager" fetchpriority="high"')
    if 'loading="lazy"' not in first:  # ensure attrs present
        eager = first.replace('<img ', '<img loading="eager" fetchpriority="high" ', 1)
    d = d.replace(first, eager, 1)
    if 'rel="preload" as="image"' not in d:
        d = d.replace('</head>', f'<link rel="preload" as="image" href="{src}"/></head>', 1)

# 5) silkier hero crossfade
d = d.replace('speed      : 1500', 'speed      : 2000').replace('interval   : 6500', 'interval   : 7000')

open(p, "w", encoding="utf-8").write(d)
print("homepage motion upgrade applied.")
print("  reveal sections:", d.count(' reveal"'))
print("  data-w-id left in <main>:", re.search(r'<main.*?</main>', d, re.S).group(0).count('data-w-id'))
