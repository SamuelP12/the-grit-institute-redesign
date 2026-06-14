/* Speaker Kit — scroll reveal + stat count-up (deferred, reduced-motion aware) */
(function () {
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var reveals = [].slice.call(document.querySelectorAll('.reveal, .reveal-stagger'));

  if (reduce || !('IntersectionObserver' in window)) {
    reveals.forEach(function (el) { el.classList.add('in'); });
    runCounts(true);
    return;
  }

  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
    });
  }, { threshold: 0.16, rootMargin: '0px 0px -8% 0px' });
  reveals.forEach(function (el) { io.observe(el); });

  // animated count-up for .sk-stat .n[data-to]
  var counted = false;
  var statWrap = document.querySelector('.sk-stats');
  if (statWrap) {
    var so = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting && !counted) { counted = true; runCounts(false); so.disconnect(); }
      });
    }, { threshold: 0.4 });
    so.observe(statWrap);
  }

  function runCounts(instant) {
    [].slice.call(document.querySelectorAll('.sk-stat .n[data-to]')).forEach(function (el) {
      var to = parseInt(el.getAttribute('data-to'), 10) || 0;
      var suffix = el.getAttribute('data-suffix') || '';
      if (instant) { el.textContent = to + suffix; return; }
      var start = null, dur = 1400;
      function step(ts) {
        if (!start) start = ts;
        var p = Math.min((ts - start) / dur, 1);
        var eased = 1 - Math.pow(1 - p, 3);
        el.textContent = Math.round(eased * to) + suffix;
        if (p < 1) requestAnimationFrame(step);
      }
      requestAnimationFrame(step);
    });
  }
})();
