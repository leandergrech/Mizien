// Loads the glyph registry (site/assets/glyphs.js, a plain browser script) for Node: the Eleventy shortcode and the build-time
// check use the very same file the browser does.
import { readFileSync } from "node:fs";

export function loadGlyphs() {
  const src = readFileSync(new URL("../site/assets/glyphs.js", import.meta.url), "utf-8");
  const win = {};
  new Function("window", src)(win);
  if (!win.MizienGlyphs) throw new Error("site/assets/glyphs.js did not define MizienGlyphs");
  return win.MizienGlyphs;
}
