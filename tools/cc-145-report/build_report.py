"""Claim Check 145 report. Run calc.py and figures.py first. Output: out/report.pdf"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import *  # noqa: E402,F401

FIG = HERE / "out"
S = []
S += [SectionHeading(None, "TL;DR"), Spacer(1, 1 * mm),
      P("After a storm in September 2026 grounded migrating birds over Malta, BirdLife Malta’s public engagement "
        "executive, Antonia Micallef, told Mongabay by email: <b>“Over 10,000 hunters [are] active at any one time”</b> "
        "and <b>“Between 14 and 21 September alone, BirdLife Malta collected 21 protected birds with confirmed shooting "
        "injuries.”</b> We checked the first figure against the regulator’s licence data and looked for any record of "
        "the second.", lead)]
S.append(key_points([
    ("“Over 10,000 hunters” matches the licence count.",
     "The Wild Birds Regulation Unit (WBRU) recorded 10,091 general licences to hunt birds on land in 2025, one per "
     "licensee."),
    ("“Active at any one time” is not measured.",
     "A licence allows hunting; it does not show how many people are out at once. No published figure counts hunters "
     "in the field on a given day. Only 636 land licensees (6.3%) filed any catch report in 2025, but reports are needed "
     "only when game is bagged, so this is not a measure of activity either."),
    ("The 21 injured birds are BirdLife’s own count.",
     "No list is published. BirdLife’s press releases from that week describe protected birds shot, but do not give the "
     "total. We could not check it."),
    ("Verdict: largely supported (moderate confidence).",
     "The number of hunters holds. The phrase “at any one time” goes further than the data can show, and the bird count "
     "rests on BirdLife’s records alone."),
]))
S += [Spacer(1, 2.5 * mm), VerdictMeter(1), Spacer(1, 3 * mm),
      tiles([("10,091", GREEN, "general licences to hunt birds on land in 2025 (WBRU)"),
             ("6.3%", AMBER, "of those licensees filed any catch report in 2025"),
             ("21", GREY, "protected birds with shooting injuries collected by BirdLife, 14–21 Sep 2026 (own count)"),
             ("0", GREY, "published counts of hunters in the field on a given day")]),
      Spacer(1, 4 * mm),
      up_down("BirdLife publishing its 14–21 September casualty log (species, date, place, veterinary or police "
              "record), and a 2026 licence count above 10,000.",
              "A 2026 licence count below 10,000, or field counts showing far fewer hunters out on peak days."),
      Spacer(1, 3 * mm)]
S += toc([("1", "The claim and what we could verify"), ("2", "Method"), ("3", "How many hunters"),
          ("4", "The 21 injured birds"), ("5", "Testing the claim"), ("6", "Verdict"), ("7", "Limitations")])
S.append(PageBreak())

S.append(SectionHeading(1, "The claim and what we could verify"))
S.append(P("Mongabay’s article of 5 October 2026 quotes Micallef directly; the square brackets are Mongabay’s [1]. "
           "The sentence before the first quotation (“Malta has the highest density of hunters in all of Europe”) is "
           "the outlet’s own and is checked separately as CC-144. Mongabay also reports that the autumn turtle-dove "
           "quota of 500 was reached soon after the storm. That is not in quotation marks and is not tested here. "
           "BirdLife’s own releases of 14 and 16 September describe the storm and the protected birds shot, but do not "
           "carry either figure [2, 3]."))
S.append(std_table([
    [C("Source", cellh), C("What it says", cellh), C("Our access", cellh), C("Status", cellh)],
    [C("<b>BirdLife Malta</b> via Mongabay, 5 Oct 2026 [1]"),
     C("“Over 10,000 hunters [are] active at any one time”; 21 protected birds with confirmed shooting injuries "
       "collected 14–21 Sep."), C("Read in full in a browser (16 Nov 2026)."), C("<b>The claim</b>")],
    [C("<b>BirdLife Malta</b>, releases 14 and 16 Sep 2026 [2, 3]"),
     C("Storm, turtle-doves and protected birds shot; “thousands of hunters”."), C("Read in full (31 Oct 2026)."),
     C("<b>Context</b>")],
    [C("<b>WBRU</b>, Game Reporting Data – 2025 Report [4]"),
     C("Licences by category and game reports filed in 2025."),
     C("Maintainer’s browser copy (wbru.gov.mt refuses scripts); tables read in full."), C("<b>Primary data</b>")],
], [38 * mm, 66 * mm, 40 * mm, 26 * mm]))
S.append(Spacer(1, 2 * mm))
S.append(P("<b>Fairness note.</b> This check is about two figures in a statement, not about hunters or about BirdLife. "
           "Most licence holders break no law, and BirdLife’s recovery of injured birds is real work that cannot be "
           "checked from outside without its records.", small))

S += [Spacer(1, 4 * mm), SectionHeading(2, "Method")]
S.append(P("We typed the WBRU’s two summary tables for 2025 into <i>data/cc-145/wbru_2025_licences.csv</i> and computed "
           "the shares in <i>tools/cc-145-report/calc.py</i> (output <i>data/cc-145/checks.csv</i>). We searched "
           "BirdLife’s September releases and the Government’s press releases of 1 September to 6 October 2026 for a "
           "count of injured birds or of hunters in the field. The WBRU report is an official statistic (grade C). "
           "BirdLife’s count is an organisation’s own unpublished record (grade D). <b>Verdicts</b> follow the five-point "
           "scale in Appendix A."))

S.append(CondPageBreak(110 * mm))
S.append(SectionHeading(3, "How many hunters"))
S.append(fig(FIG / "fig1_licences.png", width=CW * 0.98))
S.append(P("Figure 1. Licences active in 2025 by category, and licensees who filed at least one game report.", cap))
S.append(P("To hunt birds in autumn a person needs the general licence for hunting birds on land, plus a police weapons "
           "permit, insurance and membership of a hunting organisation [4]. In 2025 the WBRU recorded 10,091 such "
           "licences. Each licensee holds a category once, so this is 10,091 people, 91 above BirdLife’s figure. Many "
           "also hold other categories (7,913 held the spring licence), so the categories must not be added together. "
           "The 2026 count is not yet published."))
S.append(P("“Active at any one time” is a different claim. A licence is a right to hunt in season; it does not say how "
           "many people are hunting at once. The WBRU’s game reports are the only activity data, and they are filed only "
           "when a bird or rabbit is bagged. In 2025, 636 land licensees (6.3%) filed at least one report, and 1,265 "
           "people across all categories filed 5,924 reports [4]. That is a floor for successful outings, not a count of "
           "people out. No source we found counts hunters in the field on a given day, so the phrase cannot be tested. "
           "Read as “over 10,000 licensed and active hunters”, the figure is right."))

S.append(CondPageBreak(60 * mm))
S.append(SectionHeading(4, "The 21 injured birds"))
S.append(P("The figure is BirdLife’s count of protected birds it recovered with shooting injuries in one week. BirdLife "
           "has not published the list, and its releases of 14 and 16 September name individual cases, such as a Black "
           "Stork killed outside Buskett, without a total [2, 3]. No police or WBRU count for that week has been published. "
           "Mongabay’s wording, “collected … with confirmed shooting injuries”, is narrower than the record’s earlier "
           "summary (“21 protected birds shot”): it counts birds found, not birds shot. We have corrected the record’s "
           "title to match."))

S.append(CondPageBreak(70 * mm))
S.append(SectionHeading(5, "Testing the claim"))
verd = lambda t, c: chip(t, c, w=29 * mm)
S.append(std_table([
    [C("Sub-claim", cellh), C("Said by", cellh), C("What the evidence shows", cellh), C("Rating", cellh)],
    [C("<b>A.</b> “Over 10,000 hunters [are] active at any one time”"), C("BirdLife Malta [1]"),
     C("10,091 general licences to hunt birds on land in 2025 (WBRU). No data on how many hunt at once."),
     verd("NUMBER RIGHT", GREENC)],
    [C("<b>B.</b> “Between 14 and 21 September alone, BirdLife Malta collected 21 protected birds with confirmed "
       "shooting injuries”"), C("BirdLife Malta [1]"),
     C("BirdLife’s own record. No list or official count is published."), verd("NOT VERIFIABLE", AMBER)],
], [42 * mm, 26 * mm, 68 * mm, 34 * mm], valign="MIDDLE"))

S += [Spacer(1, 6 * mm), SectionHeading(6, "Verdict"),
      verdict_box("Largely supported", "Over 10,000 people held a licence to hunt birds on land in 2025. “At any one time” "
                  "is not shown, and the 21-bird count is BirdLife’s own. Confidence: moderate."), Spacer(1, 4 * mm)]
S.append(P("<b>Why.</b> The checkable figure is correct to within 1%. The caveats do not change the main point, that "
           "Malta has over 10,000 licensed bird hunters. But “at any one time” should not be read as 10,000 people in "
           "the field together, and the 21-bird count cannot be checked until BirdLife publishes it. Confidence is "
           "moderate because the 2026 licence count is not out and one figure is unverifiable. <b>What this verdict does "
           "not say.</b> It does not judge hunting policy, the turtle-dove quota, or enforcement."))
S.append(P("Evidence we are asking for", h2))
S.append(requests_list(["From BirdLife Malta: the list of the 21 birds (species, date, locality, and veterinary or "
                        "police reference).",
                        "From the WBRU: the 2026 licence count by category, and any data on hunters in the field on peak "
                        "days."]))
S += [Spacer(1, 4 * mm),
      callout([P("RIGHT OF REPLY", tag),
               P("Not needed for this verdict (maintainer rule of 5 October 2026).", small)], bg=AMBER_PALE, bar=AMBER)]
S += [Spacer(1, 6 * mm), SectionHeading(7, "Limitations")]
for l in ["The licence count is for 2025; the claim was made in October 2026.",
          "Mongabay’s article was read in a browser; it quotes an email we have not seen.",
          "wbru.gov.mt refuses scripts. The 2025 report is the maintainer’s browser copy (sha256 2aad41f2…0e9fd)."]:
    S.append(P("• " + l, bul))
S += [Spacer(1, 6 * mm), SectionHeading(None, "References")]
S += references([
    ("1", "Raman, S. Hunters reportedly kill hundreds of migratory birds stranded by thunderstorm in Malta. Mongabay, "
          "5 October 2026 (read 16 Nov 2026).",
     "https://news.mongabay.com/short-article/2026/10/hunters-reportedly-kill-hundreds-of-migratory-birds-stranded-by-thunderstorm-in-malta/"),
    ("2", "BirdLife Malta. Mediterranean storms bring bird-fall as hundreds of Turtle-doves are shot in Malta, along with "
          "various protected species, 14 September 2026.",
     "https://birdlifemalta.org/2026/09/mediterranean-storms-bring-bird-fall-as-hundreds-of-turtle-doves-are-shot-in-malta-along-with-various-protected-species/"),
    ("3", "BirdLife Malta. Highly protected Black Stork killed outside Buskett as post-storm casualties mount, "
          "16 September 2026.",
     "https://birdlifemalta.org/2026/09/highly-protected-black-stork-killed-outside-buskett-as-post-storm-casualties-mount/"),
    ("4", "Wild Birds Regulation Unit. Game Reporting Data – 2025 Report, July 2026, pp. 1–2 (maintainer’s browser copy, "
          "read 17 Nov 2026).", "https://wbru.gov.mt/wp-content/uploads/2026/07/Game-Reporting-Data-report-2025.pdf"),
    ("5", "MiŻien. Data and script: data/cc-145/; tools/cc-145-report/calc.py. Related check: CC-144 (hunter density).", ""),
])
S.append(PageBreak())
S += appendix_a("A experiment · B observational study with a control or gradient · C review, guidance or "
                "official statistics · D assertion or anecdote. ◆ marks a source known only second-hand.")
S += [Spacer(1, 5 * mm)]
S += revision_log([("1.0", "17 Nov 2026", "First issue. Verdict Largely supported (moderate confidence); no right of "
                    "reply needed.")])

build_report(Report(
    number="145", out=str(FIG / "report.pdf"), kicker="Hunting and birds",
    title_lines=["Ten thousand", "hunters?"],
    subtitle_lines=["Testing BirdLife Malta’s figures after the", "September 2026 storm"],
    quote_lines=["“Over 10,000 hunters [are]", "active at any one time.”"], quote_size=16,
    attribution="Antonia Micallef, BirdLife Malta, by email to Mongabay, 5 October 2026.",
    context="On hunting after a storm grounded migrating birds over Malta.",
    verdict="Largely supported", verdict_note="10,091 land licences; “at any one time” not shown",
    footer_lines=["Version 1.0  ·  17 November 2026", "Status: no right of reply needed",
                  "Prepared from public sources and open data.", "Repository: github.com/leandergrech/Mizien"],
    running_head="Hunters and injured birds – BirdLife Malta, October 2026", version="1.0", date="17 November 2026",
    pdf_title="Ten thousand hunters? Claim Check 145",
    pdf_subject="Tests BirdLife Malta's figures on active hunters and injured protected birds",
    story=S))
