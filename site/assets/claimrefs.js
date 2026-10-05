/* Miżien: a short summary of a claim, shown on a long hover (or keyboard focus) over any link to it.
   Links are marked by the site build (data-claim="CC-012") or are plain links to /claims/CC-012/. The summaries
   come from data/claim-briefs.json, loaded the first time a pointer rests on such a link. Touch screens keep the
   ordinary tap-to-open behaviour. */
(function () {
  "use strict";
  var script = document.currentScript;
  var base = script ? new URL("../", script.src).href : new URL("./", location.href).href;
  var SHOW_MS = 550, FOCUS_MS = 350, HIDE_MS = 220;
  var briefs = null, loading = null, pop = null, current = null, showTimer = null, hideTimer = null;
  var VERDICT = { "supported": ["#2e7d4f", "#fff"], "largely-supported": ["#8db36b", "#13301f"],
    "not-substantiated": ["#d9772b", "#13301f"], "misleading": ["#b5483a", "#fff"], "contradicted": ["#8e2f25", "#fff"],
    "none": ["#5d7468", "#fff"] };
  var MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];

  function load() {
    if (briefs || loading) return loading;
    loading = fetch(base + "data/claim-briefs.json").then(function (r) { return r.ok ? r.json() : {}; })
      .then(function (d) { briefs = d; return d; }).catch(function () { briefs = {}; return briefs; });
    return loading;
  }
  function idOf(a) {
    if (!a || !a.getAttribute) return null;
    var id = a.getAttribute("data-claim");
    if (id) return id;
    if (a.tagName !== "A") return null;
    var h = a.getAttribute("href") || "", part = /#(CC-\d{3}[A-Z])$/.exec(h);
    if (part) return part[1];
    var m = /\/claims\/(CC-\d{3})\/?(?:[#?].*)?$/.exec(h);
    return m ? m[1] : null;
  }
  function refAt(node) {
    var a = node && node.closest ? node.closest("[data-claim], a[href*='claims/CC-']") : null;
    return a && idOf(a) && !a.hasAttribute("data-no-brief") ? a : null;
  }
  function ukDate(s) {
    var m = /^(\d{4})(?:-(\d{2}))?(?:-(\d{2}))?$/.exec(s || "");
    if (!m) return s || "";
    return m[2] ? (m[3] ? +m[3] + " " : "") + MONTHS[+m[2] - 1] + " " + m[1] : m[1];
  }
  function el(tag, cls, text) { var e = document.createElement(tag); if (cls) e.className = cls; if (text) e.textContent = text; return e; }

  function style() {
    var css = ".cref-pop{position:fixed;z-index:1000;max-width:min(360px,calc(100vw - 24px));background:#fbfaf6;color:#13301f;" +
      "border:1px solid #c9d6cc;border-radius:12px;box-shadow:0 14px 34px rgba(7,25,17,.28);font:14px/1.45 'Liberation Sans',Arial,Helvetica,sans-serif;" +
      "overflow:hidden;opacity:0;transform:translateY(4px);transition:opacity .14s ease,transform .14s ease;pointer-events:auto}" +
      ".cref-pop.on{opacity:1;transform:none}" +
      ".cref-pop .cr-head{display:flex;gap:10px;align-items:flex-start;padding:12px 14px 8px}" +
      ".cref-pop .cr-thumb{flex:0 0 52px;width:52px;height:52px;border-radius:8px;object-fit:cover;background:#e4ebe5}" +
      ".cref-pop .cr-kicker{font:700 11px/1.3 'Liberation Sans',Arial,sans-serif;letter-spacing:.06em;text-transform:uppercase;color:#4d6457;margin:0 0 3px}" +
      ".cref-pop .cr-title{font:700 15.5px/1.3 'Liberation Sans',Arial,sans-serif;margin:0;color:#0e2a1f}" +
      ".cref-pop .cr-verdict{display:flex;flex-wrap:wrap;gap:6px;align-items:center;padding:8px 14px;border-top:1px solid #e1e8e2;border-bottom:1px solid #e1e8e2;background:#f1f4ef}" +
      ".cref-pop .cr-pill{font:700 12px/1.2 'Liberation Sans',Arial,sans-serif;letter-spacing:.05em;text-transform:uppercase;padding:4px 9px;border-radius:999px}" +
      ".cref-pop .cr-meta{font-size:12.5px;color:#4d6457}" +
      ".cref-pop .cr-body{padding:9px 14px 12px}" +
      ".cref-pop .cr-body p{margin:0 0 6px}" +
      ".cref-pop .cr-why{color:#2b3a42}.cref-pop .cr-why b{color:#0e2a1f}" +
      ".cref-pop .cr-who{font-size:12.5px;color:#4d6457;margin:0}" +
      ".cref-pop .cr-hint{font-size:12px;color:#5d7468;margin:6px 0 0}" +
      "@media (prefers-reduced-motion: reduce){.cref-pop{transition:none;transform:none}}";
    var s = document.createElement("style"); s.textContent = css; document.head.appendChild(s);
  }

  function build(id) {
    var b = briefs && briefs[id];
    if (!b) return null;
    var p = el("div", "cref-pop"); p.id = "cref-pop"; p.setAttribute("role", "tooltip");
    var head = el("div", "cr-head");
    if (b.thumb) { var img = el("img", "cr-thumb"); img.src = base + b.thumb.replace(/^\//, ""); img.alt = ""; img.width = 52; img.height = 52; head.appendChild(img); }
    var ht = el("div"); ht.appendChild(el("p", "cr-kicker", id + " · " + b.topic)); ht.appendChild(el("p", "cr-title", b.title));
    head.appendChild(ht); p.appendChild(head);
    var v = el("div", "cr-verdict"), col = VERDICT[b.slug] || VERDICT.none, meta = [];
    function pillOf(text, bg, ink) { var x = el("span", "cr-pill", text); x.style.background = bg; x.style.color = ink; v.appendChild(x); }
    if (b.part) pillOf(b.rating || "Not rated", b.tone[0], b.tone[1]);                      // a part of a claim: the report's rating
    else if (b.verdict || !b.pledge) pillOf(b.verdict || "Not yet checked", col[0], col[1]);
    if (b.pledge) { pillOf("Pledge: " + b.pledge.status, b.pledge.colour, "#fff"); meta.push("as of " + b.pledge.as_of); }
    if (b.confidence) meta.push(b.confidence.toLowerCase() + " confidence");
    var stage = b.draft ? "draft, right of reply pending" : String(b.status || "").toLowerCase();
    if (stage && stage !== String(b.verdict || "Not yet checked").toLowerCase() && !b.part) meta.push(stage);
    if (b.parts) meta.push(b.parts + " parts");
    if (meta.length) v.appendChild(el("span", "cr-meta", meta.join(" · ")));
    p.appendChild(v);
    var body = el("div", "cr-body");
    body.appendChild(el("p", null, b.brief));
    if (b.why) { var w = el("p", "cr-why"); w.appendChild(el("b", null, "Evidence: ")); w.appendChild(document.createTextNode(b.why)); body.appendChild(w); }
    if (b.speaker) body.appendChild(el("p", "cr-who", b.speaker + (b.date ? " · " + ukDate(b.date) : "")));
    body.appendChild(el("p", "cr-hint", current && current.tagName === "A" ? "Open the link for the full check." : "Select it for more."));
    p.appendChild(body);
    p.addEventListener("pointerenter", function () { clearTimeout(hideTimer); });
    p.addEventListener("pointerleave", function () { scheduleHide(); });
    return p;
  }
  function place(p, a) {
    var r = a.getBoundingClientRect(), vw = document.documentElement.clientWidth, vh = window.innerHeight;
    var w = p.offsetWidth, h = p.offsetHeight, gap = 8;
    var left = Math.max(12, Math.min(r.left, vw - w - 12));
    var top = r.bottom + gap + h <= vh - 8 || r.top - gap - h < 8 ? r.bottom + gap : r.top - gap - h;
    p.style.left = left + "px"; p.style.top = Math.max(8, top) + "px";
  }
  function show(a) {
    var id = idOf(a);
    load().then(function () {
      if (current !== a) return;
      hide(true); current = a;
      pop = build(id); if (!pop) return;
      document.body.appendChild(pop); place(pop, a);
      a.setAttribute("aria-describedby", "cref-pop");
      requestAnimationFrame(function () { if (pop) pop.classList.add("on"); });
    });
  }
  function hide(keepCurrent) {
    clearTimeout(hideTimer);
    if (pop) { pop.remove(); pop = null; }
    document.querySelectorAll("[aria-describedby='cref-pop']").forEach(function (x) { x.removeAttribute("aria-describedby"); });
    if (!keepCurrent) current = null;
  }
  function scheduleHide() { clearTimeout(hideTimer); hideTimer = setTimeout(function () { hide(); }, HIDE_MS); }
  function want(a, ms) {
    clearTimeout(showTimer); clearTimeout(hideTimer);
    if (current === a && pop) return;
    current = a; load();
    showTimer = setTimeout(function () { if (current === a) show(a); }, ms);
  }

  document.addEventListener("pointerover", function (e) {
    if (e.pointerType === "touch") return;
    var a = refAt(e.target);
    if (a) want(a, SHOW_MS);
    else if (pop && pop.contains(e.target)) clearTimeout(hideTimer);
  });
  document.addEventListener("pointerout", function (e) {
    var a = refAt(e.target);
    if (!a || a.contains(e.relatedTarget)) return;
    clearTimeout(showTimer);
    if (pop && e.relatedTarget && pop.contains(e.relatedTarget)) return;
    scheduleHide();
  });
  document.addEventListener("focusin", function (e) {
    var a = refAt(e.target);
    if (a && a === e.target && a.matches(":focus-visible")) want(a, FOCUS_MS);
  });
  document.addEventListener("focusout", function (e) { if (refAt(e.target)) { clearTimeout(showTimer); hide(); } });
  document.addEventListener("keydown", function (e) { if (e.key === "Escape" && pop) { clearTimeout(showTimer); hide(); } });
  document.addEventListener("pointerdown", function (e) { if (pop && !pop.contains(e.target)) { clearTimeout(showTimer); hide(); } });
  window.addEventListener("scroll", function () { if (pop) hide(); }, { passive: true, capture: true });
  style();
})();
