"""Figures for Claim Check 008, drawn offline from data/cc-008/ (run fetch_data.py, then calc.py) and the Malta
outline in docs/data/geo.json. Output: out/fig1_no2_monthly.png, out/fig2_jan_sep.png, out/fig3_map.png"""
import csv
import datetime as dt
import json
import math
import pathlib

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from matplotlib.lines import Line2D
from matplotlib.patches import Rectangle

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[1]
D = ROOT / "data" / "cc-008"
OUT = HERE / "out"
OUT.mkdir(exist_ok=True)
for f in ["LiberationSans-Regular", "LiberationSans-Bold", "LiberationSans-Italic"]:
    fm.fontManager.addfont(f"/usr/share/fonts/truetype/liberation/{f}.ttf")
plt.rcParams.update({"font.family": "Liberation Sans", "axes.spines.top": False, "axes.spines.right": False,
                     "axes.edgecolor": "#8A9399", "axes.labelcolor": "#2B3A42", "xtick.color": "#2B3A42",
                     "ytick.color": "#2B3A42"})
GREEN, SAGE, AMBER, RED, SLATE, GREY, ORANGE, BLUE = ("#14452F", "#7FA88B", "#E3A72F", "#B5483A", "#2B3A42",
                                                      "#8A9399", "#D9772B", "#3C6E8F")
LANDC, SEA = "#E4E1D8", "#F4F8FA"
M = list(csv.DictReader(open(D / "no2_monthly.csv")))
JS = list(csv.DictReader(open(D / "no2_jan_sep.csv")))
ST = {r["station"]: r for r in csv.DictReader(open(D / "aq_stations.csv"))}
FLY = json.load(open(D / "flyovers_osm.geojson"))["features"]
OPEN = dt.date(2025, 12, 18)  # Msida Creek flyover opened to traffic (OPM release, 17 December 2025)
LAST = "2026-09"              # last complete month; October 2026 is partial and left out
SRC = ("Source: EEA air-quality download service, hourly NO₂ (E1a validated to 2025; E2a up-to-date, unvalidated, "
       "2026), retrieved 5 Oct 2026.")
SERIES = [("MT00005", "Msida, old point (traffic, 5 m from kerb), to 2023", ORANGE, "-", 2.4),
          ("MT00011", "Msida, new point (traffic, 9 m from kerb), from Jan 2024", RED, "-", 2.6),
          ("MT00009", "St Paul’s Bay (traffic)", BLUE, "-", 1.5),
          ("MT00004", "Żejtun (urban background)", GREY, "-", 1.5),
          ("MT00008", "Attard (urban background)", SAGE, "-", 1.5)]


def mx(month):
    y, m = map(int, month.split("-"))
    return y + (m - 0.5) / 12


def dx(d):
    return d.year + (d.timetuple().tm_yday - 0.5) / (366 if d.year % 4 == 0 else 365)


