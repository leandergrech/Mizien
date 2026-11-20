"""Figures for Claim Check 152."""
import csv
import pathlib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[1]
D = ROOT / "data/cc-152"
OUT = HERE / "out"; OUT.mkdir(exist_ok=True)
for f in ["LiberationSans-Regular", "LiberationSans-Bold", "LiberationSans-Italic"]:
    fm.fontManager.addfont(f"/usr/share/fonts/truetype/liberation/{f}.ttf")
plt.rcParams.update({"font.family": "Liberation Sans", "axes.spines.top": False, "axes.spines.right": False,
                     "axes.edgecolor": "#8A9399", "axes.labelcolor": "#2B3A42", "xtick.color": "#2B3A42",
                     "ytick.color": "#2B3A42"})
GREEN, AMBER, RED, SLATE, GREY, PALE = "#14452F", "#E3A72F", "#B5483A", "#2B3A42", "#8A9399", "#C9D3CC"
es = [(int(r["year"]), float(r["nox_tonnes"]) / 1000) for r in csv.DictReader(open(D / "eurostat_nox_malta.csv")) if r["nox_tonnes"]]
fig, ax = plt.subplots(figsize=(9.6, 4.0), dpi=220)
ax.plot([y for y, _ in es], [v for _, v in es], color=SLATE, lw=2.2, marker="o", ms=3, label="NOx emissions (Eurostat)")
ax.plot([2020, 2029.5], [5.48, 5.48], color=AMBER, lw=1.4, ls="--", label="Ceiling 2020–2029 (42% below 2005)")
ax.plot([2030, 2031.5], [1.98, 1.98], color=RED, lw=2, ls="--", label="Ceiling from 2030 (79% below 2005)")
ax.scatter([2030], [3.88], s=60, color=RED, zorder=4, label="ERA projection, with measures (3.88 kt)")
ax.annotate("3.88 kt", (2030, 3.88), xytext=(2027.6, 3.2), fontsize=8, color=RED,
            arrowprops=dict(arrowstyle="-", color=GREY, lw=0.6))
ax.text(2031.6, 1.98, "1.98 kt", va="center", fontsize=8, color=RED)
ax.set_xlim(2004.5, 2033); ax.set_ylim(0, 10.5); ax.set_ylabel("NOx, kilotonnes")
ax.legend(fontsize=7.5, frameon=False, loc="upper right")
fig.text(0.01, -0.03, "Sources: Eurostat env_air_emis (updated 7 Sep 2026); ERA draft NAPCP first update (June 2026), Table 4; "
         "Directive (EU) 2016/2284, Annex II.", fontsize=7, color=GREY)
fig.tight_layout(); fig.savefig(OUT / "fig1_nox.png", bbox_inches="tight"); plt.close(fig)
