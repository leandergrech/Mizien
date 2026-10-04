// Indexing rule (maintainer decision, 4 Oct 2026): a page that shows a draft verdict stays out of
// search engines until site.index_drafts is switched on. That happens only after the disclaimer and
// the visual "How a verdict is reached" page are approved.
const isoMonth = (s) => {
  const m = /^(\d{4})-(\d{2})(?:-(\d{2}))?$/.exec(String(s ?? ""));
  if (!m) return s;
  const month = new Date(Date.UTC(+m[1], +m[2] - 1, 1)).toLocaleString("en-GB", { month: "long", timeZone: "UTC" });
  return (m[3] ? `${+m[3]} ` : "") + `${month} ${m[1]}`;
};

export default {
  eleventyComputed: {
    title: (data) => (data.claim ? `${data.claim.id}: ${data.claim.title}` : data.title),
    noindex: (data) => {
      if (data.site.index_drafts) return false;
      if (data.claim) return data.claim.is_draft;
      return (data.mizien?.claims || []).some((c) => c.is_draft && c.verdict);
    },
    description: (data) => {
      const c = data.claim;
      if (!c) return data.description;
      const verdict = c.verdict
        ? `${c.verdict}${c.verdict_confidence ? ` (${c.verdict_confidence.toLowerCase()} confidence)` : ""}`
        : "Not yet checked";
      const draft = c.is_draft && c.verdict ? "Draft check, right of reply pending. " : "";
      const when = c.claim.date ? `, ${isoMonth(c.claim.date)}` : "";
      return `${draft}${verdict}. ${c.claim.speaker}${when}: ${c.title}.`;
    },
  },
};
