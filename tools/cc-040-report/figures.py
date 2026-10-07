"""Figures for Claim Check 040, drawn from data/cc-040/ (run calc.py first)."""
import json, pathlib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm

HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE / "out"; OUT.mkdir(exist_ok=True)
D = HERE.parents[1] / "data" / "cc-040"
for f in ["LiberationSans-Regular", "LiberationSans-Bold", "LiberationSans-Italic"]:
    fm.fontManager.addfont(f"/usr/share/fonts/truetype/liberation/{f}.ttf")
plt.rcParams.update({"font.family": "Liberation Sans", "axes.spines.top": False, "axes.spines.right": False,
                     "axes.edgecolor": "#8A9399", "axes.labelcolor": "#2B3A42", "xtick.color": "#2B3A42",
                     "ytick.color": "#2B3A42"})
GREEN, SAGE, AMBER, RED, SLATE, GREY, ORANGE = "#14452F", "#7FA88B", "#E3A72F", "#B5483A", "#2B3A42", "#8A9399", "#D9772B"
S = json.load(open(D / "summary.json"))


def fig1():
    fig, ax = plt.subplots(figsize=(9.6, 4.4), dpi=220)
    rk = S["rank"]
    names = [f"{g} {y}" if y != 2024 else g for g, y, _ in rk]
    vals = [v for *_, v in rk]
    cols = [GREEN if g == "MT" else SAGE for g, *_ in rk]
    ax.bar(range(len(rk)), vals, color=cols, width=0.72)
    for i, v in enumerate(vals):
        ax.text(i, v + 4, f"{v:.0f}", ha="center", fontsize=7.5, color=SLATE)
    ax.axhline(110, color=ORANGE, ls="--", lw=1.2)
    ax.text(len(rk) - 0.5, 114, "110 l/day (the keynote's figure)", ha="right", fontsize=8, color=ORANGE)
    ax.axhline(S["median"], color=GREY, ls=":", lw=1)
    ax.text(0, S["median"] + 6, f"median {S['median']:.0f}", fontsize=8, color=GREY)
    ax.set_xticks(range(len(rk))); ax.set_xticklabels(names, fontsize=7.5, rotation=45, ha="right")
    ax.set_ylabel("Households, litres per person per day")
    ax.set_ylim(0, 320)
    fig.tight_layout(); fig.savefig(OUT / "fig1_eu_households.png"); plt.close(fig)


def fig2():
    fig, ax = plt.subplots(figsize=(9.6, 3.8), dpi=220)
    mt = S["malta"]; ys = sorted(int(y) for y in mt)
    ax.plot(ys, [mt[str(y)]["l_cap_day"] for y in ys], color=GREEN, lw=2.2, marker="o", ms=4, label="Households (Eurostat, estimated)")
    ax.axhline(110, color=ORANGE, ls="--", lw=1.2, label="110 l/day (keynote)")
    ax.set_ylim(90, 135); ax.set_ylabel("Litres per person per day"); ax.set_xticks(ys)
    ax.legend(frameon=False, fontsize=8, loc="lower left")
    fig.tight_layout(); fig.savefig(OUT / "fig2_malta_trend.png"); plt.close(fig)


fig1(); fig2()
