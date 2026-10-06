"""Figures for Claim Check 099, drawn from data/cc-099/ (run fetch.py and calc.py first)."""
import csv, pathlib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from matplotlib.lines import Line2D

HERE = pathlib.Path(__file__).resolve().parent
D = HERE.parents[1] / "data" / "cc-099"
OUT = HERE / "out"
OUT.mkdir(exist_ok=True)
for f in ["LiberationSans-Regular", "LiberationSans-Bold", "LiberationSans-Italic"]:
    fm.fontManager.addfont(f"/usr/share/fonts/truetype/liberation/{f}.ttf")
plt.rcParams.update({"font.family": "Liberation Sans", "axes.spines.top": False, "axes.spines.right": False,
                     "axes.edgecolor": "#8A9399", "axes.labelcolor": "#2B3A42", "xtick.color": "#2B3A42",
                     "ytick.color": "#2B3A42"})
GREEN, SAGE, AMBER, RED, SLATE, GREY, ORANGE, BLUE = ("#14452F", "#7FA88B", "#E3A72F", "#B5483A", "#2B3A42",
                                                      "#8A9399", "#D9772B", "#3C6E8F")


def load(f, dim):
    out = {}
    for r in csv.DictReader(open(D / f)):
        out[(r[dim], int(r["time"]))] = float(r["value"])
    return out


ctz = load("eurostat_migr_pop1ctz.csv", "citizen")
ctb = load("eurostat_migr_pop3ctb.csv", "c_birth")
flows = {}
for f in ("eurostat_migr_flows.csv", "eurostat_births_deaths_ctz.csv"):
    for r in csv.DictReader(open(D / f)):
        flows[(r["dataset"], r["citizen"], int(r["time"]))] = float(r["value"])
cens = {}
for r in csv.DictReader(open(D / "eurostat_census2021.csv")):
    cens[(r["dataset"], r["citizen"] or r["c_birth"])] = float(r["value"])
jp, jt = {}, {}
for r in csv.DictReader(open(D / "jobsplus_foreign_employment.csv")):
    jp[(r["group"], r["type"], int(r["year_end_dec"]))] = int(r["value"])
for r in csv.DictReader(open(D / "jobsplus_total_employment.csv")):
    jt[(r["series"], int(r["year_end_dec"]))] = int(r["value"])
pop26 = next(float(r["value"]) for r in csv.DictReader(open(D / "eurostat_demo_gind.csv"))
             if r["indic_de"] == "JAN" and r["time"] == "2026")
pwc = {r["item"]: r for r in csv.DictReader(open(D / "pwc_release.csv"))}
nso = {r["item"]: r for r in csv.DictReader(open(D / "nso_end2025_secondhand.csv"))}
Y = list(range(2010, 2026))
LAST = 2025


