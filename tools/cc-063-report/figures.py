"""Figures for Claim Check 063, drawn from data/cc-063/ (run fetch.py first)."""
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
GREEN, AMBER, RED, SLATE, GREY = "#14452F", "#E3A72F", "#B5483A", "#2B3A42", "#8A9399"
D = ROOT / "data/cc-063"
prd = {int(r["time"]): float(r["value"]) for r in csv.DictReader(open(D / "eurostat_sts_copr_a.csv"))}
gen = {(r["nace_r2"], r["waste"], int(r["time"])): float(r["value"]) for r in csv.DictReader(open(D / "eurostat_env_wasgen.csv"))}


def fig1():
    fig, axs = plt.subplots(1, 2, figsize=(9.6, 3.8), dpi=220)
    ax = axs[0]
    ys = list(range(2015, 2023))
    ax.plot(ys, [prd[y] for y in ys], color=GREEN, lw=2, marker="o", ms=4)
    ax.axvline(2021.4, color=RED, lw=0.9, ls=":")
    ax.text(2021.3, 104, "MDA warning,\n2 Jun 2021", color=RED, fontsize=8, ha="right")
    for y in (2020, 2021, 2022):
        ax.text(y, prd[y] + 3.5, f"{prd[y]:.0f}", ha="center", fontsize=8.5, color=SLATE, fontweight="bold")
    ax.set_ylim(90, 180)
    ax.set_title("Construction output, volume (2015 = 100)", fontsize=10, color=SLATE, loc="left")
    ax = axs[1]
    ys = [2010, 2012, 2014, 2016, 2018, 2020, 2022]
    ax.bar([str(y) for y in ys], [gen[("F", "TOTAL", y)] / 1e6 for y in ys],
           color=["#C9D3CC"] * 5 + [AMBER, GREEN])
    for i, y in enumerate(ys):
        ax.text(i, gen[("F", "TOTAL", y)] / 1e6 + 0.05, f"{gen[('F', 'TOTAL', y)] / 1e6:.1f}", ha="center", fontsize=8.5, color=SLATE)
    ax.set_ylim(0, 3.6)
    ax.set_ylabel("million tonnes")
    ax.set_title("Waste from the construction sector", fontsize=10, color=SLATE, loc="left")
    fig.text(0.01, -0.05, "Sources: Eurostat sts_copr_a (updated 2 Oct 2026; 2022 provisional; no later year published for Malta) and "
             "env_wasgen (NACE F, all waste; biennial), retrieved 5 Oct 2026.", fontsize=7, color=GREY)
    fig.tight_layout()
    fig.savefig(OUT / "fig1_output_waste.png", bbox_inches="tight", facecolor="white")


if __name__ == "__main__":
    fig1()
