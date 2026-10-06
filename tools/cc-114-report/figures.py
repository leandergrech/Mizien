"""Figures for Claim Check 114, drawn from data/cc-114/ (run fetch.py and calc.py first)."""
import csv
import pathlib

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib import font_manager as fm  # noqa: E402
from matplotlib.patches import Patch  # noqa: E402
from matplotlib.lines import Line2D  # noqa: E402

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[1]
D = ROOT / "data" / "cc-114"
OUT = HERE / "out"
OUT.mkdir(exist_ok=True)
for f in ["LiberationSans-Regular", "LiberationSans-Bold", "LiberationSans-Italic"]:
    fm.fontManager.addfont(f"/usr/share/fonts/truetype/liberation/{f}.ttf")
plt.rcParams.update({"font.family": "Liberation Sans", "axes.spines.top": False, "axes.spines.right": False,
                     "axes.edgecolor": "#8A9399", "axes.labelcolor": "#2B3A42", "xtick.color": "#2B3A42",
                     "ytick.color": "#2B3A42"})
GREEN, SAGE, AMBER, RED, SLATE, GREY, ORANGE, BLUE, PALE = ("#14452F", "#7FA88B", "#E3A72F", "#B5483A", "#2B3A42",
                                                            "#8A9399", "#D9772B", "#3C6E8F", "#E6EFE8")
V = {}
for r in csv.DictReader(open(D / "eurostat_extract.csv")):
    V[(r["dataset"], r["geo"], r["item"], r["unit"], int(r["year"]))] = float(r["value"])
RANK = {}
for r in csv.DictReader(open(D / "ranking_2013_2024.csv")):
    RANK[(r["measure"], r["geo"])] = float(r["change_2013_2024_pct"])
NAMES = {r["geo"]: r["name"] for r in csv.DictReader(open(D / "ranking_2013_2024.csv"))}
M_PUB = "Published: GHG of resident units per euro of GVA (Eurostat)"
M_INV = "Territorial inventory per euro of GDP (volumes)"
SRC = "Source: Eurostat env_ac_aeint_r2, env_air_gge, nama_10_gdp (retrieved 6 Oct 2026). 2024 values in the air " \
      "emissions accounts are Eurostat estimates (flag i)."


