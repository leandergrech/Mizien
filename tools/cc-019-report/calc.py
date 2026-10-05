#!/usr/bin/env python3
"""CC-019: test Amphora Media's 'Green to Grey' figures with formulas, not by eye.

Reads data/cc-019/ and docs/data/geo.json (island areas, OpenStreetMap); writes data/cc-019/checks.csv.
"""
import csv, json, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
D = ROOT / "data" / "cc-019"
A = {r["item"]: float(r["value"]) for r in csv.DictReader(open(D / "amphora_figures.csv"))}
C = {r["rule"]: r for r in csv.DictReader(open(D / "io_lulc_change.csv"))}
ISL = {i["name"]: i["area_m2"] for i in json.load(open(ROOT / "docs" / "data" / "geo.json"))["islands"]}
rows = []


def add(check, value, unit, source, note=""):
    rows.append({"check": check, "value": value, "unit": unit, "source": source, "note": note})


lost = A["Green land built up 2018-2023"]
land = ISL["Malta"] + ISL["Gozo"] + ISL["Comino"] + ISL["Cominotto"] + ISL["Filfla"] + ISL["St Paul's Islands"] + ISL["Manoel Island"]
add("Malta's land area (OSM outlines)", round(land / 1e6, 1), "km2", "OpenStreetMap via geo.json")
add("830,000 m2 as a share of the land area", round(100 * lost / land, 3), "%", "calculated", "Amphora: 0.26%")
add("830,000 m2 in FIFA pitches (105 x 68 m)", round(lost / (105 * 68)), "pitches", "calculated", "Amphora: 116")
add("830,000 m2 vs Comino (OSM outline)", round(lost / ISL["Comino"], 2), "x Comino", "calculated",
    f"Comino {ISL['Comino'] / 1e6:.2f} km2 in OSM; Amphora: roughly a quarter")
add("830,000 m2 vs Comino at 3.5 km2 (area often quoted)", round(lost / 3.5e6, 2), "x Comino", "calculated",
    "Amphora: roughly a quarter")
add("830,000 m2 vs Manoel Island", round(lost / ISL["Manoel Island"], 1), "x Manoel", "calculated", "Amphora: two")
add("EEA 2006-2012 + 2012-2018 + Amphora 2018-2023",
    round((A["Land take 2006-2012 (EEA)"] + A["Land take 2012-2018 (EEA)"] + lost) / 1e6, 2), "km2", "calculated",
    "Amphora: at least 1.94 km2 (methods differ)")
for rule, lab, win in (("strict", "3-year rule", "first mapped as built in 2020-2021"),
                       ("two-year", "2-year rule", "first mapped as built in 2019-2022")):
    r = C[rule]
    add(f"IO land cover, new built-up {win} ({lab})", float(r["new_built_km2"]), "km2", "Impact Observatory LULC v2",
        f"reverse change {r['reverse_km2']} km2; net {r['net_km2']} km2")
    add(f"IO land cover, new built-up from crops / rangeland ({lab})", f"{r['from_crops_pct']} / {r['from_rangeland_pct']}",
        "%", "Impact Observatory LULC v2", "Amphora: nearly 95% farmland")
r = C["single-year"]
add("IO land cover, simple 2018 vs 2023 comparison (single-year maps)", float(r["new_built_km2"]), "km2",
    "Impact Observatory LULC v2", f"reverse change {r['reverse_km2']} km2; net {r['net_km2']} km2 (noise, not credible)")
BU = {int(r["year"]): float(r["area_km2"]) for r in csv.DictReader(open(D / "io_lulc_areas.csv"))
      if r["class"] == "built area"}
steps = {f"{y - 1}->{y}": round(BU[y] - BU[y - 1], 1) for y in sorted(BU)[1:]}
add("IO built-up total, change from one year to the next (largest / smallest)",
    f"{max(abs(v) for v in steps.values())} / {min(abs(v) for v in steps.values())}", "km2",
    "Impact Observatory LULC v2", "; ".join(f"{k} {v:+}" for k, v in steps.items()))
T = {r["item"]: float(r["value"]) for r in csv.DictReader(open(D / "eea_land_take.csv"))}
lo, hi = T["Malta land take 2012-2018 (low reading)"], T["Malta land take 2012-2018 (high reading)"]
add("EEA chart: Malta land take 2012-2018", f"{lo * land / 1e12:.2f}-{hi * land / 1e12:.2f}", "km2", "EEA chart x land area",
    "Amphora quotes 920,000 m2 (0.92 km2)")
add("EEA chart: Malta's rank for land take 2012-2018", int(T["Malta rank among EEA39 countries 2012-2018"]), "of 39",
    "EEA chart", "proportion of country area")
