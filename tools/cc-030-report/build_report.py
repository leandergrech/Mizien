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
        "1,000 tonnes of carbon dioxide annually”</b> [1]. Elsewhere it says it has reached Level 3+ (“neutrality”) "
        "of Airport Carbon Accreditation (ACA) [2, 4]. We tested both against its own figures, ACA’s records, the "
        "credit registries and the EU’s list of funded projects.", lead)]
S.append(key_points([
    ("Carbon neutrality, as ACA defines it, is confirmed independently.",
     "ACA lists MIA at Level 3+ [8, 9], and registries show 3,780 of its 5,450 t of credits retired for the airport "
     "[10, 11]. A third block (1,670 t) was not found."),
    ("“Neutral” covers about 0.7% of the reported footprint.",
     "It covers Scope 1, Scope 2 and business travel. Scope 3, mostly aircraft, is 99.3% of the 738,308 t reported "
     "for 2025 [2]."),
    ("The €12.5 million programme is real.",
     "The EU’s project list confirms a €5,391,500 grant for power at all 35 stands and charging for battery ground "
     "power units, 15 electric airside buses and other equipment [12]."),
    ("The 1,000 t a year has no published method.",
     "On the one sourced rate for a diesel ground power unit, about 25 kg CO₂ an hour [13], 1,000 t needs 74 minutes "
     "of diesel power replaced at every turnaround; 22.5 minutes gives about 300 t. The rest would need "
     "auxiliary-power or vehicle savings MIA has not shown."),
    ("Verdict: not substantiated (moderate confidence).",
     "Neutrality and the programme hold; the headline number has not been shown. This is missing evidence, not "
     "evidence against. Pending right of reply."),
]))
S += [Spacer(1, 4 * mm), VerdictMeter(2), Spacer(1, 3 * mm),
      tiles([("Level 3+", GREEN, "ACA lists the airport as carbon neutral; 3,780 of 5,450 t of credits found retired"),
             ("0.7%", ORANGE, "of the reported 2025 footprint lies inside the carbon-neutral boundary"),
             ("≈300 t", ORANGE, "a year from diesel ground power at every turnaround for 22.5 min (gross, indicative)"),
             ("1,000 t", RED, "a year claimed; no method, baseline or grid treatment published")]),
      Spacer(1, 4 * mm),
      up_down("A published calculation from MIA (equipment replaced, hours, auxiliary power saved, grid electricity) "
              "that reaches about 1,000 t a year, or measured savings once stands operate: <i>Largely supported</i>.",
              "MIA’s own ground-power and auxiliary-power data showing the saving will be far below 1,000 t, or that "
              "it counts savings outside the programme."),
      Spacer(1, 5 * mm)]
S += toc([("1", "The claim and what we could verify"), ("2", "Method"), ("3", "What carbon neutrality means here"),
          ("4", "What the data show"), ("5", "Where the evidence points different ways"),
          ("6", "Testing the claim"), ("7", "Verdict and requests for evidence"), ("8", "Limitations")])
S.append(PageBreak())

# ================================================================== 1
S.append(SectionHeading(1, "The claim and what we could verify"))
S.append(P("The 25 May release [1] is about the programme and the 1,000 t; it does not mention carbon neutrality or "
           "ACA. The claim tested here is therefore assembled from several MIA documents, each quoted below with its "
           "own date: the release for the programme, and the company’s web pages and sustainability report for "
           "neutrality. The Malta Independent carried the release on 25 May 2026 under the headline “Airfield "
           "electrification at MIA set to avoid 1,000 tonnes of carbon dioxide emissions every year”; we could not "
           "read that article from our network and did not rely on it."))
