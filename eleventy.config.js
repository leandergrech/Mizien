// Eleventy builds the public site into _site/ from site/ (templates) and the
// data written by scripts/build_site_data.py. Run `npm run build`.
import { readFileSync, readdirSync, existsSync } from "node:fs";
import { HtmlBasePlugin } from "@11ty/eleventy";
import markdownIt from "markdown-it";

// GitHub Pages project site lives under /Mizien/. Set PATH_PREFIX=/ for a custom domain or local root.
const pathPrefix = process.env.PATH_PREFIX ?? "/Mizien/";
const site = JSON.parse(readFileSync(new URL("./site/_data/site.json", import.meta.url), "utf-8"));

const md = markdownIt({ html: false, linkify: false });

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

  eleventyConfig.addFilter("findBy", (list, key, value) => (list || []).find((x) => x[key] === value));
}

export const config = {
  dir: { input: "site", output: "_site", includes: "_includes", data: "_data" },
  pathPrefix,
  templateFormats: ["njk", "md", "11ty.js"],
};
