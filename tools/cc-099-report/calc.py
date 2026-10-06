#!/usr/bin/env python3
"""CC-099: test PwC Malta's statement that foreign residents 'now make up 31% of Malta's population', with the mix of
foreign to local residents 'potentially reaching around 38% by 2030'.

Reads data/cc-099/ (Eurostat and Jobsplus files written by fetch.py on 6 Oct 2026, with Eurostat's flags; the PwC
release figures and the NSO end-2025 figures as reported by news outlets, both transcribed by hand with URLs).
Writes data/cc-099/checks.csv. Every input has a source; no rate is assumed.
"""
import csv, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[2]
D = ROOT / "data" / "cc-099"
rows = []
S_CTZ = "Eurostat migr_pop1ctz (1 January, by citizenship), retrieved 6 Oct 2026"
S_CTB = "Eurostat migr_pop3ctb (1 January, by country of birth), retrieved 6 Oct 2026"
S_GIND = "Eurostat demo_gind, retrieved 6 Oct 2026"
S_PROJ = "Eurostat proj_25np (EUROPOP2025), retrieved 6 Oct 2026"
S_CENS = "Eurostat cens_21ctz_r3 / cens_21cob_r3 (Census 2021), retrieved 6 Oct 2026"
S_FLOW = "Eurostat migr_imm1ctz, migr_emi1ctz, migr_acq, retrieved 6 Oct 2026"
S_JP = "Jobsplus workbooks (December of each year), retrieved 6 Oct 2026"
S_PWC = "PwC Malta press release, as posted by Finance Malta, 17 Jul 2026"
S_NSO = "◆ NSO World Population Day release (NR 120/2026, 9 Jul 2026) as reported by Newsbook, Lovin Malta, MEETinc"


def add(check, value, unit, source, note=""):
    rows.append({"check": check, "value": value, "unit": unit, "source": source, "note": note})


def load(f, dim, **flt):
    out, flags = {}, {}
    for r in csv.DictReader(open(D / f)):
        if all(r.get(k) == v for k, v in flt.items()):
            out[(r[dim], int(r["time"]))] = float(r["value"])
            flags[(r[dim], int(r["time"]))] = r.get("flag", "")
    return out, flags


ctz, ctzf = load("eurostat_migr_pop1ctz.csv", "citizen")
ctb, ctbf = load("eurostat_migr_pop3ctb.csv", "c_birth")
gind, gindf = load("eurostat_demo_gind.csv", "indic_de")
proj, _ = load("eurostat_proj_25np.csv", "projection")
flows = {}
for f in ("eurostat_migr_flows.csv", "eurostat_births_deaths_ctz.csv"):
    for r in csv.DictReader(open(D / f)):
        flows[(r["dataset"], r["citizen"], int(r["time"]))] = float(r["value"])
cens = {}
for r in csv.DictReader(open(D / "eurostat_census2021.csv")):
    cens[(r["dataset"], r["citizen"] or r["c_birth"])] = float(r["value"])
pwc = {r["item"]: r for r in csv.DictReader(open(D / "pwc_release.csv"))}
nso = {r["item"]: r for r in csv.DictReader(open(D / "nso_end2025_secondhand.csv"))}
jp = {}
for r in csv.DictReader(open(D / "jobsplus_foreign_employment.csv")):
    jp[(r["group"], r["type"], int(r["year_end_dec"]))] = int(r["value"])
jt = {}
for r in csv.DictReader(open(D / "jobsplus_total_employment.csv")):
    jt[(r["series"], int(r["year_end_dec"]))] = int(r["value"])

YEARS = range(2010, 2026)
LAST = max(y for (c, y) in ctz if c == "TOTAL")                       # latest year with a citizenship split
foreign = lambda y: ctz[("TOTAL", y)] - ctz[("NAT", y)]                # non-Maltese citizens incl. stateless
share = lambda y: 100 * foreign(y) / ctz[("TOTAL", y)]
born_abroad = lambda y: 100 * ctb[("FOR", y)] / ctb[("TOTAL", y)]
r1 = lambda x: round(x, 1)
r2 = lambda x: round(x, 2)

# ------------------------------------------------------------------ C: the population figure in the release
pop26 = gind[("JAN", 2026)]
add("Population on 1 January 2026 (= end of 2025)", int(pop26), "persons", S_GIND,
    "flag '" + gindf[("JAN", 2026)] + "'" if gindf[("JAN", 2026)] else "no Eurostat flag; PwC: 588,254 at year-end 2025")
