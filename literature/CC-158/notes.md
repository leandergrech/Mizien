# CC-158 notes (16 Nov 2026)

No literature needed: the claim is an audit office's score, tested against its own method and data.

- **Primary wording.** NAO press release (nao.gov.mt, 7 Oct 2025), read in full from the maintainer's browser copy:
  "This Review, which presents the overall situation as at September 2025, shows that Malta has made significant strides
  in climate action." Report (Oct 2025), PDF p. 14, para 2.1.1: "Malta registered an overall ClimateScanner score of 6.92
  out of 10, which in accordance with this assessment methodology is considered as representing strong progress vis-à-vis
  climate action." Same paragraph: "this methodology mainly focuses on identifying the existence of policies, mechanisms,
  or systems, rather than evaluating their effectiveness or efficiency." Para 1.4.1(ii) says the same. Conclusions p. 33:
  "considerable progress, with an overall score of 6.92 out of 10".
- **CAA note** (climateaction.gov.mt/?p=4273, 7 Oct 2025), read in full: quotes the Auditor General's "strong progress"
  sentence correctly; its own words: "notes the feedback that highlights Malta's notable and significant progress in
  tackling climate change".
- **Method.** ClimateScanner Handbook (INTOSAI / TCU, May 2024; the NAO cites this edition, footnote 11), p. 11: four tiers
  (no / early / intermediate / advanced implementation = 0 / 3.33 / 6.66 / 10); component = mean of items; axis = mean of
  components; components >= 6.66 are strengths and <= 3.33 challenges. No overall score and no "strong progress" label are
  defined. "Implementation" means "the presence or not of certain features"; the tool asks whether mechanisms exist
  "instead of evaluating their effectiveness and the results achieved".
- **Scores.** Item tier counts for each component typed from the Appendix (PDF pp. 38-73) into data/cc-158/components.csv
  (counts taken from the extracted text and spot-checked by eye for G2 and P4). calc.py reproduces all 18 component
  scores, the three axes and 6.92 (mean of axes; mean of 18 components is 6.89). P5 was assessed twice (disaster risk,
  water), both 6.66; counted once, as the NAO's axis score implies.
- **Search log (absence).** Whole extracted text of the report (73 pp.) searched on 16 Nov 2026 for "effort-shar", "ESR",
  "target", "2030", "19 per cent", "on track", "increase in emissions": no mention of Malta's effort-sharing target, gap
  or overshoot of yearly limits (hits for "2030" are NECP titles; "target" hits are generic).
- **Outcomes** reused from CC-094 (EEA ESR emissions, EU allocations; retrieved 6 Oct 2026) and CC-025 (Eurostat env_air_gge;
  retrieved 5 Oct 2026). Not re-downloaded.
- **Gaps.** The report PDF's own URL was not recorded with the maintainer's copy. Archive snapshots of the NAO and CAA pages
  need to be made by hand (both refuse scripts).
