#!/usr/bin/env python3
"""CC-114: test "Malta is the only EU Member State that, instead of reducing, has increased the intensity of its
greenhouse gas emissions since 2013; +17% while the EU average fell 34%" (PN press release, 26 Jan 2026).

Reads data/cc-114/eurostat_extract.csv and eurostat_map_jan2026.csv (fetch.py; Eurostat, retrieved 6 Oct 2026) and
writes data/cc-114/checks.csv (every figure in the report), ranking_2013_2024.csv (the 27 Member States on four
measures) and sensitivity.csv (base and end years). Status flags are carried through: i = value imputed by Eurostat
or other receiving agencies, e = estimated, p = provisional, b = break in series.
"""
import csv
import pathlib
import statistics

ROOT = pathlib.Path(__file__).resolve().parents[2]
D = ROOT / "data" / "cc-114"
EU27 = "BE BG CZ DK DE EE IE EL ES FR HR IT CY LV LT LU HU MT NL AT PL PT RO SI SK FI SE".split()
NAMES = dict(zip(EU27, ["Belgium", "Bulgaria", "Czechia", "Denmark", "Germany", "Estonia", "Ireland", "Greece", "Spain",
                        "France", "Croatia", "Italy", "Cyprus", "Latvia", "Lithuania", "Luxembourg", "Hungary", "Malta",
                        "Netherlands", "Austria", "Poland", "Portugal", "Romania", "Slovenia", "Slovakia", "Finland",
                        "Sweden"]))
V, F = {}, {}
for r in csv.DictReader(open(D / "eurostat_extract.csv")):
    k = (r["dataset"], r["geo"], r["item"], r["unit"], int(r["year"]))
    V[k] = float(r["value"])
    F[k] = r["flag"]
MAP = {r["geo"]: float(r["change_2013_2024_pct"]) for r in csv.DictReader(open(D / "eurostat_map_jan2026.csv"))
       if r["change_2013_2024_pct"] not in ("", ":")}
ES = "Eurostat (data/cc-114/eurostat_extract.csv, retrieved 6 Oct 2026)"
rows = []
used_flags = set()


def add(check, value, unit, note="", source=ES):
    rows.append({"check": check, "value": value, "unit": unit, "source": source, "note": note})


def g(ds, geo, item, unit, y):
    k = (ds, geo, item, unit, y)
    if k in V:
        if F[k]:
            used_flags.add((ds, geo, y, F[k]))
        return V[k]
    return None


pc = lambda a, b: 100 * (a / b - 1)
r1 = lambda x: round(x, 1)

# ------------------------------------------------------------------ 1. Eurostat's published indicator
INT = ("env_ac_aeint_r2", "GHG|TOTAL|B1G", "G_EUR_CLV20")
intens = lambda geo, y, unit="G_EUR_CLV20": g(INT[0], geo, INT[1], unit, y)


def change(fn, geo, a, b):
    x, y = fn(geo, a), fn(geo, b)
    return None if x is None or y is None else pc(y, x)


ch = {c: change(intens, c, 2013, 2024) for c in EU27}
eu = change(intens, "EU27_2020", 2013, 2024)
order = sorted(EU27, key=lambda c: ch[c])
add("Published GHG intensity of GVA (g per EUR, chain-linked 2020), change 2013-2024: Malta", r1(ch["MT"]), "%",
    f"{intens('MT', 2013)} -> {intens('MT', 2024)} g/EUR; 2024 flagged '{F[(INT[0], 'MT', INT[1], INT[2], 2024)]}'")
add("Same, EU-27", r1(eu), "%", f"{intens('EU27_2020', 2013)} -> {intens('EU27_2020', 2024)} g/EUR")
add("Same: Member States with an increase", ", ".join(c for c in EU27 if ch[c] > 0) or "none", "list",
    f"{sum(ch[c] > 0 for c in EU27)} of 27")
add("Same: Malta's rank (1 = largest fall)", order.index("MT") + 1, "of 27")
add("Same: next-weakest Member State", f"{NAMES[order[-2]]} {ch[order[-2]]:.1f}%", "")
for c in ("EE", "IE", "FI"):
    add(f"Same, {NAMES[c]}", r1(ch[c]), "%")
