"""Figures for Claim Check 158 (run calc.py first)."""
import csv, pathlib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[1]
D = ROOT / "data/cc-158"
OUT = HERE / "out"; OUT.mkdir(exist_ok=True)
for f in ["LiberationSans-Regular", "LiberationSans-Bold", "LiberationSans-Italic"]:
    fm.fontManager.addfont(f"/usr/share/fonts/truetype/liberation/{f}.ttf")
plt.rcParams.update({"font.family": "Liberation Sans", "axes.spines.top": False, "axes.spines.right": False,
                     "axes.edgecolor": "#8A9399", "axes.labelcolor": "#2B3A42", "xtick.color": "#2B3A42",
                     "ytick.color": "#2B3A42"})
GREEN, AMBER, RED, SLATE, GREY, PALE = "#14452F", "#E3A72F", "#B5483A", "#2B3A42", "#8A9399", "#C9D3CC"
AXC = {"Governance": GREEN, "Public Policies": AMBER, "Finance": SLATE}


def fig1():
    comp = [r for r in csv.DictReader(open(D / "components.csv")) if r["nao_score"]]
    comp = comp[::-1]
    fig, ax = plt.subplots(figsize=(9.6, 5.4), dpi=220)
    ax.axvspan(6.66, 10.4, color="#EEF3EF", zorder=0)
    ax.axvspan(0, 3.33, color="#F6E9E6", zorder=0)
    ax.barh([f"{r['component']} {r['name']}" for r in comp], [float(r["nao_score"]) for r in comp],
            color=[AXC[r["axis"]] for r in comp], zorder=2)
    for y, r in enumerate(comp):
        ax.text(float(r["nao_score"]) + 0.1, y, f"{float(r['nao_score']):.2f}", va="center", fontsize=7.5, color=SLATE)
    for x in (3.33, 6.66):
        ax.axvline(x, color=GREY, lw=0.8, ls=":", zorder=1)
    ax.text(6.72, len(comp) - 0.35, "≥ 6.66: “strength”", fontsize=7.5, color=GREEN)
    ax.text(0.1, len(comp) - 0.35, "≤ 3.33: “challenge”", fontsize=7.5, color=RED)
    ax.set_xlim(0, 10.9); ax.set_xlabel("Component score (0–10)"); ax.tick_params(axis="y", labelsize=7.5)
    for a, c in AXC.items():
        ax.barh([0], [0], color=c, label=a)
    ax.legend(fontsize=7.5, frameon=False, loc="center right", bbox_to_anchor=(1.0, 0.6))
    fig.text(0.01, -0.04, "Source: NAO, A review of Malta’s climate action using the ClimateScanner framework (Oct 2025), "
             "Appendix; F3 not applicable. Thresholds: ClimateScanner Handbook (May 2024), p. 11.", fontsize=7, color=GREY)
    fig.savefig(OUT / "fig1_components.png", bbox_inches="tight", facecolor="white")


def fig2():
    esr = {int(r["year"]): float(r["value"]) * 1000 for r in csv.DictReader(open(ROOT / "data/cc-094/eea_esr_emissions.csv"))
           if r["country"] == "Malta" and r["series"] in ("ESD", "ESR")}
    leg = {int(r["year"]): float(r["value"]) / 1000 for r in csv.DictReader(open(ROOT / "data/cc-094/esr_legal_inputs.csv"))
           if r["country"] == "MT" and r["item"] == "Annual emission allocation"}
    base = 1020.601
    ys = list(range(2005, 2025))
    fig, ax = plt.subplots(figsize=(9.6, 3.5), dpi=220)
    ax.plot(ys, [esr[y] for y in ys], color=RED, lw=2, marker="o", ms=3, label="Malta effort-sharing emissions (EEA)")
    ly = [y for y in sorted(leg) if y >= 2022]
    ax.plot(ly, [leg[y] for y in ly], color=GREEN, lw=1.6, ls="--", label="Annual limit (allocation), 2022–2030")
    ax.axhline(base, color=GREY, lw=0.8, ls=":"); ax.text(2013.2, base - 45, "2005 level (legal base) 1,021 kt", fontsize=7.5, color=GREY)
    ax.scatter([2030], [leg[2030]], color=GREEN, zorder=3); ax.text(2029.4, leg[2030] - 70, "2030: 827 kt (−19%)", fontsize=7.5, color=GREEN, ha="center")
    ax.annotate("2024: 1,437 kt\n(+41% on 2005)", (2024, esr[2024]), xytext=(2025.2, 1500), fontsize=7.5, color=RED,
                arrowprops=dict(arrowstyle="-", color=RED, lw=0.6))
    ax.set_xlim(2004.5, 2031); ax.set_ylim(650, 1650); ax.set_ylabel("kt CO₂e")
    ax.legend(fontsize=7.5, frameon=False, loc="upper left")
    fig.text(0.01, -0.07, "Sources: EEA GHG_ESD-ESR_2025 (2005–12 EEA estimate; 2013–20 ESD review; 2021–23 ESR review; 2024 "
             "approximated); allocations: Implementing Decision (EU) 2026/895. Data saved for CC-094 (retrieved 6 Oct 2026).",
             fontsize=7, color=GREY)
    fig.savefig(OUT / "fig2_outcomes.png", bbox_inches="tight", facecolor="white")


if __name__ == "__main__":
    fig1(); fig2()
