"""Figures for Claim Check 018, drawn from data/cc-018/ and data/cc-013/ (run calc.py first)."""
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
P = defaultdict(dict)
for r in csv.DictReader(open(ROOT / "data" / "cc-018" / "eurostat_tipsho60.csv")):
    P[(r["unit"], r["geo"])][int(r["year"])] = float(r["value"])
E = defaultdict(dict)
for r in csv.DictReader(open(ROOT / "data" / "cc-013" / "eurostat_housing.csv")):
    if r["dataset"] != "#":
        E[(r["dataset"], r["geo"])][int(r["year"])] = float(r["value"])


def fig1():
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(9.6, 3.8), dpi=220)
    for geo, col, lab, ls in (("MT", GREEN, "Malta", "-"), ("EU27_2020", BLUE, "EU-27", "--")):
        s = P[("PTIR_LT_AVG", geo)]
        xs = [y for y in sorted(s) if y >= 2005]
        a1.plot(xs, [s[y] for y in xs], color=col, lw=2.3, ls=ls, label=lab)
        a1.text(xs[-1] + 0.3, s[xs[-1]], f"{s[xs[-1]]:.0f}", color=col, fontsize=8.5, fontweight="bold", va="center")
    a1.axhline(100, color=GREY, lw=0.8)
    a1.text(2005.2, 101.5, "long-term average = 100", fontsize=7.5, color=GREY)
    a1.set_title("House price-to-income ratio", fontsize=9.5, color=GREEN, loc="left", fontweight="bold")
    a1.legend(frameon=False, fontsize=8, loc="upper right")
    a1.set_xlim(2005, 2025.8)
    a1.set_xticks(range(2005, 2026, 5))
    for geo, col, lab, ls in (("MT", GREEN, "Malta", "-"), ("EU27_2020", BLUE, "EU-27", "--")):
        s = E[("ilc_lvho07a", geo)]
        xs = [y for y in sorted(s) if y >= 2010]
        a2.plot(xs, [s[y] for y in xs], color=col, lw=2.3, ls=ls, label=lab)
        a2.text(xs[-1] + 0.3, s[xs[-1]], f"{s[xs[-1]]:.1f}", color=col, fontsize=8.5, fontweight="bold", va="center")
    a2.set_ylim(0, None)
    a2.set_xlim(2010, 2026.6)
    a2.set_title("Housing-cost overburden (% of people)", fontsize=9.5, color=GREEN, loc="left", fontweight="bold")
    a2.legend(frameon=False, fontsize=8)
    fig.text(0.01, -0.03, "Sources: Eurostat tipsho60 (standardised price-to-income ratio, retrieved 4 Oct 2026) and "
             "ilc_lvho07a (households spending over 40% of income on housing).", fontsize=7, color=GREY)
    fig.tight_layout(w_pad=3)
    fig.savefig(OUT / "fig1_price_income.png", bbox_inches="tight", facecolor="white")


def fig2():
    fig, ax = plt.subplots(figsize=(9.6, 2.6), dpi=220)
    labs = ["Real estate and construction,\nshare of private loans", "Residential mortgages,\nshare of private lending"]
    old, new = [61, 44], [72, 57]
    y = range(len(labs))
    ax.barh([i + 0.2 for i in y], old, height=0.38, color=GREY, label="About 2015")
    ax.barh([i - 0.2 for i in y], new, height=0.38, color=ORANGE, label="Mid-2025")
    for i in y:
        ax.text(old[i] + 1, i + 0.2, f"{old[i]}%", va="center", fontsize=9, color=SLATE)
        ax.text(new[i] + 1, i - 0.2, f"{new[i]}%", va="center", fontsize=9, color=SLATE, fontweight="bold")
    ax.set_yticks(list(y))
    ax.set_yticklabels(labs, fontsize=9)
    ax.set_xlim(0, 85)
    ax.invert_yaxis()
    ax.legend(frameon=False, fontsize=8, loc="lower right")
    ax.set_title("Banks' exposure to property, which the IMF calls a vulnerability", fontsize=9.5, color=GREEN,
                 loc="left", fontweight="bold")
    ax.set_xlabel("Source: IMF Country Report 26/29, para. 19.", fontsize=7, color=GREY)
    fig.savefig(OUT / "fig2_bank_exposure.png", bbox_inches="tight", facecolor="white")


