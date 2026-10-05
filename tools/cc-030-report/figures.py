"""Figures for Claim Check 030, drawn from data/cc-030/ (run calc.py first)."""
import csv
import pathlib

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib import font_manager as fm  # noqa: E402

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[1]
OUT = HERE / "out"
OUT.mkdir(exist_ok=True)
for f in ["LiberationSans-Regular", "LiberationSans-Bold", "LiberationSans-Italic"]:
    fm.fontManager.addfont(f"/usr/share/fonts/truetype/liberation/{f}.ttf")
plt.rcParams.update({"font.family": "Liberation Sans", "axes.spines.top": False, "axes.spines.right": False,
                     "axes.edgecolor": "#8A9399", "axes.labelcolor": "#2B3A42", "xtick.color": "#2B3A42",
                     "ytick.color": "#2B3A42", "hatch.color": "#8A9399", "hatch.linewidth": 0.8})
GREEN, SAGE, AMBER, RED, SLATE, GREY, ORANGE, BLUE = ("#14452F", "#7FA88B", "#E3A72F", "#B5483A", "#2B3A42",
                                                      "#8A9399", "#D9772B", "#3C6E8F")
D = ROOT / "data" / "cc-030"
V = {(r["item"], r["year"]): float(r["value"]) for r in csv.DictReader(open(D / "mia_emissions.csv", encoding="utf-8"))}
G = {r["item"]: float(r["value"]) for r in csv.DictReader(open(D / "ground_power_inputs.csv", encoding="utf-8"))}


def _grid(ax):
    ax.grid(axis="x", color="#E3E6E8", lw=0.6)
    ax.set_axisbelow(True)
    ax.tick_params(axis="y", length=0)
    ax.spines["left"].set_visible(False)


