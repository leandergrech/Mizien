"""Figures for Claim Check 095, drawn from data/cc-095/ (run fetch.py and calc.py first)."""
import csv
import datetime as dt
import pathlib

import matplotlib
matplotlib.use("Agg")
import matplotlib.dates as mdates  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib import font_manager as fm  # noqa: E402
from matplotlib.lines import Line2D  # noqa: E402
from matplotlib.patches import Patch  # noqa: E402

HERE = pathlib.Path(__file__).resolve().parent
D = HERE.parents[1] / "data" / "cc-095"
OUT = HERE / "out"
OUT.mkdir(exist_ok=True)
for f in ["LiberationSans-Regular", "LiberationSans-Bold", "LiberationSans-Italic"]:
    fm.fontManager.addfont(f"/usr/share/fonts/truetype/liberation/{f}.ttf")
plt.rcParams.update({"font.family": "Liberation Sans", "axes.spines.top": False, "axes.spines.right": False,
                     "axes.edgecolor": "#8A9399", "axes.labelcolor": "#2B3A42", "xtick.color": "#2B3A42",
                     "ytick.color": "#2B3A42", "axes.grid": True, "grid.color": "#E3E7E4", "grid.linewidth": 0.6})
GREEN, SAGE, AMBER, RED, SLATE, GREY, ORANGE, BLUE = ("#14452F", "#7FA88B", "#E3A72F", "#B5483A", "#2B3A42",
                                                      "#8A9399", "#D9772B", "#3C6E8F")


def rd(name):
    return list(csv.DictReader(open(D / name, encoding="utf-8")))


def fig1():
    """(a) HICP energy index, Malta vs EU-27; (b) diesel pump prices, Malta, Italy, EU average."""
    h = rd("eurostat_hicp_energy_mt_eu_history.csv")
    s = {}
    for r in h:
        if r["coicop18"] == "NRG" and r["unit"] == "I25" and r["value"] and r["time"] >= "2019-01":
            s.setdefault(r["geo"], []).append((dt.datetime.strptime(r["time"], "%Y-%m"), float(r["value"])))
    w = rd("oil_bulletin_mt_it_eu_weekly.csv")
    o = {}
    for r in w:
        if r["product"] == "diesel" and r["basis"] == "with taxes":
            o.setdefault(r["geo"], []).append((dt.datetime.strptime(r["date"], "%Y-%m-%d"), float(r["eur_per_1000"]) / 1000))
    fig, (a, b) = plt.subplots(1, 2, figsize=(9.6, 3.3), dpi=220, gridspec_kw={"wspace": 0.28})
    for geo, col, lab in (("EU27_2020", BLUE, "EU-27"), ("MT", GREEN, "Malta")):
        xs, ys = zip(*sorted(s[geo]))
        a.plot(xs, ys, color=col, lw=2.0 if geo == "MT" else 1.6)
        a.text(xs[-1] + dt.timedelta(days=25), ys[-1], f"{lab}\n{ys[-1]:.1f}", color=col, fontsize=8, va="center",
               fontweight="bold" if geo == "MT" else "normal")
    a.axhline(100, color=GREY, lw=0.6, ls=":")
    a.set_title("(a) Energy prices in the HICP, index 2025 = 100", fontsize=9, loc="left", color=SLATE)
    a.set_ylim(60, 135)
    a.set_xlim(dt.datetime(2019, 1, 1), dt.datetime(2027, 6, 1))
    a.xaxis.set_major_locator(mdates.YearLocator())
    a.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    a.tick_params(labelsize=7.5)
    for geo, col, lab, ls in (("EU", BLUE, "EU average", "-"), ("IT", ORANGE, "Italy", "--"), ("MT", GREEN, "Malta", "-")):
        xs, ys = zip(*sorted(o[geo]))
        b.plot(xs, ys, color=col, lw=2.0 if geo == "MT" else 1.3, ls=ls)
        dy = {"EU": -0.07, "IT": 0.07, "MT": 0}[geo]
        b.text(xs[-1] + dt.timedelta(days=25), ys[-1] + dy, f"{lab}\n€{ys[-1]:.2f}", color=col, fontsize=8, va="center",
               fontweight="bold" if geo == "MT" else "normal")
    b.axvline(dt.datetime(2020, 6, 15), color=GREY, lw=0.8, ls=":")
    b.text(dt.datetime(2020, 7, 20), 2.45, "Malta's price fixed\nfrom 15 Jun 2020", fontsize=7, color=SLATE, va="top")
    b.set_title("(b) Diesel at the pump, € per litre, weekly", fontsize=9, loc="left", color=SLATE)
    b.set_ylim(0.9, 2.5)
    b.set_xlim(dt.datetime(2019, 1, 1), dt.datetime(2027, 6, 1))
    b.xaxis.set_major_locator(mdates.YearLocator())
    b.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    b.tick_params(labelsize=7.5)
    for ax in (a, b):
        for lbl in ax.get_xticklabels():
            if lbl.get_text() == "2027":
                lbl.set_visible(False)
    fig.savefig(OUT / "fig1_prices.png", bbox_inches="tight", facecolor="white")
    plt.close(fig)


