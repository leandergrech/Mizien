"""Figures for Claim Check 034, drawn from data/cc-034/ (run fetch.py, then calc.py).
Output: out/fig1_pm10_days.png, fig2_annual.png, fig3_power.png, fig4_school.png
(The 12-months-before-and-after chart for free public transport, drawn in the first draft, was dropped from the report
to keep it to 10 pages; its numbers are in the text and in checks.csv, F section.)"""
import csv
import datetime as dt
import pathlib
from collections import defaultdict

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib import font_manager as fm  # noqa: E402
from matplotlib.lines import Line2D  # noqa: E402
from matplotlib.patches import Patch  # noqa: E402

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[1]
D = ROOT / "data" / "cc-034"
OUT = HERE / "out"
OUT.mkdir(exist_ok=True)
for f in ["LiberationSans-Regular", "LiberationSans-Bold", "LiberationSans-Italic"]:
    fm.fontManager.addfont(f"/usr/share/fonts/truetype/liberation/{f}.ttf")
plt.rcParams.update({"font.family": "Liberation Sans", "axes.spines.top": False, "axes.spines.right": False,
                     "axes.edgecolor": "#8A9399", "axes.labelcolor": "#2B3A42", "xtick.color": "#2B3A42",
                     "ytick.color": "#2B3A42"})
GREEN, SLATE, GREY, PALEGREY = "#14452F", "#2B3A42", "#8A9399", "#EEF0F1"
# station colours (validated as a categorical set: scripts/validate_palette.js, light mode, all checks pass)
C = {"MT00005": "#B5483A", "MT00011": "#B5483A", "MT00004": "#2C6EAE", "MT00008": "#C9962A", "MT00007": "#2E7D4F",
     "MT00003": SLATE, "MT00009": "#7A5195"}
NAME = {"MT00005": "Msida (traffic)", "MT00011": "Msida, new point (from 2024)", "MT00004": "Żejtun (urban background)",
        "MT00008": "Attard (urban background)", "MT00007": "Għarb (rural background)", "MT00003": "Kordin (industrial)",
        "MT00009": "St Paul’s Bay (traffic)"}
ANNUAL = {(r["station"], r["pollutant"], int(r["year"])): r for r in csv.DictReader(open(D / "annual.csv",
                                                                                          encoding="utf-8"))}
G = list(csv.DictReader(open(D / "g_attainment.csv", encoding="utf-8")))


def daily(name):
    out = defaultdict(dict)
    for r in csv.DictReader(open(D / name, encoding="utf-8")):
        d = dt.date.fromisoformat(r["date"])
        for k, v in r.items():
            if k != "date" and v != "":
                out[k][d] = float(v)
    return out


def title(ax, t):
    ax.set_title(t, fontsize=9.5, color=GREEN, loc="left", fontweight="bold", pad=8)


def marker(ax, x, label, ytext, ha="left", col=SLATE):
    ax.axvline(x, color=col, lw=0.9, ls="--", zorder=1)
    ax.text(x + (0.06 if ha == "left" else -0.06), ytext, label, fontsize=7.4, color=col, ha=ha, va="top")


