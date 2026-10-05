"""Figures for Claim Check 005, drawn offline from data/cc-005/ (run fetch_data.py first for fresh data)
and the Malta outline in docs/data/geo.json. Output: out/fig1_share.png, out/fig2_map.png, out/fig3_sites.png"""
import csv
import json
import math
import pathlib

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from matplotlib.lines import Line2D
from matplotlib.patches import Rectangle

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[1]
D = ROOT / "data" / "cc-005"
OUT = HERE / "out"
OUT.mkdir(exist_ok=True)
for f in ["LiberationSans-Regular", "LiberationSans-Bold", "LiberationSans-Italic"]:
    fm.fontManager.addfont(f"/usr/share/fonts/truetype/liberation/{f}.ttf")
plt.rcParams.update({"font.family": "Liberation Sans", "axes.spines.top": False, "axes.spines.right": False,
                     "axes.edgecolor": "#8A9399", "axes.labelcolor": "#2B3A42", "xtick.color": "#2B3A42",
                     "ytick.color": "#2B3A42"})
GREEN, SAGE, AMBER, RED, SLATE, GREY, ORANGE, BLUE = ("#14452F", "#7FA88B", "#E3A72F", "#B5483A", "#2B3A42",
                                                      "#8A9399", "#D9772B", "#3C6E8F")
LANDC, SEA = "#E4E1D8", "#F4F8FA"
CLS = {"Excellent": SAGE, "Good": AMBER, "Sufficient": ORANGE, "Poor": RED}
SHARE = list(csv.DictReader(open(D / "excellent_share.csv")))
SITES = list(csv.DictReader(open(D / "mt_site_classes.csv")))
SRC = "Source: EEA bathing-water data (DiscoMap 2025 service; DiscoData WISE_BWD), retrieved 5 Oct 2026."

# Malta outline: geo.json rings are metres east/north of an origin; sites are projected the same way
geo = json.load(open(ROOT / "docs" / "data" / "geo.json"))
O = geo["origin"]
K = 111320 * math.cos(math.radians(O["lat"]))


def xy(lon, lat):
    return (lon - O["lon"]) * K, (lat - O["lat"]) * 110574


def land(ax, lw=0.5):
    for isl in geo["islands"]:
        r = isl.get("detail") or isl["coarse"]
        ax.fill(r[0::2], r[1::2], fc=LANDC, ec=GREY, lw=lw, zorder=1)


def fig1():
    yrs = [int(r["season"]) for r in SHARE]
    mt = [float(r["mt_excellent_pct"]) for r in SHARE]
    eu = [float(r["eu27_coastal_excellent_pct"]) for r in SHARE]
    n = [int(r["mt_excellent"]) for r in SHARE]
    fig, ax = plt.subplots(figsize=(9.6, 4.5), dpi=220)
    ax.axvspan(2022.55, 2023.45, color="#E6EFE8", zorder=0)
    ax.plot(yrs, eu, color=BLUE, lw=1.8, ls="--", marker="o", ms=3.5, label="EU-27 coastal bathing waters", zorder=3)
    ax.plot(yrs, mt, color=GREEN, lw=2.6, marker="o", ms=6, label="Malta: 87 coastal bathing waters (numbers: sites rated excellent)", zorder=4)
    for y, v, k in zip(yrs, mt, n):
        ax.text(y, v + 0.55, f"{k}", ha="center", va="bottom", fontsize=8.5, color=GREEN, fontweight="bold")
    ax.annotate("2023 season: 80 of 87 = 92.0%, the figure\nthe Commission quoted (2024: also 80 of 87)",
                xy=(2023, 92.0), xytext=(2019.6, 90.9), fontsize=8.6, color=SLATE, ha="center", va="top",
                arrowprops={"arrowstyle": "-", "color": SLATE, "lw": 0.7})
    ax.annotate("2025: 77 of 87 = 88.5%,\nlowest in the series", xy=(2025, 88.5), xytext=(2024.2, 85.6),
                fontsize=8.6, color=RED, ha="right", va="center", fontweight="bold",
                arrowprops={"arrowstyle": "-", "color": RED, "lw": 0.7})
    ax.text(2025.2, eu[-1] - 0.05, f"EU coastal\n{eu[-1]:.1f}%", fontsize=8, color=BLUE, va="top", ha="left")
    ax.text(2025.2, mt[-1] + 0.4, f"Malta\n{mt[-1]:.1f}%", fontsize=8, color=GREEN, va="bottom", ha="left",
            fontweight="bold")
    ax.set_xlim(2014.6, 2026.1)
    ax.set_ylim(84, 101)
    ax.set_xticks(yrs)
    ax.set_yticks(range(84, 101, 2))
    ax.set_yticklabels([f"{v}%" for v in range(84, 101, 2)])
    ax.tick_params(labelsize=8.5)
    ax.set_ylabel("Share of bathing waters rated excellent", fontsize=8.5)
    ax.legend(frameon=False, fontsize=8.5, loc="lower left")
    ax.set_title("Bathing waters rated excellent: Malta and the EU-27 coastal average, seasons 2015–2025",
                 fontsize=9.5, color=GREEN, loc="left", fontweight="bold", pad=10)
    fig.text(0.01, -0.01, "Each season’s class rests on the last four seasons’ samples. EU share: excellent ÷ all "
             "EU-27 coastal bathing waters, including those not classified.\n" + SRC, fontsize=7, color=GREY,
             va="top")
    fig.savefig(OUT / "fig1_share.png", bbox_inches="tight", facecolor="white")