def fig2():
    """Annual change in HICP energy prices, August 2026, every EU country."""
    eu27 = "AT BE BG CY CZ DE DK EE EL ES FI FR HR HU IE IT LT LU LV MT NL PL PT RO SE SI SK".split()
    d = {r["geo"]: float(r["value"]) for r in rd("eurostat_hicp_energy_eu_2025_2026.csv")
         if r["coicop18"] == "NRG" and r["unit"] == "RCH_A" and r["time"] == "2026-08" and r["value"]}
    order = sorted(eu27, key=lambda g: d[g])
    fig, ax = plt.subplots(figsize=(9.6, 2.9), dpi=220)
    ax.bar(range(len(order)), [d[g] for g in order], width=0.7, color=[GREEN if g == "MT" else SAGE for g in order],
           zorder=2)
    ax.axhline(d["EU27_2020"], color=BLUE, lw=1.1, ls="--", zorder=3)
    ax.text(3.6, d["EU27_2020"] + 0.8, f"EU-27 as a whole {d['EU27_2020']:.1f}%", color=BLUE, fontsize=8, ha="left")
    ax.axhline(0, color=SLATE, lw=0.6)
    for i, g in enumerate(order[:3]):
        ax.text(i, d[g] + 0.7, f"{d[g]:.1f}", ha="center", fontsize=7.6, color=GREEN if g == "MT" else SLATE,
                fontweight="bold" if g == "MT" else "normal")
    ax.set_xticks(range(len(order)))
    ax.set_xticklabels(order, fontsize=8)
    ax.set_ylabel("% change on Aug 2025", fontsize=8.5)
    ax.tick_params(axis="y", labelsize=7.5)
    ax.grid(axis="x", visible=False)
    fig.savefig(OUT / "fig2_energy_inflation.png", bbox_inches="tight", facecolor="white")
    plt.close(fig)


def fig3():
    """What Malta's energy support cost, by measure and year (EUR million)."""
    cs = rd("cost_series.csv")
    cof = {int(r["year"]): float(r["eur_million"]) for r in cs if r["series"].startswith("Eurostat")}
    mi = {int(r["year"]): (float(r["eur_million"]), r["kind"]) for r in cs if r["series"].startswith("Minister")}
    imf = {int(r["year"]): (float(r["eur_million"]), r["kind"]) for r in cs if r["series"].startswith("IMF")}
    plan = [float(r["eur_million"]) for r in cs if r["series"].startswith("Draft Budgetary")][0]
    inv = [float(r["eur_million"]) for r in cs if r["series"].startswith("Commission")][0]
    fig, ax = plt.subplots(figsize=(9.6, 3.6), dpi=220)
    ax.bar(list(cof), list(cof.values()), width=0.55, color=SAGE, zorder=2)
    for y, v in cof.items():
        ax.text(y, v + 12, f"{v:.0f}", ha="center", fontsize=7.4, color=SLATE)
    ys = sorted(mi)
    ax.plot(ys, [mi[y][0] for y in ys], color=GREEN, lw=1.4, ls=":", zorder=3)
    for y in ys:
        v, k = mi[y]
        hollow = k in ("projection", "forecast")
        ax.plot([y + 0.0], [v], marker="o", ms=7.5, color=GREEN, mfc="white" if hollow else GREEN, mew=1.8, zorder=4)
        dx, dy, ha = {2023: (0.17, -40, "left"), 2025: (0.0, -42, "center"), 2026: (0.0, 40, "center"),
                      2027: (0.0, 40, "center")}[y]
        ax.text(y + dx, v + dy, f"{v:.1f}" if y != 2027 else "≈400", fontsize=7.6, color=GREEN, fontweight="bold",
                va="center", ha=ha)
    yi = sorted(imf)
    ax.plot([y + 0.12 for y in yi], [imf[y][0] for y in yi], color=BLUE, lw=1.1, zorder=3)
    for y in yi:
        v, k = imf[y]
        ax.plot([y + 0.12], [v], marker="^", ms=6.5, color=BLUE, mfc="white" if k == "projection" else BLUE, mew=1.4, zorder=4)
    ax.plot([2023 - 0.22], [plan], marker="s", ms=7, color=ORANGE, mfc="white", mew=1.8, zorder=4)
    ax.plot([2023 + 0.22], [inv], marker="D", ms=6, color=RED, zorder=4)
    ax.text(2022.6, plan, f"{plan:.0f} allocated (Oct 2022)", fontsize=7.4, color=ORANGE, ha="right", va="center")
    ax.text(2023.4, inv, f"{inv:.0f} as booked by the Commission", fontsize=7.4, color=RED, ha="left", va="center")
    ax.set_xlim(2018.4, 2027.7)
    ax.set_ylim(0, 960)
    ax.set_xticks(range(2019, 2028))
    ax.tick_params(labelsize=8)
    ax.set_ylabel("EUR million", fontsize=8.5)
    ax.grid(axis="x", visible=False)
    ax.legend(handles=[Patch(color=SAGE, label="Eurostat: general-government subsidies for fuel and energy (COFOG 04.3), outturn"),
                       Line2D([], [], color=GREEN, marker="o", ms=6, lw=1.2, ls=":",
                              label="Minister, 30 Sep 2026: energy and food subsidies (hollow: 2026 projection, 2027 forecast)"),
                       Line2D([], [], color=BLUE, marker="^", ms=6, lw=1.1,
                              label="IMF Article IV: electricity and fuel subsidies (share of GDP in euros; hollow: projection)"),
                       Line2D([], [], color=ORANGE, marker="s", ms=6, mfc="white", lw=0,
                              label="Draft Budgetary Plan 2023: energy subsidies allocated for 2023"),
                       Line2D([], [], color=RED, marker="D", ms=5.5, lw=0,
                              label="Commission subsidy inventory: Malta's fossil-fuel subsidies, 2023 (CC-113)")],
              frameon=False, fontsize=7.2, loc="upper left", bbox_to_anchor=(0.0, 1.02))
    fig.savefig(OUT / "fig3_costs.png", bbox_inches="tight", facecolor="white")
    plt.close(fig)


fig1()
fig2()
fig3()
print("figures in", OUT)
