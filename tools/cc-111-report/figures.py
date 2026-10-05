"""Figures for Claim Check 111, drawn from data/cc-111/ (run fetch.py first)."""
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
v = {}
for r in csv.DictReader(open(ROOT / "data/cc-111/eurostat_env_wasmun.csv")):
    v[(r["geo"], r["wst_oper"], r["unit"], int(r["year"]))] = float(r["value"])
a = {}
for r in csv.DictReader(open(ROOT / "data/cc-111/eurostat_env_wasmun_eu27_2023_2024.csv")):
    a[(r["geo"], r["wst_oper"], int(r["year"]))] = float(r["value"])
YRS = [y for y in range(2013, 2025)]


def fig1():
    fig, axs = plt.subplots(1, 2, figsize=(9.6, 3.9), dpi=220)
    ax = axs[0]
    for g, c, lab in (("MT", GREEN, "Malta"), ("EU27_2020", BLUE, "EU-27")):
        ys = [y for y in YRS if (g, "GEN", "KG_HAB", y) in v]
        ax.plot(ys, [v[(g, "GEN", "KG_HAB", y)] for y in ys], color=c, lw=2.4, marker="o", ms=3, label=lab)
    ax.annotate("621", (2024, 621), xytext=(2022.6, 655), color=GREEN, fontsize=9, fontweight="bold")
    ax.annotate("517", (2024, 517), xytext=(2023.2, 475), color=BLUE, fontsize=9, fontweight="bold")
    ax.set_ylim(400, 750); ax.set_title("Municipal waste generated, kg per person", fontsize=10, color=SLATE, loc="left")
    ax.legend(frameon=False, fontsize=8.5, loc="upper left")
    ax = axs[1]
    for g, c, lab in (("MT", GREEN, "Malta"), ("EU27_2020", BLUE, "EU-27")):
        ys = [y for y in YRS if (g, "DSP_L_OTH", "KG_HAB", y) in v and y != 2015]
        ax.plot(ys, [100 * v[(g, "DSP_L_OTH", "KG_HAB", y)] / v[(g, "GEN", "KG_HAB", y)] for y in ys], color=c, lw=2.4, marker="o", ms=3, label=lab)
    ys = [y for y in YRS if y != 2015]
    ax.plot(ys, [100 * v[("MT", "DSP_L_OTH", "KG_HAB", y)] / v[("MT", "TRT", "KG_HAB", y)] for y in ys], color=GREEN, lw=1.2, ls="--",
            label="Malta, share of waste treated")
    ax.annotate("82%", (2013, 82), xytext=(2013, 92), color=GREEN, fontsize=9, fontweight="bold")
    ax.annotate("74% (2023)", (2023, 73.6), xytext=(2020.6, 62), color=GREEN, fontsize=9, fontweight="bold")
    ax.set_ylim(0, 100); ax.set_title("Landfill rate, % of waste generated", fontsize=10, color=SLATE, loc="left")
    ax.legend(frameon=False, fontsize=8, loc="center left")
    for ax in axs:
        ax.set_xticks(range(2013, 2025, 2))
    fig.text(0.01, -0.03, "2015 omitted from the landfill rate (landfilled tonnage exceeds generation in the dataset). EU-27 2023 landfill "
             "value not published. Source: Eurostat env_wasmun, retrieved 5 Oct 2026.", fontsize=7, color=GREY)
    fig.tight_layout()
    fig.savefig(OUT / "fig1_series.png", bbox_inches="tight", facecolor="white")


def fig2():
    fig, axs = plt.subplots(1, 2, figsize=(9.6, 4.6), dpi=220)
    for ax, (op, y, title) in zip(axs, (("GEN", 2024, "Waste per person, 2024 (kg)"), ("RATE", 2023, "Landfill rate, 2023 (%)"))):
        if op == "GEN":
            d = {g: a[(g, "GEN", y)] for g in {x[0] for x in a} if (g, "GEN", y) in a}
        else:
            d = {g: 100 * a[(g, "DSP_L_OTH", y)] / a[(g, "GEN", y)] for g in {x[0] for x in a} if (g, "DSP_L_OTH", y) in a and (g, "GEN", y) in a}
        items = sorted(d.items(), key=lambda kv: kv[1])
        ax.barh([g for g, _ in items], [x for _, x in items], color=[GREEN if g == "MT" else "#C9D3CC" for g, _ in items])
        ax.set_title(title, fontsize=10, color=SLATE, loc="left"); ax.tick_params(axis="y", labelsize=7.5)
        mt = d["MT"]; ax.text(mt, [g for g, _ in items].index("MT"), f"  {mt:.0f}", va="center", fontsize=8, color=GREEN, fontweight="bold")
    fig.text(0.01, -0.02, "Member states with data in Eurostat env_wasmun for that year (2024: 20 states). Retrieved 5 Oct 2026.", fontsize=7, color=GREY)
    fig.tight_layout()
    fig.savefig(OUT / "fig2_ranks.png", bbox_inches="tight", facecolor="white")


if __name__ == "__main__":
    fig1(); fig2()