def fig1():
    geos = sorted(NAMES, key=lambda c: RANK[(M_PUB, c)])
    eu_pub = V[("env_ac_aeint_r2", "EU27_2020", "GHG|TOTAL|B1G", "G_EUR_CLV20", 2024)] / \
        V[("env_ac_aeint_r2", "EU27_2020", "GHG|TOTAL|B1G", "G_EUR_CLV20", 2013)] * 100 - 100
    inv = lambda g, y: V[("env_air_gge", g, "GHG|TOTX4_MEMO", "MIO_T", y)] / V[("nama_10_gdp", g, "B1GQ", "CLV20_MEUR", y)]
    eu_inv = inv("EU27_2020", 2024) / inv("EU27_2020", 2013) * 100 - 100
    fig, ax = plt.subplots(figsize=(9.6, 6.7), dpi=220)
    for i, g in enumerate(geos):
        a, b = RANK[(M_PUB, g)], RANK[(M_INV, g)]
        if g == "MT":
            ax.axhspan(i - 0.5, i + 0.5, color=PALE, zorder=0)
        ax.plot([a, b], [i, i], color="#C9D0CC", lw=1.4, zorder=1)
        ax.scatter([b], [i], s=46, facecolor="white", edgecolor=BLUE, linewidth=1.8, zorder=3)
        ax.scatter([a], [i], s=46, color=RED if a > 0 else GREEN, edgecolor="white", linewidth=1.2, zorder=4)
    ax.set_yticks(range(len(geos)))
    ax.set_yticklabels([NAMES[g] for g in geos], fontsize=8.6)
    for t in ax.get_yticklabels():
        if t.get_text() == "Malta":
            t.set_fontweight("bold")
    mi = geos.index("MT")
    ax.annotate(f"{RANK[(M_PUB, 'MT')]:+.1f}%\nEurostat’s\nindicator", (RANK[(M_PUB, "MT")], mi),
                xytext=(23, mi - 5), fontsize=8, color=RED, ha="right", va="center",
                arrowprops=dict(arrowstyle="-", color=RED, lw=0.8))
    ax.annotate(f"{RANK[(M_INV, 'MT')]:+.1f}%  territorial inventory\nper euro of GDP",
                (RANK[(M_INV, "MT")], mi), xytext=(-70, mi - 8.6), fontsize=8, color=BLUE,
                ha="left", va="center", arrowprops=dict(arrowstyle="-", color=BLUE, lw=0.8))
    ax.axvline(0, color=SLATE, lw=0.8)
    ax.axvline(eu_pub, color=GREEN, lw=0.8, ls="--")
    ax.axvline(eu_inv, color=BLUE, lw=0.8, ls=":")
    ax.text(eu_pub + 0.6, len(geos) - 0.15, f"EU {eu_pub:.1f}%", color=GREEN, fontsize=7.8, ha="left", va="bottom")
    ax.text(eu_inv - 0.6, -0.65, f"EU {eu_inv:.1f}%", color=BLUE, fontsize=7.8, ha="right", va="bottom")
    ax.set_xlim(-72, 25)
    ax.set_ylim(-0.7, len(geos) + 0.6)
    ax.set_xlabel("Change in greenhouse gas emissions per euro of output, 2013–2024 (%)", fontsize=9)
    ax.legend(handles=[Line2D([], [], marker="o", ls="", color=GREEN, markersize=7,
                              label="Eurostat’s published indicator: emissions of resident units per euro of GVA "
                                    "(red = increase)"),
                       Line2D([], [], marker="o", ls="", markerfacecolor="white", markeredgecolor=BLUE,
                              markeredgewidth=1.8, markersize=7,
                              label="Territorial greenhouse gas inventory per euro of GDP (both in volumes)")],
              loc="lower center", bbox_to_anchor=(0.45, 1.0), frameon=False, fontsize=8.2, ncol=1)
    ax.grid(axis="x", color="#E3E7E4", lw=0.6)
    ax.set_axisbelow(True)
    fig.text(0.01, 0.005, SRC, fontsize=6.8, color=GREY)
    fig.savefig(OUT / "fig1_ranking.png", bbox_inches="tight", facecolor="white")
    plt.close(fig)


