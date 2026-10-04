"""Figures for Claim Check 019, drawn from data/cc-019/ and docs/data/geo.json (run fetch_data.py first)."""
import csv, json, math, pathlib
import numpy as np
import pyproj
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from matplotlib.patches import Polygon

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
D = ROOT / "data" / "cc-019"
C = {r["rule"]: r for r in csv.DictReader(open(D / "io_lulc_change.csv"))}
G = json.load(open(D / "io_lulc_grid.json"))
a, b, x0, d, e, y0 = G["transform"]
to_utm = pyproj.Transformer.from_crs(4326, G["crs"], always_xy=True).transform


def fig1():
    geo = json.load(open(ROOT / "docs" / "data" / "geo.json"))
    o = geo["origin"]
    k = 111320 * math.cos(math.radians(o["lat"]))
    fig, ax = plt.subplots(figsize=(9.6, 6.0), dpi=220)
    allp = []
    for isl in geo["islands"]:
        r = isl["coarse"]
        pts = [to_utm(o["lon"] + r[i] / k, o["lat"] + r[i + 1] / 110574) for i in range(0, len(r) - 1, 2)]
        allp += pts
        ax.add_patch(Polygon(pts, closed=True, fc="#EDEDE4", ec=GREY, lw=0.6))
    px = np.loadtxt(D / "new_built_strict.csv", delimiter=",", skiprows=1)
    xs, ys = x0 + (px[:, 1] + 0.5) * a, y0 + (px[:, 0] + 0.5) * e
    ax.scatter(xs, ys, s=0.6, c=RED, marker="s", linewidths=0, alpha=0.8)
    ax.set_aspect("equal")
    px_, py_ = zip(*allp)
    ax.set_xlim(min(px_) - 800, max(px_) + 800)
    ax.set_ylim(min(py_) - 800, max(py_) + 800)
    ax.set_xticks([]), ax.set_yticks([])
    for s in ax.spines.values():
        s.set_visible(False)
    ax.set_title("Land that became consistently built up, 2017–19 to 2021–23 (red, 10 m pixels)", fontsize=9.5,
                 color=GREEN, loc="left", fontweight="bold")
    ax.text(0.0, -0.03, "Source: Impact Observatory / Esri 10 m annual land cover v2 via Microsoft Planetary Computer; "
            "coastline © OpenStreetMap contributors. Pixels not built in 2017–2019 and built in 2021–2023.",
            transform=ax.transAxes, fontsize=7, color=GREY)
    fig.savefig(OUT / "fig1_map.png", bbox_inches="tight", facecolor="white")


def fig2():
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(9.6, 3.6), dpi=220, gridspec_kw={"width_ratios": [1.2, 1]})
    labs = ["Amphora\n(Dynamic World,\nchecked by hand)", "IO land cover,\n3-year rule\n(net)", "IO land cover,\n2-year rule\n(net)"]
    vals = [0.83, float(C["strict"]["net_km2"]), float(C["two-year"]["net_km2"])]
    gross = [None, float(C["strict"]["new_built_km2"]), float(C["two-year"]["new_built_km2"])]
    bars = a1.bar(labs, vals, color=[ORANGE, GREEN, SAGE], width=0.6)
    for i, (r, v) in enumerate(zip(bars, vals)):
        a1.text(r.get_x() + r.get_width() / 2, v + 0.08, f"{v:.2f}", ha="center", fontsize=10, fontweight="bold",
                color=SLATE)
        if gross[i]:
            a1.plot([r.get_x() + 0.05, r.get_x() + r.get_width() - 0.05], [gross[i]] * 2, color=GREY, ls=":", lw=1.2)
            a1.text(r.get_x() + r.get_width() / 2, gross[i] + 0.08, f"gross {gross[i]:.1f}", ha="center", fontsize=7.5,
                    color=GREY)
    a1.set_ylabel("km² newly built up, 2018–2023")
    a1.set_ylim(0, 5.8)
    a1.set_title("How much green land was built on?", fontsize=9.5, color=GREEN, loc="left", fontweight="bold")
    s = C["strict"]
    parts = [("Crops", float(s["from_crops_pct"]), AMBER), ("Rangeland\n(shrub, grass)", float(s["from_rangeland_pct"]), SAGE),
             ("Bare ground", float(s["from_bare_pct"]), GREY)]
    a2.barh([p[0] for p in parts], [p[1] for p in parts], color=[p[2] for p in parts], height=0.55)
    for i, p in enumerate(parts):
        a2.text(p[1] + 1.5, i, f"{p[1]:.0f}%", va="center", fontsize=9.5, color=SLATE)
    a2.axvline(95, color=ORANGE, ls="--", lw=1.2)
    a2.text(93, 1.6, "Amphora:\n“nearly 95%\nfarmland”", fontsize=7.5, color=ORANGE, ha="right", va="center")
    a2.set_xlim(0, 100)
    a2.invert_yaxis()
    a2.set_title("What it was before (IO, 3-year rule)", fontsize=9.5, color=GREEN, loc="left", fontweight="bold")
    fig.text(0.01, -0.04, "Net = new built-up minus the reverse change under the same rule (a gauge of classification "
             "noise). Dotted lines: gross change.", fontsize=7, color=GREY)
    fig.tight_layout(w_pad=3)
    fig.savefig(OUT / "fig2_estimates.png", bbox_inches="tight", facecolor="white")


fig1()
fig2()
print("figures in", OUT)
