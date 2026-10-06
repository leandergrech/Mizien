"""Figures for Claim Check 029 (run fetch.py and calc.py first): fig1_timeline.png, fig2_share.png."""
import csv, pathlib, datetime as dt
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as md
from matplotlib import font_manager as fm
HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[1]
OUT = HERE / "out"; OUT.mkdir(exist_ok=True)
for f in ["LiberationSans-Regular", "LiberationSans-Bold", "LiberationSans-Italic"]:
    fm.fontManager.addfont(f"/usr/share/fonts/truetype/liberation/{f}.ttf")
plt.rcParams.update({"font.family": "Liberation Sans", "axes.spines.top": False, "axes.spines.right": False,
                     "axes.edgecolor": "#8A9399", "axes.labelcolor": "#2B3A42", "xtick.color": "#2B3A42", "ytick.color": "#2B3A42"})
GREEN, AMBER, GREY, BLUE, SLATE, ORANGE = "#14452F", "#E3A72F", "#8A9399", "#3C6E8F", "#2B3A42", "#D9772B"
D = dt.date
ev = [(D(2024, 12, 5), "PQQ issued", GREEN, 1), (D(2025, 3, 27), "Deadline extended\nto 21 Jul", GREEN, -1),
      (D(2025, 7, 22), "Three submissions\nannounced", GREEN, 1), (D(2026, 4, 22), "Metocean survey\ntender issued", GREEN, -1)]
fig, ax = plt.subplots(figsize=(9.6, 3.1), dpi=220)
ax.axvspan(D(2026, 1, 1), D(2026, 6, 30), color=AMBER, alpha=0.28, lw=0)
ax.text(D(2026, 3, 31), 1.55, "Stated plan: qualifying candidates\ninformed 'by the first part of 2026'", ha="center", fontsize=8.5, color=SLATE)
ax.axvline(D(2026, 10, 6), color=ORANGE, lw=1.4, ls="--")
ax.text(D(2026, 10, 3), -1.55, "6 Oct 2026\nno public notice\nof the next stage found", ha="right", fontsize=8, color=ORANGE)
ax.axhline(0, color=GREY, lw=1.2)
for d, lab, c, s in ev:
    ax.plot([d, d], [0, 0.55 * s], color=c, lw=1); ax.plot(d, 0, "o", color=c, ms=6)
    ax.text(d, 0.65 * s, lab, ha="center", va="bottom" if s > 0 else "top", fontsize=8.5, color=SLATE)
ax.set_ylim(-2.0, 2.2); ax.set_yticks([])
ax.set_xlim(D(2024, 11, 1), D(2026, 11, 15))
ax.xaxis.set_major_locator(md.MonthLocator(bymonth=[1, 4, 7, 10])); ax.xaxis.set_major_formatter(md.DateFormatter("%b\n%Y"))
ax.spines["left"].set_visible(False)
fig.savefig(OUT / "fig1_timeline.png", bbox_inches="tight", facecolor="white")
plt.close(fig)
c = {r["check"]: float(r["value"]) for r in csv.DictReader(open(ROOT / "data/cc-029/checks.csv")) if r["unit"] == "GWH" or r["unit"] == "GWh"}
sup = c["Electricity supplied (production + imports - exports) 2025"]; fc = c["Final electricity consumption 2025"]
fig, ax = plt.subplots(figsize=(9.6, 2.5), dpi=220)
labs = ["Electricity supplied, 2025", "Final consumption, 2025", "Wind farm output (ICM: up to 0.8 TWh)"]
vals = [sup, fc, 800]; cols = [GREY, BLUE, GREEN]
ax.barh(labs[::-1], vals[::-1], color=cols[::-1], height=0.55)
for i, val in enumerate(vals[::-1]):
    ax.text(val + 30, i, f"{val:,.0f} GWh", va="center", fontsize=9, fontweight="bold", color=SLATE)
ax.set_xlim(0, 3900); ax.set_xlabel("GWh a year")
ax.text(0, -1.0, "Eurostat nrg_cb_e (electricity; 2025 provisional), retrieved 6 Oct 2026. Supplied = production + imports - exports. "
        "Output figure: InterConnect Malta project page.", fontsize=7, color=GREY, clip_on=False)
fig.savefig(OUT / "fig2_share.png", bbox_inches="tight", facecolor="white")
