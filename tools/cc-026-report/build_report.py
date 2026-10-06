"""Claim Check 026 report. Run calc.py and figures.py first. Output: out/report.pdf"""
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
      P("On 18 June 2026 Newsbook reported: <b>“Malta recorded the highest increase in greenhouse gas emissions among "
        "European Union member states over the past decade, according to new estimates published by Eurostat.”</b> "
        "It added that Malta’s emissions “rose by an estimated 169.4% between 2015 and 2025”. We recomputed the figure "
        "from Eurostat’s database and tested what it measures against the national inventory.", lead)]
S.append(key_points([
    ("The number is right.",
     "Eurostat’s own release of 16 June 2026 gives Malta +169.4%, the next highest being Cyprus (+10.7%). Today’s "
     "database, revised since, gives +169.7%. The EU as a whole fell 17.2%. Only four member states rose."),
    ("It is almost all air transport.",
     "Air transport emissions attributed to Malta grew from 444 to 4,730 thousand tonnes CO2e (2015–2024), 98.6% of the "
     "whole increase. Everything else combined rose 2.9%."),
    ("It is not emissions in Malta.",
     "Eurostat’s accounts follow the residence principle: emissions of resident units wherever they occur. The "
     "territorial inventory reported to the UN rose 1.6% over the same years (2015–2024), and is 27% below 2005."),
    ("The article says so.",
     "Newsbook explains the aviation difference in its own text, so the body is accurate. The headline, "
     "read alone, can leave the impression that more pollution is produced in Malta."),
    ("Verdict: largely supported (high confidence).",
     "The statement is an accurate report of Eurostat’s estimate. The caveat is what the estimate measures."),
]))
S += [Spacer(1, 4 * mm), VerdictMeter(1), Spacer(1, 3 * mm),
      tiles([("+169.7%", RED, "Malta, 2015–2025, Eurostat air emissions accounts (EU −17.2%)"),
             ("98.6%", ORANGE, "Share of the 2015–2024 increase from air transport"),
             ("+2.9%", GREEN, "Malta excluding air transport, 2015–2024"),
             ("+1.6%", GREY, "National inventory (UNFCCC), 2015–2024")]),
      Spacer(1, 4 * mm),
      up_down("Evidence that the air transport emissions are largely produced by activity in or over Malta (for example, "
              "a high share of Malta’s own passengers and flights), which would make the account a fair picture of "
              "Maltese emissions.",
              "A headline or statement that presents the Eurostat figure as emissions released in Malta; or Eurostat "
              "dropping the residence adjustment for Malta in a later revision."),
      Spacer(1, 5 * mm)]
S += toc([("1", "The claim and what we could verify"), ("2", "Method"), ("3", "What Eurostat measures"),
          ("4", "What the data show"), ("5", "Where the measures disagree"),
          ("6", "Testing the claim"), ("7", "Verdict and requests for evidence"), ("8", "Limitations")])
S.append(PageBreak())

# ================================================================== 1
S.append(SectionHeading(1, "The claim and what we could verify"))
S.append(P("The claim is a Newsbook news article by Damian Micallef, published on 18 June 2026 [1], which we read in full. "
           "Newsbook is reporting Eurostat, so we compared it with Eurostat’s own news item of 16 June 2026 [2] and "
           "with the database table behind it [3]. The speaker whose words we test is the outlet; Eurostat’s "
           "estimate is the thing reported."))
S.append(P("Headline of the article: “Malta records EU’s largest rise in greenhouse gas emissions”. The sentences "
           "quoted below are from its text.", small))
