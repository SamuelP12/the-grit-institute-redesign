#!/usr/bin/env python3
"""Build a bespoke /speaker-kit/ page from the About template (native nav/footer/scripts)."""
import os, re, html, json

SITE_URL = "https://www.thegritinstitute.com"
A = "../assets/cdn.prod.website-files.com/692709e75138a09dc8a4f247/"
V = "../assets/cdn-public.prismatico.io/grit-institute/"
LOGO_ABS = "https://cdn.prod.website-files.com/692709e75138a09dc8a4f247/69271a4e915393eb42030c40_Grit%20Institute%20logo.webp"

UNIFORM = A + "6960023a65e24bbd97f8d75c_GritFactor_Portrait_ShannonUniform.webp"
PORTRAIT = A + "69600255fcb33fc07dcde803_GritFactor_Portrait_ShannonPolson.webp"
LRG = A + "696002b4636777d067071a37_ShannonPolson122_lrg.webp"
BOOK = A + "696002cdb8be7f95be15ea36_TheGritFactorBook_ShannonPolson_TransBkgnrd.webp"
TRUST = [A + n for n in [
 "69415479b736bff8f2f717aa_trust%20logo%20%281%29.svg",
 "6941547a08eb3603c400083e_trust%20logo%20%282%29.svg",
 "6941547aa2a51c888dc849c3_trust%20logo%20%283%29.svg",
 "6941547a0b0117c0cbe88503_trust%20logo%20%284%29.svg",
 "6941547b183c7f5e4fe649bc_trust%20logo%20%285%29.svg",
 "6941547b3ca2cb14d41b3bbf_trust%20logo%20%286%29.svg",
 "6941547bbaf21e92c64db416_trust%20logo%20%287%29.svg",
 "6941547bfb54d4702564e405_trust%20logo%20%288%29.svg",
]]

ARROW = '<svg viewBox="0 0 20 20" fill="none"><path d="M4.167 10h11.667M12.5 13.333 15.833 10 12.5 6.668" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>'

KEYNOTES = [
 ("01", "The Grit Factor: Leading Through Challenge &amp; Change",
  "Grit isn't a slogan — it's a discipline. Drawing on her bestselling book and the science behind it, Shannon gives leaders a practical framework to stay clear, committed, and human when the pressure is highest.",
  ["A repeatable model for resilience under real stress",
   "How teams hold together through change and uncertainty",
   "The difference between grit and grind — and why it matters"]),
 ("02", "Decision-Making Under Pressure",
  "What does it take to decide when the stakes are highest and the information is incomplete? Shannon translates the discipline of the Apache cockpit into the decisions your leaders face every quarter.",
  ["A decision framework for high-stakes, low-certainty moments",
   "How to act decisively without acting recklessly",
   "Building a culture where good calls don't depend on luck"]),
 ("03", "Courageous Leadership",
  "The hardest part of leadership isn't strategy — it's courage: the hard conversation, the unpopular call, the stand taken when it costs something. Shannon shows leaders how to build it on purpose.",
  ["Moral courage as a trainable leadership skill",
   "Leading through fear instead of around it",
   "Turning values into action when it's inconvenient"]),
 ("04", "Women Leading in High-Stakes Environments",
  "One of the first women to fly the Apache in combat, Shannon speaks to what it takes to lead — and be heard — in rooms not built for you, without losing yourself in the process.",
  ["Confidence and credibility in male-dominated fields",
   "Owning authority without apology",
   "Sponsorship, resilience, and the long game of leadership"]),
]

FORMATS = [
 ("Keynote", "A signature 45–60 minute talk, tailored to your theme and audience."),
 ("Workshop", "Half- or full-day interactive sessions that turn ideas into practice."),
 ("Virtual Keynote", "Broadcast-quality remote talks for distributed teams and global events."),
 ("Fireside &amp; Panel", "Moderated conversations, Q&amp;A, and panels that go deep, fast."),
]

PHOTOS = [
 (UNIFORM, "Shannon Polson — uniform portrait"),
 (PORTRAIT, "Shannon Polson — portrait"),
 (LRG, "Shannon Polson — speaking portrait"),
 (BOOK, "The Grit Factor — book"),
]

# real testimonials harvested from the existing site
QUOTES = [
 ("If you aspire to become an outstanding leader, this book is a must-read.",
  "Amy McGrath — Lt. Col., USMC (Ret.)"),
 ("The Grit Factor changed how I approach challenges, lead my team, and push myself. Every leader should read this.",
  "Director, U.S. Army"),
 ("Shannon provided the &lsquo;wow factor&rsquo; that we strive to deliver to our members.",
  "Association executive"),
 ("Shannon was an absolute star, helping my team through the most challenging time in our business. Ten out of ten is not high enough.",
  "Corporate client"),
]

