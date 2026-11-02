"""CC-148 calculations. Input: data/cc-148/q_all_nsa.json (Eurostat env_ac_aigg_q, NSA, GHG, TOTAL_HH, THS_T,
retrieved 2 Nov 2026, dataset updated 2026-08-14). Output: data/cc-148/checks.csv and results.json"""
import json, csv, pathlib
D = pathlib.Path(__file__).resolve().parents[2] / "data" / "cc-148"
d = json.load(open(D / "q_all_nsa.json"))
geo = d["dimension"]["geo"]["category"]["index"]; t = d["dimension"]["time"]["category"]["index"]; n = len(t)
v = d["value"]; fl = d.get("status", {})
def g(c, q):
    i = str(geo[c] * n + t[q]); return v.get(i), fl.get(i)
MS = [c for c in geo if c != "EU27_2020"]
def yoy(c, q):
    a, _ = g(c, q.replace(q[:4], str(int(q[:4]) - 1))); b, _ = g(c, q)
    return None if not a or not b else (b / a - 1) * 100
out = {}
q1 = {c: yoy(c, "2025-Q1") for c in MS}
rank = sorted(q1, key=lambda c: q1[c])
out["q1_2025"] = {c: round(q1[c], 2) for c in rank}
out["mt_rank_q1_2025"] = rank.index("MT") + 1
out["rose"] = sum(1 for c in MS if q1[c] > 0); out["fell"] = sum(1 for c in MS if q1[c] < 0)
out["eu_q1_2025_pct"] = round(yoy("EU27_2020", "2025-Q1"), 2)
out["eu_q1_2025_mt"] = round(g("EU27_2020", "2025-Q1")[0] / 1000, 1)
out["eu_q1_2024_mt"] = round(g("EU27_2020", "2024-Q1")[0] / 1000, 1)
out["mt_q1_2024"] = g("MT", "2024-Q1")[0]; out["mt_q1_2025"] = g("MT", "2025-Q1")[0]
# Malta Q1 series with year-on-year change, and annual sums
yrs = ["2023", "2024", "2025"]
out["mt_q"] = {q: g("MT", q)[0] for q in t}
out["mt_yoy"] = {q: round(yoy("MT", q), 2) for q in t if q[:4] > "2023" and q in t}
def ann(c, y): 
    vals = [g(c, f"{y}-Q{i}")[0] for i in range(1, 5)]
    return None if None in vals else sum(vals)
out["mt_annual"] = {y: round(ann("MT", y), 1) for y in yrs}
out["mt_annual_yoy"] = {y: round((ann("MT", y) / ann("MT", str(int(y) - 1)) - 1) * 100, 2) for y in yrs[1:]}
out["eu_annual_yoy"] = {y: round((ann("EU27_2020", y) / ann("EU27_2020", str(int(y) - 1)) - 1) * 100, 2) for y in yrs[1:]}
# share of Q1 range: Malta quarterly values range 2023-2025
mt = [g("MT", q)[0] for q in t if q[:4] in yrs]
out["mt_q_min"] = min(mt); out["mt_q_max"] = max(mt)
# Q1 2026
out["q1_2026_mt"] = round(yoy("MT", "2026-Q1"), 2)
out["q1_2026_flag"] = g("MT", "2026-Q1")[1]
out["flags_q1_2025"] = {c: g(c, "2025-Q1")[1] for c in ("MT", "FI", "EU27_2020")}
json.dump(out, open(D / "results.json", "w"), indent=1)
rows = [
 ("A", "Eurostat news item 14 Aug 2025 (as published)", "Malta Q1 2025 vs Q1 2024", "-6.2%", "verbatim; news item read"),
 ("A", "Eurostat news item", "Finland / Denmark", "-4.4% / -4.3%", "verbatim"),
 ("A", "Eurostat news item", "Countries up / down", "20 / 7", "verbatim"),
 ("A", "Eurostat news item", "EU Q1 2025", "900 Mt CO2-eq, +3.4%", "verbatim"),
 ("B", "current vintage env_ac_aigg_q (updated 14 Aug 2026)", "Malta Q1 2025 vs Q1 2024", f"{q1['MT']:.2f}%", "calc.py"),
 ("B", "current vintage", "Finland Q1 2025 vs Q1 2024", f"{q1['FI']:.2f}%", "calc.py"),
 ("B", "current vintage", "Malta rank (1 = largest fall)", str(out['mt_rank_q1_2025']), "calc.py"),
 ("B", "current vintage", "EU27 Q1 2025 vs Q1 2024", f"{out['eu_q1_2025_pct']}%", "calc.py"),
 ("B", "current vintage", "Member States up / down", f"{out['rose']} / {out['fell']}", "calc.py"),
 ("C", "current vintage", "Malta annual total change 2024 / 2025", f"{out['mt_annual_yoy']['2024']}% / {out['mt_annual_yoy']['2025']}%", "sum of four quarters, calc.py"),
 ("C", "current vintage", "EU27 annual total change 2024 / 2025", f"{out['eu_annual_yoy']['2024']}% / {out['eu_annual_yoy']['2025']}%", "sum of four quarters, calc.py"),
 ("C", "current vintage", "Malta Q1 2026 vs Q1 2025", f"{out['q1_2026_mt']}%", f"flag {out['q1_2026_flag']}"),
]
with open(D / "checks.csv", "w", newline="") as f:
    w = csv.writer(f, lineterminator="\r\n"); w.writerow(["Group", "Source", "Quantity", "Value", "Note"]); w.writerows(rows)
print(json.dumps(out, indent=1))
