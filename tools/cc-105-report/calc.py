#!/usr/bin/env python3
"""CC-105: ADPD said Malta "has yet to acknowledge" noise effects on residents near the Freeport and Malta
International Airport and should study them. Reads data/cc-105/ (sources and retrieval date in its README) and writes
data/cc-105/checks.csv: (1) total people exposed to modelled aircraft noise (round 3, 2016); (2) how many of the
five Birżebbuġa monitoring points had average levels above the EU Noise Directive reporting thresholds (55 dB Lden
day-evening-night, 50 dB Lnight) at the top of their reported range, and above WHO 2018 levels for aircraft
(45 / 40 dB). Monitoring values are LAeq(10 min) day and night averages, not Lden/Lnight, so the comparison is
indicative only (stated in the report). (3) the document search results."""
import csv, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[2]
D = ROOT / "data" / "cc-105"
rows = []
A = list(csv.DictReader(open(D / "airport_exposure.csv")))
for ind in ("Lden", "Lnight"):
    for scope in ("inside agglomeration", "outside agglomeration"):
        n = sum(int(r["people"]) for r in A if r["indicator"] == ind and r["scope"] == scope)
        rows.append({"check": f"MIA aircraft noise, {ind}, {scope}, people", "value": n,
                     "note": "round 3, base year 2016; bands from 55 (Lden) / 50 (Lnight) dB"})
    tot = sum(int(r["people"]) for r in A if r["indicator"] == ind)
    rows.append({"check": f"MIA aircraft noise, {ind}, total people", "value": tot, "note": "inside + outside agglomeration"})
inside_pct = 100 * sum(int(r["people"]) for r in A if r["indicator"] == "Lden" and r["scope"] == "inside agglomeration") / \
    sum(int(r["people"]) for r in A if r["indicator"] == "Lden")
rows.append({"check": "Share of exposed (Lden) living inside the agglomeration, %", "value": round(inside_pct, 1), "note": ""})
B = list(csv.DictReader(open(D / "birzebbuga_monitoring.csv")))
day_over = sum(int(r["day_high_dBA"]) > 55 for r in B)
night_over = sum(int(r["night_high_dBA"]) > 50 for r in B)
day_low_over = sum(int(r["day_low_dBA"]) >= 55 for r in B)
night_low_over = sum(int(r["night_low_dBA"]) > 50 for r in B)
rows += [{"check": "Birżebbuġa points whose daytime range reaches above 55 dBA", "value": f"{day_over} of {len(B)}", "note": "top of range"},
         {"check": "Birżebbuġa points whose daytime range is at or above 55 dBA throughout", "value": f"{day_low_over} of {len(B)}", "note": "bottom of range"},
         {"check": "Birżebbuġa points whose night range reaches above 50 dBA", "value": f"{night_over} of {len(B)}", "note": "top of range"},
         {"check": "Birżebbuġa points whose night range is above 50 dBA throughout", "value": f"{night_low_over} of {len(B)}", "note": "bottom of range"},
         {"check": "Highest night average range reported (dBA)", "value": max(int(r["night_high_dBA"]) for r in B), "note": "Dawret il-Qalb Imqaddsa, 50-70"}]
for r in csv.DictReader(open(D / "doc_search.csv")):
    rows.append({"check": f"Search: {r['document']}", "value": f"Freeport {r['hits_Freeport']}; Birżebbuġa {r['hits_Birzebbuga']}; airport {r['hits_airport']}",
                 "note": f"{r['pages']} pages, full text"})
with open(D / "checks.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["check", "value", "note"]); w.writeheader(); w.writerows(rows)
for r in rows:
    print(f"{r['check'][:80]:80s} {r['value']}")
