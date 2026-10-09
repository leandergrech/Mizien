"""Figure for Claim Check 055 (run calc.py first): fig1_timeline.png."""
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
                     "axes.edgecolor": "#8A9399"})
GREEN, AMBER, GREY, SLATE, ORANGE = "#14452F", "#E3A72F", "#8A9399", "#2B3A42", "#D9772B"
D = dt.date
# (date, label, colour, side, height): the facts are green; later events that bear on the park are grey
ev = [(D(2026, 3, 17), "17 Mar\nin-principle deal\n(MIDI, TVM)", GREEN, 1, 0.7),
      (D(2026, 3, 20), "20 Mar\nterms of deed\nagreed (MIDI)", GREEN, -1, 0.7),
      (D(2026, 4, 28), "28 Apr\nshareholders\napprove (MIDI)", GREEN, 1, 1.5),
      (D(2026, 5, 13), "13 May\npublic deed:\nreturn to Government\n(MIDI); Abela's\npark statement", GREEN, -1, 1.5),
      (D(2026, 5, 30), "30 May\ngeneral\nelection", GREY, 1, 0.7),
      (D(2026, 7, 16), "16 Jul\nPA sanctions padel\ncourts on the island\n(Lovin Malta)", GREY, -1, 0.7),
      (D(2026, 7, 21), "21 Jul\nPM on yacht marina\nconcession (Lovin\nMalta, via MaltaToday)", GREY, 1, 1.5)]
fig, ax = plt.subplots(figsize=(9.6, 3.9), dpi=220)
ax.axhline(0, color=GREY, lw=1.2)
for d, lab, c, s, h in ev:
    ax.plot([d, d], [0, h * s], color=c, lw=1); ax.plot(d, 0, "o", color=c, ms=6)
    ax.text(d, (h + 0.08) * s, lab, ha="center", va="bottom" if s > 0 else "top", fontsize=7.6, color=SLATE)
ax.axvline(D(2026, 10, 9), color=ORANGE, lw=1.4, ls="--")
ax.text(D(2026, 10, 6), -1.0, "9 Oct 2026\nno park law, plan or\nlocal plan change\nfound in sources searched", ha="right", fontsize=7.6, color=ORANGE)
ax.set_ylim(-3.2, 3.2); ax.set_yticks([])
ax.set_xlim(D(2026, 2, 15), D(2026, 10, 20))
ax.xaxis.set_major_locator(md.MonthLocator()); ax.xaxis.set_major_formatter(md.DateFormatter("%b"))
ax.spines["left"].set_visible(False)
fig.savefig(OUT / "fig1_timeline.png", bbox_inches="tight", facecolor="white")
plt.close(fig)
print("ok")
