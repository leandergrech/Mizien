#!/usr/bin/env python3
"""Build data/claims.json and docs/data/claims.json from the single source of truth:
claims/*/claim.yml plus data/edges.csv and data/themes.csv.

Run from the repository root:  python scripts/build_site_data.py
"""
import csv
import json
import pathlib
import re
import shutil
import sys

import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
REPO = "https://github.com/leandergrech/Mizien"

CATEGORY_COLORS = {
    "Land & Trees": "#3d8b5a",
    "Climate & Energy": "#d9772b",
    "Waste": "#9a7b45",
    "Water": "#3c8fbf",
    "Nature & Wildlife": "#9a76c8",
    "Air": "#9fb3c0",
    "Transport": "#c85a3a",
    "Governance & Promises": "#e3a72f",
    "Planning & Housing": "#d16ba5",
    "Noise": "#e8836b",
}
THEME_COLORS = {
    "T1": "#e3a72f", "T2": "#6fcf97", "T3": "#56b4e9", "T4": "#f2994a", "T5": "#bdbdbd", "T6": "#bb86fc", "T7": "#4fc3c8",
    "T8": "#f06292", "T9": "#9fa8da",
}


# colours for topics and themes added later (by the weekly intake routine)
SPARE = ["#4db6ac", "#ff8a65", "#9575cd", "#aed581", "#f48fb1", "#4fc3f7", "#ffd54f", "#a1887f", "#90a4ae", "#ce93d8"]


def spare_colour(key: str) -> str:
    return SPARE[sum(map(ord, key)) % len(SPARE)]


def main() -> int:
    claims = []
    for path in sorted((ROOT / "claims").glob("CC-*/claim.yml")):
        d = yaml.safe_load(path.read_text(encoding="utf-8"))
        claims.append({
            "id": d["id"],
            "title": d["title"],
            "category": d["category"],
            "claim": d["claim"]["text"],
            "counter": d.get("counter_evidence", ""),
            "status": d.get("status", "Not started"),
            "verdict": d.get("verdict"),
            "tags": d.get("tags", []),
            **({"subtopic": d["subtopic"]} if d.get("subtopic") else {}),
            "priority": d.get("priority", ""),
            "wording_status": d["claim"].get("wording_status", ""),
            "confidence": d.get("verdict_confidence"),
            "speaker": d["claim"].get("speaker", ""),
            "date": str(d["claim"].get("date") or ""),
            "quote": d["claim"].get("quote", ""),
            "version": d.get("version"),
            **({"last_reviewed": str(d["last_reviewed"])} if d.get("last_reviewed") else {}),
            "outputs": {k: f"claim-files/{d['id']}/{pathlib.Path(v).name}" for k, v in (d.get("outputs") or {}).items()},
            "record": f"{REPO}/blob/main/claims/{d['id']}/claim.yml",
        })
    cats = []
    for c in claims:
        if c["category"] not in [x["name"] for x in cats]:
            cats.append({"name": c["category"], "color": CATEGORY_COLORS.get(c["category"]) or spare_colour(c["category"])})

    with open(ROOT / "data" / "edges.csv", newline="", encoding="utf-8") as f:
        edges = [{"from": r["From"], "to": r["To"], "theme": r["Theme ID"], "link_type": r["Link type"],
                  "strength": r["Strength"]} for r in csv.DictReader(f)]
    with open(ROOT / "data" / "themes.csv", newline="", encoding="utf-8") as f:
        themes = [{"id": r["Theme ID"], "name": r["Theme"], "color": THEME_COLORS.get(r["Theme ID"]) or spare_colour(r["Theme ID"]),
                   "dashed": r["Strength"].startswith(("Weak", "Pattern")), "link_type": r["Link type"],
                   "strength": r["Strength"], "description": r["What connects them"],
                   "members": [x.strip() for x in r["Linked claim IDs"].split(",")]} for r in csv.DictReader(f)]

    out = {"categories": cats, "claims": claims, "edges": edges, "themes": themes}
    text = json.dumps(out, ensure_ascii=False, indent=2)
    for target in (ROOT / "data" / "claims.json", ROOT / "docs" / "data" / "claims.json"):
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8")
    preview = ROOT / "docs" / "design-preview.html"
    if preview.is_file():
        page = preview.read_text(encoding="utf-8")
        page, count = re.subn(
            r'(<script id="map-data" type="application/json">).*?(</script>)',
            lambda m: m.group(1) + text.replace("<", "\\u003c") + m.group(2),
            page, count=1, flags=re.S,
        )
        if count:
            preview.write_text(page, encoding="utf-8")
    # GitHub Pages publishes only /docs. Copy claim deliverables there so the
    # same-page viewer and explicit downloads use the same-origin site files.
    files_root = ROOT / "docs" / "claim-files"
    for row in claims:
        claim_path = ROOT / "claims" / row["id"]
        for value in (row.get("outputs") or {}).values():
            filename = pathlib.Path(value).name
            source = claim_path / filename
            if source.is_file():
                dest = files_root / row["id"] / filename
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source, dest)
    print(f"Wrote {len(claims)} claims, {len(edges)} edges, {len(themes)} themes.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
