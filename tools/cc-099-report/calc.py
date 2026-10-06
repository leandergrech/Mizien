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
S_PWC = "PwC Malta press release, as published by The Malta Business Weekly, 19 Jul 2026"
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
for y in (2019, 2024, LAST):
    add(f"Born abroad, share, 1 January {y}", r2(born_abroad(y)), "%", S_CTB,
        f"{int(ctb[('FOR', y)]):,} of {int(ctb[('TOTAL', y)]):,}")
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
loc_req = P30 * (1 - SH30 / 100)
add("PwC base case for 2030", P30, "persons", S_PWC)
add("Local residents implied by 38% of 636,000", int(round(loc_req)), "persons", "calculated", "foreign: "
    f"{int(round(P30 * SH30 / 100)):,}")
add("Implied change in local residents from Maltese citizens on 1 January 2025", int(round(loc_req - nat[LAST])), "persons",
    "calculated from PwC and Eurostat")
yrs = 2030 - LAST + 1        # 1 Jan 2025 to end-2030 (= 1 Jan 2031): six years, the longest reading of 'by 2030'
need = (loc_req - nat[LAST]) / yrs
add("Required change in Maltese citizens a year, 2025-2030 (to end-2030)", int(round(need)), "persons a year",
    "calculated", f"{yrs} years from 1 January {LAST}; a 1 January 2030 horizon would need "
                  f"{int(round((loc_req - nat[LAST]) / (yrs - 1))):,} a year")
add("Ratio of non-Maltese to Maltese citizens, 1 January 2025", r1(100 * foreign(LAST) / nat[LAST]), "%", S_CTZ,
    "already above 38%, so 'mix of foreign to local' reaching 38% can only mean a share of all residents")
add("Share of all residents if 38% were a ratio of foreign to local", r1(100 * SH30 / (100 + SH30)), "%", "calculated",
    "below today's share: this reading would mean a fall, which the release does not describe")
add("Non-Maltese share at 636,000 with Maltese citizens at their 1 January 2025 count", r2(100 * (P30 - nat[LAST]) / P30),
    "%", "calculated (comparison, not a forecast)")
add("Born-abroad share at 636,000 with Malta-born residents at their 1 January 2025 count",
    r2(100 * (P30 - ctb[("NAT", LAST)]) / P30), "%", "calculated (comparison, not a forecast)",
    f"Malta-born {int(ctb[('NAT', LAST)]):,} on 1 January {LAST}")
for lab, P in (("low", "Population range for 2030 (low)"), ("high", "Population range for 2030 (high)")):
    v = int(pwc[P]["value"])
    add(f"◆ Non-Maltese share at PwC's {lab} total ({v:,}) with Maltese citizens at their 1 Jan 2025 count",
        r2(100 * (v - nat[LAST]) / v), "%", "calculated (◆ range as reported by Business Now and Newsbook)")

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
add("Residual (without naturalisations or migration), 2021-2024: range",
    f"{int(min(c[4] for c in comp))} to {int(max(c[4] for c in comp))}", "persons a year", "calculated from Eurostat",
    "close to births to Maltese mothers minus deaths of Maltese citizens ("
    f"{int(min(c[5] for c in comp))} to {int(max(c[5] for c in comp))})")
add("Acquisitions of Maltese citizenship, 2021-2024: range",
    f"{int(min(c[3] for c in comp))} to {int(max(c[3] for c in comp))}", "persons a year", S_FLOW)
add("Required fall (a year) vs the most negative residual 2021-2024", f"{int(round(need))} vs {int(min(c[4] for c in comp))}",
    "persons a year", "calculated", "38% at 636,000 needs a faster fall than even the residual alone")

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
