// /data/claim-briefs.json: what the long-hover summary of a claim shows (assets/claimrefs.js).
const cut = (s, n) => {
  s = String(s ?? "").replace(/\s+/g, " ").trim();
  if (s.length <= n) return s;
  const t = s.slice(0, n);
  return t.slice(0, Math.max(t.lastIndexOf(" "), n * 0.6)).replace(/[,;:.\s]+$/, "") + "…";
};
const firstSentence = (s) => {
  const m = /^.{40,}?[.!?](?=\s+[A-Z(“"']|$)/.exec(String(s ?? "").replace(/\s+/g, " ").trim());
  return m ? m[0] : String(s ?? "");
};

export default class {
  data() {
    return { permalink: "/data/claim-briefs.json", eleventyExcludeFromCollections: true };
  }

  render({ mizien }) {
    const out = {};
    for (const c of mizien.claims) {
      out[c.id] = {
        title: c.title, topic: c.subtopic ? `${c.category} · ${c.subtopic}` : c.category,
        verdict: c.verdict || null, slug: c.verdict_slug || "none", confidence: c.verdict_confidence || null,
        status: c.status_label, draft: Boolean(c.is_draft && c.verdict),
        speaker: c.claim.speaker || "", date: c.claim.date ? String(c.claim.date) : "",
        brief: cut(c.claim.text, 230),
        why: c.verdict && c.counter_evidence ? cut(firstSentence(c.counter_evidence), 230) : "",
        thumb: c.thumb ? c.thumb.url : null,
      };
    }
    return JSON.stringify(out);
  }
}
