"""Figures for Claim Check 051. Run fetch_data.py and calc.py first (the depth figure needs out/bathymetry.tif).
Needs shapely, pyproj, numpy, Pillow. Works offline from data/cc-051/."""
import csv, json, math, pathlib
import numpy as np
import pyproj
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
from PIL import Image
from shapely import make_valid
from shapely.geometry import Polygon, shape
from shapely.ops import transform, unary_union

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[1]
D = ROOT / "data" / "cc-051"
OUT = HERE / "out"
OUT.mkdir(exist_ok=True)
for f in ["LiberationSans-Regular", "LiberationSans-Bold", "LiberationSans-Italic"]:
    fm.fontManager.addfont(f"/usr/share/fonts/truetype/liberation/{f}.ttf")
plt.rcParams.update({"font.family": "Liberation Sans", "axes.spines.top": False, "axes.spines.right": False,
                     "axes.edgecolor": "#8A9399", "axes.labelcolor": "#2B3A42", "xtick.color": "#2B3A42",
                     "ytick.color": "#2B3A42", "hatch.linewidth": 0.6})
GREEN, SAGE, AMBER, RED, SLATE, GREY, ORANGE, BLUE = ("#14452F", "#7FA88B", "#E3A72F", "#B5483A", "#2B3A42",
                                                      "#8A9399", "#D9772B", "#3C6E8F")
REDPALE, LANDC, NEIGHBOUR = "#F3D9D3", "#C9C3B4", "#E4E1D8"
DEPTHC = ["#D6E6EF", "#8DB2C8", "#3C6E8F"]  # shelf, slope, deep: one hue, light to dark
P = pyproj.Transformer.from_crs(4326, 32633, always_xy=True).transform
NM = 1852

# ---------------------------------------------------------------- shared data
Z = {f["properties"]["zone"]: make_valid(transform(P, shape(f["geometry"]))).buffer(0)
     for f in json.load(open(D / "boundaries.geojson"))["features"]}
geo = json.load(open(ROOT / "docs" / "data" / "geo.json"))
o = geo["origin"]
k = 111320 * math.cos(math.radians(o["lat"]))
LAND = unary_union([transform(P, Polygon([(o["lon"] + r[i] / k, o["lat"] + r[i + 1] / 110574)
                                          for i in range(0, len(r) - 1, 2)])).buffer(0) for isl in geo["islands"]
                    for r in [isl.get("detail") or isl["coarse"]]])
PROT = Z["protected"]
ENV = Z["within_25nm"]
WATERS = unary_union([Z["eu_marine_waters"], ENV])  # all waters Malta reports to the EU, incl. internal waters
CHK = {r["check"]: float(r["value"]) for r in csv.DictReader(open(D / "checks.csv"))}
DEP = list(csv.DictReader(open(D / "depth_bands.csv")))
X0, Y0, X1, Y1 = 12.4, 34.0, 18.3, 36.8
GRID = OUT / "bathymetry.tif"


def poly(ax, g, **kw):
    for p in getattr(g, "geoms", [g]):
        if p.geom_type != "Polygon" or p.is_empty:
            continue
        x, y = p.exterior.xy
        ax.fill(x, y, **kw)


def holes(ax, g, fc):
    """Paint the holes of g (e.g. islands inside a zone) in colour fc."""
    for p in getattr(g, "geoms", [g]):
        for r in getattr(p, "interiors", []):
            x, y = r.xy
            ax.fill(x, y, fc=fc, ec="none")


def outline(ax, g, **kw):
    for p in getattr(g, "geoms", [g]):
        if p.geom_type != "Polygon":
            continue
        x, y = p.exterior.xy
        ax.plot(x, y, **kw)


def grid():
    a = np.array(Image.open(GRID)).astype("float64")
    H, W = a.shape
    lon = X0 + (X1 - X0) / W * (np.arange(W) + 0.5)
    lat = Y1 - (Y1 - Y0) / H * (np.arange(H) + 0.5)
    GX, GY = pyproj.Transformer.from_crs(4326, 32633, always_xy=True).transform(*np.meshgrid(lon, lat))
    return GX, GY, np.where(a < 1e9, -a, np.nan)


