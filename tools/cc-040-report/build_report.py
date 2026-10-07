"""Claim Check 040 report. Run calc.py and figures.py first. Output: out/report.pdf"""
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
      P("In a keynote to the 1st Island Water Congress (IWRA, 2024), Manuel Sapiano of the Energy and Water Agency "
        "showed a slide saying: <b>“Per capita water consumption, today stands at around 110l/cap/day.”</b> The "
        "previous slide says tariffs and engagement have “contributed to maintaining the per capita water "
        "consumption low”. We tested the figure against Eurostat’s household water-use series. It is close, but "
        "Eurostat’s estimate for Maltese households is higher, and Malta sits mid-table among the EU states that "
        "report. The keynote does not compare Malta with other countries; that framing came from the intake "
        "record, not from the speaker.", lead)]
S.append(key_points([
    ("The figure is about right.",
     "Eurostat puts Maltese households’ use of public water at 116–120 litres per person per day in 2022–2024 "
     "(an estimate, 9% above 110 in 2024), against “around 110” in the keynote."),
    ("It covers households only.",
     "All uses of the public supply, including services such as hotels, come to about 169–176 litres per head "
     "per day on the same basis, because the supply also serves tourists, shops and industry."),
    ("“Low” is not shown by this comparison.",
     "Among the 19 EU states with a recent household figure, Malta ranks 13th from the lowest, 8% above the median "
     "(111 l). The speaker made no EU comparison, so this does not contradict the keynote."),
    ("The tariff effect is untested.",
     "We found no evidence on how much the rising block tariff changed use; we did not obtain the tariff schedule."),
    ("Verdict: largely supported (moderate confidence).",
     "The central figure agrees with Eurostat within about 10%. “Low” is a qualitative word that the keynote does "
     "not benchmark."),
]))
S += [Spacer(1, 2.5 * mm), VerdictMeter(1), Spacer(1, 3 * mm),
      tiles([("110", GREEN, "litres per person per day, “today” (keynote slide)"),
             ("120", ORANGE, "Eurostat, households, public supply, 2024 (estimate)"),
             ("176", AMBER, "litres per person per day, all uses of public supply, 2024"),
             ("13th", GREY, "Malta’s rank from lowest of 19 EU states with data (median 111)")]),
      Spacer(1, 4 * mm),
      up_down("Nothing: Largely supported leaves room only for the caveats below, which are about definitions and the "
              "unquantified word “low”. (Supported is the top of the scale.)",
              "A WSC billed-consumption series showing domestic use clearly above Eurostat’s 116–120 litres, or "
              "the speaker confirming that “low” was meant against other countries (the data show Malta mid-table)."),
      Spacer(1, 3 * mm)]
S += toc([("1", "The claim and what we could verify"), ("2", "Method"), ("3", "What the data show"),
          ("4", "Where the evidence points different ways"), ("5", "Testing the claim"),
          ("6", "Verdict and requests for evidence"), ("7", "Limitations")])
S.append(PageBreak())

# ================================================================== 1
S.append(SectionHeading(1, "The claim and what we could verify"))
S.append(P("The primary source is the slide deck of the keynote “Water Management in the Maltese Islands” by Manuel "
           "Sapiano, Energy and Water Agency, at the IWRA 1st Island Water Congress, 2024 [1]. We downloaded and read "
           "all 27 slides (the file is dated 15 October 2024). It is a slide deck, not a transcript: we cannot see what "
           "was said aloud. The wording we rate is on slide 10."))
