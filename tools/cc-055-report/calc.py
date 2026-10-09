#!/usr/bin/env python3
"""CC-055: arithmetic and date checks on the Manoel Island agreement. Writes data/cc-055/checks.csv.

Inputs, all from the sources named in `SRC`: MIDI's announcement of 17 Mar 2026 (reimbursement EUR 47,321,000, about EUR 43 million net of VAT),
Lands Minister Owen Bonnici's figures as reported by TVM News on 17 Mar 2026 (MIDI asked EUR 78 million; agreed EUR 43 million, 'just over half'),
and the dates of the steps in the MIDI announcements and TVM News."""
import csv, pathlib, datetime
ROOT = pathlib.Path(__file__).resolve().parents[2]
D = ROOT / "data" / "cc-055"
SRC = "MIDI announcements MDI214/215/222 (Malta Stock Exchange); TVM News 17 Mar, 28 Apr, 13 May 2026; retrieved 9 Oct 2026"
rows = []
def add(check, value, unit, note=""):
    rows.append({"check": check, "value": value, "unit": unit, "source": SRC, "note": note})
asked, agreed, gross = 78.0, 43.0, 47.321
add("Agreed amount as a share of the amount MIDI asked for (EUR 43m / EUR 78m)", round(100 * agreed / asked, 1), "%",
    "Bonnici: 'just over half' (TVM News 17 Mar 2026); consistent")
add("Gross reimbursement less net amount (EUR 47.321m - about EUR 43m)", round(gross - agreed, 1), "EUR million",
    "MIDI says the net figure is 'circa' EUR 43 million after adjusting for VAT; the two figures in the news are the gross and net of one payment")
d = lambda a, b: (datetime.date.fromisoformat(b) - datetime.date.fromisoformat(a)).days
add("Days from in-principle agreement (17 Mar 2026) to the public deed (13 May 2026)", d("2026-03-17", "2026-05-13"), "days")
add("Days from the shareholders' meeting (28 Apr 2026) to the public deed (13 May 2026)", d("2026-04-28", "2026-05-13"), "days")
add("Days from the public deed (13 May 2026) to the Planning Authority's padel-court decision (16 Jul 2026)", d("2026-05-13", "2026-07-16"), "days", "Lovin Malta, 16 Jul 2026 (PA decision itself not read)")
add("Days from the public deed (13 May 2026) to the check date (9 Oct 2026)", d("2026-05-13", "2026-10-09"), "days", "no national park instrument, plan or local plan change found in the sources searched")
with open(D / "checks.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
for r in rows: print(f"{r['check'][:95]:95s} {r['value']:>8} {r['unit']}")
