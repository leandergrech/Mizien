"""Shared design for Miżien claim-check reports and flyers.

Extracted from tools/cc-001-report/ so that new checks match the CC-001 design without copying 1,000 lines.
Helpers tag what they build (`obj._mz`) so tools/report_html.py can publish the same report as web HTML;
the tags do not change the PDF.
CC-001's own generators are left unchanged. A claim's build script fills a `Report` / `Flyer` config
(see tools/cc-003-report/build_report.py for an example) and calls build_report() / build_flyer().
"""
import os
from dataclasses import dataclass, field

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.lib.utils import simpleSplit
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas as rl_canvas
from reportlab.platypus import (BaseDocTemplate, CondPageBreak, Flowable, Frame, Image, KeepTogether,
                                NextPageTemplate, PageBreak, PageTemplate, Paragraph, Spacer, Table,
                                TableStyle)

FD = "/usr/share/fonts/truetype/liberation/"
for n, f in [("Serif", "LiberationSerif-Regular"), ("Serif-B", "LiberationSerif-Bold"),
             ("Serif-I", "LiberationSerif-Italic"), ("Serif-BI", "LiberationSerif-BoldItalic"),
             ("Sans", "LiberationSans-Regular"), ("Sans-B", "LiberationSans-Bold"),
             ("Sans-I", "LiberationSans-Italic"), ("Sans-BI", "LiberationSans-BoldItalic")]:
    pdfmetrics.registerFont(TTFont(n, FD + f + ".ttf"))
pdfmetrics.registerFont(TTFont("DejaVu", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"))
pdfmetrics.registerFontFamily("Serif", normal="Serif", bold="Serif-B", italic="Serif-I", boldItalic="Serif-BI")
pdfmetrics.registerFontFamily("Sans", normal="Sans", bold="Sans-B", italic="Sans-I", boldItalic="Sans-BI")

# ------------------------------------------------------------------ palette (PROJECT_STATE.md)
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
ORANGE_PALE = colors.HexColor("#FBE9DA")
BLUE = colors.HexColor("#3C6E8F")
BLUE_PALE = colors.HexColor("#E3EDF3")
GREENC = colors.HexColor("#2E7D4F")
LIGHTGREEN = colors.HexColor("#BFD6C5")
RULE = colors.HexColor("#D5DBD7")

VERDICTS = ["Supported", "Largely supported", "Not substantiated", "Misleading", "Contradicted"]
VERDICT_COLS = [GREENC, colors.HexColor("#8DB36B"), ORANGE, colors.HexColor("#C85A3A"),
                colors.HexColor("#8E2F25")]
METER_LABELS = [("SUPPORTED", ""), ("LARGELY", "SUPPORTED"), ("NOT", "SUBSTANTIATED"), ("MISLEADING", ""),
                ("CONTRADICTED", "")]
# Pledge labels (methodology/verdict-scale.md, Pledges): a pure pledge check shows one of these instead of a verdict.
PLEDGES = ["Not measurable", "Not yet due", "On track", "Off track", "Met", "Missed"]
# The site's pledge palette: every colour passes 4.5:1 with white text and stays apart from the verdict colours.
PLEDGE_COLS = [colors.HexColor(h) for h in ("#716F8D", "#5C7689", "#337F71", "#AE5D33", "#23705F", "#7C2D4A")]
PLEDGE_METER_LABELS = [("NOT", "MEASURABLE"), ("NOT YET", "DUE"), ("ON", "TRACK"), ("OFF", "TRACK"), ("MET", ""),
                       ("MISSED", "")]


def scale_of(label):
    """(kind, labels, colours, meter labels, index) for a verdict or a pledge label."""
    if label in PLEDGES:
        return "pledge", PLEDGES, PLEDGE_COLS, PLEDGE_METER_LABELS, PLEDGES.index(label)
    return "verdict", VERDICTS, VERDICT_COLS, METER_LABELS, VERDICTS.index(label)


PW, PH = A4
LM = RM = 20 * mm
TM = 24 * mm
BM = 20 * mm
CW = PW - LM - RM
REPO_URL = "https://github.com/leandergrech/Mizien"
CONTEST_URL = REPO_URL + "/issues/new?template=contest-verdict.yml"   # the repository's 'Contest a verdict' form
BYLINE = "MIŻIEN  ·  AN INDEPENDENT FACT-CHECKING PROJECT"               # project name only (maintainer, 5 Oct 2026)
CONTEST = "Contest a verdict, with evidence:  github.com/leandergrech/Mizien/issues"

# ------------------------------------------------------------------ styles
body = ParagraphStyle("body", fontName="Serif", fontSize=10.2, leading=14.6, textColor=SLATE, spaceAfter=6,
                      alignment=TA_LEFT)
lead = ParagraphStyle("lead", parent=body, fontSize=11.4, leading=16.4, textColor=GREEN)
small = ParagraphStyle("small", parent=body, fontName="Sans", fontSize=8.2, leading=11.2, spaceAfter=0)
cap = ParagraphStyle("cap", parent=small, fontName="Sans-I", textColor=GREY, spaceBefore=3, spaceAfter=10)
h2 = ParagraphStyle("h2", fontName="Sans-B", fontSize=11.5, leading=15, textColor=GREEN, spaceBefore=8, spaceAfter=4)
cell = ParagraphStyle("cell", fontName="Sans", fontSize=8.1, leading=10.8, textColor=SLATE)
cellb = ParagraphStyle("cellb", parent=cell, fontName="Sans-B")
cellh = ParagraphStyle("cellh", parent=cell, fontName="Sans-B", textColor=colors.white, fontSize=7.8)
tag = ParagraphStyle("tag", fontName="Sans-B", fontSize=7.2, leading=9, textColor=GREEN, spaceAfter=2)
ref = ParagraphStyle("ref", fontName="Sans", fontSize=8, leading=11, textColor=SLATE, leftIndent=16,
                     firstLineIndent=-16, spaceAfter=3.2)
bul = ParagraphStyle("bul", parent=body, leftIndent=12, firstLineIndent=-9, spaceAfter=3)

DIAM = '<font name="DejaVu" size="6.5">◆</font>'
GRADE_BG = {"A": colors.HexColor("#CFE5D5"), "B": BLUE_PALE, "C": AMBER_PALE, "D": RED_PALE}


def P(t, s=body):
    return Paragraph(t.replace("◆", DIAM), s)


def C(t, s=cell):
    return Paragraph(t.replace("◆", DIAM), s)


def hexs(c):
    return c.hexval().replace("0x", "#")


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
        x0 = 0
        if self.num:
            c.setFillColor(GREEN)
            c.circle(5 * mm, y + 1.5 * mm, 4.6 * mm, stroke=0, fill=1)
            c.setFillColor(colors.white)
            c.setFont("Sans-B", 11.5)
            c.drawCentredString(5 * mm, y, str(self.num))
            x0 = 13 * mm
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
    """The verdict scale with this claim's verdict marked; scale="pledge" draws the six pledge labels instead."""
    def __init__(self, active, width=CW, scale="verdict"):
        super().__init__()
        self.width, self.active, self.scale = width, active, scale

    def wrap(self, aw, ah):
        return self.width, 25 * mm

    def draw(self):
        c = self.canv
        labels, cols = (PLEDGE_METER_LABELS, PLEDGE_COLS) if self.scale == "pledge" else (METER_LABELS, VERDICT_COLS)
        gap = 1.6 * mm
        sw = (self.width - (len(labels) - 1) * gap) / len(labels)
        y, h = 2 * mm, 11 * mm
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
            c.setFont("Sans-B", 6.6 if i == self.active else 6.4)
            if l2:
                c.drawCentredString(x + sw / 2, y + h / 2 + 0.9 * mm, l1)
                c.drawCentredString(x + sw / 2, y + h / 2 - 2.3 * mm, l2)
            else:
                c.drawCentredString(x + sw / 2, y + h / 2 - 1 * mm, l1)
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
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), bg), ("LINEBEFORE", (0, 0), (0, -1), 3.2, bar),
                           ("LEFTPADDING", (0, 0), (-1, -1), pad + 3), ("RIGHTPADDING", (0, 0), (-1, -1), pad),
                           ("TOPPADDING", (0, 0), (-1, -1), pad - 1), ("BOTTOMPADDING", (0, 0), (-1, -1), pad - 1)]))
    t._mz = ("callout", paras, hexs(bg), hexs(bar))
    return t


