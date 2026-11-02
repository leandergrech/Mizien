"""Claim Check 147 report. Run fetch.py (once), calc.py and figures.py first. Output: out/report.pdf"""
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
      P("A February 2026 factsheet from Malta’s Climate Action Authority says that when air and maritime transport are "
        "left out, Malta’s greenhouse-gas intensity per euro generated “reduced by 19%” between 2020 and 2024, "
        "<b>“rather than increased as per Eurostat’s figures which summed up show a growth rate of 87.2%.”</b> "
        "We rebuilt both numbers from Eurostat’s own tables. Eurostat’s all-activities series gives +86%; "
        "leaving out air and water transport gives a fall of about 21–22%, and Malta’s emissions on a territorial "
        "basis give the same direction. The 19% itself is the Authority’s own calculation and we could not reproduce "
        "it exactly.", lead)]
S.append(key_points([
    ("Aviation does dominate the Eurostat total.",
     "Air transport was 68% of Malta’s 2024 greenhouse-gas emissions on Eurostat’s residence basis (24% in 2020; the "
     "EU-27 figure is 4%). Its emissions rose 7.2-fold in four years."),
    ("The +87.2% is reproduced, within a point.",
     "From Eurostat emissions and value added in chain-linked volumes we get +86.2% for 2020–2024."),
    ("The 19% fall is right in direction and close in size.",
     "Removing air and water transport gives −22% (−21% for air alone); Malta’s territorial emissions per euro give "
     "−22%. Every start year from 2017 to 2023 gives a fall, from −8% to −28%."),
    ("But removing aviation changes the measure rather than correcting it.",
     "The factsheet itself says the Eurostat accounts follow the residence principle by design. Both figures are "
     "defensible for different purposes; which one measures “progress” depends on the question."),
    ("Verdict: largely supported (moderate confidence).",
     "The facts check out. The caveats are the exact 19%, a 2020 start year in which air transport’s value added was "
     "negative, and the framing that one figure is the “real” one."),
]))
S += [Spacer(1, 2.5 * mm), VerdictMeter(1), Spacer(1, 3 * mm),
      tiles([("68%", ORANGE, "of Malta’s 2024 greenhouse-gas emissions (residence basis) came from air transport"),
             ("+86%", RED, "Malta’s GHG per euro of value added, 2020–2024, all activities (factsheet: +87.2%)"),
             ("−22%", GREEN, "the same measure without air and water transport (factsheet: −19%)"),
             ("−15%", GREEN, "EU-27, all activities, 2020–2024, for comparison")]),
      Spacer(1, 4 * mm),
      up_down("Nothing: Supported is the top of the scale. The 19% itself would be confirmed if the Authority published its "
              "workings and they matched the Eurostat tables.",
              "Evidence that the Authority’s method double-counts or mislabels sectors, or that the Eurostat series it "
              "cites for 87.2% differs materially from the tables we used."),
      Spacer(1, 3 * mm)]
S += toc([("1", "The claim and what we could verify"), ("2", "Method"), ("3", "What the data show"),
          ("4", "Where the evidence points different ways"), ("5", "Testing the claim"),
          ("6", "Verdict and requests for evidence"), ("7", "Limitations")])
S.append(PageBreak())

# ================================================================== 1
S.append(SectionHeading(1, "The claim and what we could verify"))
S.append(P("The claim is on page 5 of the Climate Action Authority’s seven-page factsheet <i>An analysis of Malta’s GHG "
           "Emissions by Economic Activity</i>, dated February 2026 (the PDF metadata give 4 February 2026) [1]. The "
           "Authority’s own address for the file refused our download, so we read the copy that the Internet Archive "
           "captured on 15 April 2026, in full. The factsheet is the speaker’s own document, and the quotations "
           "below are its words, including its spelling."))
S.append(std_table([
    [C("What the factsheet says", cellh), C("Where", cellh), C("Access", cellh)],
    [C("“Moreover, when the GHG intensity for Malta is worked out excluding air transport and maritime transport, one "
       "may note that GHG intensity per every euro generated between 2024 and 2020 in fact reduced by 19% rather than "
       "increased as per Eurostat’s figures which summed up show a growth rate of 87.2%.”"), C("p. 5 [1]"), C("Read in full")],
    [C("The aviation sector’s emissions “became very prominent over the years”; “this has skewed the emission profile "
       "of Malta as this activity has a disporportionate statistical weighing on the final emission results” "
       "(spelling as printed)."), C("p. 3 [1]"), C("Read in full")],
    [C("The Eurostat accounts follow “the ‘residence’ principle”, counting emissions of businesses registered in "
       "Malta “irrespective of whether their activity is carried out locally or outside of the territory”."),
     C("p. 1 [1]"), C("Read in full")],
], [108 * mm, 22 * mm, 40 * mm]))
S += [Spacer(1, 4 * mm),
      callout([P("SCOPE NOTE", tag),
               P("We test the numbers in the 19% / 87.2% sentence and the statement that aviation weighs disproportionately. "
                 "The factsheet contains other figures (for example, a rise of “only 9.6%” instead of “190.9%” on page 5, and "
                 "+16.6% in 2013–2024 on page 4). They are not part of the claim as worded and are not rated; we could not "
                 "reproduce them from the tables below without knowing the periods they refer to.", small)],
              bg=AMBER_PALE, bar=AMBER), Spacer(1, 4 * mm)]

