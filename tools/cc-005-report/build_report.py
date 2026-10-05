"""Claim Check 005 report. Uses the shared Miżien report design."""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import *  # noqa: E402,F401

OUT = HERE / "out"
S = []

S += [SectionHeading(None, "TL;DR"), Spacer(1, 1 * mm),
      P("The European Commission’s 2025 Malta review says <b>92% of Maltese bathing waters were excellent</b>. "
        "That percentage matches the EEA’s 2023 season result: 80 of 87 sites. It is accurate for that reference "
        "year, but the Commission’s highlight does not state the year. The latest available EEA result when this "
        "check was prepared was 77 of 87 sites (88.5%) in 2025.", lead)]
S.append(key_points([
    ("The 92% figure checks out.", "The EEA classified 80 of 87 Maltese bathing sites as excellent in 2023: 92.0%."),
    ("It is not the latest season.", "In 2024, 80/87 were excellent; in 2025, 77/87 (88.5%) were excellent."),
    ("‘Excellent’ is a specific indicator.", "The classification uses E. coli and intestinal enterococci. It is not a general measure of marine ecosystem or chemical health."),
    ("Local pollution can coexist with the national result.", "Balluta Bay sites B08/B09 had a temporary health warning in 2024. This local episode does not change the 2023 national percentage."),
    ("Verdict: supported, with a date caveat.", "The Commission’s wording is accurate for 2023; it should not be presented as Malta’s current result."),
]))
S += [Spacer(1, 3 * mm), VerdictMeter(0), Spacer(1, 2 * mm),
      tiles([("92.0%", GREEN, "Excellent in 2023 (80/87 sites)"),
             ("92.0%", GREEN, "Excellent in 2024 (80/87 sites)"),
             ("88.5%", ORANGE, "Excellent in 2025 (77/87 sites)")]),
      Spacer(1, 3 * mm),
      up_down("None: Supported is the top of the scale. Only the date caveat remains; it would fall away if the "
              "Commission’s text named the 2023 season beside the 92% figure.",
              "A different EEA count for 2023; a source showing that the Commission meant a later season (the 2025 "
              "result was 88.5%); or evidence that its percentage used an incompatible denominator."), Spacer(1, 4 * mm)]
S += toc([("1", "Claim and sources"), ("2", "What the indicator measures"), ("3", "Season results"),
          ("4", "Local pollution and wastewater"), ("5", "Verdict and limits")])
S.append(PageBreak())

S += [SectionHeading(1, "Claim and sources"),
      P("The Commission’s <i>Environmental Implementation Review 2025: Malta</i> states: “Malta also shows "
        "excellent records under the Bathing Water Directive: 92% of Maltese bathing waters are of excellent "
        "quality.” The sentence appears in the report’s highlights. It does not name a reference year beside the "
        "percentage. The EEA data show that 92% corresponds to the 2023 season.")]
S.append(std_table([
    [C("Source", cellh), C("What it establishes", cellh), C("Use", cellh)],
    [C("European Commission, EIR 2025: Malta"), C("Exact 92% sentence; separate discussion of wastewater treatment."), C("Claim wording")],
    [C("EEA, Malta bathing-water profiles, 2023–2025"), C("Annual classifications, site counts and sampling figures."), C("Primary statistical series")],
    [C("Environmental Health Directorate, Balluta Bay report (2024)"), C("Temporary warning at sites B08/B09 and when it was lifted."), C("Local context")],
    [C("CJEU, Commission v Malta, C-304/23 (2024)"), C("Urban wastewater treatment obligations for named agglomerations."), C("Separate compliance issue")],
], [48 * mm, 91 * mm, 41 * mm]))
S += [Spacer(1, 4 * mm),
      callout([P("FAIRNESS NOTE", tag), P("Short-term pollution warnings and wastewater-treatment problems matter to public health "
        "and environmental management. They do not, by themselves, disprove a national multi-season bathing-water "
        "classification for a particular year. This check assesses the dated statistic, not whether every beach is "
        "always clean or whether Malta’s marine environment is healthy overall.", small)], bg=AMBER_PALE, bar=AMBER),
      SectionHeading(2, "What the indicator measures"),
      P("Under the Bathing Water Directive, classification is based on measured concentrations of two faecal-indicator "
        "bacteria: <i>Escherichia coli</i> and intestinal enterococci. The EEA’s country profile reports site "
        "classifications and samples. “Excellent” is a meaningful result for those parameters and the directive’s "
        "monitoring framework; it does not cover every pollutant, every day, or all dimensions of marine ecological "
        "and chemical status."),
      P("The directive’s classification is not a guarantee that no short-lived contamination event occurs. A site can "
        "receive a temporary warning and still be included in a national multi-year classification. The timeframe "
        "and denominator should accompany the percentage when it is repeated.")]

