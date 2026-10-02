"""Claim Check 002 report. Run data/cc-002/calc.py first."""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import *  # noqa: E402,F401

OUT = HERE / "out"
S = []
S += [SectionHeading(None, "TL;DR"), Spacer(1, mm),
      P("ERA's arithmetic checks out: 624 non-protected specimens plus 54 protected trees equals 678; 624 of 678 is 92.04%; and ten new indigenous trees for each of 54 protected removals equals 540. Another 348 specimens are assigned to transplantation.", lead)]
S.append(key_points([
    ("The figures describe a plan.", "They are ERA's announced categories and conditions, not completed removal, planting or transplant results."),
    ("The 92% is a status label.", "It describes specimens classified as non-protected; it is not a measure of ecological value or habitat function."),
    ("The transplant group is separate.", "ERA says 348 trees are to be transplanted; all but seven are protected. Failed transplants trigger a separate 10:1 planting condition."),
    ("Tree count is not ecological equivalence.", "Species, size, condition, provenance, survival, aftercare and time to maturity all matter."),
    ("Verdict: largely supported.", "The announced numbers are internally consistent. Ecological compensation in outcome has not been demonstrated."),
]))
S += [Spacer(1, 3 * mm), VerdictMeter(1), Spacer(1, 1 * mm),
      std_table([
          [C("ERA category", cellh), C("Count", cellh), C("What the arithmetic shows", cellh)],
          [C("Non-protected removal group"), C("624"), C("624 / 678 = 92.04%" )],
          [C("Protected removals"), C("54"), C("54 × 10 = 540 new indigenous trees" )],
          [C("Separate transplant group"), C("348"), C("341 protected; seven not protected" )],
      ], [52 * mm, 22 * mm, CW - 74 * mm]),
      Spacer(1, 3 * mm),
      up_down("Publish the final species-level schedule, approved planting plan and site-specific monitoring protocol, followed by transplant survival and habitat indicators at years 1, 3 and 5.",
              "Evidence that the figures do not describe the 7/11 August 2026 ERA plan, or that the released categories omit or double-count the stated interventions."),
      Spacer(1, 4 * mm)]
S += toc([("1", "What ERA said"), ("2", "Rechecking the counts"), ("3", "What ecological compensation means"),
          ("4", "What the science can transfer"), ("5", "Verdict and limits"), ("6", "Sources")])
S.append(PageBreak())

S += [SectionHeading(1, "What ERA said"),
      P("The exact wording comes from ERA's 11 August 2026 press release, which says that 54 protected trees “will be removed” and that 540 new indigenous trees will be planted. The authority says a compensation plan must be submitted for approval before implementation. It separately describes 624 non-protected specimens for removal and 348 trees for transplantation [1–2]."),
      callout([P("SCOPE OF THIS CHECK", tag),
               P("We check the public tree counts and the ecological meaning of the planned compensation. We do not assess the permit's legal merits or any tribunal proceedings.", lead)], bg=PALE, bar=GREEN),
      Spacer(1, 2 * mm),
      P("ERA's 7 August clarification states that all but seven of the 348 transplants are protected. The 10:1 condition for failed transplants is separate from the 540 new trees attached to the 54 protected removals [1].")]

S += [Spacer(1, 3 * mm), SectionHeading(2, "Rechecking the counts"),
      P("We transcribed only the regulator's published figures and recalculated the totals and ratios. The input table records the source URL and access date; `python data/cc-002/calc.py` writes `data/cc-002/checks.csv`."),
      std_table([
          [C("Calculation", cellh), C("Result", cellh), C("Interpretation", cellh)],
          [C("624 + 54"), C("678 specimens"), C("Removal categories sum to the stated total.")],
          [C("624 / 678 × 100"), C("92.04%"), C("Rounds to ERA's 92%.")],
          [C("54 × 10"), C("540 trees"), C("Matches the announced planting ratio.")],
          [C("348 - 7"), C("341 trees"), C("All but seven transplants are stated to be protected.")],
      ], [45 * mm, 31 * mm, CW - 76 * mm]),
      Spacer(1, 3 * mm),
      P("The 624 specimens are not all necessarily mature trees: ERA describes shrubs and landscaping specimens and says 467 are oleanders. A MaltaToday report quoting the case-officer report gives 468 oleanders. We flag the one-specimen discrepancy and avoid using that species breakdown to quantify ecological effects [2, 7]."),
      P("An NGO's earlier “around 800 trees” figure was reported before the later ERA clarification. The cited report attributes it to the NGO and does not give a species inventory or counting method. It is not like-for-like with ERA's later removal categories; nor should the separate 348 transplants be counted as removals [8].")]