add("Population change in 2025", int(gind[("GROW", 2025)]), "persons", S_GIND, "PwC: approximately 14,000")
add("Population change in 2025, % of 1 January 2025", r2(100 * gind[("GROW", 2025)] / gind[("JAN", 2025)]), "%", S_GIND,
    "PwC: 2.4%")
add("Net migration (plus statistical adjustment), 2025", int(gind[("CNMIGRAT", 2025)]), "persons", S_GIND)
add("Natural change, 2025", int(gind[("NATGROW", 2025)]), "persons", S_GIND)

# ------------------------------------------------------------------ A: 31% now
add("Latest year with Eurostat's split by citizenship (1 January)", LAST, "year", S_CTZ,
    "1 January 2026 not yet published by Eurostat")
for y in (2010, 2015, 2019, 2020, 2021, 2022, 2023, 2024, LAST):
    add(f"Non-Maltese citizens' share, 1 January {y}", r2(share(y)), "%", S_CTZ,
        f"{int(foreign(y)):,} of {int(ctz[('TOTAL', y)]):,}" + (" (flags " + ",".join(
            f for f in {ctzf[('TOTAL', y)], ctzf[('NAT', y)]} if f) + ")" if ctzf[("TOTAL", y)] or ctzf[("NAT", y)] else ""))
add(f"Of which other EU citizens, 1 January {LAST}", r2(100 * ctz[("EU27_2020_FOR", LAST)] / ctz[("TOTAL", LAST)]), "%",
    S_CTZ, f"{int(ctz[('EU27_2020_FOR', LAST)]):,}")
add(f"Of which non-EU citizens, 1 January {LAST}", r2(100 * ctz[("NEU27_2020_FOR", LAST)] / ctz[("TOTAL", LAST)]), "%",
    S_CTZ, f"{int(ctz[('NEU27_2020_FOR', LAST)]):,}")
add(f"Stateless, 1 January {LAST}", int(ctz.get(("STLS", LAST), 0)), "persons", S_CTZ)
add("Flags on the 2010-2025 citizenship series", ", ".join(
    f"{c} {y}:{ctzf[(c, y)]}" for (c, y) in sorted(ctzf) if y in YEARS and ctzf[(c, y)]) or "none", "flags", S_CTZ,
    "earlier years carry 'b' (2001, 2009 total) and 'e' (2006); not used")
for y in (2019, 2022, 2023, 2024, LAST):
    add(f"Born abroad, share, 1 January {y}", r2(born_abroad(y)), "%", S_CTB,
        f"{int(ctb[('FOR', y)]):,} of {int(ctb[('TOTAL', y)]):,}")
add("Malta-born residents, 1 January 2022 and 1 January 2023 (born-abroad series, level shift)",
    f"{int(ctb[('NAT', 2022)]):,} -> {int(ctb[('NAT', 2023)]):,}", "persons", S_CTB,
    f"{int(ctb[('NAT', 2023)] - ctb[('NAT', 2022)]):+,}; no Eurostat flag on either year (flags: "
    f"{ctbf[('NAT', 2022)] or 'none'}, {ctbf[('NAT', 2023)] or 'none'})")
add("Born abroad: 1 January 2022 share minus Census 2021 share (21 Nov 2021)",
    f"{r2(born_abroad(2022))} vs {r2(100 * cens[('cens_21cob_r3', 'FOR')] / cens[('cens_21cob_r3', 'TOTAL')])}", "%",
    S_CTB + "; " + S_CENS, "1 January 2022 is six weeks after the census date, yet its share is lower; we use only "
                           "the 2025 level of this series")
add("Census 2021: non-Maltese citizens (incl. stateless), share",
    r2(100 * (cens[("cens_21ctz_r3", "TOTAL")] - cens[("cens_21ctz_r3", "NAT")]) / cens[("cens_21ctz_r3", "TOTAL")]),
    "%", S_CENS, f"{int(cens[('cens_21ctz_r3', 'TOTAL')] - cens[('cens_21ctz_r3', 'NAT')]):,} of "
                 f"{int(cens[('cens_21ctz_r3', 'TOTAL')]):,}")
add("Census 2021: born abroad, share", r2(100 * cens[("cens_21cob_r3", "FOR")] / cens[("cens_21cob_r3", "TOTAL")]), "%",
    S_CENS)
