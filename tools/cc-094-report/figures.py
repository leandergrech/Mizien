"""Figures for Claim Check 094, drawn from data/cc-094/ (run fetch.py and calc.py first)."""
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
D = ROOT / "data" / "cc-094"
OUT = HERE / "out"
OUT.mkdir(exist_ok=True)
for f in ["LiberationSans-Regular", "LiberationSans-Bold", "LiberationSans-Italic"]:
    fm.fontManager.addfont(f"/usr/share/fonts/truetype/liberation/{f}.ttf")
plt.rcParams.update({"font.family": "Liberation Sans", "axes.spines.top": False, "axes.spines.right": False,
                     "axes.edgecolor": "#8A9399", "axes.labelcolor": "#2B3A42", "xtick.color": "#2B3A42",
                     "ytick.color": "#2B3A42"})
GREEN, SAGE, AMBER, RED, SLATE, GREY, ORANGE, BLUE = ("#14452F", "#7FA88B", "#E3A72F", "#B5483A", "#2B3A42",
                                                      "#8A9399", "#D9772B", "#3C6E8F")
EU27 = "BE BG CZ DK DE EE IE EL ES FR HR IT CY LV LT LU HU MT NL AT PL PT RO SI SK FI SE".split()


def rows_of(path):
    return [r for r in csv.DictReader(open(path)) if not r[next(iter(r))].startswith("#")]


esr, status = {}, {}
for r in rows_of(D / "eea_esr_emissions.csv"):
    if r["country"] == "Malta" and r["series"] in ("ESD", "ESR") and r["value"]:
        esr[int(r["year"])] = float(r["value"]) * 1000
        status[int(r["year"])] = r["series"]
proj = defaultdict(dict)
for r in rows_of(D / "eea_ghg_projections_esr.csv"):
    if r["submission"].startswith("2025"):
        proj[(r["country"], r["category"], r["scenario"])][int(r["year"])] = float(r["value_gapfilled"])
base, target, aea, law = {}, {}, {}, {}
for r in rows_of(D / "esr_legal_inputs.csv"):
    if r["item"] == "2005 ESR base":
        base[r["country"]] = float(r["value"]) / 1000
    elif r["item"] == "2030 target vs 2005":
        target[r["country"]] = float(r["value"])
    elif r["item"] == "Annual emission allocation":
        aea[int(r["year"])] = float(r["value"]) / 1000
    else:
        law[(r["item"], r["country"])] = float(r["value"])
B = base["MT"]
LIMIT = B * (1 + target["MT"] / 100)
wem = proj[("MT", "Total excluding LULUCF", "WEM")]
wam = proj[("MT", "Total excluding LULUCF", "WAM")]
SRC = "Sources: EEA effort-sharing emissions (2005–2024) and GHG projections (2025 submission), retrieved 6 Oct 2026; "


