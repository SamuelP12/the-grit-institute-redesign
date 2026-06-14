#!/usr/bin/env python3
"""Phase 1 redesign: declutter nav + perf pass across all built pages.
Idempotent — safe to re-run (guards on a marker)."""
import os, re, glob

ARROW = ('<svg xmlns="http://www.w3.org/2000/svg" width="100%" viewBox="0 0 20 20" fill="none">'
         '<path d="M4.16699 10H15.8337" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"></path>'
         '<path d="M12.5 13.3333L15.8333 10" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"></path>'
         '<path d="M12.5 6.66797L15.8333 10.0013" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"></path></svg>')

# slug -> (group, label-in-dropdown). Groups: about, speaking, courses, books, insights, contact
GROUP = {
    'about':'about','speaking':'speaking','speaker-kit':'speaking',
    'courses':'courses','transcend-mastermind':'courses','offerings-for-schools':'courses','powrpack':'courses',
    'the-grit-factor':'books','other-books-writing':'books',
    'podcast':'insights','blog':'insights','media':'insights',
    'contact':'contact',
}

def page_slug(path):
    if path == 'index.html': return None, None        # home
    parts = path.split('/')
    if parts[0] == 'blog' and len(parts) == 3: return 'blog', 'insights'   # a blog post
    if parts[0] == 'keynotes' and len(parts) == 3: return parts[1], 'speaking'  # a keynote page
    slug = parts[0]
    return slug, GROUP.get(slug)

def cur(cond):  # active class for top-level links
    return ' w--current' if cond else ''

def dd_cur(active_slug, slug):  # active class for dropdown child link
    return ' w--current' if active_slug == slug else ''

def build_nav_ul(p, slug, group):
    """p = relative prefix (e.g. '', '../', '../../')."""
    active_speaking = ' gi-active' if group == 'speaking' else ''
    active_courses = ' gi-active' if group == 'courses' else ''
    active_books   = ' gi-active' if group == 'books' else ''
    active_ins     = ' gi-active' if group == 'insights' else ''
    return (
      '<ul role="list" class="nav-menu_list-centered w-list-unstyled">'
      f'<li class="nav-menu_list-item"><a href="{p}about/index.html" class="nav_link w-inline-block{cur(group=="about")}"><div>About</div></a></li>'
      # Speaking dropdown
      f'<li class="nav-menu_list-item"><div data-hover="true" data-delay="0" data-w-id="gi-dd-speaking" class="nav-dropdown w-dropdown">'
      f'<div class="nav-dropdown-toggle w-dropdown-toggle{active_speaking}"><div>Speaking</div><div class="dropdown-icon w-icon-dropdown-toggle"></div></div>'
      '<nav class="dropdown-navigation w-dropdown-list">'
      f'<a href="{p}speaking/index.html" class="dropdown_links w-dropdown-link{dd_cur(slug,"speaking")}">Speaking Overview</a>'
      f'<a href="{p}speaker-kit/index.html" class="dropdown_links margin-remove w-dropdown-link{dd_cur(slug,"speaker-kit")}">Speaker Kit</a>'
      '</nav></div></li>'
      # Courses dropdown
      f'<li class="nav-menu_list-item"><div data-hover="true" data-delay="0" data-w-id="gi-dd-courses" class="nav-dropdown w-dropdown">'
      f'<div class="nav-dropdown-toggle w-dropdown-toggle{active_courses}"><div>Courses</div><div class="dropdown-icon w-icon-dropdown-toggle"></div></div>'
      '<nav class="dropdown-navigation w-dropdown-list">'
      f'<a href="{p}courses/index.html" class="dropdown_links w-dropdown-link{dd_cur(slug,"courses")}">Courses</a>'
      f'<a href="{p}transcend-mastermind/index.html" class="dropdown_links w-dropdown-link{dd_cur(slug,"transcend-mastermind")}">Transcend Mastermind</a>'
      f'<a href="{p}offerings-for-schools/index.html" class="dropdown_links w-dropdown-link{dd_cur(slug,"offerings-for-schools")}">Offerings for Schools</a>'
      f'<a href="{p}powrpack/index.html" class="dropdown_links margin-remove w-dropdown-link{dd_cur(slug,"powrpack")}">Powrpack</a>'
      '</nav></div></li>'
      # Books dropdown
      f'<li class="nav-menu_list-item"><div data-hover="true" data-delay="0" data-w-id="gi-dd-books" class="nav-dropdown w-dropdown">'
      f'<div class="nav-dropdown-toggle w-dropdown-toggle{active_books}"><div>Books</div><div class="dropdown-icon w-icon-dropdown-toggle"></div></div>'
      '<nav class="dropdown-navigation w-dropdown-list">'
      f'<a href="{p}the-grit-factor/index.html" class="dropdown_links w-dropdown-link{dd_cur(slug,"the-grit-factor")}">The Grit Factor</a>'
      f'<a href="{p}other-books-writing/index.html" class="dropdown_links margin-remove w-dropdown-link{dd_cur(slug,"other-books-writing")}">Other Books &amp; Writing</a>'
      '</nav></div></li>'
      # Insights dropdown
      f'<li class="nav-menu_list-item"><div data-hover="true" data-delay="0" data-w-id="gi-dd-insights" class="nav-dropdown w-dropdown">'
      f'<div class="nav-dropdown-toggle w-dropdown-toggle{active_ins}"><div>Insights</div><div class="dropdown-icon w-icon-dropdown-toggle"></div></div>'
      '<nav class="dropdown-navigation w-dropdown-list">'
      f'<a href="{p}podcast/index.html" class="dropdown_links w-dropdown-link{dd_cur(slug,"podcast")}">Podcast</a>'
      f'<a href="{p}blog/index.html" class="dropdown_links w-dropdown-link{dd_cur(slug,"blog")}">Blog</a>'
      f'<a href="{p}media/index.html" class="dropdown_links margin-remove w-dropdown-link{dd_cur(slug,"media")}">Media</a>'
      '</nav></div></li>'
      # CTA
      f'<li class="nav-menu_list-item nav-absolute-right"><a href="{p}contact/index.html" class="button is-nav_btn w-inline-block">'
      f'<div>Contact</div><div class="button-icon">{ARROW}</div></a></li>'
      '</ul>'
    )

