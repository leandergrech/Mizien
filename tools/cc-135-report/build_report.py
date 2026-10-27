"""Claim Check 135 report. Run fetch.py, calc.py and figures.py first. Output: out/report.pdf"""
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
      P("In a February 2025 Selected Issues paper on Malta’s infrastructure, IMF staff wrote: <b>“Peak electricity demand "
        "has increased rapidly in recent years, rising from 465 MW in 2018 to 663 MW in 2023 (an increase of 43 "
        "percent). This increase has significantly outpaced the growth in population and tourists in the peak summer "
        "season (an increase of 13 percent over the same period).”</b> The paper adds that this “may be related” to a "
        "rise in the mean temperature of the hottest month from 27.3 °C to 29.6 °C. We checked every number against the "
        "National Statistics Office’s electricity releases, Eurostat’s population and tourism tables, and the Luqa "
        "weather station record.", lead)]
S.append(key_points([
    ("The two peaks and the 43% are exact.",
     "The NSO gives a maximum demand of 465 MW in August 2018 and 663 MW in July 2023, the highest month of each year. "
     "The rise is 42.6%."),
    ("The 13% reproduces with the IMF’s own method.",
     "Residents plus tourists (nights in the peak month divided by 31, as the paper’s chart note says) grew by 13.3% to "
     "13.5% between 2018 and 2023, whichever Eurostat population count is used. Residents alone grew about 14%, "
     "tourists in August about 3%."),
    ("Peak demand did outpace population, in any window.",
     "Electricity used over the year grew about as fast as the population (final consumption +13.4%), while the peak "
     "rose much faster. The linear trend over 2017–2025 adds about 24% in five years, still well above 13%."),
    ("The end years make the rise look its largest.",
     "At Luqa, 2018 had the coolest hottest-month of 2017–2025 and 2023 the hottest. Other windows give 28% to 37%; the "
     "peak fell to 593 MW in 2024 before rising to 637 MW in 2025. The paper itself points to temperature."),
    ("Verdict: largely supported (high confidence).",
     "Every figure checks and the comparison holds. The caveat is that 43% compares a cool year with a record-hot one, "
     "so it overstates the underlying trend."),
]))
S += [Spacer(1, 2.5 * mm), VerdictMeter(1), Spacer(1, 3 * mm),
      tiles([("663 MW", GREEN, "Peak demand, July 2023 (NSO); 465 MW in August 2018"),
             ("+42.6%", GREEN, "Rise in peak demand 2018–2023 (IMF: 43%)"),
             ("+13.4%", GREEN, "Residents plus peak-month tourists 2018–2023 (IMF: 13%)"),
             ("+24%", AMBER, "Rise over five years on the 2017–2025 trend line, without the end-year effect")]),
      Spacer(1, 4 * mm),
      up_down("A ‘Supported’ verdict would need the 43% to describe the trend rather than two end years, for example if "
              "the IMF had shown that the rise holds with temperature taken into account, or with averaged end years.",
              "Evidence that the NSO has revised the 2018 or 2023 peak, or that the IMF used a different series that "
              "does not give 465 MW and 663 MW."),
      Spacer(1, 3 * mm)]
S += toc([("1", "The claim and what we could verify"), ("2", "Method"), ("3", "The peak-demand figures"),
          ("4", "The 13 percent: population and tourists"), ("5", "Peak against energy and temperature"),
          ("6", "Testing the claim"), ("7", "Verdict and requests for evidence"), ("8", "Limitations")])
S.append(PageBreak())

S.append(SectionHeading(1, "The claim and what we could verify"))
S.append(P("The claim is paragraph 5 of <i>Taking Stock of Infrastructure in Malta</i>, IMF Selected Issues Paper "
           "SIP/2025/007 by Alexander Pitt, European Department, dated February 2025 (information as of 17 December 2024; "
           "also published as IMF Country Report No. 25/18) [1]. Selected Issues papers give the views of the author and "
           "IMF staff, not of the IMF’s Executive Board. The paragraph, on page 4, reads:"))
S.append(P("“Peak electricity demand has increased rapidly in recent years, rising from 465 MW in 2018 to 663 MW in 2023 "
           "(an increase of 43 percent). This increase has significantly outpaced the growth in population and tourists "
           "in the peak summer season (an increase of 13 percent over the same period). In part, this may be related to "
           "the rise in mean temperatures in the hottest month from 27.3 °C to 29.6 °C.”", bul))
