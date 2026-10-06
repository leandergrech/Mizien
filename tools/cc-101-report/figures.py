"""Figures for Claim Check 101, drawn from data/cc-101/ (run fetch.py and calc.py first)."""
import csv
import pathlib

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from matplotlib.patches import Patch

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[1]
D = ROOT / "data" / "cc-101"
OUT = HERE / "out"
OUT.mkdir(exist_ok=True)
for f in ["LiberationSans-Regular", "LiberationSans-Bold", "LiberationSans-Italic"]:
    fm.fontManager.addfont(f"/usr/share/fonts/truetype/liberation/{f}.ttf")
plt.rcParams.update({"font.family": "Liberation Sans", "axes.spines.top": False, "axes.spines.right": False,
                     "axes.edgecolor": "#8A9399", "axes.labelcolor": "#2B3A42", "xtick.color": "#2B3A42",
                     "ytick.color": "#2B3A42"})
GREEN, SAGE, AMBER, RED, SLATE, GREY, BLUE, PALE = ("#14452F", "#7FA88B", "#E3A72F", "#B5483A", "#2B3A42",
                                                    "#8A9399", "#3C6E8F", "#E6EFE8")
E = {(r["wat_src"], r["wat_proc"], int(r["year"])): (float(r["value"]), r["flag"])
     for r in csv.DictReader(open(D / "eurostat_env_wat_abs.csv"))}
PR = list(csv.DictReader(open(D / "wise_2022_significant_pressures.csv")))
ST = list(csv.DictReader(open(D / "wise_2022_groundwater_status.csv")))


def fig1():
    """(a) Where Malta's fresh water was abstracted from in 2024; (b) water bodies reporting abstraction pressure."""
    fig, (ax, bx) = plt.subplots(1, 2, figsize=(9.6, 3.5), dpi=220, gridspec_kw={"width_ratios": [1.35, 1]})
    y = 2024
    gw = {k: E[("FGW", k, y)][0] for k in ("ABST", "ABS_PWS", "ABS_AGR")}
    sw = {k: E[("FSW", k, y)][0] for k in ("ABST", "ABS_AGR", "ABS_HH")}
    gw_other = gw["ABST"] - gw["ABS_PWS"] - gw["ABS_AGR"]
    sw_other = sw["ABST"] - sw["ABS_AGR"]
    cats = [("Agriculture", GREEN), ("Public water supply (taken as WSC)", BLUE), ("Households, industry, services", AMBER)]
    bars = {"Groundwater": [gw["ABS_AGR"], gw["ABS_PWS"], gw_other], "Surface water": [sw["ABS_AGR"], 0, sw_other]}
    for i, (lab, vals) in enumerate(bars.items()):
        left = 0
        for (cname, col), v in zip(cats, vals):
            if v <= 0:
                continue
            ax.barh(i, v - 0.15, left=left, height=0.5, color=col, edgecolor="white", linewidth=0)
            if v > 4:
                ax.text(left + v / 2, i, f"{v:.1f}", ha="center", va="center", color="white", fontsize=8.5,
                        fontweight="bold")
            left += v
        tot = sum(vals)
        ax.text(tot + 0.6, i, f"{tot:.2f} million m³", va="center", fontsize=8.5, color=SLATE, fontweight="bold")
    ax.set_yticks([0, 1], list(bars))
    ax.invert_yaxis()
    ax.set_xlim(0, 50)
    ax.set_xlabel("million m³ abstracted in 2024", fontsize=8)
    ax.tick_params(labelsize=8)
    ax.spines["left"].set_visible(False)
    ax.tick_params(axis="y", length=0)
    ax.grid(axis="x", color="#E3E6E8", lw=0.6)
    ax.set_axisbelow(True)
    ax.legend(handles=[Patch(color=c, label=n) for n, c in cats], frameon=False, fontsize=7.6, loc="lower right",
              bbox_to_anchor=(1.0, -0.02))
    ax.set_title("(a) Fresh water abstracted in Malta, 2024", fontsize=9.5, loc="left", color=SLATE, fontweight="bold")

    gwp = [r for r in PR if r["water"] == "ground"]
    fresh = [r for r in PR if r["water"] == "surface" and r["category"] in ("RW", "LW")]
    rows = [("Groundwater bodies:\nabstraction a significant pressure",
             sum("P3" in r["significant_pressures"] for r in gwp), len(gwp), AMBER),
            ("Groundwater bodies:\npoor quantitative status", sum(r["quantitative_status"] == "Poor" for r in ST),
             len(ST), RED),
            ("Watercourses and pools:\nabstraction a significant pressure",
             sum("P3" in r["significant_pressures"] for r in fresh), len(fresh), AMBER)]
    for i, (lab, n, tot, col) in enumerate(rows):
        for k in range(tot):
            bx.add_patch(plt.Rectangle((k * 1.0, i - 0.22), 0.82, 0.44, color=col if k < n else "#E3E6E8", lw=0))
        bx.text(15.6, i, f"{n} of {tot}", va="center", fontsize=8.5, color=SLATE, fontweight="bold")
    bx.set_yticks(range(len(rows)), [r[0] for r in rows], fontsize=7.8)
    bx.set_xlim(-0.3, 18.5)
    bx.set_ylim(len(rows) - 0.5, -0.6)
    bx.set_xticks([])
    for s in ("left", "bottom"):
        bx.spines[s].set_visible(False)
    bx.tick_params(axis="y", length=0)
    bx.set_title("(b) Malta's WFD water bodies, 2022 reporting", fontsize=9.5, loc="left", color=SLATE,
                 fontweight="bold")
    fig.text(0.01, -0.09, "Sources: Eurostat env_wat_abs (updated 16 Sep 2026; the 2024 values are estimates, flag e), EEA WISE "
             "WFD 2022 reporting (significant pressures; quantitative status assessed 2021), retrieved 6 Oct 2026.\n"
             "One square per water body. Watercourses and pools: Malta's three river water bodies (3.4 km in all) and "
             "two lake water bodies; coastal and transitional waters are not shown.\n"
             "\"Public water supply\" is Eurostat's category; taking it to be WSC (Water Services Corporation) is our identification.", fontsize=6.8, color=GREY)
    fig.tight_layout(w_pad=2.5)
    fig.savefig(OUT / "fig1_abstraction.png", bbox_inches="tight", facecolor="white")


