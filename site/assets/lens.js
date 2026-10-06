/* The site-wide filter ("lens") shared by the claims web, the Malta map and the timeline.
   A filter is a set of values per facet (topic, verdict, who said it, year, pattern) plus free text. Within a facet
   the values are alternatives (Water or Waste); across facets they all apply (Water, and Misleading). The filter is
   kept in the address (?topic=water&verdict=misleading,contradicted&q=bus), so it survives a reload, can be shared,
   and travels with the reader between the views.

   Each page calls MizienLens.init({ items, labels, mount, onChange }):
     items  [{ id, f: { topic: [key], verdict: [key], who: [key...], year: [key], pattern: [key...] }, text }]
     labels { facet: { key: "Display name" } } (keys are the short, address-safe values)
     mount  the element the bar is drawn into
   and asks MizienLens.match(item) which items to show. */
(function () {
  "use strict";
  var FACETS = [
    { key: "topic", label: "Topic" }, { key: "verdict", label: "Verdict" }, { key: "who", label: "Who said it" },
    { key: "year", label: "Year said" }, { key: "pattern", label: "Pattern" }
  ];
  var VERDICT_ORDER = ["supported", "largely-supported", "not-substantiated", "misleading", "contradicted"];
  var state = { q: "", only: [] }, items = [], labels = {}, onChange = null, bar = null, openFacet = null;
  FACETS.forEach(function (F) { state[F.key] = []; });

  function slug(s) { return String(s || "").normalize("NFD").replace(/[̀-ͯ]/g, "").toLowerCase().replace(/ħ/g, "h").replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, ""); }
  function plain(s) { return String(s || "").normalize("NFD").replace(/[̀-ͯ]/g, "").toLowerCase().replace(/ħ/g, "h"); }
  function esc(s) { return String(s).replace(/[&<>"']/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]; }); }

  function read() {
    var q = new URLSearchParams(location.search);
    FACETS.forEach(function (F) { var v = q.get(F.key); state[F.key] = v ? v.split(",").filter(Boolean) : []; });
    state.q = q.get("q") || "";
    state.only = (q.get("only") || "").split(",").filter(Boolean);   // "only these claims" (the pinned tray's Show only pinned)
  }
  function write() {
    var u = new URL(location.href);
    FACETS.forEach(function (F) { if (state[F.key].length) u.searchParams.set(F.key, state[F.key].join(",")); else u.searchParams.delete(F.key); });
    if (state.q.trim()) u.searchParams.set("q", state.q.trim()); else u.searchParams.delete("q");
    if (state.only.length) u.searchParams.set("only", state.only.join(",")); else u.searchParams.delete("only");
    history.replaceState(null, "", u);
  }
  // The filter part of the address, to carry into links to the other views.
  function query() {
    var p = new URLSearchParams();
    FACETS.forEach(function (F) { if (state[F.key].length) p.set(F.key, state[F.key].join(",")); });
    if (state.q.trim()) p.set("q", state.q.trim());
    if (state.only.length) p.set("only", state.only.join(","));
    return p.toString();
  }
  function active() { return !!state.q.trim() || state.only.length > 0 || FACETS.some(function (F) { return state[F.key].length; }); }

  // Does the item pass every facet (optionally ignoring one, for the counts shown next to that facet's values)?
  function match(it, except) {
    if (state.only.length && state.only.indexOf(it.id) < 0) return false;
    for (var i = 0; i < FACETS.length; i++) {
      var k = FACETS[i].key, want = state[k];
      if (k === except || !want.length) continue;
      var has = (it.f && it.f[k]) || [];
      if (!has.some(function (v) { return want.indexOf(v) >= 0; })) return false;
    }
    if (state.q.trim()) {
      var words = plain(state.q).split(/\s+/).filter(Boolean), t = it._t || (it._t = plain(it.text));
      if (!words.every(function (w) { return t.indexOf(w) >= 0; })) return false;
    }
    return true;
  }
  function count() { return items.filter(function (it) { return match(it); }).length; }
  function label(k, v) { return (labels[k] && labels[k][v]) || (k === "year" && v === "undated" ? "Undated" : v); }
  function values(k) {   // every value of a facet, with how many items it would show given the other facets
    var n = {}, all = {};
    items.forEach(function (it) { ((it.f && it.f[k]) || []).forEach(function (v) { all[v] = 1; if (match(it, k)) n[v] = (n[v] || 0) + 1; }); });
    var keys = Object.keys(all);
    if (k === "verdict") keys.sort(function (a, b) { var ia = VERDICT_ORDER.indexOf(a), ib = VERDICT_ORDER.indexOf(b);
      return (ia < 0 ? (a === "none" ? 99 : 50) : ia) - (ib < 0 ? (b === "none" ? 99 : 50) : ib) || a.localeCompare(b); });
    else if (k === "year") keys.sort(function (a, b) { return a === "undated" ? 1 : b === "undated" ? -1 : b.localeCompare(a); });
    else keys.sort(function (a, b) { return (all[b] && n[b] || 0) - (n[a] || 0) || label(k, a).localeCompare(label(k, b)); });
    return keys.map(function (v) { return { v: v, n: n[v] || 0, on: state[k].indexOf(v) >= 0 }; });
  }

  function changed() { write(); render(); if (onChange) onChange(); }
  function toggle(k, v) { var a = state[k], i = a.indexOf(v); if (i >= 0) a.splice(i, 1); else a.push(v); changed(); }
  function clear() { FACETS.forEach(function (F) { state[F.key] = []; }); state.q = ""; state.only = []; changed(); }

  // ---- the bar: search, one button per facet (opening a list with counts), the active filters as chips, the total
  function render() {
    if (!bar) return;
    var n = count(), chips = [];
    FACETS.forEach(function (F) { state[F.key].forEach(function (v) { chips.push({ k: F.key, v: v }); }); });
    var facetBtns = FACETS.map(function (F) {
      var on = state[F.key].length;
      return '<button type="button" class="lens-f' + (on ? " is-on" : "") + (openFacet === F.key ? " is-open" : "") + '" data-facet="' + F.key +
        '" aria-expanded="' + (openFacet === F.key ? "true" : "false") + '">' + esc(F.label) + (on ? ' <b>' + on + "</b>" : "") + ' <span aria-hidden="true">▾</span></button>';
    }).join("");
    bar.querySelector(".lens-facets").innerHTML = facetBtns;
    var onlyChip = state.only.length ? '<button type="button" class="lens-chip lens-only" aria-label="Show all claims again, not only the pinned ones">Only the ' +
      state.only.length + " pinned <span aria-hidden=\"true\">×</span></button>" : "";
    bar.querySelector(".lens-chips").innerHTML = onlyChip + chips.map(function (c) {
      return '<button type="button" class="lens-chip" data-k="' + c.k + '" data-v="' + esc(c.v) + '" aria-label="Remove filter ' + esc(label(c.k, c.v)) + '">' +
        esc(label(c.k, c.v)) + ' <span aria-hidden="true">×</span></button>'; }).join("");
    bar.querySelector(".lens-chips").hidden = !chips.length && !state.only.length;
    var cnt = bar.querySelector(".lens-count");
    cnt.innerHTML = active() ? "<b>" + n + "</b> of " + items.length + " claims" : "<b>" + items.length + "</b> claims";
    bar.querySelector(".lens-clear").hidden = !active();
    bar.classList.toggle("is-active", active());
    var pop = bar.querySelector(".lens-pop");
    if (!openFacet) { pop.hidden = true; return; }
    var F = FACETS.filter(function (x) { return x.key === openFacet; })[0];
    pop.hidden = false;
    pop.innerHTML = '<p class="lens-pop-h">' + esc(F.label) + '<span>Choose any; the numbers count claims that also pass the other filters.</span></p><ul>' +
      values(openFacet).map(function (o) {
        return '<li><label class="' + (o.n || o.on ? "" : "is-zero") + '"><input type="checkbox" data-k="' + openFacet + '" value="' + esc(o.v) + '"' + (o.on ? " checked" : "") + "> " +
          '<span class="lv">' + esc(label(openFacet, o.v)) + '</span><span class="ln">' + o.n + "</span></label></li>"; }).join("") + "</ul>" +
      '<p class="lens-pop-f"><button type="button" class="lens-done">Done</button></p>';
  }
  function mount(el) {
    bar = el; bar.classList.add("lens");
    bar.innerHTML = '<div class="lens-row"><label class="lens-q"><span class="visually-hidden">Search the claims</span>' +
      '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M10.5 4a6.5 6.5 0 1 0 0 13a6.5 6.5 0 1 0 0-13M15.5 15.5 20 20"/></svg>' +
      '<input type="search" placeholder="Search claims, speakers, places" autocomplete="off" spellcheck="false"></label>' +
      '<div class="lens-facets" role="group" aria-label="Filter the claims"></div><div class="lens-extra"></div>' +
      '<p class="lens-count" aria-live="polite"></p><button type="button" class="lens-clear" hidden>Clear filters</button></div>' +
      '<div class="lens-chips" hidden></div><div class="lens-pop" role="group" aria-label="Filter values" hidden></div>';
    var input = bar.querySelector(".lens-q input"), t = 0;
    input.value = state.q;
    input.addEventListener("input", function () { clearTimeout(t); t = setTimeout(function () { state.q = input.value; changed(); }, 180); });
    bar.addEventListener("click", function (e) {
      var b = e.target.closest("button"); if (!b) return;
      if (b.dataset.facet) { openFacet = openFacet === b.dataset.facet ? null : b.dataset.facet; render(); }
      else if (b.classList.contains("lens-only")) { state.only = []; changed(); }
      else if (b.classList.contains("lens-chip")) toggle(b.dataset.k, b.dataset.v);
      else if (b.classList.contains("lens-clear")) { input.value = ""; openFacet = null; clear(); }
      else if (b.classList.contains("lens-done")) { var f = openFacet; openFacet = null; render(); var fb = bar.querySelector('[data-facet="' + f + '"]'); if (fb) fb.focus(); }
    });
    bar.addEventListener("change", function (e) { var c = e.target; if (c.type === "checkbox" && c.dataset.k) { toggle(c.dataset.k, c.value);
      var again = bar.querySelector('.lens-pop input[value="' + CSS.escape(c.value) + '"]'); if (again) again.focus(); } });
    document.addEventListener("click", function (e) {   // a click outside the bar closes the list (a redrawn button is no longer in the page)
      if (openFacet && e.target.isConnected && !e.target.closest(".lens")) { openFacet = null; render(); } });
    document.addEventListener("keydown", function (e) { if (e.key === "Escape" && openFacet) { var f = openFacet; openFacet = null; render();
      var fb = bar.querySelector('[data-facet="' + f + '"]'); if (fb) fb.focus(); } });
    render();
  }

  window.MizienLens = {
    slug: slug,
    init: function (o) { read(); items = o.items || []; labels = o.labels || {}; onChange = o.onChange || null; if (o.mount) mount(o.mount); },
    match: function (it) { return match(it); },
    only: function (ids) { if (ids === undefined) return state.only.slice(); state.only = (ids || []).slice(); changed(); },
    active: active, query: query, count: count,
    refresh: render
  };
})();
