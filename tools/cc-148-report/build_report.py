"""Claim Check 148 report. Run calc.py and figures.py first. Output: out/report.pdf"""
import json
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import *  # noqa: E402,F401

FIG = HERE / "out"
R = json.load(open(HERE.parents[1] / "data" / "cc-148" / "results.json"))
S = []
LG = colors.HexColor("#8DB36B")
mt, fi = R["q1_2025"]["MT"], R["q1_2025"]["FI"]

S += [SectionHeading(None, "TL;DR"), Spacer(1, 1 * mm),
      P("On 14 August 2025 Eurostat published its first estimate of EU greenhouse-gas emissions for the first quarter "
        "of 2025. It wrote: <b>“The largest reductions in greenhouse gases were estimated for Malta (-6.2%), Finland "
        "(-4.4%) and Denmark (-4.3%).”</b> We checked that wording against the news item itself and against Eurostat’s "
        "current quarterly dataset. The statement is an accurate account of the August 2025 estimate. In the data as "
        "revised since, Malta’s fall is 5.0% and ranks second, behind Finland (10.1%); and the quarter says little "
        "about the trend, because Malta’s emissions rose in the other three quarters of 2025.", lead)]
S.append(key_points([
    ("Eurostat said it, in these words.",
     "The news item of 14 August 2025 names Malta first (−6.2%), reports an EU rise of 3.4% to 900 million tonnes "
     "CO₂-eq, and counts 20 countries up and 7 down [1]."),
    ("The estimate has since been revised.",
     f"The current dataset gives Malta {mt:+.1f}% and Finland {fi:+.1f}%, so Malta now ranks 2nd of 27 [2]. "
     "The EU rise is now +4.2% (903.7 Mt). The 20-up, 7-down split is unchanged."),
    ("One quarter is not a trend.",
     f"Summing four quarters, Malta’s 2025 emissions were {R['mt_annual_yoy']['2025']:+.1f}% on 2024 (EU "
     f"{R['eu_annual_yoy']['2025']:+.1f}%); the next three quarters were up 1.1%, 5.5% and 1.6%, and Q1 2026 is "
     f"{R['q1_2026_mt']:+.1f}% [2]."),
    ("The base was unusually high.",
     "Malta’s Q1 2025 level (1.53 Mt) is still 87% above Q1 2023 (0.82 Mt) in this series; the 2025 fall followed a "
     "large 2024 rise. We did not investigate the cause."),
    ("Verdict: largely supported (moderate confidence).",
     "As a report of what Eurostat estimated, accurate. The caveats are the later revision and what one quarter can "
     "show."),
]))
S += [Spacer(1, 2.5 * mm), VerdictMeter(1), Spacer(1, 3 * mm),
      tiles([("−6.2%", GREENC, "Malta, Q1 2025 on Q1 2024, Eurostat’s Aug 2025 estimate (largest fall)"),
             (f"{mt:+.1f}%", ORANGE, "Malta in the current dataset (2nd of 27, behind Finland " + f"{fi:+.1f}%)"),
             (f"{R['mt_annual_yoy']['2025']:+.1f}%", RED, "Malta, full-year 2025 on 2024 (sum of four quarters)"),
             (f"{R['q1_2026_mt']:+.1f}%", RED, "Malta, Q1 2026 on Q1 2025 (latest quarter)")]),
      Spacer(1, 4 * mm),
      up_down("A later Eurostat vintage restoring Malta to first place at about −6%, or showing the August 2025 figures "
              "were not revised.",
              "Eurostat’s published vintage history (not retrievable by us) showing the August 2025 ranking was not "
              "what Eurostat itself reported, or a Maltese revision that removes the Q1 2025 fall."),
      Spacer(1, 3 * mm)]
S += toc([("1", "The claim and what we could verify"), ("2", "Method"), ("3", "What Eurostat published and what the data show now"),
          ("4", "Where the evidence points different ways"), ("5", "Testing the claim"),
          ("6", "Verdict and requests for evidence"), ("7", "Limitations")])
S.append(PageBreak())

S.append(SectionHeading(1, "The claim and what we could verify"))
S.append(P("The claim record locates this statement through MaltaDaily (19 August 2025) [3], whose headline says Malta "
           "“tops” EU reductions and which also quotes the Minister for the Environment. The speaker we rate is "
           "Eurostat; the Minister’s comment and the headline are not rated. We read Eurostat’s own news item [1], "
           "which carries the wording below."))
