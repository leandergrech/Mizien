"""Claim Check 089 report. Run fetch.py, calc.py and figures.py first. Output: out/report.pdf"""
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
      P("A press release by PwC Malta on its Summer 2026 Economic Update, posted by the Malta Chamber on 22 July 2026 "
        "under the headline <b>“Malta’s rapid population growth creates urgent need to focus on the country’s "
        "infrastructure demands for the future”</b>, says that <b>“Infrastructure demands require urgent "
        "investment.”</b> The wording is PwC’s; the Chamber carried it as sponsored content. We tested the numbers against "
        "Eurostat and the World Bank: the population facts hold, the bed and electricity illustrations mostly "
        "reproduce (one percentage is mislabelled), and “urgent” is a judgement data cannot settle.", lead)]
S.append(key_points([
    ("The growth is real and unmatched.",
     "Malta’s population was 588,254 on 1 January 2026, up 14,004 (2.44%) in 2025; the EU-27 grew 0.16% and the "
     "next-fastest state, Cyprus, 1.38%. Since 2015 Malta has grown 34%, the EU 2%."),
    ("The 2030 figure is plausible, not verified.",
     "PwC’s base case of 636,000 sits between Eurostat’s EUROPOP2025 baseline (621,470 on 1 January 2030) and its "
     "higher-migration variant (650,230). PwC’s model itself was not readable."),
    ("Malta is below the EU on hospital beds and relies on imported power.",
     "391 beds per 100,000 residents in 2024 against 507 in the EU-27 (18th of 27); electricity imports rose from 648 "
     "GWh in 2023 to 970 GWh in 2024, matching PwC’s figure."),
    ("One number in the release does not follow from its inputs.",
     "Imports rising from 970 to 1,304 GWh is +34%, not “circa 25%”. The bed additions (+329, +1,054) "
     "differ from ours (+262 to +303, +1,028)."),
    ("Verdict: largely supported (moderate confidence).",
     "The factual premises hold and the policy direction follows from them; the caveats are the one mislabelled "
     "percentage, bed and density figures that are close but not identical, and an unread model."),
]))
S += [Spacer(1, 2.5 * mm), VerdictMeter(1), Spacer(1, 3 * mm),
      tiles([("+2.44%", ORANGE, "Malta’s population growth in 2025, the highest of 27 (EU-27 +0.16%)"),
             ("391", RED, "hospital beds per 100,000 residents, 2024: 18th of 27 (EU-27 507)"),
             ("+34%", ORANGE, "rise in electricity imports implied by PwC’s own figures (release says “circa 25%”)"),
             ("636,000", GREEN, "PwC’s 2030 base case: between Eurostat’s baseline (621,470) and high-migration (650,230)")]),
      Spacer(1, 4 * mm),
      up_down("PwC’s report showing its definitions and assumptions, and a published capacity indicator "
              "(not only beds and electricity) that the government or regulators accept as the benchmark.",
              "Evidence that bed or power capacity already grows faster than the population (new hospital or "
              "generation capacity), or that Malta’s lower median age makes the bed gap smaller than the headline."),
      Spacer(1, 3 * mm)]
S += toc([("1", "The claim and what we could verify"), ("2", "Method"), ("3", "What the research says"),
          ("4", "What the data show"), ("5", "Where the evidence points different ways"),
          ("6", "Testing the claim"), ("7", "Verdict and requests for evidence"), ("8", "Limitations")])
S.append(PageBreak())

# ================================================================== 1
S.append(SectionHeading(1, "The claim and what we could verify"))
S.append(P("The release was published by the Malta Chamber on 22 July 2026 under “Sponsored Content” [1]. It carries "
           "the same text as PwC Malta’s release on Finance Malta (17 July 2026), which the CC-099 check read [2]. The "
           "speaker is PwC Malta: the release names PwC’s Economic Update, PwC’s modelling and a PwC partner. The Chamber "
           "page adds no wording of its own, so we rate PwC’s statements as the Chamber published them. We read the Chamber "
           "page in full on 13 October 2026. PwC’s report itself could not be read (the PwC page held no report text)."))
