/* The Grit Institute — redesign enhancements (tiny, deferred) */
(function () {
  /* --- a11y: skip-to-content link --- */
  var main = document.querySelector('main');
  if (main) {
    if (!main.id) main.id = 'gi-main';
    var skip = document.createElement('a');
    skip.className = 'gi-skip';
    skip.href = '#' + main.id;
    skip.textContent = 'Skip to content';
    document.body.insertBefore(skip, document.body.firstChild);
  }

  /* --- nav: solidify on scroll --- */
  var nav = document.querySelector('.navigation');
  if (nav) {
    var onScroll = function () { nav.classList.toggle('is-scrolled', window.scrollY > 24); };
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });
  }

  /* --- floating "Book Shannon" CTA --- */
  var path = location.pathname;
  if (!/\/contact(\/|\/index\.html)?$/.test(path)) {
    var segs = path.split('/').filter(Boolean);
    var depth = Math.max(0, segs.length - 1);
    var prefix = depth ? new Array(depth + 1).join('../') : '';
    var cta = document.createElement('a');
    cta.className = 'gi-float-cta';
    cta.href = prefix + 'contact/index.html';
    cta.setAttribute('aria-label', 'Book Shannon');
    cta.innerHTML = 'Book Shannon<svg viewBox="0 0 20 20" fill="none"><path d="M4.167 10h11.667M12.5 13.333 15.833 10 12.5 6.668" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>';
    document.body.appendChild(cta);
    var toggleCta = function () { cta.classList.toggle('show', window.scrollY > 520); };
    toggleCta();
    window.addEventListener('scroll', toggleCta, { passive: true });
  }

  /* --- hero scroll cue (homepage) --- */
  var hero = document.querySelector('.hero_section');
  if (hero) {
    if (getComputedStyle(hero).position === 'static') hero.style.position = 'relative';
    var cue = document.createElement('button');
    cue.type = 'button';
    cue.className = 'gi-scroll-cue';
    cue.setAttribute('aria-label', 'Scroll down');
    cue.innerHTML = '<span class="mouse"></span><span>Scroll</span>';
    cue.addEventListener('click', function () {
      window.scrollTo({ top: hero.getBoundingClientRect().bottom + window.scrollY - 80, behavior: 'smooth' });
    });
    hero.appendChild(cue);
    window.addEventListener('scroll', function () {
      cue.style.opacity = window.scrollY > 160 ? '0' : '1';
    }, { passive: true });
  }

  /* --- compass motif: a slowly-rotating compass rose accent --- */
  var COMPASS =
    '<svg viewBox="0 0 200 200" fill="none" aria-hidden="true">' +
    '<circle cx="100" cy="100" r="96" stroke="currentColor" stroke-width="1.2" opacity=".5"/>' +
    '<circle cx="100" cy="100" r="74" stroke="currentColor" stroke-width="1" opacity=".3"/>' +
    '<g stroke="currentColor" stroke-width="1" opacity=".5">' +
    '<line x1="100" y1="6" x2="100" y2="26"/><line x1="100" y1="174" x2="100" y2="194"/>' +
    '<line x1="6" y1="100" x2="26" y2="100"/><line x1="174" y1="100" x2="194" y2="100"/></g>' +
    '<path d="M100 18 L112 100 L100 182 L88 100 Z" fill="currentColor" opacity=".22"/>' +
    '<path d="M18 100 L100 88 L182 100 L100 112 Z" fill="currentColor" opacity=".12"/>' +
    '<path d="M100 30 L107 100 L100 100 Z" fill="currentColor" opacity=".55"/>' +
    '<circle cx="100" cy="100" r="4" fill="currentColor"/></svg>';
  var addCompass = function (host, cls) {
    var c = document.createElement('div');
    c.className = 'gi-compass ' + (cls || '');
    c.innerHTML = COMPASS;
    if (getComputedStyle(host).position === 'static') host.style.position = 'relative';
    host.insertBefore(c, host.firstChild);
  };
  var footer = document.querySelector('footer, .footer_section');
  if (footer) addCompass(footer, 'gi-compass--footer');
  [].slice.call(document.querySelectorAll('.sk-final, .sk-dark')).slice(0, 2).forEach(function (s) {
    addCompass(s, 'gi-compass--section');
  });

  /* --- scroll-reveal engine (replaces Webflow IX2 on upgraded pages) --- */
  var reveals = [].slice.call(document.querySelectorAll('.reveal, .reveal-stagger, .gi-book-fly'));
  if (reveals.length) {
    var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    if (reduce || !('IntersectionObserver' in window)) {
      reveals.forEach(function (el) { el.classList.add('in'); });
    } else {
      var io = new IntersectionObserver(function (entries) {
        entries.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
      }, { threshold: 0.14, rootMargin: '0px 0px -8% 0px' });
      reveals.forEach(function (el) { io.observe(el); });
      // safety net: never leave content hidden if something misfires
      setTimeout(function () { reveals.forEach(function (el) { el.classList.add('in'); }); }, 2600);
    }
  }
})();
