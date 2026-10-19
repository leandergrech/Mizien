"""Claim Check 124 report. Run fetch.py, calc.py and figures.py first. Output: out/report.pdf"""
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
      P("The Climate Change Performance Index (CCPI) 2026 country page for Malta, published under Germanwatch’s copyright notice, says "
        "<b>“Malta ranks 25th in the CCPI, up nine spots and a medium performer.”</b> Its text adds that the country experts "
        "“criticise the lack of concrete efforts to reduce greenhouse (GHG) emissions”, that Malta’s share of renewable energy is low, "
        "that “automobile use has not decreased” although public transport has been free since October 2022, and that offshore wind has "
        "“not moved beyond the planning stage”. We tested what Eurostat and the operator’s own pages can answer; "
        "the rank itself was not reproduced.", lead)]
S.append(key_points([
    ("Renewables are low, but rising fast.",
     "Renewables were 17.2% of gross final energy consumption in 2024 (EU-27 25.2%), the 4th lowest of 27 Member States; "
     "Malta gained 9.0 points since 2019, the EU-27 5.4."),
    ("Car use has not fallen in total.",
     "Passenger cars rose 5.8% from 2022 to 2025 (317,234 to 335,693) and road-transport energy 4.6% from 2022 to 2024. Per head the picture "
     "is flatter: cars per 1,000 residents fell from 585 to 571 and Eurostat’s estimated car share of passenger-km from 82.9% to 80.3%."),
    ("Electric cars have risen sharply, from a small base.",
     "Battery-electric cars grew from 1,783 (2021) to 9,790 (2025), 2.9% of the fleet, the same share as the EU-27 (2.9%)."),
    ("Offshore wind is still at the procurement stage.",
     "InterConnect Malta’s April 2026 tender for two years of wind and wave data calls the project Malta’s possible “first-ever wind generation”; "
     "no turbine exists (see CC-029)."),
    ("Verdict: largely supported (moderate confidence).",
     "The testable statements hold; car use is up in total but flat or slightly down per head. The rank and the experts’ "
     "judgement are not testable from public data."),
]))
S += [Spacer(1, 2.5 * mm), VerdictMeter(1), Spacer(1, 3 * mm),
      tiles([("17.2%", RED, "of gross final energy from renewables in 2024: 4th lowest of 27 (EU-27 25.2%)"),
             ("+5.8%", ORANGE, "more passenger cars, 2022 to 2025; road-transport energy +4.6% to 2024"),
             ("9,790", GREEN, "battery-electric cars in 2025, up from 1,783 in 2021 (2.9% of the fleet, as in the EU-27)"),
             ("-11.6%", GREEN, "greenhouse gases per resident, 2022 to 2024 (4.3 to 3.8 t CO2e, excluding LULUCF)")]),
      Spacer(1, 4 * mm),
      up_down("The CCPI report with Malta’s indicator scores, weights and the anonymous experts’ questionnaire; vehicle-kilometre or "
              "traffic-count data for 2022 to 2025 that Eurostat’s estimates do not provide.",
              "Traffic counts showing a clear fall in car-kilometres per resident since October 2022 (against our finding of flat or slightly lower per-head use), or a "
              "wind-farm contract and a turbine in the water (against the “planning stage” finding)."),
      Spacer(1, 3 * mm)]
S += toc([("1", "The claim and what we could verify"), ("2", "Method"), ("3", "What the research says"),
          ("4", "What the data show"), ("5", "Where the evidence points different ways"),
          ("6", "Testing the claim"), ("7", "Verdict and requests for evidence"), ("8", "Limitations")])
S.append(PageBreak())

# ================================================================== 1
S.append(SectionHeading(1, "The claim and what we could verify"))
S.append(P("The text is on the CCPI’s Malta country page [1], read in full on 18 and 19 October 2026 and archived. The page is undated; "
           "it belongs to the 2026 edition, which the CCPI’s download page dates 18 November 2025 [2]. Its footer carries a "
           "“© 2026 Germanwatch” notice and its authors are not named on the country page. It says the national experts "
           "“chose to remain anonymous”. We treat the page as the index’s own statement and rate the sentences below as written. "
           "The MaltaToday listing that locates the story could not be read (403) and is not used."))
