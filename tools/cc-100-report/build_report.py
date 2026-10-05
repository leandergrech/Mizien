"""Claim Check 100 report. Run fetch.py, calc.py and figures.py first. Output: out/report.pdf"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import *  # noqa: E402,F401

FIG = HERE / "out"
S = []
S += [SectionHeading(None, "TL;DR"), Spacer(1, 1 * mm),
      P("In a company announcement to the Malta Stock Exchange on 14 January 2026, Malta International Airport plc "
        "said that December traffic <b>“brought full-year traffic for 2025 up to 10,061,969 passenger movements, "
        "marking a 12.3% increase over the previous year.”</b> We checked the figure against Eurostat’s airport "
        "statistics.", lead)]
S.append(key_points([
    ("The figure is right.",
     "Eurostat records 10,070,972 passengers carried through Malta’s airport in 2025, 0.09% more than the company’s "
     "figure, and 8,968,239 in 2024: an increase of 12.3%, as stated."),
    ("2025 was the first year above 10 million.",
     "Traffic was 7.3 million in 2019 and 7.8 million in 2023; it has grown 38% since 2019."),
    ("“Passenger movements” are not travellers.",
     "Each arrival and each departure is counted, so a visitor or resident on a return trip counts twice. The "
     "company’s public pages sometimes say “passengers” for the same number; its stock-exchange text says “passenger "
     "movements”, which is accurate."),
    ("Verdict: supported (high confidence).",
     "The company’s figure and growth rate are confirmed by independent statistics."),
]))
S += [Spacer(1, 2.5 * mm), VerdictMeter(0), Spacer(1, 3 * mm),
      tiles([("10.06m", GREEN, "Passenger movements in 2025 reported by the company"),
             ("10.07m", GREEN, "Passengers carried in 2025, Eurostat (+0.09%)"),
             ("+12.3%", GREEN, "Growth over 2024, both sources"),
             ("+38%", GREY, "Growth since 2019 (7.3 million)")]),
      Spacer(1, 4 * mm),
      up_down("None: Supported is the top of the scale.",
              "A revision of the airport statistics, or evidence that the company counts a different set of passengers "
              "than Eurostat."),
      Spacer(1, 3 * mm)]
S += toc([("1", "The claim and what we could verify"), ("2", "Method"), ("3", "What the data show"),
          ("4", "What the figure does not say"), ("5", "Testing the claim"),
          ("6", "Verdict and requests for evidence"), ("7", "Limitations")])
S.append(PageBreak())

S.append(SectionHeading(1, "The claim and what we could verify"))
S.append(P("The claim record came from the company’s “Facts and Figures” page, which on 5 October 2026 still said the "
           "airport was “eyeing 9.3 million passenger movements by the end of 2025”, an outdated forecast. The "
           "company’s statement of the outcome is its full-year traffic update, company announcement 461/2026 of "
           "14 January 2026 [1], read in full. Lovin Malta reported a Facebook post by the company on 30 December 2025 "
           "saying it had handled “a record 10 million passengers” [2]."))
S.append(std_table([
    [C("Source", cellh), C("What it says", cellh), C("Our access", cellh), C("Status", cellh)],
    [C("<b>Malta International Airport plc</b>, company announcement 461/2026, 14 Jan 2026 [1]"),
     C("“This figure brought full-year traffic for 2025 up to 10,061,969 passenger movements, marking a 12.3% increase "
       "over the previous year.”"), C("Full PDF read, 5 Oct 2026."), C("<b>The claim</b>")],
    [C("<b>Eurostat</b>, avia_paoc [3]"), C("Passengers carried at Malta’s airport by year, schedule and destination."),
     C("Downloaded 5 Oct 2026 (data/cc-100/)."), C("<b>Primary data</b>")],
], [38 * mm, 74 * mm, 36 * mm, 22 * mm]))

S += [Spacer(1, 4 * mm), SectionHeading(2, "Method")]
S.append(P("<b>Question.</b> Did Malta’s airport handle more than 10 million passenger movements in 2025, and did "
           "traffic grow by 12.3%?"))
S.append(P("<b>Evidence.</b> We downloaded Eurostat’s air passenger transport for Malta (avia_paoc, updated 2 October "
           "2026), 2015–2025 (<i>tools/cc-100-report/fetch.py</i>), recorded the company’s figures from its "
           "announcement (<i>data/cc-100/mia_announcements.csv</i>) and compared them (<i>calc.py</i>; outputs in "
           "<i>data/cc-100/checks.csv</i>). Eurostat’s “passengers carried” counts arriving and departing passengers at the "
           "reporting airport, the same concept as the company’s “passenger movements”. Malta has one airport, so the "
           "national figure is the airport’s."))
S.append(P("<b>Grades.</b> Official statistics, grade C; the company’s figure is its own report. No literature is "
           "needed. <b>Verdicts</b> follow the five-point scale in Appendix A."))

S.append(CondPageBreak(100 * mm))
S.append(SectionHeading(3, "What the data show"))
S.append(fig(FIG / "fig1_passengers.png", width=CW * 0.95))
S.append(P("Figure 1. Passengers carried through Malta’s airport, 2015–2025 (Eurostat).", cap))
S.append(P("Traffic passed 10 million for the first time in 2025. Eurostat’s total exceeds the company’s by 9,003 "
           "passengers (0.09%), a difference of the kind expected between an operator’s count and the statistical "
           "return. 29% of 2025 passengers flew to or from airports outside the EU."))

S.append(Spacer(1, 4 * mm))
S.append(SectionHeading(4, "What the figure does not say"))
S.append(P("The claim is about traffic, not about its effects. Ten million movements are roughly five million return "
           "journeys by visitors and residents. Growth in air traffic bears on other claims in this project: the "
           "airport’s carbon-neutrality claim (CC-030), the growth of tourism (CC-083 to CC-085) and the pressure of "
           "visitor numbers on infrastructure (CC-089). This check does not assess any of those."))

S.append(CondPageBreak(90 * mm))
S.append(SectionHeading(5, "Testing the claim"))
verd = lambda t, c: chip(t, c, w=29 * mm)
S.append(std_table([
    [C("Sub-claim", cellh), C("Said by", cellh), C("What the evidence shows", cellh), C("Rating", cellh)],
    [C("<b>A.</b> Full-year traffic for 2025 of 10,061,969 passenger movements"), C("MIA plc [1]"),
     C("Eurostat: 10,070,972 passengers carried in 2025 (+0.09%). First year above 10 million."), verd("ACCURATE", GREENC)],
    [C("<b>B.</b> A 12.3% increase over the previous year"), C("MIA plc [1]"),
     C("Eurostat: 8,968,239 in 2024 to 10,070,972 in 2025, +12.3%."), verd("ACCURATE", GREENC)],
], [42 * mm, 18 * mm, 76 * mm, 34 * mm], valign="MIDDLE"))

S += [Spacer(1, 6 * mm), SectionHeading(6, "Verdict and requests for evidence"),
      verdict_box("Supported", "Independent statistics confirm the total and the growth rate. Confidence: high."),
      Spacer(1, 4 * mm)]
S.append(P("<b>Why.</b> Both numbers reproduce from Eurostat within a tenth of a percent. <b>What this verdict does "
           "not say.</b> It does not say whether the growth is good or sustainable; it confirms a count."))
S.append(P("Evidence we are asking for", h2))
S.append(requests_list(["From the company: an update of its Facts and Figures page, which still shows the 2025 "
                        "forecast of 9.3 million."]))
S += [Spacer(1, 4 * mm),
      callout([P("RIGHT OF REPLY", tag), P("Not needed for this verdict (maintainer rule of 5 October 2026).", small)],
              bg=AMBER_PALE, bar=AMBER)]
S += [Spacer(1, 6 * mm), SectionHeading(7, "Limitations")]
for l in ["Eurostat’s and the company’s counts can differ slightly in their treatment of transit and transfer "
          "passengers; the difference here is 0.09%.",
          "We did not read the company’s Facebook post itself, only Lovin Malta’s report of it."]:
    S.append(P("• " + l, bul))
S += [Spacer(1, 6 * mm), SectionHeading(None, "References")]
S += references([
    ("1", "Malta International Airport plc (14 Jan 2026). Full-Year Traffic Update. Company announcement 461/2026.",
     "https://maltairport.com/app/uploads/2026/01/Full-Year-Traffic-Update.pdf"),
    ("2", "Lovin Malta (30 Dec 2025). Malta International Airport Records Milestone Year With 10 Million Passengers.",
     "https://lovinmalta.com/malta/malta-international-airport-records-milestone-year-with-10-million-passengers/"),
    ("3", "Eurostat. Air passenger transport by type of schedule, transport coverage and country (avia_paoc), updated "
          "2 Oct 2026, retrieved 5 Oct 2026.", "https://ec.europa.eu/eurostat/databrowser/view/avia_paoc/default/table"),
    ("4", "MiŻien. Calculation script and outputs: tools/cc-100-report/calc.py; data/cc-100/checks.csv.", ""),
])
S.append(PageBreak())
S += appendix_a("A experiment · B observational study with a control or gradient · C review, guidance or "
                "official statistics · D assertion or anecdote. ◆ marks a source known only second-hand.")
S += [Spacer(1, 5 * mm)]
S += revision_log([("1.0", "5 Oct 2026", "First issue. Verdict Supported (high confidence); no right of reply needed.")])

build_report(Report(
    number="100", out=str(FIG / "report.pdf"), kicker="Statistics and company reports",
    title_lines=["Over 10 million", "airport", "passengers?"],
    subtitle_lines=["Testing Malta International Airport’s 2025 traffic", "figure against Eurostat"],
    quote_lines=["“…full-year traffic for 2025 up to 10,061,969 passenger", "movements, marking a 12.3% increase over the",
                 "previous year.”"], quote_size=14,
    attribution="Malta International Airport plc, company announcement 461/2026, 14 January 2026.",
    context="Full-year traffic update to the Malta Stock Exchange.",
    verdict="Supported", verdict_note="Eurostat: 10,070,972 passengers in 2025, +12.3%",
    footer_lines=["Version 1.0  ·  5 October 2026", "Status: no right of reply needed",
                  "Prepared from public sources and Eurostat data.", "Repository: github.com/leandergrech/Mizien"],
    running_head="Airport passengers 2025 – Malta International Airport", version="1.0", date="5 October 2026",
    status_note="no right of reply needed",
    pdf_title="Over 10 million airport passengers? Claim Check 100",
    pdf_subject="Tests Malta International Airport's 2025 passenger traffic figure",
    story=S))
