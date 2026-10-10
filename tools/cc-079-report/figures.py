"""Figures for Claim Check 079, drawn from data/cc-079/ (run fetch.py and calc.py first). Output: out/fig*.png"""
import csv, pathlib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[1]
D = ROOT / "data" / "cc-079"
OUT = HERE / "out"
OUT.mkdir(exist_ok=True)
for f in ["LiberationSans-Regular", "LiberationSans-Bold", "LiberationSans-Italic"]:
    fm.fontManager.addfont(f"/usr/share/fonts/truetype/liberation/{f}.ttf")
plt.rcParams.update({"font.family": "Liberation Sans", "axes.spines.top": False, "axes.spines.right": False,
                     "axes.edgecolor": "#8A9399", "axes.labelcolor": "#2B3A42", "xtick.color": "#2B3A42",
                     "ytick.color": "#2B3A42"})
GREEN, AMBER, RED, SLATE, GREY, BLUE, ORANGE = "#14452F", "#E3A72F", "#B5483A", "#2B3A42", "#8A9399", "#3C6E8F", "#D9772B"
SAGE, PALEGREY = "#7FA88B", "#C9D3CC"

F = {r["key"]: float(r["value"]) for r in csv.DictReader(open(D / "document_figures.csv"))}
CHK = {r["check"]: r for r in csv.DictReader(open(D / "checks.csv"))}
wm = {}
for r in csv.DictReader(open(D / "eurostat_env_wasmun.csv")):
    wm[(r["wst_oper"], r["unit"], int(r["year"]))] = float(r["value"])


def val(check):
    return float(CHK[check]["value"])


def fig1():
    """Where the energy in 192,000 t goes, on the NECP design figures."""
    fuel = val("Energy content of 192,000 t at that value (fuel input)")
    elec = F["wasteserv_output_gwh"]
    fig, ax = plt.subplots(figsize=(9.6, 2.3), dpi=220)
    ax.barh([0], [elec], color=GREEN, height=0.5)
    ax.barh([0], [fuel - elec], left=[elec], color=PALEGREY, height=0.5)
    ax.text(elec / 2, 0, f"{elec:.0f} GWh\nelectricity to the grid", ha="center", va="center", color="white", fontsize=8.6,
            fontweight="bold")
    ax.text(elec + (fuel - elec) / 2, 0, f"{fuel - elec:.0f} GWh not delivered as electricity\n(heat and losses; "
            "WasteServ names no user for the heat)", ha="center", va="center", color=SLATE, fontsize=8.4)
    ax.annotate(f"{fuel:.0f} GWh: energy in 192,000 t of waste at the design 10 GJ per tonne",
                xy=(fuel, 0.27), xytext=(fuel, 0.62), ha="right", fontsize=8.4, color=SLATE,
                arrowprops=dict(arrowstyle="-", color=GREY, lw=0.8))
    ax.set_xlim(0, fuel * 1.01); ax.set_ylim(-0.45, 0.8)
    ax.set_yticks([]); ax.spines["left"].set_visible(False)
    ax.set_xlabel("GWh a year", fontsize=8.5)
    fig.text(0.01, -0.06, "Design figures: 2 lines x 12 t/h, 33.33 MWth heat input per line, 14-16 MW net (NECP, Dec 2024, "
             "p. 132); 126 GWh to the grid (WasteServ, ECOHIVE project page). Net electrical efficiency about 24%.",
             fontsize=7, color=GREY)
    fig.tight_layout()
    fig.savefig(OUT / "fig1_energy.png", bbox_inches="tight", facecolor="white")


