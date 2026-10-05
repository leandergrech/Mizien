// Body pages follow the claim pages' indexing rule: a page that lists a draft verdict stays out of search engines
// until site.index_drafts is switched on (maintainer decision, 4 Oct 2026).
const hasDraftVerdict = (list) => (list || []).some((c) => c.label && c.status !== "Published");   // verdict or pledge label

export default {
  eleventyComputed: {
    title: (d) => (d.body ? d.body.name : d.title),
    description: (d) => {
      const b = d.body;
      if (!b) return d.description;
      const n = b.claims.length, checked = b.claims.filter((c) => c.label).length;
      const who = b.kind === "person" ? `${b.name}${b.role ? `, ${b.role}` : ""}` : b.name;
      return `${n} claim${n === 1 ? "" : "s"} by ${who} on Miżien, ${checked} with a verdict: what was said, the topics, and the bodies linked to it. A record of what was checked, not a score.`;
    },
    feedUrl: (d) => (d.body ? `/bodies/${d.body.id}/feed.xml` : null),
    feedTitle: (d) => (d.body ? `Miżien: claims by ${d.body.name}` : null),
    noindex: (d) => !d.site.index_drafts && Boolean(d.body) && hasDraftVerdict(d.body.claims),
  },
};
