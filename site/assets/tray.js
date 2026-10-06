/* The pinned tray, shared by /explore/ (web and map) and /timeline/.
   A reader pins claims as they explore; the tray keeps them (in this browser, and in the address as ?pin=CC-001,CC-017
   so a selection can be shared), marks them in every view, and offers:
     - In common: what the pinned claims share (verdict, body, kind of body, topic, pattern, place, year, pledges, and
       the theme links and similar wording between them), each counted ("4 of 6") with a link to every claim like it;
     - Save this set: named sets kept in this browser, to pin again later (Copy link shares the set itself);
     - Show only pinned: the site-wide filter (assets/lens.js) narrowed to the pinned claims;
     - Find related: claims that share something with the pinned ones, each with its reasons (the same body, a
       theme linking them, similar wording with the shared words, the same pattern, place or topic, said within two
       months), strongest first;
     - Compare: keep the tray as A, pin a second set, and see the two side by side (verdicts, topics, bodies, places,
       dates).
   The tray never decides anything: every suggestion says why it is there.

   Claim pages have a "Pin this claim" button and the same tray (init with url: false: the address is left alone, and
   "Show only pinned" becomes links to Explore and the timeline).

   MizienTray.init({ mount, onChange, url }) · has(id) · toggle(id) · add(ids) · list() */
