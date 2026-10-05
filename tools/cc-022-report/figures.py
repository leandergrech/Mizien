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
    # v1.2: Malta and EU-27 since 2012 (band DC, EUR, all taxes), so the 2014 tariff cut is visible
    H = defaultdict(dict)
    for r in csv.DictReader(open(D / "eurostat_prices_mt_history.csv")):
        H[r["geo"]][r["time"]] = float(r["value"])
    ts = sorted(H["MT"])
    for g, col, lab, ls in (("MT", ORANGE, "Malta", "-"), ("EU27_2020", BLUE, "EU-27", "--")):
        a1.plot(range(len(ts)), [100 * H[g][t] for t in ts], color=col, lw=2.3, ls=ls, label=lab)
    i14 = ts.index("2014-S2")
    a1.annotate("2014: cut from 16.9\nto 12.5 cents", xy=(i14, 100 * H["MT"]["2014-S2"]), xytext=(i14 + 1.2, 5),
                fontsize=7.5, color=SLATE, arrowprops=dict(arrowstyle="-", color=SLATE, lw=0.7))
    a1.set_xticks(range(0, len(ts), 4))
    a1.set_xticklabels([t[:4] for t in ts[::4]], fontsize=8)
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
    fig.text(0.01, -0.04, "Left: Eurostat nrg_pc_204, band DC (2,500–4,999 kWh), all taxes; 2025-S2 provisional for Malta. Right: IMF Country Report 26/29, Table 2 (% of GDP; 2025 grey = "
             "projection) x Eurostat nominal GDP.", fontsize=7, color=GREY)
    fig.tight_layout(w_pad=3)
    fig.savefig(OUT / "fig2_price_subsidy.png", bbox_inches="tight", facecolor="white")


NAMES = {"MT": "Malta", "LU": "Luxembourg", "EU27_2020": "EU-27"}
BANDLAB = (("KWH_LT1000", "Under 1,000 kWh (DA)"), ("KWH1000-2499", "1,000–2,499 kWh (DB)"),
           ("KWH2500-4999", "2,500–4,999 kWh (DC): typical"), ("KWH5000-14999", "5,000–14,999 kWh (DD)"),
           ("KWH_GE15000", "15,000 kWh or more (DE)"), ("TOT_KWH", "All bands (Eurostat average)"))


def ordinal(n):
    return f"{n}{'th' if 10 <= n % 100 <= 20 else {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')}"


def fig3():
    """v1.2: Malta's PPS price and rank in each consumption band, 2024-S2 and 2025-S2 (small multiples)."""
    B = {}
    for r in csv.DictReader(open(D / "eurostat_prices_bands.csv")):
        B[(r["nrg_cons"], r["geo"], r["time"])] = (100 * float(r["value"]), r["flag"])
    fig, axs = plt.subplots(2, 3, figsize=(9.6, 4.6), dpi=220, sharex=True)
    for ax, (band, title) in zip(axs.flat, BANDLAB):
        for y, t in ((1, "2024-S2"), (0, "2025-S2")):
            vals = sorted((B[(band, g, t)][0], g) for g in EU if (band, g, t) in B)
            ax.scatter([v for v, g in vals if g != "MT"], [y] * (len(vals) - 1), s=16, color=GREY, alpha=0.45,
                       lw=0, zorder=2)
            eu = B[(band, "EU27_2020", t)][0]
            ax.plot([eu, eu], [y - 0.22, y + 0.22], color=BLUE, lw=2, zorder=3)
            mt, flag = B[(band, "MT", t)]
            rk = [g for _, g in vals].index("MT") + 1
            ax.scatter([mt], [y], s=60, color=RED, zorder=4, edgecolor="white", lw=0.8)
            ax.text(mt, y + 0.27, f"{ordinal(rk)} of {len(vals)}", ha="center", va="bottom", fontsize=7.6,
                    color=RED, fontweight="bold")
        ax.set_title(title, fontsize=8.6, color=GREEN, loc="left", fontweight="bold")
        ax.set_ylim(-0.5, 1.75)
        ax.set_yticks([1, 0])
        ax.set_yticklabels(["2024-S2", "2025-S2"], fontsize=7.6)
        ax.tick_params(axis="x", labelsize=7.6)
        ax.spines["left"].set_visible(False)
        ax.tick_params(axis="y", length=0)
        ax.grid(axis="x", color="#E3E6E8", lw=0.6)
        ax.set_axisbelow(True)
    for ax in axs[1]:
        ax.set_xlabel("PPS per 100 kWh, all taxes", fontsize=7.6)
    from matplotlib.lines import Line2D
    fig.legend(handles=[Line2D([], [], marker="o", ls="", color=RED, ms=7, label="Malta (rank of 27; 1 = cheapest)"),
                        Line2D([], [], marker="o", ls="", color=GREY, alpha=0.6, ms=5, label="Other Member States"),
                        Line2D([], [], color=BLUE, lw=2, label="EU-27 average")],
               loc="upper center", ncol=3, frameon=False, fontsize=7.8, bbox_to_anchor=(0.5, 1.04))
    fig.text(0.01, -0.035, "Household prices in purchasing power standards, all taxes, by annual consumption band. "
             "Malta’s 2025-S2 band prices are provisional. Luxembourg has no all-band average in 2024-S2\n(26 "
             "countries). The Netherlands’ price under 1,000 kWh is negative in 2024-S2, as Eurostat publishes it. "
             "Source: Eurostat nrg_pc_204 (retrieved 5 Oct 2026).", fontsize=7, color=GREY, va="top")
    fig.tight_layout(h_pad=1.6, w_pad=1.4)
    fig.savefig(OUT / "fig3_bands.png", bbox_inches="tight", facecolor="white")
    plt.close(fig)


