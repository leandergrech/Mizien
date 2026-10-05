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
    errs += check_timeline(d.get("timeline"))
    errs += check_history(d)
    return errs


def check_history(d) -> list:
    """`history:` in claim.yml is the research log: the date each step was done (see scripts/timeline.py)."""
    entries = d.get("history")
    if entries is None:
        return [f"version {d['version']} has no research log: add history entries (date, step: version, version, note)"] if d.get("version") else []
    sys.path.insert(0, str(ROOT / "scripts"))
    import timeline
    if not isinstance(entries, list):
        return ["history must be a list of research steps (date, step, ...)"]
    errs, versions, last = [], [], ""
    for i, e in enumerate(entries, 1):
        if not isinstance(e, dict):
            errs.append(f"history entry {i} must have date and step")
            continue
        when = timeline.parse_date(e.get("date"))
        if not when or when["precision"] != "day":
            errs.append(f"history entry {i}: date '{e.get('date')}' must be a full date (2026-10-02), the day the research was done")
        elif when["iso"] < last:
            errs.append(f"history entry {i}: dates must be in order (oldest first)")
        else:
            last = when["iso"]
        step = e.get("step")
        if step not in timeline.HISTORY_STEPS:
            errs.append(f"history entry {i}: step must be one of {', '.join(timeline.HISTORY_STEPS)}")
        if step == "version":
            if not e.get("version"):
                errs.append(f"history entry {i}: a version step needs its version number")
            versions.append(str(e.get("version")))
        if step in ("correction", "clarification") and not str(e.get("note") or "").strip():
            errs.append(f"history entry {i}: a {step} needs a note saying what was wrong and what changed")
    if d.get("version") and str(d["version"]) not in versions:
        errs.append(f"version {d['version']} has no history entry: add one with the date of the research and what changed")
    return errs


def check_timeline(entries) -> list:
    """Optional `timeline:` events in claim.yml: later statements, new data, replies or corrections (see scripts/timeline.py)."""
    if entries is None:
        return []
    sys.path.insert(0, str(ROOT / "scripts"))
    import timeline
    if not isinstance(entries, list):
        return ["timeline must be a list of events (date, kind, text, optional url)"]
    errs = []
    for i, e in enumerate(entries, 1):
        if not isinstance(e, dict):
            errs.append(f"timeline event {i} must have date, kind and text")
            continue
        if not timeline.parse_date(e.get("date")):
            errs.append(f"timeline event {i}: date '{e.get('date')}' not understood (use 2026-10-01, 2026-10 or 2026)")
        if e.get("kind") not in timeline.CURATED_KINDS:
            errs.append(f"timeline event {i}: kind must be one of {', '.join(timeline.CURATED_KINDS)}")
        if not str(e.get("text") or "").strip():
            errs.append(f"timeline event {i}: text is missing")
        if e.get("url") and not str(e["url"]).startswith(("http://", "https://")):
            errs.append(f"timeline event {i}: url must start with http:// or https://")
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
    bad += check_register(files)
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


def check_register(files) -> int:
    """data/bodies.csv: the register of bodies and people that claims are matched to (see scripts/bodies.py).

    Errors in the register fail. A claim whose speaker matches no entry only warns: add the speaker's wording to
    the Aliases column of the right row (or a new row), or list `bodies: [id, ...]` in the claim.
    """
    sys.path.insert(0, str(ROOT / "scripts"))
    import bodies
    reg = bodies.load()
    if not reg:
        return 0
    errs, warns = [], []
    import csv
    ids = [r["ID"] for r in csv.DictReader(open(ROOT / "data" / "bodies.csv", newline="", encoding="utf-8"))]
    errs += [f"register: {i} is listed twice" for i in sorted({i for i in ids if ids.count(i) > 1})]
    for b in reg.values():
        if b["id"] in bodies.RESERVED_IDS:
            errs.append(f"register: ID '{b['id']}' is reserved for another page under /bodies/")
        if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", b["id"]):
            errs.append(f"register: ID '{b['id']}' must be lower-case words joined by hyphens")
        if b["type"] not in bodies.TYPES:
            errs.append(f"register: {b['id']} has type '{b['type']}' (use one of {', '.join(bodies.TYPES)})")
        if b["kind"] not in bodies.KINDS:
            errs.append(f"register: {b['id']} has kind '{b['kind']}' (organisation or person)")
        if b["parent"] and b["parent"] not in reg:
            errs.append(f"register: {b['id']} has unknown parent '{b['parent']}'")
        if b["kind"] == "person" and not b["parent"]:
            errs.append(f"register: person {b['id']} needs a parent (the body they spoke for)")
        seen, x = set(), b["id"]
        while x and x not in seen:
            seen.add(x)
            x = reg[x]["parent"] if x in reg else None
        if x:
            errs.append(f"register: {b['id']} has a loop in its parents")
    idx = bodies.alias_index(reg)
    for p in files:
        d = yaml.safe_load(p.read_text(encoding="utf-8"))
        found, unknown = bodies.resolve(d, reg, idx)
        if d.get("bodies"):
            errs += [f"register: {d['id']} lists unknown body '{u}'" for u in unknown]
        else:
            warns += [f"register: {d['id']} speaker '{u}' matches no body in data/bodies.csv" for u in unknown]
    for e in errs:
        print("FAIL " + e)
    for w in warns:
        print("WARN " + w)
    print(f"register: {len(reg)} bodies and people, {len(errs)} problems, {len(warns)} unmatched speakers.")
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
