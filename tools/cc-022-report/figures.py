"""Figures for Claim Check 022, drawn from data/cc-022/ (run fetch_data.py first)."""
import csv, pathlib
from collections import defaultdict
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm

HERE = pathlib.Path(__file__).resolve().parent
D = HERE.parents[1] / "data" / "cc-022"
OUT = HERE / "out"
OUT.mkdir(exist_ok=True)
for f in ["LiberationSans-Regular", "LiberationSans-Bold", "LiberationSans-Italic"]:
    fm.fontManager.addfont(f"/usr/share/fonts/truetype/liberation/{f}.ttf")
plt.rcParams.update({"font.family": "Liberation Sans", "axes.spines.top": False, "axes.spines.right": False,
                     "axes.edgecolor": "#8A9399", "axes.labelcolor": "#2B3A42", "xtick.color": "#2B3A42",
                     "ytick.color": "#2B3A42"})
GREEN, SAGE, AMBER, RED, SLATE, GREY, ORANGE, BLUE = ("#14452F", "#7FA88B", "#E3A72F", "#B5483A", "#2B3A42",
                                                      "#8A9399", "#D9772B", "#3C6E8F")
EU = "AT BE BG CY CZ DE DK EE EL ES FI FR HR HU IE IT LT LU LV MT NL PL PT RO SE SI SK".split()
P = defaultdict(dict)
for r in csv.DictReader(open(D / "eurostat_prices.csv")):
    P[(r["currency"], r["geo"])][r["time"]] = float(r["value"])


def fig1():
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(9.6, 4.6), dpi=220)
    for ax, cur, title in ((a1, "EUR", "Nominal price, EUR per 100 kWh"), (a2, "PPS", "Price in purchasing power (PPS per 100 kWh)")):
        v = sorted((100 * P[(cur, g)]["2024-S2"], g) for g in EU)
        ax.barh([g for _, g in v], [x for x, _ in v], color=[ORANGE if g == "MT" else SAGE for _, g in v], height=0.7)
        ax.tick_params(axis="y", labelsize=6.5)
        ax.invert_yaxis()
        ax.set_title(title, fontsize=9, color=GREEN, loc="left", fontweight="bold")
        mt = 100 * P[(cur, "MT")]["2024-S2"]
        ax.text(mt + 0.5, [g for _, g in v].index("MT"), f"{mt:.1f}", va="center", fontsize=8, color=ORANGE,
                fontweight="bold")
    fig.text(0.01, -0.02, "Households, consumption band DC (2,500-4,999 kWh), all taxes included, second half of 2024. "
             "Source: Eurostat nrg_pc_204 (retrieved 4 Oct 2026).", fontsize=7, color=GREY)
    fig.tight_layout(w_pad=2)
    fig.savefig(OUT / "fig1_ranking.png", bbox_inches="tight", facecolor="white")


def fig2():
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(9.6, 3.6), dpi=220, gridspec_kw={"width_ratios": [1.4, 1]})
    ts = sorted(P[("EUR", "MT")])
    for g, col, lab, ls in (("MT", ORANGE, "Malta", "-"), ("EU27_2020", BLUE, "EU-27", "--")):
        a1.plot(range(len(ts)), [100 * P[("EUR", g)][t] for t in ts], color=col, lw=2.3, ls=ls, label=lab)
    a1.set_xticks(range(0, len(ts), 2))
    a1.set_xticklabels([t[:4] for t in ts[::2]], fontsize=8)
    a1.set_ylim(0, 32)
    a1.set_ylabel("EUR cents per kWh")
    a1.legend(frameon=False, fontsize=8)
    a1.set_title("Household price, nominal", fontsize=9, color=GREEN, loc="left", fontweight="bold")
    S = list(csv.DictReader(open(D / "imf_energy_subsidies.csv")))
    ys = [s["year"] for s in S]
    eur = [float(s["energy_subsidies_pct_gdp"]) / 100 * float(s["gdp_meur"]) for s in S]
    b = a2.bar(ys, eur, color=[RED, RED, RED, GREY], width=0.6)
    for r, e in zip(b, eur):
        a2.text(r.get_x() + r.get_width() / 2, e + 6, f"{e:.0f}", ha="center", fontsize=9, color=SLATE)
    a2.set_ylim(0, 380)
    a2.set_ylabel("EUR million")
    a2.set_title("Energy subsidies (electricity and fuel)", fontsize=9, color=GREEN, loc="left", fontweight="bold")
    fig.text(0.01, -0.04, "Left: Eurostat nrg_pc_204. Right: IMF Country Report 26/29, Table 2 (% of GDP; 2025 grey = "
             "projection) x Eurostat nominal GDP.", fontsize=7, color=GREY)
    fig.tight_layout(w_pad=3)
    fig.savefig(OUT / "fig2_price_subsidy.png", bbox_inches="tight", facecolor="white")


fig1()
fig2()
print("figures in", OUT)
