"""Figures for Claim Check 003, drawn from data/cc-003/ (run calc.py first)."""
import csv, os, pathlib
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
v = defaultdict(dict)
for r in csv.DictReader(open(ROOT / "data" / "cc-003" / "eurostat_ghg_population.csv")):
    v[(r["geo"], r["item"])][int(r["year"])] = float(r["value"])


def fig1():
    yrs = list(range(2005, 2025))
    pop, tot = v[("MT", "POP_NC")], v[("MT", "TOTX4_MEMO")]
    epop, etot = v[("EU27_2020", "POP_NC")], v[("EU27_2020", "TOTX4_MEMO")]
    idx = lambda s: [100 * s[y] / s[2005] for y in yrs]
    pc = {y: tot[y] / pop[y] for y in yrs}
    epc = {y: etot[y] / epop[y] for y in yrs}
    fig, ax = plt.subplots(figsize=(9.6, 4.6), dpi=220)
    ax.plot(yrs, idx(pop), color=GREY, lw=2, label="Malta population")
    ax.plot(yrs, idx(tot), color=GREEN, lw=2.6, label="Malta total emissions")
    ax.plot(yrs, idx(pc), color=AMBER, lw=2.6, label="Malta emissions per person")
    ax.plot(yrs, idx(epc), color=BLUE, lw=1.6, ls="--", label="EU-27 emissions per person")
    ax.plot(yrs, idx(etot), color=BLUE, lw=1.6, ls=":", label="EU-27 total emissions")
    ax.axhline(100, color=GREY, lw=0.6)
    for s, col, dy in ((idx(pop), GREY, 0), (idx(tot), GREEN, 0), (idx(pc), AMBER, -1), (idx(epc), BLUE, 3),
                       (idx(etot), BLUE, -4)):
        ax.text(2024.3, s[-1] + dy, f"{s[-1] - 100:+.0f}%", color=col, fontsize=8.5, va="center", fontweight="bold")
    ax.set_xlim(2005, 2026.2)
    ax.set_ylabel("Index, 2005 = 100")
    ax.legend(frameon=False, fontsize=8, loc="upper left", ncol=2)
    ax.text(2005, 38, "Emissions exclude LULUCF and international aviation and shipping. Source: Eurostat env_air_gge, "
            "nama_10_pe (retrieved 2 Oct 2026).", fontsize=7, color=GREY)
    ax.set_ylim(35, 150)
    ax.set_xticks(range(2005, 2025, 5))
    fig.savefig(OUT / "fig1_index.png", bbox_inches="tight", facecolor="white")


def fig2():
    sect = [("Power generation (ETS)", "CRF1A1", GREY), ("Agriculture (ESR)", "CRF3", SAGE),
            ("Waste (ESR)", "CRF5", SAGE), ("Buildings and other\ncombustion (ESR)", "CRF1A4", ORANGE),
            ("Domestic transport (ESR)", "CRF1A3", RED), ("F-gases: refrigeration,\nair conditioning (ESR)", "CRF2F", RED)]
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(9.6, 4.2), dpi=220, gridspec_kw={"width_ratios": [1.35, 1]})
    names, vals, cols = [], [], []
    for n, k, c in sect:
        s = v[("MT", k)]
        names.append(n); vals.append(100 * (s[2024] / s[2005] - 1)); cols.append(c)
    shown = [min(x, 120) for x in vals]
    a1.barh(names, shown, color=cols)
    for i, x in enumerate(vals):
        a1.text(min(x, 120) + (3 if x >= 0 else -3), i, f"{x:+.0f}%", va="center", ha="left" if x >= 0 else "right",
                fontsize=8.5, color=SLATE, fontweight="bold")
    a1.axvline(0, color=SLATE, lw=0.8)
    a1.set_xlim(-90, 150)
    a1.set_title("Malta: change in emissions by sector, 2005–2024", fontsize=9.5, color=GREEN, loc="left",
                 fontweight="bold")
    a1.tick_params(axis="y", labelsize=8)
    a1.set_xlabel("% change, 2005 to 2024 (F-gas bar truncated at +120%). Source: Eurostat env_air_gge.",
                  fontsize=7, color=GREY)
    # ESR panel (Commission SWD p.115)
    xs = ["2024\nactual", "2030\nexisting\nmeasures", "2030\nwith planned\nmeasures", "2030\ntarget"]
    ys = [41, 42, 30, -19]
    a2.bar(xs, ys, color=[RED, RED, ORANGE, GREEN], width=0.6)
    for i, y in enumerate(ys):
        a2.text(i, y + (2 if y >= 0 else -2), f"{y:+d}%", ha="center", va="bottom" if y >= 0 else "top",
                fontsize=9, fontweight="bold", color=SLATE)
    a2.axhline(0, color=SLATE, lw=0.8)
    a2.plot([2.3, 3.0], [30, 30], color=SLATE, lw=0.8, ls=":")
    a2.annotate("", xy=(2.65, -19), xytext=(2.65, 30), arrowprops=dict(arrowstyle="<->", color=SLATE, lw=1.1))
    a2.text(2.72, 12, "49-point\ngap", fontsize=8.5, color=SLATE, ha="left", fontweight="bold")
    a2.set_ylim(-35, 55)
    a2.set_title("Effort-sharing emissions vs 2005", fontsize=9.5, color=GREEN, loc="left", fontweight="bold")
    a2.tick_params(axis="x", labelsize=7.6)
    a2.set_xlabel("Source: Commission CAPR 2025 staff working document, p. 115.", fontsize=7, color=GREY)
    fig.tight_layout(w_pad=2.5)
    fig.savefig(OUT / "fig2_sectors_esr.png", bbox_inches="tight", facecolor="white")


fig1()
fig2()
print("figures in", OUT)
