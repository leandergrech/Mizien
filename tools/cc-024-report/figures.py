"""Figures for Claim Check 024, drawn from data/cc-024/ (run calc.py first)."""
import csv, pathlib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[1]
D = ROOT / "data" / "cc-024"
OUT = HERE / "out"
OUT.mkdir(exist_ok=True)
for f in ["LiberationSans-Regular", "LiberationSans-Bold", "LiberationSans-Italic"]:
    fm.fontManager.addfont(f"/usr/share/fonts/truetype/liberation/{f}.ttf")
plt.rcParams.update({"font.family": "Liberation Sans", "axes.spines.top": False, "axes.spines.right": False,
                     "axes.edgecolor": "#8A9399", "axes.labelcolor": "#2B3A42", "xtick.color": "#2B3A42",
                     "ytick.color": "#2B3A42"})
GREEN, SAGE, AMBER, RED, SLATE, GREY, ORANGE, BLUE = ("#14452F", "#7FA88B", "#E3A72F", "#B5483A", "#2B3A42",
                                                      "#8A9399", "#D9772B", "#3C6E8F")
eu, flag = {}, {}
for r in csv.DictReader(open(D / "eurostat_nrg_ind_ren.csv")):
    eu[(r["geo"], r["item"], int(r["year"]))] = float(r["value"])
    flag[(r["geo"], r["item"], int(r["year"]))] = r["flag"]
plan = {int(r["key"]): float(r["value"]) for r in csv.DictReader(open(D / "necp_commission_inputs.csv"))
        if r["series"] == "plan_indicative_RES_target"}


def fig_path():
    yrs = list(range(2013, 2026))
    fig, ax = plt.subplots(figsize=(9.6, 4.6), dpi=220)
    ax.plot(yrs[:-1], [eu[("MT", "REN", y)] for y in yrs[:-1]], color=GREEN, lw=2.8, label="Malta, Eurostat")
    ax.plot(yrs[-2:], [eu[("MT", "REN", y)] for y in yrs[-2:]], color=GREEN, lw=2.8, ls=":")
    ax.plot(2025, eu[("MT", "REN", 2025)], "o", color="white", mec=GREEN, mew=2, ms=7)
    ax.plot(list(plan), list(plan.values()), color=AMBER, lw=2.4, marker="s", ms=4, label="Plan's indicative target (Table 3)")
    ax.plot(yrs, [eu[("EU27_2020", "REN", y)] for y in yrs], color=BLUE, lw=1.6, ls="--", label="EU-27, Eurostat")
    ax.plot(yrs, [eu[("CY", "REN", y)] for y in yrs], color=GREY, lw=1.6, label="Cyprus, Eurostat")
    ax.plot([2025, 2027], [18, 22], "D", color=RED, ms=6, label="Commission reference points (EU 42.5% target)")
    ax.plot(2030, 28, "D", color=RED, ms=7)
    ax.annotate("28%: Commission's formula result", (2030, 28), (2026.1, 29.2), fontsize=8, color=RED,
                arrowprops=dict(arrowstyle="-", color=RED, lw=0.7))
    ax.annotate("24.5%: the plan", (2030, 24.5), (2027.6, 21.2 - 6.5), fontsize=8.5, color="#8a5d00", fontweight="bold")
    ax.annotate("17.2% (2024)", (2024, eu[("MT", "REN", 2024)]), (2022.0, 9.6), fontsize=8.5, color=GREEN,
                fontweight="bold", arrowprops=dict(arrowstyle="-", color=GREEN, lw=0.7))
    ax.annotate("2025 provisional", (2025, 18.8), (2024.0, 12.3), fontsize=7.5, color=GREY,
                arrowprops=dict(arrowstyle="-", color=GREY, lw=0.6))
    ax.axvline(2020, color=GREY, lw=0.5, ls=":")
    ax.text(2020.1, 1.5, "2020 binding target: 10%", fontsize=7.5, color=GREY)
    ax.set_xlim(2013, 2030.8); ax.set_ylim(0, 31)
    ax.set_ylabel("Renewables, % of gross final energy consumption")
    ax.legend(frameon=False, fontsize=7.8, loc="upper left")
    ax.set_xticks(range(2013, 2031, 2))
    fig.savefig(OUT / "fig_path.png", bbox_inches="tight", facecolor="white")


