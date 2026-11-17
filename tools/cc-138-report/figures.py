"""Figures for Claim Check 138."""
import csv
import pathlib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from matplotlib.patches import Rectangle

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[1]
D = ROOT / "data/cc-138"
OUT = HERE / "out"; OUT.mkdir(exist_ok=True)
for f in ["LiberationSans-Regular", "LiberationSans-Bold", "LiberationSans-Italic"]:
    fm.fontManager.addfont(f"/usr/share/fonts/truetype/liberation/{f}.ttf")
plt.rcParams.update({"font.family": "Liberation Sans", "axes.edgecolor": "#8A9399", "axes.labelcolor": "#2B3A42",
                     "xtick.color": "#2B3A42", "ytick.color": "#2B3A42"})
GREEN, AMBER, RED, SLATE, GREY, PALE = "#14452F", "#E3A72F", "#B5483A", "#2B3A42", "#8A9399", "#C9D3CC"


def fig1():
    rows = list(csv.DictReader(open(D / "park_instruments.csv", encoding="utf-8")))
    cols = [("white_rocks", "White Rocks\nL.N. 209/2026"), ("cirkewwa", "Ċirkewwa Marine Park\nL.N. 51/2026"),
            ("majjistral", "Majjistral Park\nS.L. 549.48 and 549.83")]
    fig, ax = plt.subplots(figsize=(9.6, 4.9), dpi=220)
    n = len(rows)
    for i, r in enumerate(rows):
        y = n - 1 - i
        for j, (k, _) in enumerate(cols):
            yes = r[k] == "yes"
            ax.add_patch(Rectangle((j + 0.04, y + 0.08), 0.92, 0.84, color=GREEN if yes else "#F1F1EE",
                                   ec="none"))
            ax.text(j + 0.5, y + 0.5, "Yes" if yes else "No", ha="center", va="center", fontsize=8.5,
                    color="white" if yes else GREY, fontweight="bold" if yes else "normal")
    ax.set_xlim(0, 3); ax.set_ylim(0, n)
    ax.set_xticks([j + 0.5 for j in range(3)]); ax.set_xticklabels([c[1] for c in cols], fontsize=8.5)
    ax.xaxis.tick_top(); ax.tick_params(length=0)
    ax.set_yticks([n - 0.5 - i for i in range(n)]); ax.set_yticklabels([r["provision"] for r in rows], fontsize=8.5)
    for s in ax.spines.values():
        s.set_visible(False)
    fig.text(0.01, -0.03, "Source: full texts on legislation.mt, read 17 Nov 2026 (data/cc-138/park_instruments.csv). "
             "“No” means no such provision was found in the text.", fontsize=7, color=GREY)
    fig.tight_layout()
    fig.savefig(OUT / "fig1_instruments.png", bbox_inches="tight"); plt.close(fig)


def fig2():
    ev = [("30 May 2026", 0, "Election. Labour manifesto: White Rocks to be\n“protected once and for all from development”",
           SLATE),
          ("29 Jul 2026", 1, "Cabinet approves the notice. OPM: the step\n“continues” the pledge to protect parks", AMBER),
          ("31 Jul 2026", 2, "L.N. 209 of 2026 gazetted: five regulations,\nno restriction on development", GREEN),
          ("17 Nov 2026", 3, "No further White Rocks instrument found\non legislation.mt (searched 17 Nov 2026)", GREY)]
    fig, ax = plt.subplots(figsize=(9.6, 2.6), dpi=220)
    ax.axhline(0, color=PALE, lw=2, zorder=0)
    for i, (d, x, t, c) in enumerate(ev):
        ax.scatter([x], [0], s=60, color=c, zorder=3)
        up = 1 if i % 2 == 0 else -1
        ax.plot([x, x], [0, 0.45 * up], color=c, lw=0.8)
        ax.text(x, 0.55 * up, f"{d}\n{t}", ha="center", va="bottom" if up > 0 else "top", fontsize=7.6, color=SLATE)
    ax.set_xlim(-0.6, 3.6); ax.set_ylim(-1.6, 1.6); ax.axis("off")
    fig.text(0.01, -0.02, "Sources: Labour manifesto 2026 (PDF p. 162); OPM press release PR261268; L.N. 209 of 2026; "
             "legislation.mt search. Dates not to scale.", fontsize=7, color=GREY)
    fig.savefig(OUT / "fig2_timeline.png", bbox_inches="tight"); plt.close(fig)


fig1(); fig2()
