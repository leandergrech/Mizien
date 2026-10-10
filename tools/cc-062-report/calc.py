#!/usr/bin/env python3
"""CC-062: test KPMG's '9% of GVA direct, about 14% with indirect linkages' with formulas, not by eye.

Reads data/cc-062/ (KPMG tables transcribed with page numbers; Eurostat nama_10_a64 and naio_10_cp1750 for Malta,
retrieved 8 Oct 2026) and writes data/cc-062/checks.csv.
"""
import csv, json, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
D = ROOT / "data" / "cc-062"

K = {}
for r in csv.DictReader(open(D / "kpmg_tables.csv")):
    K[(r["item"], r["year"])] = float(r["value"])
k = lambda item, y="2024": K[(item, y)]

# ---- Eurostat nama_10_a64 (current prices, EUR million)
d = json.load(open(D / "nama_10_a64_MT.json"))
ids, sz = d["id"], d["size"]
ix = {a: list(d["dimension"][a]["category"]["index"]) for a in ids}


def E(nace, item, year):
    f = 0
    for a, s in zip(ids, sz):
        c = {"nace_r2": nace, "na_item": item, "time": str(year)}.get(a)
        f = f * s + (ix[a].index(c) if c else 0)
    return d["value"].get(str(f))


rows = []


def add(check, value, unit, source, note=""):
    rows.append({"check": check, "value": value, "unit": unit, "source": source, "note": note})


R1 = lambda x, n=2: round(x, n)

# ---- 1. The '9%' (direct), KPMG's own table
f, l, tot = k("GVA construction sector (NACE F)"), k("GVA real estate activities excluding imputed rents"), \
    k("Total GVA less imputed rents")
add("KPMG Table 1.1: (F + L excl. imputed rents) / total GVA less imputed rents, 2024", R1(100 * (f + l) / tot), "%",
    "KPMG Table 1.1 (p. 23)", "recomputed; KPMG prints 9.1%")
for y in ("2020", "2021", "2022", "2023"):
    add(f"KPMG Table 1.1 share, {y}",
        R1(100 * (k("GVA construction sector (NACE F)", y) + k("GVA real estate activities excluding imputed rents", y))
           / k("Total GVA less imputed rents", y), 1), "%", "KPMG Table 1.1 (p. 23)")
imp_k = k("Total GVA", "2024") - tot
add("Imputed rents implied by KPMG (total GVA 21,378 less 20,617)", R1(imp_k, 0), "EUR million", "KPMG Tables 1.1, 1.2",
    "implied; Eurostat L68A for 2024 is 737.5")

# ---- 2. The same share from Eurostat's current vintage
for y in (2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025):
    F_, L_, I_, T_ = E("F", "B1G", y), E("L", "B1G", y), E("L68A", "B1G", y), E("TOTAL", "B1G", y)
    add(f"Eurostat {y}: (F + L - imputed rents) / (total GVA - imputed rents)", R1(100 * (F_ + L_ - I_) / (T_ - I_)),
        "%", "Eurostat nama_10_a64", "2025 is the latest annual value in the dataset on 8 Oct 2026; see report limitations"
        if y == 2025 else "")
    add(f"Eurostat {y}: (F + L) / total GVA, imputed rents included in both", R1(100 * (F_ + L_) / T_), "%",
        "Eurostat nama_10_a64")
F24, L24, I24, T24 = E("F", "B1G", 2024), E("L", "B1G", 2024), E("L68A", "B1G", 2024), E("TOTAL", "B1G", 2024)
add("Eurostat 2024 GVA: total economy", T24, "EUR million", "Eurostat nama_10_a64", "KPMG Table 1.2: 21,378.2")
add("Eurostat 2024 GVA: construction (F)", F24, "EUR million", "Eurostat nama_10_a64",
    "KPMG Table 1.2: 809.0 (an earlier vintage; Eurostat is 10% higher)")
add("Eurostat 2024 GVA: real estate (L) including imputed rents", L24, "EUR million", "Eurostat nama_10_a64",
    "KPMG Table 1.2: 1,826.9")
add("Eurostat 2024 GVA: imputed rents (L68A)", I24, "EUR million", "Eurostat nama_10_a64")

# ---- 3. The '14%': arithmetic of KPMG Table 1.3
oc, mc = k("Output from construction"), k("Construction Type 1 value added multiplier")
orr, mr = k("Output from real estate (incl. imputed rents)"), k("Real estate Type 1 value added multiplier")
vc, vr = oc * mc, orr * mr
add("Table 1.3: construction output x 0.55", R1(vc, 1), "EUR million", "KPMG Table 1.3 (p. 30)", "KPMG prints 1,317")
add("Table 1.3: real estate output x 0.78", R1(vr, 1), "EUR million", "KPMG Table 1.3 (p. 30)", "KPMG prints 1,901")
add("Table 1.3: unrounded sum less inter-industry linkages (216)", R1(vc + vr + k("Less inter-industry linkages"), 1),
    "EUR million", "KPMG Table 1.3", "KPMG prints 3,002 (3,219 - 216 = 3,003 on its rounded lines)")
