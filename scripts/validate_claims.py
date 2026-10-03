#!/usr/bin/env python3
"""Validate every claims/CC-*/claim.yml against the project's rules.

Run from the repository root:  python scripts/validate_claims.py
Exit code is non-zero if any record is invalid.
"""
import pathlib
import re
import sys
from datetime import date

import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent

STATUSES = {"Not started", "In progress", "Drafted", "Right of reply", "Published"}
VERDICTS = {None, "Supported", "Largely supported", "Not substantiated", "Misleading", "Contradicted"}
CONFIDENCE = {None, "High", "Moderate", "Low"}
WORDING = {"Verbatim found", "Paraphrase: locate quote"}
def load_tags() -> set:
    """Pattern tags are defined in methodology/pattern-tags.md (first column, bold), so new
    patterns are added in one place: the methodology table."""
    text = (ROOT / "methodology" / "pattern-tags.md").read_text(encoding="utf-8")
    return set(re.findall(r"^\|\s*\*\*(.+?)\*\*\s*\|", text, flags=re.M))


TAGS = load_tags()
REQUIRED = ["id", "title", "category", "status", "claim", "tags"]
STRICT_VERDICTS = {"Misleading", "Contradicted"}


# Landmark emblems drawn on the map (docs/index.html PLACE_ICONS); "pin" is the generic fallback.
PLACE_ICONS = {"parliament", "castille", "citygate", "barrakka", "ravelin", "waterfront", "tower", "landfill",
               "flyover", "ro_plant", "park", "crane", "ferry", "pin"}


def check(path: pathlib.Path) -> list:
    errs = []
    d = yaml.safe_load(path.read_text(encoding="utf-8"))
    for k in REQUIRED:
        if k not in d:
            errs.append(f"missing field: {k}")
    if errs:
        return errs
    if not re.fullmatch(r"CC-\d{3}", d["id"]):
        errs.append(f"bad id format: {d['id']}")
    if path.parent.name != d["id"]:
        errs.append(f"folder name {path.parent.name} does not match id {d['id']}")
    if d["status"] not in STATUSES:
        errs.append(f"unknown status: {d['status']}")
    if d.get("verdict") not in VERDICTS:
        errs.append(f"unknown verdict: {d.get('verdict')}")
    if d.get("verdict_confidence") not in CONFIDENCE:
        errs.append(f"unknown confidence: {d.get('verdict_confidence')}")
    c = d["claim"]
    if c.get("wording_status") not in WORDING:
        errs.append(f"unknown wording_status: {c.get('wording_status')}")
    for t in d["tags"]:
        if t not in TAGS:
            errs.append(f"unknown tag: {t} (add it to methodology/pattern-tags.md first)")
    if "subtopic" in d and d["subtopic"] is not None and not (isinstance(d["subtopic"], str) and d["subtopic"].strip()):
        errs.append("subtopic must be a non-empty string when present")
    if d.get("verdict") in STRICT_VERDICTS and not d.get("evidence_shown"):
        errs.append("Misleading/Contradicted requires 'evidence_shown' (documents or data that can be shown)")
    if d["status"] in {"Right of reply", "Published"} and not (d.get("right_of_reply") or {}).get("sent"):
        errs.append("status needs right_of_reply.sent date")
    if d["status"] == "Published" and c.get("wording_status") != "Verbatim found":
        errs.append("cannot publish without a verbatim, archived claim wording")
    reviewed = d.get("last_reviewed")
    if reviewed:
        try:
            date.fromisoformat(str(reviewed))
        except ValueError:
            errs.append("last_reviewed must be a YYYY-MM-DD date")
        if not (d.get("outputs") or {}).get("report") and not (d.get("outputs") or {}).get("report_pdf"):
            errs.append("last_reviewed requires a report output")
    loc = d.get("location")
    if loc is not None:
        if not isinstance(loc, dict) or not loc.get("place"):
            errs.append("location must have a place")
        else:
            try:
                lat, lon = float(loc.get("lat")), float(loc.get("lon"))
                if not (35.7 <= lat <= 36.15 and 14.1 <= lon <= 14.65):
                    errs.append(f"location {lat},{lon} is outside the Maltese islands")
            except (TypeError, ValueError):
                errs.append("location lat/lon must be numbers")
            if loc.get("scope") not in ("site", "institution", "national"):
                errs.append("location scope must be site, institution or national")
            if loc.get("icon") is not None and loc.get("icon") not in PLACE_ICONS:
                errs.append(f"location icon {loc.get('icon')} unknown (use one of {sorted(PLACE_ICONS)})")
    return errs


def main() -> int:
    bad = 0
    files = sorted((ROOT / "claims").glob("CC-*/claim.yml"))
    for p in files:
        errs = check(p)
        if errs:
            bad += 1
            print(f"FAIL {p.relative_to(ROOT)}")
            for e in errs:
                print(f"   - {e}")
    print(f"{len(files) - bad}/{len(files)} claim records valid.")
    bad += check_queue({p.parent.name for p in files})
    bad += check_conflict_markers()
    return 1 if bad else 0


def check_queue(ids: set) -> int:
    """data/queue.csv assigns claims to the nightly checker routines (worker A, B or C)."""
    import csv
    q = ROOT / "data" / "queue.csv"
    if not q.exists():
        return 0
    errs, seen = [], set()
    for row in csv.DictReader(open(q, newline="", encoding="utf-8")):
        cid, worker = (row.get("ID") or "").strip(), (row.get("Worker") or "").strip()
        if cid not in ids:
            errs.append(f"queue: {cid} has no claims/{cid}/claim.yml")
        if worker not in {"A", "B", "C"}:
            errs.append(f"queue: {cid} has worker '{worker}' (must be A, B or C)")
        if cid in seen:
            errs.append(f"queue: {cid} is listed twice")
        attempts = (row.get("Attempts") or "0").strip()
        if not attempts.isdigit():
            errs.append(f"queue: {cid} has Attempts '{attempts}' (must be a whole number)")
        seen.add(cid)
    for e in errs:
        print("FAIL " + e)
    print(f"queue: {len(seen)} claims assigned, {len(errs)} problems.")
    return 1 if errs else 0


def check_conflict_markers() -> int:
    """Unresolved merge conflicts must never reach main (automated runs merge concurrently)."""
    import re
    marker = re.compile(r"^(<{7}|>{7})( |$)", re.M)
    bad = []
    for sub in ("claims", "data", "docs", "literature", "methodology", "scripts", "tools"):
        for f in (ROOT / sub).rglob("*"):
            if f.is_file() and f.suffix in {".md", ".csv", ".yml", ".json", ".html", ".py", ".bib"}:
                if marker.search(f.read_text(encoding="utf-8", errors="ignore")):
                    bad.append(f.relative_to(ROOT))
    for f in ROOT.glob("*.md"):
        if marker.search(f.read_text(encoding="utf-8", errors="ignore")):
            bad.append(f.relative_to(ROOT))
    for f in bad:
        print(f"FAIL conflict markers in {f}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
