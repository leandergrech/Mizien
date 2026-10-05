"""Claim Check 111 report. Run fetch.py, calc.py and figures.py first. Output: out/report.pdf"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import *  # noqa: E402,F401

FIG = HERE / "out"
S = []

# ================================================================== TL;DR
S += [SectionHeading(None, "TL;DR"), Spacer(1, 1 * mm),
      P("In its 2026 Country Report on Malta (3 June 2026), the European Commission wrote that <b>“waste generation "
        "is still high with 621 kg per person generated in 2024 (compared with the EU average of 517 kg per "
        "person)”</b>, and that <b>“over the last 10 years, Malta has brought its landfill rate down from 82% to 74%. "
        "However, this is still one of the highest in the EU, and well above the EU average of 22% (2023).”</b> We "
        "re-ran the figures from the Eurostat dataset the report cites.", lead)]
S.append(key_points([
    ("The waste figures are right.",
     "Eurostat env_wasmun gives 621 kg of municipal waste per person in Malta in 2024 and 517 kg for the EU-27 "
     "(provisional). Malta is 20% above the EU average and sixth-highest of the 20 states with 2024 data."),
    ("The landfill figures are right, on the basis the report uses.",
     "Landfilled waste as a share of waste generated was 82.0% in 2013 and 73.6% in 2023. Malta had the third-highest "
     "rate in 2023 (after Greece and Romania) and the highest of the states reporting for 2024 (72.1%)."),
    ("“Down from 82% to 74%” is mostly one year.",
     "The rate stayed between 76% and 91% from 2013 to 2022 and fell from 83% to 74% between 2022 and 2023. The "
     "Commission’s own summary elsewhere in the report calls this “only a marginal drop in the last decade”."),
    ("Different sources, different landfill shares.",
     "Measured against waste <i>treated</i> rather than generated, the same 2024 data give 79.2%: this is the figure "
     "The Shift reported (CC-081). Both are correct; they answer different questions."),
    ("Verdict: supported (high confidence).",
     "Every number in the passage reproduces from the cited Eurostat data. The EU-27 landfill rate for 2023 is not "
     "published in the dataset; the 2022 and 2024 values (22.6% and 21.3%) bracket the report’s 22%."),
]))
S += [Spacer(1, 2.5 * mm), VerdictMeter(0), Spacer(1, 3 * mm),
      tiles([("621 kg", GREEN, "Municipal waste per person in Malta, 2024 (EU 517 kg)"),
             ("74%", RED, "Share of municipal waste landfilled in 2023 (EU about 22%)"),
             ("3rd", ORANGE, "Malta’s rank for landfill rate in 2023; 1st of 20 states with 2024 data"),
             ("72%", GREY, "Malta’s landfill rate in 2024, the year after the report’s figure")]),
      Spacer(1, 4 * mm),
      up_down("None: Supported is the top of the scale.",
              "A revision of the Eurostat data showing different values, or evidence that the 82% and 74% were "
              "calculated on different bases."),
      Spacer(1, 3 * mm)]
S += toc([("1", "The claim and what we could verify"), ("2", "Method"), ("3", "What the data show"),
          ("4", "Where the evidence points different ways"), ("5", "Testing the claim"),
          ("6", "Verdict and requests for evidence"), ("7", "Limitations")])
S.append(PageBreak())

# ================================================================== 1
S.append(SectionHeading(1, "The claim and what we could verify"))
S.append(P("The 2026 Country Report for Malta is a Commission staff working document (SWD(2026) 218 final) "
           "published with the European Semester spring package and transmitted to the Council as document "
           "10135/26 ADD 1 [1]. We read the Council copy in full on 5 October 2026. The waste passage is in Annex 8 "
           "(“Competitiveness and the green transition”, page 75), with footnotes (156) and (158) citing Eurostat’s "
           "municipal waste dataset [2]. The same figures appear in the report’s summary (pages 17–18), which adds the "
           "recycling rate (16.7% in 2024, EU 48%) and the 2035 landfill target of 10%."))
S.append(std_table([
    [C("Source", cellh), C("What it says", cellh), C("Our access", cellh), C("Status", cellh)],
    [C("<b>European Commission</b>, 2026 Country Report – Malta, Annex 8 [1]"),
     C("“Waste generation is still high with 621 kg per person generated in 2024 (compared with the EU average of "
       "517 kg per person)” … “Over the last 10 years, Malta has brought its landfill rate down from 82% to 74%. "
       "However, this is still one of the highest in the EU, and well above the EU average of 22% (2023).”"),
     C("Full text read (Council PDF), 5 Oct 2026."), C("<b>The claim</b>")],
    [C("<b>European Commission</b>, same report, summary (pp. 17–18) [1]"),
     C("Same figures; “the municipal waste landfill rate recorded only a marginal drop in the last decade and is "
       "still high at 74% in 2023”."), C("Read."), C("Context")],
    [C("<b>Eurostat</b>, env_wasmun [2]"), C("Municipal waste generated and treated, by operation, kg per person."),
     C("Downloaded 5 Oct 2026 (data/cc-111/)."), C("<b>Primary data</b>")],
    [C("<b>The Shift</b>, Feb 2026 (CC-081) [3]"), C("79.2% of Malta’s municipal waste landfilled in 2024."),
     C("Claim record of CC-081."), C("Context")],
], [38 * mm, 74 * mm, 36 * mm, 22 * mm]))

# ================================================================== 2
S += [Spacer(1, 4 * mm), SectionHeading(2, "Method")]
S.append(P("<b>Question.</b> Do the figures in the passage reproduce from the data the report cites, and is the "
           "comparison with other member states right?"))
S.append(P("<b>Evidence.</b> We downloaded env_wasmun (updated 30 March 2026) for Malta and the EU-27, 2012–2024, and "
           "for every member state for 2023–2024 (<i>tools/cc-111-report/fetch.py</i>), and recomputed each figure "
           "with a script (<i>calc.py</i>; outputs in <i>data/cc-111/checks.csv</i>). The “landfill rate” is landfill and "
           "other disposal (operations D1–D7 and D12) divided by waste generated, the basis that reproduces both of the "
           "report’s Malta figures; we also give the share of waste treated. The EU-27 total for 2024 carries "
           "Eurostat’s flag “i” (see metadata); Malta’s values carry no flags."))
S.append(P("<b>Grades.</b> Official statistics are grade C in our scale. The claim is a statistical statement; we "
           "used no peer-reviewed literature because none is needed to test it. <b>Verdicts</b> follow the five-point "
           "scale in Appendix A."))

# ================================================================== 3
S.append(CondPageBreak(110 * mm))
S.append(SectionHeading(3, "What the data show"))
S.append(fig(FIG / "fig1_series.png", width=CW * 0.98))
S.append(P("Figure 1. Municipal waste per person (left) and the share landfilled (right), Malta and the EU-27, "
           "2013–2024. The dashed line is Malta’s landfilled waste as a share of waste treated.", cap))
S.append(P("Malta generated 621 kg of municipal waste per person in 2024, up from 603 kg in 2023; the EU-27 figure is "
           "517 kg. Malta’s figure peaked at 697 kg in 2019. Landfilled waste was 82.0% of waste generated in 2013 and "
           "73.6% in 2023; in 2024 it was 72.1%. Incineration was 2.7% of waste generated in 2023, matching the "
           "report’s “3%”."))
S.append(fig(FIG / "fig2_ranks.png", width=CW * 0.98))
S.append(P("Figure 2. Malta among the member states with data: sixth-highest for waste per person in 2024 and "
           "third-highest for the landfill rate in 2023.", cap))

# ================================================================== 4
S.append(CondPageBreak(80 * mm))
S.append(SectionHeading(4, "Where the evidence points different ways"))
S.append(contested("Which landfill share is right: 74%, 72% or 79%?", "ALL, ON THEIR OWN BASIS", AMBER,
                   "The report’s 82% and 74% are landfilled waste as a share of waste generated, for 2013 and 2023. "
                   "On that basis the 2024 figure is 72.1%.",
                   "The Shift (CC-081) reported 79.2% for 2024: landfilled waste as a share of waste treated. Malta "
                   "treats less waste than it generates in most years (566 kg treated against 621 kg generated in "
                   "2024), so the two shares differ. The National Statistics Office uses its own definitions.",
                   "No contradiction: the figures measure different things. A reader comparing sources should check "
                   "which denominator is used.", label_a="THE REPORT’S BASIS", label_b="OTHER BASES"))
S.append(Spacer(1, 3 * mm))
S.append(contested("Is a fall from 82% to 74% “over the last 10 years” a fair description?", "ACCURATE, BUT LUMPY", AMBER,
                   "The endpoints are right: 82.0% in 2013 and 73.6% in 2023.",
                   "The fall happened in one step: the rate was 83.3% in 2022. Between 2013 and 2022 it ranged from "
                   "76% to 91%. The report’s summary describes the decade as “only a marginal drop”.",
                   "The sentence is accurate. It does not describe a steady trend, and the report does not claim one.",
                   label_a="FOR", label_b="CAVEAT"))

# ================================================================== 5
S.append(CondPageBreak(120 * mm))
S.append(SectionHeading(5, "Testing the claim"))
verd = lambda t, c: chip(t, c, w=29 * mm)
S.append(std_table([
    [C("Sub-claim", cellh), C("Said by", cellh), C("What the evidence shows", cellh), C("Rating", cellh)],
    [C("<b>A.</b> 621 kg of waste per person in 2024, against an EU average of 517 kg"), C("Commission [1]"),
     C("Eurostat env_wasmun: Malta 621 kg, EU-27 517 kg (provisional). Malta is sixth-highest of 20 states with 2024 data."),
     verd("ACCURATE", GREENC)],
    [C("<b>B.</b> Landfill rate down from 82% to 74% over ten years"), C("Commission [1]"),
     C("82.0% (2013) and 73.6% (2023), landfilled as a share of generated. Most of the fall came in 2023."),
     verd("ACCURATE", GREENC)],
    [C("<b>C.</b> Still one of the highest in the EU, well above the EU average of 22% (2023)"), C("Commission [1]"),
     C("Third-highest in 2023 (after Greece and Romania); highest of 20 states in 2024. EU-27 2023 not published; "
       "22.6% in 2022 and 21.3% in 2024."), verd("ACCURATE", GREENC)],
], [42 * mm, 18 * mm, 76 * mm, 34 * mm], valign="MIDDLE"))

# ================================================================== 6
S += [Spacer(1, 6 * mm), SectionHeading(6, "Verdict and requests for evidence"),
      verdict_box("Supported", "Every figure in the passage reproduces from the Eurostat data the report cites. "
                  "Confidence: high."), Spacer(1, 4 * mm)]
S.append(P("<b>Why.</b> The per-person figures (621 kg, 517 kg), the landfill rates (82%, 74%), the incineration rate "
           "(3%) and Malta’s position among member states all reproduce from env_wasmun on the basis the report "
           "uses. The one figure we cannot reproduce exactly, the EU-27 landfill rate for 2023, is not in the "
           "dataset, but the neighbouring years agree with it."))
S.append(P("<b>What this verdict does not say.</b> It does not rate Malta’s waste policy. The Ministry’s claim of "
           "“strong progress” on recycling is checked separately (CC-004), and the landfill shares reported by other "
           "outlets are not wrong because they differ from this one."))
S.append(P("Evidence we are asking for", h2))
S.append(requests_list([
    "From Eurostat: the EU-27 landfill rate for 2023, which env_wasmun does not yet publish.",
    "From Malta’s waste authorities: an explanation of the 2015 values, when landfilled municipal waste (676 kg per "
    "person) exceeds waste generated (643 kg).",
]))
S += [Spacer(1, 4 * mm),
      callout([P("RIGHT OF REPLY", tag),
               P("Not needed for this verdict (maintainer rule of 5 October 2026: a reply is sought only for "
                 "<i>Not substantiated</i>, <i>Misleading</i> or <i>Contradicted</i>).", small)], bg=AMBER_PALE, bar=AMBER)]

# ================================================================== 7
S += [Spacer(1, 6 * mm), SectionHeading(7, "Limitations")]
for l in ["The EU-27 total for 2024 is flagged by Eurostat; 2024 data are missing for seven member states, so the 2024 "
          "ranking covers 20 states.",
          "Municipal waste statistics depend on national reporting; definitions of municipal waste and of treatment "
          "differ between countries and over time.",
          "We did not test the summary’s recycling figures (16.7%, EU 48%) or the 2035 target; the recycling question "
          "is checked in CC-004.",
          "We read the report in its Council copy; the Commission’s own publication should be identical."]:
    S.append(P("• " + l, bul))

S += [Spacer(1, 6 * mm), SectionHeading(None, "References")]
S += references([
    ("1", "European Commission (3 June 2026). 2026 Country Report – Malta. SWD(2026) 218 final; Council document "
          "10135/26 ADD 1. Annex 8, p. 75, and summary, pp. 17–18.",
     "https://data.consilium.europa.eu/doc/document/ST-10135-2026-ADD-1/en/pdf"),
    ("2", "Eurostat. Municipal waste by waste management operations (env_wasmun), updated 30 Mar 2026, retrieved "
          "5 Oct 2026.", "https://ec.europa.eu/eurostat/databrowser/view/env_wasmun/default/table"),
    ("3", "MiŻien. CC-081 claim record (The Shift, landfill share rising) and CC-004 report (recycling): claims/CC-081, "
          "claims/CC-004.", ""),
    ("4", "MiŻien. Calculation script and outputs: tools/cc-111-report/calc.py; data/cc-111/checks.csv.", ""),
])

S.append(PageBreak())
S += appendix_a("A experiment · B observational study with a control or gradient · C review, guidance or "
                "official statistics · D assertion or anecdote. ◆ marks a source known only second-hand.")
S += [Spacer(1, 5 * mm)]
S += revision_log([("1.0", "5 Oct 2026", "First issue. Verdict Supported (high confidence); no right of reply needed.")])

build_report(Report(
    number="111", out=str(FIG / "report.pdf"), kicker="Statistics and EU data",
    title_lines=["621 kg of waste", "a head, 74%", "landfilled?"],
    subtitle_lines=["Testing the European Commission’s 2026 Country Report", "against the Eurostat data it cites"],
    quote_lines=["“Over the last 10 years, Malta has brought its landfill rate", "down from 82% to 74%. However, this is still one of",
                 "the highest in the EU.”"], quote_size=14,
    attribution="European Commission, 2026 Country Report – Malta, 3 June 2026.",
    context="Annex 8, alongside “621 kg per person generated in 2024 (compared with the EU average of 517 kg)”.",
    verdict="Supported", verdict_note="Every figure reproduces from Eurostat env_wasmun",
    footer_lines=["Version 1.0  ·  5 October 2026", "Status: no right of reply needed",
                  "Prepared from public sources and Eurostat data.", "Repository: github.com/leandergrech/Mizien"],
    running_head="Municipal waste and landfill – Commission 2026 Country Report", version="1.0", date="5 October 2026",
    status_note="no right of reply needed",
    pdf_title="621 kg of waste a head, 74% landfilled? Claim Check 111",
    pdf_subject="Tests the European Commission's 2026 Country Report figures on municipal waste in Malta",
    story=S))
