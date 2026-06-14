#!/usr/bin/env python3
"""Build 4 bespoke keynote landing pages under /keynotes/<slug>/ from the About template.
Each targets '[topic] keynote speaker', sells one talk, and cross-sells book/kit."""
import os, re, html, json

SITE_URL = "https://www.thegritinstitute.com"
A = "../../assets/cdn.prod.website-files.com/692709e75138a09dc8a4f247/"
V = "../../assets/cdn-public.prismatico.io/grit-institute/"
LOGO_ABS = "https://cdn.prod.website-files.com/692709e75138a09dc8a4f247/69271a4e915393eb42030c40_Grit%20Institute%20logo.webp"
UNIFORM = A + "6960023a65e24bbd97f8d75c_GritFactor_Portrait_ShannonUniform.webp"
PORTRAIT = A + "69600255fcb33fc07dcde803_GritFactor_Portrait_ShannonPolson.webp"
LRG = A + "696002b4636777d067071a37_ShannonPolson122_lrg.webp"
ARROW = '<svg viewBox="0 0 20 20" fill="none"><path d="M4.167 10h11.667M12.5 13.333 15.833 10 12.5 6.668" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>'

KEYNOTES = [
 {"slug":"decision-making-under-pressure","img":UNIFORM,
  "title":"Decision-Making Under Pressure — Keynote Speaker | Shannon Huffman Polson",
  "kw":"decision-making under pressure keynote speaker",
  "h1":"Decision-Making Under Pressure",
  "sub":"From the Apache cockpit to the boardroom — how the best leaders decide when the stakes are high and the information isn't all there.",
  "chips":["High-stakes industries","Executive teams","45–60 min keynote"],
  "lead":"Your people don't fail for lack of strategy. They freeze, hesitate, or overreact in the moments that matter most. Drawing on her years flying the Apache attack helicopter — where a decision could mean life or death — Shannon gives your leaders a clear, repeatable way to think and act under real pressure.",
  "who":["Executive and senior leadership teams","High-stakes fields: finance, healthcare, defense, tech","Any team that has to perform when it counts"],
  "takeaways":["A decision framework that holds up when certainty doesn't","How to act decisively without acting recklessly","Managing fear, adrenaline, and the urge to freeze","Building a culture where good calls aren't a matter of luck"],
  "quote":("Shannon was an absolute star, helping my team through the most challenging time in our business. Ten out of ten is not high enough.","Corporate client")},
 {"slug":"the-grit-factor","img":PORTRAIT,
  "title":"The Grit Factor Keynote — Resilience Speaker | Shannon Huffman Polson",
  "kw":"resilience keynote speaker",
  "h1":"The Grit Factor: Leading Through Challenge & Change",
  "sub":"Grit isn't a slogan — it's a discipline. The science and the story of how the best leaders stay clear, committed, and human when everything's hard.",
  "chips":["Resilience","Change & uncertainty","Based on the bestselling book"],
  "lead":"Built on her bestselling book and the research behind it, this keynote moves audiences from inspiration to action — giving them a practical model for resilience they can use the moment they walk out of the room, and the next time everything goes sideways.",
  "who":["Organizations navigating change, growth, or pressure","Leadership summits and all-company kickoffs","Teams that need to rebuild momentum after a hard season"],
  "takeaways":["A repeatable model for resilience under real stress","How teams hold together through change and uncertainty","The difference between grit and grind — and why it matters","Turning setbacks into the raw material of leadership"],
  "quote":("If you aspire to become an outstanding leader, this is a must-read — and an unforgettable talk.","Amy McGrath — Lt. Col., USMC (Ret.)")},
 {"slug":"courageous-leadership","img":LRG,
  "title":"Courageous Leadership Keynote Speaker | Shannon Huffman Polson",
  "kw":"courageous leadership keynote speaker",
  "h1":"Courageous Leadership",
  "sub":"The hardest part of leadership isn't strategy. It's courage — the hard conversation, the unpopular call, the stand that costs something.",
  "chips":["Moral courage","Culture & values","Leadership development"],
  "lead":"Most leaders know what the right thing is. Far fewer do it when it's inconvenient. Shannon shows audiences how to build moral courage on purpose — so values become action, not a poster on the wall — and so the hardest calls get made when they need to be.",
  "who":["Leadership development programs and offsites","Values-driven organizations and associations","Emerging leaders stepping into bigger rooms"],
  "takeaways":["Moral courage as a trainable leadership skill","Leading through fear instead of around it","Having the hard conversation before it's a crisis","Turning stated values into real decisions"],
  "quote":("Shannon provided the ‘wow factor’ that we strive to deliver to our members.","Association executive")},
 {"slug":"women-leading-under-pressure","img":UNIFORM,
  "title":"Women's Leadership Keynote Speaker | Shannon Huffman Polson",
  "kw":"women's leadership keynote speaker",
  "h1":"Women Leading in High-Stakes Environments",
  "sub":"One of the first women to fly the Apache in combat on what it takes to lead — and be heard — in rooms that weren't built for you.",
  "chips":["Women's leadership","Confidence & credibility","Male-dominated fields"],
  "lead":"This isn't a talk about barriers — it's a talk about command. Shannon speaks from lived experience leading in one of the most male-dominated environments on earth, giving women practical tools to own their authority, build credibility, and lead the long game without losing themselves.",
  "who":["Women's leadership conferences and ERGs","Organizations investing in their female talent pipeline","Mixed audiences ready for a candid, galvanizing message"],
  "takeaways":["Confidence and credibility in male-dominated fields","Owning authority without apology","Sponsorship, resilience, and the long game of leadership","Leading as yourself — not a copy of someone else"],
  "quote":("Shannon was Amazing! Her story was spot on with our mission and goals. She was outstanding!","Conference host")},
]

