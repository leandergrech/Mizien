"""Figures for Claim Check 051 (run fetch_data.py and calc.py first). Needs shapely, pyproj."""
import csv, json, math, pathlib, urllib.parse, urllib.request
import pyproj
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from matplotlib.patches import Patch
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
                     "ytick.color": "#2B3A42"})
GREEN, SAGE, AMBER, RED, SLATE, GREY, ORANGE, BLUE = ("#14452F", "#7FA88B", "#E3A72F", "#B5483A", "#2B3A42",
                                                      "#8A9399", "#D9772B", "#3C6E8F")
P = pyproj.Transformer.from_crs(4326, 32633, always_xy=True).transform
N2K = "https://bio.discomap.eea.europa.eu/arcgis/rest/services/ProtectedSites/Natura2000Sites/MapServer"


def poly(ax, g, **kw):
    for p in getattr(g, "geoms", [g]):
        x, y = p.exterior.xy
        ax.fill(x, y, **kw)


def fig1():
    geo = json.load(open(ROOT / "docs" / "data" / "geo.json"))
    o = geo["origin"]
    k = 111320 * math.cos(math.radians(o["lat"]))
    land = unary_union([transform(P, Polygon([(o["lon"] + r[i] / k, o["lat"] + r[i + 1] / 110574)
                                              for i in range(0, len(r) - 1, 2)])).buffer(0) for isl in geo["islands"]
                        for r in [isl["coarse"]]])
    codes = [r["sitecode"] for r in csv.DictReader(open(D / "natura2000_marine.csv"))
             if r["sitecode"] != "UNION" and float(r["sea_km2"] or 0) >= 1]
    gs = []
    for layer in (0, 1):
        q = urllib.parse.urlencode({"where": "MS='MT'", "outFields": "SITECODE", "returnGeometry": "true", "outSR": 4326,
                                    "f": "geojson"})
        for ft in json.load(urllib.request.urlopen(f"{N2K}/{layer}/query?{q}", timeout=180))["features"]:
            if ft["properties"]["SITECODE"] in codes:
                gs.append(transform(P, shape(ft["geometry"])).buffer(0))
    prot = unary_union(gs).difference(land)
    fig, ax = plt.subplots(figsize=(9.6, 6.6), dpi=200)
    poly(ax, land.buffer(25 * 1852, resolution=48), fc="#EAF2F6", ec=BLUE, lw=1.2, ls="--")
    poly(ax, land.buffer(12 * 1852, resolution=48), fc="#DCE9F0", ec=BLUE, lw=0.8, ls=":")
    poly(ax, prot, fc=SAGE, ec=GREEN, lw=0.6, alpha=0.85)
    poly(ax, land, fc="#C9C3B4", ec=SLATE, lw=0.5)
    ax.set_aspect("equal")
    ax.set_xticks([]), ax.set_yticks([])
    for s in ax.spines.values():
        s.set_visible(False)
    ax.legend(handles=[Patch(fc=SAGE, ec=GREEN, label="Marine Natura 2000 sites (4,138 km²)"),
                       Patch(fc="#DCE9F0", ec=BLUE, ls=":", label="12 nautical miles (territorial sea, approx.)"),
                       Patch(fc="#EAF2F6", ec=BLUE, ls="--", label="25 nm: Fisheries Management Zone (~11,480 km²)")],
              frameon=False, fontsize=8, loc="upper left", bbox_to_anchor=(0.66, 0.98))
    ax.set_title("Malta’s marine protected sites and the zones used to measure them", fontsize=9.5, color=GREEN,
                 loc="left", fontweight="bold")
    ax.text(0, -0.03, "The area Malta reports to the EU (about 75,700 km², up to 200 nm) extends far beyond this frame. "
            "Sources: EEA Natura 2000 (2024); coastline © OpenStreetMap contributors.", transform=ax.transAxes,
            fontsize=7, color=GREY)
    fig.savefig(OUT / "fig1_map.png", bbox_inches="tight", facecolor="white")


def fig2():
    C = [r for r in csv.DictReader(open(D / "checks.csv")) if r["check"].startswith("Protected share")]
    labs = ["Fisheries\nManagement Zone\n(11,480 km²)", "EEZ as mapped\ninternationally\n(~52,900 km²)",
            "Marine waters\nreported to the EU\n(75,715 km²)"]
    vals = [float(r["value"]) for r in C]
    fig, ax = plt.subplots(figsize=(9.6, 3.6), dpi=220)
    b = ax.bar(labs, vals, color=[GREEN, ORANGE, RED], width=0.55)
    for r, v in zip(b, vals):
        ax.text(r.get_x() + r.get_width() / 2, v + 1, f"{v:.1f}%", ha="center", fontsize=11, fontweight="bold", color=SLATE)
    ax.axhline(30, color=AMBER, ls="--", lw=1.4)
    ax.text(2.35, 31, "EU 2030 target: 30%", fontsize=8, color=AMBER, ha="right")
    ax.set_ylim(0, 45)
    ax.set_ylabel("% protected")
    ax.set_title("The same 4,138 km² of protected sea, divided by three reference areas", fontsize=9.5, color=GREEN,
                 loc="left", fontweight="bold")
    fig.savefig(OUT / "fig2_denominators.png", bbox_inches="tight", facecolor="white")


fig1()
fig2()
print("figures in", OUT)
