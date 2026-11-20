"""Claim Check 152 report. Run calc.py and figures.py first. Output: out/report.pdf"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import *  # noqa: E402,F401

FIG = HERE / "out"
S = []
S += [SectionHeading(None, "TL;DR"), Spacer(1, 1 * mm),
      P("In its draft update of Malta’s National Air Pollution Control Programme, put out for consultation on 5 June 2026, "
        "the Environment and Resources Authority (ERA) wrote: <b>“projections reported in 2025 indicate a significant risk "
        "of non-compliance with the NOx ceiling for 2030.”</b> It projects 3.88 kilotonnes of nitrogen oxides in 2030 "
        "against a legal ceiling of 1.98. We checked the ceiling against the EU directive, and the emissions record and "
        "source shares against Eurostat.", lead)]
S.append(key_points([
    ("The ceiling is right.",
     "The National Emission Reduction Commitments Directive requires Malta to cut NOx 79% below 2005 from 2030. On "
     "ERA’s 2005 base of 9.45 kt that is 1.98 kt."),
    ("The projection is almost double the ceiling.",
     "With measures in place at the end of 2021, ERA projects 3.88 kt in 2030, 1.96 times the ceiling. Even with its "
     "planned additional measures, NOx stays “almost double”."),
    ("The trend supports the warning.",
     "NOx fell by more than half from 2005 to 2017, mainly in power generation, but has stayed between 4.1 and 4.6 kt "
     "since. Reaching 1.98 kt needs a further cut of more than half in six years."),
    ("The source shares match.",
     "ERA gives road transport 42.6% and ferries 15.5% of NOx in 2023. Eurostat’s later inventory gives 41.4% and "
     "15.3%."),
    ("Verdict: supported (high confidence).",
     "This is a regulator warning against its own country’s interest, and every number in it checks out."),
]))
S += [Spacer(1, 2.5 * mm), VerdictMeter(0), Spacer(1, 3 * mm),
      tiles([("3.88 kt", RED, "NOx projected for 2030 with existing measures (ERA)"),
             ("1.98 kt", GREEN, "2030 ceiling: 79% below 2005 (Directive 2016/2284)"),
             ("4.4 kt", AMBER, "NOx in 2024 (Eurostat); flat since 2017"),
             ("42.6%", GREY, "share from road transport in 2023 (ERA)")]),
      Spacer(1, 4 * mm),
      up_down("Already at the top of the scale. Quantified additional measures that still leave NOx above 1.98 kt would "
              "confirm it again.",
              "A revised inventory or projection showing Malta on course for 1.98 kt by 2030."),
      Spacer(1, 3 * mm)]
S += toc([("1", "The claim and what we could verify"), ("2", "Method"), ("3", "Ceiling, projection and trend"),
          ("4", "Testing the claim"), ("5", "Verdict"), ("6", "Limitations")])
S.append(PageBreak())

S.append(SectionHeading(1, "The claim and what we could verify"))
S.append(P("Italpress (Malta News Agency) reported on 17 July 2026 that Malta “remains at significant risk of failing to "
           "meet” its 2030 NOx target. Those words are the agency’s summary [1]. ERA’s own wording is in the 102-page "
           "consultation draft (PDF pp. 11, 14 and 63) [2], which we read from the maintainer’s browser copy; era.org.mt "
           "refuses scripts. The draft says, in its summary, that “Malta remains at risk of not meeting the reduction "
           "ceiling established for 2030”, and in section 3.1 the sentence quoted above."))
S.append(std_table([
    [C("Source", cellh), C("What it says", cellh), C("Our access", cellh), C("Status", cellh)],
    [C("<b>ERA</b>, draft NAPCP first update, Jun 2026 [2]"),
     C("“significant risk of non-compliance with the NOx ceiling for 2030”; Table 4: 3.88 kt projected, 1.98 kt "
       "ceiling."), C("Maintainer’s copy, 102 pp., read."), C("<b>The claim</b>")],
    [C("<b>Italpress / MNA</b>, 17 Jul 2026 [1]"), C("Reports the programme in the agency’s own words."),
     C("Read in full (1 Nov 2026)."), C("<b>Report</b>")],
    [C("<b>Directive (EU) 2016/2284</b>, Annex II [3]"), C("Malta: NOx −42% (2020–2029), −79% (from 2030)."),
     C("EUR-Lex, read in a browser."), C("<b>Primary law</b>")],
    [C("<b>Eurostat</b>, env_air_emis [4]"), C("Malta NOx by sector, 2005–2024."), C("API, 17 Nov 2026."),
     C("<b>Primary data</b>")],
], [38 * mm, 66 * mm, 40 * mm, 26 * mm]))

S += [Spacer(1, 4 * mm), SectionHeading(2, "Method")]
S.append(P("We copied ERA’s Table 4 into <i>data/cc-152/era_napcp_table4.csv</i> and recomputed the ceiling and ratios in "
           "<i>tools/cc-152-report/calc.py</i> (output <i>checks.csv</i>). We downloaded Malta’s NOx series and sector "
           "split from Eurostat, and read the directive’s Annex II. The programme is an official projection, and Eurostat "
           "is official statistics (both grade C). <b>Verdicts</b> follow the five-point scale in Appendix A."))

S.append(CondPageBreak(110 * mm))
S.append(SectionHeading(3, "Ceiling, projection and trend"))
S.append(fig(FIG / "fig1_nox.png", width=CW * 0.98))
S.append(P("Figure 1. Malta’s NOx emissions, the NEC Directive ceilings and ERA’s 2030 projection.", cap))
S.append(P("Annex II of the directive commits Malta to cut NOx 42% below 2005 in 2020–2029 and 79% from 2030 [3]. That "
           "79% is the second-steepest NOx commitment in the EU, after Luxembourg’s 83%. ERA’s 2005 base of 9.45 kt gives a 2030 ceiling of "
           "1.98 kt. Eurostat’s later inventory puts 2005 at 9.62 kt, which would make it 2.02 kt [4]. Malta met the "
           "2020–2029 ceiling of 5.48 kt in every year since 2020."))
S.append(P("Emissions fell from about 9.7 kt in 2008 to 4.6 kt in 2017, after the Marsa power station closed and the "
           "interconnector with Sicily opened in 2015 [2]. Since then they have stayed between 4.1 and 4.6 kt (4.43 kt in "
           "2024) [4]. ERA’s With Measures projection of 3.88 kt for 2030 is 1.96 times the ceiling. It notes that it could "
           "not yet quantify most transport measures in the With Additional Measures scenario, and that NOx still stays "
           "“almost double the allowable limit” [2]. Road transport (passenger cars, vans, lorries and buses) was 42.6% "
           "of NOx in 2023 and ferries 15.5%, by ERA’s count. Eurostat gives 41.4% and 15.3% for the same year [4]."))

S.append(CondPageBreak(70 * mm))
S.append(SectionHeading(4, "Testing the claim"))
verd = lambda t, c: chip(t, c, w=29 * mm)
S.append(std_table([
    [C("Sub-claim", cellh), C("Said by", cellh), C("What the evidence shows", cellh), C("Rating", cellh)],
    [C("<b>A.</b> “a significant risk of non-compliance with the NOx ceiling for 2030”"), C("ERA [2]"),
     C("Projection 1.96 times the ceiling; emissions flat at 4.1–4.6 kt since 2017."), verd("ACCURATE", GREENC)],
    [C("<b>B.</b> 3.88 kt projected in 2030 against a 1.98 kt ceiling"), C("ERA [2]"),
     C("Ceiling = 9.45 kt × (1 − 0.79), as in Annex II of the directive."), verd("ACCURATE", GREENC)],
    [C("<b>C.</b> Road transport 42.6% and national navigation 15.5% of NOx in 2023"), C("ERA [2]"),
     C("Eurostat’s later inventory: 41.4% and 15.3%."), verd("ACCURATE", GREENC)],
], [42 * mm, 26 * mm, 68 * mm, 34 * mm], valign="MIDDLE"))

S += [Spacer(1, 6 * mm), SectionHeading(5, "Verdict"),
      verdict_box("Supported", "ERA’s projection, the legal ceiling and the source shares all check out; NOx has been "
                  "flat since 2017. Confidence: high."), Spacer(1, 4 * mm)]
S.append(P("<b>Why.</b> The ceiling follows from the directive, the projection is ERA’s own and is almost double it, and "
           "the emissions record gives no sign of the steep fall needed. <b>What this verdict does not say.</b> It does "
           "not assess whether the planned measures would close the gap. ERA itself says most could not yet be "
           "quantified. The Commission’s action over the late programme is checked as CC-129."))
S += [Spacer(1, 4 * mm),
      callout([P("RIGHT OF REPLY", tag),
               P("Not needed for this verdict (maintainer rule of 5 October 2026).", small)], bg=AMBER_PALE, bar=AMBER)]
S += [Spacer(1, 6 * mm), SectionHeading(6, "Limitations")]
for l in ["The programme read is the consultation draft (it still has placeholders such as “[insert date]”). The final "
          "version may change figures.",
          "Inventory recalculations change past values. Eurostat’s latest figures differ from ERA’s draft by up to 0.2 kt.",
          "Projections depend on assumptions about traffic, shipping and power generation."]:
    S.append(P("• " + l, bul))
S += [Spacer(1, 6 * mm), SectionHeading(None, "References")]
S += references([
    ("1", "Italpress (Malta News Agency). Malta at risk of missing 2030 NOx emissions target, ERA warns, 17 July 2026.",
     "https://www.italpress.com/?p=716573"),
    ("2", "Environment and Resources Authority. First Update of Malta’s National Air Pollution Control Programme (NAPCP), "
          "consultation draft, 5 June–17 July 2026, 102 pp. (maintainer copy; PDF pp. 11, 14, 44, 63, 85).",
     "https://era.org.mt/first-update-of-maltas-national-air-pollution-control-programme-napcp/"),
    ("3", "Directive (EU) 2016/2284 on the reduction of national emissions of certain atmospheric pollutants, Annex II, "
          "Table A.", "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32016L2284"),
    ("4", "Eurostat. Air pollutants by source sector (env_air_emis), Malta NOx, updated 7 Sep 2026, retrieved 17 Nov 2026.",
     "https://ec.europa.eu/eurostat/databrowser/view/env_air_emis/default/table"),
    ("5", "MiŻien. Data and script: data/cc-152/; tools/cc-152-report/calc.py. Related: CC-129, CC-109.", ""),
])
S.append(PageBreak())
S += appendix_a("A experiment · B observational study with a control or gradient · C review, guidance or "
                "official statistics · D assertion or anecdote. ◆ marks a source known only second-hand.")
S += [Spacer(1, 5 * mm)]
S += revision_log([("1.0", "17 Nov 2026", "First issue. Verdict Supported (high confidence); no right of reply needed.")])

build_report(Report(
    number="152", out=str(FIG / "report.pdf"), kicker="Air quality",
    title_lines=["Missing the", "NOx target?"],
    subtitle_lines=["Testing ERA’s warning on Malta’s 2030", "nitrogen-oxide ceiling"],
    quote_lines=["“…a significant risk of non-compliance", "with the NOx ceiling for 2030.”"], quote_size=15,
    attribution="Environment and Resources Authority, draft National Air Pollution Control Programme, June 2026.",
    context="Projection 3.88 kt in 2030 against a ceiling of 1.98 kt.",
    verdict="Supported", verdict_note="Projection almost double the legal ceiling",
    footer_lines=["Version 1.0  ·  17 November 2026", "Status: no right of reply needed",
                  "Prepared from public sources and open data.", "Repository: github.com/leandergrech/Mizien"],
    running_head="NOx 2030 ceiling – ERA, June 2026", version="1.0", date="17 November 2026",
    pdf_title="Missing the NOx target? Claim Check 152",
    pdf_subject="Tests ERA's warning that Malta is at significant risk of missing its 2030 NOx ceiling",
    story=S))
