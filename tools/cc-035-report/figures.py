"""Figures for Claim Check 035, drawn from data/cc-035/ (run fetch.py and calc.py first)."""
import csv, math, pathlib
from collections import defaultdict
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from matplotlib.lines import Line2D

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[1]
D = ROOT / "data" / "cc-035"
OUT = HERE / "out"
OUT.mkdir(exist_ok=True)
for f in ["LiberationSans-Regular", "LiberationSans-Bold", "LiberationSans-Italic"]:
    fm.fontManager.addfont(f"/usr/share/fonts/truetype/liberation/{f}.ttf")
plt.rcParams.update({"font.family": "Liberation Sans", "axes.spines.top": False, "axes.spines.right": False,
                     "axes.edgecolor": "#8A9399", "axes.labelcolor": "#2B3A42", "xtick.color": "#2B3A42",
                     "ytick.color": "#2B3A42"})
GREEN, SAGE, AMBER, RED, SLATE, GREY, ORANGE, BLUE, PURPLE = ("#14452F", "#7FA88B", "#E3A72F", "#B5483A", "#2B3A42",
                                                              "#8A9399", "#D9772B", "#3C6E8F", "#8A6FB0")
BASE = "Baseline from WHO 2021 AQG"
SC = {}
for r in csv.DictReader(open(D / "eea_ebd_malta_pm25.csv", encoding="utf-8")):
    if r["Health Indicator"] == "Attributable deaths (AD)":
        SC.setdefault(r["Scenario"], {})[int(r["Year"])] = r
B = SC[BASE]
YRS = sorted(B)
rate = lambda y, sc=BASE: float(SC[sc][y]["Value for 100k Of Affected Population"])


def runs(xs):
    """Split years into runs of consecutive years so a missing year (2006) is not bridged."""
    out, cur = [], [xs[0]]
    for x in xs[1:]:
        if x == cur[-1] + 1:
            cur.append(x)
        else:
            out.append(cur); cur = [x]
    out.append(cur)
    return out


def fig1():
    """The EEA's modelled rate for Malta, with its 95% CI, and the number of deaths in a second panel."""
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(9.6, 3.7), dpi=220, gridspec_kw={"width_ratios": [1.25, 1]})
    lo = {y: float(B[y]["Value for 100k Of Affected Population - lower CI"]) for y in YRS}
    hi = {y: float(B[y]["Value for 100k Of Affected Population - upper CI"]) for y in YRS}
    for run in runs(YRS):
        a1.fill_between(run, [lo[y] for y in run], [hi[y] for y in run], color=SAGE, alpha=0.35, lw=0)
        a1.plot(run, [rate(y) for y in run], color=GREEN, lw=2.2)
    a1.plot(YRS, [rate(y) for y in YRS], "o", ms=3.4, color=GREEN)
    a1.plot([2005], [rate(2005)], "o", ms=6, mfc="white", mec=GREEN, mew=1.6, zorder=4)
    a1.annotate("143.5 in 2005\n(no PM2.5 measured\nin Malta that year)", (2005, rate(2005)), xytext=(2007.2, 150),
                fontsize=7.6, color=SLATE, va="top", arrowprops=dict(arrowstyle="-", color=GREY, lw=0.7))
    a1.text(2023.3, rate(2023), "46.3\nin 2023", fontsize=8, color=GREEN, va="center", fontweight="bold")
    a1.text(2006, 12, "no 2006\nvalue", fontsize=6.8, color=GREY, ha="center")
    a1.set_ylim(0, 170); a1.set_xlim(2004.4, 2025.3)
    a1.set_xticks(range(2005, 2024, 3))
    a1.set_ylabel("deaths per 100 000 aged 30+")
    a1.set_title("Rate (what the EEA statement gives)", fontsize=9.5, color=SLATE, loc="left")
    a1.legend(handles=[Line2D([], [], color=GREEN, lw=2.2, label="EEA estimate"),
                       plt.Rectangle((0, 0), 1, 1, color=SAGE, alpha=0.35, label="95% CI (relative risk only)")],
              frameon=False, fontsize=7.4, loc="upper right")
    n = {y: float(B[y]["Value"]) for y in YRS}
    nlo = {y: float(B[y]["Value - lower CI"]) for y in YRS}
    nhi = {y: float(B[y]["Value - upper CI"]) for y in YRS}
    for run in runs(YRS):
        a2.fill_between(run, [nlo[y] for y in run], [nhi[y] for y in run], color=SAGE, alpha=0.35, lw=0)
        a2.plot(run, [n[y] for y in run], color=BLUE, lw=2.2)
    a2.plot(YRS, [n[y] for y in YRS], "o", ms=3.4, color=BLUE)
    a2.text(2005.4, n[2005] + 14, f"{n[2005]:.0f}", fontsize=8, color=BLUE, fontweight="bold")
    a2.text(2023.3, n[2023], f"{n[2023]:.0f}", fontsize=8, color=BLUE, va="center", fontweight="bold")
    a2.set_ylim(0, 420); a2.set_xlim(2004.4, 2025.3)
    a2.set_xticks(range(2005, 2024, 3))
    a2.set_ylabel("attributable deaths")
    a2.set_title("Number of deaths (fell by half)", fontsize=9.5, color=SLATE, loc="left")
    fig.text(0.01, -0.06, "Deaths from all natural causes, people aged 30+, attributed to PM2.5 above 5 µg/m³ (WHO 2021 "
             "guideline), EEA burden-of-disease table, retrieved 6 Oct 2026.\nThe rate fell 67.7% while the population aged 30+ "
             "grew 54% (242,534 to 373,208), so the number fell 50.6%. The EEA gives no 2006 value.", fontsize=7, color=GREY)
    fig.tight_layout()
    fig.savefig(OUT / "fig1_rate.png", bbox_inches="tight", facecolor="white")


