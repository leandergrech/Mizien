"""Figures for Claim Check 110, drawn from data/cc-110/ (run fetch.py first)."""
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
n = {}
for r in csv.DictReader(open(ROOT / "data/cc-110/eurostat_road_eqr_carpda.csv")):
    n[(r["geo"], r["mot_nrg"], int(r["year"]))] = float(r["value"])
share = lambda g, y: 100 * (n.get((g, "ELC", y), 0) + n.get((g, "HYD_FCELL", y), 0)) / n[(g, "TOTAL", y)]


def fig1():
    fig, ax = plt.subplots(figsize=(9.6, 4.0), dpi=220)
    yrs = list(range(2019, 2026))
    for g, c, lab in (("MT", GREEN, "Malta"), ("EU27_2020", BLUE, "EU-27"), ("DK", GREY, "Denmark (highest)")):
        ax.plot(yrs, [share(g, y) for y in yrs], color=c, lw=2.6 if g != "DK" else 1.4, marker="o", ms=3.5, label=lab,
                ls="-" if g != "DK" else "--")
    for y, dy in ((2023, -5), (2024, 3)):
        ax.annotate(f"{share('MT', y):.1f}%", (y, share("MT", y)), xytext=(y - 0.35, share("MT", y) + dy), color=GREEN, fontsize=9, fontweight="bold")
    ax.annotate(f"{share('EU27_2020', 2024):.1f}%", (2024, share("EU27_2020", 2024)), xytext=(2023.8, share("EU27_2020", 2024) - 6), color=BLUE, fontsize=9, fontweight="bold")
    ax.set_ylim(0, 75); ax.set_ylabel("Zero-emission share of new cars (%)")
    ax.legend(frameon=False, fontsize=8.5, loc="upper left")
    ax.text(2019, -11, "Zero-emission = battery electric + hydrogen. Source: Eurostat road_eqr_carpda, retrieved 5 Oct 2026.", fontsize=7, color=GREY, clip_on=False)
    fig.savefig(OUT / "fig1_share.png", bbox_inches="tight", facecolor="white")


def fig2():
    geos = [g for g in {k[0] for k in n} if (g, "TOTAL", 2024) in n]
    items = sorted(((g, share(g, 2024)) for g in geos), key=lambda kv: kv[1])
    fig, ax = plt.subplots(figsize=(9.6, 4.6), dpi=220)
    cols = [GREEN if g == "MT" else BLUE if g == "EU27_2020" else "#C9D3CC" for g, _ in items]
    ax.barh([g.replace("EU27_2020", "EU-27") for g, _ in items], [x for _, x in items], color=cols)
    for i, (g, x) in enumerate(items):
        if g in ("MT", "EU27_2020"):
            ax.text(x, i, f"  {x:.1f}%", va="center", fontsize=8, color=GREEN if g == "MT" else BLUE, fontweight="bold")
    ax.tick_params(axis="y", labelsize=7.2); ax.set_xlabel("Zero-emission share of new passenger cars, 2024 (%)")
    fig.savefig(OUT / "fig2_rank.png", bbox_inches="tight", facecolor="white")


if __name__ == "__main__":
    fig1(); fig2()
