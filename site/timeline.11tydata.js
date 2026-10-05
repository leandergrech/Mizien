// Points for the timeline page: one per claim with a recorded date. A claim keeps the precision it was published
// with (day, month or year; optionally a time of day), and the page never places it more finely than that.
const DATE = /^(\d{4})(?:-(\d{2}))?(?:-(\d{2}))?$/;

export default {
  eleventyComputed: {
    timelinePoints: (data) => {
      const points = [];
      const undated = [];
      for (const c of data.mizien?.claims || []) {
        const raw = String(c.claim?.date ?? "").trim();
        const m = DATE.exec(raw);
        const base = { id: c.id, title: c.title, path: c.path, speaker: c.claim?.speaker || "", topic: c.category,
          v: c.label_slug || "none", label: c.label || "Not yet checked", pledge: c.label_kind === "pledge" };
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
      return { points, undated, years };
    },
  },
};
