"""Figures for Claim Check 050, drawn from data/cc-050/checks.csv (run calc.py first)."""
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
GREEN, AMBER, RED, SLATE, GREY = "#14452F", "#E3A72F", "#B5483A", "#2B3A42", "#8A9399"
R = list(csv.DictReader(open(ROOT / "data/cc-050/checks.csv")))[:2]


def fig1():
    fig, ax = plt.subplots(figsize=(9.2, 3.0), dpi=220)
    labs = ["First conviction", "Second or later conviction"]
    for i, r in enumerate(R):
        cur, new = int(r["current_eur"]), int(r["proposed_eur"])
        ax.barh(i - 0.19, cur, height=0.34, color=GREEN)
        ax.barh(i + 0.19, new, height=0.34, color=AMBER)
        ax.text(cur + 150, i - 0.19, f"EUR {cur:,} (law today)", va="center", fontsize=8.2, color=SLATE)
        ax.text(new + 150, i + 0.19, f"EUR {new:,} (reported proposal, {r['change_pct']}%)", va="center", fontsize=8.2, color=SLATE)
    ax.set_yticks(range(2)); ax.set_yticklabels(labs, fontsize=8.4); ax.invert_yaxis()
    ax.set_xlim(0, 15500); ax.set_xlabel("Fine for hunting or taking a bird listed in Schedule I or IX (EUR)")
    fig.text(0.01, -0.07, "Law today: S.L. 549.42 (consolidated, amended to L.N. 251 of 2025). Proposal: ORNIS Committee, 23 Sep 2026, "
             "as reported by Newsbook and BirdLife Malta (second-hand).", fontsize=6.8, color=GREY)
    fig.savefig(OUT / "fig1_fines.png", bbox_inches="tight", facecolor="white")


if __name__ == "__main__":
    fig1()
