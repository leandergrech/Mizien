import os
HERE = os.path.dirname(os.path.abspath(__file__))
OUTDIR = os.path.join(HERE, "out")
os.makedirs(OUTDIR, exist_ok=True)
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle
from matplotlib import font_manager as fm

for f in ["LiberationSans-Regular", "LiberationSans-Bold", "LiberationSans-Italic"]:
    fm.fontManager.addfont(f"/usr/share/fonts/truetype/liberation/{f}.ttf")
plt.rcParams["font.family"] = "Liberation Sans"

GREEN = "#14452F"
SAGE = "#7FA88B"
PALE = "#E6EFE8"
AMBER = "#E3A72F"
RED = "#B5483A"
SLATE = "#2B3A42"
GREY = "#8A9399"
CREAM = "#F6F4EE"
BLUE = "#3C6E8F"

OUT = OUTDIR + os.sep


# ------------------------------------------------------------------ Fig 1
def fig_mechanism():
    fig, ax = plt.subplots(figsize=(9.6, 4.9), dpi=220)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 52)
    ax.axis("off")

    def box(x, y, w, h, text, fc, ec=None, tc="white", fs=8.6, bold=False):
        p = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.25,rounding_size=1.4",
                           fc=fc, ec=ec or fc, lw=1.1)
        ax.add_patch(p)
        ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", color=tc,
                fontsize=fs, fontweight="bold" if bold else "normal", linespacing=1.25)

    def arrow(x1, y1, x2, y2, c=GREY):
        ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="-|>", mutation_scale=11,
                                     lw=1.3, color=c, shrinkA=1, shrinkB=1))

    # column headers
    heads = [(2, "1  WHAT IS DONE"), (27, "2  WHAT CHANGES AT THE ROOT ZONE"),
             (59, "3  WHAT HAPPENS TO ROOTS"), (84, "4  WHAT THE TREE SHOWS")]
    for x, t in heads:
        ax.text(x, 50.2, t, fontsize=7.6, fontweight="bold", color=GREEN, va="center")
    ax.plot([2, 98], [48.4, 48.4], color=SAGE, lw=0.9)

    # col 1
    box(1.5, 33, 19, 10, "Excavate / remove\nsoil near trunk", GREEN, bold=True)
    box(1.5, 12, 19, 10, "Pour concrete over\nmembrane; mulch\nand pots on top", GREEN, bold=True)

    # col 2
    box(25, 38, 27, 8, "Roots cut or exposed;\nsoil compacted", PALE, ec=SAGE, tc=SLATE)
    box(25, 28, 27, 8, "Less rain / irrigation reaches\nthe root zone", PALE, ec=SAGE, tc=SLATE)
    box(25, 18, 27, 8, "Less gas exchange:\nlower O$_2$, higher CO$_2$", PALE, ec=SAGE, tc=SLATE)
    box(25, 8, 27, 8, "Warmer soil; alkaline\nleachate while curing", PALE, ec=SAGE, tc=SLATE)
    box(25, 0.6, 27, 6, "Concrete touching trunk /\nroot collar covered", PALE, ec=SAGE, tc=SLATE)

    # col 3
    box(57, 33, 24, 9, "Fine-root loss;\nshallower rooting", "#F3E3C0", ec=AMBER, tc=SLATE, bold=True)
    box(57, 18, 24, 9, "Reduced water uptake;\nhydraulic stress", "#F3E3C0", ec=AMBER, tc=SLATE, bold=True)
    box(57, 5, 24, 9, "Stress on trunk base;\nrot / decay risk", "#F3E3C0", ec=AMBER, tc=SLATE, bold=True)

    # col 4
    box(84.5, 15, 14, 18, "Thin crown,\ndieback,\ndecline", RED, bold=True)
    ax.text(91.5, 11.0, "often 3\u20135+ years\nafter the works", ha="center", va="top", fontsize=7.4,
            color=RED, fontstyle="italic")

    # arrows
    arrow(20.8, 38, 24.6, 42)
    arrow(20.8, 17, 24.6, 32)
    arrow(20.8, 17, 24.6, 22)
    arrow(20.8, 17, 24.6, 12)
    arrow(20.8, 17, 24.6, 4)
    arrow(52.4, 42, 56.6, 38)
    arrow(52.4, 32, 56.6, 36)
    arrow(52.4, 32, 56.6, 23)
    arrow(52.4, 22, 56.6, 36)
    arrow(52.4, 22, 56.6, 22)
    arrow(52.4, 12, 56.6, 22)
    arrow(52.4, 4, 56.6, 9)
    arrow(81.4, 37, 84.2, 27)
    arrow(81.4, 22, 84.2, 24)
    arrow(81.4, 9, 84.2, 19)

    fig.savefig(OUT + "fig1_mechanism.png", bbox_inches="tight", facecolor="white")
    plt.close(fig)