def chip(text, bg, fg=colors.white, w=34 * mm):
    t = Table([[Paragraph(f'<font color="{hexs(fg)}">{text}</font>',
                          ParagraphStyle("chip", fontName="Sans-B", fontSize=7, leading=8.6, alignment=TA_CENTER))]],
              colWidths=[w])
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), bg),
                           ("TOPPADDING", (0, 0), (-1, -1), 3), ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
                           ("LEFTPADDING", (0, 0), (-1, -1), 3), ("RIGHTPADDING", (0, 0), (-1, -1), 3),
                           ("ROUNDEDCORNERS", [3, 3, 3, 3])]))
    t._mz = ("chip", text, hexs(bg), hexs(fg))
    return t


def fig(path, width=CW):
    from PIL import Image as PI
    w, h = PI.open(path).size
    im = Image(path, width=width, height=width * h / w)
    im._mz = ("fig", str(path))
    return im


def grade_tag(g):
    return _tag(("grade", g), Table([[Paragraph(f'<font color="#2B3A42">{g}</font>',
                             ParagraphStyle("g", fontName="Sans-B", fontSize=8, alignment=TA_CENTER))]],
                 colWidths=[6 * mm], style=TableStyle([("BACKGROUND", (0, 0), (-1, -1), GRADE_BG.get(g, GREY_PALE)),
                                                       ("TOPPADDING", (0, 0), (-1, -1), 1),
                                                       ("BOTTOMPADDING", (0, 0), (-1, -1), 1),
                                                       ("LEFTPADDING", (0, 0), (-1, -1), 0),
                                                       ("RIGHTPADDING", (0, 0), (-1, -1), 0)])))


