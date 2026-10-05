"""Figures for Claim Check 019, drawn from data/cc-019/, docs/data/geo.json and tools/cc-019-report/out/.

Run fetch_data.py and crosscheck.py first: the map needs Amphora's polygons (out/malta-change.geojson, not committed)
and the cached land-cover maps (out/io_esri_*.npy). Version 1.2 replaces the v1.1 map of new built-up pixels with a map
of Amphora's polygons over the independent model's new built-up pixels.
"""
import csv, json, math, pathlib
import numpy as np
import pyproj
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from matplotlib.colors import ListedColormap
from matplotlib.patches import Patch, Polygon, Rectangle
from shapely.geometry import shape
from shapely.ops import transform

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[1]
OUT = HERE / "out"
OUT.mkdir(exist_ok=True)
for f in ["LiberationSans-Regular", "LiberationSans-Bold", "LiberationSans-Italic"]:
    fm.fontManager.addfont(f"/usr/share/fonts/truetype/liberation/{f}.ttf")
plt.rcParams.update({"font.family": "Liberation Sans", "axes.spines.top": False, "axes.spines.right": False,
                     "axes.edgecolor": "#8A9399", "axes.labelcolor": "#2B3A42", "xtick.color": "#2B3A42",
                     "ytick.color": "#2B3A42", "hatch.linewidth": 0.6})
GREEN, SAGE, AMBER, RED, SLATE, GREY, ORANGE, BLUE = ("#14452F", "#7FA88B", "#E3A72F", "#B5483A", "#2B3A42",
                                                      "#8A9399", "#D9772B", "#3C6E8F")
LANDC, BUILTC = "#EDEDE4", "#CFCAC0"
D = ROOT / "data" / "cc-019"
E = {r["rule"]: r for r in csv.DictReader(open(D / "io_lulc_change_ext.csv"))}
K = {r["lc2018"]: r for r in csv.DictReader(open(D / "amphora_classes.csv"))}
O = {r["measure"]: r["value"] for r in csv.DictReader(open(D / "amphora_io_overlap.csv"))}
G = json.load(open(D / "io_lulc_grid.json"))
a, b, x0, d, e, y0 = G["transform"]
to_utm = pyproj.Transformer.from_crs(4326, G["crs"], always_xy=True).transform
RULE = "two-year-2025"  # not built in the 2017 and 2018 maps, built in the 2024 and 2025 maps


def islands(ax, detail=False, **kw):
    geo = json.load(open(ROOT / "docs" / "data" / "geo.json"))
    o = geo["origin"]
    k = 111320 * math.cos(math.radians(o["lat"]))
    pts = []
    for isl in geo["islands"]:
        r = (isl.get("detail") if detail else None) or isl["coarse"]
        xy = [to_utm(o["lon"] + r[i] / k, o["lat"] + r[i + 1] / 110574) for i in range(0, len(r) - 1, 2)]
        pts += xy
        ax.add_patch(Polygon(xy, closed=True, **kw))
    return pts


def amphora(ax, **kw):
    gj = json.load(open(OUT / "malta-change.geojson"))
    for f in gj["features"]:
        g = transform(to_utm, shape(f["geometry"]))
        for p in getattr(g, "geoms", [g]):
            ax.add_patch(Polygon(np.asarray(p.exterior.coords), closed=True, **kw))


def bare(ax):
    ax.set_aspect("equal")
    ax.set_xticks([]), ax.set_yticks([])
    for s in ax.spines.values():
        s.set_visible(False)


