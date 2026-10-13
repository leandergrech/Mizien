"""Claim Check 117 report. Run fetch.py, calc.py and figures.py first. Output: out/report.pdf"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import *  # noqa: E402,F401

FIG = HERE / "out"
S = []

# ================================================================== TL;DR
S += [SectionHeading(None, "TL;DR"), Spacer(1, 1 * mm),
      P("In its July 2026 infringement package (8 July 2026), the European Commission wrote that <b>“Malta missed the "
        "targets for total packaging, paper and cardboard and metals”</b> in 2020 to 2023, and that Malta, with eleven "
        "other states, <b>“failed to meet the 50% target of preparing for reuse and recycling of municipal waste … which "
        "was to be reached by 2020”</b>. It decided to send Malta a reasoned opinion (INFR(2024)2135). We tested these "
        "findings against Eurostat’s published recycling rates.", lead)]
S.append(key_points([
    ("The infringement step is as stated.",
     "The Commission’s page lists Malta (INFR(2024)2135) among the states getting a reasoned opinion, after letters of "
     "formal notice in July 2024. Malta has two months to respond; the Commission may then refer the case to the Court "
     "of Justice. A reasoned opinion is the Commission’s position, not a court finding."),
    ("The municipal target was missed, by a wide margin.",
     "Eurostat’s recycling rate for Malta was 10.9% in 2020 (target 50%), the lowest of the EU-27; it was 16.7% in 2024 "
     "against 48.1% for the EU-27."),
    ("Total packaging and paper and cardboard were below target in every year, 2020 to 2023.",
     "Total packaging: 40.0%, 36.8%, 30.8%, 43.4% (target 55%). Paper and cardboard: 47.8%, 45.3%, 40.6%, 53.6% (target 60%)."),
    ("Metals were below target in 2021, 2022 and 2023, but not in 2020.",
     "Eurostat gives 57.2% for metal packaging in 2020 (target 50%), then 27.1%, 13.0% and 15.2%. The Commission’s "
     "wording covers the four years together."),
    ("Verdict: largely supported (high confidence).",
     "Each named finding reproduces from Eurostat. The caveats are the 2020 metals result and that we read the "
     "Commission’s summary page, not the decision text or the Directives."),
]))
S += [Spacer(1, 2.5 * mm), VerdictMeter(1), Spacer(1, 3 * mm),
      tiles([("10.9%", RED, "Malta’s municipal recycling rate in 2020 (target 50%); lowest in the EU-27"),
             ("4 of 4", RED, "years 2020–2023 below target for total packaging and for paper and cardboard"),
             ("3 of 4", ORANGE, "years below the metals target (2021–2023); 2020 met at 57.2%"),
             ("2 months", GREY, "for Malta to respond to the reasoned opinion")]),
      Spacer(1, 4 * mm),
      up_down("None: the findings are reproduced. A fully ‘Supported’ rating would need the decision text and the "
              "Directives’ calculation rules to be read and to match.",
              "Evidence that the Commission’s compliance data for Malta differ materially from Eurostat’s, or that the "
              "case was closed or the opinion withdrawn."),
      Spacer(1, 3 * mm)]
S += toc([("1", "The claim and what we could verify"), ("2", "Method"), ("3", "What the data show"),
          ("4", "Where the evidence points different ways"), ("5", "Testing the claim"),
          ("6", "Verdict and requests for evidence"), ("7", "Limitations")])
S.append(PageBreak())

# ================================================================== 1
S.append(SectionHeading(1, "The claim and what we could verify"))
S.append(P("The wording is on the page “July infringements package: key decisions”, published by the Commission’s "
           "Representation in Malta for the decisions of 8 July 2026 [1]. We read it in full on 13 October 2026. Under "
           "the heading “The European Commission calls on 12 Member States to meet waste recycling targets” it says the "
           "Commission decided to “send a reasoned opinion to … Malta (INFR(2024)2135) … for failing to meet several "
           "waste recycling targets, based on the latest available data reported by Member States”. It adds that the "
           "Commission “already issued letters of formal notice” in July 2024 and that the reasoned opinion “now has two "
           "months to respond”, after which “the Commission may decide to refer the cases to the Court of Justice”. "
           "Newsbook reported the decision on 9 July 2026 [2]."))
S.append(std_table([
    [C("Source", cellh), C("What it says", cellh), C("Our access", cellh), C("Status", cellh)],
    [C("<b>European Commission</b> (Representation in Malta), July infringements package [1]"),
     C("Malta, with eleven other states, “failed to meet the 50% target of preparing for reuse and recycling of "
       "municipal waste … which was to be reached by 2020”. For packaging: “Malta missed the targets for total "
       "packaging, paper and cardboard and metals”, within “several targets for 2020, 2021, 2022 and 2023”. The page "
       "lists material targets of 60% (glass), 60% (paper and cardboard), 50% (metals), 22.5% (plastics) and 15% (wood)."),
     C("Full page read, 13 Oct 2026."), C("<b>The claim</b>")],
    [C("<b>Newsbook</b>, 9 Jul 2026 [2]"), C("Reports the reasoned opinion in the outlet’s own words."),
     C("Read, 13 Oct 2026."), C("Locator")],
    [C("<b>Eurostat</b>, cei_wm011 and env_waspac [3][4]"),
     C("Recycling rate of municipal waste; recycling rates of packaging waste by material, by country and year."),
     C("Downloaded 13 Oct 2026 (data/cc-117/)."), C("<b>Primary data</b>")],
], [38 * mm, 74 * mm, 36 * mm, 22 * mm]))
S.append(P("We did not obtain the infringement decision text, the July 2024 letter of formal notice (neither is "
           "published on the page) or the Directives themselves. The target values below are those the Commission’s page "
           "states; the total-packaging figure (55% minimum) is the lower bound of the “between 55% and 80%” on the same "
           "page. The Commission’s original press-corner version of the package was not opened.", small))

# ================================================================== 2
S += [Spacer(1, 4 * mm), SectionHeading(2, "Method")]
S.append(P("<b>Question.</b> Do Eurostat’s published recycling rates for Malta fall short of the targets the Commission "
           "names, in the years it names?"))
S.append(P("<b>Evidence.</b> We downloaded Eurostat’s municipal waste recycling rate (cei_wm011, updated 30 March 2026) "
           "and packaging waste recycling rates by material (env_waspac, updated 11 May 2026) with "
           "<i>tools/cc-117-report/fetch.py</i>, and compared each rate with the target in <i>calc.py</i> (outputs in "
           "<i>data/cc-117/checks.csv</i>). Eurostat’s rates are calculated by Eurostat from national reports; the "
           "Commission’s compliance assessment uses the data reported by Member States under the Directives’ own "
           "calculation rules. The two should agree closely but need not match exactly, so our check is "
           "an independent test of direction and size, not a reproduction of the Commission’s calculation."))
S.append(P("<b>Grades.</b> Official statistics are grade C in our scale. The claim is a regulatory finding; no "
           "peer-reviewed literature is needed to test whether published rates sit below published targets. "
           "<b>Verdicts</b> follow the five-point scale in Appendix A."))

# ================================================================== 3
S.append(CondPageBreak(110 * mm))
S.append(SectionHeading(3, "What the data show"))
S.append(fig(FIG / "fig1_series.png", width=CW * 0.98))
S.append(P("Figure 1. Municipal recycling rate, Malta and the EU-27 (left), and Malta’s packaging recycling rates for "
           "the three materials the Commission names, against their targets (right).", cap))
S.append(P("Malta’s municipal recycling rate was 9.1% in 2019, 10.9% in 2020 and 16.7% in 2024; the EU-27 rate was 48.5% "
           "in 2020 and 48.1% in 2024. The 50% target applied to 2020, and Malta did not reach it in any year to 2024. For "
           "packaging, Malta’s total rate was below 55% in all four years, with 43.4% in 2023; 3 of the 23 member states "
           "with 2023 data were below 55% (Romania 41.0%, Malta 43.4%, Greece 48.0%), and the EU-27 rate was 67.4%."))
S.append(fig(FIG / "fig2_ranks.png", width=CW * 0.98))
S.append(P("Figure 2. Municipal recycling rate in 2020, EU-27. Malta had the lowest rate on Eurostat’s indicator.", cap))

# ================================================================== 4
S.append(CondPageBreak(80 * mm))
S.append(SectionHeading(4, "Where the evidence points different ways"))
S.append(contested("Were the metals target and the 2020 year both missed?", "MOSTLY", AMBER,
                   "The Commission says Malta missed the metals target within 2020–2023. Eurostat shows 27.1% (2021), 13.0% "
                   "(2022) and 15.2% (2023) against 50%.",
                   "Eurostat’s 2020 value for metal packaging is 57.2%, above the 50% target. The Commission’s sentence "
                   "covers the four years together and does not say that every target was missed in every year.",
                   "The statement holds for three of the four years. It would mislead only if read as every target in "
                   "every year, which the Commission’s wording does not claim.",
                   label_a="FOR", label_b="CAVEAT"))
S.append(Spacer(1, 3 * mm))
S.append(contested("Why does Eurostat show other shortfalls the Commission does not list?", "UNEXPLAINED", AMBER,
                   "The Commission lists total packaging, paper and cardboard, and metals for Malta.",
                   "Eurostat’s rates also fall below the page’s targets for plastics (2020–2022), wood (0.0% in all four "
                   "years) and glass (43.3% in 2022). We cannot say why the page does not list them: the Commission’s "
                   "assessment may use different reported data or counting rules (e.g. for wood), or a different "
                   "reference year for the glass and plastics targets. We did not read the decision text.",
                   "This does not contradict the claim, which names what the Commission found. It is a limit on how far "
                   "Eurostat’s indicator reproduces the Commission’s list, and is not rated.",
                   label_a="THE COMMISSION", label_b="EUROSTAT"))

# ================================================================== 5
S.append(CondPageBreak(120 * mm))
S.append(SectionHeading(5, "Testing the claim"))
verd = lambda t, c: chip(t, c, w=29 * mm)
S.append(std_table([
    [C("Sub-claim", cellh), C("Said by", cellh), C("What the evidence shows", cellh), C("Rating", cellh)],
    [C("<b>A.</b> A reasoned opinion (INFR(2024)2135) was sent to Malta, the second stage, after July 2024 notices"),
     C("EC [1]"),
     C("Stated on the Commission’s page and reported by Newsbook [2]. We did not see the decision text; no Maltese "
       "response found."), verd("ACCURATE", GREENC)],
    [C("<b>B.</b> Malta missed the 50% municipal preparing-for-reuse-and-recycling target for 2020"), C("EC [1]"),
     C("Eurostat: 10.9% in 2020, lowest of the EU-27; never above 17.4% to 2024."), verd("ACCURATE", GREENC)],
    [C("<b>C.</b> Malta missed the targets for total packaging, and paper and cardboard (2020–2023)"), C("EC [1]"),
     C("Total 40.0 / 36.8 / 30.8 / 43.4% against 55%; paper and cardboard 47.8 / 45.3 / 40.6 / 53.6% against 60%."),
     verd("ACCURATE", GREENC)],
    [C("<b>D.</b> Malta missed the metals target (2020–2023)"), C("EC [1]"),
     C("27.1 / 13.0 / 15.2% against 50% in 2021–2023; 57.2% in 2020 was above target."),
     verd("ACCURATE, ONE YEAR MET", AMBER)],
], [42 * mm, 18 * mm, 76 * mm, 34 * mm], valign="MIDDLE"))

# ================================================================== 6
S += [Spacer(1, 6 * mm), SectionHeading(6, "Verdict and requests for evidence"),
      verdict_box("Largely supported", "Each finding named in the claim reproduces from Eurostat, with one year of one "
                  "target met. Confidence: high."), Spacer(1, 4 * mm)]
S.append(P("<b>Why.</b> The municipal target was missed by about 39 percentage points in 2020; packaging was below "
           "target for total and for paper and cardboard in all four years and for metals in three. The procedural "
           "statement is on the Commission’s own page. We rate ‘Largely supported’, not ‘Supported’, because the metals "
           "target was met in 2020 on Eurostat’s figures, and because we read the Commission’s summary, not the "
           "decision text or the Directives."))
S.append(P("<b>What this verdict does not say.</b> It does not rate how Malta’s waste policy has performed since, "
           "or the Ministry’s statements on separation (checked in CC-004). A reasoned opinion is a step in a procedure; "
           "it is not a finding by the Court of Justice."))
S.append(P("Evidence we are asking for", h2))
S.append(requests_list([
    "From the Commission: the decision text for INFR(2024)2135 and the July 2024 letter of formal notice, with the "
    "reported data and years behind each target.",
    "From the Government of Malta: its reply to the reasoned opinion, if published.",
]))
S += [Spacer(1, 4 * mm),
      callout([P("RIGHT OF REPLY", tag),
               P("Not needed for this verdict (maintainer rule of 5 October 2026: a reply is sought only for "
                 "<i>Not substantiated</i>, <i>Misleading</i> or <i>Contradicted</i>).", small)], bg=AMBER_PALE, bar=AMBER)]

# ================================================================== 7
S += [Spacer(1, 6 * mm), SectionHeading(7, "Limitations")]
for l in ["We read the Commission’s summary page, not the infringement decision or the Directives; the targets are as "
          "that page states them. The 2020–2023 packaging targets are the 2008 targets; the higher targets apply from 2025.",
          "Eurostat’s recycling rates are not the Commission’s compliance calculation. Some Member States use "
          "alternative calculation methods under the Directives; we did not check which Malta used.",
          "Eurostat’s 2024 EU-27 municipal rate carries the flag ‘i’ (see metadata). Packaging data end in 2023.",
          "The page was published by the Commission’s Representation in Malta; its metadata give 8 July 2026 for the "
          "decisions. We did not find a Maltese response to the opinion."]:
    S.append(P("• " + l, bul))

S += [Spacer(1, 6 * mm), SectionHeading(None, "References")]
S += references([
    ("1", "European Commission, Representation in Malta (8 July 2026). July infringements package: key decisions.",
     "https://malta.representation.ec.europa.eu/news/july-infringements-package-key-decisions-2026-07-08_en"),
    ("2", "Balzan, J. (9 July 2026). EU escalates action against Malta over missed recycling targets. Newsbook.",
     "https://newsbook.com.mt/en/eu-escalates-action-against-malta-over-missed-recycling-targets/"),
    ("3", "Eurostat. Recycling rate of municipal waste (cei_wm011), updated 30 Mar 2026, retrieved 13 Oct 2026.",
     "https://ec.europa.eu/eurostat/databrowser/view/cei_wm011/default/table"),
    ("4", "Eurostat. Packaging waste by waste operations and waste flow (env_waspac), updated 11 May 2026, retrieved "
          "13 Oct 2026.", "https://ec.europa.eu/eurostat/databrowser/view/env_waspac/default/table"),
    ("5", "MiŻien. Calculation script and outputs: tools/cc-117-report/calc.py; data/cc-117/checks.csv. Related: CC-004, CC-111.", ""),
])

S.append(PageBreak())
S += appendix_a("A experiment · B observational study with a control or gradient · C review, guidance or "
                "official statistics · D assertion or anecdote. ◆ marks a source known only second-hand.")
S += [Spacer(1, 5 * mm)]
S += revision_log([("1.0", "13 Oct 2026", "First issue. Verdict Largely supported (high confidence); no right of reply needed.")])

build_report(Report(
    number="117", out=str(FIG / "report.pdf"), kicker="Waste and EU law",
    title_lines=["Did Malta miss", "its recycling", "targets?"],
    subtitle_lines=["Testing the European Commission’s July 2026 reasoned opinion", "against Eurostat recycling data"],
    quote_lines=["“Malta missed the targets for total packaging,", "paper and cardboard and metals.”"], quote_size=15,
    attribution="European Commission, July infringements package, 8 July 2026.",
    context="Also: Malta failed to meet the 50% municipal recycling target “to be reached by 2020”; reasoned opinion INFR(2024)2135.",
    verdict="Largely supported", verdict_note="Findings reproduce from Eurostat; one year of one target met",
    footer_lines=["Version 1.0  ·  13 October 2026", "Status: no right of reply needed",
                  "Prepared from public sources and Eurostat data.", "Repository: github.com/leandergrech/Mizien"],
    running_head="Recycling targets – Commission reasoned opinion, July 2026", version="1.0", date="13 October 2026",
    pdf_title="Did Malta miss its recycling targets? Claim Check 117",
    pdf_subject="Tests the European Commission's July 2026 reasoned opinion findings on Malta's recycling targets",
    story=S))