def neighbours(ax, G):
    """Neighbouring land (Sicily, Lampedusa, Linosa) from the depth grid's no-data cells."""
    GX, GY, dep = G
    ax.contourf(GX, GY, np.isnan(dep).astype(float), levels=[0.5, 1.5], colors=[NEIGHBOUR], zorder=1)


def frame(ax, g, pad=12000):
    x0, y0, x1, y1 = g.bounds
    ax.set_xlim(x0 - pad, x1 + pad)
    ax.set_ylim(y0 - pad, y1 + pad)
    ax.set_aspect("equal")
    ax.set_xticks([]), ax.set_yticks([])
    for s in ax.spines.values():
        s.set_visible(False)


def scalebar(ax, km=50, loc=(0.03, 0.04)):
    x0, x1 = ax.get_xlim()
    y0, y1 = ax.get_ylim()
    x, y = x0 + loc[0] * (x1 - x0), y0 + loc[1] * (y1 - y0)
    ax.plot([x, x + km * 1000], [y, y], color=SLATE, lw=2, solid_capstyle="butt", zorder=9)
    ax.text(x + km * 500, y + 0.015 * (y1 - y0), f"{km} km", ha="center", va="bottom", fontsize=7, color=SLATE, zorder=9)


def label(ax, lon, lat, text, **kw):
    x, y = P(lon, lat)
    ax.text(x, y, text, **{"fontsize": 7.5, "color": GREY, "ha": "center", "va": "center", "style": "italic", **kw})


def fig1():
    fig, ax = plt.subplots(figsize=(9.6, 6.6), dpi=200)
    poly(ax, ENV, fc="#EAF2F6", ec="none")
    outline(ax, ENV, color=BLUE, lw=1.2, ls="--")
    poly(ax, Z["territorial_sea"], fc="#DCE9F0", ec="none")
    outline(ax, Z["territorial_sea"], color=BLUE, lw=0.8, ls=":")
    poly(ax, PROT, fc=SAGE, ec=GREEN, lw=0.6, alpha=0.85)
    poly(ax, LAND, fc=LANDC, ec=SLATE, lw=0.5)
    frame(ax, ENV, pad=4000)
    scalebar(ax, 20)
    ax.legend(handles=[Patch(fc=SAGE, ec=GREEN, label="Marine Natura 2000 sites (4,138 km²)"),
                       Patch(fc="#DCE9F0", ec=BLUE, ls=":", label="12 nautical miles: territorial sea (3,838 km²)"),
                       Patch(fc="#EAF2F6", ec=BLUE, ls="--", label="25 nm: Fisheries Management Zone (11,480 km²)")],
              frameon=False, fontsize=8, loc="upper left", bbox_to_anchor=(0.66, 0.98))
    ax.set_title("Malta’s marine protected sites and the zones used to measure them", fontsize=9.5, color=GREEN,
                 loc="left", fontweight="bold")
    ax.text(0, -0.03, "Every protected site lies inside the 25-nm line. Zones measured from the baselines (Marine Regions). "
            "Sources: EEA Natura 2000 (2024); Marine Regions; coastline © OpenStreetMap contributors.",
            transform=ax.transAxes, fontsize=7, color=GREY)
    fig.savefig(OUT / "fig1_map.png", bbox_inches="tight", facecolor="white")