def chips(items): return "".join(f'<span class="sk-chip">{c}</span>' for c in items)
def stat(to, suf, label):
    return (f'<div class="sk-stat"><div class="n" data-to="{to}" data-suffix="{suf}">0{suf}</div>'
            f'<div class="l">{label}</div></div>')
def keynote(n,t,d,bs):
    return (f'<article class="sk-card"><div class="k-num">{n}</div><h3>{t}</h3><p>{d}</p>'
            f'<ul>{"".join(f"<li>{b}</li>" for b in bs)}</ul></article>')
def quote(q,c):
    return (f'<figure class="sk-quote"><div class="mark">&ldquo;</div><p>{q}</p>'
            f'<cite>{c}</cite></figure>')
def fmt(t,d):
    return (f'<div class="sk-format"><div class="ic">{ARROW}</div><h4>{t}</h4><p>{d}</p></div>')
def photo(src,alt):
    return (f'<div class="sk-photo"><img loading="lazy" src="{src}" alt="{alt}"/>'
            f'<a href="{src}" download>Download &darr;</a></div>')

MAIN = f'''<main class="main-wrapper sk-main">
<!-- HERO -->
<header class="sk-hero"><div class="sk-wrap"><div class="sk-hero-grid">
  <div class="sk-hero-copy reveal">
    <p class="sk-eyebrow">Speaker Kit</p>
    <h1>Shannon Huffman Polson</h1>
    <p class="sk-role">Keynote Speaker · Apache Pilot · Author of <em>The Grit Factor</em> · Professor</p>
    <p class="sk-punch">Leadership forged where the stakes were real — and translated for the decisions your people face every day.</p>
    <div class="sk-cta-row">
      <a class="sk-btn sk-btn--primary" href="../contact/index.html">Check Availability {ARROW}</a>
      <a class="sk-btn sk-btn--ghost" href="#reel">Watch the Reel</a>
      <button class="sk-btn sk-btn--ghost" onclick="window.print()" type="button">Save One-Sheet (PDF)</button>
    </div>
    <div class="sk-chips">{chips(["One of the first women to fly the Apache in combat","Bestselling author","Denali summit at 19","Fortune 500 audiences"])}</div>
  </div>
  <div class="sk-portrait reveal"><img src="{UNIFORM}" alt="Shannon Huffman Polson in uniform"/></div>
</div></div></header>

<!-- INTRO + BIOS -->
<section class="sk-section"><div class="sk-wrap"><div class="sk-intro-grid">
  <div class="reveal">
    <p class="sk-eyebrow">The Introduction</p>
    <h2 class="sk-h2">A speaker your audience won't forget — and a partner your team can count on.</h2>
    <p class="sk-lead">Shannon Huffman Polson was one of the first women to fly the Apache attack helicopter in the U.S. Army, leading soldiers in some of the most demanding conditions on earth. Today she is a sought-after keynote speaker, professor, and author of <em>The Grit Factor</em> — translating hard-won lessons in courage, grit, and decision-making into results for leaders and organizations worldwide.</p>
  </div>
  <div class="reveal-stagger">
    <div class="sk-bio-card"><h3>10-Second Intro</h3><p>Apache pilot turned bestselling author and leadership keynote speaker — teaching leaders to decide under pressure and lead with grit.</p></div>
    <div class="sk-bio-card"><h3>Read From the Stage</h3><p>&ldquo;Our next speaker was one of the first women to fly the Apache attack helicopter in combat. She&rsquo;s a professor, the author of <em>The Grit Factor</em>, and she&rsquo;s here to show us what it really takes to lead when it counts. Please welcome Shannon Huffman Polson.&rdquo;</p></div>
    <div class="sk-bio-card"><h3>At a Glance</h3><p>Founder of The Grit Institute · Author of <em>The Grit Factor</em> &amp; <em>North of Hope</em> · Youngest woman (at the time) to summit Denali at 19 · Keynotes for Fortune 500s, associations, and universities.</p></div>
  </div>
</div></div></section>

<!-- STATS -->
<section class="sk-section" style="padding-block:0"><div class="sk-wrap">
  <div class="sk-stats reveal">
    {stat(1000,"+","leaders trained worldwide")}
    {stat(100,"+","organizations served")}
    {stat(10,"+","years of measurable impact")}
  </div>
</div></section>

<!-- KEYNOTES -->
<section class="sk-section"><div class="sk-wrap">
  <div class="reveal"><p class="sk-eyebrow">Signature Keynotes</p>
  <h2 class="sk-h2">Four talks. One throughline: lead like it matters.</h2>
  <p class="sk-lead">Every talk is tailored to your audience and outcomes. These are the themes Shannon is booked for most.</p></div>
  <div class="sk-cards reveal-stagger">{"".join(keynote(*k) for k in KEYNOTES)}</div>
</div></section>

<!-- PROOF (dark) -->
<section class="sk-section sk-dark"><div class="sk-wrap">
  <div class="reveal" style="text-align:center">
    <p class="sk-eyebrow">Trusted By</p>
    <h2 class="sk-h2">The world&rsquo;s best organizations bring Shannon back.</h2>
  </div>
  <div class="sk-logos reveal">{"".join(f'<img loading="lazy" src="{t}" alt="Client logo"/>' for t in TRUST)}</div>
  <div class="sk-quotes reveal-stagger">{"".join(quote(q,c) for q,c in QUOTES)}</div>
</div></section>

<!-- REEL -->
<section class="sk-section" id="reel"><div class="sk-wrap">
  <div class="reveal"><p class="sk-eyebrow">Watch</p><h2 class="sk-h2">See Shannon on stage.</h2></div>
  <div class="sk-reel reveal"><video controls preload="metadata" playsinline poster="{LRG}">
    <source src="{V}sizzle-1.mp4" type="video/mp4"/></video></div>
</div></section>

<!-- FORMATS -->
<section class="sk-section sk-dark"><div class="sk-wrap">
  <div class="reveal"><p class="sk-eyebrow">Formats</p><h2 class="sk-h2">However your event is built, Shannon fits.</h2></div>
  <div class="sk-formats reveal-stagger">{"".join(fmt(t,d) for t,d in FORMATS)}</div>
</div></section>

<!-- PHOTOS -->
<section class="sk-section"><div class="sk-wrap">
  <div class="reveal"><p class="sk-eyebrow">Press Photos</p><h2 class="sk-h2">Hi-res photography.</h2>
  <p class="sk-lead">Hover any image to download. Need a different crop or format? Just ask.</p></div>
  <div class="sk-photos reveal-stagger">{"".join(photo(s,a) for s,a in PHOTOS)}</div>
</div></section>

<!-- FINAL CTA (dark) -->
<section class="sk-section sk-dark sk-final"><div class="sk-wrap reveal">
  <p class="sk-eyebrow" style="text-align:center">Let&rsquo;s Talk</p>
  <h2 class="sk-h2">Bring Shannon to your stage.</h2>
  <p class="sk-lead" style="margin-inline:auto;text-align:center">Tell us about your event, your audience, and your date. We&rsquo;ll take it from there.</p>
  <div class="sk-cta-row" style="justify-content:center;margin-top:1.8rem">
    <a class="sk-btn sk-btn--primary" href="../contact/index.html">Check Availability {ARROW}</a>
    <button class="sk-btn sk-btn--ghost" onclick="window.print()" type="button">Save One-Sheet (PDF)</button>
  </div>
  <div class="sk-contact">
    <span>&#9742; <a href="tel:509-996-8011">509-996-8011</a></span>
    <span>&#9993; <a href="mailto:Shannon@TheGritInstitute.com">Shannon@TheGritInstitute.com</a></span>
  </div>
</div></section>
</main>'''

