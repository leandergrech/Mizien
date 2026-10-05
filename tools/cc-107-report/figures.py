"""Figures for Claim Check 107, drawn from data/cc-107/ (run gozo_calc.py first)."""
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


def fig2():
    rows = list(csv.DictReader(open(ROOT / "data" / "cc-107" / "gozo_net_zero_arithmetic.csv")))
    sel = [r for r in rows if r["emissions_case"] in ("low", "central", "high") and "afforest" not in r["sequestration_case"]]
    fig, ax = plt.subplots(figsize=(9.6, 3.6), dpi=220)
    labs, vals, cols = [], [], []
    for r in sel:
        rate = "measured rate\n3.6 t/ha/yr" if "Yatir" in r["sequestration_case"] else "optimistic\n10 t/ha/yr"
        labs.append(f"{r['emissions_case']} emissions\n{int(r['gozo_emissions_t']) / 1000:.0f} kt, {rate}")
        vals.append(float(r["forest_needed_km2"]))
        cols.append(GREEN if "Yatir" in r["sequestration_case"] else SAGE)
    ax.bar(range(len(vals)), vals, color=cols, width=0.62)
    ax.axhline(67, color=RED, lw=2, label="Gozo’s total land area: 67 km²")
    ax.legend(frameon=False, fontsize=8.5, loc="upper left", labelcolor=RED)
    for i, v_ in enumerate(vals):
        ax.text(i, v_ + 8, f"{v_:.0f} km²\n({v_ / 67:.1f}× Gozo)", ha="center", fontsize=7.6, color=SLATE)
    ax.set_xticks(range(len(vals)))
    ax.set_xticklabels(labs, fontsize=6.9)
    ax.set_ylabel("New forest needed, km²")
    ax.set_ylim(0, 680)
    ax.set_title("Forest area needed to offset Gozo’s estimated emissions by afforestation alone", fontsize=9.5,
                 color=GREEN, loc="left", fontweight="bold")
    fig.text(0.01, -0.12, "Emissions = Gozo population (41,253) × 2.5 / 3.81 / 5.0 t per person. Measured rate: "
             "Grünzweig et al. 2007 (Aleppo pine, 35 years). Source: data/cc-107/gozo_net_zero_arithmetic.csv.",
             fontsize=7, color=GREY)
    fig.savefig(OUT / "fig2_gozo_forest.png", bbox_inches="tight", facecolor="white")


fig2()
print("figures in", OUT)
