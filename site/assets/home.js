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

/* The deck of claim panels in the hero (site/index.njk): a random chain of checks, one card at a time with the next two
   showing behind it. Swipe or drag the front card left for the next check and right to go back along the chain; the
   arrows and the arrow keys do the same. On wide screens the deck turns by itself every few seconds, pausing on hover,
   focus or a hidden tab; never with reduced motion. Each card links to its check. */
(function () {
  "use strict";
  var deck = document.getElementById("deck"), dataEl = document.getElementById("mosaic-data");
  if (!deck || !dataEl) return;
  var wrap = deck.parentNode, nav = wrap.querySelector(".deck-nav"), num = wrap.querySelector(".deck-n"), play = wrap.querySelector(".deck-play");
  var BASE = (document.currentScript && document.currentScript.src || location.href).replace(/assets\/home\.js.*$/, "");
  var reduce = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;
  var wide = window.matchMedia ? matchMedia("(min-width: 901px)") : { matches: true };
  var pool = JSON.parse(dataEl.textContent), chain = pool.slice(), at = 0, busy = false, held = false, stopped = false;
  for (var i = chain.length - 1; i > 0; i--) { var j = Math.floor(Math.random() * (i + 1)), t = chain[i]; chain[i] = chain[j]; chain[j] = t; }
  if (chain.length < 2) return;
  function esc(s) { return String(s == null ? "" : s).replace(/[&<>"']/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]; }); }
  function html(c) {
    return '<a class="dc-link" href="' + esc(BASE + c.path.replace(/^\//, "")) + '"><span class="dc-head"><span class="dc-kicker">' + esc(c.id) + " · " + esc(c.topic) +
      '</span><span class="dc-verdict">' + (c.pledge ? "Pledge: " : "") + esc(c.label) + '</span><span class="dc-tags">' +
      (c.confidence ? "<span>" + esc(c.confidence) + " confidence</span>" : "") + (c.draft ? '<span class="dc-draft">Draft</span>' : "") +
      '</span></span><span class="dc-body"><span class="dc-title">' + esc(c.title) + '</span><span class="dc-quote">“' + esc(c.quote) + '”</span><span class="dc-meta">' +
      esc(c.speaker) + (c.date ? " · " + esc(c.date) : "") + (c.place ? "<br>" + esc(c.place) : "") + '</span><span class="dc-go">Read the check →</span></span></a>';
  }
  function mod(n) { return (n % chain.length + chain.length) % chain.length; }
  function card(k, cls) { var el = document.createElement("article"); el.className = "dcard " + cls + " v-" + chain[mod(k)].v; el.innerHTML = html(chain[mod(k)]); return el; }
  function draw() {
    deck.innerHTML = "";
    deck.appendChild(card(at + 2, "is-back2")); deck.appendChild(card(at + 1, "is-back1")); deck.appendChild(card(at, "is-front"));
    deck.querySelectorAll(".dcard:not(.is-front) a").forEach(function (a) { a.tabIndex = -1; a.setAttribute("aria-hidden", "true"); });
    num.textContent = (mod(at) + 1) + " / " + chain.length;
  }
  // dir 1: the front card leaves to the left and the next one comes forward; dir -1: the previous card comes back on top
  function go(dir) {
    if (busy) return; busy = true;
    var front = deck.querySelector(".is-front");
    if (reduce) { at += dir; draw(); busy = false; return; }
    if (dir > 0) {
      front.style.transition = ""; front.classList.add("fly-left"); front.style.transform = "";
      deck.querySelector(".is-back1").classList.add("rise1"); deck.querySelector(".is-back2").classList.add("rise2");
      setTimeout(function () { at += 1; draw(); busy = false; }, 380);
    } else {
      var back = card(at - 1, "is-front from-right"); deck.appendChild(back);
      back.getBoundingClientRect(); back.classList.remove("from-right");
      front.classList.add("sink1"); deck.querySelector(".is-back1").classList.add("sink2");
      setTimeout(function () { at -= 1; draw(); busy = false; }, 380);
    }
  }
  // Drag or swipe the front card; a short movement snaps back, a long one turns the deck that way.
  var sx = 0, sy = 0, dx = 0, dragging = false, moved = false, pid = null;
  deck.addEventListener("pointerdown", function (e) {
    var f = e.target.closest(".is-front"); if (!f || busy || (e.pointerType === "mouse" && e.button !== 0)) return;
    sx = e.clientX; sy = e.clientY; dx = 0; dragging = true; moved = false; pid = e.pointerId;
  });
  deck.addEventListener("pointermove", function (e) {
    if (!dragging || e.pointerId !== pid) return;
    var x = e.clientX - sx, y = e.clientY - sy;
    if (!moved) { if (Math.abs(x) < 8) return; if (Math.abs(y) > Math.abs(x)) { dragging = false; return; } moved = true; try { deck.setPointerCapture(pid); } catch (er) {} }
    dx = x; var f = deck.querySelector(".is-front"); f.style.transition = "none"; f.style.transform = "translateX(" + dx + "px) rotate(" + (dx / 22) + "deg)";
  });
  function end() {
    if (!dragging) return; dragging = false;
    var f = deck.querySelector(".is-front"); if (!moved) return;
    f.style.transition = ""; f.style.transform = "";
    if (dx < -70) go(1); else if (dx > 70) go(-1);
  }
  deck.addEventListener("pointerup", end); deck.addEventListener("pointercancel", end);
  deck.addEventListener("click", function (e) { if (moved) { e.preventDefault(); moved = false; } }, true);   // a drag is not a click
  nav.addEventListener("click", function (e) { var b = e.target.closest("[data-go]"); if (b) { go(+b.dataset.go); } });
  wrap.addEventListener("keydown", function (e) { if (e.key === "ArrowRight") { go(1); e.preventDefault(); } else if (e.key === "ArrowLeft") { go(-1); e.preventDefault(); } });
  // turning by itself: wide screens only, and only while nobody is reading or holding the deck
  wrap.addEventListener("pointerenter", function () { held = true; }); wrap.addEventListener("pointerleave", function () { held = false; });
  wrap.addEventListener("focusin", function () { held = true; }); wrap.addEventListener("focusout", function () { held = false; });
  function auto() { return !reduce && wide.matches; }
  function syncPlay() { play.hidden = !auto(); play.textContent = stopped ? "Play" : "Pause"; play.setAttribute("aria-pressed", stopped ? "true" : "false"); }
  play.addEventListener("click", function () { stopped = !stopped; syncPlay(); });
  if (wide.addEventListener) wide.addEventListener("change", syncPlay);
  setInterval(function () { if (auto() && !held && !stopped && !document.hidden) go(1); }, 5200);
  nav.hidden = false; wrap.classList.add("is-live"); syncPlay(); draw();
})();
