"""Figures for Claim Check 115, drawn from data/cc-115/ (run fetch.py first)."""
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
g = {(r["unit"], int(r["year"])): float(r["value"]) for r in csv.DictReader(open(ROOT / "data/cc-115/eurostat_nama_10_gdp.csv"))}


def fig1():
    fig, axs = plt.subplots(1, 2, figsize=(9.6, 3.8), dpi=220, gridspec_kw={"width_ratios": [1.2, 1]})
    ax = axs[0]
    labs = ["Nominal GDP\n2025", "Nominal GDP\n2024", "Chamber's\nreal GDP 2025", "Real GDP 2025\n(2020 prices)"]
    vals = [100 * 770 / g[("CP_MEUR", 2025)], 100 * 770 / g[("CP_MEUR", 2024)], 100 * 770 / 20400, 100 * 770 / g[("CLV20_MEUR", 2025)]]
    ax.bar(labs, vals, color=[GREEN, "#C9D3CC", "#C9D3CC", "#C9D3CC"])
    for i, x in enumerate(vals):
        ax.text(i, x + 0.06, f"{x:.2f}%", ha="center", fontsize=8.5, color=SLATE, fontweight="bold" if i == 0 else None)
    ax.axhline(3.4, color=RED, lw=0.9, ls=":"); ax.text(3.45, 3.43, "claim: 3.4%", color=RED, fontsize=8, ha="right", va="bottom")
    ax.set_ylim(0, 4.6); ax.tick_params(axis="x", labelsize=7.8)
    ax.set_title("EUR 770 million as a share of GDP", fontsize=10, color=SLATE, loc="left")
    ax = axs[1]
    ax.bar(["2025", "2030 (BAU)"], [770, 917], color=[AMBER, "#C9D3CC"])
    ax.bar(["2030 (BAU)"], [195.4], bottom=[917], color="#E9C3BC")
    ax.text(0, 785, "770", ha="center", fontsize=9, fontweight="bold", color=SLATE)
    ax.text(1, 932 + 195, "917 + 195\nenvironmental", ha="center", fontsize=8, color=SLATE)
    ax.set_ylim(0, 1350); ax.set_ylabel("EUR million a year")
    ax.set_title("The plan's estimates", fontsize=10, color=SLATE, loc="left")
    fig.text(0.01, -0.05, "Sources: National Transport Master Plan 2030 (Jan 2026), p. 124; Eurostat nama_10_gdp, retrieved 5 Oct 2026. "
             "The plan does not publish how the 2025 figure was derived.", fontsize=7, color=GREY)
    fig.tight_layout(); fig.savefig(OUT / "fig1_share.png", bbox_inches="tight", facecolor="white")


if __name__ == "__main__":
    fig1()
