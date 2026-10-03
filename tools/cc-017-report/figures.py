"""Figures for Claim Check 017, drawn from data/cc-017/ and docs/data/geo.json (run fetch_data.py first)."""
import csv, json, math, pathlib
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from matplotlib.colors import ListedColormap
from matplotlib.patches import Ellipse, Polygon, Patch

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
D = ROOT / "data" / "cc-017"
L = {r["year"]: float(r["land_ha"]) for r in csv.DictReader(open(D / "s2_land_t2.csv"))}


def fig1():
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(9.6, 3.9), dpi=220, gridspec_kw={"width_ratios": [1.1, 1]})
    ys = list(L)
    base = sum(L[y] for y in ("2017", "2020", "2023")) / 3
    b = a1.bar(ys, [L[y] - base for y in ys], color=[GREY if y < "2024" else ORANGE for y in ys], width=0.6)
    for r, y in zip(b, ys):
        v = L[y] - base
        a1.text(r.get_x() + r.get_width() / 2, max(v, 0) + 0.1, f"{v:+.1f}", ha="center", fontsize=9.5, color=SLATE)
    a1.axhline(3.0, color=GREEN, ls="--", lw=1.3)
    a1.text(-0.4, 3.12, "Stated size: 30,000 m² = 3.0 ha", fontsize=8, color=GREEN)
    a1.set_ylim(-0.6, 4.6)
    a1.set_ylabel("Hectares of land added (vs 2017–23 mean)")
    a1.set_title("New land at Terminal 2, each summer", fontsize=9.5, color=GREEN, loc="left", fontweight="bold")
    m23 = np.loadtxt(D / "s2_mask_2023.csv", delimiter=",")
    m26 = np.loadtxt(D / "s2_mask_2026.csv", delimiter=",")
    img = np.where((m26 == 1) & (m23 == 0), 2, m23)  # 0 sea, 1 land 2023, 2 new by 2026
    a2.imshow(img, cmap=ListedColormap(["#D6E6EE", "#C9C3B4", ORANGE]), vmin=0, vmax=2, interpolation="nearest")
    a2.set_xticks([]), a2.set_yticks([])
    for s in a2.spines.values():
        s.set_visible(False)
    a2.set_title("Land in 2023 and new land by 2026", fontsize=9.5, color=GREEN, loc="left", fontweight="bold")
    a2.legend(handles=[Patch(fc="#C9C3B4", ec=SLATE, label="Land 2023"), Patch(color=ORANGE, label="New by summer 2026"),
                       Patch(fc="#D6E6EE", ec=SLATE, label="Sea")], frameon=True, framealpha=0.9, fontsize=7.5,
               loc="upper left")
    a2.text(108, 99, "1 km", fontsize=7, color=SLATE, ha="right", va="bottom")
    a2.plot([0, 100], [98, 98], color=SLATE, lw=1.5)
    fig.text(0.01, -0.04, "Per-pixel median of eight clear Sentinel-2 scenes each summer (May–Oct); land = NDWI < 0; 10 m "
             "pixels; about ±1 ha. Isolated specks are moored ships and wave glint.", fontsize=7, color=GREY)
    fig.tight_layout(w_pad=3)
    fig.savefig(OUT / "fig1_terminal2.png", bbox_inches="tight", facecolor="white")


def fig2():
    geo = json.load(open(ROOT / "docs" / "data" / "geo.json"))
    o = geo["origin"]
    k = 111320 * math.cos(math.radians(o["lat"]))
    to_ll = lambda x, y: (o["lon"] + x / k, o["lat"] + y / 110574)
    fig, ax = plt.subplots(figsize=(9.6, 5.2), dpi=220)
    n2k = json.load(open(D / "natura2000.geojson"))
    col = {0: (SAGE, "Habitats Directive site (SAC)"), 1: (BLUE, "Birds Directive site (SPA)")}
    for ft in n2k["features"]:
        g = ft["geometry"]
        polys = g["coordinates"] if g["type"] == "MultiPolygon" else [g["coordinates"]]
        c = col[ft["properties"]["layer"]][0]
        for poly in polys:
            ax.add_patch(Polygon(poly[0], closed=True, fc=c, ec=c, alpha=0.28, lw=0.6))
    for isl in geo["islands"]:
        pts = isl.get("detail") or isl["coarse"]
        rings = pts if isinstance(pts[0], list) else [pts]
        for r in rings:
            xy = [to_ll(r[i], r[i + 1]) for i in range(0, len(r) - 1, 2)]
            ax.add_patch(Polygon(xy, closed=True, fc="#EDE9DF", ec=SLATE, lw=0.6))
    ax.plot(14.531, 35.819, marker="s", ms=8, color=RED)
    ax.annotate("Malta Freeport", (14.531, 35.819), (14.555, 35.797), fontsize=9, color=RED, fontweight="bold",
                arrowprops={"arrowstyle": "-", "color": RED, "lw": 0.8})
    ax.add_patch(Ellipse((14.531, 35.819), 3 / (111.32 * math.cos(math.radians(35.82))), 3 / 110.574, fill=False,
                         ec=RED, ls="--", lw=1))
    ax.text(14.5, 35.835, "1.5 km", fontsize=7.5, color=RED)
    ax.set_xlim(14.40, 14.62)
    ax.set_ylim(35.77, 35.89)
    ax.set_aspect(1 / math.cos(math.radians(35.83)))
    ax.set_xticks([]), ax.set_yticks([])
    for s in ax.spines.values():
        s.set_visible(False)
    ax.set_facecolor("#F4F8FA")
    ax.legend(handles=[Patch(color=SAGE, alpha=0.5, label=col[0][1]), Patch(color=BLUE, alpha=0.5, label=col[1][1])],
              frameon=False, fontsize=8, loc="upper left")
    ax.set_title("Protected areas around the Freeport", fontsize=9.5, color=GREEN, loc="left", fontweight="bold")
    fig.text(0.13, 0.06, "Sources: EEA Natura 2000 (2024 release); coastline © OpenStreetMap contributors.",
             fontsize=7, color=GREY)
    fig.savefig(OUT / "fig2_natura.png", bbox_inches="tight", facecolor="white")


fig1()
fig2()
print("figures in", OUT)