def changed(s):
    return s["2024"] != s["2025"]


def fig2():
    fig = plt.figure(figsize=(9.6, 6.9), dpi=220)
    ax = fig.add_axes([0, 0.05, 1, 0.9])
    ax.set_facecolor(SEA)
    land(ax)
    order = ["Excellent", "Good", "Sufficient", "Poor"]
    for c in order:
        pts = [xy(float(s["longitude"]), float(s["latitude"])) for s in SITES if s["2025"] == c]
        if pts:
            big = c != "Excellent"
            ax.scatter([p[0] for p in pts], [p[1] for p in pts], s=46 if big else 22, c=CLS[c],
                       ec=SLATE if big else GREEN, lw=0.6, zorder=4 if big else 3)
    halo = {"bbox": {"fc": "white", "ec": "none", "alpha": 0.85, "pad": 1.2}}
    notes = [  # (site ids, label, text offset in metres, colour)
        (["D06", "D07"], "Xlendi Bay D06, D07\nExcellent → Good", (-1500, -3600), AMBER),
        (["C22", "C23"], "St Paul’s Bay C22, C23\nC23 Sufficient → Good;\nC22 Good since 2022", (-1500, 3900), SLATE),
        (["A11"], "Birżebbuġa A11\nSufficient → Good", (-5200, -2400), SLATE),
        (["C14"], "Mellieħa Bay C14:\nGood since 2023", (-6200, -2600), SLATE),
    ]
    idx = {s["site"]: s for s in SITES}
    for ids, txt, (dx, dy), col in notes:
        x, y = map(sum, zip(*[xy(float(idx[i]["longitude"]), float(idx[i]["latitude"])) for i in ids]))
        x, y = x / len(ids), y / len(ids)
        ax.annotate(txt, xy=(x, y), xytext=(x + dx, y + dy), fontsize=9, color=SLATE, ha="center", va="center",
                    arrowprops={"arrowstyle": "-", "color": SLATE, "lw": 0.6}, zorder=6,
                    fontweight="bold" if col != SLATE else "normal", **halo)
    # inset box: St Julian's and Sliema
    bx0, by0 = xy(14.481, 35.9075)
    bx1, by1 = xy(14.5125, 35.934)
    ax.add_patch(Rectangle((bx0, by0), bx1 - bx0, by1 - by0, fill=False, ec=SLATE, lw=0.8, zorder=5))
    ax.annotate("", xy=(bx1, by1 - 200), xytext=(bx1 + 4300, by1 + 2900),
                arrowprops={"arrowstyle": "-", "color": SLATE, "lw": 0.6})
    x0, y0 = xy(14.17, 35.79)
    x1, y1 = xy(14.60, 36.09)
    ax.set_xlim(x0, x1)
    ax.set_ylim(y0, y1)
    ax.set_aspect("equal")
    ax.set_xticks([]), ax.set_yticks([])
    for s_ in ax.spines.values():
        s_.set_visible(False)
    ax.text(*xy(14.255, 36.005), "Gozo", fontsize=9, color=GREY, style="italic", ha="center")
    ax.text(*xy(14.43, 35.885), "Malta", fontsize=9, color=GREY, style="italic", ha="center")
    # scale bar 5 km
    sx, sy = xy(14.19, 35.80)
    ax.plot([sx, sx + 5000], [sy, sy], color=SLATE, lw=2, solid_capstyle="butt")
    ax.text(sx + 2500, sy + 350, "5 km", ha="center", fontsize=7.5, color=SLATE)
    # inset map
    ins = fig.add_axes([0.575, 0.52, 0.39, 0.39])
    ins.set_facecolor(SEA)
    land(ins, lw=0.6)
    for c in order:
        pts = [(s["site"], *xy(float(s["longitude"]), float(s["latitude"]))) for s in SITES if s["2025"] == c]
        big = c != "Excellent"
        ins.scatter([p[1] for p in pts], [p[2] for p in pts], s=60 if big else 34, c=CLS[c],
                    ec=SLATE if big else GREEN, lw=0.6, zorder=4 if big else 3)
    lab = {"B03": ("St George’s Bay B03\nExcellent → Good", (1250, 420)),
           "B04": ("B04: Good since 2023", (1150, -330)),
           "B08": ("Balluta Bay B08, B09\nSufficient since 2022", (-620, -620))}
    for sid, (txt, (dx, dy)) in lab.items():
        x, y = xy(float(idx[sid]["longitude"]), float(idx[sid]["latitude"]))
        ins.annotate(txt, xy=(x, y), xytext=(x + dx, y + dy), fontsize=8.6, color=SLATE, ha="center", va="center",
                     arrowprops={"arrowstyle": "-", "color": SLATE, "lw": 0.6}, zorder=6,
                     fontweight="bold" if sid == "B03" else "normal", **halo)
    ins.set_xlim(bx0, bx1)
    ins.set_ylim(by0, by1)
    ins.set_aspect("equal")
    ins.set_xticks([]), ins.set_yticks([])
    for s_ in ins.spines.values():
        s_.set_visible(True)
        s_.set_edgecolor(SLATE)
        s_.set_linewidth(0.8)
    ins.text(0.0, 1.015, "Inset: St Julian’s and Sliema", transform=ins.transAxes, fontsize=8.6, color=SLATE,
             fontweight="bold", va="bottom")
    counts = {c: sum(s["2025"] == c for s in SITES) for c in order}
    ax.legend(handles=[Line2D([], [], ls="", marker="o", ms=7 if c != "Excellent" else 5.5, mfc=CLS[c],
                              mec=SLATE if c != "Excellent" else GREEN, label=f"{c}: {counts[c]}") for c in order],
              title="2025 class (87 sites)", title_fontsize=9, frameon=False, fontsize=9, loc="lower left",
              bbox_to_anchor=(0.0, 0.08))
    fig.text(0.0, 1.0, "Malta’s 87 bathing waters by 2025 class, with the sites that changed class since 2024",
             fontsize=9.5, color=GREEN, fontweight="bold", va="top")
    fig.text(0.0, 0.035, "Labels mark every site whose class changed between the 2024 and 2025 seasons, and the "
             "sites below excellent in both. Coastline © OpenStreetMap contributors.\n" + SRC, fontsize=7,
             color=GREY, va="top")
    fig.savefig(OUT / "fig2_map.png", bbox_inches="tight", facecolor="white")


