"""Claim Check 106 report. Run calc.py and figures.py first. Output: out/report.pdf"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import *  # noqa: E402,F401

FIG = HERE / "out"
LG = colors.HexColor("#8DB36B")
S = []
S += [SectionHeading(None, "TL;DR"), Spacer(1, 1 * mm),
      P("On its page for the LIFE Arċipelagu Garnija project, BirdLife Malta writes that the Yelkouan shearwater "
        "(<i>Garnija</i>) <b>“Malta’s population is estimated to be around 1,600 – 1,800 pairs, constituting "
        "approximately 10% of the global population.”</b> We compared both numbers with the regulator’s estimate and "
        "the published global estimates.", lead)]
S.append(key_points([
    ("Malta’s count is plausible but older than the regulator’s.",
     "The Environment and Resources Authority’s Species Action Plan 2022–2030 gives 1,795–2,635 breeding pairs, "
     "overlapping and above BirdLife Malta’s 1,600–1,800. The BirdLife page is undated; its project ran 2016–2020."),
    ("The global population is poorly known.",
     "A peer-reviewed review (Bourgeois & Vidal 2008, <i>Oryx</i>) put it at 11,355–54,524 pairs, adding that most "
     "censuses are probably overestimates. The figure most often quoted today is 21,000–36,000 pairs (CIESM guide ◆)."),
    ("“About 10%” is at the top of the range.",
     "With BirdLife Malta’s own count and 21,000–36,000 global pairs, Malta’s share is 4.4–8.6% (central 6%). With "
     "the regulator’s count it is 5.0–12.5% (central 7.8%). The regulator also says “around 10%”."),
    ("Verdict: largely supported (moderate confidence).",
     "Malta holds an internationally important share of a vulnerable seabird, which is the point of the sentence. "
     "The precise share cannot be pinned down, and the central estimates are closer to 6–8% than 10%."),
]))
S += [Spacer(1, 2.5 * mm), VerdictMeter(1), Spacer(1, 3 * mm),
      tiles([("1,600–1,800", GREEN, "Breeding pairs in Malta, BirdLife Malta (undated)"),
             ("1,795–2,635", GREEN, "Breeding pairs in Malta, ERA Species Action Plan 2022–2030"),
             ("4–13%", AMBER, "Malta’s share with either count and 21,000–36,000 global pairs"),
             ("6–8%", GREY, "Central estimates of the share (claim: about 10%)")]),
      Spacer(1, 4 * mm),
      up_down("A current, sourced global estimate under about 20,000 pairs, or a Maltese count near the top of the "
              "regulator’s range, either of which would put Malta at about 10%.",
              "A current global estimate well above 36,000 pairs, or a new Maltese census below 1,600 pairs; then "
              "“about 10%” would overstate Malta’s share."),
      Spacer(1, 3 * mm)]
S += toc([("1", "The claim and what we could verify"), ("2", "Method"), ("3", "What the evidence shows"),
          ("4", "Where the evidence points different ways"), ("5", "Testing the claim"),
          ("6", "Verdict and requests for evidence"), ("7", "Limitations")])
S.append(PageBreak())

S.append(SectionHeading(1, "The claim and what we could verify"))
S.append(P("The sentence is on BirdLife Malta’s page for LIFE Arċipelagu Garnija (LIFE14 NAT/MT/000991, 2016–2020) "
           "[1], read on 5 October 2026; the page carries no date. The same text appears on the LIFE PanPuffinus "
           "project’s species page. The European Commission’s LIFE project page [2] describes the project’s aims "
           "(to increase breeding pairs by about 10% and reproductive output by 25%) but gives no population total."))
S.append(std_table([
    [C("Source", cellh), C("What it says", cellh), C("Our access", cellh), C("Status", cellh)],
    [C("<b>BirdLife Malta</b>, LIFE Arċipelagu Garnija page [1]"),
     C("“Malta’s population is estimated to be around 1,600 – 1,800 pairs, constituting approximately 10% of the "
       "global population.”"), C("Read, 5 Oct 2026."), C("<b>The claim</b>")],
    [C("<b>ERA</b>, Species Action Plan 2022–2030 page [3]"),
     C("“around 10% of the global breeding population … an estimated population of 1,795–2,635 breeding pairs”."),
     C("Internet Archive copy, 8 Aug 2025 (live site 403)."), C("<b>Regulator</b>")],
    [C("<b>Bourgeois & Vidal</b> (2008), <i>Oryx</i> [4]"), C("Global population 11,355–54,524 pairs; probably "
       "overestimated."), C("Full text read (free to read)."), C("<b>Peer-reviewed</b>")],
    [C("<b>CIESM</b> seabird guide [5]"), C("Global 21,000–36,000 pairs; 46,000–92,000 individuals."),
     C("Read; no source given ◆."), C("Context")],
], [38 * mm, 74 * mm, 36 * mm, 22 * mm]))

S += [Spacer(1, 4 * mm), SectionHeading(2, "Method")]
S.append(P("<b>Question.</b> Is Malta’s population about 1,600–1,800 pairs, and is that about 10% of the world’s?"))
S.append(P("<b>Evidence.</b> We searched the peer-reviewed literature (OpenAlex, Crossref) and official sources for "
           "Maltese and global estimates, recorded them in <i>data/cc-106/population_estimates.csv</i>, and computed "
           "Malta’s share for each combination (<i>tools/cc-106-report/calc.py</i>): the lowest Maltese estimate over the "
           "highest global one, the reverse, and the ratio of midpoints. The IUCN Red List and BirdLife International "
           "data pages refused automated access, and we could not query the EU Birds Directive (Article 12) reports "
           "directly, so the current official global estimate is known to us only through the CIESM guide."))
S.append(P("<b>Grades.</b> Bourgeois & Vidal (2008): C (review). ERA plan: C (official). CIESM guide: C, second-hand. "
           "<b>Verdicts</b> follow the five-point scale in Appendix A."))

S.append(CondPageBreak(140 * mm))
S.append(SectionHeading(3, "What the evidence shows"))
S.append(KeepTogether([fig(FIG / "fig1_share.png", width=CW * 0.98),
    P("Figure 1. Malta’s share of the world’s Yelkouan shearwater breeding pairs under each pair of estimates. "
      "Green: with the 21,000–36,000 global estimate.", cap)]))
S.append(P("With the counts BirdLife Malta states, Malta’s share cannot exceed 8.6% unless the global population is "
           "below about 21,000 pairs. With the regulator’s newer count, 10% falls inside the range. The 2008 review’s "
           "range is so wide that it supports anything from 3% to 23%. A study of the largest colony, Tavolara in "
           "Sardinia, estimates it holds more than half of the world population (Pezzo et al. 2021) [6]."))

S.append(CondPageBreak(80 * mm))
S.append(SectionHeading(4, "Where the evidence points different ways"))
S.append(contested("Is “approximately 10%” fair?", "AT THE TOP OF THE RANGE", AMBER,
                   "The regulator uses the same figure with a higher Maltese count, and 10% lies inside the range for "
                   "that count (5–12.5%). The global total is uncertain enough that 10% cannot be ruled out.",
                   "The page’s own count, with the most-quoted global estimate, gives 4.4–8.6%. Central estimates are "
                   "6–8%. No source we found gives a calculation behind “10%”.",
                   "The share is of the right order and Malta’s population is internationally important; “about 10%” "
                   "rounds up. A safer wording would be “roughly 5–10%”.", label_a="FOR", label_b="AGAINST"))

S.append(CondPageBreak(110 * mm))
S.append(SectionHeading(5, "Testing the claim"))
verd = lambda t, c: chip(t, c, w=29 * mm)
S.append(std_table([
    [C("Sub-claim", cellh), C("Said by", cellh), C("What the evidence shows", cellh), C("Rating", cellh)],
    [C("<b>A.</b> Malta’s population is around 1,600–1,800 pairs"), C("BirdLife Malta [1]"),
     C("Overlaps the regulator’s 1,795–2,635 pairs (2022–2030 plan); the page is undated and its count is the lower."),
     verd("PLAUSIBLE, DATED", LG)],
    [C("<b>B.</b> …approximately 10% of the global population"), C("BirdLife Malta [1]"),
     C("4.4–8.6% with the page’s own count; 5.0–12.5% with the regulator’s; central 6–8%. Global total poorly known."),
     verd("UPPER END OF RANGE", AMBER)],
], [42 * mm, 18 * mm, 76 * mm, 34 * mm], valign="MIDDLE"))

S += [Spacer(1, 6 * mm), SectionHeading(6, "Verdict and requests for evidence"),
      verdict_box("Largely supported", "Malta holds an important share; “about 10%” rounds up a share closer to "
                  "6–8%. Confidence: moderate."), Spacer(1, 4 * mm)]
S.append(P("<b>Why.</b> Both numbers are of the right order and consistent with official and scientific sources, "
           "but the share is at the upper end of what the estimates allow and the global total is poorly known. "
           "Confidence is moderate because we could not read the current IUCN and Article 12 figures directly. "
           "<b>What this verdict does not say.</b> It does not question the species’ conservation need or BirdLife "
           "Malta’s conservation work; it tests a population share."))
S.append(P("Evidence we are asking for", h2))
S.append(requests_list([
    "From BirdLife Malta: the year and source of the 1,600–1,800 pairs, and the global figure behind “10%”.",
    "From ERA: the method behind 1,795–2,635 pairs and Malta’s latest Article 12 report figures.",
]))
S += [Spacer(1, 4 * mm),
      callout([P("RIGHT OF REPLY", tag), P("Not needed for this verdict (maintainer rule of 5 October 2026).", small)],
              bg=AMBER_PALE, bar=AMBER)]
S += [Spacer(1, 6 * mm), SectionHeading(7, "Limitations")]
for l in ["The IUCN Red List and BirdLife International datazone refused automated access; the 21,000–36,000 figure "
          "is from the CIESM guide, which gives no source (◆).",
          "Seabird colonies in cliffs and caves are hard to census; all estimates are ranges with wide uncertainty.",
          "The ERA plan page was read from an Internet Archive copy; the plan document itself was not read."]:
    S.append(P("• " + l, bul))
S += [Spacer(1, 6 * mm), SectionHeading(None, "References")]
S += references([
    ("1", "BirdLife Malta (undated). LIFE Arċipelagu Garnija. Read 5 Oct 2026.", "https://birdlifemalta.org/arcipelagugarnija/"),
    ("2", "European Commission, CINEA. LIFE14 NAT/MT/000991 LIFE Arċipelagu Garnija, project page.",
     "https://webgate.ec.europa.eu/life/publicWebsite/project/LIFE14-NAT-MT-000991/life-arcipelagu-garnija---securing-the-maltese-islands-for-the-yelkouan-shearwater-puffinus-yelkouan"),
    ("3", "Environment and Resources Authority. Malta Yelkouan Shearwater Species Action Plan 2022–2030 (page). Internet "
          "Archive copy of 8 Aug 2025.", "https://era.org.mt/malta-yelkouan-shearwater-species-ap-2022-2030/"),
    ("4", "Bourgeois K. & Vidal E. (2008). The endemic Mediterranean yelkouan shearwater <i>Puffinus yelkouan</i>: "
          "distribution, threats and a plea for more data. <i>Oryx</i> 42(2):187–194. doi:10.1017/S0030605308006467.",
     "https://doi.org/10.1017/S0030605308006467"),
    ("5", "CIESM. Mediterranean seabird guide: Yelkouan shearwater. ◆", "https://ciesm.org/seabird-guide/yelkouan-shearwater/"),
    ("6", "Pezzo F. et al. (2021). Productivity changes in the Mediterranean Sea drive foraging movements of yelkouan "
          "shearwater <i>Puffinus yelkouan</i>. <i>Marine Ecology</i> 42:e12668. doi:10.1111/maec.12668. (Abstract read.)",
     "https://doi.org/10.1111/maec.12668"),
    ("7", "MiŻien. Estimates and calculation: data/cc-106/; tools/cc-106-report/calc.py.", ""),
])
S.append(PageBreak())
S += appendix_a("A experiment · B observational study with a control or gradient · C review, guidance or "
                "official statistics · D assertion or anecdote. ◆ marks a source known only second-hand.")
S += [Spacer(1, 5 * mm)]
S += revision_log([("1.0", "5 Oct 2026", "First issue. Verdict Largely supported (moderate confidence); no right of reply needed.")])

build_report(Report(
    number="106", out=str(FIG / "report.pdf"), kicker="Conservation science",
    title_lines=["Shearwaters:", "10% of the world", "population?"],
    subtitle_lines=["Testing BirdLife Malta’s figure for the Yelkouan shearwater", "against regulator and published estimates"],
    quote_lines=["“Malta’s population is estimated to be around 1,600 –", "1,800 pairs, constituting approximately 10% of the",
                 "global population.”"], quote_size=14,
    attribution="BirdLife Malta, LIFE Arċipelagu Garnija project page (undated; read 5 October 2026).",
    context="On the Yelkouan shearwater (Garnija), classed as Vulnerable by the IUCN.",
    verdict="Largely supported", verdict_note="An important share; “about 10%” rounds up a central 6–8%",
    footer_lines=["Version 1.0  ·  5 October 2026", "Status: no right of reply needed",
                  "Prepared from public sources and published literature.", "Repository: github.com/leandergrech/Mizien"],
    running_head="Yelkouan shearwater – BirdLife Malta", version="1.0", date="5 October 2026",
    status_note="no right of reply needed",
    pdf_title="Shearwaters: 10% of the world population? Claim Check 106",
    pdf_subject="Tests BirdLife Malta's estimate of Malta's share of the global Yelkouan shearwater population",
    story=S))