S.append(P("A footnote adds: “Peak temperatures rose from 34 °C to almost 42 °C over the same period.” The paragraph’s "
           "chart (‘Population, Temperature, and Energy’) plots population plus tourists, peak electricity demand and the "
           "hottest-month mean temperature for 2018–2023, with the note “Number of tourists: nights spent in peak month "
           "divided by 31” and the sources “Authorities’ data, Eurostat, and IMF staff estimates” [1]. The paper does not "
           "name the series behind the 465 and 663 MW."))
S.append(std_table([
    [C("What was said", cellh), C("Who", cellh), C("Access", cellh)],
    [C("Peak demand 465 MW (2018) to 663 MW (2023), +43%"), C("IMF staff [1]"), C("Read (paper, p. 4)")],
    [C("Outpaced population and tourists in the peak summer season (+13%)"), C("IMF staff [1]"), C("Read (paper, p. 4)")],
    [C("May be related to hottest-month mean 27.3 °C to 29.6 °C; peaks 34 °C to almost 42 °C"), C("IMF staff [1]"),
     C("Read (paper, p. 4)")],
    [C("Maximum demand by month and year"), C("NSO [2–6]"), C("Read: Table 7 for 2017–2021; release text for 2022–2025")],
], [96 * mm, 30 * mm, 44 * mm]))
S += [Spacer(1, 4 * mm),
      callout([P("SCOPE NOTE", tag),
               P("This check tests the paper’s figures and its comparison. It does not test the paper’s other statements "
                 "(capacity being adequate, the authorities’ projection of about 30% more peak demand by 2040), the July "
                 "2026 power cuts (CC-027) or the Malta Chamber’s statement on them (CC-137). The IMF’s suggestion that "
                 "temperature plays a part is hedged (“may be related”) and is tested as context, not as a claim of cause.",
                 small)], bg=AMBER_PALE, bar=AMBER), Spacer(1, 4 * mm)]

S.append(SectionHeading(2, "Method"))
S.append(P("<b>Question.</b> Are 465 MW, 663 MW, 43% and 13% what the official series show, and does peak demand outpace "
           "residents and tourists over periods other than 2018–2023? <b>Evidence.</b> The NSO’s annual <i>Electricity "
           "Supply</i> releases, which give the maximum demand in each month, defined as “the highest amount of "
           "electricity consumed at any one point in time across the entire network system” [2–6]; Eurostat’s population "
           "(demo_gind), monthly nights at tourist accommodation (tour_occ_nim) and electricity balance (nrg_cb_e) [7–9]; "
           "and daily temperatures at Luqa from NOAA’s GHCN-Daily archive [10]. The NSO’s site refuses scripts, so its "
           "figures were read through a web reader and transcribed with the release, address and date of each row; the "
           "rest was downloaded by script (<i>tools/cc-135-report/fetch.py</i>) and every figure was computed in "
           "<i>calc.py</i> (results in <i>data/cc-135/checks.csv</i>). <b>Grades.</b> Official statistics are grade C; two "
           "peer-reviewed studies of temperature and peak load are context (grade B) [11, 12]. Verdicts follow the scale in "
           "Appendix A."))

S.append(CondPageBreak(120 * mm))
S.append(SectionHeading(3, "The peak-demand figures"))
S.append(P("The NSO’s release for 2021 prints the maximum demand of every month for 2017–2021 (its Table 7) [2]. The "
           "highest month of 2018 was August, at <b>465 MW</b>. The release for 2023 states that “July and August featured "
           "the highest electricity demand, registering 663 MW and 561 MW respectively” [4]: <b>663 MW</b>. Both match the "
           "IMF’s figures, and 663 / 465 − 1 = 42.6%, which rounds to the IMF’s 43%. The NSO does not say whether the "
           "figure includes power imported through the interconnector; its definition covers consumption “across the "
           "entire network system” [3]."))
S.append(fig(FIG / "fig1_peaks.png"))
S.append(P("Figure 1. Annual peak demand (highest monthly maximum, MW) and the mean temperature of the hottest month at "
           "Luqa, 2017–2025. The IMF’s end years, 2018 and 2023, are the coolest and the hottest summers of the nine.", cap))