S.append(std_table([
    [C("What the slide says", cellh), C("Who", cellh), C("Access", cellh)],
    [C("“Tariffs and a continuous engagement programme have contributed to maintaining the per capita water "
       "consumption low, and in the region of the 90 litres per person per day higher tariff threshold.”"),
     C("E&amp;WA keynote, slide 10 [1]"), C("Read in full")],
    [C("“Per capita water consumption, today stands at around 110l/cap/day.”"), C("E&amp;WA keynote, slide 10 [1]"),
     C("Read in full")],
], [104 * mm, 40 * mm, 26 * mm]))
S += [Spacer(1, 4 * mm),
      callout([P("WORDING NOTE", tag),
               P("The claim record said the figure is “relatively low compared with other European countries”. We "
                 "searched the whole deck for a comparison with other countries and found none: the only EU "
                 "comparison on the slides is that Malta has “the highest population density in the EU” (slide 2). The "
                 "comparative wording is therefore the intake’s paraphrase and is reported but not rated as the "
                 "speaker’s claim. The deck does not say whether 110 litres is billed domestic consumption, "
                 "supply per resident or another measure.", small)], bg=AMBER_PALE, bar=AMBER), Spacer(1, 4 * mm)]

# ================================================================== 2
S.append(SectionHeading(2, "Method"))
S.append(P("<b>Question.</b> Is Maltese per-person water use about 110 litres a day, and is it low?"))
S.append(P("<b>Evidence.</b> Eurostat env_wat_cat (water use by supply category and sector, OECD/Eurostat Joint "
           "Questionnaire on Inland Waters; public water supply, households) and demo_pjan (population on 1 January) "
           "[2][3], retrieved 7 October 2026. Per-person use = households’ volume divided by the mean of the 1 January "
           "population of that year and the next, converted to litres per day. Every Maltese value is flagged as "
           "estimated by Eurostat. The calculation is <i>tools/cc-040-report/calc.py</i>; inputs and results are in "
           "<i>data/cc-040/</i>."))
S.append(P("<b>Grades.</b> Official statistics are grade C; the speaker’s slide is grade D (an assertion without "
           "method or source). <b>Verdicts</b> follow the five-point scale in Appendix A."))

# ================================================================== 3
S.append(CondPageBreak(150 * mm))
S.append(SectionHeading(3, "What the data show"))
S.append(fig(FIG / "fig2_malta_trend.png"))
S.append(P("Figure 1. Maltese households’ use of public water per person, 2013–2024, from Eurostat (all values "
           "flagged as estimated), against the keynote’s 110 litres. The series has stayed between 114 and 124 "
           "litres and was 120 in 2024.", cap))
S.append(std_table([
    [C("Indicator (Malta, public water supply)", cellh), C("2019", cellh), C("2022", cellh), C("2024", cellh), C("Grade", cellh)],
    [C("Households, litres per person per day"), C("114"), C("116"), C("<b>120</b>"), grade_tag("C")],
    [C("Services (incl. hotels), litres per head of resident population"), C("42"), C("39"), C("40"), grade_tag("C")],
    [C("All uses, litres per head of resident population"), C("173"), C("169"), C("<b>176</b>"), grade_tag("C")],
    [C("Households vs the keynote’s 110"), C("+4%"), C("+5%"), C("+9%"), grade_tag("C")],
], [84 * mm, 18 * mm, 18 * mm, 18 * mm, 14 * mm]))
S.append(P("Values in <i>data/cc-040/checks.csv</i>. “All uses” divides all sectors’ use of the public supply by the "
           "resident population; it includes use by tourists and businesses, so it is not a per-resident "
           "consumption figure.", cap))
S.append(P("Malta among EU states", h2))
S.append(P("Eurostat has a recent household figure for 19 of the 27 Member States (Estonia, Finland, France, Ireland, "
           "Italy, Luxembourg, Portugal and Slovakia have none from 2020 on). Taking each state’s latest year "
           "(2020–2024; Spain and Sweden 2020, Belgium and Germany 2022), Malta’s 120 litres ranks 13th from the "
           "lowest and is 8% above the median of 111 litres (Figure 2). Latvia, Lithuania, Czechia, Belgium and "
           "Romania are below 90; Greece (220) and Cyprus (294) are far higher [2]."))
