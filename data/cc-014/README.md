# CC-014 data

`pa_enforcement_series.csv`: stop and enforcement notices issued, and complaints alleging illegal development,
by year, transcribed from MEPA and Planning Authority annual reports (read 3 Oct 2026 in a browser; the hosting
sites block automated download) and, where the report was not reachable, from news reports of the annual report or
of parliamentary answers (marked second-hand in `access_note`). Gaps (2008, 2012-2018) are years for which no
readable source was found: the 2012 and 2014 MEPA reports are scanned images and the 2013-2019 PA reports are only
on Issuu. The 2019 complaint count (3,134) was read on 5 Oct 2026 in the PA Annual Report 2019, p. 17, from the Issuu
page image https://image.isu.pub/200611082658-b4eaf717a2b602b52dbd5e973233f6a3/jpg/page_19.jpg (SHA-256
379affc5649b7d8840e90de06844245d54e028f441e4b352dda6c0b0f2fbf2ad; not committed). It replaces 3,174, which had been
derived from MaltaToday's report that 2020 complaints were 139 higher. The 2019 notice count is still the derived
value (228); the same report (p. 18) gives 229. `checks.csv` is written by `tools/cc-014-report/calc.py`.
