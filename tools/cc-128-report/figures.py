"""Figure for Claim Check 128: Malta's third RBMP against the WFD timetable (data/cc-128/timeline.csv; run calc.py first)."""
import csv, pathlib
from datetime import date
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as md
from matplotlib import font_manager as fm
HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE / "out"; OUT.mkdir(exist_ok=True)
for f in ["LiberationSans-Regular", "LiberationSans-Bold"]:
    fm.fontManager.addfont(f"/usr/share/fonts/truetype/liberation/{f}.ttf")
plt.rcParams.update({"font.family": "Liberation Sans", "axes.spines.top": False, "axes.spines.right": False, "axes.spines.left": False})
GREEN, SAGE, AMBER, RED, SLATE, GREY = "#14452F", "#7FA88B", "#E3A72F", "#B5483A", "#2B3A42", "#8A9399"
d = lambda s: date.fromisoformat(s)
fig, ax = plt.subplots(figsize=(9.6, 3.9), dpi=220)
rows = [  # (label, due, actual or None, actual label)
    ("Overview of significant\nwater management issues", d("2019-12-22"), d("2020-08-19"), "consultation opened 19 Aug 2020 *"),
    ("Draft plan for\n6-month consultation", d("2020-12-22"), d("2023-09-20"), "opened 20 Sep 2023 *"),
    ("Plan published / adopted", d("2021-12-22"), d("2024-03-31"), "'March 2024' (Commission)"),
    ("Plan reported to\nthe Commission", d("2022-03-22"), d("2024-03-31"), "with publication, March 2024 (Commission)"),
]
for i, (lab, due, act, al) in enumerate(rows[::-1]):
    ax.plot([due, act], [i, i], color=SAGE, lw=3, solid_capstyle="butt")
    ax.plot(due, i, "o", color=GREEN, ms=7); ax.plot(act, i, "o", color=RED, ms=7)
    ax.text(md.date2num(act) + 40, i, al, va="center", fontsize=7.5, color=SLATE)
    ax.text(md.date2num(d("2018-05-01")), i, lab, va="center", ha="left", fontsize=8, color=SLATE)
ax.axvline(d("2023-09-30"), color=AMBER, ls="--", lw=1)
ax.text(d("2023-09-30"), 3.55, "30 Sep 2023: Commission's cut-off,\nMalta had not submitted", fontsize=7.5, color=AMBER, ha="right", va="bottom")
ax.set_ylim(-0.6, 4.3); ax.set_yticks([])
ax.set_xlim(d("2018-01-01"), d("2026-06-30"))
ax.xaxis.set_major_locator(md.YearLocator()); ax.xaxis.set_major_formatter(md.DateFormatter("%Y"))
ax.plot([], [], "o", color=GREEN, label="Due under the Directive"); ax.plot([], [], "o", color=RED, label="Malta (* = second-hand date)")
ax.legend(frameon=False, fontsize=8, loc="upper right")
fig.savefig(OUT / "fig1_timeline.png", bbox_inches="tight", facecolor="white")
print("ok")
