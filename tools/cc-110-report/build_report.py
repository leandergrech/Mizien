"""Claim Check 110 report. Run fetch.py, calc.py and figures.py first. Output: out/report.pdf"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import *  # noqa: E402,F401

FIG = HERE / "out"
S = []
S += [SectionHeading(None, "TL;DR"), Spacer(1, 1 * mm),
      P("In its 2026 Country Report on Malta (3 June 2026), the European Commission wrote: <b>“In 2024, Malta "
        "recorded 7 700 new passenger car registrations, of which 37.7% were ZEVs – a 17.4 percentage point increase "
        "since 2023 (20.3%) and well above the EU average of 13.6%.”</b> We re-ran the figures from Eurostat’s "
        "registration data.", lead)]
S.append(key_points([
    ("Malta’s figures are right.",
     "Eurostat records 7,683 new passenger cars in Malta in 2024, of which 2,893 were battery electric (none ran on "
     "hydrogen): 37.65%. In 2023 the share was 20.31%. The rise is 17.3–17.4 points depending on rounding."),
    ("Malta is second in the EU.",
     "Only Denmark (51.3%) had a higher zero-emission share of new cars in 2024. Sweden (34.9%) and the Netherlands "
     "(34.6%) follow."),
    ("The EU average differs by a tenth of a point.",
     "Eurostat’s EU-27 figure is 13.53% (13.5%); the report says 13.6% and we could not identify the source of the "
     "extra tenth. The difference does not affect the comparison."),
    ("New cars are not the fleet.",
     "Zero-emission cars were 2.2% of Malta’s passenger-car stock at the end of 2024, the same as the EU average, and "
     "the stock grew by 6,632 cars (18 a day). The report itself goes on to say charging infrastructure is lagging."),
    ("Verdict: supported (high confidence).",
     "The statement is accurate and its comparison with the EU holds. 2025 data show the share stable at 37.6%."),
]))
S += [Spacer(1, 2.5 * mm), VerdictMeter(0), Spacer(1, 3 * mm),
      tiles([("37.7%", GREEN, "Zero-emission share of new cars in Malta, 2024 (2023: 20.3%)"),
             ("2nd", GREEN, "Malta’s rank in the EU in 2024, after Denmark (51.3%)"),
             ("13.5%", BLUE, "EU-27 share in Eurostat’s data (report: 13.6%)"),
             ("2.2%", GREY, "Zero-emission share of the whole car fleet, end 2024 (EU 2.2%)")]),
      Spacer(1, 4 * mm),
      up_down("None: Supported is the top of the scale.",
              "A revision of the registration data, or evidence that the Maltese figure counts plug-in hybrids as "
              "zero-emission (Eurostat does not)."),
      Spacer(1, 3 * mm)]
S += toc([("1", "The claim and what we could verify"), ("2", "Method"), ("3", "What the data show"),
          ("4", "Where the evidence points different ways"), ("5", "Testing the claim"),
          ("6", "Verdict and requests for evidence"), ("7", "Limitations")])
S.append(PageBreak())

S.append(SectionHeading(1, "The claim and what we could verify"))
S.append(P("The passage is in Annex 8 of the Commission’s 2026 Country Report for Malta, SWD(2026) 218 final [1], "
           "read in full from the Council copy on 5 October 2026. Footnote (142) cites Eurostat’s “Passenger cars in "
           "the EU”. The report’s statistical annex gives the same series (“New zero-emission vehicles, electricity "
           "motor, %”: 15.40, 20.31, 37.66 for 2022–2024), and the report’s summary repeats the 37.7%. The passage "
           "also gives light commercial vehicles (16.6%, EU 6.1%); that is outside the claim as recorded and not tested."))
S.append(std_table([
    [C("Source", cellh), C("What it says", cellh), C("Our access", cellh), C("Status", cellh)],
    [C("<b>European Commission</b>, 2026 Country Report – Malta, Annex 8 [1]"),
     C("“In 2024, Malta recorded 7 700 new passenger car registrations, of which 37.7% were ZEVs – a 17.4 percentage "
       "point increase since 2023 (20.3%) and well above the EU average of 13.6%.”"),
     C("Full text read (Council PDF), 5 Oct 2026."), C("<b>The claim</b>")],
    [C("<b>Eurostat</b>, road_eqr_carpda and road_eqs_carpda [2, 3]"),
     C("New passenger cars and the car stock by type of motor energy, every member state."),
     C("Downloaded 5 Oct 2026 (data/cc-110/)."), C("<b>Primary data</b>")],
], [38 * mm, 74 * mm, 36 * mm, 22 * mm]))

S += [Spacer(1, 4 * mm), SectionHeading(2, "Method")]
S.append(P("<b>Question.</b> Do the figures reproduce, and is Malta “well above” the EU average?"))
S.append(P("<b>Evidence.</b> We downloaded Eurostat’s new passenger cars by type of motor energy (road_eqr_carpda, "
           "updated 1 September 2026) for every member state and the EU-27, 2019–2025, and the passenger-car stock "
           "(road_eqs_carpda) for Malta and the EU-27 (<i>tools/cc-110-report/fetch.py</i>). A zero-emission vehicle "
           "is battery electric or hydrogen fuel cell; plug-in hybrids are excluded. Every figure is recomputed in "
           "<i>calc.py</i> (outputs in <i>data/cc-110/checks.csv</i>). No Eurostat flags apply to the Malta values."))
S.append(P("<b>Grades.</b> Official statistics are grade C. The claim is statistical; no literature is needed to "
           "test it. <b>Verdicts</b> follow the five-point scale in Appendix A."))

S.append(CondPageBreak(110 * mm))
S.append(SectionHeading(3, "What the data show"))
S.append(fig(FIG / "fig1_share.png", width=CW * 0.95))
S.append(P("Figure 1. Zero-emission share of new passenger cars, Malta, the EU-27 and Denmark, 2019–2025.", cap))
S.append(P("Malta’s share rose from 3.7% in 2019 to 15.4% in 2022, 20.3% in 2023 and 37.7% in 2024, and held at "
           "37.6% in 2025. The EU-27 share was 14.5% in 2023 and 13.5% in 2024, before rising to 17.3% in 2025. Of "
           "Malta’s 7,683 new cars in 2024, 2,893 were battery electric and 508 plug-in hybrids (6.6%, not counted)."))
S.append(fig(FIG / "fig2_rank.png", width=CW * 0.95))
S.append(P("Figure 2. Zero-emission share of new passenger cars by member state, 2024.", cap))

S.append(CondPageBreak(80 * mm))
S.append(SectionHeading(4, "Where the evidence points different ways"))
S.append(contested("Does a high share of new cars mean a cleaner fleet?", "NOT YET", AMBER,
                   "Malta’s new-car market moved faster than all but one member state, and the stock of zero-emission "
                   "cars nearly doubled in 2024 (4,364 to 7,301).",
                   "Zero-emission cars were 2.2% of the 330,484 passenger cars at the end of 2024, the EU average. The "
                   "fleet grew by 6,632 cars in 2024, about 18 a day. The same report notes that Malta had installed "
                   "about a quarter of the charging infrastructure needed for its 2030 targets.",
                   "The claim is about new registrations and is accurate. It is not evidence that road-transport "
                   "emissions are falling, which the report itself says they are not (see CC-109).",
                   label_a="WHAT THE SHARE SHOWS", label_b="WHAT IT DOES NOT SHOW"))

S.append(CondPageBreak(110 * mm))
S.append(SectionHeading(5, "Testing the claim"))
verd = lambda t, c: chip(t, c, w=29 * mm)
S.append(std_table([
    [C("Sub-claim", cellh), C("Said by", cellh), C("What the evidence shows", cellh), C("Rating", cellh)],
    [C("<b>A.</b> 7 700 new passenger cars in 2024, 37.7% of them zero-emission"), C("Commission [1]"),
     C("Eurostat: 7,683 new cars, 2,893 battery electric, no hydrogen: 37.65%."), verd("ACCURATE", GREENC)],
    [C("<b>B.</b> Up 17.4 points from 20.3% in 2023"), C("Commission [1]"),
     C("2023 share 20.31%. The rise is 17.34 points from unrounded shares, 17.35 from the report’s own annex values."),
     verd("ACCURATE", GREENC)],
    [C("<b>C.</b> Well above the EU average of 13.6%"), C("Commission [1]"),
     C("Eurostat EU-27: 13.53%. Malta is second of 27 member states, after Denmark."), verd("ACCURATE", GREENC)],
], [42 * mm, 18 * mm, 76 * mm, 34 * mm], valign="MIDDLE"))

S += [Spacer(1, 6 * mm), SectionHeading(6, "Verdict and requests for evidence"),
      verdict_box("Supported", "The figures reproduce from Eurostat and Malta is second in the EU. Confidence: high."),
      Spacer(1, 4 * mm)]
S.append(P("<b>Why.</b> The registration count, both shares and the comparison with the EU reproduce from Eurostat; "
           "the EU average differs by 0.07 points, which changes nothing. <b>What this verdict does not say.</b> It "
           "does not say Malta’s car fleet or transport emissions are falling: new cars are a small part of the fleet, "
           "and the fleet keeps growing. Transport emissions are checked in CC-109."))
S.append(P("Evidence we are asking for", h2))
S.append(requests_list(["From the Commission: the source of the EU average of 13.6% (Eurostat gives 13.5%)."]))
S += [Spacer(1, 4 * mm),
      callout([P("RIGHT OF REPLY", tag),
               P("Not needed for this verdict (maintainer rule of 5 October 2026).", small)], bg=AMBER_PALE, bar=AMBER)]
S += [Spacer(1, 6 * mm), SectionHeading(7, "Limitations")]
for l in ["Registration statistics count first registrations in the country, including imported used cars only where "
          "national practice does; definitions follow Eurostat’s road transport methodology.",
          "We did not test the light commercial vehicle figures in the same passage.",
          "We read the report in its Council copy; the Commission’s own publication should be identical."]:
    S.append(P("• " + l, bul))
S += [Spacer(1, 6 * mm), SectionHeading(None, "References")]
S += references([
    ("1", "European Commission (3 June 2026). 2026 Country Report – Malta. SWD(2026) 218 final; Council document "
          "10135/26 ADD 1. Annex 8 and statistical annex.",
     "https://data.consilium.europa.eu/doc/document/ST-10135-2026-ADD-1/en/pdf"),
    ("2", "Eurostat. New passenger cars by type of motor energy (road_eqr_carpda), updated 1 Sep 2026, retrieved 5 Oct 2026.",
     "https://ec.europa.eu/eurostat/databrowser/view/road_eqr_carpda/default/table"),
    ("3", "Eurostat. Passenger cars by type of motor energy (road_eqs_carpda), retrieved 5 Oct 2026.",
     "https://ec.europa.eu/eurostat/databrowser/view/road_eqs_carpda/default/table"),
    ("4", "MiŻien. Calculation script and outputs: tools/cc-110-report/calc.py; data/cc-110/checks.csv.", ""),
])
S.append(PageBreak())
S += appendix_a("A experiment · B observational study with a control or gradient · C review, guidance or "
                "official statistics · D assertion or anecdote. ◆ marks a source known only second-hand.")
S += [Spacer(1, 5 * mm)]
S += revision_log([("1.0", "5 Oct 2026", "First issue. Verdict Supported (high confidence); no right of reply needed.")])

build_report(Report(
    number="110", out=str(FIG / "report.pdf"), kicker="Statistics and EU data",
    title_lines=["37.7% of new", "cars zero-", "emission?"],
    subtitle_lines=["Testing the European Commission’s 2026 Country Report", "against Eurostat registration data"],
    quote_lines=["“In 2024, Malta recorded 7 700 new passenger car", "registrations, of which 37.7% were ZEVs … well above",
                 "the EU average of 13.6%.”"], quote_size=14,
    attribution="European Commission, 2026 Country Report – Malta, 3 June 2026.",
    context="Annex 8, on the decarbonisation of Malta’s vehicle fleet.",
    verdict="Supported", verdict_note="Malta is second in the EU for zero-emission new cars",
    footer_lines=["Version 1.0  ·  5 October 2026", "Status: no right of reply needed",
                  "Prepared from public sources and Eurostat data.", "Repository: github.com/leandergrech/Mizien"],
    running_head="Zero-emission new cars – Commission 2026 Country Report", version="1.0", date="5 October 2026",
    status_note="no right of reply needed",
    pdf_title="37.7% of new cars zero-emission? Claim Check 110",
    pdf_subject="Tests the European Commission's 2026 Country Report figures on zero-emission new cars in Malta",
    story=S))
