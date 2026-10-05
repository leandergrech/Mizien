"""Figures for Claim Check 037, drawn from data/cc-037/ (run fetch.py and calc.py first)."""
import csv, pathlib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from matplotlib.lines import Line2D

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[1]
OUT = HERE / "out"
OUT.mkdir(exist_ok=True)
for f in ["LiberationSans-Regular", "LiberationSans-Bold", "LiberationSans-Italic"]:
    fm.fontManager.addfont(f"/usr/share/fonts/truetype/liberation/{f}.ttf")
plt.rcParams.update({"font.family": "Liberation Sans", "axes.spines.top": False, "axes.spines.right": False,
                     "axes.edgecolor": "#8A9399", "axes.labelcolor": "#2B3A42", "xtick.color": "#2B3A42",
                     "ytick.color": "#2B3A42"})
GREEN, SAGE, AMBER, RED, SLATE, GREY, ORANGE, BLUE = ("#14452F", "#7FA88B", "#E3A72F", "#B5483A", "#2B3A42",
                                                      "#8A9399", "#D9772B", "#3C6E8F")
EU27 = "BE BG CZ DK DE EE IE EL ES FR HR IT CY LV LT LU HU MT NL AT PL PT RO SI SK FI SE".split()
V, FLAG = {}, {}
for r in csv.DictReader(open(ROOT / "data" / "cc-037" / "eurostat_ilc_mddw02.csv")):
    if r["rskpovth"] == "TOTAL":
        V[(r["geo"], int(r["time"]))] = float(r["value"])
        FLAG[(r["geo"], int(r["time"]))] = r.get("flag", "")


def fig1():
    fig, ax = plt.subplots(figsize=(9.6, 4.0), dpi=220)
    ax.axvspan(2020.5, 2022.5, color="#EEF0EE", lw=0, zorder=0)
    ax.text(2021.5, 44.5, "Not collected\n2021–22", ha="center", va="top", fontsize=7.5, color=GREY)
    for geo, col, lab, ls in (("MT", GREEN, "Malta", "-"), ("EU27_2020", BLUE, "EU-27", "--")):
        xs = sorted(y for (g, y) in V if g == geo)
        # one line per run of consecutive years, so the 2021–22 gap is not bridged
        runs, cur = [], [xs[0]]
        for x in xs[1:]:
            if x == cur[-1] + 1:
                cur.append(x)
            else:
                runs.append(cur); cur = [x]
        runs.append(cur)
        for run in runs:
            ax.plot(run, [V[(geo, y)] for y in run], color=col, lw=2.4, ls=ls, zorder=2)
        for y in xs:   # hollow markers for values Eurostat flags as estimated
            est = FLAG.get((geo, y)) == "e"
            ax.plot([y], [V[(geo, y)]], marker="o", ms=4.2 if est else 3.6, color=col,
                    mfc="white" if est else col, mew=1.2, zorder=3)
        ax.text(2023.35, V[(geo, 2023)], f"{V[(geo, 2023)]:.1f}%", color=col, fontsize=9, va="center",
                fontweight="bold")
    for y, dy in ((2011, 1.6), (2017, -3.2)):
        ax.text(y, V[("MT", y)] + dy, f"{V[('MT', y)]:.1f}%", color=GREEN, fontsize=8, ha="center")
    ax.set_ylim(0, 46)
    ax.set_xlim(2004.6, 2025)
    ax.set_xticks(range(2005, 2024, 2))
    ax.set_ylabel("% of population")
    ax.legend(handles=[Line2D([], [], color=GREEN, lw=2.4, marker="o", ms=3.6, label="Malta"),
                       Line2D([], [], color=BLUE, lw=2.4, ls="--", marker="o", ms=3.6, label="EU-27"),
                       Line2D([], [], color=BLUE, lw=0, marker="o", ms=4.2, mfc="white", mew=1.2,
                              label="Eurostat estimate (flag e)")],
              frameon=False, fontsize=8.5, loc="lower left", ncol=3)
    ax.text(2004.7, -9, "Share of people living in a household that reports pollution, grime or other environmental problems "
            "in its area. Source: Eurostat\nilc_mddw02 (EU-SILC), retrieved 5 Oct 2026. Self-reported. No EU-27 aggregate "
            "before 2010; Malta's values carry no flags.", fontsize=7, color=GREY)
    fig.savefig(OUT / "fig1_trend.png", bbox_inches="tight", facecolor="white")


def fig2():
    fig, ax = plt.subplots(figsize=(9.6, 3.9), dpi=220)
    items = sorted(((g, V[(g, 2023)]) for g in EU27), key=lambda kv: -kv[1])
    ax.bar([k for k, _ in items], [v for _, v in items], color=[GREEN if k == "MT" else SAGE for k, _ in items], width=0.72)
    for i, (k, v) in enumerate(items):
        mark = "*" if FLAG.get((k, 2023)) == "u" else ""
        ax.text(i, v + 0.5, f"{v:.1f}{mark}", ha="center", fontsize=6.8,
                color=GREEN if k == "MT" else SLATE, fontweight="bold" if k == "MT" else "normal", zorder=4,
                bbox=dict(facecolor="white", edgecolor="none", pad=0.4))
    ax.axhline(V[("EU27_2020", 2023)], color=BLUE, lw=1.4, ls="--")
    ax.text(26.4, V[("EU27_2020", 2023)] + 0.9, f"EU-27 {V[('EU27_2020', 2023)]:.1f}%", color=BLUE, fontsize=8.5, ha="right")
    ax.set_ylim(0, 40)
    ax.set_ylabel("% of population")
    ax.tick_params(axis="x", labelsize=8)
    ax.text(-0.5, -7, "Eurostat ilc_mddw02, 2023, retrieved 5 Oct 2026. Country codes are Eurostat’s (EL = Greece). "
            "* Low reliability (Eurostat flag u): Germany.", fontsize=7, color=GREY)
    fig.savefig(OUT / "fig2_rank.png", bbox_inches="tight", facecolor="white")


fig1(); fig2()
print("figures in", OUT)
