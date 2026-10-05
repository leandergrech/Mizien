"""Figures for Claim Check 016, drawn from data/cc-016/ (run calc.py first)."""
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
GREEN, SAGE, AMBER, RED, SLATE, GREY, ORANGE, BLUE = ("#14452F", "#7FA88B", "#E3A72F", "#B5483A", "#2B3A42",
                                                      "#8A9399", "#D9772B", "#3C6E8F")
D = ROOT / "data" / "cc-016"
U = {r["item"]: float(r["value"]) for r in csv.DictReader(open(D / "ops_uptake.csv"))}
CALLS = {int(r["year"]): int(r["calls"]) for r in csv.DictReader(open(D / "cruise_calls.csv"))}


def fig1():
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(9.6, 3.8), dpi=220, gridspec_kw={"width_ratios": [1.15, 1]})
    labs = ["Claimed cut in\nharbour pollution", "Berths that\nplugged in", "Berth time\nplugged in"]
    vals = [90, 100 * U["Berths connected to onshore power (OPS)"] / U["Cruise berths at Valletta Cruise Port"],
            U["Share of berth time connected"]]
    cols = [GREY, SAGE, GREEN]
    b = a1.bar(labs, vals, color=cols, width=0.62)
    for r, v in zip(b, vals):
        a1.text(r.get_x() + r.get_width() / 2, v + 2, f"{v:.0f}%", ha="center", fontsize=11, fontweight="bold",
                color=SLATE)
    a1.set_ylim(0, 105)
    a1.set_ylabel("%")
    a1.set_title("Promise and first-year use", fontsize=9.5, color=GREEN, loc="left", fontweight="bold")
    st = ["1 day\nor less", "1–2\ndays", "2–4\ndays"]
    sv = [U["Berths of 1 day or less connected"], U["Berths of 1-2 days connected"], U["Berths of 2-4 days connected"]]
    b2 = a2.bar(st, sv, color=[SAGE, SAGE, RED], width=0.6)
    for r, v in zip(b2, sv):
        a2.text(r.get_x() + r.get_width() / 2, v + 0.6, f"{v:.1f}%", ha="center", fontsize=10, color=SLATE)
    a2.set_ylim(0, 25)
    a2.set_title("Share of berths plugged in, by length of stay", fontsize=9.5, color=GREEN, loc="left",
                 fontweight="bold")
    fig.text(0.01, -0.04, "10 Jul 2024 – 10 Jul 2025. Sources: Infrastructure Malta; Amphora Media analysis of Transport "
             "Malta FOI records and the Valletta Cruise Port schedule (second-hand).", fontsize=7, color=GREY)
    fig.tight_layout(w_pad=3)
    fig.savefig(OUT / "fig1_uptake.png", bbox_inches="tight", facecolor="white")


def fig2():
    fig, ax = plt.subplots(figsize=(9.6, 3.2), dpi=220)
    ys = sorted(CALLS)
    cols = [GREY if y < 2024 else GREEN for y in ys]
    b = ax.bar([str(y) for y in ys], [CALLS[y] for y in ys], color=cols, width=0.6)
    for r, y in zip(b, ys):
        ax.text(r.get_x() + r.get_width() / 2, CALLS[y] + 6, str(CALLS[y]), ha="center", fontsize=10, color=SLATE)
    ax.set_ylim(0, 480)
    ax.set_ylabel("Cruise calls")
    ax.axvline(2.5, color=AMBER, ls="--", lw=1.4)
    ax.text(2.55, 455, "Shore power in service (trial Dec 2023, launch Jul 2024)", fontsize=8, color=AMBER)
    ax.set_xlabel("Grey: as quoted by Amphora Media (second-hand). Green: Valletta Cruise Port 2025 results release. "
                  "2020-21 omitted (pandemic).", fontsize=7, color=GREY)
    fig.savefig(OUT / "fig2_calls.png", bbox_inches="tight", facecolor="white")


