"""Figure for Claim Check 116: the Committee's requests on Valletta's setting, 2009 to 2026.
Dates and wording are from Decision 47 COM 7B.114 and the Committee's document WHC/25/47.COM/7B.Add.3, pp. 71-74."""
import pathlib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm

HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE / "out"
OUT.mkdir(exist_ok=True)
for f in ["LiberationSans-Regular", "LiberationSans-Bold", "LiberationSans-Italic"]:
    fm.fontManager.addfont(f"/usr/share/fonts/truetype/liberation/{f}.ttf")
plt.rcParams.update({"font.family": "Liberation Sans"})
GREEN, AMBER, RED, SLATE, GREY, BLUE = "#14452F", "#E3A72F", "#B5483A", "#2B3A42", "#8A9399", "#3C6E8F"

EVENTS = [  # (year, label, colour, label above?)
    (2009, "33 COM 7B.113\nBuffer zone with height\ncontrols; Views and Vistas\nAnalysis requested", SLATE, True),
    (2014, "38 COM 8E\nStatement of OUV: control\nof development in the\nsetting; FAR policy issued", SLATE, False),
    (2017, "Advisory Mission: FAR policy\na step forward, but it names\nsites for tall buildings\nin the setting", GREY, True),
    (2023, "45 COM 7B.190\n(extended 45th session)", SLATE, False),
    (2025, "47 COM 7B.114\nSetting not sufficiently\nsafeguarded; four planning\ndocuments to be revised", GREEN, True),
    (2026.92, "1 Dec 2026\nUpdated report due\n(49th session)", AMBER, False),
]


def fig1():
    fig, ax = plt.subplots(figsize=(9.6, 3.9), dpi=220)
    ax.axhline(0, color=SLATE, lw=1.4)
    for x, lab, col, up in EVENTS:
        y = 0.62 if up else -0.62
        ax.plot([x, x], [0, y * 0.78], color=col, lw=1)
        ax.scatter([x], [0], s=46, color=col, zorder=3)
        ax.text(x, y, lab, ha="center", va="bottom" if up else "top", fontsize=7.6, color=SLATE,
                fontweight="bold" if col in (GREEN,) else None, linespacing=1.25)
        ax.text(x, -0.1 if up else 0.1, f"{int(x)}", ha="center", va="top" if up else "bottom", fontsize=8.5, color=col, fontweight="bold")
    ax.set_xlim(2007.2, 2028.4); ax.set_ylim(-1.55, 1.55); ax.axis("off")
    fig.text(0.01, 0.0, "Sources: Decision 47 COM 7B.114 (whc.unesco.org/en/decisions/8838); WHC/25/47.COM/7B.Add.3, pp. 71-74. "
             "FAR = 2014 Planning Policy Guide on the Use and Applicability of the Floor Area Ratio.", fontsize=6.8, color=GREY)
    fig.savefig(OUT / "fig1_timeline.png", bbox_inches="tight", facecolor="white")


if __name__ == "__main__":
    fig1()
