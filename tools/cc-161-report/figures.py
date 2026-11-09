"""Figure for Claim Check 161, drawn from data/cc-161/ (run calc.py first)."""
import csv, pathlib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm

HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE / "out"; OUT.mkdir(exist_ok=True)
for f in ["LiberationSans-Regular", "LiberationSans-Bold"]:
    fm.fontManager.addfont(f"/usr/share/fonts/truetype/liberation/{f}.ttf")
plt.rcParams.update({"font.family": "Liberation Sans", "axes.spines.top": False, "axes.spines.right": False})
GREEN, SAGE, SLATE, GREY = "#14452F", "#7FA88B", "#2B3A42", "#8A9399"
R = list(csv.DictReader(open(HERE.parents[1] / "data" / "cc-161" / "police_noise_reports.csv", encoding="utf-8")))
fig, ax = plt.subplots(figsize=(9.2, 3.6), dpi=220)
names = [r["locality"] for r in R][::-1]
tot = [int(r["reports_total"]) for r in R][::-1]
aft = [int(r["reports_after_2300"]) for r in R][::-1]
ax.barh(names, tot, color=SAGE, label="All reports of excessive noise")
ax.barh(names, aft, color=GREEN, label="of which after 23:00")
for i, (t, a) in enumerate(zip(tot, aft)):
    ax.text(t + 0.5, i, f"{t} ({a} after 23:00)", va="center", fontsize=9, color=SLATE)
ax.set_xlim(0, 45); ax.set_xlabel("Reports to the police, January 2021 to June 2022 (second-hand, from a news report)", fontsize=9, color=SLATE)
ax.legend(frameon=False, fontsize=8.5, loc="lower right")
fig.tight_layout(); fig.savefig(OUT / "fig1_police_reports.png"); print("ok")
