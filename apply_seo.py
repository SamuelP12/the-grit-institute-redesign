#!/usr/bin/env python3
"""Quick-win SEO + hero pass. Idempotent (guarded by <!--gi-seo--> markers).
Change SITE_URL if you deploy somewhere other than the production domain."""
import os, re, glob, json, html

SITE_URL = "https://www.thegritinstitute.com"           # <-- production domain assumption
LOGO = "https://cdn.prod.website-files.com/692709e75138a09dc8a4f247/69271a4e915393eb42030c40_Grit%20Institute%20logo.webp"
SAMEAS = [
    "https://www.linkedin.com/in/shannonhpolson/",
    "https://www.youtube.com/channel/UCcpleeDo9xXWkqau90yLHog",
    "https://www.instagram.com/shannonhpolson/",
    "https://www.pinterest.com/thegritinstitute",
]

# ---- per-page title + meta description (hand-written, keyword-led) ----
META = {
 "index.html": ("Women's Leadership Keynote Speaker | Shannon Huffman Polson",
   "Shannon Huffman Polson—one of the first women to fly the Apache helicopter—delivers keynotes on courageous leadership, resilience, and decision-making under pressure."),
 "about/index.html": ("About Shannon Huffman Polson — Apache Pilot, Author & Speaker",
   "From Apache helicopter pilot to author and leadership educator—meet Shannon Huffman Polson and the story behind The Grit Institute."),
 "speaking/index.html": ("Leadership Keynote Speaker | Book Shannon Huffman Polson",
   "Book Shannon Huffman Polson, Apache pilot and author of The Grit Factor, for keynotes on courageous leadership, resilience, and high-performance teams. Check availability."),
 "courses/index.html": ("Leadership Development Courses & Training | The Grit Institute",
   "Online leadership courses on grit, purpose, and resilience from Apache pilot and author Shannon Huffman Polson. Build courageous leaders—starting at $297."),
 "transcend-mastermind/index.html": ("Transcend Leadership Mastermind | Shannon Huffman Polson",
   "An elite mastermind for purpose-driven leaders: strategic discussions, coaching, and a powerful network. Apply for the Transcend waitlist."),
 "offerings-for-schools/index.html": ("Grit & Resilience Programs for Schools | The Grit Institute",
   "Going for Grit equips students with the resilience, grit, and leadership skills to thrive. Evidence-based programs for schools and young adults."),
 "powrpack/index.html": ("Powrpack: 6-Week Leadership Accelerator | The Grit Institute",
   "The Powrpack accelerator—a proven 6-week framework plus community to build grit, purpose, and high-performance leadership. Claim your spot."),
 "the-grit-factor/index.html": ("The Grit Factor — Book by Shannon Huffman Polson",
   "The Grit Factor by Shannon Huffman Polson: the science and story of grit, and a proven framework for courageous, resilient leadership. Buy it or read a free chapter."),
 "other-books-writing/index.html": ("Books & Writing by Shannon Huffman Polson",
   "Explore books and essays by Shannon Huffman Polson—including North of Hope and The Grit Factor—on resilience, leadership, grief, and the wild."),
 "podcast/index.html": ("The Grit Factor Podcast | Shannon Huffman Polson",
   "The Grit Factor Podcast with Shannon Huffman Polson—conversations with high performers on purpose, leadership, resilience, and a meaningful life."),
 "media/index.html": ("Media & Press | Shannon Huffman Polson",
   "Shannon Huffman Polson in the media—interviews, features, and appearances on leadership, grit, and courage. Resources for conference and media planners."),
 "contact/index.html": ("Contact & Book Shannon Huffman Polson | The Grit Institute",
   "Get in touch with Shannon Huffman Polson and The Grit Institute for speaking, training, courses, and media. Let's talk about your next event."),
 "blog/index.html": ("Leadership Blog | Shannon Huffman Polson",
   "Essays on courageous leadership, grit, resilience, and decision-making under pressure from Apache pilot and author Shannon Huffman Polson."),
 "privacy-policy/index.html": ("Privacy Policy | The Grit Institute",
   "The privacy policy for The Grit Institute and Shannon Huffman Polson."),
 "404/index.html": ("Page Not Found | The Grit Institute",
   "Sorry, this page can't be found. Explore Shannon Huffman Polson's keynotes, books, and leadership resources."),
}

