"""Figures for Claim Check 032, drawn from data/cc-032/ (run fetch.py and calc.py first)."""
import csv
import pathlib

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib import font_manager as fm  # noqa: E402

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[1]
OUT = HERE / "out"
OUT.mkdir(exist_ok=True)
for f in ["LiberationSans-Regular", "LiberationSans-Bold", "LiberationSans-Italic"]:
    fm.fontManager.addfont(f"/usr/share/fonts/truetype/liberation/{f}.ttf")
plt.rcParams.update({"font.family": "Liberation Sans", "axes.spines.top": False, "axes.spines.right": False,
                     "axes.edgecolor": "#8A9399", "axes.labelcolor": "#2B3A42", "xtick.color": "#2B3A42",
                     "ytick.color": "#2B3A42"})
GREEN, SAGE, AMBER, RED, SLATE, GREY, ORANGE, BLUE, MAROON = ("#14452F", "#7FA88B", "#E3A72F", "#B5483A", "#2B3A42",
                                                              "#8A9399", "#D9772B", "#3C6E8F", "#8E2F25")
D = ROOT / "data" / "cc-032"


def fig1():
    """Dated records of SmartFlowers in Europe before the Gozo statement (data/cc-032/european_records.csv)."""
    # (date, label, place, text, colour, side, label x, alignment)
    ev = [(2015.38, "May 2015", "Switzerland", "Two SmartFlowers, an\nAustrian product, installed\nat the Umwelt Arena", BLUE, 1,
           2014.75, "left"),
          (2016.08, "Jan 2016", "Spain", "Maker presents an electric-\nvehicle charging version,\npitched at public bodies",
           GREY, -1, 2017.0, "center"),
          (2016.93, "Dec 2016", "Austria", "Motorway operator ASFINAG:\nSmartFlower in service at\nHinterbrühl rest area (A21)",
           BLUE, 1, 2017.8, "left"),
          (2021.61, "Aug 2021", "UK", "Vodafone erects a\nSmartFlower at its Newbury\nheadquarters", BLUE, -1, 2021.61,
           "center"),
          (2025.80, "21 Oct 2025", "Malta", "Minister: “these first\nsolar flowers in Europe”", MAROON, 1,
           2025.55, "right"),
          (2025.87, "14 Nov 2025", "maker", "Maker: Gozo is “one of\nthe largest installations\nin Europe”", GREY, -1,
           2026.45, "right")]
    fig, ax = plt.subplots(figsize=(8.6, 3.4), dpi=220)
    ax.axhline(0, color=SLATE, lw=1.4, zorder=1)
    for yr in range(2015, 2027):
        ax.plot([yr, yr], [-0.06, 0.06], color=SLATE, lw=0.8)
        if yr < 2026:   # the 2026 label would sit under the last leader line
            ax.text(yr, -0.12, str(yr), ha="center", va="top", fontsize=9, color=SLATE)
    for x, d, c, t, col, side, lx, ha in ev:
        y = 0.62 * side
        ax.plot([x, lx], [0, y * 0.95], color=col, lw=1, zorder=1)
        ax.scatter([x], [0], s=46, color=col, zorder=4 if col == MAROON else 3, edgecolor="white", linewidth=0.8)
        va = "bottom" if side == 1 else "top"
        ax.text(lx, y, f"{d} · {c}", ha=ha, va=va, fontsize=9.4, fontweight="bold", color=col)
        ax.text(lx, y + 0.19 * side, t, ha=ha, va=va, fontsize=8.6, color=SLATE, linespacing=1.15)
    ax.set_xlim(2014.6, 2026.6)
    ax.set_ylim(-1.7, 1.7)
    ax.axis("off")
    fig.savefig(OUT / "fig1_timeline.png", bbox_inches="tight", facecolor="white")
    plt.close(fig)


def fig2():
    """A: modelled output a day by month, two-axis vs optimal fixed (PVGIS). B: hours of 10-minute shuttle service
    that each month's average day equals, at the sourced consumption range (indicative)."""
    pv = {}
    for r in csv.DictReader(open(D / "pvgis_monthly.csv", encoding="utf-8")):
        if r["month"] != "year":
            pv.setdefault(r["system"], {})[int(r["month"])] = float(r["E_d_kWh"])
    route = sum(float(r["distance_m"]) for r in csv.DictReader(open(D / "route_osrm.csv", encoding="utf-8"))) / 1000
    km_h = 6 * route
    m = list(range(1, 13))
    lab = ["J", "F", "M", "A", "M", "J", "J", "A", "S", "O", "N", "D"]
    fig, (a, b) = plt.subplots(1, 2, figsize=(8.6, 3.3), dpi=220, gridspec_kw={"wspace": 0.34})
    w = 0.38
    a.bar([x - w / 2 for x in m], [pv["two_axis"][x] for x in m], width=w, color=GREEN, label="Two-axis tracking (as the flowers)")
    a.bar([x + w / 2 for x in m], [pv["fixed_optimal"][x] for x in m], width=w, color=SAGE,
          label="Same capacity, fixed at the best angle")
    a.set_xticks(m, lab)
    a.set_ylabel("kWh a day (37.5 kWp)")
    a.set_ylim(0, 400)
    a.legend(frameon=False, fontsize=8.4, loc="upper left")
    a.set_title("A  Modelled output, Ta’ Xħajma (PVGIS)", fontsize=10, loc="left", color=SLATE, fontweight="bold")
    a.grid(axis="y", color="#E3E6E8", lw=0.6)
    a.set_axisbelow(True)
    hi = [pv["two_axis"][x] / (km_h * 1.451) for x in m]
    lo = [pv["two_axis"][x] / (km_h * 2.1) for x in m]
    b.fill_between(m, lo, hi, color=AMBER, alpha=0.35, lw=0)
    b.plot(m, hi, color=ORANGE, lw=1.2)
    b.plot(m, lo, color=ORANGE, lw=1.2)
    b.text(6.5, max(hi) + 0.25, "at 1.45 kWh/km", ha="center", fontsize=8.6, color=SLATE)
    b.text(6.5, min(lo[5:7]) - 0.55, "at 2.1 kWh/km", ha="center", fontsize=8.6, color=SLATE)
    b.set_xticks(m, lab)
    b.set_ylim(0, 6)
    b.set_ylabel("hours of service a day")
    b.set_title("B  Hours of 10-minute shuttle it equals", fontsize=10, loc="left", color=SLATE, fontweight="bold")
    b.grid(axis="y", color="#E3E6E8", lw=0.6)
    b.set_axisbelow(True)
    fig.savefig(OUT / "fig2_output.png", bbox_inches="tight", facecolor="white")
    plt.close(fig)


fig1()
fig2()
print("figures in", OUT)
