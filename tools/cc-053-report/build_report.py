"""Claim Check 053 report. Run calc.py and figures.py first. Output: out/report.pdf"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import *  # noqa: E402,F401

FIG = HERE / "out"
S = []
S += [SectionHeading(None, "TL;DR"), Spacer(1, 1 * mm),
      P("A University of Malta team measured the brightness of the night sky across the islands and reported, in the "
        "<i>Journal of Environmental Management</i> (2020), <b>“87% of the area registering a NSB &lt; 20.39 "
        "mag<sub>SQM</sub>/arcsec² (Bortle Class 5 or higher) … with the Milky Way being visible for only 12.8% of the "
        "area”</b>. News reports rounded this to “13%”. We checked that the summary matches the study and that the "
        "study’s numbers hold together.", lead)]
S.append(key_points([
    ("The summary matches the study.",
     "The paper gives 12.8% (Bortle class 4 threshold) or 13.5% (the world atlas threshold); “about 13%” is fair. "
     "87% is the share of land in Bortle classes 5–9, as stated."),
    ("The study’s numbers hold together and agree with the world atlas.",
     "Weighting the island results by land area gives 11.6% (the paper weights its 347 survey cells, giving 12.8%). "
     "The 2016 world atlas of night-sky brightness gave 11% for Malta."),
    ("The threshold matters.",
     "On the paper’s own sensitivity test, the visible share is 6.3% to 25.9% depending on the brightness threshold "
     "chosen. “About 13%” uses a standard, stated threshold."),
    ("The data are from 2017–2019.",
     "Measurements are from 2017–2019. On the island of Malta the class 4 area fell from 3.9% to 1.6% between the two "
     "surveys. We found no newer survey."),
    ("Verdict: supported (high confidence).", "The statement reports a peer-reviewed measurement accurately."),
]))
S += [Spacer(1, 2.5 * mm), VerdictMeter(0), Spacer(1, 3 * mm),
      tiles([("12.8%", GREEN, "Area where the Milky Way is visible, 2017/18 (Bortle class 4)"),
             ("87%", RED, "Area in Bortle class 5 or brighter"),
             ("11%", GREY, "The same measure in the 2016 world atlas"),
             ("1.6%", ORANGE, "Class 4 area on the island of Malta in 2018/19 (3.9% a year earlier)")]),
      Spacer(1, 4 * mm),
      up_down("None: Supported is the top of the scale.",
              "A newer survey showing a different share, or a finding that the study’s method misclassifies large areas."),
      Spacer(1, 3 * mm)]
S += toc([("1", "The claim and what we could verify"), ("2", "Method"), ("3", "What the data show"),
          ("4", "Where the evidence points different ways"), ("5", "Testing the claim"),
          ("6", "Verdict and requests for evidence"), ("7", "Limitations")])
S.append(PageBreak())

S.append(SectionHeading(1, "The claim and what we could verify"))
S.append(P("The claim record came from a MaltaToday headline, “Milky Way only visible from 13% of Malta”, which "
           "summarised the study. Following our rule to quote the speaker, not the headline, we read the study itself: "
           "Caruana, Vella, Spiteri, Nolle, Fenech and Aquilina (2020), “A photometric mapping of the night sky brightness "
           "of the Maltese islands”, <i>Journal of Environmental Management</i> 261:110196 [1], in its accepted version on "
           "arXiv [2]. The quoted wording is the paper’s abstract."))
S.append(std_table([
    [C("Source", cellh), C("What it says", cellh), C("Our access", cellh), C("Status", cellh)],
    [C("<b>Caruana et al.</b> (2020), J. Environ. Manage. [1, 2]"),
     C("“87% of the area registering a NSB &lt; 20.39 … with the Milky Way being visible for only 12.8% of the area”; "
       "13.5% on the world atlas threshold."), C("Accepted manuscript read in full (arXiv)."), C("<b>The claim</b>")],
    [C("<b>Falchi et al.</b> (2016), Science Advances [3]"), C("World atlas of artificial night-sky brightness: 11% "
       "for Malta (as cited by Caruana et al.)."), C("Crossref verified; figure as cited ◆."), C("Comparison")],
    [C("<b>MaltaToday</b> [4]"), C("“Milky Way only visible from 13% of Malta”."), C("Locator only (site refuses "
       "automated access)."), C("Locator")],
], [38 * mm, 74 * mm, 36 * mm, 22 * mm]))

S += [Spacer(1, 4 * mm), SectionHeading(2, "Method")]
S.append(P("<b>Question.</b> Does the statement report the study accurately, and are the study’s results consistent?"))
S.append(P("<b>Evidence.</b> We transcribed the study’s Table 1 (share of land area in each Bortle class, by island) "
           "into <i>data/cc-053/caruana2020_table1.csv</i> and recomputed the archipelago-wide shares by weighting each "
           "island by its land area from OpenStreetMap (<i>tools/cc-053-report/calc.py</i>; outputs in "
           "<i>data/cc-053/checks.csv</i>). We compared the result with the paper’s own comparison to the 2016 world "
           "atlas and with its threshold sensitivity test."))
S.append(P("<b>Grades.</b> Caruana et al. (2020): B (observational measurement with a stated method and comparison). "
           "<b>Verdicts</b> follow the five-point scale in Appendix A."))

S.append(CondPageBreak(120 * mm))
S.append(SectionHeading(3, "What the data show"))
S.append(KeepTogether([fig(FIG / "fig1_bortle.png", width=CW * 0.98),
                       P("Figure 1. Share of land area in each Bortle class by island (Caruana et al. 2020, Table 1).", cap)]))
S.append(P("No part of the islands reached Bortle class 3 or darker. Class 4, where the Milky Way is clearly visible, "
           "covered 3.9% of Malta, 37.2% of Gozo and 83.3% of Comino in 2017/18, 12.8% of the islands overall. Weighting "
           "by land area gives 11.6%; the paper weights its one-kilometre survey cells, which include coastal cells, so "
           "the darker coasts count for slightly more. On the island of Malta, the second survey (2018/19) found class 4 "
           "had shrunk to 1.6%."))

S.append(Spacer(1, 4 * mm))
S.append(SectionHeading(4, "Where the evidence points different ways"))
S.append(contested("Is “13%” the right number?", "YES, ON A STATED THRESHOLD", GREENC,
                   "12.8% on the Bortle class 4 threshold, 13.5% on the world atlas threshold; the world atlas itself "
                   "gave 11%.", "With a threshold of 20.6 mag/arcsec² the share is 6.3%; with 20.0 it is 25.9%. The "
                   "measurements are from 2017–2019.",
                   "“About 13%” is accurate for the thresholds the study uses. It describes conditions in 2017–2019, "
                   "which may since have changed.", label_a="FOR", label_b="CAVEATS"))

S.append(CondPageBreak(90 * mm))
S.append(SectionHeading(5, "Testing the claim"))
verd = lambda t, c: chip(t, c, w=29 * mm)
S.append(std_table([
    [C("Sub-claim", cellh), C("Said by", cellh), C("What the evidence shows", cellh), C("Rating", cellh)],
    [C("<b>A.</b> The Milky Way is visible from only about 13% of the islands"), C("UM researchers [1]"),
     C("12.8% (class 4) or 13.5% (atlas threshold); 11.6% area-weighted; world atlas 11%."), verd("ACCURATE", GREENC)],
    [C("<b>B.</b> 87% of the area has high light pollution"), C("UM researchers [1]"),
     C("87.2% of the area in Bortle class 5 or brighter, 2017/18."), verd("ACCURATE", GREENC)],
], [42 * mm, 18 * mm, 76 * mm, 34 * mm], valign="MIDDLE"))

S += [Spacer(1, 6 * mm), SectionHeading(6, "Verdict and requests for evidence"),
      verdict_box("Supported", "The statement reports a peer-reviewed measurement accurately. Confidence: high."),
      Spacer(1, 4 * mm)]
S.append(P("<b>Why.</b> Both figures are the study’s own, the study’s parts add up, and an independent atlas agrees. "
           "<b>What this verdict does not say.</b> It does not describe the sky in 2026: the survey has not been repeated "
           "nationally since 2019."))
S.append(P("Evidence we are asking for", h2))
S.append(requests_list(["From the University of Malta team or ERA: any repeat survey of night-sky brightness since 2019.",
                        "From ERA and the Planning Authority: the status of national lighting guidelines."]))
S += [Spacer(1, 4 * mm),
      callout([P("RIGHT OF REPLY", tag), P("Not needed for this verdict (maintainer rule of 5 October 2026).", small)],
              bg=AMBER_PALE, bar=AMBER)]
S += [Spacer(1, 6 * mm), SectionHeading(7, "Limitations")]
for l in ["We read the accepted manuscript on arXiv; the published version may differ slightly in wording.",
          "The world atlas figure (11%) is as reported by Caruana et al.; we did not recompute it.",
          "Sky Quality Meter readings vary with season, cloud and the Milky Way’s position; the study discusses these."]:
    S.append(P("• " + l, bul))
S += [Spacer(1, 6 * mm), SectionHeading(None, "References")]
S += references([
    ("1", "Caruana J., Vella R., Spiteri D., Nolle M., Fenech S. & Aquilina N.J. (2020). A photometric mapping of the night "
          "sky brightness of the Maltese islands. <i>Journal of Environmental Management</i> 261:110196. "
          "doi:10.1016/j.jenvman.2020.110196.", "https://doi.org/10.1016/j.jenvman.2020.110196"),
    ("2", "Same, accepted manuscript. arXiv:2002.04435.", "https://arxiv.org/abs/2002.04435"),
    ("3", "Falchi F., Cinzano P., Duriscoe D., Kyba C.C.M. et al. (2016). The new world atlas of artificial night sky "
          "brightness. <i>Science Advances</i> 2(6):e1600377. doi:10.1126/sciadv.1600377.", "https://doi.org/10.1126/sciadv.1600377"),
    ("4", "MaltaToday. Milky Way only visible from 13% of Malta (locator).",
     "https://www.maltatoday.com.mt/news/national/100416/milky_way_only_visible_from_13_of_malta"),
    ("5", "MiŻien. Data and calculation: data/cc-053/; tools/cc-053-report/calc.py.", ""),
])
S.append(PageBreak())
S += appendix_a("A experiment · B observational study with a control or gradient · C review, guidance or "
                "official statistics · D assertion or anecdote. ◆ marks a source known only second-hand.")
S += [Spacer(1, 5 * mm)]
S += revision_log([("1.0", "5 Oct 2026", "First issue. Verdict Supported (high confidence); no right of reply needed.")])

build_report(Report(
    number="053", out=str(FIG / "report.pdf"), kicker="Environmental science",
    title_lines=["Milky Way", "visible from 13%", "of Malta?"],
    subtitle_lines=["Testing a University of Malta study of night-sky", "brightness, and how it was reported"],
    quote_lines=["“…87% of the area registering a NSB < 20.39 (Bortle Class 5", "or higher) … with the Milky Way being visible for only",
                 "12.8% of the area.”"], quote_size=13.5,
    attribution="Caruana et al., Journal of Environmental Management, 2020 (University of Malta).",
    context="Reported in the news as “Milky Way only visible from 13% of Malta”.",
    verdict="Supported", verdict_note="Accurately reports a peer-reviewed measurement from 2017–2019",
    footer_lines=["Version 1.0  ·  5 October 2026", "Status: no right of reply needed",
                  "Prepared from published research.", "Repository: github.com/leandergrech/Mizien"],
    running_head="Night-sky brightness – University of Malta study", version="1.0", date="5 October 2026",
    status_note="no right of reply needed",
    pdf_title="Milky Way visible from 13% of Malta? Claim Check 053",
    pdf_subject="Tests the reported finding that the Milky Way is visible from about 13% of the Maltese islands",
    story=S))