S.append(std_table([
    [C("What was said", cellh), C("Where", cellh), C("Our access", cellh)],
    [C("“…implementing a €12.5 million Airfield Electrification Programme, which is set to avoid the emission of an "
       "average of 1,000 tonnes of carbon dioxide annually.” Completion expected by 2028."),
     C("Press release, 25 May 2026 [1]"), C("Read in full")],
    [C("35 hatch-pit systems; battery ground power units with 20 charging points; 15 electric bus charging points; "
       "five medium-voltage substations, two generators, 7.5 MVA; an EU grant of €5.4 million."),
     C("Press release [1]; EU project list [12]"), C("Read in full")],
    [C("“Reaching carbon neutral status in 2025”, one of two interim targets of the Net Zero Carbon Plan, the other "
       "being a 65% cut in emissions by 2030 against 2015."),
     C("Facts and Figures page, updated 18 Aug 2025 [3]; plan [6]"), C("Read in full")],
    [C("Cuts in direct emissions and offsets “allowed Malta International Airport to move up … to Level 3+ "
       "(neutrality)”."),
     C("At a Glance page, updated 2 Sep 2026 [4]; company announcements, e.g. 24 Aug 2026 [5]"), C("Read in full")],
    [C("Level 3+ reached in 2025, “having satisfied criteria related to the reduction of direct emissions and the "
       "offsetting of residual emissions, namely 5,450 tonnes of carbon dioxide”."),
     C("Sustainability Report 2025, p. 31 [2]"), C("Read in full")],
], [96 * mm, 46 * mm, 28 * mm]))
S += [Spacer(1, 4 * mm),
      callout([P("FAIRNESS NOTE", tag),
               P("MIA does not claim that the whole airport, or flights, are carbon neutral. Its head of "
                 "sustainability says the programme is about “Scope 3 emissions” [1], the company reports its Scope 3 "
                 "openly, including flight emissions it does not control, and ACA’s notice limits the neutrality to "
                 "“emissions under its direct control” [9]. The questions here are whether the 1,000 t has been shown "
                 "and what “neutral” covers.", small)],
              bg=AMBER_PALE, bar=AMBER), Spacer(1, 4 * mm)]

# ================================================================== 2
S.append(SectionHeading(2, "Method"))
S.append(P("<b>Questions.</b> (A) Did MIA reach carbon neutrality as ACA defines it, and do independent records "
           "confirm it? (B) Is the programme as described? (C) Can the 1,000 t a year be reproduced from published "
           "sources? (D) How much of the airport’s footprint does “neutral” cover?"))
S.append(P("<b>Evidence.</b> MIA’s Sustainability Report 2025 [2]: Scope 1 and 2 and offsetting (pp. 26–31), the "
           "reporting criteria for Scope 1 and Scope 3 (pp. 90–91, 96–97), the assurance report (pp. 112–113), the "
           "GRI 102 and 103 tables (pp. 124–127) and the offset certificate (pp. 140–141). ACA’s rules for Level 3+ "
           "[7], its directory entry for MIA, read through the website’s public interface [8], and its notice of "
           "the upgrade [9]. The Gold Standard and Rainbow registries [10, 11]. The EU’s list of projects funded under "
           "the Alternative Fuels Infrastructure Facility (AFIF) [12]. One peer-reviewed study of aircraft ground "
           "power, read in full as the author’s accepted manuscript [13], and IPCC default fuel factors [14]. "
           "Values were transcribed to <i>data/cc-030/</i> and every ratio recomputed with "
           "<i>tools/cc-030-report/calc.py</i> (<i>data/cc-030/checks.csv</i>)."))
S.append(P("<b>Grades.</b> The company’s report is grade D by itself (self-reported), but its Scope 1 and 2 figures "
           "carry limited assurance from PwC Malta, which we treat as grade C, as we do ACA’s records, the registries "
           "and the EU list. The peer-reviewed study is grade B; the diesel-unit fuel rate it cites from a 2004 Zurich "
           "Airport report is second-hand ◆. <b>Verdicts</b> follow the five-point scale in Appendix A."))

# ================================================================== 3
S.append(CondPageBreak(90 * mm))
S.append(SectionHeading(3, "What carbon neutrality means here"))
S.append(P("Airport Carbon Accreditation is run by Airports Council International. At Level 3+ an airport must meet "
           "the lower levels, then “offset its remaining Scope 1 and 2 carbon emissions as well as emissions from "
           "staff business travel” with recognised offsets, having first reduced its emissions as far as it can [7]. "
           "Scope 1 is fuel and other direct emissions of the operator; Scope 2 is purchased electricity; Scope 3 "
           "covers everything else, including the aircraft that use the airport. So “carbon neutral” at Level 3+ is "
           "a statement about the operator’s own activity."))
