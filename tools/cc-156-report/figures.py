"""Figures for Claim Check 156, drawn from data/cc-156/country_excellent_share.csv (run fetch_data.py first).
Output: out/fig1_rank.png, out/fig2_countries.png"""
import csv, pathlib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm

HERE = pathlib.Path(__file__).resolve().parent
D = HERE.parents[1] / "data" / "cc-156"
OUT = HERE / "out"; OUT.mkdir(exist_ok=True)
for f in ["LiberationSans-Regular", "LiberationSans-Bold", "LiberationSans-Italic"]:
    fm.fontManager.addfont(f"/usr/share/fonts/truetype/liberation/{f}.ttf")
plt.rcParams.update({"font.family": "Liberation Sans", "axes.spines.top": False, "axes.spines.right": False,
                     "axes.edgecolor": "#8A9399", "axes.labelcolor": "#2B3A42", "xtick.color": "#2B3A42",
                     "ytick.color": "#2B3A42"})
GREEN, SAGE, RED, SLATE, GREY, BLUE = "#14452F", "#7FA88B", "#B5483A", "#2B3A42", "#8A9399", "#3C6E8F"
SRC = ("Source: EEA bathing-water data, DiscoMap service BathingWater_Dyna_WM_2025 layer 3, retrieved 11 Nov 2026. "
       "Share = excellent ÷ bathing waters\nwith a class that season, coastal waters of EU-27 states that report them.")
R = [r for r in csv.DictReader(open(D / "country_excellent_share.csv")) if r["scope"] == "coastal"]
yrs = list(range(2015, 2026))
mt = {int(r["season"]): r for r in R if r["country"] == "MT"}

# fig 1: Malta's rank by season
fig, ax = plt.subplots(figsize=(9.6, 3.9), dpi=220)
rk = [int(mt[y]["rank"]) for y in yrs]
ax.plot(yrs, rk, color=GREEN, lw=2.6, marker="o", ms=6)
for y, k in zip(yrs, rk):
    ax.text(y, k - 0.55, f"{k}", ha="center", va="bottom" if False else "bottom", fontsize=9, color=GREEN, fontweight="bold")
ax.axhline(11.5, color=BLUE, ls="--", lw=1)
ax.text(2015.05, 11.75, "middle of the 22 coastal states", color=BLUE, fontsize=8.3, va="top")
ax.invert_yaxis(); ax.set_ylim(14, 0.5); ax.set_xticks(yrs); ax.set_yticks([1, 3, 6, 9, 12, 15, 18, 22])
ax.set_ylim(22.5, 0.5)
ax.axhline(11.5, color=BLUE, ls="--", lw=1)
ax.tick_params(labelsize=8.5)
ax.set_ylabel("Rank by share of excellent bathing waters\n(1 = highest)", fontsize=8.5)
ax.set_title("Malta’s rank among 22 EU coastal states, seasons 2015–2025", fontsize=9.5, color=GREEN, loc="left",
             fontweight="bold", pad=10)
fig.text(0.01, -0.02, SRC, fontsize=7, color=GREY, va="top")
fig.savefig(OUT / "fig1_rank.png", bbox_inches="tight", facecolor="white")

# fig 2: dumbbell 2016 -> 2025 by country
c16 = {r["country"]: float(r["excellent_pct"]) for r in R if r["season"] == "2016"}
c25 = {r["country"]: float(r["excellent_pct"]) for r in R if r["season"] == "2025"}
order = sorted(c25, key=lambda c: c25[c])
fig, ax = plt.subplots(figsize=(9.6, 6.2), dpi=220)
for i, c in enumerate(order):
    col = GREEN if c == "MT" else GREY
    ax.plot([c16[c], c25[c]], [i, i], color=col, lw=2 if c == "MT" else 1, zorder=1)
    ax.scatter(c16[c], i, s=26, facecolor="white", edgecolor=col, lw=1.4, zorder=2)
    ax.scatter(c25[c], i, s=34, color=GREEN if c == "MT" else SLATE, zorder=3)
ax.set_yticks(range(len(order))); ax.set_yticklabels(order, fontsize=8.5)
for t in ax.get_yticklabels():
    if t.get_text() == "MT": t.set_fontweight("bold"); t.set_color(GREEN)
ax.set_xlabel("Share of coastal bathing waters rated excellent (%)", fontsize=8.5)
ax.scatter([], [], s=26, facecolor="white", edgecolor=SLATE, label="2016"); ax.scatter([], [], s=34, color=SLATE, label="2025")
ax.legend(frameon=False, fontsize=8.5, loc="lower right")
ax.set_title("Share of coastal bathing waters rated excellent, by EU state, 2016 and 2025", fontsize=9.5, color=GREEN,
             loc="left", fontweight="bold", pad=10)
fig.text(0.01, 0.0, SRC, fontsize=7, color=GREY, va="top")
fig.savefig(OUT / "fig2_countries.png", bbox_inches="tight", facecolor="white")
print("ok")
