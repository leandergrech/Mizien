#!/usr/bin/env python3
"""CC-022 v1.2: electricity 'burden' measured against income and actual use, not price alone.

Reads data/cc-022/eurostat_burden_inputs.csv (fetch_burden.py) and writes data/cc-022/burden_measures.csv: one row per
measure and EU-27 Member State, with the value, the inputs, the Eurostat flags of the inputs and the rank
(1 = lowest burden). Imported by calc.py (checks) and figures.py.

Measures (all ratios use euros on both sides, so no currency or PPS conversion is needed):
  M1  bill_median   annual bill for a fixed 3,750 kWh (mid-point of band DC) at the band-DC price, all taxes, 2024
                    average of S1 and S2, as % of median equivalised net income (EU-SILC 2025, income year 2024).
                    Sensitivity: 2,500 and 5,000 kWh; EU-SILC 2024 (income year 2023); 2025 prices.
  M2  bill_actual   average household's actual bill: household electricity use (nrg_d_hhq, 2024) divided by the number
                    of private households (lfst_hhnhtych, 2024), priced at the consumption-weighted average of the five
                    band prices (2024 S1/S2 average, weights nrg_pc_204_v 2024; Luxembourg has no 2024 weights, so its
                    2025 weights are used), as % of gross disposable income of households and NPISH per household
                    (nasa_10_nf_tr B6G S14_S15, 2024). Bulgaria has no B6G for households, so 26 countries.
  M3  bill_p20      M1 against the top cut-off of the first income quintile (20th percentile, ilc_di01 TC QU1, EU-SILC
                    2025). Sensitivity: mean income of the first quintile = 5 x its income share x mean income.
  M4  hbs_share     electricity's share of household consumption expenditure (hbs_str_t211 CP0451, 2020; 24 countries).
  M5  arrears / warm  arrears on utility bills (ilc_mdes07) and inability to keep the home adequately warm (ilc_mdes01),
                    % of people, EU-SILC 2025, total and below 60% of median income. cool: dwelling not comfortably cool
                    in summer (ilc_hcmp03, 2012 only).
"""
import csv, pathlib
from collections import defaultdict

D = pathlib.Path(__file__).resolve().parents[2] / "data" / "cc-022"
EU = "AT BE BG CY CZ DE DK EE EL ES FI FR HR HU IE IT LT LU LV MT NL PL PT RO SE SI SK".split()
BANDS = ("KWH_LT1000", "KWH1000-2499", "KWH2500-4999", "KWH5000-14999", "KWH_GE15000")
VOLBAND = {"KWH_GE15000": "KWH_LE15000"}  # nrg_pc_204_v labels band DE differently

V, F = {}, {}
for r in csv.DictReader(open(D / "eurostat_burden_inputs.csv")):
    V[(r["series"], r["item"], r["geo"], r["time"])] = float(r["value"])
    F[(r["series"], r["item"], r["geo"], r["time"])] = r["flag"]


def val(s, item, g, t):
    return V.get((s, item, g, t))


def fl(*keys):
    """Flags of the inputs, e.g. 'income 2025 b; price 2025-S2 p'."""
    return "; ".join(f"{k[0]} {k[3]} {F[k]}" for k in keys if F.get(k))


def price_year(g, band, year):
    a, b = val("price", f"nrg_cons={band}", g, f"{year}-S1"), val("price", f"nrg_cons={band}", g, f"{year}-S2")
    return (a + b) / 2 if a is not None and b is not None else None


def weighted_price(g, year):
    wy = year
    if val("volume", "nrg_cons=KWH2500-4999", g, str(year)) is None:
        wy = year + 1  # Luxembourg 2024: no weights published; use the next year's
    w = {b: val("volume", f"nrg_cons={VOLBAND.get(b, b)}", g, str(wy)) for b in BANDS}
    p = {b: price_year(g, b, year) for b in BANDS}
    if None in w.values() or None in p.values():
        return None, wy
    return sum(w[b] * p[b] for b in BANDS) / sum(w.values()), wy


