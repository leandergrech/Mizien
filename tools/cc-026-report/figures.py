"""Figures for Claim Check 026, drawn from data/cc-026/ (run calc.py first)."""
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
D = ROOT / "data" / "cc-026"
A = {int(r["year"]): r for r in csv.DictReader(open(D / "malta_ainah_ghg.csv"))}
U = {int(r["year"]): r for r in csv.DictReader(open(D / "malta_unfccc_inventory.csv"))}
EU = {r["geo"]: r for r in csv.DictReader(open(D / "eu_ainah_ghg_total_hh.csv"))}


def fig1():
    fig, ax = plt.subplots(figsize=(9.6, 4.6), dpi=220)
    ys = list(range(2005, 2025))
    tot = [float(A[y]["TOTAL_HH"]) for y in ys]
    air = [float(A[y]["H51"]) for y in ys]
    oth = [t - a for t, a in zip(tot, air)]
    ax.bar(ys, oth, color=SAGE, width=0.72, label="All other activities and households")
    ax.bar(ys, air, bottom=oth, color=ORANGE, width=0.72, label="Air transport (NACE H51)")
    ax.bar([2025], [float(A[2025]["TOTAL_HH"])], color="white", edgecolor=SLATE, hatch="///", width=0.72,
           label="2025 early estimate (no activity split)")
    uy = list(range(2005, 2025))
    ax.plot(uy, [float(U[y]["TOTX4_MEMO"]) for y in uy], color=SLATE, lw=2.4, marker="o", ms=3,
            label="National inventory (UNFCCC, territorial)")
    ax.text(2015, 7600, "+169.7%\n2015–2025", ha="center", fontsize=9, color=RED, fontweight="bold")
    ax.annotate("", xy=(2024.4, 7350), xytext=(2015.6, 3100), arrowprops=dict(arrowstyle="->", color=RED, lw=1.4))
    ax.set_ylabel("Thousand tonnes CO2-equivalent")
    ax.set_ylim(0, 8600)
    ax.set_xlim(2004.3, 2025.8)
    ax.set_xticks(range(2005, 2026, 2))
    ax.legend(frameon=False, fontsize=8, loc="upper left")
    ax.text(2004.4, -1250, "Sources: Eurostat env_ac_ainah_r2 (air emissions accounts) and env_air_gge (inventory), "
            "retrieved 5 Oct 2026.", fontsize=7, color=GREY)
    fig.savefig(OUT / "fig1_malta_accounts.png", bbox_inches="tight", facecolor="white")


def fig2():
    fig, ax = plt.subplots(figsize=(9.6, 4.2), dpi=220)
    rows = []
    for g, r in EU.items():
        if g != "EU27_2020" and r["y2015"] and r["y2025"]:
            rows.append((100 * (float(r["y2025"]) / float(r["y2015"]) - 1), r["name"]))
    rows.sort(reverse=True)
    names = [n.replace("Czechia", "Czechia") for _, n in rows]
    vals = [v for v, _ in rows]
    cols = [RED if n == "Malta" else (ORANGE if v > 0 else SAGE) for v, n in rows]
    ax.bar(range(len(vals)), vals, color=cols, width=0.72)
    ax.axhline(-17.2, color=BLUE, lw=1.4, ls="--")
    ax.text(9, -26, "EU-27 −17.2% (dashed line)", color=BLUE, fontsize=8.5, ha="left", fontweight="bold")
    ax.set_xticks(range(len(vals)))
    ax.set_xticklabels(names, rotation=75, ha="right", fontsize=7.5)
    ax.set_ylim(-48, 178)
    ax.set_ylabel("Change 2015–2025 (%)")
    ax.text(0.6, 168, "Malta +169.7%", color=RED, fontsize=8.5, fontweight="bold")
    ax.axhline(0, color=SLATE, lw=0.8)
    fig.savefig(OUT / "fig2_eu_changes.png", bbox_inches="tight", facecolor="white")


fig1()
fig2()
print("figures in", OUT)