def build():
    tpl = open("about/index.html", encoding="utf-8").read()
    # swap main
    out = re.sub(r'<main class="main-wrapper">.*?</main>', lambda _: MAIN, tpl, count=1, flags=re.S)
    # title
    title = "Speaker Kit — Shannon Huffman Polson | Keynote Speaker"
    desc = ("Shannon Huffman Polson's speaker kit: signature keynotes, bio, reel, testimonials, "
            "hi-res photos, and booking info. Apache pilot, author of The Grit Factor, leadership keynote speaker.")
    out = re.sub(r'<title>.*?</title>', '<title>' + html.escape(title) + '</title>', out, count=1, flags=re.S)
    # rebuild gi-seo block
    u = SITE_URL + "/speaker-kit"; e = lambda s: html.escape(s, quote=True)
    seo = ("<!--gi-seo-->"
           f'<meta name="description" content="{e(desc)}"/>'
           f'<link rel="canonical" href="{u}"/>'
           f'<meta property="og:title" content="{e(title)}"/>'
           f'<meta property="og:description" content="{e(desc)}"/>'
           f'<meta property="og:type" content="profile"/>'
           f'<meta property="og:url" content="{u}"/>'
           f'<meta name="twitter:card" content="summary_large_image"/>'
           f'<meta name="twitter:title" content="{e(title)}"/>'
           f'<meta name="twitter:description" content="{e(desc)}"/><!--/gi-seo-->')
    out = re.sub(r'<!--gi-seo-->.*?<!--/gi-seo-->', lambda _: seo, out, count=1, flags=re.S)
    # add stylesheet + script
    out = out.replace('</head>', '<link rel="stylesheet" href="../speaker-kit.css"/><script defer src="../speaker-kit.js"></script></head>', 1)
    os.makedirs("speaker-kit", exist_ok=True)
    open("speaker-kit/index.html", "w", encoding="utf-8").write(out)
    print("built speaker-kit/index.html")

if __name__ == "__main__":
    build()
