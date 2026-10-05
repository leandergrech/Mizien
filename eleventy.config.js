// Eleventy builds the public site into _site/ from site/ (templates) and the
// data written by scripts/build_site_data.py. Run `npm run build`.
import { readFileSync, readdirSync, existsSync } from "node:fs";
import { HtmlBasePlugin } from "@11ty/eleventy";
import markdownIt from "markdown-it";

// GitHub Pages project site lives under /Mizien/. Set PATH_PREFIX=/ for a custom domain or local root.
const pathPrefix = process.env.PATH_PREFIX ?? "/Mizien/";
const site = JSON.parse(readFileSync(new URL("./site/_data/site.json", import.meta.url), "utf-8"));

const md = markdownIt({ html: false, linkify: false });

// Line icons (24x24, stroked) used in navigation, claim pages and buttons: {% icon "map" %}
const ICONS = {
  map: "M3 6.5 9 4l6 2.5L21 4v13.5L15 20l-6-2.5L3 20zM9 4v13.5M15 6.5V20",
  list: "M9 6h11M9 12h11M9 18h11M4.5 6h.01M4.5 12h.01M4.5 18h.01",
  scale: "M12 4v16M8 20h8M4 8h16M4 8l-2.5 5h5zM20 8l-2.5 5h5z",
  info: "M12 3a9 9 0 1 0 0 18a9 9 0 1 0 0-18M12 11v6M12 7.6v.01",
  pencil: "M4 20l4.2-1L19 8.2 15.8 5 5 15.8zM13.8 7l3.2 3.2",
  report: "M7 3h7l5 5v13H7zM14 3v5h5M10 12h6M10 16h6",
  sources: "M10 14a4 4 0 0 0 5.7 0l3-3a4 4 0 0 0-5.7-5.7l-1 1M14 10a4 4 0 0 0-5.7 0l-3 3a4 4 0 0 0 5.7 5.7l1-1",
  reply: "M4 5h16v10H10l-4 4v-4H4zM8 9h8M8 12h5",
  links: "M6 8a2 2 0 1 0 0-4a2 2 0 1 0 0 4M18 9a2 2 0 1 0 0-4a2 2 0 1 0 0 4M12 20a2 2 0 1 0 0-4a2 2 0 1 0 0 4M7 7.6l4 8.6M17 8.6l-4 7.6M8 6.1l8 .8",
  download: "M12 4v11M7 10l5 5 5-5M5 20h14",
  prev: "M15 5l-7 7 7 7",
  next: "M9 5l7 7-7 7",
  panels: "M4 4h7v7H4zM13 4h7v7h-7zM4 13h7v7H4zM13 13h7v7h-7z",
  people: "M9 11a3.5 3.5 0 1 0 0-7a3.5 3.5 0 1 0 0 7M2.5 20c0-3.6 2.9-6 6.5-6s6.5 2.4 6.5 6M15.5 4.3a3.5 3.5 0 0 1 0 6.4M17.5 14.3c2.3.6 4 2.6 4 5.7",
  pattern: "M12 3a9 9 0 1 0 0 18a9 9 0 1 0 0-18M12 7a5 5 0 1 0 0 10a5 5 0 1 0 0-10M12 11a1 1 0 1 0 0 2a1 1 0 1 0 0-2",
  flag: "M5 21V4M5 4.5h11l-2.2 3.8L16 12H5",
  parts: "M4 5h4v4H4zM4 15h4v4H4zM11 7h9M11 17h9M14 11h6",
  clock: "M12 3a9 9 0 1 0 0 18a9 9 0 1 0 0-18M12 7v5l3.5 2",
  feed: "M5 5a14 14 0 0 1 14 14M5 11a8 8 0 0 1 8 8M6 19a1 1 0 1 0 0-.01",
  route: "M6 19a2 2 0 1 0 0-4a2 2 0 1 0 0 4M18 9a2 2 0 1 0 0-4a2 2 0 1 0 0 4M6 15V9.5C6 7.6 7.6 6 9.5 6H16M18 9v5.5c0 1.9-1.6 3.5-3.5 3.5H8",
};
const icon = (name, cls = "ico") =>
  `<svg class="${cls}" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="${ICONS[name] || ""}"/></svg>`;

// Claim numbers ("CC-012") mentioned anywhere in a page's text become links to that claim. assets/claimrefs.js then
// shows a short summary with the verdict on a long hover or keyboard focus. Text inside links, buttons, code, scripts
// and the page head is left alone, as is a claim's mention of itself.
const CLAIM_ID = /\bCC-\d{3}[A-Z]?\b/g;   // a sub-claim is the parent's number plus a letter (CC-017A)
const NO_LINKS = new Set(["a", "button", "code", "pre", "kbd", "samp", "head", "title", "summary", "label", "option",
  "select", "svg", "math", "time", "dfn"]);   // dfn: where a sub-claim's number is defined
