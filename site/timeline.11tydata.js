// Points for the timeline page: one per claim with a recorded date. A claim keeps the precision it was published
// with (day, month or year; optionally a time of day), and the page never places it more finely than that.
const DATE = /^(\d{4})(?:-(\d{2}))?(?:-(\d{2}))?$/;
// The same address-safe keys as assets/lens.js (the site-wide filter): "Nature & Wildlife" -> "nature-wildlife".
const slug = (s) => String(s || "").normalize("NFD").replace(/[\u0300-\u036f]/g, "").toLowerCase().replace(/ħ/g, "h")
  .replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "");

export default {
  eleventyComputed: {
    timelinePoints: (data) => {
      const bodies = {};
      for (const b of data.mizien?.bodies || []) if (b && b.id) bodies[b.id] = b;
      const points = [];
      const undated = [];
      const labels = { topic: {}, verdict: {}, who: {}, pattern: {} };
      for (const c of data.mizien?.claims || []) {
        const raw = String(c.claim?.date ?? "").trim();
        const m = DATE.exec(raw);
        const base = { id: c.id, title: c.title, path: c.path, speaker: c.claim?.speaker || "", topic: c.category,
          v: c.label_slug || "none", label: c.label || "Not yet checked", pledge: c.label_kind === "pledge",
          // for the lanes: the kind of body that made the claim (its first speaker in the register), and whether it has a place
          who: bodies[c.bodies?.[0]?.id]?.type_label || "Not in the register", place: !!c.location?.lat };
        // facets for the site-wide filter (every body named, not only the first)
        const who = [];
        for (const r of c.bodies || []) { const b = bodies[r.id]; if (b?.type && !who.includes(b.type)) { who.push(b.type); labels.who[b.type] = b.type_label; } }
        if (!who.length) { who.push("unknown"); labels.who.unknown = "Not in the register"; }
        const vk = c.label ? slug((c.label_kind === "pledge" ? "Pledge: " : "") + c.label) : "none";
        labels.verdict[vk] = c.label ? (c.label_kind === "pledge" ? "Pledge: " : "") + c.label : "Not yet checked";
        labels.topic[slug(c.category)] = c.category;
        const pattern = [];
        for (const t of c.tags || []) { pattern.push(slug(t)); labels.pattern[slug(t)] = t; }
        const ym = /^\d{4}/.exec(String(c.claim?.date ?? ""));
        base.lens = { topic: [slug(c.category)], verdict: [vk], who, year: [ym ? ym[0] : "undated"], pattern };
        base.text = [c.id, c.title, c.claim?.speaker, c.claim?.quote, c.location?.place].filter(Boolean).join(" ");
        if (!m) { undated.push(base); continue; }
        const precision = m[3] ? "day" : m[2] ? "month" : "year";
        const time = precision === "day" && /^\d{2}:\d{2}$/.test(c.claim.time || "") ? c.claim.time : null;
        points.push({ ...base, date: raw, precision, time });
      }
      points.sort((a, b) => a.date.localeCompare(b.date) || a.id.localeCompare(b.id));
      const years = [];
      for (const p of [...points].reverse()) {
        const y = p.date.slice(0, 4);
        if (!years.length || years[years.length - 1].year !== y) years.push({ year: y, items: [] });
        years[years.length - 1].items.push(p);
      }
      return { points, undated, years, labels };
    },
  },
};
