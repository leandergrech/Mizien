"""Figures for Claim Check 047, drawn from data/cc-047/."""
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
R = list(csv.DictReader(open(ROOT / "data/cc-047/study_ranges.csv")))
C = {r["item"]: float(r["value"]) for r in csv.DictReader(open(ROOT / "data/cc-047/commission_nitrates_malta_2020_2023.csv"))}


def fig1():
    rows = [r for r in R if not r["what"].startswith("EU limit")]
    labels = ["Eastern main aquifer\n(the claim; MaltaToday quoting\nthe 2026 paper)", "Groundwater under potato and\nforage fields (2025 abstract)",
              "Perched aquifer, north-west\n(2025 abstract)", "Regional aquifer under the\nperched aquifer (2025 abstract)"]
    cols = [RED, AMBER, BLUE, GREEN]
    fig, ax = plt.subplots(figsize=(9.6, 3.7), dpi=220)
    for i, r in enumerate(rows):
        lo, hi = float(r["low_mg_l"]), float(r["high_mg_l"])
        ax.barh(i, hi - lo, left=lo, color=cols[i], height=0.55)
        ax.text(hi + 4, i, f"{lo:.0f}–{hi:.0f} mg/L", va="center", fontsize=8.5, color=SLATE)
    ax.axvline(50, color=SLATE, lw=1.4, ls="--")
    ax.text(52, -0.62, "EU limit 50 mg/L", fontsize=8, color=SLATE, va="center")
    ax.set_yticks(range(len(rows)))
    ax.set_yticklabels(labels, fontsize=8)
    ax.invert_yaxis()
    ax.set_xlim(0, 420)
    ax.set_xlabel("Nitrate in groundwater, mg/L")
    fig.text(0.01, -0.04, "Ranges as reported by Laudi et al. (2026) and the team's EGU 2025 abstract. First bar is a second-hand quotation.",
             fontsize=7, color=GREY)
    fig.savefig(OUT / "fig1_ranges.png", bbox_inches="tight", facecolor="white")


def fig2():
    parts = [("Below 25", C["share_lt_25"], GREEN), ("25–39.99", C["share_25_39.99"], "#8DB36B"),
             ("40–49.99", C["share_40_49.99"], AMBER), ("50 or more", C["share_ge_50"], RED)]
    prev = {"Below 25": None}
    fig, ax = plt.subplots(figsize=(9.6, 2.3), dpi=220)
    left = 0
    for lab, v, col in parts:
        ax.barh(0, v, left=left, color=col, label=lab)
        ax.text(left + v / 2, 0, f"{v:.1f}%", ha="center", va="center", fontsize=8.5, color="white" if col != AMBER else SLATE, fontweight="bold")
        left += v
    ax.set_yticks([0])
    ax.set_yticklabels(["44 groundwater\nmonitoring points,\n2020–2023"], fontsize=8.5)
    ax.set_xlim(0, 100)
    ax.set_xlabel("Share of monitoring points by average nitrate (mg/L); 63.6% were at 50 or more in 2016–2019")
    ax.legend(frameon=False, fontsize=7.8, ncol=4, loc="upper center", bbox_to_anchor=(0.5, 1.4))
    fig.text(0.01, -0.12, "Source: European Commission, SWD(2026) 232 final, Malta fiche, section 4.2 (EWA data).", fontsize=7, color=GREY)
    fig.savefig(OUT / "fig2_commission.png", bbox_inches="tight", facecolor="white")


if __name__ == "__main__":
    fig1()
    fig2()