def fig3():
    yrs = [str(y) for y in range(2015, 2026)]
    loc = {"B03": "St George’s Bay, St Julian’s", "B04": "St George’s Bay, St Julian’s",
           "B08": "Balluta Bay, St Julian’s", "B09": "Balluta Bay, St Julian’s", "A11": "St George’s Bay, Birżebbuġa",
           "C14": "Mellieħa Bay", "C22": "St Paul’s Bay", "C23": "St Paul’s Bay", "D06": "Xlendi Bay, Gozo",
           "D07": "Xlendi Bay, Gozo"}
    rows = [s for s in SITES if any(s[y] != "Excellent" for y in yrs)]
    rows.sort(key=lambda s: (-sum(s[y] == "Sufficient" for y in yrs), -sum(s[y] != "Excellent" for y in yrs)))
    assert set(s["site"] for s in rows) == set(loc), [s["site"] for s in rows]
    fig, ax = plt.subplots(figsize=(9.6, 0.34 * (len(rows) + 3.75)), dpi=220)
    for i, s in enumerate(rows):
        for j, y in enumerate(yrs):
            c = s[y]
            ax.add_patch(Rectangle((j, -i - 0.92), 0.94, 0.86, fc=CLS[c] if c != "Excellent" else "#DCE8DF",
                                   ec="none"))
            if c != "Excellent":
                ax.text(j + 0.47, -i - 0.49, c[0], ha="center", va="center", fontsize=8,
                        color="white" if c == "Sufficient" else SLATE, fontweight="bold")
        ax.text(-0.15, -i - 0.49, f"{s['site']}  {loc[s['site']]}", ha="right", va="center", fontsize=8.5, color=SLATE)
    for j, y in enumerate(yrs):
        ax.text(j + 0.47, 0.25, y, ha="center", va="bottom", fontsize=8.3, color=SLATE,
                fontweight="bold" if y == "2023" else "normal")
    ax.add_patch(Rectangle((8 - 0.03, -len(rows) - 0.06), 1.0, len(rows) + 0.06, fill=False, ec=GREEN, lw=1.4))
    n = len(rows)
    ax.set_xlim(-5.2, 11.1)
    ax.set_ylim(-n - 2.3, 1.45)
    ax.axis("off")
    ax.text(-5.15, 1.2, "The 10 Maltese bathing waters rated below excellent in at least one season, 2015–2025",
            fontsize=9.5, color=GREEN, fontweight="bold", va="bottom")
    for i, (lab, fc) in enumerate([("Excellent", "#DCE8DF"), ("Good (G)", AMBER), ("Sufficient (S)", ORANGE)]):
        ax.add_patch(Rectangle((0.0 + 2.2 * i, -n - 0.85), 0.5, 0.45, fc=fc, ec="none"))
        ax.text(0.62 + 2.2 * i, -n - 0.62, lab, fontsize=8.3, color=SLATE, va="center")
    ax.text(-5.15, -n - 1.35, "The other 77 sites were excellent in every season. Green outline: the 2023 season "
            "quoted by the Commission.\n" + SRC, fontsize=7, color=GREY, va="top")
    fig.savefig(OUT / "fig3_sites.png", bbox_inches="tight", facecolor="white")


fig1()
fig2()
fig3()
print("figures in", OUT)
