"""Claim Check 047 report. Run calc.py and figures.py first. Output: out/report.pdf"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import *  # noqa: E402,F401

LG = colors.HexColor("#8DB36B")
FIG = HERE / "out"
S = []
S += [SectionHeading(None, "TL;DR"), Spacer(1, 1 * mm),
      P("On 13 February 2026 MaltaToday reported on a peer-reviewed study of nitrate in Malta’s groundwater. The article "
        "quotes the study: <b>“the highest concentrations of nitrate are observed in the eastern areas of the MSLA, "
        "ranging from 100 to 200 mg/L”</b>, and adds that this is “two to four times higher than the EU safety limit of "
        "50 mg/L”. We checked the arithmetic and tested the picture against the Commission’s own review of Malta’s "
        "monitoring data.", lead)]
S.append(key_points([
    ("The arithmetic and the limit are right.",
     "100 and 200 mg/L are two and four times 50 mg/L, the nitrate limit in the Nitrates Directive and the "
     "drinking-water standard."),
    ("The picture is confirmed by independent monitoring.",
     "The Commission’s 2020–2023 review of Malta’s Energy and Water Agency data finds 30 of 44 groundwater monitoring "
     "points (68.2%) with an average of 50 mg/L or more, up from 63.6% in 2016–2019."),
    ("The 100–200 mg/L figure matches the research team’s own earlier abstract.",
     "A 2025 EGU abstract by the same group gives 75–200 mg/L for groundwater under potato and forage fields in the "
     "central and eastern areas, and 25–100 mg/L in the regional aquifer under the north-western perched aquifer."),
    ("We could not read the paper’s full text.",
     "The sentence is therefore a second-hand quotation (via MaltaToday). Independent data do not give the eastern "
     "aquifer’s range separately."),
    ("Verdict: largely supported (moderate confidence).",
     "The figures are the study’s and the direction is confirmed; the exact eastern range rests on a quotation we "
     "could not check in the paper."),
]))
S += [Spacer(1, 2.5 * mm), VerdictMeter(1), Spacer(1, 3 * mm),
      tiles([("100–200", RED, "mg/L nitrate in the eastern main aquifer (study, as quoted)"),
             ("2–4×", AMBER, "multiple of the 50 mg/L EU limit (checked)"),
             ("68.2%", RED, "of 44 monitoring points averaged 50 mg/L or more, 2020–2023"),
             ("63.6%", GREY, "the same share in 2016–2019")]),
      Spacer(1, 4 * mm),
      up_down("The paper’s full text confirming the 100–200 mg/L sentence, with EWA station data for the eastern "
              "aquifer, would move this to Supported.",
              "Station data showing the eastern aquifer’s typical values well below 100 mg/L, or a statement in the "
              "paper that the range is a local maximum."),
      Spacer(1, 3 * mm)]
S += toc([("1", "The claim and what we could verify"), ("2", "Method"), ("3", "What the data show"),
          ("4", "Where the evidence points different ways"), ("5", "Testing the claim"),
          ("6", "Verdict and requests for evidence"), ("7", "Limitations")])
S.append(PageBreak())

S.append(SectionHeading(1, "The claim and what we could verify"))
S.append(P("The claim record came from a MaltaToday article by James Debono, “Potatoes and intensive farming: A "
           "slow-moving threat to Malta’s groundwater”, 13 February 2026 [1]. We read it on 5 October 2026. The relevant "
           "paragraph says: “In the eastern areas of the main aquifer, the report notes: ‘Specifically, the highest "
           "concentrations of nitrate are observed in the eastern areas of the MSLA, ranging from 100 to 200 mg/L.’ This is "
           "two to four times higher than the EU safety limit of 50 mg/L.” The words inside quotation marks are the "
           "paper’s; the comparison with the limit is the outlet’s. The paper is Laudi, Dahan, Sapiano, Schembri, Galea, "
           "Busuttil, Mangion and Turkeltaub (2026), <i>Journal of Hydrology: Regional Studies</i> 64:103162 [2]."))
S.append(std_table([
    [C("Source", cellh), C("What it says", cellh), C("Our access", cellh), C("Status", cellh)],
    [C("<b>MaltaToday</b>, 13 Feb 2026 [1]"),
     C("Quotes the paper (100–200 mg/L, eastern MSLA) and adds “two to four times higher than the EU safety limit”."),
     C("Read in full."), C("<b>The claim</b>")],
    [C("<b>Laudi et al.</b> (2026), J. Hydrol.: Reg. Stud. [2]"),
     C("Open-access (CC BY) study: 16 vadose-zone stations, five years; potato farming the dominant nitrate source for "
       "the main aquifer."),
     C("Crossref and OpenAlex abstract only; full text blocked ◆."), C("Primary study")],
    [C("<b>Laudi et al.</b> (2025), EGU abstract [3]"),
     C("Groundwater under potato and forage fields 75–200 mg/L; perched aquifer 200–350; regional aquifer 25–100."),
     C("Abstract read (Crossref)."), C("Same team, earlier")],
    [C("<b>European Commission</b>, SWD(2026) 232, Malta fiche [4]"),
     C("Of 44 groundwater points, 68.2% average 50 mg/L or more (2020–2023)."), C("Read in full (PDF)."),
     C("Independent")],
], [38 * mm, 74 * mm, 36 * mm, 22 * mm]))

S += [Spacer(1, 4 * mm), SectionHeading(2, "Method")]
S.append(P("<b>Question.</b> Is the quoted range reported accurately, is the comparison with the EU limit correct, and "
           "does independent monitoring agree with the picture?"))
S.append(P("<b>Evidence.</b> We transcribed the Commission’s figures into <i>data/cc-047/</i>, with source and retrieval "
           "date, and ran <i>tools/cc-047-report/calc.py</i> to test the arithmetic (multiples of 50 mg/L; shares times 44 "
           "stations give whole numbers; depth classes add up to 30 points). We compared the ranges in the team’s 2025 "
           "abstract with the 2026 quotation."))
S.append(P("<b>Grades.</b> Laudi et al. (2026): B (observational study, monitoring network). Commission fiche: C (official "
           "statistics from national reporting). MaltaToday: D as evidence, used only as the locator. <b>Verdicts</b> "
           "follow the scale in Appendix A."))

S.append(CondPageBreak(120 * mm))
S.append(SectionHeading(3, "What the data show"))
S.append(KeepTogether([fig(FIG / "fig2_commission.png", width=CW * 0.98),
                       P("Figure 1. Malta’s 44 groundwater monitoring points by average nitrate, 2020–2023 "
                         "(European Commission, from EWA data).", cap)]))
S.append(P("Thirty points (68.2%) average 50 mg/L or more, six (13.6%) are at 40–49.99 mg/L, six at 25–39.99 and two "
           "below 25. The share at 50 or more rose from 63.6% (28 points) in 2016–2019. The Commission counts 35 "
           "nitrate pollution hotspots (79.5% of points) and notes that among points already at 50 or more, 88.9% were rising. "
           "The highest share is among shallow (5–15 m) wells at 83.3%. Whole-island averages per station are not "
           "published, so the Commission data cannot confirm “100–200 mg/L” for the eastern aquifer; they confirm that "
           "exceedance is the norm, not the exception."))
S.append(KeepTogether([fig(FIG / "fig1_ranges.png", width=CW * 0.98),
                       P("Figure 2. Nitrate ranges reported by the research team, against the 50 mg/L limit. Top bar: the "
                         "claim, second-hand. Other bars: the team’s 2025 abstract.", cap)]))

S.append(CondPageBreak(95 * mm))
S.append(SectionHeading(4, "Where the evidence points different ways"))
S.append(contested("Are the eastern aquifer’s nitrates 100–200 mg/L?", "BROADLY YES, AS A RANGE", GREENC,
                   "The quoted sentence (study, via MaltaToday) and the team’s 2025 abstract (75–200 mg/L under potato and "
                   "forage fields; central and eastern areas) are consistent. Commission data show most points at 50 or more.",
                   "The 2025 abstract gives 25–100 mg/L for the regional aquifer beneath the north-west perched aquifer, "
                   "so values differ widely by area. “Highest concentrations” are a range at the top, not a typical value "
                   "for every well.",
                   "The statement is accurate if read as the highest concentrations, as the paper words it. It would "
                   "overstate if read as the aquifer-wide level.", label_a="FOR", label_b="CAVEATS"))

S.append(CondPageBreak(90 * mm))
S.append(SectionHeading(5, "Testing the claim"))
verd = lambda t, c: chip(t, c, w=29 * mm)
S.append(std_table([
    [C("Sub-claim", cellh), C("Said by", cellh), C("What the evidence shows", cellh), C("Rating", cellh)],
    [C("<b>A.</b> Nitrate in the eastern areas of the main aquifer is 100–200 mg/L"), C("MaltaToday, quoting Laudi et al. [1]"),
     C("Matches the team’s 2025 abstract (75–200 mg/L under potato/forage fields). Full text not read."),
     verd("LIKELY", LG)],
    [C("<b>B.</b> That is two to four times the EU limit of 50 mg/L"), C("MaltaToday [1]"),
     C("100/50 = 2 and 200/50 = 4; 50 mg/L is the Nitrates Directive and drinking-water threshold."),
     verd("ACCURATE", GREENC)],
    [C("<b>C.</b> Groundwater nitrate is a widespread problem in Malta"), C("MaltaToday [1]"),
     C("30 of 44 monitoring points at 50 mg/L or more, 2020–2023; up from 63.6% [4]."), verd("CONFIRMED", GREENC)],
], [42 * mm, 24 * mm, 70 * mm, 34 * mm], valign="MIDDLE"))

S += [Spacer(1, 6 * mm), SectionHeading(6, "Verdict and requests for evidence"),
      verdict_box("Largely supported", "The figures are the study’s and independent monitoring agrees on the picture; "
                                       "the eastern range rests on a quotation we could not check. Confidence: moderate."),
      Spacer(1, 4 * mm)]
S.append(P("<b>Why.</b> The arithmetic is right, the limit is the right one, and the Commission’s review of Malta’s own "
           "monitoring shows exceedance at most points. <b>Why not Supported.</b> The central sentence is a "
           "second-hand quotation, and no independent dataset gives the eastern aquifer’s range. <b>What this verdict "
           "does not say.</b> It does not say that the aquifer water reaching taps exceeds 50 mg/L: public supply is "
           "blended and treated, and we did not test tap-water data."))
S.append(P("Evidence we are asking for", h2))
S.append(requests_list(["From the Energy and Water Agency: station-level nitrate data for the eastern Mean Sea Level Aquifer, "
                        "2020–2025.",
                        "From the authors or the journal: the paper’s page for the 100–200 mg/L sentence (open access)."]))
S += [Spacer(1, 4 * mm),
      callout([P("RIGHT OF REPLY", tag), P("Not needed for this verdict (maintainer rule of 5 October 2026).", small)],
              bg=AMBER_PALE, bar=AMBER)]
S += [CondPageBreak(60 * mm), Spacer(1, 6 * mm), SectionHeading(7, "Limitations")]
for l in ["We could not read the full text of Laudi et al. (2026); ScienceDirect refuses scripted access. The quoted sentence is "
          "second-hand, and the 2025 abstract is a conference abstract, not peer-reviewed in the same way.",
          "The Commission figures are per-station averages of annual means; they do not give an aquifer-wide mean.",
          "The study did not assess animal husbandry, which MaltaToday notes is a major nitrate source.",
          "We did not test whether groundwater levels translate to drinking-water levels."]:
    S.append(P("• " + l, bul))
S += [Spacer(1, 6 * mm), SectionHeading(None, "References")]
S += references([
    ("1", "Debono J. (13 February 2026). Potatoes and intensive farming: A slow-moving threat to Malta’s groundwater. "
          "<i>MaltaToday</i>.", "https://www.maltatoday.com.mt/news/national/139611/potatoes_and_intensive_farming_a_slowmoving_threat_to_maltas_groundwater"),
    ("2", "Laudi L., Dahan O., Sapiano M., Schembri M., Galea L., Busuttil E., Mangion J. & Turkeltaub T. (2026). Tracing "
          "nitrate fate in Malta’s hydrogeological system using an intensive vadose-groundwater monitoring network. "
          "<i>Journal of Hydrology: Regional Studies</i> 64:103162. doi:10.1016/j.ejrh.2026.103162. ◆ (abstract only).",
     "https://doi.org/10.1016/j.ejrh.2026.103162"),
    ("3", "Laudi L., Dahan O., Sapiano M., Schembri M. & Turkeltaub T. (2025). Using vadose zone data to determine "
          "agricultural impact on groundwater pollution. EGU General Assembly abstract EGU25-13344. "
          "doi:10.5194/egusphere-egu25-13344.", "https://doi.org/10.5194/egusphere-egu25-13344"),
    ("4", "European Commission (2026). Member State country fiche, Malta, on the implementation of Directive 91/676/EEC "
          "2020–2023, SWD(2026) 232 final, Part 20/27 (Council doc. 12018/26 ADD 19).",
     "https://data.consilium.europa.eu/doc/document/ST-12018-2026-ADD-19/en/pdf"),
    ("5", "MiŻien. Data and calculation: data/cc-047/; tools/cc-047-report/calc.py.", ""),
])
S.append(PageBreak())
S += appendix_a("A experiment · B observational study with a control or gradient · C review, guidance or "
                "official statistics · D assertion or anecdote. ◆ marks a source known only second-hand.")
S += [Spacer(1, 5 * mm)]
S += revision_log([("1.0", "5 Oct 2026", "First issue. Verdict Largely supported (moderate confidence); no right of reply needed.")])

build_report(Report(
    number="047", out=str(FIG / "report.pdf"), kicker="Water and groundwater",
    title_lines=["Nitrates in", "Malta’s main", "aquifer?"],
    subtitle_lines=["Testing a reported 100–200 mg/L, two to four", "times the EU limit"],
    quote_lines=["“…the highest concentrations of nitrate are observed in the", "eastern areas of the MSLA, ranging from 100 to 200 mg/L.”"],
    quote_size=13.5,
    attribution="Laudi et al., J. Hydrol.: Regional Studies, 2026, as quoted by MaltaToday, 13 Feb 2026.",
    context="MaltaToday: “two to four times higher than the EU safety limit of 50 mg/L”.",
    verdict="Largely supported", verdict_note="Figures match the study; eastern range second-hand",
    footer_lines=["Version 1.0  ·  5 October 2026", "Status: no right of reply needed",
                  "Prepared from published research.", "Repository: github.com/leandergrech/Mizien"],
    running_head="Nitrates in Malta’s groundwater", version="1.0", date="5 October 2026",
    status_note="no right of reply needed",
    pdf_title="Nitrates in Malta’s main aquifer? Claim Check 047",
    pdf_subject="Tests the reported nitrate range in the eastern Mean Sea Level Aquifer against the EU limit",
    story=S))