EVENTS = [  # (year as decimal, "EU" or "Malta", label); one row each, in date order
    (1997.67, "Malta", "Groundwater sources registered with WSC (1997 rules)"),
    (2000.97, "EU", "Directive in force; Art. 11(3)(e): registers, authorisation, review"),
    (2003.97, "EU", "Deadline to transpose the Directive"),
    (2004.5, "Malta", "Water Policy Framework Regulations (L.N. 194 of 2004)"),
    (2008.77, "Malta", "Sources to be notified by 20 Nov 2008; drilling moratorium"),
    (2010.32, "Malta", "Groundwater Abstraction (Metering) Regulations"),
    (2012.97, "EU", "Deadline for all measures to be operational"),
    (2015.81, "Malta", "S.L. 549.100 re-made; repeats the words of Art. 11(3)(e)"),
    (2019.15, "EU", "Commission review of 2nd plan: “authorisation and/or permitting regime”"),
    (2023.9, "Malta", "Green Paper proposes abstraction permits for fixed terms"),
    (2024.2, "Malta", "3rd plan: Measure 053, abstraction licensing framework"),
    (2025.09, "EU", "Commission report: Malta’s 3rd plan not assessed (late)"),
    (2025.3, "Malta", "Interim report: framework “close to being finalised”"),
    (2026.52, "EU", "Letter of formal notice INFR(2026)2115"),
    (2026.76, "Malta", "6 Oct 2026: no abstraction permit found in the laws searched"),
]


def fig2():
    n = len(EVENTS)
    fig, ax = plt.subplots(figsize=(7.8, 3.7), dpi=260)
    fig.subplots_adjust(left=0.545, right=0.985, top=0.92, bottom=0.17)
    for yr in range(1996, 2028, 2):
        ax.axvline(yr, color="#EEF0F1", lw=0.6, zorder=0)
    for i, (yr, who, lab) in enumerate(EVENTS):
        col = BLUE if who == "EU" else GREEN
        ax.plot([1996, yr], [i, i], color="#D5DBD7", lw=0.6, zorder=1)
        ax.plot([yr], [i], marker="o", ms=6.5, color=col, mec="white", mew=1.2, zorder=3)
        ax.text(-0.012, i, lab, transform=ax.get_yaxis_transform(), ha="right", va="center", fontsize=7.6,
                color=SLATE)
    ax.set_ylim(n - 0.4, -0.8)
    ax.set_xlim(1996, 2027.4)
    ax.set_yticks([])
    ax.set_xticks(range(1996, 2028, 4))
    ax.tick_params(axis="x", labelsize=7.5)
    ax.spines["left"].set_visible(False)
    ax.legend(handles=[plt.Line2D([], [], marker="o", lw=0, ms=6.5, color=BLUE, mec="white", label="European Union"),
                       plt.Line2D([], [], marker="o", lw=0, ms=6.5, color=GREEN, mec="white", label="Malta")],
              frameon=False, fontsize=7.6, ncol=2, loc="lower right", bbox_to_anchor=(1.0, 1.0))
    fig.text(0.01, 0.0, "Sources: Directive 2000/60/EC; S.L. 549.100, 549.164–549.166 (legislation.mt); SWD(2019) 48; "
             "COM(2025) 2; Green Paper (Nov 2023);\n2nd and 3rd plans; Malta's interim report (Apr 2025); INF/26/1376. "
             "Points sit at the month of publication or entry into force\n(mid-year where only the year is known). "
             "Legal Notices and Acts of 2024–2026 and related S.L. titles on legislation.mt searched on 6 Oct 2026.", fontsize=6.8, color=GREY)
    fig.savefig(OUT / "fig2_timeline.png", bbox_inches="tight", facecolor="white")


fig1()
fig2()
print("figures in", OUT)
