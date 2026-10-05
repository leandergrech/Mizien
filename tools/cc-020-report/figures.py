"""Figures for Claim Check 020, drawn from data/cc-020/ (run calc.py first)."""
import csv, pathlib
from collections import defaultdict
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
D = ROOT / "data" / "cc-020"
S = defaultdict(dict)
for r in csv.DictReader(open(D / "eurostat_noise.csv")):
    S[r["geo"]][int(r["year"])] = float(r["value"])
R23 = {r["geo"]: float(r["value_2023_pct"]) for r in csv.DictReader(open(D / "eurostat_noise_2023_eu27.csv"))}


def fig1():
    fig, ax = plt.subplots(figsize=(9.6, 4.0), dpi=220)
    for geo, col, lab, ls in (("MT", GREEN, "Malta", "-"), ("EU27_2020", BLUE, "EU-27", "--")):
        s = S[geo]
        xs = sorted(s)
        ax.plot(xs, [s[y] for y in xs], color=col, lw=2.4, ls=ls, marker="o", ms=3.5, label=lab)
        ax.text(2023.3, s[2023], f"{s[2023]:.1f}%", color=col, fontsize=9, va="center", fontweight="bold")
    ax.axhline(13, color=AMBER, lw=1.4, ls=":")
    ax.text(2005.2, 13.8, "Malta: 13% of people modelled above the END 55 dB reporting threshold (EEA, via the study)",
            fontsize=8, color=ORANGE)
    ax.set_ylim(0, 36)
    ax.set_xlim(2004.6, 2025)
    ax.set_xticks(range(2005, 2024, 2))
    ax.set_ylabel("% of population")
    ax.legend(frameon=False, fontsize=9, loc="upper left")
    ax.text(2004.7, -6.2, "Share reporting noise from neighbours or from the street. Source: Eurostat ilc_mddw01 (EU-SILC), "
            "retrieved 5 Oct 2026. Self-reported, all noise sources. No values for 2021–2022; EU-27 from 2010.",
            fontsize=7, color=GREY)
    fig.savefig(OUT / "fig1_noise_trend.png", bbox_inches="tight", facecolor="white")


def fig2():
    fig, ax = plt.subplots(figsize=(9.6, 3.9), dpi=220)
    items = sorted(R23.items(), key=lambda kv: -kv[1])
    ax.bar([k for k, _ in items], [v for _, v in items], color=[GREEN if k == "MT" else SAGE for k, _ in items],
           width=0.72)
    for i, (k, v) in enumerate(items):
        ax.text(i, v + 0.5, f"{v:.0f}" if k != "MT" else f"{v:.1f}", ha="center", fontsize=7.5,
                color=GREEN if k == "MT" else SLATE, fontweight="bold" if k == "MT" else "normal")
    ax.axhline(18.1, color=BLUE, lw=1.4, ls="--")
    ax.text(26.4, 18.8, "EU-27 18.1%", color=BLUE, fontsize=8.5, ha="right")
    ax.set_ylim(0, 36)
    ax.set_ylabel("% of population")
    ax.tick_params(axis="x", labelsize=8)
    ax.text(-0.5, -6.5, "Eurostat ilc_mddw01, 2023, retrieved 5 Oct 2026.", fontsize=7, color=GREY)
    fig.savefig(OUT / "fig2_noise_rank.png", bbox_inches="tight", facecolor="white")


def fig3():
    fig, ax = plt.subplots(figsize=(9.6, 3.2), dpi=220)
    lab = ["Road, Lden", "Road, Lnight", "Aircraft, Lden", "Aircraft, Lnight"]
    who = [53, 45, 45, 40]
    end = [55, 50, 55, 50]
    y = range(len(lab))
    ax.barh([i + 0.2 for i in y], end, height=0.36, color=AMBER, label="Directive reporting threshold (END)")
    ax.barh([i - 0.2 for i in y], who, height=0.36, color=GREEN, label="WHO 2018 guideline level")
    for i in y:
        ax.text(end[i] + 0.3, i + 0.2, f"{end[i]} dB", va="center", fontsize=8.5, color=SLATE)
        ax.text(who[i] + 0.3, i - 0.2, f"{who[i]} dB", va="center", fontsize=8.5, color=GREEN, fontweight="bold")
    ax.set_yticks(list(y)); ax.set_yticklabels(lab); ax.invert_yaxis()
    ax.set_xlim(30, 62)
    ax.set_xlabel("Decibels (axis starts at 30 dB)")
    ax.legend(frameon=False, fontsize=8.5, loc="lower right")
    fig.savefig(OUT / "fig3_thresholds.png", bbox_inches="tight", facecolor="white")


fig1(); fig2(); fig3()
print("figures in", OUT)
