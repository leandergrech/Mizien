# CC-079 notes (10 October 2026)

## Wording (what the speaker said, and where)

- **The claim (WasteServ, 26 Jun 2023).** ECOHIVE news, "Malta's Waste-to-Energy Project Procurement Reaches its
  Final Stage", fourth paragraph, read in full: "This plant will be treating around 192,000 tonnes of non-recyclable
  waste generated locally diverting it away from landfills and converting it into green energy. It is expected to
  meet around 4.5% of Malta's total energy needs." The page is WasteServ's own text (no quotation marks needed: it is
  the speaker's publication).
- **Earlier wording (WasteServ, 23 Oct 2020 and 2 Nov 2020).** "... this plant will convert wastes that cannot be
  recycled into precious resources adding an impressive 4.5% as green energy to Malta's total energy demand." The
  23 Oct release was reprinted the same day by The Malta Business Weekly.
- **Project page (WasteServ, undated, read 10 Oct 2026).** "... this facility will be treating 40% of non-recyclable
  waste generated in Malta diverting it away from landfill disposal"; "the plant will generate 126GWh annually to the
  grid"; "With a capacity of 192,000 tonnes annually, this EUR 185 million investment is expected to be commissioned in
  December 2026." The Maltese version gives the same figures.
- **The intake record's wording** ("convert 192,000 tonnes ... into 4.5% of the nation's energy") joins these; it is
  a paraphrase and is not rated. The Amphora article (6 Jun 2025) that located the figures does not contain 192,000;
  it reports, in its own words, that the Environment Minister said in a January 2025 parliamentary answer that the
  plant will process 40% of non-recyclable waste and provide 4.5% of the country's energy needs. That answer was not
  read (parlament.mt and pq.gov.mt return 403), so the Minister's wording is not rated; the speaker is WasteServ.
- **No method.** None of the WasteServ texts says what the 4.5% is a share of, or for which year.

## What the numbers show (tools/cc-079-report/calc.py; data/cc-079/checks.csv)

- Plant output: WasteServ's 126 GWh a year to the grid; the NECP (Dec 2024, p. 132) gives 2 lines x 12 t/h and
  14-16 MW net, which at the 8,000 full-load hours implied by 192,000 t / 24 t/h is 112-128 GWh. The NECP's 2030
  pie chart (Figure 120, p. 344) has a 127 GWh slice. Heat input "between 20MWth and 33.33MWth": read per line
  (66.67 MWth in all), the design calorific value is 10.0 GJ/t, the fuel input 533 GWh a year and net electrical
  efficiency 21-24% (126 GWh: 23.6%), within the 20-24% Lombardi et al. (2015) give for small-medium plants. Read as
  a total, efficiency would be 42-48%, above the 30-31% the same review gives for the largest plants: rejected.
- Figure 120's legend colours do not match its slices unambiguously (by the legend, 453 GWh would be waste-to-energy,
  which needs about 57 MW against the 14-16 MW net on p. 132). Only the sum of the slices (3,951 GWh) is used as a
  denominator; the 127 GWh slice is cited only as consistent with 126 GWh.
- Shares of 126 GWh, 2022 (the year before the June 2023 statement): 4.7% of electricity final consumption and 4.4%
  of electricity inland demand; 1.6% of final energy consumption (FEC_EED, includes international aviation), 1.8% of
  final energy use without international aviation, 1.2% of primary energy consumption and of gross inland
  consumption, 0.4% of gross available energy (which includes marine bunkers). 2024: 4.4% / 4.1% electricity;
  1.5% / 1.8% / 1.2% / 1.1% total energy. 2030 (NECP projections): 3.2% of electricity (Figure 120 total), 1.35% of
  final and 1.1% of primary energy consumption.
- 126 GWh is exactly 4.5% of 2,800 GWh (241 ktoe). Malta's gross inland consumption was 964 ktoe in 2024.
- Upper bound (not energy delivered): the waste's whole energy content, 533 GWh, would be 4.8-5.2% of primary energy
  consumption or gross inland consumption (2022-2024; 4.8% of the NECP's 2030 primary energy) and 6.2-6.6% of final
  energy consumption. This is the only total-energy reading near 4.5%; it counts the three-quarters of the energy that
  the plant does not deliver as electricity. WasteServ names no user for the plant's heat.
- Cross-checks: Eurostat PEC_EED and FEC_EED for 2022 (887.2 and 699.6 ktoe) match the NECP's Table 27 (886.6 and
  698.7); GIC minus international aviation equals total energy supply; inland demand equals net production plus
  imports minus exports.