S.append(P("<b>Independent confirmation.</b> ACA’s directory lists MIA at Level 3+, an entry last updated on "
           "20 November 2025 [8], and an ACA notice of 18 December 2025 says the airport “has upgraded to Level 3+ … "
           "achieving carbon neutrality for emissions under its direct control” [9]. The notice says the residual "
           "emissions offset were those of 2024, so the accreditation rests on the 2024 footprint. Two of the three "
           "credit blocks on MIA’s certificate [2] are recorded as retired for the airport on 4 June 2026: 1,620 t "
           "from a safe-water and cookstove programme in Uganda (Gold Standard, vintage 2024) [10] and 2,160 t from a "
           "biogas unit in Oise, France (Rainbow registry, vintage 2022) [11]. We did not find the third (1,670 t, "
           "Igloo Cellulose, Canada): the report prints the same Gold Standard link twice. So 3,780 of the 5,450 t "
           "(69%) are confirmed as retired. We did not assess the quality of the credits."))
S.append(P("<b>The boundary arithmetic.</b> For 2024, the year ACA names, Scope 1, location-based Scope 2 and "
           "business travel came to 5,025 t (5,136 t with market-based Scope 2) [2], less than the 5,450 t of "
           "credits. For 2025 the same items total 5,444 t on a location basis, matched by the credits, but 5,555 t "
           "with market-based Scope 2, 105 t more than the credits. “Fully matched” holds only on the location "
           "basis."))
S.append(P("<b>What sits outside.</b> Diesel ground power units belong to ground handlers, so their fuel is reported "
           "in Scope 3, under “use of sold products”, alongside full-flight aircraft emissions, auxiliary power units "
           "(APUs), engine tests, tenants’ own fuel and passengers’ road trips to the airport [2, pp. 96–97]. The "
           "programme therefore reduces a part of Scope 3 outside the neutral boundary, while the grid electricity "
           "supplied instead carries 0.389 kg CO₂ per kWh on MIA’s own factor [2]. A peer-reviewed analysis of 25,195 turnarounds at "
           "125 European airports found that fixed ground power, by letting the APU stay off for an average of "
           "22 min 28 s, cut the APU’s emissions of carbon monoxide, nitrogen oxides and hydrocarbons by an average "
           "of 47.6%; with a diesel unit instead, net hydrocarbons about doubled [13]. That study measures these "
           "pollutants, not CO₂, but it shows the saving depends on what is replaced."))

# ================================================================== 4
S.append(KeepTogether([
    SectionHeading(4, "What the data show"), fig(FIG / "fig1_scopes.png"),
    P("Figure 1. Panel A: the emissions inside the carbon-neutral boundary in 2025, against the credits on MIA’s "
      "certificate, the credits found retired in public registries and the programme’s projected saving. Panel B: "
      "the whole reported footprint, on a scale 1,000 times larger. Both axes are linear [2, 10, 11].", cap)]))
