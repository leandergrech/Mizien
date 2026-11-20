"""Figures for Claim Check 145."""
import csv
import pathlib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[1]
D = ROOT / "data/cc-145"
OUT = HERE / "out"; OUT.mkdir(exist_ok=True)
for f in ["LiberationSans-Regular", "LiberationSans-Bold", "LiberationSans-Italic"]:
    fm.fontManager.addfont(f"/usr/share/fonts/truetype/liberation/{f}.ttf")
plt.rcParams.update({"font.family": "Liberation Sans", "axes.spines.top": False, "axes.spines.right": False,
                     "axes.edgecolor": "#8A9399", "axes.labelcolor": "#2B3A42", "xtick.color": "#2B3A42",
                     "ytick.color": "#2B3A42"})
GREEN, AMBER, RED, SLATE, GREY, PALE = "#14452F", "#E3A72F", "#B5483A", "#2B3A42", "#8A9399", "#C9D3CC"
SHORT = {"General Licence for Hunting birds on land": "Hunting birds on land",
         "Special Spring Hunting licence - Quail & Turtle Dove": "Spring hunting (quail, turtle-dove)",
         "General Licence for Live-Capturing of birds": "Live-capturing of birds",
         "General Licence for Hunting of wild rabbit": "Hunting wild rabbit",
         "Special Autumn Live-Capturing Licence - Song Thrush and Golden Plover": "Autumn live-capturing (derogation)",
         "General Licence for Hunting birds at sea": "Hunting birds at sea",
         "General Licence for Capture of wild rabbit with nets": "Rabbit ferreting"}
rows = list(csv.DictReader(open(D / "wbru_2025_licences.csv")))[::-1]
fig, ax = plt.subplots(figsize=(9.6, 3.9), dpi=220)
y = range(len(rows))
ax.barh(y, [int(r["licences"]) for r in rows], color=PALE, label="Licences active in 2025")
ax.barh(y, [int(r["licensees_reporting"] or 0) for r in rows], color=GREEN, label="Licensees who filed any game report")
for i, r in enumerate(rows):
    lab = f"{int(r['licences']):,}"
    if r["licensees_reporting"]:
        lab += f"   ({int(r['licensees_reporting']):,} reported)"
    ax.text(int(r["licences"]) + 120, i, lab, va="center", fontsize=7.5, color=SLATE)
ax.axvline(10000, color=RED, lw=0.9, ls="--")
ax.text(10000, len(rows) - 0.35, "10,000 ", ha="right", fontsize=7.5, color=RED)
ax.set_yticks(list(y)); ax.set_yticklabels([SHORT[r["category"]] for r in rows], fontsize=8)
ax.set_xlim(0, 13500); ax.set_xlabel("Licences / licensees")
ax.legend(fontsize=7.5, frameon=False, loc="lower right")
fig.text(0.01, -0.03, "Source: Wild Birds Regulation Unit, Game Reporting Data – 2025 Report, pp. 1–2. One person may hold "
         "several categories.", fontsize=7, color=GREY)
fig.tight_layout(); fig.savefig(OUT / "fig1_licences.png", bbox_inches="tight"); plt.close(fig)
