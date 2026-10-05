# CC-018 primary wording

Read 4 October 2026 (PDF copies supplied by the maintainer, kept locally in this folder, not committed).

## Malta Developers Association release, "A strong housing market supported by excellent fundamentals" (8 Feb 2026)

Found and read 5 October 2026 (v1.1).

https://mda.com.mt/a-strong-housing-market-supported-by-excellent-fundamentals/ (WordPress post id 1574), read
through the site's REST API, https://mda.com.mt/wp-json/wp/v2/posts?search=IMF, and the page itself (browser
User-Agent).

- Published: 2026-02-08T08:38:52 (WordPress `date` and `date_gmt`; the page's `article:published_time` gives
  +00:00).
- Modified: 2026-06-17T13:40:55 UTC (`modified_gmt`; site time 14:40:55), i.e. after publication and after
  MaltaToday's report. The original 8 February text was not available to compare.
- Retrieved: 5 Oct 2026. SHA-256 of the API's `content.rendered` field:
  071f30247cc936f15f49debb75808e652b5b0ee29910c24fd1e9c3fbc83cfc05; of its plain text (tags stripped):
  87273b9d5f64a201e6ba56928f019a9839ea4f40ceafd3083a1a325c281a5f28; of the API response as retrieved:
  1fcf1d0ef308c3860b742294d998081aaae1ab38493e4f118660ad31963726c8; of the page HTML as retrieved (indicative):
  95f673e5a0d4e524d264cace16d004954651ac412f8142104890032c13ff6ab5.

Opening sentence:

> "The IMF's assessment of the Maltese housing market confirms what the Malta Developers Association has been saying
> for several years."

This matches the sentence MaltaToday quoted, except that MaltaToday wrote "the MDA" for the association's full name.
The release does not use the words "strength and stability" (MaltaToday's paraphrase).

What the rest of the release says (paraphrased; short phrases quoted): it attributes to the IMF that "current data
do not suggest overvaluation" and that the likelihood of a weakening is "currently low"; that banks are resilient and
local markets show "no signs of financial stress"; growth of about 4%; GDP per head nearly doubled since 2013; and
that the IMF will now assess Malta every two years, which it calls a "certificate of economic governance". The
release does not mention the IMF calling banks' exposures to real estate "a vulnerability", the Board's call for
vigilance, or staff's recommendation of enhanced monitoring. The IMF phrases it quotes that are not in our notes
on CR 26/29 ("current data do not suggest overvaluation", "price increases have been in line with income growth in
recent years") were not checked against the IMF PDF in this pass (imf.org returned 403 to scripted download).

## Malta Developers Association statement, as quoted by MaltaToday (8 Feb 2026, Juliana Zammit)

https://www.maltatoday.com.mt/news/national/139634/malta_development_association_welcomes_imf_assessment_housing_market
(local PDF `maltatoday-2026-02-08-mda-imf.pdf`, sha256 eec33f82...0359)

> "The IMF's assessment of the Maltese housing market confirms what the MDA has been saying for several years,"

the association said in a statement; MaltaToday's lead paraphrases it as confirming the "strength and stability" of
the property sector. (v1.0 note: the MDA's own release was not found; it has since been found, above.)

The same article reports an MDA-commissioned study (November 2025): prices up 59% since 2017, about EUR 14,800 a
year, growth "substantially outpaced" income, price-to-income ratio rising from 14.0 (2024) to 14.5 (2025).

## IMF Country Report No. 26/29, Malta: 2025 Article IV Consultation (February 2026)

https://www.imf.org/-/media/files/publications/cr/2026/english/1mltea2026001-source-pdf.pdf
(local PDF `imf-2025-article-iv-cr26-29.pdf`, sha256 a71cc037...622e). DOI 10.5089/9798229038249.002 (checked on
Crossref 5 Oct 2026: "Malta: 2025 Article IV Consultation-Press Release; and Staff Report", IMF Staff Country
Reports vol. 2026 issue 029, February 2026). PDF page numbers:

- p.3 (press release): Directors "urged vigilance on vulnerabilities from rising exposures to real estate".
- p.11, para 6: prices +6.7% in 2024; growth moderated in early 2025 "while the house price-to-income ratio remained
  stable".
- p.12, para 9: "the likelihood of weakening of property and housing markets is currently low, it is a prospective
  risk".
- p.19, para 19-20: "significant exposures of banks to real estate are a vulnerability" (72% of private loans, from
  61%); "house prices remained aligned with fundamentals and price-to-income and price-to-rent ratios have been stable".
- p.20: "in view of rapid house price growth, staff recommend enhanced monitoring".
- p.8, para 1: population density fifteen times the EU average, "straining infrastructure, housing and public services".
