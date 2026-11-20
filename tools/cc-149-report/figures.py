"""Figures for Claim Check 149 (run calc.py first)."""
import csv
import pathlib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[1]
D = ROOT / "data/cc-149"
OUT = HERE / "out"; OUT.mkdir(exist_ok=True)
for f in ["LiberationSans-Regular", "LiberationSans-Bold", "LiberationSans-Italic"]:
    fm.fontManager.addfont(f"/usr/share/fonts/truetype/liberation/{f}.ttf")
plt.rcParams.update({"font.family": "Liberation Sans", "axes.spines.top": False, "axes.spines.right": False,
                     "axes.edgecolor": "#8A9399", "axes.labelcolor": "#2B3A42", "xtick.color": "#2B3A42",
                     "ytick.color": "#2B3A42"})
GREEN, AMBER, RED, SLATE, GREY, PALE = "#14452F", "#E3A72F", "#B5483A", "#2B3A42", "#8A9399", "#C9D3CC"
rows = list(csv.DictReader(open(D / "annual.csv")))
fig, ax = plt.subplots(figsize=(9.6, 3.8), dpi=220)
years = [int(r["year"]) for r in rows]
for r in rows:
    y, v = int(r["year"]), int(r["new_dwellings"])
    sec = "second-hand" in r["basis"]
    ax.bar(y, v, color="white" if sec else (RED if y == 2025 else GREEN), edgecolor=GREY if sec else "none",
           hatch="///" if sec else None, width=0.7)
    ax.text(y, v + 180, f"{v:,}", ha="center", fontsize=8, color=SLATE)
ax.axhline(12325, color=RED, lw=0.7, ls=":")
ax.set_xticks(range(min(years), max(years) + 1))
ax.set_ylim(0, 14500); ax.set_ylabel("Approved new dwellings")
ax.text(2020.5, 600, "2020–2021\nnot on file", ha="center", fontsize=7.5, color=GREY)
from matplotlib.patches import Patch
ax.legend(handles=[Patch(color=GREEN, label="NSO quarterly tables (sum of quarters)"),
                   Patch(facecolor="white", edgecolor=GREY, hatch="///", label="Press reports of NSO figures (second-hand)")],
          fontsize=7.5, frameon=False, loc="upper center", bbox_to_anchor=(0.55, 1.0))
fig.text(0.01, -0.03, "Sources: NSO news releases NR 028/2023, 033/2024, 028/2025, 026/2026 (Table 1); 2018–2019 as reported by "
         "MaltaToday and Lovin Malta.", fontsize=7, color=GREY)
fig.tight_layout(); fig.savefig(OUT / "fig1_annual.png", bbox_inches="tight"); plt.close(fig)
