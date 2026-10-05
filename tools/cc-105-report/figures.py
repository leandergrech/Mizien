"""Figure for Claim Check 105, drawn from data/cc-105/birzebbuga_monitoring.csv."""
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
B = list(csv.DictReader(open(ROOT / "data/cc-105/birzebbuga_monitoring.csv")))


def fig1():
    fig, ax = plt.subplots(figsize=(9.6, 3.9), dpi=220)
    n = len(B)
    for i, r in enumerate(B):
        ax.plot([int(r["day_low_dBA"]), int(r["day_high_dBA"])], [i - 0.17, i - 0.17], color=AMBER, lw=7, solid_capstyle="round")
        ax.plot([int(r["night_low_dBA"]), int(r["night_high_dBA"])], [i + 0.17, i + 0.17], color=BLUE, lw=7, solid_capstyle="round")
        ax.text(int(r["day_high_dBA"]) + 0.6, i - 0.17, f"{r['day_low_dBA']}–{r['day_high_dBA']}", va="center", fontsize=7.5, color=SLATE)
        ax.text(int(r["night_high_dBA"]) + 0.6, i + 0.17, f"{r['night_low_dBA']}–{r['night_high_dBA']}", va="center", fontsize=7.5, color=SLATE)
    ax.axvline(55, color=AMBER, lw=1, ls=":"); ax.axvline(50, color=BLUE, lw=1, ls=":")
    ax.text(55.2, -0.55, "55: day-evening-night threshold", fontsize=7, color="#9A6E10", va="center")
    ax.text(49.8, -0.55, "50: night threshold", fontsize=7, color=BLUE, va="center", ha="right")
    ax.set_yticks(range(n)); ax.set_yticklabels([f"{r['point']}  {r['location']}" for r in B], fontsize=8); ax.invert_yaxis()
    ax.set_xlim(40, 76); ax.set_ylim(n - 0.4, -0.85)
    ax.set_xlabel("Average noise level, dBA (LAeq, 10 minutes), range over nine months")
    ax.plot([], [], color=AMBER, lw=6, label="Day"); ax.plot([], [], color=BLUE, lw=6, label="Night")
    ax.legend(frameon=False, fontsize=8, loc="lower right")
    fig.text(0.01, -0.06, "Source: Falzon, Dalli Gonzi, Camilleri & Grima (2022), Int. J. Sustain. Dev. Plan. 17(7), doi:10.18280/ijsdp.170732. "
             "Dec 2020 to Aug 2021. Dotted lines are Noise Directive reporting thresholds (Lden/Lnight), shown for orientation only.",
             fontsize=6.6, color=GREY)
    fig.savefig(OUT / "fig1_birzebbuga.png", bbox_inches="tight", facecolor="white")


if __name__ == "__main__":
    fig1()