def fig2(G):
    """Zoomed out: all the waters Malta reports to the EU, and which part is protected."""
    unprot = WATERS.difference(PROT)
    fig, ax = plt.subplots(figsize=(9.6, 6.4), dpi=200)
    neighbours(ax, G)
    poly(ax, unprot, fc=REDPALE, ec="none", zorder=2)
    holes(ax, unprot, "white")
    poly(ax, PROT, fc=SAGE, ec=GREEN, lw=0.5, zorder=3)
    outline(ax, WATERS, color=RED, lw=1.0, zorder=4)
    outline(ax, Z["eez"], color=ORANGE, lw=1.1, ls=(0, (4, 2)), zorder=4)
    outline(ax, ENV, color=BLUE, lw=1.1, ls="--", zorder=4)
    poly(ax, LAND, fc=LANDC, ec=SLATE, lw=0.4, zorder=5)
    frame(ax, WATERS)
    scalebar(ax, 50)
    beyond = CHK["EU-reported marine waters beyond 25 nm"]
    x, y = P(16.3, 34.95)
    ax.text(x, y, f"No marine protected site\nbeyond 25 nautical miles:\nabout {beyond / 1000:.0f},000 km², "
            f"{100 * beyond / 75715:.0f}% of the\nwaters Malta reports to the EU", ha="center", va="center",
            fontsize=10, color=RED, fontweight="bold", zorder=6)
    label(ax, 14.95, 36.62, "Sicily")
    halo = {"bbox": {"fc": "white", "ec": "none", "alpha": 0.8, "pad": 0.6}, "zorder": 7}
    label(ax, 12.47, 35.40, "Lampedusa", ha="left", **halo)
    label(ax, 12.86, 35.95, "Linosa", **halo)
    ax.legend(handles=[Patch(fc=SAGE, ec=GREEN, label="Marine Natura 2000 sites: 4,138 km² (5.5%)"),
                       Patch(fc=REDPALE, ec="none", label="Not in any marine protected site: about 71,600 km² (94.5%)"),
                       Line2D([], [], color=RED, lw=1.0, label="Waters Malta reports to the EU (75,715 km²)"),
                       Line2D([], [], color=ORANGE, lw=1.1, ls=(0, (4, 2)),
                              label="Exclusive economic zone as mapped by Marine Regions (52,923 km²)"),
                       Line2D([], [], color=BLUE, lw=1.1, ls="--", label="25 nm: Fisheries Management Zone (11,480 km²)")],
              frameon=False, fontsize=8.6, loc="upper right", bbox_to_anchor=(1.02, 1.02))
    ax.set_title("Zooming out: the waters Malta reports to the EU, and the part that is protected", fontsize=9.5,
                 color=GREEN, loc="left", fontweight="bold")
    ax.text(0, -0.03, "EU-reported waters: EEA ‘Marine waters used in MSFD’ (map-service outline, simplified), where Malta’s "
            "area is labelled ‘Area designated for hydrocarbon exploration and exploitation’.\nSources: EEA (2020, 2024); "
            "Marine Regions EEZ v12; depth grid EMODnet via EEA; coastline © OpenStreetMap contributors.",
            transform=ax.transAxes, fontsize=7, color=GREY, va="top")
    fig.savefig(OUT / "fig2_wide_map.png", bbox_inches="tight", facecolor="white")


def fig3(G):
    """One protected area, three reference areas: small multiples on the same frame."""
    panels = [("Fisheries Management Zone", "11,480 km² · within 25 nm", ENV, 36.0, BLUE, "--"),
              ("Exclusive economic zone", "52,923 km² · as mapped internationally", Z["eez"], 7.8, ORANGE, (0, (4, 2))),
              ("Waters reported to the EU", "75,715 km² · basis for EU reporting", WATERS, 5.5, RED, "-")]
    fig = plt.figure(figsize=(9.6, 3.2), dpi=200)
    for i, (title, sub, zone, pct, col, ls) in enumerate(panels):
        ax = fig.add_axes([i / 3 + 0.005, 0.27, 1 / 3 - 0.01, 0.56])
        neighbours(ax, G)
        un = zone.difference(PROT)
        poly(ax, un, fc=REDPALE, ec="none", zorder=2)
        holes(ax, un, "white")
        poly(ax, PROT.intersection(zone.buffer(500)), fc=SAGE, ec=GREEN, lw=0.3, zorder=3)
        outline(ax, zone, color=col, lw=1.0, ls=ls, zorder=4)
        poly(ax, LAND, fc=LANDC, ec=SLATE, lw=0.3, zorder=5)
        frame(ax, WATERS, pad=6000)
        ax.text(0.5, 1.15, title, transform=ax.transAxes, ha="center", fontsize=11, fontweight="bold", color=SLATE)
        ax.text(0.5, 1.04, sub, transform=ax.transAxes, ha="center", fontsize=8.6, color=GREY)
        # progress bar against the 30% target
        bx = fig.add_axes([i / 3 + 0.04, 0.07, 1 / 3 - 0.08, 0.055])
        bx.barh([0], [100], color="#EEF0F1", height=1)
        bx.barh([0], [pct], color=SAGE, ec=GREEN, lw=0.4, height=1)
        bx.axvline(30, color=AMBER, lw=1.6)
        bx.set_xlim(0, 100), bx.set_ylim(-0.5, 0.5), bx.axis("off")
        bx.text(0, 0.9, f"{pct:.1f}% protected", va="bottom", ha="left", fontsize=11, fontweight="bold", color=SLATE)
        bx.text(30, -0.8, "30% target", ha="center", va="top", fontsize=8, color=AMBER)
    fig.text(0.005, 1.0, "The same 4,138 km² of protected sea, measured against three reference areas", fontsize=9.5,
             color=GREEN, fontweight="bold", va="top")
    fig.savefig(OUT / "fig3_three_areas.png", bbox_inches="tight", facecolor="white")