S.append(std_table([
    [C("What was said (paragraph of the release)", cellh), C("Who", cellh), C("Access", cellh)],
    [C("“Malta’s population reached 588,254 by year-end 2025 … an increase of approximately 14,000 residents (2.4%)” (1)"),
     C("PwC Malta [1]"), C("Read in full")],
    [C("Base case of “636,000 by 2030”; Malta “the fourth most densely populated country globally”, about 1,862 people per "
       "km², projected 2,013 by 2030 (2, 3)"), C("PwC Malta [1]"), C("Read in full")],
    [C("Hospital beds: 397 per 100,000 against an EU average of 511, “17th among EU peers”; “approximately 329 additional "
       "hospital beds” (15%) to keep standing, “nearly 1,054” (48%) for parity (4)"), C("PwC Malta [1]"), C("Read in full")],
    [C("Electricity: “2,138k MWh” produced locally in 2024, “970k MWh” imported; “1,304k MWh” would be imported at 636,000 "
       "residents, “a circa 25% increase in imported energy requirement” (5)"), C("PwC Malta [1]"), C("Read in full")],
    [C("“Infrastructure demands require urgent investment.” “The key policy change will be ensuring that infrastructure, public "
       "services, and long-term planning keep pace” (headline, 4, 6)"), C("PwC Malta [1]"), C("Read in full")],
], [104 * mm, 30 * mm, 36 * mm]))
S += [Spacer(1, 4 * mm),
      callout([P("SCOPE NOTE", tag),
               P("The release’s “31% foreign residents” and “around 38% by 2030” are tested separately in claim check CC-099 "
                 "and are not rated here. This check does not assess which infrastructure projects should be built or "
                 "who should pay, and it covers only the two capacity indicators the release uses.", small)],
              bg=AMBER_PALE, bar=AMBER), Spacer(1, 4 * mm)]

# ================================================================== 2
S.append(SectionHeading(2, "Method"))
S.append(P("<b>Question.</b> Are the release’s numbers right, and do they support its conclusion that population growth calls "
           "for urgent infrastructure investment?"))
S.append(P("<b>Evidence.</b> Eurostat population on 1 January for the EU-27 (demo_gind), EUROPOP2025 projections (proj_25np), "
           "hospital beds (hlth_rs_bds1), electricity balances (nrg_cb_e), land area (demo_r_d3area) and median age "
           "(demo_pjanind), with status flags; World Bank population density for 2023 [3, 4]; two peer-reviewed papers on "
           "hospital capacity and population projections [5, 6]. Every number in the release was recomputed by "
           "<i>tools/cc-089-report/calc.py</i> from files in <i>data/cc-089/</i> (retrieved 13 October 2026)."))
S.append(P("<b>Grades.</b> Official statistics are grade C; peer-reviewed modelling studies are grade B. A press release is grade D "
           "for its own claims. <b>Verdicts</b> follow the five-point scale in Appendix A."))

# ================================================================== 3
S.append(CondPageBreak(60 * mm))
S.append(SectionHeading(3, "What the research says"))
S.append(P("Capacity needs are not a fixed number of beds per head. Bagust, Place and Posnett simulated an English acute hospital and "
           "found that risks become discernible when average bed occupancy exceeds about 85%, and that regular shortages and "
           "periodic bed crises are to be expected at 90% or more [5]. A beds-per-100,000 comparison, as in the release, ignores "
           "occupancy, length of stay and day care, so it signals a gap but cannot size it."))
S.append(P("Projections are conditional on migration assumptions. Keilman’s review of United Nations projections found accuracy "
           "improving over time, with considerable differences between regions [6]. Eurostat’s own variants for Malta "
           "(Figure 1) range from 584,120 to 650,230 on 1 January 2030, so a single base case such as PwC’s is one scenario among several."))

