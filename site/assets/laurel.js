/* Laurels: the leaves around a group in the claims web, a place on the map and a clump on the timeline.
   One leaf per checked claim, coloured by its verdict (or pledge label). The laurel grows from the bottom left, up
   over the top and down the right, one slot per claim in the group, so a full laurel means every claim there is
   checked, and the colours read in order from the best verdict to the worst. A leaf's opacity is the freshness of
   the evidence behind it: full for a review in the last three months, fading over the year, and only a faint outline
   once the review is more than a year old.
   Leaves never cover each other: their size follows the space per slot, and a crowded group gets a second ring.

   MizienLaurel.leaves(n, r)          -> placements for an n-slot laurel around a disc of radius r (centre 0,0)
   MizienLaurel.svg(list, n, r, cx, cy) -> SVG markup; list = [{ color, reviewed }] in slot order
   MizienLaurel.draw(ctx, list, n, r, x, y, alpha) draws the same on a canvas
   MizienLaurel.extent(n, r)         -> the outer radius the laurel reaches (to size a box around it) */
(function () {
  "use strict";
  var START = Math.PI * (0.5 + 0.2), SPAN = Math.PI * 1.6;   // from just left of the bottom, clockwise round to just right of it
  var TILT = 0.62;                                           // leaves lie along the branch, tilted outwards (radians off the tangent)
  var cache = {};
  function geometry(n, r) {
    var key = n + "|" + Math.round(r * 4);
    if (cache[key]) return cache[key];
    // Neighbouring leaves are parallel, s apart along the branch, so they never touch while s * sin(TILT) >= the leaf's
    // width (0.4 L), i.e. L <= 1.45 s; 1.3 s keeps a margin. Too little room: a second ring, then a wider laurel.
    var maxL = Math.max(8, Math.min(14, r * 0.72)), minL = 5, gap = 2.5, K = 1.3;
    var rings = 1, R1 = r + gap, s = R1 * SPAN / Math.max(1, n), L = Math.min(maxL, K * s);
    if (L < minL && n > 1) {                                 // too many slots for one ring: alternate them over two
      rings = 2; s = R1 * SPAN / Math.ceil(n / 2); L = Math.min(maxL, K * s);
      if (L < minL) { L = minL; R1 = Math.max(R1, (Math.ceil(n / 2) * L / K) / SPAN); }
    }
    var R2 = R1 + L * 0.95, out = [];
    for (var i = 0; i < n; i++) {
      var ring = rings === 2 ? i % 2 : 0, k = rings === 2 ? Math.floor(i / 2) : i, per = rings === 2 ? Math.ceil(n / 2) : n;
      var a = START + (k + (ring ? 0.75 : 0.5)) / per * SPAN, R = ring ? R2 : R1;
      // the leaf grows from the branch, pointing along it (clockwise) and tilted outwards
      out.push({ x: Math.cos(a) * R, y: Math.sin(a) * R, rot: a + Math.PI / 2 - TILT, L: L, W: L * 0.4 });
    }
    return (cache[key] = { slots: out, outer: (rings === 2 ? R2 : R1) + L, R1: R1, L: L });
  }
  function days(when) {
    var t = Date.parse(String(when || "") + "T00:00:00Z");
    return isFinite(t) ? Math.max(0, (Date.now() - t) / 86400000) : 0;
  }
  // Freshness: opaque up to 90 days, fading to 0.15 at a year; beyond a year, an outline only.
  function look(reviewed) {
    var d = days(reviewed);
    if (d > 365) return { fill: 0, line: 0.55 };
    return { fill: d <= 90 ? 1 : Math.max(0.15, 1 - (d - 90) / 275 * 0.85), line: 0.9 };
  }
  function leafPath(x, y, rot, L, W) {
    var c = Math.cos(rot), s = Math.sin(rot);
    function P(u, v) { return (x + u * c - v * s).toFixed(1) + " " + (y + u * s + v * c).toFixed(1); }
    return "M" + P(0, 0) + " Q" + P(L * 0.45, -W) + " " + P(L, 0) + " Q" + P(L * 0.45, W) + " " + P(0, 0) + "Z";
  }
  function svg(list, n, r, cx, cy) {
    if (!list.length) return "";
    var g = geometry(Math.max(n, list.length), r), out = [];
    // the branch: a faint stem along the filled part of the laurel
    var last = g.slots[list.length - 1], a0 = START, a1 = Math.atan2(last.y, last.x);
    while (a1 < a0) a1 += Math.PI * 2;
    var R = g.R1 - 0.5, big = a1 - a0 > Math.PI ? 1 : 0;
    out.push('<path class="stem" d="M' + (cx + Math.cos(a0) * R).toFixed(1) + " " + (cy + Math.sin(a0) * R).toFixed(1) + " A" + R.toFixed(1) + " " + R.toFixed(1) +
      " 0 " + big + " 1 " + (cx + Math.cos(a1) * R).toFixed(1) + " " + (cy + Math.sin(a1) * R).toFixed(1) + '" fill="none" stroke="rgba(246,244,238,.35)" stroke-width="1"/>');
    list.forEach(function (it, i) {
      var p = g.slots[i], k = look(it.reviewed);
      out.push('<path class="leaf" d="' + leafPath(cx + p.x, cy + p.y, p.rot, p.L, p.W) + '" fill="' + it.color + '" fill-opacity="' + k.fill.toFixed(2) +
        '" stroke="rgba(246,244,238,' + k.line + ')" stroke-width="0.9"/>');
    });
    return out.join("");
  }
  function draw(ctx, list, n, r, x, y, alpha) {
    if (!list.length) return;
    var g = geometry(Math.max(n, list.length), r), A = alpha == null ? 1 : alpha;
    var last = g.slots[list.length - 1], a1 = Math.atan2(last.y, last.x);
    while (a1 < START) a1 += Math.PI * 2;
    ctx.save(); ctx.lineCap = "round";
    ctx.globalAlpha = A * 0.35; ctx.strokeStyle = "#f6f4ee"; ctx.lineWidth = 1;
    ctx.beginPath(); ctx.arc(x, y, g.R1 - 0.5, START, a1); ctx.stroke();
    list.forEach(function (it, i) {
      var p = g.slots[i], k = look(it.reviewed), c = Math.cos(p.rot), s = Math.sin(p.rot), bx = x + p.x, by = y + p.y;
      ctx.beginPath(); ctx.moveTo(bx, by);
      ctx.quadraticCurveTo(bx + p.L * 0.45 * c + p.W * s, by + p.L * 0.45 * s - p.W * c, bx + p.L * c, by + p.L * s);
      ctx.quadraticCurveTo(bx + p.L * 0.45 * c - p.W * s, by + p.L * 0.45 * s + p.W * c, bx, by);
      if (k.fill > 0) { ctx.globalAlpha = A * k.fill; ctx.fillStyle = it.color; ctx.fill(); }
      ctx.globalAlpha = A * k.line; ctx.strokeStyle = "#f6f4ee"; ctx.lineWidth = 0.9; ctx.stroke();
    });
    ctx.restore();
  }
  window.MizienLaurel = {
    leaves: function (n, r) { return geometry(n, r).slots; },
    extent: function (n, r) { return n ? geometry(n, r).outer : r; },
    svg: svg, draw: draw, look: look, days: days
  };
})();
