"""Dated events for each claim, and helpers that lay claims out on a time axis.

A claim's timeline joins:
- the statement itself (claim.date);
- the dated sources about it (data/sources.csv): statements, reports and evidence, as published;
- the research log in claim.yml (`history:`): when the claim was added, each version of its check with what changed,
  corrections and clarifications. These carry the date the research was done, recorded by whoever did it, not the
  date the site or the repository changed. A claim's intake date also comes from data/queue.csv;
- right of reply, the last evidence review and the next one due;
- outside events in claim.yml (`timeline:`): later statements, new data or replies that are not claims of their own.
Statements by the same body on the same topic are added by scripts/build_site_data.py, which knows the bodies.

Nothing here is inferred: an event without a recorded date is left out.
"""
import csv
import datetime
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
REPO = "https://github.com/leandergrech/Mizien"
MONTHS = ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"]
MONTH_NAMES = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
               "November", "December"]
CURATED_KINDS = {"statement": "Statement", "data": "New data", "reply": "Reply", "correction": "Correction by the speaker",
                 "note": "Note"}
HISTORY_STEPS = {   # research log steps (claim.yml `history:`) and how the timeline names them
    "added": "Added to the claims to check", "started": "Check started", "wording": "Exact wording found",
    "version": "Version", "reply-sent": "Right of reply sent", "reply-received": "Reply received",
    "published": "Check published", "correction": "Correction", "clarification": "Clarification", "note": "Note",
}


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
    if re.search(r"\bnews\b|briefing|clipping|locator|blog", t, re.I):
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


# ---------------------------------------------------------------- the research log

def intake_dates():
    """{claim id: date added} from data/queue.csv, the intake record of the checker routines."""
    path = ROOT / "data" / "queue.csv"
    if not path.is_file():
        return {}
    with open(path, newline="", encoding="utf-8") as f:
        return {r["ID"].strip(): r["Added"].strip() for r in csv.DictReader(f) if r.get("Added")}


def history_events(d, added=None):
    """The steps of a check from its research log, dated when the research was done."""
    ev, steps = [], d.get("history") or []
    if added and not any(h.get("step") == "added" for h in steps):
        steps = [{"date": added, "step": "added"}] + list(steps)
    versions = [str(h.get("version")) for h in steps if h.get("step") == "version"]
    for h in steps:
        when = parse_date(h.get("date"))
        step = h.get("step")
        if not when or step not in HISTORY_STEPS:
            continue
        label, text, kind, verdict = HISTORY_STEPS[step], str(h.get("note") or ""), "check", None
        fix = step in ("correction", "clarification") or (step == "version" and bool(h.get("correction")))
        if step == "version":
            v = str(h.get("version"))
            label = f"Version {v}" + (": first issue" if v in ("1", "1.0") else ": corrections" if fix else "")
            if v == str(d.get("version")) and d.get("verdict"):   # the current version carries the current verdict
                conf = d.get("verdict_confidence")
                verdict = d["verdict"] + (f", {conf.lower()} confidence" if conf else "")
        if fix:
            kind = "correction"
        ev.append({"when": when, "kind": kind, "label": label, "text": text, "url": h.get("url"), "step": step,
                   "version": str(h.get("version")) if step == "version" else None, "verdict": verdict})
    return ev


# ---------------------------------------------------------------- a claim's timeline

def claim_events(d, sources, added=None):
    """Every dated event for one claim except statements by the same body (added by the caller)."""
    ev = []
    said = parse_date((d.get("claim") or {}).get("date"))
    if said:
        ev.append({"when": said, "kind": "statement", "label": "The statement", "text": d["claim"].get("speaker", ""),
                   "url": None, "self": True})
    ev += sources.get(d["id"], [])
    ev += history_events(d, added)
    ror = d.get("right_of_reply") or {}
    for key, label in (("sent", "Right of reply sent"), ("deadline", "Right of reply deadline"),
                       ("response_date", "Reply received")):
        when = parse_date(ror.get(key))
        if when and not any(e.get("step") in ("reply-sent", "reply-received") and e["when"]["iso"] == when["iso"] for e in ev):
            ev.append({"when": when, "kind": "reply", "label": label, "text": "", "url": None})
    reviewed = parse_date(d.get("last_reviewed"))
    if reviewed:
        ev.append({"when": reviewed, "kind": "check", "label": "Evidence reviewed", "text": "", "url": None})
        if reviewed["precision"] == "day":
            due = datetime.date.fromisoformat(reviewed["iso"]) + datetime.timedelta(days=365)
            ev.append({"when": parse_date(due.isoformat()), "kind": "due", "label": "Evidence review due",
                       "text": "Each finished check is reviewed against new evidence within a year.", "url": None})
    ev += pledge_events(d)
    for t in d.get("timeline") or []:
        when = parse_date(t.get("date"))
        if when:
            ev.append({"when": when, "kind": "curated", "label": CURATED_KINDS.get(t.get("kind"), "Note"),
                       "text": str(t.get("text") or ""), "url": t.get("url")})
    return ev


def pledge_events(d):
    """A pledge's label (dated by its evidence), the end of its term and its deadline."""
    p = d.get("pledge") or {}
    ev = []
    when = parse_date(p.get("as_of"))
    if when and p.get("status"):
        ev.append({"when": when, "kind": "check", "label": f"Pledge label: {p['status']}",
                   "text": str(p.get("target") or ""), "url": None})
    for key, label in (("term_end", "The term the pledge was made for ended"), ("deadline", "Pledge deadline")):
        w = parse_date(p.get(key)) if p.get(key) is not None else None
        if w:
            ev.append({"when": w, "kind": "pledge", "label": label, "text": "", "url": None})
    return ev


def sort_events(ev):
    order = {"statement": 0, "said": 1, "same-body": 2, "reported": 3, "evidence": 4, "curated": 5, "check": 6,
             "correction": 7, "pledge": 8, "reply": 9, "due": 10}
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