S.append(KeepTogether([fig(FIG / "fig1_eu_households.png"),
                       P("Figure 2. Households’ use of public water per person per day, latest year 2020–2024, EU "
                         "states with data. Years differ between states (labelled where not 2024); definitions follow "
                         "the Joint Questionnaire but national collection methods differ.", cap)]))

# ================================================================== 4
S.append(CondPageBreak(110 * mm))
S.append(SectionHeading(4, "Where the evidence points different ways"))
S.append(contested(
    "Q1  Is consumption “around 110 litres”?", "CLOSE", GREEN,
    "Eurostat’s household series (116 in 2022, 120 in 2024) is within about 5–9% of 110; “around” covers that, and "
    "the series was 114 in 2018–2019. The speaker’s figure may be billed domestic consumption, which we have not seen.",
    "Every Maltese Eurostat value is an estimate, and the 2024 value is the highest since 2020. We did not obtain WSC "
    "billing data, so we cannot say which definition 110 follows.",
    "<b>For this claim:</b> the figure is a fair round number for households; a higher recent trend is not "
    "reflected."))
S.append(contested(
    "Q2  Is it “low”?", "NOT SHOWN", GREY,
    "On the keynote’s own terms the claim is about holding use down while the population and economy grew "
    "(slide 9). We did not test that history: the slide’s 350 litres in 1995 is production capacity per head, not "
    "consumption, so it is not comparable.",
    "Against other EU states Malta is mid-table (13th of 19; 8% above the median). Total supply per resident, "
    "176 litres, includes use by services and tourists.",
    "<b>For this claim:</b> “low” has no benchmark in the deck; against EU peers it is not low, but the speaker did "
    "not claim that."))

# ================================================================== 5
S.append(CondPageBreak(100 * mm))
S.append(SectionHeading(5, "Testing the claim"))
verd = lambda t, c: chip(t, c, w=29 * mm)
S.append(std_table([
    [C("Sub-claim", cellh), C("What the evidence shows", cellh), C("Rating", cellh)],
    [C("<b>A.</b> “Per capita water consumption, today stands at around 110l/cap/day”"),
     C("Eurostat households: 116 (2022), 120 (2024), estimates [2][3]. Within about 9%; definition of the 110 not "
       "stated."), verd("LARGELY SUPPORTED", LG)],
    [C("<b>B.</b> Consumption has been kept “low”"),
     C("No benchmark in the deck. Malta ranks 13th of 19 EU states, 8% above the median [2]."),
     verd("NOT SHOWN", GREY)],
    [C("<b>C.</b> Tariffs and engagement “contributed” to this; a “90 litres” higher-tariff threshold"),
     C("A causal claim with no evidence in the deck; the WSC tariff schedule was not obtained."),
     verd("NOT TESTED", GREY)],
    [C("<b>D.</b> “Relatively low compared with other European countries” (intake wording)"),
     C("Not in the speaker’s words; headline wording, not rated. For reference, Malta is mid-table [2]."),
     verd("NOT RATED", GREY)],
], [58 * mm, 82 * mm, 30 * mm], valign="MIDDLE"))

# ================================================================== 6
S += [Spacer(1, 6 * mm), SectionHeading(6, "Verdict and requests for evidence"),
      verdict_box("Largely supported", "The figure is about right for households; “low” is unquantified. "
                  "Confidence: moderate."), Spacer(1, 4 * mm)]
S.append(P("<b>Why.</b> (1) The headline number, 110 litres, is within about 9% of Eurostat’s household figure for "
           "2024 and 5% for 2022. (2) The keynote gives no benchmark for “low” and no source for the 110, and "
           "the tariff effect is not evidenced, so we rate them as not shown rather than false. (3) The EU "
           "comparison in the claim record is not the speaker’s statement; we report it (Malta is mid-table) without "
           "rating it. Our scale calls backing with caveats that do not change the substance <i>Largely supported</i>."))
S.append(P("<b>What this verdict does not say.</b> It does not say that Malta’s water use is low by European standards "
           "or that its water supply is sustainable. The keynote itself says natural freshwater is insufficient "
           "even at highly efficient demand (slide 3)."))