S.append(std_table([
    [C("What was written or published", cellh), C("Who", cellh), C("Access", cellh)],
    [C("“Malta recorded the highest increase in greenhouse gas emissions among European Union member states over the "
       "past decade, according to new estimates published by Eurostat.”"), C("Newsbook [1]"), C("Read in full")],
    [C("Malta’s emissions “rose by an estimated 169.4% between 2015 and 2025”, one of only four EU countries to rise "
       "(Cyprus 10.7%, Lithuania 9.5%, Romania 5.4%)."), C("Newsbook [1]"), C("Read in full")],
    [C("“Increases were estimated for Malta (+169.4%), Cyprus (+10.7%), Lithuania (+9.5%) and Romania (+5.4%).”"),
     C("Eurostat news item [2]"), C("Read in full")],
    [C("Eurostat counts aircraft registered in Malta wherever they fly; UN accounting counts emissions in Malta only. "
       "The Central Bank of Malta argued that emission intensity has been declining."),
     C("Newsbook [1] (the outlet’s paraphrase)"), C("Central Bank report not read ◆")],
], [104 * mm, 34 * mm, 32 * mm]))
S += [Spacer(1, 4 * mm),
      callout([P("FAIRNESS NOTE", tag),
               P("Newsbook did not hide the methodological point: its text sets out the aviation difference and the "
                 "Maltese authorities’ objection. This check therefore asks two things: is the number right, and does "
                 "the headline tell a reader what the number measures? We apply the same test to the Maltese "
                 "authorities’ preferred measure, which also has limits (section 5).", small)],
              bg=AMBER_PALE, bar=AMBER), Spacer(1, 4 * mm)]

# ================================================================== 2
S.append(SectionHeading(2, "Method"))
S.append(P("<b>Question.</b> Is Eurostat’s +169.4% correct and Malta’s place at the top of the EU real, and what does "
           "the figure measure?"))
S.append(P("<b>Evidence.</b> Eurostat air emissions accounts by activity, table env_ac_ainah_r2 (greenhouse gases, all "
           "activities plus households, thousand tonnes CO2-equivalent), for Malta and every member state [3]; "
           "Eurostat’s methodological metadata for that table [4]; and the national greenhouse gas inventory "
           "(UNFCCC common reporting format) as published by Eurostat in env_air_gge [5]. All numbers are recomputed by "
           "<i>tools/cc-026-report/calc.py</i> from files in <i>data/cc-026/</i>, retrieved on 5 October 2026."))
S.append(P("<b>Grades.</b> Official statistics are grade C. No peer-reviewed study was needed to test an arithmetic "
           "claim about a published statistic; the methodological statements rest on Eurostat’s own documentation. "
           "<b>Verdicts</b> follow the five-point scale in Appendix A."))

# ================================================================== 3
S.append(CondPageBreak(80 * mm))
S.append(SectionHeading(3, "What Eurostat measures"))
S.append(P("Two official ways of counting greenhouse gases are in use, and both are published by Eurostat. "
           "<b>Air emissions accounts</b> are built to sit beside national accounts. Eurostat’s metadata says they “follow "
           "the residence principle, i.e. they record emissions related to resident unit’s activities, regardless where "
           "those occur geographically” [4]. An airline that is a resident unit of Malta therefore has its flights "
           "counted for Malta, wherever they take place. The <b>national inventory</b> reported under the UN climate "
           "convention follows the territorial principle, and treats international aviation and navigation as memo "
           "items outside the national total [5]."))
S.append(P("Neither is wrong. They answer different questions: what the Maltese economy (including operators based "
           "here) emits, and what is released in Malta. Newsbook says the accounts allocate emissions to the country "
           "“where the aircraft is registered”; Eurostat’s metadata speaks of the resident unit, which is the operator. "
           "We could not tell from the data which operators are involved, and we do not assess any company."))

# ================================================================== 4
S.append(CondPageBreak(150 * mm))
S.append(SectionHeading(4, "What the data show"))
S.append(fig(FIG / "fig2_eu_changes.png"))
S.append(P("Figure 1. Change in greenhouse gas emissions of each member state’s economy and households, 2015–2025 "
           "(Eurostat env_ac_ainah_r2; 2025 is an early estimate). Malta is the largest increase, as reported.", cap))
S.append(fig(FIG / "fig1_malta_accounts.png"))
S.append(P("Figure 2. Malta’s emissions by the account (bars, split into air transport and the rest) and by the "
           "national inventory (line). The accounts and the inventory agreed until about 2014 and diverge after air "
           "transport takes off; 2025 has no activity breakdown yet.", cap))