def fig1():
    """Two linear panels: the ACA boundary against the credits, and the whole footprint in thousand tonnes."""
    s1, s2, s2m = (V[("Scope 1 GHG emissions", "2025")], V[("Scope 2 GHG emissions (location based)", "2025")],
                   V[("Scope 2 GHG emissions (market based)", "2025")])
    bt = V[("Scope 3 Category 6 business travel", "2025")]
    c11 = V[("Scope 3 Category 11 use of sold products (mostly aircraft)", "2025")]
    s3 = V[("Scope 3 total", "2025")]
    credits, found = V[("Carbon credits purchased for residual emissions", "2025")], 1620 + 2160
    fig, (a, b) = plt.subplots(1, 2, figsize=(9.4, 3.45), dpi=220, gridspec_kw={"width_ratios": [1.05, 1], "wspace": 0.95})

    # left panel: tonnes, linear 0-6,500
    rows = [("Inside the boundary\n(location-based Scope 2)", None), ("Inside the boundary\n(market-based Scope 2)", None),
            ("Credits on MIA's\ncertificate", credits), ("Credits found retired\nin public registries", found),
            ("Programme: CO$_2$ to be\navoided a year (Scope 3)", 1000)]
    for i, (lab, v) in enumerate(rows):
        if i in (0, 1):
            s2v = s2 if i == 0 else s2m
            left = 0
            for part, col in ((s1, GREEN), (s2v, SAGE), (bt, GREEN)):
                a.barh(i, part, left=left, color=col, height=0.62, edgecolor="white", linewidth=1)
                left += part
            a.text(left + 90, i, f"{left:,.0f} t", va="center", fontsize=8.8, color=SLATE, fontweight="bold")
        elif i == 2:
            a.barh(i, v, color=RED, height=0.62)
            a.text(v + 90, i, f"{v:,.0f} t", va="center", fontsize=8.8, color=SLATE, fontweight="bold")
        elif i == 3:
            a.barh(i, v, color="white", height=0.62, edgecolor=RED, hatch="////", linewidth=1)
            a.text(v + 90, i, f"{v:,.0f} t (69%)", va="center", fontsize=8.8, color=SLATE, fontweight="bold")
        else:
            a.barh(i, v, color=ORANGE, height=0.62)
            a.text(v + 90, i, f"{v:,.0f} t (claimed)", va="center", fontsize=8.8, color=SLATE, fontweight="bold")
    a.text(s1 / 2, -0.47, "Scope 1", ha="center", va="bottom", fontsize=7.4, color=SLATE)
    a.text(s1 + s2 / 2, -0.47, "Scope 2", ha="center", va="bottom", fontsize=7.4, color=SLATE)
    a.text(s1 + s2 + 60, -0.47, "business travel", ha="left", va="bottom", fontsize=7.4, color=SLATE)
    a.set_yticks(range(len(rows)))
    a.set_yticklabels([r[0] for r in rows], fontsize=8.6)
    a.invert_yaxis()
    a.set_xlim(0, 7400)
    a.set_xticks([0, 2000, 4000, 6000])
    a.set_xticklabels(["0", "2,000", "4,000", "6,000"], fontsize=8)
    a.set_xlabel("tonnes of CO$_2$, 2025", fontsize=8)
    _grid(a)
    a.set_title("A. The carbon-neutral boundary (ACA Level 3+)", fontsize=9.8, color=GREEN, loc="left",
                fontweight="bold", pad=12)

    # right panel: thousand tonnes, linear 0-800
    parts = [("Neutral boundary\n(Scope 1, 2, business travel)", (s1 + s2 + bt) / 1000, GREEN),
             ("Other Scope 3", (s3 - c11 - bt) / 1000, BLUE),
             ("Scope 3: use of sold products\n(mostly aircraft)", c11 / 1000, BLUE)]
    tot = (s1 + s2 + s3) / 1000
    for i, (lab, v, col) in enumerate(parts):
        b.barh(i, v, color=col, height=0.62)
        b.text(v + 12, i, f"{v:,.1f} kt ({100 * v / tot:.1f}%)", va="center", fontsize=8.8, color=SLATE,
               fontweight="bold")
    b.set_yticks(range(len(parts)))
    b.set_yticklabels([p[0] for p in parts], fontsize=8.6)
    b.invert_yaxis()
    b.set_xlim(0, 900)
    b.set_xticks([0, 200, 400, 600, 800])
    b.set_xticklabels(["0", "200", "400", "600", "800"], fontsize=8)
    b.set_xlabel("thousand tonnes of CO$_2$, 2025 (scale 1,000 times panel A’s)", fontsize=8)
    _grid(b)
    b.set_title(f"B. The whole reported footprint: {tot:,.0f} kt (shares of it)", fontsize=9.8, color=GREEN, loc="left",
                fontweight="bold", pad=12)
    fig.text(0.01, -0.07, "Linear scales. Sources: MIA Sustainability Report 2025, GRI 102 tables (pp. 124–125), p. 31 and "
             "certificate (pp. 140–141);\nGold Standard and Rainbow registries (retrieved 5 Oct 2026); MIA press release, "
             "25 May 2026. Scope 3 for 2025 counts full flights;\non 2024's landing-and-take-off basis it was 95.3% of the "
             "footprint. Use of sold products also includes tenants' fuel and passengers' road trips (pp. 96–97).",
             fontsize=7.2, color=GREY, ha="left", va="top")
    fig.savefig(OUT / "fig1_scopes.png", bbox_inches="tight", facecolor="white")


