// "Who said it" summaries (site/bodies/): computed at build time from the same claim data as the rest of the site, so
// the counts here, in Explore and on the timeline never disagree.
//
// whoSummary(body): what a body's card and page show about its checked claims.
//   - 5 or more checked claims: a verdict bar (counts per verdict, never percentages).
//   - 3 or 4: a tentative balance, shown as work in progress until there are enough checks for a bar. Each checked
//     claim is placed on the verdict scale (Contradicted 0 ... Supported 1) and weighted by the freshness of the
//     claim itself (the date it was made, not the date of the check): the weight halves every two years of age, and
//     an undated claim counts as if three years old.
//   - fewer: a count only ("1 of 5 checks so far").
//   Pledge labels are always shown, apart from the verdicts.
// pledgeStack(pledges, claims, ids?): the pledges as dots on stacked disks, one disk per year the pledge was made
//   (newest on top). Pledges on the same topic sit at the same angle, so similar pledges line up vertically; lines join
//   similar pledges made in different years, coloured by the average verdict of the facts checked in them.

export const BAR_MIN = 5, TENTATIVE_MIN = 3, HALF_LIFE_YEARS = 2, UNDATED_YEARS = 3;
const ORDER = ["Supported", "Largely supported", "Not substantiated", "Misleading", "Contradicted"];
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
export function freshness(date, now = new Date()) {
  const d = claimDate(date), years = d ? Math.max(0, (now - d) / (365.25 * 864e5)) : UNDATED_YEARS;
  return Math.pow(0.5, years / HALF_LIFE_YEARS);
}

// A body's pledges are those it made itself or through its offices and people (the pledge's "made by"), so a party's
// manifesto pledge stays with the party even when a ministry later reports on it.
export function family(body, bodies) {
  const ids = new Set([body.id]);
  for (const b of bodies || []) if ((b.ancestors || []).some((a) => a.id === body.id)) ids.add(b.id);
  return ids;
}
export function whoSummary(body, pledgeList, bodies, now = new Date()) {
  const mine = family(body, bodies);
  const pl = Object.fromEntries((pledgeList || []).filter((p) => (p.pledge?.made_by_ids || []).some((x) => mine.has(x))).map((p) => [p.id, p]));
  const claims = body?.claims || [];
  const checked = claims.filter((c) => c.verdict && VALUE[c.verdict] != null);
  const counts = ORDER.map((v) => ({ name: v, slug: SLUG[v], colour: COLOUR[v], n: checked.filter((c) => c.verdict === v).length })).filter((x) => x.n);
  const pledges = Object.values(pl).map((p) => ({ id: p.id, title: p.title, path: p.path, ...p.pledge }));
  let sw = 0, sv = 0;
  for (const c of checked) { const w = freshness(c.date, now); sw += w; sv += w * VALUE[c.verdict]; }
  const tier = checked.length >= BAR_MIN ? "bar" : checked.length >= TENTATIVE_MIN ? "tentative" : "few";
  return {
    total: claims.length, checked: checked.length, waiting: claims.length - checked.length, tier, counts,
    score: sw ? sv / sw : null, need: Math.max(0, BAR_MIN - checked.length), barMin: BAR_MIN,
    dates: checked.map((c) => claimDate(c.date)).filter(Boolean).sort((a, b) => a - b),
    pledges,
  };
}