def _tag(mz, obj):
    obj._mz = mz
    return obj


def std_table(rows, widths, header=True, valign="TOP", zebra=True, extra=None):
    t = Table(rows, colWidths=widths, repeatRows=1 if header else 0)
    st = [("VALIGN", (0, 0), (-1, -1), valign), ("LINEBELOW", (0, 0), (-1, -1), 0.4, RULE),
          ("TOPPADDING", (0, 0), (-1, -1), 4.5), ("BOTTOMPADDING", (0, 0), (-1, -1), 4.5),
          ("LEFTPADDING", (0, 0), (-1, -1), 5), ("RIGHTPADDING", (0, 0), (-1, -1), 5)]
    if header:
        st.append(("BACKGROUND", (0, 0), (-1, 0), GREEN))
    if zebra:
        st.append(("ROWBACKGROUNDS", (0, 1 if header else 0), (-1, -1), [colors.white, CREAM]))
    t.setStyle(TableStyle(st + (extra or [])))
    t._mz = ("table", rows, header)
    return t


def contested(title, status, status_col, side_a, side_b, why, label_a="EVIDENCE FOR THE CLAIM'S IMPRESSION",
              label_b="EVIDENCE AGAINST", label_why="WHY THEY DIFFER, AND WHAT IT MEANS HERE"):
    hdr = [Paragraph(f"<b>{title}</b>", ParagraphStyle("ch", fontName="Sans-B", fontSize=9.6, leading=12.4,
                                                     textColor=colors.white)), chip(status, status_col, w=40 * mm)]
    head = Table([hdr], colWidths=[CW - 42 * mm, 42 * mm])
    head.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), GREEN), ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                              ("LEFTPADDING", (0, 0), (0, 0), 8), ("RIGHTPADDING", (-1, 0), (-1, 0), 6),
                              ("TOPPADDING", (0, 0), (-1, -1), 5), ("BOTTOMPADDING", (0, 0), (-1, -1), 5)]))
    inner = Table([[[P(label_a, ParagraphStyle("t2", parent=tag, textColor=GREENC)), P(side_a, cell)],
                    [P(label_b, ParagraphStyle("t1", parent=tag, textColor=RED)), P(side_b, cell)]]],
                  colWidths=[CW / 2, CW / 2])
    inner.setStyle(TableStyle([("BACKGROUND", (0, 0), (0, 0), PALE), ("BACKGROUND", (1, 0), (1, 0), RED_PALE),
                               ("LEFTPADDING", (0, 0), (-1, -1), 8), ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                               ("TOPPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
                               ("VALIGN", (0, 0), (-1, -1), "TOP")]))
    foot = Table([[[P(label_why, ParagraphStyle("t3", parent=tag, textColor=SLATE)), P(why, cell)]]], colWidths=[CW])
    foot.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), GREY_PALE),
                              ("LEFTPADDING", (0, 0), (-1, -1), 8), ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                              ("TOPPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 7)]))
    return _tag(("contested", title, status, hexs(status_col), side_a, side_b, why, label_a, label_b, label_why),
                KeepTogether([head, inner, foot, Spacer(1, 5 * mm)]))


def key_points(kp):
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
    return _tag(("keypoints", kp), callout([kt], bg=PALE, bar=GREEN, pad=8))


def tiles(items):
    """items: list of (big text, colour, caption)."""
    st = {GREEN: "big", RED: "bigr", ORANGE: "bigo"}
    big = ParagraphStyle("big", fontName="Sans-B", fontSize=19, leading=22, textColor=GREEN)
    tcap = ParagraphStyle("tcap", fontName="Sans", fontSize=7.4, leading=9.6, textColor=SLATE)
    row1 = [Paragraph(b, ParagraphStyle("b" + str(i), parent=big, textColor=col)) for i, (b, col, _) in enumerate(items)]
    row2 = [Paragraph(c, tcap) for _, _, c in items]
    n = len(items)
    tt = Table([row1, row2], colWidths=[CW / n] * n)
    tt.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), CREAM), ("LINEAFTER", (0, 0), (-2, -1), 1.2, colors.white),
                            ("LEFTPADDING", (0, 0), (-1, -1), 8), ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                            ("TOPPADDING", (0, 0), (-1, 0), 7), ("BOTTOMPADDING", (0, 0), (-1, 0), 1),
                            ("TOPPADDING", (0, 1), (-1, 1), 0), ("BOTTOMPADDING", (0, 1), (-1, 1), 7),
                            ("VALIGN", (0, 0), (-1, -1), "TOP")]))
    return _tag(("tiles", [(b, hexs(col), cp) for b, col, cp in items]), tt)