def fig1():
    fig, ax = plt.subplots(figsize=(9.6, 5.0), dpi=220)
    ax.axvspan(2026, mx(LAST) + 0.06, color="#EEF0F1", zorder=0)
    ax.text(2026.02, 47.3, "2026: up-to-date data,\nnot yet validated (E2a)", fontsize=7.8, color=SLATE, va="top")
    for code, label, col, ls, lw in SERIES:
        rows = [r for r in M if r["station"] == code and "2022-01" <= r["month"] <= LAST and r["no2_ugm3"]]
        good = [r for r in rows if float(r["coverage_pct"]) >= 75]
        low = [r for r in rows if float(r["coverage_pct"]) < 75]
        xs, ys = [mx(r["month"]) for r in rows], [float(r["no2_ugm3"]) for r in rows]
        ax.plot(xs, ys, color=col, lw=lw, ls=ls, label=label, zorder=4 if code.startswith("MT0001") else 3)
        ax.scatter([mx(r["month"]) for r in good], [float(r["no2_ugm3"]) for r in good], s=9, color=col, zorder=5)
        ax.scatter([mx(r["month"]) for r in low], [float(r["no2_ugm3"]) for r in low], s=26, facecolor="white",
                   edgecolor=col, lw=1.2, zorder=6)
    ax.axvline(dx(OPEN), color=GREEN, lw=1.4, ls="--", zorder=2)
    ax.text(dx(OPEN) - 0.03, 52.6, "Msida Creek flyover\nopens to traffic,\n18 Dec 2025", fontsize=8.2, color=GREEN,
            ha="right", va="top", fontweight="bold")
    ax.axvline(2024 + 0.5 / 12, color=SLATE, lw=0.8, ls=":", zorder=2)
    ax.text(2024 + 0.6 / 12, 52.6, "Sampling point changes, Jan 2024:\nthe new point is about 300 m east;\n"
            "the two series are not continuous", fontsize=8.2, color=SLATE, va="top")
    ax.set_xlim(2022, mx(LAST) + 0.08)
    ax.set_ylim(0, 53)
    ax.set_xticks([2022, 2023, 2024, 2025, 2026])
    ax.set_xticklabels(["Jan 2022", "Jan 2023", "Jan 2024", "Jan 2025", "Jan 2026"])
    ax.tick_params(labelsize=8.5)
    ax.set_ylabel("Monthly mean NO₂, µg/m³", fontsize=8.5)
    hl, lb = ax.get_legend_handles_labels()
    hl.append(Line2D([], [], ls="", marker="o", mfc="white", mec=SLATE, ms=5))
    lb.append("Month with under 75% of hours valid")
    ax.legend(hl, lb, frameon=False, fontsize=8.6, loc="upper left", bbox_to_anchor=(-0.01, -0.07), ncol=2,
              columnspacing=1.2)
    ax.set_title("Nitrogen dioxide at the Msida roadside monitor and three comparison stations, monthly, 2022–2026",
                 fontsize=9.5, color=GREEN, loc="left", fontweight="bold", pad=8)
    fig.text(0.01, -0.095, "Monthly means of valid hourly values. The annual limit value is 40 µg/m³; the EU limit from "
             "2030 is 20 µg/m³ (Directive (EU) 2024/2881).\n" + SRC, fontsize=7, color=GREY, va="top")
    fig.savefig(OUT / "fig1_no2_monthly.png", bbox_inches="tight", facecolor="white")


def fig2():
    names = [("MT00011", "Msida (new point)\ntraffic", RED), ("MT00009", "St Paul’s Bay\ntraffic", BLUE),
             ("MT00004", "Żejtun\nurban background", GREY), ("MT00008", "Attard\nurban background", SAGE)]
    yrs = [("2024", "#D9D2C3"), ("2025", "#A9A39A"), ("2026", None)]
    fig, ax = plt.subplots(figsize=(9.6, 3.6), dpi=220)
    w = 0.26
    for i, (code, lab, col) in enumerate(names):
        for j, (y, fc) in enumerate(yrs):
            r = next(r for r in JS if r["window"] == "Jan-Sep" and r["year"] == y and r["station"] == code)
            v = float(r["no2_ugm3"])
            x = i + (j - 1) * (w + 0.02)
            ax.bar(x, v, width=w, color=fc or col, ec="none", hatch="////" if y == "2026" else None,
                   alpha=1)
            if y == "2026":
                ax.bar(x, v, width=w, fc="none", ec="white", lw=0, hatch="////")
            ax.text(x, v + 0.4, f"{v:.1f}", ha="center", va="bottom", fontsize=8.3, color=SLATE,
                    fontweight="bold" if y == "2026" else "normal")
            ax.text(x, -1.6, y, ha="center", va="top", fontsize=7.6, color=GREY)
    ax.set_xticks(range(len(names)))
    ax.set_xticklabels([n[1] for n in names], fontsize=8.5)
    ax.tick_params(axis="x", length=0, pad=19)
    ax.set_ylim(0, 29)
    ax.set_ylabel("Mean NO₂, January–September, µg/m³", fontsize=8.5)
    ax.tick_params(axis="y", labelsize=8.5)
    ax.spines["bottom"].set_visible(False)
    m = {y: float(next(r for r in JS if r["window"] == "Jan-Sep" and r["year"] == y and r["station"] == "MT00011")
                  ["no2_ugm3"]) for y, _ in yrs}
    ax.annotate(f"{100 * (m['2026'] / m['2025'] - 1):+.0f}% on 2025", xy=(0 + w + 0.02, m["2026"] + 1.6),
                xytext=(0.62, 27.2), fontsize=8.5, color=RED, fontweight="bold", ha="left", va="center",
                arrowprops={"arrowstyle": "-", "color": RED, "lw": 0.7})
    ax.set_title("Mean NO₂, January to September: 2024 and 2025 before the flyover opened, 2026 after",
                 fontsize=9.5, color=GREEN, loc="left", fontweight="bold")
    fig.text(0.01, -0.1, "Grey bars: 2024 (light; Msida from 17 Jan) and 2025 (dark), validated. Coloured, hatched "
             "bars: 2026, unvalidated. September 2026 at Msida has 61% of hours valid.\n" + SRC, fontsize=7,
             color=GREY, va="top")
    fig.savefig(OUT / "fig2_jan_sep.png", bbox_inches="tight", facecolor="white")