def fig1():
    fig, ax = plt.subplots(figsize=(9.6, 4.3), dpi=220)
    yrs = list(range(2021, 2031))
    ax.bar(yrs, [aea[y] for y in yrs], width=0.62, color="#E6EFE8", edgecolor=SAGE, lw=0.8, zorder=1)
    esd = [y for y in sorted(esr) if status[y] == "ESD"]
    ax.plot(esd, [esr[y] for y in esd], color=GREY, lw=1.6, marker="o", ms=3, zorder=3)
    esrr = [y for y in sorted(esr) if status[y] == "ESR"]
    ax.plot(esrr, [esr[y] for y in esrr], color=GREEN, lw=2.6, marker="o", ms=4.2, zorder=4)
    ax.plot([2024], [esr[2024]], marker="o", ms=6, mfc="white", mec=GREEN, mew=1.6, zorder=5)
    for sc, s, col in (("WEM", wem, RED), ("WAM", wam, ORANGE)):
        xs = [2024] + list(range(2025, 2031))
        ys = [esr[2024]] + [s[y] for y in range(2025, 2031)]
        ax.plot(xs, ys, color=col, lw=2.2, ls="--", zorder=4)
    ax.axhline(B, color=BLUE, lw=1.1, ls=":", zorder=2)
    ax.plot([2005], [B], marker="D", ms=6, color=BLUE, zorder=6)
    ax.text(2005.3, B - 60, f"2005 level used for the target: {B:,.0f} kt", color=BLUE, fontsize=8, va="top")
    ax.plot([2030], [LIMIT], marker="_", ms=18, mew=2.6, color=GREEN, zorder=6)
    ax.text(2030.75, LIMIT, f"2030 limit\n{LIMIT:,.0f} kt (−19%)", color=GREEN, fontsize=8, va="center", fontweight="bold")
    ax.text(2030.75, wem[2030] + 18, f"{wem[2030]:,.0f} kt\n+{100 * (wem[2030] / B - 1):.0f}% (existing)", color=RED,
            fontsize=8, va="center", fontweight="bold")
    ax.text(2030.75, wam[2030] - 40, f"{wam[2030]:,.0f} kt\n+{100 * (wam[2030] / B - 1):.0f}% (with planned)",
            color=ORANGE, fontsize=8, va="center", fontweight="bold")
    ax.text(2024, esr[2024] + 55, f"2024: {esr[2024]:,.0f} kt\n(+{100 * (esr[2024] / B - 1):.0f}%)", color=GREEN,
            fontsize=7.6, ha="center")
    ax.set_xlim(2004.3, 2034.0)
    ax.set_ylim(0, 2650)
    ax.set_xticks(range(2005, 2031, 5))
    ax.set_ylabel("kt CO$_2$e")
    ax.legend(handles=[Line2D([], [], color=GREY, lw=1.6, marker="o", ms=3, label="2005–2020, Effort Sharing Decision basis"),
                       Line2D([], [], color=GREEN, lw=2.6, marker="o", ms=4, label="2021–2024, Effort Sharing Regulation"),
                       Line2D([], [], color=RED, lw=2.2, ls="--", label="Projection, existing measures (WEM)"),
                       Line2D([], [], color=ORANGE, lw=2.2, ls="--", label="Projection, with planned measures (WAM)"),
                       Patch(facecolor="#E6EFE8", edgecolor=SAGE, label="Yearly limit (annual emission allocation)")],
              frameon=False, fontsize=7.6, loc="upper left", ncol=2)
    ax.text(2004.4, -500, SRC + "allocations: Implementing Decision (EU) 2026/895; 2005 level: Decision (EU) 2020/2126.\n"
            "2021–2023 reviewed in 2025; 2024 approximated (hollow marker). 2005–2020 use older rules and warming factors "
            "(AR4), so they are not directly comparable with 2021 on.\nThe 2021 limit includes a one-off 774 kt adjustment "
            "(Regulation (EU) 2018/842, Annex IV).", fontsize=6.9, color=GREY)
    fig.savefig(OUT / "fig1_path.png", bbox_inches="tight", facecolor="white")


