/* Pledges, year by year (site/_lib/who.js draws it): drag the stack sideways to turn it, like a turntable, and up or
   down to tilt it. The tilt is limited so the disks are always seen from above, never edge-on or from below, and the
   order of the years (newest on top) never flips. Arrow keys do the same when the figure has focus; Home resets. */
(function () {
  "use strict";
  var TILT_MIN = 0.1, TILT_MAX = 0.3;   // radians from edge-on: about 6 to 17 degrees, always from above
  document.querySelectorAll("svg.pstack[data-geo]").forEach(function (svg) {
    var G = JSON.parse(svg.getAttribute("data-geo")), tilt0 = Math.asin(G.ry / G.rx), yaw = 0, tilt = tilt0;
    var disks = svg.querySelectorAll(".ps-disk"), dots = Array.prototype.slice.call(svg.querySelectorAll(".ps-dot")), links = svg.querySelectorAll(".ps-link");
    var reduce = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;
    function draw() {
      var ry = G.rx * Math.sin(tilt), gap = Math.max(132, 2 * ry + 44), H = G.top + ry + (G.n - 1) * gap + ry + 30;
      svg.setAttribute("viewBox", "0 0 " + G.W + " " + H.toFixed(1));
      function cy(l) { return G.top + ry + l * gap; }
      disks.forEach(function (g) { var c = cy(+g.dataset.l), e = g.querySelectorAll("ellipse"), t = g.querySelectorAll("text");
        e[0].setAttribute("cy", (c + 7).toFixed(1)); e[0].setAttribute("ry", ry.toFixed(1)); e[1].setAttribute("cy", c.toFixed(1)); e[1].setAttribute("ry", ry.toFixed(1));
        t[0].setAttribute("y", (c + 5).toFixed(1)); t[1].setAttribute("y", (c + 22).toFixed(1)); });
      var P = dots.map(function (d) { var a = +d.dataset.a + yaw, x = G.cx + Math.cos(a) * G.rx, y = cy(+d.dataset.l) + Math.sin(a) * ry;
        var c = d.querySelector("circle"), t = d.querySelector("text");
        c.setAttribute("cx", x.toFixed(1)); c.setAttribute("cy", y.toFixed(1)); t.setAttribute("x", (x + 13).toFixed(1)); t.setAttribute("y", (y + 4).toFixed(1));
        d.style.opacity = Math.sin(a) < -0.2 ? 0.75 : 1;   // the far side of a disk is a little fainter
        return { x: x, y: y }; });
      links.forEach(function (l) { var a = P[+l.dataset.a], b = P[+l.dataset.b];
        l.setAttribute("x1", a.x.toFixed(1)); l.setAttribute("y1", a.y.toFixed(1)); l.setAttribute("x2", b.x.toFixed(1)); l.setAttribute("y2", b.y.toFixed(1)); });
    }
    function turn(dyaw, dtilt) { yaw += dyaw; tilt = Math.max(TILT_MIN, Math.min(TILT_MAX, tilt + dtilt)); draw(); }
    // drag: sideways turns, up and down tilts (on touch, only sideways: up and down scrolls the page)
    var start = null, moved = false;
    svg.addEventListener("pointerdown", function (e) { svg.classList.remove("kb"); if (e.button) return; start = { x: e.clientX, y: e.clientY, touch: e.pointerType === "touch" }; moved = false; });
    svg.addEventListener("pointermove", function (e) {
      if (!start) return; var dx = e.clientX - start.x, dy = e.clientY - start.y;
      if (!moved && Math.hypot(dx, dy) < 6) return;
      if (!moved && start.touch && Math.abs(dy) > Math.abs(dx)) { start = null; return; }
      if (!moved) { moved = true; try { svg.setPointerCapture(e.pointerId); } catch (er) {} svg.classList.add("is-turning"); }
      var w = svg.getBoundingClientRect().width / G.W;
      turn(-dx / w * 0.006, start.touch ? 0 : -dy / w * 0.002); start.x = e.clientX; start.y = e.clientY;
    });
    function end() { start = null; svg.classList.remove("is-turning"); }
    svg.addEventListener("pointerup", end); svg.addEventListener("pointercancel", end);
    svg.addEventListener("click", function (e) { if (moved) { e.preventDefault(); moved = false; } }, true);   // a drag is not a click on a pledge
    svg.setAttribute("tabindex", "0");
    svg.addEventListener("keydown", function (e) {
      var k = e.key, used = true; svg.classList.add("kb");
      if (k === "ArrowLeft") turn(0.15, 0); else if (k === "ArrowRight") turn(-0.15, 0);
      else if (k === "ArrowUp") turn(0, 0.04); else if (k === "ArrowDown") turn(0, -0.04);
      else if (k === "Home") { yaw = 0; tilt = tilt0; draw(); } else used = false;
      if (used) e.preventDefault();
    });
    svg.classList.add("is-live");
    var hint = svg.closest(".pstack-fig") && svg.closest(".pstack-fig").querySelector(".ps-hint"); if (hint) hint.hidden = false;
    if (!reduce) { var t0 = null; (function intro(ts) { if (t0 === null) t0 = ts; var k = Math.min(1, (ts - t0) / 1200); yaw = -0.35 * Math.sin(k * Math.PI); draw(); if (k < 1) requestAnimationFrame(intro); else { yaw = 0; draw(); } })(performance.now()); }
  });
})();
