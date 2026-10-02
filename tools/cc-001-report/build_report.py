import os
HERE = os.path.dirname(os.path.abspath(__file__))
OUTDIR = os.path.join(HERE, "out")
os.makedirs(OUTDIR, exist_ok=True)
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Table,
                                TableStyle, Image, PageBreak, KeepTogether, Flowable,
                                NextPageTemplate, CondPageBreak)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import stringWidth

FD = "/usr/share/fonts/truetype/liberation/"
pdfmetrics.registerFont(TTFont("Serif", FD + "LiberationSerif-Regular.ttf"))
pdfmetrics.registerFont(TTFont("Serif-B", FD + "LiberationSerif-Bold.ttf"))
pdfmetrics.registerFont(TTFont("Serif-I", FD + "LiberationSerif-Italic.ttf"))
pdfmetrics.registerFont(TTFont("Serif-BI", FD + "LiberationSerif-BoldItalic.ttf"))
pdfmetrics.registerFont(TTFont("Sans", FD + "LiberationSans-Regular.ttf"))
pdfmetrics.registerFont(TTFont("Sans-B", FD + "LiberationSans-Bold.ttf"))
pdfmetrics.registerFont(TTFont("Sans-I", FD + "LiberationSans-Italic.ttf"))
pdfmetrics.registerFont(TTFont("Sans-BI", FD + "LiberationSans-BoldItalic.ttf"))
pdfmetrics.registerFont(TTFont("DejaVu", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"))
pdfmetrics.registerFontFamily("Serif", normal="Serif", bold="Serif-B", italic="Serif-I", boldItalic="Serif-BI")
pdfmetrics.registerFontFamily("Sans", normal="Sans", bold="Sans-B", italic="Sans-I", boldItalic="Sans-BI")

# ------------------------------------------------------------------ palette
GREEN = colors.HexColor("#14452F")
SAGE = colors.HexColor("#7FA88B")
PALE = colors.HexColor("#E6EFE8")
AMBER = colors.HexColor("#E3A72F")
AMBER_PALE = colors.HexColor("#FBF1D9")
RED = colors.HexColor("#B5483A")
RED_PALE = colors.HexColor("#F7E4E0")
SLATE = colors.HexColor("#2B3A42")
GREY = colors.HexColor("#8A9399")
GREY_PALE = colors.HexColor("#EEF0F1")
CREAM = colors.HexColor("#F6F4EE")
ORANGE = colors.HexColor("#D9772B")
BLUE = colors.HexColor("#3C6E8F")
BLUE_PALE = colors.HexColor("#E3EDF3")

PW, PH = A4
LM = RM = 20 * mm
TM = 24 * mm
BM = 20 * mm
CW = PW - LM - RM  # content width

OUT = os.path.join(OUTDIR, "report.pdf")
FIG = OUTDIR + os.sep

# ------------------------------------------------------------------ styles
body = ParagraphStyle("body", fontName="Serif", fontSize=10.2, leading=14.6, textColor=SLATE,
                      spaceAfter=6, alignment=TA_LEFT)
lead = ParagraphStyle("lead", parent=body, fontSize=11.4, leading=16.4, textColor=GREEN)
small = ParagraphStyle("small", parent=body, fontName="Sans", fontSize=8.2, leading=11.2, spaceAfter=0)
cap = ParagraphStyle("cap", parent=small, fontName="Sans-I", textColor=GREY, spaceBefore=3, spaceAfter=10)
h2 = ParagraphStyle("h2", fontName="Sans-B", fontSize=11.5, leading=15, textColor=GREEN, spaceBefore=8, spaceAfter=4)
h3 = ParagraphStyle("h3", fontName="Sans-B", fontSize=9.2, leading=12, textColor=SLATE, spaceBefore=4, spaceAfter=2)
cell = ParagraphStyle("cell", fontName="Sans", fontSize=8.1, leading=10.8, textColor=SLATE)
cellb = ParagraphStyle("cellb", parent=cell, fontName="Sans-B")
cellh = ParagraphStyle("cellh", parent=cell, fontName="Sans-B", textColor=colors.white, fontSize=7.8)
tag = ParagraphStyle("tag", fontName="Sans-B", fontSize=7.2, leading=9, textColor=GREEN, spaceAfter=2)
ref = ParagraphStyle("ref", fontName="Sans", fontSize=8, leading=11, textColor=SLATE, leftIndent=16,
                     firstLineIndent=-16, spaceAfter=3.2)
bul = ParagraphStyle("bul", parent=body, leftIndent=12, firstLineIndent=-9, spaceAfter=3)


DIAM = '<font name="DejaVu" size="6.5">\u25c6</font>'


def P(t, s=body):
    return Paragraph(t.replace("\u25c6", DIAM), s)


def C(t, s=cell):
    return Paragraph(t.replace("\u25c6", DIAM), s)


# ------------------------------------------------------------------ flowables
class SectionHeading(Flowable):
    def __init__(self, num, title, width=CW):
        super().__init__()
        self.num, self.title, self.width = num, title, width
        self.keepWithNext = True
        self.toc = f"{num}  {title}" if num else title

    def wrap(self, aw, ah):
        return self.width, 15 * mm

    def draw(self):
        c = self.canv
        y = 6 * mm
        if self.num:
            c.setFillColor(GREEN)
            c.circle(5 * mm, y + 1.5 * mm, 4.6 * mm, stroke=0, fill=1)
            c.setFillColor(colors.white)
            c.setFont("Sans-B", 11.5)
            c.drawCentredString(5 * mm, y + 0.0 * mm, str(self.num))
            x0 = 13 * mm
        else:
            x0 = 0
        c.setFillColor(GREEN)
        c.setFont("Sans-B", 17)
        c.drawString(x0, y - 0.3 * mm, self.title)
        c.setStrokeColor(SAGE)
        c.setLineWidth(1)
        c.line(0, 0.8 * mm, self.width, 0.8 * mm)
        c.setStrokeColor(AMBER)
        c.setLineWidth(2.6)
        c.line(0, 0.8 * mm, 26 * mm, 0.8 * mm)


class VerdictMeter(Flowable):
    def __init__(self, width=CW, active=2):
        super().__init__()
        self.width, self.active = width, active

    def wrap(self, aw, ah):
        return self.width, 25 * mm

    def draw(self):
        c = self.canv
        labels = [("SUPPORTED", ""), ("LARGELY", "SUPPORTED"), ("NOT", "SUBSTANTIATED"),
                  ("MISLEADING", ""), ("CONTRADICTED", "")]
        cols = [colors.HexColor("#2E7D4F"), colors.HexColor("#8DB36B"), ORANGE,
                colors.HexColor("#C85A3A"), colors.HexColor("#8E2F25")]
        gap = 1.6 * mm
        sw = (self.width - 4 * gap) / 5
        y = 2 * mm
        h = 11 * mm
        for i, (l1, l2) in enumerate(labels):
            x = i * (sw + gap)
            c.setFillColor(cols[i])
            if i == self.active:
                c.roundRect(x - 0.6 * mm, y - 0.8 * mm, sw + 1.2 * mm, h + 1.6 * mm, 2 * mm, stroke=0, fill=1)
                c.setStrokeColor(SLATE)
                c.setLineWidth(1.6)
                c.roundRect(x - 0.6 * mm, y - 0.8 * mm, sw + 1.2 * mm, h + 1.6 * mm, 2 * mm, stroke=1, fill=0)
            else:
                c.roundRect(x, y, sw, h, 2 * mm, stroke=0, fill=1)
            c.setFillColor(colors.white)
            fs = 6.6 if i == self.active else 6.4
            c.setFont("Sans-B", fs)
            if l2:
                c.drawCentredString(x + sw / 2, y + h / 2 + 0.9 * mm, l1)
                c.drawCentredString(x + sw / 2, y + h / 2 - 2.3 * mm, l2)
            else:
                c.drawCentredString(x + sw / 2, y + h / 2 - 1 * mm, l1)
        # marker
        mx = self.active * (sw + gap) + sw / 2
        c.setFillColor(SLATE)
        p = c.beginPath()
        p.moveTo(mx - 2.2 * mm, y + h + 4.6 * mm)
        p.lineTo(mx + 2.2 * mm, y + h + 4.6 * mm)
        p.lineTo(mx, y + h + 1.6 * mm)
        p.close()
        c.drawPath(p, stroke=0, fill=1)
        c.setFont("Sans-B", 7)
        c.drawCentredString(mx, y + h + 6.2 * mm, "THIS CLAIM")


def callout(paras, bg=PALE, bar=GREEN, pad=7, width=CW):
    t = Table([[paras]], colWidths=[width])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), bg),
        ("LINEBEFORE", (0, 0), (0, -1), 3.2, bar),
        ("LEFTPADDING", (0, 0), (-1, -1), pad + 3),
        ("RIGHTPADDING", (0, 0), (-1, -1), pad),
        ("TOPPADDING", (0, 0), (-1, -1), pad - 1),
        ("BOTTOMPADDING", (0, 0), (-1, -1), pad - 1),
    ]))
    return t


