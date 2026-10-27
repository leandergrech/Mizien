"""Figures for Claim Check 143, drawn from data/cc-143/ and data/cc-101/."""
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
GREEN, SAGE, AMBER, RED, SLATE, GREY, BLUE = "#14452F", "#7FA88B", "#E3A72F", "#B5483A", "#2B3A42", "#8A9399", "#3C6E8F"
F = {r["id"]: float(r["value"]) for r in csv.DictReader(open(ROOT / "data/cc-143/document_facts.csv")) if r["unit"] != "date"}
E = {int(r["year"]): float(r["value"]) for r in csv.DictReader(open(ROOT / "data/cc-101/eurostat_env_wat_abs.csv"))
     if r["wat_src"] == "FGW" and r["wat_proc"] == "ABST"}


def fig1():
    """Groundwater bodies in poor status in each plan, out of 15."""
    plans = ["1st plan", "2nd plan", "3rd plan"]
    quant = [F["swd19_quant_poor_n_1st"], F["swd19_quant_poor_n_2nd"], F["swd26_quant_poor_n_3rd"]]
    chem = [F["swd19_chem_poor_n_1st"], F["swd19_chem_poor_n_2nd"], F["swd26_chem_poor_n_2021"]]
    fig, axes = plt.subplots(1, 2, figsize=(9.6, 3.3), dpi=220, sharey=True)
    for ax, vals, title, col in ((axes[0], quant, "Poor quantitative status\n(too much water taken out)", BLUE),
                                 (axes[1], chem, "Poor chemical status\n(pollution, salt)", RED)):
        bars = ax.bar(plans, vals, color=[SAGE, col, col], width=0.55)
        bars[0].set_alpha(0.55)
        for b, v in zip(bars, vals):
            ax.text(b.get_x() + b.get_width() / 2, v + 0.35, f"{int(v)}", ha="center", fontsize=10, fontweight="bold", color=SLATE)
        ax.axhline(15, color=GREY, lw=0.8, ls="--")
        ax.text(2.42, 15.25, "all 15 bodies", fontsize=7.5, color=GREY, ha="right")
        ax.set_title(title, fontsize=9, color=SLATE, loc="left")
        ax.set_ylim(0, 17.5)
        ax.tick_params(labelsize=8.5)
    axes[0].set_ylabel("groundwater bodies (of 15)", fontsize=8.5)
    fig.text(0.01, -0.03, "Sources: SWD(2019) 48 pp. 79, 86 (1st and 2nd plans); SWD(2026) 702 pp. 8-9, 28 (3rd plan; 2nd-plan counts agree). "
             "Lighter bar: 1st plan.", fontsize=7, color=GREY)
    fig.tight_layout()
    fig.savefig(OUT / "fig1_status.png", bbox_inches="tight", facecolor="white")


def fig2():
    """Eurostat's estimate of fresh groundwater abstraction."""
    ys = sorted(E)
    fig, ax = plt.subplots(figsize=(9.6, 3.0), dpi=220)
    ax.plot(ys, [E[y] for y in ys], color=BLUE, lw=2, marker="o", ms=3.5)
    for y in (2015, 2021):
        ax.annotate(f"{E[y]:.1f}", (y, E[y]), textcoords="offset points", xytext=(0, 8), ha="center", fontsize=8.5,
                    color=SLATE, fontweight="bold")
    ax.set_ylim(0, 52)
    ax.set_xticks(ys)
    ax.tick_params(labelsize=8)
    ax.set_ylabel("million m³ a year", fontsize=8.5)
    ax.grid(axis="y", color="#E3E6E8", lw=0.6)
    fig.text(0.01, -0.06, "Source: Eurostat env_wat_abs, fresh groundwater, total gross abstraction, Malta; every year flagged 'e' "
             "(estimated). Retrieved 6 Oct 2026.", fontsize=7, color=GREY)
    fig.savefig(OUT / "fig2_abstraction.png", bbox_inches="tight", facecolor="white")


if __name__ == "__main__":
    fig1()
    fig2()
