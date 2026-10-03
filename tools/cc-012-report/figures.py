"""Figures for Claim Check 012, drawn from data/cc-012/ (run fetch_s2.py and calc.py first)."""
import csv, pathlib
from datetime import date
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[1]
OUT = HERE / "out"
OUT.mkdir(exist_ok=True)
D = ROOT / "data" / "cc-012"
for f in ["LiberationSans-Regular", "LiberationSans-Bold", "LiberationSans-Italic"]:
    fm.fontManager.addfont(f"/usr/share/fonts/truetype/liberation/{f}.ttf")
plt.rcParams.update({"font.family": "Liberation Sans", "axes.spines.top": False, "axes.spines.right": False,
                     "axes.edgecolor": "#8A9399", "axes.labelcolor": "#2B3A42", "xtick.color": "#2B3A42",
                     "ytick.color": "#2B3A42"})
GREEN, SAGE, AMBER, RED, SLATE, GREY, ORANGE, BLUE = ("#14452F", "#7FA88B", "#E3A72F", "#B5483A", "#2B3A42",
                                                      "#8A9399", "#D9772B", "#3C6E8F")


def fig1():
    z = np.load(D / "rgb_crops.npz")
    zone, pr = z["zone"], z["poly_rc"]
    rs, cs = np.where(zone)
    r0, r1, c0, c1 = max(rs.min() - 25, 0), rs.max() + 25, max(cs.min() - 35, 0), cs.max() + 35
    fig, ax = plt.subplots(1, 2, figsize=(9.6, 4.2), dpi=220)
    for a, key in zip(ax, ("feb2025", "feb2026")):
        a.imshow(z[key][r0:r1, c0:c1], interpolation="nearest")
        a.contour(zone[r0:r1, c0:c1], levels=[0.5], colors=[AMBER], linewidths=1.4)
        a.plot(pr[:, 1] - c0, pr[:, 0] - r0, color="white", lw=0.8, ls="--")
        a.set_title(f"{str(z[key + '_date'])}", fontsize=9.5, color=GREEN, loc="left", fontweight="bold")
        a.set_xticks([]); a.set_yticks([])
        a.add_patch(matplotlib.patches.Rectangle((1.5, 1.5), 13, 6, color=SLATE, alpha=0.75))
        a.plot([3, 13], [6] * 2, color="white", lw=2)
        a.text(8, 4.2, "100 m", color="white", fontsize=7, ha="center", va="center")
    fig.text(0.01, -0.02, "Sentinel-2 true colour, 10 m pixels. Amber: gravel zone (surface brightened sharply between "
             "summer 2024 and summer 2025). Dashed: Ta’ Qali park polygon (OpenStreetMap). The National Stadium is to "
             "the west.\nContains modified Copernicus Sentinel data 2025–2026; © OpenStreetMap contributors.",
             fontsize=7, color=GREY)
    fig.tight_layout()
    fig.savefig(OUT / "fig1_map.png", bbox_inches="tight", facecolor="white")


def fig2():
    T = list(csv.DictReader(open(D / "ndvi_timeseries.csv")))
    d = [date.fromisoformat(r["date"]) for r in T]
    z = [float(r["ndvi_gravel_zone"]) for r in T]
    c = [float(r["ndvi_control"]) for r in T]
    fig, ax = plt.subplots(figsize=(9.6, 4.2), dpi=220)
    for y in (2023, 2024, 2025, 2026):
        ax.axvspan(date(y - 1 if y > 2023 else 2023, 12 if y > 2023 else 1, 1), date(y, 3, 31), color="#EEF3EF", zorder=0)
    ax.plot(d, c, "o-", color=BLUE, ms=3, lw=1, label="Rest of the park (control)")
    ax.plot(d, z, "o-", color=GREEN, ms=3.5, lw=1.6, label="Gravel zone")
    ax.axvline(date(2025, 6, 1), color=RED, lw=1.2)
    ax.text(date(2025, 6, 10), 0.53, "gravel laid\n(June 2025)", color=RED, fontsize=8)
    ax.axvline(date(2026, 1, 11), color=SLATE, lw=0.8, ls=":")
    ax.text(date(2026, 1, 18), 0.53, "PM: intervention\nafter the concerts", color=SLATE, fontsize=8)
    ax.set_ylabel("NDVI (greenness)")
    ax.set_ylim(0, 0.6)
    ax.legend(frameon=False, fontsize=8, loc="upper left")
    ax.text(date(2023, 1, 5), -0.11, "Shaded: winter (December–March), when unirrigated grass greens with the rain. Each "
            "point is the median of clear pixels in one Sentinel-2 scene (< 10% cloud).", fontsize=7, color=GREY)
    fig.savefig(OUT / "fig2_timeseries.png", bbox_inches="tight", facecolor="white")


fig1()
fig2()
print("figures in", OUT)
