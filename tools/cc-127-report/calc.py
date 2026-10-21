#!/usr/bin/env python3
"""CC-127: test the figures in "Malta has the lowest proportion of organic farming in the EU" (Commission SWD(2026) 702).
Reads data/cc-127/*.csv (made by fetch_data.py); writes data/cc-127/checks.csv and data/cc-127/ranking_2022.csv."""
import csv, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[2]
D = ROOT / "data" / "cc-127"
EU27 = "AT BE BG CY CZ DE DK EE EL ES FI FR HR HU IE IT LT LU LV MT NL PL PT RO SE SI SK".split()
share = {}
for r in csv.DictReader(open(D / "organic_share_pc_uaa.csv")):
    share[(r["geo"], int(r["year"]))] = (float(r["pc_uaa"]), r["flag"])
area = {}
for r in csv.DictReader(open(D / "organic_area_ha.csv")):
    if r["ha"]:
        area[(r["geo"], int(r["year"]), r["method"])] = float(r["ha"])
uaa = {int(r["year"]): float(r["uaa_ha"]) for r in csv.DictReader(open(D / "uaa_malta_ef_lus_main.csv")) if r["uaa_ha"]}
land = {int(r["year"]): float(r["km2"]) for r in csv.DictReader(open(D / "land_area_malta_km2.csv"))}
rows = []


def add(check, value, unit, note=""):
    rows.append({"check": check, "value": value, "unit": unit, "note": note})


# 1. Rank of Malta by organic share of UAA, each year with data
for y in range(2012, 2025):
    have = {g: share[(g, y)][0] for g in EU27 if (g, y) in share}
    if "MT" not in have:
        continue
    others = sorted((v, g) for g, v in have.items() if g != "MT")
    low = others[0]
    missing = [g for g in EU27 if g not in have]
    add(f"{y}: Malta share of UAA (%)", have["MT"], "%", f"lowest of {len(have)} reporting; next lowest {low[1]} {low[0]}%; missing: {', '.join(missing) or 'none'}")
    assert have["MT"] < low[0], y
# 2. Missing countries in 2022 and their last published values
for g in ("AT", "EL"):
    last = max(y for (gg, y) in share if gg == g)
    add(f"{g} last published share (year {last})", share[(g, last)][0], "%", "country absent from the 2022 release; far above Malta")
# 3. 2022 ranking table
t = sorted(((share[(g, 2022)][0], g, area.get((g, 2022, "TOTAL"), "")) for g in EU27 if (g, 2022) in share))
with open(D / "ranking_2022.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["rank_from_lowest", "geo", "organic_pc_uaa_2022", "organic_ha_2022_total"])
    for i, (v, g, a) in enumerate(t, 1):
        w.writerow([i, g, v, int(a) if a != "" else ""])
add("2022: next-lowest share / Malta share", round(t[1][0] / t[0][0], 2), "x", f"{t[1][1]} {t[1][0]}% vs Malta {t[0][0]}%")
# 4. The Commission's figures
ha66 = area[("MT", 2022, "TOTAL")]
add("Malta organic area 2022, fully converted + in conversion (org_cropar)", ha66, "ha", "Commission: 66")
add("of which fully converted", area[("MT", 2022, "FCONV")], "ha")
add("of which in conversion", area[("MT", 2022, "UCONV")], "ha")
add("66 / 10,700 ha", round(66 / 10700 * 100, 3), "%", "Commission's own two numbers; 'less than 1%'")
add("UAA implied by Eurostat share (66 / 0.62%)", round(ha66 / (share[("MT", 2022)][0] / 100)), "ha", "Eurostat's denominator, close to 10,700")
add("10,700 ha as share of land area (316 km2 = 31,600 ha)", round(10700 / (land[2014] * 100) * 100, 1), "%", "Commission: 34%")
for y in (2016, 2020, 2023):
    a = area.get(("MT", y, "TOTAL"))
    if a:
        add(f"Organic ha {y} / farm-structure-survey UAA {y} ({uaa[y]:.0f} ha)", round(a / uaa[y] * 100, 2), "%", "survey UAA is a different denominator; still below 1%")
# 5. EU average
for y in (2019, 2020):
    add(f"EU-27 average share of UAA {y}", share[("EU27_2020", y)][0], "%", "Eurostat estimate (flag e); last year with an EU aggregate in sdg_02_40")
add("Malta 2020 share / EU-27 2020 share", round(share[("MT", 2020)][0] / share[("EU27_2020", 2020)][0], 3), "ratio", "about one fifteenth")
# 6. Absolute area
small = sorted((area[(g, 2022, "TOTAL")], g) for g in EU27 if (g, 2022, "TOTAL") in area)
add("Smallest organic areas 2022 (ha)", "; ".join(f"{g} {int(a)}" for a, g in small[:4]), "ha", "Malta is also lowest in absolute hectares")
with open(D / "checks.csv", "w", newline="") as f:
    wr = csv.DictWriter(f, fieldnames=["check", "value", "unit", "note"])
    wr.writeheader()
    wr.writerows(rows)
for r in rows:
    print(f"{r['check'][:75]:75s} {str(r['value']):>10} {r['unit']} {r['note']}")
