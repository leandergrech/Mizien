"""Figures for Claim Check 135 (inputs in data/cc-135/; run fetch.py first)."""
import csv, pathlib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm

HERE = pathlib.Path(__file__).resolve().parent
D = HERE.parents[1] / "data" / "cc-135"
OUT = HERE / "out"
OUT.mkdir(exist_ok=True)
for f in ["LiberationSans-Regular", "LiberationSans-Bold", "LiberationSans-Italic"]:
    fm.fontManager.addfont(f"/usr/share/fonts/truetype/liberation/{f}.ttf")
plt.rcParams.update({"font.family": "Liberation Sans", "axes.spines.top": False, "axes.spines.right": False,
                     "axes.edgecolor": "#8A9399"})
GREEN, AMBER, BLUE, SLATE, GREY, RED = "#14452F", "#E3A72F", "#3F6E8F", "#2B3A42", "#8A9399", "#B5483A"

peak, avgmax = {}, {}
for r in csv.DictReader(open(D / "nso_max_demand.csv", encoding="utf-8")):
    y, v = int(r["year"]), int(r["max_demand_mw"])
    if r["month"] == "AVG":
        avgmax[y] = v
    else:
        peak[y] = max(peak.get(y, 0), v)
E = {(r["dataset"], r["item"], r["period"]): float(r["value"])
     for r in csv.DictReader(open(D / "eurostat_pop_tourism_electricity.csv", encoding="utf-8"))}
T = {r["month"]: r for r in csv.DictReader(open(D / "ghcnd_luqa_monthly.csv", encoding="utf-8"))}
YS = list(range(2017, 2026))


def hot(y):
    ms = [k for k in T if k.startswith(str(y)) and T[k]["tavg_mean_c"] and int(T[k]["tavg_days"]) >= 28]
    return max(float(T[m]["tavg_mean_c"]) for m in ms)


def present(y):
    n = max(E[("tour_occ_nim", "NIGHTS_I551-I553_TOTAL", "%d-%02d" % (y, m))] for m in range(1, 13))
    return E[("demo_gind", "AVG", str(y))] + n / 31


def fig1():
    fig, ax = plt.subplots(figsize=(9.2, 3.8), dpi=220)
    cols = [AMBER if y in (2018, 2023) else "#B9C4C9" for y in YS]
    ax.bar(YS, [peak[y] for y in YS], color=cols, width=0.62)
    for y in YS:
        ax.text(y, peak[y] + 8, str(peak[y]), ha="center", fontsize=8.5,
                color="#9A6B00" if y in (2018, 2023) else SLATE, weight="bold" if y in (2018, 2023) else "normal")
    ax.set_ylim(0, 760); ax.set_xticks(YS)
    ax.set_ylabel("Annual peak demand, MW", fontsize=8.5, color=SLATE)
    ax.tick_params(labelsize=8.5, colors=SLATE)
    ax2 = ax.twinx()
    ax2.plot(YS, [hot(y) for y in YS], color=RED, lw=2, marker="o", ms=4)
    for y in (2018, 2023):
        ax2.text(y + 0.12, hot(y) + (-0.45 if y == 2018 else 0.3), "%.1f °C" % hot(y), fontsize=8, color=RED)
    ax2.set_ylim(26, 36); ax2.spines["right"].set_visible(True); ax2.spines["top"].set_visible(False)
    ax2.set_ylabel("Hottest-month mean temperature, Luqa (°C)", fontsize=8.5, color=RED)
    ax2.tick_params(labelsize=8.5, colors=RED)
    ax.text(2016.55, -125, "Sources: NSO Electricity Supply releases (maximum demand, the highest month of each year); NOAA GHCN-Daily, "
            "Luqa (MT000016597). The IMF's end years are in amber.", fontsize=7, color=GREY, clip_on=False)
    fig.savefig(OUT / "fig1_peaks.png", bbox_inches="tight", facecolor="white")


def fig2():
    fig, ax = plt.subplots(figsize=(9.2, 3.8), dpi=220)
    series = [("Annual peak demand (NSO)", [peak[y] / peak[2018] * 100 for y in YS], AMBER, YS),
              ("Mean of the 12 monthly maxima (NSO)", [avgmax[y] / avgmax[2018] * 100 for y in YS], BLUE, YS),
              ("Final electricity consumption (Eurostat)",
               [E[("nrg_cb_e", "FC", str(y))] / E[("nrg_cb_e", "FC", "2018")] * 100 for y in YS], SLATE, YS),
              ("Population + peak-month tourists (Eurostat)", [present(y) / present(2018) * 100 for y in YS], GREEN, YS)]
    for lab, v, c, xs in series:
        ax.plot(xs, v, color=c, lw=2.3, marker="o", ms=3.5, label=lab)
        ax.text(2025.15, v[-1], "%.0f" % v[-1], fontsize=8, color=c, va="center")
    ax.axhline(100, color=GREY, lw=0.8, ls=":")
    ax.axvspan(2017.9, 2023.1, color="#F6F4EE", zorder=0)
    ax.text(2020.5, 151, "IMF window 2018–2023", ha="center", fontsize=8, color=GREY)
    ax.set_xticks(YS); ax.set_xlim(2016.7, 2025.7); ax.set_ylim(70, 156)
    ax.set_ylabel("Index, 2018 = 100", fontsize=8.5, color=SLATE)
    ax.tick_params(labelsize=8.5, colors=SLATE)
    ax.legend(frameon=False, fontsize=8, loc="lower right", ncol=2)
    ax.text(2016.7, 50, "Sources: NSO NR 177/2022, 176/2023, 184/2024, 178/2025, 178/2026; Eurostat demo_gind (AVG), tour_occ_nim "
            "(nights in the peak month / 31, the IMF's method), nrg_cb_e (FC). Retrieved 26 Oct 2026.", fontsize=7, color=GREY, clip_on=False)
    fig.savefig(OUT / "fig2_index.png", bbox_inches="tight", facecolor="white")


def fig3():
    fig, ax = plt.subplots(figsize=(6.4, 3.6), dpi=220)
    for y in YS:
        c = AMBER if y in (2018, 2023) else BLUE
        ax.scatter(hot(y), peak[y], color=c, s=34, zorder=3)
        ax.annotate(str(y), (hot(y), peak[y]), xytext=(5, -3), textcoords="offset points", fontsize=8, color=SLATE)
    ax.set_xlabel("Hottest-month mean temperature, Luqa (°C)", fontsize=8.5, color=SLATE)
    ax.set_ylabel("Annual peak demand, MW", fontsize=8.5, color=SLATE)
    ax.tick_params(labelsize=8.5, colors=SLATE)
    ax.set_xlim(26.6, 29.8); ax.set_ylim(440, 690)
    fig.text(0.01, -0.04, "Sources: NSO (peak demand); NOAA GHCN-Daily, Luqa. 2017–2025; Pearson r = 0.70 (nine years, descriptive).",
             fontsize=7, color=GREY)
    fig.savefig(OUT / "fig3_scatter.png", bbox_inches="tight", facecolor="white")


if __name__ == "__main__":
    fig1(); fig2(); fig3()
