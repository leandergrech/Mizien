"""Figures for Claim Check 124, drawn from data/cc-124/ (run fetch.py and calc.py first)."""
import csv, pathlib
from collections import defaultdict
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
D = ROOT / "data" / "cc-124"
load = lambda n: list(csv.DictReader(open(D / f"eurostat_{n}.csv")))
CARS, MODAL, REN = defaultdict(dict), defaultdict(dict), defaultdict(dict)
FUEL = {int(r["time"]): float(r["value"]) for r in load("fuel")}
POP = {int(r["time"]): float(r["value"]) for r in load("pop")}
for r in load("cars"):
    CARS[(r["geo"], r["mot_nrg"])][int(r["time"])] = float(r["value"])
for r in load("modal"):
    MODAL[r["vehicle"]][int(r["time"])] = float(r["value"])
for r in load("ren"):
    REN[r["geo"]][int(r["time"])] = float(r["value"])


def fig1():
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(9.6, 3.9), dpi=220, gridspec_kw={"width_ratios": [1, 1]})
    cars = CARS[("MT", "TOTAL")]
    ys = [2022, 2023, 2024, 2025]
    a1.plot(ys, [100 * cars[y] / cars[2022] for y in ys], color=SLATE, lw=2, marker="o", label="Passenger cars")
    a1.plot(ys[:3], [100 * FUEL[y] / FUEL[2022] for y in ys[:3]], color=ORANGE, lw=2, marker="o",
            label="Road-transport energy")
    a1.plot(ys, [100 * POP[y + 1] / POP[2023] for y in ys], color=SAGE, lw=2, marker="o", label="Population (1 Jan next year)")
    a1.axhline(100, color=GREY, lw=0.8, ls=":")
    a1.set_xticks(ys)
    a1.set_ylabel("Index, 2022 = 100")
    a1.set_title("Malta since free public transport began", fontsize=9.5, loc="left", color=SLATE)
    a1.legend(frameon=False, fontsize=7.5, loc="upper left")
    c, b = MODAL["CAR"], MODAL["BUS_TOT"]
    yy = list(range(2015, 2025))
    a2.plot(yy, [c[y] for y in yy], color=SLATE, lw=2, label="Cars")
    a2.plot(yy, [b[y] for y in yy], color=BLUE, lw=2, label="Buses and coaches")
    a2.axvline(2022.8, color=RED, lw=1, ls="--")
    a2.text(2022.7, 51, "Oct 2022:\nfree buses", fontsize=7, color=RED, ha="right")
    a2.set_ylim(0, 100)
    a2.set_ylabel("% of inland passenger-km (estimate)")
    a2.set_title("Modal split (Eurostat estimates)", fontsize=9.5, loc="left", color=SLATE)
    a2.legend(frameon=False, fontsize=7.5, loc="center left")
    fig.tight_layout()
    fig.savefig(OUT / "fig1_car_use.png")


def fig2():
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(9.6, 4.2), dpi=220, gridspec_kw={"width_ratios": [1.15, 1]})
    mem = {g: v[2024] for g, v in REN.items() if g != "EU27_2020"}
    order = sorted(mem, key=lambda g: mem[g])
    a1.barh(range(len(order)), [mem[g] for g in order],
            color=[RED if g == "MT" else SAGE for g in order], height=0.75)
    a1.set_yticks(range(len(order)))
    a1.set_yticklabels(order, fontsize=6.6)
    a1.axvline(REN["EU27_2020"][2024], color=SLATE, lw=1, ls="--")
    a1.text(REN["EU27_2020"][2024] + 0.4, 1, "EU-27\n25.2%", fontsize=7, color=SLATE)
    a1.set_xlabel("Renewables, % of gross final energy consumption, 2024")
    a1.set_title("Renewable share, EU Member States", fontsize=9.5, loc="left", color=SLATE)
    e = CARS[("MT", "ELC")]
    ys = list(range(2019, 2026))
    a2.bar(ys, [e[y] for y in ys], color=GREEN, width=0.7)
    for y in ys:
        a2.text(y, e[y] + 150, f"{int(e[y]):,}", ha="center", fontsize=7, color=SLATE)
    a2.set_ylabel("Battery-electric passenger cars")
    a2.set_title("Battery-electric cars, Malta", fontsize=9.5, loc="left", color=SLATE)
    fig.tight_layout()
    fig.savefig(OUT / "fig2_renewables_ev.png")


if __name__ == "__main__":
    fig1()
    fig2()
    print("ok")
