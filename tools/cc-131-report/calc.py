"""CC-131 calculations from data/cc-131/eurostat_cdw.csv (run fetch.py first).
Writes data/cc-131/checks.csv. Every figure the report uses is written here.

Recovery rate of construction and demolition waste, as published by Eurostat (indicator cei_wm040, now withdrawn from
the database) and reproduced in the JRC 2024 report's Table 10: recycling + backfilling (operations R2-R11) of
non-hazardous mineral waste from construction and demolition (EWC-Stat W121) divided by the same waste treated (TRT)."""
import csv, pathlib, statistics as st

ROOT = pathlib.Path(__file__).resolve().parents[2]
D = ROOT / "data" / "cc-131"
SRC = "Eurostat env_wastrt / env_wasgen; retrieved see eurostat_cdw.csv"
MS = "BE BG CZ DK DE EE IE EL ES FR HR IT CY LV LT LU HU MT NL AT PL PT RO SI SK FI SE".split()
rows = list(csv.DictReader(open(D / "eurostat_cdw.csv", encoding="utf-8")))
V, FL = {}, {}
for r in rows:
    k = (r["dataset"], r["geo"], r["waste"], r["hazard"], r["oper"], int(r["year"]))
    V[k] = float(r["value"]); FL[k] = r["flag"]
T = lambda g, op, y, h="NHAZ", w="W121": V.get(("env_wastrt", g, w, h, op, y))
G = lambda g, y, h="NHAZ", w="W121": V.get(("env_wasgen", g, w, h, "GEN", y))
out = []


def add(cid, desc, val, unit, note="", src=SRC):
    out.append([cid + " " + desc, ("%.3f" % val) if isinstance(val, float) else val, unit, src, note])


def rate(g, y, op="RCV_R_B", h="NHAZ"):
    t, n = T(g, "TRT", y, h), T(g, op, y, h)
    return None if not t or n is None else n / t * 100


YEARS = (2010, 2012, 2014, 2016, 2018, 2020, 2022)
# A. Malta's recovery rate (the Commission: 'is 100'; Table A8.1: 100 in 2018 and 2020)
for y in YEARS:
    add("A%d" % y, "Malta recovery rate, mineral C&D waste (W121, non-hazardous) %d" % y, rate("MT", y), "%",
        "recovered %.0f t of %.0f t treated" % (T("MT", "RCV_R_B", y), T("MT", "TRT", y)))
add("A-unit", "Unit of the Commission's '100' (Table A8.1 row and JRC Table 10 heading)", "percent", "text",
    "JRC 2024 Table 10: 'Overall recovery rate for CDW across the EU Member States (in %)'", "JRC 2024 report p. 42")
# B. EU-27 (the Commission: 'EU average of 89%'; Table A8.1: 88 in 2018, 89 latest)
for y in (2014, 2016, 2018, 2020, 2022):
    add("B%d" % y, "EU-27 recovery rate, W121 non-hazardous %d" % y, rate("EU27_2020", y), "%",
        "hazardous + non-hazardous: %.2f" % rate("EU27_2020", y, h="HAZ_NHAZ"))
for y in (2020, 2022):
    vals = {g: rate(g, y) for g in MS if rate(g, y) is not None and T(g, "RCV_R_B", y)}
    add("B%d-mean" % y, "Simple mean of Member States with data, recovery rate %d" % y, st.mean(vals.values()), "%",
        "%d states; median %.1f" % (len(vals), st.median(vals.values())))
    top = sorted(g for g, v in vals.items() if v >= 99.5)
    add("B%d-100" % y, "Member States whose rate rounds to 100 in %d" % y, len(top), "count", " ".join(top))
    lo = min(vals, key=vals.get)
    add("B%d-min" % y, "Lowest recovery rate %d" % y, vals[lo], "%", lo)
    above70 = sum(1 for v in vals.values() if v >= 70)
    add("B%d-70" % y, "Member States at or above the 70%% target, %d" % y, above70, "count", "of %d with data" % len(vals))
add("B-gap2020", "Malta minus EU-27, recovery rate 2020 (current Eurostat vintage)", rate("MT", 2020) - rate("EU27_2020", 2020), "percentage points",
    "Commission: 100 vs 89 (11 points)")
add("B-gap2022", "Malta minus EU-27, recovery rate 2022", rate("MT", 2022) - rate("EU27_2020", 2022), "percentage points")
# C. JRC Table 10 (2020 column, as printed on pp. 42-43) against current Eurostat
JRC2020 = {"EU27_2020": 89, "BE": 99, "BG": 96, "CZ": 96, "DK": 97, "DE": 94, "EE": 93, "IE": None, "EL": 100, "ES": 73,
           "FR": 74, "HR": 89, "IT": 98, "CY": 79, "LV": 99, "LT": 98, "LU": 99, "HU": 98, "MT": 100, "NL": 100, "AT": 91,
           "PL": 74, "PT": 95, "RO": 88, "SI": 97, "SK": 81, "FI": 63, "SE": 74}