S.append(std_table([
    [C("What the page says (verbatim; the page’s own words)", cellh), C("Access", cellh)],
    [C("“Malta ranks 25th in the CCPI, up nine spots and a medium performer. The country receives medium ratings in GHG Emissions, "
       "Energy Use, and Climate Policy, and low in Renewable Energy.”"), C("Read in full [1]")],
    [C("“…the CCPI country experts criticise the lack of concrete efforts to reduce greenhouse (GHG) emissions, as well as poor climate policy implementation.”"),
     C("Read in full [1]")],
    [C("“Malta’s energy consumption still has a low renewable energy share. While the experts note some progress in solar energy use, they denounce "
       "offshore wind energy as having not moved beyond the planning stage.”"), C("Read in full [1]")],
    [C("“While public transport in Malta has been free since October 2022, at least for citizens holding a tallinja card, the experts note that "
       "automobile use has not decreased …”; “a substantial increase in the number of electric vehicles”"), C("Read in full [1]")],
], [140 * mm, 30 * mm]))
S += [Spacer(1, 4 * mm),
      callout([P("SCOPE NOTE", tag),
               P("The CCPI also criticises energy subsidies and cycle-lane building, and says there is “little to no political will” for a fossil-fuel phase-out. "
                 "Those statements are judgements or concern policies tested in other checks (CC-022, CC-095, CC-071) and are not rated here. "
                 "This check does not compare Malta with other countries’ ranks.", small)],
              bg=AMBER_PALE, bar=AMBER), Spacer(1, 4 * mm)]

# ================================================================== 2
S.append(SectionHeading(2, "Method"))
S.append(P("<b>Question.</b> Do Eurostat’s series and the operator’s own pages support the testable statements on Malta’s country page, "
           "and can the rank be checked?"))
S.append(P("<b>Evidence.</b> Eurostat: passenger cars by power source (road_eqs_carpda) and per 1,000 residents (road_eqs_carhab), final energy in "
           "road transport (nrg_bal_c), modal split (tran_hv_psmod), renewable share (nrg_ind_ren), greenhouse-gas emissions (sdg_13_10) and population (demo_gind), "
           "retrieved 19 October 2026 with status flags [3]; InterConnect Malta’s project pages [4, 5]; two peer-reviewed papers [6, 7]. Every number was "
           "recomputed by <i>tools/cc-124-report/calc.py</i> from files in <i>data/cc-124/</i>."))
S.append(P("<b>Grades.</b> Official statistics are grade C; peer-reviewed studies are grade B; an index’s expert opinion is grade D. "
           "<b>Verdicts</b> follow the five-point scale in Appendix A."))

# ================================================================== 3
S.append(CondPageBreak(60 * mm))
S.append(SectionHeading(3, "What the research says"))
S.append(P("Composite indices turn many indicators into one rank, and the rank can move with construction choices. Saisana, Saltelli and "
           "Tarantola propose uncertainty and sensitivity analysis to assess how reliable such country rankings are [7]. We "
           "could not obtain the CCPI report, so we cannot say how stable Malta’s 25th place is. It also depends on the results of the other countries scored (63 countries and the EU [2])."))
S.append(P("Free fares do not by themselves guarantee fewer car trips. In Tallinn’s full-scale fare-free scheme, public-transport use rose "
           "14% almost a year after introduction, less than earlier studies reported because service was already good and fares already low [6]. "
           "The abstract does not give the effect on car use, and Tallinn is not Malta; it shows only that a ridership gain and a car-use "
           "fall are separate questions."))

# ================================================================== 4
S.append(CondPageBreak(150 * mm))
S.append(SectionHeading(4, "What the data show"))
S.append(P("Car use", h2))
S.append(fig(FIG / "fig1_car_use.png"))
S.append(P("Figure 1. Left: passenger cars (Eurostat road_eqs_carpda), road-transport final energy (nrg_bal_c; 2025 not yet published) and "
           "population on 1 January of the following year (demo_gind), each indexed to 2022. Right: modal split of inland passenger-km; every "
           "Malta value is an estimate (flag e).", cap))
