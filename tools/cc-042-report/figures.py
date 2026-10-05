"""Figures for Claim Check 042 (run calc.py first)."""
import csv
import datetime as dt
import pathlib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
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
GREEN, AMBER, RED, SLATE, GREY, BLUE, LG = "#14452F", "#E3A72F", "#B5483A", "#2B3A42", "#8A9399", "#3C6E8F", "#8DB36B"
D = dt.date


def fig1():
    fig, axs = plt.subplots(1, 2, figsize=(9.6, 3.9), dpi=220, gridspec_kw={"width_ratios": [1.25, 1]})
    ax = axs[0]
    # (label, start, end, colour, note)
    ev = [("Qui-si-Sana, Sliema\n(private drain, sewage)", D(2025, 6, 18), D(2025, 6, 24), RED),
          ("Xlendi Bay\n(field run-off after rain)", D(2025, 6, 22), D(2025, 6, 30), GREY),
          ("Fajtata Bay, Marsaskala\n(public-toilet overflow)", D(2025, 6, 30), D(2025, 7, 2), RED)]
    for i, (lab, a, b, c) in enumerate(ev):
        ax.barh(i, (b - a).days, left=mdates.date2num(a), color=c, height=0.5)
        ax.text(mdates.date2num(b) + 0.4, i + 0.32, f"{(b - a).days} days", va="center", fontsize=8, color=SLATE)
    ax.set_yticks(range(3)); ax.set_yticklabels([e[0] for e in ev], fontsize=8); ax.invert_yaxis()
    ax.axvline(mdates.date2num(D(2025, 6, 28)), color=BLUE, lw=1.2, ls="--")
    ax.text(mdates.date2num(D(2025, 6, 28)) - 0.3, 2.62, "28 Jun: 13 Blue Flags\nannounced", color=BLUE, fontsize=7.6, ha="right", va="bottom")
    ax.axvline(mdates.date2num(D(2025, 7, 1)), color=AMBER, lw=1.2, ls="--")
    ax.text(mdates.date2num(D(2025, 7, 1)) + 0.3, -0.45, "1 Jul: PN\nstatement", color="#9A6D0B", fontsize=7.6, ha="left", va="top")
    ax.xaxis_date(); ax.xaxis.set_major_formatter(mdates.DateFormatter("%d %b")); ax.xaxis.set_major_locator(mdates.DayLocator(interval=4))
    ax.set_xlim(mdates.date2num(D(2025, 6, 16)), mdates.date2num(D(2025, 7, 5))); ax.set_ylim(3.0, -0.8)
    ax.tick_params(axis="x", labelsize=8)
    ax.set_title("Bathing-water warnings, June-July 2025 (news reports of EHD notices)", fontsize=9, color=SLATE, loc="left")
    ax = axs[1]
    rows = list(csv.DictReader(open(ROOT / "data/cc-042/eea_mt_classification.csv")))
    ys = [int(r["season"]) for r in rows]
    cols = [("excellent", GREEN, "Excellent"), ("good", LG, "Good"), ("sufficient", AMBER, "Sufficient"), ("poor", RED, "Poor")]
    bottom = [0] * len(rows)
    for k, c, lab in cols:
        v = [int(r[k]) for r in rows]
        ax.bar(ys, v, bottom=bottom, color=c, label=lab, width=0.8)
        bottom = [b + x for b, x in zip(bottom, v)]
    ax.set_ylim(0, 87); ax.set_xticks(ys[::2]); ax.tick_params(axis="x", labelsize=8)
    ax.set_ylabel("Bathing waters (of 87)")
    e25 = int(rows[-1]["excellent"])
    ax.text(2025, 40, f"{e25}", ha="center", fontsize=9, color="white", fontweight="bold")
    ax.legend(fontsize=7, ncol=4, loc="lower center", bbox_to_anchor=(0.5, -0.2), frameon=False, handlelength=1, columnspacing=1)
    ax.set_title("EEA class of Malta's 87 bathing waters", fontsize=9, color=SLATE, loc="left")
    fig.text(0.01, -0.07, "Sources: Environmental Health Directorate notices as reported by MaltaToday, Malta Independent, Lovin Malta (dates: see data/cc-042/events_2025.csv); "
             "EEA bathing-water data, retrieved 5 Oct 2026.", fontsize=7, color=GREY)
    fig.tight_layout(); fig.savefig(OUT / "fig1_events.png", bbox_inches="tight", facecolor="white")


if __name__ == "__main__":
    fig1()
