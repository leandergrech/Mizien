"""Figures for Claim Check 117, drawn from data/cc-117/ (run fetch.py first)."""
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
EU27 = {"AT", "BE", "BG", "CY", "CZ", "DE", "DK", "EE", "EL", "ES", "FI", "FR", "HR", "HU", "IE", "IT", "LT", "LU", "LV", "MT", "NL", "PL", "PT", "RO", "SE", "SI", "SK"}
mun = {(r["geo"], int(r["time"])): float(r["value"]) for r in csv.DictReader(open(ROOT / "data/cc-117/eurostat_cei_wm011.csv"))}
pk = {(r["geo"], r["waste"], int(r["time"])): float(r["value"]) for r in csv.DictReader(open(ROOT / "data/cc-117/eurostat_env_waspac.csv"))
      if r["unit"] == "PC" and r["wst_oper"] == "RCY"}


def fig1():
    fig, axs = plt.subplots(1, 2, figsize=(9.6, 3.9), dpi=220)
    ax = axs[0]
    ys = list(range(2018, 2025))
    ax.plot(ys, [mun[("MT", y)] for y in ys], color=GREEN, lw=2.4, marker="o", ms=3, label="Malta")
    ax.plot(ys, [mun[("EU27_2020", y)] for y in ys], color=BLUE, lw=2.4, marker="o", ms=3, label="EU-27")
    ax.axhline(50, color=RED, lw=1.2, ls="--"); ax.text(2018, 51.5, "50% target (for 2020)", color=RED, fontsize=8)
    ax.annotate("10.9% (2020)", (2020, 10.9), xytext=(2020.2, 22), color=GREEN, fontsize=9, fontweight="bold")
    ax.set_ylim(0, 60); ax.legend(frameon=False, fontsize=8.5, loc="center right")
    ax.set_title("Municipal waste recycling rate, %", fontsize=10, color=SLATE, loc="left")
    ax = axs[1]
    series = [("W1501", "Total", 55), ("W150101", "Paper, card", 60), ("W150104", "Metals", 50)]
    cols = [GREEN, AMBER, BLUE]
    yrs = [2020, 2021, 2022, 2023]
    for (c, lab, t), col in zip(series, cols):
        ax.plot(yrs, [pk[("MT", c, y)] for y in yrs], color=col, lw=2.2, marker="o", ms=3, label=f"{lab} (target {t}%)")
        ax.hlines(t, 2019.8, 2023.2, color=col, lw=1, ls=":")
    ax.set_ylim(0, 75); ax.set_xticks(yrs); ax.legend(frameon=False, fontsize=7.5, loc="lower left", ncol=1)
    ax.set_title("Malta: packaging recycling rate by material, %", fontsize=10, color=SLATE, loc="left")
    fig.text(0.01, -0.03, "Dotted lines: targets as listed on the Commission page (total 55%, paper and cardboard 60%, metals 50%). Source: "
             "Eurostat cei_wm011 and env_waspac, retrieved 13 Oct 2026.", fontsize=7, color=GREY)
    fig.tight_layout(); fig.savefig(OUT / "fig1_series.png", bbox_inches="tight", facecolor="white")


def fig2():
    fig, ax = plt.subplots(1, 1, figsize=(9.6, 4.6), dpi=220)
    d = {g: mun[(g, 2020)] for g in EU27 if (g, 2020) in mun}
    items = sorted(d.items(), key=lambda kv: kv[1])
    ax.barh([g for g, _ in items], [x for _, x in items], color=[GREEN if g == "MT" else "#C9D3CC" for g, _ in items])
    ax.axvline(50, color=RED, lw=1.2, ls="--"); ax.text(50.5, 0, "50% target", color=RED, fontsize=8)
    ax.set_title("Municipal waste recycling rate, 2020 (%), EU-27", fontsize=10, color=SLATE, loc="left"); ax.tick_params(axis="y", labelsize=7.5)
    ax.text(d["MT"], 0, f"  {d['MT']:.1f}", va="center", fontsize=8, color=GREEN, fontweight="bold")
    fig.text(0.01, -0.02, "Eurostat cei_wm011 (recycling rate indicator), retrieved 13 Oct 2026. The Commission's list of 12 states rests on "
             "member-state compliance data, not on this indicator.", fontsize=7, color=GREY)
    fig.tight_layout(); fig.savefig(OUT / "fig2_ranks.png", bbox_inches="tight", facecolor="white")


if __name__ == "__main__":
    fig1(); fig2()
