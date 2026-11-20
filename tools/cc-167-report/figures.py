"""Figures for Claim Check 167 (run calc.py first)."""
import csv
import pathlib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[1]
D = ROOT / "data/cc-167"
OUT = HERE / "out"; OUT.mkdir(exist_ok=True)
for f in ["LiberationSans-Regular", "LiberationSans-Bold", "LiberationSans-Italic"]:
    fm.fontManager.addfont(f"/usr/share/fonts/truetype/liberation/{f}.ttf")
plt.rcParams.update({"font.family": "Liberation Sans", "axes.spines.top": False, "axes.spines.right": False,
                     "axes.edgecolor": "#8A9399", "axes.labelcolor": "#2B3A42", "xtick.color": "#2B3A42",
                     "ytick.color": "#2B3A42"})
GREEN, AMBER, RED, SLATE, GREY, PALE = "#14452F", "#E3A72F", "#B5483A", "#2B3A42", "#8A9399", "#C9D3CC"
rows = list(csv.DictReader(open(D / "eurostat_malta_energy_gdp.csv")))
chk = {r["check"]: float(r["value"]) for r in csv.DictReader(open(D / "checks.csv")) if r["unit"] == "%"}


def fig1():
    bars = [("Published indicator\n(incl. ship bunkers)", chk["Energy intensity of GDP (published, GAE/GDP, CLV10), 2019-2024"], RED),
            ("Excluding bunkers\n(gross inland)", chk["Gross inland consumption per GDP, 2019-2024"], AMBER),
            ("Final energy\nper GDP", chk["Final energy per GDP, 2019-2024"], AMBER),
            ("EU-27, published\nindicator", chk["EU-27 energy intensity (published), 2019-2024"], GREY),
            ("Final energy\nper person", chk["Final energy per person, 2019-2024"], GREEN)]
    fig, ax = plt.subplots(figsize=(9.6, 3.8), dpi=220)
    for i, (l, v, c) in enumerate(bars):
        ax.bar(i, v, color=c, width=0.6)
        ax.text(i, v - 1.2, f"{v:+.1f}%", ha="center", va="top", fontsize=8.5, color=SLATE)
    ax.axhline(0, color=GREY, lw=0.8)
    ax.set_xticks(range(len(bars))); ax.set_xticklabels([b[0] for b in bars], fontsize=8)
    ax.set_ylim(-32, 3); ax.set_ylabel("Change 2019–2024, %")
    fig.text(0.01, -0.03, "Source: Eurostat nrg_ind_ei, nrg_bal_s, nama_10_gdp, demo_gind (retrieved 17 Nov 2026). Ratios other than "
             "the published indicators use current GDP.", fontsize=7, color=GREY)
    fig.tight_layout(); fig.savefig(OUT / "fig1_change.png", bbox_inches="tight"); plt.close(fig)


def fig2():
    yrs = [int(r["year"]) for r in rows]
    base = next(r for r in rows if r["year"] == "2019")
    fig, ax = plt.subplots(figsize=(9.6, 3.6), dpi=220)
    for k, c, l in [("gdp_clv10_meur", GREEN, "Real GDP"), ("final_energy_ktoe", AMBER, "Final energy consumption"),
                    ("gic_ktoe", SLATE, "Gross inland consumption (excl. bunkers)"),
                    ("intl_maritime_bunkers_ktoe", RED, "International maritime bunkers")]:
        v = [100 * float(r[k]) / float(base[k]) for r in rows]
        ax.plot(yrs, v, color=c, lw=2, marker="o", ms=3, label=l)
        ax.text(yrs[-1] + 0.1, v[-1], f"{v[-1]:.0f}", va="center", fontsize=8, color=c)
    ax.axhline(100, color=PALE, lw=0.8); ax.set_ylabel("Index, 2019 = 100"); ax.set_xlim(2014.7, 2024.7)
    ax.legend(fontsize=7.5, frameon=False, loc="upper left")
    fig.text(0.01, -0.03, "Source: Eurostat nrg_bal_s and nama_10_gdp (chain-linked 2010 volumes).", fontsize=7, color=GREY)
    fig.tight_layout(); fig.savefig(OUT / "fig2_index.png", bbox_inches="tight"); plt.close(fig)


fig1(); fig2()
