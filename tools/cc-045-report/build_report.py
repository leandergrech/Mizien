"""Claim Check 045 report. Run calc.py and figures.py first. Output: out/report.pdf"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import *  # noqa: E402,F401

FIG = HERE / "out"
S = []

# ================================================================== TL;DR
S += [SectionHeading(None, "TL;DR"), Spacer(1, 1 * mm),
      P("On 4 July 2025 Malta’s Public Works Department said its flood-relief canals, tunnels and culverts are being "
        "extended “from 16 km to 20 km”, and its director of the Coastal and Stormwater Unit, Mario Ellul, said these "
        "systems <b>“avoid flooding and damage caused by waters every time it rains.”</b> A newspaper headline "
        "later turned this into “20 kilometres of underground tunnel helped Malta manage its flooding problems”. We "
        "tested the length, the effect and the strength of the wording against official sources and daily "
        "rainfall data.", lead)]
S.append(key_points([
    ("The 20 km is a planned total.",
     "The department describes 16 km as in use and a further 4 km as still to be built [1]. A 2020 news report "
     "also gave about 16 km [4]. The headline figure of 20 km therefore describes what is planned, not what has been "
     "operating (Figure 1)."),
    ("Design capacity is documented; outcomes are not.",
     "The European Commission describes a system that covers 65 km², is designed for a storm with a 5-year return "
     "period and is expected to benefit about 165,000 people [3]. We found no published count of flood incidents, "
     "insurance claims or road closures before and after the works."),
    ("Flooding has continued, and new tunnels are being planned.",
     "A news report of 15 September 2020 describes flooded roads in the project’s own localities [4]. In 2022 the "
     "department planned two more tunnels, at Mosta and Mater Dei, for flooding that persists in those places [2]."),
    ("“Every time it rains” is stronger than the evidence.",
     "A system built for a 5-year storm will be exceeded by larger storms, and no source shows how often it prevents "
     "flooding. Our one rain gauge cannot test this (Figure 2)."),
    ("Verdict: not substantiated (moderate confidence).",
     "The tunnels exist and are designed to reduce flooding, so “helped” is plausible. The 20 km and the strong "
     "form of the wording are not shown."),
]))
S += [Spacer(1, 4 * mm), VerdictMeter(2), Spacer(1, 3 * mm),
      tiles([("16 km", GREY, "in use, according to the Public Works Department (4 Jul 2025)"),
             ("+4 km", ORANGE, "planned, to reach the 20 km total"),
             ("5-year", GREY, "storm the system is designed for (European Commission)"),
             ("0", RED, "published before-and-after flood counts found")]),
      Spacer(1, 4 * mm),
      up_down("A published series of flood incidents (emergency calls, road closures or insurance claims) for the "
              "tunnelled catchments, showing a fall after the works, or a department document confirming that 20 km "
              "are in service. Either would move the verdict to <i>Largely supported</i>.",
              "Evidence that the same localities flooded as often or as badly after the works in storms below the "
              "design level. That would move the verdict to <i>Contradicted</i>.",
              heads=("What would move the verdict up", "What would move it down")),
      Spacer(1, 5 * mm)]
S += toc([("1", "The claim and what we could verify"), ("2", "Method"), ("3", "What the sources say"),
          ("4", "What the data show"), ("5", "Where the evidence points different ways"),
          ("6", "Testing the claim"), ("7", "Verdict and requests for evidence"), ("8", "Limitations")])
S.append(PageBreak())

# ================================================================== 1
S.append(SectionHeading(1, "The claim and what we could verify"))
S.append(P("The check began from a MaltaToday headline, “20 kilometres of underground tunnel helped Malta manage its "
           "flooding problems” [5]. That page, which carries no speaker we could read, is refused to scripts (HTTP 403), "
           "so we saw only its headline and a search summary. We therefore looked for the public statement behind "
           "it. The nearest in date and wording is a press release of the Parliamentary Secretariat for Public Works "
           "of 4 July 2025, reported with direct quotes by the public broadcaster’s news service, TVM News [1]. The "
           "release itself is on gov.mt, which refuses scripts [6]. TVM publishes its English text as a translation "
           "from Maltese, so wording below is TVM’s English rendering."))
S.append(std_table([
    [C("What was said", cellh), C("Form", cellh), C("Our access", cellh)],
    [C("The department “is working to increase from 16 km to 20 km the infrastructure of canals, tunnels and "
       "culverts in use to reduce flooding”"), C("TVM’s summary, no quotation marks [1]"), C("Read in full")],
    [C("“These are very important systems for the country, particularly for the Birkirkara localities, because they "
       "avoid flooding and damage caused by waters every time it rains.”"),
     C("Direct quote, Mario Ellul, Public Works Department [1]"), C("Read in full")],
    [C("“As a department, we are making sure the underground infrastructure, including tunnels and culverts, is "
       "cleaned and maintained regularly”"), C("Direct quote, Parliamentary Secretary Omar Farrugia [1]"),
     C("Read in full")],
    [C("“20 kilometres of underground tunnel helped Malta manage its flooding problems”"),
     C("Headline of a MaltaToday article, undated [5]"), C("Headline and search summary only")],
], [88 * mm, 50 * mm, 32 * mm]))
S += [Spacer(1, 4 * mm),
      callout([P("FAIRNESS NOTE", tag),
               P("The department’s wording is about the network’s purpose and maintenance: it says the systems are meant "
                 "“to reduce flooding” and that maintenance supports them. The stronger forms (“solved”, and 20 km already "
                 "helping) come from headlines and from the shortened version of the statement. We test both and say which "
                 "is which.")],
              bg=AMBER_PALE, bar=AMBER), Spacer(1, 4 * mm)]

# ================================================================== 2
S.append(SectionHeading(2, "Method"))
S.append(P("<b>Question.</b> Are there about 20 km of flood tunnels, and is there evidence that they have helped Malta "
           "manage flooding?"))
S.append(P("<b>Evidence.</b> We read the department’s statement as reported by TVM News [1, 2], the European "
           "Commission’s project page [3] and a 2020 news report [4]. For rainfall we used the daily record of the "
           "Luqa gauge from NOAA’s Global Historical Climatology Network [7], 1990–2025. We computed annual maxima "
           "for years with at least 330 daily readings and an empirical 5-year level (Weibull plotting position), "
           "with a script (<i>tools/cc-045-report/calc.py</i>). We searched Crossref and OpenAlex for a "
           "peer-reviewed evaluation of the Maltese tunnels and found none; OpenAlex was rate-limited on the day."))
S.append(P("<b>Grades.</b> The department statement is grade D (assertion, no data) for effect and C for length. "
           "The Commission page is grade C (official description, design figures). The rainfall record is grade C "
           "(official observations), used as context only."))

# ================================================================== 3
S.append(CondPageBreak(90 * mm))
S.append(SectionHeading(3, "What the sources say"))
S.append(P("<b>Length.</b> The Commission’s page does not give a total length; it names four basins and nine "
           "localities [3]. Lovin Malta, in 2020, wrote of “some 16 kilometres of mostly underground tunnels” and "
           "€54 million [4]. The department in 2025 gives 16 km in use and 20 km as the planned total [1]. The "
           "department’s own count includes canals and culverts, not tunnels only, so “20 km of underground tunnel” "
           "is also a looser description than the department’s."))
S.append(P("<b>Design and expected benefit.</b> The Commission says the infrastructure “covers 65 km² of the Maltese "
           "territory and is capable of handling a storm with a return period of 5 years”, and that “experts predict” "
           "it benefits some 165,000 residents [3]. These are design and forecast figures from 2013, before the "
           "works finished."))
S.append(P("<b>What continued afterwards.</b> On 15 September 2020 Lovin Malta reported flooded roads, power cuts and "
           "overflowing drains and quoted the minister blaming an unusually heavy downpour and unfinished road works "
           "[4]. In 2022 the department said it would dig two further tunnels, one near Mater Dei Hospital and one "
           "under Valletta Road in Mosta, to deal with flooding in those places [2]. Both are consistent with a "
           "network that reduces flooding where it reaches and leaves some places exposed; neither measures how much "
           "it reduced."))

# ================================================================== 4
S.append(CondPageBreak(140 * mm))
S.append(SectionHeading(4, "What the data show"))
S.append(fig(FIG / "fig1_lengths.png"))
S.append(P("Figure 1. Length of the flood-relief network as stated by the department (2025) and in a 2020 news report "
           "[1, 4]. Values in <i>data/cc-045/lengths.csv</i>.", cap))
S.append(fig(FIG / "fig2_luqa_rain.png"))
S.append(P("Figure 2. Largest daily rainfall each year at Luqa, 1990–2025, and the empirical 5-year level (104 mm) [7]. "
           "Hatched years have gaps. All values in <i>data/cc-045/luqa_annual.csv</i> and <i>checks.csv</i>.", cap))
S.append(P("Reading across the data", h2))
for t in ["• <b>The length differs by source.</b> 16 km in use and 20 km planned (department, 2025) [1]; about 16 km "
          "(press, 2020) [4]. The claim’s 20 km matches only the planned total.",
          "• <b>The rainfall record cannot test the effect.</b> The gauge is about 6 km from the Birkirkara tunnel. "
          "Luqa recorded 20.1 mm on 14 September 2020, the day before Lovin Malta’s report of flooding [4], below "
          "the 2-year level of 59 mm: localised downpours are not captured by one gauge.",
          "• <b>The record is incomplete after 2019.</b> 2020–2023 and 2025 have many missing days, so only six years "
          "from 2015 are complete. We therefore make no before-and-after comparison of storms.",
          "• <b>One storm at Luqa since 2014 exceeded the empirical 5-year level:</b> 108.7 mm on 10 February 2018. "
          "We found no sourced account of flooding that day, so we draw no conclusion from it."]:
    S.append(P(t, bul))

# ================================================================== 5
S.append(CondPageBreak(120 * mm))
S.append(SectionHeading(5, "Where the evidence points different ways"))
S.append(contested(
    "Do the tunnels reduce flooding?", "NOT SHOWN", ORANGE,
    "Design: a 5-year storm capacity over 65 km² and an expected 165,000 beneficiaries [3]. The department says the "
    "systems “avoid flooding” and spends a team on maintenance [1]. Reservoirs store rainwater for farmers [1].",
    "Flooded roads in the project’s localities in September 2020 [4]; two further tunnels planned in 2022 for places "
    "that still flood [2]. No before-and-after incident data have been published that we could find.",
    "A system can reduce flooding in many storms and still be overwhelmed by a storm above its design level, or by "
    "water arriving where no culvert reaches. Reports of flooding therefore do not show failure, and the department’s "
    "“every time it rains” cannot be tested without incident data. That is the gap behind the verdict."))
S.append(contested(
    "How long is the network?", "PLANNED TOTAL", ORANGE,
    "20 km: the department’s planned total, in the same release [1]; a MaltaToday headline [5].",
    "16 km in use (department) [1]; about 16 km (Lovin Malta, 2020) [4].",
    "The figures agree once planned and operating lengths are separated. The claim’s 20 km uses the planned figure "
    "for what has helped; the department itself says the extra 4 km is still to come."))

# ================================================================== 6
S.append(CondPageBreak(110 * mm))
S.append(SectionHeading(6, "Testing the claim"))
verd = lambda t, c: chip(t, c, w=29 * mm)
S.append(std_table([
    [C("Sub-claim", cellh), C("What the evidence shows", cellh), C("Rating", cellh)],
    [C("<b>A.</b> Some 20 km of tunnels"),
     C("16 km in use and 4 km planned (department, 4 Jul 2025) [1]; about 16 km in 2020 [4]. 20 km is the planned total."),
     verd("OVERSTATED", ORANGE)],
    [C("<b>B.</b> They are designed to reduce flooding"),
     C("65 km², 5-year storm, 165,000 expected beneficiaries (Commission, 2013) [3]."), verd("SUPPORTED", GREENC)],
    [C("<b>C.</b> They have helped Malta manage flooding"),
     C("Plausible from design; no before-and-after incident data published. Flooding reported in project localities "
       "in 2020 [4] and new tunnels planned in 2022 [2]."), verd("NOT SHOWN", GREY)],
    [C("<b>D.</b> They “avoid flooding … every time it rains”"),
     C("A 5-year design is exceeded by larger storms; no source shows how often flooding is prevented [1, 3, 4]."),
     verd("OVERSTATED", ORANGE)],
], [52 * mm, 88 * mm, 30 * mm], valign="MIDDLE"))

# ================================================================== 7
S += [Spacer(1, 6 * mm), SectionHeading(7, "Verdict and requests for evidence"),
      verdict_box("Not substantiated", "Plausible from design, but the 20 km is a planned total and no outcome data "
                  "show the effect. Confidence: moderate."),
      Spacer(1, 4 * mm)]
S.append(P("<b>Why.</b> (1) The network exists and was built to reduce flooding. (2) The 20 km figure is the planned "
           "total; the department puts 16 km in use. (3) We found no published flood-incident series before and after "
           "the works, so “helped manage” rests on design figures and the department’s statement. (4) The strongest "
           "wording, “every time it rains”, is above the 5-year design level."))
S.append(P("<b>What this verdict does not say.</b> It does not say the tunnels do not work, that flooding is worse, "
           "or that anyone misdescribed the project on purpose. The published record cannot show their effect either way."))
S.append(P("Evidence we are asking for", h2))
S.append(requests_list([
    "Flood incidents (emergency calls, road closures, insurance or compensation claims) for Birkirkara, Msida, Gżira, "
    "Qormi, Marsa, Żabbar and Marsaskala, 2005 to date.",
    "The Storm Water Master Plan and the design-storm basis of each catchment, and the operating length by tunnel.",
    "Hourly rainfall for flood days from the Malta Meteorological Office and the department’s own gauges.",
    "The gov.mt release of 4 July 2025 and the source of the 20 km figure in the MaltaToday article.",
]))
S += [Spacer(1, 4 * mm),
      callout([P("RIGHT OF REPLY", tag),
               P("Before wider circulation this draft should be sent to the Public Works Department with a fixed "
                 "deadline for reply. It is a draft pending right of reply and should not be circulated elsewhere "
                 "until the deadline has passed.")],
              bg=AMBER_PALE, bar=AMBER)]

# ================================================================== 8
S += [Spacer(1, 6 * mm), SectionHeading(8, "Limitations")]
for l in ["We could not read the MaltaToday article or the gov.mt release (HTTP 403); we rely on TVM News’s account "
          "of the release and on the article’s headline and a search summary (◆ second-hand).",
          "TVM’s English text is a translation of a statement in Maltese. The quotation marks are TVM’s.",
          "The rainfall record is one gauge, with gaps after 2019; it gives context, not a test. The 5-year level is "
          "empirical (25 complete years) and is not the project’s design storm.",
          "We did not find peer-reviewed work on the Maltese tunnels. We have no flood-incident data, so the report "
          "cannot say whether flooding fell."]:
    S.append(P("• " + l, bul))

S += [Spacer(1, 6 * mm), SectionHeading(None, "References")]
S += references([
    ("1", "TVM News (4 Jul 2025). 2,400 tonnes of waste removed from 16 km of stormwater tunnels. Reports the "
          "Parliamentary Secretariat for Public Works release; statements of Mario Ellul and Omar Farrugia.",
     "https://tvmnews.mt/en/news/2400-tonnes-of-waste-removed-from-16-km-of-stormwater-tunnels/"),
    ("2", "TVM News (28 Aug 2022). Underground tunnels being excavated to alleviate flooding.",
     "https://tvmnews.mt/en/news/underground-tunnels-being-excavated-to-alleviate-flooding/"),
    ("3", "European Commission, Inforegio (15 Oct 2013). Fighting floods in Malta (National Flood Relief Project).",
     "https://ec.europa.eu/regional_policy/projects/projects-database/fighting-floods-in-malta_en"),
    ("4", "Lovin Malta (15 Sep 2020). An underground tunnel and millions in road investment later, Malta is still "
          "flooding.",
     "https://lovinmalta.com/opinion/analysis/an-underground-tunnel-and-millions-in-road-investment-later-but-malta-is-still-flooding/"),
    ("5", "MaltaToday (undated). 20 kilometres of underground tunnel helped Malta manage its flooding problems. " + DIAM +
          " Headline and search summary only (HTTP 403).",
     "https://www.maltatoday.com.mt/environment/nature/107804/20_kilometres_of_underground_tunnel_helped_malta_manage_its_flooding_problems"),
    ("6", "Government of Malta, Department of Information (4 Jul 2025). Press release by the Parliamentary Secretariat "
          "for Public Works: over 2,400 tonnes of waste collected annually from 16 kilometres of stormwater tunnels. " + DIAM +
          " Not read (HTTP 403); cited through [1].",
     "https://www.gov.mt/en/Government/DOI/Press%20Releases/Pages/2025/07/04/pr251213en.aspx"),
    ("7", "NOAA National Centers for Environmental Information. Global Historical Climatology Network daily, station "
          "MT000016597 (Luqa), precipitation. Retrieved 6 Oct 2026.",
     "https://www.ncei.noaa.gov/access/services/data/v1?dataset=daily-summaries&stations=MT000016597&dataTypes=PRCP&format=csv"),
])

S.append(PageBreak())
S += appendix_a("A experiment · B observational study with a control or gradient · C review, guidance or "
                "official statistics · D assertion or anecdote. ◆ marks a source known only second-hand.")
S += [Spacer(1, 5 * mm)]
S += revision_log([("1.0", "6 Oct 2026", "First issue. Draft pending right of reply from the Public Works Department.")])

build_report(Report(
    number="045", out=str(FIG / "report.pdf"), kicker="Flood tunnels",
    title_lines=["Do 20 km of", "tunnels manage", "flooding?"],
    subtitle_lines=["Testing a public claim about Malta’s flood-relief network", "against official sources and rainfall data"],
    quote_lines=["“…they avoid flooding and damage caused", "by waters every time it rains.”"], quote_size=16,
    attribution="Mario Ellul, Public Works Department, as reported by TVM News, 4 July 2025.",
    context="Reported alongside a plan to extend the network from 16 km to 20 km.",
    verdict="Not substantiated", verdict_note="Plausible by design; 20 km is the planned total",
    footer_lines=["Version 1.0  ·  6 October 2026", "Status: draft for right of reply (Public Works Department)",
                  "Prepared from public sources and open data.", "Repository: github.com/leandergrech/Mizien"],
    running_head="Flood tunnels – Malta", version="1.0", date="6 October 2026",
    pdf_title="Do 20 km of tunnels manage flooding? Claim Check 045",
    pdf_subject="Tests the claim that 20 km of underground tunnels have helped Malta manage flooding",
    story=S))