same, diff = 0, []
for g, j in JRC2020.items():
    if j is None:
        continue
    now = rate(g, 2020)
    if now is not None and abs(now - j) <= 1.0:
        same += 1
    else:
        diff.append("%s JRC %d now %.1f" % (g, j, now))
add("C1", "JRC Table 10 2020 values matched by current Eurostat W121 non-hazardous (within 1 point)", same, "count",
    "of %d; differ: %s" % (sum(1 for j in JRC2020.values() if j is not None), "; ".join(diff)),
    "JRC 2024 Table 10 (typed from the PDF) vs env_wastrt")
add("C2", "France recovery rate 2020, current vintage (JRC Table 10: 74)", rate("FR", 2020), "%", "revised since the JRC extraction")
# D. Composition: recycling vs backfilling, Malta and EU-27
for g, lab in (("MT", "Malta"), ("EU27_2020", "EU-27")):
    for y in YEARS:
        r, b = rate(g, y, "RCV_R"), rate(g, y, "RCV_B")
        if r is None or (g == "EU27_2020" and y < 2014):
            continue
        add("D-%s-%d" % (g, y), "%s %d: recycling | backfilling share of treated W121" % (lab, y), r, "%",
            "backfilling %.1f%%; landfill and other disposal %.1f%%" % (b, rate(g, y, "DSP_L_OTH")))
for y in (2020, 2022):
    vals = {g: rate(g, y, "RCV_R") for g in MS if rate(g, y, "RCV_R") is not None}
    order = sorted(vals, key=lambda g: -vals[g])
    add("D-rank%d" % y, "Malta rank on recycling share of W121 %d (1 = highest)" % y, order.index("MT") + 1, "rank",
        "of %d; EU-27 aggregate %.1f%%" % (len(vals), rate("EU27_2020", y, "RCV_R")))
    bvals = {g: rate(g, y, "RCV_B") for g in MS if rate(g, y, "RCV_B") is not None}
    border = sorted(bvals, key=lambda g: -bvals[g])
    add("D-brank%d" % y, "Malta rank on backfilling share of W121 %d (1 = highest)" % y, border.index("MT") + 1, "rank",
        "of %d; top: %s" % (len(bvals), ", ".join("%s %.0f" % (g, bvals[g]) for g in border[:4])))
# E. The 2010-2012 change of classification (quarry deposits: landfill -> backfilling)
for y in (2010, 2012):
    add("E%d" % y, "Malta W121 landfill and other disposal %d" % y, T("MT", "DSP_L_OTH", y), "tonnes",
        "%.1f%% of treated; backfilling %.0f t" % (rate("MT", y, "DSP_L_OTH"), T("MT", "RCV_B", y)))
# F. Treated vs generated (the indicator's denominator is treated waste)
for y in (2018, 2020, 2022):
    add("F%d" % y, "Malta W121 treated / generated %d" % y, T("MT", "TRT", y) / G("MT", y) * 100, "%",
        "generated %.0f t; treated %.0f t" % (G("MT", y), T("MT", "TRT", y)))
for y in (2018, 2020, 2022):
    add("F-soil%d" % y, "Malta soils (W126) generated | treated %d (outside the indicator)" % y, G("MT", y, w="W126"), "tonnes",
        "treated %.0f t; recovered %.0f t" % (T("MT", "TRT", y, w="W126"), T("MT", "RCV_R_B", y, w="W126")))
# G. NSO NR 023/2026 (2024 data), read through WebFetch: backfilling of mineral C&D waste +58.0% (381,727 t),
# recycling -13.6% (197,255 t) on 2022 (revised). Derived levels are approximate (rounded percentages). Second-hand-marked.
NSO = "NSO NR 023/2026, 17 Feb 2026 (release text read via WebFetch; tables not read)"
b22, r22 = 381727 / 0.580, 197255 / 0.136
b24, r24 = b22 + 381727, r22 - 197255
add("G1", "NSO-implied 2022 (revised) backfilling | recycling of mineral C&D waste", b22, "tonnes", "recycling %.0f t" % r22, NSO)
add("G2", "NSO-implied 2024 backfilling | recycling of mineral C&D waste", b24, "tonnes", "recycling %.0f t" % r24, NSO)
add("G3", "NSO-implied 2024 backfilling share of (recycling + backfilling)", b24 / (b24 + r24) * 100, "%",
    "2022 (revised): %.1f%%; approximate, from rounded percentages" % (b22 / (b22 + r22) * 100), NSO)
# H. flags
for g in ("MT", "EU27_2020"):
    for y in (2020, 2022):
        f = {FL[k] for k in FL if k[1] == g and k[2] == "W121" and k[3] == "NHAZ" and k[5] == y and k[0] == "env_wastrt"}
        add("H-%s-%d" % (g, y), "Eurostat status flags, %s W121 non-hazardous treatment %d" % (g, y),
            ",".join(sorted(x or "none" for x in f)), "flags", "e = estimated")
with open(D / "checks.csv", "w", newline="", encoding="utf-8") as fh:
    w = csv.writer(fh, lineterminator="\r\n")
    w.writerow(["check", "value", "unit", "source", "note"]); w.writerows(out)
for o in out:
    print(o[0][:90], "|", o[1], o[2], "|", o[4])
