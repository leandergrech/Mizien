"""Claim Check 013 report. Run calc.py and figures.py first. Output: out/report.pdf"""
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
      P("In a March 2025 interview with MaltaToday, Planning Authority chief executive Johann Buttigieg was asked "
        "whether approving 91,000 dwellings in a decade was sustainable. He replied: <b>“Had we not issued these "
        "permits, Malta would face the same housing crises as other European countries. This is a supply-and-demand "
        "issue – continuing to issue permits helps keep property prices in check. Stopping them would drive prices "
        "up.”</b> We tested the economics against peer-reviewed research and the Malta data against Eurostat, the "
        "Authority’s own permit series and the 2021 census.", lead)]
S.append(key_points([
    ("The mechanism is well supported.",
     "Peer-reviewed studies in the US and England find that where supply is held back, demand growth shows up as "
     "higher prices rather than more homes. Restricting permits would be expected to push prices up."),
    ("Malta absorbed an exceptional demand shock.",
     "Malta’s population grew 31% between 2015 and 2025; the EU’s grew 2%. Real house prices rose 34% in "
     "Malta (2025 figure provisional) and 25% in the EU. Overcrowding (4.7%) and housing-cost overburden (6.0%) "
     "remain below EU averages."),
    ("But prices were not held in check against Europe.",
     "Real prices still rose faster than the EU average, and the share of people overburdened by housing costs "
     "rose from 1.1% to 2.9% between 2015 and 2022 while the EU’s fell. Eurostat flags a break in Malta’s "
     "series in 2023; since then the rate has held at about 6%. Research also finds that extra supply alone "
     "does little for affordability."),
    ("The counterfactual cannot be proved.",
     "No study estimates what Maltese prices would have been with fewer permits. Over a quarter of dwellings are "
     "not anyone’s main home, so not every approval meets resident demand."),
    ("Verdict: largely supported (moderate confidence).",
     "As a statement about supply and demand, the claim agrees with the evidence. The caveats concern how large the "
     "effect is and the worsening affordability trend, which the statement does not mention."),
]))
S += [Spacer(1, 4 * mm), VerdictMeter(1), Spacer(1, 3 * mm),
      tiles([("87,814", GREEN, "Dwelling units approved 2015–2024 (Planning Authority)"),
             ("+31%", ORANGE, "Malta population growth 2015–2025 (EU +2%)"),
             ("+34%", GREY, "Real house prices 2015–2025, Malta (EU +25%); 2025 provisional"),
             ("6.0%", RED, "People overburdened by housing costs, 2025 (2.9% in 2022, before a series break)")]),
      Spacer(1, 4 * mm),
      up_down("A Malta-specific estimate showing that prices respond strongly to approvals (for example, prices "
              "slowing where and when approvals rise, controlling for demand).",
              "Evidence that most new approvals add to secondary or vacant stock rather than housing for residents, "
              "or that prices rose as fast in places that approved more."),
      Spacer(1, 5 * mm)]
S += toc([("1", "The claim and what we could verify"), ("2", "Method"), ("3", "What the research says"),
          ("4", "What the Malta data show"), ("5", "Where the evidence points different ways"),
          ("6", "Testing the claim"), ("7", "Verdict and requests for evidence"), ("8", "Limitations")])
S.append(PageBreak())

# ================================================================== 1
S.append(SectionHeading(1, "The claim and what we could verify"))
S.append(P("The claim is the chief executive’s answer in a MaltaToday interview by James Debono published on "
           "2 March 2025 [1], which we read in full. The interviewer’s question gave the figure of 91,000 new dwellings "
           "approved in the past decade, including 21,000 on previously undeveloped land; the answer did not repeat it. "
           "The Authority’s own series gives 87,814 units approved in 2015–2024 [2], close to the interviewer’s figure."))