def fig4():
    """v1.2: Malta's rank on each burden measure (1 = lowest burden), with Malta and EU-27 values."""
    import sys
    sys.path.insert(0, str(HERE))
    from burden import measures
    R = defaultdict(dict)
    for r in measures():
        R[r["measure"]][r["geo"]] = r
    Bp = {}
    for r in csv.DictReader(open(D / "eurostat_prices_bands.csv")):
        Bp[(r["nrg_cons"], r["geo"], r["time"])] = 100 * float(r["value"])
    pv = sorted((Bp[("KWH2500-4999", g, "2024-S2")], g) for g in EU)
    rows = [("Price in purchasing power, typical household\n(the release’s measure), 2024-S2",
             {g: i + 1 for i, (_, g) in enumerate(pv)}, 27, False,
             f"{Bp[('KWH2500-4999', 'MT', '2024-S2')]:.2f} vs {Bp[('KWH2500-4999', 'EU27_2020', '2024-S2')]:.2f} PPS")]

    def row(label, key, unit="%", eu=True, dec=1):
        d = R[key]
        rk = {g: r["rank"] for g, r in d.items() if r["rank"]}
        n = d["MT"]["of"]
        e = f"{d['EU27_2020']['value']:.{dec}f}{unit}" if eu and "EU27_2020" in d else ""
        txt = f"{d['MT']['value']:.{dec}f}{unit}" + (f" vs {e}" if e else "")
        rows.append((label, rk, n, d["MT"]["tied"], txt))

    row("Bill for 3,750 kWh as a share of\nmedian income, 2024", "M1 bill 3750 kWh / median income (SILC 2025) MAIN")
    row("Same bill as a share of a low income\n(20th percentile), 2024", "M3 bill 3750 kWh / 20th-percentile income (SILC 2025) MAIN")
    row("Average household’s actual bill as a share\nof its disposable income, 2024",
        "M2 bill / disposable income per household (2024) MAIN", dec=2)
    hb = R["M4 electricity share of consumption spending, % (HBS 2020) MAIN"]
    rows.append(("Electricity’s share of household\nspending, 2020 (before the 2022 shock)",
                 {g: r["rank"] for g, r in hb.items() if r["rank"]}, hb["MT"]["of"], hb["MT"]["tied"],
                 f"{hb['MT']['value']:.1f}% vs 2.8% (median)"))
    row("People in arrears on utility bills, 2025", "M5 arrears on utility bills, % (all, 2025) MAIN")
    row("People unable to keep the home\nadequately warm, 2025", "M5 unable to keep home warm, % (all, 2025) MAIN")
    fig = plt.figure(figsize=(9.6, 5.0), dpi=220)
    ax = fig.add_axes([0.31, 0.1, 0.5, 0.8])
    n_rows = len(rows)
    for i, (label, rk, n, tied, txt) in enumerate(rows):
        y = n_rows - 1 - i
        ax.plot([1, n], [y, y], color="#E3E6E8", lw=6, solid_capstyle="round", zorder=1)
        others = [r for g, r in rk.items() if g != "MT"]
        ax.scatter(others, [y] * len(others), s=14, color=GREY, alpha=0.55, lw=0, zorder=2)
        m = rk["MT"]
        ax.scatter([m], [y], s=95, color=RED, zorder=4, edgecolor="white", lw=1)
        ax.text(m, y + 0.3, f"{'joint ' if tied else ''}{ordinal(m)} of {n}", ha="center", va="bottom", fontsize=8, fontweight="bold",
                color=SLATE)
        ax.text(-0.6, y, label, ha="right", va="center", fontsize=8.2, color=SLATE)
        ax.text(28.4, y, txt, ha="left", va="center", fontsize=8.2, color=SLATE)
    ax.set_xlim(0.3, 27.7)
    ax.set_ylim(-0.6, n_rows - 0.2)
    ax.set_yticks([])
    ax.set_xticks([1, 5, 10, 15, 20, 25, 27])
    ax.tick_params(axis="x", labelsize=7.8)
    for sp in ("left", "bottom"):
        ax.spines[sp].set_visible(False)
    ax.set_xlabel("Rank among EU Member States (1 = lowest burden)", fontsize=8.2)
    ax.text(28.4, n_rows - 0.35, "Malta vs EU-27", fontsize=8.2, color=GREY, fontweight="bold", va="bottom")
    fig.text(0.01, 0.975, "Malta is cheapest on price, second against income, fifth on actual use", fontsize=11,
             color=GREEN, ha="left", va="top", fontweight="bold")
    fig.text(0.01, 0.01, "Bills: band DC price (2024 average of S1 and S2, all taxes) x 3,750 kWh; median and "
             "20th-percentile equivalised income, EU-SILC 2025 (income year 2024). Actual bill: household use per "
             "household x\nconsumption-weighted price; income: gross disposable income of households per household. "
             "Spending share: Household Budget Survey 2020 (24 countries). Sources: Eurostat nrg_pc_204, "
             "nrg_pc_204_v,\nilc_di03, ilc_di01, nrg_d_hhq, lfst_hhnhtych, nasa_10_nf_tr, hbs_str_t211, ilc_mdes07, "
             "ilc_mdes01 (retrieved 5 Oct 2026). Data: data/cc-022/burden_measures.csv.", fontsize=6.8, color=GREY,
             va="top")
    fig.savefig(OUT / "fig4_burden.png", bbox_inches="tight", facecolor="white")
    plt.close(fig)


fig1()
fig2()
fig3()
fig4()
print("figures in", OUT)
