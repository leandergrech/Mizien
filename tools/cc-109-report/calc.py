#!/usr/bin/env python3
"""CC-109: test "Transport ... has generated 48% of these [effort-sharing] emissions in 2024, up by 45% since 2005"
with formulas, not by eye.

Inputs (data/cc-109/, written by fetch.py and read_graph.py; commission_figures.csv typed from the documents):
  eurostat_env_air_gge.csv      national inventory, 2026 submission (Eurostat, updated 2 Jun 2026)
  eea_esr_emissions.csv         EEA effort-sharing totals 2005-2024 (2024 = approximated inventory)
  eea_approx_inventory_2024.csv EEA approximated (proxy) inventory for 2024
  eea_govreg_2026v1_mt.csv      EEA GovReg 2026 v1.0 (inventory of 15 Mar 2026), cross-check of Eurostat
  graph31_bars.csv              the Commission's Graph 3.1, read from the PDF's vector paths
  commission_figures.csv        figures typed from the Country Reports and the CAPR country profiles
and, for consistency with Claim Check 003, data/cc-003/eurostat_ghg_population.csv and capr2025_esr_malta.csv.

Definition (Regulation (EU) 2018/842, Art. 2(1) as amended by Regulation (EU) 2023/857, and Art. 2(3)): effort-sharing
transport is all domestic transport (CRF 1.A.3: road, domestic navigation, rail, other) with CO2 from 1.A.3.a civil
aviation treated as zero. So ESR transport = GHG 1.A.3 - CO2 1.A.3.a. Writes data/cc-109/checks.csv.
"""
import csv, pathlib
from collections import defaultdict

ROOT = pathlib.Path(__file__).resolve().parents[2]
D = ROOT / "data" / "cc-109"
rows = []


def add(check, value, unit, source, note=""):
    rows.append({"check": check, "value": value, "unit": unit, "source": source, "note": note})


def pct(a, b):
    return 100 * (a / b - 1)


# ---------------------------------------------------------------- inputs
E = defaultdict(dict)          # (geo, airpol, crf) -> {year: Mt}
EF = {}
for r in csv.DictReader(open(D / "eurostat_env_air_gge.csv")):
    E[(r["geo"], r["airpol"], r["src_crf"])][int(r["year"])] = float(r["value"])
    if r["flag"]:
        EF[(r["geo"], r["airpol"], r["src_crf"], int(r["year"]))] = r["flag"]
UPD = r["eurostat_updated"][:10]
ES = f"Eurostat env_air_gge (2026 inventory submission; updated {UPD}), retrieved 6 Oct 2026"

ESR, ESR_ST = {}, {}
for r in csv.DictReader(open(D / "eea_esr_emissions.csv")):
    if r["country"] == "Malta" and r["year"].isdigit():
        ESR[int(r["year"])] = float(r["value"])
        ESR_ST[int(r["year"])] = r["status"]
EEA_ESR = "EEA, GHG emissions under the Effort Sharing Legislation 2005-2024 (doi:10.2909/f80bebef-447e-4882-b3e9-c4a91cbae4f5)"

PX = {}
for r in csv.DictReader(open(D / "eea_approx_inventory_2024.csv")):
    if r["country"] == "MT" and r["emissions_kt"] not in ("", None):
        try:
            PX[(r["scope"], r["crf_code"])] = float(r["emissions_kt"]) / 1000
        except ValueError:
            pass
EEA_PX = "EEA approximated GHG inventory 2024 (doi:10.2909/cd572015-4d0d-408a-abf8-290ed2057bf7)"

GV = {}
for r in csv.DictReader(open(D / "eea_govreg_2026v1_mt.csv")):
    if r["value"]:
        GV[(r["pollutant"].split(" ")[0], r["sector_code"], int(r["year"]))] = float(r["value"]) / 1000

G = {(r["year"], r["sector"]): r for r in csv.DictReader(open(D / "graph31_bars.csv"))}
GS = "Commission, 2026 Country Report - Malta, Graph 3.1 (p. 14; Council copy p. 16), read from the PDF's vector paths"

