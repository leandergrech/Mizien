"""Figures for Claim Check 111, drawn from data/cc-111/ (run fetch.py first)."""
import csv, pathlib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[1]
OUT = HERE / "out"
OUT.mkdir(exist_ok=True)
for f in ["LiberationSans-Regular", "LiberationSans-Bold", "LiberationSans-Italic"]:
    fm.fontManager.addfont(f"/usr/share/fonts/truetype/liberation/{f}.ttf")
plt.rcParams.update({"font.family": "Liberation Sans", "axes.spines.top": False, "axes.spines.right": False,
                     "axes.edgecolor": "#8A9399", "axes.labelcolor": "#2B3A42", "xtick.color": "#2B3A42",
                     "ytick.color": "#2B3A42"})
GREEN, AMBER, RED, SLATE, GREY, BLUE = "#14452F", "#E3A72F", "#B5483A", "#2B3A42", "#8A9399", "#3C6E8F"
v = {}
for r in csv.DictReader(open(ROOT / "data/cc-111/eurostat_env_wasmun.csv")):
    v[(r["geo"], r["wst_oper"], r["unit"], int(r["year"]))] = float(r["value"])
R = list(csv.DictReader(open(ROOT / "data/cc-106/checks.csv")))


def fig1():
    fig, ax = plt.subplots(figsize=(9.6, 3.6), dpi=220)
    labs = [f"Malta: {r['malta'].replace(' 2022-2030', '')}\nGlobal: {r['global']}" for r in R]
    for i, r in enumerate(R):
        lo, mid, hi = float(r["share_low_pct"]), float(r["share_mid_pct"]), float(r["share_high_pct"])
        ax.plot([lo, hi], [i, i], color=GREEN if "CIESM" in r["global"] else GREY, lw=6, solid_capstyle="round", alpha=0.85)
        ax.plot(mid, i, "o", color="white", mec=SLATE, ms=7)
        ax.text(hi + 0.4, i, f"{lo:.1f}–{hi:.1f}%  (central {mid:.1f}%)", va="center", fontsize=8, color=SLATE)
    ax.axvline(10, color=RED, lw=1, ls=":"); ax.text(10.2, -0.45, "claim: ~10%", color=RED, fontsize=8)
    ax.set_yticks(range(len(R))); ax.set_yticklabels(labs, fontsize=7.6); ax.invert_yaxis()
    ax.set_xlim(0, 32); ax.set_xlabel("Malta's share of the global population of breeding pairs (%)")
    fig.text(0.01, -0.06, "Bars: lowest Malta / highest global to highest Malta / lowest global; dots: midpoints. Sources: BirdLife Malta; ERA Species "
             "Action Plan 2022–2030; Bourgeois & Vidal (2008) Oryx; CIESM seabird guide.", fontsize=6.8, color=GREY)
    fig.savefig(OUT / "fig1_share.png", bbox_inches="tight", facecolor="white")


if __name__ == "__main__":
    fig1()