def chip(text, bg, fg=colors.white, w=34 * mm):
    t = Table([[Paragraph(f'<font color="{fg.hexval().replace("0x", "#")}">{text}</font>',
                          ParagraphStyle("chip", fontName="Sans-B", fontSize=7, leading=8.6, alignment=TA_CENTER))]],
              colWidths=[w])
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), bg),
                           ("TOPPADDING", (0, 0), (-1, -1), 3), ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
                           ("LEFTPADDING", (0, 0), (-1, -1), 3), ("RIGHTPADDING", (0, 0), (-1, -1), 3),
                           ("ROUNDEDCORNERS", [3, 3, 3, 3])]))
    return t


def fig(path, width=CW):
    from PIL import Image as PI
    w, h = PI.open(path).size
    return Image(path, width=width, height=width * h / w)


# ------------------------------------------------------------------ page decorations
def draw_cover(c, doc):
    c.saveState()
    c.setFillColor(GREEN)
    c.rect(0, 0, PW, PH, stroke=0, fill=1)
    # tree rings
    c.setStrokeColor(SAGE)
    cx, cy = PW * 0.80, PH * 0.20
    for i in range(1, 22):
        c.setStrokeAlpha(0.10 + (0.06 if i % 4 == 0 else 0))
        c.setLineWidth(1.2 if i % 4 == 0 else 0.7)
        c.ellipse(cx - i * 9.5 * mm + (i % 3) * 0.6 * mm, cy - i * 9.0 * mm,
                  cx + i * 9.5 * mm, cy + i * 9.6 * mm)
    c.setStrokeAlpha(1)
    # amber stripe
    c.setFillColor(AMBER)
    c.rect(LM, PH - 31 * mm, 14 * mm, 1.6 * mm, stroke=0, fill=1)
    c.setFillColor(AMBER)
    c.setFont("Sans-B", 9)
    c.drawString(LM, PH - 38 * mm, "MI\u017bIEN")
    c.setFillColor(colors.HexColor("#BFD6C5"))
    c.setFont("Sans", 9)
    c.drawString(LM + 19 * mm, PH - 38 * mm, "Claim Check 001  \u00b7  Literature review")

    # title
    c.setFillColor(colors.white)
    c.setFont("Serif-B", 37)
    for i, line in enumerate(["Does a concrete", "layer harm", "established trees?"]):
        c.drawString(LM, PH - 70 * mm - i * 15.5 * mm, line)
    c.setFillColor(colors.HexColor("#CFE2D4"))
    c.setFont("Serif-I", 13.5)
    c.drawString(LM, PH - 121 * mm, "Testing a public claim about the Upper Barrakka Gardens, Valletta,")
    c.drawString(LM, PH - 127 * mm, "against the scientific literature")

    # claim card
    y0 = 78 * mm
    c.setFillColor(CREAM)
    c.roundRect(LM, y0, CW, 52 * mm, 3 * mm, stroke=0, fill=1)
    c.setFillColor(AMBER)
    c.rect(LM, y0, 2.6 * mm, 52 * mm, stroke=0, fill=1)
    c.setFillColor(GREY)
    c.setFont("Sans-B", 7.6)
    c.drawString(LM + 9 * mm, y0 + 44 * mm, "THE CLAIM UNDER REVIEW")
    c.setFillColor(GREEN)
    c.setFont("Serif-BI", 16.5)
    c.drawString(LM + 9 * mm, y0 + 34 * mm, "\u201cGiven its temporary nature, it will not")
    c.drawString(LM + 9 * mm, y0 + 27 * mm, "cause damage to the tree.\u201d")
    c.setFillColor(SLATE)
    c.setFont("Sans", 8.2)
    c.drawString(LM + 9 * mm, y0 + 19.5 * mm, "Ambjent Malta, to the Times of Malta, 1 October 2026, on concrete placed in tree planters.")
    c.drawString(LM + 9 * mm, y0 + 15.3 * mm, "Context: waterproofing planters to stop water entering the Lascaris War Rooms tunnels.")

    # verdict pill
    c.setFillColor(ORANGE)
    c.roundRect(LM + 9 * mm, y0 + 4.2 * mm, 62 * mm, 7.6 * mm, 3.8 * mm, stroke=0, fill=1)
    c.setFillColor(colors.white)
    c.setFont("Sans-B", 9)
    c.drawCentredString(LM + 9 * mm + 31 * mm, y0 + 6.7 * mm, "VERDICT:  NOT SUBSTANTIATED")
    c.setFillColor(SLATE)
    c.setFont("Sans-I", 8.2)
    c.drawString(LM + 76 * mm, y0 + 6.8 * mm, "Plausible, but no evidence published")

    # footer
    c.setFillColor(colors.HexColor("#BFD6C5"))
    c.setFont("Sans", 8.4)
    c.drawString(LM, 36 * mm, "Version 1.1  \u00b7  2 October 2026  \u00b7  revised after reading the full Times of Malta article")
    c.drawString(LM, 31.5 * mm, "Status: draft for right of reply (Ambjent Malta, Fondazzjoni Wirt Artna)")
    c.drawString(LM, 27 * mm, "Prepared from public sources. No site visit or tree assessment was carried out.")
    c.drawString(LM, 22.5 * mm, "Repository: github.com/leandergrech/Mizien")
    c.restoreState()


def draw_body(c, doc):
    c.saveState()
    c.setStrokeColor(SAGE)
    c.setLineWidth(0.6)
    c.line(LM, PH - 15 * mm, PW - RM, PH - 15 * mm)
    c.setFillColor(GREEN)
    c.setFont("Sans-B", 7.2)
    c.drawString(LM, PH - 12.2 * mm, "MI\u017bIEN  \u00b7  CLAIM CHECK 001")
    c.setFillColor(GREY)
    c.setFont("Sans", 7.2)
    c.drawRightString(PW - RM, PH - 12.2 * mm, "Concrete and established trees \u2013 Upper Barrakka Gardens")
    c.setStrokeColor(colors.HexColor("#D5DBD7"))
    c.line(LM, 14 * mm, PW - RM, 14 * mm)
    c.setFillColor(GREY)
    c.setFont("Sans", 7.2)
    c.drawString(LM, 9.6 * mm, "v1.1 draft  \u00b7  2 October 2026")
    c.setFillColor(GREEN)
    c.setFont("Sans-B", 8)
    c.drawRightString(PW - RM, 9.6 * mm, f"{doc.page}")
    c.restoreState()


class Doc(BaseDocTemplate):
    def afterFlowable(self, fl):
        if isinstance(fl, SectionHeading):
            key = f"s{id(fl)}"
            self.canv.bookmarkPage(key)
            self.canv.addOutlineEntry(fl.toc, key, level=0, closed=False)


doc = Doc(OUT, pagesize=A4, leftMargin=LM, rightMargin=RM, topMargin=TM, bottomMargin=BM,
          title="Does a concrete layer harm established trees? Claim Check 001",
          author="Mi\u017bien",
          subject="Literature review testing Ambjent Malta's claim that temporary concrete will not damage Upper Barrakka trees")