const TOKEN = /<!--[\s\S]*?-->|<(script|style|textarea)\b[\s\S]*?<\/\1\s*>|<\/?([a-zA-Z][\w-]*)\b[^>]*>|<![^>]*>/g;
let knownClaims = null;
function linkClaimMentions(html, selfId, prefix) {
  if (!knownClaims) {
    const file = "build/site-data.json";
    const claims = existsSync(file) ? JSON.parse(readFileSync(file, "utf-8")).claims : [];
    knownClaims = new Set(claims.flatMap((c) => [c.id, ...(c.subclaims || []).map((x) => x.id)]));
  }
  const depth = {};
  let blocked = 0, last = 0, out = "";
  const text = (t) => (blocked ? t : t.replace(CLAIM_ID, (id) => {
    const parent = id.slice(0, 6);
    if (id === selfId || !knownClaims.has(id)) return id;
    if (id === parent) return `<a class="claimref" href="${prefix}claims/${id}/" data-claim="${id}">${id}</a>`;
    return `<a class="claimref" href="${parent === selfId ? "" : `${prefix}claims/${parent}/`}#${id}" data-claim="${id}">${id}</a>`;
  }));
  html.replace(TOKEN, (tag, raw, name, at) => {
    out += text(html.slice(last, at)) + tag;
    last = at + tag.length;
    const n = (name || "").toLowerCase();
    if (!raw && NO_LINKS.has(n) && !tag.endsWith("/>")) {
      const d = tag[1] === "/" ? -1 : 1;
      depth[n] = Math.max(0, (depth[n] || 0) + d);
      blocked = Object.values(depth).reduce((a, b) => a + b, 0);
    }
    return tag;
  });
  return out + text(html.slice(last));
}

const MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September",
  "October", "November", "December"];

export default function (eleventyConfig) {
  // Root-relative links in templates ("/claims/CC-001/") get the path prefix added at build time.
  eleventyConfig.addPlugin(HtmlBasePlugin);

  // Transition: the hand-written site in docs/ is copied through unchanged, so the built
  // site still matches what GitHub Pages serves from /docs. Pages move into site/ one at a
  // time; docs/ is retired once the Actions deploy is live.
  eleventyConfig.addPassthroughCopy({ docs: "/" });
  eleventyConfig.addPassthroughCopy({ "site/assets": "assets" });
  // The map view's map library and its reader for the self-hosted tile file (npm dependencies, copied as built).
  for (const f of ["maplibre-gl.mjs", "maplibre-gl-shared.mjs", "maplibre-gl-worker.mjs", "maplibre-gl.css"])
    eleventyConfig.addPassthroughCopy({ [`node_modules/maplibre-gl/dist/${f}`]: `assets/vendor/maplibre/${f}` });
  eleventyConfig.addPassthroughCopy({ "node_modules/pmtiles/dist/pmtiles.js": "assets/vendor/pmtiles.js" });
  // Figures of each report's web version (tools/report_html.py), next to the claim's PDFs.
  // Flyer previews made by scripts/build_site_data.py (build/ is not committed).
  if (existsSync("build/claim-previews")) eleventyConfig.addPassthroughCopy({ "build/claim-previews": "claim-files" });
  // Claim and subtopic thumbnails (scripts/thumbnails.py).
  if (existsSync("build/thumbs")) eleventyConfig.addPassthroughCopy({ "build/thumbs": "claim-files/thumbs" });
  for (const id of readdirSync("claims")) {
    const dir = `claims/${id}/report-figures`;
    if (existsSync(dir)) eleventyConfig.addPassthroughCopy({ [dir]: `claim-files/${id}/report-figures` });
  }

  // "2025-11-13" -> "13 November 2025"; "2025-09" -> "September 2025"; anything else unchanged.
  eleventyConfig.addFilter("ukDate", (value) => {
    const m = /^(\d{4})(?:-(\d{2}))?(?:-(\d{2}))?$/.exec(String(value ?? "").trim());
    if (!m) return value;
    const [, y, mo, d] = m;
    if (!mo) return y;
    return (d ? `${Number(d)} ` : "") + `${MONTHS[Number(mo) - 1]} ${y}`;
  });

  eleventyConfig.addFilter("fileSize", (bytes) => {
    if (!bytes) return "";
    return bytes >= 1e6 ? `${(bytes / 1e6).toFixed(1)} MB` : `${Math.round(bytes / 1e3)} KB`;
  });

  // Absolute URL for canonical links, feeds and social cards.
  eleventyConfig.addFilter("absoluteUrl", (path) =>
    new URL(pathPrefix.replace(/\/$/, "") + path, site.url).href);

  // Inline Markdown from methodology files (**bold**, *italic*, `code`) as HTML.
  eleventyConfig.addFilter("mdInline", (text) => md.renderInline(String(text ?? "")));

  eleventyConfig.addShortcode("icon", icon);

  eleventyConfig.addTransform("claim-mentions", function (content) {
    if (!(this.page.outputPath || "").endsWith(".html")) return content;
    const self = /\/claims\/(CC-\d{3})\/$/.exec(this.page.url || "");
    return linkClaimMentions(content, self && self[1], pathPrefix);
  });

  eleventyConfig.addFilter("findBy", (list, key, value) => (list || []).find((x) => x[key] === value));
  eleventyConfig.addFilter("without", (list, key, value) => (list || []).filter((x) => x[key] !== value));
  eleventyConfig.addFilter("where", (list, key, value) => (list || []).filter((x) => x[key] === value));
  eleventyConfig.addFilter("having", (list, path) =>
    (list || []).filter((x) => path.split(".").reduce((o, k) => (o == null ? o : o[k]), x)));
  eleventyConfig.addFilter("tagged", (list, tag) => (list || []).filter((x) => (x.tags || []).includes(tag)));
}

export const config = {
  dir: { input: "site", output: "_site", includes: "_includes", data: "_data" },
  pathPrefix,
  templateFormats: ["njk", "md", "11ty.js"],
};
