"""Figures for Claim Check 162, from data/cc-162/ and data/cc-094/ (run fetch.py and calc.py first)."""
import csv, pathlib
from collections import defaultdict
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from matplotlib.lines import Line2D
from matplotlib.patches import Patch

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[1]
D, D4 = ROOT / "data" / "cc-162", ROOT / "data" / "cc-094"
OUT = HERE / "out"
OUT.mkdir(exist_ok=True)
for f in ["LiberationSans-Regular", "LiberationSans-Bold", "LiberationSans-Italic"]:
    fm.fontManager.addfont(f"/usr/share/fonts/truetype/liberation/{f}.ttf")
plt.rcParams.update({"font.family": "Liberation Sans", "axes.spines.top": False, "axes.spines.right": False,
                     "axes.edgecolor": "#8A9399", "axes.labelcolor": "#2B3A42", "xtick.color": "#2B3A42",
                     "ytick.color": "#2B3A42"})
GREEN, SAGE, AMBER, RED, SLATE, GREY, ORANGE, BLUE = ("#14452F", "#7FA88B", "#E3A72F", "#B5483A", "#2B3A42",
                                                      "#8A9399", "#D9772B", "#3C6E8F")


def rows_of(p):
    return [r for r in csv.DictReader(open(p)) if not r[next(iter(r))].startswith("#")]


esr = {int(r["year"]): float(r["value"]) for r in rows_of(D / "eea_esr_malta_2026.csv")}
proj = defaultdict(dict)
for r in rows_of(D4 / "eea_ghg_projections_esr.csv"):
    if r["submission"].startswith("2025") and r["country"] == "MT" and r["category"] == "Total excluding LULUCF":
        proj[r["scenario"]][int(r["year"])] = float(r["value_gapfilled"])
base, target, aea, law = None, None, {}, {}
for r in rows_of(D4 / "esr_legal_inputs.csv"):
    if r["item"] == "2005 ESR base" and r["country"] == "MT":
        base = float(r["value"]) / 1000
    elif r["item"] == "2030 target vs 2005" and r["country"] == "MT":
        target = float(r["value"])
    elif r["item"] == "Annual emission allocation":
        aea[int(r["year"])] = float(r["value"]) / 1000
    else:
        law[(r["item"], r["country"])] = float(r["value"])
B, LIMIT = base, base * (1 + target / 100)
wem, wam = proj["WEM"], proj["WAM"]
SRC = "Sources: EEA effort-sharing emissions 2005–2025 (2026 edition, 2025 approximated) and GHG projections (Malta: March 2025 submission), "


def fig1():
    fig, ax = plt.subplots(figsize=(9.6, 4.3), dpi=220)
    yrs = list(range(2021, 2031))
    ax.bar(yrs, [aea[y] for y in yrs], width=0.62, color="#E6EFE8", edgecolor=SAGE, lw=0.8, zorder=1)
    ys = list(range(2021, 2026))
    ax.plot(ys, [esr[y] for y in ys], color=GREEN, lw=2.6, marker="o", ms=4.2, zorder=4)
    ax.plot([2025], [esr[2025]], marker="o", ms=6, mfc="white", mec=GREEN, mew=1.6, zorder=5)
    for s, col in ((wem, RED), (wam, ORANGE)):
        ax.plot([2025] + list(range(2026, 2031)), [esr[2025]] + [s[y] for y in range(2026, 2031)], color=col, lw=2.2, ls="--", zorder=4)
    ax.axhline(B, color=BLUE, lw=1.1, ls=":", zorder=2)
    ax.text(2020.6, B - 55, f"2005 level used for the target: {B:,.0f} kt", color=BLUE, fontsize=8, va="top")
    ax.plot([2030], [LIMIT], marker="_", ms=18, mew=2.6, color=GREEN, zorder=6)
    ax.text(2030.75, LIMIT, f"2030 limit\n{LIMIT:,.0f} kt (−19%)", color=GREEN, fontsize=8, va="center", fontweight="bold")
    ax.text(2030.75, wem[2030] + 18, f"{wem[2030]:,.0f} kt\n+{100 * (wem[2030] / B - 1):.0f}% (existing)", color=RED, fontsize=8, va="center", fontweight="bold")
    ax.text(2030.75, wam[2030] - 40, f"{wam[2030]:,.0f} kt\n+{100 * (wam[2030] / B - 1):.0f}% (with planned)", color=ORANGE, fontsize=8, va="center", fontweight="bold")
    ax.text(2025, esr[2025] + 60, f"2025: {esr[2025]:,.0f} kt\n(+{100 * (esr[2025] / B - 1):.0f}%)", color=GREEN, fontsize=7.6, ha="center")
    ax.set_xlim(2020.4, 2034.0)
    ax.set_ylim(0, 2400)
    ax.set_xticks(range(2021, 2031))
    ax.set_ylabel("kt CO$_2$e")
    ax.legend(handles=[Line2D([], [], color=GREEN, lw=2.6, marker="o", ms=4, label="2021–2025 emissions (2025 approximated)"),
                       Line2D([], [], color=RED, lw=2.2, ls="--", label="Projection, existing measures (WEM)"),
                       Line2D([], [], color=ORANGE, lw=2.2, ls="--", label="Projection, with planned measures (WAM)"),
                       Patch(facecolor="#E6EFE8", edgecolor=SAGE, label="Yearly limit (annual emission allocation)")],
              frameon=False, fontsize=7.6, loc="upper left", ncol=2)
    ax.text(2020.5, -430, SRC + "retrieved 16 Nov / 6 Oct 2026; allocations: Implementing Decision (EU) 2026/895;\n"
            "2005 level: Decision (EU) 2020/2126. The 2021 limit includes a one-off 774 kt adjustment (Regulation (EU) 2018/842, Annex IV).",
            fontsize=6.9, color=GREY)
    fig.savefig(OUT / "fig1_path.png", bbox_inches="tight", facecolor="white")


