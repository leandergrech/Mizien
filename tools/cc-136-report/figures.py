"""Figures for Claim Check 136, drawn from data/cc-136/ and data/cc-013/ (run fetch.py first)."""
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


def fig1():
    latest = {}
    for r in csv.DictReader(open(ROOT / "data/cc-136/worldbank_density.csv")):
        if r["iso3"] not in latest or r["year"] > latest[r["iso3"]][0]:
            latest[r["iso3"]] = (r["year"], float(r["people_per_km2_land"]), r["country"])
    top = sorted(latest.values(), key=lambda x: -x[1])[:10]
    fig, axs = plt.subplots(1, 2, figsize=(9.6, 3.9), dpi=220, gridspec_kw={"width_ratios": [1, 1]})
    for ax, items, title in [(axs[0], top, "Ten densest European states (people per km²)"),
                             (axs[1], top[1:], "Same list without Monaco")]:
        names = [i[2] for i in items][::-1]
        vals = [i[1] for i in items][::-1]
        cols = [AMBER if n == "Malta" else "#C9D3CC" for n in names]
        ax.barh(names, vals, color=cols)
        for y, v in enumerate(vals):
            ax.text(v + max(vals) * 0.01, y, f"{v:,.0f}", va="center", fontsize=7.5, color=SLATE)
        ax.set_xlim(0, max(vals) * 1.15); ax.tick_params(axis="y", labelsize=8)
        ax.set_title(title, fontsize=9.5, color=SLATE, loc="left")
    fig.text(0.01, -0.04, "Source: World Bank EN.POP.DNST, 2024 (land area), 44 European states; retrieved 26 Oct 2026. "
             "Vatican City and Kosovo are not in the dataset.", fontsize=7, color=GREY)
    fig.tight_layout(); fig.savefig(OUT / "fig1_density.png", bbox_inches="tight", facecolor="white")


def fig2():
    pa = {int(r["year"]): int(r["approved_units_total"]) for r in csv.DictReader(open(ROOT / "data/cc-013/pa_approved_dwellings.csv"))}
    fig, ax = plt.subplots(figsize=(9.6, 3.5), dpi=220)
    yrs = sorted(pa)
    ax.bar(yrs, [pa[y] / 1000 for y in yrs], color=["#C9D3CC" if y != 2025 else AMBER for y in yrs])
    for y in (2013, 2018, 2024, 2025):
        ax.text(y, pa[y] / 1000 + 0.2, f"{pa[y]:,}", ha="center", fontsize=7.5, color=SLATE)
    ax.set_ylabel("Approved dwelling units (thousands)"); ax.set_xticks(yrs); ax.tick_params(axis="x", labelsize=7.5, rotation=45)
    ax.set_ylim(0, 14.5)
    ax.text(2007, -3.6, "Source: Planning Authority, Approved Dwelling Units 2007–2025 (as transcribed in data/cc-013/).",
            fontsize=7, color=GREY, clip_on=False)
    fig.savefig(OUT / "fig2_approvals.png", bbox_inches="tight", facecolor="white")


def fig3():
    pop = {int(r["year"]): float(r["population_1_jan"]) for r in csv.DictReader(open(ROOT / "data/cc-136/eurostat_demo_gind_jan.csv")) if r["geo"] == "MT"}
    fig, ax = plt.subplots(figsize=(9.6, 3.2), dpi=220)
    starts = list(range(2008, 2017))
    g = [100 * (pop[a + 10] / pop[a] - 1) for a in starts]
    ax.bar([f"{a}–{str(a + 10)[2:]}" for a in starts], g, color=[AMBER if x >= 28 else "#C9D3CC" for x in g])
    for i, x in enumerate(g):
        ax.text(i, x + 0.6, f"{x:.1f}%", ha="center", fontsize=7.5, color=SLATE)
    ax.axhline(30, color=RED, lw=0.9, ls=":"); ax.text(-0.4, 30.8, "“nearly 30 percent”", color=RED, fontsize=7.5)
    ax.set_ylim(0, 36); ax.set_ylabel("Growth over ten years"); ax.tick_params(axis="x", labelsize=7.5)
    ax.text(-0.4, -7.5, "Source: Eurostat demo_gind, population on 1 January, retrieved 26 Oct 2026.", fontsize=7, color=GREY, clip_on=False)
    fig.savefig(OUT / "fig3_population.png", bbox_inches="tight", facecolor="white")


if __name__ == "__main__":
    fig1(); fig2(); fig3()