def _doc(d):
    return ("CR26" if d.startswith("2026 Country") else "CR25" if d.startswith("2025 Country") else
            "CAPR25" if "2025 country profile" in d else "CAPR24")


CF = {(_doc(r["document"]), r["item"], r["year"]): r for r in csv.DictReader(open(D / "commission_figures.csv"))}
CR = "Commission, 2026 Country Report - Malta, SWD(2026) 218"

MT = lambda pol, crf: E[("MT", pol, crf)]
EU = lambda pol, crf: E[("EU27_2020", pol, crf)]

# ESR transport series (inventory): GHG 1.A.3 minus CO2 from 1.A.3.a domestic aviation
T = {y: MT("GHG", "CRF1A3")[y] - MT("CO2", "CRF1A3A")[y] for y in MT("GHG", "CRF1A3")}
R = MT("GHG", "CRF1A3B")
N = MT("GHG", "CRF1A3D")
TEU = {y: EU("GHG", "CRF1A3")[y] - EU("CO2", "CRF1A3A")[y] for y in EU("GHG", "CRF1A3")}

# ---------------------------------------------------------------- 1. Transport's share of effort-sharing emissions, 2024
T_px, ESR_px = PX[("non-ETS", "1A3")], PX[("ESR", "Total")]
add("ESR transport 2024, approximated inventory (non-ETS 1.A.3)", round(T_px, 4), "Mt CO2e", EEA_PX,
    f"total 1.A.3 {PX[('Total', '1A3')]:.4f} Mt minus domestic-aviation CO2")
add("ESR total 2024, approximated inventory", round(ESR_px, 4), "Mt CO2e", EEA_PX + "; same value in " + EEA_ESR,
    f"EEA ESR dataset 2024: {ESR[2024]:.4f} Mt ({ESR_ST[2024]})")
share_px = 100 * T_px / ESR_px
add("Transport share of ESR emissions 2024, approximated inventory", round(share_px, 1), "%", EEA_PX)
g24 = G[("2024", "Domestic transport (excl. aviation)")]
add("Transport share of ESR emissions 2024, the report's own Graph 3.1", float(g24["share_of_bar_pct"]), "%", GS,
    f"transport {float(g24['value_mt']):.3f} of {float(g24['bar_total_mt']):.3f} Mt")
cap = CF[("CAPR25", "Transport share of effort-sharing emissions (Figure 11)", "2024")]
add("Transport share of ESR emissions 2024, Commission CAPR 2025 country profile", float(cap["value"]), "%",
    "Commission (DG CLIMA), CAPR 2025 country profile Malta, Figure 11, p. 10", cap["note"])
eu = CF[("CAPR25", "EU-27 transport share of effort-sharing emissions (Figure 11)", "2024")]
add("EU-27: transport share of ESR emissions 2024", float(eu["value"]), "%",
    "Commission (DG CLIMA), CAPR 2025 country profile Malta, Figure 11, p. 10")
# with the 2026 inventory (final submission for 2024): our estimate of the ESR total
ets = PX[("ETS", "Total")]
esr_est = MT("GHG", "TOTX4_MEMO")[2024] - ets - MT("CO2", "CRF1A3A")[2024]
add("ESR total 2024 from the 2026 inventory (our estimate)", round(esr_est, 4), "Mt CO2e", ES + "; ETS from " + EEA_PX,
    f"total excl. LULUCF {MT('GHG', 'TOTX4_MEMO')[2024]:.4f} - ETS {ets:.4f} - aviation CO2 {MT('CO2', 'CRF1A3A')[2024]:.4f}")
alt = MT("GHG", "TOTX4_MEMO")[2024] - MT("GHG", "CRF1A1")[2024] - MT("CO2", "CRF1A3A")[2024]
add("ESR total 2024, Claim Check 003 proxy (total minus power generation)", round(alt, 4), "Mt CO2e", ES,
    "CC-003's approach; Malta's ETS covers only power generation")
add("Transport share of ESR emissions 2024, 2026 inventory (our estimate)", round(100 * T[2024] / esr_est, 1), "%", ES,
    f"{T[2024]:.4f} / {esr_est:.4f} Mt; with the CC-003 proxy {100 * T[2024] / alt:.1f}%")
