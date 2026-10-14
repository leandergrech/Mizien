"""Figures for Claim Check 120, drawn from data/cc-120/ (run calc.py first)."""
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
D = ROOT / "data" / "cc-120"
POP = {r["geo"]: int(r["population_1_jan_2022"]) for r in csv.DictReader(open(D / "population_2022.csv"))}
EXP = {r["geo"]: r for r in csv.DictReader(open(D / "eea_exposure_lden55.csv"))}
H = {(r["basis"], r["geo"]): r for r in csv.DictReader(open(D / "eea_health_burden_table.csv"))}
EU = sorted(EXP)


def fig1():
    fig, ax = plt.subplots(figsize=(9.6, 3.9), dpi=220)
    items = sorted(((g, int(H[("END", g)]["deaths_total"])) for g in EU), key=lambda kv: kv[1])
    ax.bar([k for k, _ in items], [v for _, v in items], color=[GREEN if k == "MT" else SAGE for k, _ in items], width=0.72)
    for i, (k, v) in enumerate(items[:6]):
        ax.text(i, v + 150, f"{v:,}", ha="center", fontsize=7.5, color=GREEN if k == "MT" else SLATE,
                fontweight="bold" if k == "MT" else "normal")
    ax.set_ylabel("Premature deaths a year")
    ax.tick_params(axis="x", labelsize=8)
    ax.text(-0.5, -4300, "EEA, Environmental noise in Europe 2025 (corrected online version, 27 Mar 2026), Table 3.7: road, rail and air noise "
            "above END thresholds. Absolute counts, not per capita.", fontsize=7, color=GREY)
    fig.savefig(OUT / "fig1_deaths.png", bbox_inches="tight", facecolor="white")


def fig2():
    fig, ax = plt.subplots(figsize=(9.6, 4.0), dpi=220)
    order = sorted(EU, key=lambda g: (int(H[("END", g)]["dalys100k_total"]), int(H[("WHO", g)]["dalys100k_total"])))
    x = range(len(order))
    ax.scatter(x, [int(H[("END", g)]["dalys100k_total"]) for g in order], color=SAGE, s=34, zorder=3, label="Above END thresholds (the study's basis)")
    ax.scatter(x, [int(H[("WHO", g)]["dalys100k_total"]) for g in order], color=AMBER, s=34, marker="D", zorder=3, label="Above WHO 2018 levels")
    i = order.index("MT")
    ax.scatter([i], [int(H[("END", "MT")]["dalys100k_total"])], color=GREEN, s=95, zorder=4)
    ax.scatter([i], [int(H[("WHO", "MT")]["dalys100k_total"])], color=ORANGE, s=95, marker="D", zorder=4)
    ax.annotate("Malta 150", (i, 150), (i + 2.2, 60), fontsize=8.5, color=GREEN, fontweight="bold", arrowprops=dict(arrowstyle="-", color=GREEN))
    ax.annotate("Malta 310", (i, 310), (i + 2.2, 470), fontsize=8.5, color=ORANGE, fontweight="bold", arrowprops=dict(arrowstyle="-", color=ORANGE))
    ax.set_xticks(list(x)); ax.set_xticklabels(order, fontsize=7.5)
    ax.set_ylabel("DALYs per 100,000 people a year")
    ax.set_ylim(0, 880)
    ax.legend(frameon=False, fontsize=8.5, loc="upper left")
    ax.text(-0.5, -170, "EEA 2025 report (corrected 27 Mar 2026), Tables 3.7 and 3.12. Countries ordered by the END-basis value.", fontsize=7, color=GREY)
    fig.savefig(OUT / "fig2_dalys.png", bbox_inches="tight", facecolor="white")


def fig3():
    fig, ax = plt.subplots(figsize=(9.6, 3.6), dpi=220)
    share = {g: int(EXP[g]["road"]) / POP[g] * 100 for g in EU}
    items = sorted(share.items(), key=lambda kv: kv[1])
    ax.bar([k for k, _ in items], [v for _, v in items], color=[GREEN if k == "MT" else SAGE for k, _ in items], width=0.72)
    for i, (k, v) in enumerate(items):
        if k in ("MT", "SK", "LU", "CY"):
            ax.text(i, v + 0.8, f"{v:.1f}", ha="center", fontsize=8, color=GREEN if k == "MT" else SLATE, fontweight="bold")
    ax.set_ylabel("% of population")
    ax.tick_params(axis="x", labelsize=8)
    ax.text(-0.5, -9.5, "People exposed to road noise above 55 dB Lden (EEA 2025 report Table 2.1) over population on 1 Jan 2022 (Eurostat demo_pjan). "
            "Reported exposure only; coverage differs between countries.", fontsize=7, color=GREY)
    fig.savefig(OUT / "fig3_roadshare.png", bbox_inches="tight", facecolor="white")


fig1(); fig2(); fig3()
print("figures in", OUT)