def fig2():
    """Modelled population-weighted PM2.5 (EEA maps) against measured annual means at Malta's stations."""
    st = defaultdict(dict)
    for r in csv.DictReader(open(D / "eea_stations_malta_annual.csv", encoding="utf-8")):
        if r["pollutant"] == "PM2.5":
            s = "MT00005" if r["station"] in ("MT00005", "MT00011") and int(r["year"]) <= 2023 and r["station"] == "MT00005" \
                else r["station"]
            st[s][int(r["year"])] = (float(r["mean_of_valid_days_ug_m3"]), float(r["coverage_pct"]))
    fig, ax = plt.subplots(figsize=(9.6, 4.1), dpi=220)
    ax.axhline(5, color=GREY, lw=1, ls=":")
    ax.text(2025.6, 5, "WHO guideline 5", fontsize=7.5, color=GREY, va="center", ha="right",
            bbox=dict(facecolor="white", edgecolor="none", pad=0.6))
    for run in runs(YRS):
        ax.plot(run, [float(B[y]["Air Pollution Population Weighted Average [ug/m3]"]) for y in run], color=SLATE, lw=3,
                zorder=3, solid_capstyle="round")
    pwc = {y: float(B[y]["Air Pollution Population Weighted Average [ug/m3]"]) for y in YRS}
    ax.plot(YRS[1:], [pwc[y] for y in YRS[1:]], "o", ms=3, color=SLATE, zorder=3)
    ax.plot([2005], [pwc[2005]], "o", ms=7, mfc="white", mec=SLATE, mew=2, zorder=5)
    ax.annotate(f"{pwc[2005]:.1f} (map only)", (2005, pwc[2005]), xytext=(2005.55, 19.9), fontsize=7.6, va="center",
                color=SLATE, fontweight="bold", arrowprops=dict(arrowstyle="-", color=GREY, lw=0.7))
    ax.text(2023.35, pwc[2023] - 0.2, f"{pwc[2023]:.1f}", fontsize=7.6, color=SLATE, fontweight="bold", va="top")
    STY = [("MT00005", "Msida (traffic site)", GREEN, "o"), ("MT00004", "Żejtun", BLUE, "s"),
           ("MT00007", "Għarb", ORANGE, "^"), ("MT00008", "Attard", PURPLE, "D"), ("MT00009", "St Paul's Bay", RED, "v")]
    handles = [Line2D([], [], color=SLATE, lw=3, label="EEA map (modelled)")]
    for code, name, col, mk in STY:
        ys = sorted(y for y in st[code] if y <= 2023)
        if not ys:
            continue
        for run in runs(ys):
            ax.plot(run, [st[code][y][0] for y in run], color=col, lw=1.3, alpha=0.9, zorder=2)
        for y in ys:
            v, c = st[code][y]
            full = c >= 75
            ax.plot([y], [v], marker=mk, ms=5.2 if full else 5.6, color=col, mfc=col if full else "white", mew=1.2, zorder=4)
        handles.append(Line2D([], [], color=col, lw=1.3, marker=mk, ms=5, label=name))
    handles.append(Line2D([], [], color=GREY, lw=0, marker="o", ms=5.6, mfc="white", mew=1.2,
                          label="under 75% of days valid"))
    ax.axvspan(2004.5, 2005.5, color="#F3EEE2", lw=0, zorder=0)
    ax.text(2005, 0.6, "no PM2.5\nstation", fontsize=6.8, color=SLATE, ha="center")
    ax.set_ylim(0, 25); ax.set_xlim(2004.5, 2025.8)
    ax.set_xticks(range(2005, 2024, 2))
    ax.set_ylabel("PM2.5 annual mean (µg/m³)")
    ax.legend(handles=handles, frameon=False, fontsize=7.6, ncol=4, loc="upper right", bbox_to_anchor=(1.0, 1.02))
    ax.text(2004.5, -4.6, "Station means: valid daily values in the EEA's AirBase (to 2012) and E1a (from 2013) files, "
            "retrieved 6 Oct 2026; Msida is MT00005 (Scerri et al. 2018 call it a traffic site).\nModelled line: EEA "
            "burden-of-disease table (population-weighted mean of the 1 km map that combines stations, a chemical "
            "transport model and other data). No 2006 map value.", fontsize=7, color=GREY)
    fig.savefig(OUT / "fig2_measured.png", bbox_inches="tight", facecolor="white")


