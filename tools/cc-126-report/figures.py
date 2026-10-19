"""Figures for Claim Check 126 (run calc.py first)."""
import pathlib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm

HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE / "out"; OUT.mkdir(exist_ok=True)
for f in ["LiberationSans-Regular", "LiberationSans-Bold", "LiberationSans-Italic"]:
    fm.fontManager.addfont(f"/usr/share/fonts/truetype/liberation/{f}.ttf")
plt.rcParams.update({"font.family": "Liberation Sans", "axes.spines.top": False, "axes.spines.right": False,
                     "axes.edgecolor": "#8A9399", "axes.labelcolor": "#2B3A42", "xtick.color": "#2B3A42", "ytick.color": "#2B3A42"})
GREEN, AMBER, RED, SLATE, GREY, BLUE = "#14452F", "#E3A72F", "#B5483A", "#2B3A42", "#8A9399", "#3C6E8F"


def fig_targets():
    fig, ax = plt.subplots(figsize=(9.6, 3.2), dpi=220)
    pts = [(2024, "2024\ncompletion\nexpected\n(Jul 2019,\nsecond-hand)", GREY), (2025, "2025\noperations\nto start\n(Sep 2020,\nsecond-hand)", GREY),
           (2030, "2030\nindicative commissioning\n(promoter, 2022)", BLUE)]
    for x, l, c in pts:
        ax.plot([x], [1], "o", color=c, ms=11)
        ax.text(x, 1.12, l, ha="center", va="bottom", fontsize=8, color=SLATE)
    ax.axvline(2026, color=RED, lw=1.6, ls="--")
    ax.text(2026.06, 0.62, "PN: promised\n“by this year”", ha="left", va="top", fontsize=8.5, color=RED, fontweight="bold")
    ax.set_xlim(2023.3, 2030.9); ax.set_ylim(0.3, 1.9); ax.set_yticks([])
    ax.set_xticks(range(2024, 2031)); ax.spines["left"].set_visible(False)
    fig.text(0.01, -0.04, "Second-hand (via Global Energy Monitor's summary; the MaltaToday and schedule originals were not opened). "
             "Promoter: melitatransgas.com.mt, page last updated 22 Dec 2022.", fontsize=7, color=GREY)
    fig.savefig(OUT / "fig_targets.png", bbox_inches="tight", facecolor="white")


def fig_term():
    fig, ax = plt.subplots(figsize=(9.6, 2.6), dpi=220)
    import datetime as dt
    d = lambda y, m, dd: dt.date(y, m, dd).toordinal()
    ax.barh(1, d(2027, 5, 31) - d(2026, 6, 21), left=d(2026, 6, 21), color=GREEN, height=0.35)
    ax.barh(0, d(2027, 5, 31) - d(2026, 8, 13), left=d(2026, 8, 13), color=BLUE, height=0.35)
    ax.text(d(2026, 6, 25), 1, "344 days (11.3 months)", va="center", color="white", fontsize=9, fontweight="bold")
    ax.text(d(2026, 8, 17), 0, "291 days (9.6 months)", va="center", color="white", fontsize=9, fontweight="bold")
    ax.set_yticks([0, 1]); ax.set_yticklabels(["From SOCAR expiry\n(13 Aug 2026)", "From announcement\n(21 Jun 2026)"], fontsize=8.5)
    ticks = [d(2026, 6, 1), d(2026, 9, 1), d(2026, 12, 1), d(2027, 3, 1), d(2027, 6, 1)]
    ax.set_xticks(ticks); ax.set_xticklabels(["Jun 2026", "Sep", "Dec", "Mar 2027", "Jun"], fontsize=8.5)
    ax.set_xlim(d(2026, 6, 1), d(2027, 6, 15))
    fig.text(0.01, -0.05, "Source: Enemalta release 21 Jun 2026 (supply 'till the end of May 2027'); Italpress/MNA 22 Jun 2026 (SOCAR contract expires 13 Aug). "
             "Start date of BP supply not published.", fontsize=7, color=GREY)
    fig.savefig(OUT / "fig_term.png", bbox_inches="tight", facecolor="white")


fig_targets(); fig_term()
