"""Figures for Claim Check 109, drawn from data/cc-109/ (run fetch.py, read_graph.py and calc.py first)."""
import csv, pathlib
from collections import defaultdict
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from matplotlib.lines import Line2D

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[1]
D = ROOT / "data" / "cc-109"
OUT = HERE / "out"
OUT.mkdir(exist_ok=True)
for f in ["LiberationSans-Regular", "LiberationSans-Bold", "LiberationSans-Italic"]:
    fm.fontManager.addfont(f"/usr/share/fonts/truetype/liberation/{f}.ttf")
plt.rcParams.update({"font.family": "Liberation Sans", "axes.spines.top": False, "axes.spines.right": False,
                     "axes.edgecolor": "#8A9399", "axes.labelcolor": "#2B3A42", "xtick.color": "#2B3A42",
                     "ytick.color": "#2B3A42"})
GREEN, SAGE, AMBER, RED, SLATE, GREY, ORANGE, BLUE = ("#14452F", "#7FA88B", "#E3A72F", "#B5483A", "#2B3A42",
                                                      "#8A9399", "#D9772B", "#3C6E8F")
CHK = {r["check"]: r for r in csv.DictReader(open(D / "checks.csv"))}
num = lambda k: float(CHK[k]["value"])

E = defaultdict(dict)
for r in csv.DictReader(open(D / "eurostat_env_air_gge.csv")):
    E[(r["geo"], r["airpol"], r["src_crf"])][int(r["year"])] = float(r["value"])
T = {y: E[("MT", "GHG", "CRF1A3")][y] - E[("MT", "CO2", "CRF1A3A")][y] for y in E[("MT", "GHG", "CRF1A3")]}
R = E[("MT", "GHG", "CRF1A3B")]


def fig1():
    """The report's own Graph 3.1, redrawn from its vector data, with the report's 48% marked."""
    g = defaultdict(dict)
    for r in csv.DictReader(open(D / "graph31_bars.csv")):
        g[r["year"]][r["sector"]] = float(r["value_mt"])
    order = [("Domestic transport (excl. aviation)", GREEN, "Transport (excl. aviation)"),
             ("Small industry", "#B9CBD6", "Small industry"), ("Buildings (under ESR)", "#E8DCC0", "Buildings"),
             ("Agriculture", "#D3E2CC", "Agriculture"), ("Waste", "#CDD1D4", "Waste")]
    years = ["2005", "2023", "2024"]
    fig, ax = plt.subplots(figsize=(9.6, 4.4), dpi=220)
    xs = range(len(years))
    for x, y in zip(xs, years):
        base = 0
        tot = sum(g[y].values())
        for name, col, lab in order:
            v = g[y][name]
            ax.bar(x, v - 0.006, bottom=base, width=0.56, color=col, edgecolor="white", linewidth=0)
            if name.startswith("Domestic"):
                ax.text(x, base + v / 2, f"{v:.3f} Mt\n{100 * v / tot:.1f}%", ha="center", va="center",
                        color="white", fontsize=9.5, fontweight="bold")
            elif v / tot > 0.045:
                ax.text(x, base + v / 2, f"{lab} {100 * v / tot:.0f}%", ha="center", va="center", color=SLATE,
                        fontsize=7.4 if v / tot > 0.075 else 6.8)
            base += v
        ax.text(x, tot + 0.03, f"{tot:.3f} Mt", ha="center", color=SLATE, fontsize=8.5)
    tot24 = sum(g["2024"].values())
    y48 = 0.48 * tot24
    ax.plot([1.66, 2.34], [y48, y48], color=AMBER, lw=2.2, ls=(0, (4, 2)))
    ax.annotate("48% of the 2024 bar\n(the report’s text)", xy=(2.34, y48), xytext=(2.48, y48 - 0.22),
                fontsize=8.2, color=SLATE, va="center",
                arrowprops=dict(arrowstyle="-", color=AMBER, lw=1.2))
    ax.set_xticks(list(xs), years)
    ax.set_xlim(-0.55, 3.25)
    ax.set_ylim(0, 1.62)
    ax.set_ylabel("Mt CO$_2$e")
    ax.legend(handles=[Line2D([], [], color=c, lw=8, label=l) for _, c, l in order], frameon=False, fontsize=8,
              loc="upper left", ncol=5, bbox_to_anchor=(0, 1.08))
    ax.text(-0.55, -0.27, "Values read from the vector paths of Graph 3.1 in the Commission’s 2026 Country Report – Malta "
            "(p. 14; source named there: European Environment\nAgency); the 2024 total equals the EEA’s approximated "
            "inventory. Method: tools/cc-109-report/read_graph.py.", fontsize=7, color=GREY)
    fig.savefig(OUT / "fig1_graph31.png", bbox_inches="tight", facecolor="white")


