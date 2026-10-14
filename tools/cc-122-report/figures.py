"""Figures for Claim Check 122, drawn from data/cc-122/ (run fetch_eurostat.py and calc.py first)."""
import csv, pathlib
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
E = {}
for r in csv.DictReader(open(ROOT / "data" / "cc-122" / "eurostat_tourism.csv")):
    E[(r["dataset"], int(r["year"]))] = float(r["value"])


def fig1():
    fig, ax = plt.subplots(figsize=(9.6, 4.2), dpi=220)
    yrs = range(2015, 2026)
    ax.bar(yrs, [E[("tour_cap_nat", y)] / 1000 for y in yrs], color=SAGE, width=0.7, label="Bed-places in operation (Eurostat)")
    ax.bar([2026.4], [30], bottom=[E[("tour_cap_nat", 2025)] / 1000], color="white", edgecolor=RED, hatch="///", width=0.7,
           label="+30,000 beds in applications (The Shift; figure unverified)")
    ax.text(2026.4, E[("tour_cap_nat", 2025)] / 1000 + 31, "+52%", ha="center", color=RED, fontweight="bold", fontsize=9)
    ax.set_xticks(list(range(2015, 2026, 2)) + [2026.4])
    ax.set_xticklabels([str(y) for y in range(2015, 2026, 2)] + ["if all\nbuilt"])
    ax.set_ylabel("Thousand bed-places")
    ax.set_ylim(0, 105)
    ax.legend(frameon=False, fontsize=8, loc="upper left")
    fig.text(0.01, -0.02, "Eurostat tour_cap_nat, Malta, NACE I551–I553 (all collective accommodation), retrieved 14 Oct 2026. "
             "The 30,000 is The Shift's figure for hotels and extensions; the two measures differ in scope.", fontsize=7, color=GREY)
    fig.savefig(OUT / "fig1_beds.png", bbox_inches="tight", facecolor="white")


def fig2():
    fig, ax = plt.subplots(figsize=(9.6, 3.8), dpi=220)
    full, st = 30000 * 365, E[("tour_occ_ninat", 2025)] / E[("tour_occ_arnat", 2025)]
    cases = [("5 nights", 5), ("6 nights", 6), (f"{st:.1f} nights\n(2025 observed)", st)]
    w = 0.36
    for i, (lab, s) in enumerate(cases):
        a, b = full / s / 1e6, 0.7 * full / s / 1e6
        ax.bar(i - w / 2, a, w, color=GREEN, label="Every bed full all year (100%)" if i == 0 else None)
        ax.bar(i + w / 2, b, w, color=AMBER, label="70% occupancy" if i == 0 else None)
        ax.text(i - w / 2, a + 0.04, f"{a:.2f}", ha="center", fontsize=8.5)
        ax.text(i + w / 2, b + 0.04, f"{b:.2f}", ha="center", fontsize=8.5)
    ref = E[("tour_occ_arnat", 2025)] / 1e6
    ax.axhline(ref, color=RED, ls="--", lw=1.5)
    ax.text(2.55, ref + 0.05, f"2025 non-resident arrivals at establishments: {ref:.2f} million", ha="right", color=RED, fontsize=8.5)
    ax.set_xticks(range(3))
    ax.set_xticklabels([c[0] for c in cases])
    ax.set_ylabel("Additional arrivals a year (million)")
    ax.set_ylim(0, 3.0)
    ax.legend(frameon=False, fontsize=8, loc="upper left", ncol=2)
    fig.text(0.01, -0.03, "Calculated from 30,000 beds x 365 nights (inputs from The Shift, 29 Aug 2026); stay and occupancy "
             "as shown. Eurostat tour_occ_arnat and tour_occ_ninat (FOR), retrieved 14 Oct 2026.", fontsize=7, color=GREY)
    fig.savefig(OUT / "fig2_arrivals.png", bbox_inches="tight", facecolor="white")


fig1()
fig2()