def clean(s):
    s = re.sub(r'<[^>]+>', ' ', s)
    return re.sub(r'\s+', ' ', html.unescape(s)).strip()

def first_para(doc):
    m = re.search(r'<main.*?</main>', doc, re.S)
    body = m.group(0) if m else doc
    for p in re.findall(r'<p[^>]*>(.*?)</p>', body, re.S):
        t = clean(p)
        if len(t) > 60:
            return t
    return ""

def blog_meta(path, doc):
    m = re.search(r'<h1[^>]*>(.*?)</h1>', doc, re.S)
    h1 = clean(m.group(1)) if m else "Article"
    title = f"{h1} | Shannon Huffman Polson"
    desc = first_para(doc)
    if len(desc) > 155:
        desc = desc[:152].rsplit(' ', 1)[0] + "…"
    if not desc:
        desc = f"{h1} — an essay by Shannon Huffman Polson on leadership, grit, and resilience."
    return title, desc

def url_for(path):
    if path == "index.html": return SITE_URL + "/"
    return SITE_URL + "/" + path[:-len("/index.html")]

GRAPH = {
  "@context": "https://schema.org",
  "@graph": [
    {"@type": "Person", "@id": SITE_URL + "/#shannon",
     "name": "Shannon Huffman Polson",
     "jobTitle": ["Keynote Speaker", "Author", "Leadership Educator"],
     "description": "One of the first women to fly the Apache helicopter in the U.S. Army; keynote speaker and author of The Grit Factor.",
     "url": SITE_URL + "/", "image": LOGO, "sameAs": SAMEAS,
     "knowsAbout": ["Leadership", "Resilience", "Grit", "Decision-making under pressure",
                    "Women in leadership", "Military leadership", "High-performance teams", "Courageous leadership"],
     "worksFor": {"@id": SITE_URL + "/#org"}},
    {"@type": ["Organization", "ProfessionalService"], "@id": SITE_URL + "/#org",
     "name": "The Grit Institute", "url": SITE_URL + "/", "logo": LOGO,
     "image": LOGO, "founder": {"@id": SITE_URL + "/#shannon"},
     "telephone": "+1-509-996-8011", "email": "Shannon@TheGritInstitute.com", "sameAs": SAMEAS},
    {"@type": "WebSite", "@id": SITE_URL + "/#website", "url": SITE_URL + "/",
     "name": "The Grit Institute", "publisher": {"@id": SITE_URL + "/#org"}},
  ],
}
BOOK = {"@context": "https://schema.org", "@type": "Book",
        "name": "The Grit Factor", "author": {"@id": SITE_URL + "/#shannon"},
        "about": ["Leadership", "Resilience", "Grit", "Courage"],
        "inLanguage": "en", "publisher": "Harvard Business Review Press"}

# strip tags we will re-author (avoid duplicates)
STRIP = [r'<meta[^>]+property="og:(?:title|description|url|type)"[^>]*>',
         r'<meta[^>]+name="twitter:(?:title|description|card)"[^>]*>',
         r'<meta[^>]+name="description"[^>]*>',
         r'<link[^>]+rel="canonical"[^>]*>',
         r'<!--gi-seo-->.*?<!--/gi-seo-->']

def build_head(path, title, desc, is_blog):
    u = url_for(path); e = lambda s: html.escape(s, quote=True)
    ogtype = "article" if is_blog else "website"
    graphs = [GRAPH] + ([BOOK] if path == "the-grit-factor/index.html" else [])
    ld = "".join(f'<script type="application/ld+json">{json.dumps(g, ensure_ascii=False)}</script>' for g in graphs)
    return ("<!--gi-seo-->"
            f'<meta name="description" content="{e(desc)}"/>'
            f'<link rel="canonical" href="{u}"/>'
            f'<meta property="og:title" content="{e(title)}"/>'
            f'<meta property="og:description" content="{e(desc)}"/>'
            f'<meta property="og:type" content="{ogtype}"/>'
            f'<meta property="og:url" content="{u}"/>'
            f'<meta name="twitter:card" content="summary_large_image"/>'
            f'<meta name="twitter:title" content="{e(title)}"/>'
            f'<meta name="twitter:description" content="{e(desc)}"/>'
            f'{ld}<!--/gi-seo-->')