# ================================================================== 4
S.append(CondPageBreak(150 * mm))
S.append(SectionHeading(4, "What the data show"))
S.append(fig(FIG / "fig1_population.png"))
S.append(P("Figure 1. Left: population change 2015–2026 in the 27 Member States. Right: Malta’s population and Eurostat’s "
           "EUROPOP2025 variants, with PwC’s base case. EUROPOP2025’s baseline for 1 January 2026 was 585,012; the actual "
           "figure is 588,254 (0.55% higher).", cap))
S.append(std_table([
    [C("PwC figure", cellh), C("Our recalculation", cellh), C("Source", cellh), C("Result", cellh)],
    [C("588,254 at year-end 2025; +~14,000 (2.4%)"), C("588,254; +14,004 (+2.44%)"), C("Eurostat demo_gind"), C("Equal")],
    [C("“Rapid” growth"), C("+2.44% in 2025, 1st of 27 (EU-27 +0.16%; Cyprus 1.38%); +34.1% since 2015 (EU +2.1%)"),
     C("Eurostat demo_gind"), C("Supported")],
    [C("636,000 by 2030 (base case)"), C("EUROPOP2025: 621,470 (baseline), 650,230 (higher migration) on 1 Jan 2030; rebased on actual 2026: 624,914 and "
       "653,833. If “by 2030” means 1 Jan 2031: baseline 628,876, rebased 632,361"), C("Eurostat proj_25np"),
     C("Within range")],
    [C("1,862 / km² now, 2,013 by 2030"), C("1,865 and 2,016 on Eurostat’s latest area (315.4 km²); PwC’s figures imply 315.9 km² "
       "(Eurostat: 316.0 in 2008–2014)"), C("Eurostat demo_r_d3area"), C("Close")],
    [C("“Fourth most densely populated country globally”"), C("World Bank 2023: Malta 1,754 per km², 8th of 263 entries; "
       "5th among sovereign states (Maldives 1,765 just ahead)"), C("World Bank EN.POP.DNST"), C("Not reproduced")],
], [40 * mm, 72 * mm, 32 * mm, 26 * mm]))
S.append(P("All values in <i>data/cc-089/checks.csv</i>. The World Bank list is of 2023 values for all entries including "
           "territories (Macao, Hong Kong and Gibraltar are not sovereign states: general context).", cap))
S.append(P("Hospital beds", h2))
S.append(P("Eurostat’s series puts Malta at 406 beds per 100,000 residents in 2022 (17th of 27), 394 in 2023 (18th; flagged as a "
           "break in series) and 391 in 2024 (18th); the EU-27 figure was 511 in 2023 and 507 in 2024 [3]. PwC’s 397 and 17th "
           "are close to these but not identical. Malta’s 2,222 beds in 2024 would need to reach 2,484 to hold Eurostat’s own "
           "2024 rate at 636,000 residents (+262, +11.8%), or 2,525 at PwC’s 397 (+303, +13.6%), against PwC’s +329 (+15%). "
           "PwC’s +329 implies about 553,000 residents as the base, below the release’s own 588,254; we cannot say which base PwC used. For "
           "parity with the EU average (511) we get +1,028 (+46%), against PwC’s +1,054 (+48%). Malta’s median age is 40.0 "
           "years, the EU-27’s 44.9, which would lower the number of beds needed per head: context, not a bed target."))
S.append(KeepTogether([fig(FIG / "fig2_beds_electricity.png"),
                       P("Figure 2. Left: hospital beds per 100,000 residents in 2024. Right: electricity produced in Malta and "
                         "imported, 2015–2025 (2025 provisional).", cap)]))