S.append(P("Evidence we are asking for", h2))
S.append(requests_list([
    "The source and definition of the 110 litres figure (billed domestic, per resident, year).",
    "WSC domestic billed consumption and the resident population used, 2015–2024.",
    "The rising block tariff schedule and any estimate of its effect on use.",
]))

# ================================================================== 7
S += [Spacer(1, 6 * mm), SectionHeading(7, "Limitations")]
for l in ["We read slides only: any spoken qualification is not in the deck.",
          "Eurostat’s Maltese values are estimates; its metadata page for the dataset family (env_nwat_esms) "
          "refers to the Joint Questionnaire definitions, which we did not read in full.",
          "Eurostat’s per-person figure uses our population denominator (mean of two 1 January populations); WSC "
          "may use another.",
          "EU comparison covers 19 states with different years (2020–2024); countries differ in how they "
          "measure household use. Greece and Cyprus are very high, so we use the median.",
          "We did not search WSC or NSO publications for a 110 litres series; none was found through "
          "Eurostat or in our web search of 7 October 2026 (see literature/CC-040/notes.md)."]:
    S.append(P("• " + l, bul))

S += [Spacer(1, 6 * mm), SectionHeading(None, "References")]
S += references([
    ("1", "Sapiano M. (2024). Water Management in the Maltese Islands. Keynote, IWRA 1st Island Water Congress. "
          "Energy and Water Agency (slide deck, 27 slides).",
     "https://www.iwra.org/proceedings/congress/resource/IWRA2024_1stIslandWC_0609_HLP_EuroInbo_MSapiano_Keynote.pdf"),
    ("2", "Eurostat. env_wat_cat, Water use by supply category and economical sector (public water supply, "
          "households; status flags checked); retrieved 7 Oct 2026.", "https://doi.org/10.2908/ENV_WAT_CAT"),
    ("3", "Eurostat. demo_pjan, Population on 1 January by age and sex; retrieved 7 Oct 2026.",
     "https://doi.org/10.2908/DEMO_PJAN"),
    ("4", "Eurostat. Environment and water statistics, explanatory texts (env_nwat_esms).",
     "https://ec.europa.eu/eurostat/cache/metadata/en/env_nwat_esms.htm"),
    ("5", "MiŻien. Data and calculations: data/cc-040/; tools/cc-040-report/calc.py.", ""),
])

S.append(PageBreak())
S += appendix_a("A experiment · B observational study with a control or gradient · C review, guidance or "
                "official statistics · D assertion or anecdote. ◆ marks a source known only second-hand.")
S += [Spacer(1, 5 * mm)]
S += revision_log([("1.0", "7 Oct 2026", "First issue. No right of reply needed.")])

build_report(Report(
    number="040", out=str(FIG / "report.pdf"), kicker="Water",
    title_lines=["Is water use", "per head", "low?"],
    subtitle_lines=["Testing a public claim about Malta’s per-person water use",
                    "against Eurostat’s household series"],
    quote_lines=["“Per capita water consumption, today", "stands at around 110l/cap/day.”"], quote_size=16,
    attribution="Manuel Sapiano, Energy and Water Agency, keynote slide, IWRA 1st Island Water Congress, 2024.",
    context="On a slide about keeping per-person consumption “low”.",
    verdict="Largely supported", verdict_note="The figure is close; “low” is not benchmarked",
    footer_lines=["Version 1.0  ·  7 October 2026", "Status: draft · no right of reply needed",
                  "Prepared from public sources and Eurostat data.", "Repository: github.com/leandergrech/Mizien"],
    running_head="Water use per head – Malta", version="1.0", date="7 October 2026",
    pdf_title="Is water use per head low? Claim Check 040",
    pdf_subject="Tests the Energy and Water Agency's statement that per capita water consumption is around 110 litres a day",
    story=S))