s = C["strict"]
add("Amphora figure vs IO net change (3-year rule)", round(lost / 1e6 / float(s["net_km2"]), 2), "ratio", "calculated",
    "below 1 = Amphora lower than the independent estimate; periods differ (Amphora 2018-2023, IO first built 2020-21)")

# v1.2: Amphora's own polygons (crosscheck.py), the 2024-2025 maps and the CORINE change layers
K = {r["lc2018"]: r for r in csv.DictReader(open(D / "amphora_classes.csv"))}
add("Amphora polygons: number and total area (geometry, UTM 33N)", f"{K['all']['polygons']} / {int(K['all']['area_m2']):,}",
    "- / m2", "Amphora GeoJSON (crosscheck.py)", f"the file's own area_m2 field sums to {int(K['all']['area_m2_field']):,}")
farm = lambda col: round(float(K["cropland"][col]) + float(K["grass"][col]), 1)
add("Amphora: cropland + grass, share of the area with a known 2018 class (geometry / area field / count)",
    f"{farm('share_of_known_pct')} / {farm('share_of_known_by_field_pct')} / {farm('share_of_known_by_count_pct')}", "%",
    "Amphora GeoJSON", f"cropland {K['cropland']['share_of_known_pct']}%, grass {K['grass']['share_of_known_pct']}%; "
                       f"Amphora: nearly 95% farmland (basis not stated; this is our reading)")
add("Amphora: area with no 2018 class ('unknown')", float(K["unknown"]["share_of_all_pct"]), "%", "Amphora GeoJSON",
    f"{K['unknown']['polygons']} polygons")
add("Amphora: cropland share of all area / if every unknown area were farmland",
    f"{K['cropland']['share_of_all_pct']} / {round(100 - sum(float(K[k]['share_of_all_pct']) for k in ('bare', 'water', 'tree', 'bush')), 1)}",
    "%", "calculated", "bounds for 'farmland' depending on how grass and unknown are counted")
add("Amphora: polygons classed as water in 2018", f"{K['water']['polygons']} / {K['water']['area_m2']}", "- / m2",
    "Amphora GeoJSON", "Gżira and Sliema waterfronts: sea in 2018, not green land")
O = {r["measure"]: r for r in csv.DictReader(open(D / "amphora_io_overlap.csv"))}
add("Amphora's area already built in the IO 2018 map (all pixels / >= 20 m inside edges)",
    f"{O['Amphora area: built in the 2018 map']['value']} / "
    f"{O['Amphora area at least 20 m inside a polygon edge: built in the 2018 map']['value']}", "%", "IO x Amphora",
    f"built in all of 2017-19: {O['Amphora area: built in all of the 2017, 2018 and 2019 maps']['value']}%")
rules = ("strict", "two-year", "strict-2025", "two-year-2025")
sh = [float(O[f"{r}: share of Amphora's area that IO maps as new built-up"]["value"]) for r in rules]
add("Share of Amphora's area that IO maps as new built-up (persistence rules)", f"{min(sh)}-{max(sh)}", "%",
    "IO x Amphora", "; ".join(f"{r} {v}" for r, v in zip(rules, sh)))
sh = [float(O[f"{r}: share of IO new built-up inside Amphora's polygons"]["value"]) for r in rules]
s20 = [float(O[f"{r}: share of IO new built-up within 20 m of Amphora's polygons"]["value"]) for r in rules]
add("Share of IO new built-up inside Amphora's polygons (persistence rules)", f"{min(sh)}-{max(sh)}", "%",
    "IO x Amphora", f"within 20 m: {min(s20)}-{max(s20)}%")
E = {r["rule"]: r for r in csv.DictReader(open(D / "io_lulc_change_ext.csv"))}
add("IO net new built-up, all persistence rules incl. 2024-2025 maps", " / ".join(E[r]["net_km2"] for r in rules), "km2",
    "Impact Observatory / Esri 2017-2025", "; ".join(f"{r}: {E[r]['window']}" for r in rules))
ES = [r for r in csv.DictReader(open(D / "io_esri_series.csv"))]
add("Esri 2017-2023 maps identical to the Planetary Computer maps",
    min(float(r["identical_to_planetary_computer_pct"]) for r in ES if r["year"] < "2024"), "% of pixels", "both")
bu = {int(r["year"]): float(r["built_area_km2"]) for r in ES}
add("IO built-up total, change 2023->2024 / 2024->2025", f"{bu[2024] - bu[2023]:+.1f} / {bu[2025] - bu[2024]:+.1f}", "km2",
    "Impact Observatory / Esri")