# ------------------------------------------------------------------ figure 1: PM10 days over the daily limit
def fig1():
    pm10 = daily("pm10_daily.csv")
    yrs = list(range(2013, 2026))
    fig, ax = plt.subplots(figsize=(9.6, 3.25), dpi=220)
    for y in yrs:
        st = "MT00005" if y <= 2023 else "MT00011"
        n = sum(1 for d, v in pm10[st].items() if d.year == y and v > 50)
        ax.bar(y, n, width=0.62, color="#E9C9C3" if st == "MT00005" else "white", ec=C[st],
               lw=0 if st == "MT00005" else 1.1, hatch=None if st == "MT00005" else "////", zorder=2)
        ax.text(y, n + 1.2, str(n), ha="center", va="bottom", fontsize=7.4, color=GREY,
                bbox={"fc": "white", "ec": "none", "pad": 0.3}, zorder=3)
    fin = {}
    for r in G:
        if (r["pollutant"] == "PM10" and r["reportingMetric"] == "daysAbove" and r["zone"] == "ZON-MT0001"
                and r["objectiveType"] == "LV" and r["final_count"]):
            fin[int(r["year"])] = int(r["final_count"])
    xs = sorted(y for y in fin if y in yrs and y <= 2023)
    ax.plot(xs, [fin[y] for y in xs], color=C["MT00005"], lw=2, marker="o", ms=6, zorder=4,
            mec="white", mew=1.2)
    # ERA's 2024-25 counts are zone counts from other stations (new Msida point, Attard, Zejtun): shown hollow
    zs = [y for y in (2023, 2024, 2025) if y in fin]
    ax.plot(zs, [fin[y] for y in zs], color=C["MT00005"], lw=1.4, ls=(0, (3, 2)), zorder=3)
    ax.plot(zs[1:], [fin[y] for y in zs[1:]], color=C["MT00005"], lw=0, marker="o", ms=6, mfc="white", mew=1.4,
            zorder=5)
    for y in xs + zs[1:]:
        bold = fin[y] > 35 and y <= 2023
        above = bold
        ax.text(y - 0.14 if above else y + 0.12, fin[y] + (2.0 if above else -1.5), str(fin[y]), fontsize=8.2,
                color=C["MT00005"] if bold else SLATE, fontweight="bold" if bold else "normal",
                va="bottom" if above else "top", ha="right" if above else "left",
                bbox={"fc": "white", "ec": "none", "pad": 0.4}, zorder=6)
    gh = [sum(1 for d, v in pm10["MT00007"].items() if d.year == y and v > 50) for y in yrs]
    ax.plot(yrs, gh, color=C["MT00007"], lw=1.6, ls="-", marker="s", ms=4.5, zorder=3)
    ax.axhline(35, color=SLATE, lw=1.0, ls=":", zorder=1)
    ax.text(2012.45, 33.8, "35 days\nallowed", fontsize=7.6, color=SLATE, va="top", ha="left",
            bbox={"fc": "white", "ec": "none", "pad": 0.5}, zorder=5)
    ax.set_ylim(0, 112)
    ax.set_xlim(2012.4, 2025.6)
    marker(ax, 2018 + 8.5 / 12, "Free school\ntransport", 111)
    marker(ax, 2021 + 5.5 / 12, "Fast ferry", 111)
    marker(ax, 2022 + 9 / 12, "Free public\ntransport", 104)
    marker(ax, 2015 + 3 / 12, "Interconnector;\nMarsa station\nshut", 111)
    marker(ax, 2017.5, "Delimara\non gas", 111)
    marker(ax, 2024 + 0.5 / 12, "Msida monitor\nmoved ~300 m", 111, col=GREY)
    ax.set_xticks(yrs)
    ax.tick_params(labelsize=8.3)
    ax.set_ylabel("Days with daily PM10 above 50 µg/m³", fontsize=8.5)
    hl = [Patch(fc="#E9C9C3", ec="none"), Patch(fc="white", ec=C["MT00005"], hatch="////"),
          Line2D([], [], color=C["MT00005"], lw=2, marker="o", mec="white"),
          Line2D([], [], color=C["MT00005"], lw=1.4, ls=(0, (3, 2)), marker="o", mfc="white", mew=1.4),
          Line2D([], [], color=C["MT00007"], lw=1.6, marker="s", ms=4.5)]
    lb = ["Msida (old point, to 2023), all days (before deduction)", "Msida new point, all days (2024–25)",
          "Msida (old point), after ERA deducts dust and sea salt",
          "ERA’s zone count, 2024–25 (other stations; not comparable)", "Għarb (rural background), all days"]
    ax.legend(hl, lb, frameon=False, fontsize=8.2, loc="upper left", bbox_to_anchor=(-0.01, -0.08), ncol=3, columnspacing=1.2, handlelength=1.8)
    title(ax, "PM10 at the Msida traffic monitor: days over the daily limit, 2013–2025")
    fig.savefig(OUT / "fig1_pm10_days.png", bbox_inches="tight", facecolor="white")
    plt.close(fig)


