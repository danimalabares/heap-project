// Left and right arrow keys follow the
// "previous" and "next" links of a page
// (ul.neighbours), when it has them.
document.addEventListener("keydown", function(event) {
  if (event.defaultPrevented) return;
  if (event.altKey || event.ctrlKey || event.metaKey || event.shiftKey) return;
  if (event.key !== "ArrowLeft" && event.key !== "ArrowRight") return;

  // leave typing, form controls and embedded models alone
  var target = event.target;
  if (target && target.closest &&
      target.closest("input, textarea, select, button, iframe, [contenteditable]")) return;

  var side = event.key === "ArrowLeft" ? "left" : "right";
  var link = document.querySelector("ul.neighbours li." + side + " a[href]");
  if (!link) return;

  event.preventDefault();
  window.location.href = link.href;
});

// On a touch screen, a horizontal swipe does
// the same: swipe left for "next", swipe right
// for "previous".
(function() {
  var start = null;

  // true if the touch began inside something
  // that scrolls sideways (a wide formula, a
  // table, code) or inside a control or model
  function busy(node) {
    for (var el = node; el && el !== document.body; el = el.parentElement) {
      if (el.matches && el.matches("input, textarea, select, button, iframe, canvas, [contenteditable]")) return true;
      if (el.scrollWidth > el.clientWidth + 1) {
        var overflow = window.getComputedStyle(el).overflowX;
        if (overflow === "auto" || overflow === "scroll") return true;
      }
    }
    return false;
  }

  document.addEventListener("touchstart", function(event) {
    start = null;
    if (event.touches.length !== 1) return;
    if (busy(event.target)) return;
    var touch = event.touches[0];
    start = { x: touch.clientX, y: touch.clientY, time: Date.now() };
  }, { passive: true });

  document.addEventListener("touchmove", function(event) {
    // a second finger means zooming, not swiping
    if (event.touches.length !== 1) start = null;
  }, { passive: true });

  document.addEventListener("touchend", function(event) {
    if (!start) return;
    var touch = event.changedTouches[0];
    var dx = touch.clientX - start.x;
    var dy = touch.clientY - start.y;
    var elapsed = Date.now() - start.time;
    start = null;

    if (elapsed > 1000) return;
    if (Math.abs(dx) < 60 || Math.abs(dx) < 1.5 * Math.abs(dy)) return;
    // zoomed-in page: the swipe pans it
    if (window.visualViewport && window.visualViewport.scale > 1.01) return;
    // the page itself scrolls sideways
    if (document.documentElement.scrollWidth > window.innerWidth + 1) return;
    var selection = window.getSelection && window.getSelection();
    if (selection && String(selection).length > 0) return;

    var side = dx > 0 ? "left" : "right";
    var link = document.querySelector("ul.neighbours li." + side + " a[href]");
    if (link) window.location.href = link.href;
  }, { passive: true });
})();
