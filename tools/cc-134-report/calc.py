"""CC-134 calculations from data/cc-134/eurostat_envtax_gdp.csv (run fetch.py first).
Writes data/cc-134/checks.csv. Every figure the report uses is written here."""
import csv, pathlib, statistics as st

ROOT = pathlib.Path(__file__).resolve().parents[2]
D = ROOT / "data" / "cc-134"
SRC = "Eurostat env_ac_tax / nama_10_gdp; retrieved see eurostat_envtax_gdp.csv"
MS = "BE BG CZ DK DE EE IE EL ES FR HR IT CY LV LT LU HU MT NL AT PL PT RO SI SK FI SE".split()
rows = list(csv.DictReader(open(D / "eurostat_envtax_gdp.csv", encoding="utf-8")))
V = {}
FL = {}
for r in rows:
    k = (r["dataset"], r["geo"], r["item"], r["unit"], int(r["year"]))
    V[k] = float(r["value"]); FL[k] = r["flag"]
tax = lambda g, t, u, y: V.get(("env_ac_tax", g, t, u, y))
gdp = lambda g, y: V.get(("nama_10_gdp", g, "B1GQ", "CP_MEUR", y))
out = []


def add(cid, desc, val, unit, note=""):
    out.append([cid + " " + desc, ("%.3f" % val) if isinstance(val, float) else val, unit, SRC, note])


# 1. headline: ENV % GDP 2024, Malta vs EU
mt24, eu24 = tax("MT", "ENV", "PC_GDP", 2024), tax("EU27_2020", "ENV", "PC_GDP", 2024)
add("A1", "Malta total environmental taxes 2024", mt24, "% of GDP", "Commission: 1.4")
add("A2", "EU-27 total environmental taxes 2024", eu24, "% of GDP", "Commission: 2.1")
# recompute Malta from EUR and GDP
rec = tax("MT", "ENV", "MIO_EUR", 2024) / gdp("MT", 2024) * 100
add("A3", "Malta ENV 2024 recomputed: revenue (EUR m) / GDP (EUR m)", rec, "% of GDP",
    "env %.1f m EUR; GDP %.0f m EUR" % (tax("MT", "ENV", "MIO_EUR", 2024), gdp("MT", 2024)))
add("A4", "Gap Malta minus EU, 2024", mt24 - eu24, "percentage points")
add("A5", "Malta as share of EU rate, 2024", mt24 / eu24 * 100, "%")
# 2. rank among 27 (1 = highest)
for y in (2023, 2024):
    vals = {g: tax(g, "ENV", "PC_GDP", y) for g in MS}
    order = sorted(vals, key=lambda g: -vals[g])
    add("B%d" % (y - 2022), "Malta rank among 27, ENV %% GDP %d (1 = highest)" % y, order.index("MT") + 1, "rank",
        "median state %.2f; highest %s %.2f; lowest %s %.2f" % (st.median(vals.values()), order[0], vals[order[0]], order[-1], vals[order[-1]]))
    add("B%dm" % (y - 2022), "Simple mean of the 27 Member States, ENV %% GDP %d" % y, st.mean(vals.values()), "% of GDP",
        "the EU-27 aggregate is %.2f" % tax("EU27_2020", "ENV", "PC_GDP", y))
    below = sum(1 for g in MS if vals[g] < vals["MT"])
    add("B%dn" % (y - 2022), "Member States with a lower rate than Malta, %d" % y, below, "count")
# 3. composition 2023 (Commission text: energy 49%, transport 41%, pollution/resources 0.18%)
env23 = tax("MT", "ENV", "PC_GDP", 2023)
for t, n in (("NRG", "energy"), ("TRA", "transport"), ("POL_RES", "pollution and resources")):
    add("C-" + t, "Malta %s taxes 2023, %% GDP" % n, tax("MT", t, "PC_GDP", 2023), "% of GDP")
    add("C-%s-share" % t, "Malta %s taxes 2023, share of environmental taxes (revenue EUR)" % n,
        tax("MT", t, "MIO_EUR", 2023) / tax("MT", "ENV", "MIO_EUR", 2023) * 100, "%",
        "Commission: energy about 49, transport about 41")
for y in (2022, 2023, 2024):
    add("D%d" % y, "Malta POL_RES %d, %% GDP" % y, tax("MT", "POL_RES", "PC_GDP", y), "% of GDP",
        "EU-27 %.2f" % tax("EU27_2020", "POL_RES", "PC_GDP", y))
# 4. trend
for y in range(2015, 2025):
    add("E%d" % y, "ENV %% GDP %d Malta | EU-27" % y, tax("MT", "ENV", "PC_GDP", y), "% of GDP",
        "EU-27 %.2f" % tax("EU27_2020", "ENV", "PC_GDP", y))
# 5. share of total tax and social contributions (the measure Eurostat/SDG 17 uses)
for y in (2023, 2024):
    add("F%d" % y, "ENV as %% of taxes and social contributions (excl. imputed) %d Malta" % y,
        tax("MT", "ENV", "PC_TSCO_X_ISCO", y), "%", "EU-27 %.2f" % tax("EU27_2020", "ENV", "PC_TSCO_X_ISCO", y))
# 6. what would parity cost: gap x GDP
gap_eur = (eu24 - mt24) / 100 * gdp("MT", 2024)
add("G1", "Revenue if Malta were at the EU-27 share of GDP, minus actual (2024 GDP)", gap_eur, "EUR million",
    "illustration of scale, not a forecast or a recommendation")
# 7. flags
fl = {FL[("env_ac_tax", "MT", "ENV", "PC_GDP", y)] for y in (2022, 2023, 2024)}
add("H1", "Eurostat status flags on Malta ENV PC_GDP 2022-2024", ",".join(sorted(f or "none" for f in fl)), "flags")
with open(D / "checks.csv", "w", newline="", encoding="utf-8") as fh:
    w = csv.writer(fh, lineterminator="\r\n")
    w.writerow(["check", "value", "unit", "source", "note"]); w.writerows(out)
for o in out: print(o[0][:80], o[1], o[2], o[4])
