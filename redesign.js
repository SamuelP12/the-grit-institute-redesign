/* The Grit Institute — redesign micro-enhancements (tiny, deferred) */
(function () {
  /* --- nav: solidify on scroll --- */
  var nav = document.querySelector('.navigation');
  if (nav) {
    var onScroll = function () {
      nav.classList.toggle('is-scrolled', window.scrollY > 24);
    };
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });
  }

  /* --- floating "Book Shannon" CTA: appears on scroll, drives bookings --- */
  var path = location.pathname;
  var onContact = /\/contact(\/|\/index\.html)?$/.test(path);
  if (!onContact) {
    // depth-aware link to the contact page (works at any nesting level)
    var segs = path.split('/').filter(Boolean);
    var depth = Math.max(0, segs.length - 1);
    var prefix = depth ? new Array(depth + 1).join('../') : '';
    var href = prefix + 'contact/index.html';

    var cta = document.createElement('a');
    cta.className = 'gi-float-cta';
    cta.href = href;
    cta.setAttribute('aria-label', 'Book Shannon');
    cta.innerHTML = 'Book Shannon' +
      '<svg viewBox="0 0 20 20" fill="none"><path d="M4.167 10h11.667M12.5 13.333 15.833 10 12.5 6.668" ' +
      'stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>';
    document.body.appendChild(cta);

    var toggleCta = function () {
      cta.classList.toggle('show', window.scrollY > 520);
    };
    toggleCta();
    window.addEventListener('scroll', toggleCta, { passive: true });
  }
})();
