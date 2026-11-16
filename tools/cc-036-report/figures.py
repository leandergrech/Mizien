"""Figures for Claim Check 036 (run calc.py first)."""
import csv, pathlib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[1]
D = ROOT / "data/cc-036"
OUT = HERE / "out"; OUT.mkdir(exist_ok=True)
for f in ["LiberationSans-Regular", "LiberationSans-Bold", "LiberationSans-Italic"]:
    fm.fontManager.addfont(f"/usr/share/fonts/truetype/liberation/{f}.ttf")
plt.rcParams.update({"font.family": "Liberation Sans", "axes.spines.top": False, "axes.spines.right": False,
                     "axes.edgecolor": "#8A9399", "axes.labelcolor": "#2B3A42", "xtick.color": "#2B3A42",
                     "ytick.color": "#2B3A42"})
GREEN, AMBER, RED, SLATE, GREY, PALE = "#14452F", "#E3A72F", "#B5483A", "#2B3A42", "#8A9399", "#C9D3CC"
pm = {}
for r in csv.DictReader(open(D / "eea_mt_pm_annual.csv")):
    if r["verification"] == "1" and r["coverage_ok"] == "Yes":
        pm[(r["station_code"], r["pollutant"], int(r["year"]))] = float(r["annual_mean_ugm3"])


def fig1():
    st = [("MT00011", 2025, "Msida\n(traffic)"), ("MT00009", 2025, "St Paul’s Bay\n(traffic)"),
          ("MT00008", 2024, "Attard\n(background)"), ("MT00004", 2025, "Żejtun\n(background)"),
          ("MT00007", 2025, "Għarb\n(rural background)")]
    fig, ax = plt.subplots(figsize=(9.6, 3.6), dpi=220)
    for i, (s, y, lab) in enumerate(st):
        p10, p25 = pm[(s, "PM10", y)], pm[(s, "PM2.5", y)]
        ax.bar(i, p25, color=SLATE, width=0.6, label="PM2.5 (fine)" if i == 0 else None)
        ax.bar(i, p10 - p25, bottom=p25, color=AMBER, width=0.6, label="PM10 − PM2.5 (coarse)" if i == 0 else None)
        ax.text(i, p10 + 0.8, f"{p10:.1f} ({100 * (p10 - p25) / p10:.0f}% coarse)", ha="center", fontsize=7.5, color=SLATE)
    ax.axhline(15, color=RED, lw=0.9, ls=":", label="WHO 2021 guideline, PM10 annual: 15")
    ax.axhline(40, color=GREY, lw=0.8, ls="--", label="EU annual limit, PM10: 40")
    ax.set_xticks(range(len(st))); ax.set_xticklabels([f"{s[2]}\n{s[1]}" for s in st], fontsize=8)
    ax.set_ylim(0, 50); ax.set_ylabel("Annual mean (µg/m³)"); ax.legend(fontsize=7.5, frameon=False, loc="upper right", ncol=2)
    fig.text(0.01, -0.06, "Source: EEA Air Quality Statistics (verified annual means, EEA coverage filter met), retrieved 16 Nov 2026; "
             "WHO Global Air Quality Guidelines (2021). Latest verified year shown under each bar.", fontsize=7, color=GREY)
    fig.savefig(OUT / "fig1_pm_split.png", bbox_inches="tight", facecolor="white")


def fig2():
    rows = list(csv.DictReader(open(D / "vella2005_size_fractions.csv")))
    labs, seen = [], {}
    for r in rows:
        base = f"Quarry {r['sample'][-1]}, {r['operation']}" + (", dry stone" if r["moisture"] == "dry stone" else "")
        seen[base] = seen.get(base, 0) + 1
        labs.append(base)
    for b in [k for k, v in seen.items() if v > 1]:
        n = 0
        for i, l in enumerate(labs):
            if l == b:
                n += 1; labs[i] = f"{b} (tool {n})"
    below = [float(r["pct_below_10um"]) for r in rows]
    ys = list(range(len(rows)))[::-1]
    fig, ax = plt.subplots(figsize=(9.6, 3.1), dpi=220)
    ax.barh(ys, below, color=AMBER, label="< 10 µm (PM10)")
    ax.barh(ys, [100 - b for b in below], left=below, color=PALE, edgecolor=PALE, label="> 10 µm (settles out)")
    for y, b in zip(ys, below):
        ax.text(b + 1, y, f"{b:.1f}%", va="center", ha="left", fontsize=7, color=SLATE)
    ax.set_yticks(ys); ax.set_yticklabels(labs)
    ax.axvline(11, color=RED, lw=0.7, ls=":"); ax.axvline(22, color=RED, lw=0.7, ls=":")
    ax.text(16.5, len(rows) - 0.35, "ERA: 11–22%", color=RED, fontsize=7.5, ha="center")
    ax.set_xlim(0, 100); ax.set_xlabel("Share of deposited dust by mass (%)"); ax.tick_params(axis="y", labelsize=7.5)
    ax.legend(fontsize=7.5, frameon=True, loc="lower right")
    fig.text(0.01, -0.09, "Source: Vella & Camilleri (2005), Xjenza 10:47–54, Tables 2 (cutting and dressing machines) and 3 (quarry access roads).",
             fontsize=7, color=GREY)
    fig.savefig(OUT / "fig2_quarry_dust.png", bbox_inches="tight", facecolor="white")


if __name__ == "__main__":
    fig1(); fig2()
