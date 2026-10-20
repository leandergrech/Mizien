"""Figure for Claim Check 129: timeline of the NAPCP update (data/cc-129/timeline.csv, checks by calc.py)."""
import pathlib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as md
import datetime as dt
from matplotlib import font_manager as fm

HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE / "out"
OUT.mkdir(exist_ok=True)
for f in ["LiberationSans-Regular", "LiberationSans-Bold", "LiberationSans-Italic"]:
    fm.fontManager.addfont(f"/usr/share/fonts/truetype/liberation/{f}.ttf")
plt.rcParams.update({"font.family": "Liberation Sans", "axes.spines.top": False, "axes.spines.right": False,
                     "axes.spines.left": False, "axes.edgecolor": "#8A9399"})
GREEN, AMBER, RED, SLATE, GREY = "#14452F", "#E3A72F", "#B5483A", "#2B3A42", "#8A9399"
D = dt.date


def fig1():
    fig, ax = plt.subplots(figsize=(9.6, 3.6), dpi=220)
    ax.axhline(0, color=SLATE, lw=1.2)
    ev = [(D(2019, 4, 1), "1 Apr 2019\nfirst programmes due", GREEN, 1.0, False),
          (D(2023, 4, 1), "1 Apr 2023\nupdate due (reading A)", AMBER, 1.0, False),
          (D(2024, 3, 1), "Mar 2024\nupdate due (reading B)\n* month only", AMBER, -1.0, True),
          (D(2025, 7, 17), "17 Jul 2025\nletter of formal notice\nINFR(2025)2088", RED, 1.0, False),
          (D(2026, 6, 1), "Jun 2026\ndraft update consulted\n* month only", GREY, -1.0, True)]
    for d, t, c, y, hollow in ev:
        ax.plot([d, d], [0, y * 0.55], color=c, lw=1.2)
        ax.scatter([d], [0], s=70, color="white" if hollow else c, edgecolor=c, zorder=3, lw=1.6)
        ax.text(d, y * 0.62, t, ha="center", va="bottom" if y > 0 else "top", fontsize=8.2, color=SLATE)
    ax.axvspan(D(2023, 4, 1), D(2025, 7, 17), ymin=0.47, ymax=0.53, color=AMBER, alpha=0.5)
    ax.set_ylim(-1.8, 1.9); ax.set_yticks([])
    ax.set_xlim(D(2018, 9, 1), D(2027, 3, 1))
    ax.xaxis.set_major_locator(md.YearLocator()); ax.xaxis.set_major_formatter(md.DateFormatter("%Y"))
    ax.text(D(2018, 9, 1), -2.25, "Sources: Directive 2016/2284 Art. 6(3), 10(1); Commission, 17 Jul 2025; * second-hand (ERA listing, Malta News Agency). Amber bar: overdue under reading A.",
            fontsize=7, color=GREY, clip_on=False)
    fig.savefig(OUT / "fig1_timeline.png", bbox_inches="tight", facecolor="white")


if __name__ == "__main__":
    fig1()
