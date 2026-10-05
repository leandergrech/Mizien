# Claim Check 005: “92% excellent” bathing water

**Status:** Draft for maintainer review
**Version:** 1.2, 5 October 2026 (upgrade; see the revision log below)
**Verdict:** Supported, high confidence (for the statistic quoted by the Commission: the 2023 result, repeated in 2024)
**Claim source:** European Commission, *Environmental Implementation Review 2025: Malta*
**Reference year:** 2023 (named in the Commission’s full report, SWD(2025) 318)

## TL;DR

The European Commission’s 2025 Malta review says **92% of Maltese bathing waters are excellent**. The EEA data confirm it: 80 of 87 sites in 2023, the season the Commission’s full report names, and 80 of 87 again in 2024, so the figure was accurate and current when published. The same data show a decade-long slide, from 86 of 87 sites (98.9%) in 2016–2018 to 77 (88.5%) in 2025, the lowest of the eleven seasons since 2015 and now level with the EU coastal average. Ten sites account for every rating below excellent; two at Balluta Bay have been rated only ‘sufficient’ for four seasons running.

1. **The 92% figure checks out.** The EEA rated 80 of 87 Maltese bathing sites excellent in 2023 (92.0%), the season the Commission’s staff working document gives, and again 80 of 87 in 2024.
2. **It is not the latest result.** In 2025, 77 of 87 sites (88.5%) were excellent; 8 were good and 2 sufficient. None was poor.
3. **The share has fallen over ten years.** 86 sites were excellent in each season 2016–2018; then 85, 84, 84, 82, 80, 80 and 77. Malta’s lead over the EU-27 coastal average shrank from 11 percentage points in 2016 to 0.2 in 2025 (Figure 1).
4. **The decline is concentrated in a few bays.** 77 sites were excellent in every season from 2015 to 2025. In 2025 St George’s Bay B03 (St Julian’s) and Xlendi D06 and D07 fell from excellent to good, while Birżebbuġa A11 and St Paul’s Bay C23 rose from sufficient to good (Figures 2 and 3).
5. **Balluta Bay is a persistent problem.** Its two sites were excellent in 2015–2018, good in 2019–2021 and only sufficient, the lowest passing class, in every season 2022–2025. The 2024 health warning fell within that run.
6. **Verdict: supported, with a date caveat.** Accurate for 2023 and 2024. Used today without its year, it overstates the current result by about three and a half percentage points.

## 1. Claim and sources

The Commission’s *Environmental Implementation Review 2025: Malta* summary states: “Malta also shows excellent records under the Bathing Water Directive: 92% of Maltese bathing waters are of excellent quality.” The sentence appears in the highlights and gives no reference year. The Commission’s full staff working document, SWD(2025) 318 of 7 July 2025, does: “in 2023, out of the 87 Maltese bathing waters, 80 (92%) were of excellent quality” [1, 2].

| Source | What it establishes | Use |
|---|---|---|
| European Commission, EIR 2025: Malta, and SWD(2025) 318 [1, 2] | Exact 92% sentence; the full report dates it to 2023; wastewater discussed separately. | Claim wording |
| EEA bathing-water data: DiscoMap 2025 service and WISE dataset [3, 4] | Class of each of Malta’s 87 sites in every season 2015–2025, with coordinates; EU-27 totals. | Primary statistical series |
| EEA, Malta bathing-water profiles, 2024 and 2025 [5, 6] | Season totals and sample counts. | Cross-check |
| Directive 2006/7/EC [7] | What is measured, and how a season’s class is assessed. | Method |
| Environmental Health Directorate, Balluta Bay report (2024) [8] | Temporary warning at sites B08/B09 and when it was lifted. | Local context |
| CJEU, Commission v Malta, C-304/23 (2024) [9] | Urban wastewater treatment obligations for named agglomerations. | Separate compliance issue |

**Method.** We downloaded the classification of every Maltese bathing water for each season from 2015 to 2025 from the EEA’s bathing-water map service, and checked each site and season from 2015 to 2024 against the EEA’s WISE dataset: all 870 match. EU-27 shares are counted from the same sources; the 2023 result, 88.9% of coastal bathing waters excellent, matches the EEA’s published figure. Data and scripts: `data/cc-005/`, `tools/cc-005-report/`.

## 2. What the indicator measures

Under the Bathing Water Directive, classification rests on two faecal-indicator bacteria, *Escherichia coli* and intestinal enterococci. A season’s class is assessed from the samples of that season and the three before it, so a change in class reflects four seasons of results, not one bad week [7]. “Sufficient” is the minimum the directive requires; “excellent” is the best of four classes.