def fig4(G):
    """Depth bands across Malta's waters, and how much of each is protected."""
    GX, GY, dep = G
    import shapely
    shapely.prepare(WATERS)
    inside = shapely.contains_xy(WATERS, GX, GY)
    cls = np.full(dep.shape, np.nan)
    for i, (lo, hi) in enumerate([(-1e4, 200), (200, 1000), (1000, 1e5)]):
        cls[inside & (dep >= lo) & (dep < hi)] = i
    fig = plt.figure(figsize=(9.6, 6.6), dpi=200)
    ax = fig.add_axes([0, 0.25, 1, 0.71])
    neighbours(ax, G)
    from matplotlib.colors import ListedColormap
    ax.pcolormesh(GX, GY, np.ma.masked_invalid(cls), cmap=ListedColormap(DEPTHC), vmin=-0.5, vmax=2.5,
                  shading="auto", zorder=2, rasterized=True)
    poly(ax, PROT, fc="none", ec=GREEN, lw=1.0, hatch="////", zorder=3)
    outline(ax, WATERS, color=RED, lw=0.9, zorder=4)
    outline(ax, ENV, color=BLUE, lw=1.0, ls="--", zorder=4)
    poly(ax, LAND, fc=LANDC, ec=SLATE, lw=0.4, zorder=5)
    frame(ax, WATERS)
    scalebar(ax, 50)
    label(ax, 14.95, 36.62, "Sicily")
    ax.legend(handles=[Patch(fc=DEPTHC[0], label="Shelf, 0–200 m"), Patch(fc=DEPTHC[1], label="Slope, 200–1,000 m"),
                       Patch(fc=DEPTHC[2], label="Deep sea, over 1,000 m"),
                       Patch(fc="none", ec=GREEN, hatch="////", label="Marine Natura 2000 sites"),
                       Line2D([], [], color=BLUE, lw=1.0, ls="--", label="25 nm"),
                       Line2D([], [], color=RED, lw=0.9, label="Waters reported to the EU")],
              frameon=False, fontsize=8.6, loc="upper right", bbox_to_anchor=(1.02, 1.02), ncol=2)
    fig.text(0.005, 0.995, "Which kinds of sea are protected: depth bands across the waters Malta reports to the EU",
             fontsize=9.5, color=GREEN, fontweight="bold", va="top")
    # bars: share of each depth band protected
    rows = [r for r in DEP if r["zone"].startswith("All waters")]
    bx = fig.add_axes([0.3, 0.04, 0.6, 0.18])
    y = np.arange(len(rows))[::-1]
    pct = [float(r["protected_pct"]) for r in rows]
    bx.barh(y, [100] * len(rows), color="#EEF0F1", height=0.62)
    bx.barh(y, pct, color=DEPTHC, height=0.62, ec=SLATE, lw=0.3)
    for yy, r, p in zip(y, rows, pct):
        bx.text(-1.5, yy, f"{r['depth_band'].replace('-', '–')}\n{int(r['area_km2']):,} km² ({r['share_of_zone_pct']}% of the waters)",
                ha="right", va="center", fontsize=9, color=SLATE)
        bx.text(p + 1.2, yy, f"{p:.1f}% protected", ha="left", va="center", fontsize=10, fontweight="bold", color=SLATE)
    bx.set_xlim(0, 100), bx.set_ylim(-0.6, len(rows) - 0.4), bx.axis("off")
    fig.text(0.005, 0.0, "Depth: EMODnet Bathymetry grid via the EEA image service (cells of about 200 m). Areas include "
             "internal waters. Sources: EEA Natura 2000 (2024); EEA marine waters (2020); Marine Regions.",
             fontsize=7, color=GREY)
    fig.savefig(OUT / "fig4_depth.png", bbox_inches="tight", facecolor="white")


G = grid()
fig1()
fig2(G)
fig3(G)
fig4(G)
print("figures in", OUT)
