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
    # all three refer to the end of 2025 (= 1 January 2026); offset by +/-0.3 year only so they stay legible
    ax.plot([2025.6, 2025.6], [lo, hi], color=GREEN, lw=9, solid_capstyle="butt", zorder=4)
    ax.text(2026.7, 28.2, f"our range {lo:.1f}–{hi:.1f}%", color=GREEN, fontsize=8, ha="left", va="top",
            fontweight="bold")
    ax.plot([2026.4], [float(nso["Non-Maltese citizens' share"]["value"])], marker="o", ms=5.5, color=SLATE,
            mfc="white", mew=1.3, zorder=5)
    # the claim: 31% at the end of 2025; 38% plotted at the end of 2030 (the longest reading of "by 2030")
    ax.plot([2026], [31], marker="*", ms=13, color=AMBER, mec=SLATE, mew=0.6, zorder=6)
    ax.plot([2031], [38], marker="*", ms=13, color=AMBER, mec=SLATE, mew=0.6, zorder=6)
    ax.text(2031.2, 39.6, "PwC: “around 38%\nby 2030” (end-2030)", fontsize=8, color=SLATE, ha="right", va="bottom")
    ax.text(2026.7, 32.2, "PwC: 31% “now” (end-2025)", fontsize=8, color=SLATE, ha="left", va="bottom")
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
                       Line2D([], [], color=GREEN, lw=5, label="1 Jan 2026: our range from Eurostat data"),
                       Line2D([], [], color=SLATE, lw=0, marker="o", ms=5.5, mfc="white", mew=1.3,
                              label="NSO end-2025, as reported (second-hand)"),
                       Line2D([], [], color=AMBER, lw=0, marker="*", ms=11, mec=SLATE, mew=0.6, label="PwC's figures")],
              frameon=False, fontsize=7.6, loc="upper left", ncol=2)
    ax.text(2009.6, -9.4, "Sources: Eurostat migr_pop1ctz, migr_pop3ctb, cens_21ctz_r3, cens_21cob_r3, demo_gind; Jobsplus "
            "(registered employment, December). All retrieved 6 Oct 2026. Eurostat flags none of the 2010–2025\nvalues, but the "
            "born-abroad series shifts between 2022 and 2023 (Malta-born residents 397,432 to 388,690), and its 1 Jan 2022 share "
            "(23.6%) is below Census 2021 (25.7%). The 1 Jan 2026 range is\nour calculation (2010–24’s smallest and largest "
            "yearly change in Maltese citizens applied to 2025). NSO figure via news reports. The three markers at 1 Jan 2026 "
            "(end-2025) are\noffset sideways by up to 0.4 years so that they stay legible; the amber star is at 2026.",
            fontsize=6.8, color=GREY)
    fig.savefig(OUT / "fig1_shares.png", bbox_inches="tight", facecolor="white")


