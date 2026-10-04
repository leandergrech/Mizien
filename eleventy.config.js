// Eleventy builds the public site into _site/ from site/ (templates) and the
// data written by scripts/build_site_data.py. Run `npm run build`.
import { HtmlBasePlugin } from "@11ty/eleventy";

export default function (eleventyConfig) {
  // Root-relative links in templates ("/claims/CC-001/") get the path prefix
  // (e.g. /Mizien/ on GitHub Pages) added at build time.
  eleventyConfig.addPlugin(HtmlBasePlugin);

  // Transition: the hand-written site in docs/ is copied through unchanged, so
  // the built site matches what GitHub Pages serves from /docs today. Pages move
  // into site/ one at a time; docs/ is retired once the Actions deploy is live.
  eleventyConfig.addPassthroughCopy({ docs: "/" });
}

export const config = {
  dir: { input: "site", output: "_site", includes: "_includes", data: "_data" },
  // GitHub Pages project site lives under /Mizien/. Set PATH_PREFIX=/ for a custom domain or local root.
  pathPrefix: process.env.PATH_PREFIX ?? "/Mizien/",
  templateFormats: ["njk", "md", "11ty.js"],
};
