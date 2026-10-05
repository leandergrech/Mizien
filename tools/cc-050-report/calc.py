#!/usr/bin/env python3
"""CC-050: BirdLife Malta (27 May 2026) says Labour and the PN are in a 'dangerous political race' to weaken
environmental enforcement on hunting and trapping. Reads data/cc-050/penalties.csv (current law from S.L. 549.42,
retrieved 5 Oct 2026; reported ORNIS proposal, second-hand) and data/cc-050/pn_programme_search.csv; writes
data/cc-050/checks.csv with the size of the reported fine reductions and the manifesto search totals."""
import csv, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[2]
D = ROOT / "data" / "cc-050"
P = list(csv.DictReader(open(D / "penalties.csv")))
rows = []
for r in P:
    cur, new = float(r["current_fine_eur"]), float(r["reported_proposal_fine_eur"])
    rows.append({"check": f"Fine, {r['offender_stage']}", "current_eur": int(cur), "proposed_eur": int(new),
                 "change_eur": int(new - cur), "change_pct": round(100 * (new - cur) / cur, 1),
                 "note": "proposal figures reported by BirdLife Malta / Newsbook (second-hand)"})
S = list(csv.DictReader(open(D / "pn_programme_search.csv")))
rows.append({"check": "PN programme: chapters searched / total hits", "current_eur": "", "proposed_eur": "",
             "change_eur": "", "change_pct": "", "note": f"{len(S)} chapters, {sum(int(s['hits']) for s in S)} hits, "
             f"{sum(int(s['characters_searched']) for s in S):,} characters"})
with open(D / "checks.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
for r in rows:
    print(r)
