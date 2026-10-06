"""Figures for Claim Check 034, drawn from data/cc-034/ (run fetch.py, then calc.py).
Output: out/fig1_pm10_days.png, fig2_annual.png, fig3_power.png, fig4_school.png, fig5_free_pt.png"""
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
SRC = "Source: EEA air-quality download service (E1a validated data), retrieved 6 Oct 2026; Miżien calculations."
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


def note(fig, t, y=-0.02):
    fig.text(0.01, y, t, fontsize=7, color=GREY, va="top")


def marker(ax, x, label, ytext, ha="left", col=SLATE):
    ax.axvline(x, color=col, lw=0.9, ls="--", zorder=1)
    ax.text(x + (0.06 if ha == "left" else -0.06), ytext, label, fontsize=7.4, color=col, ha=ha, va="top")


# ------------------------------------------------------------------ figure 1: PM10 days over the daily limit
def fig1():
    pm10 = daily("pm10_daily.csv")
    yrs = list(range(2013, 2026))
    fig, ax = plt.subplots(figsize=(9.6, 4.8), dpi=220)
    for y in yrs:
        st = "MT00005" if y <= 2023 else "MT00011"
        n = sum(1 for d, v in pm10[st].items() if d.year == y and v > 50)
        ax.bar(y, n, width=0.62, color="#E9C9C3" if st == "MT00005" else "white", ec=C[st],
               lw=0 if st == "MT00005" else 1.1, hatch=None if st == "MT00005" else "////", zorder=2)
        ax.text(y, n + 1.2, str(n), ha="center", va="bottom", fontsize=7.4, color=GREY)
    fin = {}
    for r in G:
        if (r["pollutant"] == "PM10" and r["reportingMetric"] == "daysAbove" and r["zone"] == "ZON-MT0001"
                and r["objectiveType"] == "LV" and r["final_count"]):
            fin[int(r["year"])] = int(r["final_count"])
    xs = sorted(y for y in fin if y in yrs)
    ax.plot(xs, [fin[y] for y in xs], color=C["MT00005"], lw=2, marker="o", ms=6, zorder=4,
            mec="white", mew=1.2)
    for y in xs:
        bold = fin[y] > 35
        above = bold or y == 2020
        ax.text(y - 0.14 if above else y + 0.12, fin[y] + (2.0 if above else -1.5), str(fin[y]), fontsize=8.2,
                color=C["MT00005"] if bold else SLATE, fontweight="bold" if bold else "normal",
                va="bottom" if above else "top", ha="right" if above else "left",
                bbox={"fc": "white", "ec": "none", "pad": 0.4}, zorder=5)
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
    marker(ax, 2015 + 3 / 12, "Interconnector;\nMarsa station\nclosed", 111)
    marker(ax, 2017.5, "Delimara\non gas", 111)
    marker(ax, 2024 + 0.5 / 12, "Msida monitor\nmoved ~300 m", 111, col=GREY)
    ax.set_xticks(yrs)
    ax.tick_params(labelsize=8.3)
    ax.set_ylabel("Days with daily PM10 above 50 µg/m³", fontsize=8.5)
    hl = [Patch(fc="#E9C9C3", ec="none"), Patch(fc="white", ec=C["MT00005"], hatch="////"),
          Line2D([], [], color=C["MT00005"], lw=2, marker="o", mec="white"),
          Line2D([], [], color=C["MT00007"], lw=1.6, marker="s", ms=4.5)]
    lb = ["Msida, all days (before deduction)", "Msida new point, all days",
          "Msida, after ERA deducts dust and sea salt", "Għarb (rural background), all days"]
    ax.legend(hl, lb, frameon=False, fontsize=8.2, loc="upper left", bbox_to_anchor=(-0.01, -0.07), ncol=2)
    title(ax, "PM10 at the Msida traffic monitor: days over the daily limit, 2013–2025")
    note(fig, "Bars and the Għarb line: our counts from the EEA’s validated daily values (2024–25 from the new Msida "
         "sampling point). Red line: ERA’s own count after deducting natural\nsources, as reported to the EEA (dataflow "
         "G; 2015 onwards). Markers show when the measures began (plan, sections 10.11 and 11). " + SRC, y=-0.075)
    fig.savefig(OUT / "fig1_pm10_days.png", bbox_inches="tight", facecolor="white")
    plt.close(fig)


