"""Figures for Claim Check 148 (run calc.py first)."""
import json, pathlib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
HERE = pathlib.Path(__file__).resolve().parent; OUT = HERE / "out"; OUT.mkdir(exist_ok=True)
for f in ["LiberationSans-Regular", "LiberationSans-Bold", "LiberationSans-Italic"]:
    fm.fontManager.addfont(f"/usr/share/fonts/truetype/liberation/{f}.ttf")
plt.rcParams.update({"font.family": "Liberation Sans", "axes.spines.top": False, "axes.spines.right": False,
                     "axes.edgecolor": "#8A9399", "axes.labelcolor": "#2B3A42", "xtick.color": "#2B3A42", "ytick.color": "#2B3A42"})
GREEN, SAGE, AMBER, RED, SLATE, GREY = "#14452F", "#7FA88B", "#E3A72F", "#B5483A", "#2B3A42", "#8A9399"
R = json.load(open(HERE.parents[1] / "data" / "cc-148" / "results.json"))

# Fig 1: all Member States, Q1 2025 vs Q1 2024, current vintage
q = R["q1_2025"]; cs = list(q)
fig, ax = plt.subplots(figsize=(9.6, 4.2), dpi=220)
cols = [GREEN if c == "MT" else (AMBER if c == "FI" else SAGE) for c in cs]
ax.bar(cs, [q[c] for c in cs], color=cols)
ax.axhline(0, color=GREY, lw=0.8)
for c in ("MT", "FI", "BG"):
    ax.text(cs.index(c), q[c] + (1 if q[c] > 0 else -1.8), f"{q[c]:+.1f}%", ha="center", fontsize=8.5, fontweight="bold", color=SLATE)
ax.axhline(R["eu_q1_2025_pct"], color=RED, lw=1.2, ls="--")
ax.text(9, R["eu_q1_2025_pct"] + 0.8, f"EU-27 {R['eu_q1_2025_pct']:+.1f}%", ha="center", fontsize=8.5, color=RED)
ax.set_ylabel("Change on Q1 2024 (%)"); ax.set_ylim(-14, 29)
ax.tick_params(axis="x", labelsize=8)
ax.text(-0.5, -19.5, "Eurostat env_ac_aigg_q, non-seasonally adjusted, current vintage (updated 14 Aug 2026; retrieved 2 Nov 2026). "
        "Eurostat's Aug 2025 estimate was Malta −6.2%, Finland −4.4%.", fontsize=7, color=GREY)
fig.savefig(OUT / "fig1_member_states.png", bbox_inches="tight", facecolor="white")

# Fig 2: Malta quarterly level and yoy
mq = R["mt_q"]; ks = list(mq)
fig, ax = plt.subplots(figsize=(9.6, 3.8), dpi=220)
colq = [AMBER if k == "2025-Q1" else SAGE for k in ks]
ax.bar(range(len(ks)), [mq[k] / 1000 for k in ks], color=colq)
ax.set_xticks(range(len(ks))); ax.set_xticklabels([k.replace("-", "\n") for k in ks], fontsize=8)
for i, k in enumerate(ks):
    if k in R["mt_yoy"]:
        ax.text(i, mq[k] / 1000 + 0.04, f"{R['mt_yoy'][k]:+.0f}%" if abs(R['mt_yoy'][k]) > 20 else f"{R['mt_yoy'][k]:+.1f}%", ha="center", fontsize=8, color=SLATE, fontweight="bold" if k == "2025-Q1" else None)
ax.set_ylabel("Million tonnes CO₂-eq"); ax.set_ylim(0, 2.4)
ax.text(-0.5, -0.62, "Eurostat env_ac_aigg_q, Malta, all activities plus households, NSA (retrieved 2 Nov 2026). Labels: change on same quarter a year earlier. "
        "2026-Q1 is the latest quarter.", fontsize=7, color=GREY)
fig.savefig(OUT / "fig2_malta_quarters.png", bbox_inches="tight", facecolor="white")
