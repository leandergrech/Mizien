"""CC-133 calculations from data/cc-133/eurostat_housing.csv (run fetch.py first).
Writes data/cc-133/checks.csv. Every figure the report uses is written here."""
import csv, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
D = ROOT / "data" / "cc-133"
SRC = "Eurostat tipsho60, prc_hpi_a, prc_hicp_aind, nasa_10_nf_tr, nama_10_pe, ilc_di03; retrieved see eurostat_housing.csv"
rows = list(csv.DictReader(open(D / "eurostat_housing.csv", encoding="utf-8")))
V, FL = {}, {}
for r in rows:
    k = (r["dataset"], r["geo"], r["item"], r["unit"], int(r["year"]))
    V[k] = float(r["value"]); FL[k] = r["flag"]
MT, EU = "MT", "EU27_2020"
hpi = lambda g, y: V[("prc_hpi_a", g, "TOTAL", "I15_A_AVG", y)]
hpig = lambda g, y: V[("prc_hpi_a", g, "TOTAL", "RCH_A_AVG", y)]
ptir = lambda g, y, u="PTIR_I15": V[("tipsho60", g, "PTIR", u, y)]
gdi = lambda g, y, i="B7G": V[("nasa_10_nf_tr", g, i + "_S14_S15", "CP_MEUR", y)]
pop = lambda g, y: V[("nama_10_pe", g, "POP_NC", "THS_PER", y)]
med = lambda g, y: V[("ilc_di03", g, "MED_EI", "EUR", y)]
rent = lambda g, y: V[("prc_hicp_aind", g, "CP041", "RCH_A_AVG", y)]
pc = lambda a, b: (b / a - 1) * 100
out = []


def add(cid, desc, val, unit, note=""):
    out.append([cid + " " + desc, ("%.2f" % val) if isinstance(val, float) else val, unit, SRC, note])


# A. nominal house prices since 2014: every year up?
for y in range(2015, 2026):
    add("A%d" % y, "Nominal HPI annual change %d, Malta | EU-27" % y, hpig(MT, y), "%",
        "EU-27 %.1f; Malta faster: %s; Malta flag '%s'" % (hpig(EU, y), "yes" if hpig(MT, y) > hpig(EU, y) else "NO",
                                                           FL[("prc_hpi_a", MT, "TOTAL", "RCH_A_AVG", y)]))
add("A-min", "Smallest Malta annual nominal HPI change 2015-2025", min(hpig(MT, y) for y in range(2015, 2026)), "%")
slower = [y for y in range(2015, 2026) if hpig(MT, y) <= hpig(EU, y)]
add("A-slower", "Years 2015-2025 in which Malta's annual HPI growth was not above the EU-27's", ";".join(map(str, slower)) or "none", "years")
add("A-cum-MT", "Malta nominal HPI change 2014-2025", pc(hpi(MT, 2014), hpi(MT, 2025)), "%")
add("A-cum-EU", "EU-27 nominal HPI change 2014-2025", pc(hpi(EU, 2014), hpi(EU, 2025)), "%")
behind = [y for y in range(2015, 2026) if hpi(MT, y) / hpi(MT, 2014) <= hpi(EU, y) / hpi(EU, 2014)]
add("A-cum-behind", "Years 2015-2025 in which Malta's cumulative rise since 2014 was not above the EU-27's", ";".join(map(str, behind)) or "none", "years")
add("A-cum-2022", "Cumulative rise since 2014 to 2022, Malta | EU-27", pc(hpi(MT, 2014), hpi(MT, 2022)), "%",
    "EU-27 %.1f" % pc(hpi(EU, 2014), hpi(EU, 2022)))
add("A-2005", "Nominal HPI 2025 on 2005 = 100, Malta | EU-27", hpi(MT, 2025) / hpi(MT, 2005) * 100, "index",
    "EU-27 %.1f (Commission Graph A16.1)" % (hpi(EU, 2025) / hpi(EU, 2005) * 100))

# B. Eurostat standardised price-to-income ratio (tipsho60)
for a, b in ((2014, 2024), (2007, 2024), (2008, 2024), (2015, 2020), (2020, 2024), (2022, 2024)):
    add("B%d-%d" % (a, b), "Price-to-income ratio change %d-%d, Malta | EU-27" % (a, b), pc(ptir(MT, a), ptir(MT, b)), "%",
        "EU-27 %.1f" % pc(ptir(EU, a), ptir(EU, b)))
