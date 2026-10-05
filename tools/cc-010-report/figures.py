"""Figures for Claim Check 010, drawn from data/cc-010/ (run data/cc-010/calc.py first). Output: out/"""
import csv
import datetime as dt
import pathlib

import matplotlib
matplotlib.use("Agg")
import matplotlib.dates as mdates
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
D = ROOT / "data" / "cc-010"
N = {r["measure"]: r for r in csv.DictReader(open(D / "government_counts.csv", encoding="utf-8"))}
DT = {r["event"]: dt.date.fromisoformat(r["date"]) for r in csv.DictReader(open(D / "dates.csv", encoding="utf-8"))}


def fig1():
    """Trees reported against the five-year window of pledge 305 (trees only; shrubs and vouchers kept apart)."""
    start = DT["2022 general election"]
    end = start.replace(year=start.year + 5)
    count_date = DT["Latest cumulative count date"]
    snap = DT["2026 general election (snap)"]
    pledge = int(N["Manifesto pledge"]["value"]) / 1000
    minister = int(N["Government trees planted"]["value"]) / 1000
    party = int(N["Labour 2026 manifesto trees planted"]["value"]) / 1000
    y2024 = int(N["2024 government tree plantings"]["value"]) / 1000
    share = lambda d: 100 * (d - start).days / (end - start).days

    fig, (a1, a2) = plt.subplots(1, 2, figsize=(8.8, 4.3), dpi=220, gridspec_kw={"width_ratios": [2.15, 1]})
    a1.plot([start, end], [0, pledge], color=GREY, lw=1.2, ls=(0, (4, 3)))
    a1.text(dt.date(2022, 5, 1), 42, "even pace to 100,000\nin five years (reference only)", fontsize=8.2,
            color=GREY, ha="left", va="bottom")
    a1.axhline(pledge, color=RED, lw=1.2)
    a1.text(start + dt.timedelta(days=20), pledge + 2.5, "Pledge 305: 100,000 trees in five years", fontsize=8.4,
            color=SLATE)
    a1.plot([count_date], [minister], "o", ms=8, color=ORANGE, zorder=5)
    a1.plot([count_date], [party], "s", ms=7, color=GREEN, zorder=5)
    box = dict(boxstyle="round,pad=0.15", facecolor="white", edgecolor="none")
    a1.annotate("about 60,000: Minister,\nParliament (Feb 2026)", (count_date, minister), xytext=(-12, 10),
                textcoords="offset points", ha="right", fontsize=8.4, color=SLATE, bbox=box)
    a1.annotate("more than 57,000: Labour’s\n2026 manifesto (2022–2025)", (count_date, party), xytext=(-12, -28),
                textcoords="offset points", ha="right", fontsize=8.4, color=SLATE, bbox=box)
    a1.plot([dt.date(2024, 1, 1), dt.date(2024, 12, 31)], [y2024, y2024], color=SAGE, lw=4, solid_capstyle="butt")
    a1.text(dt.date(2024, 1, 10), y2024 + 3, "more than 8,000 in 2024 alone\n(Project Green; one year)", fontsize=8.2,
            color=SLATE)
    for d, lab in ((count_date, f"end-2025\n{share(count_date):.0f}% of the window"),
                   (snap, f"30 May 2026 election\nends the legislature\n({share(snap):.0f}%)")):
        a1.axvline(d, color=AMBER if d == snap else GREY, lw=1, ls="--" if d == snap else ":")
    a1.text(count_date - dt.timedelta(days=12), 102.5, f"end-2025 ({share(count_date):.0f}%)", fontsize=8.1,
            color=SLATE, ha="right")
    a1.text(snap + dt.timedelta(days=12), 30, f"30 May 2026\nsnap election\n({share(snap):.0f}%)", fontsize=8.1,
            color=SLATE)
    a1.text(start + dt.timedelta(days=20), 91.5, "Not trees planted, so not shown: more than 100,000 shrubs (to "
            "end-2025);\nvouchers for 23,000 trees on private land (by 13 May 2026)", fontsize=8.1, color=SLATE,
            va="top", bbox=dict(boxstyle="round,pad=0.35", facecolor="#EEF0F1", edgecolor="none"))
    a1.set_xlim(start, end + dt.timedelta(days=10))
    a1.set_ylim(0, 112)
    a1.xaxis.set_major_locator(mdates.YearLocator())
    a1.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    a1.tick_params(labelsize=8.5)
    a1.set_ylabel("Trees reported planted (thousands)", fontsize=8.5)
    a1.grid(axis="y", color="#E3E6E8", lw=0.6)
    a1.set_axisbelow(True)
    a1.set_title("Trees reported against the five years of pledge 305", fontsize=9.5, color=GREEN, loc="left",
                 fontweight="bold")

    labs = ["Window\nelapsed", "Trees\n(Minister)", "Trees\n(Labour)"]
    vals = [share(count_date), 100 * minister / pledge, 100 * party / pledge]
    b = a2.bar(labs, vals, color=[GREY, ORANGE, GREEN], width=0.62)
    for r, v, pre in zip(b, vals, ["", "~", ">"]):
        a2.text(r.get_x() + r.get_width() / 2, v + 2, f"{pre}{v:.0f}%", ha="center", fontsize=10,
                fontweight="bold", color=SLATE)
    a2.set_ylim(0, 105)
    a2.set_yticks([0, 25, 50, 75, 100])
    a2.set_yticklabels(["0", "25%", "50%", "75%", "100%"])
    a2.tick_params(labelsize=8)
    a2.set_title("End-2025: time gone, trees reported", fontsize=9.5, color=GREEN, loc="left", fontweight="bold")
    fig.text(0.01, -0.05, "Window counted from the 26 March 2022 election. Shrubs (more than 25,000 in 2024) and "
             "vouchers (a separate private-land scheme) are reported separately from trees. Sources: Project Green\n"
             "(31 Dec 2024; 13 May 2026); Parliament, PQ 34270 (18 Feb 2026); Partit Laburista manifestos 2022 "
             "(pledge 305) and 2026 (item 43); IFES ElectionGuide.", fontsize=7, color=GREY)
    fig.tight_layout(w_pad=2.5)
    fig.savefig(OUT / "fig1_pledge.png", bbox_inches="tight", facecolor="white")


if __name__ == "__main__":
    fig1()
    print("figures in", OUT)