S.append(P("Free public transport began in October 2022 [1]. Between 2022 and 2025 passenger cars rose from 317,234 to 335,693 (+5.8%); population grew "
           "8.5% over the same span, so cars per 1,000 residents fell from 585 to 571 (EU-27: 564 to 584; Malta was 609 in 2018). Road-transport "
           "final energy rose from 232.2 to 242.8 ktoe (+4.6%) between 2022 and 2024, 7.3% above 2019; per resident it was roughly flat "
           "(428 to 423 kg of oil equivalent, −1.3%; population timing differs by a year). Eurostat’s modal-split estimates put the car share at 82.9% "
           "in 2022 and 80.3% in 2024, and the bus share at 17.1% and 19.7%. Total car use, in cars and fuel, has therefore not fallen; "
           "per resident it is flat to slightly lower. We have no vehicle-kilometre series."))
S.append(P("Renewables and electric cars", h2))
S.append(fig(FIG / "fig2_renewables_ev.png"))
S.append(P("Figure 2. Left: renewable share of gross final energy consumption in 2024 (Eurostat nrg_ind_ren). Right: battery-electric passenger cars in Malta "
           "(Eurostat road_eqs_carpda, code ELC).", cap))
S.append(P("Malta’s renewable share was 8.2% in 2019 and 17.2% in 2024 (EU-27: 25.2%); the provisional 2025 value is 18.8% (EU-27 26.2%), "
           "5th lowest. Malta ranked 4th lowest in 2024 behind Belgium (14.3%), Luxembourg (14.7%) and Ireland (16.1%). The CCPI’s "
           "renewable indicator is “% of TPES” (total primary energy supply) and a target comparison, not the final-consumption share we use, so "
           "“low” is tested here only as a direction. Battery-electric cars rose from 983 (2019) to 1,783 (2021) and 9,790 (2025), 2.92% of the "
           "fleet against 2.88% in the EU-27; with plug-in hybrids the share is 4.45% (EU-27 4.64%). That is a large increase, from a small base, and no "
           "faster than in the EU as a whole."))
S.append(P("Emissions and offshore wind", h2))
S.append(P("Greenhouse-gas emissions excluding land use (Eurostat sdg_13_10) were 4.3 t CO2e per resident in 2022, 4.0 in 2023 and 3.8 in 2024 (−11.6%), "
           "and 82.7% of the 1990 level in 2024 (85.9% in 2022). Total emissions fell about 4% over the period (2.3 to 2.2 Mt CO2e, "
           "rounded values). A fall is not the same as “concrete efforts”, and we did not compare it with Malta’s targets or the EU-27 (no EU-27 series in this dataset). "
           "On wind, InterConnect Malta describes a competitive-dialogue process for a floating wind farm of about 300 MW beyond 12 nautical miles [4]; "
           "its 22 April 2026 release announces a EUR 3.6 million tender to collect two years of wind, wave and wildlife data and speaks of Malta’s "
           "“first-ever wind generation” [5]. No turbine or concession contract has been announced; claim check CC-029 records the "
           "timetable and the lack of a public notice of the next stage as of 6 October 2026."))

# ================================================================== 5
S.append(CondPageBreak(120 * mm))
S.append(SectionHeading(5, "Where the evidence points different ways"))
S.append(contested(
    "Q1  Has car use not decreased?", "IN TOTAL YES; PER HEAD FLAT", AMBER,
    "Cars are up 5.8% since 2022 and road-transport energy up 4.6% (2022 to 2024), above its pre-COVID level.",
    "Population grew faster than the fleet: cars per 1,000 residents fell from 585 to 571 and Eurostat’s estimated car share of passenger-km fell 2.6 points to 80.3%, "
    "while the bus share rose to 19.7% (all Malta values are estimates).",
    "<b>For this claim:</b> “has not decreased” holds for total cars and fuel, not for the per-head and modal-share measures."))
S.append(contested(
    "Q2  Does the “lack of concrete efforts” on emissions hold?", "A JUDGEMENT; DATA MIXED", AMBER,
    "Emissions per resident fell 11.6% from 2022 to 2024 and the total fell about 4%; per-resident fell from 4.2 t in 2018 to 3.8 t.",
    "Emissions are still 82.7% of the 1990 level, renewables are among the EU’s lowest, and road-transport energy is above 2019. The experts’ questionnaire is unseen.",
    "<b>For this claim:</b> a falling trend does not contradict a judgement about ambition; the judgement is not testable from public data."))
