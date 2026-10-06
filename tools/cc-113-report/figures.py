"""Figures for Claim Check 113, drawn from data/cc-113/ (run fetch.py and calc.py first)."""
import csv, pathlib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from matplotlib.lines import Line2D
from matplotlib.patches import Patch

HERE = pathlib.Path(__file__).resolve().parent
D = HERE.parents[1] / "data" / "cc-113"
OUT = HERE / "out"
OUT.mkdir(exist_ok=True)
for f in ["LiberationSans-Regular", "LiberationSans-Bold", "LiberationSans-Italic"]:
    fm.fontManager.addfont(f"/usr/share/fonts/truetype/liberation/{f}.ttf")
plt.rcParams.update({"font.family": "Liberation Sans", "axes.spines.top": False, "axes.spines.right": False,
                     "axes.edgecolor": "#8A9399", "axes.labelcolor": "#2B3A42", "xtick.color": "#2B3A42",
                     "ytick.color": "#2B3A42"})
GREEN, SAGE, AMBER, RED, SLATE, GREY, ORANGE, BLUE = ("#14452F", "#7FA88B", "#E3A72F", "#B5483A", "#2B3A42",
                                                      "#8A9399", "#D9772B", "#3C6E8F")
var = list(csv.DictReader(open(D / "shares_2023_variants.csv")))
A = {r["geo"]: float(r["share_of_gdp_pct"]) for r in var if r["variant"].startswith("A:")}
B = {r["geo"]: float(r["share_of_gdp_pct"]) for r in var if r["variant"].startswith("B:")}
Dx = {r["geo"]: float(r["share_of_gdp_pct"]) for r in var if r["variant"].startswith("D:")}
eu = {r["geo"]: float(r["ffs_share_of_gdp_pct"]) for r in csv.DictReader(open(D / "eea_share_of_gdp_2023.csv"))}


def fig1():
    fig, ax = plt.subplots(figsize=(9.6, 3.5), dpi=220)
    order = sorted(A, key=lambda g: -A[g])
    xs = range(len(order))
    ax.bar(xs, [A[g] for g in order], width=0.7, color=[GREEN if g == "MT" else SAGE for g in order], zorder=2)
    ax.scatter(xs, [B[g] for g in order], marker="D", s=16, color=ORANGE, zorder=3)
    ax.scatter(xs, [Dx[g] for g in order], marker="_", s=70, linewidths=1.6, color=SLATE, zorder=3)
    ax.axhline(1.5, color=RED, lw=1.1, ls="--", zorder=1)
    ax.text(26.4, 1.56, "1.5% of GDP", color=RED, fontsize=8, ha="right")
    ax.axhline(eu["EU27"], color=BLUE, lw=1.1, ls=":", zorder=1)
    ax.text(26.4, eu["EU27"] + 0.06, f"EU-27 as a whole {eu['EU27']:.2f}%", color=BLUE, fontsize=8, ha="right")
    for i, g in enumerate(order[:4]):
        ax.text(i, A[g] + 0.09, f"{A[g]:.2f}", ha="center", fontsize=7.6, color=GREEN if g == "MT" else SLATE,
                fontweight="bold" if g == "MT" else "normal")
    ax.set_xticks(list(xs))
    ax.set_xticklabels(order, fontsize=8)
    ax.set_ylim(0, 3.75)
    ax.set_ylabel("Fossil fuel subsidies, % of GDP")
    ax.legend(handles=[Patch(color=SAGE, label="EEA basis (bars; Malta dark): inventory incl. 2022 proxies, "
                                               "inventory GDP"),
                       Line2D([], [], marker="D", color=ORANGE, lw=0, ms=4.5,
                              label="Same subsidies, Eurostat GDP as of 6 Oct 2026"),
                       Line2D([], [], marker="_", color=SLATE, lw=0, ms=9, mew=1.6,
                              label="Lower bound: unconfirmed items set to zero, Eurostat GDP")],
              frameon=False, fontsize=8, loc="upper right", bbox_to_anchor=(1.0, 0.86))
    fig.savefig(OUT / "fig1_rank.png", bbox_inches="tight", facecolor="white")