def fig2():
    gap = {}
    for cc in EU27:
        for sc in ("WAM", "WEM"):
            v = proj[(cc, "Total excluding LULUCF", sc)][2030]
            gap[(cc, sc)] = 100 * (v / base[cc] - 1) - target[cc]
    order = sorted(EU27, key=lambda c: -gap[(c, "WAM")])
    fig, ax = plt.subplots(figsize=(9.6, 4.0), dpi=220)
    xs = range(len(order))
    ax.bar(xs, [gap[(c, "WAM")] for c in order], width=0.7,
           color=[RED if c == "MT" else (ORANGE if gap[(c, "WAM")] > 0 else SAGE) for c in order], zorder=2)
    ax.scatter(xs, [gap[(c, "WEM")] for c in order], marker="_", s=90, lw=2, color=SLATE, zorder=3)
    ax.axhline(0, color=SLATE, lw=0.8)
    for i, c in enumerate(order):
        if c in ("MT", "IE", "DE"):
            ax.text(i, gap[(c, "WAM")] + 2, f"{gap[(c, 'WAM')]:.0f}", ha="center", fontsize=8, fontweight="bold",
                    color=RED if c == "MT" else SLATE)
    ax.text(0.35, gap[("MT", "WEM")] + 1.5, f"{gap[('MT', 'WEM')]:.0f} (existing measures)", fontsize=7.6, color=SLATE)
    ax.set_xticks(list(xs))
    ax.set_xticklabels(order, fontsize=8)
    ax.set_ylabel("Projected 2030 emissions minus target\n(percentage points of 2005)")
    ax.set_ylim(-30, 70)
    ax.text(13, 30, "Above 0: projected to miss the 2030 target\nbefore any flexibility", ha="center", fontsize=8, color=SLATE)
    ax.legend(handles=[Patch(color=ORANGE, label="Gap, with planned measures (WAM)"),
                       Patch(color=SAGE, label="Overachievement, WAM"),
                       Line2D([], [], color=SLATE, marker="_", ms=10, mew=2, lw=0, label="Same, existing measures (WEM)")],
              frameon=False, fontsize=7.6, loc="upper right", ncol=1)
    ax.text(-0.6, -48, SRC + "\n2005 levels: Decision (EU) 2020/2126; targets: Regulation (EU) 2023/857. Country codes are "
            "Eurostat's (EL = Greece). Belgium did not report in 2025;\nthe EEA uses its 2024 submission.", fontsize=6.9,
            color=GREY)
    fig.savefig(OUT / "fig2_gaps.png", bbox_inches="tight", facecolor="white")


def fig3():
    cats = [("Transport", ["1.A.3. Transport"], "#B5483A"),
            ("Buildings and other fuel use", None, "#D9772B"),
            ("Manufacturing (fuel)", ["1.A.2. Manufacturing industries and construction"], "#E3A72F"),
            ("Industrial processes (mainly F-gases)", ["2. Industrial processes"], "#3C6E8F"),
            ("Agriculture", ["3. Agriculture"], "#7FA88B"),
            ("Waste", ["5. Waste"], "#2B3A42")]
    bars = [("2023\n(projection base)", "WEM", 2023), ("2030\nexisting measures", "WEM", 2030),
            ("2030\nwith planned measures", "WAM", 2030)]
    fig, ax = plt.subplots(figsize=(9.6, 3.9), dpi=220)
    for i, (lab, sc, y) in enumerate(bars):
        bottom = 0
        for name, keys, col in cats:
            if keys:
                v = sum(proj[("MT", k, sc)][y] for k in keys)
            else:
                v = (proj[("MT", "1. Energy", sc)][y] - proj[("MT", "1.A.3. Transport", sc)][y]
                     - proj[("MT", "1.A.2. Manufacturing industries and construction", sc)][y])
            ax.barh(i, v, left=bottom, color=col, height=0.6, edgecolor="white", lw=0.6)
            if v > 60:
                x = bottom + v / 2
                if bottom < LIMIT < bottom + v:   # keep the label clear of the dashed 2030-limit line
                    x = (bottom + LIMIT) / 2 if LIMIT - bottom >= bottom + v - LIMIT else (LIMIT + bottom + v) / 2
                ax.text(x, i, f"{v:.0f}", ha="center", va="center", fontsize=7.6, color="white", zorder=6)
            bottom += v
        ax.text(bottom + 12, i, f"{bottom:,.0f} kt", va="center", fontsize=8.4, fontweight="bold", color=SLATE)
    ax.axvline(LIMIT, color=GREEN, lw=2, ls="--", zorder=4)
    ax.text(LIMIT - 8, -0.5, f"2030 limit {LIMIT:,.0f} kt", color=GREEN, fontsize=8, ha="right", fontweight="bold")
    ax.axvline(B, color=BLUE, lw=1.1, ls=":")
    ax.text(B + 8, -0.5, f"2005 level {B:,.0f} kt", color=BLUE, fontsize=8)
    ax.set_yticks(range(3))
    ax.set_yticklabels([b[0] for b in bars], fontsize=8.4)
    ax.set_ylim(2.5, -0.68)
    ax.set_xlim(0, 1700)
    ax.set_xlabel("kt CO$_2$e")
    ax.legend(handles=[Patch(color=c, label=n) for n, _, c in cats], frameon=False, fontsize=7.4, ncol=3,
              loc="upper center", bbox_to_anchor=(0.5, -0.17))
    ax.text(0, 3.62, "Source: EEA GHG projections, 2025 submission (Malta), retrieved 6 Oct 2026. 'Buildings and other fuel "
            "use' = energy (1) minus transport (1.A.3) and manufacturing (1.A.2).", fontsize=6.9, color=GREY)
    fig.savefig(OUT / "fig3_sectors.png", bbox_inches="tight", facecolor="white")