add("Same: unweighted mean of the 27 national changes", r1(statistics.mean(ch[c] for c in EU27)), "%",
    "the -34% is the EU aggregate (EU emissions / EU GVA), not a mean of countries")
chcp = {c: change(lambda geo, y: intens(geo, y, "G_EUR_CP"), c, 2013, 2024) for c in EU27}
add("Published GHG intensity at current prices, change 2013-2024: Malta", r1(chcp["MT"]), "%",
    "risers at current prices: " + (", ".join(c for c in EU27 if chcp[c] > 0) or "none")
    + f"; EU-27 {change(lambda geo, y: intens(geo, y, 'G_EUR_CP'), 'EU27_2020', 2013, 2024):.1f}%")
add("Malta: published intensity, change 2013-2016 and 2013-2021", f"{change(intens, 'MT', 2013, 2016):.1f} / "
    f"{change(intens, 'MT', 2013, 2021):.1f}", "%")
# January vintage
add("January 2026 vintage (Eurostat map, 20 Jan 2026): Malta", MAP["MT"], "%", source="data/cc-114/eurostat_map_jan2026.csv")
add("January 2026 vintage: EU-27", MAP["EU27_2020"], "%", source="data/cc-114/eurostat_map_jan2026.csv")
add("January 2026 vintage: Member States with an increase", ", ".join(c for c in EU27 if MAP[c] > 0), "list",
    source="data/cc-114/eurostat_map_jan2026.csv")
diffs = {c: round(ch[c] - MAP[c], 1) for c in EU27 if abs(ch[c] - MAP[c]) >= 0.15}
add("Revisions between the January map and the August 2026 data (points, >=0.15)", "; ".join(
    f"{c} {MAP[c]:+.1f}->{ch[c]:+.1f}" for c in diffs), "", "Malta's NSO revised 2013-2018 air transport in Feb 2026")

# sensitivity: end year and base year
sens = []
for end in range(2014, 2025):
    c_ = {c: change(intens, c, 2013, end) for c in EU27}
    sens.append(["base 2013", end, r1(c_["MT"]), sum(v > 0 for v in c_.values()),
                 ", ".join(c for c in EU27 if c_[c] > 0), r1(change(intens, "EU27_2020", 2013, end))])
for base in [b for b in range(2008, 2024) if b != 2013]:
    c_ = {c: change(intens, c, base, 2024) for c in EU27}
    sens.append([f"base {base}", 2024, r1(c_["MT"]), sum(v > 0 for v in c_.values() if v is not None),
                 ", ".join(c for c in EU27 if c_[c] is not None and c_[c] > 0), r1(change(intens, "EU27_2020", base, 2024))])
