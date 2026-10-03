"""Figures for Claim Check 014, drawn from data/cc-014/ (run calc.py first)."""
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
S = list(csv.DictReader(open(ROOT / "data" / "cc-014" / "pa_enforcement_series.csv", encoding="utf-8")))


def fig1():
    fig, ax = plt.subplots(figsize=(9.6, 4.6), dpi=220)
    ny = [(int(r["year"]), int(r["enforcement_notices"])) for r in S if r["enforcement_notices"]]
    ky = [(int(r["year"]), int(r["complaints"])) for r in S if r["complaints"]]
    second = {int(r["year"]) for r in S if "Second-hand" in r["access_note"]}
    ax.bar([y for y, _ in ny], [n for _, n in ny], color=[SAGE if y in second else GREEN for y, _ in ny],
           width=0.7, label="Enforcement notices issued")
    ax.plot([y for y, _ in ky], [k for _, k in ky], "o", color=ORANGE, ms=7, label="Complaints of illegal development")
    for y, k in ky:
        ax.text(y, k + 110, f"{k:,}", ha="center", fontsize=7.5, color=ORANGE, fontweight="bold")
    for y, n in ny:
        ax.text(y, n + 40, f"{n:,}", ha="center", fontsize=7, color=SLATE)
    ax.axhline(1000, color=GREY, lw=0.6, ls=":")
    ax.text(2024.6, 1040, "1,000 a year", ha="right", fontsize=7.5, color=GREY)
    ax.axvspan(2011.6, 2018.4, color="#EEF1EE", zorder=0)
    ax.text(2015, 2600, "no readable\nsource found", ha="center", fontsize=7.5, color=GREY, style="italic")
    ax.set_xlim(2000.3, 2024.7)
    ax.set_ylim(0, 4100)
    ax.set_xticks(range(2001, 2025, 2))
    ax.set_ylabel("Number per year")
    ax.legend(frameon=False, fontsize=8, loc="upper right")
    ax.text(2000.4, -620, "Dark bars and 2001-2011, 2024: MEPA/PA annual reports (read). Light bars 2019-2023: reports of PA "
            "data and parliamentary answers (second-hand; 2019 derived). 2005 complaints: financial year 2004/05; "
            "2011: sites without an existing notice.", fontsize=6.6, color=GREY, wrap=True)
    fig.savefig(OUT / "fig1_series.png", bbox_inches="tight", facecolor="white")


def fig2():
    fig, ax = plt.subplots(figsize=(9.6, 2.2), dpi=220)
    parts = [("Sanctioning\napplication", 521, BLUE), ("Removed by\nowner", 482, SAGE), ("Resolved after\npersuasion", 87, AMBER),
             ("Enforcement\nnotice", 162, RED)]
    left = 0
    for name, n, col in parts:
        ax.barh([0], [n], left=left, color=col, height=0.5)
        ax.text(left + n / 2, 0, f"{n}", ha="center", va="center", color="white", fontsize=10, fontweight="bold")
        ax.text(left + n / 2, 0.32 if n > 150 else -0.32, name, ha="center", va="bottom" if n > 150 else "top",
                fontsize=8, color=SLATE)
        left += n
    ax.text(left + 15, 0, f"{left:,} cases in the four\noutcomes the PA reports", va="center", fontsize=8.5, color=SLATE)
    ax.set_xlim(0, 1600)
    ax.set_ylim(-0.75, 0.75)
    ax.axis("off")
    ax.set_title("What happened to 2,411 complaints in 2024 (about half confirmed as illegal development)",
                 fontsize=9.5, color=GREEN, loc="left", fontweight="bold")
    ax.text(0, -0.85, "Source: Planning Authority Annual Report 2024, pp. 28-30. The four "
            "categories are reported separately and may overlap.", fontsize=7, color=GREY)
    fig.savefig(OUT / "fig2_outcomes.png", bbox_inches="tight", facecolor="white")


fig1()
fig2()
print("figures in", OUT)
