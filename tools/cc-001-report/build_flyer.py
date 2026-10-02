import os
HERE = os.path.dirname(os.path.abspath(__file__))
OUTDIR = os.path.join(HERE, "out")
os.makedirs(OUTDIR, exist_ok=True)
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.utils import simpleSplit
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

FD = "/usr/share/fonts/truetype/liberation/"
for n, f in [("Serif-B", "LiberationSerif-Bold"), ("Serif-BI", "LiberationSerif-BoldItalic"),
             ("Serif-I", "LiberationSerif-Italic"), ("Sans", "LiberationSans-Regular"),
             ("Sans-B", "LiberationSans-Bold"), ("Sans-I", "LiberationSans-Italic")]:
    pdfmetrics.registerFont(TTFont(n, FD + f + ".ttf"))

GREEN = colors.HexColor("#14452F")
SAGE = colors.HexColor("#7FA88B")
PALE = colors.HexColor("#E6EFE8")
AMBER = colors.HexColor("#E3A72F")
AMBER_PALE = colors.HexColor("#FBF1D9")
RED = colors.HexColor("#B5483A")
SLATE = colors.HexColor("#2B3A42")
GREY = colors.HexColor("#8A9399")
CREAM = colors.HexColor("#F6F4EE")
ORANGE = colors.HexColor("#D9772B")
LIGHTGREEN = colors.HexColor("#BFD6C5")

OUT = os.path.join(OUTDIR, "flyer.pdf")
W, H = A4
M = 20 * mm
CW = W - 2 * M

c = canvas.Canvas(OUT, pagesize=A4)
c.setTitle("Claim Check 001 \u2013 Will concrete harm the Upper Barrakka trees?")
c.setAuthor("Mi\u017bien")


def para(x, y_top, text, font, size, color, width, leading=None, align="left"):
    """Draw wrapped text with top at y_top; return bottom y."""
    leading = leading or size * 1.28
    lines = simpleSplit(text, font, size, width)
    c.setFillColor(color)
    c.setFont(font, size)
    y = y_top - size * 0.86
    for ln in lines:
        if align == "center":
            c.drawCentredString(x + width / 2, y, ln)
        else:
            c.drawString(x, y, ln)
        y -= leading
    return y + leading - size * 0.14


# ---------------------------------------------------------------- header band
band_h = 72 * mm
c.setFillColor(GREEN)
c.rect(0, H - band_h, W, band_h, stroke=0, fill=1)
# tree rings (clipped to band)
c.saveState()
clip = c.beginPath()
clip.rect(0, H - band_h, W, band_h)
c.clipPath(clip, stroke=0, fill=0)
c.setStrokeColor(SAGE)
cx, cy = W * 0.88, H - 8 * mm
for i in range(1, 16):
    c.setStrokeAlpha(0.10 + (0.06 if i % 4 == 0 else 0))
    c.setLineWidth(1.1 if i % 4 == 0 else 0.6)
    c.ellipse(cx - i * 8.5 * mm, cy - i * 8 * mm, cx + i * 8.5 * mm, cy + i * 8.4 * mm)
c.setStrokeAlpha(1)
c.restoreState()

c.setFillColor(AMBER)
c.rect(M, H - 15 * mm, 12 * mm, 1.4 * mm, stroke=0, fill=1)
c.setFont("Sans-B", 8.5)
c.drawString(M, H - 21 * mm, "MI\u017bIEN")
c.setFillColor(LIGHTGREEN)
c.setFont("Sans", 8.5)
c.drawString(M + 19 * mm, H - 21 * mm, "Claim Check 001  \u00b7  Upper Barrakka Gardens, Valletta")

c.setFillColor(colors.white)
c.setFont("Serif-B", 30)
c.drawString(M, H - 36 * mm, "Will concrete harm")
c.drawString(M, H - 46 * mm, "the Upper Barrakka trees?")
c.setFillColor(colors.HexColor("#CFE2D4"))
c.setFont("Serif-I", 11.5)
c.drawString(M, H - 55 * mm, "A public claim, tested against the scientific literature")

# ---------------------------------------------------------------- claim card
card_top = H - 62 * mm
card_h = 44 * mm
card_y = card_top - card_h
c.setFillColor(colors.HexColor("#00000012"))
c.setFillColor(CREAM)
c.roundRect(M, card_y, CW, card_h, 3 * mm, stroke=0, fill=1)
c.setStrokeColor(colors.HexColor("#D5DBD7"))
c.setLineWidth(0.6)
c.roundRect(M, card_y, CW, card_h, 3 * mm, stroke=1, fill=0)
c.setFillColor(AMBER)
c.rect(M, card_y, 2.6 * mm, card_h, stroke=0, fill=1)
c.setFillColor(GREY)
c.setFont("Sans-B", 7.6)
c.drawString(M + 9 * mm, card_top - 8 * mm, "THE CLAIM")
c.setFillColor(GREEN)
c.setFont("Serif-BI", 18)
c.drawString(M + 9 * mm, card_top - 17 * mm, "\u201cGiven its temporary nature, it will not")
c.drawString(M + 9 * mm, card_top - 24.5 * mm, "cause damage to the tree.\u201d")
c.setFillColor(SLATE)
c.setFont("Sans-B", 8.2)
c.drawString(M + 9 * mm, card_top - 31.5 * mm, "Ambjent Malta, to the Times of Malta, 1 October 2026")
c.setFont("Sans", 7.8)
c.drawString(M + 9 * mm, card_top - 36.3 * mm,
             "About concrete placed in the tree planters, to be removed once a waterproofing membrane is in.")
