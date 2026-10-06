// The homepage lists draft verdicts (the claim cards), so it stays out of search engines until site.index_drafts is
// switched on (maintainer decision, 4 Oct 2026). homeData feeds the claim cards and the "recently checked" list.
const MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
  "November", "December"];
function ukDate(v) {
  const m = /^(\d{4})(?:-(\d{2}))?(?:-(\d{2}))?$/.exec(String(v ?? "").trim());
  if (!m) return "";
  return (m[3] ? `${Number(m[3])} ` : "") + (m[2] ? `${MONTHS[Number(m[2]) - 1]} ` : "") + m[1];
}
function clip(s, n) { s = String(s ?? "").replace(/\s+/g, " ").trim(); return s.length > n ? s.slice(0, n - 1).replace(/\s+\S*$/, "") + "…" : s; }

export default {
  eleventyComputed: {
    noindex: (data) => !data.site.index_drafts && (data.mizien?.claims || []).some((c) => c.is_draft && c.label),
    homeData: (data) => {
      const claims = data.mizien?.claims || [];
      const cards = [], places = new Set();
      for (const c of claims) {
        if (c.location?.place) places.add(c.location.place);
        if (!c.label) continue;
        cards.push({ id: c.id, title: c.title, path: c.path, topic: c.category, v: c.label_slug || "none", label: c.label,
          pledge: c.label_kind === "pledge", draft: !!c.is_draft, quote: clip(String(c.claim?.quote || c.title).trim().replace(/^[“”"'‘’]+|[“”"'‘’]+$/g, ""), 170),
          speaker: clip(c.claim?.speaker, 70), date: ukDate(c.claim?.date), reviewed: c.last_reviewed || "",
          place: c.location?.place || "", confidence: c.verdict_confidence || "" });
      }
      cards.sort((a, b) => String(b.reviewed).localeCompare(String(a.reviewed)) || a.id.localeCompare(b.id));
      return { total: claims.length, checked: cards.length, bodies: (data.mizien?.bodies || []).length, places: places.size,
        cards, recent: cards.slice(0, 6) };
    },
  },
};