S.append(KeepTogether([std_table([
    [C("Indicator", cellh), C("Value", cellh), C("Source", cellh)],
    [C("Neutral boundary 2025: Scope 1 + Scope 2 (location) + business travel"),
     C("813 + 4,582 + 49 = <b>5,444 t</b>; 5,555 t with market-based Scope 2"), C("[2], calculated")],
    [C("Neutral boundary 2024 (the year ACA names)"), C("5,025 t; 5,136 t with market-based Scope 2"),
     C("[2, 9], calculated")],
    [C("Credits on MIA’s certificate"), C("<b>5,450 t</b> (Canada 1,670; France 2,160; Uganda 1,620)"), C("[2]")],
    [C("Credits found retired for MIA in public registries"), C("<b>3,780 t</b> (69%); Canada block not found"),
     C("[10, 11]")],
    [C("Reported footprint 2025, Scope 1 + 2 + 3"), C("738,308 t; Scope 3 = 99.3% (95.3% in 2024, older basis)"),
     C("[2], calculated")],
    [C("Use of sold products (mostly aircraft), share of Scope 3"), C("673,004 t, 91.8%"), C("[2]")],
    [C("Scope 1 + 2, change from 2015"), C("6,949 t to 5,395 t, <b>−22%</b> by 2025 (−28% by 2024)"), C("[2]")],
    [C("Scope 1 + 2, change 2024 to 2025"), C("+8.4% (passengers +12%)"), C("[2]")],
    [C("Scope 1, change 2024 to 2025"), C("+94% (418 t to 813 t); fuel use +30%"), C("[2]")],
    [C("Company target: −65% by 2030 against 2015"), C("2,432 t, so a further cut of 2,963 t (55%) from 2025"),
     C("[3, 6], calculated")],
    [C("Programme: 1,000 t a year against Scope 1 + 2 / Scope 3"), C("18.5% / 0.14%"), C("[1, 2], calculated")],
    [C("EU grant"), C("€5,391,500: 50% of €10.78 million eligible costs, 43% of €12.5 million"), C("[1, 12]")],
], [74 * mm, 70 * mm, 26 * mm]),
    P("All values and inputs in <i>data/cc-030/</i>; ratios in <i>checks.csv</i>. Page numbers are the report’s "
      "printed pages.", cap)]))
S.append(P("Reading across the data", h2))
for t in ["• <b>The accounting reconciles, on one basis.</b> The credits cover the 2024 boundary on either Scope 2 "
          "basis and the 2025 boundary on the location basis, but fall 105 t short of 2025 on the market basis.",
          "• <b>The boundary is narrow by design.</b> 99.3% of the reported 2025 footprint is Scope 3, which Level 3+ "
          "does not ask the airport to offset [7]. That share rests on the 2025 switch to counting full flights; on "
          "2024’s landing-and-take-off basis it was 95.3%. The point stands either way.",
          "• <b>Direct emissions are not yet falling fast.</b> Scope 1 + 2 is 22% below 2015 and rose 8% in 2025. "
          "The −65% target for 2030 [6] means reaching 2,432 t, a further cut of about 2,960 t. MIA’s own figures for "
          "the cut so far differ by document: −31% for 2023 in the Net Zero Carbon Plan [6], −32% in ACA’s notice [9], "
          "and −28% (2024) and −22% (2025) in the report’s table [2].",
          "• <b>Scope 1 nearly doubled, and fuel does not explain it.</b> Scope 1 rose 94% while fuel use rose 30% "
          "[2, pp. 126–127]. The report’s own litres and factors give about 408 t of CO₂ from fuel in 2025, half of the "
          "813 t reported; Scope 1 also counts refrigerant top-ups and extinguisher refills [2, pp. 90–91], but the "
          "report does not break it down.",
          "• <b>The 1,000 t has no published basis.</b> The release gives no baseline, hours or treatment of grid "
          "electricity, so we asked what the figure would require (Figure 2)."]:
    S.append(P(t, bul))
S.append(P("The one sourced rate for a diesel ground power unit is 7.74 kg of fuel an hour, about 25 kg CO₂, a 2004 "
           "Zurich average cited by Padhra [13] ◆. On that rate, 1,000 t means replacing about 40,500 hours of diesel "
           "ground power a year: 74 minutes at every one of about 32,700 turnarounds [15]. A diesel unit at every turnaround for 22.5 minutes, the average "
           "time the APU stayed off on external power in the peer-reviewed sample [13], emits about 300 t a year, "
           "less once the grid electricity replacing it is counted. An APU burns about 325 kg CO₂ an hour [2, 13], so "
           "1,000 t comes within reach only if the programme also cuts APU running, by about 5.6 minutes per "
           "turnaround on its own or 3.9 minutes on top of the diesel case, or saves fuel through electric buses and "
           "other equipment. MIA has shown none of these. The 25 kg rate comes from one airport in 2004 and larger "
           "units may burn more, so this is indicative; but it is the only sourced figure we found, and version 1.0 "
           "relied instead on unsourced rates 1.6 to 3.6 times higher."))