UL_RE = re.compile(r'<ul role="list" class="nav-menu_list-centered w-list-unstyled">.*?</ul>', re.S)
WEBFONT_SCRIPT_RE = re.compile(r'<script src="[^"]*webfont\.js"[^>]*></script>', re.I)
WEBFONT_LOAD_RE = re.compile(r'<script type="text/javascript">WebFont\.load\(\{.*?\}\);</script>', re.S)

GEIST_LINK = ('<link rel="preload" as="style" href="https://fonts.googleapis.com/css2?family=Geist:wght@300;400;500;600;700&amp;display=swap">'
              '<link href="https://fonts.googleapis.com/css2?family=Geist:wght@300;400;500;600;700&amp;display=swap" rel="stylesheet">')

def optimize_head(doc, p):
    # 1) replace render-blocking webfont.js loader with a non-blocking font link
    doc = WEBFONT_SCRIPT_RE.sub('', doc)
    doc = WEBFONT_LOAD_RE.sub('', doc)
    if 'fonts.googleapis.com/css2?family=Geist' not in doc:
        doc = doc.replace('<link href="https://fonts.googleapis.com" rel="preconnect"/>',
                          '<link href="https://fonts.googleapis.com" rel="preconnect"/>' + GEIST_LINK, 1)
    # 2) defer heavy scripts (jQuery, webflow bundle, splide) — keep execution order
    doc = re.sub(r'(<script src="[^"]*(?:jquery[^"]*|the-grit-institute\.[0-9a-f]+\.[0-9a-f]+\.js|splide\.min\.js)"[^>]*?)(\s*></script>)',
                 lambda m: (m.group(1) if 'defer' in m.group(1) else m.group(1) + ' defer') + m.group(2), doc)
    # 3) inject redesign.css (last, so it wins) + redesign.js (deferred), before </head>
    if 'redesign.css' not in doc:
        inject = f'<link rel="stylesheet" href="{p}redesign.css"/><script defer src="{p}redesign.js"></script>'
        doc = doc.replace('</head>', inject + '</head>', 1)
    return doc

def process(path):
    doc = open(path, encoding='utf-8').read()
    slug, group = page_slug(path)
    depth = path.count('/')
    p = '../' * depth
    new_ul = build_nav_ul(p, slug, group)
    # a11y: make dropdown toggles keyboard-operable + screen-reader announced
    new_ul = re.sub(r'(<div class="nav-dropdown-toggle w-dropdown-toggle[^"]*")>',
                    r'\1 tabindex="0" role="button" aria-haspopup="true" aria-expanded="false">', new_ul)
    if not UL_RE.search(doc):
        print(f"  !! nav <ul> not found in {path}");
    else:
        doc = UL_RE.sub(lambda _: new_ul, doc, count=1)
    doc = optimize_head(doc, p)
    open(path, 'w', encoding='utf-8').write(doc)

def main():
    pages = [h for h in glob.glob('**/*.html', recursive=True) if not h.startswith('_raw/')]
    for h in sorted(pages):
        process(h)
        print(f"  redesigned {h}")
    print(f"\nDone: {len(pages)} pages.")

if __name__ == '__main__':
    main()