# ------------------------------------------------------------------ figure 2: annual means, traffic vs background
def fig2():
    fig, axs = plt.subplots(1, 3, figsize=(9.6, 3.9), dpi=220)
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
    axs[0].text(2018 + 8.5 / 12 + 0.1, 49, "Free school\ntransport", fontsize=6.8, color=GREY, va="top")
    axs[0].text(2022 + 9 / 12 - 0.1, 49, "Free\npublic\ntransport", fontsize=6.8, color=GREY, va="top", ha="right")
    hl = [Line2D([], [], color=C[s], lw=1.8, ls="--" if s == "MT00011" else "-", marker="o", ms=4) for s in
          ("MT00005", "MT00011", "MT00004", "MT00008", "MT00007")]
    hl.append(Line2D([], [], ls="", marker="o", mfc="white", mec=SLATE, ms=4.5))
    lb = [NAME[s] for s in ("MT00005", "MT00011", "MT00004", "MT00008", "MT00007")] + ["Year with under 85% of data"]
    fig.legend(hl, lb, frameon=False, fontsize=7.8, loc="upper left", bbox_to_anchor=(0.01, 0.02), ncol=3)
    fig.suptitle("Annual means at the Msida traffic monitor and the background stations, 2013–2025", x=0.01, ha="left",
                 fontsize=9.5, color=GREEN, fontweight="bold")
    fig.tight_layout(rect=(0, 0, 1, 0.97))
    note(fig, "Attard has PM10 only from 2024. The Msida monitor moved about 300 m in January 2024 (dashed), so 2024–25 "
         "are not a continuation of the earlier series. Vertical lines:\nfree school transport (September 2018) and free "
         "public transport (October 2022). " + SRC, y=-0.115)
    fig.savefig(OUT / "fig2_annual.png", bbox_inches="tight", facecolor="white")
    plt.close(fig)


# ------------------------------------------------------------------ figure 3: power sector
def fig3():
    emis = defaultdict(dict)
    for r in csv.DictReader(open(D / "eurostat_emissions.csv", encoding="utf-8")):
        if r["src_nfr"] == "NFR1A1A":
            emis[r["airpol"]][int(r["time"])] = float(r["value"])
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(9.6, 3.8), dpi=220)
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
    a1.text(2015.15, 12.3, "2015: inter-\nconnector;\nMarsa closed", fontsize=6.8, color=GREY, va="top", ha="right")
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
    note(fig, "A: Eurostat env_air_emis, NFR 1A1a, Malta’s inventory reported to the EEA (updated 7 Sep 2026). B: EEA "
         "validated data (AirBase before 2013); hollow markers: under 85% of hours valid.\nKordin, downwind of the "
         "Marsa power station, closed at the end of 2016. Retrieved 6 Oct 2026.", y=-0.02)
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
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(9.6, 3.7), dpi=220, gridspec_kw={"width_ratios": [1.35, 1]})
    yrs = list(range(2013, 2024))
    for st in ("MT00005", "MT00004", "MT00008"):
        pts = [(y, acc[(st, "NO2", y)][0] / acc[(st, "NO2", y)][1]) for y in yrs if acc[(st, "NO2", y)][1] > 100]
        a1.plot([p[0] for p in pts], [p[1] for p in pts], color=C[st], lw=1.8 if st == "MT00005" else 1.3,
                marker="o", ms=4)
        a1.text(pts[-1][0] + 0.15, pts[-1][1], NAME[st].split(" (")[0], fontsize=7.6, color=C[st], va="center")
    m18 = acc[("MT00005", "NO2", 2018)][0] / acc[("MT00005", "NO2", 2018)][1]
    a1.annotate("Oct–Dec 2018: first term of\nfree school transport,\nhighest of 2013–2023",
                xy=(2018, m18), xytext=(2019.3, 76), fontsize=7.4, color=C["MT00005"],
                arrowprops={"arrowstyle": "-", "color": C["MT00005"], "lw": 0.7})
    a1.set_ylim(0, 82)
    a1.set_xlim(2012.5, 2024.6)
    a1.set_title("A. NO₂, school-term weekday mornings (µg/m³)", fontsize=8.6, color=SLATE, loc="left",
                 fontweight="bold")
    pts = [(y, acc[("MT00005", "CO", y)][0] / acc[("MT00005", "CO", y)][1]) for y in yrs
           if acc[("MT00005", "CO", y)][1] > 100]
    a2.plot([p[0] for p in pts], [p[1] for p in pts], color=C["MT00005"], lw=1.8, marker="o", ms=4)
    a2.set_ylim(0, 1.3)
    a2.set_xlim(2012.5, 2023.5)
    a2.set_title("B. CO at Msida, same hours (mg/m³)", fontsize=8.6, color=SLATE, loc="left", fontweight="bold")
    for ax, top in ((a1, 80), (a2, 1.27)):
        ax.axvline(2018 + 8.5 / 12, color=GREY, lw=0.8, ls="--", zorder=1)
        ax.text(2018 + 8.5 / 12 - 0.1, top, "Free school\ntransport", fontsize=6.8, color=GREY, va="top", ha="right")
        ax.set_xticks([2013, 2015, 2017, 2019, 2021, 2023])
        ax.tick_params(labelsize=7.8)
    fig.suptitle("Free school transport (from September 2018): morning rush hour, October–December, by year", x=0.01,
                 ha="left", fontsize=9.5, color=GREEN, fontweight="bold")
    fig.tight_layout(rect=(0, 0, 1, 0.96))
    note(fig, "Means of valid hourly values, Monday to Friday, 07:00–09:59 as reported to the EEA, October to December "
         "(the months the plan uses for its Figures 25–26). CO is measured at Msida but\nnot at Attard or Żejtun in these "
         "years. 2016 CO is left out (under 100 valid hours). " + SRC, y=-0.02)
    fig.savefig(OUT / "fig4_school.png", bbox_inches="tight", facecolor="white")
    plt.close(fig)