def fig2():
    """126 GWh as a share of Malta's electricity and of its total energy, 2022, 2024 and the NECP's 2030."""
    rows = [("Electricity: final consumption", "Electricity: final consumption (nrg_cb_e FC)", None),
            ("Electricity: inland demand", "Electricity: inland demand (nrg_cb_e ID)",
             "2030 NECP electricity generation, all sources (sum of Figure 120)"),
            ("All energy: final energy use\n(excluding international aviation)",
             "Total energy: final energy use excl. international aviation (nrg_bal_c FC_E)", None),
            ("All energy: final energy consumption", "Total energy: final energy consumption (nrg_bal_c FEC_EED)",
             "2030 NECP final energy consumption (803 ktoe)"),
            ("All energy: primary energy consumption", "Total energy: primary energy consumption (nrg_bal_c PEC_EED)",
             "2030 NECP primary energy consumption (964 ktoe)"),
            ("All energy: gross inland consumption", "Total energy: gross inland consumption (nrg_bal_c GIC)", None)]
    E = F["wasteserv_output_gwh"]
    fig, ax = plt.subplots(figsize=(9.6, 4.4), dpi=220)
    n = len(rows)
    for i, (lab, key, k30) in enumerate(rows):
        y = n - 1 - i
        col = BLUE if lab.startswith("Electricity") else GREEN
        v22 = 100 * E / val(f"2022 {key}")          # from the saved denominators, rounded once
        v24 = 100 * E / val(f"2024 {key}")
        ax.barh(y + 0.18, v22, height=0.34, color=col)
        ax.barh(y - 0.18, v24, height=0.34, color=col, alpha=0.45)
        box = dict(facecolor="white", edgecolor="none", pad=0.6, alpha=0.85)
        ax.text(v22 + 0.06, y + 0.18, f"{v22:.1f}% (2022)", va="center", fontsize=7.8, color=SLATE, bbox=box, zorder=6)
        ax.text(v24 + 0.06, y - 0.18, f"{v24:.1f}% (2024)", va="center", fontsize=7.8, color=SLATE, bbox=box, zorder=6)
        if k30:
            v30 = 100 * E / val(k30)
            ax.plot([v30], [y - 0.18], marker="D", color=ORANGE, ms=6, zorder=5)
    ax.plot([], [], marker="D", color=ORANGE, ls="", ms=6, label="2030, NECP projection")
    ax.axvline(F["wasteserv_share_pct"], color=RED, ls="--", lw=1.4, zorder=2)
    ax.text(F["wasteserv_share_pct"] - 0.05, n - 0.38, "WasteServ: “around 4.5% of Malta’s total energy needs”",
            color=RED, fontsize=8.4, fontweight="bold", va="center", ha="right")
    ax.set_ylim(-0.6, n - 0.15)
    ax.set_yticks(range(n)); ax.set_yticklabels([r[0] for r in rows][::-1], fontsize=8.4)
    ax.set_xlim(0, 6.6); ax.set_xlabel("126 GWh a year as a share of Malta’s total (%)", fontsize=8.5)
    ax.legend(frameon=False, fontsize=8, loc="lower right")
    fig.text(0.01, -0.04, "Darker bars 2022 (the year before WasteServ’s June 2023 statement), lighter bars 2024. Sources: "
             "Eurostat nrg_cb_e and nrg_bal_c (retrieved 10 Oct 2026); NECP Dec 2024 (2030: Figure 120 and p. 94).",
             fontsize=7, color=GREY)
    fig.tight_layout()
    fig.savefig(OUT / "fig2_shares.png", bbox_inches="tight", facecolor="white")


def fig3():
    """Municipal waste generated and landfilled, with the plant's capacity and the 2035 residual."""
    yrs = list(range(2010, 2025))
    fig, ax = plt.subplots(figsize=(9.6, 3.8), dpi=220)
    ax.plot(yrs, [wm[("GEN", "THS_T", y)] for y in yrs], color=GREEN, lw=2.4, marker="o", ms=3, label="Municipal waste generated")
    ax.plot(yrs, [wm[("DSP_L_OTH", "THS_T", y)] for y in yrs], color=RED, lw=2.0, marker="o", ms=3, label="Municipal waste landfilled")
    cap = F["wasteserv_capacity_t"] / 1000
    ax.axhline(cap, color=SLATE, ls="--", lw=1.3)
    ax.text(2010.1, cap + 7, "Plant capacity: 192,000 t a year", color=SLATE, fontsize=8.4, fontweight="bold")
    resid = val("Municipal waste left after the 2035 recycling target (65%), at 2024 generation")
    ax.plot([2035], [resid], marker="D", color=ORANGE, ms=7)
    ax.annotate(f"{resid:.0f} kt: the most left for burning or landfill\nif 65% were recycled (2035 target),\n"
                "at 2024 generation", xy=(2035, resid), xytext=(2026.3, 30), fontsize=8, color=ORANGE,
                arrowprops=dict(arrowstyle="-", color=ORANGE, lw=0.8))
    ax.set_xlim(2009.5, 2036); ax.set_ylim(0, 420)
    ax.set_xticks(list(range(2010, 2025, 2)) + [2035])
    ax.set_ylabel("thousand tonnes a year", fontsize=8.5)
    ax.legend(frameon=False, fontsize=8.2, loc="upper left", bbox_to_anchor=(0.0, 0.93))
    fig.text(0.01, -0.03, "Landfilled: Eurostat operations D1-D7 and D12 (in 2015 more was landfilled than generated, as "
             "recorded). Sources: Eurostat env_wasmun (retrieved 10 Oct 2026); Directive (EU) 2018/851.",
             fontsize=7, color=GREY)
    fig.tight_layout()
    fig.savefig(OUT / "fig3_waste.png", bbox_inches="tight", facecolor="white")


if __name__ == "__main__":
    fig1(); fig2(); fig3()
    print("figures written to", OUT)
