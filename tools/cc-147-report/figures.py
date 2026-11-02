"""Figures for Claim Check 147, from data/cc-147/eurostat_aea.csv (run fetch.py once, then this)."""
import csv, pathlib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[1]
OUT = HERE / "out"; OUT.mkdir(exist_ok=True)
for f in ["LiberationSans-Regular", "LiberationSans-Bold", "LiberationSans-Italic"]:
    fm.fontManager.addfont(f"/usr/share/fonts/truetype/liberation/{f}.ttf")
plt.rcParams.update({"font.family": "Liberation Sans", "axes.spines.top": False, "axes.spines.right": False,
                     "axes.edgecolor": "#8A9399", "axes.labelcolor": "#2B3A42", "xtick.color": "#2B3A42", "ytick.color": "#2B3A42"})
GREEN, SAGE, AMBER, RED, SLATE, GREY, ORANGE, BLUE = ("#14452F", "#7FA88B", "#E3A72F", "#B5483A", "#2B3A42", "#8A9399", "#D9772B", "#3C6E8F")
V = {}
for r in csv.DictReader(open(ROOT / "data/cc-147/eurostat_aea.csv")):
    V[(r["dataset"], r["unit"], r["item"], r["geo"], int(r["year"]))] = float(r["value"])
em = lambda it, y, g="MT": V[("env_ac_ainah_r2", "THS_T", it, g, y)]
clv = lambda it, y, g="MT": V[("nama_10_a64", "CLV20_MEUR", it, g, y)]
ter = lambda y: V[("env_ac_aibrid_r2", "THS_T", "AEMIS_TER", "MT", y)]


def fig1():
    ys = list(range(2013, 2025))
    fig, ax = plt.subplots(figsize=(9.6, 4.2), dpi=220)
    air = [em("H51", y) / 1000 for y in ys]
    rest = [(em("TOTAL_HH", y) - em("H51", y)) / 1000 for y in ys]
    ax.bar(ys, rest, color=SAGE, width=0.7, label="Everything except air transport")
    ax.bar(ys, air, bottom=rest, color=ORANGE, width=0.7, label="Air transport (NACE H51)")
    ax.plot(ys, [ter(y) / 1000 for y in ys], color=GREEN, lw=2.2, marker="o", ms=3.5, label="Emissions on Malta’s territory (inventory basis)")
    ax.set_ylabel("Million tonnes CO₂-equivalent")
    ax.set_xticks(ys)
    ax.legend(frameon=False, fontsize=8.2, loc="upper left")
    ax.text(2024, em("TOTAL_HH", 2024) / 1000 + 0.12, f"{100*em('H51',2024)/em('TOTAL_HH',2024):.0f}% air", ha="center", fontsize=8.5, color=ORANGE, fontweight="bold")
    ax.text(2013 - 0.5, -1.35, "Residence principle, all activities plus households. Source: Eurostat env_ac_ainah_r2, env_ac_aibrid_r2 (retrieved 2 Nov 2026); 2024 flagged i.", fontsize=7, color=GREY)
    fig.savefig(OUT / "fig1_air_share.png", bbox_inches="tight", facecolor="white"); plt.close(fig)


def fig2():
    ys = list(range(2020, 2025))
    fig, ax = plt.subplots(figsize=(9.6, 4.2), dpi=220)
    def idx(f): return [100 * f(y) / f(2020) for y in ys]
    series = [("Malta, all activities (Eurostat residence basis)", RED, "-", lambda y: em("TOTAL_HH", y) / clv("TOTAL", y)),
              ("Malta, excluding air and water transport (our rebuild)", GREEN, "-", lambda y: (em("TOTAL_HH", y) - em("H50", y) - em("H51", y)) / (clv("TOTAL", y) - clv("H50", y) - clv("H51", y))),
              ("Malta, territory basis (inventory totals)", SAGE, "--", lambda y: ter(y) / clv("TOTAL", y)),
              ("EU-27, all activities", BLUE, ":", lambda y: em("TOTAL_HH", y, "EU27_2020") / clv("TOTAL", y, "EU27_2020"))]
    for lab, col, ls, f in series:
        s = idx(f); ax.plot(ys, s, color=col, lw=2.4, ls=ls, label=lab)
        ax.text(2024.08, s[-1], f"{s[-1]-100:+.0f}%".replace("-", "−"), color=col, fontsize=9, va="center", fontweight="bold")
    ax.axhline(100, color=GREY, lw=0.6)
    ax.set_xlim(2019.9, 2024.5); ax.set_xticks(ys); ax.set_ylabel("GHG per euro of value added, index 2020 = 100")
    ax.legend(frameon=False, fontsize=8, loc="upper left")
    ax.set_xlabel("GVA in chain-linked volumes (2020 prices). Sources: Eurostat env_ac_ainah_r2, env_ac_aibrid_r2, nama_10_a64 (retrieved 2 Nov 2026). The factsheet gives −19% and +87.2%.", fontsize=7, color=GREY, loc="left")
    fig.savefig(OUT / "fig2_intensity.png", bbox_inches="tight", facecolor="white"); plt.close(fig)


fig1(); fig2(); print("figures in", OUT)
