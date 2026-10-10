"""Figures for Claim Check 085 (run calc.py first): fig1_estimates.png, fig2_hotels.png."""
import csv
import pathlib

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib import font_manager as fm  # noqa: E402

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[1]
D = ROOT / "data" / "cc-085"
OUT = HERE / "out"
OUT.mkdir(exist_ok=True)
for f in ["LiberationSans-Regular", "LiberationSans-Bold", "LiberationSans-Italic"]:
    fm.fontManager.addfont(f"/usr/share/fonts/truetype/liberation/{f}.ttf")
plt.rcParams.update({"font.family": "Liberation Sans", "axes.spines.top": False, "axes.spines.right": False,
                     "axes.edgecolor": "#8A9399"})
GREEN, AMBER, GREY, SLATE, ORANGE, SAGE = "#14452F", "#E3A72F", "#8A9399", "#2B3A42", "#D9772B", "#7FA88B"

chk = {r["check"]: r for r in csv.DictReader(open(D / "checks.csv", encoding="utf-8"))}


def val(prefix):
    r = next(v for k, v in chk.items() if k.startswith(prefix))
    return float(str(r["value"]).replace(",", ""))


# ---- Figure 1: the MHRA's own estimates of the arrivals needed, against 4.7 million and actual arrivals
rows = [
    ("2022 study: bed-stock table and launch slides\n(2019 occupancy: 76.7% collective, 59.3% private)",
     [val(f"2022 slides, Sc{i}") for i in (1, 2, 3)], ["Sc1", "Sc2", "Sc3"]),
    ("2022 study: airport table, p. 66\n(guest nights +60%, +70%, +80% on 2019)",
     [val(f"2022 study p. 66, Sc{i}") / 1e6 for i in (1, 2, 3)], ["Sc1", "Sc2", "Sc3"]),
    ("Same beds as the first row at 80% occupancy\n(our calculation, collective and private)",
     [val(f"2022 study beds, Sc{i}, at 80% occupancy in collective and private") for i in (1, 2, 3)], ["Sc1", "Sc2", "Sc3"]),
    ("2024 update: full MTA pipeline\n(2023 occupancy; 15% or no old beds retired)",
     [val("2024 update, Sc3 (full pipeline") / 1000, val("2024 update, Sc3 (full pipeline") / 1000
      + val("2024 update: extra collective arrivals") / 1e6], ["15% retired", "none retired"]),
]
fig, ax = plt.subplots(figsize=(9.0, 4.3), dpi=220)
ys = list(range(len(rows)))[::-1]
for y, (lab, xs, names) in zip(ys, rows):
    ax.plot([min(xs), max(xs)], [y, y], color=SAGE, lw=2, zorder=1, solid_capstyle="round")
    for x, n in zip(xs, names):
        hit = abs(x - 4.68) < 0.005
        ax.scatter([x], [y], s=60 if hit else 42, color=ORANGE if hit else GREEN, zorder=3, edgecolor="white", linewidth=1.2)
        box = {"facecolor": "white", "edgecolor": "none", "pad": 0.6}
        ax.text(x, y + 0.2, f"{x:.2f}", ha="center", va="bottom", fontsize=8, color=SLATE, bbox=box, zorder=4)
        ax.text(x, y - 0.22, n, ha="center", va="top", fontsize=6.8, color=GREY, bbox=box, zorder=4)
ax.axvline(4.7, color=ORANGE, lw=1.2, ls="--", zorder=0)
ax.text(4.71, 3.62, "4.7 million\n(the claim)", fontsize=7.8, color=ORANGE, va="top")
ax.axvline(2.75, color=GREY, lw=1, ls=":", zorder=0)
ax.text(2.77, 3.62, "2019 arrivals:\n2.75 million", fontsize=7.6, color=GREY, va="top")
ax.axvline(4.02, color=GREY, lw=1, ls=":", zorder=0)
ax.text(4.0, -0.62, "2025 arrivals: 4.02 million (second-hand ◆)", fontsize=7.6, color=GREY, ha="right", va="center", fontfamily="DejaVu Sans")
ax.set_yticks(ys)
ax.set_yticklabels([r[0] for r in rows], fontsize=8, color=SLATE)
ax.set_ylim(-0.85, 3.75)
ax.set_xlim(2.6, 5.25)
ax.set_xlabel("Tourist arrivals a year needed, million", fontsize=8.5, color=SLATE)
ax.tick_params(axis="x", labelsize=8.5, colors=SLATE)
ax.tick_params(axis="y", length=0)
ax.spines["left"].set_visible(False)
ax.grid(axis="x", color="#E3E7E4", lw=0.6)
ax.set_axisbelow(True)
fig.savefig(OUT / "fig1_estimates.png", bbox_inches="tight", facecolor="white")
plt.close(fig)

