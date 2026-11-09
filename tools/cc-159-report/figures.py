"""Figures for Claim Check 159, drawn from data/cc-159/ (run fetch.py and calc.py first)."""
import csv, pathlib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[1]
D = ROOT / "data/cc-159"
OUT = HERE / "out"; OUT.mkdir(exist_ok=True)
for f in ["LiberationSans-Regular", "LiberationSans-Bold", "LiberationSans-Italic"]:
    fm.fontManager.addfont(f"/usr/share/fonts/truetype/liberation/{f}.ttf")
plt.rcParams.update({"font.family": "Liberation Sans", "axes.spines.top": False, "axes.spines.right": False,
                     "axes.edgecolor": "#8A9399", "axes.labelcolor": "#2B3A42", "xtick.color": "#2B3A42",
                     "ytick.color": "#2B3A42"})
GREEN, AMBER, RED, SLATE, GREY = "#14452F", "#E3A72F", "#B5483A", "#2B3A42", "#8A9399"
checks = {r["check"]: r for r in csv.DictReader(open(D / "checks.csv"))}


def fig1():
    dens = {(r["geo"], int(r["year"])): float(r["value_per_km2"]) for r in csv.DictReader(open(D / "eurostat_demo_r_d3dens.csv"))}
    ys = sorted(y for g, y in dens if g == "MT")
    ratio = [dens[("MT", y)] / dens[("EU27_2020", y)] for y in ys]
    fig, ax = plt.subplots(figsize=(9.6, 3.4), dpi=220)
    ax.bar([str(y) for y in ys], ratio, color=[AMBER if y == ys[-1] else "#C9D3CC" for y in ys])
    for i, v in enumerate(ratio):
        ax.text(i, v + 0.25, f"{v:.1f}", ha="center", fontsize=8, color=SLATE)
    ax.axhline(15, color=RED, lw=0.9, ls=":"); ax.text(-0.45, 15.3, "“fifteen times”", color=RED, fontsize=8)
    ax.set_ylim(0, 19); ax.set_ylabel("Malta ÷ EU-27 density (times)")
    fig.text(0.01, -0.07, "Source: Eurostat demo_r_d3dens (people per km² of total area; EU-27 aggregate flagged provisional/estimated), "
            "retrieved 9 Nov 2026.", fontsize=7, color=GREY, clip_on=False)
    fig.savefig(OUT / "fig1_ratio_years.png", bbox_inches="tight", facecolor="white")


def fig2():
    g = lambda k: float(checks[k]["value"])
    items = [("EU-27 aggregate, 2024 (Eurostat)", g("Eurostat 2024: Malta / EU-27 aggregate density")),
             ("EU-27 excluding Malta, 1 Jan 2025 (Eurostat)", g("Malta 1 Jan 2025 / EU-27 excluding Malta")),
             ("Median of 26 other states, 2024 (Eurostat)", g("Eurostat 2024: Malta / median other state")),
             ("Mean of 26 other states, 2024 (Eurostat)", g("Eurostat 2024: Malta / unweighted mean of the 26 other states")),
             ("Median of other EU states, 2024 (World Bank, land)", g("World Bank 2024: Malta / median other EU state")),
             ("Mean of other EU states, 2024 (World Bank, land)", g("World Bank 2024: Malta / unweighted mean of other EU states"))]
    fig, ax = plt.subplots(figsize=(9.6, 3.3), dpi=220)
    names = [i[0] for i in items][::-1]; vals = [i[1] for i in items][::-1]
    ax.barh(names, vals, color=[AMBER if "aggregate" in n else "#C9D3CC" for n in names])
    for y, v in enumerate(vals):
        ax.text(v + 0.2, y, f"{v:.1f}×", va="center", fontsize=8, color=SLATE)
    ax.axvline(15, color=RED, lw=0.9, ls=":"); ax.text(15.1, len(items) - 0.45, "15", color=RED, fontsize=8)
    ax.set_xlim(0, 20); ax.tick_params(axis="y", labelsize=8)
    fig.text(0.01, -0.07, "Sources: Eurostat demo_r_d3dens, demo_gind, reg_area3; World Bank EN.POP.DNST; retrieved 9 Nov 2026. "
            "Malta ÷ comparator.", fontsize=7, color=GREY, clip_on=False)
    fig.savefig(OUT / "fig2_ratio_bases.png", bbox_inches="tight", facecolor="white")


def fig3():
    pop = {int(r["year"]): float(r["population_1_jan"]) for r in csv.DictReader(open(D / "eurostat_demo_gind_jan.csv")) if r["geo"] == "MT"}
    imf = {2022: 520, 2023: 542, 2024: 553, 2025: 563, 2026: 573}
    ys = list(imf)
    fig, ax = plt.subplots(figsize=(9.6, 3.0), dpi=220)
    w = 0.38
    ax.bar([i - w / 2 for i in range(5)], [pop[y] / 1000 for y in ys], w, color="#C9D3CC", label="Eurostat, 1 January")
    ax.bar([i + w / 2 for i in range(5)], [imf[y] for y in ys], w, color=AMBER, label="IMF Table 1 (2024 onwards: staff estimates and projections)")
    for i, y in enumerate(ys):
        ax.text(i - w / 2, pop[y] / 1000 + 4, f"{pop[y] / 1000:.0f}", ha="center", fontsize=7.5, color=SLATE)
        ax.text(i + w / 2, imf[y] + 4, f"{imf[y]}", ha="center", fontsize=7.5, color=SLATE)
    ax.set_xticks(range(5)); ax.set_xticklabels([str(y) for y in ys]); ax.set_ylim(400, 640)
    ax.set_ylabel("Population (thousands)"); ax.legend(fontsize=7.5, frameon=False, loc="upper left")
    fig.text(0.01, -0.07, "Sources: IMF Country Report 26/29, Table 1; Eurostat demo_gind, retrieved 9 Nov 2026. Axis starts at 400.",
            fontsize=7, color=GREY, clip_on=False)
    fig.savefig(OUT / "fig3_population.png", bbox_inches="tight", facecolor="white")


if __name__ == "__main__":
    fig1(); fig2(); fig3()
