"""Figures for Claim Check 075, drawn from data/cc-075/ (run fetch.py and calc.py first)."""
import csv, pathlib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from matplotlib.lines import Line2D

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[1]
D = ROOT / "data" / "cc-075"
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


def load(f):
    out = {}
    for r in csv.DictReader(open(D / f)):
        out[(r["geo"], int(r["time"]))] = (float(r["value"]), r.get("flag", ""))
    return out


HAB = load("eurostat_road_eqs_carhab.csv")
STOCK = load("eurostat_road_eqs_carmot.csv")
POP = load("eurostat_demo_gind_jan.csv")


def ranked(y):
    return sorted(((HAB[(g, y)][0], g) for g in EU27 if (g, y) in HAB), reverse=True)


def runs(xs):
    out, cur = [], [xs[0]]
    for x in xs[1:]:
        if x == cur[-1] + 1:
            cur.append(x)
        else:
            out.append(cur); cur = [x]
    out.append(cur)
    return out


def fig1():
    """Malta and EU-27 rate (top) and Malta's rank (bottom), 1990-2025: two panels, one y-scale each."""
    fig, (ax, ax2) = plt.subplots(2, 1, figsize=(9.6, 4.9), dpi=220, sharex=True,
                                  gridspec_kw={"height_ratios": [3, 2], "hspace": 0.12})
    for geo, col, ls in (("MT", GREEN, "-"), ("EU27_2020", BLUE, "--")):
        xs = sorted(y for (g, y) in HAB if g == geo)
        for run in runs(xs):
            ax.plot(run, [HAB[(geo, y)][0] for y in run], color=col, lw=2.2, ls=ls, zorder=2)
        ax.plot(xs, [HAB[(geo, y)][0] for y in xs], ls="none", marker="o", ms=3.2, color=col, zorder=3)
    ax.axvspan(2021.6, 2022.4, color=AMBER, alpha=0.18, lw=0, zorder=0)
    ax.text(2022, 300, "2022:\nthe article’s\nfigures", ha="center", va="bottom", fontsize=7.5, color=SLATE)
    ax.axvspan(2002.6, 2004.4, color="#EEF0EE", lw=0, zorder=0)
    ax.text(2003.5, 300, "no Malta\nvalue", ha="center", va="bottom", fontsize=7, color=GREY)
    for y, dy in ((2016, 14), (2022, 16), (2025, -30)):
        ax.text(y, HAB[("MT", y)][0] + dy, f"{HAB[('MT', y)][0]:.0f}", color=GREEN, fontsize=8.5, ha="center",
                fontweight="bold")
    for y, dy in ((2010, -30), (2025, 14)):
        ax.text(y, HAB[("EU27_2020", y)][0] + dy, f"{HAB[('EU27_2020', y)][0]:.0f}", color=BLUE, fontsize=8.5,
                ha="center")
    ax.set_ylim(280, 680)
    ax.set_ylabel("passenger cars per 1,000")
    ax.legend(handles=[Line2D([], [], color=GREEN, lw=2.2, marker="o", ms=3.2, label="Malta"),
                       Line2D([], [], color=BLUE, lw=2.2, ls="--", marker="o", ms=3.2,
                              label="EU-27 (published for 2000 and 2010–2025)")],
              frameon=False, fontsize=8.5, loc="upper left")
    xs = [y for y in range(1990, 2026) if ("MT", y) in HAB]
    rk = [[g for _, g in ranked(y)].index("MT") + 1 for y in xs]
    for run in runs(xs):
        ax2.plot(run, [rk[xs.index(y)] for y in run], color=GREEN, lw=2.0, zorder=2)
    ax2.plot(xs, rk, ls="none", marker="o", ms=3.4, color=GREEN, zorder=3)
    for y, dx, dy, ha in ((1990, 0, 1.6, "center"), (2016, 0, 1.6, "center"), (2022, -0.6, 0.9, "right"),
                          (2025, 0, 1.6, "center")):
        r = rk[xs.index(y)]
        ax2.text(y + dx, r + dy, f"{r}{'th' if r not in (1, 2, 3) else {1: 'st', 2: 'nd', 3: 'rd'}[r]}", ha=ha,
                 va="top", fontsize=8.5, color=GREEN, fontweight="bold")
    ax2.axvspan(2021.6, 2022.4, color=AMBER, alpha=0.18, lw=0, zorder=0)
    ax2.axvspan(2002.6, 2004.4, color="#EEF0EE", lw=0, zorder=0)
    ax2.set_ylim(17, 0)
    ax2.set_yticks([1, 3, 7, 11, 14])
    ax2.set_ylabel("Malta’s rank in EU-27")
    ax2.set_xlim(1989.3, 2026)
    ax2.set_xticks(range(1990, 2026, 5))
    ax2.text(1989.4, 23.5, "Source: Eurostat road_eqs_carhab (updated 30 Jul 2026, retrieved 6 Oct 2026). Rank among the "
             "EU-27 countries with a value that year (25–27 before 2010, 27 from 2010).\nMalta’s values carry no Eurostat flags. "
             "Rank 1 = most cars per person.", fontsize=7, color=GREY)
    fig.savefig(OUT / "fig1_trend.png", bbox_inches="tight", facecolor="white")


