"""Figures for Claim Check 137, drawn from data/cc-137/ (run calc.py first)."""
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
GREEN, SAGE, AMBER, RED, SLATE, GREY, ORANGE = "#14452F", "#7FA88B", "#E3A72F", "#B5483A", "#2B3A42", "#8A9399", "#D9772B"
C = {r["check"].split(" ")[0]: float(r["value"]) for r in csv.DictReader(open(ROOT / "data/cc-137/checks.csv", encoding="utf-8"))
     if r["check"].split(" ")[0] != "" and r["value"].replace(".", "", 1).isdigit()}
peak = {y: C["A-%d" % y] for y in range(2017, 2026)}


def fig1():
    fig, ax = plt.subplots(figsize=(9.6, 3.9), dpi=220)
    ys = list(peak)
    ax.bar(ys, [peak[y] for y in ys], color=[SAGE if y != 2023 else ORANGE for y in ys], width=0.6)
    for y in ys:
        ax.text(y, peak[y] + 6, "%d" % peak[y], ha="center", fontsize=8.5, color=SLATE)
    b1 = C["A5"]; b0 = peak[2017] - 0  # trend line from calc: refit here for display
    import numpy as np
    k, c = np.polyfit(range(2017, 2023), [peak[y] for y in range(2017, 2023)], 1)
    xs = np.array([2016.6, 2025.4])
    ax.plot(xs, k * xs + c, color=GREEN, lw=1.6, ls="--")
    ax.text(2016.6, 700, "Dashed line: trend fitted to 2017–2022 only (+21 MW a year)", ha="left", fontsize=8.5, color=GREEN)
    ax.set_ylim(0, 740); ax.set_ylabel("Highest monthly maximum demand (MW)", fontsize=9)
    ax.set_xticks(ys); ax.tick_params(labelsize=9)
    fig.tight_layout(); fig.savefig(OUT / "fig1_peak.png"); plt.close(fig)


def fig2():
    fig, ax = plt.subplots(figsize=(9.6, 3.0), dpi=220)
    labs = ["Peak demand", "Residents + peak-month tourists", "Residents alone", "Final electricity consumption"]
    vals = [C["A1"], C["A2"], C["A3"], C["A4"]]
    ax.barh(labs[::-1], vals[::-1], color=[SAGE, SAGE, SAGE, ORANGE], height=0.55)
    for i, v in enumerate(vals[::-1]):
        ax.text(v + 0.6, i, "+%.1f%%" % v, va="center", fontsize=9, color=SLATE)
    ax.set_xlim(0, 52); ax.set_xlabel("Change 2018 to 2023 (%)", fontsize=9); ax.tick_params(labelsize=9)
    fig.tight_layout(); fig.savefig(OUT / "fig2_growth.png"); plt.close(fig)


fig1(); fig2()
