"""Figure for Claim Check 031, drawn from data/cc-031/checks.csv (run fetch.py and calc.py first)."""
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
GREEN, AMBER, GREY, BLUE, SLATE = "#14452F", "#E3A72F", "#8A9399", "#3C6E8F", "#2B3A42"
c = {r["check"]: float(r["value"]) for r in csv.DictReader(open(ROOT / "data/cc-031/checks.csv"))
     if r["unit"] in ("kt CO2e", "%")}
all_g = c["Gozo all sectors 2024, population-proportional approximation"]
road_g = c["Gozo road transport 2024, population-proportional approximation"]
fig, ax = plt.subplots(figsize=(9.6, 3.0), dpi=220)
labs = ["Gozo, all sectors (approx.)", "Gozo, road transport (approx.)", "Electric buses: estimated saving"]
vals = [all_g, road_g, 1.3]
cols = [GREY, BLUE, GREEN]
ax.barh(labs[::-1], vals[::-1], color=cols[::-1], height=0.55)
for i, (val, lab) in enumerate(zip(vals[::-1], labs[::-1])):
    ax.text(val + 2, i, f"{val:.1f} kt CO2e a year" if val < 10 else f"{val:.0f} kt CO2e a year", va="center", fontsize=9,
            fontweight="bold", color=SLATE)
ax.set_xlim(0, 215)
ax.set_xlabel("kt CO2e a year")
ax.text(0, -1.05, "Gozo figures are Malta's 2024 inventory multiplied by Gozo's 7.26% population share (not Gozo data). Bus "
        "saving: Malta Public Transport's estimate (TVM News, 4 Jul 2026). Source: Eurostat.", fontsize=7, color=GREY,
        clip_on=False)
fig.savefig(OUT / "fig1_scale.png", bbox_inches="tight", facecolor="white")
