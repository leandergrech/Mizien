// Indexing rule (maintainer decision, 4 Oct 2026): a page that shows a draft verdict stays out of
// search engines until site.index_drafts is switched on. That happens only after the disclaimer and
// the visual "How a verdict is reached" page are approved.
const isoMonth = (s) => {
  const m = /^(\d{4})-(\d{2})(?:-(\d{2}))?$/.exec(String(s ?? ""));
  if (!m) return s;
  const month = new Date(Date.UTC(+m[1], +m[2] - 1, 1)).toLocaleString("en-GB", { month: "long", timeZone: "UTC" });
  return (m[3] ? `${+m[3]} ` : "") + `${month} ${m[1]}`;
};

// Previous/next claim and a Google-style window of claim numbers (first, last, current ±3), in list order.
const brief = (x) => x && { id: x.id, title: x.title, path: x.path, verdict: x.label,
  verdict_slug: x.label_slug, n: Number(x.id.replace(/\D/g, "")) };

function pager(data) {
  const all = data.mizien?.claims || [];
  const i = all.findIndex((x) => x.id === data.claim?.id);
  if (i < 0) return null;
  const keep = new Set([0, all.length - 1]);
  for (let k = i - 3; k <= i + 3; k++) if (k >= 0 && k < all.length) keep.add(k);
  const pages = [];
  let last = -1;
  [...keep].sort((a, b) => a - b).forEach((k) => {
    if (last >= 0 && k - last > 1) pages.push({ gap: true });
    pages.push({ ...brief(all[k]), current: k === i });
    last = k;
  });
  return { prev: brief(all[i - 1]), next: brief(all[i + 1]), pages, index: i + 1, total: all.length };
}

export default {
  eleventyComputed: {
    pager: (data) => (data.claim ? pager(data) : null),
    title: (data) => (data.claim ? `${data.claim.id}: ${data.claim.title}` : data.title),
    noindex: (data) => {
      if (data.site.index_drafts) return false;
      if (data.claim) return data.claim.is_draft;
      return (data.mizien?.claims || []).some((c) => c.is_draft && c.label);
    },
    description: (data) => {
      const c = data.claim;
      if (!c) return data.description;
      const pledge = c.pledge_view ? `Pledge: ${c.pledge_view.status} (as of ${c.pledge_view.as_of})` : "";
      const verdict = c.verdict
        ? `${c.verdict}${c.verdict_confidence ? ` (${c.verdict_confidence.toLowerCase()} confidence)` : ""}${pledge ? `; ${pledge}` : ""}`
        : pledge || "Not yet checked";
      const draft = c.is_draft && c.label ? "Draft check, right of reply pending. " : "";
      const when = c.claim.date ? `, ${isoMonth(c.claim.date)}` : "";
      return `${draft}${verdict}. ${c.claim.speaker}${when}: ${c.title}.`;
    },
  },
};