share14 = 100 * k("Estimated contribution to total GVA") / k("Total GVA", "2024")
add("Table 1.3: 3,002 / total GVA 21,378 (incl. imputed rents)", R1(share14), "%", "KPMG Tables 1.2, 1.3",
    "KPMG prints 14.04%")
add("Table 1.3: construction share 1,317 / 21,378", R1(100 * k("Value added from construction (direct + indirect)")
                                                      / k("Total GVA"), 2), "%", "KPMG Table 1.3", "KPMG prints 6.16%")
add("Table 1.3: real estate share 1,901 / 21,378", R1(100 * k("Value added from real estate (direct + indirect)")
                                                     / k("Total GVA"), 2), "%", "KPMG Table 1.3", "KPMG prints 8.89%")
add("Eurostat 2024 output: construction (F)", E("F", "P1", 2024), "EUR million", "Eurostat nama_10_a64",
    "KPMG Table 1.3 uses 2,395")
add("Eurostat 2024 output: real estate (L, incl. imputed rents)", E("L", "P1", 2024), "EUR million",
    "Eurostat nama_10_a64", "KPMG Table 1.3 uses 2,438")

# ---- 4. Like-for-like decomposition of the step from 9% to 14% (KPMG's own figures)
direct_incl = k("GVA construction (F)", "2024 (Table 1.2)") + k("GVA real estate (L) including imputed rents")
s_dir_incl = 100 * direct_incl / k("Total GVA")
s_dir_excl = 100 * (f + l) / tot
add("Direct F + L including imputed rents, KPMG's figures", R1(direct_incl, 1), "EUR million", "KPMG Table 1.2 (p. 25)")
add("Direct share incl. imputed rents (same basis as the 14%)", R1(s_dir_incl), "%", "KPMG Table 1.2 (p. 25)")
add("Step 1: change of basis (imputed rents in), 9.1% -> direct incl. imputed", R1(s_dir_incl - s_dir_excl), "pp",
    "calculated")
add("Step 2: indirect linkages on the same basis, direct incl. imputed -> 14.04%", R1(share14 - s_dir_incl), "pp",
    "calculated")
add("Total step 9.1% -> 14.04%", R1(share14 - s_dir_excl), "pp", "calculated")
add("Share of the step due to change of basis", round(100 * (s_dir_incl - s_dir_excl) / (share14 - s_dir_excl)), "%",
    "calculated")
Ed_incl = 100 * (F24 + L24) / T24
add("Same, with Eurostat's current vintage: direct incl. imputed rents", R1(Ed_incl), "%", "Eurostat nama_10_a64",
    "indirect step would be 14.04 - this")
add("Multiplier-based value added beyond direct, construction (1,317 - 809)", R1(vc - k("GVA construction (F)", "2024 (Table 1.2)"), 0),
    "EUR million", "calculated", "multiplier-based, not observed")
add("Multiplier-based value added beyond direct, real estate (1,901 - 1,827)", R1(vr - k("GVA real estate (L) including imputed rents"), 0),
    "EUR million", "calculated", "multiplier-based, not observed")
add("Direct value added per EUR of output, construction (KPMG 809 / 2,395)",
    R1(k("GVA construction (F)", "2024 (Table 1.2)") / oc, 3), "ratio", "calculated",
    "compare Type 1 multiplier 0.55: indirect adds 0.55 - this")

# ---- 5. Can the multipliers be re-derived from open data? Completeness of Eurostat's Malta SIOT 2015
for y in (2015, 2020):
    s = json.load(open(D / f"naio_10_cp1750_MT_{y}.json"))
    ava = list(s["dimension"]["ind_ava"]["category"]["index"])
    use = list(s["dimension"]["ind_use"]["category"]["index"])
    g = lambda a, u: s["value"].get(str(ava.index(a) * len(use) + use.index(u))) or 0.0
    inds = [u for u in use if u in ava and not u.startswith("P") and u not in ("TOTAL", "TU", "TFU")]
    cover = sum(g("B1G", u) for u in inds if g("P1", u) > 0)
    add(f"Eurostat naio_10_cp1750 Malta {y}: value added in industries with a published column", R1(cover, 0),
        "EUR million", "Eurostat naio_10_cp1750", f"of total {R1(g('B1G', 'TOTAL'), 0)}: {R1(100 * cover / g('B1G', 'TOTAL'), 0)}%")
    add(f"Eurostat naio_10_cp1750 Malta {y}: industry columns with output > 0",
        sum(1 for u in inds if g("P1", u) > 0), "columns", "Eurostat naio_10_cp1750",
        "of 121 listed codes, including aggregates and sub-items")

with open(D / "checks.csv", "w", newline="") as fh:
    w = csv.DictWriter(fh, ["check", "value", "unit", "source", "note"])
    w.writeheader()
    w.writerows(rows)
for r in rows:
    print(f"{r['check'][:95]:95s} {r['value']} {r['unit']}")
