#!/usr/bin/env python3
"""CC-036: ERA (SoER 2018, ch. 2, p. 15): construction and quarry dust 'is considered to be more of a nuisance rather than a
health-related issue'; 'A minor percentage of this dust is in the PM10 size range, estimated to range between 11 and 22 %'.
Reads data/cc-036/. Writes data/cc-036/checks.csv."""
import csv, pathlib, statistics as st
ROOT = pathlib.Path(__file__).resolve().parents[2]
D = ROOT / "data" / "cc-036"
rows = []
def add(check, value, unit, source, note=""):
    rows.append({"check": check, "value": value, "unit": unit, "source": source, "note": note})

VC = "Vella & Camilleri (2005), Xjenza 10:47-54, Tables 2-3 (data/cc-036/vella2005_size_fractions.csv)"
vc = [float(r["pct_below_10um"]) for r in csv.DictReader(open(D / "vella2005_size_fractions.csv"))]
add("Share of deposited quarry dust below 10 um: minimum", min(vc), "%", VC, f"{len(vc)} samples")
add("Share of deposited quarry dust below 10 um: maximum", max(vc), "%", VC, "ERA: 'between 11 and 22 %'")
add("Share of deposited quarry dust above 10 um (coarse, mostly deposits)", f"{100 - max(vc):.1f}-{100 - min(vc):.1f}", "%", VC)
add("PM10 emitted by softstone quarries a year (as cited by ERA)", 1200, "t", "Vella & Camilleri (2005), abstract; ERA SoER 2018 ch. 2 p. 15")
add("PM10 emission rate in the dry months vs guideline values", "11,500 vs 100-350", "mg/m2/day", "Vella & Camilleri (2005), abstract",
    "the authors' comparison")

EEA = "EEA Air Quality Statistics, annual means, retrieved 16 Nov 2026 (data/cc-036/eea_mt_pm_annual.csv)"
pm = {}
for r in csv.DictReader(open(D / "eea_mt_pm_annual.csv")):
    if r["verification"] == "1" and r["coverage_ok"] == "Yes":
        pm[(r["station_code"], r["pollutant"], int(r["year"]))] = float(r["annual_mean_ugm3"])
NAMES = {"MT00003": "Kordin (industrial)", "MT00005": "Msida (traffic)", "MT00011": "Msida (traffic, new site)", "MT00004": "Zejtun (background)",
         "MT00007": "Gharb (rural background)", "MT00009": "St Paul's Bay (traffic)", "MT00008": "Attard (background)"}
shares = {}
for (s, p, y), v in pm.items():
    if p == "PM10" and (s, "PM2.5", y) in pm:
        c = v - pm[(s, "PM2.5", y)]
        shares.setdefault(s, {})[y] = (v, c, 100 * c / v)
for s in sorted(shares):
    ys = sorted(shares[s]); last = ys[-1]
    v, c, sh = shares[s][last]
    add(f"{NAMES.get(s, s)} {last}: coarse PM10-2.5 (PM10 minus PM2.5)", round(c, 1), "ug/m3", EEA, f"PM10 {v:.1f}; coarse share {sh:.0f}%")
    add(f"{NAMES.get(s, s)}: coarse share of PM10, mean of {len(ys)} years {ys[0]}-{last}",
        round(st.mean(x[2] for x in shares[s].values()), 0), "%", EEA)
allsh = [x[2] for d in shares.values() for x in d.values()]
add("Coarse share of PM10, all station-years with both measured", f"{min(allsh):.0f}-{max(allsh):.0f}", "%", EEA, f"{len(allsh)} station-years")
latest = {}
for (s, p, y), v in pm.items():
    if p == "PM10" and y <= 2025 and (s not in latest or y > latest[s][0]):
        latest[s] = (y, v)
WHO = "WHO Global Air Quality Guidelines (2021), Table 0.1"
above = [s for s, (y, v) in latest.items() if v > 15]
add("Stations whose latest verified PM10 annual mean exceeds the WHO 2021 guideline (15 ug/m3)", f"{len(above)} of {len(latest)}", "", f"{EEA}; {WHO}",
    "; ".join(f"{NAMES.get(s, s)} {y}: {v:.1f}" for s, (y, v) in sorted(latest.items())))
add("Coarse PM10-2.5 alone at Msida (2023) vs the WHO PM10 guideline", round(shares["MT00005"][2023][1] / 15, 1), "x", f"{EEA}; {WHO}",
    "coarse fraction alone is about twice the guideline for all PM10")

ST = "Stafoggia et al. (2016), EHP 124:413-419, doi:10.1289/ehp.1409164 (abstract)"
add("Desert-dust PM10, natural mortality per 10 ug/m3 (lag 0-1), 13 Southern European cities", "0.65 (0.24-1.06)", "%", ST)
add("Non-desert PM10, natural mortality per 10 ug/m3 (lag 0-1)", "0.55 (0.24-0.87)", "%", ST)
ISA = "US EPA ISA for PM (2019), Table ES-1 (data/cc-036/epa_isa2019_coarse.csv)"
isa = list(csv.DictReader(open(D / "epa_isa2019_coarse.csv")))
add("EPA determinations for PM10-2.5 rated 'suggestive' (none causal or likely causal)",
    sum(r["pm10_2_5"].startswith("Suggestive") for r in isa), "outcome-exposure pairs", ISA)
with open(D / "checks.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
for r in rows:
    print(f"{r['check'][:84]:84s} {str(r['value']):>14} {r['unit']:6s} {r['note'][:70]}")
