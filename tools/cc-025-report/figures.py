"""Figures for Claim Check 025, drawn from data/cc-025/ (run fetch.py first)."""
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
v = {}
for r in csv.DictReader(open(ROOT / "data/cc-025/eurostat_gdp_ghg_pop.csv")):
    v[(r["dataset"], r["geo"], r["item"], r["unit"], int(r["year"]))] = float(r["value"])


def ser(g):
    e = {y: v[("env_air_gge", g, "TOTX4_MEMO", "MIO_T", y)] for y in range(2005, 2025)}
    p = {y: v[("nama_10_pe", g, "POP_NC", "THS_PER", y)] for y in range(2005, 2026)}
    r = {y: v[("nama_10_gdp", g, "B1GQ", "CLV20_MEUR", y)] for y in range(2005, 2026)}
    n = {y: v[("nama_10_gdp", g, "B1GQ", "CP_MEUR", y)] for y in range(2005, 2026)}
    return e, p, r, n


def fig1():
    e, p, r, n = ser("MT")
    yrs = list(range(2005, 2025))
    ix = lambda s: [100 * s[y] / s[2005] for y in yrs]
    series = [("Real GDP (volumes)", ix(r), GREY, "-", 2), ("Total emissions", ix(e), GREEN, "-", 2.6),
              ("Emissions per person", ix({y: e[y] / p[y] for y in yrs}), AMBER, "-", 2.4),
              ("Emissions per unit of GDP, volumes", ix({y: e[y] / r[y] for y in yrs}), BLUE, "-", 2.6),
              ("Emissions per unit of GDP, current prices", ix({y: e[y] / n[y] for y in yrs}), RED, "--", 2.2)]
    fig, ax = plt.subplots(figsize=(9.6, 4.8), dpi=220)
    for lab, s, c, ls, lw in series:
        ax.plot(yrs, s, color=c, lw=lw, ls=ls, label=lab)
    ax.axhline(100, color=GREY, lw=0.6)
    ax.axhline(20, color=RED, lw=0.8, ls=":")
    ax.text(2005.2, 22.5, "−80%: the claimed fall", color=RED, fontsize=8)
    for (lab, s, c, ls, lw), dy in zip(series, (0, 0, 5, 0, -5)):
        ax.text(2024.3, s[-1] + dy, f"{s[-1] - 100:+.0f}%", color=c, fontsize=8.5, va="center", fontweight="bold")
    ax.set_xlim(2005, 2026.4)
    ax.set_ylim(0, 290)
    ax.set_ylabel("Index, 2005 = 100")
    ax.set_xticks(range(2005, 2025, 5))
    ax.legend(frameon=False, fontsize=8, loc="upper left")
    ax.text(2005, -30, "Malta. Emissions exclude LULUCF and international aviation and shipping. Source: Eurostat env_air_gge, "
            "nama_10_gdp, nama_10_pe (retrieved 5 Oct 2026).", fontsize=7, color=GREY, clip_on=False)
    fig.savefig(OUT / "fig1_index.png", bbox_inches="tight", facecolor="white")


def fig2():
    fig, axs = plt.subplots(1, 2, figsize=(9.6, 3.9), dpi=220, sharey=True)
    for ax, y in zip(axs, (2023, 2024)):
        vals = {}
        for g in ("MT", "EU27_2020"):
            e, p, r, n = ser(g)
            vals[g] = [100 * ((e[y] / p[y]) / (e[2005] / p[2005]) - 1), 100 * ((e[y] / r[y]) / (e[2005] / r[2005]) - 1),
                       100 * ((e[y] / n[y]) / (e[2005] / n[2005]) - 1)]
        xs = range(3)
        ax.bar([x - 0.2 for x in xs], vals["MT"], 0.38, color=GREEN, label="Malta")
        ax.bar([x + 0.2 for x in xs], vals["EU27_2020"], 0.38, color=BLUE, label="EU-27")
        for x in xs:
            ax.text(x - 0.2, vals["MT"][x] - 3, f"{vals['MT'][x]:.0f}%", ha="center", va="top", fontsize=8.5,
                    fontweight="bold", color=GREEN)
            ax.text(x + 0.2, vals["EU27_2020"][x] - 3, f"{vals['EU27_2020'][x]:.0f}%", ha="center", va="top",
                    fontsize=8.5, fontweight="bold", color=BLUE)
        ax.axhline(-44, color=AMBER, lw=0.9, ls=":")
        ax.axhline(-80, color=RED, lw=0.9, ls=":")
        ax.set_xticks(list(xs))
        ax.set_xticklabels(["per person", "per unit of GDP\n(volumes)", "per unit of GDP\n(current prices)"], fontsize=8.5)
        ax.set_title(f"Change 2005–{y}", fontsize=10, color=SLATE, loc="left")
        ax.set_ylim(-100, 0)
        ax.spines["bottom"].set_visible(False)
        ax.xaxis.tick_top()
        ax.tick_params(length=0)
    axs[0].legend(frameon=False, fontsize=8.5, loc="lower left")
    axs[0].set_ylabel("Change since 2005 (%)")
    axs[0].text(2.45, -43, "−44%", color=AMBER, fontsize=7.5, ha="right", va="bottom")
    axs[0].text(2.45, -79, "−80%", color=RED, fontsize=7.5, ha="right", va="bottom")
    fig.tight_layout()
    fig.savefig(OUT / "fig2_bars.png", bbox_inches="tight", facecolor="white")


if __name__ == "__main__":
    fig1(); fig2()