# ---- Figure 2: hotels in Eurostat: bed-places (left) and occupancy (right)
E = {}
for r in csv.DictReader(open(D / "eurostat_tourism.csv", encoding="utf-8")):
    E[(r["dataset"], r["series"], int(r["year"]))] = float(r["value"])
yrs = list(range(2010, 2026))
beds = [E[("tour_cap_nat", "nace_r2=I551|accomunit=BEDPL|unit=NR", y)] / 1000 for y in yrs]
oy = list(range(2012, 2026))
rooms = [E[("tour_occ_anor", "accomunit=BEDRM|hotelsize=TOTAL|unit=PC", y)] for y in oy]
bedp = [E[("tour_occ_anor", "accomunit=BEDPL|hotelsize=TOTAL|unit=PC", y)] for y in oy]
fig, (a1, a2) = plt.subplots(1, 2, figsize=(9.0, 3.5), dpi=220, gridspec_kw={"width_ratios": [1, 1.25], "wspace": 0.28})
a1.bar(yrs, beds, color=[ORANGE if y in (2019, 2025) else SAGE for y in yrs], width=0.72)
for y, b in zip(yrs, beds):
    if y in (2010, 2019, 2025):
        a1.text(y, (48.6 if y == 2019 else b + 0.8), f"{b * 1000:,.0f}", ha="center", fontsize=7.4, color=SLATE)
a1.set_ylim(0, 63)
a1.set_ylabel("Hotel bed-places, thousand", fontsize=8.3, color=SLATE)
a1.set_xticks([2010, 2013, 2016, 2019, 2022, 2025])
a1.tick_params(labelsize=8, colors=SLATE)
a1.set_title("Hotel bed-places", fontsize=9, color=SLATE, loc="left")
a2.axhline(80, color=ORANGE, lw=1.1, ls="--")
a2.text(2012.1, 81.2, "80% (the claim)", fontsize=7.6, color=ORANGE)
a2.plot(oy, rooms, color=GREEN, lw=2, marker="o", ms=3.5)
a2.plot(oy, bedp, color=GREY, lw=2, marker="o", ms=3.5)
a2.text(2025.3, rooms[-1], f"Rooms {rooms[-1]:.1f}%", fontsize=7.8, color=GREEN, va="center")
a2.text(2025.3, bedp[-1], f"Bed-places {bedp[-1]:.1f}%", fontsize=7.8, color=GREY, va="center")
a2.annotate(f"2019: {rooms[oy.index(2019)]:.1f}%", (2019, rooms[oy.index(2019)]), xytext=(2016.2, 88),
            fontsize=7.6, color=GREEN, arrowprops={"arrowstyle": "-", "color": GREEN, "lw": 0.7})
a2.annotate(f"2019: {bedp[oy.index(2019)]:.1f}%", (2019, bedp[oy.index(2019)]), xytext=(2013.4, 50),
            fontsize=7.6, color=GREY, arrowprops={"arrowstyle": "-", "color": GREY, "lw": 0.7})
a2.set_ylim(20, 95)
a2.set_xlim(2011.6, 2028.6)
a2.set_xticks([2012, 2015, 2018, 2021, 2024])
a2.set_ylabel("Net occupancy, %", fontsize=8.3, color=SLATE)
a2.tick_params(labelsize=8, colors=SLATE)
a2.set_title("Hotel occupancy (pandemic dip 2020–21)", fontsize=9, color=SLATE, loc="left")
fig.savefig(OUT / "fig2_hotels.png", bbox_inches="tight", facecolor="white")
plt.close(fig)
print("ok")
