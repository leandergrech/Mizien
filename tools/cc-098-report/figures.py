"""Figure for Claim Check 098: fig1_timeline.png (dated public record, 14 to 25 Jun 2026)."""
import pathlib, datetime as dt
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as md
from matplotlib import font_manager as fm
HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE / "out"; OUT.mkdir(exist_ok=True)
for f in ["LiberationSans-Regular", "LiberationSans-Bold", "LiberationSans-Italic"]:
    fm.fontManager.addfont(f"/usr/share/fonts/truetype/liberation/{f}.ttf")
plt.rcParams.update({"font.family": "Liberation Sans", "axes.spines.top": False, "axes.spines.right": False,
                     "axes.edgecolor": "#8A9399", "xtick.color": "#2B3A42"})
GREEN, AMBER, GREY, BLUE, SLATE, ORANGE = "#14452F", "#E3A72F", "#8A9399", "#3C6E8F", "#2B3A42", "#D9772B"
D = dt.date
ev = [(D(2026, 6, 14), "14 Jun\nIncident filmed\n(NGO's account)", BLUE, 1),
      (D(2026, 6, 24), "24 Jun\nNGO releases video;\nPN asks for answers", GREEN, 1),
      (D(2026, 6, 24), "24 Jun\nMinistry/MTA: area is\npublic land (TVM News)", GREEN, -1),
      (D(2026, 6, 25), "25 Jun\nPM: 'isolated episode',\narea 'not public' (Newsbook)", ORANGE, 1)]
fig, ax = plt.subplots(figsize=(9.6, 3.0), dpi=220)
ax.axhline(0, color=GREY, lw=1.2)
xo = {0: 0, 1: -0.5, 2: -0.5, 3: 1.0}   # label offsets only; markers stay on their dates
for i, (d, lab, c, s) in enumerate(ev):
    x = md.date2num(d)
    h = 0.55 if i != 3 else 1.35
    ax.plot([x, x], [0, h * s], color=c, lw=1); ax.plot(x, 0, "o", color=c, ms=6)
    ax.text(x + xo[i], (h + 0.1) * s, lab, ha="center", va="bottom" if s > 0 else "top", fontsize=8.5, color=SLATE)
ax.set_ylim(-2.3, 2.9); ax.set_yticks([]); ax.spines["left"].set_visible(False)
ax.set_xlim(md.date2num(D(2026, 6, 10)), md.date2num(D(2026, 6, 29)))
ax.xaxis.set_major_locator(md.DayLocator(interval=2)); ax.xaxis.set_major_formatter(md.DateFormatter("%d"))
ax.set_xlabel("June 2026", color=SLATE)
fig.savefig(OUT / "fig1_timeline.png", bbox_inches="tight", facecolor="white")