S.append(std_table([
    [C("What was said", cellh), C("Who", cellh), C("Access", cellh)],
    [C("“Had we not issued these permits, Malta would face the same housing crises as other European countries.”"),
     C("Chief executive [1]"), C("Read in full")],
    [C("“This is a supply-and-demand issue – continuing to issue permits helps keep property prices in check. "
       "Stopping them would drive prices up.”"), C("Chief executive [1]"), C("Read in full")],
    [C("91,000 new dwellings approved in the past decade"), C("Interviewer [1]"), C("Read; PA series gives 87,814 [2]")],
], [104 * mm, 34 * mm, 32 * mm]))
S += [Spacer(1, 4 * mm),
      callout([P("SCOPE NOTE", tag),
               P("This check is about prices and the supply argument only. It does not assess the environmental cost of "
                 "the permits, building design, or whether the land used was the right land: those are separate "
                 "questions. In the same interview the chief executive said affordability “is a concern” and proposed "
                 "smaller minimum flat sizes.", small)], bg=AMBER_PALE, bar=AMBER), Spacer(1, 4 * mm)]

# ================================================================== 2
S.append(SectionHeading(2, "Method"))
S.append(P("<b>Question.</b> Does issuing permits help keep prices in check, and is Malta better placed than other "
           "European countries because of it?"))
S.append(P("<b>Evidence.</b> Peer-reviewed literature on housing supply and prices, found through Crossref and "
           "OpenAlex and verified by DOI [5–8]. Eurostat house prices (nominal and deflated), permits, population, "
           "housing-cost overburden and overcrowding for Malta and the EU [3]; the Planning Authority’s series of "
           "approved dwellings [2]; and the NSO 2021 census of dwellings [4]. All numbers are recomputed by "
           "<i>tools/cc-013-report/calc.py</i> from files in <i>data/cc-013/</i>."))
S.append(P("<b>Grades.</b> Peer-reviewed observational studies with controls are grade B; official statistics are "
           "grade C. <b>Verdicts</b> follow the five-point scale in Appendix A."))

# ================================================================== 3
S.append(CondPageBreak(90 * mm))
S.append(SectionHeading(3, "What the research says"))
S.append(P("Economists agree that supply matters for prices; they disagree on how much. Glaeser, Gyourko and Saks "
           "found Manhattan prices far above construction costs and attributed the gap to land-use regulation; in "
           "constrained markets, rising demand led “not to more housing units but to higher prices” [5]. Hilber and "
           "Vermeulen, using 353 English planning authorities over 34 years, found that regulatory constraints make "
           "prices respond more strongly to rising incomes [6]. Saiz showed that supply elasticity depends on both "
           "geography and regulation [7]: both are tight in Malta."))
S.append(P("On the other side, Anenberg and Kung modelled what happens when supply is added and found that rents "
           "respond only weakly, because location and amenities matter more than the number of units; marginal easing "
           "of constraints “alone” is unlikely to cut rent burdens much [8]. The research therefore supports the "
           "direction of the claim (more permits, less upward pressure) but not any particular size of effect."))

# ================================================================== 4
S.append(CondPageBreak(150 * mm))
S.append(SectionHeading(4, "What the Malta data show"))
S.append(fig(FIG / "fig1_permits_prices.png"))
S.append(P("Figure 1. Dwelling units approved each year (bars) with real house prices in Malta and the EU and "
           "Malta’s population, indexed to 2015. Approvals more than tripled after 2015 as population growth "
           "accelerated. Malta’s 2025 house-price index is provisional.", cap))
S.append(fig(FIG / "fig2_affordability.png"))
S.append(P("Figure 2. Housing-cost overburden and overcrowding, Malta and EU-27. Malta remains below the EU on both. "
           "Its overburden rate rose from 1.1% to 2.9% in 2015–2022 while the EU’s fell; Eurostat flags a break "
           "in Malta’s series in 2023, so the step from 2.9% to 6.0% is not a like-for-like change.", cap))
