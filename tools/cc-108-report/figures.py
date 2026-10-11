"""Figures for Claim Check 108, drawn from data/cc-108/ (run calc.py first)."""
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
GREEN, SAGE, AMBER, RED, SLATE, GREY, ORANGE, BLUE = ("#14452F", "#7FA88B", "#E3A72F", "#B5483A", "#2B3A42",
                                                      "#8A9399", "#D9772B", "#3C6E8F")
inp = {r["id"]: float(r["value"]) for r in csv.DictReader(open(ROOT / "data/cc-108/inputs.csv", encoding="utf-8"))}


def fig1():
    years = [2016, 2022, 2023, 2024, 2025]
    vals = [inp[f"gw_{y}"] for y in years]
    fig, ax = plt.subplots(figsize=(9.6, 3.6), dpi=220)
    ax.bar(range(5), vals, color=[GREY] + [GREEN] * 4, width=0.6)
    ax.axhline(inp["cap_mm3"], color=RED, lw=2, label="Proposed cap: 14 million m³ a year up to 2030 (Green Paper, p. 12)")
    ax.legend(frameon=False, fontsize=8.5, loc="upper right", labelcolor=RED)
    for i, v in enumerate(vals):
        ax.text(i, v + 0.2, f"{v:.2f}", ha="center", fontsize=8.5, color=SLATE)
        ax.text(i, v / 2, f"{v / inp['cap_mm3'] * 100:.0f}%\nof cap", ha="center", fontsize=7.8, color="white")
    ax.set_xticks(range(5))
    ax.set_xticklabels([str(y) for y in years])
    ax.set_ylabel("WSC groundwater production, million m³")
    ax.set_ylim(0, 16.5)
    ax.set_title("WSC groundwater production against the cap proposed for it", fontsize=9.5, color=GREEN, loc="left",
                 fontweight="bold")
    fig.text(0.01, -0.06, "2016: WSC Annual Report 2016, p. 10. 2022-25: WSC Annual Report 2025, Figure 20 (chart values). "
             "Years 2017-21 not read. Source: data/cc-108/.", fontsize=7, color=GREY)
    fig.savefig(OUT / "fig1_cap.png", bbox_inches="tight", facecolor="white")


def fig2():
    labs = ["WSC groundwater\nproduction 2025", "New Water produced\n2022 (all uses)", "New Water maximum\nstated by WSC (2019)"]
    vals = [inp["gw_2025"], inp["newwater_2022"], inp["newwater_target"]]
    fig, ax = plt.subplots(figsize=(9.6, 3.3), dpi=220)
    bars = ax.bar(range(3), vals, color=[GREEN, SAGE, SAGE], width=0.5)
    bars[2].set_hatch("..")
    ax.axhline(vals[0], color=RED, lw=1.6, ls="--")
    for i, v in enumerate(vals):
        t = f"{v:.1f}" + ("" if i == 0 else f"  ({v / vals[0] * 100:.0f}% of 2025 abstraction)")
        ax.text(i, v + 0.3, t, ha="center", fontsize=8.5, color=SLATE)
    ax.set_xticks(range(3))
    ax.set_xticklabels(labs, fontsize=8)
    ax.set_ylabel("million m³")
    ax.set_ylim(0, 14)
    ax.set_title("Treated wastewater supplied, against what WSC abstracts (one part of “giving back”)", fontsize=9.5,
                 color=GREEN, loc="left", fontweight="bold")
    fig.text(0.01, -0.07, "Sapiano 2020 (p. 31) counts recharge and treated wastewater used in place of groundwater as give-back; "
             "recharge is not quantified in any source we read. New Water 2022: Green Paper p. 3; maximum: WSC release, 2 Apr 2019. "
             "Source: data/cc-108/checks.csv.", fontsize=7, color=GREY, wrap=True)
    fig.savefig(OUT / "fig2_giveback.png", bbox_inches="tight", facecolor="white")


fig1(); fig2()
print("figures in", OUT)
