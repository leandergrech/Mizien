"""CC-161: recompute figures from data/cc-161/ -> data/cc-161/checks.csv"""
import csv, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[2]
D = ROOT / "data" / "cc-161"
rows = list(csv.DictReader(open(D / "police_noise_reports.csv", encoding="utf-8")))
out = [["check", "value", "unit", "source", "note"]]
tt = ta = 0
for r in rows:
    t, a = int(r["reports_total"]), int(r["reports_after_2300"])
    tt += t; ta += a
    out.append([f"{r['locality']}: reports to police about excessive noise, Jan 2021-Jun 2022", t, "reports",
                "Lovin Malta 6 Oct 2022 (PQ, second-hand)", f"{a} after 23:00 ({100*a/t:.0f}%)"])
out.append(["Four localities: reports after 23:00 as share of reports", round(100 * ta / tt), "%",
            "calculated from police_noise_reports.csv", f"{ta} of {tt}; second-hand; an input count, not an outcome"])
out.append(["Four localities: reports a month (18 months)", round(tt / 18, 1), "reports/month",
            "calculated", "four localities together; reports received, not complaints to other bodies"])
with open(D / "checks.csv", "w", newline="", encoding="utf-8") as f:
    csv.writer(f).writerows(out)
for o in out[1:]: print(o)
