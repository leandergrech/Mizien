"""Pledges across election cycles (methodology/verdict-scale.md, Pledges).

data/cycles.csv lists the general elections; a pledge belongs to a cycle. A campaign pledge (manifesto, campaign
promise) belongs to the election it was made for: the first election on or after the date it was made. Any other
pledge belongs to the cycle in force on the date it was made: the last election before it. `cycle:` in the pledge
block overrides either.

data/manifesto_pledges.csv is a light list of manifesto pledges (party, cycle, number, wording, page, source), most of
them never checked, so that a pledge can say which earlier pledge it carries forward (`follows:`) and so that campaign
pledges nobody took up can be found.

Outliers (maintainer decision, 6 Oct 2026) break the chain campaign promise -> government commitment -> outcome:
  unanchored  a government commitment with no earlier pledge: shown only after a recorded search (`follows_search`)
  dropped     a campaign pledge of the governing party with no follow-up after the election (manifesto list)
  drift       linked, but the commitment differs from the promise (`drift:` with a type and a note)
  recycled    the same promise made again in a later cycle while the earlier one was not met
"""
import csv
import datetime as dt
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
KINDS = {
    "campaign": "Campaign pledge",          # manifesto or campaign promise, made before an election
    "government": "Government commitment",  # made in office: budget, strategy, EU plan, ministerial statement
    "proposal": "Party proposal",           # made by a party outside a campaign, or in opposition
    "target": "Institutional target",       # set by an agency or company, not a political promise
}
DRIFT_TYPES = ["target lowered", "deadline moved", "scope narrowed", "measure changed"]
MP_ID = re.compile(r"MP-[A-Z]+-\d{4}-[A-Z0-9-]+")


def load_cycles() -> list:
    p = ROOT / "data" / "cycles.csv"
    if not p.exists():
        return []
    rows = list(csv.DictReader(p.open(encoding="utf-8")))
    return sorted(rows, key=lambda r: r["election_date"])


def load_manifesto() -> dict:
    p = ROOT / "data" / "manifesto_pledges.csv"
    if not p.exists():
        return {}
    return {r["id"]: r for r in csv.DictReader(p.open(encoding="utf-8"))}


def iso(v) -> str:
    """'2026-05', 2026, '2022-03-11' or a date -> a sortable ISO prefix ('' if none)."""
    if isinstance(v, (dt.date, dt.datetime)):
        return v.isoformat()[:10]
    m = re.match(r"^(\d{4})(?:-(\d{2}))?(?:-(\d{2}))?", str(v or ""))
    return "-".join(x for x in m.groups() if x) if m else ""


def cycle_of(p: dict, cycles: list | None = None) -> str | None:
    """The election cycle a pledge belongs to (see the module notes)."""
    if p.get("cycle"):
        return str(p["cycle"])
    cycles = cycles if cycles is not None else load_cycles()
    made = iso(p.get("made_on"))
    if not made or not cycles:
        return None
    kind = p.get("kind")
    if kind == "campaign":   # the election it was made for
        for c in cycles:
            if c["election_date"] >= made[:len(c["election_date"])] or c["election_date"][:len(made)] == made:
                return c["id"]
        return None
    # The cycle in force at the START of the period the date names: a commitment dated only "2026-05" or "2026"
    # could come before the election that month or year, so it is placed in the earlier cycle unless `cycle:` says otherwise.
    start = made + "-01-01"[len(made) - 4:] if len(made) < 10 else made
    last = None
    for c in cycles:
        if c["election_date"] <= start:
            last = c["id"]
    return last or "before-" + cycles[0]["id"]


def cycle_label(cid: str | None, cycles: list | None = None) -> str | None:
    """'2022' -> '2022–26' (the election and the legislature after it); 'before-2022' -> 'before 2022'."""
    cycles = cycles if cycles is not None else load_cycles()
    if not cid:
        return None
    if cid.startswith("before-"):
        return "before " + cid[7:]
    ids = [c["id"] for c in cycles]
    if cid not in ids:
        return cid
    i = ids.index(cid)
    return f"{cid}–{ids[i + 1][2:]}" if i + 1 < len(ids) else f"{cid}–"


def cycle_order(cid: str | None) -> float | None:
    """'2022' -> 2022; 'before-2022' -> 2021.5 (sorts before it); None stays None."""
    if not cid:
        return None
    return float(cid[7:]) - 0.5 if cid.startswith("before-") else float(cid)


def link_type(this_cycle: str | None, prev_cycle: str | None, prev_status: str | None) -> str:
    """What a `follows` link is (methodology/verdict-scale.md, Outliers): 'recycled' only when the earlier pledge was made
    in an EARLIER cycle and was not met; otherwise a neutral 'follows' (for example a government commitment carrying
    forward its own party's campaign pledge in the same cycle, which is the normal chain, not an outlier)."""
    a, b = cycle_order(this_cycle), cycle_order(prev_cycle)
    if a is not None and b is not None and b < a and prev_status and prev_status != "Met":
        return "recycled"
    return "follows"