c.setFont("Sans-I", 7.4)
c.setFillColor(GREY)
c.drawString(M + 9 * mm, card_top - 40.6 * mm,
             "The headline drops the \u201ctemporary\u201d condition and simply says the concrete won\u2019t damage the trees.")

# ---------------------------------------------------------------- verdict
vt = card_y - 6 * mm
vh = 25 * mm
c.setFillColor(ORANGE)
c.roundRect(M, vt - vh, CW, vh, 3 * mm, stroke=0, fill=1)
c.setFillColor(colors.white)
c.setFont("Sans-B", 8)
c.drawString(M + 7 * mm, vt - 7 * mm, "VERDICT")
c.setFont("Sans-B", 25)
c.drawString(M + 7 * mm, vt - 17.5 * mm, "NOT SUBSTANTIATED")
c.setFont("Serif-BI", 14)
c.drawRightString(W - M - 7 * mm, vt - 11 * mm, "Plausible,")
c.drawRightString(W - M - 7 * mm, vt - 17.5 * mm, "but not shown.")

# meter
my = vt - vh - 14 * mm
labels = [("SUPPORTED", ""), ("LARGELY", "SUPPORTED"), ("NOT", "SUBSTANTIATED"), ("MISLEADING", ""),
          ("CONTRADICTED", "")]
cols = [colors.HexColor("#2E7D4F"), colors.HexColor("#8DB36B"), ORANGE, colors.HexColor("#C85A3A"),
        colors.HexColor("#8E2F25")]
gap = 1.6 * mm
sw = (CW - 4 * gap) / 5
mh = 9.5 * mm
for i, (l1, l2) in enumerate(labels):
    x = M + i * (sw + gap)
    c.setFillColor(cols[i])
    if i == 2:
        c.roundRect(x - 0.6 * mm, my - 0.7 * mm, sw + 1.2 * mm, mh + 1.4 * mm, 1.8 * mm, stroke=0, fill=1)
        c.setStrokeColor(SLATE)
        c.setLineWidth(1.5)
        c.roundRect(x - 0.6 * mm, my - 0.7 * mm, sw + 1.2 * mm, mh + 1.4 * mm, 1.8 * mm, stroke=1, fill=0)
    else:
        c.roundRect(x, my, sw, mh, 1.8 * mm, stroke=0, fill=1)
    c.setFillColor(colors.white)
    c.setFont("Sans-B", 6.2)
    if l2:
        c.drawCentredString(x + sw / 2, my + mh / 2 + 0.7 * mm, l1)
        c.drawCentredString(x + sw / 2, my + mh / 2 - 2.5 * mm, l2)
    else:
        c.drawCentredString(x + sw / 2, my + mh / 2 - 1 * mm, l1)
mx = M + 2 * (sw + gap) + sw / 2
c.setFillColor(SLATE)
p = c.beginPath()
p.moveTo(mx - 2 * mm, my + mh + 4.4 * mm)
p.lineTo(mx + 2 * mm, my + mh + 4.4 * mm)
p.lineTo(mx, my + mh + 1.6 * mm)
p.close()
c.drawPath(p, stroke=0, fill=1)

# ---------------------------------------------------------------- results
ry = my - 7 * mm
c.setFillColor(GREEN)
c.setFont("Sans-B", 10.5)
c.drawString(M, ry, "MAIN RESULTS")
c.setStrokeColor(SAGE)
c.setLineWidth(0.8)
c.line(M, ry - 2 * mm, W - M, ry - 2 * mm)
c.setStrokeColor(AMBER)
c.setLineWidth(2.4)
c.line(M, ry - 2 * mm, M + 22 * mm, ry - 2 * mm)