S.append(std_table([
    [C("Indicator", cellh), C("Malta", cellh), C("EU-27", cellh), C("Source", cellh), C("Grade", cellh)],
    [C("Population change 2015–2025"), C("<b>+31%</b>"), C("+2%"), C("Eurostat demo_gind"), grade_tag("C")],
    [C("Real house prices, 2015–2025"), C("+34% (p)"), C("+25%"), C("Eurostat tipsho10"), grade_tag("C")],
    [C("Nominal house prices, 2015–2024"), C("+64%"), C("+53%"), C("Eurostat prc_hpi_a"), grade_tag("C")],
    [C("Housing-cost overburden, 2015 → 2022; 2023 → 2025 (break in Malta’s series in 2023)"), C("1.1% → 2.9%; <b>6.0%</b> → <b>6.0%</b>"), C("11.2% → 8.7%; 8.8% → 7.7%"), C("Eurostat ilc_lvho07a"), grade_tag("C")],
    [C("Overcrowding, 2025"), C("4.7%"), C("16.8%"), C("Eurostat ilc_lvho05a"), grade_tag("C")],
    [C("Dwellings approved 2015–2024"), C("87,814"), C("–"), C("Planning Authority [2]"), grade_tag("C")],
    [C("Dwellings not a main residence, 2021"), C("27.5% (31.8% in 2011)"), C("–"), C("NSO census [4]"), grade_tag("C")],
], [62 * mm, 32 * mm, 30 * mm, 34 * mm, 12 * mm]))
S.append(P("All values in <i>data/cc-013/checks.csv</i>. Real prices are the house price index deflated by "
           "consumer prices (HICP), to 2025; nominal prices are not deflated and run to 2024. (p) Malta’s 2025 "
           "value is provisional.", cap))

# ================================================================== 5
S.append(CondPageBreak(120 * mm))
S.append(SectionHeading(5, "Where the evidence points different ways"))
S.append(contested(
    "Q1  Did permits keep prices in check?", "IN DIRECTION, NOT IN LEVEL", AMBER,
    "Population grew 31% while real prices rose 34%, only 9 points more than the EU with almost no population growth. "
    "In our reading, supply on this scale is a plausible reason prices did not rise much faster. This is our "
    "inference: it is consistent with the research but has not been tested for Malta.",
    "Malta’s real prices still outpaced the EU, and grew fastest in the record-approval years (about 3.8% a year in "
    "years with 9,000+ approvals against 1.7% in other years). Approvals respond to demand, so this does not show "
    "permits raised prices, but it does show they did not hold prices down against Europe.",
    "<b>For this claim:</b> “helps keep prices in check” is consistent with the evidence as a statement about "
    "direction; it cannot be read as a claim that prices are under control."))
S.append(contested(
    "Q2  Would Malta face the same crisis as other European countries?", "PARTLY SUPPORTED NOW; GAP NARROWING", AMBER,
    "Malta’s overcrowding (4.7%) is a quarter of the EU rate and its overburden rate (6.0%) is still below the EU’s "
    "(7.7%).",
    "Malta’s overburden rate rose from 1.1% to 2.9% in 2015–2022 while the EU’s fell. The jump to 6.0% in 2023 "
    "coincides with a break in Eurostat’s series, so it is not a like-for-like change; the rate has held at about "
    "6% since.",
    "<b>For this claim:</b> on today’s indicators Malta is not in a worse position than the EU average, but "
    "the trend is towards it."))
S.append(contested(
    "Q3  Do approvals add homes for residents?", "MOSTLY, NOT ENTIRELY", AMBER,
    "The share of dwellings that are not a main residence fell from 31.8% to 27.5% between 2011 and 2021 [4]: most "
    "new stock was occupied.",
    "81,613 dwellings (27.5%) were secondary, seasonal or vacant in 2021. Approvals are not completions, and "
    "small, investor-oriented units may not match households’ needs.",
    "<b>For this claim:</b> the supply argument holds best for approvals that become homes people live in."))

