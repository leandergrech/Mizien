"""Figures for Claim Check 013, drawn from data/cc-013/ (run calc.py first)."""
import csv, pathlib
from collections import defaultdict
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
D = ROOT / "data" / "cc-013"
E = defaultdict(dict)
for r in csv.DictReader(open(D / "eurostat_housing.csv")):
    if r["dataset"] != "#":
        E[(r["dataset"], r["geo"])][int(r["year"])] = float(r["value"])
PA = {int(r["year"]): int(r["approved_units_total"]) for r in csv.DictReader(open(D / "pa_approved_dwellings.csv"))}


def fig1():
    fig, ax = plt.subplots(figsize=(9.6, 4.6), dpi=220)
    yrs = sorted(PA)
    ax.bar(yrs, [PA[y] for y in yrs], color=SAGE, width=0.7, label="Dwelling units approved (PA, left axis)")
    ax.set_ylabel("Units approved per year")
    ax.set_ylim(0, 14500)
    ax2 = ax.twinx()
    ax2.spines["right"].set_visible(True)
    ys = list(range(2007, 2026))
    for key, col, lab, ls in ((("tipsho10", "MT"), GREEN, "Malta house prices, real", "-"),
                              (("tipsho10", "EU27_2020"), BLUE, "EU-27 house prices, real", "--"),
                              (("demo_gind", "MT"), ORANGE, "Malta population", ":")):
        s = E[key]
        xs = [y for y in ys if y in s]
        ax2.plot(xs, [100 * s[y] / s[2015] for y in xs], color=col, lw=2.4, ls=ls, label=lab)
        ax2.text(2025.3, 100 * s[2025] / s[2015], f"{100 * s[2025] / s[2015] - 100:+.0f}%", color=col, fontsize=8.5,
                 va="center", fontweight="bold")
    ax2.set_ylabel("Index, 2015 = 100")
    ax2.set_ylim(60, 145)
    ax.set_xlim(2006.3, 2026.4)
    ax.set_xticks(range(2007, 2026, 2))
    h1, l1 = ax.get_legend_handles_labels()
    h2, l2 = ax2.get_legend_handles_labels()
    ax.legend(h1 + h2, l1 + l2, frameon=False, fontsize=8, loc="upper left")
    ax.text(2006.4, -2600, "House prices deflated by HICP. Sources: Planning Authority, Approved Dwelling Units 2007–2025; "
            "Eurostat tipsho10, demo_gind (retrieved 3 Oct 2026). Changes shown are 2015–2025.", fontsize=7, color=GREY)
    fig.savefig(OUT / "fig1_permits_prices.png", bbox_inches="tight", facecolor="white")


def fig2():
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(9.6, 3.6), dpi=220)
    for ax, ds, title in ((a1, "ilc_lvho07a", "Housing cost overburden (% of people)"),
                          (a2, "ilc_lvho05a", "Overcrowding (% of people)")):
        for geo, col, lab, ls in (("MT", GREEN, "Malta", "-"), ("EU27_2020", BLUE, "EU-27", "--")):
            s = E[(ds, geo)]
            xs = [y for y in range(2010, 2026) if y in s]
            ax.plot(xs, [s[y] for y in xs], color=col, lw=2.2, ls=ls, label=lab)
            ax.text(2025.3, s[2025], f"{s[2025]:.1f}", color=col, fontsize=8.5, va="center", fontweight="bold")
        ax.set_title(title, fontsize=9.5, color=GREEN, loc="left", fontweight="bold")
        ax.set_ylim(0, None)
        ax.set_xlim(2010, 2026.5)
        ax.legend(frameon=False, fontsize=8)
    a1.set_xlabel("Source: Eurostat ilc_lvho07a (households spending over 40% of income on housing).",
                  fontsize=7, color=GREY)
    a2.set_xlabel("Source: Eurostat ilc_lvho05a.", fontsize=7, color=GREY)
    fig.tight_layout(w_pad=2.5)
    fig.savefig(OUT / "fig2_affordability.png", bbox_inches="tight", facecolor="white")


fig1()
fig2()
print("figures in", OUT)