// ---- the pledge stack
function verdictColour(avg) {   // an average on the 0..1 scale -> the colour of the nearest verdict
  let best = ORDER[0], d = 9;
  for (const v of ORDER) { const k = Math.abs(VALUE[v] - avg); if (k < d) { d = k; best = v; } }
  return { colour: COLOUR[best], name: best };
}
function pledgeYear(p) {
  const pv = p.pledge || {};
  const m = /(\d{4})/.exec(pv.made_on || "") || /^(\d{4})/.exec(p.date || "");
  return m ? +m[1] : null;
}
export function pledgeStack(pledges, claims, ids) {
  const byId = Object.fromEntries((claims || []).map((c) => [c.id, c]));
  const want = ids ? new Set(ids) : null;
  const list = (pledges || []).filter((p) => (!want || want.has(p.id)) && pledgeYear(p));
  if (!list.length) return null;
  const years = [...new Set(list.map(pledgeYear))].sort((a, b) => a - b);
  const topics = [...new Set(list.map((p) => p.category))].sort();
  // geometry: flat disks seen from slightly above, the newest on top
  const W = 700, rx = 236, ry = 48, gap = 108, cx = 300, top = 34;
  const H = top + ry + (years.length - 1) * gap + ry + 30;
  const cyOf = (y) => top + ry + (years.length - 1 - years.indexOf(y)) * gap;
  const sector = (t) => topics.indexOf(t) / topics.length * Math.PI * 2 + Math.PI * 0.5;   // topics spaced round the disk, the first at the front
  const slot = {};
  const dots = list.map((p) => {
    const y = pledgeYear(p), key = y + "|" + p.category, k = (slot[key] = (slot[key] ?? -1) + 1);
    const same = list.filter((q) => pledgeYear(q) === y && q.category === p.category).length;
    const a = sector(p.category) + (k - (same - 1) / 2) * Math.min(0.5, 1.6 / topics.length);   // several on one topic and year: side by side
    const full = byId[p.id] || {};
    return { p, y, a, x: cx + Math.cos(a) * rx, yy: cyOf(y) + Math.sin(a) * ry, front: Math.sin(a) >= 0, full,
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
  svg.push(`<svg class="pstack" viewBox="0 0 ${W} ${H}" role="img" aria-labelledby="pstack-t pstack-d">`);
  svg.push(`<title id="pstack-t">Pledges by the year they were made</title><desc id="pstack-d">${esc(years.length)} disks, one per year, newest on top; ${esc(list.length)} pledges; lines join similar pledges made in different years.</desc>`);
  // disks, oldest (bottom) first so newer ones lie over them
  for (const y of years) {
    const cy = cyOf(y), n = list.filter((p) => pledgeYear(p) === y).length;
    svg.push(`<g class="ps-disk"><ellipse cx="${cx}" cy="${cy + 7}" rx="${rx}" ry="${ry}" class="ps-edge-band"/><ellipse cx="${cx}" cy="${cy}" rx="${rx}" ry="${ry}" class="ps-top"/>` +
      `<text x="${cx + rx + 22}" y="${cy + 5}" class="ps-year">${y}</text><text x="${cx + rx + 22}" y="${cy + 22}" class="ps-n">${n} pledge${n === 1 ? "" : "s"}</text></g>`);
  }
  for (const e of edges) {
    const dash = e.avg == null ? ` stroke-dasharray="5 4"` : "";
    svg.push(`<line x1="${e.a.x.toFixed(1)}" y1="${e.a.yy.toFixed(1)}" x2="${e.b.x.toFixed(1)}" y2="${e.b.yy.toFixed(1)}" class="ps-link" stroke="${e.colour}"${dash}><title>${esc(e.a.p.id)} and ${esc(e.b.p.id)}: ${esc(e.why)}${e.name ? `; average verdict of the facts checked: ${esc(e.name)}` : "; no verdict on the facts yet"}</title></line>`);
  }
  for (const d of dots) {
    const pv = d.p.pledge || {}, ring = d.verdict ? COLOUR[d.verdict] : "#eef3ef";
    svg.push(`<a href="${esc(d.p.path)}" class="ps-dot"><title>${esc(d.p.id)} ${esc(d.p.title)}: pledge ${esc(pv.status)}${d.verdict ? `; facts: ${esc(d.verdict)}` : ""}</title>` +
      `<circle cx="${d.x.toFixed(1)}" cy="${d.yy.toFixed(1)}" r="9" fill="${esc(pv.colour || "#716f8d")}" stroke="${ring}" stroke-width="2.6"/>` +
      `<text x="${(d.x + 13).toFixed(1)}" y="${(d.yy + 4).toFixed(1)}" class="ps-id">${esc(d.p.id)}</text></a>`);
  }
  svg.push(`</svg>`);
  const rows = years.slice().reverse().map((y) => ({ year: y, items: dots.filter((d) => d.y === y).map((d) => ({ ...d.p, factVerdict: d.verdict })) }));
  return { svg: svg.join(""), rows, edges: edges.length, topics, years };
}
