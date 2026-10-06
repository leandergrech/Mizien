// The glyph key (site/about/glyphs.njk), and the build-time check on the glyph registry (site/assets/glyphs.js).
//
// Errors stop the build: two different things drawn identically (draw one anew, or list it in ALIAS if it really is the
// same idea), or a claim naming a place emblem that does not exist. Warnings do not: a topic, subtopic, pledge label,
// theme, kind of body or place in the claim records that has no glyph yet falls back to its parent's glyph, and is listed
// in the build log so one can be drawn.
import { readFileSync } from "node:fs";
import { loadGlyphs } from "../../scripts/glyphs.mjs";

const MODE_NAMES = {
  "mode:topic": "Group by topic", "mode:subtopic": "Group by subtopic", "mode:verdict": "Group by verdict",
  "mode:pattern": "Group by pattern", "mode:status": "Group by stage", "mode:speaker": "Group by who said it",
  "mode:year": "Group by when", "mode:network": "Links only",
};

export default function () {
  const G = loadGlyphs();
  const data = JSON.parse(readFileSync(new URL("../../build/site-data.json", import.meta.url), "utf-8"));
  const claims = data.claims;
  const warnings = [], errors = [];

  // 1. two different things must not share a drawing
  const seen = new Map();
  for (const [k, d] of Object.entries(G.own)) {
    if (seen.has(d)) errors.push(`"${seen.get(d)}" and "${k}" are drawn identically: draw one anew, or add it to ALIAS if it is the same idea`);
    else seen.set(d, k);
  }

  // 2. what the claim records use
  const count = (list) => list.reduce((m, x) => (x ? m.set(x, (m.get(x) || 0) + 1) : m), new Map());
  const byCategory = count(claims.map((c) => c.category));
  const bySub = count(claims.map((c) => c.subtopic));
  const subParent = new Map();
  claims.forEach((c) => { if (c.subtopic && !subParent.has(c.subtopic)) subParent.set(c.subtopic, c.category); });
  const byVerdict = count(claims.map((c) => c.verdict));
  const byTag = count(claims.flatMap((c) => c.tags || []));
  const byKind = new Map((data.by_kind.kinds || []).map((k) => [k.label, k.claims]));
  const placeUse = new Map();   // icon -> { place -> claims }
  claims.forEach((c) => {
    const L = c.location; if (!L || !L.place) return;
    const icon = L.icon || "pin";
    if (!G.paths["place:" + icon]) errors.push(`${c.id}: place emblem "${icon}" is not in site/assets/glyphs.js`);
    const m = placeUse.get(icon) || new Map(); m.set(L.place, (m.get(L.place) || 0) + 1); placeUse.set(icon, m);
  });
  const need = (name, what) => { if (!G.paths[name]) warnings.push(`no glyph for ${what}`); };
  data.categories.forEach((c) => need(c.name, `topic "${c.name}"`));
  bySub.forEach((n, s) => need(s, `subtopic "${s}" (shows ${subParent.get(s)}'s glyph)`));
  data.verdicts.forEach((v) => need(v.name, `verdict "${v.name}"`));
  data.patterns.forEach((p) => need(p.name, `pattern "${p.name}"`));
  data.pledge_labels.forEach((l) => need("pledge:" + l.name, `pledge label "${l.name}" (shows the plain flag)`));
  data.body_types.forEach((t) => need(t.label, `kind of body "${t.label}"`));
  data.themes.forEach((t) => need("theme:" + t.id, `theme ${t.id} "${t.name}"`));
  placeUse.forEach((m, icon) => { if (icon === "pin") warnings.push(`${[...m.keys()].length} place(s) use the generic pin: ${[...m.keys()].join("; ")}`); });
  warnings.forEach((w) => console.warn("[glyphs] " + w));
  if (errors.length) throw new Error("glyph registry:\n  " + errors.join("\n  "));

  // 3. the key
  const aliasOf = (k) => G.alias[k] || null;
  const themeById = new Map(data.themes.map((t) => [t.id, t]));
  const placeNames = (icon) => [...(placeUse.get(icon) || [])].map(([place, n]) => ({ place, n })).sort((a, b) => b.n - a.n);
  const label = (gid, k) => {
    if (gid === "pledge") return k === "pledge" ? "A pledge (plain flag)" : k.slice(7);
    if (gid === "theme") { const t = themeById.get(k.slice(6)); return t ? `${t.id} · ${t.name}` : k; }
    if (gid === "place") return k.slice(6);
    if (gid === "mode") return MODE_NAMES[k] || k;
    if (k === "person") return "A person";
    return k;
  };
  const groups = G.groups.map((g) => {
    const keys = g.id === "theme" ? [...new Set([...g.keys, ...Object.keys(G.alias).filter((k) => k.startsWith("theme:"))])].sort((a, b) => Number(a.slice(7)) - Number(b.slice(7)))
      : g.id === "place" ? [...new Set([...g.keys, ...Object.keys(G.alias).filter((k) => k.startsWith("place:"))])]
      : g.id === "mode" ? [...g.keys, "mode:pledges"] : g.keys;
    const items = keys.map((k) => {
      const item = { key: k, name: label(g.id, k), alias: aliasOf(k) };
      if (item.alias) item.aliasName = label(G.groups.find((x) => x.keys.includes(item.alias))?.id, item.alias);
      if (g.id === "topic") item.n = byCategory.get(k);
      if (g.id === "subtopic") { item.n = bySub.get(k); item.parent = subParent.get(k); }
      if (g.id === "verdict") item.n = byVerdict.get(k);
      if (g.id === "pattern") item.n = byTag.get(k);
      if (g.id === "speaker") item.n = byKind.get(k);
      if (g.id === "place") item.places = placeNames(k.slice(6));
      return item;
    });
    return { id: g.id, title: g.title, note: g.note, items };
  });
  return { groups, total: Object.keys(G.own).length, shared: Object.keys(G.alias).length, warnings };
}
