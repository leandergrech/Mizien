"""Figures for Claim Check 004, drawn from data/cc-004/ (run calc.py first)."""
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
v = defaultdict(dict)
for r in csv.DictReader(open(ROOT / "data" / "cc-004" / "eurostat_municipal_waste.csv")):
    v[(r["dataset"], r["geo"], r["item"])][int(r["year"])] = float(r["value"])


def fig1():
    mt = v[("cei_wm011", "MT", "wst_oper=RCY|unit=PC")]
    eu = v[("cei_wm011", "EU27_2020", "wst_oper=RCY|unit=PC")]
    fig, ax = plt.subplots(figsize=(9.6, 4.3), dpi=220)
    ym = sorted(mt)
    ax.plot(ym, [mt[y] for y in ym], color=RED, lw=2.8, marker="o", ms=3.5, label="Malta")
    ye = sorted(eu)
    ax.plot(ye, [eu[y] for y in ye], color=BLUE, lw=1.8, ls="--", label="EU-27")
    for (y, t, lab) in ((2020, 50, "2020 target 50%"), (2025, 55, "2025 target 55%"), (2030, 60, "2030 target 60%"),
                        (2035, 65, "2035 target 65%")):
        ax.scatter([y], [t], marker="_", s=420, color=GREEN, lw=2.5, zorder=3)
        ax.text(y, t + 2.2, lab, ha="center", fontsize=7.8, color=GREEN, fontweight="bold")
    ax.annotate(f"{mt[2024]:.1f}%", (2024, mt[2024]), xytext=(2024.4, mt[2024] - 1), fontsize=9, color=RED,
                fontweight="bold")
    ax.annotate("", xy=(2025, 55), xytext=(2025, mt[2024]), arrowprops=dict(arrowstyle="<->", color=SLATE, lw=1))
    ax.text(2025.4, 36, f"{55 - mt[2024]:.0f}-point gap\nto the 2025 target", fontsize=8.5, color=SLATE)
    ax.set_xlim(2009.5, 2036.5)
    ax.set_ylim(0, 72)
    ax.set_ylabel("Municipal waste recycled, % of generated")
    ax.legend(frameon=False, fontsize=8.5, loc="upper left")
    ax.set_xlabel("Source: Eurostat cei_wm011 (retrieved 2 Oct 2026); targets from Directive 2008/98/EC as amended "
                  "by Directive (EU) 2018/851.", fontsize=7, color=GREY)
    fig.savefig(OUT / "fig1_recycling_rate.png", bbox_inches="tight", facecolor="white")


def fig2():
    g = lambda op: v[("env_wasmun", "MT", f"wst_oper={op}|unit=THS_T")]
    land, rcy, rcv, trt = g("DSP_L_OTH"), g("RCY"), g("RCV_E"), g("TRT")
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(9.6, 3.9), dpi=220, gridspec_kw={"width_ratios": [1.5, 1]})
    yrs = list(range(2019, 2025))
    b1 = [land[y] for y in yrs]
    b2 = [rcy[y] for y in yrs]
    b3 = [rcv[y] for y in yrs]
    a1.bar(yrs, b1, color=GREY, label="Landfilled")
    a1.bar(yrs, b2, bottom=b1, color=GREEN, label="Recycled")
    a1.bar(yrs, b3, bottom=[x + y for x, y in zip(b1, b2)], color=AMBER, label="Energy recovery")
    for y, l, t in zip(yrs, b1, [trt[y] for y in yrs]):
        a1.text(y, l / 2, f"{100 * l / t:.0f}%", ha="center", color="white", fontsize=8.5, fontweight="bold")
    a1.set_ylabel("Thousand tonnes")
    a1.set_title("Malta: treated municipal waste by route", fontsize=9.5, color=GREEN, loc="left", fontweight="bold")
    a1.legend(frameon=False, fontsize=7.4, loc="upper center", bbox_to_anchor=(0.5, -0.1), ncol=2)
    a1.set_ylim(0, 420)
    r5 = sum(rcy[y] for y in range(2020, 2025))
    e5 = sum(rcv[y] for y in range(2020, 2025))
    a2.bar(["Ministry:\n“diverted from\nlandfill”,\nfive years"], [412], color=ORANGE, width=0.55)
    a2.bar(["Eurostat:\nrecycled + energy-\nrecovered municipal\nwaste, 2020–24"], [r5], color=GREEN, width=0.55)
    a2.bar(["Eurostat:\nrecycled + energy-\nrecovered municipal\nwaste, 2020–24"], [e5], bottom=[r5], color=AMBER,
           width=0.55)
    a2.text(0, 418, "412", ha="center", fontsize=9, fontweight="bold", color=SLATE)
    a2.text(1, r5 + e5 + 6, f"{r5 + e5:.0f}", ha="center", fontsize=9, fontweight="bold", color=SLATE)
    a2.set_ylim(0, 470)
    a2.set_title("Thousand tonnes", fontsize=9.5, color=GREEN, loc="left", fontweight="bold")
    a2.tick_params(axis="x", labelsize=7.4)
    fig.tight_layout(w_pad=3)
    fig.text(0.01, -0.06, "Source: Eurostat env_wasmun (retrieved 2 Oct 2026); Ministry press release PR260072en, "
             "19 Jan 2026. The ministry’s five-year window and scope are not stated.", fontsize=7, color=GREY)
    fig.savefig(OUT / "fig2_routes.png", bbox_inches="tight", facecolor="white")