S.append(contested(
    "Q3  Is Malta’s rank evidence of performance?", "NOT TESTED", AMBER,
    "The rank moved from 34th to 25th (second-hand: Wikipedia lists 55.78 and 60.44 points), consistent with the page’s “up nine spots”.",
    "The rank depends on other countries’ results, on indicator weights and on an expert survey, and rankings can be sensitive to such choices [7]. The report was not read.",
    "<b>For this claim:</b> we confirm only that the arithmetic of nine places is consistent; we do not rate the index’s method."))

# ================================================================== 6
S.append(CondPageBreak(110 * mm))
S.append(SectionHeading(6, "Testing the claim"))
verd = lambda t, c: chip(t, c, w=29 * mm)
S.append(std_table([
    [C("Sub-claim", cellh), C("What the evidence shows", cellh), C("Rating", cellh)],
    [C("<b>A.</b> Malta “ranks 25th … up nine spots and a medium performer”"),
     C("Internally consistent with 34th in 2025 (second-hand ◆); scores, weights and method not read [1, 2]."), verd("NOT TESTED", AMBER)],
    [C("<b>B.</b> Low rating for renewable energy; “low renewable energy share”"),
     C("17.2% in 2024, 4th lowest of 27 (EU-27 25.2%); rising faster than the EU [3]."), verd("SUPPORTED", GREENC)],
    [C("<b>C.</b> “Automobile use has not decreased” since free public transport began"),
     C("Cars +5.8% (2022–25) and road energy +4.6% (2022–24); per resident flat to slightly lower; car share of passenger-km 82.9% to 80.3% (estimate) [3]."),
     verd("LARGELY SUPPORTED", LG)],
    [C("<b>D.</b> “A substantial increase in the number of electric vehicles”"),
     C("Battery-electric cars 1,783 (2021) to 9,790 (2025); 2.9% of the fleet, as in the EU-27 [3]."), verd("SUPPORTED", GREENC)],
    [C("<b>E.</b> Offshore wind “not moved beyond the planning stage”"),
     C("Competitive dialogue and a metocean data tender (Apr 2026); no wind generation in Malta [4, 5]."), verd("SUPPORTED", GREENC)],
    [C("<b>F.</b> Experts criticise “the lack of concrete efforts to reduce” GHG emissions"),
     C("A judgement. Emissions per resident −11.6% (2022–24) but 82.7% of the 1990 level [3]."), verd("JUDGEMENT", AMBER)],
], [52 * mm, 88 * mm, 30 * mm], valign="MIDDLE"))

# ================================================================== 7
S += [Spacer(1, 6 * mm), SectionHeading(7, "Verdict and requests for evidence"),
      verdict_box("Largely supported", "The testable statements hold with minor caveats; the rank and the experts’ judgement could not be tested. "
                  "Confidence: moderate."), Spacer(1, 4 * mm)]
S.append(P("<b>Why.</b> (1) Renewables are among the EU’s lowest, as the page says, although they have risen faster than the EU’s. "
           "(2) Cars and road fuel are up in total since free public transport began, which supports “has not decreased”; the per-head measures are "
           "flat to slightly down, a caveat that does not reverse it. (3) Electric-car numbers rose sharply and offshore wind has no installation. "
           "Confidence is moderate because the index’s rank and expert survey are unseen and car use is measured by proxies."))
S.append(P("<b>What this verdict does not say.</b> It does not say Malta’s rank is right or wrong, that free public transport has failed, or "
           "that any government or agency has not acted. It says the page’s testable statements broadly match public data."))
S.append(P("Evidence we are asking for", h2))
S.append(requests_list([
    "The CCPI 2026 report and methodology, with Malta’s indicator scores and weights (it is behind a terms-of-use form).",
    "Vehicle-kilometre or traffic-count series for Malta 2019–2025 from Transport Malta or the NSO.",
    "Malta’s greenhouse-gas projections against its 2030 target, to compare with the emissions trend.",
]))

# ================================================================== 8
S += [Spacer(1, 6 * mm), SectionHeading(8, "Limitations")]
for l in ["The CCPI report and methodology PDFs were not obtained (terms-of-use form); the 2025 rank and scores are second-hand (Wikipedia), marked ◆.",
          "Car use is measured by cars registered, road-transport energy and Eurostat’s modal-split estimates (flag e); none is vehicle-kilometres. "
          "Road-transport energy covers all road vehicles, not only cars.",
          "Road-transport energy for 2025 is not yet published; renewable share for 2025 is provisional.",
          "The CCPI’s renewable and emissions indicators (share of primary supply, per capita and target comparisons) differ from the Eurostat measures used here.",
          "Both papers were read as abstracts; neither concerns Malta [6, 7].",
          "The date of free public transport (October 2022) is the page’s statement; we did not re-verify it in this check."]:
    S.append(P("• " + l, bul))