def up_down(up, down, heads=("What would move the verdict up", "What would move it down")):
    """Two boxes: what would raise and what would lower the verdict (a pledge check passes its own headings)."""
    wc = Table([[[P(heads[0].upper(), tag), P(up, small)],
                 [P(f'<font color="#B5483A">{heads[1].upper()}</font>', tag), P(down, small)]]],
               colWidths=[CW / 2, CW / 2], hAlign="LEFT")
    wc.setStyle(TableStyle([("BACKGROUND", (0, 0), (0, 0), PALE), ("BACKGROUND", (1, 0), (1, 0), RED_PALE),
                            ("LEFTPADDING", (0, 0), (-1, -1), 8), ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                            ("TOPPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
                            ("VALIGN", (0, 0), (-1, -1), "TOP")]))
    return _tag(("updown", up, down, *heads), wc)


def toc(items):
    tp = ParagraphStyle("toc", fontName="Sans", fontSize=8.6, leading=12, textColor=SLATE)
    cells = [Paragraph(f'<font name="Sans-B" color="#14452F">{n}</font>&nbsp;&nbsp;{t}', tp) for n, t in items]
    if len(cells) % 2:
        cells.append(Paragraph("", tp))
    half = len(cells) // 2
    t = Table([[cells[i], cells[i + half]] for i in range(half)], colWidths=[CW / 2, CW / 2])
    t.setStyle(TableStyle([("TOPPADDING", (0, 0), (-1, -1), 2.2), ("BOTTOMPADDING", (0, 0), (-1, -1), 2.2),
                           ("LEFTPADDING", (0, 0), (-1, -1), 0), ("LINEBELOW", (0, 0), (-1, -1), 0.3, RULE)]))
    return [P("IN THIS REPORT", tag), _tag(("toc", items), t)]


def verdict_box(verdict, subline):
    kind, _, cols, _, i = scale_of(verdict)
    vb = Table([[[Paragraph(f'<font color="white">{kind.upper()}</font>',
                            ParagraphStyle("v1", fontName="Sans-B", fontSize=8, leading=10)),
                  Paragraph(f'<font color="white">{verdict.upper()}</font>',
                            ParagraphStyle("v2", fontName="Sans-B", fontSize=20, leading=24)),
                  Paragraph(f'<font color="white">{subline}</font>',
                            ParagraphStyle("v3", fontName="Sans", fontSize=8.6, leading=11.4))]]], colWidths=[CW])
    vb.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), cols[i]), ("LEFTPADDING", (0, 0), (-1, -1), 12),
                            ("RIGHTPADDING", (0, 0), (-1, -1), 12), ("TOPPADDING", (0, 0), (-1, -1), 9),
                            ("BOTTOMPADDING", (0, 0), (-1, -1), 10), ("ROUNDEDCORNERS", [4, 4, 4, 4])]))
    return _tag(("verdictbox", verdict, subline), vb)


def requests_list(reqs):
    box = '<font name="DejaVu" color="#14452F">☐</font>'
    rq = Table([[Paragraph(box, cell), C(r)] for r in reqs], colWidths=[8 * mm, CW - 8 * mm])
    rq.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"), ("TOPPADDING", (0, 0), (-1, -1), 3.2),
                            ("BOTTOMPADDING", (0, 0), (-1, -1), 3.2), ("LINEBELOW", (0, 0), (-1, -1), 0.3, RULE)]))
    return _tag(("requests", reqs), rq)


def references(refs):
    out = []
    for n, t, u in refs:
        link = f' <link href="{u}" color="#3C6E8F">{u.replace("&", "&amp;")}</link>' if u else ""
        out.append(_tag(("ref", n, t, u), Paragraph(f"<b>[{n}]</b> {t.replace('◆', DIAM)}{link}", ref)))
    return out


