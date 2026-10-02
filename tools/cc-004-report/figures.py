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


fig1()
fig2()
print("figures in", OUT)
