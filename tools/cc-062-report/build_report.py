"""Claim Check 062 report. Run calc.py and figures.py first. Output: out/report.pdf"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import *  # noqa: E402,F401

FIG = HERE / "out"
S = []
LG = colors.HexColor("#8DB36B")
QUOTE = ("Construction and real estate collectively account for around 9% of Gross Value Added (GVA) when "
         "considering direct effects alone, rising to approximately 14% once indirect linkages are factored in.")

# ================================================================== TL;DR
S += [SectionHeading(None, "TL;DR"), Spacer(1, 1 * mm),
      P("The foreword to KPMG’s <i>Construction Industry and Property Market Report 2025</i>, prepared for the Malta "
        "Development Association (MDA), says: <b>“" + QUOTE + "”</b> We recomputed both figures from the report’s "
        "own tables and from Eurostat’s national accounts. Both reproduce. They are not, however, measured the same "
        "way: about two-thirds of the step from 9% to 14% comes from a change in how housing services are counted, "
        "not from indirect linkages.", lead)]
S.append(key_points([
    ("The 9% reproduces.",
     "KPMG’s Table 1.1: 9.1% of GVA in 2024 (imputed rents excluded). Eurostat’s current series: 9.6% for 2024, "
     "9.7% for 2025, same definition."),
    ("The 14% reproduces arithmetically.",
     "Table 1.3 applies multipliers (0.55; 0.78) to 2024 output and gets EUR 3,002 million, 14.04% of GVA; its "
     "output inputs match Eurostat’s."),
    ("The two figures are not like for like.",
     "The 9% leaves out imputed rents (the value of owner-occupiers’ housing); the 14% includes them. On KPMG’s own "
     "figures the direct share with imputed rents is 12.3%, so indirect linkages add 1.7 percentage points, not 5."),
    ("The multipliers are old and could not be re-derived.",
     "Central Bank of Malta Type I multipliers from the 2015 input-output table (second-hand); Eurostat’s Maltese "
     "table is incomplete, so we could not rebuild them. KPMG warns of assumptions that “may not hold true in real life”."),
    ("Verdict: largely supported (moderate confidence).",
     "Both figures match the data and the method is disclosed. The caveats concern what the sentence does not say: "
     "that the two figures use different treatments of imputed rents, and that the 14% is a modelled estimate."),
]))
S += [Spacer(1, 2.5 * mm), VerdictMeter(1), Spacer(1, 3 * mm),
      tiles([("9.1%", GREEN, "Direct share of GVA, 2024, KPMG Table 1.1 (Eurostat: 9.6%)"),
             ("14.0%", GREEN, "Direct plus indirect, 2024, KPMG Table 1.3 (modelled)"),
             ("+3.2 pp", AMBER, "of the 4.9-point step is imputed rents moving into the count"),
             ("+1.7 pp", ORANGE, "is what indirect linkages add on the same basis (12.3% to 14.0%)")]),
      Spacer(1, 4 * mm),
      up_down("A readable source for the multipliers (the Central Bank of Malta or NSO tables) that reproduces 0.55 and "
              "0.78, and a statement alongside the figures that the 9% excludes imputed rents and the 14% includes them.",
              "Evidence that the 2015-based multipliers differ materially from those of the NSO’s latest input-output "
              "table, or that the output figures used in Table 1.3 are not NSO’s."),
      Spacer(1, 3 * mm)]
S += toc([("1", "The claim and what we could verify"), ("2", "Method"), ("3", "What the data show"),
          ("4", "Where the evidence points different ways"), ("5", "Testing the claim"),
          ("6", "Verdict and requests for evidence"), ("7", "Limitations")])
S.append(PageBreak())

# ================================================================== 1
S.append(SectionHeading(1, "The claim and what we could verify"))
S.append(P("The sentence is in the foreword of the report, signed by Steve Stivala, Director, Advisory Services, KPMG "
           "(PDF p. 10) [1]. The report states that it was commissioned by the Malta Development Association and "
           "sponsored by four banks and the Property Malta Foundation, and that KPMG undertakes no advocacy services "
           "for the Association (PDF pp. 2–3) [1]. We read the foreword, executive summary and Chapter 1 (the "
           "economic contribution), where the figures are built; we did not read the other chapters. The "
           "foreword does not cite a table, but Table 1.1 (p. 23) and Table 1.3 (p. 30) give 9.1% and 14.04%."))
S.append(std_table([
    [C("What was said", cellh), C("Who", cellh), C("Access", cellh)],
    [C("“Construction and real estate collectively account for around 9% of Gross Value Added (GVA) when "
       "considering direct effects alone, rising to approximately 14% once indirect linkages are factored in.”"),
     C("KPMG, foreword [1]"), C("Read in full (PDF p. 10)")],
    [C("Table 1.1: 9.1% of total GVA less imputed rents in 2024 (construction F plus real estate L excluding "
       "imputed rents)"), C("KPMG, from NSO data [1]"), C("Read (PDF p. 23)")],
    [C("Table 1.3: EUR 3,002 million, 14.04% of total GVA, from output multiplied by Type 1 value-added multipliers"),
     C("KPMG, using Central Bank of Malta multipliers ◆ [1]"), C("Read (PDF p. 30); multipliers not retrieved")],
], [96 * mm, 40 * mm, 34 * mm]))
S += [Spacer(1, 4 * mm),
      callout([P("SCOPE NOTE", tag),
               P("This check is about the two shares of GVA in the sentence. It does not assess the report’s other "
                 "findings (prices, permits, employment), the industry’s environmental effects, or the commissioning "
                 "arrangement. Gross value added (GVA) is output less intermediate consumption; imputed rents are the "
                 "value national accounts assign to owner-occupiers’ housing services.", small)],
              bg=AMBER_PALE, bar=AMBER), Spacer(1, 4 * mm)]

# ================================================================== 2
S.append(SectionHeading(2, "Method"))
S.append(P("<b>Question.</b> Do the data support construction and real estate being about 9% of Malta’s GVA directly and "
           "about 14% including indirect linkages, and are the two numbers measured on the same basis?"))
S.append(P("<b>Evidence.</b> KPMG’s Tables 1.1–1.3, transcribed with page numbers [1]; Eurostat’s national accounts by "
           "industry (nama_10_a64: gross value added and output, current prices) [2]; Eurostat’s symmetric input-output "
           "tables for Malta (naio_10_cp1750, 2015 and 2020) to test whether the multipliers can be re-derived [3]. All "
           "numbers are recomputed by <i>tools/cc-062-report/calc.py</i> from files in <i>data/cc-062/</i> and written "
           "to <i>data/cc-062/checks.csv</i>."))
S.append(P("<b>Grades.</b> Official national-accounts statistics are grade C; KPMG’s report is a commissioned analysis of "
           "official statistics and is graded C; the multiplier-based estimate is a model and is graded C with the "
           "caveats in Section 4. No peer-reviewed study is needed to test an accounting ratio. <b>Verdicts</b> follow "
           "the five-point scale in Appendix A."))

# ================================================================== 3
S.append(CondPageBreak(100 * mm))
S.append(SectionHeading(3, "What the data show"))
S.append(P("<b>The direct share.</b> KPMG defines the “building industry” as construction (NACE F) plus real estate "
           "activities excluding imputed rents (part of NACE L), and divides by total GVA less imputed rents. For 2024 "
           "that is EUR 1,875 million of EUR 20,617 million, or 9.1% (Table 1.1) [1]. Eurostat’s current series gives "
           "the same ratio as 9.0% for 2023, 9.6% for 2024 and 9.7% for 2025 [2]. The 2024 difference arises because "
           "Eurostat’s construction GVA for 2024 (EUR 893.6 million) is now higher than KPMG’s (EUR 809.0 million); in "
           "2020–2023 the two series agree to within 0.15 percentage points (Figure 2)."))
S.append(fig(FIG / "fig2_series.png"))
S.append(P("Figure 2. Construction and real estate as a share of GVA. Excluding imputed rents from both numerator and "
           "denominator (KPMG’s “direct” basis) gives 8.5–9.8%; including them in both gives 10.4–12.7%.", cap))
S.append(P("<b>The 14%.</b> Table 1.3 multiplies 2024 output (construction EUR 2,395 million; real estate including "
           "imputed rents EUR 2,438 million) by Type 1 value-added multipliers of 0.55 and 0.78. That gives EUR 1,317 and "
           "1,901 million; after subtracting EUR 216 million for inter-industry linkages the total is EUR 3,002 million, "
           "which is 14.04% of total GVA of EUR 21,378 million [1]. We reproduce each step. Eurostat’s output figures "
           "for 2024 are 2,396 and 2,439, within 0.1% of KPMG’s [2]."))
S.append(P("<b>Why 9% and 14% differ.</b> The real-estate output in Table 1.3 includes imputed rents, and total GVA "
           "includes them; the 9% leaves both out. Putting the direct figures on the 14%’s basis (construction EUR 809 "
           "million plus real estate including imputed rents EUR 1,827 million, from Table 1.2, divided by total GVA of "
           "EUR 21,378 million) gives 12.3%. The step from 9.1% to 14.0% then splits into 3.2 points from the change of "
           "basis and 1.7 points from indirect linkages (Figure 1)."))
S.append(KeepTogether([fig(FIG / "fig1_steps.png"),
                       P("Figure 1. The step from KPMG’s “direct” 9.1% to its 14.0%: 65% of the 4.9-point step reflects a "
                         "change in the treatment of imputed rents; the modelled indirect linkages add 1.7 points. "
                         "All values 2024.", cap)]))
S.append(std_table([
    [C("Figure", cellh), C("Value", cellh), C("Source", cellh), C("Grade", cellh)],
    [C("Direct share, imputed rents excluded, 2024"), C("<b>9.1%</b> (KPMG); 9.6% (Eurostat)"),
     C("KPMG Table 1.1 [1]; Eurostat nama_10_a64 [2]"), grade_tag("C")],
    [C("Direct share, imputed rents included, 2024"), C("12.3% (KPMG’s figures); 12.7% (Eurostat)"),
     C("KPMG Table 1.2 [1]; Eurostat [2]"), grade_tag("C")],
    [C("Direct plus indirect (modelled), 2024"), C("<b>14.04%</b>, EUR 3,002 million"), C("KPMG Table 1.3 [1]"),
     grade_tag("C")],
    [C("Output, construction / real estate, 2024"), C("2,395 / 2,438 (KPMG); 2,396 / 2,439 (Eurostat)"),
     C("KPMG Table 1.3 [1]; Eurostat [2]"), grade_tag("C")],
    [C("Multipliers (Type 1 value added): construction / real estate"), C("0.55 / 0.78, 2015 table"),
     C("KPMG p. 30, 34 [1]; CBM publication not retrieved ◆"), grade_tag("C")],
    [C("Malta SIOT 2015 in Eurostat: value added in industries with a published column"),
     C("EUR 6,443 million of 8,889 (72%)"), C("Eurostat naio_10_cp1750 [3]"), grade_tag("C")],
], [58 * mm, 52 * mm, 48 * mm, 12 * mm]))
S.append(P("All values in <i>data/cc-062/checks.csv</i>. Eurostat figures are current-price national accounts retrieved on "
           "8 Oct 2026 and carry no status flags in the extract; KPMG’s NSO figures are an earlier vintage. "
           "pp = percentage points.", cap))

# ================================================================== 4
S.append(CondPageBreak(120 * mm))
S.append(SectionHeading(4, "Where the evidence points different ways"))
S.append(contested(
    "Q1  Is the direct share about 9%?", "YES, ON KPMG’S DEFINITION", GREEN,
    "KPMG’s Table 1.1 gives 9.1% for 2024 and 8.6–9.0% for 2020–2023; Eurostat’s current series reproduces 2020–2023 "
    "within 0.15 points and gives 9.6% for 2024 and 9.7% for 2025 [1][2].",
    "The figure depends on the definition. It leaves out imputed rents and a list of related activities KPMG names but "
    "could not include (for example architecture and engineering, quarrying, building-materials manufacturing, p. 21). "
    "Counting imputed rents in both numerator and denominator gives 12.7% (2024, Eurostat).",
    "<b>For this claim:</b> “around 9%” matches the data for the report’s own definition. The sentence does not say "
    "that real estate excludes imputed rents; Table 1.1 does."))
S.append(contested(
    "Q2  Is about 14% a fair figure “once indirect linkages are factored in”?", "REPRODUCES; BASIS AND MODEL CAVEATS",
    AMBER,
    "The arithmetic reproduces (14.04%), the method is disclosed (output times Type 1 multiplier, less inter-industry "
    "linkages) and the output inputs match Eurostat [1][2]. KPMG states the multipliers are the latest published "
    "Central Bank of Malta Type 1 value-added multipliers, based on the 2015 input-output table ◆.",
    "The 14% counts imputed rents; the 9% does not, so the two are not on one basis (Figure 1). The multipliers are "
    "from a 2015 table, and KPMG’s footnote 16 says they rest on assumptions on relative prices and supply "
    "constraints that “may not hold true in real life”. We could not re-derive 0.55 and 0.78: Eurostat’s published "
    "Malta table covers 72% of value added.",
    "<b>For this claim:</b> the 14% is a reproducible model estimate, not a measured share. It is a fair statement "
    "of KPMG’s own result; how much of it is indirect linkage (1.7 points on a like-for-like basis) is not in the "
    "sentence."))

# ================================================================== 5
S.append(CondPageBreak(90 * mm))
S.append(SectionHeading(5, "Testing the claim"))
verd = lambda t, c: chip(t, c, w=29 * mm)
S.append(std_table([
    [C("Sub-claim", cellh), C("What the evidence shows", cellh), C("Rating", cellh)],
    [C("<b>A.</b> Construction and real estate account for around 9% of GVA, direct effects alone"),
     C("KPMG Table 1.1: 9.1% (2024); Eurostat: 9.6% (2024), 9.7% (2025), same definition (imputed rents excluded)."),
     verd("SUPPORTED", GREENC)],
    [C("<b>B.</b> About 14% once indirect linkages are factored in"),
     C("Reproduces from KPMG Table 1.3 (14.04%); outputs match Eurostat. Modelled with 2015 multipliers we could not "
       "re-derive; counts imputed rents, which the 9% does not."), verd("LARGELY SUPPORTED", LG)],
], [52 * mm, 88 * mm, 30 * mm], valign="MIDDLE"))

# ================================================================== 6
S += [CondPageBreak(75 * mm), Spacer(1, 6 * mm), SectionHeading(6, "Verdict and requests for evidence"),
      verdict_box("Largely supported", "Both figures reproduce from the data; the two use different bases and the "
                  "14% is a model estimate. Confidence: moderate."), Spacer(1, 4 * mm)]
S.append(P("<b>Why.</b> (1) The 9% is KPMG’s own Table 1.1 and is reproduced by Eurostat (9.6% for 2024 on the same "
           "definition). (2) The 14% is KPMG’s Table 1.3; we reproduce every line, and the output inputs match "
           "Eurostat. (3) Two caveats limit the claim: the 14% includes imputed rents while the 9% does not, which "
           "accounts for 3.2 of the 4.9 points between them, and the multipliers behind the indirect part could not be "
           "verified. Neither changes the substance (the sector is about a tenth of GVA directly, and more once "
           "linkages are modelled), which our scale calls <i>Largely supported</i>. Confidence is moderate because "
           "the indirect part rests on a model we could not re-derive."))
S.append(P("<b>What this verdict does not say.</b> It does not say the sector’s true economic weight is 14%, that "
           "multiplier effects are a share of GDP, or anything about the report’s other findings. It says the two "
           "figures in the foreword match the data and the report’s own tables."))
S.append(P("Evidence we are asking for", h2))
S.append(requests_list([
    "The Central Bank of Malta or NSO table that gives the 2015-based Type 1 value-added multipliers (0.55; 0.78).",
    "Multipliers from a more recent NSO input-output table, if one has been published.",
    "A note, where the figures are quoted, that the 9% excludes imputed rents and the 14% includes them.",
]))

# ================================================================== 7
S += [Spacer(1, 6 * mm), SectionHeading(7, "Limitations")]
for l in ["We read the foreword, executive summary and Chapter 1 of a 124-page report, not the whole report.",
          "The NSO figures in Tables 1.1–1.3 are read through KPMG (◆ second-hand); nso.gov.mt returns 403 to scripts, "
          "and we compared them with Eurostat’s national accounts, which carry NSO’s data.",
          "We could not retrieve the Central Bank of Malta publication of the multipliers (centralbankmalta.org returned "
          "403); the multipliers are therefore known only through KPMG ◆. Web searches (8 Oct 2026) found a Central "
          "Bank working paper and an Xjenza article on Maltese multipliers for other base years, which we did not open.",
          "Eurostat’s Maltese input-output table is partial (72% of value added in 2015; empty columns for several "
          "industries), so we could not rebuild the multipliers; this is a limit of the open data, not evidence that "
          "KPMG’s figures are wrong.",
          "Eurostat’s 2024 and 2025 national-accounts values are subject to revision; 2025 is the latest annual value in "
          "the dataset and is not flagged in our extract.",
          "A multiplier is a modelled response to a hypothetical change in demand, not an observed share of the "
          "economy; KPMG’s footnote 16 (p. 30) says multipliers should be interpreted with caution."]:
    S.append(P("• " + l, bul))

S += [CondPageBreak(60 * mm), Spacer(1, 6 * mm), SectionHeading(None, "References")]
S += references([
    ("1", "KPMG (Dec 2025). Construction Industry and Property Market Report 2025, 9th edition, for the Malta "
          "Development Association. 124 pp. Read 8 Oct 2026 (foreword, executive summary, Chapter 1).",
     "https://assets.kpmg.com/content/dam/kpmgsites/mt/pdf/2025/12/kpmg-mda-construction-industry-and-property-market-report-2025.pdf"),
    ("2", "Eurostat. nama_10_a64: gross value added and output by industry (NACE A*64), current prices, Malta, "
          "2015–2025; retrieved 8 Oct 2026.", "https://ec.europa.eu/eurostat/databrowser/view/nama_10_a64/"),
    ("3", "Eurostat. naio_10_cp1750: symmetric input-output table at basic prices, industry by industry, domestic "
          "output, Malta, 2015 and 2020; retrieved 8 Oct 2026.",
     "https://ec.europa.eu/eurostat/databrowser/view/naio_10_cp1750/"),
    ("4", "MiŻien. Data and calculations: data/cc-062/; tools/cc-062-report/calc.py.", ""),
])

S.append(PageBreak())
S += appendix_a("A experiment · B observational study with a control or gradient · C review, guidance or "
                "official statistics · D assertion or anecdote. ◆ marks a source known only second-hand.")
S += [Spacer(1, 5 * mm)]
S += revision_log([("1.0", "8 Oct 2026", "First issue. Verdict Largely supported (moderate confidence); no right of "
                    "reply needed.")])

build_report(Report(
    number="062", out=str(FIG / "report.pdf"), kicker="Planning and housing",
    title_lines=["Is construction", "9% or 14% of", "the economy?"],
    subtitle_lines=["Testing a KPMG report’s shares of Malta’s gross value added",
                    "against its own tables and Eurostat"],
    quote_lines=["“…around 9% of Gross Value Added … rising to", "approximately 14% once indirect linkages", "are factored in.”"],
    quote_size=15,
    attribution="KPMG (Steve Stivala), foreword, Construction Industry and Property Market Report 2025.",
    context="Dec 2025; commissioned by the Malta Development Association.",
    verdict="Largely supported", verdict_note="Both figures reproduce; different bases, modelled 14%",
    footer_lines=["Version 1.0  ·  8 October 2026", "Status: draft",
                  "Prepared from public sources, KPMG’s report and Eurostat data.",
                  "Repository: github.com/leandergrech/Mizien"],
    running_head="Construction share of GVA – Malta", version="1.0", date="8 October 2026",
    pdf_title="Is construction 9% or 14% of the economy? Claim Check 062",
    pdf_subject="Tests KPMG's statement that construction and real estate are about 9% of Malta's GVA directly and 14% with indirect linkages",
    story=S))