CL = list(csv.DictReader(open(D / "corine_change.csv")))
for per, amph in (("2006-2012", "Land take 2006-2012 (EEA)"), ("2012-2018", "Land take 2012-2018 (EEA)")):
    lt = [r for r in CL if r["period"] == per and r["land_take"] == "yes"]
    ha = sum(float(r["area_ha"]) for r in lt)
    add(f"CORINE change polygons {per}: change to artificial land (CLC class 1)", round(ha, 1), "ha",
        "EEA CORINE Land Cover change layer", f"{len(lt)} polygon{'s' if len(lt) != 1 else ''}; Amphora quotes {A[amph] / 1e4:.0f} ha; "
        "changes under 5 ha are not mapped")
lt = [r for r in CL if r["period"] == "2012-2018" and r["land_take"] == "yes"]
q = sum(float(r["area_ha"]) for r in lt if r["to_code"] == "131")
add("CORINE 2012-2018: share of land take that became quarries (CLC 131)",
    round(100 * q / sum(float(r["area_ha"]) for r in lt), 1), "%", "EEA CORINE Land Cover change layer",
    f"{q:.1f} ha; airport (CLC 124) from farmland "
    f"{sum(float(r['area_ha']) for r in lt if r['to_code'] == '124'):.1f} ha")

# v1.2, maintainer decision 5 Oct 2026: imagery spot-check of a PPS sample of Amphora's polygons (spotcheck.py)
SP = list(csv.DictReader(open(D / "imagery_spotcheck.csv")))
SS = {(r["group"], r["item"]): r for r in csv.DictReader(open(D / "imagery_spotcheck_summary.csv"))}
nd = sum(int(r["draws"]) for r in SP)
cl = lambda k: SS[("class", k)]
ci = lambda r: f"{r['share_of_draws_pct']} ({r['wilson95_lo_pct']}-{r['wilson95_hi_pct']})"
add(f"Imagery spot-check: share of Amphora's area confirmed green to grey ({nd} PPS draws, {len(SP)} polygons)",
    ci(cl("confirmed")), "% (95% CI)", "Esri World Imagery Wayback x Amphora (spotcheck.py)",
    f"partial {cl('partial')['share_of_draws_pct']}, already grey {cl('already grey')['share_of_draws_pct']}, still open "
    f"{cl('still open')['share_of_draws_pct']}, unclear {cl('unclear')['share_of_draws_pct']}; confirmed + half of "
    f"partial {SS[('rule', 'confirmed + half of partial')]['share_of_draws_pct']}; seed {SP[0]['seed']}; classified by eye")
tm = sum(int(r["draws"]) for r in SP if r["class"] == "unclear" and r["state_sep_2018"] == "mostly cleared or built")
add("Imagery spot-check: sampled area open in 2015-16 but mostly being developed by 4 Sep 2018 (unclear, timing)",
    round(100 * tm / nd, 1), "%", "Esri World Imagery Wayback x Amphora", "no imagery of these spots from Aug 2016 to Sep 2018")
g = SS[("confirmed draws: mostly grey by 6 May 2023", "yes")]
add("Imagery spot-check: confirmed area already mostly grey by 6 May 2023", g["share_of_draws_pct"], "% of confirmed",
    "Esri World Imagery Wayback x Amphora",
    f"partly {SS[('confirmed draws: mostly grey by 6 May 2023', 'partly')]['share_of_draws_pct']}, not yet "
    f"{SS[('confirmed draws: mostly grey by 6 May 2023', 'no')]['share_of_draws_pct']}; article: 2018-2023, map file: 2018-2025")
add("Imagery spot-check: share of Amphora's area confirmed and mostly grey by 6 May 2023",
    ci(SS[("rule", "confirmed and mostly grey by 6 May 2023 (article's 2018-2023)")]), "% (95% CI)",
    "Esri World Imagery Wayback x Amphora", "the article's window, 2018-2023")
grp = "before land type (draws open in the before image)"
f1, f2 = SS[(grp, "fields (cultivated + fallow)")], SS[(grp, "farmland (fields + orchards)")]
add("Imagery spot-check: fields (cultivated + fallow) / with orchards, share of the sampled land open before",
    f"{f1['share_of_draws_pct']} / {f2['share_of_draws_pct']}", "%", "Esri World Imagery Wayback x Amphora",
    f"95% CI {f1['wilson95_lo_pct']}-{f1['wilson95_hi_pct']} / {f2['wilson95_lo_pct']}-{f2['wilson95_hi_pct']}; "
    f"scrub, garrigue or rough grass {SS[(grp, 'grass-scrub-garrigue')]['share_of_draws_pct']}; Amphora: nearly 95% farmland")

with open(D / "checks.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\r\n")
    w.writeheader()
    w.writerows(rows)
for x in rows:
    print(f"{x['check']:70s} {str(x['value']):>14} {x['unit']:9s} {x['note']}")