cover_frame = Frame(LM, BM, CW, 20, id="cf", leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
body_frame = Frame(LM, BM, CW, PH - TM - BM + 4 * mm, id="bf", leftPadding=0, rightPadding=0,
                   topPadding=0, bottomPadding=0)
doc.addPageTemplates([PageTemplate("cover", [cover_frame], onPage=draw_cover),
                      PageTemplate("body", [body_frame], onPage=draw_body)])

S = []
S += [Spacer(1, 1), NextPageTemplate("body"), PageBreak()]

# ================================================================== TL;DR
S.append(SectionHeading(None, "TL;DR"))
S.append(Spacer(1, 1 * mm))
S.append(P("Ambjent Malta told the Times of Malta that concrete placed in the tree planters at Upper Barrakka will "
           "not damage the trees <b>because it is temporary</b>: it stays only until a waterproofing membrane is "
           "installed. Ambjent also said prolonged cover would be a concern, and that concrete lying directly on "
           "the roots has since been removed. The works protect the historic Lascaris War Rooms from water ingress. "
           "That aim is legitimate and is not questioned here. <b>The question is whether the tree-safety "
           "statement is backed by evidence.</b>", lead))

kp = [
    ("The claim is conditional, and its logic points the right way.",
     "Ambjent itself says prolonged cover would be a problem, for reasons (less water, bark and nutrient "
     "transport, decay) that match the research on sealed soils."),
    ("But \u201ctemporary\u201d is undefined, and the claim covers only the concrete.",
     "No duration is given. The article also reports that soil was removed from the planter and that concrete "
     "lay around the roots. Root exposure, contact with fresh concrete and how it was removed are not addressed."),
    ("No evidence has been published.",
     "No species, tree ages, dates, arborist report or monitoring data. The \u201cfive planters, no tree "
     "died\u201d statement is anecdote, and decline often takes 3\u20135+ years to show."),
    ("The science: mixed for permanent sealing, silent on temporary cover.",
     "Studies of permanent sealing range from no harm in a five-year trial to clear harm in holm oak. We found "
     "<i>no</i> study of short-term concrete contact with roots."),
    ("Verdict: not substantiated.",
     "Plausible for a short, well-managed cover, but not shown for these trees. Ambjent responded quickly and "
     "was candid about the risk."),
]
rows = []
for i, (a, b) in enumerate(kp, 1):
    n = Table([[Paragraph(f'<font color="white">{i}</font>',
                          ParagraphStyle("n", fontName="Sans-B", fontSize=10, alignment=TA_CENTER))]],
              colWidths=[6.5 * mm], rowHeights=[6.5 * mm])
    n.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), GREEN), ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                           ("ROUNDEDCORNERS", [3.2, 3.2, 3.2, 3.2]), ("LEFTPADDING", (0, 0), (-1, -1), 0),
                           ("RIGHTPADDING", (0, 0), (-1, -1), 0), ("TOPPADDING", (0, 0), (-1, -1), 0),
                           ("BOTTOMPADDING", (0, 0), (-1, -1), 0)]))
    rows.append([n, Paragraph(f"<b>{a}</b> {b}", ParagraphStyle("kp", parent=body, fontSize=9.6, leading=13.0,
                                                              spaceAfter=0))])
kt = Table(rows, colWidths=[10 * mm, CW - 10 * mm - 20 * mm])
kt.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"), ("TOPPADDING", (0, 0), (-1, -1), 2.8),
                        ("BOTTOMPADDING", (0, 0), (-1, -1), 2.8), ("LEFTPADDING", (0, 0), (-1, -1), 0)]))
S.append(callout([kt], bg=PALE, bar=GREEN, pad=8))
S.append(Spacer(1, 4 * mm))
S.append(VerdictMeter(CW, active=2))
S.append(Spacer(1, 3 * mm))

big = ParagraphStyle("big", fontName="Sans-B", fontSize=19, leading=22, textColor=GREEN)
bigr = ParagraphStyle("bigr", parent=big, textColor=RED)
bigo = ParagraphStyle("bigo", parent=big, textColor=ORANGE)
tcap = ParagraphStyle("tcap", fontName="Sans", fontSize=7.4, leading=9.6, textColor=SLATE)
tiles = [
    [Paragraph("Undefined", bigo), Paragraph("3\u20135+ yrs", bigr), Paragraph("None found", bigr),
     Paragraph("28", big)],
    [Paragraph("How long \u201ctemporary\u201d lasts: no duration published", tcap),
     Paragraph("Typical delay before construction damage shows in the crown", tcap),
     Paragraph("Studies of short-term concrete contact with roots; published arborist data", tcap),
     Paragraph("Water-infiltration points the works are meant to fix", tcap)],
]
tt = Table(tiles, colWidths=[CW / 4] * 4)
tt.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), CREAM), ("LINEAFTER", (0, 0), (-2, -1), 1.2, colors.white),
                        ("LEFTPADDING", (0, 0), (-1, -1), 8), ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                        ("TOPPADDING", (0, 0), (-1, 0), 7), ("BOTTOMPADDING", (0, 0), (-1, 0), 1),
                        ("TOPPADDING", (0, 1), (-1, 1), 0), ("BOTTOMPADDING", (0, 1), (-1, 1), 7),
                        ("VALIGN", (0, 0), (-1, -1), "TOP")]))
S.append(tt)
S.append(Spacer(1, 4 * mm))

wc = Table([[
    [P("WHAT WOULD MOVE THE VERDICT UP", tag),
     P("A stated, short duration with dates; roots shown to have been kept covered and moist and not cut; "
       "clean removal of the concrete; arborist inspection before and after; a membrane design that drains; "
       "monitoring of crown health for several years.", small)],
    [P('<font color="#B5483A">WHAT WOULD MOVE IT DOWN</font>', tag),
     P("Concrete in contact with roots or bark for days or weeks; roots left exposed in hot, dry weather or "
       "cut; bark damaged on removal; sealed planters that waterlog; monitoring data withheld or never "
       "collected.", small)],
]], colWidths=[CW / 2, CW / 2], hAlign="LEFT")
wc.setStyle(TableStyle([("BACKGROUND", (0, 0), (0, 0), PALE), ("BACKGROUND", (1, 0), (1, 0), RED_PALE),
                        ("LEFTPADDING", (0, 0), (-1, -1), 8), ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                        ("TOPPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
                        ("VALIGN", (0, 0), (-1, -1), "TOP")]))
S.append(wc)
S.append(Spacer(1, 5 * mm))
toc_items = [("1", "The claim and what we could verify"), ("2", "Method and how to read this report"),
             ("3", "How concrete could harm a tree"), ("4", "What the studies found"),
             ("5", "Where the science disagrees"), ("6", "Testing the claim at Upper Barrakka"),
             ("7", "Verdict and requests for evidence"), ("8", "Limitations")]
tp = ParagraphStyle("toc", fontName="Sans", fontSize=8.6, leading=12, textColor=SLATE)
cells = [[Paragraph(f'<font name="Sans-B" color="#14452F">{n}</font>&nbsp;&nbsp;{t}', tp)] for n, t in toc_items]
half = len(cells) // 2
toc = Table([[cells[i][0], cells[i + half][0]] for i in range(half)], colWidths=[CW / 2, CW / 2])
toc.setStyle(TableStyle([("TOPPADDING", (0, 0), (-1, -1), 2.2), ("BOTTOMPADDING", (0, 0), (-1, -1), 2.2),
                         ("LEFTPADDING", (0, 0), (-1, -1), 0), ("LINEBELOW", (0, 0), (-1, -1), 0.3,
                                                                  colors.HexColor("#D5DBD7"))]))
S.append(P("IN THIS REPORT", tag))
S.append(toc)
S.append(PageBreak())

# ================================================================== 1 THE CLAIM
S.append(SectionHeading(1, "The claim and what we could verify"))
S.append(P("The claim comes from a Times of Malta article by Nicole Meilak (1 October 2026), read in full. Its "
           "headline says the concrete layer will not damage the trees. <b>Ambjent Malta\u2019s own words are "
           "narrower</b>: the concrete is temporary, so it will not cause damage, and prolonged cover would be a "
           "concern. We treat Ambjent\u2019s wording as the claim and the headline as the paper\u2019s summary of "
           "it. Statements from Fondazzjoni Wirt Artna (FWA), which runs the tunnels, are labelled as FWA\u2019s."))

src_rows = [
    [C("Source", cellh), C("What it says", cellh), C("Our access", cellh), C("Status", cellh)],
    [C("<b>Times of Malta</b>, 1 Oct 2026 [3]"),
     C("Concrete laid at the bottom of tree planters; soil removed from at least one planter. Ambjent: the "
       "concrete is temporary, remaining only until a waterproofing membrane is installed, so it will not damage "
       "the tree; harm could arise if left prolonged. Concrete directly on the roots has since been removed "
       "(photo caption). No duration given."),
     C("Read in full (supplied PDF)."), C("<b>The claim itself</b>")],
    [C("<b>Same article</b>, quoting FWA"),
     C("Severe flooding of the war rooms from storm and irrigation water leaking from the gardens. Ambjent made "
       "every effort to save existing trees, especially old ones. Every leak point addressed."),
     C("Read in full."), C("Partner body\u2019s statement")],
    [C("<b>Newsbook</b>, 1 Oct 2026, reporting FWA [1]"),
     C("Waterproofing includes \u201ctanking\u201d of planters. 28 water-infiltration points addressed. Five "
       "planters treated so far with no tree dying or removed."),
     C("Search excerpt only; page blocks automated access."), C("Partner body\u2019s statement")],
    [C("<b>MaltaToday</b>, c. Dec 2025, quoting FWA\u2019s executive chairman [2]"),
     C("Waterproofing membrane under the concrete; mulch on top; large pots of flowers and plants; trunks "
       "and crowns untouched."),
     C("Read in full."), C("Earlier phase of works")],
]
st = Table(src_rows, colWidths=[36 * mm, 76 * mm, 36 * mm, 22 * mm], repeatRows=1)
st.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), GREEN), ("VALIGN", (0, 0), (-1, -1), "TOP"),
                        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, CREAM]),
                        ("LINEBELOW", (0, 0), (-1, -1), 0.4, colors.HexColor("#D5DBD7")),
                        ("TOPPADDING", (0, 0), (-1, -1), 5), ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                        ("LEFTPADDING", (0, 0), (-1, -1), 6), ("RIGHTPADDING", (0, 0), (-1, -1), 6)]))