S.append(P("Figure 1 puts the two end years in a longer series. The peak was 488 MW in 2017, dipped to 465 MW in 2018, and "
           "then rose to 581 MW in 2022 and 663 MW in 2023. It fell to 593 MW in 2024 and rose again to 637 MW in 2025 [2–6]. "
           "Measured from other end years, the rise is 36% (2017–2023), 32% (2019–2023), 28% (2018–2024) or 37% "
           "(2018–2025). A straight line fitted to the nine annual peaks rises by about 23 MW a year, or 24% over five "
           "years from its 2018 value; averaged over three years, the peak rose 24% from 2017–2019 to 2021–2023 "
           "(<i>checks.csv</i>, B). Every measure is a rapid rise; 43% is the largest of them."))

S.append(CondPageBreak(90 * mm))
S.append(SectionHeading(4, "The 13 percent: population and tourists"))
S.append(P("The paper’s chart note gives the method: tourists are the nights spent in the peak month divided by 31, an "
           "estimate of the tourists present on an average day of that month [1]. Eurostat’s monthly nights at tourist "
           "accommodation establishments peak in August in both years: 1,166,568 nights in August 2018 and 1,200,154 in "
           "August 2023, or about 37,600 and 38,700 tourists a day [8]. Added to the resident population, the total grew by:"))
S.append(std_table([
    [C("Population count used (Eurostat demo_gind)", cellh), C("2018 total", cellh), C("2023 total", cellh),
     C("Growth", cellh), C("Residents only", cellh)],
    [C("1 January of the same year"), C("512,468"), C("580,766"), C("<b>13.3%</b>"), C("14.2%")],
    [C("Annual average"), C("521,534"), C("591,462"), C("<b>13.4%</b>"), C("14.2%")],
    [C("End of year (1 January of the next year)"), C("530,599"), C("602,158"), C("<b>13.5%</b>"), C("14.3%")],
], [66 * mm, 25 * mm, 25 * mm, 22 * mm, 32 * mm]))
S.append(P("Source: Eurostat demo_gind and tour_occ_nim (nights at tourist accommodation, NACE I551–I553, all "
           "residences), retrieved 26 October 2026 [7, 8]. Tourists = August nights / 31.", cap))
S.append(P("All three give 13% when rounded, as the IMF says. The paper’s own text uses the end-of-year count (“around "
           "563,000 at end-2023”), which is Eurostat’s 563,443 for 1 January 2024 [1, 7]. Two things follow. First, the "
           "residents dominate the total: tourists present in August are about 7% of it, and their number grew only about "
           "3%. Second, Eurostat’s accommodation series counts nights in tourist accommodation establishments only; the "
           "NSO’s frontier survey, which also counts stays in private and non-rented accommodation, would give a larger "
           "tourist number. We could not open those releases. Since residents alone grew about 14%, the combined figure would rise above that only if the NSO’s "
           "tourist count grew faster than the residents; we have not tested that series."))

S.append(CondPageBreak(110 * mm))
S.append(SectionHeading(5, "Peak against energy and temperature"))
S.append(fig(FIG / "fig2_index.png"))
S.append(P("Figure 2. Peak demand, the mean of the twelve monthly maxima, final electricity consumption and residents plus "
           "peak-month tourists, indexed to 2018 = 100. The 2023 monthly-maxima value is the one first published (446 MW).", cap))
S.append(P("<b>Energy grew with the population; the peak grew faster.</b> Final electricity consumption rose 13.4% between "
           "2018 and 2023, and supply (production plus imports less exports) 14.8% [9], close to the 13% growth in people "
           "present. The NSO’s ‘annual average demand’, the mean of the twelve monthly maxima, rose 14.9% as first "
           "published (388 to 446 MW) [2, 4]. The annual peak rose 42.6%. As a result, the average load fell from about 63% "
           "to 51% of the peak, and peak demand per person present rose from about 0.89 kW to 1.12 kW (<i>checks.csv</i>, "
           "C and D). This supports the IMF’s point: the peak has been rising faster than the number of people and faster "
           "than the electricity they use over a year."))