add("Change in the share of non-Maltese citizens during 2024 (1 Jan 2024 to 1 Jan 2025)", r2(share(LAST) - share(LAST - 1)),
    "points", "calculated")
add("Change in the share of non-Maltese citizens during 2023", r2(share(LAST - 1) - share(LAST - 2)), "points", "calculated")

# Maltese citizens: every annual change on record, and what it means for 1 January 2026
nat = {y: ctz[("NAT", y)] for y in YEARS}
dnat = {y: nat[y + 1] - nat[y] for y in range(2010, LAST)}
add("Maltese citizens, 1 January 2010 and 1 January 2025", f"{int(nat[2010]):,} -> {int(nat[LAST]):,}", "persons", S_CTZ)
add("Annual change in Maltese citizens, 2010-2024: smallest", int(min(dnat.values())), "persons a year", S_CTZ,
    f"in {min(dnat, key=dnat.get)}")
add("Annual change in Maltese citizens, 2010-2024: largest", int(max(dnat.values())), "persons a year", S_CTZ,
    f"in {max(dnat, key=dnat.get)}")
add("Years 2010-2024 in which the number of Maltese citizens fell", sum(v < 0 for v in dnat.values()), "years", S_CTZ,
    f"of {len(dnat)}")
lo_nat, hi_nat = nat[LAST] + min(dnat.values()), nat[LAST] + max(dnat.values())
sh_hi = 100 * (pop26 - lo_nat) / pop26
sh_lo = 100 * (pop26 - hi_nat) / pop26
add("Non-Maltese share on 1 January 2026 if 2025's change in Maltese citizens lay within the 2010-2024 range",
    f"{sh_lo:.1f}-{sh_hi:.1f}", "%", "calculated from Eurostat (first-hand)",
    f"total {int(pop26):,}; Maltese citizens {int(lo_nat):,}-{int(hi_nat):,}; PwC: 31%")
nso_for = int(nso["Non-Maltese citizens"]["value"])
add("NSO: non-Maltese citizens at end-2025", nso_for, "persons", S_NSO, "second-hand")
add("NSO: share", r2(100 * nso_for / pop26), "%", S_NSO, "reported as 31.1%")
add("Maltese citizens implied by the NSO figures, end-2025", int(pop26 - nso_for), "persons", "calculated (◆ NSO via outlets)")
add("Implied change in Maltese citizens during 2025", int(pop26 - nso_for - nat[LAST]), "persons", "calculated (◆)",
    "within the 2010-2024 range of annual changes")

# workforce (a different measure)
for y in (2019, 2025):
    fn = jp[("Grand Total", "Total", y)]
    te = jt[("Total employed (full- and part-time)", y)]
    add(f"Jobsplus: employed foreign nationals, December {y}", fn, "persons", S_JP)
    add(f"Jobsplus: foreign nationals' share of total employment, December {y}", r1(100 * fn / te), "%", S_JP,
        f"{fn:,} of {te:,} (full- and part-time)")
ft25 = sum(jp[(g, "Full-time", 2025)] for g in ("EU National", "EEA & EFTA", "EU Dependent", "Third Country National"))
add("Jobsplus: foreign nationals' share of full-time employment, December 2025",
    r1(100 * ft25 / jt[("Gainfully employed (full-time)", 2025)]), "%", S_JP,
    f"{ft25:,} of {jt[('Gainfully employed (full-time)', 2025)]:,}")
add("Jobsplus: third-country nationals' share of employed foreign nationals, December 2025",
    r1(100 * jp[("Third Country National", "Total", 2025)] / jp[("Grand Total", "Total", 2025)]), "%", S_JP)

# ------------------------------------------------------------------ B: 38% by 2030
P30 = int(pwc["Population projected for 2030 (base case)"]["value"])
SH30 = float(pwc["Mix of foreign to local residents by 2030"]["value"])
BAND = (37.5, 38.0, 38.5)    # "around 38%": the values that round to 38, the same tolerance used for every reading
loc = {s: P30 * (1 - s / 100) for s in BAND}
add("PwC base case for 2030", P30, "persons", S_PWC)
for s in BAND:
    add(f"Local residents left by {s}% of 636,000", int(round(loc[s])), "persons", "calculated",
        f"foreign: {int(round(P30 * s / 100)):,}")