(function () {
  "use strict";
  var ROOT = (document.currentScript && document.currentScript.src || location.href).replace(/assets\/tray\.js.*$/, "");
  var keepUrl = true, sets = [], pins = [], saved = null, data = null, byId = {}, themes = {}, bodies = {}, types = {}, hooks = [], btn = null, pop = null, mode = "pins";
  var VERDICTS = ["Supported", "Largely supported", "Not substantiated", "Misleading", "Contradicted"];
  var VC = { "Supported": "#2e7d4f", "Largely supported": "#8db36b", "Not substantiated": "#d9772b", "Misleading": "#c85a3a", "Contradicted": "#8e2f25" };

  function esc(s) { return String(s == null ? "" : s).replace(/[&<>"']/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]; }); }
  function store() {
    try { localStorage.setItem("mizien.tray", JSON.stringify({ pins: pins, saved: saved, sets: sets })); } catch (e) {}
    if (!keepUrl) return;   // claim pages keep their own address
    var u = new URL(location.href);
    if (pins.length) u.searchParams.set("pin", pins.join(",")); else u.searchParams.delete("pin");
    history.replaceState(null, "", u);
  }
  function load() {
    try { var t = JSON.parse(localStorage.getItem("mizien.tray") || "null"); if (t) { pins = t.pins || []; saved = t.saved || null; sets = t.sets || []; } } catch (e) {}
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
      (d.body_types || []).forEach(function (t) { types[t.id] = t.label; });
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
  // ---- in common: what the pinned claims share, counted from the record, each with a way to see every claim like it
  function slug(x) { return String(x || "").normalize("NFD").replace(/[\u0300-\u036f]/g, "").toLowerCase().replace(/ħ/g, "h").replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, ""); }
  function common() {
    var cs = pins.map(function (id) { return byId[id]; }).filter(Boolean), n = cs.length, rows = [], set = {};
    cs.forEach(function (c) { set[c.id] = 1; });
    function tally(label, f, link) {
      var k = {}, names = {};
      cs.forEach(function (c) { var seen = {}; [].concat(f(c)).forEach(function (v) { if (!v || seen[v[0]]) return; seen[v[0]] = 1; k[v[0]] = (k[v[0]] || []).concat(c.id); names[v[0]] = v[1]; }); });
      Object.keys(k).forEach(function (key) { if (k[key].length >= 2) rows.push({ n: k[key].length, what: label, name: names[key], ids: k[key], href: link ? link(key) : null }); });
    }
    var X = ROOT + "explore/?";
    tally("verdict", function (c) { var v = verdictOf(c); return [[c.verdict || c.pledge ? slug(v) : "none", v]]; }, function (k) { return X + "view=ghanqbuta&verdict=" + k; });
    tally("said by", function (c) { return (c.bodies || []).map(function (b) { return [b, bodies[b] ? bodies[b].name : b]; }); }, function (k) { return ROOT + "bodies/" + k + "/"; });
    tally("kind of body", function (c) { return (c.bodies || []).map(function (b) { var t = bodies[b] && bodies[b].type; return t ? [t, types[t] || t] : null; }); }, function (k) { return X + "view=ghanqbuta&group=speaker&who=" + k; });
    tally("topic", function (c) { return [[slug(c.category), c.category]]; }, function (k) { return X + "view=ghanqbuta&topic=" + k; });
    tally("pattern", function (c) { return (c.tags || []).map(function (t) { return [slug(t), t]; }); }, function (k) { return X + "view=ghanqbuta&group=pattern&pattern=" + k; });
    tally("place", function (c) { return c.location ? [[c.location.place, c.location.place]] : []; }, null);
    tally("year said", function (c) { var y = /^\d{4}/.exec(String(c.date || "")); return y ? [[y[0], y[0]]] : []; }, function (k) { return ROOT + "timeline/?year=" + k; });
    tally("kind of claim", function (c) { return c.pledge ? [["pledge", "a pledge"]] : []; }, null);
    rows.sort(function (a, b) { return b.n - a.n || a.what.localeCompare(b.what); });
    var links = [];
    (data.edges || []).forEach(function (e) { if (set[e.from] && set[e.to]) links.push({ a: e.from, b: e.to, why: "linked by " + (themes[e.theme] || e.theme) }); });
    cs.forEach(function (c) { (c.similar || []).forEach(function (x) { if (set[x.id] && c.id < x.id) links.push({ a: c.id, b: x.id, why: "similar wording: " + x.terms.join(", ") }); }); });
    return { n: n, rows: rows, links: links };
  }
  function commonHtml() {
    if (pins.length < 2) return '<p class="tr-note">Pin two or more claims to see what they have in common.</p>';
    var C = common(), h = '<p class="tr-note">What the ' + C.n + ' pinned claims share, counted from the record. A shared feature is a lead to look into, not a finding.</p>';
    if (!C.rows.length && !C.links.length) return h + '<p class="tr-note">No verdict, body, topic, pattern, place or year is shared by two or more of them.</p>';
    h += '<ul class="tr-common">' + C.rows.map(function (r) {
      return '<li><span class="tr-share" style="--k:' + (r.n / C.n).toFixed(2) + '"><b>' + r.n + "</b> of " + C.n + "</span><span>" + esc(r.what) + ": <b>" + esc(r.name) + "</b>" +
        '<span class="tr-ids">' + esc(r.ids.join(", ")) + "</span></span>" + (r.href ? '<a class="tr-see" href="' + esc(r.href) + '">See all</a>' : "<span></span>") + "</li>"; }).join("") + "</ul>";
    if (C.links.length) h += '<p class="tr-h2">Links between them</p><ul class="tr-common tr-pairs">' + C.links.map(function (l) {
      return "<li><span><b>" + esc(l.a) + "</b> and <b>" + esc(l.b) + "</b></span><span>" + esc(l.why) + "</span></li>"; }).join("") + "</ul>";
    return h;
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
    var openIn = ROOT + "explore/?pin=" + pins.join(",") + "&only=" + pins.join(",");
    var h = '<div class="tr-tabs" role="tablist">' + [["pins", "Pinned"], ["common", "In common"], ["related", "Find related"], ["compare", "Compare"]].map(function (t) {
      return '<button type="button" role="tab" data-tab="' + t[0] + '" aria-selected="' + (mode === t[0]) + '">' + t[1] + "</button>"; }).join("") + "</div>";
    if (mode === "pins") {
      if (!pins.length) h += '<p class="tr-note">Nothing pinned yet. Open a claim, a group or a place and press <b>Pin</b>; pinned claims are marked in every view and kept in this browser.</p>';
      else {
        h += '<ul class="tr-list">' + pins.map(function (id) { var c = byId[id]; return c ? row(c, '<button type="button" class="tr-x" data-unpin="' + id + '" aria-label="Unpin ' + id + '">×</button>') : ""; }).join("") + "</ul>";
        h += '<p class="tr-acts">' + (Lens ? '<button type="button" data-act="only" aria-pressed="' + !!onlyOn + '">' + (onlyOn ? "Show all claims" : "Show only pinned") + "</button>"
          : '<a class="tr-open" href="' + esc(openIn) + '">Open in Explore</a><a class="tr-open" href="' + esc(ROOT + "timeline/?pin=" + pins.join(",") + "&only=" + pins.join(",")) + '">On the timeline</a>') +
          '<button type="button" data-act="share">Copy link</button><button type="button" data-act="save">Save this set</button><button type="button" data-act="clear">Clear</button></p>';
      }
      if (sets.length) h += '<p class="tr-h2">Saved sets</p><ul class="tr-list tr-sets">' + sets.map(function (st, i) {
        return '<li><span class="tr-dot"></span><button type="button" class="tr-load" data-load="' + i + '"><b>' + esc(st.name) + "</b> · " + st.pins.length + " claims</button>" +
          '<span class="tr-v">' + esc(st.date || "") + '</span><button type="button" class="tr-x" data-drop="' + i + '" aria-label="Delete the set ' + esc(st.name) + '">×</button></li>'; }).join("") + "</ul>";
    } else if (mode === "common") {
      h += commonHtml();
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
      if (b.dataset.load) { var st = sets[+b.dataset.load]; if (st) { pins = st.pins.slice(); changed(); } return; }
      if (b.dataset.drop) { sets.splice(+b.dataset.drop, 1); changed(); return; }
      var a = b.dataset.act, Lens = window.MizienLens;
      if (a === "only" && Lens) { var on = Lens.only().join(",") === pins.join(","); Lens.only(on ? [] : pins); render(); }
      else if (a === "share") { var u = keepUrl ? location.href : new URL(ROOT + "explore/?pin=" + pins.join(","), location.href).href; (navigator.clipboard ? navigator.clipboard.writeText(u) : Promise.reject()).then(function () { b.textContent = "Link copied"; }, function () { prompt("Copy this link", u); }); }
      else if (a === "clear") { pins = []; changed(); }
      else if (a === "save") { var nm = prompt("A name for this set of " + pins.length + " claims (kept in this browser)", "Set " + (sets.length + 1));
        if (nm && nm.trim()) { sets = sets.filter(function (x) { return x.name !== nm.trim(); }); sets.unshift({ name: nm.trim().slice(0, 60), pins: pins.slice(), date: new Date().toLocaleDateString("en-GB", { day: "numeric", month: "short", year: "numeric" }) }); changed(); } }
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
    init: function (o) { if (o.url === false) keepUrl = false; if (o.mount) mount(o.mount); if (o.onChange) hooks.push(o.onChange); },
    onChange: function (f) { hooks.push(f); },
    has: function (id) { return pins.indexOf(id) >= 0; },
    toggle: function (id) { if (pins.indexOf(id) >= 0) remove(id); else add([id]); },
    add: add, remove: remove, list: function () { return pins.slice(); }
  };
})();