S.append(P("<b>Temperature.</b> At the Luqa station, the hottest month averaged 26.9 °C in 2018 (July) and 29.4 °C in 2023 "
           "(July), a rise of 2.5 °C [10]; the IMF gives 27.3 °C and 29.6 °C, a rise of 2.3 °C, from “authorities’ data” we "
           "could not see. The highest daily maximum at Luqa was 35.7 °C in 2018 and 42.7 °C in 2023; the IMF’s footnote "
           "gives 34 °C and “almost 42 °C”. The station series and the IMF’s figures differ by up to 1.7 °C on the 2018 "
           "peak, which may reflect a different station or measure; they agree that 2023 was far hotter than 2018. In the "
           "Luqa record, 2018 had the coolest hottest-month of 2017–2025 and 2023 the hottest."))
S.append(fig(FIG / "fig3_scatter.png", width=118 * mm))
S.append(P("Figure 3. Annual peak demand against the hottest-month mean temperature at Luqa, 2017–2025.", cap))
S.append(P("Across the nine years, annual peak demand and the hottest-month mean go together (Pearson r = 0.70). A simple "
           "fit of the peak on a time trend and that temperature gives a trend of about 19 MW a year and about 34 MW per "
           "1 °C; with temperature held at its average, the fitted rise from 2018 to 2023 is about 19% (<i>checks.csv</i>, "
           "E5–E7). With nine points this is a description, not an estimate of cause, and it leaves out other drivers the "
           "paper names (electric vehicles, shore power for cruise ships) [1]. Larger studies find that daily peak load "
           "rises with hot-day temperatures, more sharply than total consumption, and that warming raises peak load most in "
           "southern Europe [11, 12]."))
S.append(contested(
    "Is 43% the rise in peak demand, or the gap between a cool and a hot summer?", "BOTH, IN PART", AMBER,
    "The figures are exact. Every window and the trend line show peak demand rising faster than residents and tourists "
    "(peak +28% to +43% on the windows tested, +24% on the trend line, against +9% to +20% for residents and tourists over the same windows). Peaks in 2021, 2022 and 2025 were all well above 2018 [2–6].",
    "2018 was the lowest peak and the coolest summer of 2017–2025; 2023 the highest peak and the hottest summer. The peak "
    "fell 10% in 2024. Holding temperature at its average, a simple fit gives about 19% over 2018–2023.",
    "The paper states the end-year change correctly and itself links part of it to temperature. Read as a trend, the "
    "43% is at the top of the range; read as the 2018–2023 change, it is correct. The comparison with 13% survives "
    "either reading."))

S.append(CondPageBreak(90 * mm))
S.append(SectionHeading(6, "Testing the claim"))
S.append(std_table([
    [C("Sub-claim", cellh), C("What the evidence shows", cellh), C("Rating", cellh)],
    [C("<b>A.</b> Peak electricity demand was 465 MW in 2018"),
     C("NSO: maximum demand 465 MW in August 2018, the highest month of the year [2]."), verd("ACCURATE", GREENC)],
    [C("<b>B.</b> Peak electricity demand was 663 MW in 2023"),
     C("NSO: 663 MW in July 2023, the highest month of the year [4]."), verd("ACCURATE", GREENC)],
    [C("<b>C.</b> An increase of 43 percent"), C("663 / 465 − 1 = 42.6% [2, 4]."), verd("ACCURATE", GREENC)],
    [C("<b>D.</b> Population and tourists in the peak summer season grew 13 percent over the same period"),
     C("Reproduced with the IMF’s method: 13.3% to 13.5% depending on the population count; residents alone about 14% [7, 8]."),
     verd("ACCURATE", GREENC)],
    [C("<b>E.</b> Peak demand has increased rapidly and significantly outpaced population and tourists"),
     C("Holds in every window tested (peak +24% to +37% on other end years and the trend); 2018 and 2023 are the coolest and "
       "hottest summers, so 43% is the largest measure [2–6, 10]."), verd("ACCURATE, END-YEAR CAVEAT", LG)],
    [C("<b>F.</b> Hottest-month mean temperature rose from 27.3 °C to 29.6 °C"),
     C("Luqa station: 26.9 °C to 29.4 °C (+2.5 °C against +2.3 °C); the IMF’s source not seen [10]."),
     verd("BROADLY CONFIRMED", LG)],
], [56 * mm, 84 * mm, 30 * mm], valign="MIDDLE"))
S.append(P("The paper’s link between temperature and demand is worded as a possibility (“may be related”) and is not rated "
           "as a claim of cause.", cap))