def fig2():
    ets = law[("ETS flexibility total 2021-2030", "MT")] / 1e6
    lul = law[("LULUCF flexibility maximum 2021-2030", "MT")]
    fig, ax = plt.subplots(figsize=(9.6, 3.0), dpi=220)
    for i, (lab, s) in enumerate((("WAM", wam), ("WEM", wem))):
        e = {y: esr[y] for y in range(2021, 2026)}
        e.update({y: s[y] for y in range(2026, 2031)})
        bal = sum(aea[y] - e[y] for y in range(2021, 2031)) / 1000
        ax.barh(i, bal, color=RED, height=0.5)
        ax.barh(i, ets, left=bal, color=SAGE, height=0.5)
        ax.barh(i, lul, left=bal + ets, color=BLUE, height=0.5)
        ax.text(bal - 0.05, i, f"net excess\n{-bal:.2f} Mt", ha="right", va="center", fontsize=8.2, fontweight="bold", color=RED)
        ax.text(bal + ets / 2, i, f"ETS +{ets:.2f}", ha="center", va="center", fontsize=7.4, color="white")
        ax.text(0.06, i, f"still to cover: {-(bal + ets + lul):.2f} Mt", va="center", fontsize=8.2, color=SLATE)
    ax.axvline(0, color=SLATE, lw=0.8)
    ax.set_yticks([0, 1])
    ax.set_yticklabels(["With planned\nmeasures (WAM)", "Existing\nmeasures (WEM)"], fontsize=8.4)
    ax.set_xlim(-3.4, 1.4)
    ax.set_xlabel("Mt CO$_2$e, 2021–2030 total (negative = emissions above the yearly limits)")
    ax.legend(handles=[Patch(color=SAGE, label="Covered by the ETS flexibility (0.51 Mt)"),
                       Patch(color=BLUE, label="LULUCF flexibility, maximum (0.03 Mt)"),
                       Patch(color=RED, label="Not covered: to buy from other Member States or cut")],
              frameon=False, fontsize=7.4, ncol=3, loc="upper center", bbox_to_anchor=(0.45, -0.27))
    ax.text(-3.4, 2.85, "Emissions: 2021–2024 reviewed, 2025 approximated (EEA 2026 edition), 2026–2030 projected (March 2025 submission). "
            "Allocations: Decision (EU) 2026/895.\nETS flexibility: Decision (EU) 2024/1884; LULUCF: Regulation (EU) 2018/842, Annex III.",
            fontsize=6.9, color=GREY)
    ax.set_ylim(1.6, -0.6)
    fig.savefig(OUT / "fig2_ledger.png", bbox_inches="tight", facecolor="white")


fig1(); fig2()
print("figures in", OUT)