def fig2():
    inv = {int(r["year"]): float(r["ffs_share_of_gdp_pct"]) for r in csv.DictReader(open(D / "eea_malta_trend_soer2025.csv"))
           if r["series"] == "Historical trend Malta"}
    oth = list(csv.DictReader(open(D / "other_estimates_transcribed.csv")))
    gov = {int(r["year"]): float(r["value"]) for r in oth if r["measure"].startswith("Energy support measures")}
    imf = {int(r["year"]): float(r["value"]) for r in oth if r["measure"] == "Energy subsidies (IMF Article IV)"}
    com24 = [float(r["value"]) * 100 for r in oth if r["measure"].startswith("Fossil fuel subsidies per unit")][0]
    pg = {int(r["year"]): float(r["pct_of_gdp"]) for r in csv.DictReader(open(D / "imf_ffs_eu27.csv"))
          if r["geo"] == "MT" and r["indicator"] == "Explicit Fossil Fuel Subsidies - Total"}
    fig, ax = plt.subplots(figsize=(9.6, 3.0), dpi=220)

    def series(d, col, mk, ms, hollow_from, lw=2, ls="-", z=3):
        """Line through all points; filled markers for outturns, hollow for expected or projected values."""
        ys = sorted(d)
        ax.plot(ys, [d[y] for y in ys], color=col, lw=lw, ls=ls, zorder=z)
        for y in ys:
            h = y >= hollow_from
            ax.plot([y], [d[y]], marker=mk, ms=ms, color=col, mfc="white" if h else col, mew=1.4, lw=0, zorder=z + 1)

    series(inv, GREEN, "o", 4.8, 9999, lw=2.2, z=4)
    ax.plot([2024], [com24], marker="o", ms=6, mfc="white", mec=GREEN, mew=1.6, lw=0, zorder=5)
    series(gov, ORANGE, "s", 4.8, 2023)          # DBP 2024 (Oct 2023) gives 2023 as expected; 2024-25 expected
    series(imf, BLUE, "^", 5.2, 2025)            # CR 26/29: 2025 is a projection
    yp = {y: pg[y] for y in sorted(pg) if y <= 2025}
    series(yp, GREY, "D", 3.6, 2023, lw=1.6, ls="--", z=2)   # 2023 update published Aug 2023
    ax.text(2023.15, inv[2023] + 0.02, f"{inv[2023]:.2f}%", color=GREEN, fontsize=8.5, fontweight="bold", va="center")
    ax.text(2024.15, com24 + 0.12, "≈1.8% (2026 report,\nread from chart)", color=GREEN, fontsize=7.4)
    ax.text(2022.0, gov[2022] + 0.14, f"{gov[2022]:.1f}%", color=ORANGE, fontsize=8, ha="center")
    ax.text(2023.12, gov[2023] + 0.1, f"{gov[2023]:.1f}%", color=ORANGE, fontsize=8, ha="left")
    ax.text(2023.0, imf[2023] - 0.27, f"{imf[2023]:.1f}%", color=BLUE, fontsize=8, ha="center")
    ax.set_xlim(2014.6, 2025.9)
    ax.set_ylim(-0.15, 3.75)
    ax.set_xticks(range(2015, 2026))
    ax.set_ylabel("% of GDP")
    ax.legend(handles=[Line2D([], [], color=GREEN, lw=2.2, marker="o", ms=4.5,
                              label="EU inventory method (EEA indicator; 2024 edition)"),
                       Line2D([], [], color=ORANGE, lw=2, marker="s", ms=4.5,
                              label="Government of Malta: energy support measures (draft budgetary plans)"),
                       Line2D([], [], color=BLUE, lw=2, marker="^", ms=5,
                              label="IMF Article IV: electricity and fuel subsidies"),
                       Line2D([], [], color=GREY, lw=1.6, ls="--", marker="D", ms=3.6,
                              label="IMF price-gap database: explicit subsidies (zero)"),
                       Line2D([], [], color=SLATE, lw=0, marker="o", ms=5, mfc="white", mew=1.4,
                              label="Hollow: expected, projected or estimated before the year ended")],
              frameon=False, fontsize=7.8, loc="upper left")
    fig.savefig(OUT / "fig2_measures.png", bbox_inches="tight", facecolor="white")


fig1(); fig2()
print("figures in", OUT)