S += [Spacer(1, 6 * mm), SectionHeading(7, "Verdict and requests for evidence"),
      verdict_box("Largely supported", "Every figure checks; the end years make the rise look its largest. Confidence: high."),
      Spacer(1, 4 * mm)]
S.append(P("<b>Why.</b> (1) The 465 MW, 663 MW and 43% are the NSO’s figures. (2) The 13% reproduces from Eurostat with "
           "the method the paper states. (3) Peak demand outpaced residents and tourists however the period is chosen, "
           "while energy consumed over the year kept pace with them. (4) The one caveat is the choice of end years: 2018 "
           "and 2023 are the coolest and hottest summers of 2017–2025, so 43% is the largest of the measures, against "
           "about 24% on the trend line. The paper points to temperature itself, which is why we treat this as a minor "
           "caveat rather than a flaw. Confidence is high because two independent official sources (NSO, Eurostat) "
           "reproduce every figure. <b>What this verdict does not say.</b> It does not rate the paper’s view that "
           "capacity is adequate, its 2040 projection, or what caused the 2023 and 2026 power cuts."))
S.append(P("Evidence we are asking for", h2))
S.append(requests_list([
    "IMF staff: the series behind the 465 and 663 MW (NSO or Enemalta) and the temperature station used for 27.3 °C, "
    "29.6 °C, 34 °C and 42 °C.",
    "NSO: Table 7 of the 2024 and 2025 releases, to confirm whether the 2023 monthly maxima were revised (the 2024 "
    "release implies a 2023 annual average of about 470 MW, not the 446 MW first published).",
    "Enemalta or the Regulator for Energy and Water Services: hourly system load for 2017–2025, so that peak demand can be "
    "adjusted for temperature properly.",
]))
S += [Spacer(1, 4 * mm),
      callout([P("RIGHT OF REPLY", tag), P("Not needed for this verdict (maintainer rule of 5 October 2026).", small)],
              bg=AMBER_PALE, bar=AMBER)]
S += [Spacer(1, 6 * mm), SectionHeading(8, "Limitations")]
for l in ["The NSO pages refuse scripts; its figures were read through a web reader on 26 October 2026 and transcribed. "
          "Table 7 was read only in the 2021 release; for 2022–2025 we have the highest months and the annual average from "
          "the release text.",
          "The NSO says its data are subject to revision. The 2024 release’s percentage change implies that the 2023 annual "
          "average was revised; we do not know whether the 663 MW peak was.",
          "The IMF paper was read through a web reader on 26 October 2026 (the intake read the PDF on 25 October); the "
          "chart’s plotted values could not be read, so the IMF’s exact population count is inferred.",
          "Eurostat’s tourist nights cover accommodation establishments only; the NSO’s frontier-survey tourists were not "
          "tested.",
          "Temperatures are from one station (Luqa) in NOAA’s archive, not from the Malta Meteorological Office. The fit of "
          "peak on trend and temperature uses nine annual points and leaves out other drivers.",
          "The peer-reviewed studies are read as abstracts only and concern Europe as a whole and the United States, not "
          "Malta."]:
    S.append(P("• " + l, bul))

