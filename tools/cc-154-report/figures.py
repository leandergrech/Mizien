"""Figure for Claim Check 154: fig1_timeline.png (October to November 2025)."""
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
GREEN, GREY, BLUE, SLATE, ORANGE = "#14452F", "#8A9399", "#3C6E8F", "#2B3A42", "#D9772B"
D = dt.date
# (date, label, colour, side, height, x offset in days)
ev = [(D(2025, 10, 15), "15 Oct\nCommissioner meets\nthe Minister", BLUE, 1, 0.9, -1.2),
      (D(2025, 10, 17), "17 Oct\nNew 'research\nderogation' adopted", ORANGE, -1, 0.9, -0.5),
      (D(2025, 10, 24), "24 Oct\nLetter e-signed\n(Italpress: 27 Oct)", GREEN, 1, 2.0, 0),
      (D(2025, 11, 1), "1 Nov\nBirdLife Malta\nposts the letter", BLUE, -1, 0.9, 0),
      (D(2025, 11, 2), "2 Nov\nItalpress\nreport", BLUE, 1, 0.9, 1.6),
      (D(2025, 11, 21), "21 Nov\nNew formal notice\nINFR(2025)2128\n(second-hand)", GREY, -1, 0.9, 0)]
fig, ax = plt.subplots(figsize=(9.6, 3.2), dpi=220)
ax.axhline(0, color=GREY, lw=1.2)
for d, lab, c, s, h, xo in ev:
    x = md.date2num(d)
    ax.plot([x, x], [0, h * s], color=c, lw=1); ax.plot(x, 0, "o", color=c, ms=6)
    ax.text(x + xo, (h + 0.1) * s, lab, ha="center", va="bottom" if s > 0 else "top", fontsize=8.5, color=SLATE)
ax.set_ylim(-2.6, 3.6); ax.set_yticks([]); ax.spines["left"].set_visible(False)
ax.set_xlim(md.date2num(D(2025, 10, 11)), md.date2num(D(2025, 11, 26)))
ax.xaxis.set_major_locator(md.DayLocator(interval=5)); ax.xaxis.set_major_formatter(md.DateFormatter("%d %b"))
ax.set_xlabel("2025", color=SLATE)
fig.savefig(OUT / "fig1_timeline.png", bbox_inches="tight", facecolor="white")
