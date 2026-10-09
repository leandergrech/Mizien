"""Figures for Claim Check 065 (run calc.py first): fig1_timeline.png, fig2_margins.png."""
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
                     "axes.edgecolor": "#8A9399"})
GREEN, AMBER, GREY, SLATE, ORANGE = "#14452F", "#E3A72F", "#8A9399", "#2B3A42", "#D9772B"
D = dt.date

# ---- Figure 1: timeline of application PA/00570/21
ev = [(D(2023, 11, 9), "9 Nov 2023\nfirst approval\n(no heritage\nassessment)", GREY, 1, 0.8),
      (D(2024, 3, 7), "7 Mar 2024\npermit revoked;\nPA: wrong buffer-zone\ninformation given", GREEN, -1, 0.8),
      (D(2026, 2, 15), "Feb 2026\nheritage impact\nassessment\ncompleted", GREY, 1, 2.1),
      (D(2026, 3, 12), "Mar 2026 (Shift, 12 Mar)\nboard adjourns\nsix weeks", GREY, -1, 1.5),
      (D(2026, 4, 30), "30 Apr 2026\nboard approves,\n10 to 1", GREEN, 1, 0.7),
      (D(2026, 5, 2), "2 May\nADPD statement", ORANGE, -1, 0.8)]
fig, ax = plt.subplots(figsize=(9.6, 3.6), dpi=220)
ax.axhline(0, color=GREY, lw=1.2)
for d, lab, c, s, h in ev:
    ax.plot([d, d], [0, h * s], color=c, lw=1); ax.plot(d, 0, "o", color=c, ms=6)
    ax.text(d + dt.timedelta(days={"30 Apr":-3}.get(lab[:6], 0)), (h + 0.08) * s, lab, ha="left" if lab.startswith("30 Apr") else ("left" if lab.startswith("13 Jun") else "center"), va="bottom" if s > 0 else "top", fontsize=7.6, color=SLATE)
ax.set_ylim(-3.0, 4.6); ax.set_yticks([])
ax.set_xlim(D(2023, 8, 1), D(2026, 9, 15))
ax.xaxis.set_major_locator(md.MonthLocator(bymonth=[1, 7])); ax.xaxis.set_major_formatter(md.DateFormatter("%b %Y"))
ax.spines["left"].set_visible(False)
fig.savefig(OUT / "fig1_timeline.png", bbox_inches="tight", facecolor="white")
plt.close(fig)

# ---- Figure 2: how far the buffer zone extends from the temple edge, by direction (from the management plan's map)
rows = list(csv.DictReader(open(ROOT / "data" / "cc-065" / "margins.csv")))
names = [r["direction"] for r in rows]; vals = [int(r["margin_m"]) for r in rows]
fig, ax = plt.subplots(figsize=(9.0, 3.4), dpi=220)
cols = [GREEN if v >= 157 else AMBER for v in vals]
ax.axvspan(150, 157, color=ORANGE, alpha=0.35, lw=0)
ax.barh(names[::-1], vals[::-1], color=cols[::-1], height=0.62)
for y, v in enumerate(vals[::-1]): ax.text(515, y, f"{v} m", va="center", ha="right", fontsize=8, color=SLATE)
ax.text(153.5, len(vals) - 0.35, "reported distance of the site, 150\u2013157 m", ha="left", va="bottom", fontsize=7.8, color=ORANGE)
ax.axvline(100, color=GREY, lw=1.1, ls=":")
ax.text(103, -0.95, "100 m minimum radius (management plan)", ha="left", va="center", fontsize=7.6, color=GREY)
ax.set_xlim(0, 520); ax.set_ylim(-1.4, len(vals) + 0.9)
ax.set_xlabel("Metres from the edge of the temple site to the buffer-zone boundary, measured on the plan's map", fontsize=8, color=SLATE)
ax.tick_params(labelsize=8, colors=SLATE)
fig.savefig(OUT / "fig2_margins.png", bbox_inches="tight", facecolor="white")
plt.close(fig)
print("ok")
