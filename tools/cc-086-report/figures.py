"""Figure for Claim Check 086: timeline of statements, drawn from data/cc-086/statements.csv."""
import csv
import datetime as dt
import pathlib

import matplotlib
matplotlib.use("Agg")
import matplotlib.dates as mdates  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib import font_manager as fm  # noqa: E402

HERE = pathlib.Path(__file__).resolve().parent
D = HERE.parents[1] / "data" / "cc-086"
OUT = HERE / "out"
OUT.mkdir(exist_ok=True)
for f in ["LiberationSans-Regular", "LiberationSans-Bold", "LiberationSans-Italic"]:
    fm.fontManager.addfont(f"/usr/share/fonts/truetype/liberation/{f}.ttf")
plt.rcParams.update({"font.family": "Liberation Sans"})
GREEN, AMBER, RED, SLATE, GREY, BLUE = "#14452F", "#E3A72F", "#B5483A", "#2B3A42", "#8A9399", "#3C6E8F"
d = lambda s: dt.datetime.strptime(s, "%Y-%m-%d")

fig, ax = plt.subplots(figsize=(9.6, 3.1), dpi=220)
ax.axhline(0, color=GREY, lw=1)
ax.axvspan(d("2026-06-01"), d("2026-08-31"), color="#FBF1D9", zorder=0)
ax.text(d("2026-07-16"), -1.45, "summer 2026 (1 Jun – 31 Aug)", ha="center", va="center", fontsize=7.6, color=SLATE)
ev = [("2025-03-03", 0.62, BLUE, "3 Mar 2025\nMinister: ‘around 11 kiosks,\nbut this might be too many’"),
      ("2025-04-14", -0.62, GREEN, "14 Apr 2025\nMinister: ‘starting in the summer\nof 2026, everyone will have to compete’"),
      ("2026-02-08", 0.62, RED, "8 Feb 2026\nMTA: no competitive tenders\nthis summer; ‘will have to wait\nuntil we have the permit’"),
      ("2026-06-24", -0.62, RED, "24 Jun 2026\nThe Shift: no tender reported;\nkiosks still without permits"),
      ("2026-10-12", 0.62, SLATE, "12 Oct 2026\nThis check: no tender\nfound")]
for ds, y, col, txt in ev:
    ax.plot([d(ds), d(ds)], [0, y * 0.78], color=col, lw=1.2)
    ax.plot([d(ds)], [0], marker="o", ms=7, color=col)
    ax.text(d(ds), y, txt, ha="center", va="bottom" if y > 0 else "top", fontsize=7.4, color=col, linespacing=1.25)
ax.set_ylim(-1.55, 1.55)
ax.set_xlim(d("2024-12-20"), d("2027-02-10"))
ax.xaxis.set_major_locator(mdates.MonthLocator(bymonth=(1, 4, 7, 10)))
ax.xaxis.set_major_formatter(mdates.DateFormatter("%b\n%Y"))
ax.tick_params(labelsize=7.2, length=2)
ax.get_yaxis().set_visible(False)
for s in ("top", "right", "left"):
    ax.spines[s].set_visible(False)
fig.savefig(OUT / "fig1_timeline.png", bbox_inches="tight", facecolor="white")
print("figure in", OUT)
