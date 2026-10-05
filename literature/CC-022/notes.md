# CC-022 notes

| Key | Source | Access | Finding used | Grade |
|---|---|---|---|---|
| gov_pr250746 | Ministry press release, 6 May 2025 | F | The claim and its figures. | (claim) |
| eurostat_nrg_pc_204 | Eurostat | data | 2024-S2, band DC (2,500-4,999 kWh): Malta 14.35 PPS/100 kWh, lowest of 27; EUR 0.1303/kWh, third lowest; CZ 41.00, CY 35.70, DE 35.23 PPS. Malta -0.2% 2020-S1 to 2025-S2; EU +35%. Other bands, 2024-S2 PPS: 16th (DA), 3rd (DB), 2nd (DD), 23rd of 27 (DE), 4th of 26 (all bands); 2025-S2: 9th, 2nd, 2nd, 24th, 3rd of 27. Malta band DC EUR 0.1689 (2013-S2) to 0.1248 (2014-S2), then 0.1248-0.1328 to 2025-S2 (2025-S2 provisional). | C |
| eurostat_ilc_mdes | Eurostat | data | 2025: unable to keep home warm 7.6% (EU 8.8%); arrears on utility bills 4.5% (EU 7.0%). | C |
| imf_cr2629 | IMF CR 26/29 (doi:10.5089/9798229038249.002) | F | Energy subsidies (electricity and fuel) 1.8% of GDP 2022, 1.4% 2023, 0.9% 2024, 0.8% 2025 (proj.); about EUR 1.0bn 2022-2025 with Eurostat GDP. IMF recommends cost-recovery tariffs with targeted support. | C |

| eurostat_burden (v1.2) | Eurostat nrg_pc_204, nrg_pc_204_v, ilc_di03, ilc_di01, nrg_d_hhq, lfst_hhnhtych, nasa_10_nf_tr, hbs_str_t211, ilc_mdes01/07, ilc_hcmp03 | data | Burden against income and use (data/cc-022/burden_measures.csv). Bill for 3,750 kWh at the 2024 band-DC price / median equivalised income (EU-SILC 2025 = 2024 income): Malta 2.19%, EU 4.74%, 2nd of 27 (LU 1.52% 1st); same with 2,500 or 5,000 kWh, EU-SILC 2024, or 2025 prices: still 2nd. Against the 20th-percentile income: 3.48% vs 7.28%, 2nd. Actual use: 4,617 kWh per household (21st of 27; EU 3,524), 19.5% for space cooling (EU 3.1%), 25.8% water heating (EU 11.4%); consumption-weighted price EUR 0.149/kWh (3rd); average bill EUR 689 (12th; EU 1,041); 1.26% of gross disposable income per household (EU 1.91%), 5th of 26 (LU, NL, HU, RO lower; SK 1.263%); BG has no S14_S15 B6G. HBS 2020 electricity share 2.3% (flag e), joint 7th of 24 with BE (median 2.8%; reviewer said 8th: alphabetical tie-break). Arrears 4.5% (EU 7.0%) 9th; below 60% median 9.2% (EU 16.8%) 7th. Unable to keep warm 7.6% (EU 8.8%) 17th; below 60% 10.9% (EU 19.6%) 9th. Not comfortably cool in summer (2012 module, only year): 35.4% (EU 21.4%), 25th of 27. No 2023-module summer-cooling table exists in Eurostat's catalogue (only winter warmth, ilc_lvhe11-15). | C |

## Gaps

- The IMF figure covers electricity and fuel together; an electricity-only figure (Enemalta / budget lines) was not found.
- v1.1 gap closed in v1.2: burden is now measured against income and actual use (see the eurostat_burden row). The
  spending share (HBS) is from 2020 only, before the 2022 price shock.
- Income bases differ: EU-SILC income is per adult-equivalent; national-accounts B6G includes NPISH and imputed items.
- No peer-reviewed study of Malta's tariff freeze was found; the check is about statistics.