“Excellent” is a meaningful result for those parameters, but it does not cover every pollutant or the ecological and chemical state of the sea, and it does not rule out short-lived contamination: a site can receive a temporary warning and keep its class. The year and the denominator should accompany the percentage when it is repeated.

## 3. What the season data show

The 92% is the 2023 result, repeated in 2024. Seen across eleven seasons, it is a point on a falling line. Malta rated 86 of its 87 sites excellent in each season from 2016 to 2018. Since then the count has fallen every few seasons, to 77 in 2025 (Figure 1). Over the same period the EU-27 coastal average edged up, from 87.8% in 2016 to 88.3% in 2025, so Malta’s lead over it has all but gone.

*Figure 1. Share of bathing waters rated excellent, Malta and the EU-27 coastal average, seasons 2015–2025.*

| Season | Excellent | Good | Sufficient | Poor | EU-27 coastal, excellent | Samples |
|---|---:|---:|---:|---:|---:|---:|
| 2022 | 82 (94.3%) | 2 | 3 | 0 | 89.0% | 2,006 |
| **2023** | **80 (92.0%)** | 3 | 4 | 0 | 88.9% | 2,021 |
| 2024 | **80 (92.0%)** | 3 | 4 | 0 | 89.0% | 2,107 |
| 2025 | **77 (88.5%)** | 8 | 2 | 0 | 88.3% | 2,100 |

**Which sites.** The decline is not spread along the coast. Of the 87 sites, 77 were excellent in every season from 2015 to 2025; ten account for every lower rating (Figure 3). Between 2024 and 2025 five sites changed class. Three fell from excellent to good: B03 on the left of St George’s Bay in St Julian’s, and D06 and D07 at Xlendi Bay in Gozo. Two rose from sufficient to good: A11 at St George’s Bay in Birżebbuġa and C23 in St Paul’s Bay (Figure 2). The net effect was three fewer excellent sites and two fewer sufficient ones.

*Figure 2. Malta’s 87 bathing waters coloured by their 2025 class, with the sites that changed class between 2024 and 2025 and those below excellent in both.*

*Figure 3. Class of the ten sites rated below excellent in at least one season, 2015–2025. Balluta Bay’s two sites have been only sufficient since 2022; St George’s Bay in St Julian’s now has both sites at good.*

## 4. Where the evidence points different ways

**Q1. Was “92% excellent” a fair description of Malta’s bathing water? Accurate, now dated.**

- *For the claim’s impression:* the figure is exact for 2023 and the Commission’s full report says so. The 2024 season gave the same 80 of 87, so the figure was also current when the review appeared in mid-2025. 92% was above the EU-27 coastal average (88.9% in 2023), and every Maltese site met at least the minimum standard.
- *Against:* the summary sentence omits the year, and “excellent records” describes a record that was getting worse: 98.9% in 2016–2018, 92.0% in 2023–2024, 88.5% in 2025, the lowest in the series. In 2025 Malta was level with the EU coastal average. Two Balluta Bay sites have been at the minimum standard for four seasons.
- *For this claim:* the number was right when it was published, so the verdict stays Supported. The fair reading adds two things the sentence does not say: the result belongs to 2023 and 2024, and the trend since 2018 is downward. Quoted today without its year, 92% overstates the current result.

## 5. Balluta Bay and wastewater

Balluta Bay’s two sites, B08 and B09, were excellent from 2015 to 2018, good from 2019 to 2021 and only sufficient in every season from 2022 to 2025 (Figure 3). Because each class draws on four seasons of samples, that is a persistent problem at these two sites, not a single bad summer [7]. Within that run, the Environmental Health Directorate issued a temporary warning at both sites in late May 2024, after microbial contamination and foul water from a storm-water tunnel; it was lifted on 12 August after three consecutive samples fell below the thresholds [8]. The 2023 national count already reflects Balluta’s sufficient rating: the two sites are among the seven not rated excellent that year.

In Case C-304/23, the Court of Justice found failures to comply with urban wastewater treatment obligations for named agglomerations [9]. That judgment is not a bathing-water classification, and it does not show that the EEA’s 2023 result was false. The Commission’s own review reports bathing-water quality and wastewater treatment under separate headings.

**Fairness note.** Warnings and wastewater failures matter for public health and for the sea, but they measure different things from the national classification. This check assesses the dated statistic and what the same data show since; it does not judge whether every beach is always clean or whether Malta’s marine environment is healthy overall.

## 6. Verdict and limits

**Supported (high confidence).** 80 of 87 sites (92.0%) in 2023 and again in 2024. Since then: 77 of 87 (88.5%) in 2025.