# ------------------------------------------------------------------ figure 2: annual means, traffic vs background
def fig2():
    fig, axs = plt.subplots(1, 3, figsize=(9.6, 2.15), dpi=220)
    panels = [("PM10", ["MT00005", "MT00011", "MT00004", "MT00008", "MT00007"], 50),
              ("PM2.5", ["MT00005", "MT00011", "MT00004", "MT00008", "MT00007"], 20),
              ("NO2", ["MT00005", "MT00011", "MT00004", "MT00008", "MT00007"], 42)]
    for ax, (pol, sts, ymax) in zip(axs, panels):
        for st in sts:
            pts = [(y, float(ANNUAL[(st, pol, y)]["mean"]), float(ANNUAL[(st, pol, y)]["coverage_pct"]))
                   for y in range(2013, 2026) if (st, pol, y) in ANNUAL]
            if not pts:
                continue
            xs, ys = [p[0] for p in pts], [p[1] for p in pts]
            ls = "--" if st == "MT00011" else "-"
            ax.plot(xs, ys, color=C[st], lw=1.8 if st in ("MT00005", "MT00011") else 1.3, ls=ls, zorder=3)
            for x, yv, cv in pts:
                ax.plot(x, yv, marker="o", ms=4.2, color=C[st], mfc=C[st] if cv >= 85 else "white", mew=1.1,
                        zorder=4)
        for x in (2018 + 8.5 / 12, 2022 + 9 / 12):
            ax.axvline(x, color=GREY, lw=0.8, ls="--", zorder=1)
        ax.set_xlim(2012.5, 2025.5)
        ax.set_ylim(0, ymax)
        ax.set_xticks([2013, 2016, 2019, 2022, 2025])
        ax.tick_params(labelsize=7.8)
        lab = {"PM10": "PM10", "PM2.5": "PM2.5", "NO2": "NO₂"}[pol]
        ax.set_title(f"{lab}, annual mean (µg/m³)", fontsize=8.6, color=SLATE, loc="left", fontweight="bold")
    axs[0].text(2018 + 8.5 / 12 - 0.15, 1.2, "Free school\ntransport", fontsize=6.8, color=GREY, va="bottom", ha="right")
    axs[0].text(2022 + 9 / 12 + 0.15, 1.2, "Free public\ntransport", fontsize=6.8, color=GREY, va="bottom", ha="left")
    hl = [Line2D([], [], color=C[s], lw=1.8, ls="--" if s == "MT00011" else "-", marker="o", ms=4) for s in
          ("MT00005", "MT00011", "MT00004", "MT00008", "MT00007")]
    hl.append(Line2D([], [], ls="", marker="o", mfc="white", mec=SLATE, ms=4.5))
    lb = [NAME[s] for s in ("MT00005", "MT00011", "MT00004", "MT00008", "MT00007")] + ["Year with under 85% of data"]
    fig.legend(hl, lb, frameon=False, fontsize=7.8, loc="upper left", bbox_to_anchor=(0.01, 0.02), ncol=3)
    fig.suptitle("Annual means at the Msida traffic monitor and the background stations, 2013–2025", x=0.01, ha="left",
                 fontsize=9.5, color=GREEN, fontweight="bold")
    fig.tight_layout(rect=(0, 0, 1, 0.95))
    fig.savefig(OUT / "fig2_annual.png", bbox_inches="tight", facecolor="white")
    plt.close(fig)


