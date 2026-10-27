// "Who said it" summaries (site/bodies/): computed at build time from the same claim data as the rest of the site, so
// the counts here, in Explore and on the timeline never disagree.
//
// whoSummary(body): what a body's row, panel and page show about its claims, as one verdict strip for every body
//   (maintainer decision, 27 Oct 2026, replacing the three-tier bar / tentative balance / count of 6 Oct 2026):
//   one square per claim, the checked ones filled in verdict order from Contradicted to Supported, the rest hollow.
//   Counts, never percentages. Below 5 checks the strip carries the note "too few to summarise".
//   Pledge labels are always shown, apart from the verdicts.
// pledgeStack(pledges, claims, ids?): the pledges as dots on stacked disks, one disk per election cycle (newest on top).
//   Pledges on the same topic sit at the same angle, so similar pledges line up vertically; lines join similar pledges
//   made in different years, coloured by the average verdict of the facts checked in them.

export const FEW_MIN = 5;
const ORDER = ["Contradicted", "Misleading", "Not substantiated", "Largely supported", "Supported"];
const SLUG = { "Supported": "supported", "Largely supported": "largely-supported", "Not substantiated": "not-substantiated", "Misleading": "misleading", "Contradicted": "contradicted" };
const VALUE = { "Supported": 1, "Largely supported": 0.75, "Not substantiated": 0.5, "Misleading": 0.25, "Contradicted": 0 };
const COLOUR = { "Supported": "#2e7d4f", "Largely supported": "#8db36b", "Not substantiated": "#d9772b", "Misleading": "#b5483a", "Contradicted": "#8e2f25" };

function esc(s) { return String(s ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[c]); }
// "2024-12-31", "2026-05" or "2025" -> the middle of the period it names, as a Date (null if unreadable)
export function claimDate(s) {
  const m = /^(\d{4})(?:-(\d{2}))?(?:-(\d{2}))?/.exec(String(s ?? ""));
  if (!m) return null;
  return new Date(Date.UTC(+m[1], m[2] ? +m[2] - 1 : 6, m[3] ? +m[3] : m[2] ? 15 : 1));
}

// A body's pledges are those it made itself or through its offices and people (the pledge's "made by"), so a party's
// manifesto pledge stays with the party even when a ministry later reports on it.
export function family(body, bodies) {
  const ids = new Set([body.id]);
  for (const b of bodies || []) if ((b.ancestors || []).some((a) => a.id === body.id)) ids.add(b.id);
  return ids;
}
export function whoSummary(body, pledgeList, bodies) {
  const mine = family(body, bodies);
  const own = (pledgeList || []).filter((p) => (p.pledge?.made_by_ids || []).some((x) => mine.has(x)));
  const pl = Object.fromEntries(own.filter((p) => p.pledge.kind !== "target").map((p) => [p.id, p]));   // institutional targets are listed apart
  const targets = own.filter((p) => p.pledge.kind === "target").map((p) => ({ id: p.id, title: p.title, path: p.path, ...p.pledge }));
  const claims = body?.claims || [];
  const checked = claims.filter((c) => c.verdict && VALUE[c.verdict] != null);
  const counts = ORDER.map((v) => ({ name: v, slug: SLUG[v], colour: COLOUR[v], n: checked.filter((c) => c.verdict === v).length })).filter((x) => x.n);
  // the strip: one entry per claim, checked ones first in verdict order, then the rest (pledge-only and unchecked)
  const squares = counts.flatMap((v) => Array.from({ length: v.n }, () => ({ slug: v.slug, name: v.name })));
  const pledges = Object.values(pl).map((p) => ({ id: p.id, title: p.title, path: p.path, ...p.pledge }));
  return {
    total: claims.length, checked: checked.length, waiting: claims.length - checked.length, counts, squares,
    few: checked.length < FEW_MIN, fewMin: FEW_MIN,
    dates: checked.map((c) => claimDate(c.date)).filter(Boolean).sort((a, b) => a - b),
    pledges, targets,
  };
}

