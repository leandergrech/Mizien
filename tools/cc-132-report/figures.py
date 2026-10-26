"""Figures for Claim Check 132, drawn from data/cc-132/ (run calc.py first)."""
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
A1 = {(r["geo"], r["frequenc"]): float(r["value"])
      for r in csv.DictReader(open(ROOT / "data" / "cc-132" / "eurostat_ilc_atst01_2024.csv"))}
MS = ["BE", "BG", "CZ", "DK", "DE", "EE", "IE", "EL", "ES", "FR", "HR", "IT", "CY", "LV", "LT", "LU", "HU", "MT", "NL",
      "AT", "PL", "PT", "RO", "SI", "SK", "FI", "SE"]


def fig1():
    order = sorted(MS, key=lambda g: -A1[(g, "NVR")])
    fig, ax = plt.subplots(figsize=(9.6, 4.4), dpi=220)
    cols = [RED if g == "MT" else SAGE for g in order]
    ax.bar(order, [A1[(g, "NVR")] for g in order], color=cols, width=0.72)
    eu = A1[("EU27_2020", "NVR")]
    ax.axhline(eu, color=SLATE, lw=1.4, ls="--")
    ax.text(26.4, eu + 1.2, f"EU-27: {eu}%", ha="right", fontsize=9, color=SLATE, fontweight="bold")
    mt = A1[("MT", "NVR")]
    i = order.index("MT")
    ax.text(i, mt + 1.5, f"Malta {mt}%", ha="center", fontsize=9, color=RED, fontweight="bold")
    ax.set_ylabel("People 16+ never using public transport (%)")
    ax.set_ylim(0, 92)
    ax.text(-0.6, -17, "Eurostat ilc_atst01, 2024, persons aged 16 or over (retrieved 26 Oct 2026). "
            "Malta is tied with Croatia (58.6%).", fontsize=7, color=GREY)
    fig.savefig(OUT / "fig1_never_use.png", bbox_inches="tight", facecolor="white")


def fig2():
    fig, ax = plt.subplots(figsize=(9.6, 2.5), dpi=220)
    cats = [("DAY", "Every day", GREEN), ("WEEK", "Every week", SAGE), ("MTH", "Every month", BLUE),
            ("LT1M", "Less than monthly", AMBER), ("NVR", "Never", RED)]
    for y, (g, lab) in enumerate((("EU27_2020", "EU-27"), ("MT", "Malta"))):
        left = 0
        for k, name, c in cats:
            v = A1[(g, k)]
            ax.barh(y, v, left=left, color=c, height=0.6, label=name if y == 0 else None)
            ax.text(left + v / 2, y, f"{v:.1f}", ha="center", va="center", fontsize=8.5,
                    color="white" if k in ("DAY", "NVR", "MTH") else SLATE, fontweight="bold")
            left += v
    ax.set_yticks([0, 1])
    ax.set_yticklabels(["EU-27", "Malta"])
    ax.set_xlim(0, 100)
    ax.set_xlabel("% of persons aged 16+, by how often they use public transport, 2024")
    ax.legend(ncol=5, frameon=False, fontsize=8, loc="upper center", bbox_to_anchor=(0.5, 1.25))
    fig.savefig(OUT / "fig2_frequency.png", bbox_inches="tight", facecolor="white")


fig1()
fig2()
