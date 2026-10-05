"""Claim Check 030 report. Run calc.py and figures.py first. Output: out/report.pdf"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import *  # noqa: E402,F401

FIG = HERE / "out"
S = []

# ================================================================== TL;DR
S += [SectionHeading(None, "TL;DR"), Spacer(1, 1 * mm),
      P("On 25 May 2026 Malta International Airport (MIA) announced that it is implementing a "
        "<b>“€12.5 million Airfield Electrification Programme, which is set to avoid the emission of an average of "
        "1,000 tonnes of carbon dioxide annually”</b> [1]. The company also describes itself as carbon neutral "
        "after reaching Level 3+ of Airport Carbon Accreditation (ACA) in 2025 [2, 3]. We tested both statements "
        "against the company’s own 2025 sustainability report, the ACA rules, and what an airport’s footprint "
        "contains.", lead)]
S.append(key_points([
    ("Carbon neutrality, as ACA defines it, is documented.",
     "MIA bought 5,450 t of credits for 2025. Its Scope 1 (813 t), location-based Scope 2 (4,582 t) and business "
     "travel (49 t) add up to 5,444 t, within 0.1% of the credits [2]. PwC Malta gave limited assurance on Scope 1 "
     "and 2 [2]."),
    ("“Neutral” covers about 1% of the footprint the airport reports.",
     "Scope 3, mostly aircraft, is 99.3% of the 738,308 t reported for 2025 [2]. ACA Level 3+ does not require "
     "offsetting it [4]. Emissions inside the neutrality boundary rose 8% in 2025 and are 22% below 2015, against "
     "a company target of −65% by 2030 [2, 3]."),
    ("The 1,000 t figure is a projection, and a plausible one.",
     "It is 18.5% of Scope 1 and 2 but 0.14% of Scope 3. It needs about 11,000–25,000 hours of diesel ground power "
     "replaced a year under illustrative emission rates, which is 20–46 minutes per turnaround if spread over "
     "all turnarounds. The release does not say whether the saving is gross or net of grid electricity."),
    ("The saving falls in Scope 3, not in the neutral boundary.",
     "Ground power for aircraft is reported under Scope 3 [2], which fits the company’s own words: the project "
     "addresses “Scope 3 emissions” [1]."),
    ("Verdict: largely supported (moderate confidence).",
     "The neutrality claim is documented and the programme is real and co-financed; the avoided tonnes cannot be "
     "checked before the system runs in 2028, and “neutral” needs its scope stated."),
]))
S += [Spacer(1, 4 * mm), VerdictMeter(1), Spacer(1, 3 * mm),
      tiles([("5,444 t", GREEN, "Scope 1 + 2 + business travel, 2025, against 5,450 t of credits bought"),
             ("99.3%", ORANGE, "Share of the airport’s reported footprint that is Scope 3"),
             ("1,000 t", GREEN, "Projected CO₂ avoided a year from 2028, 18.5% of Scope 1 + 2"),
             ("−22%", ORANGE, "Scope 1 + 2 in 2025 against 2015 (target −65% by 2030)")]),
      Spacer(1, 4 * mm),
      up_down("Published method for the 1,000 t (diesel baseline, hours, grid emissions), or measured savings once "
              "the first hatch pits operate; the ACA certificate and credit retirements checked at the registries.",
              "A method showing the 1,000 t is gross and that net savings after grid electricity are much smaller; "
              "or a registry record showing the credits were not retired for 2025."),
      Spacer(1, 5 * mm)]
S += toc([("1", "The claim and what we could verify"), ("2", "Method"), ("3", "What carbon neutrality means here"),
          ("4", "What the data show"), ("5", "Where the evidence points different ways"),
          ("6", "Testing the claim"), ("7", "Verdict and requests for evidence"), ("8", "Limitations")])
S.append(PageBreak())

# ================================================================== 1
S.append(SectionHeading(1, "The claim and what we could verify"))
S.append(P("The wording is in a Malta International Airport press release [1], which we read on the company’s "
           "website. The company’s sustainability report for 2025 [2] and its sustainability page [3] contain the "
           "carbon-neutrality statements. The Malta Independent carried the release on 25 May 2026 under the "
           "headline “Airfield electrification at MIA set to avoid 1,000 tonnes of carbon dioxide emissions every "
           "year”; we could not read that article from our network and did not rely on it."))
S.append(std_table([
    [C("What was said", cellh), C("Form", cellh), C("Our access", cellh)],
    [C("“…implementing a €12.5 million Airfield Electrification Programme, which is set to avoid the emission of an "
       "average of 1,000 tonnes of carbon dioxide annually.” Completion expected by 2028."),
     C("Company press release [1]"), C("Read in full")],
    [C("35 hatch-pit systems, mobile battery ground power units with 20 charging points, 15 electric bus charging "
       "points, five medium-voltage substations; EU grant of €5.4 million."), C("Company press release [1]"),
     C("Read in full")],
    [C("Progression to Level 3+ of ACA in 2025, “having satisfied criteria related to the reduction of direct "
       "emissions and the offsetting of residual emissions, namely 5,450 tonnes of carbon dioxide”."),
     C("Company sustainability report 2025 [2]"), C("Read in full")],
    [C("“Reaching carbon neutral status in 2025” as a target; “Net Zero Carbon Plan … carbon neutrality by 2025 "
       "and net zero carbon emissions by 2050”."), C("Company website [3]"), C("Read in full")],
], [104 * mm, 36 * mm, 30 * mm]))
S += [Spacer(1, 4 * mm),
      callout([P("FAIRNESS NOTE", tag),
               P("The release does not claim that the whole airport, or flights, are carbon neutral, and the "
                 "company’s head of sustainability says the programme is about “Scope 3 emissions”. The company "
                 "also reports Scope 3 openly, including flight emissions it does not control. The question here is "
                 "what “neutral” and “avoid 1,000 tonnes” can be read to mean.", small)],
              bg=AMBER_PALE, bar=AMBER), Spacer(1, 4 * mm)]

# ================================================================== 2
S.append(SectionHeading(2, "Method"))
S.append(P("<b>Questions.</b> (A) Did MIA reach carbon neutrality as ACA defines it? (B) Is the programme as "
           "described? (C) Is a saving of about 1,000 t CO₂ a year plausible, and how large is it against the "
           "airport’s footprint?"))
S.append(P("<b>Evidence.</b> We read MIA’s Sustainability Report 2025 [2] (GRI 102 tables, pp. 32–33, 124–127, the "
           "assurance statement and the offset appendix), the ACA description of Level 3+ [4], MIA’s release [1], "
           "and one peer-reviewed study of aircraft ground power [5]. Values were transcribed to "
           "<i>data/cc-030/mia_emissions.csv</i> and every ratio recomputed with <i>tools/cc-030-report/calc.py</i> "
           "(<i>data/cc-030/checks.csv</i>). The ACA directory and the offset registries are behind bot walls from "
           "our network and were not consulted."))
S.append(P("<b>Grades.</b> The company’s report is grade D by itself (self-reported) but its Scope 1 and 2 "
           "figures carry limited assurance from PwC Malta, which we treat as grade C. The peer-reviewed study is "
           "grade B. <b>Verdicts</b> follow the five-point scale in Appendix A."))

# ================================================================== 3
S.append(CondPageBreak(90 * mm))
S.append(SectionHeading(3, "What carbon neutrality means here"))
S.append(P("Airport Carbon Accreditation is run by Airports Council International Europe. At Level 3+ an airport "
           "must meet the lower levels, then “offset its remaining Scope 1 and 2 carbon emissions as well as "
           "emissions from staff business travel” with recognised offsets, and must have reduced its emissions as "
           "far as it can first [4]. Scope 1 is fuel burnt by the airport operator; Scope 2 is purchased "
           "electricity; Scope 3 covers everything else, including the aircraft that use the airport. So "
           "“carbon neutral” at Level 3+ is a statement about the operator’s own activity."))
S.append(P("This matters for the second claim. Diesel ground power units belong to ground handlers, so their fuel "
           "is reported as Scope 3 (aircraft emissions “including … GPU usage”) [2]. The programme therefore reduces "
           "a part of Scope 3 that sits outside the neutral boundary. Electricity supplied to aircraft will in turn be "
           "bought from the grid; the report’s own Scope 2 factor is 0.389 kg CO₂ per kWh [2]. A peer-reviewed "
           "analysis of 25,195 turnarounds at 125 airports found external power cuts turnaround emissions by up to "
           "47.6% against running the aircraft’s auxiliary power unit, but that with a diesel ground unit as the "
           "source hydrocarbon emissions doubled [5]: the benefit depends on the baseline replaced."))

# ================================================================== 4
S.append(CondPageBreak(130 * mm))
S.append(SectionHeading(4, "What the data show"))
S.append(fig(FIG / "fig1_scopes.png"))
S.append(P("Figure 1. MIA’s reported 2025 emissions by scope against the projected annual saving and the credits "
           "bought (log scale). Scope 3 for 2025 covers the full flight path; 2024 covered the landing and take-off "
           "cycle only, so the seven-fold rise in Scope 3 is a change of method, not of emissions [2].", cap))
S.append(std_table([
    [C("Indicator", cellh), C("Value", cellh), C("Source", cellh)],
    [C("Scope 1 + Scope 2 (location) + business travel, 2025"), C("813 + 4,582 + 49 = <b>5,444 t</b>"), C("[2]")],
    [C("Credits bought for 2025 residual emissions"), C("<b>5,450 t</b> (Canada 1,670; France 2,160; Uganda 1,620)"),
     C("[2]")],
    [C("Reported footprint 2025, Scope 1 + 2 + 3"), C("738,308 t; Scope 3 = 99.3%"), C("[2], calculated")],
    [C("Aircraft use of sold products, share of Scope 3"), C("673,004 t, 91.8%"), C("[2]")],
    [C("Scope 1 + 2, change 2015 to 2025"), C("6,949 t to 5,395 t, <b>−22%</b>"), C("[2]")],
    [C("Scope 1 + 2, change 2024 to 2025"), C("+8.4% (passengers +12%)"), C("[2]")],
    [C("Programme: 1,000 t a year against Scope 1 + 2 / Scope 3"), C("18.5% / 0.14%"), C("[1, 2], calculated")],
    [C("EU grant share of €12.5 million"), C("43.2% (€5.4 million)"), C("[1]")],
], [76 * mm, 66 * mm, 28 * mm]))
S.append(P("All values in <i>data/cc-030/checks.csv</i>. Scope 1 doubled in 2025 (418 t to 813 t); the report "
           "attributes fuel growth to more vehicle use, firefighting training moved onto airport grounds and "
           "generators for building works [2].", cap))
S.append(fig(FIG / "fig2_gpu.png"))
S.append(P("Figure 2. An inversion of the 1,000 t figure, not an estimate of it. The emission rates on the "
           "horizontal axis are illustrative assumptions; we have not found a sourced figure for Maltese ground "
           "handlers’ units. About 32,700 turnarounds is half of 65,470 aircraft movements reported for 2025 "
           "(second-hand ◆).", cap))
S.append(P("Reading across the data", h2))
for t in ["• <b>The accounting reconciles.</b> The three categories ACA requires add up to 5,444 t "
          "(5,555 t with market-based Scope 2) against 5,450 t of credits, and the credits are itemised by project.",
          "• <b>The boundary is narrow by design.</b> 99.3% of the reported footprint is Scope 3, which Level 3+ "
          "does not ask the airport to offset [4].",
          "• <b>Direct emissions are not yet falling fast.</b> Scope 1 + 2 is 22% below 2015 and rose 8% in 2025. "
          "A reduction of 65% by 2030 [3] needs about 2,430 t from 5,395 t.",
          "• <b>The 1,000 t is of a plausible size.</b> It equals about 30 kg of CO₂ per turnaround across all "
          "turnarounds, or 20–46 minutes of diesel ground power per turnaround at 40–90 kg CO₂ an hour. We cannot "
          "say whether the real baseline is diesel units, aircraft auxiliary power or a mix, nor whether the "
          "1,000 t is net of grid electricity."]:
    S.append(P(t, bul))

# ================================================================== 5
S.append(CondPageBreak(120 * mm))
S.append(SectionHeading(5, "Where the evidence points different ways"))
S.append(contested(
    "Q1  Is the airport carbon neutral?", "YES, AS ACA DEFINES IT", GREEN,
    "Scope 1, 2 and business travel are fully matched by credits, with limited assurance on the first two. "
    "The accreditation scheme sets this definition, and MIA reports its much larger Scope 3 openly.",
    "A reader hearing “carbon neutral” may think of the airport’s whole footprint, including flights. By the "
    "company’s own tables 99.3% of the reported footprint is outside the neutral boundary, and credits were bought "
    "for 0.74% of it.",
    "<b>For this claim:</b> true as defined; the statement should name its scope."))
S.append(contested(
    "Q2  Will the programme avoid 1,000 t a year?", "PLAUSIBLE; NOT VERIFIABLE YET", AMBER,
    "Replacing diesel ground power with grid power at 35 stands plus battery units, in a year with about 32,700 "
    "turnarounds, can deliver tonnes of this order. The figure is an average and is presented as expected.",
    "The release gives no method, baseline or grid emissions. Peer-reviewed work shows the saving depends on what "
    "is replaced (auxiliary power unit or diesel unit) [5]. Nothing can be measured before completion in 2028.",
    "<b>For this claim:</b> a projection; confidence moderate because the inputs are not public."))
S.append(contested(
    "Q3  Does ‘avoid’ mean the airport’s emissions fall?", "NOT NECESSARILY", AMBER,
    "Fewer diesel units reduces fuel burnt on the apron, which lowers Scope 3 and local pollution.",
    "The avoided tonnes sit in Scope 3, outside the neutral boundary, while added electricity use sits in "
    "Scope 2, which the airport offsets.",
    "<b>For this claim:</b> the release is consistent with this, quoting “Scope 3 emissions”."))

# ================================================================== 6
S.append(CondPageBreak(110 * mm))
S.append(SectionHeading(6, "Testing the claim"))
verd = lambda t, c: chip(t, c, w=29 * mm)
S.append(std_table([
    [C("Sub-claim", cellh), C("What the evidence shows", cellh), C("Rating", cellh)],
    [C("<b>A.</b> MIA reached carbon neutrality (ACA Level 3+) in 2025"),
     C("5,444 t in scope against 5,450 t of credits; Scope 1–2 limited assurance by PwC [2]. ACA directory and "
       "registries not checked."), verd("SUPPORTED", GREENC)],
    [C("<b>B.</b> A €12.5 million airfield electrification programme"),
     C("Described in the release with 35 hatch pits, 20 charging points, five substations; 43% EU-funded [1]."),
     verd("ACCURATE", GREENC)],
    [C("<b>C.</b> It will avoid an average of 1,000 t CO₂ a year"),
     C("Plausible size (about 30 kg per turnaround); method, baseline and grid emissions unpublished; completion "
       "2028."), verd("NOT YET TESTABLE", AMBER)],
    [C("<b>D.</b> Scope of ‘neutral’"),
     C("Scope 3 is 99.3% of the reported footprint; Level 3+ does not cover it [2, 4]."),
     verd("NEEDS CONTEXT", AMBER)],
], [52 * mm, 88 * mm, 30 * mm], valign="MIDDLE"))

# ================================================================== 7
S += [Spacer(1, 6 * mm), SectionHeading(7, "Verdict and requests for evidence"),
      verdict_box("Largely supported", "Documented neutrality within its ACA scope; a plausible but unverifiable "
                  "projection. Confidence: moderate. Based on MIA’s assured 2025 figures and the ACA rules."),
      Spacer(1, 4 * mm)]
S.append(P("<b>Why.</b> (1) The offset arithmetic matches the credits to 0.1%, and the two largest items carry "
           "independent limited assurance. (2) The programme is described concretely and co-financed by the EU. "
           "(3) The 1,000 t is of a plausible size but is a company projection with no published method. "
           "(4) The caveats are about scope: “neutral” leaves 99% of the reported footprint outside, and the saved "
           "tonnes fall outside the neutral boundary too. They do not change the substance of what was said, so "
           "the verdict is <i>Largely supported</i> rather than <i>Supported</i>."))
S.append(P("<b>What this verdict does not say.</b> It does not say the credits are of high quality (we did not "
           "assess the three projects), that offsetting is an adequate climate strategy, or that anyone acted in "
           "bad faith. A clearer statement would read: <i>“Our own operations are carbon neutral under ACA Level 3+; "
           "the programme is expected to cut about 1,000 t a year of mainly Scope 3 emissions, on a stated "
           "basis.”</i>"))
S.append(P("Evidence we are asking for", h2))
S.append(requests_list([
    "The calculation behind 1,000 t: baseline equipment, hours, fuel, and electricity added; gross or net.",
    "The ACA certificate for 2025 and the registry records retiring the 5,450 t of credits.",
    "Aircraft movements and ground-power use by year, and the share of stands to be served by hatch pits.",
    "Measured savings once the first stands operate.",
]))
S += [Spacer(1, 4 * mm),
      callout([P("RIGHT OF REPLY", tag),
               P("Not needed under our standards for a <i>Largely supported</i> verdict. The company is welcome to "
                 "supply the evidence listed above, and we will revisit the verdict.", small)],
              bg=AMBER_PALE, bar=AMBER)]

# ================================================================== 8
S += [Spacer(1, 6 * mm), SectionHeading(8, "Limitations")]
for l in ["Most numbers come from the company’s own report. Only Scope 1 and 2 (and energy) were assured; Scope 3 and "
          "the credits were not part of the assurance scope.",
          "We did not retrieve the ACA directory (behind a bot wall) or the Gold Standard and Rainbow Standard "
          "registry records, and did not assess the quality of the credits.",
          "Aircraft movements for 2025 (65,470) are second-hand, from a search-result summary of MIA’s annual "
          "traffic release; monthly releases we read (September 6,013; November 4,973) are consistent with it. "
          "Figure 2 shows a range of assumed emission rates because we found no sourced rate for the equipment "
          "in use at MIA.",
          "The Malta Independent article that carried the release was not readable from our network; we used the "
          "company’s original.",
          "One peer-reviewed study (abstract read) is used for context; no study of Maltese airport ground power "
          "was found."]:
    S.append(P("• " + l, bul))

S += [Spacer(1, 6 * mm), SectionHeading(None, "References")]
S += references([
    ("1", "Malta International Airport (25 May 2026). Airfield electrification at MIA set to avoid 1,000 tonnes of CO₂ "
          "emissions annually. Press release.",
     "https://maltairport.com/corporate-news/airfield-electrification-at-mia-set-to-avoid-1000-tonnes-of-co2-emissions-annually/"),
    ("2", "Malta International Airport plc (2026). Sustainability Report 2025: GRI 102 (pp. 124–125), GRI 103, "
          "Scope 1–3 and offsetting (pp. 32–33), Independent Assurance Report (PwC Malta).",
     "https://maltairport.com/app/uploads/2026/10/Final_MIA26-Sustaibability.pdf"),
    ("3", "Malta International Airport. Sustainability (webpage) and Net Zero Carbon Plan.",
     "https://maltairport.com/corporate/corporate-responsibility/sustainability/"),
    ("4", "Airport Carbon Accreditation. Level 3+ (Neutrality). Airports Council International Europe.",
     "https://www.airportcarbonaccreditation.org/about/7-levels-of-accreditation/neutrality/"),
    ("5", "Padhra A. (2018). Emissions from auxiliary power units and ground power units during intraday aircraft "
          "turnarounds at European airports. <i>Transportation Research Part D</i> 63:433–444. "
          "doi:10.1016/j.trd.2018.06.015. (Abstract read via the UWL repository.)",
     "https://doi.org/10.1016/j.trd.2018.06.015"),
    ("6", "Malta International Airport (2025). Company announcements, September and November 2025 traffic results "
          "(aircraft movements).", "https://maltairport.com/app/uploads/2025/10/September-Traffic-Results.pdf"),
    ("7", "Miżien. Data and calculations: data/cc-030/; tools/cc-030-report/calc.py.", ""),
])

S.append(PageBreak())
S += appendix_a("A experiment · B observational study with a control or gradient · C review, guidance or "
                "official statistics · D assertion or anecdote. ◆ marks a source known only second-hand.")
S += [Spacer(1, 5 * mm)]
S += revision_log([("1.0", "5 Oct 2026", "First issue. No right of reply needed (Largely supported).")])

build_report(Report(
    number="030", out=str(FIG / "report.pdf"), kicker="Airport emissions",
    title_lines=["Carbon neutral,", "and what", "else?"],
    subtitle_lines=["Testing Malta International Airport’s carbon claims", "against its own assured figures"],
    quote_lines=["“…set to avoid the emission of an average of", "1,000 tonnes of carbon dioxide annually.”"], quote_size=16,
    attribution="Malta International Airport plc, press release, 25 May 2026.",
    context="A €12.5 million airfield electrification programme; the airport holds ACA Level 3+ (carbon neutral).",
    verdict="Largely supported", verdict_note="Neutral within its ACA scope; the saving is a plausible projection",
    footer_lines=["Version 1.0  ·  5 October 2026", "Status: no right of reply needed",
                  "Prepared from public sources and company reports.", "Repository: github.com/leandergrech/Mizien"],
    running_head="Airport carbon claims – Malta", version="1.0", date="5 October 2026",
    status_note="no right of reply needed",
    pdf_title="Carbon neutral, and 1,000 tonnes to avoid. Claim Check 030",
    pdf_subject="Tests Malta International Airport's carbon neutrality and electrification claims",
    story=S))
