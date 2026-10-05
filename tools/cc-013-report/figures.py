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


EU = "AT BE BG CY CZ DE DK EE EL ES FI FR HR HU IE IT LT LU LV MT NL PL PT RO SE SI SK".split()
NAMES = {"MT": "Malta", "LU": "Luxembourg", "IE": "Ireland", "PT": "Portugal", "HU": "Hungary", "DE": "Germany",
         "FR": "France", "IT": "Italy", "HR": "Croatia", "EU27_2020": "EU-27 aggregate"}


def fig3():
    """v1.2: population change vs real house price change, 2015-2025, all EU-27 Member States."""
    import statistics
    V = defaultdict(dict)
    for r in csv.DictReader(open(D / "eurostat_eu27_pop_prices_rents.csv")):
        V[(r["series"], r["geo"])][r["time"]] = float(r["value"])
    ch = lambda s, g: 100 * (V[(s, g)]["2025"] / V[(s, g)]["2015"] - 1)
    fig, ax = plt.subplots(figsize=(9.6, 5.0), dpi=220)
    med = statistics.median(ch("real", g) for g in EU)
    ax.axhline(med, color=GREY, lw=0.8, ls=":")
    ax.text(-19.5, med + 2.5, f"median Member State {med:+.0f}%", fontsize=7.6, color=GREY, ha="left")
    ax.axhline(0, color=GREY, lw=0.6)
    ax.axvline(0, color=GREY, lw=0.6)
    for g in EU:
        if g == "MT":
            continue
        lab = g in NAMES
        ax.scatter(ch("pop", g), ch("real", g), s=34 if lab else 22, color=SLATE if lab else GREY,
                   alpha=0.9 if lab else 0.5, lw=0, zorder=3)
    e = ("EU27_2020")
    ax.scatter(ch("pop", e), ch("real", e), s=70, marker="D", color=BLUE, zorder=4, edgecolor="white", lw=0.8)
    ax.scatter(ch("pop", "MT"), ch("real", "MT"), s=110, color=RED, zorder=5, edgecolor="white", lw=1)
    off = {"MT": (-0.8, -10, "right"), "LU": (0.7, 0, "left"), "IE": (0.7, 0, "left"), "PT": (0.7, 0, "left"),
           "HU": (0.7, -1, "left"), "DE": (0.7, -3.5, "left"), "FR": (0.7, -7, "left"), "IT": (0.7, -1, "left"),
           "HR": (0.7, 0, "left"), "EU27_2020": (0.8, 4.5, "left")}
    for g, (dx, dy, ha) in off.items():
        x, y = ch("pop", g), ch("real", g)
        txt = f"{NAMES[g]}  {y:+.0f}%".replace("  -", "  −") if g != "MT" else f"Malta: population {x:+.0f}%, real prices {y:+.0f}%\n16th of 27 on price growth"
        if g == "FR":
            ax.plot([x + 0.2, x + 0.8], [y - 1.2, y + dy + 1.6], color=SLATE, lw=0.6)
        ax.text(x + dx, y + dy, txt, fontsize=8.6 if g == "MT" else 7.8, ha=ha, va="center",
                color=RED if g == "MT" else BLUE if g == "EU27_2020" else SLATE,
                fontweight="bold" if g in ("MT", "EU27_2020") else "normal")
    ax.set_xlim(-20, 34)
    ax.set_ylim(-15, 118)
    ax.set_xlabel("Change in population, 2015–2025 (%)")
    ax.set_ylabel("Change in real house prices, 2015–2025 (%)")
    ax.set_title("Fastest population growth in the EU; house prices rose less than in most Member States",
                 fontsize=10.5, color=GREEN, loc="left", fontweight="bold")
    ax.text(-20, -38, "Real prices: house price index deflated by consumer prices (HICP), annual averages. Malta’s and "
            "Hungary’s 2025 values provisional; Greece’s estimated; series breaks in 2015 for Bulgaria and Cyprus.\n"
            "Population on 1 January. Source: Eurostat tipsho10, demo_gind (retrieved 5 Oct 2026). In the EU-27 "
            "aggregate Germany, France and Italy carry 49% of the weight (prc_hpi_cow, 2025).",
            fontsize=7, color=GREY, va="top")
    fig.savefig(OUT / "fig3_eu_scatter.png", bbox_inches="tight", facecolor="white")
    plt.close(fig)


fig1()
fig2()
fig3()
print("figures in", OUT)
