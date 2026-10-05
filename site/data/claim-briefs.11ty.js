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
    const tones = { green: ["#2e7d4f", "#fff"], lime: ["#8db36b", "#13301f"], amber: ["#e3a72f", "#13301f"],
      orange: ["#d9772b", "#13301f"], red: ["#b5483a", "#fff"], maroon: ["#8e2f25", "#fff"], grey: ["#6b7c74", "#fff"] };
    for (const c of mizien.claims) {
      const pv = c.pledge_view;
      out[c.id] = {
        title: c.title, topic: c.subtopic ? `${c.category} · ${c.subtopic}` : c.category,
        verdict: c.verdict || null, slug: c.verdict_slug || "none", confidence: c.verdict_confidence || null,
        pledge: pv ? { status: pv.status, as_of: pv.as_of, colour: pv.colour, target: pv.target, pure: pv.pure } : null,
        status: c.status_label, draft: Boolean(c.is_draft && c.label), reply_sought: c.reply_sought,
        speaker: c.claim.speaker || "", date: c.claim.date ? String(c.claim.date) : "",
        brief: cut(c.claim.text, 230),
        why: c.verdict && c.counter_evidence ? cut(firstSentence(c.counter_evidence), 230) : "",
        thumb: c.thumb ? c.thumb.url : null,
        parts: (c.subclaims || []).length,
      };
      for (const x of c.subclaims || []) {
        out[x.id] = {
          title: cut(x.text, 160), topic: `Part of ${c.id} · ${c.title}`, part: true,
          verdict: null, slug: "none", rating: x.rating || null, tone: tones[x.tone] || tones.grey,
          status: c.status_label, draft: Boolean(c.is_draft && c.label), speaker: x.said_by || c.claim.speaker || "",
          date: "", brief: x.finding ? cut(x.finding, 230) : "", why: "", thumb: null,
        };
      }
    }
    return JSON.stringify(out);
  }
}
