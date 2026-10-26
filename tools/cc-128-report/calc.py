#!/usr/bin/env python3
"""CC-128: date arithmetic for the Commission's statement that Malta did not consult on, adopt or report its third RBMP on the WFD timetable.
Input: data/cc-128/timeline.csv. Output: data/cc-128/checks.csv"""
import csv, pathlib
from datetime import date
ROOT = pathlib.Path(__file__).resolve().parents[2]
D = ROOT / "data" / "cc-128"
T = {r["item"]: date.fromisoformat(r["date"]) for r in csv.DictReader(open(D / "timeline.csv", encoding="utf-8"))}
k = lambda s: next(v for n, v in T.items() if n.startswith(s))
due_plan, due_rep, due_draft = k("Third RBMP due"), k("Third RBMP reporting"), k("Draft plan due")
due_issues = k("Overview of significant")
c_open, c_close = k("Malta draft third RBMP consultation opens"), k("Malta draft third RBMP consultation closes")
pub, cutoff = k("Third RBMP published"), k("Cut-off")
iss_open, iss_close = k("Malta consultation on significant water management issues opens"), k("Malta consultation on significant water management issues closes")
mo = lambda a, b: round((b - a).days / 30.4375, 1)
rows = []
def add(check, value, unit, note=""): rows.append([check, value, unit, note])
add("Plan due (Art. 13(7))", due_plan.isoformat(), "date", "22 Dec 2000 + 15 years + 6 years")
add("Draft still open for comment on 18 Mar 2024, days after the plan was due", (c_close - due_plan).days, "days", f"{mo(due_plan, c_close)} months; a plan cannot be adopted before its own consultation closes, so adoption was at least this late")
add("Latest possible 'published' date (March 2024) after the plan was due", (pub - due_plan).days, "days", f"{mo(due_plan, pub)} months (end of March 2024)")
add("Reporting date (March 2022) to cut-off of the Commission's assessment", (cutoff - due_rep).days, "days", "Malta had not submitted at 30 Sep 2023")
add("Reporting date to end of March 2024", (pub - due_rep).days, "days", "if reported with publication as the SWD says")
add("Draft plan due to consultation opening", (c_open - due_draft).days, "days", f"{mo(due_draft, c_open)} months")
add("Draft consultation length", (c_close - c_open).days, "days", "Art. 14(2) requires at least six months (about 183 days): 20 Sep 2023 to 18 Mar 2024 is 180 days, i.e. six calendar months")
add("Significant-issues overview due to consultation opening", (iss_open - due_issues).days, "days", f"{mo(due_issues, iss_open)} months; ERA dates ◆ second-hand")
add("Significant-issues consultation length", (iss_close - iss_open).days, "days", "ERA dates ◆ second-hand")
add("Member States without RBMP or FRMP at 30 Sep 2023 (COM(2025) 2)", 5, "of 27", "Bulgaria, Cyprus, Greece, Malta, Portugal; Slovenia and Ireland FRMP only; Slovakia RBMP only")
add("Member States not in the RBMP assessment (COM(2025) 2)", 7, "of 27", "Bulgaria, Cyprus, Greece, Malta, Portugal, Slovenia, Ireland")
with open(D / "checks.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f); w.writerow(["check", "value", "unit", "note"]); w.writerows(rows)
for r in rows: print(r)