S += [PageBreak(), SectionHeading(3, "What ecological compensation means"),
      P("A replacement ratio answers “how many new planting units are required for each removed specimen?” It does not answer “how much habitat function will return, and when?” The latter depends on which species are planted, their provenance and size, establishment and survival, future growth, site conditions, and how the affected habitat is measured."),
      P("The phrase “not protected” describes a protection classification. It does not establish that every specimen has negligible ecological value. Conversely, “protected” does not alone quantify the ecological contribution of a particular tree. A fair ecological assessment needs species, condition, age or size, habitat and location information."),
      P("The 2026 Comino flora inventory combines historical records and repeated field surveys. It documents 490 vascular taxa, including 58 strictly protected taxa and 21 endemic or subendemic taxa. The authors distinguish alien plants that are widespread from the smaller set effectively invasive on Comino. They also describe planted trees and alien species as habitat pressures in some settings [3]."),
      contested("Does the 10:1 ratio demonstrate a net ecological gain?", "PLANTING REQUIREMENT, OUTCOME UNMEASURED", AMBER,
        "ERA specifies 540 new indigenous trees for 54 protected trees removed, plus 10 new trees for each transplant that fails. This is a concrete, auditable planting condition [1–2].",
        "The public release does not give the final species-and-size plan, survival observations, habitat metrics or the time required for new trees to provide comparable structure and function. A multiplication of plants is not a measured habitat balance.",
        "The ratio supports the factual statement about the authority's plan. It cannot, on its own, substantiate that ecological losses are fully offset."),
      Spacer(1, 3 * mm),
      P("The public data also do not yet provide a reconciled, species-level inventory for the 624 non-protected specimens. For that reason, this report does not treat all of them as invasive, disposable, or equivalent in ecological function.")]

S += [P("HV Hospitality says it has been growing mother plants propagated from seeds native to Comino and Gozo in an on-site nursery since 2023, and that the transplanted specimens will be cared for there [9]. This is relevant evidence of the developer's stated preparation, but the page gives no public stock list, specimen-level condition record, survival data or independently verified nursery inventory. It therefore does not close the outcome-evidence gap.")]

S += [PageBreak(), SectionHeading(4, "What the science can transfer"),
      P("A review of plant-translocation records in Italy analysed 178 cases. Survival data were available for only about 40% of them. Outcomes varied with source material, site protection and suitability, planting approach, preparation and aftercare [4]. This supports the need for well-designed methods and monitoring; it is not a survival estimate for the 348 Comino specimens."),
      P("A controlled field comparison followed eight transplanted mature olive trees and eight controls over two years. Even after heavy pruning, irrigation and fertilisation, the transplanted trees showed substantially lower photosynthesis and transpiration and other physiological changes [5]. The small study involved olive trees in another environment. It shows that survival alone may conceal stress, not what proportion of Comino trees will survive."),
      P("Evidence on alien-plant removal is also context-dependent. A controlled before-after study in the Azores found later gains in native seed and food-web indicators after removal, but also immediate declines in native plants in one design and responses favouring some alien seedlings [6]. It cannot establish the outcome for Comino without knowing the species, habitat and restoration that follow removal."),
      P("The evidence therefore supports conditional conclusions: targeted removal can be part of restoration, and transplanted plants can survive, but neither outcome follows automatically from a tree count. Species-specific monitoring on Comino is needed to show what happened.")]