def fig1():
    fig, ax = plt.subplots(figsize=(9.6, 4.5), dpi=220)
    s_ctz = [100 * (ctz[("TOTAL", y)] - ctz[("NAT", y)]) / ctz[("TOTAL", y)] for y in Y]
    s_ctb = [100 * ctb[("FOR", y)] / ctb[("TOTAL", y)] for y in Y]
    jy = [y for y in range(2015, 2026) if ("Total employed (full- and part-time)", y) in jt]
    s_job = [100 * jp[("Grand Total", "Total", y)] / jt[("Total employed (full- and part-time)", y)] for y in jy]
    ax.plot(Y, s_ctb, color=BLUE, lw=2.0, ls="--", marker="o", ms=3.2, zorder=2)
    ax.plot([y + 11 / 12 for y in jy], s_job, color=GREY, lw=1.6, ls=":", marker="s", ms=3.0, zorder=2)
    ax.plot(Y, s_ctz, color=GREEN, lw=2.6, marker="o", ms=3.6, zorder=3)
    # Census 2021 (reference date 21 November 2021)
    cx = 2021 + 10.7 / 12
    ax.plot([cx], [100 * (cens[("cens_21ctz_r3", "TOTAL")] - cens[("cens_21ctz_r3", "NAT")]) /
                   cens[("cens_21ctz_r3", "TOTAL")]], marker="D", ms=5.5, color=GREEN, mfc="white", mew=1.4, zorder=4)
    ax.plot([cx], [100 * cens[("cens_21cob_r3", "FOR")] / cens[("cens_21cob_r3", "TOTAL")]], marker="D", ms=5.5,
            color=BLUE, mfc="white", mew=1.4, zorder=4)
    # 1 January 2026: first-hand bracket (Eurostat) and the NSO figure as reported (second-hand)
    nat = {y: ctz[("NAT", y)] for y in Y}
    d = [nat[y + 1] - nat[y] for y in range(2010, LAST)]
    lo = 100 * (pop26 - (nat[LAST] + max(d))) / pop26
    hi = 100 * (pop26 - (nat[LAST] + min(d))) / pop26
    ax.plot([2026, 2026], [lo, hi], color=GREEN, lw=9, solid_capstyle="butt", zorder=4)
    ax.text(2026.0, lo - 1.4, f"{lo:.1f}–{hi:.1f}%", color=GREEN, fontsize=8, ha="center", va="top",
            fontweight="bold")
    ax.plot([2026.45], [float(nso["Non-Maltese citizens' share"]["value"])], marker="o", ms=5.5, color=SLATE,
            mfc="white", mew=1.3, zorder=5)
    # the claim (31% at end-2025; 38% plotted at end-2030, the longest reading of "by 2030")
    ax.plot([2026.9], [31], marker="*", ms=13, color=AMBER, mec=SLATE, mew=0.6, zorder=6)
    ax.plot([2031], [38], marker="*", ms=13, color=AMBER, mec=SLATE, mew=0.6, zorder=6)
    ax.plot([2026.9, 2031], [31, 38], color=AMBER, lw=1.4, ls=(0, (4, 3)), zorder=1)
    ax.text(2031.2, 39.6, "PwC: “around 38%\nby 2030” (end-2030)", fontsize=8, color=SLATE, ha="right", va="bottom")
    ax.text(2027.3, 30.1, "PwC: 31% “now”", fontsize=8, color=SLATE, ha="left", va="top")
    ax.text(2016.2, s_ctz[Y.index(2017)] - 4.2, "Non-Maltese citizens", color=GREEN, fontsize=9, fontweight="bold")
    ax.text(2012.6, s_ctb[Y.index(2013)] + 2.4, "Born abroad", color=BLUE, fontsize=9, fontweight="bold")
    ax.text(2017.0, 31.5, "Foreign nationals’ share of\nregistered employment (Jobsplus)", color=GREY, fontsize=8)
    for y, s in ((2010, s_ctz[0]), (LAST, s_ctz[-1])):
        ax.text(y, s - 2.6 if y == 2010 else s - 3.2, f"{s:.1f}%", color=GREEN, fontsize=8, ha="center")
    ax.text(LAST, s_ctb[-1] + 1.3, f"{s_ctb[-1]:.1f}%", color=BLUE, fontsize=8, ha="center")
    ax.set_xlim(2009.5, 2031.6)
    ax.set_ylim(0, 45)
    ax.set_xticks(list(range(2010, 2032, 2)))
    ax.set_ylabel("% of residents (or of employment)")
    ax.legend(handles=[Line2D([], [], color=GREEN, lw=2.6, marker="o", ms=3.6, label="Non-Maltese citizens, 1 January"),
                       Line2D([], [], color=BLUE, lw=2.0, ls="--", marker="o", ms=3.2, label="Born abroad, 1 January"),
                       Line2D([], [], color=GREY, lw=1.6, ls=":", marker="s", ms=3, label="Employment share, December"),
                       Line2D([], [], color=GREEN, lw=0, marker="D", ms=5.5, mfc="white", mew=1.4, label="Census 2021"),
                       Line2D([], [], color=GREEN, lw=5, label="1 Jan 2026: range from Eurostat data"),
                       Line2D([], [], color=SLATE, lw=0, marker="o", ms=5.5, mfc="white", mew=1.3,
                              label="NSO end-2025, as reported (second-hand)"),
                       Line2D([], [], color=AMBER, lw=0, marker="*", ms=11, mec=SLATE, mew=0.6, label="PwC's figures")],
              frameon=False, fontsize=7.6, loc="upper left", ncol=2)
    ax.text(2009.6, -8.2, "Sources: Eurostat migr_pop1ctz, migr_pop3ctb, cens_21ctz_r3, cens_21cob_r3, demo_gind; Jobsplus "
            "(full- and part-time employment, December). All retrieved\n6 Oct 2026; no Eurostat flags on 2010–2025. The "
            "1 Jan 2026 range applies 2010–24's smallest and largest yearly change in Maltese citizens. NSO via news reports.",
            fontsize=6.8, color=GREY)
    fig.savefig(OUT / "fig1_shares.png", bbox_inches="tight", facecolor="white")


