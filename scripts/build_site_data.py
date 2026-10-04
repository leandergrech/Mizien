#!/usr/bin/env python3
"""Build data/claims.json and docs/data/claims.json from the single source of truth:
claims/*/claim.yml plus data/edges.csv and data/themes.csv.

Also writes build/site-data.json (git-ignored): the fuller record the Eleventy site
is built from (claim pages, list, feeds), with sources joined to archive/manifest.csv.

Run from the repository root:  python scripts/build_site_data.py
"""
import csv
import json
import pathlib
import re
import shutil
import sys
import unicodedata
from datetime import date, datetime

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
    claims, records = [], []
    for path in sorted((ROOT / "claims").glob("CC-*/claim.yml")):
        d = yaml.safe_load(path.read_text(encoding="utf-8"))
        records.append(d)
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
            **({"location": d["location"]} if d.get("location") else {}),
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
    write_site_data(records, out)
    print(f"Wrote {len(claims)} claims, {len(edges)} edges, {len(themes)} themes.")
    return 0


# ---------------------------------------------------------------- build/site-data.json for the Eleventy site

SITE_DATA = ROOT / "build" / "site-data.json"
VERDICT_RATING = {"Supported": 5, "Largely supported": 4, "Not substantiated": 3, "Misleading": 2, "Contradicted": 1}
STATUS_LABELS = {
    "Not started": "Not yet checked",
    "In progress": "Check in progress",
    "Drafted": "Draft: right of reply pending",
    "Right of reply": "Sent to the body concerned for reply",
    "Published": "Published",
}
OUTPUT_LABELS = {"report": "Report", "report_pdf": "Report", "flyer_pdf": "Flyer (PDF)", "flyer_png": "Flyer (image)",
                 "document": "Document", "appendix": "Appendix"}


def slug(text: str) -> str:
    """ASCII slug that keeps Maltese letters readable: ħ -> h, ż -> z, għ -> gh."""
    text = (text or "").replace("ħ", "h").replace("Ħ", "H").replace("&", " and ")
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def jsonable(x):
    """YAML gives dates as date objects; the site wants plain strings."""
    if isinstance(x, dict):
        return {k: jsonable(v) for k, v in x.items()}
    if isinstance(x, list):
        return [jsonable(v) for v in x]
    if isinstance(x, (date, datetime)):
        return x.isoformat()
    return x


def norm_url(url: str) -> str:
    url = re.sub(r"^https?://(www\.)?", "", (url or "").strip(), flags=re.I)
    host, _, rest = url.partition("/")
    return (host.lower() + ("/" + rest if rest else "")).rstrip("/")


def load_archive() -> dict:
    rows = {}
    path = ROOT / "archive" / "manifest.csv"
    if path.is_file():
        with open(path, newline="", encoding="utf-8") as f:
            for r in csv.DictReader(f):
                key = norm_url(r.get("url"))
                if key and (key not in rows or (r.get("archived_url") and not rows[key].get("archived_url"))):
                    rows[key] = r
    return rows


def archive_entry(url: str, manifest: dict) -> dict:
    """How a cited source is preserved: archived (snapshot link), hashed (fetched and hashed, no
    snapshot), offline (no public URL, e.g. a PDF supplied by the maintainer) or missing."""
    if not (url or "").lower().startswith("http"):
        return {"state": "offline"}
    r = manifest.get(norm_url(url))
    if not r:
        return {"state": "missing"}
    snapshot = (r.get("archived_url") or "").strip()
    if snapshot.startswith("http://"):
        snapshot = "https://" + snapshot[len("http://"):]
    return {
        "state": "archived" if snapshot else ("hashed" if r.get("sha256") else "missing"),
        "url": snapshot or None,
        "sha256": r.get("sha256") or None,
        "retrieved_utc": r.get("retrieved_utc") or None,
    }


PROCESS_NOTE = re.compile(r"right of reply|must not be published|maintainer", re.I)


def public_limitations(caveats: str) -> str:
    """claim.yml 'caveats' mixes the check's limitations with editorial process notes (right-of-reply
    status, publication holds). The site shows the limitations; right of reply has its own section.
    Until claim.yml has a separate 'limitations' field, sentences about process are left out here."""
    sentences = re.split(r"(?<=[.!?])\s+(?=[A-Z'\u2018\u201c(])", (caveats or "").strip())
    return " ".join(s for s in sentences if s and not PROCESS_NOTE.search(s))


def bold_table(md_file: str) -> list:
    """Rows of a methodology table whose first cell is bold: [(name, meaning), ...]."""
    text = (ROOT / "methodology" / md_file).read_text(encoding="utf-8")
    return re.findall(r"^\|\s*\*\*(.+?)\*\*\s*\|\s*(.+?)\s*\|\s*$", text, flags=re.M)


def write_site_data(records: list, out: dict) -> None:
    manifest = load_archive()
    titles = {d["id"]: d["title"] for d in records}
    theme_names = {t["id"]: t["name"] for t in out["themes"]}
    site_claims = []
    for d in records:
        cid, rec = d["id"], jsonable(d)
        files = []
        for key, value in (d.get("outputs") or {}).items():
            name = pathlib.Path(value).name
            src = ROOT / "claims" / cid / name
            files.append({"key": key, "label": OUTPUT_LABELS.get(key, key.replace("_", " ").capitalize()), "name": name,
                          "url": f"/claim-files/{cid}/{name}", "type": src.suffix.lstrip(".").upper(),
                          "bytes": src.stat().st_size if src.is_file() else None})
        links = []
        for e in out["edges"]:
            if cid in (e["from"], e["to"]):
                other = e["to"] if e["from"] == cid else e["from"]
                links.append({"id": other, "title": titles.get(other, other), "theme_id": e["theme"],
                              "theme": theme_names.get(e["theme"], e["theme"]), "link_type": e["link_type"],
                              "strength": e["strength"]})
        site_claims.append({
            **rec,
            "path": f"/claims/{cid}/",
            "status_label": STATUS_LABELS.get(d.get("status"), d.get("status")),
            "is_draft": d.get("status") != "Published",
            "limitations": public_limitations(d.get("caveats")),
            "rating": VERDICT_RATING.get(d.get("verdict")),
            "verdict_slug": slug(d["verdict"]) if d.get("verdict") else None,
            "category_slug": slug(d["category"]),
            "sources": [{**jsonable(s), "archive": archive_entry(s.get("url"), manifest)}
                        for s in (d["claim"].get("sources") or [])],
            "files": files,
            "links": links,
            "record_url": f"{REPO}/blob/main/claims/{cid}/claim.yml",
        })
    data = {
        "claims": site_claims,
        "categories": [{**c, "slug": slug(c["name"])} for c in out["categories"]],
        "themes": out["themes"],
        "verdicts": [{"name": n, "meaning": m, "rating": VERDICT_RATING.get(n), "slug": slug(n)}
                     for n, m in bold_table("verdict-scale.md")],
        "grades": [{"grade": g, "meaning": m} for g, m in bold_table("evidence-grades.md")],
        "patterns": [{"name": n, "meaning": m} for n, m in bold_table("pattern-tags.md")],
    }
    SITE_DATA.parent.mkdir(parents=True, exist_ok=True)
    SITE_DATA.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")


if __name__ == "__main__":
    sys.exit(main())
