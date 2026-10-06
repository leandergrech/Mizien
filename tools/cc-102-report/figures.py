"""CC-102 figures. Reads data/cc-102/rates.csv (run calc.py first). Output: out/fig1_rates.png"""
import csv
import pathlib

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
GREEN, SAGE, AMBER, RED, SLATE, GREY, ORANGE, BLUE = ("#14452F", "#7FA88B", "#E3A72F", "#B5483A", "#2B3A42",
                                                      "#8A9399", "#D9772B", "#3C6E8F")
rows = list(csv.DictReader(open(ROOT / "data" / "cc-102" / "rates.csv")))


def get(year, office):
    return next(r for r in rows if r["year"] == year and r["office"] == office)


fig, (a, b) = plt.subplots(1, 2, figsize=(7.3, 3.9), dpi=220, gridspec_kw={"width_ratios": [1, 1.2]})
# Panel 1: Environment and Planning over time
labs, vals, ns, cols = [], [], [], []
for y in ("2023", "2024", "2025"):
    r = get(y, "Environment and Planning")
    labs.append(y + "\nat closure")
    vals.append(float(r["rate_of_sustained_pct"]))
    ns.append(f"{r['not_implemented']} of {r['sustained_cases']}")
    cols.append(RED if y == "2025" else SAGE)
r = get("2025 (chapter 3, at time of writing)", "Environment and Planning")
labs.append("2025\nstill open*")
vals.append(float(r["rate_of_sustained_pct"]))
ns.append("5 of 12")
cols.append(AMBER)
a.bar(range(4), vals, color=cols, width=0.62)
for i, (v, n) in enumerate(zip(vals, ns)):
    a.text(i, v + 2, f"{v:.0f}%\n{n}", ha="center", fontsize=9, color=SLATE)
a.set_xticks(range(4))
a.set_xticklabels(labs, fontsize=8.5)
a.set_ylim(0, 80)
a.set_ylabel("Not implemented, % of sustained cases", fontsize=8)
a.set_title("Environment and Planning, by year", fontsize=10, color=GREEN, loc="left", fontweight="bold")
# Panel 2: 2025 by office on two denominators
offices = ["Environment and Planning", "Education", "Parliamentary Ombudsman", "Health"]
short = ["Environment\nand Planning", "Education", "Parliamentary\nOmbudsman", "Health"]
x = range(len(offices))
w = 0.38
v1 = [float(get("2025", o)["rate_of_sustained_pct"]) for o in offices]
v2 = [float(get("2025", o)["rate_of_cases_with_recommendation_pct"]) for o in offices]
b.bar([i - w / 2 for i in x], v1, w, color=GREEN, label="of all sustained cases")
b.bar([i + w / 2 for i in x], v2, w, color=SAGE, label="of cases with a recommendation")
for i, (p, q) in enumerate(zip(v1, v2)):
    b.text(i - w / 2, p + 1.5, f"{p:.0f}%", ha="center", fontsize=8.5, color=SLATE)
    b.text(i + w / 2, q + 1.5, f"{q:.0f}%", ha="center", fontsize=8.5, color=SLATE)
b.set_xticks(list(x))
b.set_xticklabels(short, fontsize=8.5)
b.set_ylim(0, 92)
b.legend(frameon=False, fontsize=8, loc="upper right")
b.set_title("2025: ranking depends on denominator", fontsize=10, color=GREEN, loc="left", fontweight="bold")
fig.tight_layout()
fig.savefig(OUT / "fig1_rates.png", bbox_inches="tight", facecolor="white")
print("figure in", OUT)
