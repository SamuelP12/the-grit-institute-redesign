/* The Grit Institute — redesign micro-enhancements (tiny, deferred) */
(function () {
  var nav = document.querySelector('.navigation');
  if (nav) {
    var onScroll = function () {
      nav.classList.toggle('is-scrolled', window.scrollY > 24);
    };
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });
  }
})();
