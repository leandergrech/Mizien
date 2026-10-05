"""Dated events for each claim, and helpers that lay claims out on a time axis.

A claim's timeline joins:
- the statement itself (claim.date);
- the dated sources about it (data/sources.csv): statements, reports and evidence, as published;
- the steps of its check, read from the history of its claim.yml in git: added, check started, verdict recorded or
  changed, confidence changed, report versions, evidence reviewed. Each links to the change on GitHub;
- right of reply (sent, deadline, response) and the next evidence review;
- curated events in claim.yml under `timeline:` (date, kind, text, optional url), for later statements, new data,
  corrections and replies that are not claims of their own.
Statements by the same body on the same topic are added by scripts/build_site_data.py, which knows the bodies.

Dates of statements and sources are as published. Dates of check steps are when the change was committed to the
public repository. Nothing here is inferred: an event without a date is left out.
"""
import csv
import datetime
import pathlib
import re
import subprocess

import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
REPO = "https://github.com/leandergrech/Mizien"
MONTHS = ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"]
MONTH_NAMES = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
               "November", "December"]
CURATED_KINDS = {"statement": "Statement", "data": "New data", "reply": "Reply", "correction": "Correction",
                 "note": "Note"}
STAGE_EVENTS = {"In progress": "Check started", "Drafted": "Draft check recorded",
                "Right of reply": "Sent to the body concerned for reply", "Published": "Check published"}


# ---------------------------------------------------------------- dates

def parse_date(text):
    """A published date as {iso, precision, approx, mid, label}, or None.

    Accepts 2026-10-01, 2025-09, 2019, 1 Oct 2026, Oct 2026, October 1, 2026 and a leading "c." for approximate
    dates. Retrieval and access dates are not publication dates and are ignored, as are "n/d" and free text.
    """
    s = str(text or "").strip()
    if not s or re.match(r"(?i)(retrieved|accessed|n/?d\b|undated|earlier|various|ongoing)", s):
        return None
    approx = bool(re.match(r"(?i)(c\.|ca\.|circa|about|around|~)\s*", s))
    s = re.sub(r"(?i)^(c\.|ca\.|circa|about|around|~)\s*", "", s).strip().rstrip(".")
    y = mo = d = None
    for pattern, order in ((r"(\d{4})-(\d{2})-(\d{2})", "ymd"), (r"(\d{4})-(\d{2})", "ym"), (r"(\d{4})", "y"),
                           (r"(\d{1,2})\s+([A-Za-z]{3,9})\.?,?\s+(\d{4})", "dMy"), (r"([A-Za-z]{3,9})\.?,?\s+(\d{4})", "My"),
                           (r"([A-Za-z]{3,9})\.?\s+(\d{1,2}),?\s+(\d{4})", "Mdy")):
        m = re.fullmatch(pattern, s)
        if not m:
            continue
        parts = dict(zip(order, m.groups()))
        try:
            y = int(parts["y"])
            if "m" in parts:
                mo = int(parts["m"])
            if "M" in parts:
                mo = MONTHS.index(parts["M"][:3].lower()) + 1
            if "d" in parts:
                d = int(parts["d"])
            datetime.date(y, mo or 1, d or 1)
        except (ValueError, KeyError):
            return None
        break
    if y is None or not 1900 < y < 2100:
        return None
    precision = "day" if d else "month" if mo else "year"
    iso = f"{y:04d}" + (f"-{mo:02d}" if mo else "") + (f"-{d:02d}" if d else "")
    mid = datetime.date(y, mo or 7, d or (15 if mo else 1))   # the middle of a month or year, for sorting and axes
    label = (f"{d} " if d else "") + (f"{MONTH_NAMES[mo - 1]} " if mo else "") + str(y)
    return {"iso": iso, "precision": precision, "approx": approx, "mid": mid.isoformat(),
            "label": ("c. " if approx else "") + label}


# ---------------------------------------------------------------- sources

def source_kind(kind_text):
    t = str(kind_text or "")
    if t.lower().startswith("news"):
        return "reported", "Reported"
    if re.search(r"statement|manifesto|parliament|press|speech|interview|post\b|minutes", t, re.I):
        return "said", "Statement published"
    return "evidence", "Evidence published"


