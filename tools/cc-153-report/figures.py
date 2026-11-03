"""Figure for Claim Check 153, from data/cc-153/commission_nbrp_page.csv."""
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
GREEN, SAGE, AMBER, RED, SLATE, GREY, ORANGE = ("#14452F", "#7FA88B", "#E3A72F", "#B5483A", "#2B3A42", "#8A9399", "#D9772B")
rows = sorted(((r["entry"], dt.date.fromisoformat(r["date_printed_beside_draft_plan"]))
               for r in csv.DictReader(open(ROOT / "data/cc-153/commission_nbrp_page.csv"))), key=lambda x: x[1])
dl, notice = dt.date(2025, 12, 31), dt.date(2026, 3, 12)
fig, ax = plt.subplots(figsize=(9.6, 5.4), dpi=220)
ys = list(range(len(rows)))
for y, (n, d) in zip(ys, rows):
    ax.plot([dl, d], [y, y], color=SAGE if d <= dl else GREY, lw=1, zorder=1)
    ax.scatter([d], [y], color=GREEN if d <= dl else ORANGE, s=28, zorder=2)
ax.set_yticks(ys); ax.set_yticklabels([n for n, _ in rows], fontsize=8)
ax.axvline(dl, color=SLATE, lw=1.2); ax.axvline(notice, color=RED, lw=1.2, ls="--")
ax.text(dl, len(rows) + 0.2, "Deadline\n31 Dec 2025", ha="right", fontsize=8, color=SLATE, va="bottom")
ax.text(notice, len(rows) + 0.2, "Letters of formal notice\n12 Mar 2026", ha="left", fontsize=8, color=RED, va="bottom")
ax.text(dt.date(2026, 9, 25), 1.0, "Malta: no entry on\nthe Commission page\n(read 3 Nov 2026)", fontsize=9, color=RED, fontweight="bold", ha="center")
ax.set_ylim(-0.7, len(rows) + 1.6)
ax.xaxis.set_major_formatter(md.DateFormatter("%b %Y"))
ax.set_xlabel("Date printed beside each draft plan on the Commission page (may be the translation date). Source: energy.ec.europa.eu NBRP page, read 3 Nov 2026.", fontsize=7, color=GREY, loc="left")
fig.savefig(OUT / "fig1_timeline.png", bbox_inches="tight", facecolor="white"); plt.close(fig); print("ok")