S.append(st)
S.append(Spacer(1, 4 * mm))
S.append(callout([P("FAIRNESS NOTE", tag),
                  P("The seepage problem is real and serious: storm and irrigation water entered a complex whose "
                    "parts date to 1570, 1640 and 1715, and FWA says some areas are permanently lost. Sealing "
                    "planters is a recognised way to stop leaks. Ambjent responded within days, stated the "
                    "tree risk plainly and had concrete removed from the roots. This is a trade-off between two "
                    "goods. The issue examined here is narrower: <b>whether the statement that the trees will not "
                    "be harmed is supported by evidence.</b>", small)],
                 bg=AMBER_PALE, bar=AMBER))
S.append(Spacer(1, 4 * mm))

# ================================================================== 2 METHOD
S.append(SectionHeading(2, "Method and how to read this report"))
S.append(P("<b>Question.</b> Does pouring concrete over or near the roots of an established tree harm it, and "
           "does the research support Ambjent Malta\u2019s position that a <i>temporary</i> layer will not?"))
S.append(P("<b>Evidence.</b> Targeted searches of peer-reviewed literature and credible grey literature (university "
           "extension services, park services, arboricultural reviews), run in October 2026. We favoured studies on "
           "<i>established</i> trees with a control. Few studies address poured concrete specifically, so most "
           "evidence comes from pavements and soil sealing generally, and we found none on short-term, temporary cover."))
S.append(P("<b>Evidence grades</b> used in the tables:"))
grades = [
    [C("A", cellb), C("Controlled or randomised experiment on trees"), C("B", cellb),
     C("Observational field study with a control or gradient")],
    [C("C", cellb), C("Review or professional guidance"), C("D", cellb), C("Assertion or anecdote with no data")],
]
gt = Table(grades, colWidths=[8 * mm, CW / 2 - 8 * mm, 8 * mm, CW / 2 - 8 * mm])
gt.setStyle(TableStyle([("BACKGROUND", (0, 0), (0, 0), colors.HexColor("#CFE5D5")),
                        ("BACKGROUND", (2, 0), (2, 0), BLUE_PALE), ("BACKGROUND", (0, 1), (0, 1), AMBER_PALE),
                        ("BACKGROUND", (2, 1), (2, 1), RED_PALE), ("ALIGN", (0, 0), (0, -1), "CENTER"),
                        ("ALIGN", (2, 0), (2, -1), "CENTER"), ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                        ("LINEBELOW", (0, 0), (-1, -1), 0.4, colors.white),
                        ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4)]))
S.append(gt)
S.append(Spacer(1, 2 * mm))
S.append(P("<b>Verdicts</b> follow a five-point scale defined in Appendix A. Differing scientific views are shown "
           "side by side in Section 5 rather than averaged away. Where the science has not settled, we say so "
           "instead of choosing a side."))

# ================================================================== 3 MECHANISMS
S.append(CondPageBreak(120 * mm))
S.append(SectionHeading(3, "How concrete could harm a tree"))
S.append(P("Concrete can affect an established tree in three largely separate ways. The literature treats them "
           "very differently, and it is easy to conflate them."))
S.append(P("<b>1. During the works.</b> Digging, regrading and compaction cut or crush roots, and any root left "
           "exposed can dry out quickly, especially in hot or windy weather. Guidance is to avoid hot, dry conditions "
           "and to cover exposed roots with soil, mulch or damp burlap as soon as possible [13, 17]. Park-service and "
           "extension guidance names compaction and root severance as the commonest causes of construction-related "
           "decline, with symptoms sometimes taking years to appear [12, 13].", bul))
S.append(P("<b>2. After the works: soil sealing.</b> A sealed surface reduces rain and irrigation reaching the soil and "
           "slows gas exchange with the air. Sealed soils can run warmer; roots can be killed above roughly 40\u00b0C "
           "[11]. Reported consequences include lower soil oxygen, higher CO<sub>2</sub> and fewer fine roots [4, 5].", bul))
S.append(P("<b>3. At the trunk and in the chemistry.</b> Fresh cement-based material leaches strongly alkaline water for "
           "a time [14, 15]. Industry guidance also cautions against burying the root flare [18]. We found no controlled "
           "study of concrete placed against roots or trunks, temporary or permanent. <b>Duration is the unknown:</b> "
           "the sealing studies measure months to years.", bul))
S.append(Spacer(1, 2 * mm))
S.append(fig(FIG + "fig1_mechanism.png"))
S.append(P("Figure 1. Pathways by which concrete works could harm an established tree. Which pathways operate, and how "
           "strongly, depends on species, age, the fraction of the root zone sealed, distance from the trunk, soil "
           "and water supply.", cap))
S.append(callout([P("WHY OXYGEN MATTERS", tag),
                  P("Roots generally perform best above about 10% soil oxygen. Estimated minimum thresholds are "
                    "roughly 3% for root survival and 5\u201310% for growth [16]. Soil under impervious concrete "
                    "had lower oxygen than under pervious concrete or bare soil, especially when wet [4].", small)],
                 bg=BLUE_PALE, bar=BLUE))

# ================================================================== 4 STUDIES
S.append(PageBreak())
S.append(SectionHeading(4, "What the studies found"))
S.append(P("Figure 2 places each source on a qualitative scale from \u201cadverse effect reported\u201d to \u201cno adverse "
           "effect detected\u201d. <b>Placement is our judgement of each source\u2019s headline finding. It is not a "
           "statistical meta-analysis.</b> Diamonds mark sources we know only through another paper\u2019s "
           "summary."))
S.append(fig(FIG + "fig2_evidence_map.png"))
S.append(P("Figure 2. Evidence map. Fini et al. found root morphology altered by pavements but no drought stress or "
           "above-ground growth penalty; Hauer et al. found only a small mortality rise for works at distance.", cap))

Gtag = lambda g, bg: Table([[Paragraph(f'<font color="#2B3A42">{g}</font>',
                                       ParagraphStyle("g", fontName="Sans-B", fontSize=8, alignment=TA_CENTER))]],
                           colWidths=[6 * mm], style=TableStyle([("BACKGROUND", (0, 0), (-1, -1), bg),
                                                                 ("TOPPADDING", (0, 0), (-1, -1), 1),
                                                                 ("BOTTOMPADDING", (0, 0), (-1, -1), 1),
                                                                 ("LEFTPADDING", (0, 0), (-1, -1), 0),
                                                                 ("RIGHTPADDING", (0, 0), (-1, -1), 0)]))
gA, gB, gC = colors.HexColor("#CFE5D5"), BLUE_PALE, AMBER_PALE


def study_cell(name, g, bg, extra=""):
    return [C(f"<b>{name}</b>{extra}"), Spacer(1, 2), Gtag(g, bg)]