add("Road transport only (1.A.3.b), 2026 inventory, as share of the approximated ESR total, 2024",
    round(100 * R[2024] / ESR_px, 1), "%", ES + "; " + EEA_PX,
    f"{R[2024]:.4f} / {ESR_px:.4f} Mt: the one combination of published figures we found that gives 48% (our identification)")
add("Road transport only, share of the reviewed ESR total, 2023", round(100 * R[2023] / ESR[2023], 1), "%",
    ES + "; " + EEA_ESR, f"{R[2023]:.4f} / {ESR[2023]:.4f} Mt")
add("Report's figure: transport share of ESR emissions 2024", 48, "%", CR + ", pp. 6, 14, 66")
add("Gap: approximated-inventory share minus the report's 48%", round(share_px - 48, 1), "pp", "calculated")

# ---------------------------------------------------------------- 2. 'up by 45% since 2005'
g05 = G[("2005", "Domestic transport (excl. aviation)")]
add("Transport change 2005-2024, the report's own Graph 3.1", round(pct(float(g24["value_mt"]), float(g05["value_mt"])), 1),
    "%", GS, f"{float(g05['value_mt']):.3f} -> {float(g24['value_mt']):.3f} Mt")
add("Transport change 2005-2024, inventory 2005 and approximated 2024", round(pct(T_px, T[2005]), 1), "%",
    ES + "; " + EEA_PX, f"{T[2005]:.4f} -> {T_px:.4f} Mt")
add("Transport change 2005-2024, 2026 inventory (final submission)", round(pct(T[2024], T[2005]), 1), "%", ES,
    f"{T[2005]:.4f} -> {T[2024]:.4f} Mt (GHG 1.A.3 minus CO2 1.A.3.a)")
add("Road transport only (1.A.3.b) change 2005-2024", round(pct(R[2024], R[2005]), 1), "%", ES,
    f"{R[2005]:.4f} -> {R[2024]:.4f} Mt")
add("Domestic navigation (1.A.3.d) change 2005-2024", round(pct(N[2024], N[2005]), 1), "%", ES,
    f"{N[2005]:.4f} -> {N[2024]:.4f} Mt")
cars = MT("GHG", "CRF1A3B1")
add("Cars (1.A.3.b.i) change 2005-2024", round(pct(cars[2024], cars[2005]), 1), "%", ES,
    f"{cars[2005]:.4f} -> {cars[2024]:.4f} Mt")
add("Road share of ESR transport, 2024", round(100 * R[2024] / T[2024], 1), "%", ES)
add("Domestic navigation share of ESR transport, 2005 and 2024", f"{100 * N[2005] / T[2005]:.1f} / {100 * N[2024] / T[2024]:.1f}",
    "%", ES)
inc = T[2024] - T[2005]
add("Share of the 2005-2024 transport increase from road", round(100 * (R[2024] - R[2005]) / inc, 0), "%", ES,
    f"increase {inc:.4f} Mt; navigation {100 * (N[2024] - N[2005]) / inc:.0f}%")
add("Domestic aviation CO2 (excluded from ESR), 2005 and 2024", f"{MT('CO2', 'CRF1A3A')[2005]:.4f} / {MT('CO2', 'CRF1A3A')[2024]:.4f}",
    "Mt CO2e", ES)
# share reading: did the share rise 45%?
sh05_g = float(g05["share_of_bar_pct"])
sh05_i = 100 * T[2005] / ESR[2005]
add("Transport share of ESR emissions 2005", f"{sh05_g:.1f} (Graph 3.1) / {sh05_i:.1f} (inventory over EEA 2005 ESR estimate)",
    "%", GS + "; " + ES + "; " + EEA_ESR, f"EEA 2005 ESR {ESR[2005]:.4f} Mt ({ESR_ST[2005]})")
add("Change in transport's share 2005-2024 (share reading of 'up by 45%')", round(pct(float(g24["share_of_bar_pct"]), sh05_g), 1),
    "%", GS, f"{sh05_g:.1f}% -> {float(g24['share_of_bar_pct']):.1f}%: the share barely moved, so '45%' is the level")