def fig2():
    fig, (a, b) = plt.subplots(1, 2, figsize=(9.6, 4.1), dpi=220, gridspec_kw={"width_ratios": [1.25, 1]})
    nat = {y: ctz[("NAT", y)] for y in Y}
    P30 = int(pwc["Population projected for 2030 (base case)"]["value"])
    band = [P30 * (1 - s / 100) for s in (37.5, 38.5)]          # "around 38%": 37.5-38.5%
    d = [nat[y + 1] - nat[y] for y in range(2010, LAST)]
    s_lo, s_hi = nat[LAST] + min(d), nat[LAST] + max(d)          # our 1 January 2026 range
    a.plot(Y, [nat[y] / 1000 for y in Y], color=GREEN, lw=2.4, marker="o", ms=3.4)
    a.plot([2026, 2026], [s_lo / 1000, s_hi / 1000], color=GREEN, lw=6, solid_capstyle="butt")
    a.fill_between([2026, 2031], [s_lo / 1000, band[0] / 1000], [s_lo / 1000, band[1] / 1000], color=RED, alpha=0.12, lw=0)
    a.plot([2026, 2031], [s_lo / 1000, band[0] / 1000], color=RED, lw=1.2, ls=(0, (4, 3)))
    a.plot([2026, 2031], [s_lo / 1000, band[1] / 1000], color=RED, lw=1.2, ls=(0, (4, 3)))
    a.plot([2031, 2031], [band[1] / 1000, band[0] / 1000], color=RED, lw=6, solid_capstyle="butt")
    a.text(2030.7, band[1] / 1000 - 0.8, f"{band[1]:,.0f}–{band[0]:,.0f} local residents:\n37.5–38.5% of 636,000 foreign",
           color=RED, fontsize=7.4, ha="right", va="top")
    a.text(2010.3, nat[2010] / 1000 - 1.2, f"{nat[2010]:,.0f}", color=GREEN, fontsize=7.4, ha="left", va="top")
    a.text(LAST - 0.3, nat[LAST] / 1000 + 1.2, f"{nat[LAST]:,.0f}", color=GREEN, fontsize=7.4, ha="center")
    a.set_ylim(385, 412)
    a.set_xlim(2009.3, 2031.8)
    a.set_xticks(list(range(2010, 2032, 4)))
    a.set_ylabel("Maltese citizens, thousands (1 January)")
    a.set_title("A. Maltese citizens rose every year 2010–2024", fontsize=9.5, color=SLATE, loc="left")
    yrs = list(range(2021, 2025))
    mig = [flows[("migr_imm1ctz", "NAT", y)] - flows[("migr_emi1ctz", "NAT", y)] for y in yrs]
    acq = [flows[("migr_acq", "TOTAL", y)] for y in yrs]
    tot = [nat[y + 1] - nat[y] for y in yrs]
    res = [t_ - m - q for t_, m, q in zip(tot, mig, acq)]
    w = 0.6
    b.bar(yrs, acq, w, color=SAGE, label="Acquisitions of Maltese citizenship")
    b.bar(yrs, mig, w, bottom=acq, color=BLUE, label="Net migration of Maltese citizens")
    b.bar(yrs, res, w, color=GREY, label="Everything else (mainly\ndeaths exceeding births)")
    b.plot(yrs, tot, color=GREEN, marker="D", ms=5, lw=0, label="Total change", zorder=4)
    need = [(x - s_lo) / 5 for x in band]                        # 2026-2030, from the lower end-2025 start
    b.axhspan(need[1], need[0], color=RED, alpha=0.13, lw=0)
    b.axhline(need[0], color=RED, lw=1.2, ls=(0, (4, 3)))
    b.text(2020.55, need[1] - 90, f"Needed a year in 2026–30 for 37.5–38.5% of 636,000:\n{need[0]:,.0f} to "
           f"{need[1]:,.0f}".replace("-", "−"), color=RED, fontsize=7.2, va="top")
    b.axhline(0, color=SLATE, lw=0.6)
    b.set_ylim(-3700, 3700)
    b.set_xticks(yrs)
    b.set_ylabel("persons a year")
    b.set_title("B. What changed the count, 2021–2024", fontsize=9.5, color=SLATE, loc="left")
    b.legend(frameon=False, fontsize=6.7, loc="upper left", ncol=2, columnspacing=0.8, handlelength=1.4)
    fig.text(0.01, -0.07, "Sources: Eurostat migr_pop1ctz, migr_imm1ctz, migr_emi1ctz, migr_acq (retrieved 6 Oct 2026); PwC base "
             "case of 636,000 and “around 38%” (press release, 17 Jul 2026),\ntaken as 37.5–38.5%. The shaded paths in A run "
             "from the lower end of our 1 Jan 2026 range (405,549) to the end of 2030. “Everything else” is the remainder after\n"
             "migration and acquisitions; births to Maltese mothers minus deaths of Maltese citizens (Eurostat demo_faczc, "
             "demo_maczc) were −857 to −1,119 a year.", fontsize=6.8, color=GREY)
    fig.tight_layout()
    fig.savefig(OUT / "fig2_locals.png", bbox_inches="tight", facecolor="white")


fig1(); fig2()
print("figures in", OUT)