ev = [
    [C("Source", cellh), C("Design and trees", cellh), C("Key finding", cellh), C("Reading", cellh)],
    [study_cell("Viswanathan et al. 2011 [4]", "A", gA),
     C("Field experiment: concrete installed over <b>pre-existing mature</b> sweetgum on clay."),
     C("Lower soil oxygen under impervious concrete (esp. wet), higher CO<sub>2</sub>; far less fine-root length than "
       "unpaved controls. Pervious concrete did not help on low-permeability clay."),
     C("<b>Adverse</b> (roots)")],
    [study_cell("Fini et al. 2022 [5]", "A", gA),
     C("5-year randomised trial, 48 trees in 1 m\u00b2 pits (planted 2012); <i>Celtis australis</i>, <i>Fraxinus ornus</i>; "
       "wetter temperate site."),
     C("No evidence of drought stress or above-ground growth loss. Impermeable surfaces cut soil moisture, "
       "especially winter\u2013spring. Root morphology altered, likely via CO<sub>2</sub>."),
     C("<b>No above-ground effect</b>; roots altered")],
    [study_cell("Savi et al. 2015 [6]", "B", gB),
     C("Four urban sites with different impervious cover; <b>holm oak</b> (<i>Quercus ilex</i>), Trieste, Italy."),
     C("More impervious cover: greater drought stress, reduced leaf gas exchange, more xylem cavitation."),
     C("<b>Adverse</b> (Mediterranean species)")],
    [study_cell("Cui et al. 2022 [7]", "B", gB),
     C("40 paired paved/vegetated sites in Beijing; <i>Ginkgo biloba</i>, <i>Platanus orientalis</i>."),
     C("Growth increments lower on paved land: ginkgo \u221244.5% diameter, \u221231.9% height; plane \u221231.7% and "
       "\u221260.1%."),
     C("<b>Adverse</b>")],
    [study_cell("Volder et al. 2009 [8] \u25c6", "B", gB),
     C("Field study, 15\u201318-year-old sweetgum (as reported in [5])."),
     C("Leaf gas exchange, fluorescence and water relations did not differ between paved and unpaved."),
     C("<b>No effect detected</b>")],
    [study_cell("Hauer et al. 1994 [10] \u25c6", "B", gB),
     C("Street trees near construction (as summarised in [9])."),
     C("Works at 5\u20137 trunk diameters from the tree: about +4% mortality, \u22125% condition rating."),
     C("<b>Small effect</b> at distance")],
    [study_cell("North et al. 2015 \u25c6", "B", gB),
     C("Cited in a TreeNet summary [11]."),
     C("Tree health and condition fall as the pavement edge nears the trunk."),
     C("<b>Adverse</b> with proximity")],
    [study_cell("Arboric. & Urban For. review 2014 [9]", "C", gC),
     C("Review of root-management strategies."),
     C("Pavement effects on the root environment are mixed. Soil moisture can be higher under pavement. Benefits "
       "of pervious paving not consistently shown."),
     C("<b>Mixed</b>")],
    [study_cell("NPS / extension guidance [12, 13]", "C", gC),
     C("Professional guidance, no new data."),
     C("Construction damage may take 3\u20135+ years to show. Rule of thumb: ~20% root loss tolerated, ~40% likely fatal."),
     C("<b>Context</b>")],
    [study_cell("Wirt Artna via Newsbook [1]", "D", RED_PALE),
     C("Five treated planters; species, ages and dates not stated."),
     C("No tree has died or been removed."),
     C("<b>Anecdote</b>")],
]
et = Table(ev, colWidths=[34 * mm, 44 * mm, 58 * mm, 34 * mm], repeatRows=1)
rowbg = []
for i, col in enumerate([RED_PALE, PALE, RED_PALE, RED_PALE, PALE, AMBER_PALE, RED_PALE, AMBER_PALE, GREY_PALE,
                         GREY_PALE], start=1):
    rowbg.append(("BACKGROUND", (3, i), (3, i), col))
et.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), GREEN), ("VALIGN", (0, 0), (-1, -1), "TOP"),
                        ("LINEBELOW", (0, 0), (-1, -1), 0.4, colors.HexColor("#D5DBD7")),
                        ("TOPPADDING", (0, 0), (-1, -1), 4.5), ("BOTTOMPADDING", (0, 0), (-1, -1), 4.5),
                        ("LEFTPADDING", (0, 0), (-1, -1), 5), ("RIGHTPADDING", (0, 0), (-1, -1), 5)] + rowbg))
S.append(et)
S.append(P("Grades: A controlled experiment \u00b7 B observational \u00b7 C review/guidance \u00b7 D anecdote. "
           "\u25c6 known to us second-hand.", cap))
S.append(P("Reading across the evidence", h2))
S.append(P("\u2022 <b>No study we found tests the Upper Barrakka configuration:</b> concrete over a waterproofing "
           "membrane around older trees in a Mediterranean climate, and none tests a <i>temporary</i> cover.", bul))
S.append(P("\u2022 <b>The closest evidence points the wrong way.</b> Holm oak, the Mediterranean species most studied, "
           "showed greater hydraulic stress where impervious cover was high. That evidence is observational.", bul))
S.append(P("\u2022 <b>The best-controlled evidence is more reassuring but transfers poorly.</b> It concerns relatively "
           "young trees in small pits at a temperate site averaging about 1,100 mm of rain a year, far wetter than "
           "the Maltese Islands.", bul))
S.append(P("\u2022 <b>Roots react more consistently than crowns, and crowns lag.</b> Several studies find altered roots "
           "without an immediate canopy penalty, which is why short monitoring windows can mislead.", bul))

# ================================================================== 5 CONTESTED
S.append(PageBreak())
S.append(SectionHeading(5, "Where the science disagrees"))
S.append(P("Six questions drive the dispute. For each we set out the best evidence on each side, why the findings "
           "may differ, and what that means for Upper Barrakka."))


