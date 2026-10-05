"""Figures for Claim Check 030, drawn from data/cc-030/ (run calc.py first)."""
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
V = {(r["item"], r["year"]): float(r["value"]) for r in csv.DictReader(open(ROOT / "data" / "cc-030" / "mia_emissions.csv",
                                                                           encoding="utf-8"))}


def fig1():
    """Footprint by scope, 2025, on a log axis so that every bar is visible."""
    s1, s2 = V[("Scope 1 GHG emissions", "2025")], V[("Scope 2 GHG emissions (location based)", "2025")]
    c11 = V[("Scope 3 Category 11 use of sold products (aircraft incl. APU and GPU)", "2025")]
    s3 = V[("Scope 3 total", "2025")]
    items = [("Programme: CO$_2$ avoided\n(projected, a year)", 1000, ORANGE), ("Scope 1", s1, GREEN), ("Scope 2", s2, GREEN),
             ("Scope 3 other\nthan aircraft", s3 - c11, BLUE), ("Scope 3: aircraft\n(full flight)", c11, BLUE)]
    fig, ax = plt.subplots(figsize=(9.6, 3.6), dpi=220)
    for i, (n, v, c) in enumerate(items):
        ax.barh(i, v, color=c, height=0.6)
        ax.text(v * 1.15 if v != 4582 else v * 1.6, i, f"{v:,.0f} t", va="center", fontsize=8.5, color=SLATE, fontweight="bold")
    ax.axvline(5450, color=RED, lw=1, ls="--")
    ax.text(5450 * 1.1, -0.45, "credits bought: 5,450 t", color=RED, fontsize=8, va="center")
    ax.set_yticks(range(len(items)))
    ax.set_yticklabels([n for n, _, _ in items], fontsize=8.5)
    ax.invert_yaxis()
    ax.set_xscale("log")
    ax.set_xlim(300, 4e6)
    ax.set_xlabel("tonnes of CO$_2$ in 2025 (log scale)")
    ax.set_title("Carbon neutrality covers Scope 1 and 2; the airport's reported footprint is 99% Scope 3",
                 fontsize=9.5, color=GREEN, loc="left", fontweight="bold")
    ax.text(300, 5.55, "Source: MIA Sustainability Report 2025, GRI 102-5 to 102-7 and p.33; MIA press release May 2026. "
            "Scope 3 for 2025 uses a wider aircraft method than 2024.", fontsize=6.6, color=GREY)
    fig.savefig(OUT / "fig1_scopes.png", bbox_inches="tight", facecolor="white")


def fig2():
    """GPU-hours needed to avoid 1,000 t under assumed emission rates."""
    fig, ax = plt.subplots(figsize=(9.6, 3.0), dpi=220)
    kgs = list(range(30, 121, 5))
    ax.plot(kgs, [1e6 / k / 1000 for k in kgs], color=GREEN, lw=2)
    turn = 65470 / 2
    for k in (40, 60, 90):
        h = 1e6 / k / 1000
        ax.plot([k], [h], "o", color=ORANGE, ms=6)
        ax.text(k + 4, h + 3.2, f"{h*1000:,.0f} h\n({h*1000/turn*60:.0f} min per turnaround)", ha="left", fontsize=7.5, color=SLATE)
    ax.set_xlabel("Assumed CO$_2$ emitted per hour of diesel ground power (kg) – an illustration, not a sourced value")
    ax.set_ylabel("Thousand GPU-hours a year")
    ax.set_ylim(0, 42)
    ax.set_title("What must be true for 1,000 t a year: hours of diesel ground power replaced", fontsize=9.5, color=GREEN,
                 loc="left", fontweight="bold")
    ax.text(30, -9.5, "Minutes per turnaround assume every one of about 32,700 turnarounds (65,470 movements, second-hand) "
            "used ground power.", fontsize=6.8, color=GREY)
    fig.savefig(OUT / "fig2_gpu.png", bbox_inches="tight", facecolor="white")


fig1()
fig2()
print("figures in", OUT)
