"""Claim Check 035 report. Run fetch.py, calc.py and figures.py first. Output: out/report.pdf"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import *  # noqa: E402,F401

FIG = HERE / "out"
S = []
LG = colors.HexColor("#8DB36B")
QUOTE = ("“is estimated to have been reduced by 67.7% between 2005 and 2023 (from 143.5 to 46.3, respectively), "
         "resulting in 172 (95% CI: 131-192) attributable deaths in 2023.”")

# ================================================================== TL;DR
S += [SectionHeading(None, "TL;DR"), Spacer(1, 1 * mm),
      P("The European Environment Agency’s <i>Air pollution quick country facts</i> (page modified 1 December 2025) "
        "say that in Malta the rate of natural deaths attributable to long-term exposure to PM2.5 above 5 µg/m³, per "
        "100 000 people aged 30 or over, <b>" + QUOTE + "</b>", lead)]
S.append(key_points([
    ("The figures are the EEA’s own, reported exactly.",
     "The EEA’s table gives 143.5 (2005) and 46.3 (2023), a fall of 67.74%, and 172 deaths (95% CI 131–192) in "
     "2023; Eurostat republishes the same. The technical report gives 173 (132–193): one death."),
    ("The method is the documented one, and it reproduces.",
     "8% more deaths per 10 µg/m³ (WHO), counted above 5 µg/m³, applied to natural deaths of people aged 30+. From "
     "Eurostat’s own death counts we get 346 and 170 deaths for 2005 and 2023, within 1.2% of the EEA’s 348 and 172."),
    ("Measured PM2.5 fell; 2005 is a map value.",
     "At Msida PM2.5 fell 39% from 2007 to 2023, and at three long-running stations 25% from 2010: direct evidence of a "
     "fall. The EEA’s map is built on these stations, so they anchor it rather than check it. No Maltese PM2.5 was "
     "reported to the EEA for 2005; that year’s 21.0 µg/m³ comes from an older map method and model."),
    ("It is a rate, and the start and threshold matter.",
     "The number of deaths fell by half (348 to 172) because the over-30 population grew 54%. Counting all "
     "concentrations, or starting in 2007, the fall is about 55–57%."),
    ("Verdict: largely supported (high confidence).",
     "The statement accurately reports the EEA’s estimate and says it is an estimate. The caveat: the exact 67.7% "
     "rests on a 2005 map value, and the 95% CI covers only the risk function."),
]))
S += [Spacer(1, 4 * mm), VerdictMeter(1), Spacer(1, 3 * mm),
      tiles([("67.7%", GREEN, "fall in the modelled rate, 2005–2023: reproduced from the EEA’s table"),
             ("172", GREEN, "attributable deaths in 2023 (95% CI 131–192); the technical report says 173"),
             ("−51%", ORANGE, "fall in the number of deaths (348 → 172); the over-30 population grew 54%"),
             ("0", ORANGE, "Malta stations reporting PM2.5 to the EEA for 2005: that year’s value comes from a map")]),
      Spacer(1, 4 * mm),
      up_down("The EEA’s confirmation of which 2005 map it used, with an uncertainty range for Malta’s 2005 exposure "
              "that keeps the fall near two-thirds.",
              "An EEA revision of the series, or evidence that the 2005 map was off by much more than its typical error "
              "(about 3 µg/m³), so that the 2005–2023 fall changes materially."),
      Spacer(1, 5 * mm)]
S += toc([("1", "The claim and what we could verify"), ("2", "Method"), ("3", "How the estimate is made"),
          ("4", "What the measurements show"), ("5", "Where the evidence points different ways"),
          ("6", "Testing the claim"), ("7", "Verdict and requests for evidence"), ("8", "Limitations")])
S.append(PageBreak())

# ================================================================== 1
S.append(SectionHeading(1, "The claim and what we could verify"))
S.append(P("The statement is the EEA’s own text on its <i>Air pollution quick country facts</i> page, part of the 2025 "
           "air pollution country fact sheets, read in the page HTML on 6 October 2026 [1]. The page gives a sentence of "
           "the same form for each country it covers. The EEA is the EU’s environment agency; we assess the wording of "
           "its statement, not the agency. Because it is the EEA’s own statistic, the questions are whether the sentence "
           "reports the EEA’s estimate accurately, and what that estimate does and does not mean."))
S.append(std_table([
    [C("What", cellh), C("Where", cellh), C("Access", cellh)],
    [C("The Malta sentence (quoted on the cover and in the TL;DR)"), C("Air pollution quick country facts [1]"),
     C("Read in full, 6 Oct 2026")],
    [C("The estimates by year and scenario, with population and concentration"), C("EEA burden-of-disease table [2]; "
     "Eurostat sdg_11_52 [3]"), C("Downloaded, 6 Oct 2026")],
    [C("The method and its history"), C("EEA briefing [4] and indicator [5]; ETC HE technical report [6]; map "
     "reports for 2005 [7] and 2023 [8]"), C("[4, 5] read in full; [6–8] pages read")],
    [C("Measured PM2.5 and PM10 in Malta, 2004–2025, and station types"), C("EEA station files [10] and metadata "
     "[17]; PQ 29696 table via CC-007 [15]"), C("Downloaded; reused")],
], [70 * mm, 64 * mm, 36 * mm]))
S.append(P("Our intake record first paraphrased the statement as “PM2.5 deaths down two-thirds”. The EEA speaks of the "
           "<i>rate</i>, and the number of deaths fell by about half (section 6), so the record title is now “PM2.5 "
           "death rate down two-thirds”. The EEA’s <i>Europe’s environment 2025</i> page for Malta draws the same series "
           "as a chart, with data to 2022 [14]; it is context, not the statement checked."))
S += [Spacer(1, 2 * mm),
      callout([P("SCOPE NOTE", tag),
               P("This check tests the EEA’s statement about its own estimate. It does not assess Malta’s air-quality "
                 "policy or any authority, and it does not count deaths: attributable deaths are a statistical estimate "
                 "for a population, not deaths certified as caused by air pollution (the EEA explains the difference "
                 "in material linked from its briefing [4]).", small)],
              bg=AMBER_PALE, bar=AMBER), Spacer(1, 4 * mm)]

# ================================================================== 2
S.append(SectionHeading(2, "Method"))
S.append(P("<b>Question.</b> Do 143.5, 46.3, 67.7% and 172 (131–192) match the EEA’s own estimates; is the method as "
           "described; is the 2005 starting point comparable with 2023; and did Malta’s measured PM2.5 fall?"))
S.append(P("<b>Evidence.</b> We downloaded the EEA’s <i>Burden of disease of air pollution (Countries &amp; NUTS)</i> "
           "table through its Table publisher [2]: Malta for every scenario, all countries, and the EU-27. We downloaded "
           "Eurostat sdg_11_52 (the same estimates, republished [3]), Eurostat population, deaths and causes of death "
           "[11] and emissions [12], every Malta PM2.5 and PM10 file in the EEA’s station archive [10] and the EEA’s "
           "station metadata [17], all on 6 October 2026 with Eurostat’s flags (none on the Malta values used). "
           "<i>tools/cc-035-report/calc.py</i> recomputes every figure from <i>data/cc-035/</i>. We read the EEA’s "
           "briefing and indicator [4, 5], the relevant parts of the technical report behind the estimates [6] and of "
           "the two map reports [7, 8], and searched Crossref and Europe PMC for peer-reviewed work on the risk "
           "function and on Malta’s PM2.5 [9, 13]."))
S.append(P("<b>Grades.</b> Official estimates and statistics are grade C, as is the meta-analysis behind the risk "
           "function (a review); Malta’s source-apportionment study is grade B. <b>Verdicts</b> follow the five-point "
           "scale in Appendix A."))

# ================================================================== 3
S.append(CondPageBreak(60 * mm))
S.append(SectionHeading(3, "How the estimate is made"))
S.append(P("The EEA’s estimate combines four things, cell by cell on a 1 km grid, and adds up the cells [6, Annex 1]:"))
for b in ["<b>Concentration.</b> An annual PM2.5 map that interpolates between monitoring stations, with “pseudo” "
          "PM2.5 values estimated from PM10 stations, a chemical transport model and other data (altitude, "
          "meteorology, population) [6, 8]. For Malta in 2023 its population-weighted mean is 10.9 µg/m³ [6].",
          "<b>Population.</b> Gridded population scaled to Eurostat totals; for all-cause deaths, people aged 30 or "
          "over (373,208 in Malta in 2023; Eurostat 373,224 [2, 11]).",
          "<b>Baseline deaths.</b> Deaths from natural causes (all causes except injuries and other external causes) "
          "by age and sex, from Eurostat. Cause-of-death data begin in 2011, so 2011 stands in for 2005–2010 [6].",
          "<b>Risk.</b> 8% more natural deaths per 10 µg/m³ (95% CI 6–9%), the WHO 2021 recommendation from Chen and "
          "Hoek’s meta-analysis of 107 studies [6, 9], counted only above 5 µg/m³, the WHO 2021 guideline level [4]."]:
    S.append(P("• " + b, bul))
S.append(P("The attributable fraction in a cell is 1 − exp(−β × (C − 5)), with β = ln(1.08)/10, and the deaths are that "
           "fraction of the cell’s baseline deaths [6, Annex 1]. Using Malta’s national mean concentration and "
           "Eurostat’s natural deaths aged 30+ [11], we get 346 deaths for 2005 and 170 for 2023, against the EEA’s 348 "
           "and 172 (−0.6% and −1.2%). The small gap is expected, since the EEA works cell by cell [6, pp. 45–46]."))
S.append(P("<b>What changed in the method.</b> The health calculation is now the same for every year. Until 2021 the "
           "EEA used a risk of 6.2% per 10 µg/m³ counted from 0 µg/m³; from 2022 it uses 8% counted above 5 µg/m³, and "
           "since 2024 it gives rates per person aged 30 or over; it recalculated every year back to 2005 this way [5]. "
           "The concentration maps are not one method: PM2.5 maps use an updated mapping method only from 2017, 2005 "
           "and 2009 exist in old and updated versions, the ETC’s own trend uses old-method maps for 2005–2014 "
           "[8, pp. 74–77], and the chemical transport model changed from EMEP to CAMS from 2020 [8, p. 108]. Which 2005 "
           "version the EEA’s table uses is not stated. No 2006 map was prepared, hence no 2006 value [8, p. 76]. The "
           "95% CI reflects the uncertainty in the risk only; “other possible uncertainties (for instance, the one "
           "related to exposure assessments) are not quantified” [4]."))
S.append(KeepTogether([fig(FIG / "fig1_rate.png"), P(
    "Figure 1. The EEA’s estimate for Malta, with its 95% CI (an error bar for 2005, which stands alone). Left: the rate "
    "the statement gives. Right: the number of attributable deaths. The rate fell 67.7%; the number fell 50.6% because "
    "more people were aged 30 or over. 2005 is drawn hollow: it is a map value, with no Maltese PM2.5 reported to the "
    "EEA for that year [2, 8, 10].", cap)]))

# ================================================================== 4
S.append(CondPageBreak(110 * mm))
S.append(SectionHeading(4, "What the measurements show"))
S.append(KeepTogether([fig(FIG / "fig2_measured.png"), P(
    "Figure 2. The EEA’s modelled population-weighted PM2.5 for Malta (thick line) and the annual means at Malta’s "
    "stations (thin lines; hollow markers where fewer than 75% of days have valid data), with station types from the "
    "EEA’s metadata [2, 10, 17]. The map is built on these stations, so it follows them by construction.", cap)]))
S.append(P("<b>Measured PM2.5 fell.</b> At Msida (a traffic station) PM2.5 went from 22.7 µg/m³ in 2007 to 13.9 in "
           "2023 (−39%); the mean of Msida, Żejtun and Għarb, the three stations with at least 75% of days in every "
           "year from 2010 (except 2012), fell from 15.1 to 11.2 (−25%) [10]. This is direct evidence that PM2.5 fell. "
           "It is not an independent check of the map: the map interpolates between these same stations [6, 8], so "
           "it is anchored to them. In 2023 the five stations in the parliamentary table used in CC-007 average 10.9 "
           "µg/m³, the map’s value, but that is an unweighted mean of two traffic, two urban background and one rural "
           "station [10, 15, 17]."))
S.append(P("<b>Two cautions.</b> PM10 at the same stations did not fall (Msida 42.5 µg/m³ in 2009 and 43.7 in 2023; "
           "Żejtun 29.3 in 2007 and 28.7 in 2023) while their PM2.5 fell by about 40% [10]. And the PM2.5 instruments "
           "changed: beta-attenuation monitors from 2006, gravimetric reference samplers from 2014, an optical (GRIMM) "
           "monitor at Msida from 24 September 2021, and a TEOM-FDMS at Għarb [17]; where two sampling points report "
           "the same day, our means average them. We have not untangled these effects."))
S.append(P("<b>2005.</b> The EEA’s station archive has no Maltese PM2.5 before 29 August 2006 (Żejtun) [10]. For 2005 "
           "Malta reported PM10 at two stations: Kordin, which the EEA’s metadata classes as industrial, and MT00002, "
           "whose type is not in the current metadata [10, 17]. The ETC maps use background and traffic stations only "
           "[7, Table A.1], so Kordin probably did not feed the 2005 map, and the 2005 value may rest on no Maltese "
           "measurement at all. Our identification of the 2005 map is ETC/ATNI Report 2020/1 (updated method), which "
           "gives Malta 21.2 µg/m³ [7]; the EEA’s table has 21.0 [2], a gap we cannot explain. That map’s typical "
           "cross-validation error was 2.9 µg/m³ in urban background areas [7]. As a rough test, the 2007 PM2.5/PM10 "
           "ratios at Msida (0.54) and Żejtun (0.62) applied to the 2005 PM10 means (49.0 at MT00002, 42.4 at Kordin) "
           "give 23–30 µg/m³ at those two sites, not below the map’s 21.0. This is indicative only: one site is "
           "industrial, the other’s type is unknown, and the ratios come from other sites and another year."))
S.append(P("<b>Context.</b> Malta’s reported primary PM2.5 emissions fell from 750 to 310 tonnes between 2005 and 2023, "
           "with public electricity and heat production down from 420 to 3 tonnes [12]. Emissions are not the whole "
           "story: at Msida in 2016, Saharan dust and sea salt made up about a third of PM2.5 [13], and the method "
           "treats all PM2.5 mass alike [6, Annex 1]."))
S.append(KeepTogether([
    std_table([
        [C("Indicator", cellh), C("Malta", cellh), C("Comparison", cellh), C("Source", cellh), C("Grade", cellh)],
        [C("Rate per 100 000 aged 30+, 2005 → 2023"), C("<b>143.5 → 46.3</b>"), C("EU-27 153.0 → 59.7"), C("[2]"),
         grade_tag("C")],
        [C("Fall in the rate, 2005–2023"), C("<b>67.7%</b>"), C("EU-27 61.0%; Malta 14th of 27"), C("calculated"),
         grade_tag("C")],
        [C("Attributable deaths, 2005 → 2023"), C("348 → 172"), C("EU-27 423,593 → 182,399"), C("[2, 3]"),
         grade_tag("C")],
        [C("Modelled population-weighted PM2.5 (µg/m³)"), C("21.0 → 10.9"), C("EU-27 19.4 → 10.2"), C("[2]"),
         grade_tag("C")],
        [C("Measured PM2.5 at Msida, 2007 → 2023 (µg/m³)"), C("22.7 → 13.9"), C("three stations, 2010 → 2023: "
           "15.1 → 11.2"), C("[10]"), grade_tag("C")],
        [C("Natural deaths aged 30+, baseline rate per 100 000"), C("1,238 → 1,038"), C("implied by the EEA figures; "
           "Eurostat 1,231 → 1,026"), C("calculated [11]"), grade_tag("C")],
    ], [62 * mm, 26 * mm, 42 * mm, 24 * mm, 16 * mm]),
    P("All values in <i>data/cc-035/checks.csv</i>, <i>station_vs_model.csv</i> and <i>eu27_rate_change.csv</i>.", cap)]))

# ================================================================== 5
S.append(CondPageBreak(120 * mm))
S.append(SectionHeading(5, "Where the evidence points different ways"))
S.append(contested(
    "Q1  Is the 2005 starting point comparable with 2023?", "SAME HEALTH METHOD; MAPS DIFFER; 2005 A MAP VALUE", LG,
    "The health calculation is the same for every year: the EEA recalculated 2005–2023 with the current risk "
    "function, threshold and age group [5, 6]. Our approximation, using the EEA’s concentrations and Eurostat’s death "
    "counts, matches both ends within 1.2%. Measured PM2.5 at Malta’s stations fell from 2007 (section 4).",
    "The maps are not one method: PM2.5 maps use the updated method only from 2017, 2005 exists in old and updated "
    "versions, and the model changed from EMEP to CAMS from 2020 [8, pp. 74–77, 108]; which 2005 version the table "
    "uses is not stated. No Maltese PM2.5 was reported to the EEA for 2005 [10], and both the 2005 and 2023 maps use "
    "PM10-based pseudo stations [7; 8, pp. 108, 118]. Shifting Malta’s 2005 value by the map’s typical error (2.9 µg/m³) "
    "gives a fall of 61% to 72% (indicative). The 95% CI leaves exposure error out [4].",
    "<b>For this claim:</b> the health side is consistent; the exposure side is not one method, and the 2005 value is "
    "a map value. The fall is less certain than its one decimal place suggests. That PM2.5 fell is borne out by "
    "measurements from 2007."))
S.append(contested(
    "Q2  Does a 67.7% fall in the rate mean two-thirds fewer deaths?", "ACCURATE AS WORDED", GREEN,
    "The EEA says “rate”, names the threshold (above 5 µg/m³) and the age group, and says “is estimated”. A rate per "
    "person at risk is how the EEA compares countries [4]. Eurostat’s rate per inhabitant of all ages fell 64% [3].",
    "The number of deaths fell 50.6% (348 to 172), because the over-30 population grew 54% [2]. Part of the rate’s fall "
    "is a 16% lower baseline death rate among people over 30, not cleaner air (section 6). Counting all concentrations "
    "the fall is 54.7% [2]. And 5 µg/m³ is not a no-effect level: studies at low concentrations find similar or "
    "higher risks [9], and the EEA notes no evidence of a threshold [4].",
    "<b>For this claim:</b> the sentence answers one well-defined question correctly. It does not say that two-thirds "
    "fewer people died from PM2.5, and readers should not take it that way."))

# ================================================================== 6
S.append(CondPageBreak(85 * mm))
S.append(SectionHeading(6, "Testing the claim"))
verd = lambda t, c: chip(t, c, w=28 * mm)
S.append(std_table([
    [C("Sub-claim", cellh), C("What the evidence shows", cellh), C("Rating", cellh)],
    [C("<b>A.</b> The rate was 143.5 per 100 000 aged 30+ in 2005"),
     C("EEA table: 143.5 (348 deaths, 242,534 people aged 30+) [2]; Eurostat: 348 deaths [3]."),
     verd("ACCURATE", GREENC)],
    [C("<b>B.</b> It was 46.3 in 2023"),
     C("EEA table and technical report: 46.3 (35.2–51.7) [2, 6]."), verd("ACCURATE", GREENC)],
    [C("<b>C.</b> “reduced by 67.7% between 2005 and 2023”"),
     C("(143.5 − 46.3) / 143.5 = 67.74%. The 2005 value is a map value, from maps of another method and model, with "
       "no Maltese PM2.5 reported to the EEA [8, 10]; from 2007 the fall is 56.6%; the 95% CI covers the risk only [4]."),
     verd("LARGELY ACCURATE", LG)],
    [C("<b>D.</b> “172 (95% CI: 131-192) attributable deaths in 2023”"),
     C("EEA table and Eurostat: 172 (131–192) [2, 3]. Technical report: 173 (132–193) [6]. The rate implies 172.8 "
       "deaths, but rounding does not explain the lower bound (35.2 → 131.4): a one-death difference, unexplained."),
     verd("ACCURATE", GREENC)],
    [C("<b>E.</b> Natural deaths, long-term exposure above 5 µg/m³, people aged 30+"),
     C("Matches the documented method [4–6]; recomputed from Eurostat deaths within 1.2% (section 3)."),
     verd("ACCURATE", GREENC)],
], [52 * mm, 80 * mm, 38 * mm], valign="MIDDLE"))
S.append(Spacer(1, 3 * mm))
S.append(P("<b>Why the rate fell.</b> Splitting the change: the attributable fraction fell from 11.6% to 4.4% of "
           "natural deaths (×0.383), as the modelled excess above 5 µg/m³ fell from 16.0 to 5.9 µg/m³; and the "
           "baseline natural death rate among people aged 30+ fell 16% (×0.838) [2, 11]. Together: ×0.321, a fall of "
           "68%. On the attributable fraction alone the fall would be 61.7%."))
S.append(KeepTogether([fig(FIG / "fig3_choices.png"), P(
    "Figure 3. The same EEA estimates measured different ways; every bar is the EEA’s modelled estimate. Only the top "
    "bar is the statement; the others show how the size of the fall depends on the threshold (10 µg/m³ is the 2030 EU "
    "limit value [8, p. 76]), the method, the start year and whether rates or numbers are compared [2].", cap)]))

# ================================================================== 7
S += [CondPageBreak(90 * mm), Spacer(1, 4 * mm), SectionHeading(7, "Verdict and requests for evidence"),
      verdict_box("Largely supported", "The statement reports the EEA’s own estimate exactly and calls it an estimate; "
                  "its 2005 starting value is a map value, with no Maltese PM2.5 reported to the EEA for that year. "
                  "Confidence: high."), Spacer(1, 4 * mm)]
S.append(P("<b>Why.</b> (1) Every figure in the sentence reproduces exactly from the EEA’s own table (Eurostat "
           "republishes the same estimates, so it is not a separate source). (2) Recomputed from Eurostat’s own death "
           "counts and the EEA’s concentrations, the deaths come within 1.2% of the EEA’s, so the method is as described. (3) The sentence is "
           "carefully worded: a rate, above 5 µg/m³, people aged 30+, “is estimated”. (4) Measured PM2.5 fell at "
           "Malta’s stations from 2007, direct evidence that the exposure behind the estimate fell; the map is built on "
           "these stations, so their agreement with it is not a separate check. (5) The caveat is the start: the 2005 "
           "value is a map value, from an older map method and model, with no Maltese PM2.5 reported to the EEA, and "
           "the 95% CI leaves exposure error out, so the exact 67.7% is less certain than it looks. That is a minor "
           "caveat; it does not change the substance, a large fall. Confidence is high because three separate lines "
           "agree: the figures reproduce exactly, the deaths reproduce from Eurostat’s death counts, and measured "
           "PM2.5 has declined since 2007. We do not count Eurostat’s sdg_11_52 (the EEA’s estimate republished) or "
           "the station–map match (the map is anchored to the stations)."))
S.append(P("<b>What this verdict does not say.</b> It does not say that two-thirds fewer people died because of PM2.5 "
           "(the number fell by about half), that Malta’s air meets the WHO guideline (10.9 µg/m³ against 5 in 2023), or "
           "anything about the causes of the fall or any authority’s policy."))
S.append(P("Evidence we are asking for", h2))
S.append(requests_list([
    "From the EEA: which 2005 PM2.5 map (old or updated method) the burden-of-disease table uses, and an uncertainty "
    "range for Malta’s modelled exposure in 2005, which the 95% CI does not include.",
    "From the EEA: why the quick-facts page gives 172 (131–192) and the technical report 173 (132–193).",
    "From the Environment and Resources Authority, which runs Malta’s stations: any 2005 PM2.5 measurements not "
    "reported to the EEA, and the type of station MT00002.",
]))

# ================================================================== 8
S += [Spacer(1, 6 * mm), SectionHeading(8, "Limitations")]
for l in ["The statement is a modelled estimate; we tested it against the EEA’s own data, its documented method and "
          "measured concentrations, not against an independent mortality study for Malta (we found none).",
          "Our recomputation uses Malta’s national mean concentration, not the EEA’s 1 km grid, so it is a check on "
          "the order of the result, not a replication.",
          "The stations anchor the map, so they show that PM2.5 fell but cannot test the map’s values; the 2023 match "
          "(10.9) is largely by construction.",
          "PM10 at Msida and Żejtun did not fall while PM2.5 did, and the PM2.5 instruments changed over the period "
          "(section 4); we have not untangled the two.",
          "The map errors we quote are Europe-wide cross-validation statistics, not Malta-specific; the 61–72% range "
          "and the 2005 PM10-ratio test are indicative.",
          "The 2005 map is our identification (ETC/ATNI 2020/1); the EEA does not say which version it used.",
          "Station annual means are averages of valid days from the EEA’s files, not the authority’s official annual "
          "statistics; for 2023 they match the PQ 29696 table to 0.1 µg/m³.",
          "Chen and Hoek [9] and Scerri et al. [13] were read as abstracts; a corrigendum to Scerri et al. "
          "(<i>Chemosphere</i> 219:1061–1062, 2019) was not read (Europe PMC lists no abstract and no open-access text).",
          "The quick-facts and Malta pages were not archived (the Wayback Machine refused requests on 6 October 2026)."]:
    S.append(P("• " + l, bul))

S += [Spacer(1, 6 * mm), SectionHeading(None, "References")]
S += references([
    ("1", "European Environment Agency. Air pollution quick country facts (Air pollution country fact sheets 2025). "
          "Modified 1 Dec 2025. Read 6 Oct 2026.",
     "https://www.eea.europa.eu/en/topics/in-depth/air-pollution/air-pollution-country-fact-sheets-2025/quick-country-facts"),
    ("2", "European Environment Agency. Burden of disease of air pollution (Countries &amp; NUTS), Table publisher. "
          "Retrieved 6 Oct 2026.",
     "https://discomap.eea.europa.eu/App/AQViewer/index.html?fqn=Airquality_Dissem.ebd.countries_and_nuts"),
    ("3", "Eurostat. sdg_11_52 Premature deaths due to exposure to fine particulate matter (PM2.5); updated 9 Dec "
          "2025, retrieved 6 Oct 2026. doi:10.2908/SDG_11_52. (Republishes the EEA’s estimates.)",
     "https://ec.europa.eu/eurostat/databrowser/view/sdg_11_52/default/table"),
    ("4", "European Environment Agency (2025). Harm to human health from air pollution in Europe: burden of disease "
          "status, 2025. EEA Briefing 16/2025. doi:10.2800/8961999. Read 6 Oct 2026.",
     "https://www.eea.europa.eu/en/analysis/publications/harm-to-human-health-from-air-pollution-burden-of-disease-status-2025"),
    ("5", "European Environment Agency. Premature deaths due to exposure to fine particulate matter in Europe "
          "(indicator). Published 30 Nov 2025. Read 6 Oct 2026.",
     "https://www.eea.europa.eu/en/analysis/indicators/health-impacts-of-exposure-to"),
    ("6", "Soares J., Plass D., Kienzler S., González Ortiz A., Gsella A., Horálek J. (2025). Assessing the "
          "environmental burden of disease related to air pollution in Europe in 2023. ETC HE Report 2025/8. "
          "doi:10.5281/zenodo.17658760. Table 1.1, section 2.1, Annexes 1–4.", "https://doi.org/10.5281/zenodo.17658760"),
    ("7", "Horálek J., Schreiberová M., Marková J. (2020). Reference air quality maps 2005 and 2009. ETC/ATNI Report "
          "2020/1. doi:10.5281/zenodo.4293744. Table 2.3, Tables A.1 and A.4.", "https://doi.org/10.5281/zenodo.4293744"),
    ("8", "Horálek J. et al. (2025). Air quality maps of EEA member and cooperating countries for 2023. ETC HE Report "
          "2025/5. doi:10.5281/zenodo.17427294. Table 2.3, pp. 74–77, 108 and 118.",
     "https://doi.org/10.5281/zenodo.17427294"),
    ("9", "Chen J., Hoek G. (2020). Long-term exposure to PM and all-cause and cause-specific mortality: a systematic "
          "review and meta-analysis. <i>Environment International</i> 143:105974. doi:10.1016/j.envint.2020.105974. "
          "(Abstract read.)", "https://doi.org/10.1016/j.envint.2020.105974"),
    ("10", "European Environment Agency. Air Quality download service: AirBase and E1a station files for Malta, PM2.5 "
           "and PM10. Retrieved 6 Oct 2026; file list and SHA-256 in data/cc-035/eea_station_file_manifest.csv.",
     "https://eeadmz1-downloads-webapp.azurewebsites.net/"),
    ("11", "Eurostat. demo_pjan (population on 1 January by age), demo_magec (deaths by age), hlth_cd_aro (causes of "
           "death). Retrieved 6 Oct 2026.", "https://ec.europa.eu/eurostat/databrowser/view/demo_pjan/default/table"),
    ("12", "Eurostat. env_air_emis Air pollutants by source sector; updated 7 Sep 2026, retrieved 6 Oct 2026.",
     "https://ec.europa.eu/eurostat/databrowser/view/env_air_emis/default/table"),
    ("13", "Scerri M.M., Kandler K., Weinbruch S., Yubero E., Galindo N., Prati P., Caponi L., Massabò D. (2018). "
           "Estimation of the contributions of the sources driving PM2.5 levels in a Central Mediterranean coastal "
           "town. <i>Chemosphere</i> 211:465–481. doi:10.1016/j.chemosphere.2018.07.104. (Abstract read; corrigendum "
           "doi:10.1016/j.chemosphere.2018.12.121, Crossref-verified, not read.)", "https://doi.org/10.1016/j.chemosphere.2018.07.104"),
    ("14", "European Environment Agency. Health impacts of air pollution: Malta (Europe’s environment 2025). "
           "Published 29 Sep 2025. Read 6 Oct 2026.",
     "https://www.eea.europa.eu/en/europe-environment-2025/countries/malta/health-impacts-of-air-pollution"),
    ("15", "Miżien. Claim Check 007: Within EU limits vs WHO guideline (PQ 29696 station table). data/cc-007/.", ""),
    ("16", "Miżien. Data and calculations: data/cc-035/; tools/cc-035-report/calc.py.", ""),
    ("17", "European Environment Agency. Air quality station metadata (PanEuropean_metadata.csv): Malta’s PM10 and "
           "PM2.5 sampling points, station types and sampling processes. Retrieved 6 Oct 2026 "
           "(data/cc-035/eea_station_metadata_mt.csv).",
     "https://discomap.eea.europa.eu/map/fme/metadata/PanEuropean_metadata.csv"),
])

S.append(PageBreak())
S += appendix_a("A experiment · B observational study with a control or gradient · C review, guidance or "
                "official statistics · D assertion or anecdote. ◆ marks a source known only second-hand (none in this "
                "report).")
S += [Spacer(1, 5 * mm)]
S += revision_log([("1.0", "6 Oct 2026", "First issue. Verdict Largely supported (high confidence); no right of reply "
                                         "needed.")])

build_report(Report(
    number="035", out=str(FIG / "report.pdf"), kicker="Air quality and health statistics",
    title_lines=["Did Malta’s PM2.5", "death rate fall", "by two-thirds?"],
    subtitle_lines=["Testing the EEA’s own estimate against its data,", "its method and Malta’s station measurements"],
    quote_lines=["“… is estimated to have been reduced by 67.7% between 2005",
                 "and 2023 (from 143.5 to 46.3, respectively), resulting in",
                 "172 (95% CI: 131-192) attributable deaths in 2023.”"],
    quote_size=12.5,
    attribution="European Environment Agency, Air pollution quick country facts (country fact sheets 2025), 1 Dec 2025.",
    context="The rate: deaths attributable to PM2.5 above 5 µg/m³ per 100 000 people aged 30+, Malta.",
    verdict="Largely supported", verdict_note="Accurate report of an estimate; 2005 is a map value",
    footer_lines=["Version 1.0  ·  6 October 2026", "Status:",
                  "Prepared from public sources and EEA and Eurostat data.", "Repository: github.com/leandergrech/Mizien"],
    running_head="Malta’s PM2.5 death rate, 2005–2023", version="1.0", date="6 October 2026",
    pdf_title="Did Malta's PM2.5 death rate fall by two-thirds? Claim Check 035",
    pdf_subject="Tests the European Environment Agency's statement that Malta's PM2.5-attributable death rate fell by "
                "67.7% between 2005 and 2023, with 172 attributable deaths in 2023",
    story=S))