def fig1():
    """Amphora's polygons over the independent model's new built-up pixels: all islands and two close-ups."""
    Y = {y: np.load(OUT / f"io_esri_{y}.npy") for y in ("2017", "2018", "2024", "2025")}
    new = (Y["2017"] != 7) & (Y["2018"] != 7) & (Y["2024"] == 7) & (Y["2025"] == 7)
    new &= np.all([(Y[y] != 1) & (Y[y] != 0) for y in Y], axis=0)
    fig = plt.figure(figsize=(9.6, 6.3), dpi=220)
    ax = fig.add_axes([0.0, 0.06, 0.6, 0.86])
    pts = islands(ax, fc=LANDC, ec=GREY, lw=0.6)
    rr, cc = np.nonzero(new)
    ax.scatter(x0 + (cc + 0.5) * a, y0 + (rr + 0.5) * e, s=0.35, c=BLUE, marker="s", linewidths=0, zorder=3)
    amphora(ax, fc=ORANGE, ec=ORANGE, lw=0.9, zorder=4)
    px, py = zip(*pts)
    ax.set_xlim(min(px) - 600, max(px) + 600)
    ax.set_ylim(min(py) - 600, max(py) + 600)
    bare(ax)
    zooms = [("A", "Ħal Far, Birżebbuġa", 455500, 3963550), ("B", "Imqabba and Siġġiewi", 450850, 3967050)]
    H = 1700
    for i, (lab, name, cx, cy) in enumerate(zooms):
        ax.add_patch(Rectangle((cx - H / 2, cy - H / 2), H, H, fill=False, ec=SLATE, lw=1.0, zorder=5))
        ax.text(cx + H / 2 + 250, cy, lab, fontsize=9, fontweight="bold", color=SLATE, va="center", zorder=5)
        z = fig.add_axes([0.62, 0.50 - i * 0.44, 0.37, 0.40])
        r0, r1 = int((y0 - (cy + H / 2)) / -e), int((y0 - (cy - H / 2)) / -e)
        c0, c1 = int((cx - H / 2 - x0) / a), int((cx + H / 2 - x0) / a)
        cat = np.where(new, 2, np.where(Y["2018"] == 7, 1, np.where(Y["2018"] == 1, 3, 0)))[r0:r1, c0:c1]
        z.imshow(cat, cmap=ListedColormap([LANDC, BUILTC, BLUE, "#E3EDF3"]), vmin=0, vmax=3, interpolation="nearest",
                 extent=(x0 + c0 * a, x0 + c1 * a, y0 + r1 * e, y0 + r0 * e), zorder=1)
        amphora(z, fc=ORANGE, ec="#9A4E14", lw=0.7, alpha=0.75, zorder=3)
        z.set_xlim(cx - H / 2, cx + H / 2)
        z.set_ylim(cy - H / 2, cy + H / 2)
        bare(z)
        z.text(0.02, 0.97, f"{lab}  {name}", transform=z.transAxes, fontsize=9, fontweight="bold", color=SLATE,
               va="top", bbox={"fc": "white", "ec": "none", "alpha": 0.85, "pad": 1.5})
        z.plot([cx - H / 2 + 100, cx - H / 2 + 600], [cy - H / 2 + 110] * 2, color=SLATE, lw=1.8, zorder=6)
        z.text(cx - H / 2 + 350, cy - H / 2 + 150, "500 m", fontsize=7, color=SLATE, ha="center", va="bottom", zorder=6,
               bbox={"fc": "white", "ec": "none", "alpha": 0.8, "pad": 0.8})
    ax.legend(handles=[Patch(fc=ORANGE, ec=ORANGE, label="Amphora’s polygons, 2018–23 (397; 0.83 km²)"),
                       Patch(fc=BLUE, label=f"Model: new built-up, first mapped 2019–24 "
                                            f"({float(E[RULE]['new_built_km2']):.1f} km²)"),
                       Patch(fc=BUILTC, label="Model: built-up already in 2018 (close-ups)"),
                       Patch(fc="#E3EDF3", label="Sea (close-ups)")],
              frameon=False, fontsize=8.6, loc="upper right", bbox_to_anchor=(1.04, 1.0))
    fig.text(0.0, 0.985, "Where Amphora and the independent model see new building", fontsize=9.5, color=GREEN,
             fontweight="bold", va="top")
    share = O[f"{RULE}: share of IO new built-up inside Amphora's polygons"]
    fig.text(0.0, 0.035, f"Only {share}% of the model’s new built-up pixels fall inside Amphora’s polygons, and the model "
             f"already mapped {float(O['Amphora area: built in the 2018 map']):.0f}% of Amphora’s area as built-up in 2018.",
             fontsize=8.6, color=SLATE)
    fig.text(0.0, 0.0, "Sources: Amphora Media, Green to Grey change polygons (amphora.media, retrieved 5 Oct 2026); Impact "
             "Observatory / Esri 10 m annual land cover (2017–2025); coastline © OpenStreetMap contributors.",
             fontsize=7, color=GREY)
    fig.savefig(OUT / "fig1_overlap.png", bbox_inches="tight", facecolor="white")


