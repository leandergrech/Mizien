"""Claim Check 132 report. Run calc.py and figures.py first. Output: out/report.pdf"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import *  # noqa: E402,F401

FIG = HERE / "out"
S = []
LG = colors.HexColor("#8DB36B")

# ================================================================== TL;DR
S += [SectionHeading(None, "TL;DR"), Spacer(1, 1 * mm),
      P("The European Commission’s 2026 Country Report for Malta says: <b>“In 2024, 58% of people in Malta reported "
        "never using public transport, below the EU average of 50.6%”</b>. We compared it with the Eurostat survey table "
        "it cites. The figures are right to within a rounding gap, but the comparison word is not: Malta is "
        "<i>above</i> the EU average, not below it.", lead)]
S.append(key_points([
    ("The EU figure is exact.", "Eurostat gives 50.6% of people aged 16+ in the EU never using public transport in 2024."),
    ("Malta’s figure is 58.6%, not 58%.", "Eurostat’s table now shows 58.6% (rounds to 59%); a press report of the "
     "March release gave 58.0% <font name='DejaVu' size='6.5'>◆</font>. We could not retrieve the earlier vintage, so we cannot say which the Commission used."),
    ("“Below” is wrong.", "Malta is 8.0 points above the EU average and tied 7th highest of 27 (with Croatia); six "
     "states are higher. The sentence’s own numbers contradict its wording."),
    ("The point the sentence makes still stands.", "High non-use is consistent with the Annex’s view that bus "
     "measures have had limited reach, though the survey cannot show how effective any measure has been."),
    ("Verdict: largely supported (high confidence on the figures).",
     "The substance (many people in Malta never use public transport, more than the EU average) is backed by the data; "
     "one word reverses the comparison and should read “above”."),
]))
S += [Spacer(1, 2.5 * mm), VerdictMeter(1), Spacer(1, 3 * mm),
      tiles([("58.6%", RED, "Malta: people 16+ who never used public transport, 2024 (Commission: 58%)"),
             ("50.6%", GREEN, "EU-27 average, as the Commission wrote"),
             ("+8.0", ORANGE, "Percentage points Malta is above the EU average, not below"),
             ("7th", AMBER, "Malta’s rank of 27 (tied with Croatia); 6 states are higher")]),
      Spacer(1, 4 * mm),
      up_down("Nothing: Supported is the top of the scale. Only the word “below” and the 58% rounding stand between "
              "this and Supported; a corrected sentence would be Supported.",
              "Evidence that the Commission’s figures come from a different, published Eurostat series in which "
              "Malta was below the EU average (we found none); or that Eurostat’s “never” category is not what the "
              "sentence describes."),
      Spacer(1, 3 * mm)]
S += toc([("1", "The claim and what we could verify"), ("2", "Method"), ("3", "What the data show"),
          ("4", "Where the sources differ"), ("5", "Testing the claim"), ("6", "Verdict and requests for evidence"),
          ("7", "Limitations")])
S.append(PageBreak())

# ================================================================== 1
S.append(SectionHeading(1, "The claim and what we could verify"))
S.append(P("The sentence is in Annex 8 (transport) of the Commission’s 2026 Country Report for Malta, Commission staff "
           "working document SWD(2026) 218, dated 3 June 2026 and transmitted to the Council on 8 June 2026 [1]. We read "
           "it in the Council register copy (printed page 73, footnote 145). It follows a statement that Malta "
           "“has expanded free access to public transport for all holders of the Tallinja card”, increased bus routes "
           "and launched park and ride, and that “the effectiveness of these measures has been limited”. Footnote 145 cites "
           "the Eurostat news article “51% of people didn’t use public transport in 2024”, 11 March 2026 [2]."))
S.append(std_table([
    [C("What was said", cellh), C("Who", cellh), C("Access", cellh)],
    [C("“In 2024, 58% of people in Malta reported never using public transport, below the EU average of 50.6%”"),
     C("Commission staff [1]"), C("Read in full")],
    [C("“the effectiveness of these measures has been limited”"), C("Commission staff [1]"), C("Read in full")],
    [C("“51% of people didn’t use public transport in 2024”: EU-27 50.6%; Malta not named in the news text"),
     C("Eurostat [2]"), C("Read in full")],
], [104 * mm, 34 * mm, 32 * mm]))
S += [Spacer(1, 4 * mm),
      callout([P("SCOPE NOTE", tag),
               P("This check tests the sentence’s figures and comparison against Eurostat’s own table. It does not assess "
                 "Malta’s transport policy, the free-fare scheme or bus performance; those are the subject of "
                 "CC-069, CC-070 and CC-071.", small)], bg=AMBER_PALE, bar=AMBER), Spacer(1, 4 * mm)]

# ================================================================== 2
S.append(SectionHeading(2, "Method"))
S.append(P("<b>Question.</b> Are the 58% and 50.6% in the Commission’s sentence the figures Eurostat publishes, and is "
           "58% “below” 50.6%?"))
S.append(P("<b>Evidence.</b> Eurostat’s survey tables ilc_atst01 (persons using public transport by frequency) and ilc_atst02 "
           "(persons not using it regularly, by reason), for persons aged 16 or over, both sexes, 2024, for all 27 "
           "Member States and the EU aggregate [3, 4], retrieved through Eurostat’s dissemination API on 26 October 2026. "
           "All numbers are recomputed by <i>tools/cc-132-report/calc.py</i> from files in <i>data/cc-132/</i>. "
           "Eurostat’s news item [2] was read in full."))
S.append(P("<b>Grades.</b> Official statistics are grade C. <b>Verdicts</b> follow the five-point scale in Appendix A."))

# ================================================================== 3
S.append(CondPageBreak(150 * mm))
S.append(SectionHeading(3, "What the data show"))
S.append(fig(FIG / "fig1_never_use.png"))
S.append(P("Figure 1. Share of people aged 16+ who never used public transport in 2024, all 27 Member States. Malta "
           "(red) is above the EU-27 aggregate (dashed line) and tied with Croatia.", cap))
S.append(std_table([
    [C("Indicator, 2024, persons 16+", cellh), C("Malta", cellh), C("EU-27", cellh), C("Source", cellh), C("Grade", cellh)],
    [C("Never use public transport"), C("<b>58.6%</b>"), C("<b>50.6%</b>"), C("Eurostat ilc_atst01"), grade_tag("C")],
    [C("Malta minus EU-27"), C("<b>+8.0 points</b> (ratio 1.16)"), C("–"), C("calc.py"), grade_tag("C")],
    [C("Rank among the 27 (1 = highest never-use share)"), C("7th, tied with Croatia"), C("–"), C("ilc_atst01"), grade_tag("C")],
    [C("Use public transport every day"), C("9.9%"), C("10.7%"), C("ilc_atst01"), grade_tag("C")],
    [C("Use it every week"), C("9.7%"), C("11.6%"), C("ilc_atst01"), grade_tag("C")],
    [C("Use it every month"), C("7.5%"), C("10.0%"), C("ilc_atst01"), grade_tag("C")],
    [C("Use it less than once a month"), C("14.4%"), C("17.1%"), C("ilc_atst01"), grade_tag("C")],
], [62 * mm, 36 * mm, 24 * mm, 36 * mm, 12 * mm]))
S.append(P("All values in <i>data/cc-132/checks.csv</i>. Malta’s categories sum to 100.1 because of rounding. Eurostat "
           "attaches no quality flag to the Malta or EU values.", cap))
S.append(fig(FIG / "fig2_frequency.png"))
S.append(P("Figure 2. How often people use public transport, Malta and EU-27, 2024. Every frequency of use is lower in "
           "Malta than in the EU, and “never” is higher.", cap))
S.append(P("<b>Reasons.</b> Eurostat also publishes why people who do not use public transport regularly say they "
           "do not [4]. Among Maltese people who never use it, 82.0% give “other reason” (EU 62.0%), 7.7% a long commute "
           "(EU 4.8%), 6.0% the schedule (EU 12.7%), 0.1% that no service is available (EU 12.2%) and 0.0% financial "
           "reasons (EU 2.7%). The shares sum to 100 across Eurostat’s reasons, so we read them as shares of non-users. "
           "The dominant answer is uninformative, so these figures do not explain why use is low."))

# ================================================================== 4
S.append(CondPageBreak(100 * mm))
S.append(SectionHeading(4, "Where the sources differ"))
S.append(contested(
    "Q1  Is Malta’s figure 58%?", "CLOSE, NOT EXACT", AMBER,
    "A press report of Eurostat’s March 2026 release gives Malta as 58.0% <font name='DejaVu' size='6.5'>◆</font> [5] (second-hand: seen in a search summary; "
    "the article itself was not readable). The Commission’s 58% matches it.",
    "Eurostat’s table, read on 26 October 2026, gives 58.6% [3]; the table’s update stamp is 17 September 2026, after the "
    "news item, and we could not retrieve the earlier version. 58.6% rounds to 59%, not 58%.",
    "<b>For this claim:</b> the 58% is within 0.6 points of Eurostat’s current value; the difference does not change "
    "any conclusion. We do not know whether it is a data revision or a rounding choice."))
S.append(contested(
    "Q2  Is 58% “below” 50.6%?", "NO", RED,
    "Nothing in the data supports “below”: 58.6% is above 50.6%, and every other Eurostat frequency category shows "
    "Malta using public transport less than the EU does.",
    "The sentence’s own numbers give the reverse of its wording; the surrounding Annex text describes limited effect "
    "of the measures, which fits “above”.",
    "<b>For this claim:</b> the comparison word is wrong as printed. We make no claim about how it arose."))

# ================================================================== 5
S.append(CondPageBreak(90 * mm))
S.append(SectionHeading(5, "Testing the claim"))
verd = lambda t, c: chip(t, c, w=29 * mm)
S.append(std_table([
    [C("Sub-claim", cellh), C("What the evidence shows", cellh), C("Rating", cellh)],
    [C("<b>A.</b> In 2024, 58% of people in Malta reported never using public transport"),
     C("Eurostat: 58.6% (persons 16+) [3]; 58.0% in a press report of the March release <font name='DejaVu' size='6.5'>◆</font> [5].",), verd("CLOSE", LG)],
    [C("<b>B.</b> The EU average is 50.6%"), C("Eurostat: 50.6% (EU-27, persons 16+) [2, 3]."),
     verd("SUPPORTED", GREENC)],
    [C("<b>C.</b> Malta’s figure is “below” the EU average"),
     C("Malta is 8.0 points above the EU average, tied 7th highest of 27 [3]."), verd("CONTRADICTED", RED)],
    [C("<b>D.</b> The effectiveness of Malta’s public-transport measures “has been limited”"),
     C("Not tested. Low use is consistent with it, but a single-year survey cannot measure the effect of any measure."),
     verd("NOT TESTED", GREY)],
], [52 * mm, 88 * mm, 30 * mm], valign="MIDDLE"))

# ================================================================== 6
S += [Spacer(1, 6 * mm), SectionHeading(6, "Verdict and requests for evidence"),
      verdict_box("Largely supported", "Both figures are Eurostat’s to within a rounding gap; one word reverses the "
                  "comparison. Confidence: high on the figures."), Spacer(1, 4 * mm)]
S.append(P("<b>Why.</b> (1) The EU average of 50.6% is exactly Eurostat’s figure. (2) Malta’s share is 58.6% in Eurostat’s "
           "current table, against 58% in the report: a small gap. (3) “Below” is wrong, since 58.6% is 8.0 points "
           "<i>above</i> 50.6%. The substance, that Malta has a high share of people who never use public transport, "
           "is backed by the data and is what the surrounding text relies on. The word error is a material "
           "wording slip but not a different finding, which our scale calls <i>Largely supported</i>; the sub-claim "
           "on “below” is rated Contradicted on its own."))
S.append(P("<b>What this verdict does not say.</b> It does not say the free-fare scheme or the bus network works or "
           "fails, and it does not assess the sentence’s author."))
S.append(P("Evidence we are asking for", h2))
S.append(requests_list([
    "The Eurostat table version (or the Commission’s working file) that gives Malta as 58%.",
    "The survey question and reference period behind the “never” category (Eurostat’s metadata page was not "
    "retrievable by us).",
    "Any before-and-after survey that measures the effect of the 2022 free-fare scheme on use.",
]))

# ================================================================== 7
S += [Spacer(1, 6 * mm), SectionHeading(7, "Limitations")]
for l in ["We could not retrieve Eurostat’s metadata for these tables, so the exact survey question and reference "
          "period of “never” are not verified here; Eurostat’s own news item calls the category “did not use public "
          "transport”.",
          "Eurostat’s March 2026 vintage of the table was not available to us; Malta’s 58.0% in March is known only from "
          "a press report <font name='DejaVu' size='6.5'>◆</font> (second-hand).",
          "Survey estimates have sampling error; Eurostat’s table gives no confidence interval, so a 0.6-point difference "
          "is within what we would expect from revision or rounding.",
          "2024 is a single year: the data say nothing about trends or about the effect of any policy.",
          "The reasons table (ilc_atst02) is read as shares of non-users because the shares sum to 100; Eurostat’s "
          "denominator note was not retrieved."]:
    S.append(P("• " + l, bul))

S += [Spacer(1, 6 * mm), SectionHeading(None, "References")]
S += references([
    ("1", "European Commission (3 Jun 2026). 2026 Country Report – Malta, Annex 8, SWD(2026) 218 final; Council "
          "document ST 10135/2026 ADD 1, 8 Jun 2026. Printed p. 73, footnote 145. Read in full.",
     "https://data.consilium.europa.eu/doc/document/ST-10135-2026-ADD-1/en/pdf"),
    ("2", "Eurostat (11 Mar 2026). 51% of people didn’t use public transport in 2024. News article.",
     "https://ec.europa.eu/eurostat/web/products-eurostat-news/w/ddn-20260311-2"),
    ("3", "Eurostat. ilc_atst01: Persons using public transport by frequency, age, sex and risk of poverty or social "
          "exclusion; 2024; updated 17 Sep 2026; retrieved 26 Oct 2026.",
     "https://ec.europa.eu/eurostat/databrowser/view/ilc_atst01/default/table"),
    ("4", "Eurostat. ilc_atst02: Persons not using public transport regularly by reason, frequency, age, sex and "
          "risk of poverty or social exclusion; 2024; retrieved 26 Oct 2026.",
     "https://ec.europa.eu/eurostat/databrowser/view/ilc_atst02/default/table"),
    ("5", "<font name='DejaVu' size='6.5'>◆</font> The Malta Independent (11 Mar 2026). 58% of people in Malta did not use public transport in 2024. "
          "Second-hand: the page is 403 to scripts; the 58.0% figure was seen only in a search summary.",
     "https://www.independent.com.mt/articles/2026-03-11/local-news/58-of-people-in-Malta-did-not-use-public-transport-in-2024-Eurostat-6736287902"),
])

S.append(PageBreak())
S += appendix_a("A experiment · B observational study with a control or gradient · C review, guidance or "
                "official statistics · D assertion or anecdote. ◆ marks a source known only second-hand.")
S += [Spacer(1, 5 * mm)]
S += revision_log([("1.0", "26 Oct 2026", "First issue. No right of reply needed.")])

build_report(Report(
    number="132", out=str(FIG / "report.pdf"), kicker="Public transport",
    title_lines=["Is Malta below", "the EU on public", "transport use?"],
    subtitle_lines=["Testing a sentence in the Commission’s 2026 Country Report",
                    "against Eurostat’s own survey table"],
    quote_lines=["“58% of people in Malta reported never using", "public transport, below the EU average of 50.6%.”"],
    quote_size=14,
    attribution="European Commission, 2026 Country Report for Malta, 3 June 2026.",
    context="Annex 8 (transport), citing a Eurostat news article.",
    verdict="Largely supported", verdict_note="Figures close to Eurostat’s; “below” should read “above”",
    footer_lines=["Version 1.0  ·  26 October 2026", "Status: draft",
                  "Prepared from public sources and Eurostat data.", "Repository: github.com/leandergrech/Mizien"],
    running_head="Public transport non-use – Malta", version="1.0", date="26 October 2026",
    pdf_title="Is Malta below the EU on never using public transport? Claim Check 132",
    pdf_subject="Tests a sentence on public-transport non-use in the Commission's 2026 Country Report for Malta",
    story=S))
