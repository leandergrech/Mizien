"""Figures for Claim Check 071 (run calc.py first): fig1_payments.png, fig2_cars.png."""
import csv, pathlib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[1]
OUT = HERE / "out"; OUT.mkdir(exist_ok=True)
for f in ["LiberationSans-Regular", "LiberationSans-Bold", "LiberationSans-Italic"]:
    fm.fontManager.addfont(f"/usr/share/fonts/truetype/liberation/{f}.ttf")
plt.rcParams.update({"font.family": "Liberation Sans", "axes.spines.top": False, "axes.spines.right": False,
                     "axes.edgecolor": "#8A9399"})
GREEN, AMBER, GREY, SLATE, ORANGE = "#14452F", "#E3A72F", "#8A9399", "#2B3A42", "#D9772B"

# ---- Figure 1: payments to the bus operator, as reported (all second-hand)
rows = list(csv.DictReader(open(ROOT / "data" / "cc-071" / "subsidy_series.csv")))
yrs = [r["year"] for r in rows]; vals = [float(r["payments_eur_million"]) for r in rows]
fig, ax = plt.subplots(figsize=(9.0, 3.4), dpi=220)
bars = ax.bar(yrs, vals, color=[GREY] * 4 + [AMBER], width=0.6)
for b, v in zip(bars, vals):
    ax.text(b.get_x() + b.get_width() / 2, v + 1.8, f"{v:g}", ha="center", fontsize=8.5, color=SLATE)
ax.axhline(100, color=ORANGE, lw=1.1, ls="--")
ax.text(-0.45, 101.5, "EUR 100 million (the headline figure)", fontsize=8, color=ORANGE, va="bottom")
ax.axvline(1.5, color=GREY, lw=0.9, ls=":")
ax.text(1.55, 108, "free travel from\n1 October 2022", fontsize=7.6, color=GREY, va="top")
ax.set_ylim(0, 112); ax.set_ylabel("EUR million", fontsize=8.5, color=SLATE)
ax.tick_params(labelsize=8.5, colors=SLATE)
fig.savefig(OUT / "fig1_payments.png", bbox_inches="tight", facecolor="white")
plt.close(fig)

# ---- Figure 2: cars and population, index 2019 = 100
rows = list(csv.DictReader(open(ROOT / "data" / "cc-071" / "cars_population.csv")))
y = [int(r["year"]) for r in rows]
c = [int(r["passenger_cars_31dec"]) for r in rows]; p = [int(r["population_1jan"]) for r in rows]
ci = [v / c[0] * 100 for v in c]; pi = [v / p[0] * 100 for v in p]
fig, ax = plt.subplots(figsize=(9.0, 3.4), dpi=220)
ax.plot(y, pi, color=GREY, lw=2, marker="o", ms=4)
ax.plot(y, ci, color=GREEN, lw=2.2, marker="o", ms=4)
ax.text(y[-1] + 0.08, pi[-1], f"Population {pi[-1]:.0f}", fontsize=8.5, color=GREY, va="center")
ax.text(y[-1] + 0.08, ci[-1], f"Passenger cars {ci[-1]:.0f}", fontsize=8.5, color=GREEN, va="center")
ax.axvline(2022.75, color=ORANGE, lw=1, ls=":")
ax.text(2022.8, 99, "free buses from\nOct 2022", fontsize=7.6, color=ORANGE, va="bottom")
ax.set_xlim(2018.8, 2026.6); ax.set_ylim(96, 122)
ax.set_ylabel("Index, 2019 = 100", fontsize=8.5, color=SLATE)
ax.tick_params(labelsize=8.5, colors=SLATE)
fig.savefig(OUT / "fig2_cars.png", bbox_inches="tight", facecolor="white")
plt.close(fig)
print("ok")