S.append(P("Electricity", h2))
S.append(P("Eurostat’s imports for 2024, 970.4 GWh, equal PwC’s “970k MWh”. PwC’s “locally generated” 2,138 is 2.2% below "
           "Eurostat’s gross production of 2,186 GWh (a net-of-own-use figure would explain a gap; we did not test that). PwC’s 1,304 is "
           "reproduced exactly by scaling 2024 demand (2,138 + 970) by 636,000 / 574,250, the 1 January 2025 population, and subtracting "
           "the unchanged local output: 3,108 × 1.1075 − 2,138 = 1,304. Using the 1 January 2026 population as the base would give 1,222. "
           "The rise from 970 to 1,304 is <b>+34.4%</b>; the release’s “circa 25%” matches only the rise as a share of the new "
           "1,304 (25.6%). Electricity per resident was 5,279 kWh in 2023, 5,460 kWh in 2024 and 5,517 kWh in 2025 (provisional), "
           "so per-head demand did not fall as population grew. The assumption of unchanged local output is a scenario: "
           "production was 2,344, 2,186 and 2,222 GWh in 2023–2025, and imports 648, 970 and 1,031 GWh [3]."))

# ================================================================== 5
S.append(CondPageBreak(120 * mm))
S.append(SectionHeading(5, "Where the evidence points different ways"))
S.append(contested(
    "Q1  Is population growth outpacing capacity?", "ON THE RELEASE’S TWO INDICATORS, YES", AMBER,
    "Malta has the EU’s fastest growth (+34% since 2015) and fewer hospital beds per head than the EU average (391 vs 507). "
    "Electricity imports rose 59% between 2023 and 2025 (648 to 1,031 GWh, 2025 provisional) while local output stayed "
    "near 2,200 GWh.",
    "Beds per head is a crude indicator: Malta is younger (median age 40.0 vs 44.9), its bed count rose in 2024 "
    "(2,177 to 2,222), and beds say nothing about occupancy or day care [5]. Imports also fluctuate (1,526 GWh in 2016, "
    "420 in 2020), and growth in imports is not in itself a shortage.",
    "<b>For this claim:</b> the premises are consistent with a growing gap, but two indicators do not show how large or "
    "how urgent it is."))
S.append(contested(
    "Q2  Is 636,000 by 2030 a fair base case?", "PLAUSIBLE; ONE SCENARIO", AMBER,
    "Malta’s actual population is already 0.55% above Eurostat’s EUROPOP2025 baseline for 2026. Rebased, the baseline "
    "gives 624,914 for 1 January 2030 and 632,361 for 1 January 2031; PwC’s 636,000 is +1.8% and +0.6% from those.",
    "Eurostat’s variants run from 584,120 (no migration) to 650,230 (higher migration) for 1 January 2030, and PwC’s "
    "assumptions (a slowdown in net migration) are not shown. Reaching 636,000 needs about 1.97% a year to 1 January "
    "2030 (1.57% to 2031), below 2025’s 2.44%.",
    "<b>For this claim:</b> a reasonable central case, not a certain one; we have not seen PwC’s model."))
S.append(contested(
    "Q3  Does the release’s arithmetic support its message?", "MOSTLY; ONE SLIP", AMBER,
    "The population, density, electricity-import and parity-bed figures reproduce within a few per cent; the 1,304 GWh "
    "reproduces exactly.",
    "“Circa 25%” should be about 34% on the release’s own figures; the keep-standing bed addition (+329) is higher than "
    "our +262 to +303 and rests on a base we could not reproduce; “fourth most densely populated” is fifth among sovereign "
    "states on World Bank 2023 data.",
    "<b>For this claim:</b> the slips are in the illustrations, and correcting them (34% instead of 25%) strengthens "
    "rather than weakens the message."))

