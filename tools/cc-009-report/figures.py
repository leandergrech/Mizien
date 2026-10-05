"""Figures for Claim Check 009 (v1.2). Run fetch_data.py and data/cc-009/calc.py first.

out/fig1_wsc_sources.png   WSC potable-water production by source, 2022-2025 (data/cc-009/wsc_production.csv)
out/fig2_abstraction.png   national fresh groundwater abstraction by sector, 2015-2024, with estimated recharge
                           (data/cc-009/eurostat_water.csv)
out/fig3_gwb_map.png       groundwater bodies by quantitative status, 3rd-cycle EU reporting
                           (data/cc-009/wise_gwb_2022.geojson; island outlines from docs/data/geo.json)
"""
import csv
import json
import math
import pathlib

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import pyproj  # noqa: E402
from matplotlib import font_manager as fm  # noqa: E402
from matplotlib.lines import Line2D  # noqa: E402
from matplotlib.patches import Patch  # noqa: E402
from shapely.geometry import Polygon, shape  # noqa: E402
from shapely.ops import transform  # noqa: E402

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[1]
D = ROOT / "data" / "cc-009"
OUT = HERE / "out"
OUT.mkdir(exist_ok=True)
for f in ["LiberationSans-Regular", "LiberationSans-Bold", "LiberationSans-Italic"]:
    fm.fontManager.addfont(f"/usr/share/fonts/truetype/liberation/{f}.ttf")
plt.rcParams.update({"font.family": "Liberation Sans", "axes.spines.top": False, "axes.spines.right": False,
                     "axes.edgecolor": "#8A9399", "axes.labelcolor": "#2B3A42", "xtick.color": "#2B3A42",
                     "ytick.color": "#2B3A42"})
GREEN, SAGE, AMBER, RED, SLATE, GREY, ORANGE, BLUE = ("#14452F", "#7FA88B", "#E3A72F", "#B5483A", "#2B3A42",
                                                      "#8A9399", "#D9772B", "#3C6E8F")
LIGHT = "#C9D0D4"


def title(ax, t):
    ax.set_title(t, fontsize=10.5, color=GREEN, loc="left", fontweight="bold", pad=10)


def fig1():
    rows = list(csv.DictReader(open(D / "wsc_production.csv")))
    yrs = [int(r["year"]) for r in rows]
    ro = [int(r["ro_m3"]) / 1e6 for r in rows]
    gw = [int(r["groundwater_m3"]) / 1e6 for r in rows]
    fig, ax = plt.subplots(figsize=(8.0, 3.9), dpi=220)
    ax.bar(yrs, gw, width=0.62, color=SAGE, label="Groundwater", zorder=2)
    ax.bar(yrs, ro, width=0.62, bottom=gw, color=BLUE, label="Reverse osmosis (seawater)", zorder=2)
    for y, g, r in zip(yrs, gw, ro):
        ax.text(y, g / 2, f"{g:.1f}", ha="center", va="center", color="white", fontsize=9, fontweight="bold")
        ax.text(y, g + r / 2, f"{r:.1f}", ha="center", va="center", color="white", fontsize=9, fontweight="bold")
        ax.text(y, g + r + 0.8, f"RO {100 * r / (g + r):.1f}%", ha="center", va="bottom", color=SLATE, fontsize=9,
                fontweight="bold")
    ax.set_xticks(yrs)
    ax.set_ylim(0, 47)
    ax.set_ylabel("Million m³ a year")
    ax.grid(axis="y", color="#E3E7E5", lw=0.6, zorder=0)
    ax.legend(frameon=False, fontsize=8.5, loc="upper left", ncol=2)
    title(ax, "WSC potable-water production by source")
    fig.text(0.01, -0.02, "Source: WSC Annual Report 2025, Figure 20 (values transcribed; data/cc-009/wsc_production.csv). "
             "WSC production only, not national abstraction.", fontsize=7.4, color=GREY)
    fig.savefig(OUT / "fig1_wsc_sources.png", bbox_inches="tight", facecolor="white")