S.append(KeepTogether([fig(FIG / "fig2_gpu.png"), P("Figure 2. What 1,000 t a year would require, anchored on the one sourced rate for a diesel ground power "
           "unit (about 25 kg CO₂ an hour, a 2004 Zurich average known only through [13] ◆) and on measured APU fuel "
           "burn [13]. Turnarounds are half of the 65,470 aircraft movements of 2025 [15]. Gross figures, before the "
           "grid electricity that replaces the diesel. An illustration of what the claim needs, not an estimate of "
           "the programme’s effect.", cap)]))

# ================================================================== 5
S.append(CondPageBreak(85 * mm))
S.append(SectionHeading(5, "Where the evidence points different ways"))
S.append(contested(
    "Q1  Is the airport carbon neutral?", "YES, AS ACA DEFINES IT", GREEN,
    "ACA lists MIA at Level 3+ and says so in a notice [8, 9]. Two of three credit blocks are retired for MIA in "
    "public registries [10, 11], and the credits match the boundary emissions, with limited assurance on Scope 1 "
    "and 2 [2]. MIA reports its much larger Scope 3 openly.",
    "A reader hearing “carbon neutral” may think of the airport’s whole footprint, including flights. By the "
    "company’s own tables 99.3% of the reported footprint is outside the neutral boundary, and one credit block "
    "(1,670 t) could not be traced.",
    "<b>For this claim:</b> true as defined, now independently confirmed; the statement should name its scope."))
S.append(contested(
    "Q2  Will the programme avoid 1,000 t a year?", "NOT SHOWN", ORANGE,
    "The programme replaces diesel ground power at 35 stands and adds charging for electric buses and other "
    "equipment [1, 12]. If it also shortens APU running (about 325 kg CO₂ an hour), 5.6 fewer APU minutes per turnaround would avoid 1,000 t "
    "on their own. MIA already collects ground-power fuel and APU times from ground handlers [2, pp. 96–97].",
    "No method, baseline or grid treatment is published. On the one sourced diesel-unit rate [13] ◆, 1,000 t needs "
    "74 minutes of diesel power replaced at every turnaround; 22.5 minutes gives about 300 t, before grid "
    "electricity. Nothing can be measured before completion in 2028.",
    "<b>For this claim:</b> 1,000 t is possible only with savings MIA has not shown; until it publishes the "
    "calculation the figure is not substantiated."))
S.append(contested(
    "Q3  Does ‘avoid’ mean the airport’s emissions fall?", "NOT NECESSARILY", AMBER,
    "Fewer diesel units means less fuel burnt on the apron, which lowers Scope 3 and local pollution.",
    "The avoided tonnes sit in Scope 3, outside the neutral boundary, while the added electricity sits in Scope 2, "
    "which the airport offsets.",
    "<b>For this claim:</b> the release is consistent with this, naming “Scope 3 emissions”."))

# ================================================================== 6
S.append(CondPageBreak(110 * mm))
S.append(SectionHeading(6, "Testing the claim"))
verd = lambda t, c: chip(t, c, w=29 * mm)
S.append(std_table([
    [C("Sub-claim", cellh), C("What the evidence shows", cellh), C("Rating", cellh)],
    [C("<b>A.</b> MIA reached carbon neutrality (ACA Level 3+) in 2025"),
     C("ACA lists MIA at Level 3+ (updated 20 Nov 2025; notice 18 Dec 2025); 3,780 of 5,450 t of credits found "
       "retired; credits match the boundary emissions on the location basis [2, 8–11]."), verd("SUPPORTED", GREENC)],
    [C("<b>B.</b> A €12.5 million airfield electrification programme"),
     C("EU list confirms project 24-MT-TC-AE-MIA: €10.78m eligible costs, €5,391,500 grant; power at 35 stands, "
       "charging for 20 battery units, 15 e-buses and other equipment [1, 12]."), verd("ACCURATE", GREENC)],
    [C("<b>C.</b> It will avoid an average of 1,000 t CO₂ a year"),
     C("No method, baseline or grid treatment published. Diesel ground power at every turnaround gives about 300 t "
       "gross; 1,000 t needs APU or vehicle savings not shown [1, 13]."), verd("NOT SUBSTANTIATED", ORANGE)],
    [C("<b>D.</b> Scope of ‘neutral’"),
     C("Covers Scope 1, 2 and business travel, 0.7% of the reported 2025 footprint; MIA’s documents and ACA tie it "
       "to emissions under the company’s control [2, 4, 7, 9]."), verd("NEEDS CONTEXT", AMBER)],
], [52 * mm, 88 * mm, 30 * mm], valign="MIDDLE"))

