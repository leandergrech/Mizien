"""Figures for Claim Check 088, drawn from data/cc-088/ (run fetch.py first)."""
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
v = {}
for r in csv.DictReader(open(ROOT / "data/cc-088/eurostat_demo_gind.csv")):
    v[(r["indic_de"], int(r["year"]))] = float(r["value"])


def fig1():
    fig, axs = plt.subplots(1, 2, figsize=(9.6, 3.8), dpi=220, gridspec_kw={"width_ratios": [1.1, 1]})
    ax = axs[0]
    yrs = list(range(2015, 2027))
    ax.plot(yrs, [v[("JAN", y)] / 1000 for y in yrs], color=GREEN, lw=2.6, marker="o", ms=3.5)
    ax.annotate("588,254\n(end 2025)", (2026, 588.254), xytext=(2021.6, 585), color=GREEN, fontsize=8.5, fontweight="bold",
                arrowprops=dict(arrowstyle="-", color=GREEN, lw=0.6), va="top")
    ax.set_ylim(420, 610); ax.set_ylabel("Population on 1 January (thousands)")
    ax.set_title("Malta’s population", fontsize=10, color=SLATE, loc="left")
    ax = axs[1]
    ys = list(range(2015, 2026))
    g = [100 * (v[("JAN", y + 1)] / v[("JAN", y)] - 1) for y in ys]
    ax.bar([str(y) for y in ys], g, color=["#C9D3CC"] * (len(ys) - 1) + [GREEN])
    for i, x in enumerate(g):
        ax.text(i, x + 0.08, f"{x:.1f}%", ha="center", fontsize=7.5, color=SLATE)
    ax.set_ylim(0, 4.6); ax.tick_params(axis="x", labelsize=7.5, rotation=45)
    ax.set_title("Growth during each calendar year", fontsize=10, color=SLATE, loc="left")
    fig.text(0.01, -0.04, "Source: Eurostat demo_gind (data supplied by the NSO), retrieved 5 Oct 2026.", fontsize=7, color=GREY)
    fig.tight_layout(); fig.savefig(OUT / "fig1_population.png", bbox_inches="tight", facecolor="white")


def fig2():
    fig, ax = plt.subplots(figsize=(9.6, 3.4), dpi=220)
    yrs = list(range(2015, 2026))
    nat = [v[("NATGROW", y)] / 1000 for y in yrs]; mig = [v[("CNMIGRAT", y)] / 1000 for y in yrs]
    ax.bar(yrs, mig, color=BLUE, label="Net migration")
    ax.bar(yrs, nat, bottom=mig, color=GREEN, label="Natural increase (births minus deaths)")
    ax.text(2025, mig[-1] + 0.5, "13,906", ha="center", fontsize=8, color=BLUE, fontweight="bold")
    ax.set_ylabel("Thousands of people"); ax.legend(frameon=False, fontsize=8.5, loc="upper left")
    ax.set_xticks(yrs); ax.tick_params(axis="x", labelsize=8)
    ax.text(2015, -2.6, "Source: Eurostat demo_gind, retrieved 5 Oct 2026.", fontsize=7, color=GREY, clip_on=False)
    fig.savefig(OUT / "fig2_components.png", bbox_inches="tight", facecolor="white")


if __name__ == "__main__":
    fig1(); fig2()
