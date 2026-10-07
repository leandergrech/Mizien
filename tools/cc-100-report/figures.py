"""Figures for Claim Check 100, drawn from data/cc-100/ (run fetch.py first)."""
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
e = {(r["tra_meas"], r["schedule"], r["tra_cov"], int(r["year"])): float(r["value"]) for r in csv.DictReader(open(ROOT / "data/cc-100/eurostat_avia_paoc.csv"))}


def fig1():
    yrs = [y for y in range(2015, 2026) if ("PAS_CRD", "TOTAL", "TOTAL", y) in e]
    v = [e[("PAS_CRD", "TOTAL", "TOTAL", y)] / 1e6 for y in yrs]
    fig, ax = plt.subplots(figsize=(9.6, 3.9), dpi=220)
    ax.bar(yrs, v, color=[GREEN if y == 2025 else "#C9D3CC" for y in yrs])
    for y, x in zip(yrs, v):
        ax.text(y, x + 0.15, f"{x:.1f}", ha="center", fontsize=8.5, color=SLATE, fontweight="bold" if y == 2025 else None)
    ax.axhline(10, color=AMBER, lw=0.9, ls=":"); ax.text(2014.6, 10.2, "10 million", color="#8a6417", fontsize=8)
    ax.set_ylabel("Passengers (millions)"); ax.set_ylim(0, 11.5); ax.set_xticks(yrs)
    ax.text(2014.6, -1.6, "Passengers carried (arrivals and departures), all flights. Source: Eurostat avia_paoc, retrieved 5 Oct 2026.", fontsize=7, color=GREY, clip_on=False)
    fig.savefig(OUT / "fig1_passengers.png", bbox_inches="tight", facecolor="white")


if __name__ == "__main__":
    fig1()