S += [Spacer(1, 6 * mm), SectionHeading(None, "References")]
S += references([
    ("1", "Pitt A. (February 2025). Taking Stock of Infrastructure in Malta. IMF Selected Issues Paper SIP/2025/007 (also "
          "Country Report No. 25/18), para. 5 and chart, p. 4. Read 26 Oct 2026.",
     "https://meetings.imf.org/-/media/Files/Publications/Selected-Issues-Papers/2025/English/SIPEA2025007.ashx"),
    ("2", "NSO (6 Oct 2022). Electricity Supply: 2021. News release 177/2022, Table 7 (maximum demand 2017–2021).",
     "https://nso.gov.mt/wp-content/uploads/News2022_177.pdf"),
    ("3", "NSO (5 Oct 2023). Electricity Supply: 2022. News release 176/2023.", "https://nso.gov.mt/electricity-supply-2022/"),
    ("4", "NSO (8 Oct 2024). Electricity Supply: 2023. News release 184/2024.", "https://nso.gov.mt/electricity-supply-2023/"),
    ("5", "NSO (8 Oct 2025). Electricity Supply: 2024. News release 178/2025.", "https://nso.gov.mt/electricity-supply-2024/"),
    ("6", "NSO (8 Oct 2026). Electricity Supply: 2025. News release 178/2026.", "https://nso.gov.mt/electricity-supply-2025/"),
    ("7", "Eurostat. Population change – demographic balance (demo_gind), Malta, retrieved 26 Oct 2026.",
     "https://ec.europa.eu/eurostat/databrowser/view/demo_gind"),
    ("8", "Eurostat. Nights spent at tourist accommodation establishments, monthly (tour_occ_nim), Malta, retrieved 26 Oct 2026.",
     "https://ec.europa.eu/eurostat/databrowser/view/tour_occ_nim"),
    ("9", "Eurostat. Supply, transformation and consumption of electricity (nrg_cb_e), Malta, retrieved 26 Oct 2026.",
     "https://ec.europa.eu/eurostat/databrowser/view/nrg_cb_e"),
    ("10", "NOAA NCEI. GHCN-Daily, station MT000016597 (Luqa), retrieved 26 Oct 2026; Menne M.J. et al. (2012). An overview of "
           "the Global Historical Climatology Network-Daily database. <i>J. Atmos. Oceanic Technol.</i> 29(7):897–910. "
           "doi:10.1175/JTECH-D-11-00103.1.", "https://www.ncei.noaa.gov/data/global-historical-climatology-network-daily/access/MT000016597.csv"),
    ("11", "Wenz L., Levermann A., Auffhammer M. (2017). North–south polarization of European electricity consumption under "
           "future warming. <i>PNAS</i> 114(38). doi:10.1073/pnas.1704339114. (Abstract read.)", "https://doi.org/10.1073/pnas.1704339114"),
    ("12", "Auffhammer M., Baylis P., Hausman C.H. (2017). Climate change is projected to have severe impacts on the frequency "
           "and intensity of peak electricity demand across the United States. <i>PNAS</i> 114(8):1886–1891. "
           "doi:10.1073/pnas.1613193114. (Abstract read.)", "https://doi.org/10.1073/pnas.1613193114"),
    ("13", "Miżien. Data and calculations: data/cc-135/; tools/cc-135-report/calc.py (checks.csv).", ""),
])
S.append(PageBreak())
S += appendix_a("A experiment · B observational study with a control or gradient · C review, guidance or official "
                "statistics · D assertion or anecdote. ◆ marks a source known only second-hand.")
S += [Spacer(1, 5 * mm)]
S += revision_log([("1.0", "26 Oct 2026", "First issue. Verdict Largely supported (high confidence); no right of reply needed.")])

build_report(Report(
    number="135", out=str(FIG / "report.pdf"), kicker="Electricity and population",
    title_lines=["Peak electricity", "demand: up 43%", "in five years?"],
    subtitle_lines=["Testing an IMF staff paper against NSO,", "Eurostat and weather-station data"],
    quote_lines=["“Peak electricity demand has increased rapidly", "in recent years, rising from 465 MW in 2018 to",
                 "663 MW in 2023 (an increase of 43 percent).”"],
    quote_size=14.5,
    attribution="IMF staff (A. Pitt), Taking Stock of Infrastructure in Malta, SIP/2025/007, February 2025.",
    context="Para. 5: ‘significantly outpaced the growth in population and tourists’ (13 percent).",
    verdict="Largely supported", verdict_note="Figures exact; end years flatter the trend",
    footer_lines=["Version 1.0  ·  26 October 2026", "Status:",
                  "Prepared from public sources and official data.", "Repository: github.com/leandergrech/Mizien"],
    running_head="Peak electricity demand – IMF staff", version="1.0", date="26 October 2026",
    pdf_title="Peak electricity demand up 43% in five years? Claim Check 135",
    pdf_subject="Tests the IMF staff paper's figures on Malta's peak electricity demand, population and tourists",
    story=S))