S.append(std_table([
    [C("Indicator", cellh), C("Value", cellh), C("Source", cellh), C("Grade", cellh)],
    [C("Malta, all activities and households, 2015 → 2025"), C("2,603 → 7,021 kt (<b>+169.7%</b>)"),
     C("Eurostat env_ac_ainah_r2"), grade_tag("C")],
    [C("EU-27, same measure"), C("−17.2%"), C("Eurostat env_ac_ainah_r2"), grade_tag("C")],
    [C("Member states that increased"), C("4 of 27: MT +169.7%, CY +10.7%, LT +8.4%, RO +5.6%"),
     C("Eurostat env_ac_ainah_r2"), grade_tag("C")],
    [C("Malta air transport (NACE H51), 2015 → 2024"), C("444 → 4,730 kt (×10.7); 17% → 68% of total"),
     C("Eurostat env_ac_ainah_r2"), grade_tag("C")],
    [C("Share of 2015–2024 increase due to air transport"), C("<b>98.6%</b>"), C("calculated"), grade_tag("C")],
    [C("Malta excluding air transport, 2015 → 2024"), C("2,159 → 2,221 kt (+2.9%)"), C("calculated"), grade_tag("C")],
    [C("Electricity, gas and steam (NACE D), 2015 → 2024"), C("890 → 743 kt (−16.5%)"),
     C("Eurostat env_ac_ainah_r2"), grade_tag("C")],
    [C("National inventory (UNFCCC, territorial), 2015 → 2024"), C("2,136 → 2,170 kt (+1.6%); 2005–2024: −27.4%"),
     C("Eurostat env_air_gge [5]"), grade_tag("C")],
    [C("International aviation memo item (fuel sold in Malta), 2015 → 2024"), C("360 → 528 kt (+46.6%)"),
     C("Eurostat env_air_gge [5]"), grade_tag("C")],
], [66 * mm, 62 * mm, 30 * mm, 12 * mm]))
S.append(P("All values in <i>data/cc-026/checks.csv</i>. The numbers in Eurostat’s 16 June release (Malta +169.4%, "
           "Lithuania +9.5%, Romania +5.4%) differ slightly from today’s database (+169.7%, +8.4%, +5.6%) because "
           "Eurostat revises the series; the ranking is unchanged.", cap))

# ================================================================== 5
S.append(CondPageBreak(120 * mm))
S.append(SectionHeading(5, "Where the measures disagree"))
S.append(contested(
    "Q1  Did Malta’s emissions rise by 169%?", "YES ON ONE MEASURE, NO ON ANOTHER", AMBER,
    "In Eurostat’s air emissions accounts, Malta’s emissions rose by 169.7% (2015–2025), the biggest increase in the "
    "EU, driven by air transport (98.6% of the 2015–2024 rise). Eurostat itself reports the number in this form [2].",
    "In the national inventory under the territorial principle, emissions were 2,136 kt in 2015 and 2,170 kt in 2024 "
    "(+1.6%), and 27% below 2005 [5]. The fuel sold for international aviation in Malta rose 46.6%, not tenfold.",
    "The measures count different things: operators resident in Malta wherever they fly, against emissions released "
    "in Malta. <b>For this claim:</b> the figure is correct as an account of Malta’s economy; it is not a measure "
    "of the pollution produced in Malta.",
    label_a="EVIDENCE FOR THE CLAIM", label_b="EVIDENCE FOR A DIFFERENT PICTURE"))
S.append(contested(
    "Q2  Is the territorial view the fairer one for Malta?", "NOT NECESSARILY", AMBER,
    "The inventory shows what happens inside Malta’s borders and is what national targets under the Paris "
    "Agreement are judged on. It excludes international aviation and shipping altogether.",
    "Excluding them leaves out a real and growing source: the accounts attribute 4,730 kt to Malta-based air transport in "
    "2024, more than twice the entire national inventory (2,170 kt). Other countries’ residents’ flights are counted "
    "for their own countries in the accounts, so the comparison is like with like within the accounts.",
    "Both views are legitimate; each omits something. A fair statement names which one it uses. <b>For this claim:</b> "
    "the body of the Newsbook article does that; the headline does not.",
    label_a="FOR THE TERRITORIAL (OFFICIAL) VIEW", label_b="AGAINST RELYING ON IT ALONE"))