# ================================================================== 2
S.append(SectionHeading(2, "Method"))
S.append(P("<b>Question.</b> Do Eurostat’s published tables give +87.2% for 2020–2024, and does removing air and water transport "
           "give a fall of about 19%?"))
S.append(P("<b>Evidence.</b> Eurostat air emissions accounts by activity (env_ac_ainah_r2: greenhouse gases, all activities plus "
           "households, air transport H51, water transport H50), gross value added in chain-linked volumes at 2020 prices and at "
           "current prices (nama_10_a64), and the table bridging the accounts to the territorial inventory totals "
           "(env_ac_aibrid_r2), for Malta and the EU-27, retrieved 2 November 2026 [2]. All numbers are recomputed by "
           "<i>tools/cc-147-report/calc.py</i> from <i>data/cc-147/eurostat_aea.csv</i> and written to <i>checks.csv</i>. "
           "We found no peer-reviewed study of this particular measure; the evidence here is official statistics "
           "(grade C). The search log is in <i>literature/CC-147/notes.md</i>."))
S.append(P("<b>Our definition of intensity.</b> Emissions (kt CO₂-equivalent, residence basis, activities plus households) divided by total "
           "gross value added in chain-linked 2020 euros. To leave out a sector we subtract its emissions and its chain-linked "
           "value added. Chain-linked volumes are not strictly additive, so this is an approximation, which we cross-check "
           "with current prices and with the territorial totals. The Authority’s own workings are not published in the factsheet."))
S.append(P("<b>Grades.</b> Official statistics are grade C. <b>Verdicts</b> follow the five-point scale in Appendix A."))

# ================================================================== 3
S.append(CondPageBreak(150 * mm))
S.append(SectionHeading(3, "What the data show"))
S.append(P("Aviation’s weight", h2))
S.append(fig(FIG / "fig1_air_share.png"))
S.append(P("Figure 1. Malta’s greenhouse-gas emissions on Eurostat’s residence basis, split into air transport and everything "
           "else, 2013–2024, with emissions on the territory (inventory) basis as a line. Everything except air transport "
           "has been broadly flat since 2015.", cap))
S.append(P("Air transport emitted 662 kt CO₂e in 2020 and 4,730 kt in 2024, 24% and 68% of the total. In the EU-27 it is 4% "
           "[2]. Residents’ air fuel bought abroad alone is 68% of the 2024 residence total in Eurostat’s bridging table; emissions "
           "on Malta’s territory, the basis used for UNFCCC reporting, were 2,086 kt in 2020 and 2,198 kt in 2024 (+5.4%; 2024 "
           "flagged ‘i’, see Eurostat metadata) [2]. The claim that aviation weighs disproportionately on the total is therefore "
           "borne out by the tables."))
S.append(P("Rebuilding the two intensity figures", h2))
S.append(fig(FIG / "fig2_intensity.png"))
S.append(P("Figure 2. Greenhouse-gas emissions per euro of value added, index 2020 = 100. The factsheet’s +87.2% and −19% correspond to "
           "the red and dark-green lines; we get +86% and −22%.", cap))
S.append(std_table([
    [C("Measure, Malta, 2020 → 2024", cellh), C("Our result", cellh), C("Factsheet", cellh), C("Grade", cellh)],
    [C("Intensity, all activities plus households (CLV 2020)"), C("<b>+86.2%</b> (209.5 → 390.1 g/EUR)"), C("+87.2%"), grade_tag("C")],
    [C("Same, activities only (households excluded)"), C("+98.6%"), C("–"), grade_tag("C")],
    [C("Excluding air and water transport; emissions / GVA, CLV"), C("<b>−22.2%</b> (emissions +4.6%, GVA +34.4%)"), C("−19%"), grade_tag("C")],
    [C("Excluding air transport only"), C("−21.2%"), C("–"), grade_tag("C")],
    [C("Excluding air and water transport; GVA at current prices (cross-check only)"), C("−33.7%"), C("–"), grade_tag("C")],
    [C("Territory-basis emissions / total GVA (CLV)"), C("−22.2%"), C("–"), grade_tag("C")],
    [C("EU-27, all activities"), C("−15.1%"), C("–"), grade_tag("C")],
], [76 * mm, 52 * mm, 24 * mm, 18 * mm]))
S.append(P("Values in <i>data/cc-147/checks.csv</i>. The factsheet’s own page-3 chart gives emissions without air and water transport as 2,016.34 "
           "kt (2020) and 2,116.77 kt (2024); we get 2,016.3 and 2,108.3 from the current Eurostat release, a difference of 8.5 kt "
           "that we attribute to data vintage (2024 values carry flag ‘i’).", cap))
