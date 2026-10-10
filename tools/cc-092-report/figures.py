"""Figures for Claim Check 092, drawn from data/cc-092/ (run calc.py first). Output: out/*.png"""
import csv, pathlib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[1]
D = ROOT / "data" / "cc-092"
OUT = HERE / "out"
OUT.mkdir(exist_ok=True)
for f in ["LiberationSans-Regular", "LiberationSans-Bold", "LiberationSans-Italic"]:
    fm.fontManager.addfont(f"/usr/share/fonts/truetype/liberation/{f}.ttf")
plt.rcParams.update({"font.family": "Liberation Sans", "axes.spines.top": False, "axes.spines.right": False,
                     "axes.edgecolor": "#8A9399", "axes.labelcolor": "#2B3A42", "xtick.color": "#2B3A42",
                     "ytick.color": "#2B3A42"})
GREEN, SAGE, AMBER, RED, SLATE, GREY, ORANGE, BLUE, PALE = ("#14452F", "#7FA88B", "#E3A72F", "#B5483A", "#2B3A42",
                                                            "#8A9399", "#D9772B", "#3C6E8F", "#E6EFE8")
C2 = 44 / 12
t16 = {int(r["year"]): float(r["co2_t"]) for r in csv.DictReader(open(D / "gozo_energy_baseline_table16.csv"))
       if r["sector"] == "Total"}
rates = {r["key"]: r for r in csv.DictReader(open(D / "sequestration_rates.csv"))}
GOZO_HA = 6700


def tco2(k):
    r = rates[k]
    v = float(r["value"])
    return v / 100 * C2 if r["unit"].startswith("g C") else v


def fig1():
    """Measured and reviewed sequestration rates against the rate all of Gozo would need."""
    need_lo, need_hi = t16[2020] / GOZO_HA, t16[2019] / GOZO_HA
    rows = [  # label, low, high, point, used-case
        ("Native holm and cork oak on former cropland, Spain\n(tree biomass; Renna et al. 2024)",
         tco2("renna2024_low"), tco2("renna2024_high"), tco2("renna2024_low"), "low case"),
        ("Aleppo pine on former shrubland, Yatir, Israel\n(trees and soil, 35-year mean; Grünzweig et al. 2007)",
         None, None, tco2("grunzweig2007"), "central case"),
        ("Planted oak, temperate dry climates\n(biomass, first 20 years; Bernal et al. 2018)", 5.3 - 3.5, 5.3 + 3.5, 5.3, ""),
        ("Planted conifers other than pine, temperate dry\n(biomass, first 20 years; Bernal et al. 2018)", 6.4 - 1.9, 6.4 + 1.9, 6.4, ""),
        ("Planted pine, temperate dry climates\n(biomass, first 20 years; Bernal et al. 2018)", 7.6 - 2.0, 7.6 + 2.0, 7.6, "high case"),
    ]
    fig, ax = plt.subplots(figsize=(9.6, 3.9), dpi=220)
    ax.axvspan(need_lo, need_hi, color=RED, alpha=0.13, lw=0)
    ax.text((need_lo + need_hi) / 2, len(rows) - 0.35, "Rate every hectare\nof Gozo would need\nto offset its energy CO₂",
            ha="center", va="top", fontsize=7.6, color=RED)
    for i, (lab, lo, hi, pt, case) in enumerate(rows):
        y = len(rows) - 1 - i
        if lo is not None:
            ax.plot([lo, hi], [y, y], color=SAGE if not case else GREEN, lw=2.2, solid_capstyle="round")
        ax.plot([pt], [y], "o", ms=7, color=GREEN if case else GREY, mec="white", mew=1.4, zorder=3)
        txt = f"{pt:.2f}" if pt < 1 else f"{pt:.1f}"
        ax.text(pt, y + 0.22, txt + (f"  ({case})" if case else ""), fontsize=7.4, color=SLATE, ha="left")
    ax.set_yticks(range(len(rows)))
    ax.set_yticklabels([r[0] for r in rows][::-1], fontsize=7.2)
    ax.set_xlim(0, 25)
    ax.set_ylim(-0.6, len(rows) - 0.2)
    ax.set_xlabel("t CO₂ per hectare per year (bars: reported range or 95% interval)", fontsize=8)
    ax.grid(axis="x", color="#D5DBD7", lw=0.6)
    ax.set_axisbelow(True)
    ax.set_title("Carbon stored by new Mediterranean and dry-climate forests, and what Gozo would need",
                 fontsize=9.5, color=GREEN, loc="left", fontweight="bold")
    fig.text(0.01, -0.06, f"Need: Gozo's energy CO₂ 2016–20 ({t16[2020]:,.0f}–{t16[2019]:,.0f} t, Energy Baseline Scenario for "
             f"Gozo, Table 16) ÷ 6,700 ha = {need_lo:.1f}–{need_hi:.1f} t. Source: data/cc-092/sequestration_rates.csv.",
             fontsize=6.8, color=GREY)
    fig.savefig(OUT / "fig1_rates.png", bbox_inches="tight", facecolor="white")
    plt.close(fig)


