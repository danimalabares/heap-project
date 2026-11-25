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
