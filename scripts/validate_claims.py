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
    errs += check_subclaims(d)
    errs += check_pledge(d)
    return errs


TONES = {"green", "lime", "amber", "orange", "red", "maroon", "grey"}


def check_subclaims(d) -> list:
    """`subclaims:` are the parts of a claim tested separately: numbered parent + A, B, C... in order."""
    subs = d.get("subclaims")
    if subs is None:
        return []
    if not isinstance(subs, list) or not all(isinstance(x, dict) for x in subs):
        return ["subclaims must be a list of parts (id, text, finding, rating, tone)"]
    errs = []
    for i, x in enumerate(subs):
        want = f"{d['id']}{chr(ord('A') + i)}"
        if x.get("id") != want:
            errs.append(f"sub-claim {i + 1} must be numbered {want} (the parent's number plus the next letter)")
        if not str(x.get("text") or "").strip():
            errs.append(f"sub-claim {x.get('id') or i + 1}: text is missing")
        if x.get("tone") is not None and x["tone"] not in TONES:
            errs.append(f"sub-claim {x.get('id')}: tone must be one of {', '.join(sorted(TONES))}")
    return errs


def load_pledge_labels() -> list:
    """Labels from the 'Pledges' section of methodology/verdict-scale.md: lines '- **Label**: meaning'."""
    text = (ROOT / "methodology" / "verdict-scale.md").read_text(encoding="utf-8")
    m = re.search(r"^## Pledges\s*$(.*?)(?=^## |\Z)", text, flags=re.M | re.S)
    return re.findall(r"^- \*\*(.+?)\*\*:", m.group(1), flags=re.M) if m else []


def check_pledge(d) -> list:
    """`pledge:` gives a pledge its label (methodology/verdict-scale.md, Pledges) instead of, or beside, a verdict."""
    p = d.get("pledge")
    if p is None:
        return []
    sys.path.insert(0, str(ROOT / "scripts"))
    import bodies
    import timeline
    if not isinstance(p, dict):
        return ["pledge must be a block with status, as_of, made_by, made_on, vehicle, deadline and target"]
    errs, labels = [], load_pledge_labels()
    status = p.get("status")
    if status not in labels:
        errs.append(f"pledge status '{status}' must be one of: {', '.join(labels)}" if labels
                    else "pledge labels are not defined yet: add a 'Pledges' section to methodology/verdict-scale.md")
    as_of = timeline.parse_date(p.get("as_of"))
    if not as_of or as_of["precision"] != "day":
        errs.append("pledge as_of must be a full date (the date of the evidence behind the label)")
    made_on = timeline.parse_date(p.get("made_on"))
    if not made_on:
        errs.append("pledge made_on must be a date (a year or month is enough)")
    elif as_of and as_of["iso"] < made_on["iso"][:len(as_of["iso"])]:
        errs.append("pledge as_of is before made_on")
    reg = bodies.load()
    made_by = p.get("made_by")
    if not isinstance(made_by, list) or not made_by:
        errs.append("pledge made_by must be a list of ids from data/bodies.csv")
    else:
        errs += [f"pledge made_by '{b}' is not in data/bodies.csv" for b in made_by if b not in reg]
    for key in ("vehicle", "target"):
        if not str(p.get(key) or "").strip():
            errs.append(f"pledge {key} is missing")
    if "deadline" not in p:
        errs.append("pledge deadline is missing (use null if none is stated)")
    deadline = timeline.parse_date(p.get("deadline")) if p.get("deadline") is not None else None
    if p.get("deadline") is not None and not deadline:
        errs.append(f"pledge deadline '{p.get('deadline')}' is not a date")
    term_end = timeline.parse_date(p.get("term_end")) if p.get("term_end") is not None else None
    if p.get("term_end") is not None and not term_end:
        errs.append(f"pledge term_end '{p.get('term_end')}' is not a date")
    ended = [x["iso"] for x in (deadline, term_end) if x]
    if as_of and status == "Not yet due" and deadline and deadline["iso"] <= as_of["iso"]:
        errs.append("pledge cannot be 'Not yet due' after its deadline")
    if status == "Missed":
        if not (as_of and any(e <= as_of["iso"] for e in ended)):
            errs.append("pledge can be 'Missed' only after its deadline or term has passed (set deadline or term_end)")
        if not d.get("evidence_shown"):
            errs.append("pledge 'Missed' requires evidence_shown (documents or data that can be shown)")
    for o in p.get("overlaps") or []:
        if not re.fullmatch(r"CC-\d{3}", str(o)) or not (ROOT / "claims" / str(o) / "claim.yml").is_file():
            errs.append(f"pledge overlaps '{o}' is not a claim")
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
        if "correction" in e and not isinstance(e["correction"], bool):
            errs.append(f"history entry {i}: correction must be true or false")
        if e.get("correction") and step != "version":
            errs.append(f"history entry {i}: correction: true marks a version that corrects errors; use step: correction otherwise")
        if (step in ("correction", "clarification") or e.get("correction")) and not str(e.get("note") or "").strip():
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
