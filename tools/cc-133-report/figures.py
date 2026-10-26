"""Figures for Claim Check 133 (data/cc-133/eurostat_housing.csv)."""
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
                     "axes.edgecolor": "#8A9399"})
GREEN, AMBER, BLUE, SLATE, GREY = "#14452F", "#E3A72F", "#3F6E8F", "#2B3A42", "#8A9399"
ROWS = list(csv.DictReader(open(ROOT / "data" / "cc-133" / "eurostat_housing.csv", encoding="utf-8")))
V = {(r["dataset"], r["geo"], r["item"], r["unit"], int(r["year"])): float(r["value"]) for r in ROWS}
MT, EU = "MT", "EU27_2020"
hpi = lambda g, y: V[("prc_hpi_a", g, "TOTAL", "I15_A_AVG", y)]
ptir = lambda g, y: V[("tipsho60", g, "PTIR", "PTIR_I15", y)]
SRC = "retrieved 26 Oct 2026"


def fig1():
    fig, ax = plt.subplots(figsize=(9.2, 3.9), dpi=220)
    ys = list(range(2005, 2026)); yp = list(range(2005, 2025))
    ax.plot(ys, [hpi(MT, y) / hpi(MT, 2005) * 100 for y in ys], color=GREEN, lw=2.4, label="House prices, Malta (nominal)")
    ax.plot(ys, [hpi(EU, y) / hpi(EU, 2005) * 100 for y in ys], color=AMBER, lw=2.4, label="House prices, EU-27 (nominal)")
    ax.plot(yp, [ptir(MT, y) / ptir(MT, 2005) * 100 for y in yp], color=GREEN, lw=2, ls="--", label="Price-to-income ratio, Malta")
    ax.plot(yp, [ptir(EU, y) / ptir(EU, 2005) * 100 for y in yp], color=AMBER, lw=2, ls="--", label="Price-to-income ratio, EU-27")
    ax.axvline(2014, color=GREY, lw=0.8, ls=":")
    ax.text(2014.15, 285, "2014", fontsize=8, color=GREY)
    for v, c, y, dy in ((hpi(MT, 2025) / hpi(MT, 2005) * 100, GREEN, 2025, 0), (hpi(EU, 2025) / hpi(EU, 2005) * 100, AMBER, 2025, 0),
                        (ptir(MT, 2024) / ptir(MT, 2005) * 100, GREEN, 2024, -9), (ptir(EU, 2024) / ptir(EU, 2005) * 100, AMBER, 2024, 9)):
        ax.text(y + 0.25, v + dy, f"{v:.0f}", fontsize=8.5, color=c, va="center")
    ax.set_xlim(2004.6, 2026.3); ax.set_ylim(60, 310); ax.set_xticks(range(2005, 2026, 2))
    ax.set_ylabel("Index, 2005 = 100", fontsize=8.5, color=SLATE)
    ax.tick_params(labelsize=8.5, colors=SLATE)
    ax.legend(frameon=False, fontsize=8, loc="upper left")
    ax.text(2004.6, 5, "Source: Eurostat prc_hpi_a (house price index, total) and tipsho60 (standardised price-to-income ratio), rebased to 2005, " + SRC + ". 2025 house prices provisional.",
            fontsize=6.8, color=GREY, clip_on=False)
    fig.savefig(OUT / "fig1_index.png", bbox_inches="tight", facecolor="white")


def fig2():
    ys = list(range(2015, 2026))
    fig, ax = plt.subplots(figsize=(9.2, 3.4), dpi=220)
    w = 0.38
    mt = [V[("prc_hpi_a", MT, "TOTAL", "RCH_A_AVG", y)] for y in ys]
    eu = [V[("prc_hpi_a", EU, "TOTAL", "RCH_A_AVG", y)] for y in ys]
    ax.bar([y - w / 2 for y in ys], mt, w, color=GREEN, label="Malta")
    ax.bar([y + w / 2 for y in ys], eu, w, color=AMBER, label="EU-27")
    for y, a, b in zip(ys, mt, eu):
        ax.text(y - w / 2, a + 0.2, f"{a:.1f}", ha="center", fontsize=7, color=GREEN)
        ax.text(y + w / 2, max(b, 0) + 0.2, f"{b:.1f}", ha="center", fontsize=7, color="#9A6B00")
    ax.axvspan(2019.5, 2022.5, color="#F6E7C4", zorder=0)
    ax.text(2021, 9.3, "EU-27 faster", ha="center", fontsize=8, color="#9A6B00")
    ax.axhline(0, color=GREY, lw=0.8)
    ax.set_xticks(ys); ax.set_ylim(-1.2, 10)
    ax.set_ylabel("Nominal house prices, % change on previous year", fontsize=8.2, color=SLATE)
    ax.tick_params(labelsize=8.5, colors=SLATE)
    ax.legend(frameon=False, fontsize=8.5, loc="upper left")
    ax.text(2014.4, -3.6, "Source: Eurostat prc_hpi_a (annual average rate of change, total purchases), " + SRC + ". 2025 Malta value provisional.",
            fontsize=6.8, color=GREY, clip_on=False)
    fig.savefig(OUT / "fig2_growth.png", bbox_inches="tight", facecolor="white")


def fig3():
    ys = list(range(2014, 2025))
    inc = lambda y: V[("nasa_10_nf_tr", MT, "B7G_S14_S15", "CP_MEUR", y)] / V[("nama_10_pe", MT, "POP_NC", "THS_PER", y)]
    med = lambda y: V[("ilc_di03", MT, "MED_EI", "EUR", y + 1)]  # SILC year t+1 = income year t
    fig, ax = plt.subplots(figsize=(9.2, 3.6), dpi=220)
    s = [("House prices (nominal)", [hpi(MT, y) / hpi(MT, 2014) * 100 for y in ys], GREEN, "-"),
         ("Adjusted household disposable income per head (national accounts)", [inc(y) / inc(2014) * 100 for y in ys], BLUE, "-"),
         ("Median equivalised household income (EU-SILC)", [med(y) / med(2014) * 100 for y in ys], AMBER, "--")]
    for lab, v, c, ls in s:
        ax.plot(ys, v, color=c, lw=2.3, ls=ls, marker="o", ms=3, label=lab)
        ax.text(2024.2, v[-1], f"{v[-1]:.0f}", fontsize=8.5, color=c, va="center")
    ax.set_xticks(ys); ax.set_xlim(2013.7, 2024.9); ax.set_ylim(90, 205)
    ax.set_ylabel("Malta, index 2014 = 100", fontsize=8.5, color=SLATE)
    ax.tick_params(labelsize=8.5, colors=SLATE)
    ax.legend(frameon=False, fontsize=8, loc="upper left")
    ax.text(2013.7, 66, "Source: Eurostat prc_hpi_a; nasa_10_nf_tr (B7G, S14_S15) / nama_10_pe; ilc_di03 (survey year t+1 plotted at income year t), " + SRC + ".",
            fontsize=6.8, color=GREY, clip_on=False)
    fig.savefig(OUT / "fig3_income.png", bbox_inches="tight", facecolor="white")


if __name__ == "__main__":
    fig1(); fig2(); fig3()