def source_events():
    """{claim id: [events]} from data/sources.csv, for sources with a publication date."""
    path = ROOT / "data" / "sources.csv"
    out = {}
    if not path.is_file():
        return out
    with open(path, newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            when = parse_date(r.get("Date"))
            if not when:
                continue
            kind, label = source_kind(r.get("Type"))
            url = (r.get("URL") or "").strip()
            for cid in re.findall(r"CC-\d{3}", r.get("Claim IDs") or ""):
                out.setdefault(cid, []).append({
                    "when": when, "kind": kind, "label": label, "text": (r.get("Source") or "").strip(),
                    "by": (r.get("Publisher") or "").strip(), "url": url if url.startswith("http") else None})
    return out


# ---------------------------------------------------------------- the history of each claim.yml

def _git(*args, data=None):
    return subprocess.run(["git", *args], cwd=ROOT, input=data, capture_output=True, check=True).stdout


def claim_history():
    """{claim id: [(date, sha, subject, record)]}, oldest first, from git. None without full history (a shallow
    clone would date every claim to its last commit, so no check steps are shown rather than wrong ones)."""
    try:
        if _git("rev-parse", "--is-shallow-repository").decode().strip() != "false":
            return None
        log = _git("log", "--no-merges", "--format=@@%H%x09%cs%x09%s", "--name-only", "--", "claims/*/claim.yml").decode("utf-8")
    except (OSError, subprocess.CalledProcessError):
        return None
    commits, cur = [], None
    for line in log.splitlines():
        if line.startswith("@@"):
            sha, date, subject = (line[2:].split("\t", 2) + ["", ""])[:3]
            cur = {"sha": sha, "date": date, "subject": subject, "files": []}
            commits.append(cur)
        elif line.strip() and cur:
            cur["files"].append(line.strip())
    wanted = [(c, f) for c in commits for f in c["files"] if re.fullmatch(r"claims/CC-\d{3}/claim\.yml", f)]
    if not wanted:
        return {}
    raw = _git("cat-file", "--batch", data="".join(f"{c['sha']}:{f}\n" for c, f in wanted).encode())
    out, pos = {}, 0
    for c, f in wanted:
        end = raw.index(b"\n", pos)
        header = raw[pos:end].decode().split()
        pos = end + 1
        record = None
        if len(header) == 3 and header[1] == "blob":
            size = int(header[2])
            try:
                record = yaml.safe_load(raw[pos:pos + size].decode("utf-8"))
            except (yaml.YAMLError, UnicodeDecodeError):
                record = None
            pos += size + 1
        if isinstance(record, dict):
            out.setdefault(f.split("/")[1], []).append((c["date"], c["sha"], c["subject"], record))
    for cid in out:
        out[cid].reverse()   # git log lists newest first
    return out


def check_events(versions):
    """The steps of a check, from successive versions of its claim.yml."""
    events, prev = [], None

    def add(date, label, text="", sha=None, subject=""):
        events.append({"when": parse_date(date), "kind": "check", "label": label, "text": text,
                       "url": f"{REPO}/commit/{sha}" if sha else None, "change": subject})

    for date, sha, subject, d in versions:
        status, verdict, conf = d.get("status"), d.get("verdict"), d.get("verdict_confidence")
        version, reviewed = d.get("version"), d.get("last_reviewed")
        wording = (d.get("claim") or {}).get("wording_status")
        if prev is None:
            add(date, "Added to the claims to check", "", sha, subject)
        p = prev or {}
        if prev is not None and status != p.get("status") and status in STAGE_EVENTS:
            add(date, STAGE_EVENTS[status], "", sha, subject)
        if verdict and verdict != p.get("verdict"):
            label = "Verdict changed" if p.get("verdict") else "Draft verdict recorded"
            text = (f"{p['verdict']} → " if p.get("verdict") else "") + verdict + (f", {conf.lower()} confidence" if conf else "")
            add(date, label, text, sha, subject)
        elif verdict and conf and p.get("verdict_confidence") and conf != p.get("verdict_confidence"):
            add(date, "Confidence changed", f"{p['verdict_confidence']} → {conf}", sha, subject)
        if version and str(version) != str(p.get("version") or ""):
            add(date, f"Report version {version}", "", sha, subject)
        if wording == "Verbatim found" and p.get("wording") not in (None, "Verbatim found") and prev is not None:
            add(date, "Exact wording found", "", sha, subject)
        if reviewed and str(reviewed) != str(p.get("reviewed") or "") and parse_date(reviewed):
            add(str(reviewed), "Evidence reviewed", "", sha, subject)
        prev = {"status": status, "verdict": verdict, "verdict_confidence": conf, "version": version,
                "reviewed": reviewed, "wording": wording}
    seen, out = set(), []
    for e in events:   # one event per step and day, even when several commits repeat it
        key = (e["label"], e["text"], e["when"]["iso"] if e["when"] else "")
        if e["when"] and key not in seen:
            seen.add(key)
            out.append(e)
    return out


# ---------------------------------------------------------------- a claim's timeline

def claim_events(d, sources, history):
    """Every dated event for one claim except statements by the same body (added by the caller)."""
    ev = []
    said = parse_date((d.get("claim") or {}).get("date"))
    if said:
        ev.append({"when": said, "kind": "statement", "label": "The statement", "text": d["claim"].get("speaker", ""),
                   "url": None, "self": True})
    ev += sources.get(d["id"], [])
    ev += check_events(history.get(d["id"], [])) if history else []
    ror = d.get("right_of_reply") or {}
    for key, label in (("sent", "Right of reply sent"), ("deadline", "Right of reply deadline"),
                       ("response", "Reply received")):
        when = parse_date(ror.get("response_date") if key == "response" else ror.get(key))
        if when:
            ev.append({"when": when, "kind": "reply", "label": label, "text": "", "url": None})
    reviewed = parse_date(d.get("last_reviewed"))
    if reviewed and reviewed["precision"] == "day":
        due = datetime.date.fromisoformat(reviewed["iso"]) + datetime.timedelta(days=365)
        ev.append({"when": parse_date(due.isoformat()), "kind": "due", "label": "Evidence review due",
                   "text": "Each finished check is reviewed against new evidence within a year.", "url": None})
    for t in d.get("timeline") or []:
        when = parse_date(t.get("date"))
        if when:
            ev.append({"when": when, "kind": "curated", "label": CURATED_KINDS.get(t.get("kind"), "Note"),
                       "text": str(t.get("text") or ""), "url": t.get("url")})
    return ev


def sort_events(ev):
    order = {"statement": 0, "said": 1, "same-body": 2, "reported": 3, "evidence": 4, "curated": 5, "check": 6,
             "reply": 7, "due": 8}
    return sorted(ev, key=lambda e: (e["when"]["mid"], order.get(e["kind"], 9)))


# ---------------------------------------------------------------- claims on a time axis

def _ordinal(iso_mid):
    return datetime.date.fromisoformat(iso_mid).toordinal()


def axis(mids, pad=0.04):
    """A time range around the given mid-dates, with year (or quarter) ticks as percentages."""
    if not mids:
        return None
    lo, hi = min(map(_ordinal, mids)), max(map(_ordinal, mids))
    if hi - lo < 240:   # at least eight months wide, centred on the dates
        c = (lo + hi) / 2
        lo, hi = c - 120, c + 120
    span = hi - lo
    lo, hi = lo - span * pad, hi + span * pad
    first, last = datetime.date.fromordinal(int(lo)), datetime.date.fromordinal(int(hi))
    ticks = []
    if (hi - lo) > 2.5 * 365:
        for y in range(first.year + 1, last.year + 1):
            ticks.append({"x": round((datetime.date(y, 1, 1).toordinal() - lo) / (hi - lo) * 100, 2), "label": str(y)})
    else:
        for y in range(first.year, last.year + 1):
            for m in (1, 4, 7, 10):
                o = datetime.date(y, m, 1).toordinal()
                if lo < o < hi:
                    ticks.append({"x": round((o - lo) / (hi - lo) * 100, 2),
                                  "label": (str(y) if m == 1 else MONTH_NAMES[m - 1][:3]), "major": m == 1})
    return {"lo": lo, "hi": hi, "ticks": ticks, "from": first.year, "to": last.year}


def place(items, ax, gap=2.6):
    """Give each item (with a `mid` date) an x position (0-100) and a row, so that close dots stack."""
    rows = []
    out = []
    for it in sorted(items, key=lambda i: i["mid"]):
        x = round((_ordinal(it["mid"]) - ax["lo"]) / (ax["hi"] - ax["lo"]) * 100, 2)
        row = next((i for i, last in enumerate(rows) if x - last >= gap), len(rows))
        if row == len(rows):
            rows.append(x)
        else:
            rows[row] = x
        out.append({**it, "x": x, "row": row})
    return out, len(rows)