# ================================================================== 6
S.append(CondPageBreak(110 * mm))
S.append(SectionHeading(6, "Testing the claim"))
verd = lambda t, c: chip(t, c, w=29 * mm)
S.append(std_table([
    [C("Sub-claim", cellh), C("What the evidence shows", cellh), C("Rating", cellh)],
    [C("<b>A.</b> Population 588,254 at year-end 2025, up about 14,000 (2.4%)"),
     C("Eurostat demo_gind: 588,254 and +14,004 (+2.44%) [3]."), verd("SUPPORTED", GREENC)],
    [C("<b>B.</b> Malta’s population growth is “rapid”"),
     C("+2.44% in 2025, 1st of 27 (EU-27 +0.16%); +34% since 2015 (EU +2%) [3]."), verd("SUPPORTED", GREENC)],
    [C("<b>C.</b> Base case of 636,000 by 2030"),
     C("Between Eurostat’s baseline and higher-migration variant, rebased or not; PwC’s model unread [3]."),
     verd("WITHIN RANGE", LG)],
    [C("<b>D.</b> Density 1,862 now and 2,013 by 2030"),
     C("1,865 and 2,016 on Eurostat’s area; within 0.2% [3]."), verd("CLOSE", GREENC)],
    [C("<b>E.</b> “Fourth most densely populated country globally”"),
     C("World Bank 2023: 8th of 263 entries, 5th among sovereign states (1,754 vs Maldives 1,765) [4]."),
     verd("NOT REPRODUCED", AMBER)],
    [C("<b>F.</b> Hospital beds: 397 vs EU 511 (17th); +329 to keep standing (15%), +1,054 for parity (48%)"),
     C("391 vs 507 in 2024, 18th (2022: 17th); +262 to +303 to keep standing; +1,028 for parity [3]."),
     verd("CLOSE", GREENC)],
    [C("<b>G.</b> Electricity: 970 GWh imported; 1,304 at 636,000; “circa 25%” rise"),
     C("970 equal; 1,304 reproduced exactly; the rise is +34%, not about 25% [3]."), verd("ONE ERROR", AMBER)],
    [C("<b>H.</b> “Infrastructure demands require urgent investment”"),
     C("A judgement. The premises hold on two indicators; size and urgency are not shown by the release."),
     verd("LARGELY SUPPORTED", LG)],
], [52 * mm, 88 * mm, 30 * mm], valign="MIDDLE"))

# ================================================================== 7
S += [Spacer(1, 6 * mm), SectionHeading(7, "Verdict and requests for evidence"),
      verdict_box("Largely supported", "The factual premises hold; one percentage is mislabelled and “urgent” is a "
                  "judgement. Confidence: moderate."), Spacer(1, 4 * mm)]
S.append(P("<b>Why.</b> (1) Malta’s population growth is the EU’s fastest and the release’s population figures equal "
           "Eurostat’s. (2) Malta has fewer hospital beds per head than the EU average and depends increasingly on imported "
           "electricity, which supports the direction of the headline. (3) The 2030 base case lies within Eurostat’s range. "
           "(4) The illustrations are close to reproducible, with one error (25% for 34%) and bed and density-rank figures that "
           "differ slightly from Eurostat’s and the World Bank’s. These caveats do not change the substance, which our scale calls "
           "<i>Largely supported</i>; the model behind the projection is unread, which is why confidence is moderate."))
S.append(P("<b>What this verdict does not say.</b> It does not say which projects are needed, that hospital beds or "
           "generation are the right measures, or that any institution has failed. It says that the release’s numbers "
           "mostly hold and point the way its headline says."))
S.append(P("Evidence we are asking for", h2))
S.append(requests_list([
    "PwC’s Summer 2026 Economic Update: definitions, base populations, bed and electricity sources, and migration assumptions.",
    "Planned hospital-bed and generation or interconnection capacity to 2030, from the health ministry and the energy regulator.",
    "A published national benchmark for infrastructure capacity per resident that covers more than beds and electricity.",
]))

# ================================================================== 8
S += [Spacer(1, 6 * mm), SectionHeading(8, "Limitations")]
for l in ["PwC’s report was not readable; where we reproduce its figures we infer its method from the numbers in the press release.",
          "Eurostat’s hospital-bed series flags a break for Malta in 2023; ranks depend on the year used. Electricity for 2025 is provisional and "
          "EU-27 population values for 2026 are provisional.",
          "The World Bank ranking uses 2023 data and land area; the Maldives’ current figure was not tested, so the “fourth” "
          "ranking could hold on newer data.",
          "Beds per 100,000 and electricity imports are two indicators; roads, water, schools and housing were not tested.",
          "Both papers were read as abstracts; neither concerns Malta [5, 6].",
          "The Malta Chamber posted the release as sponsored content; we did not find a separate statement by the Chamber."]:
    S.append(P("• " + l, bul))