// ---- the pledge stack
function verdictColour(avg) {   // an average on the 0..1 scale -> the colour of the nearest verdict
  let best = ORDER[0], d = 9;
  for (const v of ORDER) { const k = Math.abs(VALUE[v] - avg); if (k < d) { d = k; best = v; } }
  return { colour: COLOUR[best], name: best };
}
// A pledge's disk is its election cycle (scripts/pledges.py): campaign pledges sit on the election they were made for,
// commitments in office on the legislature they were made in. Cycles sort by their year ("before-2022" first).
function pledgeYear(p) { return p.pledge?.cycle || null; }
function cycleKey(c) { return c.startsWith("before-") ? +c.slice(7) - 0.5 : +c; }
const RING = { campaign: 1, proposal: 1, government: 0.58 };   // the outer ring: promises made in a campaign; inside: in office
export function pledgeStack(pledges, claims, ids) {
  const byId = Object.fromEntries((claims || []).map((c) => [c.id, c]));
  const want = ids ? new Set(ids) : null;
  const list = (pledges || []).filter((p) => (!want || want.has(p.id)) && pledgeYear(p) && p.pledge?.kind !== "target");
  if (!list.length) return null;
  const years = [...new Set(list.map(pledgeYear))].sort((a, b) => cycleKey(a) - cycleKey(b));
  const labelOf = Object.fromEntries(list.map((p) => [pledgeYear(p), p.pledge.cycle_label || pledgeYear(p)]));
  const topics = [...new Set(list.map((p) => p.category))].sort();
  // geometry: flat disks seen from slightly above, the newest on top
  // geometry, shared with assets/pstack.js (which turns and tilts the stack): rx the disk radius, ry its height on
  // screen at the starting tilt; the gap between disks grows with the tilt so the back of a disk stays clear of the
  // front of the one above
  const W = 660, rx = 230, ry = 44, cx = 340, top = 30, gap = Math.max(132, 2 * ry + 44);
  const H = top + ry + (years.length - 1) * gap + ry + 30;
  const level = (y) => years.length - 1 - years.indexOf(y);   // 0 = the top (newest) disk
  const cyOf = (y) => top + ry + level(y) * gap;
  const sector = (t) => topics.indexOf(t) / topics.length * Math.PI * 2 + Math.PI * 0.5;   // topics spaced round the disk, the first at the front
  const slot = {};
  const dots = list.map((p) => {
    const y = pledgeYear(p), key = y + "|" + p.category, k = (slot[key] = (slot[key] ?? -1) + 1);
    const same = list.filter((q) => pledgeYear(q) === y && q.category === p.category).length;
    const a = sector(p.category) + (k - (same - 1) / 2) * Math.min(0.5, 1.6 / topics.length);   // several on one topic and year: side by side
    const full = byId[p.id] || {}, k2 = RING[p.pledge.kind] || 1;
    return { p, y, a, k2, x: cx + Math.cos(a) * rx * k2, yy: cyOf(y) + Math.sin(a) * ry * k2, front: Math.sin(a) >= 0, full,
      verdict: p.verdict && VALUE[p.verdict] != null ? p.verdict : null };
  });
  // similar pledges made in different years: the same topic, the same subtopic, or similar wording (scripts/similarity.py)
  const edges = [];
  for (let i = 0; i < dots.length; i++) for (let j = i + 1; j < dots.length; j++) {
    const A = dots[i], B = dots[j]; if (A.y === B.y) continue;
    const sim = (A.full.similar || []).some((s) => s.id === B.p.id) || (B.full.similar || []).some((s) => s.id === A.p.id);
    const why = sim ? "similar wording" : A.p.subtopic && A.p.subtopic === B.p.subtopic ? "same subtopic" : A.p.category === B.p.category ? "same topic" : null;
    if (!why) continue;
    const vs = [A.verdict, B.verdict].filter(Boolean).map((v) => VALUE[v]);
    const avg = vs.length ? vs.reduce((s, x) => s + x, 0) / vs.length : null;
    edges.push({ a: A, b: B, why, avg, ...(avg == null ? { colour: "#8a9a90", name: null } : verdictColour(avg)) });
  }
  const svg = [];
  svg.push(`<svg class="pstack" viewBox="0 0 ${W} ${H}" role="img" aria-labelledby="pstack-t pstack-d" data-geo='${JSON.stringify({ W, rx, ry, cx, top, n: years.length })}'>`);
  svg.push(`<title id="pstack-t">Pledges by election cycle</title><desc id="pstack-d">${esc(years.length)} disks, one per election cycle, newest on top; campaign pledges on the outer ring, commitments in office inside; ${esc(list.length)} pledges; lines join similar pledges made in different years.</desc>`);
  // disks, oldest (bottom) first so newer ones lie over them
  for (const y of years) {
    const cy = cyOf(y), n = list.filter((p) => pledgeYear(p) === y).length;
    svg.push(`<g class="ps-disk" data-l="${level(y)}"><ellipse cx="${cx}" cy="${cy + 7}" rx="${rx}" ry="${ry}" class="ps-edge-band"/><ellipse cx="${cx}" cy="${cy}" rx="${rx}" ry="${ry}" class="ps-top"/>` +
      `<ellipse cx="${cx}" cy="${cy}" rx="${(rx * RING.government).toFixed(1)}" ry="${(ry * RING.government).toFixed(1)}" class="ps-inner"/><text x="${cx - rx - 22}" y="${cy + 5}" class="ps-year" text-anchor="end">${esc(labelOf[y])}</text><text x="${cx - rx - 22}" y="${cy + 22}" class="ps-n" text-anchor="end">${n} pledge${n === 1 ? "" : "s"}</text></g>`);
  }
  for (const e of edges) {
    const dash = e.avg == null ? ` stroke-dasharray="5 4"` : "";
    svg.push(`<line data-a="${dots.indexOf(e.a)}" data-b="${dots.indexOf(e.b)}" x1="${e.a.x.toFixed(1)}" y1="${e.a.yy.toFixed(1)}" x2="${e.b.x.toFixed(1)}" y2="${e.b.yy.toFixed(1)}" class="ps-link" stroke="${e.colour}"${dash}><title>${esc(e.a.p.id)} and ${esc(e.b.p.id)}: ${esc(e.why)}${e.name ? `; average verdict of the facts checked: ${esc(e.name)}` : "; no verdict on the facts yet"}</title></line>`);
  }
  for (const d of dots) {
    // a pledge is a square (a promise), in its label colour; a check that also tested facts has the verdict as a dot inside
    const pv = d.p.pledge || {};
    svg.push(`<a href="${esc(d.p.path)}" class="ps-dot" data-a="${d.a.toFixed(4)}" data-l="${level(d.y)}" data-r="${d.k2}"><title>${esc(d.p.id)} ${esc(d.p.title)}: pledge ${esc(pv.status)}${d.verdict ? `; facts: ${esc(d.verdict)}` : ""}</title>` +
      `<rect x="${(d.x - 9).toFixed(1)}" y="${(d.yy - 9).toFixed(1)}" width="18" height="18" rx="2.5" fill="${esc(pv.colour || "#b0b8c1")}" stroke="#eef3ef" stroke-width="1.6"/>` +
      (d.verdict ? `<circle cx="${d.x.toFixed(1)}" cy="${d.yy.toFixed(1)}" r="4.6" fill="${COLOUR[d.verdict]}" stroke="#eef3ef" stroke-width="1.2"/>` : "") +
      `<text x="${(d.x + 13).toFixed(1)}" y="${(d.yy + 4).toFixed(1)}" class="ps-id">${esc(d.p.id)}</text></a>`);
  }
  svg.push(`</svg>`);
  const rows = years.slice().reverse().map((y) => ({ year: labelOf[y], items: dots.filter((d) => d.y === y).map((d) => ({ ...d.p, factVerdict: d.verdict })) }));
  return { svg: svg.join(""), rows, edges: edges.length, topics, years };
}