def appendix_a(evidence_note, pledges=False):
    S = [SectionHeading(None, "Appendix A: series standards and verdict scale"),
         P("Every investigation in this series follows the same rules so that verdicts are comparable and "
           "challengeable.", lead)]
    meanings = ["Evidence consistently backs the claim as stated.",
                "Backed by the evidence, with minor caveats that do not change the substance.",
                "Stated more strongly than the evidence offered or available allows. May be true in some "
                "conditions but has not been shown.",
                "Omits material facts so that the overall impression is inaccurate, even if individual statements "
                "are defensible.",
                "The available evidence points against the claim."]
    rows = [[C("Verdict", cellh), C("Meaning", cellh)]] + \
           [[chip(v.upper(), VERDICT_COLS[i], w=36 * mm), C(meanings[i])] for i, v in enumerate(VERDICTS)]
    S.append(std_table(rows, [42 * mm, CW - 42 * mm], valign="MIDDLE", zebra=False))
    if pledges:
        pmean = ["The pledge as worded has no definition, baseline or date against which delivery could be checked.",
                 "Measurable; the deadline or term has not passed and no progress data have been published yet.",
                 "Published progress is at or ahead of a straight-line path (or the pledge's own milestones) to the "
                 "target by the deadline.",
                 "Published progress is behind that path, and the target has not yet been shown to be met or missed.",
                 "Documents or data show the target was reached, by the deadline if one was set.",
                 "The deadline or term has passed, and documents or data that can be shown say the target was not "
                 "reached."]
        S += [Spacer(1, 3 * mm), P("Pledge labels", h2),
              P("A pledge is a promise of future action, so it cannot be true or false when it is made. It gets one of "
                "these labels instead of a verdict, with the date of the evidence behind it.")]
        S.append(std_table([[C("Pledge label", cellh), C("Meaning", cellh)]] +
                           [[chip(v.upper(), PLEDGE_COLS[i], w=36 * mm), C(pmean[i])] for i, v in enumerate(PLEDGES)],
                           [42 * mm, CW - 42 * mm], valign="MIDDLE", zebra=False))
    S += [Spacer(1, 3 * mm), P("Confidence", h2),
          P("<b>High</b>: multiple independent lines of evidence agree. <b>Moderate</b>: evidence is relevant but "
            "incomplete or indirect. <b>Low</b>: evidence is thin, second-hand or conflicting."),
          P("Evidence grades", h2), P(evidence_note), P("Standards", h2)]
    for s_ in ["<b>Quote the speaker, not the headline,</b> with outlet and date, and link the original where possible.",
               "<b>Separate the claim from the evidence offered for it,</b> and say who made which statement.",
               "<b>Grade the evidence</b> and show differing views side by side where the evidence is unsettled.",
               "<b>State what we could not access or verify,</b> and what would change the verdict either way.",
               "<b>Ask for the missing evidence</b> in specific, answerable requests.",
               "<b>Offer a right of reply</b> where a check finds a claim Not substantiated, Misleading or Contradicted "
               "(or a pledge Not measurable, Off track or Missed), before wider circulation, and append responses.",
               "<b>Correct errors openly</b> with a version number and change log.",
               "<b>Whistle-blow only on evidence:</b> a verdict of <i>Misleading</i> or <i>Contradicted</i> requires "
               "documents or data that can be shown, not inference.",
               "<b>Check every side.</b> Government, opposition, NGOs and developers are held to the same standard."]:
        S.append(P("• " + s_, bul))
    return S


def revision_log(entries):
    rows = [[C("Version", cellh), C("Date", cellh), C("Change", cellh)]] + \
           [[C(f"<b>{v}</b>"), C(d), C(t)] for v, d, t in entries]
    return [SectionHeading(None, "Appendix B: revision log"), std_table(rows, [16 * mm, 22 * mm, CW - 38 * mm],
                                                                        zebra=False)]


# ------------------------------------------------------------------ report document
@dataclass
class Report:
    number: str                 # "003"
    out: str                    # output pdf path
    kicker: str                 # cover kicker after "Claim Check NNN · "
    title_lines: list           # cover title lines
    subtitle_lines: list        # cover italic subtitle lines
    quote_lines: list           # claim card quote lines (already with curly quotes)
    attribution: str            # claim card line 1
    context: str                # claim card line 2
    verdict: str
    verdict_note: str           # next to cover pill
    footer_lines: list          # cover footer lines
    running_head: str           # body page header right
    version: str
    date: str
    pdf_title: str
    pdf_subject: str
    title_size: float = 37
    quote_size: float = 16.5
    status_note: str = None     # page footer and cover "Status:" line; None = derived from verdict and pledge_label
    pledge_label: str = None    # a mixed check's pledge label (a pure pledge passes it as `verdict`)
    story: list = field(default_factory=list)


REPLY_VERDICTS = {"Not substantiated", "Misleading", "Contradicted"}   # maintainer rule, 5 Oct 2026
REPLY_PLEDGES = {"Not measurable", "Off track", "Missed"}


def reply_status(verdict, pledge_label=None):
    """The one wording for the cover and every page footer: a reply is sought only for these verdicts and labels."""
    needs = verdict in REPLY_VERDICTS or verdict in REPLY_PLEDGES or (pledge_label in REPLY_PLEDGES)
    return "pending right of reply" if needs else "no right of reply needed"