# ------------------------------------------------------------------ figure 3: power sector
def fig3():
    emis = defaultdict(dict)
    for r in csv.DictReader(open(D / "eurostat_emissions.csv", encoding="utf-8")):
        if r["src_nfr"] == "NFR1A1A":
            emis[r["airpol"]][int(r["time"])] = float(r["value"])
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(9.6, 2.75), dpi=220)
    yrs = list(range(2005, 2025))
    for p, lab, col in (("SOX", "Sulphur oxides", C["MT00005"]), ("NOX", "Nitrogen oxides", C["MT00004"]),
                        ("PM2_5", "PM2.5", C["MT00008"])):
        a1.plot(yrs, [emis[p][y] / 1000 for y in yrs], color=col, lw=1.8, marker="o", ms=3.5, label=lab)
    a1.set_ylabel("Thousand tonnes a year", fontsize=8.3)
    a1.set_ylim(0, 12.5)
    a1.set_title("A. Emissions from public electricity production", fontsize=8.6, color=SLATE, loc="left",
                 fontweight="bold")
    a1.text(2008.3, 10.6, "Sulphur oxides", fontsize=7.6, color=C["MT00005"], ha="left")
    a1.text(2005.0, 6.3, "Nitrogen oxides", fontsize=7.6, color=C["MT00004"])
    a1.text(2005.0, 1.0, "PM2.5", fontsize=7.6, color=C["MT00008"])
    for ax in (a1, a2):
        for x in (2015 + 3 / 12, 2017.5):
            ax.axvline(x, color=GREY, lw=0.8, ls="--", zorder=1)
        ax.tick_params(labelsize=7.8)
        ax.set_xticks([2006, 2010, 2014, 2018, 2022])
    a1.text(2015.15, 12.3, "2015: inter-\nconnector;\nMarsa shut", fontsize=6.8, color=GREY, va="top", ha="right")
    a1.text(2017.6, 12.3, "2017: Delimara\non gas", fontsize=6.8, color=GREY, va="top")
    for st in ("MT00003", "MT00004", "MT00005", "MT00007"):
        pts = [(y, float(ANNUAL[(st, "SO2", y)]["mean"]), float(ANNUAL[(st, "SO2", y)]["coverage_pct"]))
               for y in range(2006, 2024) if (st, "SO2", y) in ANNUAL]
        a2.plot([p[0] for p in pts], [p[1] for p in pts], color=C[st], lw=1.5, label=NAME[st].split(" (")[0])
        for x, yv, cv in pts:
            a2.plot(x, yv, marker="o", ms=3.8, color=C[st], mfc=C[st] if cv >= 85 else "white", mew=1)
    a2.set_ylim(0, 19)
    a2.set_title("B. Sulphur dioxide in the air, annual mean (µg/m³)", fontsize=8.6, color=SLATE, loc="left",
                 fontweight="bold")
    a2.legend(frameon=False, fontsize=7.6, loc="upper right")
    fig.suptitle("The power-sector reform: emissions and sulphur dioxide in the air", x=0.01, ha="left", fontsize=9.5,
                 color=GREEN, fontweight="bold")
    fig.tight_layout(rect=(0, 0, 1, 0.96))
    fig.savefig(OUT / "fig3_power.png", bbox_inches="tight", facecolor="white")
    plt.close(fig)


