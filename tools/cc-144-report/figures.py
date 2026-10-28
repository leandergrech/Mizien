"""Figures for Claim Check 144, drawn from data/cc-144/ (run calc.py first)."""
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
R = list(csv.DictReader(open(ROOT / "data" / "cc-144" / "ranking_2010.csv", encoding="utf-8")))


def panel(ax, key, rk, title, xl):
    top = sorted(R, key=lambda r: float(r[rk]))[:8]
    if not any(r["country"] == "Malta" for r in top):
        top = top[:7] + [r for r in R if r["country"] == "Malta"]
    top = top[::-1]
    ax.barh([r["country"] for r in top], [float(r[key]) for r in top],
            color=[ORANGE if r["country"] == "Malta" else SAGE for r in top])
    for i, r in enumerate(top):
        ax.text(float(r[key]), i, f"  {float(r[key]):.1f}", va="center", fontsize=8, color=SLATE)
    ax.set_title(title, fontsize=10.5, color=SLATE, loc="left", fontweight="bold")
    ax.set_xlabel(xl, fontsize=9)
    ax.tick_params(labelsize=9)


def fig1():
    fig, (a, b) = plt.subplots(1, 2, figsize=(9.6, 4.2), dpi=220)
    panel(a, "per_km2", "rank_per_km2", "Per square kilometre", "Hunters per km² of land area")
    panel(b, "per_1000", "rank_per_1000", "Per 1,000 inhabitants", "Hunters per 1,000 inhabitants")
    a.set_xlim(0, 58); b.set_xlim(0, 98)
    fig.tight_layout()
    fig.savefig(OUT / "fig1_ranking.png"); plt.close(fig)


def fig2():
    fig, ax = plt.subplots(figsize=(9.6, 3.4), dpi=220)
    labs = ["FACE count\n15,000", "WBRU 2025 land licences\n10,091 (second-hand)", "BirdLife via\nMongabay 10,000", "Stress test\n5,000"]
    vals = [15000 / 316, 10091 / 316, 10000 / 316, 5000 / 316]
    ax.bar(labs, vals, color=[ORANGE, ORANGE, ORANGE, GREY], width=0.55)
    ax.axhline(5.0, color=GREEN, lw=1.6, ls="--")
    ax.text(3.45, 5.8, "Next highest country (Ireland, 5.0 per km², FACE 2010)", ha="right", fontsize=8.5, color=GREEN)
    for i, v in enumerate(vals):
        ax.text(i, v + 0.8, f"{v:.1f}", ha="center", fontsize=9, color=SLATE)
    ax.set_ylabel("Malta hunters per km²", fontsize=9)
    ax.tick_params(labelsize=8.5)
    fig.tight_layout()
    fig.savefig(OUT / "fig2_sensitivity.png"); plt.close(fig)


fig1(); fig2()