def seo_page(path):
    doc = open(path, encoding="utf-8").read()
    is_blog = path.startswith("blog/") and path != "blog/index.html"
    if is_blog:
        title, desc = blog_meta(path, doc)
    elif path in META:
        title, desc = META[path]
    else:
        return
    # title
    doc = re.sub(r'<title>.*?</title>', '<title>' + html.escape(title) + '</title>', doc, count=1, flags=re.S)
    # strip + inject head block
    for pat in STRIP:
        doc = re.sub(pat, '', doc, flags=re.S)
    doc = doc.replace('</head>', build_head(path, title, desc, is_blog) + '</head>', 1)
    open(path, "w", encoding="utf-8").write(doc)

# ---------- HERO rewrite (homepage) ----------
def hero():
    p = "index.html"; d = open(p, encoding="utf-8").read()
    reps = [
      ("Science, story, and strategy for courageous leadership.",
       "Apache pilot · Author of <em>The Grit Factor</em> · Founder, The Grit Institute"),
      ('Lead with Purpose.<span class="text-style-larger"> Live with Grit</span>',
       'Lead Like Lives<span class="text-style-larger"> Depend On It.</span>'),
      ("The Grit Institute helps leaders and organizations build purpose, resilience, and meaning—so they can thrive through challenge and change.",
       "One of the first women to fly the Apache helicopter, Shannon Huffman Polson teaches leaders to decide under pressure, build teams that perform in the hardest conditions, and lead with grit when it counts."),
      ('<a href="contact/index.html" class="button is-icon is-medium w-inline-block"><div>Book a call with shannon</div>',
       '<a href="speaking/index.html" class="button is-icon is-medium w-inline-block"><div>Book Shannon to Speak</div>'),
    ]
    for a, b in reps:
        if a in d: d = d.replace(a, b, 1)
        else: print("  hero: pattern not found ->", a[:48])
    open(p, "w", encoding="utf-8").write(d)

# ---------- Speaking CTA fix ----------
def speaking_cta():
    p = "speaking/index.html"; d = open(p, encoding="utf-8").read()
    # final CTA band: Enroll Now -> Check Availability (contact); Explore Courses -> Watch Shannon Speak (media)
    d = d.replace('<a href="../contact/index.html" class="button is-icon is-medium w-inline-block"><div>Enroll Now</div>',
                  '<a href="../contact/index.html" class="button is-icon is-medium w-inline-block"><div>Check Availability</div>', 1)
    d = d.replace('<a href="../courses/index.html" class="button is-secondary is-medium w-inline-block"><div>Explore Courses</div>',
                  '<a href="../media/index.html" class="button is-secondary is-medium w-inline-block"><div>Watch Shannon Speak</div>', 1)
    # fallbacks if class differs
    d = re.sub(r'(<a href="\.\./courses/index\.html"[^>]*>)<div>Explore Courses</div>',
               r'\1<div>Watch Shannon Speak</div>', d)  # text only fallback
    d = d.replace('>Explore Courses<', '>Watch Shannon Speak<')
    d = d.replace('>Enroll Now<', '>Check Availability<')
    open(p, "w", encoding="utf-8").write(d)

# ---------- typo / casing sweep (all pages, targeted & safe) ----------
TYPO = [
  ("Leadershiop", "Leadership"),
  ("clearer , and", "clearer, and"),
  ("Ready to Talk? i’m Ready to Help.", "Ready to Talk? I’m Ready to Help."),
  ("Meet shannon Polson", "Meet Shannon Polson"),
  ("With shannon Polson", "With Shannon Polson"),
  ("with shannon and the grit institute", "with Shannon and The Grit Institute"),
  ("Work with shannon", "Work with Shannon"),
  ("Book a call with shannon", "Book a Call with Shannon"),
  ("Book a call with Shannon", "Book a Call with Shannon"),
]
def typos(path):
    d = open(path, encoding="utf-8").read(); o = d
    for a, b in TYPO: d = d.replace(a, b)
    if d != o: open(path, "w", encoding="utf-8").write(d)

def main():
    pages = [h for h in glob.glob("**/*.html", recursive=True) if not h.startswith("_raw/")]
    for h in sorted(pages):
        seo_page(h)
    hero()
    speaking_cta()
    for h in sorted(pages):
        typos(h)
    print(f"SEO + hero applied to {len(pages)} pages.")

if __name__ == "__main__":
    main()
