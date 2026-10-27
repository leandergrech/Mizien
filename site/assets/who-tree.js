/* Who said it (site/bodies/index.njk): the register tree on the left, the selected body in the panel on the right.
   The tree and every strip are built at build time; this script only selects, searches and fills the panel from the
   JSON in #who-data (site/_lib/who.js, whoPanel). Without it, each name is a link to the body's own page.
   URL state, as in Explore: ?sel=<body id> selects a body, ?q=<text> searches. Pinning uses assets/tray.js. */
(function () {
  "use strict";
  var dataEl = document.getElementById("who-data"), tree = document.getElementById("who-tree"), panel = document.getElementById("who-panel");
  var empty = document.getElementById("wp-empty"), bodyEl = document.getElementById("wp-body"), q = document.getElementById("who-q");
  if (!dataEl || !tree || !panel) return;
  var DATA; try { DATA = JSON.parse(dataEl.textContent); } catch (e) { return; }
  var prefix = (function () { var a = tree.querySelector("a.wt-name[data-id]"); return a ? a.getAttribute("href").replace(/bodies\/[^/]+\/$/, "") : "/"; })();
  var ICON = { links: "M6 8a2 2 0 1 0 0-4a2 2 0 1 0 0 4M18 9a2 2 0 1 0 0-4a2 2 0 1 0 0 4M12 20a2 2 0 1 0 0-4a2 2 0 1 0 0 4M7 7.6l4 8.6M17 8.6l-4 7.6M8 6.1l8 .8",
    clock: "M12 3a9 9 0 1 0 0 18a9 9 0 1 0 0-18M12 7v5l3.5 2", feed: "M5 5a14 14 0 0 1 14 14M5 11a8 8 0 0 1 8 8M6 19a1 1 0 1 0 0-.01",
    report: "M7 3h7l5 5v13H7zM14 3v5h5M10 12h6M10 16h6", map: "M3 6.5 9 4l6 2.5L21 4v13.5L15 20l-6-2.5L3 20zM9 4v13.5M15 6.5V20" };
  function esc(s) { return String(s == null ? "" : s).replace(/[&<>"']/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]; }); }
  function icon(n) { return '<svg class="ico" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="' + ICON[n] + '"/></svg>'; }
  function ukDate(v) {
    var m = /^(\d{4})(?:-(\d{2}))?(?:-(\d{2}))?$/.exec(String(v || "")); if (!m) return v || "";
    var M = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
    return (m[3] ? Number(m[3]) + " " : "") + (m[2] ? M[Number(m[2]) - 1] + " " : "") + m[1];
  }
  var selected = null, tray = null;

  // ---- the panel
  function render(b) {
    var h = [];
    var glyph = (tree.querySelector('.wt-item[data-id="' + b.id + '"] .wt-frame') || {}).innerHTML || "";
    var kindEl = tree.querySelector('.wt-kind[data-type="' + b.type + '"]'), kind = kindEl ? kindEl.style.getPropertyValue("--kind") : "";
    h.push('<div class="wp-head" style="--kind: ' + esc(kind || "var(--sage)") + '">');
    h.push('<button type="button" class="wp-close" aria-label="Close">×</button>');
    h.push('<span class="wp-frame' + (b.kind === "person" ? " is-person" : "") + '" aria-hidden="true">' + glyph + "</span>");
    h.push('<div class="wp-title"><p class="wp-kicker">' + (b.kind === "person" ? "Person · " : "") + esc(b.type_label) + "</p>");
    h.push("<h2>" + esc(b.name) + "</h2>");
    var sub = [];
    if (b.role) sub.push(esc(b.role));
    if (b.parent) sub.push((b.kind === "person" ? "speaking for " : "part of ") + '<a href="' + esc(b.parent.path) + '" data-id="' + esc(b.parent.id) + '">' + esc(b.parent.name) + "</a>");
    if (sub.length) h.push('<p class="wp-sub">' + sub.join(", ") + "</p>");
    if (b.note) h.push('<p class="wp-note small">' + esc(b.note) + "</p>");
    h.push("</div></div>");
    // the strip, the same as the build-time one (site/_includes/who-meter.njk)
    h.push('<div class="wp-sum"><p class="wp-counts"><b>' + b.total + "</b> claim" + (b.total === 1 ? "" : "s") + " · <b>" + b.checked + "</b> checked" +
      (b.people.length ? " · <b>" + b.people.length + "</b> " + (b.people.length === 1 ? "person" : "people") : "") +
      (b.offices.length ? " · <b>" + b.offices.length + "</b> office" + (b.offices.length === 1 ? "" : "s") : "") + "</p>");
    var sq = [];
    b.counts.forEach(function (v) { for (var i = 0; i < v.n; i++) sq.push('<i class="v-' + v.slug + '" title="' + esc(v.name) + '"></i>'); });
    for (var i = 0; i < b.waiting; i++) sq.push('<i class="is-open" title="Not yet checked"></i>');
    h.push('<div class="wm"><div class="wm-strip" role="img" aria-label="' + (b.checked ? "Verdicts on " + b.checked + " of " + b.total + " claims" : b.total + " claims, none checked yet") + '">' + sq.join("") + "</div>");
    h.push('<p class="wm-key">' + b.counts.map(function (v) { return '<span><i class="v-' + v.slug + '"></i>' + esc(v.name) + " <b>" + v.n + "</b></span>"; }).join("") +
      (b.waiting ? '<span><i class="is-open"></i>not yet checked <b>' + b.waiting + "</b></span>" : "") +
      (b.few ? '<span class="wm-few">' + (b.checked ? b.checked + " of " + b.fewMin + " checks: too few to summarise" : "no checks yet") + "</span>" : "") + "</p></div>");
    if (b.kind === "person") h.push('<p class="small">Checks of claims by ' + esc(b.name) + (b.parent ? " count towards " + esc(b.parent.name) + ", the body they spoke for" : "") + ": Miżien summarises bodies, not people.</p>");
    if (b.pledges.length) h.push('<p class="wm-pledges">' + b.pledges.map(function (p) {
      return '<a class="pl-chip' + (p.kind === "target" ? " is-target" : "") + '" href="' + esc(p.path) + '" style="--pl: ' + esc(p.colour) + "; --pl-ink: " + esc(p.ink) + '" title="' + esc(p.id + " " + p.title + ": " + p.status + ", as of " + p.as_of) + '">' + (p.kind === "target" ? "Target: " : "Pledge: ") + esc(p.status) + " <span>" + esc(p.id) + "</span></a>";
    }).join("") + "</p>");
    h.push("</div>");
    // tools
    h.push('<nav class="who-tools wp-tools" aria-label="' + esc(b.name) + ' in the other views">');
    h.push('<a class="wp-open" href="' + esc(b.path) + '">' + icon("report") + "<span>Open page</span></a>");
    h.push('<a href="' + prefix + "explore/?group=speaker&sel=body:" + esc(b.id) + '">' + icon("links") + "<span>In the claims web</span></a>");
    h.push('<a href="' + prefix + "timeline/?who=" + esc(b.type) + "&lanes=verdict" + '">' + icon("clock") + "<span>On the timeline</span></a>");
    h.push('<button type="button" class="who-pin" data-ids="' + b.claims.map(function (c) { return c.id; }).join(",") + '" hidden>Pin all ' + b.total + " claims</button>");
    h.push('<span class="who-tray" id="who-tray"></span>');
    h.push('<a href="' + esc(b.path) + 'feed.xml">' + icon("feed") + "<span>Feed</span></a>");
    h.push("</nav>");
    // people and offices
    if (b.offices.length || b.people.length) {
      h.push('<p class="wp-under small">Also counted here: ' + b.offices.concat(b.people).map(function (x) {
        return '<a href="' + esc(x.path) + '" data-id="' + esc(x.id) + '">' + esc(x.name) + "</a>" + (x.role ? ' <span class="wt-role">' + esc(x.role) + "</span>" : "");
      }).join(", ") + ".</p>");
    }
    // claims, newest first
    h.push('<h3 class="wp-h">Claims</h3><ul class="wp-claims">');
    b.claims.forEach(function (c) {
      h.push('<li><a class="wp-claim v-' + esc(c.slug || "none") + '" href="' + esc(c.path) + '" data-claim="' + esc(c.id) + '"><span class="cref-dot" aria-hidden="true"></span><span class="wp-cid">' + esc(c.id) + "</span> " + esc(c.title) + "</a>");
      h.push('<span class="wp-cmeta">' + (c.label ? '<span class="badge v-' + esc(c.slug) + '">' + (c.kind === "pledge" ? "Pledge: " : "") + esc(c.label) + "</span>" + (c.status !== "Published" ? ' <span class="small">draft</span>' : "") : '<span class="small">not yet checked</span>') +
        (c.date ? ' <span class="small">· ' + esc(ukDate(c.date)) + "</span>" : "") + ' <span class="small">· ' + esc(c.category) + "</span>" +
        (c.by.length ? ' <span class="small">· with ' + c.by.map(esc).join(", ") + "</span>" : "") + "</span></li>");
    });
    h.push("</ul>");
    return h.join("");
  }
  function pinInit() {
    var T = window.MizienTray, btn = bodyEl.querySelector(".who-pin"), mount = document.getElementById("who-tray");
    if (!T || !btn || !mount) return;
    var ids = btn.dataset.ids.split(",").filter(Boolean);
    function sync() { var all = ids.every(function (id) { return T.has(id); }); btn.textContent = (all ? "Unpin these " : "Pin all ") + ids.length + " claims"; btn.setAttribute("aria-pressed", all ? "true" : "false"); }
    btn.addEventListener("click", function () { if (ids.every(function (id) { return T.has(id); })) ids.forEach(function (id) { T.remove(id); }); else T.add(ids); });
    if (!tray) { T.init({ mount: mount, url: false, onChange: function () { var b2 = bodyEl.querySelector(".who-pin"); if (b2 === btn) sync(); } }); tray = T; } else T.init({ mount: mount, url: false, onChange: function () { var b2 = bodyEl.querySelector(".who-pin"); if (b2 === btn) sync(); } });
    btn.hidden = false; sync();
  }
  function select(id, push, focus) {
    var b = DATA[id]; if (!b) return;
    selected = id;
    tree.querySelectorAll(".wt-row.is-selected").forEach(function (r) { r.classList.remove("is-selected"); r.removeAttribute("aria-current"); });
    var item = tree.querySelector('.wt-item[data-id="' + id + '"]');
    if (item) {
      var row = item.querySelector(".wt-row"); row.classList.add("is-selected"); row.setAttribute("aria-current", "true");
      var d = item.parentElement; while (d && d !== tree) { if (d.tagName === "DETAILS") d.open = true; d = d.parentElement; }
      if (!item.hidden) row.scrollIntoView({ block: "nearest" });
    }
    bodyEl.innerHTML = render(b); bodyEl.hidden = false; empty.hidden = true;
    panel.classList.add("is-open"); document.getElementById("who-stage").classList.add("panel-open");
    pinInit();
    if (push) { var u = new URL(location.href); u.searchParams.set("sel", id); history.pushState({ sel: id }, "", u); }
    if (focus) { var hd = bodyEl.querySelector("h2"); if (hd) { hd.tabIndex = -1; hd.focus({ preventScroll: true }); } }
    document.title = b.name + " · Who said it · Miżien";
  }
  function clear(push) {
    selected = null; bodyEl.hidden = true; bodyEl.innerHTML = ""; empty.hidden = false;
    panel.classList.remove("is-open"); document.getElementById("who-stage").classList.remove("panel-open");
    tree.querySelectorAll(".wt-row.is-selected").forEach(function (r) { r.classList.remove("is-selected"); r.removeAttribute("aria-current"); });
    if (push) { var u = new URL(location.href); u.searchParams.delete("sel"); history.pushState({}, "", u); }
    document.title = "Who said it · Miżien";
  }
  // a click on a name in the tree or on a body link in the panel selects it; everything else keeps its link
  document.addEventListener("click", function (e) {
    var a = e.target.closest("a[data-id]"); if (a && (tree.contains(a) || panel.contains(a)) && !e.metaKey && !e.ctrlKey && !e.shiftKey && e.button === 0) { e.preventDefault(); select(a.dataset.id, true, panel.contains(a)); return; }
    if (e.target.closest(".wp-close")) clear(true);
  });
  // a summary row: clicking the row (not the name) toggles the branch as usual; Enter on the name follows the link handler above
  addEventListener("popstate", function () { var id = new URL(location.href).searchParams.get("sel"); if (id && DATA[id]) select(id, false); else clear(false); });

  // ---- search: filter rows by name, alias or role; matches are shown with their ancestors, branches opened
  if (q) {
    q.hidden = false;
    var items = Array.prototype.slice.call(tree.querySelectorAll(".wt-item")), kinds = Array.prototype.slice.call(tree.querySelectorAll(".wt-kind"));
    var norm = function (s) { return String(s || "").toLowerCase().replace(/[’']/g, "'").replace(/\s+/g, " ").trim(); };
    var state = null;
    function apply(text) {
      var t = norm(text);
      if (!t) {
        items.forEach(function (it) { it.hidden = false; it.classList.remove("is-hit"); });
        kinds.forEach(function (k) { k.hidden = false; });
        if (state) { state.forEach(function (s) { s.el.open = s.open; }); state = null; }
        return;
      }
      if (!state) state = Array.prototype.map.call(tree.querySelectorAll("details"), function (d) { return { el: d, open: d.open }; });
      items.forEach(function (it) { it.hidden = true; it.classList.remove("is-hit"); });
      var hits = items.filter(function (it) { return norm(it.dataset.search).indexOf(t) >= 0; });
      hits.forEach(function (it) {
        it.classList.add("is-hit");
        var p = it; while (p && p !== tree) { if (p.classList && p.classList.contains("wt-item")) p.hidden = false; if (p.tagName === "DETAILS") p.open = true; p = p.parentElement; }
        it.querySelectorAll(".wt-item").forEach(function (c) { c.hidden = false; });
      });
      kinds.forEach(function (k) { k.hidden = !k.querySelector(".wt-item:not([hidden])"); });
    }
    var timer;
    q.addEventListener("input", function () { clearTimeout(timer); timer = setTimeout(function () { apply(q.value); var u = new URL(location.href); if (q.value) u.searchParams.set("q", q.value); else u.searchParams.delete("q"); history.replaceState(history.state, "", u); }, 80); });
    q.addEventListener("keydown", function (e) { if (e.key === "Escape") { q.value = ""; apply(""); } if (e.key === "Enter") { var first = tree.querySelector(".wt-item.is-hit a[data-id]"); if (first) select(first.dataset.id, true, true); } });
    var q0 = new URL(location.href).searchParams.get("q"); if (q0) { q.value = q0; apply(q0); }
  }
  // the hash and ?sel= forms both select
  var sel0 = new URL(location.href).searchParams.get("sel") || (location.hash && location.hash.slice(1));
  if (sel0 && DATA[sel0]) select(sel0, false);
  // a selected body's branch: when a person or office is selected, open the parent so the row is visible
  document.documentElement.classList.add("who-js");
})();