with open(D / "sensitivity.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["base", "end_year", "malta_change_pct", "n_member_states_rising", "rising", "eu27_change_pct"])
    w.writerows(sens)
add("End year 2023 (last year Malta reported; 2024 is a Eurostat estimate): Malta 2013-2023",
    r1(change(intens, "MT", 2013, 2023)), "%",
    "risers 2013-2023: " + (", ".join(c for c in EU27 if change(intens, c, 2013, 2023) > 0) or "none"))
add("End year 2022: Malta 2013-2022", r1(change(intens, "MT", 2013, 2022)), "%")
only_years = [s[1] for s in sens if s[0] == "base 2013" and s[4] == "MT"]
add("End years (base 2013) in which Malta is the only riser", ", ".join(map(str, only_years)) or "none", "years")
add("Base years (end 2024) in which Malta is the only riser",
    ", ".join(s[0][5:] for s in sens if s[0] != "base 2013" and s[4] == "MT") or "none", "years")
add("Malta: published intensity 2008, 2013, 2016, 2020, 2022, 2023, 2024",
    ", ".join(f"{intens('MT', y):.0f}" for y in (2008, 2013, 2016, 2020, 2022, 2023, 2024)), "g/EUR")
add("Malta: change 2022-2024", r1(change(intens, "MT", 2022, 2024)), "%")

# ------------------------------------------------------------------ 2. Malta: what drives it
AE = "env_ac_ainah_r2"
em = lambda geo, n, y: g(AE, geo, f"GHG|{n}", "THS_T", y)
gva = lambda geo, n, y: g("nama_10_a64", geo, f"{n}|B1G", "CLV20_MEUR", y)
for y in (2013, 2024):
    add(f"Malta: recomputed intensity {y} (ainah TOTAL / a64 GVA)", round(1000 * em("MT", "TOTAL", y) /
        gva("MT", "TOTAL", y), 1), "g/EUR", f"published {intens('MT', y)}; GVA vintage of 6 Oct 2026")
add("Malta: GHG of resident production units (NACE total), 2013 -> 2024",
    f"{em('MT', 'TOTAL', 2013) / 1000:.2f} -> {em('MT', 'TOTAL', 2024) / 1000:.2f}", "Mt CO2e",
    f"{pc(em('MT', 'TOTAL', 2024), em('MT', 'TOTAL', 2013)):+.0f}%")
add("Malta: real GVA change 2013-2024", r1(pc(gva("MT", "TOTAL", 2024), gva("MT", "TOTAL", 2013))), "%",
    "nama_10_a64, chain-linked volumes 2020")
add("EU-27: real GVA change 2013-2024", r1(pc(gva("EU27_2020", "TOTAL", 2024), gva("EU27_2020", "TOTAL", 2013))), "%")
for n, lab in (("H51", "air transport"), ("D", "electricity, gas, steam"), ("H50", "water transport"),
               ("H49", "land transport"), ("HH", "households (not in the intensity)")):
    a, b = em("MT", n, 2013), em("MT", n, 2024)
    add(f"Malta: {lab} ({n}), 2013 -> 2024", f"{a:.0f} -> {b:.0f}", "kt CO2e", f"{pc(b, a):+.0f}%")
rest = lambda y: em("MT", "TOTAL", y) - em("MT", "H", y) - em("MT", "D", y)
add("Malta: all other activities (NACE total less transport and electricity), 2013 -> 2024",
    f"{rest(2013):.0f} -> {rest(2024):.0f}", "kt CO2e", f"{pc(rest(2024), rest(2013)):+.0f}%")
sh = 100 * em("MT", "H51", 2024) / em("MT", "TOTAL", 2024)
add("Malta: air transport share of NACE-total GHG, 2024", r1(sh), "%",
    f"2013: {100 * em('MT', 'H51', 2013) / em('MT', 'TOTAL', 2013):.1f}%")
add("Malta: increase in NACE-total GHG 2013-2024 accounted for by air transport",
    r1(100 * (em("MT", "H51", 2024) - em("MT", "H51", 2013)) / (em("MT", "TOTAL", 2024) - em("MT", "TOTAL", 2013))),
    "%", "more than 100% means the other activities fell together")
add("Cross-check with CC-026: Malta air transport (H51) 2015 -> 2024", f"{em('MT', 'H51', 2015):.0f} -> "
    f"{em('MT', 'H51', 2024):.0f}", "kt CO2e", "CC-026 reported 444 -> 4,730 kt (data/cc-026/)")
BR = "env_ac_aibrid_r2"
br = lambda geo, ind, y: g(BR, geo, f"GHG|{ind}", "THS_T", y)
add("Malta (bridging table): emissions by resident units from fuel bought abroad, air transport, 2013/2019/2022/2023/2024",
    " / ".join(f"{br('MT', 'AEMIS_RES_ABR_ATR', y):.0f}" for y in (2013, 2019, 2022, 2023, 2024)), "kt CO2e",
    "2024 imputed by Eurostat (i)")
add("Malta: fuel-bought-abroad air emissions as % of air transport (H51), 2024",
    r1(100 * br("MT", "AEMIS_RES_ABR_ATR", 2024) / em("MT", "H51", 2024)), "%")
add("Malta (bridging table): territorial inventory total (no LULUCF), 2013 -> 2024",
    f"{br('MT', 'AEMIS_TER', 2013):.0f} -> {br('MT', 'AEMIS_TER', 2024):.0f}", "kt CO2e",
    f"{pc(br('MT', 'AEMIS_TER', 2024), br('MT', 'AEMIS_TER', 2013)):+.0f}%; residence total incl. households "
    f"{br('MT', 'AEMIS_RES', 2013):.0f} -> {br('MT', 'AEMIS_RES', 2024):.0f}")
add("Malta's share of EU-27 air-transport emissions from fuel bought abroad by resident units, 2013 / 2024",
    f"{100 * br('MT', 'AEMIS_RES_ABR_ATR', 2013) / br('EU27_2020', 'AEMIS_RES_ABR_ATR', 2013):.1f} / "
    f"{100 * br('MT', 'AEMIS_RES_ABR_ATR', 2024) / br('EU27_2020', 'AEMIS_RES_ABR_ATR', 2024):.1f}", "%",
    f"Malta's share of EU-27 real GVA 2024: {100 * gva('MT', 'TOTAL', 2024) / gva('EU27_2020', 'TOTAL', 2024):.2f}%")
add("EU-27 (bridging table): fuel bought abroad by resident units, air transport, 2013 -> 2024",
    f"{br('EU27_2020', 'AEMIS_RES_ABR_ATR', 2013) / 1000:.1f} -> {br('EU27_2020', 'AEMIS_RES_ABR_ATR', 2024) / 1000:.1f}",
    "Mt CO2e", f"{pc(br('EU27_2020', 'AEMIS_RES_ABR_ATR', 2024), br('EU27_2020', 'AEMIS_RES_ABR_ATR', 2013)):+.0f}%")


# ------------------------------------------------------------------ 3. other measures, all Member States
def int_x51(geo, y):
    e, h, v_ = em(geo, "TOTAL", y), em(geo, "H51", y), gva(geo, "TOTAL", y)
    return None if None in (e, h, v_) else 1000 * (e - h) / v_


def int_xh(geo, y):
    e, h, v_, vh = em(geo, "TOTAL", y), em(geo, "H", y), gva(geo, "TOTAL", y), gva(geo, "H", y)
    return None if None in (e, h, v_, vh) else 1000 * (e - h) / (v_ - vh)


inv = lambda geo, y: g("env_air_gge", geo, "GHG|TOTX4_MEMO", "MIO_T", y)
gdp = lambda geo, y, u="CLV20_MEUR": g("nama_10_gdp", geo, "B1GQ", u, y)
pop = lambda geo, y: g("nama_10_pe", geo, "POP_NC", "THS_PER", y)
int_inv = lambda geo, y: None if None in (inv(geo, y), gdp(geo, y)) else 1e6 * inv(geo, y) / gdp(geo, y)
int_inv_cp = lambda geo, y: None if None in (inv(geo, y), gdp(geo, y, "CP_MEUR")) else 1e6 * inv(geo, y) / gdp(geo, y, "CP_MEUR")
pp_inv = lambda geo, y: 1000 * inv(geo, y) / pop(geo, y)
pp_res = lambda geo, y: em(geo, "TOTAL_HH", y) / pop(geo, y)
MEAS = [("Published: GHG of resident units per euro of GVA (Eurostat)", intens),
        ("Same, without air transport emissions (H51)", int_x51),
        ("Same, without transport and storage (H) in emissions and GVA", int_xh),
        ("Territorial inventory per euro of GDP (volumes)", int_inv),
        ("Territorial inventory per euro of GDP (current prices)", int_inv_cp),
        ("Territorial inventory per person", pp_inv),
        ("Residence accounts incl. households, per person", pp_res)]
rank_rows = []
for lab, fn in MEAS:
    c_ = {c: change(fn, c, 2013, 2024) for c in EU27}
    ok = [c for c in EU27 if c_[c] is not None]
    o = sorted(ok, key=lambda c: c_[c])
    e_ = change(fn, "EU27_2020", 2013, 2024)
    add(f"{lab}, change 2013-2024: Malta", r1(c_["MT"]), "%",
        f"EU-27 {e_:+.1f}%; Malta rank {o.index('MT') + 1} of {len(ok)} (1 = largest fall); risers: "
        + (", ".join(c for c in ok if c_[c] > 0) or "none") + (f"; missing: {', '.join(set(EU27) - set(ok))}"
                                                               if len(ok) < 27 else ""))
    for c in EU27:
        rank_rows.append([lab, c, NAMES[c], None if c_[c] is None else r1(c_[c]),
                          None if c_[c] is None else o.index(c) + 1, r1(e_)])
with open(D / "ranking_2013_2024.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["measure", "geo", "name", "change_2013_2024_pct", "rank_1_is_largest_fall", "eu27_change_pct"])
    w.writerows(rank_rows)
# CC-025 cross-check: territorial per unit of GDP since 2005
add("Cross-check with CC-025: territorial GHG per unit of GDP, Malta 2005-2024, volumes / current prices",
    f"{change(int_inv, 'MT', 2005, 2024):.1f} / {change(int_inv_cp, 'MT', 2005, 2024):.1f}", "%",
    "CC-025 reported -72% (volumes) and -84% (current prices)")
c25 = {r_["check"]: r_["value"] for r_ in csv.DictReader(open(ROOT / "data/cc-025/checks.csv"))}
add("EU-27: territorial GHG per unit of GDP 2005-2024, volumes / current prices",
    f"{change(int_inv, 'EU27_2020', 2005, 2024):.1f} / {change(int_inv_cp, 'EU27_2020', 2005, 2024):.1f}", "%")
add("CC-025 checks.csv, same figures", c25.get("Malta: GHG per unit of GDP, chain-linked volumes (2020 prices), change "
                                               "2005-2024") + " / " + c25.get("Malta: GHG per unit of GDP, current "
                                                                             "prices, change 2005-2024"), "%",
    source="data/cc-025/checks.csv")
add("Malta: inventory memo items, international navigation / aviation bunkers sold in Malta, 2024",
    f"{g('env_air_gge', 'MT', 'GHG|CRF1D1B', 'MIO_T', 2024):.2f} / {g('env_air_gge', 'MT', 'GHG|CRF1D1A', 'MIO_T', 2024):.2f}",
    "Mt CO2e", "fuel sold on the territory to ships and aircraft of any residence; outside both measures above")

# ------------------------------------------------------------------ 4. the other figures in the release
for c in ("EE", "IE", "FI"):
    add(f"{NAMES[c]}: GHG of resident production units, change 2013-2024 (the release says 'reduced emissions by')",
        r1(pc(em(c, "TOTAL", 2024), em(c, "TOTAL", 2013))), "%", f"intensity change {ch[c]:.1f}%")
REN = lambda geo, b, y: g("nrg_ind_ren", geo, b, "PC", y)
for b, lab in (("REN", "overall (gross final energy consumption)"), ("REN_ELC", "electricity")):
    for y in (2023, 2024):
        o = sorted(EU27, key=lambda c: REN(c, b, y))
        add(f"Renewable share, {lab}, {y}: Malta / EU-27", f"{REN('MT', b, y):.1f} / {REN('EU27_2020', b, y):.1f}", "%",
            f"Malta {o.index('MT') + 1} from the bottom of 27; lowest three: "
            + ", ".join(f"{c} {REN(c, b, y):.1f}" for c in o[:3]))

# ------------------------------------------------------------------ flags
fl = sorted({(ds, y, f) for ds, geo, y, f in used_flags if geo == "MT"})
add("Eurostat status flags on Malta values used", "; ".join(f"{ds} {y}:{f}" for ds, y, f in fl) or "none", "flags",
    "i = imputed by Eurostat or other receiving agencies; e = estimated; p = provisional")
with open(D / "checks.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0]))
    w.writeheader()
    w.writerows(rows)
for r_ in rows:
    print(f"{r_['check'][:96]:96s} {str(r_['value'])[:40]:>40} {r_['unit']}  {r_['note'][:150]}")