def fig2():
    """What 1,000 t a year would require, anchored on the one sourced ground-power rate."""
    turn = G["Aircraft movements 2025"] / 2
    ef_d = G["Diesel (gas/diesel oil) CO2 emission factor"] * G["Diesel (gas/diesel oil) net calorific value"] / 1e6
    gpu = G["Mobile diesel GPU fuel consumption (Zurich Airport average 2004)"] * ef_d
    apu = G["APU fuel flow in single-cycle events (duration-weighted average)"] * G["Jet A-1 CO2 factor used by MIA for aircraft and APU"]
    dur = G["APU switched off between arrival and departure when external power was used (double-cycle events)"]
    m_gpu, m_apu = 60 * 1e6 / gpu / turn, 60 * 1e6 / apu / turn
    gross = gpu * dur / 60 * turn / 1000
    rest_min = 60 * (1e6 - 1000 * gross) / apu / turn

    fig, (a, b) = plt.subplots(1, 2, figsize=(9.4, 3.2), dpi=220, gridspec_kw={"width_ratios": [1.1, 1], "wspace": 0.75})
    rows = [(f"Diesel ground power\nunit replaced\n(≈{gpu:.0f} kg CO$_2$ an hour)", m_gpu, ORANGE),
            (f"Aircraft APU running\navoided\n(≈{apu:.0f} kg CO$_2$ an hour)", m_apu, BLUE)]
    for i, (lab, v, col) in enumerate(rows):
        a.barh(i, v, color=col, height=0.55)
        a.text(v + 1.5, i, f"{v:.0f} min" if v > 10 else f"{v:.1f} min", va="center", fontsize=9, color=SLATE,
               fontweight="bold", zorder=5, bbox=dict(boxstyle="square,pad=0.15", fc="white", ec="none"))
    a.axvline(dur, color=SLATE, lw=1, ls="--")
    a.text(dur + 1.2, -0.98, f"{dur:.1f} min: average time the APU stayed off\non external power (Padhra 2018)",
           fontsize=7.4, color=SLATE, va="top")
    a.set_yticks(range(len(rows)))
    a.set_yticklabels([r[0] for r in rows], fontsize=8.6)
    a.set_ylim(1.5, -1.05)
    a.set_xlim(0, 95)
    a.set_xticks([0, 20, 40, 60, 80])
    a.set_xticklabels(["0", "20", "40", "60", "80"], fontsize=8)
    a.set_xlabel("minutes per turnaround, at every one of 32,735 turnarounds", fontsize=8)
    _grid(a)
    a.set_title("A. To avoid 1,000 t a year, each turnaround needs…", fontsize=9.8, color=GREEN, loc="left",
                fontweight="bold", pad=10)

    b.barh(0, gross, color=ORANGE, height=0.55)
    b.barh(0, 1000 - gross, left=gross, color="white", edgecolor=GREY, hatch="////", height=0.55, linewidth=0.8)
    b.text(gross / 2, 0, f"≈{gross:.0f} t", ha="center", va="center", fontsize=9, color="white", fontweight="bold")
    b.text(gross + (1000 - gross) / 2, 0, f"≈{1000 - gross:.0f} t not shown\n(≈{rest_min:.1f} min less APU per\n"
           "turnaround, or e-bus and\nequipment savings)", ha="center", va="center", fontsize=7.6, color=SLATE,
           bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="none"))
    b.axvline(1000, color=RED, lw=1.2)
    b.text(1000, -0.48, "1,000 t claimed ", color=RED, fontsize=8.6, ha="right", va="bottom", fontweight="bold")
    b.set_yticks([0])
    b.set_yticklabels([f"Diesel ground\npower on every\nturnaround for\n{dur:.1f} min (gross)"], fontsize=8)
    b.set_ylim(0.6, -0.75)
    b.set_xlim(0, 1100)
    b.set_xticks([0, 250, 500, 750, 1000])
    b.set_xticklabels(["0", "250", "500", "750", "1,000"], fontsize=8)
    b.set_xlabel("tonnes of CO$_2$ a year", fontsize=8)
    _grid(b)
    b.set_title("B. What diesel ground power alone gives", fontsize=9.8, color=GREEN, loc="left", fontweight="bold",
                pad=10)
    fig.text(0.01, -0.1, "Assumptions and sources: diesel unit 7.74 kg of fuel an hour (Zurich 2004; Fleuti 2006, known only "
             "through Padhra 2018: second-hand, indicative)\n× 3.19 kg CO$_2$/kg (IPCC 2006 default). APU 103.2 kg of fuel "
             "an hour (Padhra 2018) × 3.163 kg CO$_2$/kg (MIA's factor). Turnarounds = 65,470\naircraft movements in 2025 / 2 "
             "(MIA, 14 Jan 2026). Gross figures: grid power at 0.389 kg CO$_2$/kWh (MIA) replaces the diesel, so the net "
             "saving is smaller.\nAn illustration of what the claim would require, not an estimate of the programme's "
             "effect. Calculations: tools/cc-030-report/calc.py.",
             fontsize=7.2, color=GREY, ha="left", va="top")
    fig.savefig(OUT / "fig2_gpu.png", bbox_inches="tight", facecolor="white")


fig1()
fig2()
print("figures in", OUT)
