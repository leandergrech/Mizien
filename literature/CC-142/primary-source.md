# CC-142: data behind the 7% (read in a browser, 16 November 2026)

The claim's wording was already verbatim (SWD(2026) 702). The blocker was the 2022 data behind it. Both pages below
were read on 16 Nov 2026 in a headless Chromium browser in the cloud session (scripted SQL to discodata was refused).

**1. EEA, WISE Freshwater, "Malta | Country profiles on Urban Waste Water Treatment"**,
https://water.europa.eu/freshwater/countries/uwwt/malta (data/sources.csv ref 1080). Source line: "Waterbase -
UWWTD: Urban Waste Water Treatment Directive – 2022 reported data. European Environment Agency (EEA)". The page's
figures (rendered by script):
- 3 urban areas generate 0.7 million p.e.; 3 treatment plants (2022).
- Required: collection 0.7 million p.e.; biological treatment 0.7 million p.e.; biological treatment with nitrogen
  removal 0.1 million p.e.
- "Malta has met the targets for: Collection of urban waste water".
- Further efforts needed: biological treatment to additional 0.67 million p.e. (93.1%); biological treatment with
  nitrogen removal to additional 0.08 million p.e. (100.0%).
- "Overall, 7% of the urban waste water in Malta is treated according to the requirements of the UWWTD."
The page rounds to 0.1 million p.e.; the agglomeration table itself (per-plant p.e. and compliance) is in the map pop-ups
and Waterbase, not in the page text.

**2. Office International de l'Eau & Ramboll for the Commission, *UWWTD National Summary Chapter 2020: Malta***
(12th reporting cycle), CIRCABC,
https://circabc.europa.eu/d/d/workspace/SpacesStore/28ed65e1-12bb-454b-83f1-b92c8064faee/2020-MS-chapter_Malta.pdf
(ref 1079). 13 pages, downloaded 16 Nov 2026, SHA-256 4af412b6bb0d3aa4dd66d01692f6245bba7fdfc705e623f130adeb3d56076a4c.
For 2020: 3 agglomerations of 2,000 p.e. or more, total load 643,039 p.e.; 1 agglomeration (37,537 p.e., 6%) compliant;
2 (605,502 p.e.) not compliant (secondary and more stringent treatment); load in full compliance with Article 4
(secondary treatment) 5.8%. This is the 2020 data; the claim is about the 2022 data (13th cycle), which has no
national chapter found yet.

Notes for the check: 0.67/0.7 = about 93%, so about 7% meets every requirement, consistent with the claim; compare
with 2020 (6% of load in compliant agglomerations). Not yet obtained: the per-agglomeration 2022 table.
