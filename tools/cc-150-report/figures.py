"""Figures for Claim Check 150 (run calc.py first)."""
import csv
import pathlib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[1]
D = ROOT / "data/cc-150"
OUT = HERE / "out"; OUT.mkdir(exist_ok=True)
for f in ["LiberationSans-Regular", "LiberationSans-Bold", "LiberationSans-Italic"]:
    fm.fontManager.addfont(f"/usr/share/fonts/truetype/liberation/{f}.ttf")
plt.rcParams.update({"font.family": "Liberation Sans", "axes.spines.top": False, "axes.spines.right": False,
                     "axes.edgecolor": "#8A9399", "axes.labelcolor": "#2B3A42", "xtick.color": "#2B3A42",
                     "ytick.color": "#2B3A42"})
GREEN, AMBER, RED, SLATE, GREY, PALE = "#14452F", "#E3A72F", "#B5483A", "#2B3A42", "#8A9399", "#C9D3CC"
rows = list(csv.DictReader(open(D / "five_year.csv")))


def fig1():
    five = [r for r in rows if 2020 <= int(r["year"]) <= 2024]
    tot = lambda k: sum(int(r[k]) for r in five) / 1000
    bars = [("Claim: “diverted …\naway from landfill”", 412, RED),
            ("Separately collected\n(gross, before rejects)", tot("separately_collected_recyclables_and_organic"), AMBER),
            ("Generated minus\nlandfilled", tot("generated_minus_landfilled"), GREY),
            ("Landfill below\nthe 2019 peak", tot("landfill_below_2019"), GREY),
            ("Recycled, recovered\nor reused", tot("recovered_or_recycled"), GREEN)]
    fig, ax = plt.subplots(figsize=(9.6, 3.9), dpi=220)
    for i, (l, v, c) in enumerate(bars):
        ax.bar(i, v, color=c, width=0.62)
        ax.text(i, v + 6, f"{v:,.0f}", ha="center", fontsize=8.5, color=SLATE)
    ax.set_xticks(range(len(bars))); ax.set_xticklabels([b[0] for b in bars], fontsize=8)
    ax.set_ylabel("Thousand tonnes over five years"); ax.set_ylim(0, 480)
    fig.text(0.01, -0.03, "Source: NSO, Municipal Waste: 2024 (NR 225/2025), Tables 1, 2 and 4; five years 2020–2024 (2025 not "
             "yet published). Claim: Minister for the Environment, 19 Jan 2026.", fontsize=7, color=GREY)
    fig.tight_layout(); fig.savefig(OUT / "fig1_five_year.png", bbox_inches="tight"); plt.close(fig)


def fig2():
    yrs = [int(r["year"]) for r in rows]
    fig, ax = plt.subplots(figsize=(9.6, 3.4), dpi=220)
    for k, c, l in [("landfill", RED, "Landfilled"), ("separately_collected_recyclables_and_organic", AMBER,
                                                      "Separately collected recyclables and organic"),
                    ("recovered_or_recycled", GREEN, "Recycled, recovered or reused")]:
        v = [int(r[k]) / 1000 for r in rows]
        ax.plot(yrs, v, color=c, lw=2.2, marker="o", ms=4, label=l)
        ax.text(yrs[-1] + 0.08, v[-1], f"{v[-1]:,.0f}", va="center", fontsize=8, color=c)
    ax.set_ylim(0, 340); ax.set_xlim(2018.7, 2024.6); ax.set_ylabel("Thousand tonnes a year")
    ax.legend(fontsize=7.5, frameon=False, loc="center left", bbox_to_anchor=(0.0, 0.62))
    fig.text(0.01, -0.03, "Source: NSO, Municipal Waste: 2024 (NR 225/2025). Separately collected = paper, metals, glass, mixed "
             "packaging and organic.", fontsize=7, color=GREY)
    fig.tight_layout(); fig.savefig(OUT / "fig2_trend.png", bbox_inches="tight"); plt.close(fig)


fig1(); fig2()