S.append(std_table([
    [C("What was said", cellh), C("Who", cellh), C("Access", cellh)],
    [C("“The largest reductions in greenhouse gases were estimated for Malta (-6.2%), Finland (-4.4%) and Denmark (-4.3%).”"),
     C("Eurostat news item, 14 Aug 2025 [1]"), C("Read in full")],
    [C("“…a 3.4% increase compared with the same quarter of 2024 (871 million tonnes of CO2-eq)”; EU emissions "
       "“estimated at 900 million tonnes”"), C("Eurostat [1]"), C("Read in full")],
    [C("“…increases in greenhouse gas emissions were estimated for 20 EU countries, while decreases were estimated for "
       "the remaining 7 countries.”"), C("Eurostat [1]"), C("Read in full")],
], [104 * mm, 40 * mm, 26 * mm]))
S += [Spacer(1, 4 * mm),
      callout([P("SCOPE NOTE", tag),
               P("The claim record’s phrase “sharpest drop” is MaltaDaily’s; Eurostat’s wording is “largest reductions”, "
                 "and every figure is an <i>estimate</i> (Eurostat, non-seasonally adjusted, same quarter of the previous "
                 "year). Eurostat’s measure counts international aviation and shipping in each country’s total, which "
                 "differs from United Nations reporting rules [1]. This check does not assess Malta’s climate policy.",
                 small)], bg=AMBER_PALE, bar=AMBER), Spacer(1, 4 * mm)]

S.append(SectionHeading(2, "Method"))
S.append(P("<b>Question.</b> Was the statement an accurate report of Eurostat’s estimate, and does the quarterly "
           "dataset as it stands today still support it?"))
S.append(P("<b>Evidence.</b> The news item [1] and Eurostat’s quarterly air-emissions accounts for greenhouse gases "
           "(<i>env_ac_aigg_q</i>, non-seasonally adjusted, thousand tonnes CO₂-eq) for all 27 Member States and the EU "
           "[2], downloaded on 2 November 2026 (dataset last updated 14 August 2026). All figures are recomputed by "
           "<i>tools/cc-148-report/calc.py</i> from <i>data/cc-148/q_all_nsa.json</i>; results are in "
           "<i>data/cc-148/checks.csv</i>. We could not retrieve the dataset as it stood in August 2025, so we cannot "
           "say which revision moved Malta’s and Finland’s figures. <b>Grades:</b> official statistics are grade C. "
           "<b>Verdicts</b> follow the five-point scale in Appendix A."))

S.append(CondPageBreak(150 * mm))
S.append(SectionHeading(3, "What Eurostat published and what the data show now"))
S.append(fig(FIG / "fig1_member_states.png"))
S.append(P(f"Figure 1. Change in greenhouse-gas emissions, Q1 2025 on Q1 2024, in the current dataset. Malta "
           f"({mt:+.1f}%) is second behind Finland ({fi:+.1f}%). Seven Member States fell and 20 rose, as Eurostat "
           "reported in August 2025.", cap))
S.append(std_table([
    [C("Quantity", cellh), C("Eurostat news item, 14 Aug 2025 [1]", cellh), C("Current dataset [2]", cellh), C("Grade", cellh)],
    [C("Malta, Q1 2025 on Q1 2024"), C("<b>−6.2%</b>"), C(f"<b>{mt:+.1f}%</b> (1.614 → 1.533 Mt)"), grade_tag("C")],
    [C("Finland"), C("−4.4%"), C(f"{fi:+.1f}%"), grade_tag("C")],
    [C("Denmark"), C("−4.3%"), C(f"{R['q1_2025']['DK']:+.1f}%"), grade_tag("C")],
    [C("Malta’s rank for the largest fall"), C("1st"), C("2nd"), grade_tag("C")],
    [C("EU emissions, Q1 2025"), C("900 Mt, +3.4%"), C(f"{R['eu_q1_2025_mt']} Mt, {R['eu_q1_2025_pct']:+.1f}%"), grade_tag("C")],
    [C("Member States up / down"), C("20 / 7"), C(f"{R['rose']} / {R['fell']}"), grade_tag("C")],
], [58 * mm, 46 * mm, 54 * mm, 12 * mm]))
S.append(P("Values in <i>data/cc-148/checks.csv</i>. The news item’s figures were read from the item; current-dataset "
           "figures are recomputed from the downloaded file. Every quarterly value in the dataset carries Eurostat flag "
           "“i”.", cap))