def chips(items): return "".join(f'<span class="sk-chip">{c}</span>' for c in items)
def li(items): return "".join(f"<li>{x}</li>" for x in items)

def page_main(k):
    others = [o for o in KEYNOTES if o["slug"] != k["slug"]][:3]
    more = "".join(
      f'<article class="sk-card"><h3>{o["h1"]}</h3>'
      f'<p>{o["sub"]}</p><a class="sk-btn sk-btn--outline" href="../{o["slug"]}/index.html">Explore {ARROW}</a></article>'
      for o in others)
    return f'''<main class="main-wrapper sk-main">
<header class="sk-hero"><div class="sk-wrap"><div class="sk-hero-grid">
  <div class="sk-hero-copy reveal">
    <p class="sk-eyebrow">Signature Keynote</p>
    <h1>{k["h1"]}</h1>
    <p class="sk-role">{k["sub"]}</p>
    <div class="sk-cta-row">
      <a class="sk-btn sk-btn--primary" href="../../contact/index.html">Check Availability {ARROW}</a>
      <a class="sk-btn sk-btn--ghost" href="../../speaker-kit/index.html">Speaker Kit</a>
    </div>
    <div class="sk-chips">{chips(k["chips"])}</div>
  </div>
  <div class="sk-portrait reveal"><img src="{k["img"]}" alt="Shannon Huffman Polson"/></div>
</div></div></header>

<section class="sk-section"><div class="sk-wrap"><div class="sk-intro-grid">
  <div class="reveal"><p class="sk-eyebrow">The Talk</p>
    <h2 class="sk-h2">What your audience walks away with.</h2>
    <p class="sk-lead">{k["lead"]}</p></div>
  <div class="reveal">
    <div class="sk-bio-card"><h3>Who It's For</h3><p>{"</p><p>".join(k["who"])}</p></div>
  </div>
</div></div></section>

<section class="sk-section sk-dark"><div class="sk-wrap">
  <div class="reveal"><p class="sk-eyebrow">Outcomes</p><h2 class="sk-h2">Four things they'll take back to work.</h2></div>
  <div class="sk-cards reveal-stagger">
    {"".join(f'<article class="sk-card"><div class="k-num">0{i+1}</div><p>{t}</p></article>' for i,t in enumerate(k["takeaways"]))}
  </div>
  <div class="sk-quotes reveal" style="grid-template-columns:1fr;max-width:780px;margin-inline:auto">
    <figure class="sk-quote"><div class="mark">&ldquo;</div><p>{k["quote"][0]}</p><cite>{k["quote"][1]}</cite></figure>
  </div>
</div></section>

<section class="sk-section"><div class="sk-wrap">
  <div class="reveal"><p class="sk-eyebrow">More Keynotes</p><h2 class="sk-h2">Explore Shannon's other talks.</h2></div>
  <div class="sk-cards reveal-stagger">{more}</div>
</div></section>

<section class="sk-section sk-dark sk-final"><div class="sk-wrap reveal">
  <p class="sk-eyebrow" style="text-align:center">Let&rsquo;s Talk</p>
  <h2 class="sk-h2">Bring &ldquo;{k["h1"]}&rdquo; to your stage.</h2>
  <p class="sk-lead" style="margin-inline:auto;text-align:center">Tell us about your event, audience, and date — we&rsquo;ll take it from there.</p>
  <div class="sk-cta-row" style="justify-content:center;margin-top:1.8rem">
    <a class="sk-btn sk-btn--primary" href="../../contact/index.html">Check Availability {ARROW}</a>
    <a class="sk-btn sk-btn--ghost" href="../../the-grit-factor/index.html">Read the Book</a>
  </div>
  <div class="sk-contact"><span>&#9742; <a href="tel:509-996-8011">509-996-8011</a></span>
    <span>&#9993; <a href="mailto:Shannon@TheGritInstitute.com">Shannon@TheGritInstitute.com</a></span></div>
</div></section>
</main>'''

