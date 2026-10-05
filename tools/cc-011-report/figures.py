"""Figures for Claim Check 011, drawn from data/cc-011/ (run green_access.py first)."""
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


def fig1():
    rows = list(csv.DictReader(open(ROOT / "data" / "cc-011" / "green_access_results.csv")))
    defs = []
    for r in rows:
        if r["definition"] not in defs:
            defs.append(r["definition"])
    order = ["D3 open or green space", "D2 green space, broad", "D1 public parks and gardens",
             "D2 green space >= 0.5 ha", "D1 parks >= 0.5 ha", "D1 parks >= 1 ha"]
    labels = {"D3 open or green space": "Open or green space\n(incl. squares, beaches)",
              "D2 green space, broad": "Any green space\n(incl. scrub, garrigue, verges)",
              "D1 public parks and gardens": "Public parks and gardens,\nany size",
              "D2 green space >= 0.5 ha": "Green space\n≥ 0.5 ha",
              "D1 parks >= 0.5 ha": "Parks and gardens\n≥ 0.5 ha (WHO core size)",
              "D1 parks >= 1 ha": "Parks and gardens\n≥ 1 ha"}
    get = {(r["definition"], int(r["distance_m"])): float(r["population_share_within"]) * 100 for r in rows}
    fig, ax = plt.subplots(figsize=(9.6, 4.8), dpi=220)
    ys = range(len(order))
    h = 0.26
    for j, (d, col, lab) in enumerate(((800, SAGE, "800 m straight line (optimistic 10-min walk)"),
                                       (615, GREEN, "800 m walking route (615 m straight line)"),
                                       (300, AMBER, "300 m straight line (WHO Europe indicator)"))):
        vals = [get[(o, d)] for o in order]
        pos = [y + (j - 1) * h for y in ys]
        ax.barh(pos, vals, height=h, color=col, label=lab)
        for p, v_ in zip(pos, vals):
            ax.text(v_ + 0.8, p, f"{v_:.0f}%", va="center", fontsize=7.4, color=SLATE)
    ax.set_yticks(list(ys))
    ax.set_yticklabels([labels[o] for o in order], fontsize=8)
    ax.invert_yaxis()
    ax.set_xlim(0, 108)
    ax.set_xlabel("Share of Malta’s residents within the distance (%). Sources: WorldPop 2025 (100 m), "
                  "OpenStreetMap 2 Oct 2026; our analysis.", fontsize=7.2, color=GREY)
    ax.legend(frameon=False, fontsize=7.6, loc="lower right")
    fig.savefig(OUT / "fig1_green_access.png", bbox_inches="tight", facecolor="white")


fig1()
print("figures in", OUT)
