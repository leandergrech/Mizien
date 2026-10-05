"""Figures for Claim Check 014, drawn from data/cc-014/ (run calc.py first)."""
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
D = ROOT / "data" / "cc-014"
S = list(csv.DictReader(open(D / "pa_enforcement_series.csv", encoding="utf-8")))
O = list(csv.DictReader(open(D / "outcomes_by_year.csv", encoding="utf-8")))


def title(ax, t, y=1.06):
    ax.set_title(t, fontsize=10.5, color=GREEN, loc="left", fontweight="bold", y=y)


def fig1():
    fig, ax = plt.subplots(figsize=(9.6, 4.9), dpi=220)
    ny = [(int(r["year"]), int(r["enforcement_notices"])) for r in S if r["enforcement_notices"]]
    ky = [(int(r["year"]), int(r["complaints"])) for r in S if r["complaints"]]
    second = {int(r["year"]) for r in S if "Second-hand" in r["access_note"]}
    ax.bar([y for y, _ in ny], [n for _, n in ny], color=[SAGE if y in second else GREEN for y, _ in ny],
           width=0.7, label="Enforcement notices issued", zorder=2)
    ax.plot([y for y, _ in ky], [k for _, k in ky], "o", color=ORANGE, ms=7, label="Complaints of illegal development",
            zorder=3)
    for y, k in ky:
        ax.text(y, k + 120, f"{k:,}", ha="center", fontsize=8, color=ORANGE, fontweight="bold")
    for y, n in ny:
        ax.text(y, n + 45, f"{n:,}", ha="center", fontsize=8, color=SLATE)
    ax.axhline(1000, color=GREY, lw=0.6, ls=":")
    ax.text(2016.4, 1050, "1,000 a year", ha="right", fontsize=8, color=GREY)
    ax.axvspan(2011.6, 2016.4, color="#EEF1EE", zorder=0)
    ax.text(2014, 2350, "2012–2016:\nno readable\nsource found", ha="center", fontsize=8.5, color=GREY,
            style="italic")
    ax.text(2008, 90, "no\ndata", ha="center", fontsize=8, color=GREY, style="italic")
    ax.set_xlim(2000.3, 2024.7)
    ax.set_ylim(0, 4150)
    ax.set_xticks(range(2001, 2025, 2))
    ax.set_ylabel("Number per year", fontsize=9)
    ax.legend(frameon=False, fontsize=8.5, loc="upper right", bbox_to_anchor=(1.0, 1.04))
    title(ax, "Notices fell by four-fifths; complaints of illegal development did not")
    ax.text(2000.4, -640, "Sources: MEPA annual reports 2004–2011 (notices 2001–2011); Planning Authority annual reports "
            "2017–2024 (2017–2023 read as page images).\nComplaints: 2005 is financial year 2004/05; 2011 excludes sites "
            "already under a notice; 2017 is rounded in the report; 2018 excludes 1,572\nconstruction-site complaints "
            "counted separately; 2019 includes complaints under the third-party-damage regulations.",
            fontsize=8, color=GREY, va="top")
    fig.savefig(OUT / "fig1_series.png", bbox_inches="tight", facecolor="white")
    plt.close(fig)