def fig2():
    yrs = list(range(2008, 2025))
    em = lambda n, y: V[("env_ac_ainah_r2", "MT", f"GHG|{n}", "THS_T", y)] / 1000
    air = [em("H51", y) for y in yrs]
    elec = [em("D", y) for y in yrs]
    other = [em("TOTAL", y) - em("H51", y) - em("D", y) for y in yrs]
    inv = [V[("env_air_gge", "MT", "GHG|TOTX4_MEMO", "MIO_T", y)] for y in yrs]
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(10.4, 4.3), dpi=220, gridspec_kw={"width_ratios": [1.05, 1]})
    for i, y in enumerate(yrs):
        hatch = "////" if y == 2024 else None
        a1.bar(y, elec[i], 0.78, color=SLATE, edgecolor="white", linewidth=0.6, hatch=hatch)
        a1.bar(y, other[i], 0.78, bottom=elec[i], color=SAGE, edgecolor="white", linewidth=0.6, hatch=hatch)
        a1.bar(y, air[i], 0.78, bottom=elec[i] + other[i], color=RED, edgecolor="white", linewidth=0.6, hatch=hatch)
    a1.plot(yrs, inv, color=BLUE, lw=2, marker="o", markersize=3.5, markerfacecolor="white", zorder=5)
    a1.text(2008.2, inv[0] + 0.25, "Territorial inventory (all of Malta)", color=BLUE, fontsize=7.8)
    a1.text(2024.5, elec[-1] + other[-1] + air[-1] / 2, f"air\ntransport\n{air[-1]:.1f} Mt", color=RED, fontsize=7.6,
            va="center")
    a1.text(2024.5, elec[-1] / 2, f"electricity\n{elec[-1]:.1f} Mt", color=SLATE, fontsize=7.6, va="center")
    a1.text(2024.5, elec[-1] + other[-1] / 2, "other", color=GREEN, fontsize=7.6, va="center")
    a1.set_xlim(2007.3, 2027.6)
    a1.set_ylim(0, 7.4)
    a1.set_xticks([2008, 2013, 2018, 2024])
    a1.set_ylabel("Mt CO₂ equivalent", fontsize=9)
    a1.set_title("A. Malta: greenhouse gases of resident production units", fontsize=9.6, color=SLATE, loc="left")
    a1.legend(handles=[Patch(color=RED, label="Air transport (H51)"), Patch(color=SAGE, label="Other activities"),
                       Patch(color=SLATE, label="Electricity, gas, steam (D)"),
                       Patch(facecolor="white", edgecolor=GREY, hatch="////", label="2024: Eurostat estimate")],
              frameon=False, fontsize=7.4, loc="upper left", bbox_to_anchor=(0.0, 0.92))
    pub = {y: V[("env_ac_aeint_r2", "MT", "GHG|TOTAL|B1G", "G_EUR_CLV20", y)] for y in yrs}
    gva = {y: V[("nama_10_a64", "MT", "TOTAL|B1G", "CLV20_MEUR", y)] for y in yrs}
    x51 = {y: (em("TOTAL", y) - em("H51", y)) / gva[y] for y in yrs}
    gdp = {y: V[("nama_10_gdp", "MT", "B1GQ", "CLV20_MEUR", y)] for y in yrs}
    tin = {y: V[("env_air_gge", "MT", "GHG|TOTX4_MEMO", "MIO_T", y)] / gdp[y] for y in yrs}
    ix = lambda s: [100 * s[y] / s[2013] for y in yrs]
    for s, c, ls, lab, dy in ((ix(pub), RED, "-", "Eurostat’s indicator (resident units)", 0),
                              (ix(x51), GREEN, "--", "Same, without air transport (H51)", 3),
                              (ix(tin), BLUE, ":", "Territorial inventory per € of GDP", -5)):
        a2.plot(yrs, s, color=c, lw=2.2, ls=ls, label=lab)
        a2.text(2024.35, s[-1] + dy, f"{s[-1] - 100:+.0f}%", color=c, fontsize=8.4, fontweight="bold", va="center")
    a2.legend(frameon=False, fontsize=7.6, loc="lower left", bbox_to_anchor=(0.0, 0.02), handlelength=3)
    a2.axhline(100, color=GREY, lw=0.7)
    a2.axvspan(2023.5, 2024.5, color="#EEF0F1", zorder=0)
    a2.text(2024, 6, "est.", ha="center", fontsize=7, color=GREY)
    a2.set_xlim(2007.3, 2026.6)
    a2.set_ylim(0, 150)
    a2.set_xticks([2008, 2013, 2018, 2024])
    a2.set_ylabel("Index, 2013 = 100", fontsize=9)
    a2.set_title("B. Malta: emissions per euro of output", fontsize=9.6, color=SLATE, loc="left")
    fig.text(0.01, -0.02, "Source: Eurostat env_ac_ainah_r2, env_ac_aeint_r2, env_air_gge (excl. LULUCF and "
             "international bunkers), nama_10_a64, nama_10_gdp; chain-linked volumes (2020). Retrieved 6 Oct 2026.",
             fontsize=6.8, color=GREY)
    fig.tight_layout()
    fig.savefig(OUT / "fig2_malta.png", bbox_inches="tight", facecolor="white")
    plt.close(fig)


if __name__ == "__main__":
    fig1()
    fig2()
    print("figures ->", OUT)