# ================================================================== 7
S += [Spacer(1, 6 * mm), SectionHeading(7, "Verdict and requests for evidence"),
      verdict_box("Not substantiated", "Neutral within its ACA scope, and the programme is real; the 1,000 t a year "
                  "has not been shown. Confidence: moderate. Missing evidence, not evidence against."),
      Spacer(1, 4 * mm)]
S.append(P("<b>Why.</b> (1) Neutrality as ACA defines it is now confirmed by ACA’s own records and, for 69% of the "
           "credits, by the registries. (2) The programme and its funding are confirmed by the EU’s list. (3) The "
           "central number of the 25 May statement, 1,000 t a year, comes with no method, baseline or treatment of "
           "grid electricity. The one sourced rate we found puts diesel ground power, the saving the release "
           "describes, at about 300 t a year gross; 1,000 t is reachable only if it includes savings from aircraft "
           "auxiliary power or electric vehicles that MIA has not shown. The figure is stated more strongly than the "
           "evidence offered allows, so the verdict is <i>Not substantiated</i>."))
S.append(P("<b>Why not Misleading.</b> MIA hides nothing material: the release itself stresses Scope 3, and the "
           "company reports Scope 3 openly. <b>Why moderate confidence.</b> The gap is missing evidence, not "
           "evidence against, and the diesel-unit rate is second-hand and from one airport. A published calculation "
           "from MIA could move the verdict to <i>Largely supported</i>."))
S.append(P("<b>Change from version 1.0.</b> Version 1.0 rated the claim <i>Largely supported</i>, calling the "
           "1,000 t plausible on emission rates of 40–90 kg CO₂ an hour that had no source. The only sourced rate is "
           "about 25 kg, so that test did not hold; the maintainer changed the verdict on 5 October 2026."))
S.append(P("<b>What this verdict does not say.</b> It does not say the 1,000 t is wrong, that the credits are of high "
           "or low quality (we did not assess them), that offsetting is an adequate climate strategy, or that anyone "
           "acted in bad faith. A clearer statement would read: <i>“Our own operations are carbon neutral under ACA "
           "Level 3+; the programme is expected to cut about 1,000 t a year of mainly Scope 3 emissions, calculated "
           "as follows.”</i>"))
S.append(KeepTogether([P("Evidence we are asking for", h2), requests_list([
    "The calculation behind 1,000 t: equipment replaced (diesel units, APU running, buses, other equipment), hours "
    "and fuel, electricity added and its emission factor; gross or net.",
    "The ground-power diesel and APU parts of Scope 3 “use of sold products”, which MIA collects from ground "
    "handlers, and any CO₂ estimate in the AFIF application.",
    "The registry record of the third credit block (Igloo Cellulose, Canada, 1,670 t), and the footprint year the "
    "5,450 t were retired against.",
    "A breakdown of Scope 1 for 2024 and 2025 (fuel, refrigerants, extinguishers) explaining the 94% rise.",
])]))
S += [Spacer(1, 4 * mm),
      callout([P("RIGHT OF REPLY", tag),
               P("A right of reply will be sought from Malta International Airport before this check is circulated "
                 "beyond Miżien’s site, with a fixed deadline (suggested 14 days). Its response will be appended and "
                 "the verdict revisited.", small)],
              bg=AMBER_PALE, bar=AMBER)]