**Why.** The EEA’s data confirm 80 excellent sites out of 87 in 2023, the season the Commission’s full report names, which rounds to the 92% quoted; 2024 gave the same count, so the statement was current when published. Confidence is high because two EEA sources agree site by site. The caveat is the date: the share has fallen since 2018 and was 88.5% in 2025, so the year should be stated whenever 92% is used to describe Malta’s bathing water.

**Limits.** This verdict covers only the quoted statistic. The classification uses data reported by Malta; this check is not an independent sampling programme. It does not assess chemical pollutants, marine ecological status or health outcomes beyond the directive’s two microbiological indicators, and it does not explain why individual sites declined.

Right of reply has not been sought, as directed by the maintainer. The report remains a draft for maintainer review.

## References

1. European Commission, [Environmental Implementation Review 2025: Malta](https://op.europa.eu/webpub/env/eir-country-reports-summaries/en/malta.html) (country summary). Exact claim wording; separate wastewater discussion.
2. European Commission, [2025 Environmental Implementation Review Country Report – Malta, SWD(2025) 318 final](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:52025SC0318), 7 July 2025. Dates the 92% to the 2023 season.
3. EEA, bathing-water map service [BathingWater_Dyna_WM_2025, layer 3](https://water.discomap.eea.europa.eu/arcgis/rest/services/BathingWater/BathingWater_Dyna_WM_2025/MapServer/3) (class of each bathing water, seasons 2015–2025, with coordinates). Queried 5 October 2026; extract in `data/cc-005/mt_site_classes.csv`.
4. EEA, WISE Bathing Water Directive dataset, `[WISE_BWD].[latest].[assessment_BathingWaterStatus]` and `[timeseries_MonitoringResult]`, via [DiscoData SQL](https://discodata.eea.europa.eu/sql). Retrieved 5 October 2026; `data/cc-005/`.
5. EEA, [Bathing water quality in the season of 2024: Malta](https://environmentalhealth.gov.mt/wp-content/uploads/2025/07/Malta_bathing_water_2024.pdf) (country factsheet). 80/87 excellent; 2,107 samples.
6. EEA, [Bathing water quality in the season of 2025: Malta](https://www.eea.europa.eu/en/topics/in-depth/bathing-water/state-of-bathing-water/bathing-water-country-factsheets-2025/mt-bathing-water-country-factsheet-2025.pdf/@@download/file) (country factsheet). 77/87 excellent; 2,100 samples.
7. [Directive 2006/7/EC](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32006L0007) of the European Parliament and of the Council concerning the management of bathing water quality, Article 4 and Annex II.
8. Environmental Health Directorate, [Report on the temporary closure at B08 and B09 Balluta Bay](https://environmentalhealth.gov.mt/wp-content/uploads/2024/09/Report-for-Balluta-Bay-the-Bathing-Prohibition-Period-and-Short-Term-Pollution-Period.pdf) (2024).
9. Court of Justice of the European Union, [Commission v Malta, C-304/23, ECLI:EU:C:2024:906](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:62023CJ0304) (17 October 2024).

## Revision log

| Version | Date | Change |
|---|---|---|
| 1.0 | 2 Oct 2026 | First issue. Right of reply not sought, at the maintainer's direction. |
| 1.1 | 5 Oct 2026 | Corrections: (1) the report's "what would move the verdict" boxes were reversed; now "up": none (Supported is the top of the scale; naming the 2023 season would remove the date caveat), "down": a different 2023 count, a later intended season or an incompatible denominator. (2) Balluta Bay warning start: "31 May" → "late May 2024"; the bibliography gave 21 May and the primary report could not be re-opened. (3) 2023 sample count: "—" → 2,021 (EEA WISE dataset). (4) PDF page footer: "pending right of reply" → "right of reply not sought"; this file's closing line now says the same. Verdict and confidence unchanged. |
| 1.2 | 5 Oct 2026 | Upgrade: added the EEA classification of all 87 sites for every season 2015–2025 (map service, checked site by site against the WISE dataset) and the EU-27 coastal share; three figures (Malta against the EU coastal average, a map of the 2025 classes, and the ten sites ever below excellent). New findings stated: the 92% was also the 2024 result, so it was current when published; the share has fallen from 98.9% (2016–2018) to 88.5% (2025), the lowest since 2015 and level with the EU coastal average; the five sites that changed class in 2025 are named. Balluta Bay is now described as sufficient in every season 2022–2025, not as a single local episode. Added SWD(2025) 318, which dates the figure, and Directive 2006/7/EC. Verdict and confidence unchanged. |