S.append(KeepTogether([P("Malta across the year", h2), fig(FIG / "fig2_malta_quarters.png"),
    P("Figure 2. Malta’s quarterly emissions, with the change on the same quarter a year earlier. Only Q4 2024 (−1.3%) "
      "and Q1 2025 (−5.0%, highlighted) are falls on the year before.", cap)]))
S.append(P(f"Over the full years, Malta’s four-quarter total was {R['mt_annual']['2023']/1000:.2f} Mt in 2023, "
           f"{R['mt_annual']['2024']/1000:.2f} Mt in 2024 ({R['mt_annual_yoy']['2024']:+.1f}%) and "
           f"{R['mt_annual']['2025']/1000:.2f} Mt in 2025 ({R['mt_annual_yoy']['2025']:+.1f}%); the EU’s changed "
           f"{R['eu_annual_yoy']['2024']:+.1f}% and {R['eu_annual_yoy']['2025']:+.1f}% [2]. Malta’s emissions in this "
           "series therefore rose strongly in 2024 and were roughly flat in 2025, with the Q1 fall offset later in the "
           "year. We did not investigate why the 2024 level is so much higher than 2023; the dataset gives no reason."))

S.append(CondPageBreak(100 * mm))
S.append(SectionHeading(4, "Where the evidence points different ways"))
S.append(contested(
    "Q1  Did Malta have the largest fall in Q1 2025?", "TRUE AT RELEASE; NOT NOW", AMBER,
    "Eurostat’s news item names Malta first at −6.2% [1]. A reader checking the statement against the release finds it "
    "exact.",
    f"The current dataset gives Malta {mt:+.1f}% and Finland {fi:+.1f}% [2], so Malta is second. Eurostat’s methodology "
    "note says the figures are estimates [1], so later revision is possible.",
    "<b>For this claim:</b> an accurate report of an early estimate; the ranking did not survive revision. The size of "
    "Malta’s fall is also smaller (−5.0%)."))
S.append(contested(
    "Q2  Does a one-quarter fall say anything about the trend?", "VERY LITTLE", AMBER,
    "Malta’s emissions fell year on year in Q1 2025 while its economy grew [1], and the fall is still present in "
    "the current dataset [2].",
    f"The next three quarters rose year on year, the full year was {R['mt_annual_yoy']['2025']:+.1f}%, and Q1 2026 "
    f"is {R['q1_2026_mt']:+.1f}% [2]. The Q1 2025 level is far above Q1 2023. One quarter, compared with a "
    "year-earlier quarter that was itself unusually high, is a weak basis for “tops the EU”.",
    "<b>For this claim:</b> Eurostat did not claim a trend. MaltaDaily’s headline (“tops EU reductions”) and any use "
    "of the figure as evidence of progress go beyond the news item; they are not rated here."))

S.append(CondPageBreak(90 * mm))
S.append(SectionHeading(5, "Testing the claim"))
verd = lambda t, c: chip(t, c, w=29 * mm)
S.append(std_table([
    [C("Sub-claim (Eurostat’s wording)", cellh), C("What the evidence shows", cellh), C("Rating", cellh)],
    [C("<b>A.</b> Malta’s emissions fell, estimated −6.2% in Q1 2025 on Q1 2024"),
     C(f"Matches the news item [1]. Current data: {mt:+.1f}% [2]."), verd("LARGELY SUPPORTED", LG)],
    [C("<b>B.</b> This was the largest reduction among EU countries"),
     C(f"Largest in the August 2025 estimate [1]; second behind Finland ({fi:+.1f}%) in the current data [2]."),
     verd("REVISED", ORANGE)],
    [C("<b>C.</b> EU emissions rose 3.4% to about 900 Mt CO₂-eq"),
     C(f"Matches the news item [1]; now {R['eu_q1_2025_pct']:+.1f}%, {R['eu_q1_2025_mt']} Mt [2]."),
     verd("LARGELY SUPPORTED", LG)],
    [C("<b>D.</b> Increases in 20 countries, decreases in 7"),
     C(f"Matches the news item [1] and the current data ({R['rose']} up, {R['fell']} down) [2]."),
     verd("SUPPORTED", GREENC)],
], [56 * mm, 84 * mm, 30 * mm], valign="MIDDLE"))

S += [Spacer(1, 6 * mm), SectionHeading(6, "Verdict and requests for evidence"),
      verdict_box("Largely supported", "An accurate report of Eurostat’s estimate; Malta’s rank and figure were later "
                  "revised, and one quarter is not a trend. Confidence: moderate."), Spacer(1, 4 * mm)]