def fig2():
    """2022, all 27 Member States: the year the article's figures match."""
    y = 2022
    fig, ax = plt.subplots(figsize=(9.6, 3.5), dpi=220)
    items = [(g, v) for v, g in ranked(y)]
    ax.bar([k for k, _ in items], [v for _, v in items], color=[GREEN if k == "MT" else SAGE for k, _ in items],
           width=0.72)
    for i, (k, v) in enumerate(items):
        f = HAB[(k, y)][1]
        ax.text(i, v + 8, f"{v:.0f}" + (f"\n{f}" if f else ""), ha="center", va="bottom", fontsize=6.6,
                color=GREEN if k == "MT" else SLATE, fontweight="bold" if k == "MT" else "normal", linespacing=0.9,
                zorder=4, bbox=dict(facecolor="white", edgecolor="none", pad=0.3))
    eu = HAB[("EU27_2020", y)][0]
    ax.axhline(eu, color=BLUE, lw=1.3, ls="--")
    ax.text(26.4, eu + 52, f"EU-27 {eu:.0f}", color=BLUE, fontsize=8.5, ha="right")
    i = [k for k, _ in items].index("MT")
    ax.annotate("Malta 7th", xy=(i, HAB[("MT", y)][0] + 45), xytext=(i + 3.2, 720), fontsize=9, color=GREEN,
                fontweight="bold", arrowprops=dict(arrowstyle="-", color=GREEN, lw=0.9))
    ax.set_ylim(0, 760)
    ax.set_ylabel("passenger cars per 1,000")
    ax.tick_params(axis="x", labelsize=8)
    ax.text(-0.5, -150, "Eurostat road_eqs_carhab, 2022, retrieved 6 Oct 2026. All 27 Member States have a value. "
            "Flags: b = break in time series (DE, LV), i = imputed (PL),\ne = estimated (RO). Country codes are "
            "Eurostat’s (EL = Greece).", fontsize=7, color=GREY)
    fig.savefig(OUT / "fig2_rank2022.png", bbox_inches="tight", facecolor="white")


def fig5():
    """2023 as Eurostat published it in July 2024 (Statistics Explained Figure 3, read by pixel in read_charts.py)."""
    names = {"Belgium": "BE", "Bulgaria": "BG", "Czechia": "CZ", "Denmark": "DK", "Germany": "DE", "Estonia": "EE",
             "Ireland": "IE", "Greece": "EL", "Spain": "ES", "France": "FR", "Croatia": "HR", "Italy": "IT",
             "Cyprus": "CY", "Latvia": "LV", "Lithuania": "LT", "Luxembourg": "LU", "Hungary": "HU", "Malta": "MT",
             "Netherlands": "NL", "Austria": "AT", "Poland": "PL", "Portugal": "PT", "Romania": "RO", "Slovenia": "SI",
             "Slovakia": "SK", "Finland": "FI", "Sweden": "SE"}
    rd = [r for r in csv.DictReader(open(D / "chart_reads.csv")) if r["file"] == "es_fig3_motorisation_2023.png"]
    eu = next(float(r["value_read"]) for r in rd if r["label"] == "EU")
    items = sorted(((names[r["label"]], float(r["value_read"])) for r in rd if r["label"] in names),
                   key=lambda kv: -kv[1])
    fig, ax = plt.subplots(figsize=(9.6, 3.5), dpi=220)
    ax.bar([k for k, _ in items], [v for _, v in items], color=[RED if k == "MT" else SAGE for k, _ in items],
           width=0.72)
    for i, (k, v) in enumerate(items):
        if k in ("FR", "MT", "AT"):   # only Malta and its neighbours: read values carry about +/-1 of error
            ax.text(i, v + 8, f"≈{v:.0f}", ha="center", va="bottom", fontsize=6.8, color=RED if k == "MT" else SLATE,
                    fontweight="bold" if k == "MT" else "normal", zorder=4,
                    bbox=dict(facecolor="white", edgecolor="none", pad=0.3))
    ax.axhline(eu, color=BLUE, lw=1.3, ls="--")
    ax.text(26.4, eu + 52, f"EU 571 (Eurostat’s text)", color=BLUE, fontsize=8.5, ha="right")
    i = [k for k, _ in items].index("MT")
    ax.annotate("Malta 12th", xy=(i, items[i][1] + 45), xytext=(i + 3.2, 720), fontsize=9, color=RED,
                fontweight="bold", arrowprops=dict(arrowstyle="-", color=RED, lw=0.9))
    ax.set_ylim(0, 760)
    ax.set_ylabel("passenger cars per 1,000")
    ax.tick_params(axis="x", labelsize=8)
    ax.text(-0.5, -150, "2023 values as Eurostat published them by 25 July 2024 (Statistics Explained, ‘Passenger cars in "
            "the EU’, Figure 3; revision 647912, live 19 Aug – 5 Nov 2024),\nread by pixel measurement from Eurostat’s "
            "chart (within 1.1 of every value Eurostat prints in the text, so labels are approximate). Retrieved 6 Oct 2026.", fontsize=7, color=GREY)
    fig.savefig(OUT / "fig5_published2023.png", bbox_inches="tight", facecolor="white")


fig1(); fig2(); fig5()
print("figures in", OUT)
