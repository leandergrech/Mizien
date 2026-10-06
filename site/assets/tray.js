/* The pinned tray, shared by /explore/ (web and map) and /timeline/.
   A reader pins claims as they explore; the tray keeps them (in this browser, and in the address as ?pin=CC-001,CC-017
   so a selection can be shared), marks them in every view, and offers:
     - Show only pinned: the site-wide filter (assets/lens.js) narrowed to the pinned claims;
     - Find related: claims that share something with the pinned ones, each with its reasons (the same body, a
       theme linking them, similar wording with the shared words, the same pattern, place or topic, said within two
       months), strongest first;
     - Compare: keep the tray as A, pin a second set, and see the two side by side (verdicts, topics, bodies, places,
       dates).
   The tray never decides anything: every suggestion says why it is there.

   MizienTray.init({ mount, onChange }) · has(id) · toggle(id) · add(ids) · list() */
(function () {
  "use strict";
  var ROOT = (document.currentScript && document.currentScript.src || location.href).replace(/assets\/tray\.js.*$/, "");
  var pins = [], saved = null, data = null, byId = {}, themes = {}, bodies = {}, hooks = [], btn = null, pop = null, mode = "pins";
  var VERDICTS = ["Supported", "Largely supported", "Not substantiated", "Misleading", "Contradicted"];
  var VC = { "Supported": "#2e7d4f", "Largely supported": "#8db36b", "Not substantiated": "#d9772b", "Misleading": "#c85a3a", "Contradicted": "#8e2f25" };

  function esc(s) { return String(s == null ? "" : s).replace(/[&<>"']/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]; }); }
  function store() {
    try { localStorage.setItem("mizien.tray", JSON.stringify({ pins: pins, saved: saved })); } catch (e) {}
    var u = new URL(location.href);
    if (pins.length) u.searchParams.set("pin", pins.join(",")); else u.searchParams.delete("pin");
    history.replaceState(null, "", u);
  }
  function load() {
    try { var t = JSON.parse(localStorage.getItem("mizien.tray") || "null"); if (t) { pins = t.pins || []; saved = t.saved || null; } } catch (e) {}
    var q = new URLSearchParams(location.search).get("pin");
    if (q) pins = q.split(",").filter(function (x) { return /^CC-\d{3}$/.test(x); });   // a shared link wins
  }
  function changed() { store(); render(); hooks.forEach(function (f) { try { f(); } catch (e) {} }); }

  function loadData() {
    if (data) return Promise.resolve(data);
    return fetch(ROOT + "data/claims.json").then(function (r) { return r.json(); }).then(function (d) {
      data = d; d.claims.forEach(function (c) { byId[c.id] = c; });
      (d.themes || []).forEach(function (t) { themes[t.id] = t.name || t.id; });
      (d.bodies || []).forEach(function (b) { bodies[b.id] = b; });
      return d;
    });
  }
  function verdictOf(c) { return c.verdict || (c.pledge ? "Pledge: " + c.pledge.status : "Not yet checked"); }
  function colourOf(c) { return VC[c.verdict] || (c.pledge ? "#716f8d" : "#5d7468"); }
  function day(s) { var m = /^(\d{4})(?:-(\d{2}))?(?:-(\d{2}))?/.exec(String(s || "")); return m && m[2] ? Date.UTC(+m[1], +m[2] - 1, +(m[3] || 15)) : null; }

  // ---- related: every claim not pinned, scored by what it shares with the pinned ones, with the reasons
  function related() {
    var set = {}; pins.forEach(function (id) { set[id] = 1; });
    var P = pins.map(function (id) { return byId[id]; }).filter(Boolean), out = {};
    function add(id, w, why) { if (set[id] || !byId[id]) return; var o = out[id] || (out[id] = { id: id, score: 0, why: {} }); o.score += w; o.why[why] = 1; }
    (data.edges || []).forEach(function (e) {
      if (set[e.from]) add(e.to, 3, "linked to " + e.from + " by " + (themes[e.theme] || e.theme));
      if (set[e.to]) add(e.from, 3, "linked to " + e.to + " by " + (themes[e.theme] || e.theme));
    });
    data.claims.forEach(function (c) {
      if (set[c.id]) return;
      P.forEach(function (p) {
        (c.bodies || []).forEach(function (b) { if ((p.bodies || []).indexOf(b) >= 0) add(c.id, 3, "also said by " + (bodies[b] ? bodies[b].name : b)); });
        (c.tags || []).forEach(function (t) { if ((p.tags || []).indexOf(t) >= 0) add(c.id, 2, "same pattern: " + t); });
        if (c.location && p.location && c.location.place === p.location.place) add(c.id, 2, "same place: " + c.location.place);
        if (c.category === p.category) add(c.id, 1, "same topic: " + c.category);
        (p.similar || []).forEach(function (x) { if (x.id === c.id) add(c.id, x.score >= 0.4 ? 3 : 2, "similar wording to " + p.id + ": " + x.terms.join(", ")); });
        var a = day(c.date), b = day(p.date);
        if (a && b && Math.abs(a - b) <= 61 * 864e5) add(c.id, 1, "said within two months of " + p.id);
      });
    });
    return Object.keys(out).map(function (k) { return out[k]; }).sort(function (a, b) { return b.score - a.score || a.id.localeCompare(b.id); }).slice(0, 12);
  }
  // ---- compare: a summary of a set of claims
  function summary(ids) {
    var cs = ids.map(function (id) { return byId[id]; }).filter(Boolean), tally = function (f) { var n = {}; cs.forEach(function (c) { [].concat(f(c)).forEach(function (v) { if (v) n[v] = (n[v] || 0) + 1; }); });
      return Object.keys(n).sort(function (a, b) { return n[b] - n[a] || a.localeCompare(b); }).slice(0, 5).map(function (k) { return k + " (" + n[k] + ")"; }).join(", ") || "none"; };
    var ds = cs.map(function (c) { return String(c.date || "").slice(0, 4); }).filter(function (y) { return /^\d{4}$/.test(y); }).sort();
    var bar = cs.slice().sort(function (a, b) { var ia = VERDICTS.indexOf(a.verdict), ib = VERDICTS.indexOf(b.verdict); return (ia < 0 ? 9 : ia) - (ib < 0 ? 9 : ib); })
      .map(function (c) { return '<span style="background:' + colourOf(c) + '" title="' + esc(c.id + " · " + verdictOf(c)) + '"></span>'; }).join("");
    return '<p class="tr-n"><b>' + cs.length + "</b> claims · " + cs.filter(function (c) { return c.verdict || c.pledge; }).length + " checked</p>" +
      '<div class="tr-bar" role="img" aria-label="Verdicts: ' + esc(tally(verdictOf)) + '">' + bar + "</div>" +
      "<dl><dt>Verdicts</dt><dd>" + esc(tally(verdictOf)) + "</dd><dt>Topics</dt><dd>" + esc(tally(function (c) { return c.category; })) +
      "</dd><dt>Who said it</dt><dd>" + esc(tally(function (c) { return (c.bodies || []).map(function (b) { return bodies[b] ? bodies[b].name : b; }); })) +
      "</dd><dt>Places</dt><dd>" + esc(tally(function (c) { return c.location ? c.location.place : null; })) +
      "</dd><dt>Said</dt><dd>" + (ds.length ? esc(ds[0] === ds[ds.length - 1] ? ds[0] : ds[0] + " to " + ds[ds.length - 1]) : "dates not recorded") + "</dd></dl>";
  }

  // ---- the button and its panel
  function row(c, extra) {
    return '<li><span class="tr-dot" style="background:' + colourOf(c) + '"></span><a href="' + esc(ROOT + "claims/" + c.id + "/") + '"><b>' + esc(c.id) + "</b> " + esc(c.title) +
      '</a><span class="tr-v">' + esc(verdictOf(c)) + "</span>" + (extra || "") + "</li>";
  }
  function render() {
    if (!btn) return;
    btn.innerHTML = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M9 3h6l-1 6 4 4H6l4-4zM12 13v8"/></svg>Pinned' + (pins.length ? " <b>" + pins.length + "</b>" : "");
    btn.classList.toggle("is-on", pins.length > 0);
    if (pop.hidden) return;
    if (!data) { pop.innerHTML = '<p class="tr-h">Pinned claims</p><p class="tr-note">Loading…</p>'; return; }
    var Lens = window.MizienLens, onlyOn = Lens && Lens.only().length && Lens.only().join(",") === pins.join(",");
    var h = '<div class="tr-tabs" role="tablist">' + [["pins", "Pinned"], ["related", "Find related"], ["compare", "Compare"]].map(function (t) {
      return '<button type="button" role="tab" data-tab="' + t[0] + '" aria-selected="' + (mode === t[0]) + '">' + t[1] + "</button>"; }).join("") + "</div>";
    if (mode === "pins") {
      if (!pins.length) h += '<p class="tr-note">Nothing pinned yet. Open a claim, a group or a place and press <b>Pin</b>; pinned claims are marked in every view and kept in this browser.</p>';
      else {
        h += '<ul class="tr-list">' + pins.map(function (id) { var c = byId[id]; return c ? row(c, '<button type="button" class="tr-x" data-unpin="' + id + '" aria-label="Unpin ' + id + '">×</button>') : ""; }).join("") + "</ul>";
        h += '<p class="tr-acts"><button type="button" data-act="only" aria-pressed="' + !!onlyOn + '">' + (onlyOn ? "Show all claims" : "Show only pinned") + "</button>" +
          '<button type="button" data-act="share">Copy link</button><button type="button" data-act="clear">Clear</button></p>';
      }
    } else if (mode === "related") {
      if (!pins.length) h += '<p class="tr-note">Pin a claim first; related claims are found from what they share with it.</p>';
      else { var R = related();
        h += '<p class="tr-note">Claims that share something with the pinned ones, strongest first. Each says why it is here.</p>';
        h += R.length ? '<ul class="tr-list tr-rel">' + R.map(function (o) { return row(byId[o.id], '<button type="button" class="tr-add" data-pin="' + o.id + '" aria-label="Pin ' + o.id + '">Pin</button><span class="tr-why">' +
          esc(Object.keys(o.why).slice(0, 4).join(" · ")) + "</span>"); }).join("") + "</ul>" +
          '<p class="tr-acts"><button type="button" data-act="addall">Pin all ' + R.length + "</button></p>" : '<p class="tr-note">Nothing shares a body, theme, pattern, place or topic with the pinned claims.</p>';
      }
    } else {
      h += '<p class="tr-note">' + (saved ? "A is the set you kept; B is what is pinned now." : "Pin a set of claims, keep it as A, then pin another set to compare.") + "</p>";
      h += '<p class="tr-acts"><button type="button" data-act="keep"' + (pins.length ? "" : " disabled") + ">Keep the pinned claims as A</button>" +
        (saved ? '<button type="button" data-act="swap">Pin A again</button><button type="button" data-act="forget">Forget A</button>' : "") + "</p>";
      if (saved) h += '<div class="tr-cmp"><section><h3>A</h3>' + summary(saved) + "</section><section><h3>B · pinned now</h3>" + (pins.length ? summary(pins) : '<p class="tr-note">Nothing pinned.</p>') + "</section></div>";
    }
    pop.innerHTML = h;
  }
  function mount(el) {
    var wrap = document.createElement("div"); wrap.className = "tray";
    btn = document.createElement("button"); btn.type = "button"; btn.className = "tr-btn"; btn.setAttribute("aria-expanded", "false");
    pop = document.createElement("div"); pop.className = "tr-pop"; pop.hidden = true; pop.setAttribute("role", "dialog"); pop.setAttribute("aria-label", "Pinned claims");
    wrap.appendChild(btn); el.appendChild(wrap);
    (el.closest(".lens") || el).appendChild(pop);
    btn.addEventListener("click", function (e) { e.stopPropagation(); show(pop.hidden); });
    pop.addEventListener("click", function (e) {
      e.stopPropagation();
      var b = e.target.closest("button"); if (!b) return;
      if (b.dataset.tab) { mode = b.dataset.tab; render(); return; }
      if (b.dataset.unpin) { remove(b.dataset.unpin); return; }
      if (b.dataset.pin) { add([b.dataset.pin]); return; }
      var a = b.dataset.act, Lens = window.MizienLens;
      if (a === "only" && Lens) { var on = Lens.only().join(",") === pins.join(","); Lens.only(on ? [] : pins); render(); }
      else if (a === "share") { var u = location.href; (navigator.clipboard ? navigator.clipboard.writeText(u) : Promise.reject()).then(function () { b.textContent = "Link copied"; }, function () { prompt("Copy this link", u); }); }
      else if (a === "clear") { pins = []; changed(); }
      else if (a === "addall") add(related().map(function (o) { return o.id; }));
      else if (a === "keep") { saved = pins.slice(); pins = []; changed(); }
      else if (a === "swap") { var t = pins; pins = saved.slice(); saved = t.length ? t : saved; changed(); }
      else if (a === "forget") { saved = null; changed(); }
    });
    document.addEventListener("click", function (e) { if (!pop.hidden && e.target.isConnected && !e.target.closest(".tray") && !e.target.closest(".tr-pop")) show(false); });
    document.addEventListener("keydown", function (e) { if (e.key === "Escape" && !pop.hidden) { show(false); btn.focus(); } });
    render();
  }
  function show(on) { pop.hidden = !on; btn.setAttribute("aria-expanded", on ? "true" : "false"); if (on) loadData().then(render); render(); }
  function add(ids) { ids.forEach(function (id) { if (pins.indexOf(id) < 0) pins.push(id); }); changed(); }
  function remove(id) { pins = pins.filter(function (x) { return x !== id; }); changed(); }

  load();
  window.MizienTray = {
    init: function (o) { if (o.mount) mount(o.mount); if (o.onChange) hooks.push(o.onChange); },
    onChange: function (f) { hooks.push(f); },
    has: function (id) { return pins.indexOf(id) >= 0; },
    toggle: function (id) { if (pins.indexOf(id) >= 0) remove(id); else add([id]); },
    add: add, remove: remove, list: function () { return pins.slice(); }
  };
})();
