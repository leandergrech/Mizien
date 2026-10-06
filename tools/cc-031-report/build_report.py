"""Claim Check 031 report. Run fetch.py, calc.py and figures.py first. Output: out/report.pdf"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import *  # noqa: E402,F401

FIG = HERE / "out"
S = []

# ================================================================== TL;DR
S += [SectionHeading(None, "TL;DR"), Spacer(1, 1 * mm),
      P("Presenting the Gozo climate neutrality plan on 25 September 2026, the Minister for Gozo said: <b>“The plan "
        "published today is an important step to continue to realise our vision of Gozo becoming the first "
        "climate-neutral region in Malta.”</b> Gozo Today adds, in its own words, that he said Gozo had already begun its "
        "transition, including a fully electric public transport fleet. We checked the fleet against public reports and "
        "Eurostat data, and asked whether the “vision” can be measured.", lead)]
S.append(key_points([
    ("The fleet statement holds.",
     "TVM News reported on 28 May 2026 that public transport in Gozo is now run entirely with electric buses (22 new "
     "buses, EUR 11 million, a new charging depot at Ta’ Xħajma) and on 4 July 2026 that this “marked the end of "
     "diesel-powered buses in Gozo”. The sources are the operator and the government; we did not find independent "
     "fleet records."),
    ("It is a small part of the job.",
     "Malta Public Transport estimates the electric fleet saves about 1,300 tonnes of CO2 a year. Against a rough, "
     "population-proportional estimate of Gozo’s road-transport emissions (about 50 kt CO2e) that is about 2.6%. "
     "This is an order of magnitude, not a Gozo measurement: Eurostat has no regional inventory."),
    ("The “vision” has no date or measure in the words quoted.",
     "No target year, baseline or boundary is named, so it is rated a pledge: <i>Not measurable</i> as of 6 October 2026. "
     "We could not obtain the published plan, which may set a date."),
    ("Verdict on the factual part: largely supported (moderate confidence).",
     "The buses are electric. The caveat is that this is one early measure, from operator-side sources, and the "
     "statement does not claim more."),
]))
S += [Spacer(1, 2.5 * mm), VerdictMeter(1), Spacer(1, 3 * mm),
      tiles([("100%", GREEN, "Gozo’s buses electric since late May 2026 (TVM News)"),
             ("1,300 t", GREEN, "CO2 a year saved, Malta Public Transport’s estimate"),
             ("≈2.6%", ORANGE, "Of an approximate Gozo road-transport total (our scale check)"),
             ("Not measurable", GREY, "Pledge label for the “vision”, as of 6 Oct 2026")]),
      Spacer(1, 4 * mm),
      up_down("None: this is not the top of the scale only because the fleet evidence comes from the operator and the "
              "government, and the transport regulator’s fleet page could not be read. Supported would need an independent "
              "fleet record (Transport Malta licensing or fleet data).",
              "A fleet record showing diesel buses still in scheduled Gozo service; or the plan or the minister claiming "
              "more for the fleet than the evidence allows. For the pledge label: the published plan setting a "
              "target year and boundary would move it to Not yet due, On track or Off track."),
      Spacer(1, 3 * mm)]
S.append(PageBreak())

# ================================================================== 1
S.append(SectionHeading(1, "The claim and what we could verify"))
S.append(P("Gozo Today reported the event on 25 September 2026 [1]: a memorandum of understanding between the Gozo "
           "Regional Development Authority (GRDA) and the Climate Action Authority was signed at the “Gozo Towards "
           "Climate Neutrality” conference, where a plan was presented. The GRDA’s own notice says the plan was "
           "presented by KPMG as a “strategic reference framework” [2]. The report was read in full by the maintainer and by us; "
           "the wording is recorded in <i>literature/CC-031/primary-source.md</i>. Only one sentence is in quotation "
           "marks; the rest is the outlet’s paraphrase, and we label it so."))
S.append(std_table([
    [C("Source", cellh), C("What it says", cellh), C("Our access", cellh), C("Status", cellh)],
    [C("<b>Clint Camilleri</b>, Minister for Gozo, as quoted by Gozo Today, 25 Sep 2026 [1]"),
     C("“The plan published today is an important step to continue to realise our vision of Gozo becoming the first "
       "climate-neutral region in Malta.”"),
     C("Read in full, 5 Oct 2026."), C("<b>The claim (quoted)</b>")],
    [C("<b>Gozo Today</b> [1]"),
     C("“Camilleri said Gozo had already begun its transition through measures including a fully electric public "
       "transport fleet, investment in renewable energy and cleaner mobility…” (outlet’s paraphrase, not in quotation marks)."),
     C("Same article."), C("<b>Paraphrase</b>")],
    [C("<b>TVM News</b>, 28 May and 4 Jul 2026 [3, 4]"),
     C("Gozo’s bus service “completely operated with electric buses”; 22 new buses; EUR 11 million; first full month "
       "carried 332,000 passengers; “end of diesel-powered buses in Gozo”; 1,300 t CO2 a year estimated saving."),
     C("Read in full, 6 Oct 2026."), C("Evidence (operator and government statements)")],
    [C("<b>Eurostat</b>, env_air_gge and demo_r_pjangrp3 [5, 6]"),
     C("Malta greenhouse-gas inventory by sector; population of Gozo and Comino (NUTS 3, MT002)."),
     C("Downloaded 6 Oct 2026 (data/cc-031/)."), C("<b>Primary data</b>")],
], [38 * mm, 74 * mm, 36 * mm, 22 * mm]))
S += [Spacer(1, 4 * mm),
      callout([P("WHAT WE COULD NOT READ", tag),
               P("The plan itself (KPMG for the GRDA and the Climate Action Authority) was not available to us: it is "
                 "not on the GRDA pages we could read, and Transport Malta, the Independent and MaltaToday returned "
                 "access errors. A 2025 tender summary we could only see through search results says the plan would "
                 "“establish” the target date from an energy baseline and a greenhouse-gas inventory; we did not read "
                 "the tender itself [7 ◆]. Routes tried are listed in <i>literature/CC-031/README.md</i>.", small)],
              bg=AMBER_PALE, bar=AMBER), Spacer(1, 4 * mm)]

# ================================================================== 2
S.append(SectionHeading(2, "Method"))
S.append(P("<b>Questions.</b> (A) Is the first climate-neutral region a measurable commitment? (B) Is Gozo’s public "
           "transport fleet fully electric? (C) How much of the task does the fleet change address?"))
S.append(P("<b>Evidence.</b> For A we read the quoted words and looked for a target year, baseline and boundary. For B "
           "we read two TVM News reports of Malta Public Transport and government statements. For C, on 6 October "
           "2026 we downloaded Malta’s greenhouse-gas inventory (Eurostat env_air_gge, total excluding land use and "
           "international transport, and the road-transport line) and population (demo_r_pjangrp3, Gozo and Comino "
           "NUTS 3) with <i>fetch.py</i>, and computed the scale check with <i>calc.py</i> (outputs in "
           "<i>data/cc-031/checks.csv</i>). No Eurostat status flags apply to the values used."))
S.append(P("<b>The limit of the scale check.</b> Eurostat has no Gozo inventory. We multiplied Malta’s sector totals by "
           "Gozo’s share of population (7.26% in 2024). That is a crude proxy: Gozo has no power station, a different "
           "vehicle and tourism mix, and its sea link to Malta runs on ferry fuel that may be counted elsewhere. We use it "
           "only to show whether the buses are a large or small part of the total, not to state a Gozo figure."))
S.append(P("<b>Grades.</b> Official statistics are grade C in our scale; news reports of operator statements are grade D "
           "and are used only to establish what was announced. <b>Verdicts</b> and <b>pledge labels</b> follow Appendix A."))

# ================================================================== 3
S.append(CondPageBreak(110 * mm))
S.append(SectionHeading(3, "What the evidence shows"))
S.append(P("<b>The fleet.</b> TVM News reported on 28 May 2026 that public transport in Gozo “is now being completely "
           "operated with electric buses and zero emissions through an €11-million investment”, including a new "
           "charging depot at Ta’ Xħajma; the minister described it as “the biggest ever investment in public transport "
           "in Gozo” and a step towards a carbon-neutral island [3]. A month later TVM News reported that Malta Public "
           "Transport carried more than 332,000 passengers in the first full month (up 11% on a year earlier), that the "
           "change “marked the end of diesel-powered buses in Gozo”, and that the operator estimates the electric fleet "
           "will eliminate about 1,300 tonnes of CO2 a year [4]."))
S.append(fig(FIG / "fig1_scale.png", width=CW * 0.95))
S.append(P("Figure 1. The estimated annual saving from the electric buses against an approximate Gozo road-transport total "
           "and an approximate all-sector total (population-proportional, 2024).", cap))
S.append(P("<b>Scale.</b> Malta’s 2024 inventory was 2,170 kt CO2e, of which road transport was 690 kt (32%). Gozo and "
           "Comino hold 7.26% of the population, so the proportional approximations are about 158 kt for all sectors and "
           "50 kt for road transport. The operator’s 1.3 kt is about 2.6% of the road-transport approximation, 0.19% of "
           "Malta’s road transport and 0.06% of Malta’s total. Road-transport emissions in Malta rose 39% between 2005 and "
           "2024, from 17% to 32% of the total, so the pressure runs against the plan."))
S.append(callout([P("WHAT THIS DOES AND DOES NOT SHOW", tag),
                  P("The fleet change is real and concrete, and the statement does not say it is enough. But a region "
                    "is only climate-neutral when its remaining emissions are cut or offset to zero within a defined "
                    "boundary. The plan’s boundary (does it include the ferry link, electricity imported by cable, "
                    "private cars?) decides what counts, and we have not seen it.", small)],
                 bg=BLUE_PALE, bar=BLUE))

# ================================================================== 4
S.append(Spacer(1, 4 * mm))
S.append(SectionHeading(4, "Where the evidence points different ways"))
S.append(contested("Is the electric fleet a meaningful step towards climate neutrality?", "YES, BUT SMALL", AMBER,
                   "All Gozo bus services are now electric (TVM News [3, 4]); the operator estimates 1,300 t CO2 a "
                   "year saved and patronage rose 11% in the first full month; 22 new buses and a charging depot were funded.",
                   "On our rough scale check the saving is about 2.6% of Gozo’s road-transport emissions, which are "
                   "in turn roughly a third of Malta’s total. Most road emissions are private vehicles. The estimate is "
                   "the operator’s own, and it depends on the grid mix that charges the buses, which we did not "
                   "assess.",
                   "Both sides can hold at once. The minister listed the fleet as a measure begun, not as the whole "
                   "transition, so the second column limits how far it is read, not whether it is true.",
                   label_a="EVIDENCE FOR THE CLAIM", label_b="CAVEATS"))

# ================================================================== 5
S.append(CondPageBreak(120 * mm))
S.append(SectionHeading(5, "Testing the claim"))
verd = lambda t, c: chip(t, c, w=29 * mm)
S.append(std_table([
    [C("Sub-claim", cellh), C("Said by", cellh), C("What the evidence shows", cellh), C("Rating", cellh)],
    [C("<b>A.</b> Vision of Gozo becoming the first climate-neutral region in Malta"), C("Camilleri (quoted) [1]"),
     C("A statement of intent. The words give no target year, baseline or boundary. The plan, which may, was not "
       "obtained. Rated as a pledge."), verd("NOT MEASURABLE (PLEDGE)", GREY)],
    [C("<b>B.</b> Gozo already has a fully electric public transport fleet"), C("Camilleri, paraphrased by Gozo Today [1]"),
     C("TVM News: all Gozo buses electric since late May 2026, end of diesel buses (operator and government "
       "statements) [3, 4]. No independent fleet record read."), verd("LARGELY ACCURATE", GREENC)],
    [C("<b>C.</b> Gozo has begun its transition (fleet, renewables, mobility, water)"), C("Camilleri, paraphrased [1]"),
     C("Only the fleet could be tested. The renewables, rehabilitation and water items are named without figures in "
       "the report we read and are not tested here."), verd("NOT TESTED", GREY)],
    [C("<b>D.</b> Scale of the fleet change (our check)"), C("Not claimed"),
     C("About 1.3 kt CO2 a year, roughly 2.6% of a proportional Gozo road-transport estimate: a small part of the "
       "total, and not something the statement asserts otherwise."), verd("CONTEXT", AMBER)],
], [42 * mm, 24 * mm, 70 * mm, 34 * mm], valign="MIDDLE"))

# ================================================================== 6
S += [Spacer(1, 6 * mm), SectionHeading(6, "Verdict, pledge and requests for evidence"),
      verdict_box("Largely supported", "The fleet part is backed by public reports; the “vision” is rated as a pledge "
                  "(Not measurable). Confidence: moderate."), Spacer(1, 4 * mm)]
S.append(P("<b>Why.</b> (1) The factual part that can be tested, the electric fleet, is consistently reported, with "
           "dates, numbers and the operator’s own name behind it. (2) It rests on operator and government statements; "
           "the Transport Malta fleet page could not be read, so we rate it <i>Largely supported</i>, not <i>Supported</i>, "
           "and our confidence is moderate. (3) The minister did not claim the fleet was sufficient, and the "
           "scale check shows it is a small part of the total, which is context rather than a flaw in the statement."))
S.append(callout([P("PLEDGE LABEL: NOT MEASURABLE (AS OF 6 OCT 2026)", tag),
                  P("The sentence expresses a vision with no date, baseline or boundary, so delivery cannot be checked "
                    "against it. This is a label about the wording, not a judgement of the plan, which may set a target "
                    "year; we could not read it. If it does, the label should be revisited as a measurable pledge. "
                    "The label does not say the aim is unrealistic or that anyone intends otherwise.", small)],
                 bg=GREY_PALE, bar=GREY))
S.append(P("Evidence we are asking for", h2))
S.append(requests_list([
    "The published Climate Neutrality Plan for Gozo: target year, baseline year and emissions, boundary and measures.",
    "Gozo’s greenhouse-gas inventory, or the method used to estimate it, if the plan has one.",
    "Transport Malta’s fleet or licensing record showing the buses in Gozo service by fuel type.",
    "Whether the Gozo–Malta ferry link and imported electricity are inside the boundary.",
]))
S += [Spacer(1, 4 * mm),
      callout([P("RIGHT OF REPLY", tag),
               P("A reply is sought for the pledge label <i>Not measurable</i> (maintainer rule of 5 October 2026). "
                 "The maintainer handles it; nothing has been sent. Until the deadline has passed this is a draft "
                 "label on this site only and is not to be circulated elsewhere.", small)], bg=AMBER_PALE, bar=AMBER)]

# ================================================================== 7
S += [Spacer(1, 6 * mm), SectionHeading(7, "Limitations")]
for l in ["We did not read the plan, so we cannot say whether it sets a target year, and the pledge label may change.",
          "Only one sentence of the minister’s words is in quotation marks. The fleet statement is the outlet’s paraphrase "
          "of him, so we test it as reported, not as spoken.",
          "Fleet evidence is from TVM News reporting the operator and the minister; Transport Malta’s page and the "
          "Independent’s report (found in search results) could not be read.",
          "The Gozo emissions figures are a population-proportional approximation of Malta’s inventory, not Gozo data. The "
          "1,300 t saving is the operator’s estimate and we did not recompute it from bus mileage or the electricity mix.",
          "Production-based national inventory: it excludes international aviation and shipping and imported emissions."]:
    S.append(P("• " + l, bul))

S += [Spacer(1, 6 * mm), SectionHeading(None, "References")]
S += references([
    ("1", "Calleja L. (25 Sep 2026). Gozo climate neutrality plan enters implementation phase. Gozo Today.",
     "https://gozotoday.com.mt/2026/09/25/gozo-climate-neutrality-plan-enters-implementation-phase/"),
    ("2", "Gozo Regional Development Authority (30 Sep 2026). Gozo Towards Climate Neutrality Conference. News notice.",
     "https://grda.mt/gozo-towards-climate-neutrality-conference/"),
    ("3", "TVM News (28 May 2026). Public transport in Gozo is now being completely operated with electric buses.",
     "https://tvmnews.mt/en/news/public-transport-in-gozo-is-now-being-completely-operated-with-electric-buses/"),
    ("4", "Micallef M. (4 Jul 2026). 11% increase in public transport use in Gozo since full transition to electric "
          "buses. TVM News.",
     "https://tvmnews.mt/en/news/11-increase-in-public-transport-use-in-gozo-since-full-transition-to-electric-buses/"),
    ("5", "Eurostat. Greenhouse gas emissions by source sector (env_air_gge), retrieved 6 Oct 2026.",
     "https://ec.europa.eu/eurostat/databrowser/view/env_air_gge/default/table"),
    ("6", "Eurostat. Population on 1 January by age group, sex and NUTS 3 region (demo_r_pjangrp3), retrieved 6 Oct 2026.",
     "https://ec.europa.eu/eurostat/databrowser/view/demo_r_pjangrp3/default/table"),
    ("7", "MaltaToday. Gozo seeks experts to set target date for climate neutrality. (Seen only as a search result; "
          "page returns 403. Second-hand.)",
     "https://www.maltatoday.com.mt/environment/planning/131454/gozo_seeks_experts_to_set_target_date_for_climate_neutrality"),
    ("8", "Miżien. Calculation script and outputs: tools/cc-031-report/calc.py; data/cc-031/checks.csv.", ""),
])

S.append(PageBreak())
S += appendix_a("A experiment · B observational study with a control or gradient · C review, guidance or "
                "official statistics · D assertion or anecdote. ◆ marks a source known only second-hand.", pledges=True)
S += [Spacer(1, 5 * mm)]
S += revision_log([("1.0", "6 Oct 2026", "First issue. Verdict Largely supported (moderate confidence); pledge label Not "
                                         "measurable; pending right of reply.")])

build_report(Report(
    number="031", out=str(FIG / "report.pdf"), kicker="Climate and energy",
    title_lines=["Gozo, the first", "climate-neutral", "region?"],
    subtitle_lines=["Testing the minister’s “vision” and", "the electric buses against public data"],
    quote_lines=["“The plan published today is an important step to continue", "to realise our vision of Gozo becoming the first",
                 "climate-neutral region in Malta.”"], quote_size=14,
    attribution="Clint Camilleri, Minister for Gozo, 25 September 2026.",
    context="As quoted by Gozo Today; the fleet statement is the outlet’s paraphrase.",
    verdict="Largely supported", verdict_note="Buses are electric; the “vision” is Not measurable (pledge)",
    footer_lines=["Version 1.0  ·  6 October 2026", "Status: draft, pending right of reply (pledge label)",
                  "Prepared from public sources and Eurostat data.", "Repository: github.com/leandergrech/Mizien"],
    running_head="Gozo climate neutrality and electric buses", version="1.0", date="6 October 2026",
    status_note="pending right of reply",
    pdf_title="Gozo, the first climate-neutral region? Claim Check 031",
    pdf_subject="Tests the Minister for Gozo's statement on the climate neutrality plan and the electric bus fleet",
    story=S))