NAMES = {"AT": "Austria", "BE": "Belgium", "BG": "Bulgaria", "CY": "Cyprus", "CZ": "Czechia", "DE": "Germany",
         "DK": "Denmark", "EE": "Estonia", "EL": "Greece", "ES": "Spain", "FI": "Finland", "FR": "France",
         "HR": "Croatia", "HU": "Hungary", "IE": "Ireland", "IT": "Italy", "LT": "Lithuania", "LU": "Luxembourg",
         "LV": "Latvia", "MT": "Malta", "NL": "Netherlands", "PL": "Poland", "PT": "Portugal", "RO": "Romania",
         "SE": "Sweden", "SI": "Slovenia", "SK": "Slovakia", "EU27_2020": "EU-27"}


def fig3():
    """EU-27: municipal recycling rate (latest year) and change since 2019, Malta highlighted."""
    e = defaultdict(dict)
    for r in csv.DictReader(open(ROOT / "data" / "cc-004" / "eurostat_cei_wm011_eu27.csv")):
        e[r["geo"]][int(r["year"])] = float(r["value"])
    rows = sorted(e, key=lambda g: e[g][max(e[g])])  # lowest at the bottom of the chart
    yy = range(len(rows))
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(8.2, 6.6), dpi=220, sharey=True,
                                 gridspec_kw={"width_ratios": [1.7, 1], "wspace": 0.08})

    def col(g, latest_year):
        if g == "MT":
            return RED
        if g == "EU27_2020":
            return BLUE
        return SAGE if latest_year == 2024 else "#C9D0D4"

    labels = []
    for i, g in enumerate(rows):
        y = max(e[g])
        a1.barh(i, e[g][y], height=0.66, color=col(g, y), zorder=2)
        a1.text(e[g][y] + 0.7, i, f"{e[g][y]:.1f}", va="center", fontsize=7.8, zorder=3,
                color=SLATE, fontweight="bold" if g in ("MT", "EU27_2020") else "normal",
                bbox=dict(boxstyle="square,pad=0.12", fc="white", ec="none"))
        labels.append(NAMES[g] + ("" if y == 2024 else f" ({y})"))
        if 2019 in e[g] and 2024 in e[g]:
            d = e[g][2024] - e[g][2019]
            a2.barh(i, d, height=0.66, color=col(g, 2024))
            a2.text(d + (0.35 if d >= 0 else -0.35), i, f"{d:+.1f}".replace("-", "\u2212"), va="center", ha="left" if d >= 0 else "right",
                    fontsize=7.8, color=SLATE, fontweight="bold" if g in ("MT", "EU27_2020") else "normal")
        else:
            a2.text(0.35, i, "no 2024 data", va="center", fontsize=6.8, color=GREY, style="italic")
    a1.set_yticks(list(yy))
    a1.set_yticklabels(labels, fontsize=8.6)
    for t, g in zip(a1.get_yticklabels(), rows):
        if g in ("MT", "EU27_2020"):
            t.set_fontweight("bold")
            t.set_color(RED if g == "MT" else BLUE)
    a1.axvline(55, color=GREEN, lw=1.6, ls="--", zorder=1)
    a1.text(55, len(rows) - 0.25, "2025 target 55%", fontsize=8, color=GREEN, fontweight="bold", ha="center",
            va="bottom", clip_on=False)
    a1.set_xlim(0, 75)
    a1.set_ylim(-0.7, len(rows) - 0.3)
    a1.set_xlabel("Municipal waste recycled, %, 2024 (or 2023 where 2024 is not yet published)", fontsize=8)
    a1.set_title("Recycling rate", fontsize=9.5, color=GREEN, loc="left", fontweight="bold", pad=14)
    a2.axvline(0, color=GREY, lw=0.8)
    a2.set_xlim(-9, 15)
    a2.set_xlabel("Change 2019–2024, percentage points", fontsize=8)
    a2.set_title("Change since 2019", fontsize=9.5, color=GREEN, loc="left", fontweight="bold", pad=14)
    for a in (a1, a2):
        a.tick_params(axis="x", labelsize=7.6)
        a.tick_params(axis="y", length=0)
        a.grid(axis="x", color="#E3E7E5", lw=0.6)
        a.set_axisbelow(True)
    fig.text(0.01, 0.045, "Source: Eurostat cei_wm011 (dataset updated 30 Mar 2026; retrieved 5 Oct 2026). Grey bars: "
             "latest value is for 2023.\nMalta’s rise is the 4th-largest of the 20 states with both years.",
             fontsize=7.4, color=GREY, va="top")
    fig.savefig(OUT / "fig3_eu27.png", bbox_inches="tight", facecolor="white")


fig1()
fig2()
fig3()
print("figures in", OUT)