S.append(P("<b>Why.</b> (1) Every figure in the statement is in Eurostat’s own news item [1]. (2) The 20-up, 7-down "
           "split and the existence of a Maltese fall hold in the current data [2]. (3) The ranking (first) and the size "
           "(−6.2%) do not: the current dataset has Malta at −5.0% and second. That is a caveat to a statement of an "
           "early estimate, not a reversal, which our scale calls <i>Largely supported</i>. Confidence is moderate "
           "because we could not retrieve the August 2025 vintage and so cannot say what moved the figures."))
S.append(P("<b>What this verdict does not say.</b> It does not say that Malta’s emissions are falling: over 2025 as a "
           "whole they were flat (+1.0%) and Q1 2026 is up 4.2%. Other checks look at annual emissions (CC-026, CC-146)."))
S.append(P("Evidence we are asking for", h2))
S.append(requests_list([
    "Eurostat’s record of earlier vintages of env_ac_aigg_q, to show when and why Malta’s and Finland’s Q1 2025 figures changed.",
    "An explanation, from the National Statistics Office or Eurostat, of the step up in Malta’s quarterly series between 2023 and 2024.",
]))

S += [Spacer(1, 6 * mm), SectionHeading(7, "Limitations")]
for l in ["We could not retrieve the dataset as it stood in August 2025; revisions are described only by comparing the news item with today’s data.",
          "Quarterly figures are Eurostat estimates, not national inventories; they include international aviation and "
          "shipping, which weigh heavily in a small island economy, and differ from United Nations reporting [1].",
          "Annual totals are sums of the four non-seasonally adjusted quarters in the dataset, not Eurostat’s annual accounts.",
          "We did not test sectors (electricity, aviation, shipping) behind Malta’s quarterly movements.",
          "The Minister’s reported comment and MaltaDaily’s headline are not rated."]:
    S.append(P("• " + l, bul))

S += [Spacer(1, 6 * mm), SectionHeading(None, "References")]
S += references([
    ("1", "Eurostat (14 Aug 2025). EU economy greenhouse gas emissions: +3.4% in Q1 2025. News article.",
     "https://ec.europa.eu/eurostat/web/products-eurostat-news/w/ddn-20250814-1"),
    ("2", "Eurostat. Air emissions accounts for greenhouse gases by NACE Rev. 2 activity – quarterly data (env_ac_aigg_q); "
          "downloaded 2 Nov 2026, dataset updated 14 Aug 2026.",
     "https://ec.europa.eu/eurostat/databrowser/view/env_ac_aigg_q"),
    ("3", "MaltaDaily (19 Aug 2025). Malta tops EU greenhouse gas emission reduction charts in first quarter of 2025. "
          "Locates the claim; not evidence.",
     "https://maltadaily.mt/articles/malta-tops-eu-greenhouse-gas-emission-reductions-charts-in-first-quarter-of-2025"),
    ("4", "Miżien. Data and calculations: data/cc-148/; tools/cc-148-report/calc.py.", ""),
])

S.append(PageBreak())
S += appendix_a("A experiment · B observational study with a control or gradient · C review, guidance or "
                "official statistics · D assertion or anecdote. ◆ marks a source known only second-hand.")
S += [Spacer(1, 5 * mm)]
S += revision_log([("1.0", "2 Nov 2026", "First issue. No right of reply needed (verdict Largely supported).")])

build_report(Report(
    number="148", out=str(FIG / "report.pdf"), kicker="Climate and energy",
    title_lines=["Did Malta cut", "emissions most", "in Q1 2025?"],
    subtitle_lines=["Testing a Eurostat statement on quarterly greenhouse-gas emissions",
                    "against Eurostat’s revised data"],
    quote_lines=["“The largest reductions in greenhouse gases", "were estimated for Malta (-6.2%).”"], quote_size=16,
    attribution="Eurostat, news item, 14 August 2025.",
    context="First estimate of Q1 2025 emissions, same quarter of 2024 as base.",
    verdict="Largely supported", verdict_note="Accurate at release; later revised, and one quarter is not a trend",
    footer_lines=["Version 1.0  ·  2 November 2026", "Status: draft",
                  "Prepared from public sources and Eurostat data.", "Repository: github.com/leandergrech/Mizien"],
    running_head="Emissions in Q1 2025 – Malta", version="1.0", date="2 November 2026",
    pdf_title="Did Malta cut emissions most in Q1 2025? Claim Check 148",
    pdf_subject="Tests Eurostat's statement that Malta had the largest fall in greenhouse-gas emissions in Q1 2025",
    story=S))