S.append(P("The 2020 starting point", h2))
S.append(P("Air transport’s value added was negative in 2020 (−EUR 219 million; Covid-19 year) and changes sign in later years "
           "in the chain-linked series (+185, −115, −237, −171 million in 2021–2024) [2]. Removing it therefore raises the 2020 "
           "denominator and makes the starting year unusually favourable for the “excluding aviation” series. We tested other "
           "start years (air transport removed, chain-linked value added available from 2017): the fall persists but shrinks "
           "from −28% (2017) and −21% (2020) to −14% (2021) and −8% (2023). The all-activities increase stays between +57% "
           "and +86% for 2017–2022 starts."))

# ================================================================== 4
S.append(CondPageBreak(120 * mm))
S.append(SectionHeading(4, "Where the evidence points different ways"))
S.append(contested(
    "Q1  Is the +87.2% a fair picture of Malta’s emissions intensity?", "ACCURATE, BUT A RESIDENCE-BASIS MEASURE", AMBER,
    "We reproduce the Eurostat-based increase (+86%) and the factsheet says plainly, on page 1, that the Eurostat accounts follow the "
    "residence principle. Aviation emissions are real emissions of Malta-registered businesses.",
    "Most of that air fuel is bought abroad (Eurostat bridging table), and emissions on Malta’s own territory moved little "
    "(+5.4% in 2020–2024, against value added +36%). The total mostly reflects the activity of airlines registered in Malta.",
    "<b>For this claim:</b> the 87.2% is correct as a statement about Eurostat’s residence-basis series; whether it is the "
    "right measure of Malta’s “progress” depends on what is being asked."))
S.append(contested(
    "Q2  Does leaving out aviation “correct” the figure?", "CHANGES THE MEASURE", AMBER,
    "Excluding air and water transport, or using territorial totals, gives a fall of about 21–22% and a result that holds for "
    "every start year tested. The EU-27 fell 15% on the all-activities measure.",
    "The exclusion is a choice. Resident airlines’ emissions are in Eurostat’s accounts; removing them also removes the "
    "sector from the denominator; the 2020 base is a pandemic year; and the factsheet’s workings are not published.",
    "<b>For this claim:</b> “in fact reduced” is borne out by the numbers, but the sentence’s “rather than increased as per "
    "Eurostat” sets two different measures against each other as if one were right and the other wrong."))

# ================================================================== 5
S.append(CondPageBreak(110 * mm))
S.append(SectionHeading(5, "Testing the claim"))
verd = lambda t, c: chip(t, c, w=29 * mm)
S.append(std_table([
    [C("Sub-claim", cellh), C("What the evidence shows", cellh), C("Rating", cellh)],
    [C("<b>A.</b> Aviation has a disproportionate weight in Malta’s emissions-intensity figure"),
     C("Air transport is 68% of 2024 residence-basis emissions (EU-27: 4%) and rose 7.2-fold since 2020 [2]."), verd("SUPPORTED", GREEN)],
    [C("<b>B.</b> Eurostat’s published figures show growth of 87.2% in 2020–2024"),
     C("We get +86.2% from Eurostat tables; the remaining point is plausibly data vintage or the Authority’s exact definition [2]."),
     verd("LARGELY SUPPORTED", LG)],
    [C("<b>C.</b> Excluding air and maritime transport, emissions per euro fell by 19% in 2020–2024"),
     C("We get −22% (CLV subtraction) and −22% on a territorial basis; the fall holds for all start years 2017–2023 but is "
       "smaller from later starts; the exact 19% could not be reproduced and the 2020 base is unusual [2]."),
     verd("LARGELY SUPPORTED", LG)],
    [C("<b>D.</b> This is “in fact” the correct result “rather than” Eurostat’s"),
     C("Framing: two measures, both valid, for different questions; the factsheet itself says so on page 1 [1]. Not rated separately."),
     verd("NOT RATED", GREY)],
], [52 * mm, 88 * mm, 30 * mm], valign="MIDDLE"))

# ================================================================== 6
S += [Spacer(1, 6 * mm), SectionHeading(6, "Verdict and requests for evidence"),
      verdict_box("Largely supported", "The numbers check out within a few points; the framing treats two valid measures "
                  "as right and wrong. Confidence: moderate."), Spacer(1, 4 * mm)]
