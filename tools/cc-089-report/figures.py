"""Figures for Claim Check 089, drawn from data/cc-089/ (run fetch.py and calc.py first)."""
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
D = ROOT / "data" / "cc-089"
EU = "AT BE BG CY CZ DE DK EE EL ES FI FR HR HU IE IT LT LU LV MT NL PL PT RO SE SI SK".split()
load = lambda n: list(csv.DictReader(open(D / f"{n}.csv")))
POP, PROJ, BEDS, EL = defaultdict(dict), defaultdict(dict), defaultdict(dict), defaultdict(dict)
for r in load("eurostat_pop"):
    POP[r["geo"]][int(r["time"])] = float(r["value"])
for r in load("eurostat_proj"):
    PROJ[r["projection"]][int(r["time"])] = float(r["value"])
for r in load("eurostat_beds_100k"):
    BEDS[r["geo"]][int(r["time"])] = float(r["value"])
for r in load("eurostat_elec"):
    EL[r["nrg_bal"]][int(r["time"])] = float(r["value"])


def fig1():
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(9.6, 4.2), dpi=220, gridspec_kw={"width_ratios": [1.05, 1]})
    g = {c: 100 * (POP[c][2026] / POP[c][2015] - 1) for c in EU}
    order = sorted(EU, key=lambda c: g[c])
    a1.barh(range(len(order)), [g[c] for c in order], color=[RED if c == "MT" else SAGE for c in order], height=0.75)
    a1.set_yticks(range(len(order)))
    a1.set_yticklabels(order, fontsize=6.6)
    a1.axvline(100 * (POP["EU27_2020"][2026] / POP["EU27_2020"][2015] - 1), color=BLUE, lw=1, ls="--")
    a1.text(100 * (POP["EU27_2020"][2026] / POP["EU27_2020"][2015] - 1) + 0.6, 2, "EU-27 +2%", color=BLUE, fontsize=8)
    a1.text(g["MT"] - 0.6, len(order) - 1, f"Malta +{g['MT']:.0f}%", color="white", fontsize=8.6, ha="right", va="center",
            fontweight="bold")
    a1.set_title("Population change, 1 Jan 2015 to 1 Jan 2026 (%)", fontsize=9.5, color=GREEN, loc="left", fontweight="bold")
    yrs = list(range(2015, 2027))
    a2.plot(yrs, [POP["MT"][y] / 1000 for y in yrs], color=GREEN, lw=2.6, label="Malta, actual (1 January)")
    py = list(range(2026, 2032))
    for v, col, lab, ls in (("HMIGR", ORANGE, "EUROPOP2025, higher migration", "--"), ("BSL", BLUE, "EUROPOP2025, baseline", "--"),
                            ("LMIGR", GREY, "EUROPOP2025, lower migration", ":")):
        a2.plot(py, [PROJ[v][y] / 1000 for y in py], color=col, lw=1.8, ls=ls, label=lab)
    a2.scatter([2030, 2031], [636, 636], color=RED, s=34, zorder=5, marker="D", label="PwC base case: 636,000 by 2030")
    a2.set_ylim(455, 670)
    a2.set_xlim(2014.6, 2031.4)
    a2.set_ylabel("Thousand residents")
    a2.legend(frameon=False, fontsize=7, loc="upper left")
    a2.set_title("Actual and projected population", fontsize=9.5, color=GREEN, loc="left", fontweight="bold")
    fig.text(0.01, -0.03, "Sources: Eurostat demo_gind (updated 30 Sep 2026; EU-27 values provisional), proj_25np (EUROPOP2025, 11 Jun 2026); "
             "PwC Malta release (diamonds: the release says “by 2030”, so both 2030 and 2031 are marked). Retrieved 13 Oct 2026.",
             fontsize=6.6, color=GREY)
    fig.tight_layout(w_pad=2)
    fig.savefig(OUT / "fig1_population.png", bbox_inches="tight", facecolor="white")
    plt.close(fig)


def fig2():
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(9.6, 4.3), dpi=220, gridspec_kw={"width_ratios": [1.05, 1]})
    v = {c: BEDS[c][2024] for c in EU}
    order = sorted(EU, key=lambda c: v[c])
    a1.barh(range(len(order)), [v[c] for c in order], color=[RED if c == "MT" else SAGE for c in order], height=0.75)
    a1.set_yticks(range(len(order)))
    a1.set_yticklabels(order, fontsize=6.6)
    a1.axvline(BEDS["EU27_2020"][2024], color=BLUE, lw=1, ls="--")
    a1.text(BEDS["EU27_2020"][2024] + 6, 1.5, f"EU-27 {BEDS['EU27_2020'][2024]:.0f}", color=BLUE, fontsize=8)
    a1.text(v["MT"] + 6, order.index("MT"), f"Malta {v['MT']:.0f} (18th)", color=RED, fontsize=8.4, va="center", fontweight="bold",
            bbox=dict(facecolor="white", edgecolor="none", pad=1.5), zorder=6)
    a1.set_title("Hospital beds per 100,000 residents, 2024", fontsize=9.5, color=GREEN, loc="left", fontweight="bold")
    yrs = list(range(2015, 2026))
    a2.bar([y - 0.2 for y in yrs], [EL["GEP"][y] for y in yrs], width=0.4, color=SAGE, label="Produced in Malta (gross)")
    a2.bar([y + 0.2 for y in yrs], [EL["IMP"][y] for y in yrs], width=0.4, color=ORANGE, label="Imported (interconnector)")
    a2.set_ylabel("GWh")
    a2.legend(frameon=False, fontsize=7.4, loc="upper left")
    a2.set_title("Electricity produced and imported", fontsize=9.5, color=GREEN, loc="left", fontweight="bold")
    fig.text(0.01, -0.03, "Sources: Eurostat hlth_rs_bds1 (Malta 2023 flagged break in series); nrg_cb_e (2025 provisional). "
             "Retrieved 13 Oct 2026.", fontsize=6.6, color=GREY)
    fig.tight_layout(w_pad=2)
    fig.savefig(OUT / "fig2_beds_electricity.png", bbox_inches="tight", facecolor="white")
    plt.close(fig)


fig1()
fig2()
print("figures in", OUT)