def fig2():
    """Forest area needed, as a multiple of Gozo's land area."""
    cases = [("Low rate, 0.92 t\n(native oaks, Spain)", tco2("renna2024_low")),
             ("Central rate, 3.62 t\n(Yatir pine forest)", tco2("grunzweig2007")),
             ("High rate, 7.6 t\n(planted pine, review)", 7.6)]
    fig, ax = plt.subplots(figsize=(9.6, 2.9), dpi=220)
    for i, (lab, r) in enumerate(cases):
        y = len(cases) - 1 - i
        lo, hi = t16[2020] / r / GOZO_HA, t16[2019] / r / GOZO_HA
        ax.barh(y, hi, height=0.5, color=PALE, edgecolor="none")
        ax.barh(y, lo, height=0.5, color=GREEN if i == 1 else SAGE, edgecolor="none")
        ax.text(hi + 0.3, y, f"{lo:.1f}–{hi:.1f}× Gozo  ({lo * 67:,.0f}–{hi * 67:,.0f} km²)", va="center", fontsize=8,
                color=SLATE)
    ax.axvline(1, color=RED, lw=1.8)
    ax.text(1.25, len(cases) - 0.45, "All of Gozo (67 km²)", color=RED, fontsize=7.8, va="bottom")
    ax.set_yticks(range(len(cases)))
    ax.set_yticklabels([c[0] for c in cases][::-1], fontsize=7.8)
    ax.set_xlim(0, 32)
    ax.set_ylim(-0.5, len(cases) - 0.1)
    ax.set_xlabel("New forest needed, as a multiple of Gozo’s land area (dark: 2020, lowest year; light: 2019, highest)",
                  fontsize=8)
    ax.grid(axis="x", color="#D5DBD7", lw=0.6)
    ax.set_axisbelow(True)
    ax.set_title("Forest needed to offset Gozo’s energy CO₂ by trees alone", fontsize=9.5, color=GREEN, loc="left",
                 fontweight="bold")
    fig.text(0.01, -0.1, "Emissions: Energy Baseline Scenario for Gozo (2023), Table 16. Rates: Renna et al. 2024; "
             "Grünzweig et al. 2007; Bernal et al. 2018. Source: data/cc-092/afforestation_offset.csv.", fontsize=6.8,
             color=GREY)
    fig.savefig(OUT / "fig2_forest_needed.png", bbox_inches="tight", facecolor="white")
    plt.close(fig)