def fig4():
    ets = law[("ETS flexibility total 2021-2030", "MT")] / 1e6
    lul = law[("LULUCF flexibility maximum 2021-2030", "MT")]
    fig, ax = plt.subplots(figsize=(9.6, 3.0), dpi=220)
    for i, (sc, s) in enumerate((("With planned measures (WAM)", wam), ("Existing measures (WEM)", wem))):
        e = {y: esr[y] for y in (2021, 2022, 2023, 2024)}
        e.update({y: s[y] for y in range(2025, 2031)})
        bal = sum(aea[y] - e[y] for y in range(2021, 2031)) / 1000
        ax.barh(i, bal, color=RED, height=0.5)
        ax.barh(i, ets, left=bal, color=SAGE, height=0.5)
        ax.barh(i, lul, left=bal + ets, color=BLUE, height=0.5)
        rest = bal + ets + lul
        ax.text(bal - 0.05, i, f"net excess\n{-bal:.2f} Mt", ha="right", va="center", fontsize=8.2, fontweight="bold",
                color=RED)
        ax.text(bal + ets / 2, i, f"ETS +{ets:.2f}", ha="center", va="center", fontsize=7.4, color="white")
        ax.text(0.06, i, f"still to cover: {-rest:.2f} Mt", va="center", fontsize=8.2, color=SLATE)
    ax.axvline(0, color=SLATE, lw=0.8)
    ax.set_yticks([0, 1])
    ax.set_yticklabels(["With planned\nmeasures (WAM)", "Existing\nmeasures (WEM)"], fontsize=8.4)
    ax.set_xlim(-3.4, 1.4)
    ax.set_xlabel("Mt CO$_2$e, 2021–2030 total (negative = emissions above the yearly limits)")
    ax.legend(handles=[Patch(color=SAGE, label="Covered by the ETS flexibility (0.51 Mt)"),
                       Patch(color=BLUE, label="LULUCF flexibility, maximum (0.03 Mt)"),
                       Patch(color=RED, label="Not covered: to buy from other Member States or cut")],
              frameon=False, fontsize=7.4, ncol=3, loc="upper center", bbox_to_anchor=(0.45, -0.27))
    ax.text(-3.4, 2.85, "Emissions: 2021–2023 reviewed, 2024 approximated (EEA), 2025–2030 projected (2025 submission). "
            "Allocations: Decision (EU) 2026/895. ETS flexibility: Decision (EU) 2024/1884;\nLULUCF: Regulation (EU) "
            "2018/842, Annex III. The remainder would have to be bought from other Member States or cut further.",
            fontsize=6.9, color=GREY)
    ax.set_ylim(1.6, -0.6)
    fig.savefig(OUT / "fig4_ledger.png", bbox_inches="tight", facecolor="white")


fig1(); fig2(); fig3(); fig4()
print("figures in", OUT)