def contested(title, status, status_col, harm, nohar, why):
    hdr = [Paragraph(f"<b>{title}</b>", ParagraphStyle("ch", fontName="Sans-B", fontSize=9.6, leading=12.4,
                                                     textColor=colors.white)),
           chip(status, status_col, w=40 * mm)]
    rows = [
        hdr,
        [[P("EVIDENCE OF HARM", ParagraphStyle("t1", parent=tag, textColor=RED)), P(harm, cell)],
         [P("EVIDENCE OF LITTLE OR NO HARM", ParagraphStyle("t2", parent=tag, textColor=colors.HexColor("#2E7D4F"))),
          P(nohar, cell)]],
        [[P("WHY THEY MAY DIFFER, AND WHAT IT MEANS FOR UPPER BARRAKKA", ParagraphStyle("t3", parent=tag,
                                                                                         textColor=SLATE)),
          P(why, cell)], ""],
    ]
    t = Table(rows, colWidths=[CW - 40 * mm - 2 * mm, 40 * mm])
    # a 2-col grid for evidence rows needs custom approach: nest
    inner = Table([[rows[1][0], rows[1][1]]], colWidths=[CW / 2, CW / 2])
    inner.setStyle(TableStyle([("BACKGROUND", (0, 0), (0, 0), RED_PALE),
                               ("BACKGROUND", (1, 0), (1, 0), PALE),
                               ("LEFTPADDING", (0, 0), (-1, -1), 8), ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                               ("TOPPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
                               ("VALIGN", (0, 0), (-1, -1), "TOP")]))
    head = Table([hdr], colWidths=[CW - 42 * mm, 42 * mm])
    head.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), GREEN), ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                              ("LEFTPADDING", (0, 0), (0, 0), 8), ("RIGHTPADDING", (-1, 0), (-1, 0), 6),
                              ("TOPPADDING", (0, 0), (-1, -1), 5), ("BOTTOMPADDING", (0, 0), (-1, -1), 5)]))
    foot = Table([[rows[2][0]]], colWidths=[CW])
    foot.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), GREY_PALE),
                              ("LEFTPADDING", (0, 0), (-1, -1), 8), ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                              ("TOPPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 7)]))
    return KeepTogether([head, inner, foot, Spacer(1, 5 * mm)])


S.append(Spacer(1, 2 * mm))
S.append(contested(
    "Q1  Does sealing cause drought stress in established trees?", "UNRESOLVED", ORANGE,
    "Holm oak among more impervious cover showed greater drought stress, reduced gas exchange and more xylem "
    "cavitation [6]. Ginkgo and oriental plane on paved ground grew markedly less than neighbours on vegetated "
    "ground [7].",
    "A five-year randomised trial on established <i>Celtis</i> and <i>Fraxinus</i> found no drought stress or "
    "above-ground growth penalty [5]. Soil moisture can be higher under pavement because evaporation is reduced [9]. "
    "Gas exchange in 15\u201318-year sweetgum was unchanged [8].",
    "Species differ; the Italian trial was in a wetter climate with small pits; the harm studies are observational and "
    "may be confounded. <b>For Barrakka:</b> the holm-oak data are the closest match to Malta\u2019s climate, but nobody "
    "has published tree-level data for these trees."))
S.append(contested(
    "Q2  Does a temporary cover matter?", "EVIDENCE GAP", GREY,
    "Exposed roots can dry out quickly in hot or windy weather [13, 17]. Fresh concrete leachate is strongly "
    "alkaline [14, 15]. Soil oxygen under impervious concrete was lower than under other surfaces, and roots need "
    "oxygen (about 3% is a survival minimum) [4, 16].",
    "No direct evidence. Ambjent\u2019s premise is that harm comes from prolonged cover. The sealing studies "
    "measured effects over months to years [4, 5], which is consistent with duration mattering. <i>That is our "
    "inference, not a tested result.</i>",
    "We found no study of short-term concrete contact with roots, so both sides here are reasoning, not data. "
    "<b>For Barrakka:</b> the outcome depends on how long, in what weather, and whether exposed roots were "
    "protected. None of this is reported."))
S.append(contested(
    "Q3  Does it matter whether the surface is permeable?", "LEANING: LITTLE CONSISTENT BENEFIT", SAGE,
    "Impervious cover blocks infiltration and gas exchange, and permeable paving has been proposed as a "
    "mitigation [5, 9].",
    "Benefits of pervious paving are not consistently shown [9]. Pervious concrete over low-permeability clay did not "
    "improve the root zone of mature trees [4]. Permeable options did not enhance above-ground growth [5].",
    "Narrow pavements may let air and water diffuse in from the edges anyway [9]. <b>For Barrakka:</b> the design is "
    "impervious on purpose, because the membrane exists to stop water reaching the rock below. The real question is "
    "where the trees\u2019 water will come from."))
S.append(contested(
    "Q4  Are mature trees more or less vulnerable than young ones?", "UNRESOLVED", ORANGE,
    "Large established trees transpire more and may deplete soil water if infiltration is blocked. Their root "
    "responses are the least certain [5]. Reported dieback occurred in holm oak and linden older than 20 years [5].",
    "Young trees often establish <i>faster</i> in paved pits, helped by reduced evaporation (e.g. plane trees grew "
    "larger in paved than unpaved soil) [5].",
    "Most experiments use young trees. In-situ studies on old trees carry confounding. <b>For Barrakka:</b> Wirt Artna "
    "describes the trees as older and well established, the least-studied and most uncertain category."))
S.append(contested(
    "Q5  Does concrete alkalinity harm roots?", "PROBABLY MINOR; UNDER-STUDIED", SAGE,
    "Fresh cement-based material leaches very alkaline water: crushed non-carbonated concrete reaches pH 13\u201314 [14], "
    "and early-age concrete raised water pH to about 11 in the lab [15]. High pH can limit nutrient availability.",
    "Soil buffers the effect and clay soils slow the alkaline front [14]. In the Italian trial pavements did not "
    "change soil chemical traits [5]. We found no field study showing alkaline-leachate death of an established tree.",
    "Most evidence is lab-scale or from recycled aggregate. <b>For Barrakka:</b> fresh concrete touching roots, even briefly, is the "
    "least-studied scenario; the Maltese substrate is already calcareous (general knowledge, not reviewed here)."))
S.append(contested(
    "Q6  How much root loss can a tree tolerate?", "HEURISTICS, NOT THRESHOLDS", AMBER,
    "Guidance suggests ~20% root loss is tolerated and ~40% probably fatal [13]. Severing roots over about 5 cm "
    "(2 in) can reduce stability and uptake [12].",
    "Street works at 5\u20137 trunk diameters raised mortality only about 4% [10]. Tolerance depends on species, "
    "health and <i>which</i> roots are lost.",
    "Rules of thumb are not validated thresholds. <b>For Barrakka:</b> excavation depth, distance to trunk and the "
    "share of the root zone under the slab are all unreported. The article reports soil removed from the planter."))

# ================================================================== 6 TESTING
S.append(PageBreak())
S.append(SectionHeading(6, "Testing the claim at Upper Barrakka"))
S.append(P("We split the public statements into checkable sub-claims and rated each against the evidence above."))

verd = lambda t, c: chip(t, c, w=29 * mm)
GREENC = colors.HexColor("#2E7D4F")
sub = [
    [C("Sub-claim", cellh), C("Said by", cellh), C("What the evidence shows", cellh), C("Rating", cellh)],
    [C("<b>A.</b> \u201cGiven its temporary nature, it will not cause damage to the tree\u201d"),
     C("Ambjent Malta (Times of Malta)"),
     C("Plausible in direction, since sealing harm builds with time. But \u201ctemporary\u201d has no stated "
       "duration, no tree-specific assessment is given, and the statement does not address the soil removal or "
       "root exposure the article reports."), verd("NOT SUBSTANTIATED", ORANGE)],
    [C("<b>B.</b> Prolonged cover would be a concern: water, bark, nutrient transport, decay"),
     C("Ambjent Malta"),
     C("Matches mechanisms in the literature (table below). Candid and accurate as far as it goes."),
     verd("CONSISTENT WITH RESEARCH", GREENC)],
    [C("<b>C.</b> Concrete directly on the roots has since been removed"),
     C("Times of Malta / Ambjent"),
     C("The photo and caption show concrete cleared from directly around the trunk, leaving a mound of loose soil "
       "and stone. Root and bark condition after removal is not reported."), verd("PARTLY VERIFIED", AMBER)],
    [C("<b>D.</b> Ambjent made every effort to save old trees"), C("FWA (Times of Malta)"),
     C("No method statement, root-protection plan or arborist report seen."), verd("UNVERIFIED", GREY)],
    [C("<b>E.</b> Five treated planters, no tree has died or been removed"), C("FWA (Newsbook)"),
     C("Death is a late, coarse signal; decline may take 3\u20135+ years. No dates, species or condition data "
       "(Figure 3)."), verd("WEAK EVIDENCE", AMBER)],
    [C("<b>F.</b> Earlier phase: membrane, mulch and pots; trunks and crowns untouched"),
     C("FWA chairman (MaltaToday, c. Dec 2025)"),
     C("The Oct 2026 article reports soil removed from at least one planter, so \u201cuntouched\u201d can only "
       "refer to trunks and crowns. Root condition is not addressed."), verd("UNVERIFIED / AMBIGUOUS", GREY)],
]
sbt = Table(sub, colWidths=[42 * mm, 24 * mm, 68 * mm, 36 * mm], repeatRows=1)
sbt.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), GREEN), ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                         ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, CREAM]),
                         ("LINEBELOW", (0, 0), (-1, -1), 0.4, colors.HexColor("#D5DBD7")),
                         ("TOPPADDING", (0, 0), (-1, -1), 5), ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                         ("LEFTPADDING", (0, 0), (-1, -1), 5), ("RIGHTPADDING", (0, 0), (-1, -1), 5)]))
S.append(sbt)
S.append(Spacer(1, 4 * mm))
S.append(callout([P("HEADLINE VERSUS STATEMENT", tag),
                  P("The headline states the point without condition. Ambjent Malta\u2019s own words are conditional "
                    "on the concrete being temporary and acknowledge a risk if it stays. This report assesses the "
                    "conditional statement. A reader who sees only the headline gets a stronger reassurance than "
                    "Ambjent actually gave.", small)],
                 bg=BLUE_PALE, bar=BLUE))
S.append(Spacer(1, 3 * mm))

S.append(P("Ambjent Malta\u2019s reasoning, checked", h2))
rz = [
    [C("Ambjent\u2019s stated concern", cellh), C("What the research says", cellh), C("Match", cellh)],
    [C("Could restrict water availability around the trunk"),
     C("Sealed surfaces reduce infiltration and soil moisture in several studies [4, 5]. Effect on established-tree "
       "drought stress is contested (Section 5, Q1)."), chip("CONSISTENT", GREENC, w=24 * mm)],
    [C("Could affect the bark and nutrient transport"),
     C("Fine-root loss reduces uptake [4]; guidance cautions against burying the root flare [18]. No controlled "
       "study of concrete against bark."), chip("PLAUSIBLE", AMBER, w=24 * mm)],
    [C("Could contribute to decay"),
     C("Guidance links root and trunk-base stress to decay risk [12, 18]. No controlled study of concrete contact."),
     chip("PLAUSIBLE", AMBER, w=24 * mm)],
    [C("Only if left in place for a prolonged period"),
     C("No published threshold for how long cover is tolerated. Delayed symptoms (3\u20135+ years) mean short-term "
       "outcomes can mislead [12]."), chip("UNTESTED", GREY, w=24 * mm)],
]
rzt = Table(rz, colWidths=[44 * mm, 88 * mm, 38 * mm], repeatRows=1)
rzt.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), GREEN), ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                         ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, CREAM]),
                         ("LINEBELOW", (0, 0), (-1, -1), 0.4, colors.HexColor("#D5DBD7")),
                         ("TOPPADDING", (0, 0), (-1, -1), 4.5), ("BOTTOMPADDING", (0, 0), (-1, -1), 4.5),
                         ("LEFTPADDING", (0, 0), (-1, -1), 5), ("RIGHTPADDING", (0, 0), (-1, -1), 5),
                         ("ALIGN", (2, 1), (2, -1), "CENTER")]))
