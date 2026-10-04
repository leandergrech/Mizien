"""Claim Check 022 report. Run fetch_data.py, calc.py and figures.py first. Output: out/report.pdf"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import *  # noqa: E402,F401

FIG = HERE / "out"
S = []
LG = colors.HexColor("#8DB36B")

S += [SectionHeading(None, "TL;DR"), Spacer(1, 1 * mm),
      P("On 6 May 2025 the Energy Ministry said that <b>“Malta has the lowest electricity prices for domestic consumers "
        "in the European Union when measured in terms of purchasing power standards”</b>, and that “the burden on Maltese "
        "families is the lowest in the EU, at 14.33 PPS per 100kWh”. We checked every figure against Eurostat and looked "
        "at what keeps the price low.", lead)]
S.append(key_points([
    ("Every figure checks out.",
     "Eurostat now shows Malta at 14.35 PPS per 100 kWh in the second half of 2024, the lowest of 27 countries; the "
     "nominal price of EUR 0.130 is the third lowest; the Czech, Cypriot and German figures match exactly."),
    ("Prices really were stable.",
     "Malta’s household price was flat between 2020 and 2025 (−0.2%) while the EU average rose 35%."),
    ("The price is held down with public money.",
     "Tariffs have been frozen since 2014. The IMF puts energy subsidies (electricity and fuel) at 1.8% of GDP in 2022, "
     "falling to about 0.8% in 2025: roughly EUR 1 billion over four years, paid through public finances. The IMF "
     "recommends phasing out untargeted subsidies."),
    ("Few households struggle with bills.",
     "7.6% of people cannot keep their home adequately warm (EU 8.8%) and 4.5% are in arrears on utility bills (EU 7.0%)."),
    ("Verdict: largely supported (high confidence).",
     "The comparison is accurate. “Burden” is measured by price only; the cost of keeping that price low falls on the "
     "state budget, which the release does not mention."),
]))
S += [Spacer(1, 4 * mm), VerdictMeter(1), Spacer(1, 3 * mm),
      tiles([("1st", GREEN, "Lowest price in the EU in purchasing power, 2024-S2"),
             ("3rd", GREEN, "Lowest nominal price, EUR 0.130 per kWh"),
             ("−0.2%", GREEN, "Change in Malta’s price 2020–2025 (EU +35%)"),
             ("€1.0bn", RED, "Energy subsidies 2022–2025 (IMF, electricity and fuel)")]),
      Spacer(1, 4 * mm),
      up_down("A household-expenditure measure showing the lowest share of income spent on electricity, with the "
              "subsidy cost shown alongside.",
              "Evidence that the PPS figure was misread, or that subsidy costs fall on households through other bills."),
      Spacer(1, 5 * mm)]
S += toc([("1", "The claim"), ("2", "Method"), ("3", "What the data show"), ("4", "Where the evidence points different ways"),
          ("5", "Testing the claim"), ("6", "Verdict and requests for evidence"), ("7", "Limitations")])
S.append(PageBreak())

S.append(SectionHeading(1, "The claim"))
S.append(P("The press release by the Ministry for the Environment, Energy and Public Cleanliness was read in full [1]."))
S.append(std_table([
    [C("What was said", cellh), C("Access", cellh)],
    [C("“Malta has the lowest electricity prices for domestic consumers in the European Union when measured in terms of "
       "purchasing power standards (PPS)… for the second half of 2024.”"), C("Read in full")],
    [C("“…third-lowest nominal electricity price… at €0.131 per unit… the burden on Maltese families is the lowest in the "
       "EU, at 14.33 PPS per 100kWh.” Czech Republic 41.00, Cyprus 35.70, Germany 35.23 PPS."), C("Read in full")],
    [C("“This is clear confirmation that our policy is working for the benefit of the people.” (Minister Miriam Dalli)"),
     C("Read in full")],
], [140 * mm, 30 * mm]))

S += [Spacer(1, 4 * mm), SectionHeading(2, "Method")]
S.append(P("Eurostat household electricity prices (band DC, all taxes) for all EU countries, 2019–2025, in euros and "
           "purchasing power standards [2]; Eurostat energy-poverty indicators [3]; energy subsidies from the IMF’s "
           "2025 Article IV report [4], converted to euros with Eurostat GDP. Numbers are recomputed by "
           "<i>tools/cc-022-report/calc.py</i>. Official statistics and assessments are grade C."))

S.append(CondPageBreak(150 * mm))
S.append(SectionHeading(3, "What the data show"))
S.append(fig(FIG / "fig1_ranking.png"))
S.append(P("Figure 1. Household electricity prices in the EU, second half of 2024. Malta is third cheapest in euros and "
           "cheapest once prices are adjusted for purchasing power.", cap))
S.append(fig(FIG / "fig2_price_subsidy.png"))
S.append(P("Figure 2. Left: Malta’s price stayed flat while the EU average rose. Right: what that stability cost in "
           "energy subsidies.", cap))
S.append(std_table([
    [C("Indicator", cellh), C("Claim", cellh), C("Eurostat / IMF", cellh), C("Grade", cellh)],
    [C("Malta, PPS per 100 kWh, 2024-S2"), C("14.33, lowest"), C("<b>14.35, lowest of 27</b>"), grade_tag("C")],
    [C("Malta, nominal price, 2024-S2"), C("EUR 0.131, third lowest"), C("EUR 0.1303, third lowest"), grade_tag("C")],
    [C("Czechia / Cyprus / Germany, PPS"), C("41.00 / 35.70 / 35.23"), C("41.00 / 35.70 / 35.23"), grade_tag("C")],
    [C("Price change 2020-S1 → 2025-S2"), C("“remained stable”"), C("Malta −0.2%; EU +35.4%"), grade_tag("C")],
    [C("Energy subsidies 2022–2025"), C("not mentioned"), C("EUR 325m, 293m, 208m, 197m"), grade_tag("C")],
    [C("Unable to keep home warm, 2025"), C("–"), C("7.6% (EU 8.8%)"), grade_tag("C")],
    [C("Arrears on utility bills, 2025"), C("–"), C("4.5% (EU 7.0%)"), grade_tag("C")],
], [60 * mm, 40 * mm, 56 * mm, 14 * mm]))
S.append(P("All values in <i>data/cc-022/checks.csv</i>.", cap))

S.append(CondPageBreak(110 * mm))
S.append(SectionHeading(4, "Where the evidence points different ways"))
S.append(contested(
    "Q1  Is the burden on families the lowest in the EU?", "ON PRICE, YES", GREENC,
    "Price adjusted for purchasing power is the lowest in the EU, and fewer Maltese than average struggle to pay bills or "
    "heat their homes.",
    "PPS adjusts for general price levels, not for how much electricity households use or their income; it is a price "
    "comparison, not a measure of burden.",
    "<b>For this claim:</b> as a statement about price, it is accurate."))
S.append(contested(
    "Q2  Is it confirmation that the policy works?", "INCOMPLETE", AMBER,
    "Prices stayed flat through the 2022 energy shock, protecting households.",
    "The stability was bought with energy subsidies of about EUR 1 billion in 2022–2025 [4], paid through public "
    "finances; the IMF recommends replacing untargeted subsidies with cost-recovery tariffs and targeted support.",
    "<b>For this claim:</b> the release presents the benefit without its cost."))

S.append(CondPageBreak(90 * mm))
S.append(SectionHeading(5, "Testing the claim"))
verd = lambda t, c: chip(t, c, w=29 * mm)
S.append(std_table([
    [C("Sub-claim", cellh), C("What the evidence shows", cellh), C("Rating", cellh)],
    [C("<b>A.</b> Lowest price in PPS, 2024-S2"), C("Confirmed by Eurostat [2]."), verd("SUPPORTED", GREENC)],
    [C("<b>B.</b> Third-lowest nominal price; comparison figures"), C("Confirmed [2]."), verd("SUPPORTED", GREENC)],
    [C("<b>C.</b> Prices stable since 2020"), C("−0.2% vs EU +35% [2]."), verd("SUPPORTED", GREENC)],
    [C("<b>D.</b> Lowest “burden” on families"), C("True for price; the subsidy cost is not counted [4]."),
     verd("LARGELY SUPPORTED", LG)],
], [52 * mm, 88 * mm, 30 * mm], valign="MIDDLE"))

S += [Spacer(1, 6 * mm), SectionHeading(6, "Verdict and requests for evidence"),
      verdict_box("Largely supported", "Every figure is accurate; the cost of keeping prices low is left out. "
                  "Confidence: high."), Spacer(1, 4 * mm)]
S.append(P("<b>Why.</b> The statistical claims match Eurostat exactly. The word “burden” and the minister’s conclusion "
           "rest on price alone, while the tariff freeze is financed by public subsidies the IMF puts at about EUR 1 "
           "billion over 2022–2025. That omission qualifies the claim without contradicting it."))
S.append(P("Evidence we are asking for", h2))
S.append(requests_list([
    "The electricity-only subsidy to Enemalta by year, separate from fuel.",
    "Household spending on electricity as a share of income, by income group.",
]))
S += [Spacer(1, 6 * mm), SectionHeading(7, "Limitations")]
for l in ["The IMF subsidy series covers electricity and fuel; 2025 is a staff projection.",
          "Band DC is a typical household; very large or very small users face different prices.",
          "Eurostat revised Malta’s PPS figure from 14.33 to 14.35 after the release; the ranking is unchanged."]:
    S.append(P("• " + l, bul))
S += [Spacer(1, 6 * mm), SectionHeading(None, "References")]
S += references([
    ("1", "Ministry for the Environment, Energy and Public Cleanliness (6 May 2025). Electricity prices in the EU: "
          "Maltese households with lowest burden. PR250746en.",
     "https://www.gov.mt/en/Government/DOI/Press%20Releases/Pages/2025/05/06/pr250746en.aspx"),
    ("2", "Eurostat. nrg_pc_204, electricity prices for household consumers; retrieved 4 Oct 2026.",
     "https://ec.europa.eu/eurostat/databrowser/view/nrg_pc_204/default/table"),
    ("3", "Eurostat. ilc_mdes01, ilc_mdes07; retrieved 4 Oct 2026.", "https://ec.europa.eu/eurostat/databrowser/view/ilc_mdes01/default/table"),
    ("4", "International Monetary Fund (2026). Malta: 2025 Article IV Consultation. Country Report 26/29, Table 2 and "
          "para. on energy subsidies.", "https://www.imf.org/-/media/files/publications/cr/2026/english/1mltea2026001-source-pdf.pdf"),
    ("5", "MiŻien. Data and calculations: data/cc-022/; tools/cc-022-report/.", ""),
])
S.append(PageBreak())
S += appendix_a("A experiment · B observational study with a control or gradient · C review, guidance or official "
                "statistics · D assertion or anecdote.")
S += [Spacer(1, 5 * mm)]
S += revision_log([("1.0", "4 Oct 2026", "First issue. Right of reply to the Energy Ministry not yet sent.")])

build_report(Report(
    number="022", out=str(FIG / "report.pdf"), kicker="Climate and energy",
    title_lines=["The lowest", "electricity", "burden in the EU?"],
    subtitle_lines=["Testing a ministry claim about household electricity prices",
                    "against Eurostat and the IMF"],
    quote_lines=["“…the burden on Maltese families is the", "lowest in the EU, at 14.33 PPS per 100kWh.”"],
    quote_size=16,
    attribution="Ministry for the Environment, Energy and Public Cleanliness, 6 May 2025.",
    context="Based on Eurostat figures for the second half of 2024.",
    verdict="Largely supported", verdict_note="Accurate figures; the subsidy cost is left out",
    footer_lines=["Version 1.0  ·  4 October 2026", "Status: draft (right of reply: Energy Ministry)",
                  "Prepared from Eurostat data and the IMF report.", "Repository: github.com/leandergrech/Mizien"],
    running_head="Electricity prices – Malta", version="1.0", date="4 October 2026",
    pdf_title="The lowest electricity burden in the EU? Claim Check 022",
    pdf_subject="Tests the Energy Ministry's claim that Maltese households have the EU's lowest electricity burden",
    story=S))
