"""Figures for Claim Check 119, drawn from data/cc-119/ (run fetch.py and calc.py first)."""
import csv, pathlib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm

HERE = pathlib.Path(__file__).resolve().parent
D = HERE.parents[1] / "data" / "cc-119"
OUT = HERE / "out"; OUT.mkdir(exist_ok=True)
for f in ["LiberationSans-Regular", "LiberationSans-Bold", "LiberationSans-Italic"]:
    fm.fontManager.addfont(f"/usr/share/fonts/truetype/liberation/{f}.ttf")
plt.rcParams.update({"font.family": "Liberation Sans", "axes.spines.top": False, "axes.spines.right": False,
                     "axes.edgecolor": "#8A9399", "axes.labelcolor": "#2B3A42", "xtick.color": "#2B3A42", "ytick.color": "#2B3A42"})
GREEN, SAGE, AMBER, RED, SLATE, GREY, ORANGE, BLUE = ("#14452F", "#7FA88B", "#E3A72F", "#B5483A", "#2B3A42", "#8A9399", "#D9772B", "#3C6E8F")
V = {}
for r in csv.DictReader(open(D / "eurostat_extract.csv")):
    V[(r["dataset"], r["geo"], r["item"], r["year"])] = float(r["value"])
rk = list(csv.DictReader(open(D / "ranking_2024_2025.csv")))


def fig_measures():
    """Malta's 2025 'electricity' figure on the three bases, with the EU-27 on the same bases."""
    labs = ["Renewables in domestic\nnet generation (2025)", "Renewables vs final electricity\nconsumption, simple ratio (2025)",
            "Eurostat SHARES indicator,\nrenewable electricity (2025, prov.)"]
    mt = [16.69, 12.2, 11.2]; eu = [47.3, None, 49.9]
    fig, ax = plt.subplots(figsize=(9.6, 3.6), dpi=220)
    xs = range(3)
    ax.bar([x - 0.2 for x in xs], mt, 0.4, color=GREEN, label="Malta")
    ax.bar([x + 0.2 for x in xs if eu[x]] if False else [x + 0.2 for x in xs if eu[x]], [e for e in eu if e], 0.4, color=BLUE, label="EU-27")
    for x, m in zip(xs, mt): ax.text(x - 0.2, m + 1, f"{m:.1f}%", ha="center", fontsize=9, fontweight="bold", color=GREEN)
    for x, e in zip(xs, eu):
        if e: ax.text(x + 0.2, e + 1, f"{e:.1f}%", ha="center", fontsize=9, color=BLUE)
    ax.text(1.2, 3, "not computed\nfor the EU-27", ha="center", fontsize=7.5, color=GREY)
    ax.axhline(16.7, color=AMBER, lw=1, ls="--"); ax.text(1.2, 18.4, "Council: 16.7%", fontsize=8, color="#8a5d00", ha="center")
    ax.set_xticks(list(xs)); ax.set_xticklabels(labs, fontsize=8); ax.set_ylim(0, 60); ax.set_ylabel("% of electricity")
    ax.legend(frameon=False, fontsize=8, loc="upper left")
    fig.text(0.01, -0.03, "Source: Eurostat nrg_cb_pem, nrg_cb_e, nrg_ind_ren (retrieved 12 Oct 2026). 2025 values are Eurostat early estimates.", fontsize=7, color=GREY)
    fig.savefig(OUT / "fig_measures.png", bbox_inches="tight", facecolor="white")


def fig_sources():
    yrs = list(range(2013, 2025))
    pv = [V[("nrg_bal_peh", "MT", "GEP|RA420", str(y))] for y in yrs]
    bio = [V[("nrg_bal_peh", "MT", "GEP|R5300", str(y))] for y in yrs]
    wind = [V[("nrg_bal_peh", "MT", "GEP|RA300", str(y))] for y in yrs]
    fig, ax = plt.subplots(figsize=(9.6, 3.6), dpi=220)
    ax.bar(yrs, pv, color=AMBER, label="Solar PV")
    ax.bar(yrs, bio, bottom=pv, color=SAGE, label="Biogas (combustible renewables)")
    ax.bar(yrs, wind, bottom=[a + b for a, b in zip(pv, bio)], color=BLUE, label="Wind (0.03 to 0.09 GWh: invisible at this scale)")
    ax.text(2024, pv[-1] + bio[-1] + 8, "336 GWh", ha="center", fontsize=8.5, fontweight="bold", color=GREEN)
    ax.text(2013, 40, "35 GWh", ha="center", fontsize=8.5, fontweight="bold", color=GREEN)
    ax.set_ylabel("Renewable electricity generated, GWh"); ax.set_xticks(yrs); ax.set_ylim(0, 380)
    ax.legend(frameon=False, fontsize=8, loc="upper left")
    fig.text(0.01, -0.03, "Source: Eurostat nrg_bal_peh (GEP, GWh), retrieved 12 Oct 2026. No hydro recorded in any year.", fontsize=7, color=GREY)
    fig.savefig(OUT / "fig_sources.png", bbox_inches="tight", facecolor="white")


def fig_rank():
    rows = sorted(rk, key=lambda r: float(r["ren_share_gross_final_energy_2024_pc"]))
    fig, ax = plt.subplots(figsize=(9.6, 3.9), dpi=220)
    cols = [GREEN if r["geo"] == "MT" else SAGE for r in rows]
    ax.bar([r["geo"] for r in rows], [float(r["ren_share_gross_final_energy_2024_pc"]) for r in rows], color=cols)
    ax.axhline(V[("nrg_ind_ren", "EU27_2020", "REN", "2024")], color=BLUE, ls="--", lw=1.4)
    ax.text(26.4, V[("nrg_ind_ren", "EU27_2020", "REN", "2024")] + 1, "EU-27 25.2%", color=BLUE, fontsize=8.5, ha="right")
    ax.text(3, 17.21 + 1, "Malta 17.2%", color=GREEN, fontsize=8.5, fontweight="bold", ha="center")
    ax.set_ylabel("Renewables, % of gross final energy consumption, 2024"); ax.tick_params(axis="x", labelsize=8)
    fig.text(0.01, -0.03, "Source: Eurostat nrg_ind_ren (REN, 2024), retrieved 12 Oct 2026.", fontsize=7, color=GREY)
    fig.savefig(OUT / "fig_rank.png", bbox_inches="tight", facecolor="white")


fig_measures(); fig_sources(); fig_rank()
print("ok")