def fig2():
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(9.6, 3.9), dpi=220, gridspec_kw={"width_ratios": [1.25, 1]})
    rules = [("strict", "IO 3-yr\n2020–21"), ("two-year", "IO 2-yr\n2019–22"), ("strict-2025", "IO 3-yr\n2020–23"),
             ("two-year-2025", "IO 2-yr\n2019–24")]
    labs = ["Amphora\n2018–23"] + [l for _, l in rules]
    vals = [0.83] + [float(E[r]["net_km2"]) for r, _ in rules]
    gross = [None] + [float(E[r]["new_built_km2"]) for r, _ in rules]
    cols = [ORANGE, GREEN, SAGE, GREEN, SAGE]
    bars = a1.bar(labs, vals, color=cols, width=0.62)
    a1.axhline(0, color=GREY, lw=0.8)
    for i, (r, v) in enumerate(zip(bars, vals)):
        a1.text(r.get_x() + r.get_width() / 2, max(v, 0) + 0.1, f"{v:.2f}".replace("-", "−"), ha="center", fontsize=9.5,
                fontweight="bold", color=SLATE)
        if gross[i]:
            a1.plot([r.get_x() + 0.04, r.get_x() + r.get_width() - 0.04], [gross[i]] * 2, color=GREY, ls=":", lw=1.2)
            a1.text(r.get_x() + r.get_width() / 2, gross[i] + 0.1, f"gross {gross[i]:.1f}", ha="center", fontsize=7.5,
                    color=GREY)
    a1.set_ylabel("km² of new built-up land (net)")
    a1.set_ylim(-0.4, 5.9)
    a1.tick_params(axis="x", labelsize=8)
    a1.set_title("Net new built-up land: Amphora and four rules", fontsize=9.5, color=GREEN, loc="left",
                 fontweight="bold")
    # right: what the land was in 2018, Amphora's own classes vs the independent model
    s = E["strict"]
    am = [("Cropland", float(K["cropland"]["share_of_all_pct"]), AMBER, None),
          ("Grass", float(K["grass"]["share_of_all_pct"]), SAGE, None),
          ("Other", sum(float(K[k]["share_of_all_pct"]) for k in ("bare", "water", "tree", "bush")), GREY, None),
          ("Unknown", float(K["unknown"]["share_of_all_pct"]), "#ECEDEE", "////")]
    io = [("Crops", float(s["from_crops_pct"]), AMBER, None), ("Rangeland", float(s["from_rangeland_pct"]), SAGE, None),
          ("Bare", float(s["from_bare_pct"]), GREY, None)]
    for y, parts in ((1, am), (0, io)):
        left = 0
        for name, v, c, h in parts:
            a2.barh(y, v, left=left, color=c, hatch=h, ec="white" if h is None else GREY, lw=0.6, height=0.55)
            if v >= 6:
                a2.text(left + v / 2, y, f"{name}\n{v:.0f}%", ha="center", va="center", fontsize=7.6, color=SLATE)
            left += v
    a2.set_yticks([1, 0])
    a2.set_yticklabels(["Amphora’s\npolygons", "Independent\nmodel (3-yr)"], fontsize=8.5)
    a2.set_xlim(0, 100)
    a2.set_ylim(-0.5, 1.9)
    a2.set_xlabel("% of area")
    k = float(K["cropland"]["share_of_known_pct"]) + float(K["grass"]["share_of_known_pct"])
    a2.text(0, 1.48, f"Cropland + grass = {k:.0f}% of the area with a known class:\nthe likely source of “nearly 95%”",
            fontsize=7.6, color=ORANGE, va="center")
    a2.set_title("What the land was in 2018", fontsize=9.5, color=GREEN, loc="left", fontweight="bold")
    fig.text(0.01, -0.05, "Left: net = new built-up minus the reverse change under the same rule; dotted lines are gross. "
             "Windows: when land was first mapped as built-up.\nRight: Amphora’s 2018 classes come from Dynamic World "
             "(cropland, grass, other; 37% unknown); the model’s classes are Impact Observatory’s.", fontsize=7,
             color=GREY, va="top")
    fig.tight_layout(w_pad=3)
    fig.savefig(OUT / "fig2_estimates.png", bbox_inches="tight", facecolor="white")


fig1()
fig2()
print("figures in", OUT)
