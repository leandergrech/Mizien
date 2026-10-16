"""Figures for Claim Check 123, drawn from data/cc-123/ (run calc.py first)."""
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


def fig1():
    pa = {int(r["year"]): int(r["approved_units_total"])
          for r in csv.DictReader(open(ROOT / "data" / "cc-013" / "pa_approved_dwellings.csv")) if int(r["year"]) >= 2015}
    ys = sorted(pa)
    fig, ax = plt.subplots(figsize=(9.6, 4.0), dpi=220)
    cols = [AMBER if y in (2023, 2024) else (GREEN if y == 2025 else SAGE) for y in ys]
    ax.bar(ys, [pa[y] for y in ys], color=cols, width=0.68)
    for y in ys:
        ax.text(y, pa[y] + 180, f"{pa[y]:,}", ha="center", fontsize=7.6, color=SLATE,
                fontweight="bold" if y in (2023, 2024, 2025) else "normal")
    ax.set_xticks(ys)
    ax.set_ylabel("Dwelling units approved in the year")
    ax.set_ylim(0, 14500)
    ax.text(2014.4, -2500, "Planning Authority, Approved Dwelling Units 2007–2025 (transcribed in data/cc-013, 3 Oct 2026). "
            "Amber: the 2023 base and the 2024 figure KPMG quotes (+7.4%);\ngreen: 2025.",
            fontsize=7, color=GREY, va="top")
    fig.savefig(OUT / "fig1_annual.png", bbox_inches="tight", facecolor="white")
    plt.close(fig)


def fig2():
    rows = list(csv.DictReader(open(ROOT / "data" / "cc-123" / "nso_quarterly_secondhand.csv")))
    labels = [f"{r['quarter']}\n{r['year']}" for r in rows]
    dw = [int(r["dwellings"]) for r in rows]
    pm = [int(r["permits"]) for r in rows]
    x = list(range(len(rows)))
    fig, ax = plt.subplots(figsize=(9.6, 4.0), dpi=220)
    cols = [GREEN if (r["year"] == "2025" and r["quarter"] in ("Q1", "Q2")) else SAGE for r in rows]
    ax.bar(x, dw, color=cols, width=0.66, label="New dwellings approved")
    ax.bar(x, pm, color=AMBER, width=0.34, label="Building permits (count)")
    for i in x:
        ax.text(i, dw[i] + 60, f"{dw[i]:,}", ha="center", fontsize=7.6, color=SLATE)
        ax.text(i, pm[i] + 60, f"{pm[i]}", ha="center", fontsize=7, color=SLATE)
    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontsize=8)
    ax.set_ylim(0, 4400)
    ax.set_ylabel("Number")
    ax.legend(frameon=False, fontsize=8, loc="upper left")
    ax.text(-0.5, -1050, "NSO quarterly Residential Building Permits releases, as reported in search summaries and one outlet article "
            "(second-hand; nso.gov.mt refuses scripts).\nDark green: January–June 2025, whose two quarters sum to 5,170 dwellings: "
            "the number KPMG calls “permits”.", fontsize=7, color=GREY, va="top")
    fig.savefig(OUT / "fig2_quarters.png", bbox_inches="tight", facecolor="white")
    plt.close(fig)


fig1()
fig2()
print("figures in", OUT)
