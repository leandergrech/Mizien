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
    # ESR panel (Commission SWD Table 25, printed p. 114)
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
    a2.set_xlabel("Source: Commission CAPR 2025 staff working document, p. 114.", fontsize=7, color=GREY)
    fig.tight_layout(w_pad=2.5)
    fig.savefig(OUT / "fig2_sectors_esr.png", bbox_inches="tight", facecolor="white")


EU = "AT BE BG CY CZ DE DK EE EL ES FI FR HR HU IE IT LT LU LV MT NL PL PT RO SE SI SK".split()
NAMES = {"MT": "Malta", "LU": "Luxembourg", "IE": "Ireland", "CY": "Cyprus", "EE": "Estonia", "LV": "Latvia",
         "EU27_2020": "EU-27"}


def fig_rank():
    """v1.2: the same 27 countries ranked on the per-person cut and on the total cut, 2005-2024."""
    g = defaultdict(dict)
    for r in csv.DictReader(open(ROOT / "data" / "cc-003" / "eurostat_ghg_pop_eu27.csv")):
        g[(r["geo"], r["dataset"])][int(r["year"])] = float(r["value"])
    cut = {}
    for c in EU + ["EU27_2020"]:
        e, p = g[(c, "env_air_gge")], g[(c, "nama_10_pe")]
        cut[c] = (-100 * ((e[2024] / p[2024]) / (e[2005] / p[2005]) - 1), -100 * (e[2024] / e[2005] - 1))
    rk_pc = sorted(EU, key=lambda c: -cut[c][0])
    rk_t = sorted(EU, key=lambda c: -cut[c][1])
    fig, ax = plt.subplots(figsize=(9.6, 4.3), dpi=220)
    for c in EU:
        if c == "MT":
            continue
        lab = c in ("LU", "IE", "CY")
        ax.plot([0, 1], cut[c], color=SLATE if lab else GREY, lw=1.3 if lab else 0.8, alpha=1 if lab else 0.55,
                marker="o", ms=3.5 if lab else 2.5, zorder=2)
    ax.plot([0, 1], cut["EU27_2020"], color=BLUE, lw=1.8, ls="--", marker="o", ms=4, zorder=3)
    ax.plot([0, 1], cut["MT"], color=RED, lw=3, marker="o", ms=7, zorder=4)
    # direct labels: Malta both ends, a few notable countries on the right
    pc, t = cut["MT"]
    ax.text(-0.04, pc, f"Malta  −{pc:.1f}%\n{rk_pc.index('MT') + 1}rd of 27", ha="right", va="center", fontsize=10,
            color=RED, fontweight="bold")
    ax.text(1.04, t, f"Malta  −{t:.1f}%  ·  {rk_t.index('MT') + 1}th of 27", ha="left", va="center", fontsize=10,
            color=RED, fontweight="bold")
    for c, dy in (("LU", 0), ("IE", 0), ("CY", 0), ("EU27_2020", 0.6), ("EE", 1.2), ("LV", 0)):
        col = BLUE if c == "EU27_2020" else SLATE
        ax.text(1.04, cut[c][1] + dy, f"{NAMES[c]}  −{cut[c][1]:.1f}%", ha="left", va="center", fontsize=8.3, color=col)
    ax.text(-0.04, cut["LU"][0], f"Luxembourg  −{cut['LU'][0]:.1f}%", ha="right", va="center", fontsize=8.3,
            color=SLATE)
    ax.text(-0.04, cut["EU27_2020"][0], f"EU-27  −{cut['EU27_2020'][0]:.1f}%", ha="right", va="center", fontsize=8.3,
            color=BLUE)
    ax.set_xlim(-0.62, 1.62)
    ax.set_ylim(-7, 64)
    ax.set_xticks([0, 1])
    ax.set_xticklabels(["Cut in emissions\nper person", "Cut in total\nemissions"], fontsize=10, fontweight="bold")
    ax.xaxis.tick_top()
    ax.tick_params(axis="x", length=0, pad=6)
    ax.spines["bottom"].set_visible(False)
    ax.set_ylabel("Cut since 2005, % (higher = bigger cut)")
    ax.set_yticks(range(0, 61, 10))
    ax.set_yticklabels([f"{y}%" for y in range(0, 61, 10)])
    ax.axhline(0, color=GREY, lw=0.6)
    ax.set_title("EU-27, 2005–2024: Malta’s cut ranks 3rd per person but 20th in total", fontsize=11,
                 color=GREEN, loc="left", fontweight="bold", pad=34)
    ax.text(-0.62, -10, "Each line is one Member State (27). Emissions exclude LULUCF and international aviation and "
            "shipping. Source: Eurostat env_air_gge (TOTX4_MEMO) and nama_10_pe\n(population, national concept; 2024 "
            "provisional for BE, CY, DE, EL, ES, FR, HR, NL), retrieved 5 Oct 2026. Latvia’s emissions per person "
            "rose (+5.1%).", fontsize=7, color=GREY, va="top")
    fig.savefig(OUT / "fig_rank.png", bbox_inches="tight", facecolor="white")
    plt.close(fig)


