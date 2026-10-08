"""Figures for Claim Check 062, drawn from data/cc-062/checks.csv (run calc.py first)."""
import csv, pathlib, re
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
C = {r["check"]: float(r["value"]) for r in csv.DictReader(open(ROOT / "data" / "cc-062" / "checks.csv"))
     if re.fullmatch(r"-?[\d.]+", r["value"])}


def fig1():
    a = C["KPMG Table 1.1: (F + L excl. imputed rents) / total GVA less imputed rents, 2024"]
    b = C["Direct share incl. imputed rents (same basis as the 14%)"]
    c = C["Table 1.3: 3,002 / total GVA 21,378 (incl. imputed rents)"]
    fig, ax = plt.subplots(figsize=(9.6, 4.4), dpi=220)
    xs = [0, 1, 2]
    ax.bar(0, a, color=SAGE, width=0.62)
    ax.bar(1, b, color=SAGE, width=0.62)
    ax.bar(1, 0, color=AMBER)
    ax.bar(1, b - a, bottom=a, color=AMBER, width=0.62)
    ax.bar(2, b, color=SAGE, width=0.62)
    ax.bar(2, c - b, bottom=b, color=BLUE, width=0.62)
    ax.bar(1, a, color=SAGE, width=0.62)
    ax.text(0, a + 0.25, f"{a:.1f}%", ha="center", fontsize=11, fontweight="bold", color=GREEN)
    ax.text(1, b + 0.25, f"{b:.1f}%", ha="center", fontsize=11, fontweight="bold", color=GREEN)
    ax.text(2, c + 0.25, f"{c:.1f}%", ha="center", fontsize=11, fontweight="bold", color=GREEN)
    ax.text(1, a + (b - a) / 2, f"+{b - a:.1f} pp\nimputed rents\nincluded", ha="center", va="center", fontsize=8.3,
            color=SLATE)
    ax.text(2, b + (c - b) / 2, f"+{c - b:.1f} pp\nindirect linkages\n(modelled)", ha="center", va="center",
            fontsize=7.6, color="white", fontweight="bold")
    ax.set_xticks(xs)
    ax.set_xticklabels(["KPMG “direct”\n(Table 1.1: excludes\nimputed rents)", "Same activities, direct,\nimputed rents included\n(Table 1.2)",
                        "KPMG “with indirect\nlinkages”\n(Table 1.3)"], fontsize=8.6)
    ax.set_ylabel("Share of gross value added, 2024 (%)")
    ax.set_ylim(0, 16.5)
    ax.text(-0.45, -4.6, "Construction (NACE F) and real estate (NACE L). Source: KPMG/MDA report 2025, Tables 1.1–1.3 (NSO data; "
            "KPMG analysis); steps\ncalculated in tools/cc-062-report/calc.py. pp = percentage points.", fontsize=7, color=GREY, va="top")
    fig.savefig(OUT / "fig1_steps.png", bbox_inches="tight", facecolor="white")
    plt.close(fig)


def fig2():
    yrs = list(range(2018, 2026))
    ex = [C[f"Eurostat {y}: (F + L - imputed rents) / (total GVA - imputed rents)"] for y in yrs]
    inc = [C[f"Eurostat {y}: (F + L) / total GVA, imputed rents included in both"] for y in yrs]
    kp = {2020: 8.9, 2021: 8.9, 2022: 8.6, 2023: 9.0, 2024: 9.1}
    fig, ax = plt.subplots(figsize=(9.6, 4.0), dpi=220)
    ax.plot(yrs, inc, color=AMBER, lw=2.2, ls="--", label="Eurostat: imputed rents included in both")
    ax.plot(yrs, ex, color=GREEN, lw=2.4, label="Eurostat: imputed rents excluded from both (KPMG’s “direct” basis)")
    ax.scatter(list(kp), list(kp.values()), color=RED, s=46, zorder=5, label="KPMG Table 1.1 (as printed)")
    ax.text(2025.12, ex[-1], f"{ex[-1]:.1f}", color=GREEN, fontsize=8.5, va="center", fontweight="bold")
    ax.text(2025.12, inc[-1], f"{inc[-1]:.1f}", color=AMBER, fontsize=8.5, va="center", fontweight="bold")
    ax.set_ylim(6, 15)
    ax.set_xlim(2017.7, 2025.6)
    ax.set_ylabel("Share of total GVA (%)")
    ax.legend(frameon=False, fontsize=8, loc="upper left")
    ax.text(2017.7, 4.3, "Eurostat nama_10_a64 (current prices; retrieved 8 Oct 2026; latest vintage). Eurostat’s 2024 construction GVA "
            "is 893.6, KPMG’s 809.0:\nthe two agree to within 0.15 pp in 2020–2023 and differ by 0.5 pp in 2024. 2025 is the latest annual "
            "value in the dataset.", fontsize=7, color=GREY, va="top")
    fig.savefig(OUT / "fig2_series.png", bbox_inches="tight", facecolor="white")
    plt.close(fig)


fig1()
fig2()
print("figures in", OUT)
