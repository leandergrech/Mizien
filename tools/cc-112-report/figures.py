"""Figures for Claim Check 111, drawn from data/cc-111/ (run fetch.py first)."""
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
for r in csv.DictReader(open(ROOT / "data/cc-111/eurostat_env_wasmun.csv")):
    v[(r["geo"], r["wst_oper"], r["unit"], int(r["year"]))] = float(r["value"])
v = {}
for r in csv.DictReader(open(ROOT / "data/cc-112/eurostat_demo_gind.csv")):
    v[(r["geo"], r["indic_de"], int(r["year"]))] = float(r["value"])
P = lambda y: v[("MT", "JAN", y)]


def fig1():
    fig, axs = plt.subplots(1, 2, figsize=(9.6, 3.9), dpi=220, gridspec_kw={"width_ratios": [1.15, 1]})
    ax = axs[0]
    yrs = list(range(2005, 2027))
    ax.plot(yrs, [P(y) / 1000 for y in yrs], color=GREEN, lw=2.6, marker="o", ms=3)
    ax.axvspan(2012, 2022, color=AMBER, alpha=0.15)
    ax.text(2012.3, 585, "2012–2022: +24.6%", color="#8a6417", fontsize=8.5)
    ax.annotate("588,254\n(1 Jan 2026)", (2026, 588.254), xytext=(2020.2, 430), color=GREEN, fontsize=8.5, fontweight="bold",
                arrowprops=dict(arrowstyle="-", color=GREEN, lw=0.6))
    ax.set_ylim(380, 620); ax.set_ylabel("Population on 1 January (thousands)")
    ax.set_title("Malta’s population", fontsize=10, color=SLATE, loc="left")
    ax = axs[1]
    starts = list(range(2008, 2017))
    g = [100 * (P(a + 10) / P(a) - 1) for a in starts]
    ax.bar([f"{a}–{str(a + 10)[2:]}" for a in starts], g, color=[AMBER if abs(x - 25) < 1.5 else "#C9D3CC" for x in g])
    for i, x in enumerate(g):
        ax.text(i, x + 0.6, f"{x:.0f}%", ha="center", fontsize=7.5, color=SLATE)
    ax.axhline(25, color=RED, lw=0.9, ls=":"); ax.text(-0.4, 26, "IMF: 25%", color=RED, fontsize=7.5)
    ax.set_ylim(0, 36); ax.tick_params(axis="x", labelsize=7, rotation=45)
    ax.set_title("Growth over each ten-year window", fontsize=10, color=SLATE, loc="left")
    fig.text(0.01, -0.04, "Source: Eurostat demo_gind, retrieved 5 Oct 2026. Windows run from 1 January to 1 January.", fontsize=7, color=GREY)
    fig.tight_layout(); fig.savefig(OUT / "fig1_population.png", bbox_inches="tight", facecolor="white")


def fig2():
    fig, ax = plt.subplots(figsize=(9.6, 3.6), dpi=220)
    yrs = list(range(2005, 2026))
    nat = [v[("MT", "NATGROW", y)] / 1000 for y in yrs]; mig = [v[("MT", "CNMIGRAT", y)] / 1000 for y in yrs]
    ax.bar(yrs, mig, color=BLUE, label="Net migration (incl. statistical adjustment)")
    ax.bar(yrs, nat, bottom=mig, color=GREEN, label="Natural change (births minus deaths)")
    ax.set_ylabel("Thousands of people"); ax.legend(frameon=False, fontsize=8.5, loc="upper left")
    ax.set_xticks(range(2005, 2026, 2)); ax.tick_params(axis="x", labelsize=8)
    ax.text(2005, -5, "Source: Eurostat demo_gind, retrieved 5 Oct 2026.", fontsize=7, color=GREY, clip_on=False)
    fig.savefig(OUT / "fig2_components.png", bbox_inches="tight", facecolor="white")


if __name__ == "__main__":
    fig1(); fig2()
