#!/usr/bin/env python3
"""CC-153: check the claim's figures against the Commission's own pages -> data/cc-153/checks.csv."""
import csv, pathlib, datetime as dt
ROOT = pathlib.Path(__file__).resolve().parents[2]
D = ROOT / "data" / "cc-153"
inf = list(csv.DictReader(open(D / "infringement_list.csv")))
pg = list(csv.DictReader(open(D / "commission_nbrp_page.csv")))
deadline = dt.date(2025, 12, 31)
notice = dt.date(2026, 3, 12)
rows = []
def add(c, v, u, s, n=""): rows.append({"check": c, "value": v, "unit": u, "source": s, "note": n})
S1 = "Commission Representation in Malta, 12 Mar 2026 (read 3 Nov 2026)"
S2 = "Commission DG Energy NBRP page (read 3 Nov 2026)"
add("Member States sent a letter of formal notice", len(inf), "count", S1, "Malta + 18 others")
add("Malta's case number", [r["case_number"] for r in inf if r["member_state"] == "Malta"][0], "id", S1)
add("Months to respond (as stated)", 2, "months", S1)
add("Draft-plan deadline (as stated)", "2025-12-31", "date", S1, "Directive (EU) 2024/1275 Art. 3: first draft by 31 Dec 2025 (German text read at gesetze.legal; EUR-Lex refused)")
add("Entries on Commission NBRP page", len(pg), "count", S2, "18 Member States + Walloon Region")
add("Malta has an entry on the Commission NBRP page", "no", "", S2)
by = [r for r in pg if dt.date.fromisoformat(r["date_printed_beside_draft_plan"]) <= deadline]
add("Entries dated on or before 31 Dec 2025", len(by), "count", S2, ", ".join(r["entry"] for r in by))
after = [r for r in pg if dt.date.fromisoformat(r["date_printed_beside_draft_plan"]) > deadline]
add("Entries dated after 31 Dec 2025", len(after), "count", S2)
late_after_notice = [r for r in pg if dt.date.fromisoformat(r["date_printed_beside_draft_plan"]) > notice]
add("Entries dated after the 12 Mar 2026 notice", len(late_after_notice), "count", S2)
names = {r["member_state"] for r in inf}
pnames = {r["entry"].split(" (")[0] for r in pg}
add("Notified states with an entry on the page by 3 Nov 2026", ", ".join(sorted(n for n in names if n in pnames)), "list", S1 + "; " + S2)
add("Notified states with no entry on the page", ", ".join(sorted(n for n in names if n not in pnames)), "list", S1 + "; " + S2, "includes Malta; page may lag submissions")
add("Days from deadline to notice", (notice - deadline).days, "days", S1)
with open(D / "checks.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["check", "value", "unit", "source", "note"]); w.writeheader(); w.writerows(rows)
for r in rows: print(r["check"], "=", r["value"])