def fig3():
    """v1.2: house prices (quarterly) against income per head (annual), Malta, 2015 = 100."""
    M, FL = defaultdict(dict), {}
    for r in csv.DictReader(open(ROOT / "data" / "cc-018" / "eurostat_more.csv")):
        M[(r["dataset"], r["unit"])][r["time"]] = float(r["value"]) if r["geo"] == "MT" else None
        if r["geo"] == "MT":
            FL[(r["dataset"], r["unit"], r["time"])] = r["flag"]
    hq = {k: v for k, v in M[("prc_hpi_q", "I15_Q")].items() if v is not None}
    inc, pop = M[("nasa_10_nf_tr", "CP_MEUR")], M[("nama_10_pe", "THS_PER")]
    iph = {y: inc[y] / pop[y] for y in inc if y in pop and inc[y] is not None}
    iph = {y: 100 * v / iph["2015"] for y, v in iph.items()}
    gdp = {y: v for y, v in M[("nama_10_pc", "CP_EUR_HAB")].items() if v is not None and y >= "2015"}
    gdp = {y: 100 * v / gdp["2015"] for y, v in gdp.items()}
    qx = lambda q: int(q[:4]) + (int(q[-1]) - 1) / 4 + 0.125
    fig, ax = plt.subplots(figsize=(9.6, 4.0), dpi=220)
    qs = sorted(hq)
    fin = [q for q in qs if "p" not in FL[("prc_hpi_q", "I15_Q", q)]]
    prov = [q for q in qs if "p" in FL[("prc_hpi_q", "I15_Q", q)]]
    ax.plot([qx(q) for q in fin], [hq[q] for q in fin], color=GREEN, lw=2, label="House prices (quarterly)")
    ax.plot([qx(q) for q in [fin[-1]] + prov], [hq[q] for q in [fin[-1]] + prov], color=GREEN, lw=2, ls=(0, (2, 1.4)))
    ys = sorted(iph)
    ax.plot([int(y) + 0.5 for y in ys], [iph[y] for y in ys], color=BLUE, lw=2, marker="o", ms=4.5,
            label="Household disposable income per head (annual)")
    yg = sorted(gdp)
    ax.plot([int(y) + 0.5 for y in yg], [gdp[y] for y in yg], color=GREY, lw=1.6, ls="--", marker="s", ms=3.5,
            label="GDP per head, current prices (annual)")
    lq, ly, lg = qs[-1], ys[-1], yg[-1]
    ax.annotate(f"{hq[lq]:.0f}  house prices,\n{lq} (provisional)", (qx(lq), hq[lq]), xytext=(8, -4),
                textcoords="offset points", fontsize=8, color=SLATE, va="top")
    ax.annotate(f"{iph[ly]:.0f}  income per head, {ly}", (int(ly) + 0.5, iph[ly]), xytext=(-6, 9),
                textcoords="offset points", fontsize=8, color=SLATE, ha="right")
    ax.annotate(f"{gdp[lg]:.0f}  GDP per head, {lg}", (int(lg) + 0.5, gdp[lg]), xytext=(8, 4),
                textcoords="offset points", fontsize=8, color=SLATE)
    ax.axhline(100, color=GREY, lw=0.7)
    ax.set_xlim(2015, 2028.4)
    ax.set_xticks(range(2015, 2027))
    ax.tick_params(labelsize=8.5)
    ax.set_ylim(90, 200)
    ax.set_ylabel("Index, 2015 = 100", fontsize=8.5)
    ax.grid(axis="y", color="#E3E6E8", lw=0.6)
    ax.set_axisbelow(True)
    ax.legend(frameon=False, fontsize=8, loc="upper left")
    ax.set_title("House prices and incomes per head, Malta", fontsize=9.5, color=GREEN, loc="left",
                 fontweight="bold")
    fig.text(0.01, -0.05, "Sources: Eurostat prc_hpi_q (house price index; dashed: provisional), nasa_10_nf_tr "
             "(households' gross disposable income, B6G, S14_S15) divided by nama_10_pe (population; 2021-24 "
             "provisional;\nno data after 2024) and nama_10_pc (GDP per head). Retrieved 5 Oct 2026. Annual values "
             "plotted at mid-year.", fontsize=7, color=GREY)
    fig.tight_layout()
    fig.savefig(OUT / "fig3_prices_incomes.png", bbox_inches="tight", facecolor="white")


if __name__ == "__main__":
    import sys
    todo = sys.argv[1:] or ["fig1", "fig2", "fig3"]
    for f in todo:
        globals()[f]()
    print("figures in", OUT)