- Capacity: 192,000 t is 54% of municipal waste generated in 2024 (354 kt), 75% of municipal waste landfilled (255 kt)
  and 67% of all non-mineral waste landfilled in 2022 (286.5 kt). The Commission's EIR 2025 gives 190,000 t.
  At 2024 generation, meeting the 2035 target (65% recycled) would leave at most 124 kt of municipal waste for energy
  recovery or landfill, 68 kt less than the capacity; generation would have to reach 549 kt (+55%) for 35% to equal
  192,000 t. Malta renounced the postponement of the municipal targets in November 2024 (EIR 2025, p. 8).
- The "40%": with 192,000 t it implies 480,000 t of non-recyclable waste. On landfill-based measures 192,000 t is
  67-75%; against all non-mineral waste generated in 2022 (598 kt, including separately collected recyclables) it is
  32%. "Non-recyclable waste" is not a published statistic and WasteServ does not define it.
- "Green": the RED II definition counts only the biodegradable fraction of municipal waste as renewable (Directive
  (EU) 2018/2001, Art. 2(24)). Radiocarbon studies at Swiss plants found roughly half the CO2 biogenic (Mohn et al.
  2008: slightly above 50%; Mohn et al. 2012: fossil 43.4-54.5%, mean 48%); these are carbon shares at Swiss plants,
  not Maltese energy shares, and are used only as context. The NECP's renewable-electricity trajectory (Figure 14,
  p. 84) shows only solar PV and biogas, and p. 144 says of the new thermal treatment plant: "This is not expected to
  contribute to Malta's RES share." The same plan (p. 84) says waste-to-energy plants contribute "a relatively small
  share" of RES-E; that sentence sits beside a figure that shows biogas, not incineration.

## Search log (what was searched, where, and when)

All on 10 Oct 2026 unless stated.
- Claim record URL (Amphora): read in full (200). Wayback: web.archive.org reset the connection (net_check.py);
  archive.org availability API returned 429.
- WebSearch: "Magħtab waste-to-energy plant 192,000 tonnes 4.5% energy ECOHIVE"; "waste to energy plant Malta 4.5%
  energy needs Miriam Dalli parliamentary question"; "Dalli waste-to-energy 4.5 energy parliamentary question January
  2025 40% non-recyclable"; Maltese-language search for "4.5%" and "skart mhux riċiklabbli"; "126 GWh"; TVM News.
  Found the Malta Business Weekly reprint (23 Oct 2020) and led to WasteServ's own site; no TVM News item found.
- Speaker's site: wasteservmalta.com redirects to wsm.com.mt (home page only read). ecohive.com.mt: project page
  (English and Maltese), news list and all 15 news articles listed on 10 Oct 2026 (English and Maltese URLs), read in
  full. The 4.5% appears in three of them (23 Oct 2020, 2 Nov 2020, 26 Jun 2023); 192,000 t in three (26 Jun, 31 Jul and
  13 Oct 2023) and on the project page. The Maltese-language article URLs serve the same English text.
- gov.mt press release PR221484 (31 Oct 2022): 403. parlament.mt (questions pages and a 2018 sitting transcript,
  /media/98829/20181210_013d_dev.docx): 403. pq.gov.mt: 403. MaltaToday (two articles found by search): 403.
- Government and EU documents: Malta's updated NECP (Dec 2024) read in the relevant sections (searched for
  "waste-to-energy", "WtE", "incinerat", "Waste to Energy"); Commission EIR 2025 (Malta) and the 2023 early-warning
  SWD searched for "waste-to-energy", "incinerat", "capacity".
- EIA for the plant: not found in a readable copy (ERA and PA sites return 403 to scripts; no copy surfaced in web
  search). Not read.
- Peer-reviewed literature on this plant or on Malta's waste-to-energy: Crossref queries "Maltese islands municipal
  waste management incineration landfill", "Malta waste-to-energy plant Maghtab", "waste to energy Malta island
  municipal solid waste" found none; OpenAlex search returned 429 (rate limit) and was not completed. So "no
  peer-reviewed study of this plant was found" rests on Crossref only.

## Second-hand leads (not used as evidence)

- ◆ MaltaToday (403; seen only in a search summary): a smaller 120,000 t option was dropped because it would have
  required much higher recycling rates. Not read; not used for any figure.
- ◆ A 2018 parliamentary transcript (parlament.mt docx, 403; search summary only) is said to give about 120,000 t
  and "40%" for an earlier design. Not read.
- The Shift News (3 Mar 2026, read): the latest procurement was aborted and no 2026 funds were allocated.

## Gaps

- WasteServ's method for the 4.5% (which energy measure, which year).
- The plant's EIA (design calorific value, heat use, net output, feedstock list).
- Whether the plant will export heat (it would raise delivered energy); none is described in any source read.
- The Minister's January 2025 parliamentary answer (wording not read).