def fig2():
    """Transport's 2024 share of effort-sharing emissions, by source and definition."""
    items = [
        ("The report’s text (pp. 6, 14, 66)", 48.0, AMBER, "claim"),
        ("Road transport only (1.A.3.b) ÷ ESR total\n(road-only ratios give "
         f"{CHK['Range of road-transport-only ratios that round to 48%']['value'].replace('-', '–')}%; our identification)",
         num("Road transport only (1.A.3.b), 2026 inventory, as share of the approximated ESR total, 2024"), GREY, ""),
        ("EEA approximated inventory 2024\n(transport excl. aviation CO2 ÷ ESR total)",
         num("Transport share of ESR emissions 2024, approximated inventory"), GREEN, ""),
        ("Commission CAPR 2025 country profile, Fig. 11",
         num("Transport share of ESR emissions 2024, Commission CAPR 2025 country profile"), GREEN, ""),
        ("The report’s own Graph 3.1 (p. 14)",
         num("Transport share of ESR emissions 2024, the report's own Graph 3.1"), GREEN, ""),
        ("2026 inventory, final submission\n(our estimate of the ESR total)",
         num("Transport share of ESR emissions 2024, 2026 inventory (our estimate)"), SAGE, ""),
    ]
    fig, ax = plt.subplots(figsize=(9.6, 4.0), dpi=220)
    for i, (lab, v, col, kind) in enumerate(items):
        y = len(items) - 1 - i
        ax.barh(y, v, height=0.58, color=col, hatch="////" if col == GREY else None, edgecolor="white", lw=0)
        txt = f"{v:.0f}%" if v == round(v) and kind == "claim" else f"{v:.1f}%"
        ax.text(v + 0.6, y, txt, va="center", fontsize=9.5, color=SLATE, fontweight="bold")
    ax.set_yticks(range(len(items)), [l for l, *_ in reversed(items)], fontsize=8.4)
    ax.axvline(48, color=AMBER, lw=1.2, ls=(0, (4, 2)))
    ax.set_xlim(0, 62)
    ax.set_xlabel("% of Malta’s effort-sharing (ESR) emissions in 2024")
    ax.text(0, -2.05, "Dark green: the definition the report uses for Graph 3.1 and the ESR uses (all domestic transport, CO2 "
            "from aviation excluded); light green: the same with the final 2026 inventory.\nGrey, hatched: road only, a narrower scope. Sources: data/cc-109/checks.csv "
            "(EEA, Eurostat, Commission documents; retrieved or read 6 Oct 2026).", fontsize=7, color=GREY,
            transform=ax.get_yaxis_transform())
    fig.savefig(OUT / "fig2_shares.png", bbox_inches="tight", facecolor="white")


def fig3():
    """Change since 2005: ESR transport and road only, with the report's Table A8.1 values."""
    cf = list(csv.DictReader(open(D / "commission_figures.csv")))
    tab = {int(r["year"]): float(r["value"]) for r in cf
           if r["document"].startswith("2026 Country") and r["item"] == "Table A8.1 domestic road transport vs base year"}
    old = [float(r["value"]) for r in cf if r["document"].startswith("2025 Country")
           and r["item"] == "Table A7.1 domestic road transport vs base year"][0]
    yrs = list(range(2005, 2025))
    fig, ax = plt.subplots(figsize=(9.6, 4.3), dpi=220)
    ax.axhline(0, color=GREY, lw=0.7)
    ax.plot(yrs, [100 * (T[y] / T[2005] - 1) for y in yrs], color=GREEN, lw=2.4,
            label="ESR transport: all domestic transport, aviation CO2 excluded (2026 inventory)")
    ax.plot(yrs, [100 * (R[y] / R[2005] - 1) for y in yrs], color=GREY, lw=1.8, ls="--",
            label="Road transport only (1.A.3.b)")
    ax.scatter(list(tab), list(tab.values()), s=46, color=AMBER, edgecolor=SLATE, lw=0.6, zorder=4,
               label="Report’s Table A8.1, row ‘domestic road transport’")
    ax.scatter([2023], [old], s=46, facecolor="white", edgecolor=RED, lw=1.6, zorder=5,
               label="2023 as approximated in the 2025 report")
    t24, r24 = 100 * (T[2024] / T[2005] - 1), 100 * (R[2024] / R[2005] - 1)
    ax.text(2024.4, t24 + 1.5, f"{t24:+.1f}%", color=GREEN, fontsize=9, fontweight="bold", va="center")
    ax.text(2024.4, tab[2024] - 1.8, f"{tab[2024]:+.1f}%", color=SLATE, fontsize=9, va="center")
    ax.text(2024.4, r24 - 3, f"{r24:+.1f}%", color=GREY, fontsize=9, va="center")
    ax.text(2022.6, old - 3.5, f"{old:+.1f}%", color=RED, fontsize=8.2, ha="center")
    ax.set_xlim(2004.5, 2026.3)
    ax.set_ylim(-12, 62)
    ax.set_xticks(range(2005, 2025, 3))
    ax.set_ylabel("% change since 2005")
    ax.legend(frameon=False, fontsize=7.8, loc="upper left")
    ax.text(2004.5, -26, "Greenhouse gases, CO2 equivalent. Source: Eurostat env_air_gge (2026 inventory, updated 2 Jun "
            "2026; no flags on these rows); Commission 2026 and 2025 Country Reports (Table A8.1).\nThe 2024 Table A8.1 value "
            "rests on the approximated inventory (our recomputation from it: "
            f"{num('Transport change 2005-2024, inventory 2005 and approximated 2024'):+.1f}%). "
            "Retrieved or read 6 Oct 2026.", fontsize=7, color=GREY)
    fig.savefig(OUT / "fig3_change.png", bbox_inches="tight", facecolor="white")


fig1(); fig2(); fig3()
print("figures in", OUT)