S += [PageBreak(), SectionHeading(3, "What the season data show")]
S.append(std_table([
    [C("Bathing season", cellh), C("Excellent", cellh), C("Other classifications", cellh), C("Sites", cellh), C("Samples", cellh)],
    [C("2023"), C("<b>80 (92.0%)</b>"), C("3 good; 4 sufficient"), C("87"), C("2,021")],
    [C("2024"), C("<b>80 (92.0%)</b>"), C("3 good; 4 sufficient"), C("87"), C("2,107")],
    [C("2025"), C("<b>77 (88.5%)</b>"), C("8 good; 2 sufficient"), C("87"), C("2,100")],
], [35 * mm, 31 * mm, 57 * mm, 24 * mm, 33 * mm]))
S += [Spacer(1, 4 * mm),
      callout([P("READING THE SERIES", tag), P("The 2023 and 2024 excellent shares were both 92%. The 2025 share was 88.5%. "
        "All 87 sites in 2025 were classified at least sufficient; none was classified poor or left unclassified. "
        "The 2025 result is the latest annual profile available for this check.", small)], bg=PALE, bar=GREEN),
      SectionHeading(4, "Local pollution and wastewater")]
S.append(P("The Environmental Health Directorate’s Balluta Bay report records a temporary warning and closure at sites "
           "B08 and B09 beginning in late May 2024. The report describes microbial contamination and foul water from a "
           "storm-water tunnel. The warning was lifted on 12 August after three consecutive samples fell below the "
           "relevant thresholds. This was a serious local event over a defined period; it does not alter the count of "
           "sites classified excellent for 2023."))
S.append(P("In Case C-304/23, the Court of Justice found failures to comply with urban wastewater treatment obligations "
           "for named agglomerations. That judgment is not a bathing-water classification, and it does not show that "
           "the EEA’s 2023 result was false. The Commission’s own review reports both bathing-water quality and "
           "wastewater-treatment concerns under separate headings."))

S += [SectionHeading(5, "Verdict and limits"),
      callout([P("SUPPORTED · HIGH CONFIDENCE", tag), P("The EEA’s 2023 figures confirm 80 excellent sites out of 87, "
        "which rounds to the Commission’s 92%. The figure is accurate for 2023. The 2025 result is 88.5%, so the "
        "year should be stated whenever the 92% figure is used as a description of Malta’s bathing-water quality.", small)],
        bg=PALE, bar=GREEN),
      P("This verdict covers only the quoted 2023 statistic. The EEA classification uses data reported by Malta; this "
        "check is not an independent resampling programme. It does not assess chemical pollutants, marine ecological "
        "status, or health outcomes beyond the directive’s microbiological classification."),
      P("Right of reply has not been sought, as directed by the maintainer. The report remains a draft for maintainer "
        "review.", small),
      Spacer(1, 4 * mm), SectionHeading(None, "References")]
for n, txt in enumerate([
    "European Commission, <i>Environmental Implementation Review 2025: Malta</i>. Exact claim wording and separate wastewater discussion.",
    "European Environment Agency, Malta bathing-water profiles for seasons 2023, 2024 and 2025. Site classifications, sample counts and parameters. The 2023 sample count is from the EEA’s WISE Bathing Water Directive dataset (DiscoData, retrieved 5 October 2026; data/cc-005/).",
    "Environmental Health Directorate, <i>Report on the temporary closure at B08 and B09 Balluta Bay</i> (2024).",
    "Court of Justice of the European Union, <i>Commission v Malta</i>, Case C-304/23, ECLI:EU:C:2024:906 (17 October 2024).",
], 1):
    S.append(P(f"{n}. {txt}", ref))

S += [Spacer(1, 4 * mm)]
S += revision_log([
    ("1.0", "2 Oct 2026", "First issue. Right of reply not sought, at the maintainer’s direction."),
    ("1.1", "5 Oct 2026", "Corrections: (1) the ‘what would move the verdict’ boxes were reversed. ‘Up’ listed conditions "
     "that would lower the verdict, and ‘down’ cited a newer season at 92% or more. Now: up, none (Supported is the "
     "top of the scale; naming the 2023 season would remove the date caveat); down, a different 2023 count, a later "
     "intended season or an incompatible denominator. (2) Balluta Bay warning start: ‘31 May 2024’ → ‘late May "
     "2024’. Our bibliography gave 21 May, and news reports date the two sites’ warnings ten days apart; the "
     "primary report could not be re-opened to settle it. "
     "(3) 2023 sample count: ‘—’ → 2,021 (EEA WISE dataset). (4) Page footer: ‘pending right of reply’ → ‘right "
     "of reply not sought’, matching the maintainer’s decision. Verdict and confidence unchanged."),
])

build_report(Report(number="005", out=str(OUT / "report.pdf"), kicker="Bathing water, Malta",
    title_lines=["92% excellent", "bathing water"],
    subtitle_lines=["A public claim, tested against EEA season data", "A dated result is not a current trend."],
    quote_lines=["“92% of Maltese bathing waters are", "of excellent quality.”"],
    attribution="European Commission, Environmental Implementation Review 2025",
    context="The percentage matches 80 of 87 sites in the EEA’s 2023 season data.",
    verdict="Supported", verdict_note="Accurate for 2023; date it.",
    footer_lines=["Draft for maintainer review", "Public data · Right of reply not sought, per maintainer direction"],
    running_head="92% excellent bathing water", version="1.1", date="5 October 2026",
    status_note="right of reply not sought",
    pdf_title="Claim Check 005 – 92% excellent bathing water",
    pdf_subject="Malta bathing water classification, seasons 2023 to 2025", story=S))