def fig3():
    """v1.2: the 373 berths split by connection, and the 90% per connected ship against the harbour-wide share."""
    from matplotlib.patches import Rectangle
    berths = int(U["Cruise berths at Valletta Cruise Port"])
    conn = int(U["Berths connected to onshore power (OPS)"])
    msc = int(U["Connections by MSC World Europa"])
    t = U["Share of berth time connected"]
    LIGHT = "#D5DBD7"
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(9.6, 4.1), dpi=220, gridspec_kw={"width_ratios": [1.05, 1]})
    cols, rows = 25, 15
    kinds = [GREEN] * msc + [SAGE] * (conn - msc) + [LIGHT] * (berths - conn)
    for i, col in enumerate(kinds):
        cx, cy = i // rows, rows - 1 - i % rows
        a1.add_patch(Rectangle((cx + 0.08, cy + 0.08), 0.84, 0.84, facecolor=col, edgecolor="none"))
    a1.set_xlim(0, cols)
    a1.set_ylim(-5.2, rows)
    a1.set_aspect("equal")
    a1.axis("off")
    leg = [(GREEN, f"{msc} plugged in: MSC World Europa (LNG-powered)"),
           (SAGE, f"{conn - msc} plugged in: all other ships"),
           (LIGHT, f"{berths - conn} not plugged in")]
    for k, (col, lab) in enumerate(leg):
        y = -1.4 - k * 1.3
        a1.add_patch(Rectangle((0.08, y), 0.84, 0.84, facecolor=col, edgecolor="none"))
        a1.text(1.4, y + 0.42, lab, fontsize=9.5, color=SLATE, va="center")
    a1.set_title(f"The {berths} cruise berths, Jul 2024 – Jul 2025 (one square each)", fontsize=9.5, color=GREEN,
                 loc="left", fontweight="bold")
    labs = ["NO2", "Particulate matter", "SO2", "CO2"]
    vals = [U[f"Per-liner cut on shore power: {k}"] for k in
            ["nitrogen dioxide", "particulate matter", "sulphur dioxide", "carbon dioxide"]]
    ys = [5.4, 4.6, 3.8, 3.0]
    a2.barh(ys, vals, height=0.62, color=[GREEN, GREEN, GREEN, SAGE])
    for y, v, lab in zip(ys, vals, labs):
        a2.text(1.5, y, lab, va="center", fontsize=9, color="white", fontweight="bold")
        a2.text(v + 1.5, y, f"−{v:g}%", va="center", fontsize=9.5, color=SLATE)
    a2.text(0, 6.15, "Per connected liner while plugged in (Infrastructure Malta)", fontsize=8.5, color=SLATE,
            fontweight="bold")
    a2.barh([1.2], [t], height=0.62, color=RED)
    a2.text(t + 1.5, 1.2, f"≤{t:g}%", va="center", fontsize=9.5, color=SLATE)
    a2.text(0, 1.95, "Harbour-wide: share of cruise berth time plugged in, year one", fontsize=8.5, color=SLATE,
            fontweight="bold")
    a2.text(0, 0.45, "upper bound on the cut in at-berth cruise emissions", fontsize=8.5, color=GREY)
    a2.vlines(90, 2.55, 6.55, color=AMBER, ls="--", lw=1.3)
    a2.text(89, 6.6, "claimed: 90%", fontsize=8.5, color=SLATE, ha="right", va="bottom")
    a2.set_xlim(0, 112)
    a2.set_ylim(0, 7.1)
    a2.set_yticks([])
    a2.spines["left"].set_visible(False)
    a2.set_xticks([0, 25, 50, 75, 100])
    a2.set_xticklabels(["0", "25%", "50%", "75%", "100%"], fontsize=8)
    a2.set_title("The same 90%, two scopes", fontsize=9.5, color=GREEN, loc="left", fontweight="bold")
    fig.text(0.01, -0.035, "Berth and connection counts: Amphora Media analysis of Transport Malta FOI records and the "
             "Valletta Cruise Port schedule, 10 Jul 2024 – 10 Jul 2025 (second-hand; the FOI reply is not public).\n"
             "Per-liner cuts: Infrastructure Malta, 30 Nov 2020 (study not cited). MSC World Europa's fuel: MSC Cruises, "
             "24 Oct 2022 (dual-fuel LNG / low-sulphur marine gasoil).", fontsize=7, color=GREY)
    fig.tight_layout(w_pad=2.5)
    fig.savefig(OUT / "fig3_scope.png", bbox_inches="tight", facecolor="white")


if __name__ == "__main__":
    import sys
    for f in sys.argv[1:] or ["fig1", "fig2", "fig3"]:
        globals()[f]()
    print("figures in", OUT)