# ================================================================== 6
S.append(CondPageBreak(110 * mm))
S.append(SectionHeading(6, "Testing the claim"))
verd = lambda t, c: chip(t, c, w=29 * mm)
S.append(std_table([
    [C("Sub-claim", cellh), C("Said by", cellh), C("What the evidence shows", cellh), C("Rating", cellh)],
    [C("<b>A.</b> Eurostat estimates Malta’s emissions rose 169.4% in 2015–2025"), C("Newsbook [1]"),
     C("Eurostat’s release says +169.4% [2]; recomputed from the database +169.7% after revision [3]."),
     verd("SUPPORTED", GREENC)],
    [C("<b>B.</b> This is the highest increase in the EU; only four rose"), C("Newsbook [1]"),
     C("Malta first, then Cyprus +10.7%, Lithuania, Romania; 23 fell [2][3]."), verd("SUPPORTED", GREENC)],
    [C("<b>C.</b> Eurostat counts Malta-registered aircraft wherever they fly; the UN counts emissions in Malta only"),
     C("Newsbook [1] (outlet’s paraphrase)"),
     C("Eurostat: residence principle, resident units [4]; inventory: territorial, international aviation a memo "
       "item [5]. “Registered” is the outlet’s wording; Eurostat speaks of the resident operator."),
     verd("LARGELY SUPPORTED", LG)],
    [C("<b>D.</b> Headline: “largest rise in greenhouse gas emissions” (read alone)"),
     C("Newsbook [1] (headline)"),
     C("True of the accounts; territorial emissions rose 1.6% (2015–2024). The body gives the context."),
     verd("NEEDS CONTEXT", AMBER)],
    [C("<b>E.</b> Central Bank of Malta: intensity declining and at historic lows"),
     C("Newsbook [1], citing the Central Bank (second-hand ◆)"),
     C("Second-hand: we did not read the report ◆. Not tested."), verd("NOT TESTED", GREY)],
], [46 * mm, 26 * mm, 70 * mm, 28 * mm], valign="MIDDLE"))

# ================================================================== 7
S += [Spacer(1, 6 * mm), SectionHeading(7, "Verdict and requests for evidence"),
      verdict_box("Largely supported", "An accurate report of Eurostat’s estimate; what it measures needs saying. "
                  "Confidence: high."), Spacer(1, 4 * mm)]
S.append(P("<b>Why.</b> (1) The figure matches Eurostat’s own release and our recomputation, and Malta’s place at the "
           "top of the EU holds. (2) The increase is almost entirely air transport attributed to Malta under the "
           "residence principle; the territorial inventory is nearly flat (+1.6%). (3) Newsbook’s text explains this, so "
           "the article as a whole is not misleading; the headline alone would be incomplete. These caveats qualify the "
           "claim but do not reverse it, which our scale calls <i>Largely supported</i>."))
S.append(P("<b>What this verdict does not say.</b> It does not say Malta’s climate record is good or bad. It does not "
           "say the account or the inventory is the right yardstick, and it makes no judgement about any airline or "
           "authority. Malta’s non-aviation emissions did not fall either (+2.9% 2015–2024) while the EU’s did."))
S.append(P("Evidence we are asking for", h2))
S.append(requests_list([
    "From the Maltese authorities: the Central Bank of Malta report on emission intensity, and the national "
    "estimate of aviation emissions attributable to flights from and to Malta.",
    "From Eurostat: the activity breakdown for 2025 when published, and Malta’s residence-adjustment bridge items.",
    "Which operators account for the air transport emissions (not assessed here, and not attributed to anyone).",
]))