def fig_sectors():
    yrs = list(range(2013, 2025))
    fig, (a, b) = plt.subplots(1, 2, figsize=(9.6, 4.0), dpi=220, gridspec_kw={"width_ratios": [1.5, 1]})
    for it, lab, col in (("REN_HEAT_CL", "Heating and cooling", ORANGE), ("REN_ELC", "Electricity", GREEN),
                         ("REN_TRA", "Transport", BLUE)):
        a.plot(yrs, [eu[("MT", it, y)] for y in yrs], color=col, lw=2.4, label=lab)
        a.text(2024.2, eu[("MT", it, 2024)] + {"REN_ELC": -2.2, "REN_TRA": 2.2, "REN_HEAT_CL": 0}[it], f"{eu[('MT', it, 2024)]:.1f}%", color=col, fontsize=8.5, va="center", fontweight="bold")
    a.set_xlim(2013, 2025.6); a.set_ylim(0, 65)
    a.set_title("Malta: renewable share by sector", fontsize=9.5, color=GREEN, loc="left", fontweight="bold")
    a.set_ylabel("% of sector's final consumption")
    a.legend(frameon=False, fontsize=8, loc="upper left")
    labs = ["Electricity", "Heating and\ncooling", "Transport"]
    mt = [eu[("MT", i, 2024)] for i in ("REN_ELC", "REN_HEAT_CL", "REN_TRA")]
    e27 = [eu[("EU27_2020", i, 2024)] for i in ("REN_ELC", "REN_HEAT_CL", "REN_TRA")]
    xs = range(3)
    b.bar([x - 0.2 for x in xs], mt, 0.4, color=GREEN, label="Malta")
    b.bar([x + 0.2 for x in xs], e27, 0.4, color=BLUE, label="EU-27")
    for x, m, e in zip(xs, mt, e27):
        b.text(x - 0.2, m + 1, f"{m:.0f}", ha="center", fontsize=8); b.text(x + 0.2, e + 1, f"{e:.0f}", ha="center", fontsize=8)
    b.set_xticks(list(xs)); b.set_xticklabels(labs, fontsize=8)
    b.set_ylim(0, 65)
    b.set_title("2024, Malta and EU-27", fontsize=9.5, color=GREEN, loc="left", fontweight="bold")
    b.legend(frameon=False, fontsize=8)
    fig.text(0.01, -0.02, "Source: Eurostat nrg_ind_ren (retrieved 5 Oct 2026).", fontsize=7, color=GREY)
    fig.tight_layout()
    fig.savefig(OUT / "fig_sectors.png", bbox_inches="tight", facecolor="white")


def fig_pv():
    fig, ax = plt.subplots(figsize=(9.6, 3.4), dpi=220)
    c23, c24, t = 241.0, 252.255, 350.0
    ax.plot([2023, 2024], [c23, c24], color=GREEN, lw=2.8, marker="o")
    ax.plot([2024, 2030], [c24, t], color=AMBER, lw=2.4, ls="--", marker="o")
    ax.plot([2024, 2030], [c24, c24 + (c24 - c23) * 6], color=GREY, lw=1.6, ls=":")
    ax.text(2030.1, t, "350 MWp (plan)", fontsize=8.5, va="center", color="#8a5d00", fontweight="bold")
    ax.text(2030.1, c24 + (c24 - c23) * 6, f"{c24 + (c24 - c23) * 6:.0f} if 2024's pace continued", fontsize=8, va="center", color=GREY)
    ax.text(2023, c23 - 12, "241 (plan, end-2023)", fontsize=8, color=GREEN, ha="left")
    ax.text(2024.05, c24 - 12, "252.3 (NSO, end-2024)", fontsize=8, color=GREEN, ha="left")
    ax.set_xlim(2022.8, 2033); ax.set_ylim(210, 380)
    ax.set_ylabel("Installed solar PV, MWp")
    ax.set_xticks(range(2023, 2031))
    ax.text(2022.9, 215, "Sources: Malta final updated NECP pp.74, 84; NSO NR 111/2025 (second-hand). The straight line to\n"
            "350 MWp needs about 16 MWp a year; 2024 added 11.5 (net).", fontsize=7, color=GREY)
    fig.savefig(OUT / "fig_pv.png", bbox_inches="tight", facecolor="white")


fig_path(); fig_sectors(); fig_pv()
print("ok")
