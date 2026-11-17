"""Figures for Claim Check 164 (run calc.py first)."""
import pathlib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from matplotlib.patches import Patch

HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE / "out"; OUT.mkdir(exist_ok=True)
for f in ["LiberationSans-Regular", "LiberationSans-Bold", "LiberationSans-Italic"]:
    fm.fontManager.addfont(f"/usr/share/fonts/truetype/liberation/{f}.ttf")
plt.rcParams.update({"font.family": "Liberation Sans", "axes.spines.top": False, "axes.spines.right": False,
                     "axes.edgecolor": "#8A9399", "axes.labelcolor": "#2B3A42", "xtick.color": "#2B3A42",
                     "ytick.color": "#2B3A42"})
GREEN, AMBER, RED, SLATE, GREY, PALE = "#14452F", "#E3A72F", "#B5483A", "#2B3A42", "#8A9399", "#C9D3CC"
bars = [("Budget speech:\n“madwar €182 miljun”", 182, RED, False),
        ("Our estimate: 2025 nights,\nadults, no caps", 175.7, GREEN, False),
        ("Our estimate: scaled to\n28 million nights (2026)", 193.4, GREEN, False),
        ("Estimates 2027 total,\nas reported (Amphora)", 213, GREY, True),
        ("Estimates 2027 minus\n2026 (€21m), as reported", 192, GREY, True)]
fig, ax = plt.subplots(figsize=(9.6, 3.9), dpi=220)
for i, (l, v, c, sec) in enumerate(bars):
    ax.bar(i, v, color="white" if sec else c, edgecolor=GREY if sec else "none", hatch="///" if sec else None, width=0.6)
    ax.text(i, v + 4, f"€{v:,.0f}m", ha="center", fontsize=8.5, color=SLATE)
ax.set_xticks(range(len(bars))); ax.set_xticklabels([b[0] for b in bars], fontsize=7.8)
ax.set_ylim(0, 250); ax.set_ylabel("€ million a year")
ax.legend(handles=[Patch(facecolor="white", edgecolor=GREY, hatch="///", label="Second-hand (Estimates not read)")],
          fontsize=7.5, frameon=False, loc="upper left")
fig.text(0.01, -0.03, "Sources: Budget Speech 2027 p. 27; NSO Inbound Tourism December 2025 (NR 020/2026); Amphora Media 13 Nov 2026. "
         "Our estimates do not apply the 8-night caps or exemptions.", fontsize=7, color=GREY)
fig.tight_layout(); fig.savefig(OUT / "fig1_yield.png", bbox_inches="tight"); plt.close(fig)
