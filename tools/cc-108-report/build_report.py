"""Claim Check 108 report. Run calc.py and figures.py first. Output: out/report.pdf"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import *  # noqa: E402,F401

FIG = HERE / "out"
S = []

# ================================================================== TL;DR
S += [SectionHeading(None, "TL;DR"), Spacer(1, 1 * mm),
      P("The Energy and Water Agency’s Green Paper of November 2023 [1] proposes that groundwater sources run by the "
        "<b>Water Services Corporation (WSC)</b> stay outside the new abstraction licensing framework, “given that the "
        "Corporation is moving towards the achievement of a net-zero impact on the groundwater environment through its "
        "operations”, and that WSC’s annual abstraction “will be capped at a maximum level of 14 Mm³ up to 2030”. We tested "
        "both statements against WSC’s production reports, Eurostat and the EU’s groundwater-body assessments.", lead)]
S.append(key_points([
    ("The cap is not tight.",
     "WSC groundwater production was 11.5 million m³ in 2025 [6, 7], 82% of the proposed 14. The highest year we read "
     "(13.5 million m³ in 2016) was already 96% of it, so the ceiling sits about 4% above that year and 21% above 2025."),
    ("“Net-zero impact” has no definition, baseline or date in the Green Paper.",
     "Sapiano (Energy and Water Agency, 2020) describes it as giving back to the aquifer environment “at least, as much water” "
     "as WSC abstracts, by recharge and by supplying treated wastewater in place of groundwater [2]. We found no published "
     "balance."),
    ("The give-back we can count is small.",
     "New Water (treated wastewater) was 1.6 million m³ in 2022 [1]: 13% of WSC’s abstraction that year, and meant "
     "for crop irrigation rather than to replace WSC’s own boreholes. WSC’s stated maximum of 7 million m³ [3] would be 61% of "
     "2025 abstraction, before any recharge, which no source we read quantifies."),
    ("The aquifers are still in poor quantitative status.",
     "The Green Paper says good status “will not be achieved” for the main sea-level bodies [1]."),
    ("Pledge label: not measurable (as of 11 October 2026).",
     "The aim cannot be checked as worded; the cap can, and is met so far. A gap in what was published, not a finding of failure."),
]))
S += [Spacer(1, 4 * mm), VerdictMeter(0, scale="pledge"), Spacer(1, 3 * mm),
      tiles([("11.5 million m³", GREEN, "WSC groundwater production, 2025 (proposed cap: 14)"),
             ("−15%", GREEN, "WSC production, 2025 vs 2016 (13.5 million m³)"),
             ("13%", ORANGE, "New Water output in 2022 against WSC’s abstraction that year"),
             ("34%", BLUE, "of national fresh groundwater abstraction (2024) is WSC’s, outside the proposed licensing")]),
      Spacer(1, 4 * mm),
      up_down("A definition of the net-zero balance (what is given back, where, measured how), a baseline and a date, "
              "with annual figures; or the adopted rule, with the 14 million m³ cap in force and reported against.",
              "Annual WSC abstraction above 14 million m³, or a published balance showing give-back far below abstraction.",
              heads=("What would make it measurable or on track", "What would count against it")),
      Spacer(1, 2 * mm)]
S += toc([("1", "The statements and their sources"), ("2", "Method"), ("3", "The 14 million m³ cap"),
          ("4", "‘Net-zero impact’: what can be counted"), ("5", "Testing the statements"),
          ("6", "Pledge label and requests for evidence"), ("7", "Limitations")])
S.append(PageBreak())

# ================================================================== 1
S.append(SectionHeading(1, "The statements and their sources"))
S.append(P("Our candidate record combined statements from several documents, and some of its wording came from search "
           "summaries. We read the Green Paper in full and two WSC pages, and separate what each says."))
S.append(std_table([
    [C("Source", cellh), C("Wording", cellh), C("Status", cellh)],
    [C("<b>Energy and Water Agency</b>, Green Paper on the Regulation of Groundwater Abstraction in the Maltese "
       "Islands, Nov 2023, p. 12 [1]"),
     C("“The Groundwater Abstraction Licensing Framework will not be applicable to groundwater sources operated by the "
       "Water Services Corporation, given that the Corporation is moving towards the achievement of a net-zero impact on "
       "the groundwater environment through its operations. Annual groundwater abstraction levels by the Water Services "
       "Corporation will be capped at a maximum level of 14 Mm³ up to 2030.”"),
     C("<b>Primary wording</b> (verbatim). A proposal in a consultation document; outcome not found")],
    [C("<b>Sapiano</b> (Energy and Water Agency), <i>Acque Sotterranee</i> 2020, p. 31 [2]"),
     C("Describes the concept, citing WSC 2018: the utility gives back “at least, as much water as the groundwater it "
       "abstracts … through intended and unintended aquifer recharge and the supply of treated wastewaters to be used in "
       "substitution of groundwater”."),
     C("Agency author’s description of WSC’s aim")],
    [C("<b>WSC</b> news release, 2 April 2019 [3]"),
     C("Says the project will cut groundwater abstraction “by 4 billion litres per year” and make “A maximum of 7 billion "
       "litres a year of recycled water” available to agriculture. Checked separately in Claim Check 039."),
     C("Primary; context")],
    [C("<b>Sustain Europe</b>, unsigned article, 6 Nov 2018 [5]"),
     C("Says WSC “will be giving back to the environment, at least an equivalent volume of the abstracted natural "
       "freshwater resources”. The article does not name its source."),
     C("Outlet text; speaker not named, not rated")],
], [44 * mm, 100 * mm, 26 * mm]))
S += [Spacer(1, 4 * mm),
      callout([P("WHAT THIS CHECK DOES NOT COVER", tag),
               P("We did not find the “give back … an equivalent volume” wording on either WSC page we read [3, 4]; the "
                 "candidate record took it from a search summary, and it is not rated here as WSC’s statement. The "
                 "Green Paper is a proposal: we test its two claims about WSC, not the wisdom of exempting WSC from "
                 "licensing. Claim Check 039 tests WSC’s 4 billion litre pledge; Claim Check 009 its 2025 production.",
                 small)], bg=AMBER_PALE, bar=AMBER),
      Spacer(1, 4 * mm)]

# ================================================================== 2
S.append(SectionHeading(2, "Method"))
S.append(P("<b>Question.</b> Is WSC’s groundwater abstraction within the proposed cap, and is there evidence that it is "
           "“moving towards” a net-zero impact on the groundwater environment? Can either be checked as worded?"))
S.append(P("<b>Cap.</b> We compare the 14 million m³ with WSC’s reported groundwater production: 2016 from its 2016 "
           "annual report [6] and 2022–2025 from the 2025 report’s production chart [7], transcribed for Claim Check 009. "
           "Years 2017–2021 were not read. Eurostat’s public-supply groundwater abstraction (2024, estimated) [8] is shown "
           "for comparison; it measures something different and runs about 1.2 million m³ above WSC’s own 2024 figure."))
S.append(P("<b>Net-zero impact.</b> We take the concept as Sapiano [2] describes it and count what can be counted: WSC’s "
           "own abstraction, the New Water volume (Green Paper [1]; WSC [3]) and national abstraction and recharge "
           "(Eurostat [8]). Aquifer status is from the EEA’s WISE reporting of the third river basin management plan cycle "
           "(status assessed 2021) [9]. Code: <i>tools/cc-108-report/calc.py</i>; results in <i>data/cc-108/checks.csv</i>."))
S.append(P("<b>Grades.</b> The Green Paper and WSC reports are self-reported or agency documents (C); Eurostat figures are "
           "official statistics flagged as estimates (C); our arithmetic is an order-of-magnitude check and is labelled so."))

# ================================================================== 3
S.append(PageBreak())
S.append(SectionHeading(3, "The 14 million m³ cap"))
S.append(fig(FIG / "fig1_cap.png"))
S.append(P("Figure 1. WSC groundwater production (boreholes and pumping stations, Malta and Gozo) against the proposed cap.", cap))
S.append(std_table([
    [C("Measure", cellh), C("Value", cellh), C("Source", cellh)],
    [C("Proposed cap for WSC, up to 2030"), C("14.0 million m³ a year"), C("Green Paper p. 12 [1]")],
    [C("WSC groundwater production 2016 / 2022 / 2023 / 2024 / 2025"), C("13.51 / 12.68 / 13.16 / 13.09 / 11.54"),
     C("WSC AR 2016, AR 2025 [6, 7]")],
    [C("Share of the cap, same years"), C("96% / 91% / 94% / 94% / <b>82%</b>"), C("calculated")],
    [C("Cap above the highest year read (2016)"), C("+3.7%"), C("calculated")],
    [C("Cap above 2025 production"), C("+21% (2.46 million m³ of headroom)"), C("calculated")],
    [C("Eurostat public-supply groundwater abstraction, 2024"), C("14.28 million m³ (estimated)"), C("Eurostat env_wat_abs [8]")],
    [C("WSC share of national fresh groundwater abstraction, 2024"), C("34% (13.09 of 38.46 million m³)"), C("calculated [7, 8]")],
], [78 * mm, 55 * mm, 37 * mm]))
S.append(P("The 2025 chart values carry the small internal differences recorded for Claim Check 009.", cap))
S.append(callout([P("READING THE NUMBERS", tag),
                  P("WSC has stayed below 14 million m³ in every year we read, so the cap is met so far. It would also have "
                    "been met in all of them without any effort: the ceiling is close to the highest of those years and well "
                    "above the latest. The Green Paper’s own text adds a reason for care: its Figure 5 shows WSC abstraction "
                    "falling since 1990, but “the decrease also reflects the general degradation in the quality of the aquifer "
                    "systems” (p. 6) [1], so lower pumping is not by itself evidence of lower impact. Eurostat’s public-supply "
                    "series is above 14 in 2024, but we cannot tell what it includes beyond WSC (Claim Check 009 found the same "
                    "gap of about 1 million m³), so we do not read it as a breach.", small)], bg=BLUE_PALE, bar=BLUE))
S.append(Spacer(1, 3 * mm))
S.append(P("Fairness to WSC and the Agency", h2))
for t in ["• WSC’s production fell about 15% from 2016 to 2025 while its total production rose about 23% (Claim Check 039): "
          "groundwater’s share of its supply fell from 42% to 29%.",
          "• The Green Paper proposes the cap and the exemption; it is a consultation document. We did not find the "
          "adopted regulation, so the cap is tested as a stated intention, not as a legal limit.",
          "• The Green Paper also says WSC’s abstraction is “fully accounted for” and that its stations are monitored for "
          "salinity (p. 5) [1]. That is context for the exemption, not the reason the Green Paper gives for it."]:
    S.append(P(t, bul))

# ================================================================== 4
S.append(CondPageBreak(95 * mm))
S.append(SectionHeading(4, "‘Net-zero impact’: what can be counted"))
S.append(fig(FIG / "fig2_giveback.png"))
S.append(P("Figure 2. What we can count of the “give-back”, against WSC’s 2025 groundwater production.", cap))
S.append(std_table([
    [C("Item", cellh), C("Value", cellh), C("Source", cellh)],
    [C("New Water produced in 2022 (combined; intended for crop irrigation)"), C("1.6 million m³ (13% of WSC’s 2022 abstraction)"), C("Green Paper p. 3 [1]; calculated")],
    [C("New Water maximum stated by WSC, 2019"), C("7 million m³ a year (61% of WSC’s 2025 abstraction)"), C("WSC release [3]; calculated")],
    [C("Aquifer recharge from WSC operations (leaks, sewer exfiltration)"), C("not quantified in any source we read"), C("—")],
    [C("National fresh groundwater abstraction 2024 against estimated recharge"), C("38.5 vs 41.5 million m³ (93%), both estimates"), C("Eurostat [8]")],
    [C("Groundwater bodies in poor quantitative status (3rd cycle, assessed 2021)"), C("4 of 15, including both main sea-level bodies"), C("EEA WISE [9]")],
    [C("Groundwater bodies in poor chemical status (same)"), C("15 of 15"), C("EEA WISE [9]")],
], [70 * mm, 60 * mm, 40 * mm]))
S.append(P("What the counting shows", h2))
for t in ["• <b>Direction, yes; balance, not shown.</b> WSC’s abstraction is lower than in 2016 and treated wastewater is "
          "being supplied, so “moving towards” is consistent with the numbers. But on Sapiano’s definition [2] the give-back "
          "must equal what is abstracted, and the quantified part is far from it: even at WSC’s stated maximum for New "
          "Water, 4.5 million m³ of 2025 abstraction would be unmatched, unless unquantified recharge makes up the difference.",
          "• <b>New Water mostly replaces other people’s groundwater.</b> It is meant for crop irrigation [1], so it relieves the "
          "aquifer by displacing farm boreholes, not WSC’s own. That fits Sapiano’s definition, which counts treated "
          "wastewater “used in substitution of groundwater”, but it means the accounting is across users, and no source "
          "we read does it.",
          "• <b>The aquifer’s condition does not settle it either way.</b> The sea-level bodies are in poor quantitative "
          "status, and the Green Paper says good status “will not be achieved” for them (p. 10) [1]. The Green Paper "
          "names over-abstraction as the cause of saline intrusion (p. 2) [1], and agriculture is the largest abstractor [8]; the "
          "status data do not isolate WSC’s share, and residence times of years to decades (Claim Check 009) mean one year cannot show recovery.",
          "• <b>No target date, no metric.</b> The Green Paper says “moving towards”; it gives no year for reaching net zero "
          "and no indicator that would show it."]:
    S.append(P(t, bul))

# ================================================================== 5
S.append(CondPageBreak(80 * mm))
S.append(SectionHeading(5, "Testing the statements"))
verd = lambda t, c: chip(t, c, w=29 * mm)
S.append(std_table([
    [C("Sub-claim", cellh), C("Said by", cellh), C("What the evidence shows", cellh), C("Rating", cellh)],
    [C("<b>A.</b> WSC’s annual groundwater abstraction “will be capped at a maximum level of 14 Mm³ up to 2030”"),
     C("Energy and Water Agency [1]"),
     C("Production was 11.5 million m³ in 2025 (82% of the cap) and below 14 in every year read (highest 13.5 in 2016). "
       "The cap is 4% above that highest year; a proposal, adoption not found."), verd("WITHIN CAP SO FAR", GREENC)],
    [C("<b>B.</b> WSC “is moving towards the achievement of a net-zero impact on the groundwater environment”"),
     C("Energy and Water Agency [1]"),
     C("No definition, baseline or date. Abstraction is 15% below 2016, but part of the fall reflects aquifer degradation [1]; "
       "New Water (1.6 million m³ in 2022) and unquantified recharge do not yet show a balance; sea-level aquifers still poor."),
     verd("NOT MEASURABLE AS WORDED", GREY)],
], [46 * mm, 22 * mm, 68 * mm, 34 * mm], valign="MIDDLE"))

# ================================================================== 6
S += [Spacer(1, 6 * mm), SectionHeading(6, "Pledge label and requests for evidence"),
      verdict_box("Not measurable", "As of 11 October 2026. The net-zero aim has no definition, baseline or date; "
                  "the cap is met so far but sits above recent use."), Spacer(1, 4 * mm)]
S.append(P("<b>Why.</b> The Green Paper states an intention (“moving towards”) and a proposed cap. The cap can be "
           "checked, and is met so far. The net-zero aim, which is the reason the Green Paper gives for the exemption, "
           "has no indicator, so delivery cannot be shown or refuted. A target is not a statement of fact, so we do not "
           "call it false; we label it <i>Not measurable</i> (Appendix A lists the six pledge labels)."))
S.append(P("<b>What this label does not say.</b> It does not say WSC is failing or that the exemption is wrong. Lower "
           "abstraction and wastewater reuse are sound aims. A checkable version would read: <i>“From [year], WSC’s "
           "groundwater abstraction minus the volume it returns to or saves from the aquifer, measured as [method], "
           "will be zero or negative by [date].”</i>"))
S.append(CondPageBreak(45 * mm))
_req = [P("Evidence we are asking for", h2), requests_list([
    "From the Energy and Water Agency: the definition, baseline year, date and indicator behind “net-zero impact on the "
    "groundwater environment”, and whether the Green Paper’s cap and exemption were adopted.",
    "From WSC: annual groundwater abstraction by source since 2014, and the annual volume of New Water supplied and where "
    "it is used.",
    "From WSC and the Agency: any estimate of unintended aquifer recharge from the networks, and the 2018 framework "
    "document that Sapiano [2] cites.",
    "From the Agency: how the 14 million m³ is measured (metered abstraction or production) and how it relates to "
    "Eurostat’s public-supply series.",
]), Spacer(1, 4 * mm),
      callout([P("RIGHT OF REPLY", tag),
               P("Before wider circulation this draft should be sent to the Energy and Water Agency and the Water Services "
                 "Corporation with a fixed deadline (suggested 14 days). Responses will be appended and the label revisited.",
                 small)], bg=AMBER_PALE, bar=AMBER)]
S.append(KeepTogether(_req))

# ================================================================== 7
S += [Spacer(1, 6 * mm), SectionHeading(7, "Limitations")]
for l in ["The Green Paper is a consultation proposal. We did not find the White Paper, regulation or any report on whether "
          "the cap and exemption were adopted (a web search of 11 Oct 2026 found only the Green Paper, its consultation "
          "pages and comment letters; ERA and legislation.mt were not searched in full).",
          "WSC’s 2016 and 2025 production series come from different reports; we did not verify that definitions match. "
          "Years 2017–2021 were not read. The 2025 values are read from a chart.",
          "We do not know whether the Green Paper’s “abstraction” means WSC’s reported production or metered abstraction, "
          "or how Eurostat’s public-supply figure is built.",
          "Page numbers for the Green Paper are the printed spread numbers (the PDF holds two pages per sheet). Sapiano’s "
          "page is the journal pagination (PDF page 7 of 8).",
          "The New Water maximum is a capacity statement from 2019, not an outturn. No New Water volume after 2022 was found, "
          "so the give-back figures are a lower bound on what is delivered today.",
          "The WSC pages were read live on 11 Oct 2026. We did not find the “equivalent volume” wording on them and did "
          "not read WSC’s 2018 framework document; the concept is taken from Sapiano’s description."]:
    S.append(P("• " + l, bul))

S += [Spacer(1, 6 * mm), SectionHeading(None, "References")]
S += references([
    ("1", "Energy and Water Agency (Nov 2023). Green Paper on the Regulation of Groundwater Abstraction in the Maltese "
          "Islands, pp. 3, 5, 6, 10, 12. (Full text read 11 Oct 2026; page numbers are the printed spread numbers.)",
     "https://energywateragency.gov.mt/wp-content/uploads/2023/11/GREEN-PAPER.pdf"),
    ("2", "Sapiano M. (2020). Integrated Water Resources Management in the Maltese Islands. <i>Acque Sotterranee – "
          "Italian Journal of Groundwater</i> 9(3):25–32. doi:10.7343/as-2020-477. (Full text read; open access; "
          "author at the Energy and Water Agency.)", "https://doi.org/10.7343/as-2020-477"),
    ("3", "Water Services Corporation (2 April 2019). European Commission Endorses WSC’s ‘Net Zero-Impact’ Utility "
          "Project. News release. (Read live 11 Oct 2026.)",
     "https://www.wsc.com.mt/european-commission-endorses-wscs-net-zero-impact-utility-project/"),
    ("4", "Water Services Corporation (16 April 2018). Towards a Net Zero-Impact Utility: new €100 million EU-funded "
          "project. (Read live 11 Oct 2026.)",
     "https://www.wsc.com.mt/towards-a-net-zero-impact-utility-new-e100-million-eu-funded-project-set-to-improve-water-quality-to-all-new-highs/"),
    ("5", "Sustain Europe (6 November 2018). Closing the water loop – improving the sustainability of Malta’s water "
          "resources. Unsigned article.",
     "https://www.sustaineurope.com/closing-the-water-loop-%E2%80%93-improving-the-sustainability-of-malta%E2%80%99s-water-resources-20181105.html"),
    ("6", "Water Services Corporation (2017). Annual Report 2016, p. 10. (Read in the Internet Archive copy for Claim Check 039.)",
     "https://www.wsc.com.mt/wp-content/uploads/2018/03/Annual_Report_-_16.pdf"),
    ("7", "Water Services Corporation. Annual Report 2025, Figure 20 (groundwater production 2022–2025), as transcribed for "
          "Claim Check 009; parlament.mt refused this site’s request on 11 Oct 2026.",
     "https://parlament.mt/media/139352/wsc-annual-report-2025.pdf"),
    ("8", "Eurostat. Water abstraction by source and sector (env_wat_abs) and renewable freshwater resources (env_wat_res), "
          "Malta; retrieved 5 Oct 2026. Values flagged ‘e’ (estimated).",
     "https://ec.europa.eu/eurostat/databrowser/view/env_wat_abs/default/table"),
    ("9", "European Environment Agency. WISE Water Framework Directive database, groundwater bodies, Malta, 2nd and 3rd "
          "reporting cycles; retrieved 5 Oct 2026 for Claim Check 009 (data/cc-009/wise_gwb_status.csv).",
     "https://water.discomap.eea.europa.eu/arcgis/rest/services/WISE_WFD/WFD2022_GroundWaterBody_WM/MapServer/0"),
    ("10", "MiŻien. Analysis code and outputs: tools/cc-108-report/; data/cc-108/.", ""),
])

S.append(PageBreak())
S += appendix_a("A experiment · B observational study with a control or gradient · C review, guidance or "
                "official statistics · D assertion or anecdote. The Green Paper, WSC reports and Sapiano (an Energy and Water "
                "Agency author) are agency or self-reported documents (C); our own arithmetic is an order-of-magnitude "
                "estimate.", pledges=True)
S += [Spacer(1, 5 * mm)]
S += revision_log([
    ('1.0', '11 Oct 2026', 'First issue. Pledge label: not measurable. The 14 million m³ cap is met so far (WSC production 11.5 million m³ in 2025, 82% of it) but sits close to the highest year read (13.5 in 2016). The net-zero aim has no definition, baseline or date; the give-back we can count (New Water 1.6 million m³ in 2022) is small against 11.5 million m³ abstracted. Draft pending right of reply from the Energy and Water Agency and the Water Services Corporation.')])

build_report(Report(
    number="108", out=str(FIG / "report.pdf"), kicker="Water, checked",
    title_lines=["Net-zero impact", "on the aquifer?"],
    subtitle_lines=["Testing the Green Paper’s reasons for exempting WSC’s", "boreholes from groundwater licensing"],
    quote_lines=["“…the Corporation is moving towards the achievement of", "a net-zero impact on the groundwater environment…”"],
    quote_size=14,
    attribution="Energy and Water Agency, Green Paper on groundwater abstraction, November 2023, p. 12.",
    context="Same page: WSC abstraction “will be capped at a maximum level of 14 Mm³ up to 2030”.",
    verdict="Not measurable", verdict_note="As of 11 Oct 2026: no definition, baseline or date for net zero",
    footer_lines=["Version 1.0  ·  11 October 2026",
                  "Status: pending right of reply",
                  "Prepared from public sources and open data. No site visits.", "Repository: github.com/leandergrech/Mizien"],
    running_head="WSC net-zero impact – Green Paper 2023", version="1.0", date="11 October 2026",
    pdf_title="Net-zero impact on the aquifer? Claim Check 108",
    pdf_subject="Tests the Green Paper's statements on WSC's groundwater cap and net-zero impact",
    story=S))