def fig2():
    es = {}
    for r in csv.DictReader(open(D / "eurostat_water.csv")):
        es[(r["wat_proc"], int(r["year"]))] = float(r["value"])
    yrs = list(range(2015, 2025))
    tot = [es[("ABST", y)] for y in yrs]
    agr = [es[("ABS_AGR", y)] for y in yrs]
    oth = [sum(es.get((c, y), 0) for c in ("ABS_HH", "ABS_IND", "ABS_SER", "ABS_MIN")) for y in yrs]
    fig, ax = plt.subplots(figsize=(8.0, 4.4), dpi=220)
    for i, y in enumerate(yrs):
        pws = es.get(("ABS_PWS", y))
        ax.bar(y, agr[i], width=0.66, color=AMBER, zorder=2)
        if pws is None:  # 2021: public-supply value not published; show the remainder, hatched
            ax.bar(y, tot[i] - agr[i] - oth[i], bottom=agr[i], width=0.66, facecolor="white", edgecolor=BLUE,
                   hatch="////", lw=0.8, zorder=2)
            pws = tot[i] - agr[i] - oth[i]
        else:
            ax.bar(y, pws, bottom=agr[i], width=0.66, color=BLUE, zorder=2)
        ax.bar(y, oth[i], bottom=agr[i] + pws, width=0.66, color=LIGHT, zorder=2)
    ax.text(2015, tot[0] + 0.6, f"{tot[0]:.1f}", ha="center", va="bottom", fontsize=8.4, color=SLATE, fontweight="bold")
    ax.text(2024.4, tot[-1], f"{tot[-1]:.1f}", ha="left", va="center", fontsize=8.4, color=SLATE, fontweight="bold")
    rch = [es[("AQUI", y)] for y in yrs]
    ax.plot(yrs, rch, color=GREEN, lw=2.2, marker="o", ms=4.5, zorder=4)
    ax.text(2024.4, rch[-1] + 1.8, f"{rch[-1]:.1f}", ha="left", va="center", fontsize=8.4, color=GREEN, fontweight="bold")
    ax.axhline(37, color=SLATE, lw=1.2, ls=(0, (2, 2)), zorder=3)
    ax.set_xticks(yrs)
    ax.set_ylim(0, 72)
    ax.set_xlim(2014.4, 2025.1)
    ax.set_ylabel("Million m³ a year")
    ax.grid(axis="y", color="#E3E7E5", lw=0.6, zorder=0)
    handles = [Line2D([], [], color=GREEN, lw=2.2, marker="o", ms=4.5, label="Estimated recharge into the aquifers"),
               Patch(color=AMBER, label="Agriculture"), Patch(color=BLUE, label="Public water supply"),
               Line2D([], [], color=SLATE, lw=1.2, ls=(0, (2, 2)), label="Available for abstraction (long-term, Sapiano 2020)"),
               Patch(color=LIGHT, label="Households, industry, services"),
               Patch(facecolor="white", edgecolor=BLUE, hatch="////", label="Public supply, not published (2021)")]
    ax.legend(handles=handles, frameon=False, fontsize=7.8, loc="upper center", bbox_to_anchor=(0.5, -0.08), ncol=2,
              handlelength=1.8, columnspacing=1.6)
    title(ax, "Malta: fresh groundwater abstraction by user, and estimated recharge")
    fig.text(0.01, -0.17, "Source: Eurostat env_wat_abs (updated 16 Sep 2026) and env_wat_res (updated 3 Jul 2026), "
             "retrieved 5 Oct 2026; all values flagged as estimates.\nThe 37 million m³ line is the published long-term "
             "average from Sapiano (2020), Table 1: recharge less natural discharge to the sea and unrecoverable runoff.",
             fontsize=7.2, color=GREY)
    fig.savefig(OUT / "fig2_abstraction.png", bbox_inches="tight", facecolor="white")