def fig3():
    """How large the 'fall' is depends on what is counted: same EEA maps and data, different choices."""
    sc = lambda s: 100 * (1 - rate(2023, s) / rate(2005, s))
    n = lambda y: float(B[y]["Value"])
    items = [
        ("Rate above 5 µg/m³, 2005–2023 (the statement)", 100 * (1 - rate(2023) / rate(2005)), GREEN),
        ("Number of deaths above 5 µg/m³, 2005–2023", 100 * (1 - n(2023) / n(2005)), SAGE),
        ("Rate above 5 µg/m³, 2007–2023 (no 2006 value)", 100 * (1 - rate(2023) / rate(2007)), SAGE),
        ("Rate above 5 µg/m³, 2010–2023 (three stations, ≥75% of days)", 100 * (1 - rate(2023) / rate(2010)), SAGE),
        ("Rate, all concentrations (above 0), 2005–2023", sc("Sensitivity: WHO 2021 AQG but CF=0 for NO2 and PM2.5; SOMO10 included"), SAGE),
        ("Rate, previous EEA method (RR 1.062, above 0), 2005–2023", sc("Baseline from WHO 2005 (HRAPIE 2013)"), SAGE),
        ("Rate above 10 µg/m³ (2030 EU limit), 2005–2023", sc("Sensitivity: WHO 2021 AQG but CF=20 for NO2 and CF=10 for PM2.5"), SAGE),
    ]
    fig, ax = plt.subplots(figsize=(9.6, 3.9), dpi=220)
    ys = list(range(len(items)))[::-1]
    for yy, (lab, v, col) in zip(ys, items):
        ax.barh(yy, v, color=col, height=0.62)
        ax.text(v + 1, yy, f"{v:.1f}%", va="center", fontsize=10, color=SLATE,
                fontweight="bold" if col == GREEN else "normal")
    ax.set_yticks(ys)
    ax.set_yticklabels([i[0] for i in items], fontsize=10)
    ax.set_xlim(0, 100)
    ax.set_xticks([0, 25, 50, 75, 100])
    ax.set_xlabel("fall to 2023 (%)")
    ax.tick_params(axis="y", length=0)
    ax.text(0, -2.25, "All values from the EEA burden-of-disease table for Malta (same concentration maps and population), "
            "retrieved 6 Oct 2026; percentages calculated in calc.py.", fontsize=7, color=GREY)
    fig.savefig(OUT / "fig3_choices.png", bbox_inches="tight", facecolor="white")


fig1(); fig2(); fig3()
print("figures in", OUT)