S.append(rzt)
S.append(Spacer(1, 4 * mm))

S.append(CondPageBreak(95 * mm))
S.append(P("Why \u201cno tree has died\u201d is weak evidence", h2))
S.append(P("Guidance literature stresses that trees damaged in construction can look healthy for years before "
           "crown thinning and dieback appear [12]. An absence of deaths therefore says little unless the works "
           "are old enough, and the trees are monitored with something finer than survival: canopy density, leaf "
           "area, shoot growth, root-collar condition."))
S.append(fig(FIG + "fig3_timeline.png", width=CW * 0.98))
S.append(P("Figure 3. Schematic only. The decline window reflects guidance in [12, 13], not a measured curve for these trees.",
           cap))
S.append(callout([P("WHAT THE PHOTOGRAPH CAN AND CANNOT SHOW", tag),
                  P("The article\u2019s photograph (caption: the concrete directly under the trunk has been removed) "
                    "shows a mound of loose soil and stone at the base, surrounded by a grey concrete layer across "
                    "the planter floor, with the planter\u2019s soil gone. It was taken after removal. It cannot show "
                    "how long the concrete was in contact, the condition of the roots and bark, or whether roots "
                    "were cut. Those are the quantities that determine the outcome.", small)],
                 bg=GREY_PALE, bar=SLATE))

# ================================================================== 7 VERDICT
S.append(Spacer(1, 8 * mm))
S.append(SectionHeading(7, "Verdict and requests for evidence"))
vb = Table([[
    [Paragraph('<font color="white">VERDICT</font>', ParagraphStyle("v1", fontName="Sans-B", fontSize=8, leading=10)),
     Paragraph('<font color="white">NOT SUBSTANTIATED</font>',
               ParagraphStyle("v2", fontName="Sans-B", fontSize=20, leading=24)),
     Paragraph('<font color="white">Plausible, but not shown. Confidence: moderate. Limited by absent site data '
               'and the absence of studies on temporary cover.</font>',
               ParagraphStyle("v3", fontName="Sans", fontSize=8.6, leading=11.4))]
]], colWidths=[CW])
vb.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), ORANGE), ("LEFTPADDING", (0, 0), (-1, -1), 12),
                        ("RIGHTPADDING", (0, 0), (-1, -1), 12), ("TOPPADDING", (0, 0), (-1, -1), 9),
                        ("BOTTOMPADDING", (0, 0), (-1, -1), 10), ("ROUNDEDCORNERS", [4, 4, 4, 4])]))
S.append(vb)
S.append(Spacer(1, 4 * mm))
S.append(P("<b>Why.</b> (1) The claim is conditional and its logic is sound in direction: the research suggests harm "
           "from sealing builds with time, and Ambjent itself names prolonged cover as the concern. (2) But no "
           "duration is given for \u201ctemporary\u201d, and the statement is silent on the soil removal and root "
           "exposure the article reports, which guidance literature treats as a major risk. (3) No tree-specific "
           "evidence has been published. (4) For permanent sealing the literature is mixed, with holm-oak data "
           "pointing toward harm; for temporary cover we found no studies at all."))
S.append(P("<b>What this verdict does not say.</b> It does not say the trees have been or will be damaged, that the "
           "works were unjustified, or that Ambjent acted in bad faith. Ambjent responded within days, stated the "
           "risk plainly and had concrete removed from the roots. A defensible statement would read: "
           "<i>\u201cThe concrete was in place for [N days]; exposed roots were protected by [method]; an arborist "
           "inspected on [date]; we will monitor [indicators] for [years].\u201d</i> That turns a reassurance into "
           "something checkable."))

S.append(P("Evidence we are asking for", h2))
box = '<font name="DejaVu" color="#14452F">\u2610</font>'
reqs = [
    "Species, estimated age and trunk diameter of every tree in a treated planter.",
    "For each planter: when the concrete was placed and when it was removed (duration of contact).",
    "How the soil was removed, whether roots were exposed, cut or damaged, and how exposed roots were protected "
    "(kept covered and moist, work in cooler weather).",
    "How the concrete was cleared from the roots and trunk base, and photographs of root and bark condition afterwards.",
    "The membrane design: drainage, the substrate that replaces the soil, and how the trees will be watered.",
    "Any pre- and post-works arborist report.",
    "Dates, species and monitoring records behind the \u201cfive planters, no tree died\u201d statement.",
    "Whether any tree is protected under the Trees and Woodlands (Protection) Regulations, and any permit "
    "conditions that applied.",
]
rq = Table([[Paragraph(box, cell), C(r)] for r in reqs], colWidths=[8 * mm, CW - 8 * mm])
rq.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"), ("TOPPADDING", (0, 0), (-1, -1), 3.2),
                        ("BOTTOMPADDING", (0, 0), (-1, -1), 3.2),
                        ("LINEBELOW", (0, 0), (-1, -1), 0.3, colors.HexColor("#D5DBD7"))]))
S.append(rq)
S.append(Spacer(1, 4 * mm))
S.append(callout([P("RIGHT OF REPLY", tag),
                  P("Before wider circulation this report should be sent to Ambjent Malta and Fondazzjoni Wirt Artna "
                    "with a fixed deadline for comment. Responses, and any evidence supplied, should be appended "
                    "and the verdict revisited. If new evidence moves the verdict, this document will be re-issued "
                    "with a change log (Appendix B).", small)],
                 bg=AMBER_PALE, bar=AMBER))

# ================================================================== 8 LIMITATIONS
S.append(Spacer(1, 6 * mm))
S.append(SectionHeading(8, "Limitations"))
lims = [
    "This is a targeted review, not a systematic one. Searches were run in October 2026 and may have missed relevant work.",
    "We found no studies of short-term, temporary concrete contact with roots. The core of Ambjent\u2019s claim is "
    "therefore assessed by mechanism and guidance, not by direct evidence.",
    "The Times of Malta article was read in full from a supplied PDF. The Newsbook page blocks automated access, so "
    "we read only a search excerpt. For several papers we read abstracts or summaries, and some sources are known "
    "only through other papers (marked \u25c6).",
    "Few studies examine concrete over a membrane around old Mediterranean trees. We extrapolate from pavement "
    "and soil-sealing research, mostly from wetter sites with different soils.",
    "No site visit or tree assessment was done; we saw published photographs only.",
    "Evidence-map positions are our qualitative judgement. Corrections and additional studies are welcome.",
]
for l in lims:
    S.append(P("\u2022 " + l, bul))