# ================================================================== 6
S.append(CondPageBreak(110 * mm))
S.append(SectionHeading(6, "Testing the claim"))
verd = lambda t, c: chip(t, c, w=29 * mm)
S.append(std_table([
    [C("Sub-claim", cellh), C("What the evidence shows", cellh), C("Rating", cellh)],
    [C("<b>A.</b> Price is a supply-and-demand issue; more permits help keep prices in check"),
     C("Supported in direction by peer-reviewed studies [5–7]; effect size uncertain and possibly small for "
       "affordability [8]."), verd("LARGELY SUPPORTED", LG)],
    [C("<b>B.</b> Stopping permits would drive prices up"), C("Consistent with the same research; not tested for "
       "Malta directly."), verd("LARGELY SUPPORTED", LG)],
    [C("<b>C.</b> Without the permits Malta would face the same crises as other European countries"),
     C("Counterfactual. Malta is below the EU on overcrowding and overburden today, but its prices grew faster and "
       "overburden is rising."), verd("NOT SHOWN", GREY)],
    [C("<b>D.</b> 91,000 dwellings in a decade (interviewer)"), C("87,814 approved 2015–2024 [2]."),
     verd("CLOSE", GREENC)],
], [52 * mm, 88 * mm, 30 * mm], valign="MIDDLE"))

# ================================================================== 7
S += [Spacer(1, 6 * mm), SectionHeading(7, "Verdict and requests for evidence"),
      verdict_box("Largely supported", "Agrees with the research on supply and prices; the size of the effect is "
                  "unproven and affordability is worsening. Confidence: moderate."), Spacer(1, 4 * mm)]
S.append(P("<b>Why.</b> (1) The research consistently finds that restricting housing supply raises prices, so issuing "
           "permits plausibly restrains them. (2) Malta absorbed population growth fifteen times the EU’s with real "
           "price growth only moderately above the EU average, and remains below the EU on overcrowding and cost "
           "overburden. (3) The statement does not show how much permits restrain prices, and affordability worsened "
           "between 2015 and 2022 on Eurostat’s comparable series. These caveats limit the claim but do not reverse it, which our scale calls "
           "<i>Largely supported</i>."))
S.append(P("<b>What this verdict does not say.</b> It does not say that more permits are good overall, that the "
           "land, design or environmental costs are justified, or that prices are affordable. It says that, as an "
           "economic statement about supply and prices, the claim agrees with the evidence."))
S.append(P("Evidence we are asking for", h2))
S.append(requests_list([
    "Completions (not only approvals) by year and type, and how many new units become main residences.",
    "Any Malta-specific estimate of how prices respond to approvals, controlling for demand.",
    "The source and definition of the 91,000 figure used in the interview question.",
]))

# ================================================================== 8
S += [Spacer(1, 6 * mm), SectionHeading(8, "Limitations")]
for l in ["The research cited is from the US and England; no peer-reviewed estimate of supply elasticity for Malta was found.",
          "Approvals are not completions; we did not find a completions series.",
          "Malta’s overburden rate jumps between 2022 and 2023, the year Eurostat flags a break in its series; we "
          "compare only within 2015–2022 and 2023–2025.",
          "National averages hide differences between localities, tenures and income groups.",
          "Peer-reviewed papers were read as abstracts; findings used are those stated in the abstracts."]:
    S.append(P("• " + l, bul))

S += [Spacer(1, 6 * mm), SectionHeading(None, "References")]
S += references([
    ("1", "Debono J. (2 Mar 2025). Johann Buttigieg: ‘Issuing permits helps keep property prices in check’. "
          "<i>MaltaToday</i>, interview.",
     "https://www.maltatoday.com.mt/news/interview/133858/johann_buttigieg_issuing_permits_helps_keep_property_prices_in_check_"),
    ("2", "Planning Authority (2026). Approved Dwelling Units for 2007–2025.", "https://www.pa.org.mt/file.aspx?f=37489"),
    ("3", "Eurostat. prc_hpi_a, tipsho10, sts_cobp_a, demo_gind, ilc_lvho07a, ilc_lvho05a; retrieved 3 Oct 2026 "
          "(status flags checked 5 Oct 2026).",
     "https://ec.europa.eu/eurostat/databrowser/"),
    ("4", "National Statistics Office (2023). Census of Population and Housing 2021, Final Report vol. 2: Dwelling "
          "Characteristics.", "https://nso.gov.mt/wp-content/uploads/Census-2021-Volume-2.pdf"),
    ("5", "Glaeser E.L., Gyourko J., Saks R. (2005). Why is Manhattan so expensive? Regulation and the rise in housing "
          "prices. <i>Journal of Law and Economics</i> 48(2):331–369. doi:10.1086/429979. (Abstract read.)",
     "https://doi.org/10.1086/429979"),
    ("6", "Hilber C.A.L., Vermeulen W. (2016). The impact of supply constraints on house prices in England. "
          "<i>Economic Journal</i> 126(591):358–405. doi:10.1111/ecoj.12213. (Abstract read.)",
     "https://doi.org/10.1111/ecoj.12213"),
    ("7", "Saiz A. (2010). The geographic determinants of housing supply. <i>Quarterly Journal of Economics</i> "
          "125(3):1253–1296. doi:10.1162/qjec.2010.125.3.1253. (Abstract read.)",
     "https://doi.org/10.1162/qjec.2010.125.3.1253"),
    ("8", "Anenberg E., Kung E. (2020). Can more housing supply solve the affordability crisis? Evidence from a "
          "neighborhood choice model. <i>Regional Science and Urban Economics</i> 80:103363. "
          "doi:10.1016/j.regsciurbeco.2018.04.012. (Abstract read, working-paper version.)",
     "https://doi.org/10.1016/j.regsciurbeco.2018.04.012"),
    ("9", "MiŻien. Data and calculations: data/cc-013/; tools/cc-013-report/calc.py.", ""),
])

