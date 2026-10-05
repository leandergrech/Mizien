"""Figures for Claim Check 111, drawn from data/cc-111/ (run fetch.py first)."""
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
v = {}
for r in csv.DictReader(open(ROOT / "data/cc-111/eurostat_env_wasmun.csv")):
    v[(r["geo"], r["wst_oper"], r["unit"], int(r["year"]))] = float(r["value"])
T = {r["bortle_class"]: r for r in csv.DictReader(open(ROOT / "data/cc-053/caruana2020_table1.csv"))}


def fig1():
    cols = [("malta_2017_18_pct", "Malta 2017/18"), ("malta_2018_19_pct", "Malta 2018/19"), ("gozo_2017_18_pct", "Gozo"),
            ("comino_2017_18_pct", "Comino"), ("all_2017_18_pct", "All islands")]
    cls = [("4", "Class 4: Milky Way visible", "#2B4C7E"), ("5", "Class 5", "#8DB36B"), ("6-7", "Classes 6–7", "#E3A72F"), ("8-9", "Classes 8–9 (city sky)", "#B5483A")]
    fig, ax = plt.subplots(figsize=(9.6, 3.6), dpi=220)
    for i, (k, lab) in enumerate(cols):
        left = 0
        for c, cl, col in cls:
            v = float(T[c][k]); ax.barh(i, v, left=left, color=col, label=cl if i == 0 else None)
            if v >= 6: ax.text(left + v / 2, i, f"{v:.0f}%", ha="center", va="center", fontsize=8, color="white", fontweight="bold")
            left += v
    ax.set_yticks(range(len(cols))); ax.set_yticklabels([l for _, l in cols], fontsize=8.5); ax.invert_yaxis()
    ax.set_xlim(0, 100); ax.set_xlabel("Share of land area (%)")
    ax.legend(frameon=False, fontsize=7.8, ncol=4, loc="upper center", bbox_to_anchor=(0.5, 1.16))
    fig.text(0.01, -0.06, "Bortle classes from Sky Quality Meter readings in 347 one-km cells. Source: Caruana et al. (2020) Table 1.", fontsize=7, color=GREY)
    fig.savefig(OUT / "fig1_bortle.png", bbox_inches="tight", facecolor="white")


if __name__ == "__main__":
    fig1()