# ------------------------------------------------------------------ figure 5: free public transport
def fig5():
    s = {"PM10": daily("pm10_daily.csv"), "PM2.5": daily("pm25_daily.csv"), "NO2": daily("no2_daily.csv")}
    w0 = (dt.date(2021, 10, 1), dt.date(2022, 9, 30))
    w1 = (dt.date(2022, 10, 1), dt.date(2023, 9, 30))
    fig, axs = plt.subplots(1, 3, figsize=(9.6, 3.3), dpi=220, sharey=True)
    sts = ["MT00005", "MT00004", "MT00008", "MT00007"]
    for ax, pol in zip(axs, ("PM10", "PM2.5", "NO2")):
        for i, st in enumerate(sts):
            ser = s[pol].get(st, {})
            a = [v for d, v in ser.items() if w0[0] <= d <= w0[1]]
            b = [v for d, v in ser.items() if w1[0] <= d <= w1[1]]
            if len(a) < 300 or len(b) < 300:
                ax.text(1, i, "no data", fontsize=7, color=GREY, va="center")
                continue
            ma, mb = sum(a) / len(a), sum(b) / len(b)
            ax.annotate("", xy=(mb, i), xytext=(ma, i),
                        arrowprops={"arrowstyle": "-|>", "color": C[st], "lw": 1.6, "mutation_scale": 9})
            ax.plot(ma, i, marker="o", ms=6, mfc="white", mec=C[st], mew=1.4)
            off = 0.045 * {"PM10": 52, "PM2.5": 17, "NO2": 36}[pol]
            ax.text(max(ma, mb) + off, i, f"{mb - ma:+.1f}", fontsize=7.8, color=SLATE, va="center",
                    fontweight="bold" if st == "MT00005" else "normal")
        lab = {"PM10": "PM10", "PM2.5": "PM2.5", "NO2": "NO₂"}[pol]
        ax.set_title(f"{lab} (µg/m³)", fontsize=8.6, color=SLATE, loc="left", fontweight="bold")
        ax.set_xlim(0, {"PM10": 52, "PM2.5": 17, "NO2": 36}[pol])
        ax.tick_params(labelsize=7.8)
        ax.grid(axis="x", color=PALEGREY, lw=0.6)
    axs[0].set_yticks(range(len(sts)))
    axs[0].set_yticklabels([NAME[s] for s in sts], fontsize=7.8)
    axs[0].invert_yaxis()
    fig.suptitle("Free public transport (from 1 October 2022): 12 months before and 12 months after", x=0.01,
                 ha="left", fontsize=9.5, color=GREEN, fontweight="bold")
    fig.tight_layout(rect=(0, 0, 1, 0.95))
    note(fig, "Hollow circle: mean of October 2021–September 2022; arrowhead: October 2022–September 2023; number: "
         "change. Daily values (NO₂: days with at least 18 valid hours).\nAttard had no PM10 monitor before 2024. No "
         "adjustment for weather. " + SRC, y=-0.02)
    fig.savefig(OUT / "fig5_free_pt.png", bbox_inches="tight", facecolor="white")
    plt.close(fig)


if __name__ == "__main__":
    fig1()
    fig2()
    fig3()
    fig4()
    fig5()
    print("figures written to", OUT)
