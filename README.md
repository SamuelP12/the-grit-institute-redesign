# The Grit Institute — REDESIGN (working copy)

> **This is the working copy we edit and improve.**
> The untouched original lives at github.com/SamuelP12/the-grit-institute-original
> and locally at ~/grit-institute. Never edit that one.

---

A complete, editable static copy of `https://the-grit-institute.webflow.io`,
captured 2026-06-13. Every page, image, stylesheet, font reference, and script
is downloaded and rewritten to load from local files.

## View it locally
```bash
cd ~/grit-institute
python3 -m http.server 8099
# open http://localhost:8099/
```

## Structure
- `index.html` … each page lives at `<slug>/index.html` (e.g. `about/index.html`,
  `blog/the-astronaut-standard/index.html`). The homepage is `index.html`.
- `assets/` — all downloaded first-party files, mirrored by their original host/path:
  - `assets/cdn.prod.website-files.com/.../` — images (`.webp/.svg`), the site CSS
    (`.../css/*.css`), the Webflow interaction JS, lottie JSON, favicons.
  - `assets/d3e54v103j8qbb.cloudfront.net/` — jQuery.
- `_raw/` — untouched original HTML for each page (backup; safe to ignore/delete).
- `crawl.py` / `build.py` / `fix_css.py` / `verify.py` — the tooling used to
  capture and localize the site. Re-runnable.

## 27 pages captured
Home, About, Speaking, Courses, Transcend Mastermind, Offerings for Schools,
Powrpack, The Grit Factor, Other Books & Writing, Podcast, Blog, Media, Contact,
Privacy Policy, 404, plus all 12 blog posts.

## What stays remote (by design)
- **Outbound links** the site points to (Bookshop, Amazon, YouTube, news articles,
  social profiles, the live `thegritinstitute.com` domain) — left pointing at their
  real destinations.
- **Fonts** — Google Fonts (Geist) and Adobe Typekit load from their CDNs when online.
- Third-party embeds (YouTube/Spotify players, Substack, embedly).

## Verified
2,631 in-page references + 698 CSS `url()` references resolve to real local files —
0 broken. All 27 pages return HTTP 200 locally.
