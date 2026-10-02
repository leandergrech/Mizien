"""Visualise the official annual station values from data/cc-007/station_pm25.csv."""
import csv
import pathlib

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[1]
OUT = HERE / "out"
OUT.mkdir(exist_ok=True)
for font in ["LiberationSans-Regular", "LiberationSans-Bold", "LiberationSans-Italic"]:
    fm.fontManager.addfont(f"/usr/share/fonts/truetype/liberation/{font}.ttf")
plt.rcParams.update({"font.family": "Liberation Sans", "axes.spines.top": False,
                     "axes.spines.right": False, "axes.edgecolor": "#8A9399",
                     "axes.labelcolor": "#2B3A42", "xtick.color": "#2B3A42",
                     "ytick.color": "#2B3A42"})

data = {}
with (ROOT / "data" / "cc-007" / "station_pm25.csv").open(encoding="utf-8", newline="") as f:
    for row in csv.DictReader(f):
        data.setdefault(row["station"], {})[int(row["year"])] = (
            float(row["annual_pm25_ug_m3"]) if row["annual_pm25_ug_m3"] else None)

colours = {"Attard": "#14452F", "Msida": "#B5483A", "St Paul's Bay": "#3C6E8F",
           "Żejtun": "#D9772B", "Għarb": "#6D7F70"}
years = list(range(2020, 2025))
fig, ax = plt.subplots(figsize=(9.2, 4.15), dpi=220)
for station, series in data.items():
    vals = [series.get(y) for y in years]
    ax.plot(years, vals, marker="o", markersize=4.7, linewidth=2.1,
            color=colours[station], label=station)
ax.axhline(5, color="#8A9399", linewidth=1.2, linestyle=(0, (3, 2)),
           label="WHO annual guideline · 5")
ax.axhline(10, color="#E3A72F", linewidth=1.5, linestyle=(0, (4, 2)),
           label="EU limit due 2030 · 10")
ax.set_xlim(2019.75, 2024.55)
ax.set_ylim(4.1, 15.8)
ax.set_xticks(years)
ax.set_ylabel("Annual mean PM₂.₅ (µg/m³)")
ax.set_title("Every reported annual mean exceeds WHO’s guideline", loc="left",
             fontsize=10.4, color="#14452F", fontweight="bold", pad=11)
ax.legend(frameon=False, ncol=4, fontsize=7.0, loc="upper center",
          bbox_to_anchor=(0.52, -0.14), handlelength=1.6, columnspacing=1.4)
ax.grid(axis="y", color="#D5DBD7", linewidth=0.55)
ax.set_axisbelow(True)
fig.text(0.12, 0.015,
         "Source: PQ 29696 annex. St Paul’s Bay has no reported value for 2020–21. "
         "All 23 reported means are below the then-applicable EU limit of 25 µg/m³.",
         fontsize=7.1, color="#68747A")
fig.tight_layout(rect=(0.04, 0.08, 0.99, 1))
fig.savefig(OUT / "station_pm25.png", bbox_inches="tight", facecolor="white")
print("figure in", OUT)
