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
};
const icon = (name, cls = "ico") =>
  `<svg class="${cls}" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="${ICONS[name] || ""}"/></svg>`;

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

  eleventyConfig.addFilter("findBy", (list, key, value) => (list || []).find((x) => x[key] === value));
}

export const config = {
  dir: { input: "site", output: "_site", includes: "_includes", data: "_data" },
  pathPrefix,
  templateFormats: ["njk", "md", "11ty.js"],
};
