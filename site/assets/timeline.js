/* Timeline of claims on a straight line of calendar days (site/timeline.njk).
   Claims are clumped by month, week, day or hour depending on the zoom, and a claim is never placed more finely than
   its recorded date allows: a claim dated only to a month or a year is drawn as a dashed bar across that period.
   All dates are handled as UTC calendar dates, so no daylight-saving or time-zone shift can move a claim. */
(function () {
  "use strict";
  var root = document.getElementById("tl");
  var dataEl = document.getElementById("tl-data");
  if (!root || !dataEl) return;

  var DAY = 86400000, HOUR = 3600000;
  var MON = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
  var MONL = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
  var DOW = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];
  var LEVELS = [
    { name: "year", rank: 0, from: 0, ppd: 0.5, noun: "year" },
    { name: "month", rank: 1, from: 1.2, ppd: 4, noun: "month" },
    { name: "week", rank: 2, from: 10, ppd: 28, noun: "week" },
    { name: "day", rank: 3, from: 70, ppd: 200, noun: "day" },
    { name: "hour", rank: 4, from: 800, ppd: 1600, noun: "hour" }
  ];
  var MIN_PPD = 0.12, MAX_PPD = 4800;

  var stage = document.getElementById("tl-stage");
  var panel = document.getElementById("tl-panel");
  var over = document.getElementById("tl-over");
  var rangeEl = document.getElementById("tl-range");
  var reduce = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;
  // The site's root (it is served under /Mizien/ on GitHub Pages): links in the data are root-relative, so they are
  // resolved against the folder this script is served from.
  var BASE = (document.currentScript && document.currentScript.src || location.href).replace(/assets\/timeline\.js.*$/, "");
  function href(path) { return BASE + String(path || "").replace(/^\//, ""); }
  // Lanes split the line by topic, by the kind of body that spoke, or by verdict; "checked only" hides claims not yet
  // checked. Both are kept in the address (?lanes=topic&checked=1), so a view can be shared.
  var q0 = new URLSearchParams(location.search);
  var lanes = ["topic", "who", "verdict"].indexOf(q0.get("lanes")) >= 0 ? q0.get("lanes") : "none", checkedOnly = q0.get("checked") === "1";
  var VERDICT_LANES = ["Supported", "Largely supported", "Not substantiated", "Misleading", "Contradicted", "Pledge", "Not yet checked"];
  function laneOf(p) { return lanes === "topic" ? p.topic : lanes === "who" ? p.who : p.pledge ? "Pledge" : p.label; }
  function shown(p) { return !checkedOnly || p.v !== "none"; }

  // ------------------------------------------------------------ data
  var pts = JSON.parse(dataEl.textContent).map(function (p) {
    var m = /^(\d{4})(?:-(\d{2}))?(?:-(\d{2}))?$/.exec(p.date);
    var y = +m[1], mo = m[2] ? +m[2] - 1 : null, d = m[3] ? +m[3] : null;
    if (p.precision === "year") { p.start = Date.UTC(y, 0, 1); p.end = Date.UTC(y + 1, 0, 1); p.rank = 0; }
    else if (p.precision === "month") { p.start = Date.UTC(y, mo, 1); p.end = Date.UTC(y, mo + 1, 1); p.rank = 1; }
    else if (p.time) {
      p.start = Date.UTC(y, mo, d, +p.time.slice(0, 2), +p.time.slice(3)); p.end = p.start + 60000; p.rank = 4;
    } else { p.start = Date.UTC(y, mo, d); p.end = p.start + DAY; p.rank = 3; }
    return p;
  });
  if (!pts.length) return;
  var byId = {};
  pts.forEach(function (p) { byId[p.id] = p; });

  var now = new Date();
  var today = Date.UTC(now.getFullYear(), now.getMonth(), now.getDate());
  var R0 = Math.min.apply(null, pts.map(function (p) { return p.start; })) - 30 * DAY;
  var R1 = Math.max(today + DAY, Math.max.apply(null, pts.map(function (p) { return p.end; }))) + 45 * DAY;

  // ------------------------------------------------------------ helpers
  function esc(s) { return String(s).replace(/[&<>"']/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]; }); }
  function clamp(v, a, b) { return Math.max(a, Math.min(b, v)); }
  function dt(t) { return new Date(t); }
  function pad(n) { return (n < 10 ? "0" : "") + n; }
  function levelFor(ppd) { var l = LEVELS[0]; LEVELS.forEach(function (x) { if (ppd >= x.from) l = x; }); return l; }
  function startOf(level, t) {
    var d = dt(t);
    if (level === "month") return Date.UTC(d.getUTCFullYear(), d.getUTCMonth(), 1);
    if (level === "week") { var day = Math.floor(t / DAY) * DAY; return day - ((dt(day).getUTCDay() + 6) % 7) * DAY; }
    if (level === "day") return Math.floor(t / DAY) * DAY;
    if (level === "year") return Date.UTC(d.getUTCFullYear(), 0, 1);
    return Math.floor(t / HOUR) * HOUR;
  }
  function endOf(level, s) {
    var d = dt(s);
    if (level === "month") return Date.UTC(d.getUTCFullYear(), d.getUTCMonth() + 1, 1);
    if (level === "year") return Date.UTC(d.getUTCFullYear() + 1, 0, 1);
    if (level === "week") return s + 7 * DAY;
    if (level === "day") return s + DAY;
    return s + HOUR;
  }
  function longDate(t) { var d = dt(t); return d.getUTCDate() + " " + MONL[d.getUTCMonth()] + " " + d.getUTCFullYear(); }
  function shortDate(t) { var d = dt(t); return d.getUTCDate() + " " + MON[d.getUTCMonth()]; }
  function pointDate(p) {
    if (p.precision === "year") return p.date;
    if (p.precision === "month") { return MONL[+p.date.slice(5, 7) - 1] + " " + p.date.slice(0, 4); }
    return longDate(p.start) + (p.time ? ", " + p.time : "");
  }
  function periodName(level, s) {
    var d = dt(s);
    if (level === "year") return String(d.getUTCFullYear());
    if (level === "month") return MONL[d.getUTCMonth()] + " " + d.getUTCFullYear();
    if (level === "week") return "Week of " + longDate(s);
    if (level === "day") return longDate(s);
    return longDate(s) + ", " + pad(d.getUTCHours()) + ":00 to " + pad((d.getUTCHours() + 1) % 24) + ":00";
  }

  // Verdict colours are read from the stylesheet so the markers always match the badges.
  var colourCache = {};
  function colour(slug) {
    if (colourCache[slug]) return colourCache[slug];
    var probe = document.createElement("span");
    probe.className = "v-" + slug; probe.style.cssText = "position:absolute;visibility:hidden";
    document.body.appendChild(probe);
    var c = getComputedStyle(probe).getPropertyValue("--v").trim() || "#5d7468";
    document.body.removeChild(probe);
    return (colourCache[slug] = c);
  }
  function ring(items) {
    var slugs = items.map(function (i) { return i.v; }).sort();
    var step = 100 / slugs.length, stops = slugs.map(function (s, i) {
      return colour(s) + " " + (i * step).toFixed(2) + "% " + ((i + 1) * step).toFixed(2) + "%";
    });
    return "conic-gradient(" + stops.join(",") + ")";
  }

  // ------------------------------------------------------------ view state
  var W = 800, t0 = 0, ppd = 4, selected = {}, picks = [], anim = 0, raf = 0, lastH = 0;

  function span() { return W / ppd * DAY; }
  function tAt(x) { return t0 + x / ppd * DAY; }
  function xAt(t) { return (t - t0) / DAY * ppd; }
  function setView(newT0, newPpd) {
    ppd = clamp(newPpd, MIN_PPD, MAX_PPD);
    var c = clamp(newT0 + span() / 2, R0, R1);
    t0 = c - span() / 2;
    schedule();
  }
  function centre() { return t0 + span() / 2; }
  function goTo(c, p, instant) {
    p = clamp(p, MIN_PPD, MAX_PPD);
    cancelAnimationFrame(anim);
    if (reduce || instant) { ppd = p; setView(c - W / p / 2 * DAY, p); return; }
    var c0 = centre(), l0 = Math.log(ppd), l1 = Math.log(p), start = performance.now(), dur = 260;
    (function step(now) {
      var k = clamp((now - start) / dur, 0, 1), e = 1 - Math.pow(1 - k, 3);
      var pp = Math.exp(l0 + (l1 - l0) * e);
      ppd = pp; setView(c0 + (c - c0) * e - W / pp / 2 * DAY, pp);
      if (k < 1) anim = requestAnimationFrame(step);
    })(start);
  }
  function zoomAt(factor, ax) {
    var p = clamp(ppd * factor, MIN_PPD, MAX_PPD), t = tAt(ax);
    setView(t - ax / p * DAY, p);
  }
  function schedule() { if (!raf) raf = requestAnimationFrame(function () { raf = 0; render(); }); }

  // ------------------------------------------------------------ ticks and axis
  function ticks(level, lo, hi) {
    // Fine ticks (labelled) and coarse periods (sticky heading) for the visible range.
    var fine = level.name;
    var coarse = level.name === "year" ? null : level.name === "month" ? "year" : level.name === "hour" ? "day" : "month";
    var out = { fine: [], coarse: [] }, s, e, n;
    for (s = startOf(fine, lo), n = 0; s < hi && n < 400; s = endOf(fine, s), n++) {
      var d = dt(s), label;
      if (fine === "year") label = String(d.getUTCFullYear());
      else if (fine === "month") label = ppd * 30 >= 34 ? MON[d.getUTCMonth()] : (d.getUTCMonth() % 3 === 0 ? MON[d.getUTCMonth()] : "");
      else if (fine === "week") label = shortDate(s);
      else if (fine === "day") label = DOW[d.getUTCDay()] + " " + d.getUTCDate();
      else label = pad(d.getUTCHours()) + ":00";
      out.fine.push({ s: s, label: label, major: fine === "year" ? true : fine === "month" ? d.getUTCMonth() === 0 : fine === "hour" ? d.getUTCHours() === 0 : false });
    }
    if (coarse) for (s = startOf(coarse, lo), n = 0; s < hi && n < 100; s = e, n++) {
      e = endOf(coarse, s);
      out.coarse.push({ s: s, e: e, label: periodName(coarse, s).replace(/^Week of /, "") });
    }
    return out;
  }

  // ------------------------------------------------------------ render
  var narrow = false, A = 170, LH = 46, LTOP = 26;
  function laneList() {
    if (lanes === "none") return [];
    var n = {}; pts.forEach(function (p) { if (shown(p)) n[laneOf(p)] = (n[laneOf(p)] || 0) + 1; });
    var names = Object.keys(n);
    if (lanes === "verdict") names.sort(function (a, b) { return VERDICT_LANES.indexOf(a) - VERDICT_LANES.indexOf(b); });
    else names.sort(function (a, b) { return n[b] - n[a] || a.localeCompare(b); });
    return names.map(function (name) { return { name: name, n: n[name] }; });
  }
  function render() {
    W = stage.clientWidth || W;
    narrow = W < 560;
    var LN = laneList();
    A = LN.length ? LTOP + LN.length * LH + 4 : 142;
    var level = levelFor(ppd);
    var margin = 190 / ppd * DAY;
    var lo = t0 - margin, hi = t0 + span() + margin;
    var html = "", items = {}, k = 0;

    // Calendar ticks, coarse headings and the axis line itself.
    var tk = ticks(level, lo, hi);
    tk.coarse.forEach(function (c) {
      var x = xAt(c.s), xe = xAt(c.e);
      html += '<i class="tlv-gl" style="left:' + x.toFixed(1) + 'px"></i>';
      var lw = c.label.length * 7.4, lx = clamp(x, 8, Math.max(8, xe - 8 - lw));
      if (xe > 0 && x < W && Math.min(xe, W) - Math.max(x, 0) >= lw + 16) html += '<span class="tlv-co" style="left:' + lx.toFixed(1) + 'px;top:' + (A + 30) + 'px">' + esc(c.label) + "</span>";
    });
    tk.fine.forEach(function (t) {
      var x = xAt(t.s);
      html += '<i class="tlv-tk' + (t.major ? " is-major" : "") + '" style="left:' + x.toFixed(1) + 'px;top:' + A + 'px"></i>';
      if (t.label) html += '<span class="tlv-fl" style="left:' + x.toFixed(1) + 'px;top:' + (A + 9) + 'px">' + esc(t.label) + "</span>";
    });
    html += '<i class="tlv-axis" style="top:' + A + 'px"></i>';
    if (today >= lo && today <= hi) {
      html += '<i class="tlv-today" style="left:' + xAt(today + DAY / 2).toFixed(1) + 'px;top:22px;height:' + (A - 22) + 'px"></i>' +
        '<span class="tlv-todaylab" style="left:' + xAt(today + DAY / 2).toFixed(1) + 'px;top:6px">Today</span>';
    }

    // Exact claims are clumped into one marker per month / week / day / hour; the rest become bars.
    if (LN.length) return renderLanes(LN, level, lo, hi, html, items, k);
    var buckets = {}, bars = {};
    pts.forEach(function (p) {
      if (!shown(p)) return;
      if (p.end < lo && p.start < lo) return;
      if (p.start > hi) return;
      if (p.rank >= level.rank) {
        var s = startOf(level.name, p.start);
        (buckets[s] = buckets[s] || { s: s, items: [] }).items.push(p);
      } else {
        var key = p.rank + ":" + p.start;
        (bars[key] = bars[key] || { s: p.start, e: p.end, rank: p.rank, items: [] }).items.push(p);
      }
    });

    var marks = Object.keys(buckets).map(function (s) { return buckets[s]; }).sort(function (a, b) { return a.s - b.s; });
    var maxLab = narrow ? 118 : 170, N = 3, last = [];
    for (var i = 0; i < N; i++) last.push(-1e9);
    marks.forEach(function (m) {
      var mid = m.s + (endOf(level.name, m.s) - m.s) / 2;
      m.x = xAt(mid);
      m.single = m.items.length === 1;
      m.text = m.single ? m.items[0].id + " " + m.items[0].title : m.items.length + " claims";
      m.lw = Math.min(maxLab, m.text.length * 6.4 + 6);
      m.h = m.single ? 20 : 28;
      var placed = false, lv, j;
      for (lv = 0; lv < N && !placed; lv++) {
        var ok = last[lv] <= m.x - 16;
        for (j = 0; j < lv && ok; j++) ok = last[j] <= m.x - 8;
        if (ok) { m.lv = lv; m.lab = true; last[lv] = m.x + 16 + m.lw; placed = true; }
      }
      for (lv = 0; lv < N && !placed; lv++) {
        var ok2 = last[lv] <= m.x - 14;
        for (j = 0; j < lv && ok2; j++) ok2 = last[j] <= m.x - 8;
        if (ok2) { m.lv = lv; m.lab = false; last[lv] = m.x + 14; placed = true; }
      }
      if (!placed) { m.lv = 0; m.lab = false; last[0] = Math.max(last[0], m.x + 14); }
    });
    marks.forEach(function (m) {
      var key = "m" + k++; items[key] = { items: m.items, level: level.name, s: m.s };
      var stem = 22 + m.lv * 38, top = A - stem - m.h, ids = m.items.map(function (i) { return i.id; });
      var sel = ids.some(function (id) { return selected[id]; });
      var aria = m.single ? m.items[0].id + ": " + m.items[0].title + ", " + pointDate(m.items[0]) + ", " + m.items[0].label
        : m.items.length + " claims, " + periodName(level.name, m.s);
      html += '<button type="button" class="tlv-m' + (sel ? " is-selected" : "") + (m.single ? " v-" + m.items[0].v : " is-clump") +
        '" data-k="' + key + '" style="left:' + (m.x - m.h / 2).toFixed(1) + "px;top:" + top + "px;height:" + m.h + 'px" aria-label="' + esc(aria) + '">' +
        '<i class="tlv-stem" style="left:' + (m.h / 2 - 1) + "px;top:" + m.h + "px;height:" + stem + 'px"></i>' +
        '<span class="tlv-head" style="width:' + m.h + "px;height:" + m.h + "px" + (m.single ? "" : ";background:" + ring(m.items)) + '">' +
        (m.single ? "" : "<b>" + m.items.length + "</b>") + "</span>" +
        (m.lab ? '<span class="tlv-lab" style="max-width:' + maxLab + 'px">' + esc(m.text) + "</span>" : "") + "</button>";
    });

    // Bars for claims dated only to a month or a year.
    var bl = Object.keys(bars).map(function (b) { return bars[b]; }).sort(function (a, b) { return a.s - b.s || b.e - a.e; });
    var rows = [], laneTop = A + 66;
    bl.forEach(function (b) {
      var x0 = xAt(b.s), x1 = xAt(b.e);
      if (x1 < -4 || x0 > W + 4) return;
      var r = 0;
      while (rows[r] !== undefined && rows[r] > x0 - 3) r++;
      rows[r] = x1;
      var vis0 = Math.max(x0, 0), vis1 = Math.min(x1, W);
      var name = (b.rank === 0 ? dt(b.s).getUTCFullYear() : MON[dt(b.s).getUTCMonth()] + " " + dt(b.s).getUTCFullYear()) +
        " · " + b.items.length + (b.items.length === 1 ? " claim" : " claims");
      var key = "b" + k++; items[key] = { items: b.items, bar: true, rank: b.rank, s: b.s };
      var sel = b.items.some(function (i) { return selected[i.id]; });
      var off = Math.max(0, Math.min(-x0, x1 - x0 - 90)) + 8;
      html += '<button type="button" class="tlv-pill' + (sel ? " is-selected" : "") + '" data-k="' + key + '" style="left:' + x0.toFixed(1) +
        "px;width:" + Math.max(10, x1 - x0).toFixed(1) + "px;top:" + (laneTop + r * 28) + 'px" aria-label="' + esc(name + ", " + (b.rank === 0 ? "year only" : "month only")) +
        '"><span style="margin-left:' + off.toFixed(0) + 'px">' + esc(name) + "</span></button>";
    });
    var H = laneTop + Math.max(rows.length, 0) * 28 + (rows.length ? 10 : 0);
    html += rows.length ? '<span class="tlv-lane" style="top:' + (laneTop - 19) + 'px">Date known only to the month or year</span>' : "";
    H = Math.max(H, A + 72);
    finish(html, items, H, level);
  }
  // Lanes: one line per topic, kind of body or verdict, each with its own clumps. Dates known only to a month or a
  // year are a dashed stretch on the lane's line.
  function renderLanes(LN, level, lo, hi, html, items, k) {
    var idx = {}; LN.forEach(function (L, i) { idx[L.name] = i; });
    var cells = {}, bars = {};
    pts.forEach(function (p) {
      if (!shown(p) || (p.end < lo && p.start < lo) || p.start > hi) return;
      var li = idx[laneOf(p)];
      if (p.rank >= level.rank) { var s = startOf(level.name, p.start), key = li + ":" + s;
        (cells[key] = cells[key] || { li: li, s: s, items: [] }).items.push(p); }
      else { var bk = li + ":" + p.rank + ":" + p.start; (bars[bk] = bars[bk] || { li: li, s: p.start, e: p.end, rank: p.rank, items: [] }).items.push(p); }
    });
    LN.forEach(function (L, i) {
      var y = LTOP + i * LH + LH / 2;
      html += '<i class="tlv-lline" style="top:' + y + 'px"></i>' +
        '<span class="tlv-lname" style="top:' + (y - LH / 2 + 2) + 'px">' + esc(L.name) + ' <b>' + L.n + "</b></span>";
    });
    Object.keys(bars).forEach(function (bk) { var b = bars[bk], x0 = xAt(b.s), x1 = xAt(b.e); if (x1 < -4 || x0 > W + 4) return;
      var y = LTOP + b.li * LH + LH / 2, key = "b" + k++; items[key] = { items: b.items, bar: true, rank: b.rank, s: b.s };
      var sel = b.items.some(function (i) { return selected[i.id]; });
      html += '<button type="button" class="tlv-lbar' + (sel ? " is-selected" : "") + '" data-k="' + key + '" style="left:' + x0.toFixed(1) + "px;width:" +
        Math.max(8, x1 - x0).toFixed(1) + "px;top:" + (y - 5) + 'px" aria-label="' + esc(LN[b.li].name + ": " + b.items.length + (b.items.length === 1 ? " claim" : " claims") +
        " dated only to " + (b.rank === 0 ? "the year " + dt(b.s).getUTCFullYear() : MONL[dt(b.s).getUTCMonth()] + " " + dt(b.s).getUTCFullYear())) + '"></button>'; });
    Object.keys(cells).forEach(function (ck) { var c = cells[ck], x = xAt(c.s + (endOf(level.name, c.s) - c.s) / 2); if (x < -20 || x > W + 20) return;
      var y = LTOP + c.li * LH + LH / 2, single = c.items.length === 1, h = single ? 16 : 24, key = "m" + k++;
      items[key] = { items: c.items, level: level.name, s: c.s };
      var sel = c.items.some(function (i) { return selected[i.id]; });
      var aria = single ? c.items[0].id + ": " + c.items[0].title + ", " + pointDate(c.items[0]) + ", " + c.items[0].label : c.items.length + " claims, " + LN[c.li].name + ", " + periodName(level.name, c.s);
      html += '<button type="button" class="tlv-m tlv-lm' + (sel ? " is-selected" : "") + (single ? " v-" + c.items[0].v : " is-clump") + '" data-k="' + key +
        '" style="left:' + (x - h / 2).toFixed(1) + "px;top:" + (y - h / 2) + "px;height:" + h + 'px" aria-label="' + esc(aria) + '">' +
        '<span class="tlv-head" style="width:' + h + "px;height:" + h + "px" + (single ? "" : ";background:" + ring(c.items)) + '">' + (single ? "" : "<b>" + c.items.length + "</b>") + "</span></button>"; });
    finish(html, items, A + 52, level);
  }
  function finish(html, items, H, level) {
    if (H !== lastH) { stage.style.height = H + "px"; lastH = H; }
    stage.innerHTML = html;
    picks = items;

    // Controls and readout.
    root.querySelectorAll("[data-level]").forEach(function (b) { b.setAttribute("aria-pressed", b.dataset.level === level.name ? "true" : "false"); });
    root.querySelectorAll("[data-lanes]").forEach(function (b) { b.setAttribute("aria-pressed", b.dataset.lanes === lanes ? "true" : "false"); });
    rangeEl.textContent = "Showing " + longDate(Math.max(t0, R0)) + " to " + longDate(Math.min(t0 + span(), R1)) +
      " · grouped by " + level.noun + (checkedOnly ? " · checked claims only" : "");
    renderOver();
  }

  // ------------------------------------------------------------ overview strip
  function renderOver() {
    var total = R1 - R0, html = "";
    for (var y = dt(R0).getUTCFullYear() + 1; Date.UTC(y, 0, 1) < R1; y++) {
      html += '<span class="tlv-oy" style="left:' + ((Date.UTC(y, 0, 1) - R0) / total * 100).toFixed(2) + '%">' + y + "</span>";
    }
    pts.forEach(function (p) { if (!shown(p)) return;
      html += '<i class="tlv-od v-' + p.v + (p.rank < 3 ? " is-rough" : "") + '" style="left:' + (((p.start + p.end) / 2 - R0) / total * 100).toFixed(2) + '%"></i>';
    });
    var l = clamp((t0 - R0) / total, 0, 1), w = clamp(span() / total, 0.006, 1);
    html += '<i class="tlv-ow" style="left:' + (l * 100).toFixed(2) + "%;width:" + (w * 100).toFixed(2) + '%"></i>';
    over.innerHTML = html;
  }
  var overDrag = false;
  function overTo(ev) {
    var r = over.getBoundingClientRect();
    goTo(R0 + clamp((ev.clientX - r.left) / r.width, 0, 1) * (R1 - R0), ppd, true);
  }
  over.addEventListener("pointerdown", function (ev) { overDrag = true; over.setPointerCapture(ev.pointerId); overTo(ev); });
  over.addEventListener("pointermove", function (ev) { if (overDrag) overTo(ev); });
  over.addEventListener("pointerup", function () { overDrag = false; });
  over.addEventListener("pointercancel", function () { overDrag = false; });

  // ------------------------------------------------------------ selection panel
  function select(key) {
    var it = picks[key]; if (!it) return;
    selected = {}; it.items.forEach(function (i) { selected[i.id] = 1; });
    var title, sub = "";
    if (it.bar) {
      title = (it.rank === 0 ? dt(it.s).getUTCFullYear() : MONL[dt(it.s).getUTCMonth()] + " " + dt(it.s).getUTCFullYear());
      sub = "These claims are dated only to the " + (it.rank === 0 ? "year" : "month") + ", so they are not placed on a day.";
    } else {
      title = periodName(it.level, it.s);
      if (it.level === "hour") sub = "Claims with no recorded time sit in the date-only bars, not on an hour.";
    }
    var html = '<h2 class="tlv-ph">' + esc(title) + ' <span class="small">· ' + it.items.length + (it.items.length === 1 ? " claim" : " claims") + "</span></h2>";
    if (sub) html += '<p class="small">' + esc(sub) + "</p>";
    html += '<ul class="tlv-claims">' + it.items.map(function (i) {
      var also = '<span class="tlv-also small">' + (i.place ? '<a href="' + esc(href("/?view=map&sel=claim:" + i.id)) + '">On the map</a> · ' : "") +
        '<a href="' + esc(href("/?view=ghanqbuta&sel=claim:" + i.id)) + '">In the claims web</a></span>';
      return '<li><a class="tlv-cl" href="' + esc(href(i.path)) + '"><span class="tlv-cid">' + esc(i.id) + '</span><span class="tlv-ct">' + esc(i.title) + "</span></a>" +
        '<span class="tlv-cm small">' + esc(i.speaker ? i.speaker + " · " : "") + esc(pointDate(i)) + "</span>" +
        '<span class="badge v-' + esc(i.v) + '">' + (i.pledge ? "Pledge: " : "") + esc(i.label) + "</span>" + also + "</li>";
    }).join("") + "</ul>";
    var next = !it.bar && it.items.length > 1 && it.level !== "hour";
    if (next) html += '<button type="button" class="tlv-btn tlv-wide" data-act="into" data-k="' + key + '">Zoom in on this ' + it.level + "</button>";
    panel.innerHTML = html;
    panel._it = it;
    render();
  }
  function zoomInto(it) {
    var s = it.s, e = endOf(it.level, s), want = it.level === "year" ? 365 : it.level === "month" ? 30 : it.level === "week" ? 7 : it.level === "day" ? 1 : 0.04;
    var next = LEVELS[Math.min(LEVELS.length - 1, LEVELS.map(function (l) { return l.name; }).indexOf(it.level) + 1)];
    goTo(s + (e - s) / 2, Math.max(next.ppd, W * 0.85 / want));
  }

  // ------------------------------------------------------------ input
  var drag = null, moved = false, ptrs = {}, pinch = null;
  stage.addEventListener("pointerdown", function (ev) {
    ptrs[ev.pointerId] = { x: ev.clientX, y: ev.clientY };
    var ids = Object.keys(ptrs);
    if (ids.length === 2) {
      var a = ptrs[ids[0]], b = ptrs[ids[1]];
      pinch = { d: Math.hypot(a.x - b.x, a.y - b.y), ppd: ppd }; drag = null; moved = true;
    } else if (ids.length === 1) {
      drag = { x: ev.clientX, t0: t0, id: ev.pointerId }; moved = false; cancelAnimationFrame(anim);
    }
  });
  stage.addEventListener("pointermove", function (ev) {
    if (!ptrs[ev.pointerId]) return;
    ptrs[ev.pointerId] = { x: ev.clientX, y: ev.clientY };
    var ids = Object.keys(ptrs);
    if (pinch && ids.length === 2) {
      var a = ptrs[ids[0]], b = ptrs[ids[1]], d = Math.hypot(a.x - b.x, a.y - b.y) || 1;
      var r = stage.getBoundingClientRect(), mx = (a.x + b.x) / 2 - r.left;
      var p = clamp(pinch.ppd * d / pinch.d, MIN_PPD, MAX_PPD), t = tAt(mx);
      setView(t - mx / p * DAY, p);
    } else if (drag && ev.pointerId === drag.id) {
      var dx = ev.clientX - drag.x;
      if (!moved && Math.abs(dx) > 5) { moved = true; try { stage.setPointerCapture(ev.pointerId); } catch (e) {} stage.classList.add("is-drag"); }
      if (moved) setView(drag.t0 - dx / ppd * DAY, ppd);
    }
  });
  function end(ev) {
    delete ptrs[ev.pointerId];
    if (Object.keys(ptrs).length < 2) pinch = null;
    if (drag && ev.pointerId === drag.id) drag = null;
    stage.classList.remove("is-drag");
  }
  stage.addEventListener("pointerup", end);
  stage.addEventListener("pointercancel", end);
  stage.addEventListener("click", function (ev) {
    if (moved) { moved = false; ev.preventDefault(); ev.stopPropagation(); return; }
    var m = ev.target.closest("[data-k]");
    if (m) { var k = m.dataset.k; select(k); var again = stage.querySelector('[data-k="' + k + '"]'); if (again) again.focus({ preventScroll: true }); }
  }, true);
  stage.addEventListener("dblclick", function (ev) {
    var m = ev.target.closest("[data-k]"), it = m && picks[m.dataset.k];
    if (it && !it.bar && it.items.length > 1 && it.level !== "hour") zoomInto(it);
  });
  stage.addEventListener("wheel", function (ev) {
    var r = stage.getBoundingClientRect();
    if (ev.ctrlKey || ev.metaKey) { ev.preventDefault(); zoomAt(Math.exp(-ev.deltaY * 0.01), ev.clientX - r.left); }
    else if (Math.abs(ev.deltaX) > Math.abs(ev.deltaY) || ev.shiftKey) {
      ev.preventDefault(); setView(t0 + (ev.deltaX || ev.deltaY) / ppd * DAY, ppd);
    }
  }, { passive: false });
  stage.addEventListener("keydown", function (ev) {
    if (ev.target !== stage) return;
    var k = ev.key, h = true;
    if (k === "ArrowLeft") setView(t0 - span() * 0.15, ppd);
    else if (k === "ArrowRight") setView(t0 + span() * 0.15, ppd);
    else if (k === "+" || k === "=") goTo(centre(), ppd * 1.8);
    else if (k === "-" || k === "_") goTo(centre(), ppd / 1.8);
    else if (k === "Home") goTo(R0 + 30 * DAY, ppd);
    else if (k === "End") latest();
    else h = false;
    if (h) ev.preventDefault();
  });

  function latest() {
    var last = pts[pts.length - 1], p = Math.max(initialPpd(), ppd < 10 ? 4 : ppd);
    goTo(last.start + (last.end - last.start) / 2 - W * 0.25 / p * DAY, p);
  }
  function initialPpd() { return clamp(W / 200, 3, 6); }
  function showAll() { goTo((R0 + R1) / 2, W / ((R1 - R0) / DAY)); }

  root.addEventListener("click", function (ev) {
    var b = ev.target.closest("button"); if (!b || b.closest(".tlv-stage")) return;
    if (b.dataset.level) { var l = LEVELS.filter(function (x) { return x.name === b.dataset.level; })[0]; goTo(centre(), l.ppd); }
    else if (b.dataset.act === "in") goTo(centre(), ppd * 1.8);
    else if (b.dataset.act === "out") goTo(centre(), ppd / 1.8);
    else if (b.dataset.act === "latest") latest();
    else if (b.dataset.act === "all") showAll();
    else if (b.dataset.act === "into" && panel._it) zoomInto(panel._it);
    else if (b.dataset.lanes) { lanes = b.dataset.lanes; syncAddress(); render(); }
  });
  var chk = document.getElementById("tl-checked");
  if (chk) { chk.checked = checkedOnly; chk.addEventListener("change", function () { checkedOnly = chk.checked; syncAddress(); render(); }); }
  function syncAddress() {
    var u = new URL(location.href);
    if (lanes === "none") u.searchParams.delete("lanes"); else u.searchParams.set("lanes", lanes);
    if (checkedOnly) u.searchParams.set("checked", "1"); else u.searchParams.delete("checked");
    history.replaceState(null, "", u);
  }

  // ------------------------------------------------------------ start
  root.hidden = false;
  var list = document.getElementById("tl-list"); if (list) list.open = false;
  W = stage.clientWidth || 800;
  ppd = initialPpd();
  var lastPt = pts[pts.length - 1];
  t0 = lastPt.start - W * 0.7 / ppd * DAY;
  var id = (location.hash || "").slice(1);
  if (byId[id]) {
    var p = byId[id], dayLevel = p.rank >= 3;
    ppd = dayLevel ? LEVELS[1].ppd : 4;
    setView(p.start + (p.end - p.start) / 2 - W / 2 / ppd * DAY, ppd);
    selected[id] = 1;
  }
  render();
  if (selected[id]) {
    var hit = Object.keys(picks).filter(function (k) { return picks[k].items.some(function (i) { return i.id === id; }); })[0];
    if (hit) select(hit);
  }
  var rz; window.addEventListener("resize", function () { clearTimeout(rz); rz = setTimeout(function () { var c = centre(); W = stage.clientWidth || W; setView(c - W / ppd / 2 * DAY, ppd); }, 60); });
})();
