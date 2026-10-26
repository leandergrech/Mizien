"""Figures for Claim Check 131 (data/cc-131/eurostat_cdw.csv; Eurostat env_wastrt, W121 non-hazardous)."""
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
GREEN, AMBER, BLUE, SLATE, GREY, RED = "#14452F", "#E3A72F", "#3F6E8F", "#2B3A42", "#8A9399", "#B5452F"
ROWS = list(csv.DictReader(open(ROOT / "data" / "cc-131" / "eurostat_cdw.csv", encoding="utf-8")))
V = {(r["geo"], r["oper"], int(r["year"])): float(r["value"]) for r in ROWS
     if r["dataset"] == "env_wastrt" and r["waste"] == "W121" and r["hazard"] == "NHAZ"}
MS = "BE BG CZ DK DE EE IE EL ES FR HR IT CY LV LT LU HU MT NL AT PL PT RO SI SK FI SE".split()
share = lambda g, op, y: V[(g, op, y)] / V[(g, "TRT", y)] * 100


def fig1():
    ys = [2010, 2012, 2014, 2016, 2018, 2020, 2022]
    rec = [share("MT", "RCV_R", y) for y in ys]
    bf = [share("MT", "RCV_B", y) for y in ys]
    ld = [share("MT", "DSP_L_OTH", y) for y in ys]
    fig, ax = plt.subplots(figsize=(9.2, 3.8), dpi=220)
    x = range(len(ys))
    ax.bar(x, rec, color=GREEN, width=0.62, label="Recycling")
    ax.bar(x, bf, bottom=rec, color=AMBER, width=0.62, label="Backfilling (counted as recovery)")
    ax.bar(x, ld, bottom=[a + b for a, b in zip(rec, bf)], color="#B9C4C9", width=0.62, label="Landfill and other disposal")
    for i, (r, b, l) in enumerate(zip(rec, bf, ld)):
        ax.text(i, r / 2, f"{r:.0f}%", ha="center", va="center", fontsize=8, color="white", weight="bold")
        if b > 6:
            ax.text(i, r + b / 2, f"{b:.0f}%", ha="center", va="center", fontsize=8, color=SLATE)
        if l > 6:
            ax.text(i, r + b + l / 2, f"{l:.0f}%", ha="center", va="center", fontsize=8, color=SLATE)
        ax.text(i, 102, f"{r + b:.0f}", ha="center", fontsize=8.5, color=GREEN, weight="bold")
    ax.text(-0.45, 102, "Recovery\nrate:", ha="right", va="bottom", linespacing=0.9, fontsize=8, color=GREEN)
    ax.set_xticks(list(x)); ax.set_xticklabels(ys, fontsize=8.5, color=SLATE)
    ax.set_ylim(0, 108); ax.set_xlim(-1.25, len(ys) - 0.5)
    ax.set_yticks([0, 25, 50, 75, 100])
    ax.set_ylabel("% of treated mineral C&D waste", fontsize=8.5, color=SLATE)
    ax.tick_params(axis="y", labelsize=8.5, colors=SLATE)
    ax.legend(frameon=False, fontsize=8, loc="upper center", bbox_to_anchor=(0.5, -0.1), ncol=3)
    ax.text(-1.25, -36, "Source: Eurostat env_wastrt (W121, non-hazardous), retrieved 26 Oct 2026; 2022 values estimated (flag e). Deposits in spent quarries\n"
            "appear as landfill in the 2010 data and as backfilling from 2012 (Commission factsheet, 2015).", fontsize=7, color=GREY, clip_on=False, va="top")
    fig.savefig(OUT / "fig1_malta_series.png", bbox_inches="tight", facecolor="white")


def fig2(y=2020):
    gs = [g for g in MS if (g, "TRT", y) in V and V[(g, "TRT", y)] and (g, "RCV_R_B", y) in V]
    gs = sorted(gs, key=lambda g: share(g, "RCV_R_B", y))
    fig, ax = plt.subplots(figsize=(9.2, 3.9), dpi=220)
    rec = [share(g, "RCV_R", y) for g in gs]
    tot = [share(g, "RCV_R_B", y) for g in gs]
    bf = [t - r for t, r in zip(tot, rec)]
    ax.bar(range(len(gs)), rec, color=[GREEN if g == "MT" else "#9DB7A8" for g in gs], width=0.72, label="Recycling")
    ax.bar(range(len(gs)), bf, bottom=rec, color=[AMBER if g == "MT" else "#F0D49A" for g in gs], width=0.72,
           label="Backfilling and other material recovery")
    eu = share("EU27_2020", "RCV_R_B", y)
    ax.axhline(eu, color=SLATE, lw=1.2, ls="--")
    ax.text(-0.4, eu + 2.5, f"EU-27 recovery {eu:.1f}%", fontsize=8, color=SLATE)
    ax.set_xticks(range(len(gs))); ax.set_xticklabels(gs, fontsize=7.5, color=SLATE)
    for t in ax.get_xticklabels():
        if t.get_text() == "MT":
            t.set_weight("bold"); t.set_color(GREEN)
    i = gs.index("MT")
    ax.text(i, 103, "100", ha="center", fontsize=8.5, color=GREEN, weight="bold")
    ax.set_ylim(0, 112); ax.set_yticks([0, 25, 50, 75, 100])
    ax.tick_params(axis="y", labelsize=8.5, colors=SLATE)
    ax.set_ylabel(f"% of treated mineral C&D waste, {y}", fontsize=8.5, color=SLATE)
    ax.legend(frameon=False, fontsize=8, loc="upper center", bbox_to_anchor=(0.5, -0.1), ncol=2)
    ax.text(0, -40, f"Source: Eurostat env_wastrt (W121, non-hazardous), {y}, retrieved 26 Oct 2026. Bar height = recovery rate; "
            "Malta in strong colours. Sorted by recovery rate.", fontsize=7, color=GREY, clip_on=False,
            transform=ax.get_yaxis_transform())
    fig.savefig(OUT / f"fig2_eu_{y}.png", bbox_inches="tight", facecolor="white")


if __name__ == "__main__":
    fig1(); fig2(2020)