# ================================================================== 8
S += [Spacer(1, 6 * mm), SectionHeading(8, "Limitations")]
for l in ["The 2025 figure is an early estimate (sum of four quarterly accounts) with no breakdown by activity; the "
          "decomposition is for 2015–2024.",
          "Eurostat revises its series: today’s figures differ slightly from the 16 June release.",
          "We did not read Eurostat’s residence-adjustment guidelines in full; the principle is quoted from the "
          "table’s metadata. We did not read the Central Bank of Malta report.",
          "We did not estimate how much of the air transport total arises from flights to, from or over Malta.",
          "No peer-reviewed literature was used: the claim is about a published statistic."]:
    S.append(P("• " + l, bul))

S += [Spacer(1, 6 * mm), SectionHeading(None, "References")]
S += references([
    ("1", "Micallef D. (18 Jun 2026). Malta records EU’s largest rise in greenhouse gas emissions. <i>Newsbook</i>.",
     "https://newsbook.com.mt/en/malta-records-eus-largest-rise-in-greenhouse-gas-emissions/"),
    ("2", "Eurostat (16 Jun 2026). EU economy greenhouse gas emissions: −17% since 2015. News article.",
     "https://ec.europa.eu/eurostat/web/products-eurostat-news/w/ddn-20260616-2"),
    ("3", "Eurostat. Air emissions accounts by NACE Rev. 2 activity (env_ac_ainah_r2); updated 7 Aug 2026; retrieved "
          "5 Oct 2026.", "https://ec.europa.eu/eurostat/databrowser/view/env_ac_ainah_r2/"),
    ("4", "Eurostat. Reference metadata for env_ac_ainah_r2 (air emissions accounts), coverage and concepts.",
     "https://ec.europa.eu/eurostat/cache/metadata/EN/env_ac_ainah_r2_simsae_dk.htm"),
    ("5", "Eurostat. Greenhouse gas emissions by source sector (env_air_gge), national inventory data; updated "
          "2 Jun 2026; retrieved 5 Oct 2026.", "https://ec.europa.eu/eurostat/databrowser/view/env_air_gge/"),
    ("6", "MiŻien. Data and calculations: data/cc-026/; tools/cc-026-report/calc.py.", ""),
])

S.append(PageBreak())
S += appendix_a("A experiment · B observational study with a control or gradient · C review, guidance or "
                "official statistics · D assertion or anecdote. ◆ marks a source known only second-hand.")
S += [Spacer(1, 5 * mm)]
S += revision_log([("1.0", "5 Oct 2026", "First issue. No right of reply needed: the claim reports a Eurostat "
                    "estimate and the verdict is Largely supported."),
                   ("1.1", "6 Oct 2026", "Corrections after the 6 Oct audit: cover status line now reads \"no right of "
                    "reply needed\" (it said draft); cover and flyer label the quoted sentence as the article’s "
                    "opening line, not the headline; sub-claim table gives who said each part; article date and author "
                    "recorded in the claim record. Findings, verdict and confidence unchanged.")])

build_report(Report(
    number="026", out=str(FIG / "report.pdf"), kicker="Climate and energy",
    title_lines=["Malta’s", "169% rise in", "emissions"],
    subtitle_lines=["Testing a news report of a Eurostat estimate",
                    "against the accounts and the national inventory"],
    quote_lines=["“Malta recorded the highest increase in greenhouse", "gas emissions among European Union member states”"],
    quote_size=14,
    attribution="Newsbook, 18 June 2026, opening line of the article, reporting Eurostat.",
    context="Malta’s emissions “rose by an estimated 169.4% between 2015 and 2025”.",
    verdict="Largely supported", verdict_note="The number is right; check what it counts",
    footer_lines=["Version 1.1  ·  6 October 2026", "Status:",
                  "Prepared from public sources and Eurostat data.", "Repository: github.com/leandergrech/Mizien"],
    running_head="Malta greenhouse gas emissions – Eurostat estimate", version="1.1", date="6 October 2026",
    pdf_title="Malta’s 169% rise in emissions? Claim Check 026",
    pdf_subject="Tests Newsbook's report of Eurostat's estimate of Malta's greenhouse gas emissions growth",
    story=S))