# start points: our end-2025 range (first-hand bound from section A) and, for comparison, 1 January 2025
add("Start: Maltese citizens on 1 January 2026 (our calculation from Eurostat, 2010-24 range of yearly changes)",
    f"{int(lo_nat):,}-{int(hi_nat):,}", "persons", "calculated from Eurostat")
for s in BAND:
    lo_need = (loc[s] - lo_nat) / 5     # 1 Jan 2026 to end-2030 (= 1 Jan 2031): five years
    hi_need = (loc[s] - hi_nat) / 5
    add(f"Change in Maltese citizens a year needed for {s}%, 2026-2030 (from our end-2025 range)",
        f"{int(round(lo_need)):,} to {int(round(hi_need)):,}", "persons a year", "calculated",
        "smaller fall from the lower start (405,549)")
    add(f"Change a year needed for {s}%, counted from 1 January 2025 over six years (spreads the fall over 2025, when "
        "the count rose)", int(round((loc[s] - nat[LAST]) / 6)), "persons a year", "calculated (comparison)")
    add(f"Change a year needed for {s}%, from the NSO-implied end-2025 count", int(round((loc[s] - (pop26 - nso_for)) / 5)),
        "persons a year", "calculated (◆ NSO via outlets)")
NEED_MIN = (loc[37.5] - lo_nat) / 5
add("Smallest yearly fall needed for 'around 38%' (37.5%, from the lower end-2025 start)", int(round(NEED_MIN)),
    "persons a year", "calculated", "the figure used in the report's text")
add("Ratio of non-Maltese to Maltese citizens, 1 January 2025", r1(100 * foreign(LAST) / nat[LAST]), "%", S_CTZ,
    "already above 38%, so 'mix of foreign to local' reaching 38% can only mean a share of all residents")
add("Share of all residents if 38% were a ratio of foreign to local", r1(100 * SH30 / (100 + SH30)), "%", "calculated",
    "below today's share: this reading would mean a fall, which the release does not describe")
add("Non-Maltese share at 636,000 with Maltese citizens at their 1 January 2025 count", r2(100 * (P30 - nat[LAST]) / P30),
    "%", "calculated (comparison, not a forecast)")
add("Non-Maltese share at 636,000 with Maltese citizens at our end-2025 range",
    f"{100 * (P30 - hi_nat) / P30:.1f}-{100 * (P30 - lo_nat) / P30:.1f}", "%", "calculated (comparison, not a forecast)")
mb = ctb[("NAT", LAST)]
add("Born-abroad share at 636,000 with Malta-born residents at their 1 January 2025 count",
    r2(100 * (P30 - mb) / P30), "%", "calculated (comparison, not a forecast)", f"Malta-born {int(mb):,} on 1 January {LAST}")
add("Change in Malta-born residents to 2030 for a 37.5-38.5% born-abroad share at 636,000",
    f"{int(round(loc[38.5] - mb)):+,} to {int(round(loc[37.5] - mb)):+,}", "persons", "calculated (comparison)")
for lab, P in (("low", "Population range for 2030 (low)"), ("high", "Population range for 2030 (high)")):
    v = int(pwc[P]["value"])
    add(f"◆ Non-Maltese share at PwC's {lab} total ({v:,}) with Maltese citizens at their 1 Jan 2025 count",
        r2(100 * (v - nat[LAST]) / v), "%", "calculated (◆ range as reported by Business Now and Newsbook)")

# clues to PwC's definition (second-hand wording; decide nothing)
add("Clue: non-Maltese citizens vs born abroad, 1 January 2019", f"{share(2019):.2f} vs {born_abroad(2019):.2f}", "%",
    S_CTZ + "; " + S_CTB, "◆ Business Now: 'In 2019, it was 20 per cent' (outlet's paraphrase of the report)")
add("Clue: born abroad, 1 January 2024", r2(born_abroad(2024)), "%", S_CTB, "31% also matches this")
add("Clue: Maltese citizens vs Malta-born residents, 1 January 2025", f"{int(nat[LAST]):,} vs {int(mb):,}", "persons",
    S_CTZ + "; " + S_CTB, "◆ Business Now: local population 'has remained at just over 400,000' (outlet's paraphrase)")