S += [Spacer(1, 6 * mm), SectionHeading(None, "References")]
S += references([
    ("1", "Climate Change Performance Index (Germanwatch). Malta: Climate Performance Ranking 2026. Country page, read 18 and 19 Oct 2026.",
     "https://ccpi.org/country/mlt/"),
    ("2", "Climate Change Performance Index 2026 (report page; publication date 18 Nov 2025; download behind a terms-of-use form).",
     "https://ccpi.org/download/climate-change-performance-index-2026/"),
    ("3", "Eurostat. road_eqs_carpda, road_eqs_carhab, nrg_bal_c, tran_hv_psmod, nrg_ind_ren, sdg_13_10, demo_gind; retrieved 19 Oct 2026 with status flags.",
     "https://ec.europa.eu/eurostat/databrowser/"),
    ("4", "InterConnect Malta. Offshore Renewable Energy Project (project page), read 19 Oct 2026.",
     "https://icm.mt/projects/offshore-renewable-energy-project/"),
    ("5", "InterConnect Malta (22 Apr 2026). Offshore floating wind farm: ICM issues tender to collect data on wind, wave conditions.",
     "https://icm.mt/offshore-floating-wind-farm-icm-issues-tender-to-collect-data-on-wind-wave-conditions/"),
    ("6", "Cats O., Susilo Y.O., Reimal T. (2017). The prospects of fare-free public transport: evidence from Tallinn. <i>Transportation</i> "
          "44(5):1083–1104. doi:10.1007/s11116-016-9695-5. (Abstract read.)", "https://doi.org/10.1007/s11116-016-9695-5"),
    ("7", "Saisana M., Saltelli A., Tarantola S. (2005). Uncertainty and sensitivity analysis techniques as tools for the quality assessment of "
          "composite indicators. <i>Journal of the Royal Statistical Society A</i> 168(2):307–323. doi:10.1111/j.1467-985X.2005.00350.x. (Abstract read.)",
     "https://doi.org/10.1111/j.1467-985X.2005.00350.x"),
    ("8", "Wikipedia. Climate Change Performance Index (table of ranks; second-hand ◆, read 19 Oct 2026).",
     "https://en.wikipedia.org/wiki/Climate_Change_Performance_Index"),
    ("9", "Miżien. Claim check CC-029: First offshore wind farm.", ""),
    ("10", "Miżien. Data and calculations: data/cc-124/; tools/cc-124-report/calc.py.", ""),
])

S.append(PageBreak())
S += appendix_a("A experiment · B observational study with a control or gradient · C review, guidance or "
                "official statistics · D assertion or anecdote. ◆ marks a source known only second-hand.")
S += [Spacer(1, 5 * mm)]
S += revision_log([("1.0", "19 Oct 2026", "First issue. No right of reply needed (verdict Largely supported).")])

build_report(Report(
    number="124", out=str(FIG / "report.pdf"), kicker="Climate performance index, Malta",
    title_lines=["CCPI 2026:", "Malta 25th"],
    subtitle_lines=["Testing the Climate Change Performance Index’s Malta page",
                    "against Eurostat and operator data"],
    quote_lines=["“Malta ranks 25th in the CCPI,", "up nine spots and a medium performer.”"], quote_size=16,
    attribution="Climate Change Performance Index 2026, Malta country page (ccpi.org; © 2026 Germanwatch).",
    context="The page adds that “automobile use has not decreased” and that offshore wind has “not moved beyond the planning stage”.",
    verdict="Largely supported", verdict_note="Testable statements hold; rank untested",
    footer_lines=["Version 1.0  ·  19 October 2026", "Status: draft",
                  "Prepared from public sources, Eurostat and operator data.", "Repository: github.com/leandergrech/Mizien"],
    running_head="CCPI 2026 – Malta", version="1.0", date="19 October 2026",
    pdf_title="CCPI 2026: Malta 25th. Claim Check 124",
    pdf_subject="Tests the statements on the CCPI 2026 Malta country page against Eurostat and ICM data",
    story=S))
