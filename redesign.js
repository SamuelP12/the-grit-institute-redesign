/* The Grit Institute — redesign enhancements (tiny, deferred) */
(function () {
  /* --- forms: submit to Formspree, inline success (overrides dead Webflow handler) --- */
  document.addEventListener('submit', function (e) {
    var form = e.target;
    if (!form || !form.matches || !form.matches('form[data-gi-form]')) return;
    e.preventDefault();
    e.stopImmediatePropagation();
    var action = form.getAttribute('action') || '';
    var wrap = form.closest('.w-form') || form.parentNode;
    var done = wrap && wrap.querySelector('.w-form-done');
    var fail = wrap && wrap.querySelector('.w-form-fail');
    var btn = form.querySelector('[type="submit"], input[type="submit"]');
    if (action.indexOf('YOUR_FORMSPREE_ID') !== -1) {
      console.warn('[forms] Set your Formspree form ID in the form action to receive submissions.');
    }
    if (btn) { btn.dataset.label = btn.value || btn.textContent; if ('value' in btn) btn.value = 'Sending…'; }
    fetch(action, { method: 'POST', body: new FormData(form), headers: { Accept: 'application/json' } })
      .then(function (r) {
        if (r.ok) {
          form.style.display = 'none';
          if (done) done.style.display = 'block'; else { form.reset(); form.style.display = ''; }
        } else if (fail) { fail.style.display = 'block'; }
      })
      .catch(function () { if (fail) fail.style.display = 'block'; })
      .finally(function () { if (btn && 'value' in btn && btn.dataset.label) btn.value = btn.dataset.label; });
  }, true);

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

  /* --- a11y: keyboard-operable nav dropdowns + announced state --- */
  [].slice.call(document.querySelectorAll('.nav-dropdown')).forEach(function (dd) {
    var toggle = dd.querySelector('.nav-dropdown-toggle');
    if (!toggle) return;
    var set = function (open) { toggle.setAttribute('aria-expanded', open ? 'true' : 'false'); };
    dd.addEventListener('focusin', function () { set(true); });
    dd.addEventListener('focusout', function () { if (!dd.contains(document.activeElement)) set(false); });
    dd.addEventListener('mouseenter', function () { set(true); });
    dd.addEventListener('mouseleave', function () { set(false); });
    toggle.addEventListener('keydown', function (e) {
      if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        var first = dd.querySelector('.dropdown-navigation a');
        if (first) first.focus();
      } else if (e.key === 'Escape') {
        toggle.blur();
      }
    });
    // Escape from within the menu returns focus to the toggle
    dd.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') { e.preventDefault(); toggle.focus(); toggle.blur(); }
    });
  });

  /* --- footer: keep the copyright year current --- */
  var yr = new Date().getFullYear();
  [].slice.call(document.querySelectorAll('.gi-year')).forEach(function (el) { el.textContent = yr; });

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
    // reuse the nav's Contact link href so it's correct at any deploy path (e.g. GitHub Pages sub-path)
    var navContact = document.querySelector('.button.is-nav_btn') ||
                     document.querySelector('a[href$="contact/index.html"]');
    var contactHref = navContact ? navContact.getAttribute('href') : 'contact/index.html';
    var cta = document.createElement('a');
    cta.className = 'gi-float-cta';
    cta.href = contactHref;
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

  /* --- count-up for homepage stat numbers (static text -> animated) --- */
  var reduceMotion = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var stats = [].slice.call(document.querySelectorAll('.counters-number-style'));
  if (stats.length && 'IntersectionObserver' in window && !reduceMotion) {
    var countUp = function (el) {
      var to = parseInt(el.dataset.to, 10) || 0, suf = el.dataset.suffix || '', start = null, dur = 1600;
      var step = function (ts) {
        if (!start) start = ts;
        var p = Math.min((ts - start) / dur, 1), eased = 1 - Math.pow(1 - p, 3);
        el.textContent = Math.round(eased * to) + suf;
        if (p < 1) requestAnimationFrame(step);
      };
      requestAnimationFrame(step);
    };
    var sObs = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) { if (e.isIntersecting) { countUp(e.target); sObs.unobserve(e.target); } });
    }, { threshold: 0.5 });
    stats.forEach(function (el) {
      var txt = (el.textContent || '').trim();
      el.dataset.to = txt.replace(/[^0-9]/g, '');
      el.dataset.suffix = txt.replace(/[0-9]/g, '');
      el.textContent = '0' + el.dataset.suffix;
      sObs.observe(el);
    });
  }

  /* --- scroll-reveal engine (replaces Webflow IX2 on upgraded pages) --- */
  /* --- Apache: scroll-LINKED fly-in (progresses as you scroll), then hover --- */
  var heli = document.querySelector('.gi-heli-fly');
  if (heli) {
    if (window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
      heli.style.opacity = '1';
    } else {
      var heliLanded = false, heliTick = false;
      var updateHeli = function () {
        var r = heli.getBoundingClientRect(), vh = window.innerHeight || 800;
        var p = Math.max(0, Math.min(1, (vh - r.top) / (vh * 0.62)));  // 0=entering bottom, 1=landed
        if (p >= 1) {
          if (!heliLanded) { heliLanded = true; heli.style.transform = ''; heli.style.opacity = '1'; heli.classList.add('gi-landed'); }
        } else {
          if (heliLanded) { heliLanded = false; heli.classList.remove('gi-landed'); }
          heli.style.opacity = Math.min(1, p * 1.6);
          heli.style.transform = 'translateY(' + ((1 - p) * 150).toFixed(1) + 'px) scale(' + (0.62 + p * 0.38).toFixed(3) + ')';
        }
        heliTick = false;
      };
      var onHeliScroll = function () { if (!heliTick) { heliTick = true; requestAnimationFrame(updateHeli); } };
      updateHeli();
      window.addEventListener('scroll', onHeliScroll, { passive: true });
      window.addEventListener('resize', onHeliScroll, { passive: true });
    }
  }

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