def fig2():
    fig, ax = plt.subplots(figsize=(9.6, 4.9), dpi=220)
    w = 0.62
    for o in O:
        y = int(o["year"])
        parts = [("sanctioning", BLUE, None), ("removed", SAGE, "///" if o["removed_how"] != "read" else None),
                 ("persuasion", AMBER, None), ("notice", RED, None)]
        bottom = 0
        for key, col, hatch in parts:
            v = int(o[key])
            if not v:
                continue
            ax.bar(y, v, bottom=bottom, width=w, color=col, hatch=hatch, edgecolor="white", lw=0.8, zorder=2)
            lab = ("~" if hatch else "") + f"{v:,}"
            if key == "persuasion":
                ax.text(y + w / 2 + 0.04, bottom + v / 2, f"{v}", va="center", ha="left", fontsize=8, color=SLATE)
            else:
                ax.text(y, bottom + v / 2, lab, ha="center", va="center", fontsize=8.5, color="white",
                        fontweight="bold", zorder=5, bbox=dict(facecolor=col, edgecolor="none", pad=1.2))
            bottom += v
        conf = int(o["confirmed"])
        ax.plot([y - w / 2 - 0.06, y + w / 2 + 0.06], [conf, conf], color=SLATE, lw=2.2, zorder=4)
        ax.text(y, max(conf, bottom) + 45, f"~{conf:,}", ha="center", va="bottom", fontsize=8.5, color=SLATE,
                fontweight="bold")
        share = 100 * int(o["notice"]) / conf
        ax.text(y, -230, f"{share:.0f}", ha="center", va="top", fontsize=9, color=RED, fontweight="bold")
    ax.text(2017.42, -230, "Notices per 100\nconfirmed cases", ha="right", va="top", fontsize=8, color=RED)
    ax.set_xlim(2017.45, 2024.55)
    ax.set_ylim(0, 2250)
    ax.set_xticks(range(2018, 2025))
    ax.tick_params(axis="x", length=0, labelsize=9.5)
    ax.set_ylabel("Complaints confirmed as illegal development", fontsize=9)
    handles = [Patch(color=BLUE, label="Owner applied to sanction the works"),
               Patch(color=SAGE, label="Owner removed the works"),
               Patch(facecolor=SAGE, edgecolor="white", hatch="///", label="Removed (from a stated %)"),
               Patch(color=AMBER, label="Resolved after persuasion (2024 only)"),
               Patch(color=RED, label="Enforcement notice"),
               Line2D([0], [0], color=SLATE, lw=2.2, label="Confirmed cases (stated share)")]
    ax.legend(handles=handles, frameon=False, fontsize=8, ncol=3, loc="upper left", bbox_to_anchor=(0.0, 1.13),
              columnspacing=1.2, handlelength=1.6)
    title(ax, "Complaints confirmed as illegal development, and how the cases ended", y=1.15)
    ax.text(2017.45, -560, "Source: Planning Authority annual reports 2018–2024 (2018–2023 read as page images; 2024 "
            "pp. 28–30). Confirmed = the stated share\n(about half to 59%) × complaints received. Hatched: removals given "
            "only as a percentage of confirmed cases (2020–2022) or as “the rest of\nthe cases” (2018). The reported "
            "outcomes do not always add up to the stated share; the 2024 categories may overlap.",
            fontsize=8, color=GREY, va="top")
    fig.savefig(OUT / "fig2_outcomes_by_year.png", bbox_inches="tight", facecolor="white")
    plt.close(fig)


def fig3():
    fig, ax = plt.subplots(figsize=(9.6, 3.1), dpi=220)
    pts = [(int(r["year"]), 100 * int(r["enforcement_notices"]) / int(r["complaints"])) for r in S
           if r["enforcement_notices"] and r["complaints"]]
    xs = list(range(len(pts)))
    gap = 3  # index of the first PA year: leave a visual break between 2011 and 2017
    xs = [i if i < gap else i + 1 for i in xs]
    cols = [GREEN if y <= 2011 else ORANGE for y, _ in pts]
    ax.bar(xs, [v for _, v in pts], color=cols, width=0.62, zorder=2)
    for x, (y, v) in zip(xs, pts):
        ax.text(x, v - 0.8, f"{v:.0f}", ha="center", va="top", fontsize=9, color="white", fontweight="bold", zorder=3)
    mepa = [v for y, v in pts if y <= 2011]
    pa = [v for y, v in pts if y >= 2017]
    ax.plot([-0.4, 2.4], [sum(mepa) / len(mepa)] * 2, color=GREEN, ls="--", lw=1, zorder=1)
    ax.plot([3.6, xs[-1] + 0.4], [sum(pa) / len(pa)] * 2, color=ORANGE, ls="--", lw=1, zorder=1)
    ax.text(1, 48, f"MEPA years: {sum(mepa) / len(mepa):.0f} on average", ha="center", fontsize=8.5, color=GREEN)
    ax.text((4 + xs[-1]) / 2, 17, f"Planning Authority, 2017–2024: {sum(pa) / len(pa):.1f} on average", ha="center",
            fontsize=8.5, color=ORANGE)
    ax.text(3, 2, "2012–16\nno data", ha="center", fontsize=8, color=GREY, style="italic")
    ax.set_xticks(xs)
    ax.set_xticklabels([("FY04/05" if y == 2005 else str(y)) for y, _ in pts])
    ax.tick_params(axis="x", length=0)
    ax.set_ylim(0, 54)
    ax.set_xlim(-0.6, xs[-1] + 0.6)
    ax.set_ylabel("Notices per 100 complaints", fontsize=9)
    title(ax, "Enforcement notices issued per 100 complaints of illegal development")
    ax.text(-0.6, -11, "Source: data/cc-014/checks.csv, from MEPA annual reports 2005–2011 and Planning Authority annual "
            "reports 2017–2024. Only years with both counts are shown.", fontsize=8, color=GREY, va="top")
    fig.savefig(OUT / "fig3_ratio.png", bbox_inches="tight", facecolor="white")
    plt.close(fig)


fig1()
fig2()
fig3()
print("figures in", OUT)
