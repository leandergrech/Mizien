// Same indexing rule as the claim pages: the homepage lists draft verdicts, so it stays out of
// search engines until site.index_drafts is switched on (maintainer decision, 4 Oct 2026).
export default {
  eleventyComputed: {
    noindex: (data) => !data.site.index_drafts && (data.mizien?.claims || []).some((c) => c.is_draft && c.label),
  },
};
