"""Figures for Claim Check 039, drawn from data/cc-039/ (run calc.py first)."""
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
inp = {r["id"]: float(r["value"]) for r in csv.DictReader(open(ROOT / "data/cc-039/inputs.csv", encoding="utf-8"))}
M = 1e6


def fig1():
    years = [2016, 2022, 2023, 2024, 2025]
    vals = [inp[f"gw_m3_{y}"] / M for y in years]
    fig, ax = plt.subplots(figsize=(9.6, 3.6), dpi=220)
    ax.bar(range(5), vals, color=[GREY] + [GREEN] * 4, width=0.6)
    ax.axhline(vals[0] - 4.0, color=RED, lw=2, label="2016 level minus the pledged 4.0 million m³ = 9.5")
    ax.legend(frameon=False, fontsize=8.5, loc="upper right", labelcolor=RED)
    for i, v in enumerate(vals):
        ax.text(i, v + 0.2, f"{v:.2f}", ha="center", fontsize=8.5, color=SLATE)
        if i:
            ax.text(i, v / 2, f"{v - vals[0]:+.2f}\nvs 2016", ha="center", fontsize=7.6, color="white")
    ax.set_xticks(range(5))
    ax.set_xticklabels([str(y) for y in years])
    ax.set_ylabel("WSC groundwater production, million m³")
    ax.set_ylim(0, 16)
    ax.set_title("WSC groundwater production against the pledged 4 billion litre (4.0 million m³) cut", fontsize=9.5,
                 color=GREEN, loc="left", fontweight="bold")
    fig.text(0.01, -0.06, "2016: WSC Annual Report 2016, p. 10. 2022-25: WSC Annual Report 2025, Figure 20 (chart values). "
             "Years 2017-21 not read. Source: data/cc-039/.", fontsize=7, color=GREY)
    fig.savefig(OUT / "fig1_groundwater.png", bbox_inches="tight", facecolor="white")


def fig2():
    e16 = inp["ro_m3_2016"] / M * inp["spec_kwh_2016"]
    e24 = inp["ro_m3_2024"] / M * 4.68
    e25 = inp["ro_m3_2025"] / M * inp["spec_kwh_2016"]
    fig, ax = plt.subplots(figsize=(9.6, 3.4), dpi=220)
    labs = ["2016\n18.6 million m³ × 4.85 kWh/m³\n(WSC report)", "2024, indicative\n25.7 million m³ × 4.68 kWh/m³\n(4.68 is second-hand)",
            "2025, scenario\n27.9 million m³ × 4.85 kWh/m³\n(2016 specific energy held)"]
    vals = [e16, e24, e25]
    bars = ax.bar(range(3), vals, color=[GREEN, SAGE, SAGE], width=0.55)
    bars[1].set_hatch("//"); bars[2].set_hatch("..")
    ax.axhline(e16, color=RED, lw=1.6, ls="--")
    for i, v in enumerate(vals):
        ax.text(i, v + 2, f"{v:.0f} GWh" + ("" if i == 0 else f"\n({(v / e16 - 1) * 100:+.0f}%)"), ha="center", fontsize=8.5,
                color=SLATE)
    ax.set_xticks(range(3))
    ax.set_xticklabels(labs, fontsize=7.4)
    ax.set_ylabel("Electricity for reverse osmosis, GWh")
    ax.set_ylim(0, 165)
    ax.set_title("Electricity used by WSC’s reverse osmosis plants (volume × specific energy)", fontsize=9.5,
                 color=GREEN, loc="left", fontweight="bold")
    fig.text(0.01, -0.12, "Estimates, not metered totals. Staying at the 2016 level in 2025 would need 3.24 kWh/m³ "
             "(33% below 4.85). Source: data/cc-039/checks.csv.", fontsize=7, color=GREY)
    fig.savefig(OUT / "fig2_ro_energy.png", bbox_inches="tight", facecolor="white")


fig1(); fig2()
print("figures in", OUT)