# Table A8.1 row 'domestic road transport': which series is it?
diffs_T, diffs_R = [], []
for y in range(2018, 2024):
    tab = float(CF[("CR26", "Table A8.1 domestic road transport vs base year", str(y))]["value"])
    t, rr = pct(T[y], T[2005]), pct(R[y], R[2005])
    diffs_T.append(abs(tab - t))
    diffs_R.append(abs(tab - rr))
    add(f"Table A8.1 'domestic road transport' {y} vs our series", tab, "%", CR + ", Table A8.1, p. 71",
        f"ESR transport (1.A.3 - aviation CO2) {t:.1f}%; road only (1.A.3.b) {rr:.1f}%")
add("Table A8.1 row vs ESR transport series, 2018-2023: largest difference", round(max(diffs_T), 1), "pp", "calculated",
    "the row is all domestic transport except aviation CO2, despite its label")
add("Table A8.1 row vs road-only series, 2018-2023: largest difference", round(max(diffs_R), 1), "pp", "calculated")

# ---------------------------------------------------------------- 3. Is transport the dominant source?
secs24 = {"Transport (excl. aviation CO2)": T_px, "Buildings (1.A.4, non-ETS)": PX[("non-ETS", "1A4")],
          "Agriculture (3)": PX[("Total", "3")], "Waste (5)": PX[("Total", "5")]}
secs24["Small industry (residual)"] = ESR_px - sum(secs24.values())
for k, v in sorted(secs24.items(), key=lambda kv: -kv[1]):
    add(f"ESR sector share 2024 (approximated): {k}", round(100 * v / ESR_px, 1), "%", EEA_PX, f"{v:.4f} Mt")
lead_years = []
for y in range(2005, 2025):
    others = {"buildings": MT("GHG", "CRF1A4")[y], "agriculture": MT("GHG", "CRF3")[y], "waste": MT("GHG", "CRF5")[y],
              "industry and F-gases": MT("GHG", "CRF1A2")[y] + MT("GHG", "CRF2")[y]}
    if T[y] > max(others.values()):
        lead_years.append(y)
add("Years 2005-2024 in which transport exceeds every other effort-sharing sector", f"{len(lead_years)} of 20", "years", ES,
    "comparison with 1.A.4, 3, 5 and 1.A.2 + 2 (Malta's ETS covers only power generation)")

# ---------------------------------------------------------------- 4. Data status and consistency
add("ESR total 2024 vs 2005, EEA series", round(pct(ESR[2024], ESR[2005]), 1), "%", EEA_ESR,
    f"{ESR[2005]:.4f} ({ESR_ST[2005]}) -> {ESR[2024]:.4f} ({ESR_ST[2024]}); the Commission gives +40.8% on its base")
add("ESR 2005 base implied by the Commission's +40.8% for 2024", round(ESR[2024] / 1.408, 4), "Mt CO2e", "calculated",
    "approximated 2024 total / 1.408; Table A8.1 gives 1.0")
add("ESR transport 2024: approximated vs final inventory", round(pct(T[2024], T_px), 1), "%", ES + "; " + EEA_PX,
    f"{T_px:.4f} (approximated, Nov 2025) vs {T[2024]:.4f} Mt (inventory, Mar 2026)")
a23 = float(CF[("CR26", "Table A8.1 domestic road transport vs base year", "2023")]["value"])
p23 = float(CF[("CR25", "Table A8.1 domestic road transport vs base year", "2023")]["value"])
add("2023 transport change since 2005: approximated (2025 report) vs final (2026 report)", f"{p23} -> {a23}", "%",
    "Commission, 2025 Country Report Table A8.1 (p. 69); 2026 Country Report Table A8.1 (p. 71)",
    f"revised up by {a23 - p23:.1f} points once the final inventory replaced the approximated one")
