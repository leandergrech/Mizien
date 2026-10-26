"""Claim Check 134 report. Run calc.py and figures.py first. Output: out/report.pdf"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import *  # noqa: E402,F401

FIG = HERE / "out"
verd = lambda t, c: chip(t, c, w=29 * mm)
LG = colors.HexColor("#8DB36B")
S = []
S += [SectionHeading(None, "TL;DR"), Spacer(1, 1 * mm),
      P("In its 2026 Country Report for Malta, published on 3 June 2026, the European Commission wrote: <b>“Total "
        "environmental tax revenue is lower than the EU average (1.4% of GDP in 2024 against the EU average of "
        "2.1%).”</b> It added that in 2023 revenues came “primarily” from energy and transport taxes (“around 49% and "
        "41%, respectively”), and that taxes on pollution and resources stood at 0.18% of GDP against an EU average of "
        "0.08%. We recomputed every figure from Eurostat’s environmental tax accounts, the dataset the Commission’s "
        "numbers are drawn from.", lead)]
S.append(key_points([
    ("The headline comparison is exact.",
     "Eurostat gives 1.35% of GDP for Malta in 2024 (EUR 312.5 million on a GDP of EUR 23,079 million) and 2.08% for the "
     "EU-27: 1.4% and 2.1% when rounded. The gap is 0.73 percentage points; Malta collects about 65% of the EU rate."),
    ("Malta is near the bottom of the EU.",
     "Malta ranks 25th of 27 in 2024; only Ireland (0.98%) and Luxembourg (1.18%) are lower. The simple average of the "
     "27 states (2.19%) and the median state (2.06%) are also well above Malta."),
    ("The 2023 split is right; one figure is from another year.",
     "Energy taxes were 48.5% and transport taxes 41.6% of the 2023 total, matching “around 49% and 41%”. The 0.18% for "
     "pollution and resources is Eurostat’s figure for 2022; for 2023 Eurostat gives 0.15% (0.14% in 2024). The EU "
     "average of 0.08% is correct for each year."),
    ("The trend is downwards.",
     "Malta’s rate fell from 2.61% of GDP in 2015 to 1.35% in 2024; the EU’s moved from 2.68% to 2.08%."),
    ("Verdict: largely supported (high confidence).",
     "The statement is accurate. The caveats are one figure from a different year and what the measure shows: revenue "
     "as a share of GDP is not a measure of how strict environmental policy is."),
]))
S += [Spacer(1, 2.5 * mm), VerdictMeter(1), Spacer(1, 3 * mm),
      tiles([("1.35%", GREEN, "Malta’s environmental tax revenue, % of GDP, 2024 (Commission: 1.4%)"),
             ("2.08%", GREEN, "EU-27, 2024 (Commission: 2.1%)"),
             ("25th", AMBER, "Malta’s rank of 27 Member States, 2024; only Ireland and Luxembourg are lower"),
             ("0.15%", AMBER, "Pollution and resource taxes, 2023 (Commission: 0.18%, Eurostat’s 2022 value)")]),
      Spacer(1, 4 * mm),
      up_down("A ‘Supported’ verdict would need the Commission’s pollution-and-resources figure to match the year it "
              "is attached to, for example if Eurostat’s 2023 value were revised to 0.18% or the Commission stated that "
              "it used another vintage of the data.",
              "Eurostat revising Malta’s 2024 revenue or GDP so that the rate rose to or above the EU’s, which "
              "would need a change of about EUR 170 million in the revenue series."),
      Spacer(1, 3 * mm)]
S += toc([("1", "The claim and what we could verify"), ("2", "Method"), ("3", "The headline comparison"),
          ("4", "Composition: energy, transport, pollution and resources"), ("5", "What the measure does and does not show"),
          ("6", "Testing the claim"), ("7", "Verdict and requests for evidence"), ("8", "Limitations")])
S.append(PageBreak())

S.append(SectionHeading(1, "The claim and what we could verify"))
S.append(P("The claim is in the Commission’s 2026 Country Report for Malta (staff working document SWD(2026) 218 final), "
           "Annex 10, in the section on the circular economy [1]. We read the document in full from the Council’s register "
           "copy on 25 October 2026. The passage reads:"))
S.append(P("“Malta has scope to develop its fiscal tools to encourage circular practices, raise revenue and reduce waste. "
           "Total environmental tax revenue is lower than the EU average (1.4% of GDP in 2024 against the EU average of "
           "2.1%) (see Annex 3). In 2023, revenues were primarily derived from energy and transport taxes (around 49% and "
           "41%, respectively), with taxes on pollution and resources at 0.18 % (EU average: 0.08 %)”", bul))
S.append(P("Annex 3 of the same report (taxation) repeats the headline in a table: environmental taxes were 2.4% of GDP in "
           "2019, 1.6% in 2022, 1.5% in 2023 and 1.4% in 2024 for Malta, against 2.6%, 2.1%, 2.1% and 2.1% for the EU-27 [1]. "
           "A later passage notes that the share of pollution and resource taxes in total environmental taxes was above the "
           "EU average [1]."))
S.append(std_table([
    [C("What was said", cellh), C("Who", cellh), C("Access", cellh)],
    [C("Total environmental tax revenue is lower than the EU average: 1.4% of GDP in 2024, EU 2.1%"),
     C("Commission [1]"), C("Read in full")],
    [C("In 2023, around 49% energy and 41% transport taxes"), C("Commission [1]"), C("Read in full")],
    [C("Pollution and resource taxes 0.18% of GDP, EU average 0.08% (year stated by the sentence: 2023)"),
     C("Commission [1]"), C("Read in full")],
], [104 * mm, 34 * mm, 32 * mm]))
S += [Spacer(1, 4 * mm),
      callout([P("SCOPE NOTE", tag),
               P("This check tests the figures and what the comparison does and does not show. It does not assess whether "
                 "Malta should raise environmental taxes, or the energy-support measures and fossil-fuel subsidies that "
                 "other checks cover (CC-022, CC-095, CC-113): those are spending, not tax revenue. The Commission "
                 "uses the comparison to argue for more fiscal tools to encourage circular practices; we do not rate that "
                 "recommendation.", small)], bg=AMBER_PALE, bar=AMBER), Spacer(1, 4 * mm)]

S.append(SectionHeading(2, "Method"))
S.append(P("<b>Question.</b> Are the Commission’s figures what Eurostat’s environmental tax accounts show, and how should "
           "the comparison be read? <b>Evidence.</b> Eurostat env_ac_tax (revenue from environmental taxes, by category, as a "
           "share of GDP and in euro) and nama_10_gdp (GDP at current prices) for Malta, the EU-27 and all 27 Member States, "
           "2015–2024, downloaded on 26 October 2026 with status flags [2, 3]. We recomputed Malta’s share from the euro "
           "revenue and GDP, ranked the 27 states, and recomputed the composition from the euro revenue by category "
           "(<i>tools/cc-134-report/calc.py</i>; inputs in <i>data/cc-134/</i>; results in <i>checks.csv</i>). The "
           "definition is Eurostat’s [4]. <b>Grades.</b> Official statistics are grade C; a peer-reviewed study on what "
           "environmental tax revenue does and does not measure is cited as context (grade B) [5]. Verdicts follow the "
           "scale in Appendix A."))

S.append(CondPageBreak(110 * mm))
S.append(SectionHeading(3, "The headline comparison"))
S.append(P("Eurostat counts as environmental taxes only payments that national accounts classify as taxes and whose tax "
           "base is a physical unit (or proxy) of something with a proven specific negative impact on the environment: "
           "energy (including fuel for transport), transport (such as vehicle taxes), pollution and resources [4]. On that "
           "definition, Malta’s environmental taxes raised EUR 312.5 million in 2024. Divided by GDP of EUR 23,079 million "
           "this is 1.354%, equal to Eurostat’s published 1.35% [2, 3]. The EU-27 figure is 2.08%. The Commission’s 1.4% "
           "and 2.1% are these values, rounded."))
S.append(fig(FIG / "fig1_trend.png"))
S.append(P("Figure 1. Environmental tax revenue as a share of GDP, Malta and the EU-27, 2015–2024. Malta’s share fell by "
           "almost half; the EU’s by about a fifth.", cap))
S.append(P("Malta’s rate was below the EU’s in every year of 2015–2024, by 0.07 percentage points in 2015, 0.19 in 2019 "
           "and 0.73 in 2024. The decline from 2.38% in 2019 to 1.35% in 2024 is 1.03 percentage points, against 0.49 "
           "points for the EU-27 [2]. The data do not say why, and we did not test causes: revenue as a share of GDP falls "
           "when GDP grows faster than the taxed activity or when rates are cut."))
S.append(fig(FIG / "fig2_rank.png"))
S.append(P("Figure 2. Environmental taxes as a share of GDP, 2024, all 27 Member States. Malta (green) ranks 25th; the "
           "dashed line is the EU-27 aggregate.", cap))
S.append(P("Ranked among the 27, Malta is 25th (Ireland 0.98%, Luxembourg 1.18%, Malta 1.35%). The highest is Greece at "
           "3.76%. The simple average of the 27 states is 2.19% and the median state is 2.06% [2]. The Commission’s claim "
           "that Malta is “lower than the EU average” therefore holds against the EU-27 aggregate, the simple average "
           "and the median."))

S.append(CondPageBreak(100 * mm))
S.append(SectionHeading(4, "Composition: energy, transport, pollution and resources"))
S.append(std_table([
    [C("Malta, % of GDP", cellh), C("2022", cellh), C("2023", cellh), C("2024", cellh), C("EU-27, 2023", cellh)],
    [C("Energy taxes"), C("0.80"), C("<b>0.72</b> (48.5% of total)"), C("0.68"), C("1.61")],
    [C("Transport taxes"), C("0.62"), C("<b>0.62</b> (41.6% of total)"), C("0.54"), C("0.36")],
    [C("Pollution and resources"), C("<b>0.18</b>"), C("<b>0.15</b> (9.8% of total)"), C("0.14"), C("0.08")],
    [C("Total environmental taxes"), C("1.60"), C("1.49"), C("1.35"), C("2.06")],
], [52 * mm, 24 * mm, 46 * mm, 24 * mm, 24 * mm]))
S.append(P("Source: Eurostat env_ac_tax, percentage of GDP; shares computed from revenue in euro [2]. Figures in bold are those "
           "the Commission cites or that bear on its sentence. Categories may not sum exactly because of rounding.", cap))
S.append(P("<b>Energy and transport.</b> In 2023 energy taxes were 48.5% and transport taxes 41.6% of Malta’s environmental tax "
           "revenue [2]. The Commission writes “around 49% and 41%”. The energy share rounds to 49%; the transport share "
           "rounds to 42%, not 41%. We treat this as within ‘around’: the two categories together are 90.2% in "
           "Eurostat and 90% in the Commission’s sentence."))
S.append(P("<b>Pollution and resources.</b> The sentence puts the 0.18% in the same breath as the 2023 split. Eurostat’s "
           "value for Malta is 0.18% in 2022, 0.15% in 2023 and 0.14% in 2024 [2]. The EU-27 value is 0.08% in each of the "
           "three years. So “0.18%” is correct for 2022 but not for 2023, and the “EU average: 0.08%” is correct for either. "
           "The difference is 0.03 percentage points of GDP (roughly EUR 7 million at 2024 GDP) and does not change the "
           "Commission’s point, that Malta’s pollution-and-resources taxes are above the EU average: 0.15% against 0.08% is still "
           "almost twice the EU rate. We cannot tell whether the Commission used an earlier release of the data or took "
           "the 2022 value; the report does not say, and we did not test earlier Eurostat vintages."))

S.append(CondPageBreak(95 * mm))
S.append(SectionHeading(5, "What the measure does and does not show"))
S.append(P("<b>It is a revenue measure.</b> Environmental tax revenue as a share of GDP depends on how much of the taxed "
           "activity there is (fuel sold, vehicles registered), on the tax rate, and on the size of GDP. A lower share can "
           "mean lower rates, a smaller taxed base, or faster GDP growth; it does not by itself show how much "
           "environmental damage is priced. In a study of 27 OECD economies over 1995–2023, environmental taxes were found to "
           "reduce ecological footprints on average only insignificantly, with an effect that grew where environmental "
           "pressure was higher [5]. We read the abstract only. That finding supports caution, not a conclusion about Malta."))
S.append(P("<b>A different denominator gives a different picture in some years.</b> As a share of total taxes and social "
           "contributions (excluding imputed contributions), Malta’s environmental taxes were 5.68% in 2023, above the EU-27’s "
           "5.29%, and 4.69% in 2024, below the EU-27’s 5.28% [2]. The Commission’s text uses the share of GDP, which is the "
           "standard comparison, and we do not say the choice is wrong; but the statement “lower than the EU average” depends "
           "on the measure and the year. Malta’s total tax take is lower than the EU’s (28.9% of GDP in 2024 against 39.4% "
           "for the EU-27, in the report’s own Annex 3 table [1]), which lowers every tax category when measured against "
           "GDP."))
S.append(P("<b>Scale.</b> The gap of 0.73 percentage points of GDP in 2024 is equivalent to about EUR 168 million a year at "
           "Malta’s 2024 GDP [2]. This is an illustration of scale, not a forecast and not a recommendation: it assumes the "
           "same base and GDP, and says nothing about what rates would achieve it."))

S.append(CondPageBreak(80 * mm))
S.append(SectionHeading(6, "Testing the claim"))
S.append(std_table([
    [C("Sub-claim", cellh), C("What the evidence shows", cellh), C("Rating", cellh)],
    [C("<b>A.</b> Total environmental tax revenue is lower than the EU average: 1.4% of GDP in 2024, EU 2.1%"),
     C("Eurostat: 1.35% and 2.08%; recomputed from euro revenue and GDP; Malta 25th of 27 [2, 3].", ), verd("ACCURATE", GREENC)],
    [C("<b>B.</b> In 2023 revenues were primarily from energy and transport taxes, around 49% and 41%"),
     C("48.5% and 41.6% [2]; together 90.2%.", ), verd("ACCURATE", GREENC)],
    [C("<b>C.</b> Pollution and resource taxes 0.18% of GDP (EU average 0.08%), in the 2023 sentence"),
     C("0.18% is Eurostat’s 2022 value; 2023 is 0.15%, 2024 is 0.14%; EU 0.08% in each year [2]. Still above the EU average.", ),
     verd("MINOR ERROR OF YEAR", LG)],
], [58 * mm, 82 * mm, 30 * mm], valign="MIDDLE"))
S.append(P("The Commission’s recommendation that Malta develop its fiscal tools is policy advice and is not rated.", cap))

S += [Spacer(1, 6 * mm), SectionHeading(7, "Verdict and requests for evidence"),
      verdict_box("Largely supported", "The headline and the composition are exact; one figure is from the previous year. Confidence: high."),
      Spacer(1, 4 * mm)]
S.append(P("<b>Why.</b> (1) The central claim, that Malta’s environmental tax revenue is below the EU average, with figures of "
           "1.4% and 2.1% of GDP, matches Eurostat and recomputes from euro revenue and GDP. (2) The 2023 split agrees with "
           "Eurostat. (3) One figure, the 0.18% for pollution and resources, belongs to 2022 and not to the year the sentence "
           "names; the correct 2023 value, 0.15%, supports the same point. These are minor caveats, which is why the verdict is "
           "‘largely supported’ rather than ‘supported’. Confidence is high because the Commission’s source and Eurostat’s "
           "series agree on every other figure and we recomputed them. <b>What this verdict does not say.</b> It does "
           "not say that Malta’s environmental policy is weak or strong, or that higher taxes are the right response."))
S.append(P("Evidence we are asking for", h2))
S.append(requests_list([
    "European Commission: the data vintage behind the 0.18% in the Country Report, or a correction to the year.",
    "Ministry for Finance: the revenue by tax (fuel duty, vehicle registration and circulation taxes, others) behind "
    "Eurostat’s three categories, so that the fall since 2019 can be attributed.",
]))
S += [Spacer(1, 4 * mm),
      callout([P("RIGHT OF REPLY", tag), P("Not needed for this verdict (maintainer rule of 5 October 2026).", small)],
              bg=AMBER_PALE, bar=AMBER)]
S += [Spacer(1, 6 * mm), SectionHeading(8, "Limitations")]
for l in ["Eurostat revises its series; the values here are those of the 10 February 2026 release (environmental taxes) and the "
          "22 October 2026 release (GDP). We did not find or test earlier vintages.",
          "We tested Eurostat’s tables, not Malta’s tax rates or the underlying national accounts. The Commission’s Annex 3 table also "
          "draws on the OECD and other sources that we did not read beyond the rows cited.",
          "The peer-reviewed study cited is read as an abstract only and concerns OECD countries, not Malta.",
          "Malta’s 2023 shares are computed from euro revenue by category; the Commission’s “around 49% and 41%” may have been "
          "computed from another vintage or rounding.",
          "We do not know why the 0.18% appears; the explanation of a prior vintage is a possibility we could not test."]:
    S.append(P("• " + l, bul))

S += [Spacer(1, 6 * mm), SectionHeading(None, "References")]
S += references([
    ("1", "European Commission (3 Jun 2026; transmitted to the Council 8 Jun 2026). 2026 Country Report – Malta, "
          "SWD(2026) 218 final, Annexes (Council document 10135/26 ADD 1), PDF pp. 44 (circular economy section) and 77 "
          "(Annex 3, taxation).", "https://data.consilium.europa.eu/doc/document/ST-10135-2026-ADD-1/en/pdf"),
    ("2", "Eurostat. Revenue from environmental taxes (env_ac_tax), 2015–2024, Malta, EU-27 and the 27 Member States, "
          "dataset updated 10 Feb 2026; downloaded 26 Oct 2026.", "https://ec.europa.eu/eurostat/databrowser/view/env_ac_tax"),
    ("3", "Eurostat. GDP and main components, current prices (nama_10_gdp, B1GQ, CP_MEUR), downloaded 26 Oct 2026.",
     "https://ec.europa.eu/eurostat/databrowser/view/nama_10_gdp"),
    ("4", "Eurostat. Environmental taxes (env_ac_tax_esms): concepts and definitions, reference metadata.",
     "https://ec.europa.eu/eurostat/cache/metadata/en/env_ac_tax_esms.htm"),
    ("5", "Turan T., Esen Ö., Yıldırım S. (2026). Do environmental taxes prioritise environmental effectiveness or "
          "revenue-raising motivation? Evidence from OECD countries. <i>Sustainability</i> 18(17):8703. "
          "doi:10.3390/su18178703. (Abstract read.)", "https://doi.org/10.3390/su18178703"),
    ("6", "Miżien. Data and calculations: data/cc-134/; tools/cc-134-report/calc.py (checks.csv).", ""),
])
S.append(PageBreak())
S += appendix_a("A experiment · B observational study with a control or gradient · C review, guidance or official "
                "statistics · D assertion or anecdote. ◆ marks a source known only second-hand.")
S += [Spacer(1, 5 * mm)]
S += revision_log([("1.0", "26 Oct 2026", "First issue. Verdict Largely supported (high confidence); no right of reply needed.")])

build_report(Report(
    number="134", out=str(FIG / "report.pdf"), kicker="Climate policy and taxation",
    title_lines=["Malta’s environmental", "taxes: below the", "EU average?"],
    subtitle_lines=["Testing the Commission’s 2026 Country Report", "against Eurostat’s environmental tax accounts"],
    quote_lines=["“Total environmental tax revenue is lower than the", "EU average (1.4% of GDP in 2024 against 2.1%).”"],
    quote_size=14.5,
    attribution="European Commission, 2026 Country Report – Malta, 3 June 2026.",
    context="Annex 10, circular economy: ‘Malta has scope to develop its fiscal tools’.",
    verdict="Largely supported", verdict_note="Figures exact; one number is from the previous year",
    footer_lines=["Version 1.0  ·  26 October 2026", "Status:",
                  "Prepared from public sources and Eurostat data.", "Repository: github.com/leandergrech/Mizien"],
    running_head="Environmental taxes – European Commission", version="1.0", date="26 October 2026",
    pdf_title="Malta's environmental taxes below the EU average? Claim Check 134",
    pdf_subject="Tests the Commission's 2026 Country Report statement on Malta's environmental tax revenue",
    story=S))
