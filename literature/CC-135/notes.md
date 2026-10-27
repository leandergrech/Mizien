# CC-135 notes

- **Wording:** IMF SIP/2025/007, para. 5 (p. 4), read via WebFetch on 26 Oct 2026 (curl 403 that day; the intake read the
  PDF on 25 Oct 2026). Verbatim: "Peak electricity demand has increased rapidly in recent years, rising from 465 MW in 2018
  to 663 MW in 2023 (an increase of 43 percent). This increase has significantly outpaced the growth in population and
  tourists in the peak summer season (an increase of 13 percent over the same period). In part, this may be related to the
  rise in mean temperatures in the hottest month from 27.3 °C to 29.6 °C." Footnote 3: "Peak temperatures rose from 34 °C
  to almost 42 °C over the same period." Chart 'Population, Temperature, and Energy': notes "Mean temperature in hottest
  month." and "Number of tourists: nights spent in peak month divided by 31."; "Sources: Authorities' data, Eurostat, and
  IMF staff estimates." The paper does not name the series behind 465/663 MW, nor whether it is gross or net.
  Para. 2: population "around 563,000 at end-2023". Para. 8: the authorities project peak demand about 30% higher by 2040
  under a high-temperature, high-population scenario (not tested).
- **Peak demand (NSO):** NR 177/2022 (Electricity Supply: 2021) Table 7, monthly maxima 2017-2021, read via WebFetch of the
  PDF (2018 maximum = August, 465 MW). NR 184/2024 text: July 2023 663 MW, August 561 MW, annual average 446 MW (down 5.9%).
  NR 176/2023: 2022 July 581, August 575, average 473. NR 178/2025: 2024 July 593, September 592, average 478 (+1.8%,
  implying a revised 2023 average of about 470). NR 178/2026 (8 Oct 2026): 2025 July 637, August 585, average 492 (+2.9%).
  Definition: "the highest amount of electricity consumed at any one point in time across the entire network system".
  The 'annual average demand' is the mean of the 12 monthly maxima (checked on the 2021 table). Table 7 of the 2022-2025
  releases was not reachable (the other nso.gov.mt PDFs failed in WebFetch; curl gets 403).
- **Population and tourists:** Eurostat demo_gind (JAN, AVG) and tour_occ_nim (I551-I553, TOTAL), retrieved 26 Oct 2026.
  The IMF's 13% reproduces: 13.3% / 13.4% / 13.5% for 1 Jan same year / average / end-year. The peak tourist month is
  August in both years. NSO inbound-tourism releases (frontier survey; includes private accommodation) failed in
  WebFetch: not tested.
- **Controls:** Eurostat nrg_cb_e final consumption +13.4% 2018-2023; supply (GEP + IMP - EXP) +14.8%.
- **Temperature:** NOAA GHCN-Daily MT000016597 (Luqa) daily TAVG: hottest month 26.94 °C (July 2018) and 29.43 °C (July
  2023); highest TMAX 35.7 °C (2018) and 42.7 °C (2023). IMF: 27.3/29.6 and 34/almost 42; the IMF's source ("authorities'
  data") not seen. NASA POWER (MERRA-2 grid) gave lower, smoothed values and was not used; Open-Meteo returned 429.
- **Literature:** Wenz, Levermann & Auffhammer 2017 PNAS (10.1073/pnas.1704339114) and Auffhammer, Baylis & Hausman 2017
  PNAS (10.1073/pnas.1613193114): DOIs, titles and authors verified in Crossref on 26 Oct 2026; abstracts via OpenAlex.
  Abstract only; context, not findings on Malta. Menne et al. 2012 (GHCN-Daily) DOI verified in Crossref. No PDFs
  committed (PNAS user licence, not CC).
- **Search log (absence statements, 26 Oct 2026):** "the paper does not name the series": paragraph 5, its footnotes and
  the chart notes read via WebFetch; footnote 4 names Enemalta only for distribution investment and outages. Not searched:
  the Article IV staff report (Country Report 25/17). "We do not know whether 663 MW was revised": only the release texts
  of 2024 and 2025 were read, not their Table 7.
- **Gap:** hourly system load (Enemalta / REWS) to adjust the peak for temperature properly.
