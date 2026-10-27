# CC-131 notes

- **Wording:** Commission 2026 Country Report for Malta (SWD(2026) 218 final), Council register copy ST-10135-2026-ADD-1
  (126 pp., sha256 684d13b1..., identical to the copy archived on 5 Oct 2026 for CC-109 to CC-111), read 25-26 Oct 2026.
  The sentence is in **Annex 8** (industry decarbonisation, circularity and climate; 'Sustainable industry', 'Circular
  economy'), PDF p. 76 (printed p. 74), not Annex 10 as the intake record said. Verbatim: 'By contrast, the rate of
  recovery of construction and demolition waste is 100 (152), above the EU average of 89%.' Footnote 152:
  'Techno-economic and environmental assessment of CDW management, JRC, 2024, Link.' The link target (read from the PDF's
  link annotations with pypdf) is the JRC report on build-up.ec.europa.eu.
- **Unit:** the page image (rendered at 300 dpi) shows '100' with no percent sign. Table A8.1 (PDF p. 79) gives
  'Construction and demolition waste (CDW) recovery' for Malta as 100 (2018), - (2019), 100 (2020) and the EU as 88 (2018)
  and 89 (latest), also without a unit; its notes say 'Other indicators: Eurostat'. The JRC report's Table 10 is headed
  'Overall recovery rate for CDW across the EU Member States (in %)'. So the 100 is a percentage.
- **Source of the figures:** JRC 2024, Section 4.5 (p. 41): the recovery rate 'varies from 63% for Finland to 100% for Malta,
  Greece and the Netherlands, and equals on average 89% for the EU in 2020' (Table 10, from Eurostat env_wastrt). The
  Commission's 100 and 89 are the JRC's 2020 values.
- **Data:** Eurostat env_wastrt (W121 mineral waste from C&D, W126 soils; HAZ_NHAZ and NHAZ; all operations; 2010-2022;
  updated 23 Sep 2025) and env_wasgen (updated 14 Oct 2026), downloaded 26 Oct 2026 with tools/cc-131-report/fetch.py.
  Recovery rate = RCV_R_B / TRT for W121, non-hazardous; this reproduces 25 of 27 values in the JRC's 2020 column
  (differences: France 74 then, 81.7 now; EU-27 89 then, 90.9 now). The Eurostat indicator cei_wm040 (recovery rate of C&D
  waste) is no longer in the Eurostat catalogue (table of contents checked 26 Oct 2026) and the API answers 'not available
  for dissemination'; the DBnomics mirror shows its last update as 13 Jan 2023. Malta's 2022 treatment values carry flag 'e'.
- **Findings:** Malta 99.9996% (2020) and 99.9998% (2022): 100 when rounded. EU-27 87.9% (2018), 90.9% (2020), 91.4% (2022).
  Malta's 100% splits into recycling 41.8% and backfilling 58.2% in 2020 (EU 78.7% and 12.2%), and 67.3% and 32.7% in 2022
  (EU 80.3% and 11.1%). On recycling alone Malta ranked 21st of 27 (2020) and 18th of 26 (2022). In 2010 Malta reported
  84.1% of this waste as landfilled (recovery 15.9%); from 2012 landfill is under 0.3% and backfilling 65-81%.
- **The reclassification:** Commission factsheet (Deloitte, Sept 2015) pp. 4-5: until the 2012 reporting, waste deposited
  in spent quarries was reported as landfilled; in early 2015 MEPA told the NSO it should be classified as backfilling, and
  'a large amount previously reported as landfilling, now is reported as recovery and contributes to the fulfilment of the
  WFD targets'. The same factsheet (p. 3) calls backfilling 'the principal CDW management practice in Malta' and notes
  treated amounts above generated amounts (2012). Current Eurostat shows the change from the 2012 data year.
- **Law:** WFD Art. 11(2)(b) counts 'other material recovery, including backfilling operations' towards the 70% target;
  Decision 2011/753/EU Art. 4(3) requires backfilling to be reported separately; Directive 2018/851 Art. 3(17a) defines
  backfilling (waste must substitute non-waste materials and be limited to the amount strictly necessary) and Art. 11(6)
  asked the Commission to consider re-use and recycling targets for C&D waste by 31 Dec 2024. Whether such a proposal
  followed was not searched.
- **NSO 2024 (second-hand, ◆):** NR 023/2026 (17 Feb 2026), read through WebFetch only: in 2024 backfilling of mineral C&D
  waste 'surged by 58.0 per cent (381,727 tonnes)' and recycling 'declined by 13.6 per cent (197,255 tonnes)'; 2021-2022
  figures revised. Implied 2024 backfilling share of recycling + backfilling about 45% (calc.py G3; approximate). The NSO
  says inert mineral waste managed in quarries 'also includes clean geological material from excavation works'.
- **ERA (paraphrase, ◆):** The Shift (17 Jun 2026) reports ERA as saying Malta recycled more than half of locally generated
  C&D waste in recent years and surpassed the 70% recovery target. Not ERA's own words.
- **Search log (absence statements), 26 Oct 2026:** (1) No regulator or audit finding on whether Malta's quarry deposits meet
  the 2018 backfilling definition: WebSearch (two queries on Malta, quarries, backfilling, 'strictly necessary', Commission
  early warning/implementation report); era.org.mt pages 403 to curl (strategy page read via WebFetch: page text only, the
  strategy PDF not reached); Commission factsheet 2015 read. Not searched: the Commission's Article 11 implementation
  reports, parlament.mt, the 2021-2030 C&D Waste Strategy PDF. (2) cei_wm040's withdrawal: Eurostat catalogue (txt TOC)
  and API checked; the reason for withdrawal was not found (one WebSearch).
- **Literature:** Moschen-Schimek et al. 2023 (Waste Management 167; CC BY 4.0; abstract only): Eurostat recovery rates use
  treatment data for non-hazardous mineral C&D waste; non-unified data collection, waste coding and 'misinterpretations of the
  term backfilling' impede cross-country comparison. Villoria Sáez & Osmani 2019 (J. Cleaner Production 241; abstract only):
  assesses Eurostat C&D data reliability. Both DOIs verified in Crossref.
- **Not read:** the JRC's Box 1 was read only as cited in Section 4.3; Malta's national quality reports to Eurostat;
  the C&D Waste Strategy 2021-2030 PDF; the Waste Management Plan 2014-2020 (only as summarised by the factsheet).
- **Gap:** whether excavated rock reported in W121 would be reported as soils (W126, excluded from the indicator) elsewhere:
  Malta reports almost no W126 (44 t generated in 2018, 80 t in 2022), but the data do not show how excavation spoil is coded.