def fig_path():
    """v1.2: Malta's effort-sharing allocations against emissions, 2021-2030 (Commission SWD Table 26, p. 125)."""
    s = defaultdict(dict)
    for r in csv.DictReader(open(ROOT / "data" / "cc-003" / "capr2025_esr_malta.csv")):
        if r["table"] == "Table 26" and r["year"].isdigit() and int(r["year"]) >= 2021:
            s[r["series"]][int(r["year"])] = float(r["value"])
    yrs = list(range(2021, 2031))
    aea, em, cb = s["Malta estimated AEAs"], s["Malta emissions"], s["Malta cumulative balance of AEAs"]
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(9.6, 3.8), dpi=220, gridspec_kw={"width_ratios": [1.45, 1]})
    for y in yrs:
        a1.bar(y, aea[y], width=0.68, color=SAGE if y <= 2025 else "#C9DACE", edgecolor="white", lw=0.8)
    a1.plot([y for y in yrs if y <= 2024], [em[y] for y in yrs if y <= 2024], color=RED, lw=2.6, marker="o", ms=6,
            zorder=3)
    a1.plot([y for y in yrs if y >= 2024], [em[y] for y in yrs if y >= 2024], color=RED, lw=2, ls="--", marker="o",
            ms=5, mfc="white", zorder=3)
    for y in yrs:
        a1.text(y, aea[y] / 2, f"{aea[y]:.1f}", ha="center", va="center", fontsize=7.5, color=SLATE)
    a1.text(2021.4, 2.02, "2021 limit: about twice\n2005 emissions (+102%)", fontsize=7.8, color=SLATE, va="top")
    a1.annotate("2022–24: emissions +43%, +42%, +41% above\n2005, against limits of +21%, +16%, +11%",
                xy=(2023.1, 1.43), xytext=(2024.9, 1.9), fontsize=7.8, color=RED, va="center", ha="left",
                arrowprops=dict(arrowstyle="-", color=RED, lw=0.8))
    a1.set_xticks(yrs)
    a1.set_xticklabels([str(y) if y in (2021, 2024, 2027, 2030) else f"’{str(y)[2:]}" for y in yrs], fontsize=8)
    a1.set_ylim(0, 2.3)
    a1.set_ylabel("Mt CO₂-eq")
    a1.set_title("Yearly limit (bars) and emissions (line)", fontsize=9.5, color=GREEN, loc="left", fontweight="bold")
    from matplotlib.patches import Patch
    from matplotlib.lines import Line2D
    a1.legend(handles=[Patch(color=SAGE, label="Annual allocation, set"),
                       Patch(color="#C9DACE", label="Annual allocation, Commission estimate"),
                       Line2D([], [], color=RED, lw=2.6, marker="o", label="Emissions"),
                       Line2D([], [], color=RED, lw=2, ls="--", marker="o", mfc="white",
                              label="Projected, with planned measures")],
              frameon=False, fontsize=7.6, loc="upper left", bbox_to_anchor=(-0.02, -0.08), ncol=2)
    cols = [GREEN if cb[y] > 0 else (GREY if cb[y] == 0 else RED) for y in yrs]
    bars = a2.bar(yrs, [cb[y] for y in yrs], width=0.68, color=cols, edgecolor="white", lw=0.8)
    for b, y in zip(bars, yrs):
        if y >= 2025:
            b.set_alpha(0.55)
        v = cb[y]
        a2.text(y, v + (0.06 if v >= 0 else -0.06), f"{v:+.1f}".replace("-", "−") if v else "0.0", ha="center",
                va="bottom" if v >= 0 else "top", fontsize=7.5, color=SLATE, fontweight="bold")
    a2.axhline(0, color=SLATE, lw=0.8)
    a2.axvline(2024.5, color=GREY, lw=0.6, ls=":")
    a2.text(2024.6, 0.62, "projected →", fontsize=7.5, color=GREY)
    a2.text(2020.45, -1.35, "The 2021 surplus covered\nthe overshoot until 2024.\nFirst compliance check:\n"
            "2027 (for 2021–25).", fontsize=7.3, color=SLATE, va="top")
    a2.set_xticks(yrs)
    a2.set_xticklabels([str(y) if y in (2021, 2024, 2027, 2030) else f"’{str(y)[2:]}" for y in yrs], fontsize=8)
    a2.set_ylim(-2.6, 1.0)
    a2.set_ylabel("Mt CO₂-eq")
    a2.set_title("Cumulative balance, before flexibilities", fontsize=9.5, color=GREEN, loc="left", fontweight="bold")
    fig.text(0.01, -0.035, "Source: European Commission, Climate Action Progress Report 2025 staff working document, "
             "Table 26 (p. 125; values rounded to 0.1 Mt; later years are projections\nwith planned measures; transfers "
             "and cancellations not counted) and Table 25 (p. 114, percentages). Malta also has 0.5 Mt of ETS "
             "flexibility for 2021–2030.", fontsize=7, color=GREY, va="top")
    fig.tight_layout(w_pad=2.5)
    fig.savefig(OUT / "fig_path.png", bbox_inches="tight", facecolor="white")
    plt.close(fig)


fig1()
fig2()
fig_rank()
fig_path()
print("figures in", OUT)
