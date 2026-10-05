"""Figures for Claim Check 037, drawn from data/cc-037/ (run calc.py first)."""
import csv, pathlib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm

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
V = {}
for r in csv.DictReader(open(ROOT / "data" / "cc-037" / "eurostat_ilc_mddw02.csv")):
    if r["rskpovth"] == "TOTAL":
        V[(r["geo"], int(r["time"]))] = float(r["value"])


def fig1():
    fig, ax = plt.subplots(figsize=(9.6, 4.0), dpi=220)
    for geo, col, lab, ls in (("MT", GREEN, "Malta", "-"), ("EU27_2020", BLUE, "EU-27", "--")):
        xs = sorted(y for (g, y) in V if g == geo)
        ax.plot(xs, [V[(geo, y)] for y in xs], color=col, lw=2.4, ls=ls, marker="o", ms=3.5, label=lab)
        ax.text(2023.3, V[(geo, 2023)], f"{V[(geo, 2023)]:.1f}%", color=col, fontsize=9, va="center", fontweight="bold")
    ax.set_ylim(0, 46)
    ax.set_xlim(2004.6, 2025)
    ax.set_xticks(range(2005, 2024, 2))
    ax.set_ylabel("% of population")
    ax.legend(frameon=False, fontsize=9, loc="upper right")
    ax.text(2004.7, -9, "Share reporting pollution, grime or other environmental problems in their area. Source: Eurostat "
            "ilc_mddw02 (EU-SILC),\nretrieved 5 Oct 2026. Self-reported. No values for 2021–2022; EU-27 series from 2010.",
            fontsize=7, color=GREY)
    fig.savefig(OUT / "fig1_trend.png", bbox_inches="tight", facecolor="white")


def fig2():
    fig, ax = plt.subplots(figsize=(9.6, 3.9), dpi=220)
    items = sorted(((g, V[(g, 2023)]) for g in EU27), key=lambda kv: -kv[1])
    ax.bar([k for k, _ in items], [v for _, v in items], color=[GREEN if k == "MT" else SAGE for k, _ in items], width=0.72)
    for i, (k, v) in enumerate(items):
        ax.text(i, v + 0.5, f"{v:.1f}" if k == "MT" else f"{v:.0f}", ha="center", fontsize=7.5,
                color=GREEN if k == "MT" else SLATE, fontweight="bold" if k == "MT" else "normal")
    ax.axhline(V[("EU27_2020", 2023)], color=BLUE, lw=1.4, ls="--")
    ax.text(26.4, V[("EU27_2020", 2023)] + 0.9, f"EU-27 {V[('EU27_2020', 2023)]:.1f}%", color=BLUE, fontsize=8.5, ha="right")
    ax.set_ylim(0, 40)
    ax.set_ylabel("% of population")
    ax.tick_params(axis="x", labelsize=8)
    ax.text(-0.5, -7, "Eurostat ilc_mddw02, 2023, retrieved 5 Oct 2026. Country codes are Eurostat’s (EL = Greece).",
            fontsize=7, color=GREY)
    fig.savefig(OUT / "fig2_rank.png", bbox_inches="tight", facecolor="white")


fig1(); fig2()
print("figures in", OUT)