def fig3():
    P = pyproj.Transformer.from_crs(4326, 32633, always_xy=True).transform
    g = json.load(open(D / "wise_gwb_2022.geojson"))
    geo = json.load(open(ROOT / "docs" / "data" / "geo.json"))
    o = geo["origin"]
    k = 111320 * math.cos(math.radians(o["lat"]))
    land = [transform(P, Polygon([(o["lon"] + r[i] / k, o["lat"] + r[i + 1] / 110574) for i in range(0, len(r) - 1, 2)]))
            for isl in geo["islands"] for r in [isl.get("detail") or isl["coarse"]]]
    bodies = []
    for f in g["features"]:
        p = f["properties"]
        bodies.append((p["euGroundWaterBodyCode"], p["groundWaterBodyName"].title(), int(p["gwQuantitativeStatusValue"]),
                       transform(P, shape(f["geometry"]))))
    lower = {"MT001", "MT005", "MT006", "MT009", "MT010", "MT012", "MT013"}  # sea-level and coastal bodies
    fig, axes = plt.subplots(1, 2, figsize=(9.0, 4.6), dpi=220)
    names = {"MT001": "Malta Mean\nSea Level", "MT013": "Gozo Mean\nSea Level", "MT005": "Pwales\nCoastal",
             "MT010": "Marfa\nCoastal"}
    for ax, group, t in ((axes[0], lower, "Sea-level and coastal aquifers"),
                         (axes[1], None, "Perched aquifers (above the clay)")):
        for poly in land:
            for q in getattr(poly, "geoms", [poly]):
                x, y = q.exterior.xy
                ax.fill(x, y, fc="#F1F2EE", ec=GREY, lw=0.5, zorder=1)
        for code, name, st, geom in bodies:
            if (group is not None) != (code in lower):
                continue
            for q in getattr(geom, "geoms", [geom]):
                x, y = q.exterior.xy
                ax.fill(x, y, fc=RED if st == 3 else SAGE, ec="white", lw=0.6, zorder=2, alpha=0.95)
        ax.set_aspect("equal")
        ax.axis("off")
        ax.set_title(t, fontsize=10.5, color=GREEN, loc="left", fontweight="bold")
    # labels for the poor bodies (left panel)
    ax = axes[0]
    for code, name, st, geom in bodies:
        if code in names:
            c = geom.representative_point()
            dx, dy = {"MT001": (0, -1500), "MT013": (0, 0), "MT005": (6500, 3200), "MT010": (-5200, -2600)}[code]
            ax.annotate(names[code], (c.x, c.y), (c.x + dx, c.y + dy), fontsize=8.8, color="white" if not dx else SLATE,
                        ha="center", va="center", fontweight="bold",
                        arrowprops=None if not dx else dict(arrowstyle="-", color=SLATE, lw=0.6))
    xmin = min(b[3].bounds[0] for b in bodies) - 1500
    xmax = max(b[3].bounds[2] for b in bodies) + 1500
    ymin = min(b[3].bounds[1] for b in bodies) - 1500
    ymax = max(b[3].bounds[3] for b in bodies) + 1500
    for a in axes:
        a.set_xlim(xmin, xmax)
        a.set_ylim(ymin, ymax)
    axes[1].plot([xmin + 1000, xmin + 11000], [ymin + 1200] * 2, color=SLATE, lw=1.5)
    axes[1].text(xmin + 6000, ymin + 1800, "10 km", ha="center", fontsize=8.6, color=SLATE)
    fig.legend(handles=[Patch(color=RED, label="Poor quantitative status"), Patch(color=SAGE, label="Good quantitative status")],
               frameon=False, fontsize=9.2, loc="lower center", ncol=2, bbox_to_anchor=(0.5, -0.02))
    fig.text(0.01, -0.09, "Source: EEA WISE, Malta's 3rd river basin management plan reporting (status assessed 2021), "
             "WFD2022_GroundWaterBody_WM, retrieved 5 Oct 2026.\nAll 15 bodies are in poor chemical status. Perched "
             "bodies lie above parts of the sea-level aquifers, so the two layers are drawn separately.\n"
             "Coastline © OpenStreetMap contributors.", fontsize=7.6, color=GREY)
    fig.tight_layout(w_pad=1.0)
    fig.savefig(OUT / "fig3_gwb_map.png", bbox_inches="tight", facecolor="white")


fig1()
fig2()
fig3()
print("figures in", OUT)