def fig3():
    """Gozo's land cover (CORINE 2018) and the share of its energy CO2 that planting could offset."""
    chk = {r["check"]: r for r in csv.DictReader(open(D / "checks.csv"))}
    v = lambda k: float(chk[k]["value"])
    built = v("Gozo built-up and other artificial land (CORINE 112 + 131 + 142)")
    farm = v("Gozo farmland (CORINE 211 + 242 + 243)")
    semi = v("Gozo semi-natural land (CORINE 323 + 333)")
    fig, (a1, a2) = plt.subplots(2, 1, figsize=(9.6, 4.6), dpi=220, gridspec_kw={"height_ratios": [1, 2.1], "hspace": 0.75})
    left = 0
    for val, col, lab in ((built, GREY, "Built-up and other artificial"), (farm, AMBER, "Farmland"),
                          (semi, GREEN, "Semi-natural")):
        a1.barh(0, val, left=left, color=col, height=0.6, edgecolor="white", linewidth=2)
        a1.text(left + val / 2, 0, f"{lab}\n{val:,.0f} ha ({100 * val / (built + farm + semi):.0f}%)", ha="center",
                va="center", fontsize=7.2, color="white" if col != AMBER else SLATE)
        left += val
    a1.set_xlim(0, left)
    a1.set_yticks([])
    a1.spines["left"].set_visible(False)
    a1.set_xlabel("Hectares (CORINE Land Cover 2018; no forest class mapped on Gozo)", fontsize=7.6)
    a1.set_title("Gozo’s land, and how much of its energy CO₂ planting it could offset", fontsize=9.5, color=GREEN,
                 loc="left", fontweight="bold")
    scen = [("Plant all semi-natural land\n(about 1,270 ha)", "Semi-natural land (CORINE 323 + 333)"),
            ("Plant all farmland and\nsemi-natural land (about 5,070 ha)", "All farmland and semi-natural land (CORINE 2xx + 3xx)"),
            ("Plant all of Gozo\n(6,700 ha)", "All of Gozo (67 km2)")]
    for i, (lab, key) in enumerate(scen):
        y = len(scen) - 1 - i
        lo = float(chk[f"Share of Gozo's 2016-2020 energy CO2 offset if {key} were forest, low rate"]["value"].split("-")[0])
        hi = float(chk[f"Share of Gozo's 2016-2020 energy CO2 offset if {key} were forest, high rate"]["value"].split("-")[1])
        c_lo, c_hi = (float(x) for x in chk[f"Share of Gozo's 2016-2020 energy CO2 offset if {key} were forest, central rate"]["value"].split("-"))
        a2.plot([lo, hi], [y, y], color=SAGE, lw=6, solid_capstyle="butt")
        a2.plot([c_lo, c_hi], [y, y], color=GREEN, lw=6, solid_capstyle="butt")
        a2.text(hi + 1.5, y, f"{lo:.0f}–{hi:.0f}% (central {c_lo:.0f}–{c_hi:.0f}%)", va="center", fontsize=7.8, color=SLATE)
    a2.axvline(100, color=RED, lw=1.8)
    a2.text(98.5, len(scen) - 0.55, "Net zero by\ntrees alone", color=RED, fontsize=7.6, ha="right", va="top")
    a2.set_yticks(range(len(scen)))
    a2.set_yticklabels([s[0] for s in scen][::-1], fontsize=7.6)
    a2.set_xlim(0, 105)
    a2.set_ylim(-0.5, len(scen) - 0.4)
    a2.set_xlabel("Share of Gozo’s 2016–20 energy CO₂ offset (light: low to high rate; dark: central rate)", fontsize=7.6)
    a2.grid(axis="x", color="#D5DBD7", lw=0.6)
    a2.set_axisbelow(True)
    fig.text(0.01, -0.03, "Land: EEA CORINE Land Cover 2018 (25 ha mapping unit). Offset = area × rate ÷ 118,333–153,997 t. "
             "Ceilings, not plans. Semi-natural = classes 323 (incl. garrigue and maquis) and 333. Source: data/cc-092/checks.csv.",
             fontsize=6.8, color=GREY)
    fig.savefig(OUT / "fig3_land_offset.png", bbox_inches="tight", facecolor="white")
    plt.close(fig)


fig1()
fig2()
fig3()
print("figures in", OUT)
