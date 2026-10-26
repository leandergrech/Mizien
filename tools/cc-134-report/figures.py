"""Figures for Claim Check 134 (data/cc-134/eurostat_envtax_gdp.csv; Eurostat env_ac_tax, PC_GDP)."""
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
                     "axes.edgecolor": "#8A9399"})
GREEN, AMBER, BLUE, SLATE, GREY = "#14452F", "#E3A72F", "#3F6E8F", "#2B3A42", "#8A9399"
ROWS = list(csv.DictReader(open(ROOT / "data" / "cc-134" / "eurostat_envtax_gdp.csv", encoding="utf-8")))
V = {(r["geo"], r["item"], r["unit"], int(r["year"])): float(r["value"]) for r in ROWS if r["dataset"] == "env_ac_tax"}
MS = "BE BG CZ DK DE EE IE EL ES FR HR IT CY LV LT LU HU MT NL AT PL PT RO SI SK FI SE".split()


def fig1():
    ys = list(range(2015, 2025))
    fig, ax = plt.subplots(figsize=(9.2, 3.6), dpi=220)
    ax.plot(ys, [V[("MT", "ENV", "PC_GDP", y)] for y in ys], color=GREEN, lw=2.4, marker="o", label="Malta")
    ax.plot(ys, [V[("EU27_2020", "ENV", "PC_GDP", y)] for y in ys], color=AMBER, lw=2.4, marker="o", label="EU-27")
    for g, c, dy in (("MT", GREEN, -0.17), ("EU27_2020", AMBER, 0.08)):
        ax.text(2024.12, V[(g, "ENV", "PC_GDP", 2024)] + dy * 0.4, f"{V[(g, 'ENV', 'PC_GDP', 2024)]:.2f}", fontsize=8.5, color=c, va="center")
    ax.set_ylim(0, 3.1); ax.set_xticks(ys); ax.set_xlim(2014.6, 2024.7)
    ax.set_ylabel("Environmental taxes, % of GDP", fontsize=8.5, color=SLATE)
    ax.tick_params(labelsize=8.5, colors=SLATE)
    ax.legend(frameon=False, fontsize=8.5, loc="lower left")
    ax.text(2014.6, -0.62, "Source: Eurostat env_ac_tax (PC_GDP), retrieved 26 Oct 2026. Total environmental taxes (energy, transport, pollution and resources).",
            fontsize=7, color=GREY, clip_on=False)
    fig.savefig(OUT / "fig1_trend.png", bbox_inches="tight", facecolor="white")


def fig2():
    vals = sorted(MS, key=lambda g: V[(g, "ENV", "PC_GDP", 2024)])
    fig, ax = plt.subplots(figsize=(9.2, 3.9), dpi=220)
    cols = [GREEN if g == "MT" else "#B9C4C9" for g in vals]
    ax.bar(range(27), [V[(g, "ENV", "PC_GDP", 2024)] for g in vals], color=cols, width=0.72)
    ax.axhline(V[("EU27_2020", "ENV", "PC_GDP", 2024)], color=AMBER, lw=1.6, ls="--")
    ax.text(0, V[("EU27_2020", "ENV", "PC_GDP", 2024)] + 0.07, "EU-27 2.08", fontsize=8.5, color="#9A6B00")
    ax.set_xticks(range(27)); ax.set_xticklabels(vals, fontsize=7.5, color=SLATE)
    ax.tick_params(axis="y", labelsize=8.5, colors=SLATE)
    ax.set_ylabel("Environmental taxes, % of GDP, 2024", fontsize=8.5, color=SLATE)
    i = vals.index("MT")
    ax.text(i, V[("MT", "ENV", "PC_GDP", 2024)] + 0.07, "MT 1.35", ha="center", fontsize=8.5, color=GREEN, weight="bold")
    ax.text(0, -0.62, "Source: Eurostat env_ac_tax (PC_GDP), 2024, retrieved 26 Oct 2026. Malta is 25th of 27; only Ireland and Luxembourg are lower.",
            fontsize=7, color=GREY, clip_on=False, transform=ax.get_yaxis_transform())
    fig.savefig(OUT / "fig2_rank.png", bbox_inches="tight", facecolor="white")


if __name__ == "__main__":
    fig1(); fig2()
