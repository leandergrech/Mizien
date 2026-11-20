"""Figures for Claim Check 141 (run calc.py first)."""
import csv
import pathlib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[1]
D = ROOT / "data/cc-141"
OUT = HERE / "out"; OUT.mkdir(exist_ok=True)
for f in ["LiberationSans-Regular", "LiberationSans-Bold", "LiberationSans-Italic"]:
    fm.fontManager.addfont(f"/usr/share/fonts/truetype/liberation/{f}.ttf")
plt.rcParams.update({"font.family": "Liberation Sans", "axes.spines.top": False, "axes.spines.right": False,
                     "axes.edgecolor": "#8A9399", "axes.labelcolor": "#2B3A42", "xtick.color": "#2B3A42",
                     "ytick.color": "#2B3A42"})
GREEN, AMBER, RED, SLATE, GREY, PALE = "#14452F", "#E3A72F", "#B5483A", "#2B3A42", "#8A9399", "#C9D3CC"
rows = [r for r in csv.DictReader(open(D / "eurostat_demo_find_tfr.csv")) if r["tfr"]]
NAMES = {"MT": "Malta", "ES": "Spain", "IT": "Italy", "LT": "Lithuania", "EU27_2020": "EU-27"}


def series(g):
    s = [(int(r["year"]), float(r["tfr"])) for r in rows if r["geo"] == g]
    return [x for x, _ in s], [y for _, y in s]


def fig1():
    fig, ax = plt.subplots(figsize=(9.6, 4.4), dpi=220)
    others = sorted({r["geo"] for r in rows} - set(NAMES))
    for g in others:
        x, y = series(g)
        ax.plot(x, y, color=PALE, lw=0.8, zorder=1)
    for g, c, lw in [("EU27_2020", SLATE, 1.6), ("ES", AMBER, 1.6), ("IT", GREY, 1.4), ("LT", "#7A9A86", 1.4),
                     ("MT", RED, 2.6)]:
        x, y = series(g)
        ax.plot(x, y, color=c, lw=lw, zorder=3, label=NAMES[g])
    ax.scatter([2024], [1.34], marker="o", facecolor="white", edgecolor=SLATE, zorder=4, s=28)
    ax.annotate("EU-27 2024: 1.34\n(Statistics Explained)", (2024, 1.34), xytext=(2019.6, 1.43), fontsize=7.5,
                color=SLATE, arrowprops=dict(arrowstyle="-", color=GREY, lw=0.6))
    ax.axvspan(2016.5, 2024.5, color="#F6E9E6", zorder=0)
    ax.text(2016.7, 2.02, "Malta lowest\nevery year", fontsize=7.5, color=RED, va="top")
    ax.set_xlim(2000, 2024.8); ax.set_ylabel("Total fertility rate (live births per woman)")
    ax.legend(fontsize=7.5, frameon=False, loc="upper right", bbox_to_anchor=(0.86, 1.0), ncol=5)
    fig.text(0.01, -0.03, "Source: Eurostat demo_find (updated 13 Nov 2026). Grey lines: the other Member States. "
             "EU-27 2022–2023 not published in the table.", fontsize=7, color=GREY)
    fig.tight_layout(); fig.savefig(OUT / "fig1_trend.png", bbox_inches="tight"); plt.close(fig)


def fig2():
    v = {r["geo"]: float(r["tfr"]) for r in rows if r["year"] == "2024" and r["geo"] != "EU27_2020"}
    order = sorted(v, key=lambda g: v[g])
    fig, ax = plt.subplots(figsize=(9.6, 3.6), dpi=220)
    ax.bar(range(len(order)), [v[g] for g in order], color=[RED if g == "MT" else PALE for g in order])
    for i, g in enumerate(order):
        ax.text(i, v[g] + 0.02, f"{v[g]:.2f}", ha="center", fontsize=6.3, color=SLATE, rotation=90)
    ax.axhline(1.34, color=SLATE, lw=0.8, ls="--")
    ax.text(len(order) - 0.5, 1.36, "EU-27 1.34", ha="right", fontsize=7.5, color=SLATE)
    ax.set_xticks(range(len(order))); ax.set_xticklabels(order, fontsize=7.5)
    ax.set_ylim(0, 2.0); ax.set_ylabel("Total fertility rate, 2024")
    fig.text(0.01, -0.03, "Source: Eurostat demo_find (updated 13 Nov 2026); EU-27 from Eurostat, Fertility statistics.",
             fontsize=7, color=GREY)
    fig.tight_layout(); fig.savefig(OUT / "fig2_2024.png", bbox_inches="tight"); plt.close(fig)


fig1(); fig2()