c23 = float(CF[("CAPR24", "Transport emissions change on 2022 (approximated)", "2023")]["value"])
add("2023 vs 2022 transport change: approximated (CAPR 2024 profile) vs inventory", f"{c23} / {pct(T[2023], T[2022]):.1f}", "%",
    "Commission CAPR 2024 country profile Malta, p. 6; " + ES)
gv_diff = max(abs(GV[("All", c, y)] - MT("GHG", k)[y]) for c, k in (("1.A.3", "CRF1A3"), ("1.A.3.b", "CRF1A3B"),
                                                                    ("1.A.3.d", "CRF1A3D")) for y in range(2005, 2025))
add("EEA GovReg 2026 v1.0 (15 Mar 2026) vs Eurostat (2 Jun 2026), Malta transport rows: largest difference",
    round(gv_diff * 1000, 3), "kt CO2e", "EEA GovReg 2026 v1.0 (doi:10.2909/83ee8f8c-1422-4e3f-af63-ba88146811e5); " + ES,
    "the inventory available to the Commission when it drafted the report is the one republished by Eurostat")
c3 = defaultdict(dict)
for r in csv.DictReader(open(ROOT / "data" / "cc-003" / "eurostat_ghg_population.csv")):
    c3[(r["geo"], r["item"])][int(r["year"])] = float(r["value"])
d3 = max(abs(c3[("MT", "CRF1A3")][y] - MT("GHG", "CRF1A3")[y]) for y in (2005, 2023, 2024))
add("Consistency with Claim Check 003: Malta CRF 1.A.3 (2005, 2023, 2024), largest difference", round(d3 * 1000, 3),
    "kt CO2e", "data/cc-003/eurostat_ghg_population.csv (retrieved 2 Oct 2026) vs " + ES,
    f"CC-003 gives domestic transport incl. aviation +{pct(c3[('MT', 'CRF1A3')][2024], c3[('MT', 'CRF1A3')][2005]):.1f}%")
esr3 = {r["series"] + r["year"]: r["value"] for r in csv.DictReader(open(ROOT / "data" / "cc-003" / "capr2025_esr_malta.csv"))}
add("Consistency with Claim Check 003: ESR emissions 2024 vs 2005 (CAPR 2025 Table 25)", esr3["Malta ESR emissions vs 20052024"],
    "%", "data/cc-003/capr2025_esr_malta.csv", "the 2026 Country Report gives 40.8%")
flags = sorted({f"{k[2]} {k[3]}: {v}" for k, v in EF.items() if k[0] == "MT" and k[2] in ("CRF1A3", "CRF1A3A", "CRF1A3B", "CRF1A3D")})
ghg_other = sum(len(MT("GHG", c)) for c in ("CRF1A3C", "CRF1A3E"))
co2_other = max(v for c in ("CRF1A3C", "CRF1A3E") for v in MT("CO2", c).values())
notes = sorted({r["notation"] for r in csv.DictReader(open(D / "eea_govreg_2026v1_mt.csv"))
                if r["sector_code"] in ("1.A.3.c", "1.A.3.e") and r["pollutant"] == "CO2"})
add("Eurostat flags on Malta transport rows used (1.A.3, 1.A.3.a, 1.A.3.b, 1.A.3.d), 2005-2024", "; ".join(flags) or "none",
    "", ES, f"rail (1.A.3.c) and other (1.A.3.e): {ghg_other} GHG values published, CO2 at most {co2_other}; "
    f"inventory notation for CO2 {', '.join(notes)} (NO = not occurring), so ESR transport is road plus navigation")

# ---------------------------------------------------------------- 5. EU-27 context
add("EU-27: ESR transport (1.A.3 - aviation CO2) change 2005-2024", round(pct(TEU[2024], TEU[2005]), 1), "%", ES,
    f"{TEU[2005]:.1f} -> {TEU[2024]:.1f} Mt; Table A8.1 gives -5.6% for 2023 (ours {pct(TEU[2023], TEU[2005]):.1f}%)")

with open(D / "checks.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["check", "value", "unit", "source", "note"])
    w.writeheader()
    w.writerows(rows)
for r in rows:
    print(f"{r['check'][:95]:95s} {r['value']} {r['unit']}  | {r['note'][:110]}")
