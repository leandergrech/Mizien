// Miżien homepage: the claims web and Malta map, drawn on a canvas.
// Moved verbatim from the inline <script> in docs/index.html (October 2026).
(function () {
  "use strict";
  var canvas = document.getElementById("map"), ctx = canvas.getContext("2d");
  var stage = document.getElementById("stage"), panel = document.getElementById("panel"), tip = document.getElementById("tip");
  var viewer = document.getElementById("doc-viewer"), viewerFrame = viewer.querySelector("iframe"), viewerImage = viewer.querySelector("img");
  var DATA = null, claims = [], edges = [], byId = {}, themeById = {}, stars = [];
  var hubPool = {}, hubs = [];            // hubPool: every hub ever made (key = mode|value); hubs: those of the current mode
  var subHubs = [];                      // topic view: subtopic hubs orbiting their topic hub (claim.yml `subtopic`)
  var mode = "topic";
  var showSpokes = true, themeOn = {};
  var cam = { yaw: 0.6, pitch: -0.22, zoom: 1, tyaw: null, tpitch: -0.22, fx: 0, fy: 0, fz: 0, em: 1, tem: 1, px: 0, py: 0, tpx: 0, tpy: 0 };
  var ZMIN = 0.4, ZMAX = 5;
  // map view: claims on a stylised map of the islands; districts open into detailed views
  var view = "graph", GEO = null, mapLevel = null, mapZ = 1, tmapZ = 1, mapC = { x: 0, y: -700 }, tmapC = { x: 0, y: -700 }, MPU = 68, HOME = { x: 0, y: -700 }, badges = [], MAP_PITCH = 1.12;
  var spinBeforeMap = true;
  // fisheye lens: magnifies the middle of the stage, compresses the rim, leaves the rest untouched
  var lensPref = null, lensK = 0, LENS_D = 2.2;
  try { var lp = localStorage.getItem("mizien.lens"); if (lp === "on" || lp === "off") lensPref = lp === "on"; } catch (e) {}
  function lensWanted() { return lensPref !== null ? lensPref : (view === "map" && W < 700); }
  function lensR() { return 0.46 * Math.min(W - leftInset() - panelInset(), H - 120 - topInset()); }
  var expanded = null;                    // hub whose sub-graph is opened out
  var labelMode = "code", showText = true;
  try { if (localStorage.getItem("mizien.labels") === "tag") labelMode = "tag"; if (localStorage.getItem("mizien.text") === "off") showText = false; } catch (e) {}
  var spinning = true, sway = false;
  var sel = null, hover = null;
  var W = 0, H = 0, dpr = 1, R = 250, t0 = performance.now(), lastT = 0;
  var MAP_THEME = document.documentElement.getAttribute("data-map-theme") || "botanical";
  var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (reduce) spinning = false;

  var VC = { "Supported": "#2e7d4f", "Largely supported": "#8db36b", "Not substantiated": "#d9772b",
             "Misleading": "#c85a3a", "Contradicted": "#8e2f25" };
  var NOT_YET = "Not yet checked", NOT_YET_COL = "#5d7468";
  var ICONS = {
    // topics
    "Land & Trees": "M12 2.5 L5.5 11 H9 L5 16.5 H19 L15 11 H18.5 Z M12 16.5 V21.5",
    "Climate & Energy": "M13.5 2.5 L5 13.5 H11 L10 21.5 L19 10 H13 Z",
    "Waste": "M4 6.5 H20 M9.5 6.5 V4 H14.5 V6.5 M6 6.5 L7 20.5 H17 L18 6.5 M10 10 V17 M14 10 V17",
    "Water": "M12 2.5 C12 2.5 5.5 10 5.5 14.5 A6.5 6.5 0 0 0 18.5 14.5 C18.5 10 12 2.5 12 2.5 Z",
    "Nature & Wildlife": "M2.5 13 C6 13 8 11 9 7.5 C10.5 11 13 12.5 16 12.5 L21.5 9 L19.5 14 C17.5 18 14 19.5 10 19.5 C6 19.5 3.5 17 2.5 13 Z M14.5 9.5 L14.6 9.6",
    "Air": "M3 8.5 H13 A3 3 0 1 0 10 5.5 M3 12.5 H18 A3 3 0 1 1 15 15.5 M3 16.5 H9",
    "Transport": "M3 13.5 L5.5 7.5 H18.5 L21 13.5 V18 H3 Z M3 13.5 H21 M6 18 V20 M18 18 V20 M7 15.8 H8.5 M15.5 15.8 H17",
    "Governance & Promises": "M12 3 V20.5 M7.5 20.5 H16.5 M4.5 6.5 H19.5 M4.5 6.5 L2 12.5 H7 Z M19.5 6.5 L17 12.5 H22 Z",
    "Planning & Housing": "M3 11 L12 3.5 L21 11 M5.5 9 V20.5 H18.5 V9 M10 20.5 V14.5 H14 V20.5",
    "Noise": "M3.5 9.5 H7.5 L12.5 5 V19 L7.5 14.5 H3.5 Z M16 9 C17.3 10.5 17.3 13.5 16 15 M18.8 6.5 C21.4 9.5 21.4 14.5 18.8 17.5",
    // verdicts
    "Supported": "M5 12.5 L10 17.5 L19 7",
    "Largely supported": "M4 13 L8.5 17.5 L15.5 9 M12.5 17 L14 18.5 L21 10",
    "Not substantiated": "M8.8 9 A3.3 3.3 0 1 1 13.6 12 C12.4 12.6 12 13.3 12 14.6 M12 18 V18.1",
    "Misleading": "M12 3.5 L21.5 20 H2.5 Z M12 10 V14.5 M12 17 V17.1",
    "Contradicted": "M6 6 L18 18 M18 6 L6 18",
    "Not yet checked": "M5.5 12 V12.1 M12 12 V12.1 M18.5 12 V12.1",
    // patterns
    "Selective metric": "M10.5 4 A6.5 6.5 0 1 0 10.51 4 M15.2 15.2 L20.5 20.5",
    "Input-as-outcome": "M3.5 5 H20.5 L14 12.5 V19.5 L10 17.5 V12.5 Z",
    "Compliance-not-health": "M12 3 L19 6 V11 C19 15.5 16 19 12 21 C8 19 5 15.5 5 11 V6 Z M9 12 L11 14 L15 10",
    "Conditional-turned-unconditional": "M6 3.5 V20.5 M6 12 C11 12 12 6 18 6 M15 3 L18 6 L15 9",
    "Promise-without-baseline": "M5.5 21 V3.5 M5.5 4 H17.5 L15 8 L17.5 12 H5.5",
    "No pattern tag": "M12 8 A4 4 0 1 0 12.01 8",
    // stages
    "Not started": "M12 3 A9 9 0 1 0 12.01 3 M12 7 V12 L15.5 14",
    "In progress": "M4 12 H19 M13 6 L19 12 L13 18",
    "Drafted": "M4 20 L8.5 19 L19.5 8 L16 4.5 L5 15.5 Z M14 6.5 L17.5 10",
    "Right of reply": "M4 4.5 H20 V15 H10.5 L6.5 19.5 V15 H4 Z",
    "Published": "M3.5 5 H10.5 C11.4 5 12 5.6 12 6.5 V20 C12 19.2 11.4 18.6 10.5 18.6 H3.5 Z M20.5 5 H13.5 C12.6 5 12 5.6 12 6.5 V20 C12 19.2 12.6 18.6 13.5 18.6 H20.5 Z",
    // speakers
    "Government": "M3 9 L12 4 L21 9 Z M5.5 9.5 V17.5 M10 9.5 V17.5 M14 9.5 V17.5 M18.5 9.5 V17.5 M3 20 H21",
    "Regulators & agencies": "M8.5 3.5 H15.5 V6.5 H8.5 Z M6.5 5 H4.5 V21 H19.5 V5 H17.5 M8 11.5 H16 M8 15.5 H13",
    "Political parties": "M4.5 10 H19.5 V20.5 H4.5 Z M8.5 10 L12 4 L15.5 10 M9 15 H15",
    "Business & developers": "M4 8 H20 V19.5 H4 Z M9 8 V5 H15 V8 M4 13 H20",
    "NGOs & civil society": "M8 7.5 A2.8 2.8 0 1 0 8.01 7.5 M16 7.5 A2.8 2.8 0 1 0 16.01 7.5 M2.5 19.5 C2.5 15 13.5 15 13.5 19.5 M10.5 19.5 C10.5 15 21.5 15 21.5 19.5",
    "Media": "M4 5 H17 V19.5 H6 C4.9 19.5 4 18.6 4 17.5 Z M17 9 H20 V17.5 C20 18.6 19.1 19.5 18 19.5 M7 8.5 H14 M7 12 H14 M7 15.5 H11",
    "EU & international": "M12 3 A9 9 0 1 0 12.01 3 M3 12 H21 M12 3 C15.5 6.5 15.5 17.5 12 21 C8.5 17.5 8.5 6.5 12 3",
    // grouping buttons
    "mode:topic": "M12 3 A9 9 0 1 0 12.01 3 M7 9 A1.5 1.5 0 1 0 7.01 9 M16 8 A1.5 1.5 0 1 0 16.01 8 M11 16 A1.5 1.5 0 1 0 11.01 16",
    "mode:subtopic": "M12 3 A9 9 0 1 0 12.01 3 M12 7.5 A4.5 4.5 0 1 0 12.01 7.5 M12 3 V7.5 M12 16.5 V21 M3 12 H7.5 M16.5 12 H21",
    "mode:verdict": "M12 3 V20.5 M7.5 20.5 H16.5 M4.5 6.5 H19.5 M4.5 6.5 L2 12.5 H7 Z M19.5 6.5 L17 12.5 H22 Z",
    "mode:pattern": "M12 3 A9 9 0 1 0 12.01 3 M12 7 A5 5 0 1 0 12.01 7 M12 11 A1 1 0 1 0 12.01 11",
    "mode:status": "M3 12 H21 M5 12 A1.5 1.5 0 1 0 5.01 12 M12 12 A1.5 1.5 0 1 0 12.01 12 M19 12 A1.5 1.5 0 1 0 19.01 12",
    "mode:speaker": "M4 5 H20 V15 H10.5 L6.5 19 V15 H4 Z",
    "mode:network": "M5 6 A2 2 0 1 0 5.01 6 M19 7 A2 2 0 1 0 19.01 7 M12 18 A2 2 0 1 0 12.01 18 M6.5 7.5 L11 16 M17.5 8.5 L13 16 M7 6.2 L17 6.8"
  };
  function iconKey(name) { return ICONS[name] ? name : String(name || "").split(" · ")[0]; } // subtopics reuse their topic's icon
  var ICON_PATHS = {};
  Object.keys(ICONS).forEach(function (k) { ICON_PATHS[k] = new Path2D(ICONS[k]); });

  var PALETTE = ["#e3a72f", "#56b4e9", "#6fcf97", "#f2994a", "#bb86fc", "#f06292", "#4fc3c8", "#9fa8da", "#cfd8dc"];
  var SPEAKER_RULES = [
    ["Media", /newsbook|amphora|times of malta|maltatoday|independent|shift news/i],
    ["EU & international", /european commission|european parliament|\bimf\b|\beu\b/i],
    ["Regulators & agencies", /planning authority|environment and resources|\bera\b|transport malta|ornis|wild birds/i],
    ["Political parties", /partit|labour party|nationalist|\bpn\b|\bpl\b|momentum/i],
    ["Business & developers", /developers|\bmda\b|hili|hospitality|chamber/i],
    ["NGOs & civil society", /graffitti|birdlife|din l-art|friends of the earth|ngo/i],
    ["Government", /minist|government|prime minister|authority|project green|infrastructure malta|water services|ambjent|wasteserv/i]
  ];
  function speakerGroup(s) {
    var first = (s || "").split(";")[0];
    for (var i = 0; i < SPEAKER_RULES.length; i++) if (SPEAKER_RULES[i][1].test(first)) return SPEAKER_RULES[i][0];
    for (i = 0; i < SPEAKER_RULES.length; i++) if (SPEAKER_RULES[i][1].test(s || "")) return SPEAKER_RULES[i][0];
    return "Other";
  }

  // ------------------------------------------------------------ groupings
  var MODES = {
    topic: { label: "Topic", title: "Claims by topic", sub: "Each hub is a topic, with its subtopics orbiting it; coloured threads link claims across topics.",
             layout: "sphere", key: function (c) { return [c.category]; },
             order: function () { return DATA.categories.map(function (c) { return c.name; }); },
             color: function (v) { var c = DATA.categories.filter(function (x) { return x.name === v; })[0]; return c ? c.color : "#7fa88b"; } },
    subtopic: { label: "Subtopic", title: "Claims by subtopic", sub: "Topics split into subtopics where a topic has grown large; other topics stay whole.",
             layout: "sphere", key: function (c) { return [c.subtopic ? c.category + " · " + c.subtopic : c.category]; },
             order: function () {
               var cats = DATA.categories.map(function (c) { return c.name; }), seen = {}, out = [];
               DATA.claims.slice().sort(function (a, b) { return cats.indexOf(a.category) - cats.indexOf(b.category) || String(a.subtopic || "").localeCompare(String(b.subtopic || "")); })
                 .forEach(function (c) { var k = c.subtopic ? c.category + " · " + c.subtopic : c.category; if (!seen[k]) { seen[k] = 1; out.push(k); } });
               return out; },
             color: function (v) { var base = String(v).split(" · ")[0], c = DATA.categories.filter(function (x) { return x.name === base; })[0]; return c ? c.color : "#7fa88b"; } },
    verdict: { label: "Verdict", title: "Claims by verdict", sub: "From supported to contradicted, left to right.",
             layout: "arc", key: function (c) { return [c.verdict || NOT_YET]; },
             order: function () { return Object.keys(VC).concat([NOT_YET]); },
             color: function (v) { return VC[v] || NOT_YET_COL; } },
    pattern: { label: "Pattern", title: "Claims by pattern", sub: "Recurring ways a claim can mislead. Faint spokes show a claim's second pattern.",
             layout: "ring", key: function (c) { return c.tags && c.tags.length ? c.tags : ["No pattern tag"]; },
             order: function () { return ["Selective metric", "Input-as-outcome", "Compliance-not-health", "Conditional-turned-unconditional", "Promise-without-baseline", "No pattern tag"]; },
             color: function (v, i) { return v === "No pattern tag" ? NOT_YET_COL : PALETTE[i % PALETTE.length]; } },
    status: { label: "Stage", title: "Claims by stage", sub: "Where each check stands, from candidate to published.",
             layout: "line", key: function (c) { return [c.status]; },
             order: function () { return ["Not started", "In progress", "Drafted", "Right of reply", "Published"]; },
             color: function (v) { return { "Not started": "#5d7468", "In progress": "#56b4e9", "Drafted": "#e3a72f", "Right of reply": "#f2994a", "Published": "#6fcf97" }[v] || "#7fa88b"; } },
    speaker: { label: "Who said it", title: "Claims by who made them", sub: "Every side is held to the same standard.",
             layout: "ring", key: function (c) { return [speakerGroup(c.speaker)]; },
             order: function () { return ["Government", "Regulators & agencies", "Political parties", "Business & developers", "NGOs & civil society", "Media", "EU & international", "Other"]; },
             color: function (v, i) { return PALETTE[i % PALETTE.length]; } },
    network: { label: "Links only", title: "The web of links", sub: "No groups: claims are pulled together by the themes that connect them.",
             layout: "force", key: function () { return []; }, order: function () { return []; }, color: function () { return "#7fa88b"; } }
  };
  var MODE_ORDER = ["topic", "subtopic", "verdict", "pattern", "status", "speaker", "network"];

  function rng(seed) {
    var h = 1779033703 ^ seed.length;
    for (var i = 0; i < seed.length; i++) { h = Math.imul(h ^ seed.charCodeAt(i), 3432918353); h = (h << 13) | (h >>> 19); }
    var a = h >>> 0;
    return function () { a |= 0; a = (a + 0x6D2B79F5) | 0; var t = Math.imul(a ^ (a >>> 15), 1 | a);
      t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t; return ((t ^ (t >>> 14)) >>> 0) / 4294967296; };
  }
  function el(tag, cls, text) { var e = document.createElement(tag); if (cls) e.className = cls; if (text != null) e.textContent = text; return e; }
  function rgba(hex, a) { var n = parseInt(hex.slice(1), 16); return "rgba(" + (n >> 16) + "," + ((n >> 8) & 255) + "," + (n & 255) + "," + a + ")"; }
  function iconSvg(name, color) {
    var ns = "http://www.w3.org/2000/svg", svg = document.createElementNS(ns, "svg"), p = document.createElementNS(ns, "path");
    svg.setAttribute("viewBox", "0 0 24 24"); svg.setAttribute("aria-hidden", "true"); p.setAttribute("d", ICONS[name] || ICONS[iconKey(name)] || "M12 12 h0");
    p.setAttribute("fill", "none"); p.setAttribute("stroke", color || "#fff"); p.setAttribute("stroke-width", "2.2");
    p.setAttribute("stroke-linecap", "round"); p.setAttribute("stroke-linejoin", "round"); svg.appendChild(p); return svg;
  }
  function drawLeaf(x, y, angle, size) {
    ctx.save(); ctx.translate(x, y); ctx.rotate(angle); ctx.beginPath(); ctx.moveTo(-size, 0);
    ctx.quadraticCurveTo(-size * .3, -size * .8, size, 0); ctx.quadraticCurveTo(-size * .3, size * .8, -size, 0);
    ctx.fill(); ctx.stroke(); ctx.restore();
  }
  function reviewAgeDays(dateText) {
    var stamp = Date.parse(dateText + "T00:00:00Z");
    return Number.isFinite(stamp) ? Math.max(0, Math.floor((Date.now() - stamp) / 86400000)) : 0;
  }
  function reviewLeafColor(age) {
    var t = Math.max(0, Math.min(1, age / 365)), fresh = [76, 164, 97], due = [145, 84, 48];
    return "rgb(" + fresh.map(function (v, i) { return Math.round(v + (due[i] - v) * t); }).join(",") + ")";
  }
  function roundRect(x, y, w, h, r) { ctx.beginPath(); ctx.moveTo(x + r, y); ctx.arcTo(x + w, y, x + w, y + h, r);
    ctx.arcTo(x + w, y + h, x, y + h, r); ctx.arcTo(x, y + h, x, y, r); ctx.arcTo(x, y, x + w, y, r); ctx.closePath(); }

  function resize() {
    dpr = window.devicePixelRatio || 1;
    W = stage.clientWidth; H = stage.clientHeight;
    canvas.width = W * dpr; canvas.height = H * dpr;
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  }

  // ------------------------------------------------------------ init
  function init(data) {
    DATA = data;
    data.themes.forEach(function (t) { themeById[t.id] = t; themeOn[t.id] = true; });
    data.claims.forEach(function (c) {
      var rnd = rng(c.id);
      var node = { kind: "claim", id: c.id, data: c, phase: rnd() * 6.28, x: (rnd() - .5) * 60, y: (rnd() - .5) * 60, z: (rnd() - .5) * 60,
                   tx: 0, ty: 0, tz: 0, hub: null, extra: [] };
      if (c.last_reviewed && c.outputs && (c.outputs.report || c.outputs.report_pdf) && (c.status === "Drafted" || c.status === "Published")) {
        node.reviewAgeDays = reviewAgeDays(c.last_reviewed); node.reviewLeafColor = reviewLeafColor(node.reviewAgeDays);
      }
      claims.push(node); byId[c.id] = node;
    });
    var pairCount = {};
    edges = data.edges.filter(function (e) { return byId[e.from] && byId[e.to]; }).map(function (e) {
      var key = [e.from, e.to].sort().join("|"); var k = pairCount[key] = (pairCount[key] || 0) + 1;
      return { kind: "edge", from: e.from, to: e.to, theme: e.theme, link_type: e.link_type, strength: e.strength,
               bend: 0.1 + 0.12 * (k - 1) * (k % 2 ? 1 : -1) };
    });
    var sr = rng("stars");
    for (var i = 0; i < 220; i++) stars.push({ x: sr(), y: sr(), r: sr() * 1.3 + 0.2, a: sr() * 0.32 + 0.04, tw: sr() * 6.28, d: sr() });
    buildStats(); buildGroupBy(); buildLinkBar(); buildKey(); buildTable(); resize();
    setMode(new URLSearchParams(location.search).get("group") || "topic", true);
    buildViewBy(); setHint();
    var wantMap = new URLSearchParams(location.search).get("view") === "map";
    try { if (!new URLSearchParams(location.search).get("view") && localStorage.getItem("mizien.view") === "map") wantMap = true; } catch (e) {}
    if (wantMap) { view = "map"; loadGeo(); }   // the island outlines load only when the map view is used
    requestAnimationFrame(frame);
  }

  function buildStats() {
    var s = document.getElementById("stats"); s.textContent = "";
    var withV = DATA.claims.filter(function (c) { return c.verdict; }).length;
    [[DATA.claims.length, "claims"], [withV, "with a verdict"], [DATA.edges.length, "links"], [DATA.themes.length, "themes"]].forEach(function (p) {
      var d = el("div"); d.appendChild(el("b", null, String(p[0]))); d.appendChild(document.createTextNode(p[1])); s.appendChild(d);
    });
  }

  // ------------------------------------------------------------ layouts
  function hubKey(m, v) { return m + "|" + v; }
  function getHub(m, v, i) {
    var k = hubKey(m, v);
    if (!hubPool[k]) hubPool[k] = { kind: "hub", key: k, mode: m, name: v, color: MODES[m].color(v, i), x: 0, y: 0, z: 0, tx: 0, ty: 0, tz: 0, alpha: 0, talpha: 0, claims: [] };
    return hubPool[k];
  }
  function spiral(n, i, r) { // even points on a sphere
    if (n === 1) return { x: 0, y: 0, z: 0 };
    var y = 1 - (i / (n - 1)) * 2, rad = Math.sqrt(Math.max(0, 1 - y * y)), th = Math.PI * (3 - Math.sqrt(5)) * i;
    return { x: Math.cos(th) * rad * r, y: y * r, z: Math.sin(th) * rad * r };
  }
  function clusterRadius(n) { return n <= 1 ? 0 : 34 + 15 * Math.sqrt(n); }

  function setMode(m, instant) {
    if (!MODES[m]) m = "topic";
    mode = m; var M = MODES[m];
    Object.keys(hubPool).forEach(function (k) { hubPool[k].talpha = 0; });
    claims.forEach(function (c) { c.hub = null; c.extra = []; c.sub = null; });
    var order = M.order(), groups = {};
    claims.forEach(function (c) {
      var keys = M.key(c.data);
      keys.forEach(function (v, j) { (groups[v] = groups[v] || []).push({ c: c, primary: j === 0 }); });
    });
    // unseen values (e.g. a new status) go at the end
    Object.keys(groups).forEach(function (v) { if (order.indexOf(v) < 0) order.push(v); });
    hubs = [];
    order.forEach(function (v, i) {
      var h = getHub(m, v, i); h.color = M.color(v, i); h.claims = []; h.reviewLeaves = [];
      var members = groups[v] || [];
      members.forEach(function (o) { if (o.primary) { o.c.hub = h; h.claims.push(o.c); if (o.c.reviewLeafColor) h.reviewLeaves.push(o.c); } else o.c.extra.push(h); });
      h.count = h.claims.length; h.empty = h.count === 0;
      if (M.layout === "force") return;
      if (h.empty && (m === "topic" || m === "subtopic" || m === "speaker" || m === "pattern")) return; // hide empty groups where order is not meaningful
      hubs.push(h);
    });
    buildSubHubs(m);
    // hub targets
    var n = hubs.length;
    if (M.layout === "sphere") {
      hubs.forEach(function (h, i) { var p = spiral(n, i, R * 1.05); h.tx = p.x; h.ty = p.y * 0.78; h.tz = p.z; });
    } else if (M.layout === "ring") {
      hubs.forEach(function (h, i) { var a = (i / n) * Math.PI * 2; h.tx = Math.cos(a) * R * 1.12; h.tz = Math.sin(a) * R * 1.12; h.ty = (i % 2 ? 1 : -1) * 34; });
    } else if (M.layout === "arc" || M.layout === "line") {
      var widths = hubs.map(function (h) { return Math.max(60, clusterRadius(h.count) + 46); });
      var total = widths.reduce(function (a, b) { return a + b * 2; }, 0) + (n - 1) * 22, x = -total / 2;
      hubs.forEach(function (h, i) {
        x += widths[i]; h.tx = x; x += widths[i] + 22;
        var u = n > 1 ? i / (n - 1) - 0.5 : 0;
        h.ty = M.layout === "arc" ? -60 * Math.cos(u * Math.PI) + 40 : (i % 2 ? 26 : -26);
        h.tz = M.layout === "arc" ? 120 * Math.cos(u * Math.PI) - 60 : 0;
        if (h.name === NOT_YET) { h.ty += 60; }
      });
      var scale = Math.min(1, (R * 3.5) / total); hubs.forEach(function (h) { h.tx *= scale; });
    }
    hubs.forEach(function (h) {
      if (h.alpha < 0.05) { // a new hub grows out of its members' current centroid
        var cs = h.claims.length ? h.claims : claims, sx = 0, sy = 0, sz = 0;
        cs.forEach(function (c) { sx += c.x; sy += c.y; sz += c.z; });
        h.x = sx / cs.length; h.y = sy / cs.length; h.z = sz / cs.length;
      }
      h.talpha = 1;
      layoutMembers(h, false);
    });
    if (M.layout === "force") forceLayout();
    // camera: carousels spin, spectra and pipelines face the viewer and sway
    sway = M.layout === "arc" || M.layout === "line";
    if (sway) { cam.tyaw = 0; cam.tpitch = -0.12; } else { cam.tyaw = null; cam.tpitch = M.layout === "ring" ? -0.38 : -0.22; }
    if (instant) { claims.concat(hubs, subHubs).forEach(function (n) { n.x = n.tx; n.y = n.ty; n.z = n.tz; }); hubs.concat(subHubs).forEach(function (h) { h.alpha = 1; }); }
    if (view === "map") mapifyMode();
    clearSel();
    var mt = document.getElementById("modeTitle"); mt.querySelector(".t").textContent = M.title; mt.querySelector(".s").textContent = M.sub;
    document.querySelectorAll("#groupby button").forEach(function (b) { b.setAttribute("aria-pressed", b.dataset.mode === m ? "true" : "false"); });
    buildGroups();
    var u = new URL(location.href); if (m === "topic") u.searchParams.delete("group"); else u.searchParams.set("group", m);
    history.replaceState(null, "", u);
  }

  // Topic view: a topic whose claims carry two or more subtopics gets a small hub per subtopic, orbiting it.
  function getSubHub(h, s) {
    var k = "topic-sub|" + h.name + " · " + s;
    if (!hubPool[k]) hubPool[k] = { kind: "hub", sub: true, key: k, mode: "topic", name: s, x: h.x, y: h.y, z: h.z, tx: h.x, ty: h.y, tz: h.z, alpha: 0, talpha: 0, claims: [] };
    var sh = hubPool[k]; sh.parent = h; sh.color = mix(h.color, "#ffffff", 0.3); return sh;
  }
  function buildSubHubs(m) {
    subHubs = [];
    hubs.forEach(function (h) {
      h.subs = [];
      if (m !== "topic") return;
      var by = {}, names = [];
      h.claims.forEach(function (c) { var s = c.data.subtopic; if (!s) return; if (!by[s]) { by[s] = []; names.push(s); } by[s].push(c); });
      if (names.length < 2) return; // one subtopic adds nothing: the topic stays a single cluster
      names.sort().forEach(function (s) {
        var sh = getSubHub(h, s); sh.claims = by[s]; sh.count = sh.claims.length; sh.empty = false; sh.reviewLeaves = [];
        sh.claims.forEach(function (c) { c.sub = sh; });
        h.subs.push(sh); subHubs.push(sh);
      });
    });
  }
  function layoutWithSubs(h, open) {
    var subs = h.subs, ns = subs.length, byClaimId = function (a, b) { return a.id < b.id ? -1 : 1; };
    var rs = open ? Math.max(120, 56 + 26 * ns + 6 * Math.sqrt(h.count)) : 24 + 9 * ns + 6 * Math.sqrt(h.count), reach = 0;
    subs.forEach(function (sh, i) {
      var a = (i / ns) * Math.PI * 2 - Math.PI / 2;
      var p = open ? { x: Math.cos(a) * rs, y: Math.sin(a) * rs * 0.82, z: Math.sin(a * 2) * rs * 0.18 } : spiral(ns, i, rs);
      sh.tx = h.tx + p.x; sh.ty = h.ty + p.y; sh.tz = h.tz + p.z; sh.talpha = 1;
      var len = Math.hypot(p.x, p.y, p.z) || 1, out = { x: p.x / len, y: p.y / len, z: p.z / len };
      var m = sh.claims.length, r = open ? Math.max(46, 24 + 18 * Math.sqrt(m)) : 10 + 8 * Math.sqrt(m);
      sh.claims.slice().sort(byClaimId).forEach(function (c, j) {
        var q;
        if (m === 1) q = { x: out.x * r, y: out.y * r, z: out.z * r };       // a lone claim sits just outside its sub-hub
        else if (open) { var spread = Math.min(Math.PI * 1.15, 0.45 + 0.3 * m), b = a + (j / (m - 1) - 0.5) * spread;
          q = { x: Math.cos(b) * r, y: Math.sin(b) * r * 0.82, z: 0 }; }     // fan outward, away from the topic centre
        else q = spiral(m, j, r);
        c.tx = sh.tx + q.x; c.ty = sh.ty + q.y; c.tz = sh.tz + q.z;
      });
      reach = Math.max(reach, r);
    });
    var loose = h.claims.filter(function (c) { return !c.sub; }).sort(byClaimId), nl = loose.length, rl = open ? 46 : 16;
    loose.forEach(function (c, i) { var q = nl === 1 ? { x: 0, y: rl, z: 0 } : spiral(nl, i, rl); c.tx = h.tx + q.x; c.ty = h.ty + q.y; c.tz = h.tz + q.z; });
    h.ringR = rs; h.openR = rs + reach;
  }
  function layoutMembers(h, open) {
    if (h.subs && h.subs.length) return layoutWithSubs(h, open);
    h.ringR = null;
    var n = h.claims.length, r = clusterRadius(n);
    if (open) r = Math.max(110, r * 2.3);
    h.claims.slice().sort(function (a, b) { return a.id < b.id ? -1 : 1; }).forEach(function (c, i) {
      var p;
      if (open && n > 1) { var a = (i / n) * Math.PI * 2 - Math.PI / 2; p = { x: Math.cos(a) * r, y: Math.sin(a) * r * 0.82, z: Math.sin(a * 2) * r * 0.18 }; }
      else p = spiral(n, i, r);
      c.tx = h.tx + p.x; c.ty = h.ty + p.y; c.tz = h.tz + p.z;
      if (n === 1) c.ty += open ? 90 : 46;
    });
    h.openR = r;
  }
  function expandHub(h) {
    if (h.sub) h = h.parent;
    if (expanded === h) return;
    if (expanded) layoutMembers(expanded, false);
    expanded = h; layoutMembers(h, true);
    cam.tem = Math.max(1.15, Math.min(2.4, 175 / (h.openR || 110)));
    var cr = document.getElementById("crumb"); cr.textContent = "";
    cr.appendChild(document.createTextNode(MODES[mode].label + " · ")); cr.appendChild(el("b", null, h.name));
    cr.appendChild(document.createTextNode(" · " + h.count + (h.count === 1 ? " claim" : " claims")));
    var back = el("button", null, "Show all groups"); back.type = "button"; back.onclick = function () { clearSel(); }; cr.appendChild(back);
    cr.style.display = "inline-flex";
  }
  function collapse() {
    if (!expanded) return;
    layoutMembers(expanded, false); expanded = null; cam.tem = 1;
    document.getElementById("crumb").style.display = "none";
  }

  function forceLayout() {
    var rnd = rng("force"), n = claims.length, P = claims.map(function (c) { return { x: c.x + rnd() * 4, y: c.y + rnd() * 4, z: c.z + rnd() * 4, vx: 0, vy: 0, vz: 0 }; });
    var idx = {}; claims.forEach(function (c, i) { idx[c.id] = i; });
    for (var it = 0; it < 420; it++) {
      var cool = 1 - it / 420;
      for (var i = 0; i < n; i++) for (var j = i + 1; j < n; j++) {
        var dx = P[i].x - P[j].x, dy = P[i].y - P[j].y, dz = P[i].z - P[j].z, d2 = dx * dx + dy * dy + dz * dz + 25, f = 5200 / d2;
        var d = Math.sqrt(d2); dx /= d; dy /= d; dz /= d;
        P[i].vx += dx * f; P[i].vy += dy * f; P[i].vz += dz * f; P[j].vx -= dx * f; P[j].vy -= dy * f; P[j].vz -= dz * f;
      }
      edges.forEach(function (e) {
        var a = P[idx[e.from]], b = P[idx[e.to]], dx = b.x - a.x, dy = b.y - a.y, dz = b.z - a.z, d = Math.sqrt(dx * dx + dy * dy + dz * dz) + .01;
        var f = (d - 105) * 0.012; dx /= d; dy /= d; dz /= d;
        a.vx += dx * f * d * .02; a.vy += dy * f * d * .02; a.vz += dz * f * d * .02;
        b.vx -= dx * f * d * .02; b.vy -= dy * f * d * .02; b.vz -= dz * f * d * .02;
      });
      P.forEach(function (p) { p.vx -= p.x * 0.012; p.vy -= p.y * 0.012; p.vz -= p.z * 0.012;
        p.x += p.vx * 0.5 * cool; p.y += p.vy * 0.5 * cool; p.z += p.vz * 0.5 * cool; p.vx *= .55; p.vy *= .55; p.vz *= .55; });
    }
    var mx = 0; P.forEach(function (p) { mx = Math.max(mx, Math.hypot(p.x, p.y, p.z)); });
    var s = (R * 1.35) / (mx || 1);
    claims.forEach(function (c, i) { c.tx = P[i].x * s; c.ty = P[i].y * s * 0.8; c.tz = P[i].z * s; });
  }

  // ------------------------------------------------------------ chrome
  function buildGroupBy() {
    var g = document.getElementById("groupby"); g.textContent = "";
    MODE_ORDER.forEach(function (m) {
      var b = el("button"); b.type = "button"; b.dataset.mode = m; b.appendChild(iconSvg("mode:" + m, "#eef3ef"));
      b.appendChild(document.createTextNode(MODES[m].label)); b.onclick = function () { setMode(m); }; g.appendChild(b);
    });
  }
  function buildGroups() {
    var g = document.getElementById("groups"), note = document.getElementById("groupnote"); g.textContent = ""; note.textContent = "";
    document.getElementById("groupsTitle").textContent = mode === "network" ? "ISOLATED CLAIMS" : MODES[mode].label.toUpperCase() + " GROUPS";
    if (mode === "network") {
      var lone = claims.filter(function (c) { return !edges.some(function (e) { return e.from === c.id || e.to === c.id; }); });
      lone.forEach(function (c) { var b = el("button"); b.type = "button"; var s = el("span", "sw"); s.style.background = c.data.verdict ? VC[c.data.verdict] : NOT_YET_COL;
        b.appendChild(s); b.appendChild(el("span", null, c.id + " " + c.data.title)); b.onclick = function () { selectClaim(c.id); }; g.appendChild(b); });
      note.textContent = lone.length ? "Not yet linked to any other claim." : "Every claim is linked to at least one other.";
      return;
    }
    hubs.forEach(function (h) {
      var b = el("button"); b.type = "button"; var s = el("span", "sw"); s.style.background = h.color; s.appendChild(iconSvg(h.name));
      b.appendChild(s); b.appendChild(el("span", null, h.name)); b.appendChild(el("span", "n", String(h.count)));
      b.onclick = function () { selectHub(h); }; g.appendChild(b);
    });
    if (mode === "pattern") note.textContent = "Tags are provisional until a report is finished.";
    if (mode === "speaker") note.textContent = "Grouped by the first body named as speaker.";
  }
  function buildLinkBar() {
    var bar = document.getElementById("linkbar"); bar.textContent = "";
    bar.appendChild(el("span", "kicker", "LINES"));
    var sp = el("button"); sp.type = "button"; sp.appendChild(el("span", "ln")).style.borderColor = "rgba(207,226,212,.55)";
    sp.appendChild(document.createTextNode("Group spokes")); sp.setAttribute("aria-pressed", "true");
    sp.onclick = function () { showSpokes = !showSpokes; sp.classList.toggle("off", !showSpokes); sp.setAttribute("aria-pressed", showSpokes); };
    bar.appendChild(sp); bar.appendChild(el("span", "sep"));
    var themeBtns = [];
    DATA.themes.forEach(function (t) {
      var b = el("button"); b.type = "button"; b.title = t.description || t.name; b.setAttribute("aria-pressed", "true");
      var l = el("span", "ln"); l.style.borderColor = t.color; if (t.dashed) l.style.borderTopStyle = "dashed";
      b.appendChild(l); b.appendChild(document.createTextNode(t.name));
      b.onclick = function (e) {
        if (e.shiftKey || e.altKey) { selectTheme(t.id); return; }
        themeOn[t.id] = !themeOn[t.id]; b.classList.toggle("off", !themeOn[t.id]); b.setAttribute("aria-pressed", themeOn[t.id]);
      };
      b.ondblclick = function () { selectTheme(t.id); };
      themeBtns.push([t.id, b]); bar.appendChild(b);
    });
    bar.appendChild(el("span", "sep"));
    function all(v) { themeBtns.forEach(function (p) { themeOn[p[0]] = v; p[1].classList.toggle("off", !v); p[1].setAttribute("aria-pressed", v); }); }
    var on = el("button", "mini", "All"); on.type = "button"; on.onclick = function () { all(true); }; bar.appendChild(on);
    var off = el("button", "mini", "None"); off.type = "button"; off.onclick = function () { all(false); }; bar.appendChild(off);
  }
  function buildKey() {
    var k = document.getElementById("vkey"); k.textContent = "";
    Object.keys(VC).concat([NOT_YET]).forEach(function (v) {
      var s = el("span"), d = el("span", "vdot" + (VC[v] ? "" : " open")); d.style.background = VC[v] || NOT_YET_COL;
      s.appendChild(d); s.appendChild(document.createTextNode(v)); k.appendChild(s);
    });
  }
  function verdictClass(v) { return "v-" + (v ? v.toLowerCase().replace(/[^a-z]+/g, "-") : "none"); }
  function buildTable() {
    var tb = document.querySelector("#claims tbody");
    // Rows rendered on the server link to each claim page; clicking elsewhere on a row shows it on the map.
    function showOnMap(tr, id) {
      var go = function () { selectClaim(id); stage.scrollIntoView({ behavior: "smooth", block: "center" }); };
      tr.classList.add("click"); tr.tabIndex = 0;
      tr.addEventListener("click", function (e) { if (!e.target.closest("a")) go(); });
      tr.addEventListener("keydown", function (e) { if (e.key === "Enter" && e.target === tr) go(); });
    }
    var rows = tb.querySelectorAll("tr[data-id]");
    if (rows.length) { rows.forEach(function (tr) { showOnMap(tr, tr.dataset.id); }); return; }
    DATA.claims.forEach(function (c) {
      var tr = el("tr");
      tr.appendChild(el("td", null, c.id)); tr.appendChild(el("td", null, c.category)); tr.appendChild(el("td", null, c.title));
      var td = el("td"); td.appendChild(el("span", "chip " + verdictClass(c.verdict), c.verdict ? c.verdict : c.status));
      if (c.verdict) td.appendChild(el("span", "muted", " " + c.status));
      tr.appendChild(td); showOnMap(tr, c.id);
      tb.appendChild(tr);
    });
  }

  // ------------------------------------------------------------ projection
  function leftInset() { return W > 900 ? 270 : 0; }
  function panelOpen() { return W > 900 && panel.style.display === "block"; }
  function panelInset() { return panelOpen() && !wide ? panel.offsetWidth + 22 : 0; }
  function topInset() { return panelOpen() && wide ? Math.min(H * 0.55, panel.offsetTop + panel.offsetHeight) : 0; }
  var cyNow = null;
  function cyTarget() { var top = topInset(); return top ? (top + H - 40) / 2 : (H - sheetInset()) / 2 + 6; }
  var cxNow = null;
  function cxTarget() { return leftInset() + (W - leftInset() - panelInset()) / 2; }
  function baseScale() {
    var usable = Math.min(W - leftInset() - panelInset(), H - 120 - topInset());
    return view === "map"   // fit the archipelago (about 520 x 440 world units) to the free area
      ? Math.max(0.3, Math.min((W - leftInset() - panelInset()) * 0.92 / 520, (H - 120 - topInset()) * 0.92 / 440))
      : Math.max(0.6, usable / 400);
  }
  // Node size: grows only gently with zoom and the lens (zoom^0.3), capped, so pins never blow up on any screen.
  function nodeScale(p) {
    var zf = cam.zoom * cam.em, rel = p.s / zf;                     // size the node would have at zoom 1
    var phone = W < 700 ? 0.85 : 1;
    return Math.max(0.6, Math.min(view === "map" ? 1.9 : 2.3, rel * 1.1 * Math.pow(zf, 0.3) * phone * (view === "map" ? 0.82 : 1)));
  }
  function project(p) {
    var cy = Math.cos(cam.yaw), sy = Math.sin(cam.yaw), cp = Math.cos(cam.pitch), sp = Math.sin(cam.pitch);
    var px = p.x - cam.fx, py = p.y - cam.fy, pz = p.z - cam.fz;
    var x1 = px * cy - pz * sy, z1 = px * sy + pz * cy;
    var y2 = py * cp - z1 * sp, z2 = py * sp + z1 * cp;
    var F = 900, s = view === "map" ? 1 : F / (F + z2 + 300);   // the map is orthographic, so transitions fold exactly
    var base = baseScale() * cam.zoom * cam.em;
    var sx = cxNow + cam.px + x1 * s * base, sy = cyNow + cam.py + y2 * s * base, sc = s * base;
    if (lensK > 0.01) { var ldx = sx - cxNow, ldy = sy - cyNow, lr = Math.hypot(ldx, ldy), LR = lensR();
      if (lr < LR) { var D = LENS_D * lensK, lx = lr / LR, f = (D + 1) / (D * lx + 1), dv = f / (D * lx + 1);
        sx = cxNow + ldx * f; sy = cyNow + ldy * f; sc *= Math.pow(f * dv, 0.35); } }
    return { sx: sx, sy: sy, z: z2, s: sc };
  }
  function ctrl(a, b, bend) {
    var mx = (a.sx + b.sx) / 2, my = (a.sy + b.sy) / 2, dx = b.sx - a.sx, dy = b.sy - a.sy;
    var nx = -dy, ny = dx, side = ((mx - cxNow) * nx + (my - cyNow) * ny) >= 0 ? 1 : -1;
    return { x: mx + nx * bend * side, y: my + ny * bend * side };
  }
  function qpt(g, s) { var u = 1 - s; return { x: u * u * g.a.sx + 2 * u * s * g.c.x + s * s * g.b.sx, y: u * u * g.a.sy + 2 * u * s * g.c.y + s * s * g.b.sy }; }

  function focusSet() {
    if (!sel) return null;
    var ids = {}, es = {}, hb = null;
    if (sel.kind === "claim") { ids[sel.id] = 1; edges.forEach(function (e, i) { if (themeOn[e.theme] && (e.from === sel.id || e.to === sel.id)) { es[i] = 1; ids[e.from] = ids[e.to] = 1; } }); }
    if (sel.kind === "hub") { hb = sel.hub; (sel.hub.claims || []).forEach(function (c) { ids[c.id] = 1; }); claims.forEach(function (c) { if (c.extra.indexOf(sel.hub) >= 0) ids[c.id] = 1; }); }
    if (sel.kind === "edge") { es[sel.index] = 1; ids[sel.edge.from] = ids[sel.edge.to] = 1; }
    if (sel.kind === "theme") edges.forEach(function (e, i) { if (e.theme === sel.id) { es[i] = 1; ids[e.from] = ids[e.to] = 1; } });
    if (sel.kind === "place") sel.place.claims.forEach(function (c) { ids[c.id] = 1; edges.forEach(function (e, i) { if (themeOn[e.theme] && (e.from === c.id || e.to === c.id)) es[i] = 1; }); });
    return { ids: ids, es: es, hub: hb };
  }

  // ------------------------------------------------------------ render loop
  function frame(now) {
    var t = (now - t0) / 1000, dt = Math.max(0, Math.min(0.4, t - lastT)); lastT = t;
    var k = reduce ? 1 : 1 - Math.pow(0.04, dt);            // morph easing, frame-rate independent
    lensK += ((lensWanted() ? 1 : 0) - lensK) * Math.min(1, k * 1.5);
    cam.px += (cam.tpx - cam.px) * Math.min(1, k * 1.6); cam.py += (cam.tpy - cam.py) * Math.min(1, k * 1.6);
    if (view === "map") { stepMapAnim(dt); mapTargets(); }
    var kc = view === "map" ? (mapAnim ? 1 : Math.min(1, k * 2.4)) : k;
    claims.forEach(function (c) { c.x += (c.tx - c.x) * kc; c.y += (c.ty - c.y) * kc; c.z += (c.tz - c.z) * kc; });
    Object.keys(hubPool).forEach(function (key) { var h = hubPool[key];
      h.x += (h.tx - h.x) * k; h.y += (h.ty - h.y) * k; h.z += (h.tz - h.z) * k; h.alpha += (h.talpha - h.alpha) * Math.min(1, k * 1.3); });
    if (cxNow === null) cxNow = cxTarget(); cxNow += (cxTarget() - cxNow) * Math.min(1, k * 1.2);
    if (cyNow === null) cyNow = cyTarget(); cyNow += (cyTarget() - cyNow) * Math.min(1, k * 1.2);
    var fxT = expanded ? expanded.x : 0, fyT = expanded ? expanded.y : 0, fzT = expanded ? expanded.z : 0;
    if (expanded) { var avail = Math.min(W - leftInset() - panelInset(), H - 120 - topInset() - sheetInset()), b0 = Math.max(0.6, avail / 400) * cam.zoom;
      cam.tem = Math.max(1, Math.min(3.4, 0.34 * avail / ((expanded.openR || 110) * b0 * 0.75))); }
    cam.fx += (fxT - cam.fx) * k; cam.fy += (fyT - cam.fy) * k; cam.fz += (fzT - cam.fz) * k; cam.em += (cam.tem - cam.em) * k;
    if (view === "map") { if (cam.tyaw !== null) cam.yaw += (cam.tyaw - cam.yaw) * k * 0.6; }
    else if (sway) { var target = cam.tyaw + (spinning ? 0.32 * Math.sin(t * 0.18) : 0); cam.yaw += (target - cam.yaw) * k * 0.6; }
    else if (spinning) cam.yaw += (expanded ? 0.04 : 0.13) * Math.min(dt, 0.05);
    cam.pitch += (cam.tpitch - cam.pitch) * k * 0.5;

    ctx.clearRect(0, 0, W, H);
    stars.forEach(function (s) {
      ctx.globalAlpha = s.a * (0.65 + 0.35 * Math.sin(t * 0.7 + s.tw));
      ctx.fillStyle = s.d > .85 ? "#f6e3b4" : "#cfe2d4";
      var px = (s.x * W + cam.yaw * 30 * s.d) % W; if (px < 0) px += W;
      ctx.beginPath(); ctx.arc(px, s.y * H, s.r, 0, 6.283); ctx.fill();
    });
    ctx.globalAlpha = 1;
    if (view === "map") drawMap(t);
    if (lensK > 0.01) { var LR0 = lensR();
      ctx.save(); ctx.globalAlpha = lensK; ctx.strokeStyle = "rgba(227,167,47,.45)"; ctx.lineWidth = 1.5;
      ctx.beginPath(); ctx.arc(cxNow, cyNow, LR0, 0, 6.283); ctx.stroke();
      var lg = ctx.createRadialGradient(cxNow, cyNow, LR0 * 0.9, cxNow, cyNow, LR0 * 1.04);
      lg.addColorStop(0, "rgba(227,167,47,0)"); lg.addColorStop(1, "rgba(227,167,47,.12)"); ctx.fillStyle = lg;
      ctx.beginPath(); ctx.arc(cxNow, cyNow, LR0 * 1.04, 0, 6.283); ctx.fill(); ctx.restore(); }

    var allHubs = Object.keys(hubPool).map(function (k) { return hubPool[k]; }).filter(function (h) { return h.alpha > 0.01; });
    var P = new Map(); allHubs.concat(claims).forEach(function (n) { P.set(n, project(n)); });
    var F = focusSet(), labels = [];
    function fog(p) { return Math.max(0.35, Math.min(1, 1.05 - p.z / 900)); }

    // orbit rings around active hubs
    allHubs.forEach(function (h) {
      if (!h.count || h.sub) return; var p = P.get(h), r = (h.ringR || clusterRadius(h.count) + 10) * p.s;
      ctx.save(); ctx.globalAlpha = h.alpha * (F && F.hub !== h ? 0.08 : 0.22) * fog(p); ctx.strokeStyle = h.color; ctx.lineWidth = 1;
      ctx.setLineDash([2, 6]); ctx.beginPath(); ctx.ellipse(p.sx, p.sy, r, r * (0.32 + 0.5 * Math.abs(Math.sin(cam.pitch))), 0, 0, 6.283); ctx.stroke(); ctx.restore();
    });

    // spokes: claim to its group (and faint spokes to secondary groups)
    if (showSpokes && mode !== "network" && view === "graph") subHubs.forEach(function (sh) {
      if (sh.alpha < 0.02 || sh.parent.alpha < 0.02) return;
      var a = P.get(sh.parent), b = P.get(sh), on = F && (F.hub === sh || F.hub === sh.parent || sh.claims.some(function (c) { return F.ids[c.id]; }));
      ctx.strokeStyle = rgba(sh.parent.color, 0.5 * sh.alpha * (F && !on ? 0.35 : 1)); ctx.lineWidth = on ? 2.4 : 1.8;
      ctx.beginPath(); ctx.moveTo(a.sx, a.sy); ctx.lineTo(b.sx, b.sy); ctx.stroke();
    });
    if (showSpokes && mode !== "network" && view === "graph") claims.forEach(function (c) {
      [c.sub && c.sub.alpha > 0.02 ? c.sub : c.hub].concat(c.extra).forEach(function (h, j) {
        if (!h || h.alpha < 0.02) return;
        var a = P.get(h), b = P.get(c), on = F && (F.hub === h || F.ids[c.id]);
        var g = ctx.createLinearGradient(a.sx, a.sy, b.sx, b.sy);
        var al = (j ? 0.18 : 0.42) * h.alpha * (F && !on ? 0.35 : 1);
        g.addColorStop(0, rgba(h.color, al)); g.addColorStop(1, rgba(h.color, al * 0.25));
        ctx.strokeStyle = g; ctx.lineWidth = on ? 2 : 1.4; ctx.setLineDash(j ? [3, 5] : []);
        ctx.beginPath(); ctx.moveTo(a.sx, a.sy);
        ctx.quadraticCurveTo((a.sx + b.sx) / 2 + Math.sin(t * 0.8 + c.phase) * 7, (a.sy + b.sy) / 2 - 6, b.sx, b.sy); ctx.stroke();
      });
    });
    ctx.setLineDash([]);

    // theme links
    edges.forEach(function (e, i) {
      e._g = null; if (!themeOn[e.theme]) return;
      var a = P.get(byId[e.from]), b = P.get(byId[e.to]), c = ctrl(a, b, e.bend);
      e._g = { a: a, b: b, c: c };
      var hi = F && F.es[i], hv = hover && hover.kind === "edge" && hover.index === i;
      var depth = Math.min(fog(a), fog(b)), col = (themeById[e.theme] || {}).color || "#7fa88b";
      var weak = e.strength && (e.strength.indexOf("Weak") === 0 || e.strength.indexOf("Pattern") === 0);
      ctx.setLineDash(weak ? [6, 5] : []);
      ctx.strokeStyle = rgba(col, hi || hv ? 0.4 : (F ? 0.03 : 0.1)); ctx.lineWidth = hi || hv ? 12 : 6;
      ctx.beginPath(); ctx.moveTo(a.sx, a.sy); ctx.quadraticCurveTo(c.x, c.y, b.sx, b.sy); ctx.stroke();
      ctx.strokeStyle = col; ctx.globalAlpha = hi || hv ? 1 : (F ? 0.1 : (view === "map" ? 0.38 : 0.7) * depth); ctx.lineWidth = hi || hv ? 3 : (view === "map" ? 1.3 : 1.7);
      if (hi && weak) ctx.lineDashOffset = -t * 18;
      ctx.beginPath(); ctx.moveTo(a.sx, a.sy); ctx.quadraticCurveTo(c.x, c.y, b.sx, b.sy); ctx.stroke();
      ctx.lineDashOffset = 0; ctx.globalAlpha = 1;
      if ((hi || hv) && !reduce) { // particles travelling along highlighted links
        ctx.setLineDash([]); ctx.fillStyle = "#fff";
        for (var q = 0; q < 3; q++) { var s = ((t * 0.35 + q / 3 + i * 0.07) % 1), pt = qpt(e._g, s);
          ctx.globalAlpha = 0.9 * Math.sin(s * Math.PI); ctx.beginPath(); ctx.arc(pt.x, pt.y, 2.4, 0, 6.283); ctx.fill(); }
        ctx.globalAlpha = 1;
      }
    });
    ctx.setLineDash([]);

    // nodes, far to near
    var items = allHubs.concat(claims).sort(function (m, n) { return P.get(n).z - P.get(m).z; });
    items.forEach(function (n) {
      var p = P.get(n), isHub = n.kind === "hub", sc = nodeScale(p), fg = fog(p);
      var on = !F || (isHub ? F.hub === n || n.claims.some(function (c) { return F.ids[c.id]; }) : F.ids[n.id]);
      var isSel = sel && ((isHub && sel.hub === n) || (!isHub && sel.kind === "claim" && sel.id === n.id));
      var isHov = hover && ((isHub && hover.hub === n) || (!isHub && hover.kind === "claim" && hover.id === n.id));
      if (isHub) {
        var a = n.alpha * (on ? 1 : 0.3), r = (n.sub ? 12 : 23) * sc * (isHov ? 1.08 : 1) * (0.6 + 0.4 * n.alpha);
        ctx.globalAlpha = a;
        var g = ctx.createRadialGradient(p.sx, p.sy, r * 0.5, p.sx, p.sy, r * 3);
        g.addColorStop(0, rgba(n.color, n.sub ? 0.32 : 0.5)); g.addColorStop(1, rgba(n.color, 0));
        ctx.fillStyle = g; ctx.beginPath(); ctx.arc(p.sx, p.sy, r * 3, 0, 6.283); ctx.fill();
        var g2 = ctx.createRadialGradient(p.sx - r * .35, p.sy - r * .4, r * .1, p.sx, p.sy, r);
        g2.addColorStop(0, rgba("#ffffff", 0.55)); g2.addColorStop(0.25, n.color); g2.addColorStop(1, rgba(n.color, 0.85));
        ctx.fillStyle = g2; ctx.beginPath(); ctx.arc(p.sx, p.sy, r, 0, 6.283); ctx.fill();
        ctx.strokeStyle = isSel ? "#fff" : "rgba(255,255,255,.6)"; ctx.lineWidth = isSel ? 3 : 1.5; ctx.stroke();
        var ip = ICON_PATHS[iconKey(n.sub ? n.parent.name : n.name)];
        if (ip) { ctx.save(); var s2 = r * 1.15 / 24; ctx.translate(p.sx - 12 * s2, p.sy - 12 * s2); ctx.scale(s2, s2);
          ctx.strokeStyle = "rgba(10,30,20,.9)"; ctx.lineWidth = 2.3; ctx.lineCap = "round"; ctx.lineJoin = "round"; ctx.stroke(ip); ctx.restore(); }
        (n.reviewLeaves || []).forEach(function (rv, ri) {
          var count = n.reviewLeaves.length, ang = -Math.PI / 2 + (ri - (count - 1) / 2) * .42;
          ctx.fillStyle = rv.reviewLeafColor; ctx.strokeStyle = "rgba(246,244,238,.85)"; ctx.lineWidth = 1;
          drawLeaf(p.sx + Math.cos(ang) * r * 1.5, p.sy + Math.sin(ang) * r * 1.5, ang + Math.PI / 2, 6);
        });
        n._p = { x: p.sx, y: p.sy, r: r, live: n.alpha > 0.5 };
        if (n.sub) { if (n.alpha > 0.3 && ((expanded ? expanded === n.parent : cam.zoom >= 1.8) || isHov || isSel)) labels.push({ x: p.sx, y: p.sy + r + 13, text: n.name,
          sub: n.count + (n.count === 1 ? " claim" : " claims"), hub: true, small: true, color: n.color, alpha: a, pri: expanded === n.parent || isSel || isHov ? 3.6 : 1.5 }); }
        else if (n.alpha > 0.3 && n !== expanded) labels.push({ x: p.sx, y: p.sy + r + 15, text: n.name, sub: n.count + (n.count === 1 ? " claim" : " claims"),
          hub: true, color: n.color, alpha: a * (expanded ? 0.45 : 1), pri: expanded ? 1 : 3 + (isSel ? 2 : 0) });
        ctx.globalAlpha = 1;
      } else {
        var d = n.data, col = d.verdict ? VC[d.verdict] : NOT_YET_COL, ring = n.hub && mode !== "network" ? n.hub.color : "#cfe2d4";
        var r2 = 9 * sc * (isHov || isSel ? 1.3 : 1) * (n.clustered ? 0.55 : 1), pulse = d.verdict && !reduce ? 1 + 0.07 * Math.sin(t * 2 + n.phase) : 1;
        ctx.globalAlpha = (on ? 1 : 0.18) * fg * (n.offmap ? 0.75 : 1);
        if (view === "map" && n.anchor) { var gp = project(n.anchor);
          ctx.fillStyle = "rgba(0,0,0,.35)"; ctx.beginPath(); ctx.ellipse(gp.sx, gp.sy, 4 * sc, 1.8 * sc, 0, 0, 6.283); ctx.fill();
          ctx.strokeStyle = n.offmap ? "rgba(207,226,212,.35)" : rgba(col, 0.8); ctx.lineWidth = 1.4; ctx.setLineDash(n.offmap ? [3, 4] : []);
          ctx.beginPath(); ctx.moveTo(gp.sx, gp.sy); ctx.lineTo(p.sx, p.sy); ctx.stroke(); ctx.setLineDash([]);
          if (!n.offmap) { ctx.fillStyle = col; ctx.beginPath(); ctx.arc(gp.sx, gp.sy, 2.4, 0, 6.283); ctx.fill(); } }
        if (d.verdict) { var gh = ctx.createRadialGradient(p.sx, p.sy, r2, p.sx, p.sy, r2 * 2.8 * pulse);
          gh.addColorStop(0, rgba(col, 0.55)); gh.addColorStop(1, rgba(col, 0)); ctx.fillStyle = gh;
          ctx.beginPath(); ctx.arc(p.sx, p.sy, r2 * 2.8 * pulse, 0, 6.283); ctx.fill(); }
        var g3 = ctx.createRadialGradient(p.sx - r2 * .4, p.sy - r2 * .4, r2 * .1, p.sx, p.sy, r2);
        g3.addColorStop(0, rgba("#ffffff", 0.5)); g3.addColorStop(0.35, col); g3.addColorStop(1, col);
        ctx.fillStyle = g3; ctx.beginPath(); ctx.arc(p.sx, p.sy, r2, 0, 6.283); ctx.fill();
        ctx.strokeStyle = ring; ctx.lineWidth = 2.6; ctx.beginPath(); ctx.arc(p.sx, p.sy, r2 + 1.6, 0, 6.283); ctx.stroke();
        if (!d.verdict) { ctx.setLineDash([2, 3]); ctx.strokeStyle = "rgba(255,255,255,.7)"; ctx.lineWidth = 1.1;
          ctx.beginPath(); ctx.arc(p.sx, p.sy, r2 + 4.6, 0, 6.283); ctx.stroke(); ctx.setLineDash([]); }
        if (isSel) { ctx.strokeStyle = "#fff"; ctx.lineWidth = 1.6; ctx.beginPath(); ctx.arc(p.sx, p.sy, r2 + 7 + 1.5 * Math.sin(t * 3), 0, 6.283); ctx.stroke(); }
        n._p = { x: p.sx, y: p.sy, r: r2 + 3, live: !n.clustered };
        var focused = F && F.ids[n.id];
        var member = expanded && n.hub === expanded, tagged = labelMode === "tag" || member;
        var hp = member ? P.get(n.sub && n.sub.alpha > 0.3 ? n.sub : expanded) : null, ddx = hp ? p.sx - hp.sx : 0, ddy = hp ? p.sy - hp.sy : 1, dl = Math.hypot(ddx, ddy) || 1;
        if ((!expanded || member || isHov || isSel) && !n.clustered) labels.push({ x: p.sx, y: p.sy + r2 + 13, text: (tagged ? d.title : n.id) + (n.offmap && n.ringFirst && n.data.location && W >= 700 ? "  → " + shortPlace(n.data.location.place) : ""),
          sub: (isHov || isSel || (member && W > 700)) ? (tagged ? d.id + (d.verdict ? " · " + d.verdict : " · not yet checked") : d.title) : "",
          hub: false, tag: tagged, color: col, alpha: (on ? 1 : 0.25) * fg, ax: p.sx, ay: p.sy, rr: r2 + 6,
          dir: member && expanded.claims.length > 1 ? { x: ddx / dl, y: ddy / dl } : null,
          pri: isSel || isHov ? 4 : member ? 3.5 : focused ? 2 : p.s > 0.9 ? 1 : 0 });
        ctx.globalAlpha = 1;
      }
    });

    // labels last, highest priority first, skipping overlaps so hub titles always stay readable
    if (!showText) labels = [];
    labels.sort(function (a, b) { return b.pri - a.pri; });
    var placed = [];
    labels.forEach(function (L) {
      var titleFont = L.small ? "700 11.5px Arial, sans-serif" : L.hub ? "700 13px Arial, sans-serif" : "600 11px Arial, sans-serif";
      ctx.font = titleFont;
      var w = ctx.measureText(L.text).width, w2 = 0;
      if (L.sub) { ctx.font = L.hub ? "11px Arial, sans-serif" : "italic 11px Arial, sans-serif"; w2 = Math.min(220, ctx.measureText(L.sub).width); }
      var bw = Math.max(w, w2) + (L.hub ? 18 : 10), bh = L.sub ? 32 : 18;
      if (L.dir) { // push the label outward from the group centre so an opened group fans its names out
        var cxl = L.ax + L.dir.x * (L.rr + bw / 2 * Math.abs(L.dir.x)), cyl = L.ay + L.dir.y * (L.rr + bh / 2 * Math.abs(L.dir.y));
        L.x = cxl; L.y = cyl - bh / 2 + 12;
      }
      var box = { x: L.x - bw / 2, y: L.y - 12, w: bw, h: bh };
      if (L.pri < 3.5 && placed.some(function (o) { return box.x < o.x + o.w && box.x + box.w > o.x && box.y < o.y + o.h && box.y + box.h > o.y; })) return;
      placed.push(box); ctx.globalAlpha = L.alpha;
      if (L.hub) { ctx.fillStyle = "rgba(7,25,17,.78)"; roundRect(box.x, box.y, box.w, box.h, 9); ctx.fill();
        ctx.strokeStyle = rgba(L.color, 0.7); ctx.lineWidth = 1; ctx.stroke(); }
      else if (L.sub || L.tag) { ctx.fillStyle = "rgba(7,25,17,.82)"; roundRect(box.x, box.y, box.w, box.h, 7); ctx.fill();
        if (L.tag) { ctx.strokeStyle = rgba(L.color, 0.85); ctx.lineWidth = 1.2; ctx.stroke(); } }
      ctx.textAlign = "center"; ctx.fillStyle = "#eef3ef"; ctx.font = titleFont;
      ctx.fillText(L.text, L.x, L.y + 1);
      if (L.sub) { ctx.font = L.hub ? "11px Arial, sans-serif" : "italic 11px Arial, sans-serif"; ctx.fillStyle = "#a9c2b1";
        var sub = L.sub; while (ctx.measureText(sub).width > 220 && sub.length > 4) sub = sub.slice(0, -2);
        ctx.fillText(sub === L.sub ? sub : sub + "…", L.x, L.y + 15); }
      ctx.globalAlpha = 1;
    });
    requestAnimationFrame(frame);
  }

  function pick(x, y) {
    if (view === "map" && !mapLevel) for (var bi = 0; bi < badges.length; bi++) { var B = badges[bi];
      if (Math.hypot(B.x - x, B.y - y) < Math.max(B.r, 22)) return { kind: "district", d: B.d, locked: B.locked }; }
    var best = null, bd = 1e9;
    claims.concat(hubs, subHubs).forEach(function (n) { if (!n._p || !n._p.live || (n.kind === "hub" && n.alpha < 0.5)) return; var d = Math.hypot(n._p.x - x, n._p.y - y);
      var hit = Math.max(n._p.r + 5, W < 700 ? 16 : 0); if (d < hit && d < bd) { bd = d; best = n; } });
    if (best) return best.kind === "hub" ? { kind: "hub", hub: best } : { kind: "claim", id: best.id };
    if (view === "map") for (var pi = 0; pi < PLACES.length; pi++) { var Q = PLACES[pi]._p;
      if (Q && Math.hypot(Q.x - x, Q.y - y) < Q.r + 4) return { kind: "place", place: PLACES[pi] }; }
    var be = -1; bd = 8;
    edges.forEach(function (e, i) { if (!e._g) return;
      for (var q = 0; q <= 24; q++) { var p = qpt(e._g, q / 24), d = Math.hypot(p.x - x, p.y - y); if (d < bd) { bd = d; be = i; } } });
    return be >= 0 ? { kind: "edge", index: be, edge: edges[be] } : null;
  }

  // ------------------------------------------------------------ map view
  // Each completed check unlocks more of the map. Thresholds count claims with a verdict.
  var TIERS = [
    { n: 0, key: "islands", label: "Island outlines" },
    { n: 3, key: "names", label: "Island names, compass and scale" },
    { n: 5, key: "contours", label: "Coastal depth lines" },
    { n: 7, key: "places", label: "Claim sites named on the map" },
    { n: 9, key: "valletta", label: "District: Valletta & Floriana" },
    { n: 12, key: "streets", label: "Valletta street grid and bastions" },
    { n: 15, key: "gozo", label: "District: Victoria & the Ċittadella, with its walls" },
    { n: 20, key: "harbour", label: "District: Grand Harbour & the Three Cities" },
    { n: 30, key: "sea", label: "Living sea: ferries and currents" }
  ];
  function checksDone() { return DATA ? DATA.claims.filter(function (c) { return c.verdict; }).length : 0; }
  function has(key) { var t = TIERS.filter(function (x) { return x.key === key; })[0]; return t && checksDone() >= t.n; }
  function unlocked(d) { return d && checksDone() >= d.unlock; }
  function lockText(d) { var k = d.unlock - checksDone(); return d.name + " unlocks after " + k + " more completed check" + (k === 1 ? "" : "s"); }
  function districtClaims(d) { return claims.filter(function (c) { return c.district === d; }); }
  function shortPlace(p) { return String(p || "").split(/[,(]/)[0].trim(); }
  function geoXY(lat, lon) { var O = GEO.origin; return { x: (lon - O.lon) * 111320 * Math.cos(O.lat * Math.PI / 180), y: (lat - O.lat) * 110574 }; }
  function toWorld(mx, my) { return { x: (mx - mapC.x) / MPU * mapZ, y: 0, z: (my - mapC.y) / MPU * mapZ }; }
  // Landmark emblems (24 x 24 line art) for every place a claim is about. Keys come from claim.yml location.icon.
  var PLACE_ICONS = {
    parliament: "M2 20.5 H22 M4 20.5 V9.5 H11 V20.5 M13 20.5 V9.5 H20 V20.5 M3 9.5 H21 M6 12 V18 M8.5 12 V18 M15.5 12 V18 M18 12 V18 M4 7 H20",
    castille: "M2 20.5 H22 M3 20.5 V10.5 H21 V20.5 M10 20.5 V16 A2 2 0 0 1 14 16 V20.5 M3 10.5 L12 6.5 L21 10.5 M12 6.5 V2.5 L15.5 3.5 L12 4.6 M6 13 V15.5 M18 13 V15.5",
    citygate: "M2 21 H22 M4.5 21 V5.5 L8.5 4 V21 M15.5 21 V4 L19.5 5.5 V21 M8.5 21 H15.5 M10.5 9 H13.5 M10.5 13 H13.5",
    barrakka: "M2 20.5 H22 M3 20.5 V11.5 A3 3 0 0 1 9 11.5 V20.5 M9 11.5 A3 3 0 0 1 15 11.5 V20.5 M15 11.5 A3 3 0 0 1 21 11.5 V20.5 M3 8.5 H21 M17 6 L21 4.5",
    ravelin: "M12 2.5 L21.5 10 L18 20.5 H6 L2.5 10 Z M7.5 17.5 H16.5 M12 6.5 V11 M9.5 11 H14.5",
    waterfront: "M2 20.5 H22 M3 20.5 V12 H21 V20.5 M5 20.5 V16 A1.5 1.5 0 0 1 8 16 V20.5 M10.5 20.5 V16 A1.5 1.5 0 0 1 13.5 16 V20.5 M16 20.5 V16 A1.5 1.5 0 0 1 19 16 V20.5 M3 12 L12 8 L21 12",
    tower: "M8 19 V8.5 H15 V19 M7 8.5 H16 M8 5.5 H15 V8.5 M8 5.5 V4 M11.5 5.5 V4 M15 5.5 V4 M10.5 12 H12.5 M2 21.5 C5 20.5 7 22.5 10 21.5 C13 20.5 15 22.5 18 21.5 C19.5 21 20.5 21.2 22 21.5",
    landfill: "M2 20.5 C5 13 9 10 13 12 C16 13.5 19 16.5 22 20.5 Z M15.5 9.5 V4 H17.5 V10.5 M7 17.5 L9.5 15 M12 17 L14 14.5",
    flyover: "M2 18 C8 18 10 10 16 10 H22 M2 12 H8 C14 12 15 18 22 18 M6 18 V21.5 M18 10 V21.5 M12 13.5 V21.5",
    ro_plant: "M6 21 V12.5 H18 V21 Z M6 16 H18 M9.5 12.5 V21 M14.5 12.5 V21 M12 2.5 C12 2.5 9 6.5 9 8.5 A3 3 0 0 0 15 8.5 C15 6.5 12 2.5 12 2.5 Z",
    park: "M2 20.5 H22 M7 20.5 V13.5 M7 4 C3 6 3 12 7 13.5 C11 12 11 6 7 4 Z M13 15.5 H21 M14 15.5 L13 20.5 M20 15.5 L21 20.5 M14.5 13 H19.5",
    crane: "M4.5 21 V5.5 H20.5 M4.5 5.5 L8.5 2.5 H18.5 L20.5 5.5 M15 5.5 V10.5 M12.5 10.5 H17.5 V13.5 H12.5 Z M9.5 21 V17 H21 V21 M2 21 H22",
    ferry: "M3 15 H21 L19 19 H5 Z M6.5 15 V11.5 H16.5 V15 M8.5 11.5 V8.5 H13.5 V11.5 M17.5 8 V11.5 M2 21.5 C5 20.5 7 22.5 10 21.5 C13 20.5 15 22.5 18 21.5 C19.5 21 20.5 21.2 22 21.5",
    pin: "M12 21 C12 21 5 14 5 9 A7 7 0 0 1 19 9 C19 14 12 21 12 21 Z M12 9 V9.1",
    unknown: "M9 9 A3 3 0 1 1 13.5 11.6 C12.4 12.2 12 13 12 14.2 M12 17.6 V17.7"
  };
  var PLACE_PATHS = {}; Object.keys(PLACE_ICONS).forEach(function (k) { PLACE_PATHS[k] = new Path2D(PLACE_ICONS[k]); });
  var PLACES = [];
  function buildPlaces() {
    var by = {}; PLACES = [];
    claims.forEach(function (c) { var L = c.data.location; if (!L || !c.m) return;
      var P = by[L.place]; if (!P) { P = by[L.place] = { kind: "place", name: L.place, short: shortPlace(L.place), m: c.m, icon: L.icon || "pin", district: c.district, claims: [] }; PLACES.push(P); }
      P.claims.push(c); c.place = P; });
    PLACES.forEach(function (P) { P.discovered = P.claims.some(function (c) { return c.data.verdict; }); });
  }
  function placeVisible(P) { return mapLevel ? P.district === mapLevel : !(P.district && unlocked(P.district)); }
  function drawPlaces() {
    var zs = Math.max(1, Math.min(1.5, Math.pow(cam.zoom, 0.3))) * (W < 700 ? 0.85 : 1);
    PLACES.forEach(function (P) {
      P._p = null; if (!placeVisible(P)) return;
      var tp = project(P.t || toWorld(P.m.x, P.m.y)), p = project(P.w || P.t || toWorld(P.m.x, P.m.y)), R = 15 * zs;
      if (Math.hypot(tp.sx - p.sx, tp.sy - p.sy) > R * 0.6) { ctx.save(); ctx.strokeStyle = P.discovered ? "rgba(227,167,47,.55)" : "rgba(207,226,212,.35)";
        ctx.lineWidth = 1; ctx.beginPath(); ctx.moveTo(tp.sx, tp.sy); ctx.lineTo(p.sx, p.sy); ctx.stroke();
        ctx.fillStyle = ctx.strokeStyle; ctx.beginPath(); ctx.arc(tp.sx, tp.sy, 2.2, 0, 6.283); ctx.fill(); ctx.restore(); }
      var on = sel && sel.kind === "place" && sel.place === P;
      var hov = hover && hover.kind === "place" && hover.place === P;
      ctx.save();
      if (P.discovered) { var g = ctx.createRadialGradient(p.sx, p.sy, R * 0.6, p.sx, p.sy, R * 2.2); g.addColorStop(0, "rgba(227,167,47,.28)"); g.addColorStop(1, "rgba(227,167,47,0)");
        ctx.fillStyle = g; ctx.beginPath(); ctx.arc(p.sx, p.sy, R * 2.2, 0, 6.283); ctx.fill(); }
      ctx.fillStyle = "rgba(8,30,21,.9)"; ctx.beginPath(); ctx.arc(p.sx, p.sy, R * (hov || on ? 1.12 : 1), 0, 6.283); ctx.fill();
      ctx.setLineDash(P.discovered ? [] : [3, 3]); ctx.lineWidth = on ? 2.4 : 1.6;
      ctx.strokeStyle = P.discovered ? "#e3a72f" : "rgba(207,226,212,.5)"; ctx.stroke(); ctx.setLineDash([]);
      var path = PLACE_PATHS[P.discovered ? P.icon : "unknown"] || PLACE_PATHS.pin, k = (R * 1.25) / 24;
      ctx.translate(p.sx - 12 * k, p.sy - 12 * k); ctx.scale(k, k);
      ctx.strokeStyle = P.discovered ? "#f6e3b4" : "rgba(207,226,212,.75)"; ctx.lineWidth = 1.7; ctx.lineCap = "round"; ctx.lineJoin = "round"; ctx.stroke(path);
      ctx.restore();
      if (has("places") && showText) { ctx.font = "italic 11px 'Liberation Serif', Georgia, serif"; ctx.textAlign = "center";
        ctx.fillStyle = P.discovered ? "rgba(246,227,180,.9)" : "rgba(207,226,212,.6)"; ctx.fillText(P.discovered ? P.short : "Undiscovered site", p.sx, p.sy + R + 12); }
      P._p = { x: p.sx, y: p.sy, r: R };
    });
  }
  function selectPlace(P) {
    sel = { kind: "place", place: P };
    var done = P.claims.filter(function (c) { return c.data.verdict; }).length;
    openPanel("PLACE · " + (P.discovered ? "DISCOVERED" : "NOT YET CHECKED"), P.discovered ? P.name : "Undiscovered site", P.discovered ? "#e3a72f" : NOT_YET_COL,
      [P.claims.length + (P.claims.length === 1 ? " claim" : " claims"), done + " checked"]);
    pbody.appendChild(el("p", "small", P.discovered ? "Claims about this place. Each completed check adds to the map."
      : "Complete a check on one of these claims to reveal this site on the map. Located at: " + P.name + "."));
    label("CLAIMS HERE"); var box = el("div", "links"); P.claims.forEach(function (c) { claimLink(c.id, box); }); pbody.appendChild(box); fitPanel();
  }
  function geoReady() {
    var nl = 0; claims.forEach(function (c) { if (!c.data.location) c.noLocIndex = nl++; });
    if (nl > claims.length / 2) showToast("Claim locations are still loading; reload the page in a minute if pins look misplaced.");
    GEO.islands.forEach(function (I) { var cx = 0, cy = 0, n = I.coarse.length / 2; for (var i = 0; i < I.coarse.length; i += 2) { cx += I.coarse[i]; cy += I.coarse[i + 1]; } I.cx = cx / n; I.cy = cy / n; });
    claims.forEach(function (c) {
      var L = c.data.location; c.m = null; c.district = null;
      if (L) { c.m = geoXY(+L.lat, +L.lon);
        var best = 1e9; GEO.districts.forEach(function (d) { var dd = Math.hypot(c.m.x - d.x, c.m.y - d.y); if (dd <= d.radius_m && dd < best) { best = dd; c.district = d; } }); }
    });
    buildPlaces(); buildViewBy(); buildMapHud();
    if (view === "map") setView("map", true);
  }
  function mapTargets() {
    if (!GEO) return;
    var vis = [], places = {}, off = [];
    claims.forEach(function (c) {
      c.clustered = false; c.offmap = false; c.ringR = 0; c.ringFirst = false;
      var m = c.m || { x: 16000 + (c.noLocIndex || 0) * 900, y: -19000 }; // no location yet: a row in the sea, south-east
      if (!mapLevel && c.district && unlocked(c.district)) {          // bunched into the district badge
        var w = toWorld(c.district.x, c.district.y), a = (claims.indexOf(c) * 2.4);
        c.tx = w.x + Math.cos(a) * 5; c.tz = w.z + Math.sin(a) * 5; c.ty = -10; c.clustered = true; c.anchor = null; return;
      }
      var W0 = toWorld(m.x, m.y), key = Math.round(m.x / 25) + "," + Math.round(m.y / 25);
      if (mapLevel && c.district !== mapLevel) { var dd = Math.hypot(W0.x, W0.z) || 1;   // elsewhere: parked on the outer ring
        W0.x *= OUTER / dd; W0.z *= OUTER / dd; c.offmap = true; }
      c.anchor = { x: W0.x, y: 0, z: W0.z };
      if (c.offmap) { off.push(c); vis.push(c); return; }
      (places[key] = places[key] || []).push(c); vis.push(c);
    });
    // elsewhere: one slot per site near its true bearing, slots kept apart, a site's claims stacked outwards
    if (off.length) {
      var sg = {}, slots = [];
      off.forEach(function (c) { var k = c.data.location ? c.data.location.place : "?";
        if (!sg[k]) { sg[k] = { ang: Math.atan2(c.anchor.z, c.anchor.x), cs: [] }; slots.push(sg[k]); } sg[k].cs.push(c); });
      slots.sort(function (a, b) { return a.ang - b.ang; });
      var ns = slots.length, gap = Math.min(0.2, 2 * Math.PI / ns * 0.9);
      for (var ia = 0; ia < 80; ia++) for (var q = 0; q < ns; q++) {
        var A0 = slots[q], B0 = slots[(q + 1) % ns], dA = B0.ang - A0.ang + (q === ns - 1 ? 2 * Math.PI : 0);
        if (ns > 1 && dA < gap) { var push = (gap - dA) / 2; A0.ang -= push; B0.ang += push; } }
      slots.forEach(function (S) { S.cs.forEach(function (c, i) { c.ringR = OUTER + i * 24; c.ringFirst = i === S.cs.length - 1;
        c.anchor = { x: Math.cos(S.ang) * c.ringR, y: 0, z: Math.sin(S.ang) * c.ringR }; places["off" + c.id] = [c]; }); });
    }
    // site medallions: kept apart (they can be metres apart in Valletta), each drawn with a leader to its true spot
    var vp = PLACES.filter(placeVisible);
    vp.forEach(function (P) { var w = toWorld(P.m.x, P.m.y); P.t = { x: w.x, y: 0, z: w.z }; P.w = { x: w.x, y: 0, z: w.z }; });
    var minP = (W < 700 ? 30 : 34) * (mapLevel ? 0.6 + 0.75 * spreadF() : 1);
    for (var ip = 0; ip < 40; ip++) {
      for (var a1 = 0; a1 < vp.length; a1++) for (var b1 = a1 + 1; b1 < vp.length; b1++) {
        var U = vp[a1].w, V2 = vp[b1].w, ex = V2.x - U.x, ez = V2.z - U.z, dl = Math.hypot(ex, ez) || 0.01;
        if (dl < minP) { var ff = (minP - dl) / 2 / dl; U.x -= ex * ff; U.z -= ez * ff; V2.x += ex * ff; V2.z += ez * ff; } }
      vp.forEach(function (P) { P.w.x += (P.t.x - P.w.x) * 0.03; P.w.z += (P.t.z - P.w.z) * 0.03; });
    }
    vis.forEach(function (c) { if (!c.offmap && c.place && c.place.w && placeVisible(c.place)) c.anchor = { x: c.place.w.x, y: 0, z: c.place.w.z }; });
    Object.keys(places).forEach(function (k) { var g = places[k], n = g.length;
      g.forEach(function (c, i) { var a = (i / n) * Math.PI * 2 - Math.PI / 2, r = n > 1 ? (9 + 4 * n) * spreadF() : 0;
        c.tx = c.anchor.x + Math.cos(a) * r; c.tz = c.anchor.z + Math.sin(a) * r; c.ty = mapLevel ? -64 - 70 * spreadF() : -64; }); });
    for (var it = 0; it < 24; it++) {                               // keep pins apart, pulled back to their sites
      for (var i = 0; i < vis.length; i++) for (var j = i + 1; j < vis.length; j++) {
        var A = vis[i], B = vis[j], dx = B.tx - A.tx, dz = B.tz - A.tz, d = Math.hypot(dx, dz) || 0.01, min = mapLevel ? 26 + 10 * spreadF() : 26;
        if (d < min) { var f = (min - d) / 2 / d; A.tx -= dx * f; A.tz -= dz * f; B.tx += dx * f; B.tz += dz * f; } }
      vis.forEach(function (c) { c.tx += (c.anchor.x - c.tx) * 0.04; c.tz += (c.anchor.z - c.tz) * 0.04;
        if (c.offmap) { var dd2 = Math.hypot(c.tx, c.tz) || 1, rr = c.ringR || OUTER; c.tx *= rr / dd2; c.tz *= rr / dd2; } });
    }
  }
  var OUTER = 255;
  function ringPath(arr) { ctx.beginPath(); for (var i = 0; i < arr.length; i += 2) { var p = project(toWorld(arr[i], arr[i + 1]));
    if (i) ctx.lineTo(p.sx, p.sy); else ctx.moveTo(p.sx, p.sy); } ctx.closePath(); }
  function linePath(arr) { ctx.beginPath(); for (var i = 0; i < arr.length; i += 2) { var p = project(toWorld(arr[i], arr[i + 1]));
    if (i) ctx.lineTo(p.sx, p.sy); else ctx.moveTo(p.sx, p.sy); } }
  function drawMap(t) {
    if (!GEO) return;
    var zoomScale = cam.zoom * mapZ, detail = mapZ > 3, dz = Math.max(0, Math.min(1, (mapZ - 3) / 7)), done = checksDone();
    // graticule
    ctx.save(); ctx.strokeStyle = "rgba(127,168,139,.08)"; ctx.lineWidth = 1;
    for (var g = -40000; g <= 40000; g += (mapLevel ? 500 : 5000)) {
      linePath([g, -40000, g, 40000]); ctx.stroke(); linePath([-40000, g, 40000, g]); ctx.stroke(); }
    ctx.restore();
    // coastal depth lines
    if (has("contours")) GEO.islands.forEach(function (I) { if (I.area_m2 < 1e6) return;
      [3.2, 2.1, 1.2].forEach(function (wf, i) { ringPath(detail && I.detail ? I.detail : I.coarse); ctx.strokeStyle = "rgba(86,180,233," + ((0.05 + i * 0.025) * (1 - 0.6 * dz)) + ")";
        ctx.lineWidth = Math.min(34, wf * 9 * Math.sqrt(cam.zoom)); ctx.lineJoin = "round"; ctx.stroke(); }); });
    // land
    GEO.islands.forEach(function (I) {
      var ring = detail && I.detail ? I.detail : I.coarse;
      ringPath(ring);
      var g0 = project(toWorld(5000, -2000)), gr = ctx.createRadialGradient(g0.sx - 80, g0.sy - 80, 10, g0.sx, g0.sy, Math.max(W, H) * 0.8);
      gr.addColorStop(0, "rgba(74,138,98,.78)"); gr.addColorStop(1, "rgba(31,84,58,.82)");
      ctx.fillStyle = gr; ctx.fill();
      ctx.strokeStyle = detail ? "rgba(227,167,47," + (0.35 + 0.4 * dz) + ")" : "rgba(207,226,212,.55)"; ctx.lineWidth = detail ? 1.4 + dz : 1.1; ctx.stroke();
    });
    // island names
    var narrow = W < 700;
    if (has("names") && !mapLevel) [["MALTA", "Malta"], [narrow ? "GOZO" : "GĦAWDEX · GOZO", "Gozo"]].concat(narrow ? [] : [["KEMMUNA", "Comino"]]).forEach(function (L) {
      var I = GEO.islands.filter(function (x) { return x.name === L[1]; })[0]; if (!I) return;
      var p = project(toWorld(I.cx, I.cy + (L[1] === "Malta" ? 3500 : L[1] === "Gozo" ? 1800 : -900)));
      ctx.font = "700 " + (L[1] === "Comino" ? 10 : narrow ? 11 : 14) + "px 'Liberation Serif', Georgia, serif"; ctx.textAlign = "center";
      ctx.fillStyle = "rgba(238,243,239,.42)"; ctx.fillText(L[0].split("").join(String.fromCharCode(8202)), p.sx, p.sy); });
    // district detail: streets and landmarks
    if (dz > 0.02) GEO.districts.forEach(function (V) {
      if (!unlocked(V)) return;
      if (V.id !== "valletta" || has("streets")) {                    // Valletta's grid is its own later unlock
        V.streets.forEach(function (S) { linePath(S.pts); ctx.strokeStyle = "rgba(238,243,239," + (S.major ? 0.42 : 0.2) * dz + ")";
          ctx.lineWidth = S.major ? 2.2 : 1; ctx.stroke(); });
        (V.walls || []).forEach(function (Wl) { linePath(Wl); ctx.strokeStyle = "rgba(227,167,47," + 0.42 * dz + ")";   // bastions and citadel walls
          ctx.lineWidth = 2.6; ctx.lineJoin = "round"; ctx.stroke(); }); }
      V.landmarks.forEach(function (L) { if (PLACES.some(function (P) { return Math.hypot(P.m.x - L.x, P.m.y - L.y) < 60; })) return;
        var p = project(toWorld(L.x, L.y)); ctx.globalAlpha = dz;
        ctx.fillStyle = "#e3a72f"; ctx.save(); ctx.translate(p.sx, p.sy); ctx.rotate(Math.PI / 4); ctx.fillRect(-3.5, -3.5, 7, 7); ctx.restore();
        ctx.font = "600 11px Arial, sans-serif"; ctx.textAlign = "left"; ctx.fillStyle = "rgba(238,243,239,.85)"; ctx.fillText(L.name, p.sx + 8, p.sy + 4);
        ctx.globalAlpha = 1; });
    });
    // district level: the rest of Malta is folded onto an outer ring
    if (mapLevel) { var o0 = project({ x: 0, y: 0, z: 0 }), o1 = project({ x: OUTER, y: 0, z: 0 }), o2 = project({ x: 0, y: 0, z: OUTER });
      var rx = Math.abs(o1.sx - o0.sx), ry = Math.abs(o2.sy - o0.sy);
      ctx.save(); ctx.strokeStyle = "rgba(207,226,212,.28)"; ctx.setLineDash([3, 7]); ctx.lineWidth = 1.2;
      ctx.beginPath(); ctx.ellipse(o0.sx, o0.sy, rx, ry, -cam.yaw * 0, 0, 6.283); ctx.stroke(); ctx.restore();
      ctx.font = "700 10.5px Arial, sans-serif"; ctx.textAlign = "center"; ctx.fillStyle = "rgba(207,226,212,.55)";
      ctx.fillText("ELSEWHERE IN MALTA", o0.sx, o0.sy - ry - 8); }
    // landmark medallions for every claim site (discovered once a claim there has a verdict)
    drawPlaces();
    // district badges (Malta level)
    badges = [];
    if (!mapLevel) GEO.districts.forEach(function (d) {
      var nextLock = GEO.districts.filter(function (x) { return !unlocked(x); }).sort(function (a, b) { return a.unlock - b.unlock; })[0];
      if (!unlocked(d) && d !== nextLock) return;                      // tease only the next district to unlock
      var c = project(toWorld(d.x, d.y)), e = project(toWorld(d.x + d.radius_m * 1.35, d.y)), r = Math.max(18, Math.abs(e.sx - c.sx));
      var open = unlocked(d), n = districtClaims(d).length;
      ctx.save(); ctx.setLineDash(open ? [] : [4, 5]);
      if (open) { var gl = ctx.createRadialGradient(c.sx, c.sy, r * 0.4, c.sx, c.sy, r * 1.6); gl.addColorStop(0, "rgba(227,167,47,.22)"); gl.addColorStop(1, "rgba(227,167,47,0)");
        ctx.fillStyle = gl; ctx.beginPath(); ctx.arc(c.sx, c.sy, r * 1.6, 0, 6.283); ctx.fill(); }
      ctx.strokeStyle = open ? "rgba(227,167,47," + (0.65 + 0.25 * Math.sin(t * 2.2)) + ")" : "rgba(207,226,212,.35)"; ctx.lineWidth = open ? 2 : 1.3;
      ctx.beginPath(); ctx.arc(c.sx, c.sy, r, 0, 6.283); ctx.stroke(); ctx.restore();
      var txt = open ? d.name : "🔒 " + d.name, sub = open ? n + (n === 1 ? " claim" : " claims") + " · click to open" : (d.unlock - done) + " more check" + (d.unlock - done === 1 ? "" : "s") + " to unlock";
      ctx.font = (narrow ? "700 11px" : "700 12px") + " Arial, sans-serif"; var w = Math.max(ctx.measureText(txt).width, narrow ? 104 : 120) + 18;
      var bx = c.sx - w / 2, by = open ? c.sy - r - 40 : c.sy + r + 8;   // locked teasers hang below, clear of open badges ctx.fillStyle = open ? "rgba(227,167,47,.95)" : "rgba(8,30,21,.8)";
      roundRect(bx, by, w, 32, 9); ctx.fill(); ctx.textAlign = "center"; ctx.fillStyle = open ? "#13301f" : "rgba(238,243,239,.75)";
      ctx.fillText(txt, c.sx, by + 14); ctx.font = "11px Arial, sans-serif"; ctx.fillText(sub, c.sx, by + 27);
      badges.push({ x: c.sx, y: c.sy, r: r, d: d, locked: !open });
    });
    // compass and scale bar
    if (has("names")) { var cxp = W - 54, cyp = H - 92;
      ctx.save(); ctx.translate(cxp, cyp); ctx.rotate(-cam.yaw); ctx.strokeStyle = "rgba(238,243,239,.6)"; ctx.fillStyle = "#e3a72f"; ctx.lineWidth = 1.2;
      ctx.beginPath(); ctx.arc(0, 0, 18, 0, 6.283); ctx.stroke(); ctx.beginPath(); ctx.moveTo(0, -16); ctx.lineTo(5, 0); ctx.lineTo(0, 4); ctx.lineTo(-5, 0); ctx.closePath(); ctx.fill();
      ctx.fillStyle = "rgba(238,243,239,.8)"; ctx.font = "700 10px Arial"; ctx.textAlign = "center"; ctx.fillText("N", 0, -22); ctx.restore();
      if (lensK < 0.5) { var a0 = project(toWorld(mapC.x, mapC.y)), len = mapLevel ? 200 : 5000, a1 = project(toWorld(mapC.x + len, mapC.y)), px = Math.abs(a1.sx - a0.sx);
      ctx.strokeStyle = "rgba(238,243,239,.6)"; ctx.lineWidth = 2; ctx.beginPath(); ctx.moveTo(W - 100 - px, H - 46); ctx.lineTo(W - 100, H - 46); ctx.stroke();
      ctx.font = "11px Arial"; ctx.textAlign = "right"; ctx.fillStyle = "rgba(238,243,239,.7)"; ctx.fillText(mapLevel ? "200 m" : "5 km", W - 100, H - 52); } }
    // living sea (late unlock)
    if (has("sea") && !reduce) { ctx.strokeStyle = "rgba(207,226,212,.12)"; ctx.lineWidth = 1;
      for (var q = 0; q < 6; q++) { var y0 = (H * (q + 0.5) / 6 + t * 8) % H; ctx.beginPath(); ctx.moveTo(0, y0);
        for (var xq = 0; xq <= W; xq += 40) ctx.lineTo(xq, y0 + Math.sin(xq / 90 + t + q) * 4); ctx.stroke(); } }
  }
  function mapifyMode() {
    hubs.concat(subHubs).forEach(function (h) { h.talpha = 0; }); sway = false;
    cam.tyaw = mapLevel ? cam.tyaw : 0; cam.tpitch = MAP_PITCH;
  }
  // Smooth transitions. The camera's zoom and pan are first folded into the map scale and centre, so the first
  // frame is exactly what was on screen; the scale then moves in log space about the one screen point that stays put.
  var mapAnim = null;
  function districtScale(d) { return 175 * MPU / d.radius_m; }
  function spreadF() { if (!mapLevel) return 1; var S1 = districtScale(mapLevel);
    return Math.max(0, Math.min(1, Math.log(Math.max(1, mapZ)) / Math.log(S1))); }
  function screenCentreGeo() {
    var K = baseScale() * cam.zoom * cam.em, cy = Math.cos(cam.yaw), sy = Math.sin(cam.yaw), sp = Math.sin(cam.pitch) || 0.5;
    var x1 = -cam.px / K, y2 = -cam.py / K, z1 = -y2 / sp;
    var wx = x1 * cy + z1 * sy, wz = -x1 * sy + z1 * cy;
    return { x: mapC.x + wx * MPU / mapZ, y: mapC.y + wz * MPU / mapZ };
  }
  function foldCamera() {
    var G = screenCentreGeo(); mapZ = mapZ * cam.zoom; mapC = G; tmapZ = mapZ; tmapC = { x: G.x, y: G.y };
    cam.zoom = 1; cam.px = cam.tpx = 0; cam.py = cam.tpy = 0;
  }
  function animateMap(c1, S1, done) {
    foldCamera();
    var c0 = { x: mapC.x, y: mapC.y }, S0 = mapZ, r = S0 / S1, P = null;
    if (Math.abs(1 - r) > 0.02) P = { x: (c1.x - c0.x * r) / (1 - r), y: (c1.y - c0.y * r) / (1 - r) };
    mapAnim = { c0: c0, c1: c1, S0: S0, S1: S1, P: P, u: 0, dur: reduce ? 0.01 : 0.95, done: done };
    tmapZ = S1; tmapC = { x: c1.x, y: c1.y };
  }
  function stepMapAnim(dt) {
    var A = mapAnim; if (!A) return;
    A.u = Math.min(1, A.u + dt / A.dur);
    var e = A.u < 0.5 ? 4 * A.u * A.u * A.u : 1 - Math.pow(-2 * A.u + 2, 3) / 2;   // ease in-out cubic
    mapZ = Math.exp(Math.log(A.S0) + (Math.log(A.S1) - Math.log(A.S0)) * e);
    if (A.P) { var q = A.S0 / mapZ; mapC = { x: A.P.x + (A.c0.x - A.P.x) * q, y: A.P.y + (A.c0.y - A.P.y) * q }; }
    else mapC = { x: A.c0.x + (A.c1.x - A.c0.x) * e, y: A.c0.y + (A.c1.y - A.c0.y) * e };
    if (A.u >= 1) { mapAnim = null; mapZ = A.S1; mapC = { x: A.c1.x, y: A.c1.y }; if (A.done) A.done(); }
  }
  function enterDistrict(d) {
    if (!GEO || !unlocked(d) || mapLevel === d) return; mapLevel = d;
    animateMap({ x: d.x, y: d.y }, districtScale(d));
    var cr = document.getElementById("crumb"); cr.textContent = "";
    cr.appendChild(document.createTextNode("Malta › ")); cr.appendChild(el("b", null, d.name));
    cr.appendChild(document.createTextNode(" · " + districtClaims(d).length + " claims"));
    var back = el("button", null, "Back to Malta"); back.type = "button"; back.onclick = exitDistrict; cr.appendChild(back);
    cr.style.display = "inline-flex"; setHint();
  }
  function exitDistrict() {
    if (!mapLevel) return;
    document.getElementById("crumb").style.display = "none";
    animateMap({ x: HOME.x, y: HOME.y }, 1, function () { mapLevel = null; setHint(); });   // claims regroup as the map shrinks
  }
  function districtZoomCheck(mx, my) {
    if (view !== "map" || !GEO) return;
    if (mapAnim) return;
    if (mapLevel && cam.zoom < 0.7) { exitDistrict(); return; }
    if (!mapLevel && cam.zoom > 2.6) GEO.districts.forEach(function (d) { if (!unlocked(d) || mapLevel) return;
      var c = project(toWorld(d.x, d.y)); if (Math.hypot(c.sx - mx, c.sy - my) < Math.min(W, H) * 0.3) enterDistrict(d); });
  }
  function fitView() {
    if (view === "map") { cam.tyaw = 0; cam.tpitch = MAP_PITCH;       // fold the current zoom and pan, then glide home
      if (mapLevel) animateMap({ x: mapLevel.x, y: mapLevel.y }, districtScale(mapLevel)); else animateMap({ x: HOME.x, y: HOME.y }, 1); return; }
    cam.zoom = 1; cam.tpx = 0; cam.tpy = 0; cam.yaw = 0.6; cam.pitch = cam.tpitch; if (sway) cam.yaw = 0;
  }
  function setView(v, instant) {
    if (v === "map" && !GEO) { view = "map"; loadGeo(); return; }
    var was = view; view = v;
    try { localStorage.setItem("mizien.view", v); } catch (e) {}
    var u = new URL(location.href); u.searchParams.set("view", v === "map" ? "map" : "ghanqbuta"); history.replaceState(null, "", u);
    collapse(); cam.tpx = 0; cam.tpy = 0; cam.zoom = 1;
    mapAnim = null;
    if (v === "map") { if (was !== "map") spinBeforeMap = spinning; setSpin(false); mapLevel = null; tmapZ = mapZ = 1; tmapC = { x: HOME.x, y: HOME.y }; mapC = { x: HOME.x, y: HOME.y };
      cam.tyaw = 0; mapifyMode(); document.getElementById("crumb").style.display = "none"; }
    else { mapLevel = null; document.getElementById("crumb").style.display = "none"; claims.forEach(function (c) { c.clustered = false; c.offmap = false; c.anchor = null; });
      setMode(mode, false); if (spinBeforeMap && !reduce) setSpin(true); }
    document.getElementById("maphud").style.display = v === "map" ? "block" : "none";
    document.querySelectorAll("#viewby button").forEach(function (b) { b.setAttribute("aria-pressed", b.dataset.view === v ? "true" : "false"); });
    var mt = document.getElementById("modeTitle");
    if (v === "map") { mt.querySelector(".t").textContent = "Claims across the islands"; mt.querySelector(".s").textContent = "Each check reveals more of the map · colours and groups still apply"; }
    else { var M = MODES[mode]; mt.querySelector(".t").textContent = M.title; mt.querySelector(".s").textContent = M.sub; }
    syncLens(); setHint(); if (instant) { claims.forEach(function (c) { c.x = c.tx; c.y = c.ty; c.z = c.tz; }); if (v === "map") { cam.yaw = 0; cam.pitch = MAP_PITCH; } }
  }
  function setHint() {
    var h = document.getElementById("hint");
    h.querySelector(".desktop-hint").textContent = view === "map"
      ? (mapLevel ? "Drag to pan · right-drag to tilt · scroll out or Back to leave the district" : "Drag to pan · right-drag to tilt · scroll to zoom · click a district to open it")
      : "Drag to rotate · right-drag or Shift-drag to pan · scroll to zoom · double-click to zoom in";
    h.querySelector(".mobile-hint").textContent = view === "map" ? "Drag to pan · pinch to zoom · tap a district" : "Drag to turn · two fingers to pan and zoom · tap a node";
  }
  function loadGeo() {
    fetch("data/geo.json", { cache: "no-cache" }).then(function (r) { return r.json(); }).then(function (g) { GEO = g; geoReady(); })
      .catch(function () { showToast("The map outline could not be loaded."); view = "graph"; });
  }
  function buildViewBy() {
    var g = document.getElementById("viewby"); g.textContent = "";
    // "Għanqbuta" is Maltese for spider: a web of claims, with topic hubs, spokes and the threads that link them.
    [["graph", "Għanqbuta", "mode:network", "Għanqbuta (spider): a web of claims, with topic hubs, spokes and the threads that link them"],
     ["map", "Malta map", "mode:topic", "Claims placed where they happened, across Malta and Gozo"]].forEach(function (v) {
      var b = el("button"); b.type = "button"; b.dataset.view = v[0]; b.title = v[3]; b.setAttribute("aria-pressed", view === v[0] ? "true" : "false");
      if (v[0] === "map") { b.innerHTML = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3 6.5 L9 4 L15 6.5 L21 4 V17.5 L15 20 L9 17.5 L3 20 Z M9 4 V17.5 M15 6.5 V20" fill="none" stroke="#cfe2d4" stroke-width="1.8" stroke-linejoin="round"/></svg>'; }
      else b.appendChild(iconSvg(v[2], "#cfe2d4"));
      b.appendChild(document.createTextNode(v[1])); b.onclick = function () { setView(v[0]); }; g.appendChild(b);
    });
  }
  function buildMapHud() {
    var hud = document.getElementById("maphud"), done = checksDone(); hud.textContent = "";
    var level = TIERS.filter(function (x) { return done >= x.n; }).length, next = TIERS.filter(function (x) { return done < x.n; })[0];
    var prev = TIERS[level - 1] ? TIERS[level - 1].n : 0;
    var top = el("div", "lvl"); top.appendChild(el("b", null, "Map level " + level + " of " + TIERS.length));
    var disc = PLACES.filter(function (P) { return P.discovered; }).length;
    top.appendChild(el("span", null, done + (done === 1 ? " check" : " checks") + " · " + disc + "/" + PLACES.length + " sites discovered")); hud.appendChild(top);
    var bar = el("div", "bar"), fill = el("i"); fill.style.width = (next ? Math.round(100 * (done - prev) / (next.n - prev)) : 100) + "%"; bar.appendChild(fill); hud.appendChild(bar);
    hud.appendChild(el("div", "next", next ? (next.n - done) + " more check" + (next.n - done === 1 ? "" : "s") + " unlock: " + next.label : "Every layer unlocked."));
    var det = el("details"); det.appendChild(el("summary", null, "What each check unlocks"));
    var ul = el("ul"); TIERS.forEach(function (x) { var li = el("li", done >= x.n ? "on" : null); li.appendChild(el("span", null, done >= x.n ? "✓" : "🔒"));
      li.appendChild(el("span", null, x.n + " · " + x.label)); ul.appendChild(li); }); det.appendChild(ul); hud.appendChild(det);
    var seen = 0; try { seen = +(localStorage.getItem("mizien.mapSeen") || 0); localStorage.setItem("mizien.mapSeen", String(done)); } catch (e) {}
    var fresh = TIERS.filter(function (x) { return x.n > seen && x.n <= done && seen > 0; });
    if (fresh.length) showToast("New on the map: " + fresh.map(function (x) { return x.label; }).join(", "));
  }
  var toastTimer = null;
  function showToast(msg) { var t = document.getElementById("toast"); t.textContent = msg; t.style.display = "block";
    clearTimeout(toastTimer); toastTimer = setTimeout(function () { t.style.display = "none"; }, 4200); }

  // ------------------------------------------------------------ panels
  // colour helpers for the panel theme
  function hexRgb(h) { var n = parseInt(h.slice(1), 16); return [n >> 16, (n >> 8) & 255, n & 255]; }
  function mix(h1, h2, t) { var a = hexRgb(h1), b = hexRgb(h2); return "#" + a.map(function (v, i) { return ("0" + Math.round(v + (b[i] - v) * t).toString(16)).slice(-2); }).join(""); }
  function lum(h) { var c = hexRgb(h).map(function (v) { v /= 255; return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4); }); return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]; }
  function themePanel(col) {
    var light = lum(col) > 0.36, st = panel.style;
    st.setProperty("--p-head", col); st.setProperty("--p-head2", mix(col, "#000000", 0.28));
    st.setProperty("--p-head-ink", light ? mix(col, "#000000", 0.78) : "#ffffff");
    st.setProperty("--p-bg", mix(col, "#ffffff", 0.9)); st.setProperty("--p-soft", mix(col, "#ffffff", 0.74));
    st.setProperty("--p-line", mix(col, "#ffffff", 0.62)); st.setProperty("--p-ink", mix(col, "#000000", 0.74));
    st.setProperty("--p-link", mix(col, "#000000", 0.5)); st.setProperty("--p-muted", mix(col, "#5a6468", 0.55));
    return light;
  }
  var pbody = null, wide = false;
  try { wide = localStorage.getItem("mizien.wide") === "1"; } catch (e) {}
  function openPanel(kicker, title, accent, pills) {
    panel.textContent = ""; panel.style.display = "block"; panel.scrollTop = 0;
    var light = themePanel(accent || "#14452f");
    panel.classList.toggle("wide", wide);
    var head = el("div", "phead"), btns = el("div", "hbtns");
    var w = el("button", "wbtn", wide ? "⤡" : "⤢"); w.type = "button"; w.title = wide ? "Narrow view" : "Wide view";
    w.setAttribute("aria-label", w.title); w.setAttribute("aria-pressed", wide ? "true" : "false");
    w.onclick = function () { wide = !wide; try { localStorage.setItem("mizien.wide", wide ? "1" : "0"); } catch (e) {}
      panel.classList.toggle("wide", wide); w.textContent = wide ? "⤡" : "⤢"; w.title = wide ? "Narrow view" : "Wide view";
      w.setAttribute("aria-label", w.title); w.setAttribute("aria-pressed", wide ? "true" : "false"); fitPanel(); setTimeout(fitPanel, 400); };
    var x = el("button", "x", "×"); x.type = "button"; x.setAttribute("aria-label", "Close"); x.onclick = clearSel;
    // phones: lower the card to a peek bar; the selection stays highlighted underneath
    var pb = el("button", "pbtn", "▾"); pb.type = "button"; pb.onclick = function () { setPeek(!panel.classList.contains("peek")); };
    btns.appendChild(w); btns.appendChild(pb); btns.appendChild(x); head.appendChild(btns);
    head.appendChild(el("div", "grab")); sheetGestures(head); setPeek(false);
    head.appendChild(el("div", "id", kicker)); head.appendChild(el("h3", null, title));
    if (pills && pills.length) { var vl = el("div", "verdictline"); pills.forEach(function (t) { vl.appendChild(el("span", "vpill" + (light ? " dark" : ""), t)); }); head.appendChild(vl); }
    panel.appendChild(head); pbody = el("div", "pbody"); panel.appendChild(pbody);
  }
  // ------------------------------------------------------------ phone bottom sheet
  // On phones the panel is a bottom sheet. It can be lowered (button, or swipe down on its header) to a peek bar
  // without clearing the selection, so the highlighted group can be panned and zoomed; tap or swipe up to restore.
  function isSheet() { return W <= 900; }
  function sheetInset() {
    if (!isSheet() || panel.style.display !== "block") return 0;
    return Math.min(panel.offsetHeight, H * 0.62) + 8;
  }
  function setPeek(on) {
    panel.classList.toggle("peek", !!on);
    var b = panel.querySelector(".pbtn");
    if (b) { b.textContent = on ? "▴" : "▾"; b.setAttribute("aria-expanded", on ? "false" : "true");
      b.setAttribute("aria-label", on ? "Show the details again" : "Lower the card to see the map"); b.title = b.getAttribute("aria-label"); }
    if (on) panel.scrollTop = 0;
  }
  function sheetGestures(head) {
    var drag = null;
    head.addEventListener("pointerdown", function (e) {
      if (!isSheet() || e.target.closest("button")) return;
      drag = { y: e.clientY, id: e.pointerId, moved: 0 }; head.setPointerCapture(e.pointerId);
    });
    head.addEventListener("pointermove", function (e) {
      if (!drag || e.pointerId !== drag.id) return;
      var dy = e.clientY - drag.y; drag.moved = Math.max(drag.moved, Math.abs(dy));
      if (!panel.classList.contains("peek") && dy > 0) panel.style.transform = "translateY(" + dy + "px)";
    });
    function end(e) {
      if (!drag || e.pointerId !== drag.id) return;
      var dy = e.clientY - drag.y, tap = drag.moved < 6; drag = null; panel.style.transform = "";
      if (panel.classList.contains("peek")) { if (tap || dy < -24) setPeek(false); }
      else if (dy > 48) setPeek(true);
    }
    head.addEventListener("pointerup", end);
    head.addEventListener("pointercancel", function () { drag = null; panel.style.transform = ""; });
  }
  function fitPanel() { var need = (panel.firstChild ? panel.firstChild.offsetHeight : 0) + (pbody ? pbody.offsetHeight : 0); panel.classList.toggle("fit", need < stage.clientHeight - 140); }
  function label(t) { pbody.appendChild(el("div", "label", t)); }
  function claimLink(id, box) {
    var c = byId[id].data, b = el("button", "link"); b.type = "button";
    var dot = el("span", "dot"); dot.style.background = c.verdict ? VC[c.verdict] : NOT_YET_COL;
    b.appendChild(dot); b.appendChild(document.createTextNode(c.id + "  " + c.title));
    b.onclick = function () { selectClaim(id); }; box.appendChild(b);
  }
  function openDocument(title, url) {
    document.getElementById("viewer-title").textContent = title;
    viewerFrame.removeAttribute("src"); viewerImage.removeAttribute("src");
    var isImage = /\.(png|jpe?g|webp|gif)$/i.test(url);
    viewerImage.hidden = !isImage; viewerFrame.hidden = isImage;
    if (isImage) viewerImage.src = url; else viewerFrame.src = url;
    if (typeof viewer.showModal === "function") viewer.showModal(); else window.open(url, "_blank", "noopener");
  }
  viewer.querySelector(".viewer-close").addEventListener("click", function () { viewer.close(); });
  viewer.addEventListener("click", function (event) { if (event.target === viewer) viewer.close(); });
  viewer.addEventListener("close", function () { viewerFrame.removeAttribute("src"); viewerImage.removeAttribute("src"); });
  function addFileAction(box, title, url) {
    var group = el("span", "file-action");
    var open = el("button", "btn", "Open " + title); open.type = "button"; open.onclick = function () { openDocument(title, url); };
    var download = el("a", "btn ghost", "Download"); download.href = url; download.download = url.split("/").pop();
    download.setAttribute("aria-label", "Download " + title);
    group.appendChild(open); group.appendChild(download); box.appendChild(group);
  }

  function selectClaim(id) {
    var c = byId[id]; if (!c) return; sel = { kind: "claim", id: id };
    var d = c.data;
    if (expanded && c.hub !== expanded) collapse();
    if (view === "map") { if (c.district && c.district !== mapLevel && unlocked(c.district)) enterDistrict(c.district); else if (!c.district && mapLevel) exitDistrict(); }
    var pills = d.verdict ? [d.verdict].concat(d.confidence ? [d.confidence + " confidence"] : []) : [d.status, "not yet checked"];
    openPanel(d.id + " · " + d.category.toUpperCase(), d.title, d.verdict ? VC[d.verdict] : NOT_YET_COL, pills);
    if (d.quote) pbody.appendChild(el("blockquote", null, "“" + d.quote + "”"));
    pbody.appendChild(el("p", null, d.claim));
    if (d.speaker) pbody.appendChild(el("p", "small", d.speaker + (d.date ? " · " + d.date : "")));
    var chips = el("div");
    if (d.verdict) chips.appendChild(el("span", "chip soft", d.status + (d.status === "Drafted" ? ", pending right of reply" : "")));
    if (d.wording_status && !d.verdict) chips.appendChild(el("span", "chip soft", d.wording_status));
    (d.tags || []).forEach(function (t) { chips.appendChild(el("span", "chip soft", t)); }); pbody.appendChild(chips);
    if (d.last_reviewed) {
      var days = c.reviewAgeDays || 0, remaining = Math.max(0, 365 - days);
      label("STUDY FRESHNESS");
      pbody.appendChild(el("p", "small", "Evidence last reviewed " + d.last_reviewed + " · " + (days >= 365 ? "refresh due" : remaining + " days until refresh due") + "."));
    }
    if (d.counter) { label("CONTEXT AND EVIDENCE"); pbody.appendChild(el("p", null, d.counter)); }
    var mine = edges.map(function (e, i) { return { e: e, i: i }; }).filter(function (o) { return o.e.from === id || o.e.to === id; });
    if (mine.length) {
      label("LINKED CLAIMS · CLICK A THEME OR A CLAIM"); var box = el("div", "links");
      mine.forEach(function (o) {
        var other = o.e.from === id ? o.e.to : o.e.from, row = el("div", "lrow");
        var tb = el("button", "tchip", themeById[o.e.theme] ? themeById[o.e.theme].name : o.e.theme); tb.type = "button";
        tb.style.borderColor = (themeById[o.e.theme] || {}).color || "#7fa88b"; tb.onclick = function () { selectEdge(o.i); };
        row.appendChild(tb); claimLink(other, row); box.appendChild(row);
      });
      pbody.appendChild(box);
    }
    var acts = el("div", "acts");
    var outputLabels = { report: "Report", report_pdf: "Report", flyer_pdf: "Flyer PDF", flyer_png: "Flyer image", document: "Document", appendix: "Appendix" };
    Object.keys(d.outputs || {}).forEach(function (key) { addFileAction(acts, outputLabels[key] || key.replace(/[_-]+/g, " "), d.outputs[key]); });
    var page = el("a", "btn", "Claim page"); page.href = "claims/" + d.id + "/"; acts.insertBefore(page, acts.firstChild);
    var rec = el("a", "btn ghost", "Claim record"); rec.href = d.record; rec.target = "_blank"; rec.rel = "noopener"; acts.appendChild(rec);
    if (c.hub && mode !== "network") { var hb = el("button", "btn ghost", c.hub.name); hb.type = "button"; hb.onclick = function () { selectHub(c.hub); }; acts.appendChild(hb); }
    pbody.appendChild(acts); fitPanel();
  }
  function selectHub(h) {
    sel = { kind: "hub", hub: h };
    var withV = h.claims.filter(function (c) { return c.data.verdict; }).length;
    openPanel(h.sub ? "SUBTOPIC · " + h.parent.name.toUpperCase() : MODES[mode].label.toUpperCase() + " GROUP", h.name, h.color, [h.count + (h.count === 1 ? " claim" : " claims"), withV + " with a verdict"]);
    if (view === "graph") expandHub(h);
    var list = h.claims, done = list.filter(function (c) { return c.data.verdict; }).length, reviewed = h.reviewLeaves || [];
    pbody.appendChild(el("p", "small", list.length + (list.length === 1 ? " claim" : " claims") + ", " + done + " with a verdict, " + reviewed.length + " completed evidence reviews."));
    if (reviewed.length) {
      label("LEAVES · ONE PER COMPLETED REVIEW"); var freshness = el("div", "links");
      reviewed.forEach(function (c) { var age = c.reviewAgeDays || 0;
        freshness.appendChild(el("p", "small", c.id + " · last reviewed " + c.data.last_reviewed + " · " + (age >= 365 ? "refresh due" : Math.max(0, 365 - age) + " days until due"))); });
      pbody.appendChild(freshness);
    }
    if (h.subs && h.subs.length) { // a topic lists its claims by subtopic
      h.subs.forEach(function (sh) { label(sh.name.toUpperCase()); var sb = el("div", "links"); sh.claims.forEach(function (c) { claimLink(c.id, sb); }); pbody.appendChild(sb); });
      var loose = list.filter(function (c) { return !c.sub; });
      if (loose.length) { label("NO SUBTOPIC"); var lb = el("div", "links"); loose.forEach(function (c) { claimLink(c.id, lb); }); pbody.appendChild(lb); }
    } else { label("CLAIMS IN THIS GROUP"); var box = el("div", "links");
      list.forEach(function (c) { claimLink(c.id, box); }); pbody.appendChild(box); }
    var also = claims.filter(function (c) { return c.extra.indexOf(h) >= 0; });
    if (also.length) { label("ALSO TAGGED (SECOND PATTERN)"); var b2 = el("div", "links"); also.forEach(function (c) { claimLink(c.id, b2); }); pbody.appendChild(b2); }
    fitPanel();
  }
  function selectEdge(i) {
    var e = edges[i], th = themeById[e.theme] || {}; sel = { kind: "edge", index: i, edge: e };
    openPanel("LINK · " + (th.link_type || e.link_type || "").toUpperCase(), th.name || e.theme, th.color, [e.from + " ↔ " + e.to]);
    var box = el("div", "links"); claimLink(e.from, box); claimLink(e.to, box); pbody.appendChild(box);
    if (th.description) { label("WHAT CONNECTS THEM"); pbody.appendChild(el("p", null, th.description)); }
    var chips = el("div"); chips.appendChild(el("span", "chip soft", "Strength: " + (e.strength || th.strength))); pbody.appendChild(chips);
    var acts = el("div", "acts"), all = el("button", "btn ghost", "Show every claim in this theme"); all.type = "button";
    all.onclick = function () { selectTheme(e.theme); }; acts.appendChild(all); pbody.appendChild(acts); fitPanel();
  }
  function selectTheme(id) {
    var th = themeById[id]; if (!th) return; sel = { kind: "theme", id: id };
    if (!themeOn[id]) { themeOn[id] = true; buildLinkBar(); }
    openPanel("THEME · " + (th.link_type || "").toUpperCase(), th.name, th.color, [(th.members || []).length + " claims", th.strength]);
    if (th.description) pbody.appendChild(el("p", null, th.description));
    var chips = el("div"); chips.appendChild(el("span", "chip soft", "Strength: " + th.strength)); pbody.appendChild(chips);
    label("CLAIMS LINKED BY THIS THEME"); var box = el("div", "links");
    (th.members || []).forEach(function (m) { if (byId[m]) claimLink(m, box); }); pbody.appendChild(box); fitPanel();
  }
  function clearSel() { sel = null; panel.classList.remove("peek"); panel.style.display = "none"; collapse(); }

  function showTip(h, x, y) {
    if (!h) { tip.style.display = "none"; return; }
    var txt;
    if (h.kind === "claim") { var d = byId[h.id].data; txt = d.id + " · " + d.title + (d.verdict ? " — " + d.verdict : " — not yet checked"); }
    else if (h.kind === "place") { var dn = h.place.claims.filter(function (c) { return c.data.verdict; }).length;
      txt = (h.place.discovered ? h.place.name : "Undiscovered site") + " · " + h.place.claims.length + (h.place.claims.length === 1 ? " claim" : " claims") + ", " + dn + " checked"; }
    else if (h.kind === "district") txt = h.locked ? lockText(h.d) : h.d.name + " · " + districtClaims(h.d).length + " claims · click to open";
    else if (h.kind === "hub") txt = (h.hub.sub ? h.hub.parent.name + " › " : "") + h.hub.name + " · " + h.hub.count + (h.hub.count === 1 ? " claim" : " claims");
    else { var th = themeById[h.edge.theme] || {}; txt = (th.name || h.edge.theme) + ": " + h.edge.from + " ↔ " + h.edge.to; }
    tip.textContent = txt; tip.style.display = "block";
    tip.style.left = Math.min(x + 14, W - tip.offsetWidth - 8) + "px"; tip.style.top = (y + 16) + "px";
  }

  // ------------------------------------------------------------ interaction
  var down = null, moved = 0, pinch = null, activePointers = {}, multiGesture = false;
  function pointerCount() { return Object.keys(activePointers).length; }
  function pointerDistance() {
    var pts = Object.keys(activePointers).map(function (id) { return activePointers[id]; });
    return pts.length > 1 ? Math.hypot(pts[0].x - pts[1].x, pts[0].y - pts[1].y) : 0;
  }
  function setSpin(v) { spinning = v; var b = document.getElementById("spin"); b.textContent = v ? "Pause" : "Resume";
    b.setAttribute("aria-label", v ? "Pause map rotation" : "Resume map rotation"); }
  function zoomAt(f, mx, my) {
    var z0 = cam.zoom, z1 = Math.max(ZMIN, Math.min(ZMAX, z0 * f)), r = z1 / z0;
    if (mx == null) { mx = cxNow + cam.px; my = cyNow + cam.py; }
    cam.tpx = cam.px = (mx - cxNow) - ((mx - cxNow) - cam.px) * r;
    cam.tpy = cam.py = (my - cyNow) - ((my - cyNow) - cam.py) * r;
    cam.zoom = z1; districtZoomCheck(mx, my);
  }
  function panBy(dx, dy) { cam.tpx = cam.px += dx; cam.tpy = cam.py += dy; }
  function orbitBy(dx, dy) {
    cam.yaw += dx * 0.006; if (cam.tyaw !== null) cam.tyaw += dx * 0.006;
    var lo = view === "map" ? 0.25 : -1.35, hi = view === "map" ? 1.45 : 1.35;
    cam.tpitch = cam.pitch = Math.max(lo, Math.min(hi, cam.pitch + dy * 0.006));
  }
  function midpoint() { var pts = Object.keys(activePointers).map(function (id) { return activePointers[id]; });
    return { x: (pts[0].x + pts[1].x) / 2, y: (pts[0].y + pts[1].y) / 2 }; }
  var dragKind = null, lastMid = null;
  canvas.addEventListener("contextmenu", function (e) { e.preventDefault(); });
  canvas.addEventListener("pointerdown", function (e) {
    activePointers[e.pointerId] = { x: e.clientX, y: e.clientY };
    canvas.setPointerCapture(e.pointerId); canvas.classList.add("dragging");
    if (pointerCount() > 1) { multiGesture = true; moved = 100; down = null; pinch = pointerDistance(); lastMid = midpoint(); }
    else { down = { x: e.clientX, y: e.clientY }; moved = 0;
      var alt = e.button === 2 || e.button === 1 || e.shiftKey || e.ctrlKey || e.metaKey;
      dragKind = view === "map" ? (alt ? "orbit" : "pan") : (alt ? "pan" : "orbit"); }
  });
  canvas.addEventListener("pointermove", function (e) {
    if (activePointers[e.pointerId]) activePointers[e.pointerId] = { x: e.clientX, y: e.clientY };
    var r = canvas.getBoundingClientRect();
    if (multiGesture && pointerCount() > 1) { var distance = pointerDistance(), mid = midpoint();
      if (lastMid) panBy(mid.x - lastMid.x, mid.y - lastMid.y);
      if (pinch && distance) zoomAt(distance / pinch, mid.x - r.left, mid.y - r.top);
      pinch = distance; lastMid = mid; down = null; showTip(null); return; }
    var mx = e.clientX - r.left, my = e.clientY - r.top;
    if (down) { var dx = e.clientX - down.x, dy = e.clientY - down.y; moved += Math.abs(dx) + Math.abs(dy);
      if (dragKind === "pan") panBy(dx, dy); else orbitBy(dx, dy);
      down = { x: e.clientX, y: e.clientY }; showTip(null); }
    else { hover = pick(mx, my); canvas.style.cursor = hover ? "pointer" : "grab"; showTip(hover, mx, my); }
  });
  canvas.addEventListener("pointerleave", function () { hover = null; showTip(null); });
  canvas.addEventListener("pointerup", function (e) {
    delete activePointers[e.pointerId];
    if (multiGesture) { down = null; pinch = null; lastMid = null; if (!pointerCount()) { multiGesture = false; canvas.classList.remove("dragging"); } return; }
    canvas.classList.remove("dragging");
    if (moved < 6) { var r = canvas.getBoundingClientRect(); var h = pick(e.clientX - r.left, e.clientY - r.top);
      if (!h) clearSel(); else if (h.kind === "district") { if (!h.locked) enterDistrict(h.d); else showToast(lockText(h.d)); } else if (h.kind === "place") selectPlace(h.place); else if (h.kind === "claim") selectClaim(h.id); else if (h.kind === "hub") selectHub(h.hub); else selectEdge(h.index); }
    else if (view === "graph" && dragKind === "orbit") setSpin(false);
    down = null;
  });
  canvas.addEventListener("pointercancel", function () { activePointers = {}; down = null; pinch = null; lastMid = null; multiGesture = false; canvas.classList.remove("dragging"); });
  canvas.addEventListener("wheel", function (e) { e.preventDefault(); var r = canvas.getBoundingClientRect();
    if (e.ctrlKey || Math.abs(e.deltaY) >= Math.abs(e.deltaX) || view === "graph") zoomAt(Math.exp(-e.deltaY * (e.ctrlKey ? 0.01 : 0.0018)), e.clientX - r.left, e.clientY - r.top);
    else panBy(-e.deltaX, 0); }, { passive: false });
  canvas.addEventListener("dblclick", function (e) { var r = canvas.getBoundingClientRect(), mx = e.clientX - r.left, my = e.clientY - r.top;
    var h = pick(mx, my); if (h && h.kind === "district" && !h.locked) { enterDistrict(h.d); return; } if (!h) zoomAt(1.7, mx, my); });
  canvas.addEventListener("keydown", function (e) {
    var step = 40, used = true;
    if (e.key === "ArrowLeft") { if (view === "map") panBy(step, 0); else orbitBy(-step, 0); }
    else if (e.key === "ArrowRight") { if (view === "map") panBy(-step, 0); else orbitBy(step, 0); }
    else if (e.key === "ArrowUp") { if (view === "map") panBy(0, step); else orbitBy(0, -step); }
    else if (e.key === "ArrowDown") { if (view === "map") panBy(0, -step); else orbitBy(0, step); }
    else if (e.key === "+" || e.key === "=") zoomAt(1.2); else if (e.key === "-" || e.key === "_") zoomAt(1 / 1.2);
    else if (e.key === "0") fitView(); else used = false;
    if (used) { e.preventDefault(); setSpin(false); }
  });
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape") clearSel();
    if ((e.target === document.body || e.target === canvas) && /^[1-7]$/.test(e.key)) setMode(MODE_ORDER[+e.key - 1]);
    if ((e.target === document.body || e.target === canvas) && (e.key === "m" || e.key === "M")) setView(view === "map" ? "graph" : "map");
  });
  document.getElementById("spin").onclick = function () { setSpin(!spinning); };
  function syncLens() { var b = document.getElementById("lenstoggle"); b.setAttribute("aria-pressed", lensWanted() ? "true" : "false"); }
  document.getElementById("lenstoggle").onclick = function () { lensPref = !lensWanted();
    try { localStorage.setItem("mizien.lens", lensPref ? "on" : "off"); } catch (e) {} syncLens(); };
  function syncLabelButtons() {
    var lb = document.getElementById("labelmode"), tb = document.getElementById("texttoggle");
    lb.textContent = labelMode === "tag" ? "Codes" : "Names"; lb.setAttribute("aria-pressed", labelMode === "tag" ? "true" : "false");
    lb.title = labelMode === "tag" ? "Show claim codes (CC-001)" : "Show claim names instead of codes";
    tb.textContent = showText ? "Hide text" : "Show text"; tb.setAttribute("aria-pressed", showText ? "false" : "true");
  }
  document.getElementById("labelmode").onclick = function () { labelMode = labelMode === "tag" ? "code" : "tag";
    try { localStorage.setItem("mizien.labels", labelMode); } catch (e) {} syncLabelButtons(); };
  document.getElementById("texttoggle").onclick = function () { showText = !showText;
    try { localStorage.setItem("mizien.text", showText ? "on" : "off"); } catch (e) {} syncLabelButtons(); };
  syncLabelButtons(); syncLens(); window.addEventListener("resize", syncLens);
  document.getElementById("zoomout").onclick = function () { zoomAt(1 / 1.25); };
  document.getElementById("zoomin").onclick = function () { zoomAt(1.25); };
  document.getElementById("reset").onclick = function () { fitView(); };
  document.addEventListener("keydown", function (e) { if (e.target !== document.body) return;
    if (e.key === "n" || e.key === "N") document.getElementById("labelmode").click();
    if (e.key === "t" || e.key === "T") document.getElementById("texttoggle").click();
    if (e.key === "l" || e.key === "L") document.getElementById("lenstoggle").click(); });
  window.addEventListener("resize", resize);
  if (reduce) setSpin(false);

  var previewPayload = new URLSearchParams(location.search).get("previewData");
  if (previewPayload) {
    try { init(JSON.parse(previewPayload)); } catch (e) { stage.appendChild(el("p", null, "The embedded map data could not be read.")).style.cssText = "padding:24px;color:#e3a72f"; }
  } else {
    fetch("data/claims.json", { cache: "no-cache" }).then(function (r) { return r.json(); }).then(init).catch(function () {
      stage.appendChild(el("p", null, "Could not load data/claims.json. If you opened this file directly, serve the docs folder instead (python -m http.server -d docs).")).style.cssText = "padding:24px;color:#e3a72f";
    });
  }
})();