peak = max(range(2000, 2025), key=lambda y: ptir(MT, y))
add("B-peak", "Year of Malta's highest price-to-income ratio (2000-2024)", str(peak), "year", "index %.2f" % ptir(MT, peak))
rises = [y for y in range(2015, 2025) if ptir(MT, y) > ptir(MT, y - 1)]
add("B-rises", "Years 2015-2024 in which Malta's ratio rose", ";".join(map(str, rises)), "years")
for y in (2023, 2024):
    add("B-lt%d" % y, "Ratio relative to long-term average (2000-latest = 100) %d, Malta | EU-27" % y, ptir(MT, y, "PTIR_LT_AVG"),
        "index", "EU-27 %.2f; Commission Graph A16.3 gives MT %s, EU %s (2000-25 avg = 100)" % (
            ptir(EU, y, "PTIR_LT_AVG"), {2023: "96.9", 2024: "92.7"}[y], {2023: "102.0", 2024: "100.2"}[y]))
    add("B-yoy%d" % y, "Ratio annual change %d, Malta" % y, ptir(MT, y, "RCH_A_AVG"), "%",
        "Commission Graph A16.3: %s" % {2023: "-2.2", 2024: "-4.3"}[y])

# C. recompute the ratio: HPI / (adjusted GDI per head), and alternatives
inc = lambda g, y, i="B7G": gdi(g, y, i) / pop(g, y)
for g in (MT, EU):
    r24 = (hpi(g, 2024) / inc(g, 2024)) / (hpi(g, 2015) / inc(g, 2015)) * 100
    add("C-rec-%s" % g, "Recomputed HPI / adjusted GDI per head, 2024 (2015 = 100), %s" % g, r24, "index",
        "Eurostat tipsho60: %.2f" % ptir(g, 2024))
for g in (MT, EU):
    add("C-inc-%s" % g, "Adjusted household GDI per head (B7G) change 2014-2024, %s" % g, pc(inc(g, 2014), inc(g, 2024)), "%",
        "HPI change 2014-2024 %.1f" % pc(hpi(g, 2014), hpi(g, 2024)))
add("C-inc07", "Adjusted GDI per head change 2007-2024, Malta", pc(inc(MT, 2007), inc(MT, 2024)), "%",
    "HPI 2007-2024 %.1f" % pc(hpi(MT, 2007), hpi(MT, 2024)))
add("C-b6", "Unadjusted GDI (B6G) per head change 2014-2024, Malta", pc(inc(MT, 2014, "B6G"), inc(MT, 2024, "B6G")), "%")
add("C-b6ratio", "HPI / unadjusted GDI per head, change 2014-2024, Malta",
    pc(hpi(MT, 2014) / inc(MT, 2014, "B6G"), hpi(MT, 2024) / inc(MT, 2024, "B6G")), "%")
add("C-gdi-tot", "Adjusted GDI (total, not per head) change 2014-2024, Malta", pc(gdi(MT, 2014), gdi(MT, 2024)), "%")
add("C-pop", "Population change 2014-2024, Malta | EU-27", pc(pop(MT, 2014), pop(MT, 2024)), "%",
    "EU-27 %.1f" % pc(pop(EU, 2014), pop(EU, 2024)))
add("C-flags", "Eurostat flags on Malta B7G 2021-2024", ",".join(FL[("nasa_10_nf_tr", MT, "B7G_S14_S15", "CP_MEUR", y)] or "none" for y in range(2021, 2025)), "flags",
    "p = provisional")
# EU-SILC median equivalised net income: survey year t reports income of year t-1
for a, b in ((2014, 2024), (2013, 2023), (2007, 2024)):
    m = pc(med(MT, a + 1), med(MT, b + 1))
    h = pc(hpi(MT, a), hpi(MT, b))
    add("D%d-%d" % (a, b), "Malta median equivalised income change, income years %d-%d (SILC %d-%d)" % (a, b, a + 1, b + 1), m, "%",
        "HPI %d-%d %.1f; HPI / median income ratio change %.1f%%" % (a, b, h, ((1 + h / 100) / (1 + m / 100) - 1) * 100))
    em = pc(med(EU, a + 1), med(EU, b + 1)); eh = pc(hpi(EU, a), hpi(EU, b))
    add("D%d-%d-EU" % (a, b), "EU-27 median equivalised income change, income years %d-%d" % (a, b), em, "%",
        "HPI %.1f; ratio change %.1f%%" % (eh, ((1 + eh / 100) / (1 + em / 100) - 1) * 100))
# E. rents (HICP actual rentals)
for y in (2023, 2024, 2025):
    add("E%d" % y, "HICP actual rentals annual change %d, Malta | EU-27" % y, rent(MT, y), "%", "EU-27 %.1f" % rent(EU, y))
add("E-hpi25", "Nominal HPI annual change 2025, Malta", hpig(MT, 2025), "%", "Commission Annex 16: house prices +5.9%, rents +1.7% in 2024-2025")
with open(D / "checks.csv", "w", newline="", encoding="utf-8") as fh:
    w = csv.writer(fh, lineterminator="\r\n")
    w.writerow(["check", "value", "unit", "source", "note"]); w.writerows(out)
for o in out: print(o[0][:92], o[1], o[2], o[4])