# ------------------------------------------------------------------ Fig 2
def fig_evidence_map():
    rows = [
        # label, x position (-1 adverse .. +1 no adverse effect), design, second-hand?
        ("Viswanathan et al. 2011\nsweetgum, field expt, concrete over mature trees", -0.85, "exp", False),
        ("Savi et al. 2015\nholm oak, 4 urban sites (Trieste)", -0.70, "obs", False),
        ("Cui et al. 2022\nginkgo & plane, 40 paired sites (Beijing)", -0.60, "obs", False),
        ("North et al. 2015\ncondition falls nearer pavement", -0.45, "obs", True),
        ("Review, Arboric. & Urban For. 2014\nmixed effects on root environment", -0.06, "rev", False),
        ("Hauer et al. 1994\nstreet works at 5\u20137\u00d7 trunk diameter: small (+4%) mortality rise", 0.10, "obs", True),
        ("Fini et al. 2022\nCeltis & Fraxinus, 5-yr randomised: no growth loss, roots altered", 0.50, "exp", False),
        ("Volder et al. 2009\nsweetgum 15\u201318 yr, gas exchange unchanged", 0.80, "obs", True),
    ]
    col = {"exp": GREEN, "obs": BLUE, "rev": AMBER}
    fig, ax = plt.subplots(figsize=(9.6, 5.0), dpi=220)
    ax.set_xlim(-1.15, 1.15)
    ax.set_ylim(-0.7, len(rows) - 0.3)
    ax.axvspan(-1.15, -0.2, color="#F4DEDA", alpha=0.65, lw=0)
    ax.axvspan(-0.2, 0.2, color="#F6EBCD", alpha=0.75, lw=0)
    ax.axvspan(0.2, 1.15, color="#DDEBDF", alpha=0.75, lw=0)
    ax.text(-0.675, len(rows) - 0.38, "ADVERSE EFFECT REPORTED", ha="center", fontsize=7.8,
            fontweight="bold", color=RED)
    ax.text(0.0, len(rows) - 0.38, "MIXED", ha="center", fontsize=7.8, fontweight="bold", color="#9A6B00")
    ax.text(0.675, len(rows) - 0.38, "NO ADVERSE EFFECT DETECTED", ha="center", fontsize=7.8,
            fontweight="bold", color=GREEN)
    for i, (lab, x, d, sh) in enumerate(rows):
        y = len(rows) - 1 - i - 0.35
        ax.hlines(y, -1.15, 1.15, color="white", lw=0.8)
        ax.scatter([x], [y], s=190, color=col[d], zorder=3, edgecolor="white", lw=1.6,
                   marker="o" if not sh else "D")
        side = "left" if x > 0 else "right"
        dx = -0.07 if x > 0 else 0.07
        # labels placed on the opposite side of the dot's half
        if x < -0.2:
            ax.text(x + 0.09, y, lab, va="center", ha="left", fontsize=7.1, color=SLATE, linespacing=1.2)
        elif x > 0.2:
            ax.text(x - 0.09, y, lab, va="center", ha="right", fontsize=7.1, color=SLATE, linespacing=1.2)
        else:
            ax.text(x + 0.09, y, lab, va="center", ha="left", fontsize=7.1, color=SLATE, linespacing=1.2)
    ax.set_yticks([])
    ax.set_xticks([])
    for s in ax.spines.values():
        s.set_visible(False)
    # legend
    from matplotlib.lines import Line2D
    h = [Line2D([0], [0], marker="o", color="w", markerfacecolor=GREEN, markersize=9, label="Randomised experiment"),
         Line2D([0], [0], marker="o", color="w", markerfacecolor=BLUE, markersize=9, label="Observational / field survey"),
         Line2D([0], [0], marker="o", color="w", markerfacecolor=AMBER, markersize=9, label="Review"),
         Line2D([0], [0], marker="D", color="w", markerfacecolor="#BFC5C9", markersize=8, label="Diamond = known to us second-hand")]
    ax.legend(handles=h, loc="upper center", bbox_to_anchor=(0.5, -0.02), ncol=4, frameon=False, fontsize=7.4)
    fig.savefig(OUT + "fig2_evidence_map.png", bbox_inches="tight", facecolor="white")
    plt.close(fig)


# ------------------------------------------------------------------ Fig 3
def fig_timeline():
    fig, ax = plt.subplots(figsize=(9.6, 2.5), dpi=220)
    ax.set_xlim(0, 8.4)
    ax.set_ylim(0, 3)
    ax.axis("off")
    # axis line
    ax.annotate("", xy=(8.3, 1.1), xytext=(0, 1.1), arrowprops=dict(arrowstyle="-|>", color=SLATE, lw=1.4))
    for t in range(0, 9):
        ax.plot([t, t], [1.05, 1.15], color=SLATE, lw=1)
        ax.text(t, 0.8, f"{t}", ha="center", va="top", fontsize=7.6, color=SLATE)
    ax.text(4.2, 0.18, "years since the works", ha="center", fontsize=8, color=SLATE, fontstyle="italic")
    # symptom window
    ax.add_patch(Rectangle((3, 1.25), 2.6, 0.5, fc="#F3C9C2", ec=RED, lw=1.1))
    ax.text(4.3, 1.5, "decline typically becomes visible: 3\u20135+ yrs", ha="center", va="center",
            fontsize=7.6, color=RED, fontweight="bold")
    ax.add_patch(Rectangle((0, 1.25), 3, 0.5, fc="#E6EFE8", ec=SAGE, lw=1.1))
    ax.text(1.5, 1.5, "tree can look healthy", ha="center", va="center", fontsize=7.6, color=GREEN, fontweight="bold")
    # claim marker: position unknown
    ax.annotate("", xy=(8.25, 2.25), xytext=(0.05, 2.25),
                arrowprops=dict(arrowstyle="<|-|>", color=AMBER, lw=1.6, ls=(0, (4, 3))))
    ax.text(4.15, 2.62, "Where does \u201cno tree has died\u201d fall on this line?  The dates of the earlier works are not published.",
            ha="center", va="center", fontsize=7.9, color=SLATE, fontweight="bold")
    ax.text(4.15, 2.0, "?", ha="center", va="center", fontsize=11, color=AMBER, fontweight="bold")
    fig.savefig(OUT + "fig3_timeline.png", bbox_inches="tight", facecolor="white")
    plt.close(fig)


fig_mechanism()
fig_evidence_map()
fig_timeline()
print("ok")