def fig2():
    fig, (a, b) = plt.subplots(1, 2, figsize=(9.6, 3.9), dpi=220, gridspec_kw={"width_ratios": [1.25, 1]})
    nat = {y: ctz[("NAT", y)] for y in Y}
    P30 = int(pwc["Population projected for 2030 (base case)"]["value"])
    SH = float(pwc["Mix of foreign to local residents by 2030"]["value"])
    req = P30 * (1 - SH / 100)
    a.plot(Y, [nat[y] / 1000 for y in Y], color=GREEN, lw=2.4, marker="o", ms=3.4)
    a.plot([LAST, 2031], [nat[LAST] / 1000, req / 1000], color=RED, lw=1.5, ls=(0, (4, 3)))
    a.plot([2031], [req / 1000], marker="o", ms=6, color=RED)
    a.text(2030.8, req / 1000 - 1.3, f"{req:,.0f} local residents:\n38% of 636,000 is foreign", color=RED,
           fontsize=7.6, ha="right", va="top")
    a.text(2010, nat[2010] / 1000 + 1.0, f"{nat[2010]:,.0f}", color=GREEN, fontsize=7.6, ha="center")
    a.text(LAST, nat[LAST] / 1000 + 1.0, f"{nat[LAST]:,.0f}", color=GREEN, fontsize=7.6, ha="center")
    a.set_ylim(385, 412)
    a.set_xlim(2009.3, 2031.8)
    a.set_xticks(list(range(2010, 2032, 4)))
    a.set_ylabel("Maltese citizens, thousands (1 January)")
    a.set_title("A. Maltese citizens rose every year", fontsize=9.5, color=SLATE, loc="left")
    yrs = list(range(2021, 2025))
    mig = [flows[("migr_imm1ctz", "NAT", y)] - flows[("migr_emi1ctz", "NAT", y)] for y in yrs]
    acq = [flows[("migr_acq", "TOTAL", y)] for y in yrs]
    tot = [nat[y + 1] - nat[y] for y in yrs]
    res = [t - m - q for t, m, q in zip(tot, mig, acq)]
    w = 0.6
    b.bar(yrs, acq, w, color=SAGE, label="Acquisitions of Maltese citizenship")
    b.bar(yrs, mig, w, bottom=acq, color=BLUE, label="Net migration of Maltese citizens")
    b.bar(yrs, res, w, color=GREY, label="Everything else (mainly\ndeaths exceeding births)")
    b.plot(yrs, tot, color=GREEN, marker="D", ms=5, lw=0, label="Total change", zorder=4)
    need = (req - nat[LAST]) / (2031 - LAST)
    b.axhline(need, color=RED, lw=1.5, ls=(0, (4, 3)))
    b.text(2020.55, need - 120, f"Needed for 38% at 636,000: {need:,.0f} a year".replace("-", "−"), color=RED, fontsize=7.6, va="top")
    b.axhline(0, color=SLATE, lw=0.6)
    b.set_ylim(-2600, 3700)
    b.set_xticks(yrs)
    b.set_ylabel("persons a year")
    b.set_title("B. What changed the count, 2021–2024", fontsize=9.5, color=SLATE, loc="left")
    b.legend(frameon=False, fontsize=6.7, loc="upper left", ncol=2, columnspacing=0.8, handlelength=1.4)
    fig.text(0.01, -0.06, "Sources: Eurostat migr_pop1ctz, migr_imm1ctz, migr_emi1ctz, migr_acq (retrieved 6 Oct 2026); PwC base "
             "case of 636,000 and 38% (press release, 19 Jul 2026). The dashed line in A runs\nfrom 1 Jan 2025 to end-2030 "
             "(the longest reading of “by 2030”). “Everything else” is the remainder after migration and acquisitions; "
             "births to Maltese mothers minus\ndeaths of Maltese citizens (Eurostat demo_faczc, demo_maczc) were "
             "−857 to −1,119 a year.", fontsize=6.8, color=GREY)
    fig.tight_layout()
    fig.savefig(OUT / "fig2_locals.png", bbox_inches="tight", facecolor="white")


fig1(); fig2()
print("figures in", OUT)
