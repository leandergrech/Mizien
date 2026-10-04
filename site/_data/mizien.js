// Claim data for the site, written by scripts/build_site_data.py (run `npm run build`).
import { readFileSync, existsSync } from "node:fs";

const file = new URL("../../build/site-data.json", import.meta.url);

export default function () {
  if (!existsSync(file)) {
    throw new Error("build/site-data.json is missing: run `python3 scripts/build_site_data.py` (or `npm run build`).");
  }
  return JSON.parse(readFileSync(file, "utf-8"));
}