# ================================================================== 8
S += [Spacer(1, 6 * mm), CondPageBreak(75 * mm), SectionHeading(8, "Limitations")]
for l in ["Most numbers come from the company’s own report. Only Scope 1 and 2 (and energy) were assured; Scope 3 and "
          "the credits were not part of the assurance scope.",
          "ACA’s directory and notice were read through the website’s public interface on 5 October 2026; we did not "
          "see the accreditation certificate. We did not assess the quality of the credits, and one of the three "
          "blocks could not be traced.",
          "The only sourced diesel-unit rate (7.74 kg of fuel an hour) is a 2004 Zurich average known second-hand "
          "through Padhra (2018); the APU rates are for short-haul narrow-body jets in 2015. Figure 2 is indicative, "
          "and treats every movement pair as a turnaround at a served stand.",
          "The Malta Independent article that carried the release was not readable from our network; we used the "
          "company’s original.",
          "No study of Maltese airport ground power was found."]:
    S.append(P("• " + l, bul))

S += [Spacer(1, 6 * mm), SectionHeading(None, "References")]
S += references([
    ("1", "Malta International Airport (25 May 2026). Airfield electrification at MIA set to avoid 1,000 tonnes of CO₂ "
          "emissions annually. Press release.",
     "https://maltairport.com/corporate-news/airfield-electrification-at-mia-set-to-avoid-1000-tonnes-of-co2-emissions-annually/"),
    ("2", "Malta International Airport plc (2026). Sustainability Report 2025: Scope 1–3 and offsetting (pp. 26–31), "
          "reporting criteria (pp. 90–91, 96–97), Independent Assurance Report, PwC Malta (pp. 112–113), GRI 102 and "
          "103 tables (pp. 124–127), carbon offset certificate (pp. 140–141).",
     "https://maltairport.com/app/uploads/2026/10/Final_MIA26-Sustaibability.pdf"),
    ("3", "Malta International Airport. Facts and Figures (webpage, updated 18 August 2025; read 5 October 2026).",
     "https://maltairport.com/corporate/our-airport/facts-and-figures/"),
    ("4", "Malta International Airport. At a Glance (webpage, updated 2 September 2026; read 5 October 2026).",
     "https://maltairport.com/corporate/our-airport/at-a-glance/"),
    ("5", "Malta International Airport plc (24 August 2026). Company announcement 495/2026, share buyback programme "
          "(company description).",
     "https://maltairport.com/app/uploads/2026/08/MIA-CoAnn-495-2026-Buyback-Week-Ended-21-August.pdf"),
    ("6", "Malta International Airport (2024). Our Journey to Net Zero Carbon (Net Zero Carbon Plan).",
     "https://maltairport.com/app/uploads/2026/01/Net-Zero-Carbon-Plan.pdf"),
    ("7", "Airport Carbon Accreditation. Level 3+ (Neutrality). Airports Council International.",
     "https://www.airportcarbonaccreditation.org/about/7-levels-of-accreditation/neutrality/"),
    ("8", "Airport Carbon Accreditation. Directory entry, Malta International Airport (level: Level 3+; updated "
          "20 November 2025), public interface, retrieved 5 October 2026.",
     "https://www.airportcarbonaccreditation.org/wp-json/wp/v2/accredited-airport?slug=malta"),
    ("9", "Airport Carbon Accreditation (18 December 2025). Malta International Airport reaches Level 3+.",
     "https://www.airportcarbonaccreditation.org/malta-international-airport-reaches-level-3/"),
    ("10", "Gold Standard registry. Credit block 585497: 1,620 credits, Uganda safe water and cookstoves (GS2296), "
           "vintage 2024, retired for Malta International Airport, 4 June 2026.",
     "https://public-api.goldstandard.org/credits/585497"),
    ("11", "Rainbow registry. Transaction 9e16ced5-8874-4ea6-8e0d-3f0344b137e8: 2,160 credits, Chemin du Roi biogas, "
           "France, vintage 2022, retired on behalf of Malta International Airport, 4 June 2026.",
     "https://registry.rainbowstandard.io/ledger/transactions/9e16ced5-8874-4ea6-8e0d-3f0344b137e8"),
    ("12", "European Climate, Infrastructure and Environment Executive Agency (CINEA) (November 2025). CEF Transport "
           "AFIF, second cut-off: list of selected projects (24-MT-TC-AE-MIA).",
     "https://cinea.ec.europa.eu/document/download/c152fb88-a997-432a-b28c-5b33a1995abf_en?filename=CEF-T-2024-AFIF_Cut-off+2_Evaluation+outcome_Communication+item_list+of+projects.pdf"),
    ("13", "Padhra A. (2018). Emissions from auxiliary power units and ground power units during intraday aircraft "
           "turnarounds at European airports. <i>Transportation Research Part D</i> 63:433–444. "
           "doi:10.1016/j.trd.2018.06.015. Full text read as the accepted manuscript (University of West London "
           "repository, CC BY-NC-ND); it cites Fleuti (2006) for the diesel-unit fuel rate ◆.",
     "https://repository.uwl.ac.uk/id/eprint/5214/"),
    ("14", "IPCC (2006). 2006 IPCC Guidelines for National Greenhouse Gas Inventories, Vol. 2, Ch. 1, Tables 1.2 and "
           "1.4 (default net calorific value and CO₂ factor for diesel).",
     "https://www.ipcc-nggip.iges.or.jp/public/2006gl/pdf/2_Volume2/V2_1_Ch1_Introduction.pdf"),
    ("15", "Malta International Airport plc (14 January 2026). Company announcement 461/2026, Full-Year Traffic "
           "Update (65,470 aircraft movements in 2025).",
     "https://maltairport.com/app/uploads/2026/01/Full-Year-Traffic-Update.pdf"),
    ("16", "Miżien. Data and calculations: data/cc-030/; tools/cc-030-report/calc.py.", ""),
])