S.append(P("<b>Why.</b> (1) Eurostat’s tables reproduce the +87.2% to within a point and show that air transport is 68% of the "
           "2024 total. (2) Removing air and water transport, or using territorial emissions, gives a fall of about 21–22%, close "
           "to the stated 19% and in the same direction for every start year tested. (3) The caveats are the unpublished workings behind "
           "the exact 19%, the unusual 2020 base year and the framing, but they do not change the substance, which our scale "
           "calls <i>Largely supported</i>. Confidence is moderate because we could not see the Authority’s own calculation."))
S.append(P("<b>What this verdict does not say.</b> It does not say that Malta’s climate performance is good or bad, that "
           "aviation emissions should be excluded from policy, or that the Authority acted in any particular way. It says that "
           "the figures in the sentence agree with Eurostat’s data."))
S.append(P("Evidence we are asking for", h2))
S.append(requests_list([
    "The Authority’s workings for the −19% (sector list, deflator, base year).",
    "The vintage of Eurostat data behind the factsheet’s +87.2% and the page-3 chart.",
    "The periods for the factsheet’s “9.6%” and “190.9%” figures on page 5.",
]))

# ================================================================== 7
S += [Spacer(1, 6 * mm), SectionHeading(7, "Limitations")]
for l in ["We could not read the factsheet at the Authority’s own address (it refused our download); we read the Internet Archive’s "
          "capture of 15 April 2026 and compared it with the PDF metadata (created 4 February 2026).",
          "Chain-linked volumes are not additive; subtracting a sector’s value added is an approximation, and air transport’s "
          "chain-linked value added is negative in 2020, 2022, 2023 and 2024. We show current-price and territorial cross-checks.",
          "Eurostat’s 2024 values carry flag ‘i’ (see Eurostat metadata); our data are the release of 2 November 2026 and may differ "
          "from the vintage the Authority used.",
          "We found no peer-reviewed literature on this measure; evidence is official statistics only (search log in the notes).",
          "This check does not assess Malta’s progress towards its climate targets, which use the territorial inventory."]:
    S.append(P("• " + l, bul))

S += [Spacer(1, 6 * mm), SectionHeading(None, "References")]
S += references([
    ("1", "Climate Action Authority (Malta) (February 2026). An analysis of Malta’s GHG Emissions by Economic Activity "
          "(FACTSHEET-AEA.pdf), 7 pp. Read in the Internet Archive capture of 15 April 2026.",
     "https://web.archive.org/web/20260415130840/https://climateaction.gov.mt/wp-content/uploads/2026/02/FACTSHEET-AEA.pdf"),
    ("2", "Eurostat. env_ac_ainah_r2, env_ac_aibrid_r2, nama_10_a64 (B1G; CLV20_MEUR and CP_MEUR); Malta and EU-27; retrieved 2 Nov 2026.",
     "https://ec.europa.eu/eurostat/databrowser/"),
    ("3", "Miżien. Data and calculations: data/cc-147/; tools/cc-147-report/calc.py.", ""),
])

S.append(PageBreak())
S += appendix_a("A experiment · B observational study with a control or gradient · C review, guidance or "
                "official statistics · D assertion or anecdote. ◆ marks a source known only second-hand.")
S += [Spacer(1, 5 * mm)]
S += revision_log([("1.0", "2 Nov 2026", "First issue. Verdict: Largely supported; no right of reply needed.")])

build_report(Report(
    number="147", out=str(FIG / "report.pdf"), kicker="Climate and energy",
    title_lines=["Did emissions", "intensity fall", "19%?"],
    subtitle_lines=["Testing a Climate Action Authority factsheet on Malta’s",
                    "greenhouse-gas intensity against Eurostat’s tables"],
    quote_lines=["“GHG intensity per every euro generated between", "2024 and 2020 in fact reduced by 19%”"], quote_size=16,
    attribution="Climate Action Authority (Malta), factsheet on air emissions accounts, February 2026.",
    context="Excluding air and maritime transport; Eurostat’s figures “show a growth rate of 87.2%”.",
    verdict="Largely supported", verdict_note="Numbers check out; two valid measures are set against each other",
    footer_lines=["Version 1.0  ·  2 November 2026", "Status: draft · no right of reply needed",
                  "Prepared from public sources and Eurostat data.", "Repository: github.com/leandergrech/Mizien"],
    running_head="Emissions intensity – Malta", version="1.0", date="2 November 2026",
    pdf_title="Did emissions intensity fall 19%? Claim Check 147",
    pdf_subject="Tests the Climate Action Authority factsheet's claim that Malta's GHG intensity excluding air and maritime transport fell 19% in 2020-2024",
    story=S))
