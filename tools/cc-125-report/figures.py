"""Figure for Claim Check 125: when the Fund's EUR 45.4 million is paid out (data/cc-125/payouts.csv, Annex II)."""
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
                     "axes.edgecolor": "#8A9399"})
GREEN, AMBER, BLUE, SLATE, GREY = "#14452F", "#E3A72F", "#3F6E8F", "#2B3A42", "#8A9399"
COL = {"C1 Buildings": GREEN, "C2 Road transport": BLUE, "C4 Technical assistance": AMBER}


def fig1():
    rows = list(csv.DictReader(open(ROOT / "data" / "cc-125" / "payouts.csv")))
    years = list(range(2027, 2033))
    fig, ax = plt.subplots(figsize=(9.2, 3.7), dpi=220)
    bottom = [0.0] * len(years)
    for comp, c in COL.items():
        vals = [sum(int(r["payout_eur"]) for r in rows if r["component"] == comp and int(r["year"]) == y) / 1e6 for y in years]
        ax.bar(years, vals, bottom=bottom, color=c, width=0.62, label=comp.split(" ", 1)[1] if comp != "C4 Technical assistance" else "Technical assistance")
        bottom = [b + v for b, v in zip(bottom, vals)]
    for y, b in zip(years, bottom):
        if b:
            ax.text(y, b + 0.2, f"{b:.1f}", ha="center", fontsize=8.5, color=SLATE)
    ax.set_xticks(years); ax.set_ylabel("EUR million of Fund payout value", fontsize=8.5, color=SLATE)
    ax.tick_params(labelsize=8.5, colors=SLATE)
    ax.legend(frameon=False, fontsize=8.5, loc="upper left")
    ax.text(2026.55, -3.1, "Source: Commission Implementing Decision C(2026) 5266, Annex II (16 milestones and targets; total 45,410,023). "
            "Year = indicative year of achievement.", fontsize=7, color=GREY, clip_on=False)
    fig.savefig(OUT / "fig1_payouts.png", bbox_inches="tight", facecolor="white")


if __name__ == "__main__":
    fig1()