S.append(PageBreak())
S += appendix_a("A experiment · B observational study with a control or gradient · C review, guidance or "
                "official statistics · D assertion or anecdote. ◆ marks a source known only second-hand.")
S += [Spacer(1, 2 * mm)]
S += revision_log([
    ("1.0", "5 Oct 2026", "First issue. No right of reply needed (Largely supported)."),
    ("1.1", "5 Oct 2026",
     "Corrections and maintainer decision: verdict changed from Largely supported to Not substantiated (moderate): "
     "the 1,000 t has no published method, and v1.0 tested it with unsourced emission rates. Figure 2 redone on a "
     "sourced rate; neutrality and the programme confirmed in independent records; claim restated from MIA’s own "
     "documents; citations, page references and context corrected; Figure 1 on linear axes."),
])

build_report(Report(
    number="030", out=str(FIG / "report.pdf"), kicker="Airport emissions",
    title_lines=["Carbon neutral,", "and what", "else?"],
    subtitle_lines=["Testing Malta International Airport’s carbon claims", "against its figures and public registries"],
    quote_lines=["“…set to avoid the emission of an average of", "1,000 tonnes of carbon dioxide annually.”"], quote_size=16,
    attribution="Malta International Airport plc, press release, 25 May 2026.",
    context="A €12.5 million airfield electrification programme; the airport holds ACA Level 3+ (carbon neutral).",
    verdict="Not substantiated", verdict_note="Neutral within its ACA scope; the 1,000 t has not been shown",
    footer_lines=["Version 1.1  ·  5 October 2026", "Status: draft, pending right of reply (Malta International Airport)",
                  "Prepared from public sources, company reports and registries.",
                  "Repository: github.com/leandergrech/Mizien"],
    running_head="Airport carbon claims – Malta", version="1.1", date="5 October 2026",
    pdf_title="Carbon neutral, and 1,000 tonnes to avoid. Claim Check 030",
    pdf_subject="Tests Malta International Airport's carbon neutrality and electrification claims",
    story=S))
