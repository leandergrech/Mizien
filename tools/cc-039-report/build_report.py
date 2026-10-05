"""Claim Check 039 report. Run calc.py and figures.py first. Output: out/report.pdf"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import *  # noqa: E402,F401

FIG = HERE / "out"
S = []

# ================================================================== TL;DR
S += [SectionHeading(None, "TL;DR"), Spacer(1, 1 * mm),
      P("In a statement of 2 April 2019 [1], the <b>Water Services Corporation (WSC)</b> said that the EU part-financed "
        "<b>Net Zero Impact Utility</b> project would cut its groundwater abstraction “by 4 billion litres per year” and "
        "produce “much more water with less energy”. The project’s framework has also been described as letting "
        "extra production be met “without increasing the overall net power requirements” of the utility [3]. We tested "
        "these statements against WSC’s own production reports and Eurostat.", lead)]
S.append(key_points([
    ("The groundwater pledge has no baseline and no date.",
     "4 billion litres is 4.0 million m³, about 30% of the 13.5 million m³ WSC took from boreholes in 2016 [4]. WSC "
     "does not say from which year, or by when."),
    ("Measured against 2016, the cut so far is real but partial.",
     "WSC groundwater production was 11.5 million m³ in 2025 [6], 2.0 million m³ below 2016: about half the pledged "
     "amount. In 2023 and 2024 it was only 0.3–0.4 million m³ below. Eurostat’s public-supply series is 1.0–1.2 million "
     "m³ lower in 2024 than in 2018–19 [7]."),
    ("More water now comes from desalination, which costs energy.",
     "Reverse-osmosis output rose about 50% between 2016 and 2025 (18.6 to 27.9 million m³) [4, 6]. At the 2016 "
     "specific energy that is about 45 GWh more electricity a year; to stand still, specific energy would have to fall "
     "by a third."),
    ("Pledge label: not measurable (as of 5 October 2026).",
     "Neither promise states a baseline, boundary or date, and WSC’s total electricity use by year was not found. "
     "That is a gap in what WSC published, not a finding of failure."),
]))
S += [Spacer(1, 4 * mm), VerdictMeter(0, scale="pledge"), Spacer(1, 3 * mm),
      tiles([("−2.0 million m³", GREEN, "WSC groundwater production, 2025 vs 2016 (pledge: −4.0)"),
             ("49%", ORANGE, "of the pledged cut seen in 2025 against 2016; 10% in 2024"),
             ("+50%", RED, "reverse-osmosis output, 2016 to 2025"),
             ("−33%", ORANGE, "fall in specific energy needed to hold RO electricity flat")]),
      Spacer(1, 4 * mm),
      up_down("A stated baseline year and completion date for the 4 billion litre cut, and WSC’s total electricity use "
              "(kWh) by year on a stated boundary, showing it flat or falling while production rose.",
              "WSC’s own series showing groundwater production back near 13 million m³ with the project complete, or "
              "metered electricity use rising with production.",
              heads=("What would make it measurable or on track", "What would count against it")),
      Spacer(1, 5 * mm)]
S += toc([("1", "The statements and their sources"), ("2", "Method"), ("3", "Groundwater: what the data show"),
          ("4", "Energy: what the data show"), ("5", "Testing the statements"),
          ("6", "Pledge label and requests for evidence"), ("7", "Limitations")])
S.append(PageBreak())

# ================================================================== 1
S.append(SectionHeading(1, "The statements and their sources"))
S.append(P("Our candidate record combined several statements from different documents. We read two WSC pages (through "
           "the Internet Archive, because wsc.com.mt shows a bot challenge to scripts) and a peer-reviewed overview by an "
           "Energy and Water Agency author, and separate what each says."))
S.append(std_table([
    [C("Source", cellh), C("Wording", cellh), C("Status", cellh)],
    [C("<b>WSC</b> news release, 2 April 2019 [1]"),
     C("“The Corporation’s ground water abstraction will be reduced by 4 billion litres per year.” Also: the "
       "capacity and efficiency of the desalination plants “are being upgraded thereby producing much more water with "
       "less energy”."), C("<b>Primary wording</b> (verbatim)")],
    [C("<b>WSC</b> project page, 16 April 2018 [2]"),
     C("Describes the project’s components (more efficient RO plants, many more remotely monitored boreholes “rested” "
       "as needed, a new RO plant at Ħondoq, a tunnel from Pembroke to Ta’ Qali). Says the tunnel will save “approximately "
       "3.5 Giga Watts of energy” (sic) and about 1,800 t of CO₂ a year. No groundwater volume."),
     C("Primary; context")],
    [C("<b>Sapiano</b> (Energy and Water Agency), <i>Acque Sotterranee</i> 2020, p. 30 [3]"),
     C("Describes WSC’s “Net-Zero Impact” framework (citing WSC 2018, which we did not read): it aims to "
       "“enable any increased production to address water demand to be met without increasing the overall net power "
       "requirements of the water utility”."),
     C("Second-hand description of WSC’s aim")],
], [44 * mm, 100 * mm, 26 * mm]))
S += [Spacer(1, 4 * mm),
      callout([P("WHAT THIS CHECK DOES NOT COVER", tag),
               P("The idea that the utility gives back to the aquifer “at least as much” water as it abstracts is a "
                 "different statement, tracked as Claim Check 108. “No net increase in energy use”, as our candidate "
                 "record put it, is not WSC’s wording in either page we read; it paraphrases the framework as Sapiano "
                 "describes it [3]. We treat it as that and say so.", small)], bg=AMBER_PALE, bar=AMBER),
      Spacer(1, 4 * mm)]

# ================================================================== 2
S.append(SectionHeading(2, "Method"))
S.append(P("<b>Question.</b> Is there evidence that WSC’s groundwater abstraction has fallen by 4 billion litres a year, "
           "and that it produces more water without more energy? Can either promise be checked as worded?"))
S.append(P("<b>Groundwater.</b> 4 billion litres = 4.0 million m³ (1 m³ = 1,000 litres). We compare it with WSC’s "
           "reported groundwater production: 2016 from WSC’s 2016 annual report [4] (the last year before the project "
           "framework that we could read in full), and 2022–2025 from the 2025 report’s production chart [6], "
           "transcribed for Claim Check 009 (WSC’s 2022 report gives about 12.7 million m³ for 2022 [5], the same). We "
           "also use Eurostat’s public-supply groundwater abstraction for 2018, 2019 and 2024 [7] (estimated values, "
           "a different measure that runs about 1 million m³ above WSC’s own series). Years 2017–2021 were not read."))
S.append(P("<b>Energy.</b> WSC’s 2016 report gives the specific power of its RO plants (4.85 kWh/m³) [4]. We multiply "
           "volume by specific energy for 2016, and show two projections for 2024–2025: one holding the 2016 specific "
           "energy (a scenario) and one using the 4.68 kWh/m³ that WSC’s 2024 report is said to give (second-hand: we could "
           "not open that report, so this is indicative only). We found no total kWh for the whole utility. Code: "
           "<i>tools/cc-039-report/calc.py</i>; results in <i>data/cc-039/checks.csv</i>."))
S.append(P("<b>Grades.</b> WSC’s annual reports are self-reported company documents (C); Eurostat figures are official "
           "statistics, flagged as estimates (C); our arithmetic is an order-of-magnitude check and is labelled as such."))

# ================================================================== 3
S.append(PageBreak())
S.append(SectionHeading(3, "Groundwater: what the data show"))
S.append(fig(FIG / "fig1_groundwater.png"))
S.append(P("Figure 1. WSC groundwater production (boreholes and pumping stations, Malta and Gozo) against the level the "
           "pledge would imply if the baseline were 2016.", cap))
S.append(std_table([
    [C("Measure", cellh), C("Baseline", cellh), C("Latest", cellh), C("Change", cellh), C("Share of the 4.0 pledged", cellh)],
    [C("WSC groundwater production, 2016 → 2025 [4, 6]"), C("13.51"), C("11.54"), C("−1.96"), C("<b>49%</b>")],
    [C("WSC groundwater production, 2016 → 2024 [4, 6]"), C("13.51"), C("13.09"), C("−0.41"), C("10%")],
    [C("Eurostat public supply, 2018 → 2024 [7]"), C("15.24"), C("14.28"), C("−0.96"), C("24%")],
    [C("Eurostat public supply, 2019 → 2024 [7]"), C("15.52"), C("14.28"), C("−1.24"), C("31%")],
], [70 * mm, 20 * mm, 20 * mm, 20 * mm, 40 * mm]))
S.append(P("All volumes in million m³. A full 4.0 million m³ cut from the 2016 level would leave 9.5 million m³; "
           "no year we read is near that.", cap))
S.append(callout([P("READING THE NUMBERS", tag),
                  P("The 2025 figure is the lowest we have, and WSC attributes lower groundwater use to a lower-salinity blend and more RO water [5, 6]. It follows a 2024 value only 0.4 million m³ below 2016, "
                    "so one year is not yet a trend. WSC groundwater is also a small part of national abstraction: "
                    "4.0 million m³ is about 10% of Malta’s 38.5 million m³ of fresh groundwater abstracted in 2024 "
                    "(Eurostat, estimated), most of it by agriculture [7].", small)], bg=BLUE_PALE, bar=BLUE))
S.append(Spacer(1, 3 * mm))
S.append(P("Fairness to WSC", h2))
for t in ["• Its groundwater share of production fell from 42% (2016) to 29% (2025) while total production grew by "
          "about 23% (32.1 to 39.5 million m³) [4, 6]. Put against demand growth, the groundwater cut is larger than "
          "the raw change suggests.",
          "• WSC’s 2022 report describes reactivating eight boreholes or pumping sources by 2022 to spread abstraction "
          "(to relieve local pressure) [5]. Spreading abstraction is a quality aim; it does not by itself reduce volume.",
          "• The 2019 statement gave no baseline or date; we chose 2016 as a published pre-project reference and "
          "other choices move the result."]:
    S.append(P(t, bul))

# ================================================================== 4
S.append(CondPageBreak(95 * mm))
S.append(SectionHeading(4, "Energy: what the data show"))
S.append(fig(FIG / "fig2_ro_energy.png"))
S.append(P("Figure 2. Estimated electricity for reverse osmosis: 2016 (WSC report), 2024 using a second-hand specific "
           "energy, and a 2025 scenario holding the 2016 specific energy.", cap))
S.append(std_table([
    [C("Input or result", cellh), C("Value", cellh), C("Source", cellh)],
    [C("RO output 2016 → 2025"), C("18.6 → 27.9 million m³ (+50%)"), C("WSC AR 2016, AR 2025 [4, 6]")],
    [C("RO specific energy 2016"), C("4.85 kWh/m³"), C("WSC AR 2016 [4]")],
    [C("RO electricity 2016 (estimate)"), C("90 GWh"), C("calculated")],
    [C("Specific energy for flat RO electricity in 2025"), C("3.24 kWh/m³ (−33%)"), C("calculated")],
    [C("RO electricity 2024 at 4.68 kWh/m³"), C("120 GWh (+33%)"), C("second-hand input; indicative")],
    [C("Electricity bill 2016, RO plants’ share"), C("€10.1M of €16.6M (61%)"), C("WSC AR 2016, note 2 [4]")],
    [C("Ħondoq RO plant vs conventional plants"), C("23.5% less energy"), C("WSC AR 2022 [5]")],
], [70 * mm, 55 * mm, 45 * mm]))
S.append(P("The 2024 specific energy (4.68 kWh/m³, +1.4% on 2023) and the Ħondoq plant’s 3.11 kWh/m³ are known to us "
           "only from a summary of WSC’s 2024 report; they are not used for any rating.", cap))
S.append(P("What the energy data mean", h2))
for t in ["• <b>“Much more water with less energy” can be read per cubic metre.</b> On that reading, WSC’s 2016 figure "
          "(4.85 kWh/m³) and the second-hand 2024 figure (4.68) differ by 3.5%; the Ħondoq plant, which WSC says uses "
          "23.5% less energy than conventional plants [5], serves a small share of output (5.0% of RO water in 2022 [5]).",
          "• <b>“Without increasing the overall net power requirements” is a total, not a per-unit, claim.</b> RO "
          "output grew by half; a fall of a third in specific energy would be needed to keep RO electricity flat. The "
          "figures we have point the other way. WSC’s own 2022 report says its expenditure rose by about €2 "
          "million in energy consumed, which it ties to “a strategic decision to improve potable water quality by increasing the "
          "production from its reverse osmosis plants” [5].",
          "• <b>The offsetting savings WSC cites are small.</b> The Pembroke–Ta’ Qali tunnel is said to save about "
          "3.5 GWh a year (WSC writes “Giga Watts”) [2], against an RO increase of tens of GWh. WSC’s figure is its own estimate.",
          "• <b>We could not test the whole utility.</b> Groundwater pumping, sewage treatment and distribution "
          "energy, and any renewable generation, are outside our RO estimate, and no total kWh by year was found."]:
    S.append(P(t, bul))

# ================================================================== 5
S.append(CondPageBreak(80 * mm))
S.append(SectionHeading(5, "Testing the statements"))
verd = lambda t, c: chip(t, c, w=29 * mm)
S.append(std_table([
    [C("Sub-claim", cellh), C("Said by", cellh), C("What the evidence shows", cellh), C("Rating", cellh)],
    [C("<b>A.</b> Groundwater abstraction “will be reduced by 4 billion litres per year”"), C("WSC [1]"),
     C("No baseline year or date. Against 2016, WSC groundwater production is lower by 0.4–2.0 million m³ in "
       "2022–25 (10–49% of 4.0), lowest in 2025."), verd("NO BASELINE OR DATE", ORANGE)],
    [C("<b>B.</b> Desalination produces “much more water with less energy”"), C("WSC [1]"),
     C("More water: RO output +50% since 2016. Less energy per m³: small at best (4.85 to 4.68 kWh/m³, second-hand); "
       "RO electricity use is likely higher in total."), verd("MIXED", ORANGE)],
    [C("<b>C.</b> Extra production without increasing the utility’s overall net power requirements"),
     C("WSC framework, as described in [3]"),
     C("RO alone would need a third lower specific energy to stay flat. No whole-utility kWh found."),
     verd("NOT TESTABLE AS WORDED", GREY)],
], [46 * mm, 22 * mm, 68 * mm, 34 * mm], valign="MIDDLE"))

# ================================================================== 6
S += [Spacer(1, 6 * mm), SectionHeading(6, "Pledge label and requests for evidence"),
      verdict_box("Not measurable", "As of 5 October 2026. No baseline, date or boundary stated; indicators move the "
                  "right way for groundwater and the wrong way for RO energy."), Spacer(1, 4 * mm)]
S.append(P("<b>Why.</b> Both promises are statements of intended outcome. The groundwater promise names an amount but "
           "no starting year and no completion date; the energy promise names no baseline, boundary or date. A pledge is "
           "not a statement of fact, so we do not call it false. As worded it cannot be shown to have been met or missed, "
           "so we label it <i>Not measurable</i> (Appendix A lists the six pledge labels). Our indicative figures are "
           "given so readers can see where the data point."))
S.append(P("<b>What this label does not say.</b> It does not say the project failed, that WSC’s figures are wrong, or "
           "that the aim is undesirable. Water security and lower energy intensity are sound goals. A checkable version "
           "would read: <i>“Compared with [year], WSC’s groundwater production will fall by 4.0 million m³ a year by "
           "[date], while its total electricity use stays at or below [X] GWh.”</i>"))
S.append(CondPageBreak(45 * mm))
S.append(P("Evidence we are asking for", h2))
S.append(requests_list([
    "From WSC: the baseline year and completion date behind “4 billion litres per year”, and annual groundwater "
    "abstraction by source since 2014.",
    "From WSC: total electricity consumption (kWh) by year, split by RO, groundwater pumping, distribution and sewage "
    "treatment, and the boundary of “net zero” impact on energy.",
    "From WSC: whether all components of the Net Zero Impact Utility project are complete, and the 2018 framework "
    "document that Sapiano [3] cites.",
    "From WSC: the specific energy of each RO plant by year, including the 2024 figures.",
]))
S += [Spacer(1, 4 * mm),
      callout([P("RIGHT OF REPLY", tag),
               P("Before wider circulation this draft should be sent to the Water Services Corporation with a fixed "
                 "deadline (suggested 14 days). Responses will be appended and the label revisited.", small)],
              bg=AMBER_PALE, bar=AMBER)]

# ================================================================== 7
S += [Spacer(1, 6 * mm), SectionHeading(7, "Limitations")]
for l in ["WSC’s 2016 and 2025 production series come from different reports; we did not verify that definitions "
          "match (WSC’s 2022 report agrees with the 2025 report for 2022). Years 2017–2021 were not read.",
          "The 2025 values are read from a chart and carry the small internal differences recorded for Claim Check 009.",
          "The 4.68 kWh/m³ figure is second-hand and used only for an indicative bar. WSC’s 2024 report could not be "
          "opened (parlament.mt refuses scripts).",
          "The RO electricity estimates are volume times specific energy, not metered totals.",
          "We did not establish which project components were complete, or when. The live wsc.com.mt pages show a bot "
          "challenge to scripts; both WSC pages were read in Wayback copies of 2024.",
          "Sapiano’s description of the framework cites a WSC 2018 document that we did not read."]:
    S.append(P("• " + l, bul))

S += [Spacer(1, 6 * mm), SectionHeading(None, "References")]
S += references([
    ("1", "Water Services Corporation (2 April 2019). European Commission Endorses WSC’s ‘Net Zero-Impact’ Utility "
          "Project. News release. (Read in the Internet Archive copy of 10 Sep 2024.)",
     "https://www.wsc.com.mt/european-commission-endorses-wscs-net-zero-impact-utility-project/"),
    ("2", "Water Services Corporation (16 April 2018). Towards a Net Zero-Impact Utility: new €100 Million EU-funded project "
          "set to improve water quality to all-new highs. (Read in the Internet Archive.)",
     "https://www.wsc.com.mt/towards-a-net-zero-impact-utility-new-e100-million-eu-funded-project-set-to-improve-water-quality-to-all-new-highs/"),
    ("3", "Sapiano M. (2020). Integrated Water Resources Management in the Maltese Islands. <i>Acque Sotterranee – "
          "Italian Journal of Groundwater</i> 9(3):25–32. doi:10.7343/as-2020-477. (Full text read; open access.)",
     "https://doi.org/10.7343/as-2020-477"),
    ("4", "Water Services Corporation (2017). Annual Report 2016, pp. 9–10 and note 2. (Read in the Internet Archive copy.)",
     "https://www.wsc.com.mt/wp-content/uploads/2018/03/Annual_Report_-_16.pdf"),
    ("5", "Water Services Corporation (2023). Annual Report 2022, pp. 13–14 and 28. (Read in the Internet Archive copy.)",
     "https://www.wsc.com.mt/wp-content/uploads/2023/06/WSC-Annual-Report-2022.pdf"),
    ("6", "Water Services Corporation. Annual Report 2025, Figure 20 (groundwater and RO production, 2022–2025), as "
          "transcribed for Claim Check 009. Supplied by the maintainer; this site could not open it.",
     "https://parlament.mt/media/139352/wsc-annual-report-2025.pdf"),
    ("7", "Eurostat. Water abstraction by source and sector (env_wat_abs), Malta, fresh groundwater; updated 16 Sep 2026, "
          "retrieved 5 Oct 2026. Values flagged ‘e’ (estimated).",
     "https://ec.europa.eu/eurostat/databrowser/view/env_wat_abs/default/table"),
    ("8", "MiŻien. Analysis code and outputs: tools/cc-039-report/; data/cc-039/. The 2024 specific energy (4.68 "
          "kWh/m³) is from a search-engine summary of WSC’s Annual Report 2024 (parlament.mt/media/134182), not read directly.", ""),
])

S.append(PageBreak())
S += appendix_a("A experiment · B observational study with a control or gradient · C review, guidance or "
                "official statistics · D assertion or anecdote. WSC annual reports are self-reported (C); our own "
                "arithmetic is an order-of-magnitude estimate.", pledges=True)
S += [Spacer(1, 5 * mm)]
S += revision_log([("1.0", "5 Oct 2026", "First issue. Pledge label: not measurable. Groundwater: no baseline or date; "
                                         "against 2016, WSC production was 2.0 million m³ lower in 2025 (49% of the "
                                         "pledged 4.0). Energy: RO output up 50% since 2016; WSC’s total electricity "
                                         "use not found. Draft pending right of reply from the Water Services "
                                         "Corporation.")])

build_report(Report(
    number="039", out=str(FIG / "report.pdf"), kicker="Water, checked",
    title_lines=["A net-zero-impact", "water utility?"],
    subtitle_lines=["Testing WSC’s promise of 4 billion litres less", "groundwater and less energy per litre"],
    quote_lines=["“The Corporation’s ground water abstraction will be", "reduced by 4 billion litres per year.”"],
    quote_size=14,
    attribution="Water Services Corporation, news release, 2 April 2019.",
    context="Same release: desalination upgrades mean “much more water with less energy”.",
    verdict="Not measurable", verdict_note="As of 5 Oct 2026: no baseline, date or boundary stated",
    footer_lines=["Version 1.0  ·  5 October 2026",
                  "Status: draft pending right of reply (Water Services Corporation)",
                  "Prepared from public sources and open data. No site visits.", "Repository: github.com/leandergrech/Mizien"],
    running_head="Net Zero Impact Utility – WSC 2019", version="1.0", date="5 October 2026",
    pdf_title="A net-zero-impact water utility? Claim Check 039",
    pdf_subject="Tests WSC's 2019 statements on groundwater abstraction and energy in its Net Zero Impact Utility project",
    story=S))