def _selftest() -> None:
    """Run by validate_claims.py: the rules above, on fixed cases."""
    cy = [{"id": "2022", "election_date": "2022-03-26"}, {"id": "2026", "election_date": "2026-05-30"}]
    assert cycle_of({"made_on": "2022-03-11", "kind": "campaign"}, cy) == "2022"
    assert cycle_of({"made_on": "2026-05", "kind": "campaign"}, cy) == "2026"
    assert cycle_of({"made_on": "2026-05", "kind": "government"}, cy) == "2022"      # month of the election: the earlier cycle
    assert cycle_of({"made_on": "2026-06-02", "kind": "government"}, cy) == "2026"
    assert cycle_of({"made_on": "2019-04-02", "kind": "target"}, cy) == "before-2022"
    assert link_type("2022", "2022", "Off track") == "follows"     # same cycle: the normal chain, not an outlier
    assert link_type("2026", "2022", "Off track") == "recycled"    # made again later while the earlier one was not met
    assert link_type("2026", "2022", "Met") == "follows"
    assert link_type("2026", "2022", None) == "follows"            # status unknown (an unchecked manifesto pledge)


def check(p: dict, claim_ids: set) -> list:
    """Errors in the pledge fields added for cycles and links (the rest is checked in validate_claims.py)."""
    errs = []
    kind = p.get("kind")
    if kind not in KINDS:
        errs.append(f"pledge kind '{kind}' must be one of: {', '.join(KINDS)}")
    cycles = {c["id"] for c in load_cycles()}
    if p.get("cycle") is not None and str(p["cycle"]) not in cycles:
        errs.append(f"pledge cycle '{p['cycle']}' is not in data/cycles.csv")
    mp = load_manifesto()
    for f in p.get("follows") or []:
        f = str(f)
        if re.fullmatch(r"CC-\d{3}", f):
            if f not in claim_ids:
                errs.append(f"pledge follows '{f}' is not a claim")
        elif MP_ID.fullmatch(f):
            if f not in mp:
                errs.append(f"pledge follows '{f}' is not in data/manifesto_pledges.csv")
        else:
            errs.append(f"pledge follows '{f}' must be a claim (CC-NNN) or a manifesto pledge (MP-...)")
    fs = p.get("follows_search")
    if fs is not None:
        if not isinstance(fs, dict) or not iso(fs.get("date")) or not isinstance(fs.get("searched"), list) or not fs.get("searched"):
            errs.append("pledge follows_search must be {date, searched: [what was searched], found: [...] (optional)}")
    d = p.get("drift")
    if d is not None:
        if not p.get("follows"):
            errs.append("pledge drift needs follows (drift is a change from an earlier pledge)")
        if not isinstance(d, dict) or d.get("type") not in DRIFT_TYPES or not str(d.get("note") or "").strip():
            errs.append(f"pledge drift must be {{type: one of {', '.join(DRIFT_TYPES)}, note: what changed, in the words of both}}")
    return errs


def check_files(claim_ids: set) -> list:
    errs = []
    cycles = load_cycles()
    for c in cycles:
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", c.get("election_date", "")):
            errs.append(f"data/cycles.csv: {c.get('id')} election_date must be YYYY-MM-DD")
        if not (c.get("source") or "").strip():
            errs.append(f"data/cycles.csv: {c.get('id')} needs a source")
    ids = {c["id"] for c in cycles}
    for mid, r in load_manifesto().items():
        if not MP_ID.fullmatch(mid):
            errs.append(f"data/manifesto_pledges.csv: id '{mid}' must look like MP-PL-2022-305")
        if r.get("cycle") not in ids:
            errs.append(f"data/manifesto_pledges.csv: {mid} cycle '{r.get('cycle')}' is not in data/cycles.csv")
        if r.get("claim") and r["claim"] not in claim_ids:
            errs.append(f"data/manifesto_pledges.csv: {mid} claim '{r['claim']}' is not a claim")
        for f in [x.strip() for x in (r.get("follows") or "").split(";") if x.strip()]:
            if not (re.fullmatch(r"CC-\d{3}", f) and f in claim_ids) and f not in load_manifesto():
                errs.append(f"data/manifesto_pledges.csv: {mid} follows '{f}', which is neither a claim nor a manifesto pledge")
        if r.get("measurable", "") not in ("", "yes", "no"):
            errs.append(f"data/manifesto_pledges.csv: {mid} measurable must be yes, no or empty")
        if not (r.get("wording") or r.get("summary")):
            errs.append(f"data/manifesto_pledges.csv: {mid} needs a summary (own words) or verbatim wording")
        if r.get("wording") and r.get("wording_status") != "Verbatim found":
            errs.append(f"data/manifesto_pledges.csv: {mid} has wording but wording_status is not 'Verbatim found'")
        if not (r.get("source_url") or "").startswith("http"):
            errs.append(f"data/manifesto_pledges.csv: {mid} needs a source_url")
    return errs
