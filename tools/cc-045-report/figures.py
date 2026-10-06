"""Figures for Claim Check 045, drawn from data/cc-045/ (run calc.py first)."""
import csv, pathlib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from matplotlib.patches import Patch
from matplotlib.lines import Line2D

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[1]
OUT = HERE / "out"
OUT.mkdir(exist_ok=True)
for f in ["LiberationSans-Regular", "LiberationSans-Bold", "LiberationSans-Italic"]:
    fm.fontManager.addfont(f"/usr/share/fonts/truetype/liberation/{f}.ttf")
plt.rcParams.update({"font.family": "Liberation Sans", "axes.spines.top": False, "axes.spines.right": False,
                     "axes.edgecolor": "#8A9399", "axes.labelcolor": "#2B3A42", "xtick.color": "#2B3A42",
                     "ytick.color": "#2B3A42", "xtick.labelsize": 9, "ytick.labelsize": 9, "hatch.linewidth": 1.2})
GREEN, SAGE, AMBER, RED, SLATE, GREY, ORANGE, BLUE = ("#14452F", "#7FA88B", "#E3A72F", "#B5483A", "#2B3A42",
                                                      "#8A9399", "#D9772B", "#3C6E8F")
D = ROOT / "data" / "cc-045"


def title(ax, t, y=1.06):
    ax.set_title(t, fontsize=10.5, color=GREEN, loc="left", fontweight="bold", y=y)


def fig1():
    fig, ax = plt.subplots(figsize=(9.6, 3.3), dpi=220)
    ax.barh([1], [16], color=GREEN, height=0.5, label="In use (Public Works Department, 4 Jul 2025)")
    ax.barh([1], [4], left=16, color="white", edgecolor=ORANGE, hatch="////", height=0.5,
            label="Planned: a further 4 km")
    ax.barh([0], [16], color=SAGE, height=0.5, label="Lovin Malta, 15 Sep 2020 (outlet's statement)")
    ax.text(8, 1, "16 km", ha="center", va="center", color="white", fontweight="bold", fontsize=10)
    ax.text(18, 1, "+4 km", ha="center", va="center", color=ORANGE, fontweight="bold", fontsize=10,
            bbox=dict(facecolor="white", edgecolor="none", pad=1.5))
    ax.text(16.3, 0, "16 km", va="center", color=SLATE, fontsize=9)
    ax.axvline(20, color=RED, lw=1.2, ls="--")
    ax.text(20.2, 1.42, "20 km: planned total", color=RED, fontsize=8.5, va="center")
    ax.set_yticks([1, 0]); ax.set_yticklabels(["Department:\nin use and planned", "Press, 2020:\n'some 16 km'"], fontsize=9)
    ax.set_xlim(0, 24); ax.set_ylim(-0.5, 1.7)
    ax.set_xlabel("Kilometres of tunnels, canals and culverts", fontsize=9)
    ax.legend(frameon=False, fontsize=8, loc="upper center", bbox_to_anchor=(0.45, -0.28), ncol=2)
    title(ax, "The 20 km is the department's planned total; 16 km is described as in use")
    fig.savefig(OUT / "fig1_lengths.png", bbox_inches="tight", facecolor="white")
    plt.close(fig)


def fig2():
    A = list(csv.DictReader(open(D / "luqa_annual.csv", encoding="utf-8")))
    C = {r["check"]: r["value"] for r in csv.DictReader(open(D / "checks.csv", encoding="utf-8"))}
    five = float(C["Empirical 5-year daily rainfall at Luqa (Weibull)"])
    fig, ax = plt.subplots(figsize=(9.6, 4.2), dpi=220)
    for r in A:
        y, v, ok = int(r["year"]), float(r["max_day_mm"]), r["complete"] == "1"
        if ok:
            ax.bar(y, v, color=GREEN, width=0.7, zorder=2)
        else:
            ax.bar(y, v, color="white", edgecolor=GREY, hatch="////", width=0.7, zorder=2)
    ax.axhline(five, color=RED, lw=1.1, ls="--")
    ax.text(1990.2, five + 3, f"empirical 5-year daily rainfall at Luqa: {five:.0f} mm", color=RED, fontsize=8.5,
            bbox=dict(facecolor="white", edgecolor="none", pad=1.5), zorder=5)
    ax.axvline(2014.5, color=GREY, lw=0.8, ls=":")
    ax.text(2014.7, 188, "Project works\nfinished 2014", fontsize=8, color=GREY, va="top")
    ax.annotate("14 Sep 2020: 20 mm at Luqa on\nthe day of reported flooding", xy=(2020, 20), xytext=(2015.6, 140),
                fontsize=8, color=SLATE, arrowprops=dict(arrowstyle="->", color=SLATE, lw=0.8))
    ax.set_xlim(1989.3, 2025.7); ax.set_ylim(0, 190)
    ax.set_xticks(range(1990, 2026, 5))
    ax.set_ylabel("Largest daily total (mm)", fontsize=9)
    ax.legend(handles=[Patch(facecolor=GREEN, label="Year with at least 330 daily readings"),
                       Patch(facecolor="white", edgecolor=GREY, hatch="////", label="Year with gaps: maximum may be understated")],
              frameon=False, fontsize=8, loc="upper center", bbox_to_anchor=(0.5, 1.0))
    title(ax, "One gauge, 36 years: it cannot show whether the tunnels reduced flooding")
    ax.text(1989.4, -52, "Source: NOAA NCEI GHCN-Daily, Luqa (MT000016597), daily precipitation, retrieved 6 Oct 2026. Return level: empirical "
            "(Weibull), 25 complete years.\nA single gauge about 6 km from the Birkirkara tunnel; the project's design storm is "
            "defined for each catchment, so the line is context, not a test.", fontsize=8, color=GREY, va="top")
    fig.savefig(OUT / "fig2_luqa_rain.png", bbox_inches="tight", facecolor="white")
    plt.close(fig)


fig1(); fig2()
print("ok")
