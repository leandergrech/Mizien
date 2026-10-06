/* Homepage claim cards (site/index.njk): every few seconds one card is swapped for another check from the record, so
   the size of the record shows. Rotation pauses while the pointer or keyboard focus is on the cards, while the tab is
   hidden, and never starts for readers who prefer reduced motion. A Pause button stops it for good. */
(function () {
  "use strict";
  var grid = document.getElementById("mosaic"), dataEl = document.getElementById("mosaic-data"), btn = document.getElementById("mosaic-pause");
  if (!grid || !dataEl) return;
  var BASE = (document.currentScript && document.currentScript.src || location.href).replace(/assets\/home\.js.*$/, "");
  var pool = JSON.parse(dataEl.textContent), shown = {}, held = false, stopped = false, timer = 0;
  var reduce = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;
  function esc(s) { return String(s).replace(/[&<>"']/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]; }); }
  function card(c) {
    return '<a class="mc-link" href="' + esc(BASE + c.path.replace(/^\//, "")) + '"><span class="mc-top"><span class="badge v-' + esc(c.v) + '">' +
      (c.pledge ? "Pledge: " : "") + esc(c.label) + "</span>" + (c.draft ? '<span class="mc-draft" title="Pending right of reply where the verdict needs one">Draft</span>' : "") +
      '</span><span class="mc-quote">“' + esc(c.quote) + '”</span><span class="mc-meta">' + esc(c.speaker) + (c.date ? " · " + esc(c.date) : "") +
      '</span><span class="mc-id">' + esc(c.id) + " · " + esc(c.topic) + "</span></a>";
  }
  // Start from a random selection, so each visit opens on different checks.
  var items = grid.children, order = pool.slice().sort(function () { return Math.random() - 0.5; });
  for (var i = 0; i < items.length && i < order.length; i++) { items[i].className = "mcard v-" + order[i].v; items[i].innerHTML = card(order[i]); shown[order[i].id] = 1; }
  if (reduce || pool.length <= items.length) return;
  function swap() {
    if (held || stopped || document.hidden) return;
    var free = pool.filter(function (c) { return !shown[c.id]; }); if (!free.length) return;
    var next = free[Math.floor(Math.random() * free.length)], li = items[Math.floor(Math.random() * items.length)];
    var old = li.querySelector(".mc-id"); if (old) delete shown[old.textContent.split(" · ")[0]];
    li.classList.add("is-out");
    setTimeout(function () { li.className = "mcard v-" + next.v + " is-in"; li.innerHTML = card(next); shown[next.id] = 1;
      setTimeout(function () { li.classList.remove("is-in"); }, 450); }, 350);
  }
  timer = setInterval(swap, 3800);
  grid.addEventListener("pointerenter", function () { held = true; });
  grid.addEventListener("pointerleave", function () { held = false; });
  grid.addEventListener("touchstart", function () { held = true; }, { passive: true });
  grid.addEventListener("focusin", function () { held = true; });
  grid.addEventListener("focusout", function () { held = false; });
  if (btn) { btn.hidden = false;
    btn.addEventListener("click", function () { stopped = !stopped; btn.setAttribute("aria-pressed", stopped ? "true" : "false"); btn.textContent = stopped ? "Play" : "Pause"; }); }
})();