def build_report(R: Report):
    vkind, _, vcols, _, vi = scale_of(R.verdict)
    if R.status_note is None:                       # derived, so cover, footers and the record cannot disagree
        R.status_note = reply_status(R.verdict, R.pledge_label)
    status_line = "Status: draft, pending right of reply" if R.status_note == "pending right of reply" else \
        "Status: no right of reply needed" if R.status_note == "no right of reply needed" else f"Status: {R.status_note}"
    R.footer_lines = [status_line if str(l).startswith("Status:") else l for l in R.footer_lines]

    def draw_cover(c, doc):
        c.saveState()
        c.setFillColor(GREEN)
        c.rect(0, 0, PW, PH, stroke=0, fill=1)
        c.setStrokeColor(SAGE)
        cx, cy = PW * 0.80, PH * 0.20
        for i in range(1, 22):
            c.setStrokeAlpha(0.10 + (0.06 if i % 4 == 0 else 0))
            c.setLineWidth(1.2 if i % 4 == 0 else 0.7)
            c.ellipse(cx - i * 9.5 * mm + (i % 3) * 0.6 * mm, cy - i * 9.0 * mm, cx + i * 9.5 * mm, cy + i * 9.6 * mm)
        c.setStrokeAlpha(1)
        c.setFillColor(AMBER)
        c.rect(LM, PH - 31 * mm, 14 * mm, 1.6 * mm, stroke=0, fill=1)
        c.setFont("Sans-B", 9)
        c.drawString(LM, PH - 38 * mm, "MIŻIEN")
        c.setFillColor(LIGHTGREEN)
        c.setFont("Sans", 9)
        c.drawString(LM + 19 * mm, PH - 38 * mm, f"Claim Check {R.number}  ·  {R.kicker}")
        c.setFillColor(colors.white)
        c.setFont("Serif-B", R.title_size)
        step = R.title_size * 0.42 * mm
        for i, line in enumerate(R.title_lines):
            c.drawString(LM, PH - 70 * mm - i * step, line)
        ys = PH - 70 * mm - (len(R.title_lines) - 1) * step - 15 * mm
        c.setFillColor(colors.HexColor("#CFE2D4"))
        c.setFont("Serif-I", 13.5)
        for i, line in enumerate(R.subtitle_lines):
            c.drawString(LM, ys - i * 6 * mm, line)
        y0 = 78 * mm
        c.setFillColor(CREAM)
        c.roundRect(LM, y0, CW, 52 * mm, 3 * mm, stroke=0, fill=1)
        c.setFillColor(AMBER)
        c.rect(LM, y0, 2.6 * mm, 52 * mm, stroke=0, fill=1)
        c.setFillColor(GREY)
        c.setFont("Sans-B", 7.6)
        c.drawString(LM + 9 * mm, y0 + 44 * mm, "THE CLAIM UNDER REVIEW")
        c.setFillColor(GREEN)
        qs = R.quote_size
        c.setFont("Serif-BI", qs)
        for i, line in enumerate(R.quote_lines):
            c.drawString(LM + 9 * mm, y0 + 35 * mm - i * (qs * 0.43) * mm, line)
        c.setFillColor(SLATE)
        c.setFont("Sans", 8.2)
        c.drawString(LM + 9 * mm, y0 + 19.5 * mm - (0 if len(R.quote_lines) <= 2 else 1.5 * mm), R.attribution)
        c.drawString(LM + 9 * mm, y0 + 15.3 * mm - (0 if len(R.quote_lines) <= 2 else 1.5 * mm), R.context)
        c.setFillColor(vcols[vi])
        pill = f"{vkind.upper()}:  {R.verdict.upper()}"
        pw_ = pdfmetrics.stringWidth(pill, "Sans-B", 9) + 14 * mm
        c.roundRect(LM + 9 * mm, y0 + 4.2 * mm, pw_, 7.6 * mm, 3.8 * mm, stroke=0, fill=1)
        c.setFillColor(colors.white)
        c.setFont("Sans-B", 9)
        c.drawCentredString(LM + 9 * mm + pw_ / 2, y0 + 6.7 * mm, pill)
        c.setFillColor(SLATE)
        c.setFont("Sans-I", 8.2)
        c.drawString(LM + 14 * mm + pw_, y0 + 6.8 * mm, R.verdict_note)
        c.setFillColor(LIGHTGREEN)
        c.setFont("Sans", 8.4)
        for i, line in enumerate(R.footer_lines):
            c.drawString(LM, 36 * mm - i * 4.5 * mm, line)
        c.setFillColor(AMBER)
        c.setFont("Sans-B", 7.6)
        c.drawString(LM, 14.6 * mm, BYLINE)
        c.setFillColor(LIGHTGREEN)
        c.setFont("Sans", 8.4)
        c.drawString(LM, 10.1 * mm, CONTEST)
        c.linkURL(CONTEST_URL, (LM, 9 * mm, LM + pdfmetrics.stringWidth(CONTEST, "Sans", 8.4), 13 * mm), relative=0)
        c.restoreState()

    def draw_body(c, doc):
        c.saveState()
        c.setStrokeColor(SAGE)
        c.setLineWidth(0.6)
        c.line(LM, PH - 15 * mm, PW - RM, PH - 15 * mm)
        c.setFillColor(GREEN)
        c.setFont("Sans-B", 7.2)
        c.drawString(LM, PH - 12.2 * mm, f"MIŻIEN  ·  CLAIM CHECK {R.number}")
        c.setFillColor(GREY)
        c.setFont("Sans", 7.2)
        c.drawRightString(PW - RM, PH - 12.2 * mm, R.running_head)
        c.setStrokeColor(RULE)
        c.line(LM, 14 * mm, PW - RM, 14 * mm)
        c.drawString(LM, 9.6 * mm, f"v{R.version} draft  ·  {R.date}  ·  {R.status_note}")
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

    os.makedirs(os.path.dirname(R.out), exist_ok=True)
    doc = Doc(R.out, pagesize=A4, leftMargin=LM, rightMargin=RM, topMargin=TM, bottomMargin=BM,
              title=R.pdf_title, author="Miżien", subject=R.pdf_subject)
    cover_frame = Frame(LM, BM, CW, 20, id="cf", leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
    body_frame = Frame(LM, BM, CW, PH - TM - BM + 4 * mm, id="bf", leftPadding=0, rightPadding=0, topPadding=0,
                       bottomPadding=0)
    doc.addPageTemplates([PageTemplate("cover", [cover_frame], onPage=draw_cover),
                          PageTemplate("body", [body_frame], onPage=draw_body)])
    doc.build([Spacer(1, 1), NextPageTemplate("body"), PageBreak()] + R.story)
    print("built", R.out)


# ------------------------------------------------------------------ flyer
@dataclass
class Flyer:
    number: str
    out: str
    kicker: str
    title_lines: list
    subtitle: str
    quote_lines: list
    attribution: str
    context: str
    note: str
    verdict: str
    verdict_right: list          # two short italic lines
    cards: list                  # 5 tuples (big, colour, title, text)
    fair: str
    asks: list                   # 4 short requests
    footer: str
    pdf_title: str


def build_flyer(F: Flyer):
    W, H = A4
    M = 20 * mm
    FW = W - 2 * M
    vkind, _, vcols, mlabels, vi = scale_of(F.verdict)
    os.makedirs(os.path.dirname(F.out), exist_ok=True)
    c = rl_canvas.Canvas(F.out, pagesize=A4)
    c.setTitle(F.pdf_title)
    c.setAuthor("Miżien")

    def para(x, y_top, text, font, size, color, width, leading=None):
        leading = leading or size * 1.28
        lines = simpleSplit(text, font, size, width)
        c.setFillColor(color)
        c.setFont(font, size)
        y = y_top - size * 0.86
        for ln in lines:
            c.drawString(x, y, ln)
            y -= leading
        return y + leading - size * 0.14

    band_h = 72 * mm
    c.setFillColor(GREEN)
    c.rect(0, H - band_h, W, band_h, stroke=0, fill=1)
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
    c.drawString(M, H - 21 * mm, "MIŻIEN")
    c.setFillColor(LIGHTGREEN)
    c.setFont("Sans", 8.5)
    c.drawString(M + 19 * mm, H - 21 * mm, f"Claim Check {F.number}  ·  {F.kicker}")
    c.setFillColor(colors.white)
    c.setFont("Serif-B", 30)
    for i, line in enumerate(F.title_lines):
        c.drawString(M, H - 36 * mm - i * 10 * mm, line)
    c.setFillColor(colors.HexColor("#CFE2D4"))
    c.setFont("Serif-I", 11.5)
    c.drawString(M, H - 55 * mm, F.subtitle)

    card_top = H - 62 * mm
    card_h = 44 * mm
    card_y = card_top - card_h
    c.setFillColor(CREAM)
    c.roundRect(M, card_y, FW, card_h, 3 * mm, stroke=0, fill=1)
    c.setStrokeColor(RULE)
    c.setLineWidth(0.6)
    c.roundRect(M, card_y, FW, card_h, 3 * mm, stroke=1, fill=0)
    c.setFillColor(AMBER)
    c.rect(M, card_y, 2.6 * mm, card_h, stroke=0, fill=1)
    c.setFillColor(GREY)
    c.setFont("Sans-B", 7.6)
    c.drawString(M + 9 * mm, card_top - 8 * mm, "THE CLAIM")
    c.setFillColor(GREEN)
    qs = 18 if len(F.quote_lines) <= 2 else 15
    c.setFont("Serif-BI", qs)
    for i, line in enumerate(F.quote_lines):
        c.drawString(M + 9 * mm, card_top - 17 * mm - i * (qs * 0.42) * mm, line)
    c.setFillColor(SLATE)
    c.setFont("Sans-B", 8.2)
    c.drawString(M + 9 * mm, card_top - 31.5 * mm, F.attribution)
    c.setFont("Sans", 7.8)
    c.drawString(M + 9 * mm, card_top - 36.3 * mm, F.context)
    c.setFont("Sans-I", 7.4)
    c.setFillColor(GREY)
    c.drawString(M + 9 * mm, card_top - 40.6 * mm, F.note)

    vt = card_y - 6 * mm
    vh = 25 * mm
    c.setFillColor(vcols[vi])
    c.roundRect(M, vt - vh, FW, vh, 3 * mm, stroke=0, fill=1)
    c.setFillColor(colors.white)
    c.setFont("Sans-B", 8)
    c.drawString(M + 7 * mm, vt - 7 * mm, vkind.upper())
    # Leave a clear gutter before the right-hand summary for longer verdicts.
    c.setFont("Sans-B", 20 if len(F.verdict) > 13 else 25)
    c.drawString(M + 7 * mm, vt - 17.5 * mm, F.verdict.upper())
    c.setFont("Serif-BI", 14)
    c.drawRightString(W - M - 7 * mm, vt - 11 * mm, F.verdict_right[0])
    c.drawRightString(W - M - 7 * mm, vt - 17.5 * mm, F.verdict_right[1])

    my = vt - vh - 14 * mm
    gap = 1.6 * mm
    sw = (FW - (len(mlabels) - 1) * gap) / len(mlabels)
    mh = 9.5 * mm
    for i, (l1, l2) in enumerate(mlabels):
        x = M + i * (sw + gap)
        c.setFillColor(vcols[i])
        if i == vi:
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
    mx = M + vi * (sw + gap) + sw / 2
    c.setFillColor(SLATE)
    p = c.beginPath()
    p.moveTo(mx - 2 * mm, my + mh + 4.4 * mm)
    p.lineTo(mx + 2 * mm, my + mh + 4.4 * mm)
    p.lineTo(mx, my + mh + 1.6 * mm)
    p.close()
    c.drawPath(p, stroke=0, fill=1)

    def section(y, label):
        c.setFillColor(GREEN)
        c.setFont("Sans-B", 10.5)
        c.drawString(M, y, label)
        c.setStrokeColor(SAGE)
        c.setLineWidth(0.8)
        c.line(M, y - 2 * mm, W - M, y - 2 * mm)
        c.setStrokeColor(AMBER)
        c.setLineWidth(2.4)
        c.line(M, y - 2 * mm, M + 22 * mm, y - 2 * mm)

    ry = my - 7 * mm
    section(ry, "MAIN RESULTS")
    gx = 4 * mm
    cwid = (FW - 2 * gx) / 3
    chh = 36.5 * mm
    top1 = ry - 6 * mm
    pale = {GREEN: PALE, ORANGE: ORANGE_PALE, RED: RED_PALE, AMBER: AMBER_PALE}
    for i, (big, bc, t, tx) in enumerate(F.cards):
        x = M + (i % 3) * (cwid + gx)
        ytop = top1 - (i // 3) * (chh + gx)
        c.setFillColor(pale.get(bc, GREY_PALE))
        c.roundRect(x, ytop - chh, cwid, chh, 2.4 * mm, stroke=0, fill=1)
        c.setFillColor(bc)
        c.rect(x, ytop - 1.4 * mm, cwid, 1.4 * mm, stroke=0, fill=1)
        c.setFont("Sans-B", 16)
        c.drawString(x + 4 * mm, ytop - 11 * mm, big)
        c.setFillColor(SLATE)
        c.setFont("Sans-B", 8.4)
        c.drawString(x + 4 * mm, ytop - 16.6 * mm, t)
        para(x + 4 * mm, ytop - 19.2 * mm, tx, "Sans", 7.7, SLATE, cwid - 8 * mm, leading=9.8)
    x = M + 2 * (cwid + gx)
    ytop = top1 - (chh + gx)
    c.setFillColor(AMBER_PALE)
    c.roundRect(x, ytop - chh, cwid, chh, 2.4 * mm, stroke=0, fill=1)
    c.setFillColor(AMBER)
    c.rect(x, ytop - chh, 1.6 * mm, chh, stroke=0, fill=1)
    c.setFillColor(SLATE)
    c.setFont("Sans-B", 8.4)
    c.drawString(x + 5 * mm, ytop - 8 * mm, "FAIR TO SAY")
    para(x + 5 * mm, ytop - 11 * mm, F.fair, "Sans", 7.7, SLATE, cwid - 9 * mm, leading=9.8)

    sy = top1 - 2 * chh - gx - 8 * mm
    section(sy, "WHAT WOULD SETTLE IT")
    col_w = (FW - 6 * mm) / 2
    for i, a in enumerate(F.asks):
        x = M + (i % 2) * (col_w + 6 * mm)
        yy = sy - 8 * mm - (i // 2) * 11 * mm
        c.setStrokeColor(GREEN)
        c.setLineWidth(1)
        c.rect(x, yy - 3.2 * mm, 3.4 * mm, 3.4 * mm, stroke=1, fill=0)
        para(x + 6 * mm, yy + 0.4 * mm, a, "Sans", 8.2, SLATE, col_w - 6 * mm, leading=10.2)

    fh = 17 * mm
    c.setFillColor(GREEN)
    c.rect(0, 0, W, fh, stroke=0, fill=1)
    c.setFillColor(AMBER)
    c.setFont("Sans-B", 7.6)
    c.drawString(M, 12.4 * mm, BYLINE)
    contest = "CONTEST A VERDICT:  github.com/leandergrech/Mizien/issues"
    c.drawRightString(W - M, 12.4 * mm, contest)
    c.linkURL(CONTEST_URL, (W - M - pdfmetrics.stringWidth(contest, "Sans-B", 7.6), 11.4 * mm, W - M, 15.2 * mm),
              relative=0)
    c.setFillColor(LIGHTGREEN)
    c.setFont("Sans", 7.2)
    c.drawString(M, 8.3 * mm, "Full report, data and references:  github.com/leandergrech/Mizien")
    c.linkURL(REPO_URL, (M, 7.4 * mm, M + 75 * mm, 10.6 * mm), relative=0)
    c.drawString(M, 4.4 * mm, F.footer)
    c.showPage()
    c.save()
    print("saved", F.out)


def flyer_png(pdf, png, dpi=200):
    """Render the flyer PDF to PNG with pdftoppm (poppler-utils)."""
    import subprocess
    base = png[:-4]
    subprocess.run(["pdftoppm", "-png", "-r", str(dpi), "-singlefile", pdf, base], check=True)
    print("saved", png)