def build():
    tpl = open("about/index.html", encoding="utf-8").read()
    # about template nav/footer/scripts use ../ ; keynote pages are depth 2 -> need ../../
    for k in KEYNOTES:
        # about template is depth-1 (all relative paths are "../"); keynote pages are depth-2.
        # bump every "../" to "../../" FIRST, then swap in our main (already written with ../../).
        out = tpl.replace('../', '../../')
        out = re.sub(r'<main class="main-wrapper">.*?</main>', lambda _: page_main(k), out, count=1, flags=re.S)
        # title + SEO
        e = lambda s: html.escape(s, quote=True)
        u = f"{SITE_URL}/keynotes/{k['slug']}"
        desc = f"{k['h1']} — a keynote by Shannon Huffman Polson, Apache pilot and author of The Grit Factor. {k['sub']}"
        if len(desc) > 158: desc = desc[:155].rsplit(' ',1)[0] + "…"
        out = re.sub(r'<title>.*?</title>', '<title>' + html.escape(k["title"]) + '</title>', out, count=1, flags=re.S)
        svc = {"@context":"https://schema.org","@type":"Service","serviceType":k["kw"],
               "name":k["h1"],"description":desc,"provider":{"@id":SITE_URL+"/#shannon"},"areaServed":"Worldwide","url":u}
        seo = ("<!--gi-seo-->"
               f'<meta name="description" content="{e(desc)}"/>'
               f'<link rel="canonical" href="{u}"/>'
               f'<meta property="og:title" content="{e(k["title"])}"/>'
               f'<meta property="og:description" content="{e(desc)}"/>'
               f'<meta property="og:type" content="website"/><meta property="og:url" content="{u}"/>'
               f'<meta name="twitter:card" content="summary_large_image"/>'
               f'<meta name="twitter:title" content="{e(k["title"])}"/>'
               f'<meta name="twitter:description" content="{e(desc)}"/>'
               f'<script type="application/ld+json">{json.dumps(svc, ensure_ascii=False)}</script><!--/gi-seo-->')
        out = re.sub(r'<!--gi-seo-->.*?<!--/gi-seo-->', lambda _: seo, out, count=1, flags=re.S)
        out = out.replace('</head>', '<link rel="stylesheet" href="../../speaker-kit.css"/><script defer src="../../speaker-kit.js"></script></head>', 1)
        os.makedirs(f"keynotes/{k['slug']}", exist_ok=True)
        open(f"keynotes/{k['slug']}/index.html", "w", encoding="utf-8").write(out)
        print("built keynotes/%s/index.html" % k["slug"])

if __name__ == "__main__":
    build()
