"""Figures for Claim Check 016, drawn from data/cc-016/ (run calc.py first)."""
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
GREEN, SAGE, AMBER, RED, SLATE, GREY, ORANGE, BLUE = ("#14452F", "#7FA88B", "#E3A72F", "#B5483A", "#2B3A42",
                                                      "#8A9399", "#D9772B", "#3C6E8F")
D = ROOT / "data" / "cc-016"
U = {r["item"]: float(r["value"]) for r in csv.DictReader(open(D / "ops_uptake.csv"))}
CALLS = {int(r["year"]): int(r["calls"]) for r in csv.DictReader(open(D / "cruise_calls.csv"))}


def fig1():
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(9.6, 3.8), dpi=220, gridspec_kw={"width_ratios": [1.15, 1]})
    labs = ["Claimed cut in\nharbour pollution", "Berths that\nplugged in", "Berth time\nplugged in"]
    vals = [90, 100 * U["Berths connected to onshore power (OPS)"] / U["Cruise berths at Valletta Cruise Port"],
            U["Share of berth time connected"]]
    cols = [GREY, SAGE, GREEN]
    b = a1.bar(labs, vals, color=cols, width=0.62)
    for r, v in zip(b, vals):
        a1.text(r.get_x() + r.get_width() / 2, v + 2, f"{v:.0f}%", ha="center", fontsize=11, fontweight="bold",
                color=SLATE)
    a1.set_ylim(0, 105)
    a1.set_ylabel("%")
    a1.set_title("Promise and first-year use", fontsize=9.5, color=GREEN, loc="left", fontweight="bold")
    st = ["1 day\nor less", "1–2\ndays", "2–4\ndays"]
    sv = [U["Berths of 1 day or less connected"], U["Berths of 1-2 days connected"], U["Berths of 2-4 days connected"]]
    b2 = a2.bar(st, sv, color=[SAGE, SAGE, RED], width=0.6)
    for r, v in zip(b2, sv):
        a2.text(r.get_x() + r.get_width() / 2, v + 0.6, f"{v:.1f}%", ha="center", fontsize=10, color=SLATE)
    a2.set_ylim(0, 25)
    a2.set_title("Share of berths plugged in, by length of stay", fontsize=9.5, color=GREEN, loc="left",
                 fontweight="bold")
    fig.text(0.01, -0.04, "10 Jul 2024 – 10 Jul 2025. Sources: Infrastructure Malta; Amphora Media analysis of Transport "
             "Malta FOI records and the Valletta Cruise Port schedule (second-hand).", fontsize=7, color=GREY)
    fig.tight_layout(w_pad=3)
    fig.savefig(OUT / "fig1_uptake.png", bbox_inches="tight", facecolor="white")


def fig2():
    fig, ax = plt.subplots(figsize=(9.6, 3.2), dpi=220)
    ys = sorted(CALLS)
    cols = [GREY if y < 2024 else GREEN for y in ys]
    b = ax.bar([str(y) for y in ys], [CALLS[y] for y in ys], color=cols, width=0.6)
    for r, y in zip(b, ys):
        ax.text(r.get_x() + r.get_width() / 2, CALLS[y] + 6, str(CALLS[y]), ha="center", fontsize=10, color=SLATE)
    ax.set_ylim(0, 480)
    ax.set_ylabel("Cruise calls")
    ax.axvline(2.5, color=AMBER, ls="--", lw=1.4)
    ax.text(2.55, 455, "Shore power in service (trial Dec 2023, launch Jul 2024)", fontsize=8, color=AMBER)
    ax.set_xlabel("Grey: as quoted by Amphora Media (second-hand). Green: Valletta Cruise Port 2025 results release. "
                  "2020-21 omitted (pandemic).", fontsize=7, color=GREY)
    fig.savefig(OUT / "fig2_calls.png", bbox_inches="tight", facecolor="white")


fig1()
fig2()
print("figures in", OUT)