def measures():
    rows = []

    def add(m, g, value, inputs, flags):
        rows.append({"measure": m, "geo": g, "value": value, "inputs": inputs, "flags": flags})

    for g in EU + ["EU27_2020"]:
        pdc = price_year(g, "KWH2500-4999", 2024)
        pdc25 = price_year(g, "KWH2500-4999", 2025)
        fp = fl(*[("price", "nrg_cons=KWH2500-4999", g, t) for t in ("2024-S1", "2024-S2")])
        for kwh in (2500, 3750, 5000):
            for sy in ("2025", "2024"):
                med = val("income", "statinfo=MED_EI", g, sy)
                key = ("income", "statinfo=MED_EI", g, sy)
                add(f"M1 bill {kwh} kWh / median income (SILC {sy})" + ("" if (kwh, sy) != (3750, "2025") else " MAIN"),
                    g, 100 * kwh * pdc / med, f"price {pdc:.4f} EUR/kWh; median {med:.0f} EUR", "; ".join(
                        x for x in (fp, fl(key)) if x))
        med = val("income", "statinfo=MED_EI", g, "2025")
        add("M1b bill 3750 kWh at 2025 prices / median income (SILC 2025)", g, 100 * 3750 * pdc25 / med,
            f"price {pdc25:.4f} EUR/kWh; median {med:.0f} EUR",
            fl(*[("price", "nrg_cons=KWH2500-4999", g, t) for t in ("2025-S1", "2025-S2")],
               ("income", "statinfo=MED_EI", g, "2025")))
        p20 = val("quintile", "statinfo=TC|quant_inc=QU1", g, "2025")
        add("M3 bill 3750 kWh / 20th-percentile income (SILC 2025) MAIN", g, 100 * 3750 * pdc / p20,
            f"price {pdc:.4f}; P20 {p20:.0f} EUR", fl(("quintile", "statinfo=TC|quant_inc=QU1", g, "2025")))
        p20b = val("quintile", "statinfo=TC|quant_inc=QU1", g, "2024")
        add("M3c bill 3750 kWh / 20th-percentile income (SILC 2024)", g, 100 * 3750 * pdc / p20b,
            f"price {pdc:.4f}; P20 {p20b:.0f} EUR", fl(("quintile", "statinfo=TC|quant_inc=QU1", g, "2024")))
        q1 = 5 * val("quintile", "statinfo=SHARE|quant_inc=QU1", g, "2025") / 100 * val("income", "statinfo=MEAN_EI", g, "2025")
        add("M3b bill 3750 kWh / mean income of first quintile (SILC 2025)", g, 100 * 3750 * pdc / q1,
            f"price {pdc:.4f}; Q1 mean {q1:.0f} EUR", fl(("quintile", "statinfo=SHARE|quant_inc=QU1", g, "2025")))
        # M2: actual use per household
        use, hh = val("use", "nrg_bal=FC_OTH_HH_E", g, "2024"), val("households", "", g, "2024")
        inc = val("hhincome", "", g, "2024")
        if use and hh:
            kwh_hh = use * 1e6 / (hh * 1e3)
            add("M2a electricity use per household, kWh (2024)", g, kwh_hh, f"use {use:.0f} GWh; {hh:.1f} thousand households",
                fl(("use", "nrg_bal=FC_OTH_HH_E", g, "2024"), ("households", "", g, "2024")))
            if g == "EU27_2020":  # no EU weights are published: use Eurostat's own all-band average price
                wp, wy = price_year(g, "TOT_KWH", 2024), "Eurostat all-band average"
            else:
                wp, wy = weighted_price(g, 2024)
            if wp is not None:
                add("M2b consumption-weighted price, EUR/kWh (2024)", g, wp, f"weights {wy}", "")
                add("M2c annual bill, average household, EUR (2024)", g, kwh_hh * wp, "", "")
                if inc:
                    inc_hh = inc * 1e6 / (hh * 1e3)
                    add("M2 bill / disposable income per household (2024) MAIN", g, 100 * kwh_hh * wp / inc_hh,
                        f"{kwh_hh:.0f} kWh x {wp:.4f} EUR; income {inc_hh:.0f} EUR per household (weights {wy})",
                        fl(("use", "nrg_bal=FC_OTH_HH_E", g, "2024"), ("households", "", g, "2024"), ("hhincome", "", g, "2024")))
        tot = val("enduse", "nrg_bal=FC_OTH_HH_E", g, "2024")
        for code, lab in (("SC", "space cooling"), ("WH", "water heating"), ("SH", "space heating"),
                          ("LE", "lighting and appliances")):
            x = val("enduse", f"nrg_bal=FC_OTH_HH_E_{code}", g, "2024")
            if tot and x is not None:
                add(f"M2e share of household electricity used for {lab}, % (2024)", g, 100 * x / tot,
                    f"{x:.1f} of {tot:.1f} GWh", "")
        hbs = val("spending", "coicop=CP0451", g, "2020")
        if hbs is not None:
            add("M4 electricity share of consumption spending, % (HBS 2020) MAIN", g, hbs / 10, f"{hbs} per mille",
                fl(("spending", "coicop=CP0451", g, "2020")))
        for s, lab in (("arrears", "M5 arrears on utility bills, %"), ("warm", "M5 unable to keep home warm, %")):
            for grp, gl in (("rskpovth=TOTAL", "all"), ("rskpovth=B_60", "below 60% of median income")):
                x = val(s, grp, g, "2025")
                add(f"{lab} ({gl}, 2025)" + (" MAIN" if grp.endswith("TOTAL") else ""), g, x, "", fl((s, grp, g, "2025")))
        for grp, gl in (("quant_inc=TOTAL", "all"), ("quant_inc=QU1", "first quintile")):
            x = val("cool", grp, g, "2012")
            add(f"M5 dwelling not comfortably cool in summer, % ({gl}, 2012)", g, x, "", fl(("cool", grp, g, "2012")))
    # ranks among EU-27 Member States (1 = lowest burden / best)
    by = defaultdict(list)
    for r in rows:
        if r["geo"] != "EU27_2020" and r["value"] is not None:
            by[r["measure"]].append(r)
    for m, rs in by.items():
        if len(rs) < 10:  # Malta-and-EU-only rows are not ranked
            continue
        rs.sort(key=lambda r: r["value"])
        for r in rs:  # competition ranking: equal values (at Eurostat's published precision) share a rank
            r["rank"] = 1 + sum(round(x["value"], 6) < round(r["value"], 6) for x in rs)
            r["of"] = len(rs)
            r["tied"] = sum(round(x["value"], 6) == round(r["value"], 6) for x in rs) > 1
    for r in rows:
        r.setdefault("rank", "")
        r.setdefault("of", "")
        r.setdefault("tied", "")
    return rows


def write(rows):
    with open(D / "burden_measures.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["measure", "geo", "value", "rank", "of", "tied", "inputs", "flags"],
                           lineterminator="\r\n")
        w.writeheader()
        for r in rows:
            w.writerow({**r, "value": "" if r["value"] is None else round(r["value"], 4)})


if __name__ == "__main__":
    rows = measures()
    write(rows)
    for r in rows:
        if r["geo"] in ("MT", "EU27_2020"):
            print(f"{r['measure'][:72]:72s} {r['geo']:9s} {'' if r['value'] is None else round(r['value'], 3):>10} "
                  f"{r['rank']}/{r['of']}{' (tied)' if r['tied'] else ''}  {r['flags']}")
