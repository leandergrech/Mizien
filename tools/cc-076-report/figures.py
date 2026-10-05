"""Figures for Claim Check 076, drawn from data/cc-076/ (run fetch.py and calc.py first)."""
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
GREEN, AMBER, RED, SLATE, GREY, BLUE = "#14452F", "#E3A72F", "#B5483A", "#2B3A42", "#8A9399", "#3C6E8F"
rows = list(csv.DictReader(open(ROOT / "data/cc-076/daily_increase.csv")))


def fig1():
    fig, ax = plt.subplots(figsize=(9.6, 3.9), dpi=220)
    labs = [f"{r['quarter']}\n{r['year']}" for r in rows]
    vals = [float(r["per_day"]) for r in rows]
    cols = [GREEN if (r["year"], r["quarter"]) == ("2026", "Q1") else ("#C9D3CC" if (r["year"], r["quarter"]) != ("2025", "Q4") else BLUE) for r in rows]
    ax.bar(labs, vals, color=cols)
    for i, v in enumerate(vals):
        ax.text(i, v + 1, f"{v:.0f}", ha="center", fontsize=8.5, color=SLATE, fontweight="bold" if i >= len(vals) - 4 else "normal")
    ax.set_ylim(0, 68)
    ax.set_title("Net average daily increase in licensed motor vehicles, by quarter (vehicles per day)", fontsize=10, color=SLATE, loc="left")
    ax.tick_params(axis="x", labelsize=8)
    fig.text(0.01, -0.04, "Green: Q1 2026 (the claim, 36). Blue: Q4 2025 (the Commission's 35). Stock difference divided by days in the quarter, "
             "NSO method note 7. Source: NSO NR 085/2026 Table 1, retrieved 5 Oct 2026.", fontsize=7, color=GREY)
    fig.tight_layout()
    fig.savefig(OUT / "fig1_daily.png", bbox_inches="tight", facecolor="white")


def fig2():
    fig, ax = plt.subplots(figsize=(9.6, 3.3), dpi=220)
    items = [("Newly licensed", 5680, GREEN), ("Taken off the road\n(restrictions started)", -6963, RED),
             ("Restrictions ended", 4140, BLUE), ("Net by NSO's\nflow identity", 2857, GREY), ("Net by stock\ndifference (headline)", 3245, GREEN)]
    ax.bar([a for a, _, _ in items], [b for _, b, _ in items], color=[c for _, _, c in items])
    for i, (_, v, _) in enumerate(items):
        ax.text(i, v + (250 if v > 0 else -750), f"{v:,}", ha="center", fontsize=9, color=SLATE, fontweight="bold")
    ax.axhline(0, color=GREY, lw=0.8); ax.set_ylim(-8200, 7200)
    ax.set_title("Q1 2026 vehicle flows (number of motor vehicles)", fontsize=10, color=SLATE, loc="left")
    ax.tick_params(axis="x", labelsize=8)
    fig.text(0.01, -0.05, "Flows from the NSO release text (NR 085/2026). The two net figures differ by 388 (0.08% of the stock); NSO "
             "attributes such gaps to database cut-off dates.", fontsize=7, color=GREY)
    fig.tight_layout()
    fig.savefig(OUT / "fig2_flows.png", bbox_inches="tight", facecolor="white")


if __name__ == "__main__":
    fig1(); fig2()
