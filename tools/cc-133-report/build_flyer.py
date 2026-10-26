"""Claim Check 133 flyer. Output: out/flyer.pdf and out/flyer.png"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import Flyer, build_flyer, flyer_png, GREEN, ORANGE, RED, GREY  # noqa: E402

OUT = HERE / "out"
build_flyer(Flyer(
    number="133", out=str(OUT / "flyer.pdf"), kicker="Housing and affordability",
    title_lines=["House prices against", "incomes in Malta"],
    subtitle="The Commission’s 2026 Country Report, checked against Eurostat",
    quote_lines=["“With income growth exceeding these gains, the", "price-to-income ratio has actually declined.”"],
    attribution="European Commission, 2026 Country Report – Malta, 3 June 2026",
    context="After: nominal prices ‘have risen steadily since 2014 and consistently outpace EU average growth’.",
    note="Annex 16 adds that the ratio ‘has declined since 2007’; its source is Eurostat.",
    verdict="Largely supported", verdict_right=["True on the named indicator;", "not for median income since 2014."],
    cards=[("−11.5%", GREEN, "Ratio, 2014–2024", "Eurostat’s price-to-income ratio for Malta; −23.1% since 2007. EU-27: +5.8% since 2014."),
           ("+83.6%", GREEN, "Prices, 2014–2025", "Up every year, by 3.4% to 6.7%. EU-27: +65.6%."),
           ("2020–22", ORANGE, "EU faster", "EU-27 prices rose faster than Malta’s in three years, so ‘consistently’ is too strong."),
           ("+95.7%", GREEN, "Income per head", "Household disposable income per head, national accounts, 2014–2024: faster than prices (+73.3%)."),
           ("+62.6%", ORANGE, "Median income", "EU-SILC median household income grew slower than prices: on it the ratio rose 6.6%.")],
    fair="The ratio is an average of prices against income. It does not show affordability for renters or lower-income households.",
    asks=["Commission: the vintage behind its Graph A16.3.", "NSO: why national-accounts and survey income diverge.",
          "Central Bank: any household-level affordability series.", "No right of reply needed."],
    footer="Version 1.0  ·  26 October 2026  ·  Public data only  ·  No right of reply needed",
    pdf_title="Claim Check 133 – House prices against incomes in Malta"))
flyer_png(str(OUT / "flyer.pdf"), str(OUT / "flyer.png"))