geo = json.load(open(ROOT / "docs" / "data" / "geo.json"))
O = geo["origin"]
K = 111320 * math.cos(math.radians(O["lat"]))


def xy(lon, lat):
    return (lon - O["lon"]) * K, (lat - O["lat"]) * 110574


def land(ax, lw=0.5):
    for isl in geo["islands"]:
        r = isl.get("detail") or isl["coarse"]
        ax.fill(r[0::2], r[1::2], fc=LANDC, ec=GREY, lw=lw, zorder=1)


def frame(ax, lon0, lat0, lon1, lat1):
    x0, y0 = xy(lon0, lat0)
    x1, y1 = xy(lon1, lat1)
    ax.set_xlim(x0, x1)
    ax.set_ylim(y0, y1)
    ax.set_aspect("equal")
    ax.set_xticks([]), ax.set_yticks([])
    ax.set_facecolor(SEA)
    for s in ax.spines.values():
        s.set_visible(True)
        s.set_edgecolor(GREY)
        s.set_linewidth(0.6)
    return x0, y0, x1, y1


def station(ax, code, active, size=46, label=None, off=(0, 0), **kw):
    x, y = xy(float(ST[code]["lon"]), float(ST[code]["lat"]))
    ax.scatter([x], [y], s=size, marker="^", c=(RED if code in ("MT00005", "MT00011") else BLUE) if active else "white",
               ec=SLATE if active else (RED if code == "MT00005" else GREY), lw=1.1, zorder=6)
    if label:
        ax.annotate(label, xy=(x, y), xytext=(x + off[0], y + off[1]), zorder=7,
                    **{"fontsize": 9.2, "color": SLATE, "ha": "center", "va": "center",
                       "arrowprops": {"arrowstyle": "-", "color": GREY, "lw": 0.5},
                       "bbox": {"fc": "white", "ec": "none", "alpha": 0.85, "pad": 1.0}, **kw})