S += [Spacer(1, 6 * mm), SectionHeading(None, "References")]
S += references([
    ("1", "PwC Malta, posted by The Malta Chamber (22 Jul 2026). Malta’s rapid population growth creates urgent need to focus on the "
          "country’s infrastructure demands for the future. Sponsored Content.",
     "https://maltachamber.org.mt/maltas-rapid-population-growth-creates-urgent-need-to-focus-on-the-countrys-infrastructure-demands-for-the-future/"),
    ("2", "PwC Malta, posted by Finance Malta (17 Jul 2026). Same title; earliest copy found, read by the CC-099 check.",
     "https://financemalta.org/industry-updates/malta-s-rapid-population-growth-creates-urgent-need-to-focus-on-the-country-s-infrastructure-demands-for-the-future"),
    ("3", "Eurostat. demo_gind, proj_25np, hlth_rs_bds1, nrg_cb_e, demo_r_d3area, demo_pjanind; retrieved 13 Oct 2026 with status flags.",
     "https://ec.europa.eu/eurostat/databrowser/"),
    ("4", "World Bank. Population density (people per sq. km of land area), EN.POP.DNST, 2023; retrieved 13 Oct 2026.",
     "https://data.worldbank.org/indicator/EN.POP.DNST"),
    ("5", "Bagust A., Place M., Posnett J.W. (1999). Dynamics of bed use in accommodating emergency admissions: stochastic "
          "simulation model. <i>BMJ</i> 319(7203):155–158. doi:10.1136/bmj.319.7203.155. (Abstract read.)",
     "https://doi.org/10.1136/bmj.319.7203.155"),
    ("6", "Keilman N. (1998). How accurate are the United Nations world population projections? <i>Population and Development "
          "Review</i> 24:15 (first page as recorded by Crossref). doi:10.2307/2808049. (Abstract read.)", "https://doi.org/10.2307/2808049"),
    ("7", "Miżien. Claim check CC-099: Foreign residents, 31% now, 38% by 2030 (same release).", ""),
    ("8", "Miżien. Data and calculations: data/cc-089/; tools/cc-089-report/calc.py.", ""),
])

S.append(PageBreak())
S += appendix_a("A experiment · B observational study with a control or gradient · C review, guidance or "
                "official statistics · D assertion or anecdote. ◆ marks a source known only second-hand.")
S += [Spacer(1, 5 * mm)]
S += revision_log([("1.0", "13 Oct 2026", "First issue. No right of reply needed (verdict Largely supported).")])

build_report(Report(
    number="089", out=str(FIG / "report.pdf"), kicker="Population and infrastructure",
    title_lines=["Growth outpacing", "infrastructure?"],
    subtitle_lines=["Testing PwC Malta’s population and infrastructure figures",
                    "against Eurostat and the World Bank"],
    quote_lines=["“Infrastructure demands require", "urgent investment.”"], quote_size=16,
    attribution="PwC Malta, Summer 2026 Economic Update release, posted by the Malta Chamber, 22 July 2026.",
    context="Headline: “Malta’s rapid population growth creates urgent need to focus on the country’s infrastructure demands”.",
    verdict="Largely supported", verdict_note="Premises hold; one percentage mislabelled; “urgent” is a judgement",
    footer_lines=["Version 1.0  ·  13 October 2026", "Status: draft · no right of reply needed",
                  "Prepared from public sources, Eurostat and World Bank data.", "Repository: github.com/leandergrech/Mizien"],
    running_head="Population growth and infrastructure – Malta", version="1.0", date="13 October 2026",
    pdf_title="Growth outpacing infrastructure? Claim Check 089",
    pdf_subject="Tests PwC Malta's population and infrastructure figures, as posted by the Malta Chamber",
    story=S))