S.append(PageBreak())
S += appendix_a("A experiment · B observational study with a control or gradient · C review, guidance or "
                "official statistics · D assertion or anecdote. ◆ marks a source known only second-hand.")
S += [Spacer(1, 5 * mm)]
S += revision_log([("1.0", "3 Oct 2026", "First issue. Right of reply to the Planning Authority not yet sent."),
                   ("1.1", "5 Oct 2026",
                    "Corrections. (1) Housing-cost overburden: Eurostat flags a break in Malta’s series in 2023, "
                    "so “1.1% (2015) → 6.0% (2025)” and “more than fivefold” → like-for-like runs “1.1% → 2.9% "
                    "(2015–2022)” and “6.0% → 5.9% → 6.0% (2023–2025)” (TL;DR, tiles, Figure 2 caption, Section 4 "
                    "table, Q2, Section 7, Limitations, flyer). (2) Real house prices 2015–2025 (+34% Malta, +25% "
                    "EU) now written to checks.csv by calc.py, which previously held only 2015–2024 (+26%, +21%); "
                    "Malta’s 2025 value marked provisional (TL;DR, tiles, Figure 1 caption, table “+34%” → “+34% (p)”); "
                    "table note now states each price row’s basis and period (real, HICP-deflated, to 2025; "
                    "nominal to 2024). (3) data/cc-013/eurostat_housing.csv: the second sts_cobp_a series each year "
                    "relabelled as m² of useful floor area (it had the dwellings label); Eurostat flags recorded. "
                    "(4) Q1: “the most plausible reason … the research supports this” → stated as our inference, "
                    "not tested for Malta. Verdict and confidence unchanged.")])

build_report(Report(
    number="013", out=str(FIG / "report.pdf"), kicker="Housing and planning",
    title_lines=["Do permits keep", "prices in", "check?"],
    subtitle_lines=["Testing a public claim about housing supply and prices in Malta",
                    "against research, Eurostat and the census"],
    quote_lines=["“Continuing to issue permits helps keep", "property prices in check.”"], quote_size=16,
    attribution="Johann Buttigieg, Planning Authority CEO, MaltaToday interview, 2 March 2025.",
    context="Answering a question on 91,000 dwellings approved in a decade.",
    verdict="Largely supported", verdict_note="Right in direction; the size of the effect is unproven",
    footer_lines=["Version 1.1  ·  5 October 2026", "Status: draft (right of reply: Planning Authority)",
                  "Prepared from public sources, Eurostat and NSO data.", "Repository: github.com/leandergrech/Mizien"],
    running_head="Permits and property prices – Malta", version="1.1", date="5 October 2026",
    pdf_title="Do permits keep prices in check? Claim Check 013",
    pdf_subject="Tests the Planning Authority CEO's claim that issuing permits keeps property prices in check",
    story=S))