def fig3():
    fig = plt.figure(figsize=(9.6, 5.9), dpi=220)
    a1 = fig.add_axes([0.0, 0.08, 0.36, 0.84])
    a2 = fig.add_axes([0.38, 0.08, 0.62, 0.84])
    # overview
    land(a1, lw=0.4)
    frame(a1, 14.17, 35.80, 14.58, 36.09)
    for code, lab, off in [("MT00008", "Attard", (0, -1700)), ("MT00004", "Żejtun", (0, -1700)),
                           ("MT00009", "St Paul’s Bay", (-2400, 1500)), ("MT00007", "Għarb", (1500, -1500)),
                           ("MT00011", "Msida", (1500, 2200))]:
        station(a1, code, True, size=34, label=lab, off=off)
    station(a1, "MT00003", False, size=26)
    zx0, zy0 = xy(14.477, 35.872)
    zx1, zy1 = xy(14.519, 35.903)
    a1.add_patch(Rectangle((zx0, zy0), zx1 - zx0, zy1 - zy0, fill=False, ec=SLATE, lw=0.9, zorder=8))
    a1.text(0.0, 1.015, "All EEA-reported NO₂ stations in Malta", transform=a1.transAxes, fontsize=9, color=SLATE,
            fontweight="bold", va="bottom")
    # zoom
    land(a2, lw=0.7)
    frame(a2, 14.477, 35.872, 14.519, 35.903)
    for f_ in FLY:
        c = f_["geometry"]["coordinates"]
        a2.plot(*zip(*[xy(*p) for p in c]), color=GREEN, lw=3.2, solid_capstyle="round", zorder=4)
    fx, fy = xy(14.4882, 35.8965)
    a2.annotate("Msida Creek flyover\n(opened 18 Dec 2025)", xy=(fx, fy), xytext=(fx - 950, fy + 380), fontsize=9.6,
                color=GREEN, fontweight="bold", ha="center", va="center",
                arrowprops={"arrowstyle": "-", "color": GREEN, "lw": 0.7},
                bbox={"fc": "white", "ec": "none", "alpha": 0.85, "pad": 1.0}, zorder=7)
    mx_, my_ = xy(14.49449, 35.88289)
    a2.scatter([mx_], [my_], s=420, marker="o", fc="none", ec=GREEN, lw=1.6, ls="--", zorder=4)
    a2.annotate("Marsa Junction Project\n(completed 2021)", xy=(mx_, my_), xytext=(mx_ - 1050, my_ - 520),
                fontsize=9.6, color=GREEN, fontweight="bold", ha="center", va="center",
                arrowprops={"arrowstyle": "-", "color": GREEN, "lw": 0.7},
                bbox={"fc": "white", "ec": "none", "alpha": 0.85, "pad": 1.0}, zorder=7)
    station(a2, "MT00005", False, size=70, label="MT00005, old Msida point\nNO₂ data to Dec 2023; closed Feb 2024",
            off=(-200, -720))
    station(a2, "MT00011", True, size=70, label="MT00011, new Msida point\nfrom 17 Jan 2024; 300 m east",
            off=(1150, -420))
    station(a2, "MT00003", False, size=70, label="MT00003 Kordin (Paola)\nclosed end of 2016", off=(-200, 650))
    # scale bar 500 m
    x0, y0 = xy(14.4795, 35.8735)
    a2.plot([x0, x0 + 500], [y0, y0], color=SLATE, lw=2, solid_capstyle="butt", zorder=8)
    a2.text(x0 + 250, y0 + 70, "500 m", ha="center", fontsize=8.5, color=SLATE, zorder=8)
    a2.legend(handles=[Line2D([], [], ls="", marker="^", ms=7, mfc=RED, mec=SLATE, label="Msida monitor, operating"),
                       Line2D([], [], ls="", marker="^", ms=7, mfc=BLUE, mec=SLATE, label="Other station, operating"),
                       Line2D([], [], ls="", marker="^", ms=7, mfc="white", mec=GREY, label="Closed station"),
                       Line2D([], [], color=GREEN, lw=3, label="Flyover carriageways (OpenStreetMap)")],
              frameon=True, facecolor="white", edgecolor="none", framealpha=0.9, fontsize=9, loc="lower right")
    fig.text(0.0, 0.985, "Where NO₂ is measured near the Msida and Marsa junctions", fontsize=9.5, color=GREEN,
             fontweight="bold", va="top")
    fig.text(0.0, 0.06, "Station locations: ERA’s station metadata reported to the EEA (Eionet, dataset D, 2025). Marsa "
             "junction marked at the location used for this claim. No EEA-reported station has operated within\n"
             "1.4 km of the Marsa junction since Kordin closed in 2016. Coastline and flyover © OpenStreetMap "
             "contributors.", fontsize=7, color=GREY, va="top")
    fig.savefig(OUT / "fig3_map.png", bbox_inches="tight", facecolor="white")


fig1()
fig2()
fig3()
print("figures in", OUT)