# ------------------------------------------------------------------ figure 4: free school transport
def fig4():
    acc = defaultdict(lambda: [0.0, 0])
    for r in csv.DictReader(open(D / "diurnal.csv", encoding="utf-8")):
        if r["season"] == "Oct-Dec" and r["daytype"] == "weekday" and 7 <= int(r["hour"]) <= 9:
            k = (r["station"], r["pollutant"], int(r["year"]))
            acc[k][0] += float(r["mean"]) * int(r["n_hours"])
            acc[k][1] += int(r["n_hours"])

    def wdays(y):   # weekdays in October-December
        d, n = dt.date(y, 10, 1), 0
        while d <= dt.date(y, 12, 31):
            n += d.weekday() < 5
            d += dt.timedelta(1)
        return n

    cov = lambda st, pol, y: 100 * acc[(st, pol, y)][1] / (3 * wdays(y))   # share of the 07:00-09:59 hours with a value
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(9.6, 3.0), dpi=220, gridspec_kw={"width_ratios": [1.35, 1]})
    yrs = list(range(2013, 2024))
    for st in ("MT00005", "MT00004", "MT00008"):
        pts = [(y, acc[(st, "NO2", y)][0] / acc[(st, "NO2", y)][1], cov(st, "NO2", y)) for y in yrs
               if acc[(st, "NO2", y)][1] > 100]
        a1.plot([p[0] for p in pts], [p[1] for p in pts], color=C[st], lw=1.8 if st == "MT00005" else 1.3, zorder=3)
        for x, yv, cv in pts:
            a1.plot(x, yv, marker="o", ms=4.2, color=C[st], mfc=C[st] if cv >= 85 else "white", mew=1.1, zorder=4)
        a1.text(pts[-1][0] + 0.15, pts[-1][1], NAME[st].split(" (")[0], fontsize=7.6, color=C[st], va="center")
    # the sustained fall: mean of the annual values 2013-17 and 2019-23 at Msida
    ann = {y: acc[("MT00005", "NO2", y)][0] / acc[("MT00005", "NO2", y)][1] for y in yrs}
    for ys_, lab in (((2013, 2017), 2013.0), ((2019, 2023), 2019.0)):
        m = sum(ann[y] for y in range(ys_[0], ys_[1] + 1)) / (ys_[1] - ys_[0] + 1)
        a1.plot([ys_[0] - 0.3, ys_[1] + 0.3], [m, m], color=C["MT00005"], lw=1.0, ls=":", zorder=2)
    m18 = ann[2018]
    a1.text(2012.7, 3, "Dotted: Msida mean of the annual\nvalues, 2013–17: 60.4; 2019–23: 48.9", fontsize=7.2,
            color=C["MT00005"], va="bottom", ha="left")
    a1.annotate("Oct–Dec 2018: first term of\nfree school transport,\nhighest of 2013–2023",
                xy=(2018, m18), xytext=(2019.3, 76), fontsize=7.4, color=C["MT00005"],
                arrowprops={"arrowstyle": "-", "color": C["MT00005"], "lw": 0.7})
    a1.set_ylim(0, 82)
    a1.set_xlim(2012.5, 2024.6)
    a1.set_title("A. NO₂, school-term weekday mornings (µg/m³)", fontsize=8.6, color=SLATE, loc="left",
                 fontweight="bold")
    pts = [(y, acc[("MT00005", "CO", y)][0] / acc[("MT00005", "CO", y)][1], cov("MT00005", "CO", y)) for y in yrs
           if acc[("MT00005", "CO", y)][1] > 100]
    a2.plot([p[0] for p in pts], [p[1] for p in pts], color=C["MT00005"], lw=1.8, zorder=3)
    for x, yv, cv in pts:
        a2.plot(x, yv, marker="o", ms=4.2, color=C["MT00005"], mfc=C["MT00005"] if cv >= 85 else "white", mew=1.1,
                zorder=4)
    a2.set_ylim(0, 1.3)
    a2.set_xlim(2012.5, 2023.5)
    a2.set_title("B. CO at Msida, same hours (mg/m³)", fontsize=8.6, color=SLATE, loc="left", fontweight="bold")
    for ax, top in ((a1, 80), (a2, 1.27)):
        ax.axvline(2018 + 8.5 / 12, color=GREY, lw=0.8, ls="--", zorder=1)
        if ax is a2:
            ax.text(2018 + 8.5 / 12 - 0.1, top, "Free school\ntransport", fontsize=6.8, color=GREY, va="top", ha="right")
        ax.set_xticks([2013, 2015, 2017, 2019, 2021, 2023])
        ax.tick_params(labelsize=7.8)
    fig.suptitle("Free school transport (from September 2018): morning rush hour, October–December, by year", x=0.01,
                 ha="left", fontsize=9.5, color=GREEN, fontweight="bold")
    fig.tight_layout(rect=(0, 0, 1, 0.96))
    fig.savefig(OUT / "fig4_school.png", bbox_inches="tight", facecolor="white")
    plt.close(fig)


if __name__ == "__main__":
    fig1()
    fig2()
    fig3()
    fig4()
    print("figures written to", OUT)