# components of the change in Maltese citizens, 2021-2024 (all four first-hand)
comp = []
for y in range(2021, LAST):
    imm = flows[("migr_imm1ctz", "NAT", y)]
    emi = flows[("migr_emi1ctz", "NAT", y)]
    acq = flows[("migr_acq", "TOTAL", y)]
    resid = dnat[y] - (imm - emi) - acq
    nat_bd = flows[("demo_faczc", "NAT", y)] - flows[("demo_maczc", "NAT", y)]
    comp.append((y, dnat[y], imm - emi, acq, resid, nat_bd))
    add(f"Maltese citizens, components of change {y}", f"{int(dnat[y])} = {int(imm - emi)} + {int(acq)} + {int(resid)}",
        "persons", S_FLOW, "total change = net migration of Maltese citizens + acquisitions of Maltese citizenship + "
                           "residual (everything else: births minus deaths, losses of citizenship, statistical adjustment)")
    add(f"Births to Maltese mothers minus deaths of Maltese citizens, {y}", int(nat_bd), "persons",
        "Eurostat demo_faczc, demo_maczc, retrieved 6 Oct 2026",
        f"{int(flows[('demo_faczc', 'NAT', y)]):,} births, {int(flows[('demo_maczc', 'NAT', y)]):,} deaths; "
        "approximate (a child's citizenship can differ from the mother's)")
R_MIN = min(c[4] for c in comp)
add("Residual (without naturalisations or migration), 2021-2024: range",
    f"{int(R_MIN)} to {int(max(c[4] for c in comp))}", "persons a year", "calculated from Eurostat",
    "close to births to Maltese mothers minus deaths of Maltese citizens ("
    f"{int(min(c[5] for c in comp))} to {int(max(c[5] for c in comp))})")
add("Acquisitions of Maltese citizenship, 2021-2024: range",
    f"{int(min(c[3] for c in comp))} to {int(max(c[3] for c in comp))}", "persons a year", S_FLOW)
add("Smallest fall needed (37.5%) vs the most negative residual 2021-2024", f"{int(round(NEED_MIN))} vs {int(R_MIN)}",
    "persons a year", "calculated", "even the residual alone falls more slowly than needed")
# comparison only: 2024's residual (the largest fall) repeated, i.e. no naturalisations and no Maltese migration
for start, lab, n in ((nat[LAST], "from 1 January 2025, six years", 6), (lo_nat, "from 405,549 (end-2025), five years", 5),
                      (hi_nat, "from 406,706 (end-2025), five years", 5)):
    end = start + n * R_MIN
    add(f"Comparison: 2024's residual ({int(R_MIN)}) repeated {lab}: non-Maltese share at 636,000",
        r2(100 * (P30 - end) / P30), "%", "calculated (comparison, not a forecast)", f"Maltese citizens {int(end):,}")

# the Central Bank of Malta's baseline (second-hand; no naturalisations)
cbm = list(csv.DictReader(open(D / "cbm_secondhand.csv")))
c0 = float(cbm[0]["value"])
for r in cbm[1:]:
    v = float(r["value"])
    for yrs_ in (26, 27):
        add(f"◆ CBM baseline native population {int(c0):,} -> {int(v):,} by 2050: average change over {yrs_} years",
            int(round((v - c0) / yrs_)), "persons a year", "calculated (◆ " + r["outlet"] + ")",
            "path to 2030 unknown; decides nothing")
for r in cbm[1:]:
    v = float(r["value"])
    for yrs_ in (26, 27):
        rate = (v - c0) / yrs_
        end = lo_nat + 5 * rate
        add(f"◆ Comparison: CBM average ({int(round(rate))}) applied 2026-30 from 405,549: non-Maltese share at 636,000",
            r2(100 * (P30 - end) / P30), "%", "calculated (comparison, ◆)")

# EUROPOP2025 (Eurostat): totals only, no split by citizenship
for t in ("BSL", "HMIGR", "LMIGR", "NMIGR"):
    add(f"EUROPOP2025 {t}: population 1 January 2030 / 1 January 2031", f"{int(proj[(t, 2030)]):,} / {int(proj[(t, 2031)]):,}",
        "persons", S_PROJ)
add("EUROPOP2025 baseline for 1 January 2026 vs actual", f"{int(proj[('BSL', 2026)]):,} vs {int(pop26):,}", "persons",
    S_PROJ + "; " + S_GIND, f"actual higher by {int(pop26 - proj[('BSL', 2026)]):,}")
add("Dimensions of EUROPOP2025 national projections", "age, sex, type of projection", "", S_PROJ,
    "no citizenship or country-of-birth split")

with open(D / "checks.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
for r in rows:
    print(f"{r['check'][:96]:96s} {str(r['value']):>24} {r['unit']}  {r['note']}")