cards = [
    ("Sound logic", GREEN, PALE,
     "Right reasoning",
     "Ambjent itself says prolonged cover is a risk (water, bark, nutrients, decay). That matches the research."),
    ("Undefined", ORANGE, colors.HexColor("#FBE9DA"),
     "How long is \u201ctemporary\u201d?",
     "No duration is given, yet harm from sealing builds with time."),
    ("Not addressed", RED, colors.HexColor("#F7E4E0"),
     "Soil removal and roots",
     "Soil was taken out of the planter. Root exposure and clearing concrete off roots aren\u2019t covered."),
    ("0 studies", RED, colors.HexColor("#F7E4E0"),
     "On temporary cover",
     "We found no research on short-term concrete contact with roots. For permanent sealing the science is mixed."),
    ("3\u20135+ years", ORANGE, colors.HexColor("#FBE9DA"),
     "Before damage shows",
     "Decline often appears late, so \u201cno tree has died\u201d in five treated planters says little."),
]
gx = 4 * mm
cwid = (CW - 2 * gx) / 3
chh = 36.5 * mm
top1 = ry - 6 * mm


def card(ix, iy, big, bigcol, bg, title, text):
    x = M + ix * (cwid + gx)
    ytop = top1 - iy * (chh + gx)
    c.setFillColor(bg)
    c.roundRect(x, ytop - chh, cwid, chh, 2.4 * mm, stroke=0, fill=1)
    c.setFillColor(bigcol)
    c.rect(x, ytop - 1.4 * mm, cwid, 1.4 * mm, stroke=0, fill=1)
    c.setFont("Sans-B", 16)
    c.drawString(x + 4 * mm, ytop - 11 * mm, big)
    c.setFillColor(SLATE)
    c.setFont("Sans-B", 8.4)
    c.drawString(x + 4 * mm, ytop - 16.6 * mm, title)
    para(x + 4 * mm, ytop - 19.2 * mm, text, "Sans", 7.7, SLATE, cwid - 8 * mm, leading=9.8)


for i, (big, bc, bg, t, tx) in enumerate(cards):
    card(i % 3, i // 3, big, bc, bg, t, tx)

# fairness card (6th cell)
x = M + 2 * (cwid + gx)
ytop = top1 - 1 * (chh + gx)
c.setFillColor(AMBER_PALE)
c.roundRect(x, ytop - chh, cwid, chh, 2.4 * mm, stroke=0, fill=1)
c.setFillColor(AMBER)
c.rect(x, ytop - chh, 1.6 * mm, chh, stroke=0, fill=1)
c.setFillColor(SLATE)
c.setFont("Sans-B", 8.4)
c.drawString(x + 5 * mm, ytop - 8 * mm, "FAIR TO SAY")
para(x + 5 * mm, ytop - 11 * mm,
     "Protecting the Lascaris War Rooms from flooding is a legitimate aim. Ambjent responded within days and "
     "had concrete removed from the roots. This check covers only the tree-safety statement.",
     "Sans", 7.7, SLATE, cwid - 9 * mm, leading=9.8)

# ---------------------------------------------------------------- what would settle it
sy = top1 - 2 * chh - 1 * gx - 8 * mm
c.setFillColor(GREEN)
c.setFont("Sans-B", 10.5)
c.drawString(M, sy, "WHAT WOULD SETTLE IT")
c.setStrokeColor(SAGE)
c.setLineWidth(0.8)
c.line(M, sy - 2 * mm, W - M, sy - 2 * mm)
c.setStrokeColor(AMBER)
c.setLineWidth(2.4)
c.line(M, sy - 2 * mm, M + 22 * mm, sy - 2 * mm)

asks = [
    "How long the concrete stayed on each planter.",
    "How roots were protected, and that none were cut.",
    "An arborist\u2019s report, plus crown monitoring for several years.",
    "How the sealed planters drain and how the trees will be watered.",
]
col_w = (CW - 6 * mm) / 2
for i, a in enumerate(asks):
    x = M + (i % 2) * (col_w + 6 * mm)
    yy = sy - 8 * mm - (i // 2) * 11 * mm
    c.setStrokeColor(GREEN)
    c.setLineWidth(1)
    c.rect(x, yy - 3.2 * mm, 3.4 * mm, 3.4 * mm, stroke=1, fill=0)
    para(x + 6 * mm, yy + 0.4 * mm, a, "Sans", 8.2, SLATE, col_w - 6 * mm, leading=10.2)

# ---------------------------------------------------------------- footer
fh = 17 * mm
c.setFillColor(GREEN)
c.rect(0, 0, W, fh, stroke=0, fill=1)
c.setFillColor(AMBER)
c.setFont("Sans-B", 7.8)
c.drawString(M, 10.2 * mm, "FULL REPORT, EVIDENCE AND REFERENCES:  github.com/leandergrech/Mizien")
c.setFillColor(LIGHTGREEN)
c.setFont("Sans", 7.2)
c.drawString(M, 5.6 * mm, "Version 1.1  \u00b7  2 October 2026  \u00b7  Prepared from public sources, no site visit  \u00b7  "
                          "Draft pending right of reply from Ambjent Malta and Fondazzjoni Wirt Artna")
c.showPage()
c.save()
print("saved", OUT)
