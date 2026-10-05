// Lists claims with their verdicts, so it follows the homepage's indexing rule for draft verdicts.
export default {
  eleventyComputed: {
    noindex: (d) => !d.site.index_drafts && (d.mizien?.claims || []).some((c) => c.is_draft && c.verdict),
  },
};