# ================================================================== REFERENCES
S.append(Spacer(1, 6 * mm))
S.append(SectionHeading(None, "References"))
refs = [
    ("1", "Micallef D. (1 Oct 2026). Wirt Artna explains concrete around Upper Barrakka tree: \u2018It is protecting "
          "historic tunnels\u2019. <i>Newsbook</i>.",
     "https://newsbook.com.mt/en/wirt-artna-explains-concrete-around-upper-barrakka-tree-it-is-protecting-historic-tunnels/"),
    ("2", "Parts of Upper Barrakka have been cemented over, but don\u2019t panic just yet\u2026 (c. Dec 2025). "
          "<i>MaltaToday</i>.",
     "https://www.maltatoday.com.mt/environment/environment/138909/parts_of_upper_barrakka_have_been_cemented_over_but_dont_panic_just_yet"),
    ("3", "Meilak N. (1 Oct 2026). Concrete layer won\u2019t damage Upper Barrakka trees, Ambjent Malta says. "
          "<i>Times of Malta</i>. (Read in full from a supplied PDF.)", ""),
    ("4", "Viswanathan B. et al. (2011). Impervious and pervious pavements increase soil CO<sub>2</sub> concentrations "
          "and reduce root production of American sweetgum (<i>Liquidambar styraciflua</i>). <i>Urban Forestry &amp; "
          "Urban Greening</i>.",
     "https://www.sciencedirect.com/science/article/abs/pii/S1618866711000057"),
    ("5", "Fini A. et al. (2022). Effects of pavements on established urban trees: growth, physiology, ecosystem "
          "services and disservices. <i>Landscape and Urban Planning</i> 226:104501. doi:10.1016/j.landurbplan.2022.104501.",
     "https://www.sciencedirect.com/science/article/abs/pii/S0169204622001505"),
    ("6", "Savi T. et al. (2015). Drought-induced xylem cavitation and hydraulic deterioration: risk factors for "
          "urban trees under climate change? <i>New Phytologist</i> 205(3). doi:10.1111/nph.13112.",
     "https://nph.onlinelibrary.wiley.com/doi/10.1111/nph.13112"),
    ("7", "Cui B. et al. (2022). Responses of tree growth, leaf area and physiology to pavement in <i>Ginkgo biloba</i> "
          "and <i>Platanus orientalis</i>. <i>Frontiers in Plant Science</i> 13:1003266.", ""),
    ("8", "Volder A. et al. (2009). Potential use of pervious concrete for maintaining existing mature trees during "
          "and after urban development. <i>Urban Forestry &amp; Urban Greening</i>. (Cited in [5]; not read directly.)",
     "https://www.sciencedirect.com/science/article/pii/S1618866709000557"),
    ("9", "The management of tree root systems in urban and suburban settings II: a review of strategies to mitigate "
          "human impacts. <i>Arboriculture &amp; Urban Forestry</i> 40(5):249 (2014).",
     "https://auf.isa-arbor.com/content/40/5/249"),
    ("10", "Hauer R.J., Miller R.W., Ouimet D.M. (1994). Street tree decline and construction damage. <i>Journal of "
           "Arboriculture</i> 20:94\u201397. (Cited in [9]; not read directly.)", ""),
    ("11", "TreeNet. Permeable pavements and their influence on tree growth of <i>Melaleuca quinquenervia</i>: a "
           "summary (cites North et al. 2015; Kozlowski 1984; Ingram et al. 1989).",
     "https://treenet.org/resource/permeable-pavements-and-their-influence-on-tree-growth-of-melaleuca-quinquenervia-a-summary/"),
    ("12", "US National Park Service. Preservation Matters: protecting historic trees during construction.",
     "https://www.nps.gov/articles/000/preservation-matters-landscape-maintenance-protecting-historic-trees-during-construction.htm"),
    ("13", "Minnesota Department of Natural Resources. Construction damage causes and remedies.",
     "https://www.dnr.state.mn.us/treecare/maintenance/construction_damage.html"),
    ("14", "Washington State Department of Ecology. Recycled concrete aggregate leachate: a literature review "
           "(Publication 22-03-003).", "https://apps.ecology.wa.gov/publications/documents/2203003.pdf"),
    ("15", "Effect of leaching from freshly cast concrete on pH (laboratory study). ResearchGate.",
     "https://www.researchgate.net/publication/272026868_Effect_of_Leaching_from_Freshly_Cast_Concrete_on_pH"),
    ("16", "A case study of street tree soil aeration in two different soil types (Helsinki). <i>Arboriculture &amp; "
           "Urban Forestry</i> 44(4):174 (citing Kozlowski &amp; Davies 1975).",
     "https://auf.isa-arbor.com/content/44/4/174"),
    ("17", "Minnesota Pollution Control Agency, Minnesota Stormwater Manual. Protection of existing trees on "
           "construction sites (cites Johnson 1999 on covering exposed roots and avoiding hot, dry weather).",
     "https://stormwater.pca.state.mn.us/protection_of_existing_trees_on_construction_sites"),
    ("18", "Tree Care Advisors. Protecting trees during construction (industry guide; lower evidential weight).",
     "https://treecareadvisors.com/guides/construction-damage/"),
]
for n, t, u in refs:
    link = f' <link href="{u}" color="#3C6E8F">{u}</link>' if u else ""
    S.append(Paragraph(f"<b>[{n}]</b> {t}{link}", ref))

# ================================================================== APPENDIX
S.append(PageBreak())
S.append(SectionHeading(None, "Appendix A: series standards and verdict scale"))
S.append(P("Every investigation in this series follows the same rules so that verdicts are comparable and "
           "challengeable.", lead))
scale = [
    [C("Verdict", cellh), C("Meaning", cellh)],
    [chip("SUPPORTED", colors.HexColor("#2E7D4F"), w=36 * mm),
     C("Evidence consistently backs the claim as stated.")],
    [chip("LARGELY SUPPORTED", colors.HexColor("#8DB36B"), w=36 * mm),
     C("Backed by the evidence, with minor caveats that do not change the substance.")],
    [chip("NOT SUBSTANTIATED", ORANGE, w=36 * mm),
     C("Stated more strongly than the evidence offered or available allows. May be true in some conditions but "
       "has not been shown.")],
    [chip("MISLEADING", colors.HexColor("#C85A3A"), w=36 * mm),
     C("Omits material facts so that the overall impression is inaccurate, even if individual statements are "
       "defensible.")],
    [chip("CONTRADICTED", colors.HexColor("#8E2F25"), w=36 * mm),
     C("The available evidence points against the claim.")],
]
sct = Table(scale, colWidths=[42 * mm, CW - 42 * mm])
sct.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), GREEN), ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                         ("LINEBELOW", (0, 0), (-1, -1), 0.4, colors.HexColor("#D5DBD7")),
                         ("TOPPADDING", (0, 0), (-1, -1), 5), ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                         ("LEFTPADDING", (0, 0), (-1, -1), 5)]))
S.append(sct)
S.append(Spacer(1, 3 * mm))
S.append(P("Confidence", h2))
S.append(P("<b>High</b>: multiple independent lines of evidence agree. <b>Moderate</b>: evidence is relevant but "
           "incomplete or indirect. <b>Low</b>: evidence is thin, second-hand or conflicting."))
S.append(P("Standards", h2))
stds = [
    "<b>Quote the speaker, not the headline,</b> with outlet and date, and link the original where possible.",
    "<b>Separate the claim from the evidence offered for it,</b> and say who made which statement.",
    "<b>Grade the evidence</b> and show differing views side by side where the science is unsettled.",
    "<b>State what we could not access or verify,</b> and what would change the verdict either way.",
    "<b>Ask for the missing evidence</b> in specific, answerable requests.",
    "<b>Offer a right of reply</b> before wider circulation and append responses.",
    "<b>Correct errors openly</b> with a version number and change log.",
    "<b>Whistle-blow only on evidence:</b> a verdict of <i>Misleading</i> or <i>Contradicted</i> requires "
    "documents or data that can be shown, not inference.",
]
for s_ in stds:
    S.append(P("\u2022 " + s_, bul))


S.append(Spacer(1, 5 * mm))
S.append(SectionHeading(None, "Appendix B: revision log"))
rl = [
    [C("Version", cellh), C("Date", cellh), C("Change", cellh)],
    [C("<b>1.0</b>"), C("2 Oct 2026"),
     C("First issue. Based on the headline and secondary reporting; the full article was not accessed. Treated the "
       "claim as a blanket statement that concrete will not harm trees.")],
    [C("<b>1.1</b>"), C("2 Oct 2026"),
     C("Incorporates the full Times of Malta article. Claim restated as conditional on the concrete being "
       "temporary. Added a check of Ambjent\u2019s own reasoning, a new contested question on temporary cover, "
       "and sub-claims B, C and F. Photo description revised. Added references [17] and [18]. Verdict label "
       "unchanged (Not substantiated); the reasoning changed from <i>blanket claim overstated</i> to "
       "<i>conditional claim plausible but unevidenced</i>.")],
]
rlt = Table(rl, colWidths=[16 * mm, 22 * mm, CW - 38 * mm])
rlt.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), GREEN), ("VALIGN", (0, 0), (-1, -1), "TOP"),
                         ("LINEBELOW", (0, 0), (-1, -1), 0.4, colors.HexColor("#D5DBD7")),
                         ("TOPPADDING", (0, 0), (-1, -1), 5), ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                         ("LEFTPADDING", (0, 0), (-1, -1), 5)]))
S.append(rlt)

doc.build(S)
print("built", OUT)
