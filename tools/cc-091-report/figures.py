"""Figures for Claim Check 091, drawn from data/cc-091/ (run fetch.py first)."""
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
GREEN, AMBER, RED, SLATE, GREY, BLUE = "#14452F", "#E3A72F", "#B5483A", "#2B3A42", "#8A9399", "#3C6E8F"
o = {(r["item"], int(r["year"])): float(r["value"]) for r in csv.DictReader(open(ROOT / "data/cc-091/ohsa_annual_reports.csv"))}


def fig1():
    fig, axs = plt.subplots(1, 2, figsize=(9.6, 3.9), dpi=220, gridspec_kw={"width_ratios": [1.5, 1]})
    ax = axs[0]
    ys = list(range(2021, 2026))
    vals = [o[("Inspections (total)", y)] for y in ys]
    ax.bar(ys, vals, color=[GREY] * 4 + [GREEN], width=0.65)
    for y, v in zip(ys, vals):
        ax.text(y, v + 400, f"{v:,.0f}", ha="center", fontsize=8.5, color=GREEN if y == 2025 else SLATE, fontweight="bold" if y == 2025 else None)
    ax.annotate("x2.53", (2025, 23711), xytext=(2023.6, 21500), color=GREEN, fontsize=9, fontweight="bold")
    ax.set_title("OHSA inspections per year", fontsize=10, color=SLATE, loc="left")
    ax.set_xticks(ys); ax.set_ylim(0, 27500)
    ax = axs[1]
    ys = [2023, 2024, 2025]
    d = [o[("Fatal accidents at place of work", 2023)], o[("Fatal accidents investigated", 2024)], o[("Accident investigations: fatal", 2025)]]
    ax.bar(ys, d, color=[GREY, GREY, RED], width=0.6)
    for y, v in zip(ys, d):
        ax.text(y, v + 0.2, f"{v:.0f}", ha="center", fontsize=9, color=SLATE, fontweight="bold")
    ax.set_title("Workplace deaths investigated by OHSA", fontsize=10, color=SLATE, loc="left")
    ax.set_xticks(ys); ax.set_ylim(0, 11)
    fig.text(0.01, -0.03, "Source: OHSA Annual Reports 2023, 2024 and 2025 (Table 14; fatal accident sections), transcribed in data/cc-091/.", fontsize=7, color=GREY)
    fig.tight_layout()
    fig.savefig(OUT / "fig1_inspections_deaths.png", bbox_inches="tight", facecolor="white")


def fig2():
    fig, axs = plt.subplots(1, 2, figsize=(9.6, 3.6), dpi=220, gridspec_kw={"width_ratios": [1, 1.3]})
    ax = axs[0]
    parts = [("Adequate compliance", 74, GREEN), ("Orders issued", 21, AMBER), ("Stop-work orders", 5, RED)]
    left = 0
    for lab, v, c in parts:
        ax.barh([0], [v], left=left, color=c, height=0.5)
        ax.text(left + v / 2, 0, f"{v}%", ha="center", va="center", color="white" if c != AMBER else SLATE, fontsize=9, fontweight="bold")
        left += v
    ax.set_yticks([]); ax.set_xlim(0, 100); ax.set_ylim(-0.6, 1.2)
    ax.set_title("Construction inspections, 2025 (OHSA Table 6)", fontsize=10, color=SLATE, loc="left")
    for i, (lab, v, c) in enumerate(parts):
        ax.text(0, 0.62 + 0 * i, "", fontsize=8)
    ax.legend(handles=[plt.Rectangle((0, 0), 1, 1, color=c) for _, _, c in parts], labels=[p[0] for p in parts], frameon=False, fontsize=8, loc="upper center", ncol=3, bbox_to_anchor=(0.5, -0.05))
    ax = axs[1]
    items = [("Safe use of lifting machinery", 65), ("Safe use of scaffolds", 76), ("Protection against falls", 77), ("Housekeeping", 88), ("Fire safety precautions", 94), ("Safe access to site", 96)]
    ax.barh([n for n, _ in items], [v for _, v in items], color=[RED, AMBER, AMBER, "#C9D3CC", "#C9D3CC", "#C9D3CC"])
    for i, (n, v) in enumerate(items):
        ax.text(v + 1, i, f"{v}%", va="center", fontsize=8.5, color=SLATE)
    ax.set_xlim(0, 110); ax.tick_params(axis="y", labelsize=8)
    ax.set_title("Share of applicable sites adequate, by feature (Table 9)", fontsize=10, color=SLATE, loc="left")
    fig.text(0.01, -0.06, "Source: OHSA Annual Report 2025, pp. 42-43. Six of the eleven features in Table 9 are shown (the three lowest and three others).", fontsize=7, color=GREY)
    fig.tight_layout()
    fig.savefig(OUT / "fig2_construction.png", bbox_inches="tight", facecolor="white")


if __name__ == "__main__":
    fig1(); fig2()
