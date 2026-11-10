"""Claim Check 157 report. Run calc.py and figures.py first. Output: out/report.pdf"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import *  # noqa: E402,F401

FIG = HERE / "out"
S = []
LG = colors.HexColor("#8DB36B")

S += [SectionHeading(None, "TL;DR"), Spacer(1, 1 * mm),
      P("On 18 July 2025 Business Now reported that extreme heat could cut Malta’s GDP by more than 2.5% in "
        "2055–2064, citing a Nature Communications study by David García-León and colleagues. The outlet states a "
        "projection from a published paper, so we checked the paper. It is open access and we read it in full. "
        "Malta is not named in its text; Malta is one row of Figure 4b. Measured from that figure, the paper "
        "projects a Malta loss of <b>about 2.8% of GDP a year in 2055–2064</b>, the fourth largest of the 29 entries "
        "plotted, under a high-emissions climate scenario and with no further adaptation by firms and households.", lead)]
S.append(key_points([
    ("The number holds.",
     "Malta’s value in Figure 4b is about −2.8% (±0.1 percentage points from our measurement), beyond the 2.5% "
     "in the claim. Only Cyprus, Croatia and Portugal are higher."),
    ("It is a model projection, not a forecast.",
     "It uses two regional climate models under RCP8.5, a fixed economy and no extra adaptation such as more air "
     "conditioning; the authors list five gaps, including heat-island effects and sector detail."),
    ("The source is from 2021.",
     "The study was published on 4 October 2021, not in 2025; the outlets reported it as current research. "
     "Nothing in the Business Now sentence says it is new."),
    ("Not published as a table.",
     "The paper gives no country table for Malta; the figure was measured by pixel, and no Malta-specific "
     "uncertainty range is given."),
    ("Verdict: largely supported (moderate confidence).",
     "The central figure and its conditions match the study; caveats are the approximate reading, the scenario "
     "and the model limits."),
]))
S += [Spacer(1, 2.5 * mm), VerdictMeter(1), Spacer(1, 3 * mm),
      tiles([("−2.8%", ORANGE, "Malta’s projected annual GDP loss from heatwaves, 2055–2064 (read from Fig. 4b)"),
             ("2.5%", GREEN, "Threshold in the claim (“exceeding”)"),
             ("4th", RED, "Malta’s rank among 29 plotted entries (largest losses: Cyprus, Croatia, Portugal)"),
             ("−1.1%", GREY, "Europe-wide average in the 2060s, stated in the paper (0.21% in 1981–2010)")]),
      Spacer(1, 4 * mm),
      up_down("Nothing: the top of the scale is Supported; a published country table with Malta’s value and range would "
              "firm up the confidence.",
              "A Malta value below 2.5% in the paper’s data or a correction; or evidence that the study’s Malta "
              "figure rests on a different scenario from the one described."),
      Spacer(1, 3 * mm)]
S += toc([("1", "The claim and what we could verify"), ("2", "Method"), ("3", "What the study says"),
          ("4", "What Malta’s value is"), ("5", "Where the evidence points different ways"),
          ("6", "Testing the claim"), ("7", "Verdict and requests for evidence"), ("8", "Limitations")])
S.append(PageBreak())

S.append(SectionHeading(1, "The claim and what we could verify"))
S.append(P("The statement is Business Now’s, published on 18 July 2025 [1]. Our own read of the page on 10 November 2026 "
           "came through a summarising tool (the site blocks scripted access), so we did not re-confirm its exact "
           "wording. The sentence recorded in the claim file, from an earlier read, is “GDP impacts from extreme heat "
           "exceeding -2.5 per cent by the 2055-2064 period”. Euronews, which Business Now cites, carries the same "
           "figure [2], also seen only through a summarising tool (◆ second-hand). The study behind both is "
           "García-León et al. [3]."))
S.append(std_table([
    [C("What was said", cellh), C("Who", cellh), C("Access", cellh)],
    [C("GDP impacts from extreme heat “exceeding -2.5 per cent” by 2055–2064, for Malta (claim file)"),
     C("Business Now [1]"), C("Summary only; wording from earlier read")],
    [C("Impacts “reaching or exceeding -2.5% of GDP by the 2055–2064 period” for countries including Malta"),
     C("Euronews [2] ◆"), C("Summary only ◆")],
    [C("The projection itself"), C("García-León et al. [3]"), C("Full text read")],
], [100 * mm, 36 * mm, 34 * mm]))
S += [Spacer(1, 4 * mm),
      callout([P("SCOPE NOTE", tag),
               P("We rate the statement that the study projects a loss beyond 2.5% for Malta, and what the study "
                 "shows. We do not rate whether the model is right about 2055–2064, which no one can yet observe. "
                 "The outlet’s wording is rated as written; the quoted headline is the outlet’s, not the authors’.",
                 small)], bg=AMBER_PALE, bar=AMBER), Spacer(1, 4 * mm)]

S.append(SectionHeading(2, "Method"))
S.append(P("<b>Question.</b> Does the cited study project a Malta GDP loss from extreme heat of more than 2.5% in "
           "2055–2064, and under what conditions?"))
S.append(P("<b>Evidence.</b> The paper and its Supplementary Information were read in full text [3]; its DOI, title "
           "and authors were verified in Crossref and its open-access status in OpenAlex. Malta’s value was measured "
           "from Figure 4b (published under CC BY 4.0) with <i>tools/cc-157-report/calc.py</i>, calibrated on the "
           "figure’s axis ticks; readings are saved in <i>data/cc-157/</i>."))
S.append(P("<b>Grades.</b> A peer-reviewed modelling study is grade B: it is a model with a published method, not an "
           "observation. News reports are grade D as evidence (they locate the claim). <b>Verdicts</b> follow "
           "Appendix A."))

S.append(CondPageBreak(60 * mm))
S.append(SectionHeading(3, "What the study says"))
S.append(P("The authors translate heat stress (a wet-bulb globe temperature index) into lost working capacity and feed "
           "it into a regional economic model covering 274 regions [3]. Historically, heatwaves in 2003, 2010, 2015 and "
           "2018 cost Europe 0.3–0.5% of GDP in those years, against about 0.2% in an average year. For the future, "
           "two regional climate models under the high-emissions scenario RCP8.5 give an average loss of 0.77% "
           "in 2035–2045 and “beyond 1.14%” in the 2060s for Europe as a whole."))
S.append(P("Countries differ widely. The text names Cyprus, Portugal, Spain and Croatia as moving to around 3% by 2060, and "
           "the Balkans, Italy and Greece above 2% in 2055–2064; the UK, Iceland and Scandinavia lose 0–0.2% [3]. "
           "Malta is not named; it appears in Figure 4b."))
S.append(P("The study says what it leaves out: it “does not consider” adaptation such as air conditioning, though "
           "the authors argue it matters little outdoors; it omits heat-related injuries and the urban heat island; "
           "and the heat functions rest on a few empirical studies [3]."))

S.append(CondPageBreak(150 * mm))
S.append(SectionHeading(4, "What Malta’s value is"))
S.append(fig(FIG / "fig1_countries.png"))
S.append(P("Figure 1. Projected annual GDP loss from heatwaves in 2055–2064 for the fourteen largest losses among the "
           "29 entries in Figure 4b of the study [3] (EFTA is plotted as one group). Values are measured from the "
           "published image and are approximate (about ±0.1 percentage points).", cap))
S.append(std_table([
    [C("Indicator", cellh), C("Value", cellh), C("Source", cellh), C("Grade", cellh)],
    [C("Malta, 2055–2064"), C("<b>≈ −2.8%</b> of GDP a year (read from figure)"), C("Fig. 4b [3]; calc.py"), grade_tag("B")],
    [C("Claim threshold"), C("exceeding 2.5%"), C("Business Now [1]"), grade_tag("D")],
    [C("Cyprus, Croatia, Portugal"), C("≈ 3.4%, 3.1%, 3.0%"), C("Fig. 4b [3]"), grade_tag("B")],
    [C("Europe, 2060s (stated)"), C("beyond 1.14% (s.d. 0.25%)"), C("Text [3]"), grade_tag("B")],
    [C("Europe, 1981–2010 (stated)"), C("0.21%"), C("Text [3]"), grade_tag("B")],
], [48 * mm, 62 * mm, 48 * mm, 12 * mm]))
S.append(P("All values in <i>data/cc-157/checks.csv</i> and <i>fig4b_readings.csv</i>. The loss is relative to a "
           "no-heatwave baseline, with the economic structure held at today’s.", cap))
S.append(P("Malta is not mentioned in the paper’s text and no table of country values is published; the model’s economic "
           "data are licensed (GTAP) and “available from the authors upon reasonable request” [3]. The measurement is "
           "therefore the best available reading of the published figure, and a reader should treat 2.8% as "
           "“between about 2.7% and 2.9%”."))

S.append(CondPageBreak(120 * mm))
S.append(SectionHeading(5, "Where the evidence points different ways"))
S.append(contested(
    "Q1  Is Malta’s loss “exceeding 2.5%”?", "YES, ON THE FIGURE", GREEN,
    "Figure 4b puts Malta at about −2.8% in 2055–2064, beyond −2.5%, fourth of 29 entries. Malta’s earlier "
    "values on the same plot are far smaller, so the loss grows sharply in the model.",
    "The value is a reading of a dot plot, not a published number; the margin above 2.5% is about 0.3 points, "
    "larger than our measurement error but not large against the model’s own spread, which is not shown for Malta. "
    "Europe-wide, the interannual spread (s.d.) is about ±0.25 points in the 2060s.",
    "<b>For this claim:</b> the figure is consistent with the claim’s threshold, with a modest margin."))
S.append(contested(
    "Q2  “If there is no further adaptation or mitigation”", "PARTLY: CONDITION IS SCENARIO-DEPENDENT", AMBER,
    "The headline Malta value belongs to the RCP8.5 high-emissions run with no extra adaptation: the "
    "“no further mitigation” reading matches.",
    "The authors say the two climate models give a very similar signal “irrespectively of the emission scenario” "
    "for the next four decades and diverge after 2050, and that productivity losses will rise “even if stringent "
    "mitigation pathways were adopted”. They also say there are “big margins for adaptation”. We did not read the "
    "Supplementary Discussion that compares scenarios, so we cannot say what Malta’s value is under lower emissions.",
    "<b>For this claim:</b> the condition is stated and correct for the figure shown; the claim does not say that "
    "lower-emission paths would also leave large losses, which the authors suggest (rising losses)."))
S.append(contested(
    "Q3  Is this current research?", "NO: 2021 STUDY", AMBER,
    "The statement says what the study projects and does not call the study new.",
    "The paper dates from 4 October 2021 and the outlets reported it in July 2025; we did not search for a newer "
    "study with a Malta value (see notes), and the Business Now text did not link the paper.",
    "<b>For this claim:</b> no effect on the figure; readers may assume the work is more recent."))

S.append(CondPageBreak(110 * mm))
S.append(SectionHeading(6, "Testing the claim"))
verd = lambda t, c: chip(t, c, w=29 * mm)
S.append(std_table([
    [C("Sub-claim", cellh), C("What the evidence shows", cellh), C("Rating", cellh)],
    [C("<b>A.</b> The study projects a Malta GDP loss from extreme heat exceeding 2.5% in 2055–2064"),
     C("Figure 4b: about −2.8% (±0.1 pp, measured) [3]."), verd("SUPPORTED", GREENC)],
    [C("<b>B.</b> Condition: if there is no further adaptation or mitigation"),
     C("Correct for the RCP8.5 run with no extra adaptation; other scenarios not read; authors expect rising losses "
       "also under stringent mitigation [3]."), verd("LARGELY SUPPORTED", LG)],
    [C("<b>C.</b> The sentence’s framing as a current projection"),
     C("Study is from 2021; no newer paper searched for."), verd("NOT RATED", GREY)],
], [52 * mm, 88 * mm, 30 * mm], valign="MIDDLE"))

S += [Spacer(1, 6 * mm), SectionHeading(7, "Verdict and requests for evidence"),
      verdict_box("Largely supported", "The study does project a Malta loss beyond 2.5%; the value is approximate and "
                  "scenario-bound. Confidence: moderate."), Spacer(1, 4 * mm)]
S.append(P("<b>Why.</b> (1) The study’s own figure puts Malta at about 2.8%, beyond the claim’s 2.5% (Section 4). "
           "(2) The conditions in the sentence match the model’s set-up. (3) The number is read from a figure, "
           "has no Malta uncertainty range, depends on a fixed economy and on the scenario, and the study is "
           "four years older than the reports. These caveats limit the claim but do not reverse it, which our scale calls "
           "<i>Largely supported</i>."))
S.append(P("<b>What this verdict does not say.</b> It does not say that Malta will lose 2.8% of GDP: it says a published "
           "model projects that under stated assumptions. It does not assess Malta’s heat policy."))
S.append(P("Evidence we are asking for", h2))
S.append(requests_list([
    "The authors’ Malta value and its model range for 2055–2064 under each climate scenario.",
    "Any newer study with a Malta estimate, with its scenario and treatment of adaptation.",
    "The link from Business Now to the paper it relies on.",
]))

S += [Spacer(1, 6 * mm), SectionHeading(8, "Limitations")]
for l in ["Malta’s value is measured from an image of a dot plot (about ±0.1 percentage points); the paper does not "
          "tabulate it.",
          "Business Now and Euronews were read through a summarising tool, not as raw pages; the exact Business Now "
          "wording was not re-confirmed and the Euronews wording is second-hand (◆).",
          "We did not read the Supplementary Discussion on scenarios; our Supplementary file holds the region list only.",
          "We did not search the literature for newer Malta heat-and-GDP estimates.",
          "We test the statement against the study; we do not test the model’s validity for Malta."]:
    S.append(P("• " + l, bul))

S += [Spacer(1, 6 * mm), SectionHeading(None, "References")]
S += references([
    ("1", "Business Now (18 Jul 2025). Extreme heat set to leave 2.5% dent in Malta’s GDP by mid-century. (Read through a "
          "summarising tool, 10 Nov 2026.)",
     "https://businessnow.mt/extreme-heat-set-to-leave-2-5-dent-in-maltas-gdp-by-mid-century/"),
    ("2", "◆ Yanatma S. (15 Jul 2025). Heatwaves in Europe: which countries face the biggest GDP and labour productivity "
          "losses. <i>Euronews</i>. (Second-hand: summarising tool only.)",
     "https://www.euronews.com/business/2025/07/15/heatwaves-in-europe-which-countries-face-the-biggest-gdp-and-labour-productivity-losses"),
    ("3", "García-León D., Casanueva A., Standardi G., Burgstall A., Flouris A.D., Nybo L. (2021). Current and projected "
          "regional economic impacts of heatwaves in Europe. <i>Nature Communications</i> 12:5807. "
          "doi:10.1038/s41467-021-26050-z. (CC BY 4.0; full text and Supplementary Information read.)",
     "https://doi.org/10.1038/s41467-021-26050-z"),
    ("4", "MiŻien. Data and calculations: data/cc-157/; tools/cc-157-report/calc.py.", ""),
])
S.append(PageBreak())
S += appendix_a("A experiment · B observational or modelling study with a published method · C review, guidance or "
                "official statistics · D assertion or anecdote. ◆ marks a source known only second-hand.")
S += [Spacer(1, 5 * mm)]
S += revision_log([("1.0", "10 Nov 2026", "First issue. No right of reply needed.")])

build_report(Report(
    number="157", out=str(FIG / "report.pdf"), kicker="Climate and economy",
    title_lines=["Will heat cost", "Malta 2.5% of", "GDP?"],
    subtitle_lines=["Testing a reported projection of heatwave losses",
                    "against the study it cites"],
    quote_lines=["“GDP impacts from extreme heat", "exceeding -2.5 per cent by the 2055-2064", "period.”"], quote_size=15,
    attribution="Business Now, 18 July 2025, reporting García-León et al. (2021).",
    context="A projection for Malta, with no further adaptation or mitigation.",
    verdict="Largely supported", verdict_note="The study’s figure for Malta is about 2.8%; a model projection",
    footer_lines=["Version 1.0  ·  10 November 2026", "Status: no right of reply needed",
                  "Prepared from the open-access study and public sources.", "Repository: github.com/leandergrech/Mizien"],
    running_head="Heat and GDP – Malta", version="1.0", date="10 November 2026",
    pdf_title="Will heat cost Malta 2.5% of GDP? Claim Check 157",
    pdf_subject="Tests a reported projection that extreme heat could cut Malta's GDP by over 2.5% in 2055-2064",
    story=S))
