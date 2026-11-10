"""Figure for Claim Check 157, from data/cc-157/fig4b_readings.csv (run calc.py first)."""
import csv, pathlib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[1]
OUT = HERE / "out"
OUT.mkdir(exist_ok=True)
for f in ["LiberationSans-Regular", "LiberationSans-Bold", "LiberationSans-Italic"]:
    fm.fontManager.addfont(f"/usr/share/fonts/truetype/liberation/{f}.ttf")
plt.rcParams.update({"font.family": "Liberation Sans", "axes.spines.top": False, "axes.spines.right": False,
                     "axes.edgecolor": "#8A9399", "axes.labelcolor": "#2B3A42", "xtick.color": "#2B3A42",
                     "ytick.color": "#2B3A42"})
GREEN, SAGE, AMBER, RED, SLATE, GREY = "#14452F", "#7FA88B", "#E3A72F", "#B5483A", "#2B3A42", "#8A9399"
rows = [(r["country"], float(r["gdp_impact_pct_read_from_figure"]))
        for r in csv.DictReader(open(ROOT / "data" / "cc-157" / "fig4b_readings.csv"))]
rows.sort(key=lambda t: t[1])
rows = rows[:14]  # the fourteen largest losses
fig, ax = plt.subplots(figsize=(9.6, 4.8), dpi=220)
names = [n for n, _ in rows]
vals = [v for _, v in rows]
cols = [GREEN if n == "Malta" else SAGE for n in names]
ax.barh(names, [-v for v in vals], color=cols, height=0.68)
ax.axvline(2.5, color=RED, lw=1.8, ls="--")
ax.text(2.55, len(names) - 0.55, "claim: more than 2.5%", color=RED, fontsize=9, va="top")
for i, v in enumerate(vals):
    ax.text(-v + 0.04, i, f"{-v:.1f}%", va="center", fontsize=8.5, color=SLATE,
            fontweight="bold" if names[i] == "Malta" else "normal")
ax.set_xlabel("Projected annual GDP loss from heatwaves, 2055–2064 (% of GDP; values read from the published figure)")
ax.set_xlim(0, 3.9)
ax.invert_yaxis()
fig.tight_layout()
fig.savefig(OUT / "fig1_countries.png")
print("ok")
