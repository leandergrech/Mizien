"""Figures for Claim Check 140, drawn from data/cc-140/ (run fetch.py first)."""
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
GREEN, AMBER, SLATE, GREY, BLUE = "#14452F", "#E3A72F", "#2B3A42", "#8A9399", "#3C6E8F"
e = {(r["geo"], int(r["year"])): float(r["value_pc"]) for r in csv.DictReader(open(ROOT / "data/cc-140/eurostat_nrg_ind_id.csv"))}


def fig1():
    yrs = list(range(2015, 2025))
    fig, ax = plt.subplots(figsize=(9.6, 3.9), dpi=220)
    for g, c, lab in [("MT", GREEN, "Malta"), ("CY", BLUE, "Cyprus"), ("LU", GREY, "Luxembourg"), ("EU27_2020", AMBER, "EU-27")]:
        ax.plot(yrs, [e[(g, y)] for y in yrs], color=c, lw=2.2 if g == "MT" else 1.5, marker="o", ms=3.5, label=lab)
    ax.axhline(98, color=SLATE, lw=0.8, ls=":"); ax.text(2015, 80, "Dotted line: 98.0, the figure in the Pre-Budget Document", fontsize=8, color=SLATE)
    ax.set_ylabel("Net imports as % of gross available energy"); ax.set_ylim(40, 108); ax.set_xticks(yrs)
    ax.legend(frameon=False, ncol=4, loc="lower center", fontsize=8.5)
    ax.text(2015, 28, "Source: Eurostat nrg_ind_id (updated 16 Jul 2026), retrieved 30 Oct 2026. Values above 100% occur when stocks are drawn down.",
            fontsize=7, color=GREY, clip_on=False)
    fig.savefig(OUT / "fig1_dependency.png", bbox_inches="tight", facecolor="white")


if __name__ == "__main__":
    fig1()