S += [Spacer(1, 2 * mm), SectionHeading(5, "Verdict, limits and evidence needed"),
      verdict_box("Largely supported", "ERA's published counts check out; ecological replacement remains unmeasured."),
      Spacer(1, 3 * mm),
      P("The figures in ERA's August statements reconcile: 624 + 54 = 678, 624/678 rounds to 92%, and 54 × 10 = 540. The 348 transplant group is separately described, with all but seven protected. That supports the claim as a description of the plan. Confidence is moderate because we have not inspected the complete permit annex, and because the source reports intended conditions rather than observed outcomes."),
      P("This verdict does not say the scheme will fail. It says the arithmetic and promise are not outcome evidence. The ecological effect could be better or worse than the count suggests, depending on species, transplant success, site, aftercare and habitat response. The developer reports nursery propagation since 2023, but its public page does not publish stock or survival records [9]."),
      P("Evidence that would settle the ecological question", h2),
      requests_list([
          "The full species-level schedule, including condition, size and location for removal and transplant groups.",
          "The approved planting design: species, local provenance, stock size, microsites and aftercare.",
          "Public survival and condition results at years 1, 3 and 5, including failed transplants and replacement plantings.",
          "Vegetation and habitat monitoring that tests native biodiversity and function at intervention and comparison sites.",
      ]),
      Spacer(1, 2 * mm),
      P("<b>Right of reply.</b> Not sought in this draft, at the maintainer's direction.", small),
      P("<b>Limitations.</b> The complete permit annex and final method statements were not available for this review. The transplant and restoration studies are scientifically relevant but not site-specific substitutes for Comino monitoring.", small),
      PageBreak(), SectionHeading(6, "Sources"),
      *references([
          (1, "ERA, Clarification on Comino, 7 August 2026.", "https://era.org.mt/press-releases/clarification-on-comino/"),
          (2, "ERA, ERA clarifies environmental measures linked to the Comino Hotel project, 11 August 2026.", "https://era.org.mt/press-releases/era-clarifies-environmental-measures-linked-to-the-comino-hotel-project/"),
          (3, "Mifsud, S., Pavon, D. & Médail, F. (2026), PhytoKeys 272:217–282, doi:10.3897/phytokeys.272.184198.", "https://doi.org/10.3897/phytokeys.272.184198"),
          (4, "D'Agostino, M. et al. (2024), Conservation Biology 38(4):e14233, doi:10.1111/cobi.14233.", "https://doi.org/10.1111/cobi.14233"),
          (5, "Dror, D. et al. (2020), Agricultural and Forest Meteorology 295:108192, doi:10.1016/j.agrformet.2020.108192.", "https://doi.org/10.1016/j.agrformet.2020.108192"),
          (6, "Heleno, R. et al. (2010), Ecological Applications 20(5):1191–1203, doi:10.1890/09-1384.1.", "https://doi.org/10.1890/09-1384.1"),
          (7, "MaltaToday, Fact-check: What the Comino hotel project means for the island's trees, 8 August 2026 (secondary; 468 oleanders).", "https://www.maltatoday.com.mt/news/national/143679/factcheck_what_the_comino_hotel_project_means_for_the_islands_trees"),
          (8, "MaltaToday, ERA approval paves way for uprooting of 800 trees for proposed Comino hotel, 7 August 2026 (secondary account of stakeholder statements).", "https://www.maltatoday.com.mt/environment/planning/143667/era_approves_preliminary_works_for_proposed_comino_hotel"),
          (9, "HV Hospitality, Comino project page (stakeholder account of nursery propagation and planned transplant care; no public inventory or outcome data).", "https://hilihospitality.com/comino/"),
      ]),
      Spacer(1, 3 * mm), P("Version 1.1 · 3 October 2026 · Draft pending right of reply · Calculations: data/cc-002/checks.csv · Generator: tools/cc-002-report/build_report.py", cap)]

build_report(Report(
    number="002", out=str(OUT / "report.pdf"), kicker="Land and trees, Malta",
    title_lines=["What does ten", "trees compensate?"],
    subtitle_lines=["Comino's removal, transplant and replacement", "figures checked against the science"],
    quote_lines=["“54 protected trees will be removed”", "“540 new indigenous trees”"],
    attribution="Environment and Resources Authority, 11 August 2026",
    context="Comino hotel site · planned removal and transplantation",
    verdict="Largely supported", verdict_note="Plan maths checks out; ecological outcome is open.",
    footer_lines=["Miżien · independent, science-first fact-checking", "Draft for review · right of reply remains with the maintainer"],
    running_head="Comino tree compensation", version="1.1", date="3 October 2026",
    pdf_title="Miżien Claim Check 002 – What does ten trees compensate?",
    pdf_subject="Comino tree-removal counts, transplanting and ecological compensation",
    story=S,
))
