# CC-014 data

`pa_enforcement_series.csv`: stop and enforcement notices issued, and complaints alleging illegal development, by
year. 2001-2011 from MEPA annual reports (read 3 Oct 2026 in a browser; the hosting site blocks automated download);
2017-2023 from Planning Authority annual reports, read 5 Oct 2026 as Issuu page images; 2024 from the PA Annual Report
2024 (read 3 Oct 2026 in a browser). The provenance columns give, per value, the report year, printed page, page-image
URL and the image's SHA-256 (images are not committed). Gaps (2008, 2012-2016) are years for which no readable source
was found: the 2012 and 2014 MEPA reports are scanned images and no report was found for 2013, 2015 or 2016.

`pa_annual_reports_2017_2023.csv`: every value read in the PA annual reports 2017-2023 (one row per value: year,
measure, value, unit, how it was read, report, printed page, image URL, image SHA-256, short wording where relevant,
note). Includes complaints received and closed, the stated share confirmed as illegal development, outcomes of
confirmed complaints (sanctioning applications, removals, notices), notices issued, the share with daily fines,
pending notices, notices closed and the Authority's stated enforcement policy. `calc.py` checks that the series file
carries exactly these notices and complaints values for 2017-2023.

Image URLs follow `https://image.isu.pub/DOCUMENT-ID/jpg/page_N.jpg`. Document ids: 2017
180528134326-e008b595a30d9c9d8c83aa585c183c36; 2018 190612091633-48f91f0e7444d11f42e78e132ad1ff21 (two-page spreads);
2019 200611082658-b4eaf717a2b602b52dbd5e973233f6a3 (printed page = image page minus 2); 2020
210719100023-72a629834062339679de572a3a5a0b84; 2021 240109101246-583208ef917d9cc32f97facede01dee9 (Issuu slug says
2022); 2022 240109101631-eb1b678abe73ec641796e5760f79c072; 2023 250204110148-4e1aeca18c00179350bf7ff79723d25b.

Values that replaced v1.1's second-hand figures: 2019 notices 228 (derived) -> 229; 2023 complaints 2,456 (complaints
closed, from a news report) -> 2,463 received. 2020-2023 notices and 2020 complaints were confirmed unchanged.

`outcomes_by_year.csv` and `checks.csv` are written by `tools/cc-014-report/calc.py`. In `outcomes_by_year.csv`,
`confirmed` = stated share x complaints received; `removed_how` says whether the removal count was read or derived
(from a stated percentage, or as the remainder for 2018). See `literature/CC-014/notes.md` for definitions that change
across years.
