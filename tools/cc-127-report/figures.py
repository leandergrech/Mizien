"""Figures for Claim Check 127, drawn from data/cc-127/."""
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
GREEN, AMBER, RED, SLATE, GREY, BLUE = "#14452F", "#E3A72F", "#B5483A", "#2B3A42", "#8A9399", "#3C6E8F"
S = {}
for r in csv.DictReader(open(ROOT / "data/cc-127/organic_share_pc_uaa.csv")):
    S[(r["geo"], int(r["year"]))] = float(r["pc_uaa"])
EU27 = "AT BE BG CY CZ DE DK EE EL ES FI FR HR HU IE IT LT LU LV MT NL PL PT RO SE SI SK".split()


def fig1():
    """Organic share of farmland, 2022, all reporting Member States (AT, EL: latest year, hatched)."""
    items = []
    for g in EU27:
        if (g, 2022) in S:
            items.append((S[(g, 2022)], g, False))
    items.append((S[("AT", 2020)], "AT", True))
    items.append((S[("EL", 2021)], "EL", True))
    items.sort()
    fig, ax = plt.subplots(figsize=(9.6, 3.9), dpi=220)
    for i, (v, g, old) in enumerate(items):
        col = RED if g == "MT" else (GREY if old else BLUE)
        ax.bar(i, v, color=col, hatch="//" if old else None, edgecolor="white" if old else col, linewidth=0)
        ax.text(i, v + 0.5, f"{v:.1f}" if v >= 1 else f"{v:.2f}", ha="center", fontsize=6.8, color=SLATE,
                fontweight="bold" if g == "MT" else "normal")
    ax.axhline(S[("EU27_2020", 2020)], color=SLATE, lw=1.1, ls="--")
    ax.text(-0.4, S[("EU27_2020", 2020)] + 0.6, "EU-27 average 2020: 9.1% (estimate)", ha="left", fontsize=7.5, color=SLATE)
    ax.set_xticks(range(len(items)))
    ax.set_xticklabels([g for _, g, _ in items], fontsize=8)
    ax.set_ylabel("Organic share of farmland, %")
    fig.text(0.01, -0.04, "Eurostat sdg_02_40, 2022; hatched = Austria (2020) and Greece (2021), absent from the 2022 release. "
             "Retrieved 21 Oct 2026.", fontsize=7, color=GREY)
    fig.savefig(OUT / "fig1_ranking.png", bbox_inches="tight", facecolor="white")


def fig2():
    """Malta against the next-lowest Member State, 2012-2024."""
    yrs = list(range(2012, 2025))
    mt = [S[("MT", y)] for y in yrs]
    nxt = [min(S[(g, y)] for g in EU27 if g != "MT" and (g, y) in S) for y in yrs]
    fig, ax = plt.subplots(figsize=(9.6, 2.9), dpi=220)
    ax.plot(yrs, nxt, color=BLUE, lw=2, marker="o", ms=3.5, label="Lowest of the other Member States")
    ax.plot(yrs, mt, color=RED, lw=2.4, marker="o", ms=4, label="Malta")
    ax.set_ylim(0, 4.5)
    ax.set_ylabel("Organic share of farmland, %")
    ax.set_xticks(yrs)
    ax.tick_params(labelsize=8)
    ax.legend(frameon=False, fontsize=8, loc="upper left")
    fig.text(0.01, -0.04, "Eurostat sdg_02_40. From 2021 Austria, and from 2022 Greece, are missing from the release (both were far above Malta when last published).",
             fontsize=7, color=GREY)
    fig.savefig(OUT / "fig2_series.png", bbox_inches="tight", facecolor="white")


if __name__ == "__main__":
    fig1()
    fig2()
