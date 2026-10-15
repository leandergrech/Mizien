"""Figures for Claim Check 118, drawn from data/cc-118/ (run fetch.py and calc.py first)."""
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
D = ROOT / "data" / "cc-118"
rd = lambda n: list(csv.DictReader(open(D / n, encoding="utf-8")))
EU27 = {"Austria", "Belgium", "Bulgaria", "Croatia", "Cyprus", "Czechia", "Denmark", "Estonia", "Finland", "France",
        "Germany", "Greece", "Hungary", "Ireland", "Italy", "Latvia", "Lithuania", "Luxembourg", "Malta", "Netherlands",
        "Poland", "Portugal", "Romania", "Slovakia", "Slovenia", "Spain", "Sweden"}


def fig1():
    rows = sorted(((float(r["max_seasonal_wei_plus_pct"]), r["country"], r["worst_quarter"]) for r in rd("eea_worst_seasonal_wei_2023.csv")
                   if r["country"] in EU27), reverse=True)
    fig, ax = plt.subplots(figsize=(9.6, 5.0), dpi=220)
    y = list(range(len(rows)))[::-1]
    cols = [GREEN if c == "Malta" else (SAGE if v >= 20 else "#C9D3CD") for v, c, q in rows]
    ax.barh(y, [v for v, _, _ in rows], color=cols, height=0.72)
    for yi, (v, c, q) in zip(y, rows):
        ax.text(v + 1, yi, f"{v:.1f}%  ({q})", va="center", fontsize=7.5, color=GREEN if c == "Malta" else SLATE,
                fontweight="bold" if c == "Malta" else "normal")
    ax.set_yticks(y)
    ax.set_yticklabels([c for _, c, _ in rows], fontsize=8)
    for t in ax.get_yticklabels():
        if t.get_text() == "Malta":
            t.set_fontweight("bold"); t.set_color(GREEN)
    for x, lab in ((20, "20%: scarcity"), (40, "40%: severe")):
        ax.axvline(x, color=AMBER if x == 20 else RED, lw=1, ls="--")
        ax.text(x + 0.5, len(rows) - 0.3, lab, fontsize=7.5, color=AMBER if x == 20 else RED, va="bottom")
    ax.set_xlabel("Highest seasonal WEI+ in 2023 (% of renewable freshwater used), with the quarter it occurs in")
    ax.set_xlim(0, 108)
    fig.savefig(OUT / "fig1_wei.png", bbox_inches="tight", facecolor="white")


def fig2():
    c = {r["check"].strip(): r["value"] for r in rd("checks.csv")}
    fig, ax = plt.subplots(figsize=(9.6, 3.4), dpi=220)
    groups = [("Surface water: good or high\necological status", float(c["share by number (denominator 19)"]), float(c["share by area"])),
              ("Groundwater: poor\nquantitative status", float(c["poor quantitative status: share by number"]), float(c["poor quantitative status: share by area"]))]
    w = 0.34
    for i, (lab, n, a) in enumerate(groups):
        ax.bar(i - w / 2 - 0.01, n, w, color=SAGE, label="By number of water bodies" if i == 0 else None)
        ax.bar(i + w / 2 + 0.01, a, w, color=GREEN, label="By area" if i == 0 else None)
        ax.text(i - w / 2 - 0.01, n + 2, f"{n:.0f}%", ha="center", fontsize=10, color=SLATE, fontweight="bold")
        ax.text(i + w / 2 + 0.01, a + 2, f"{a:.0f}%", ha="center", fontsize=10, color=GREEN, fontweight="bold")
    ax.set_xticks([0, 1]); ax.set_xticklabels([g[0] for g in groups], fontsize=9)
    ax.set_ylim(0, 125); ax.set_ylabel("% of water bodies")
    ax.legend(frameon=False, fontsize=8.5, loc="upper left", ncol=2)
    ax.text(-0.45, -34, "EEA WISE, Malta's WFD reporting of 2022 (19 surface water bodies, 15 groundwater bodies). Surface area excludes the 3 rivers (3.4 km in all) and territorial waters.",
            fontsize=7, color=GREY)
    fig.savefig(OUT / "fig2_denominators.png", bbox_inches="tight", facecolor="white")


if __name__ == "__main__":
    fig1(); fig2(); print("ok")
