"""Figures for Claim Check 017, drawn from data/cc-017/ and docs/data/geo.json (run fetch_data.py first).

Figure 3 (v1.2, the Marsaxlokk Bay map) also needs fetch_bay.py's out/ files: the EMODnet depth grid and the UNEP-WCMC
seagrass polygons, which are not committed (the UNEP-WCMC licence does not allow redistribution)."""
import csv, json, math, pathlib
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from matplotlib.colors import ListedColormap
from matplotlib.lines import Line2D
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


def fig3():
    """Marsaxlokk Bay: depth, mapped Posidonia, Natura 2000 sites and the new land at Terminal 2."""
    import pyproj, rasterio
    from rasterio.warp import transform_bounds
    from scipy import ndimage
    from shapely import make_valid
    from shapely.geometry import box, shape
    from shapely.ops import transform, unary_union
    P = pyproj.Transformer.from_crs(4326, 32633, always_xy=True).transform
    S = {r["item"]: r for r in csv.DictReader(open(D / "bay_stats.csv"))}

    def polys(ax, g, **kw):
        for p in getattr(g, "geoms", [g]):
            if p.geom_type == "Polygon" and not p.is_empty:
                ax.add_patch(Polygon(np.asarray(p.exterior.coords), closed=True, **kw))

    def lines(ax, g, **kw):
        for p in getattr(g, "geoms", [g]):
            if p.geom_type == "Polygon":
                x, y = p.exterior.xy
                ax.plot(x, y, **kw)

    geo = json.load(open(ROOT / "docs" / "data" / "geo.json"))
    o = geo["origin"]
    k = 111320 * math.cos(math.radians(o["lat"]))
    isl = [i for i in geo["islands"] if i["name"] == "Malta"][0]
    r = isl["detail"]
    land = np.array([P(o["lon"] + r[i] / k, o["lat"] + r[i + 1] / 110574) for i in range(0, len(r) - 1, 2)])
    with rasterio.open(OUT / "bathymetry_bay.tif") as s:
        a = s.read(1).astype(float)
        H, W = a.shape
        lon = s.bounds.left + (np.arange(W) + 0.5) * s.res[0]
        lat = s.bounds.top - (np.arange(H) + 0.5) * s.res[1]
    GX, GY = P(*np.meshgrid(lon, lat))
    dep = np.where(a < 0, -a, np.nan)
    wc = json.load(open(OUT / "seagrass_wcmc_bay.geojson"))["features"]
    sg = unary_union([make_valid(transform(P, shape(f["geometry"]))) for f in wc
                      if f["properties"]["scientific"] == "Posidonia oceanica"])
    em = unary_union([make_valid(transform(P, shape(f["geometry"])))
                      for f in json.load(open(D / "seagrass_emodnet_bay.geojson"))["features"]])
    n2k = [(f["properties"], make_valid(transform(P, shape(f["geometry"]))))
           for f in json.load(open(D / "natura2000_bay.geojson"))["features"]]
    # new land at Terminal 2 (as distances.py)
    minx, _, _, maxy = transform_bounds("EPSG:4326", "EPSG:32633", 14.515, 35.805, 14.555, 35.835)
    x0, y0 = minx + 180 * 10, maxy - 110 * 10
    m23 = np.loadtxt(D / "s2_mask_2023.csv", delimiter=",")
    m26 = np.loadtxt(D / "s2_mask_2026.csv", delimiter=",")
    lab, n = ndimage.label((m26 == 1) & (m23 == 0))
    keep = [i for i in range(1, n + 1) if (lab == i).sum() >= 20]
    rr, cc = np.nonzero(np.isin(lab, keep))
    new = unary_union([box(x0 + j * 10, y0 - (i + 1) * 10, x0 + (j + 1) * 10, y0 - i * 10) for i, j in zip(rr, cc)])

    fig, ax = plt.subplots(figsize=(9.6, 7.6), dpi=220)
    bands = [0, 10, 20, 30, 50, 1000]
    cols = ["#E6EFF5", "#C7DBE8", "#A2C2D7", "#759FBD", "#4A7A9C"]
    ax.set_facecolor("white")
    ax.contourf(GX, GY, dep, levels=bands, colors=cols, zorder=1)
    cs = ax.contour(GX, GY, dep, levels=[10, 20, 30, 50], colors=[SLATE], linewidths=0.45, zorder=2)
    X0, Y0 = P(14.512, 35.799)
    X1, Y1 = P(14.594, 35.853)
    for tx in ax.clabel(cs, fmt=lambda v: f"{v:.0f} m", fontsize=7.5, inline=True):
        x, y = tx.get_position()
        if x < X0 + 900 or y < Y0 + 300 or x > X1 - 200 or y > Y1 - 200:  # crowded at the frame edges
            tx.remove()
    polys(ax, sg, fc=SAGE, ec=GREEN, lw=0.4, alpha=0.95, zorder=3)
    lines(ax, em, color=GREEN, lw=0.9, ls=(0, (1.2, 1.4)), zorder=4)
    ax.add_patch(Polygon(land, closed=True, fc="#EDE9DF", ec=SLATE, lw=0.6, zorder=5))
    for prop, g in n2k:
        ls = "-" if prop["type"] == "SAC" else (0, (4, 2))
        lines(ax, g, color=RED, lw=1.1, ls=ls, zorder=6)
    polys(ax, new, fc=ORANGE, ec=ORANGE, lw=0.6, zorder=7)
    ax.set_xlim(X0, X1)
    ax.set_ylim(Y0, Y1)
    ax.set_aspect("equal")
    ax.set_xticks([]), ax.set_yticks([])
    for s in ax.spines.values():
        s.set_visible(False)

    def lab_(lon, lat, text, **kw):
        x, y = P(lon, lat)
        ax.text(x, y, text, **{"fontsize": 8.5, "color": SLATE, "ha": "center", "va": "center", "zorder": 9, **kw})
    lab_(14.5235, 35.8300, "Birżebbuġa", fontweight="bold")
    lab_(14.5445, 35.8465, "Marsaxlokk", fontweight="bold")
    lab_(14.5640, 35.8290, "Delimara", fontweight="bold")
    lab_(14.5455, 35.8262, "Marsaxlokk Bay", style="italic", color=BLUE, fontsize=8.5)
    lab_(14.5290, 35.8165, "Malta\nFreeport", fontweight="bold")
    big = max(getattr(new, "geoms", [new]), key=lambda g: g.area)
    nx, ny = big.centroid.x, big.centroid.y
    ax.annotate("New land at Terminal 2,\n2023–2026 (3.3 ha)", (nx, ny), P(14.5140, 35.8225), fontsize=8.5,
                color=ORANGE, fontweight="bold", ha="left", va="center", zorder=9,
                arrowprops={"arrowstyle": "-", "color": ORANGE, "lw": 0.9})
    lab_(14.5420, 35.8010, "Marine SPA MT0000111", color="white", fontsize=8, style="italic")
    lab_(14.5880, 35.8300, "Marine SPA\nMT0000108", color="white", fontsize=8, style="italic")
    lab_(14.5195, 35.8125, "Cliffs: SAC MT0000024,\nSPA MT0000033", color=RED, fontsize=7.5, style="italic")
    for prop, g in n2k:
        if prop["type"] == "SAC" and prop["sitecode"] in ("MT0000014", "MT0000011", "MT0000035"):
            c = g.representative_point()
            if X0 < c.x < X1 and Y0 < c.y < Y1:
                name = {"MT0000014": "Il-Ballut SAC", "MT0000011": "Għar Dalam SAC",
                        "MT0000035": "Ħas-Saptan SAC"}[prop["sitecode"]]
                ax.text(g.bounds[2] + 60, c.y, name, fontsize=7.5, color=RED, style="italic", va="center",
                        zorder=9)
    x, y = P(14.5145, 35.8012)
    ax.plot([x, x + 1000], [y, y], color=SLATE, lw=2, solid_capstyle="butt", zorder=9)
    ax.text(x + 500, y + 60, "1 km", ha="center", va="bottom", fontsize=7.5, color=SLATE, zorder=9)
    h = [Patch(fc=c, label=l) for c, l in zip(cols, ["Sea 0–10 m deep", "10–20 m", "20–30 m", "30–50 m",
                                                    "over 50 m"])]
    h += [Patch(fc="white", ec=GREY, lw=0.5, label="No depth in the grid")]
    h += [Patch(fc=SAGE, ec=GREEN, label="Posidonia mapped by UNEP-WCMC v7.1"),
          Line2D([], [], color=GREEN, lw=0.9, ls=(0, (1.2, 1.4)), label="Posidonia, EMODnet Seabed Habitats (gridded)"),
          Line2D([], [], color=RED, lw=1.1, label="Natura 2000: Habitats Directive (SAC)"),
          Line2D([], [], color=RED, lw=1.1, ls=(0, (4, 2)), label="Natura 2000: Birds Directive (SPA)"),
          Patch(fc=ORANGE, label="New land at Terminal 2, 2023–2026")]
    ax.legend(handles=h, frameon=False, fontsize=8.6, loc="upper left", bbox_to_anchor=(-0.01, -0.01), ncol=3,
              columnspacing=1.4, handlelength=1.8)
    fig.text(0.125, 0.905, "Marsaxlokk Bay: sea depth, mapped seagrass and protected sites around the Freeport",
             fontsize=9.5, color=GREEN, fontweight="bold")
    d1 = S["Depth of the sea within 1 km of the new land: 10th / 50th / 90th percentile"]["value"].split(" / ")
    sg1 = S["Mapped P. oceanica within 1 km of the new land: UNEP-WCMC v7.1, all P. oceanica"]["value"]
    dsg = S["Shortest distance, new land to mapped P. oceanica: UNEP-WCMC v7.1, all P. oceanica"]["value"]
    ax.text(0, -0.168, f"Within 1 km of the new land the sea is mostly {d1[0]}–{d1[2]} m deep (median {d1[1]} m), "
             f"with {float(sg1):.0f} ha of mapped Posidonia; the nearest mapped meadow is {float(dsg):.1f} km away.",
             fontsize=8.6, color=SLATE, transform=ax.transAxes)
    ax.text(0, -0.19, "Seagrass: UNEP-WCMC, Short F.T. (2021), Global Distribution of Seagrasses v7.1, "
             "www.unep-wcmc.org (survey dates 1961–2014; not redistributed); EMODnet Seabed Habitats (2025).\nDepth: "
             "EMODnet Bathymetry DTM 2024 (cells of about 100 m). Natura 2000: EEA (2024). New land: Copernicus "
             "Sentinel-2. Coastline © OpenStreetMap contributors.", fontsize=7, color=GREY, va="top",
            transform=ax.transAxes)
    fig.savefig(OUT / "fig3_bay.png", bbox_inches="tight", facecolor="white")


if __name__ == "__main__":
    import sys
    for name in sys.argv[1:] or ["fig1", "fig2", "fig3"]:
        globals()[name]()
    print("figures in", OUT)
