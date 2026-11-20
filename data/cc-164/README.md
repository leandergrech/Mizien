# CC-164 data

`nso_inbound_2025.csv`: inbound tourism 2025 (NSO news release *Inbound Tourism: December 2025*, NR 020/2026, Tables 1-2,
read in the built-in browser 17 Nov 2026; xlsx refuses scripts), plus the 2026 totals stated in the Budget Speech.
"Other rented" is NSO's rented private accommodation, the closest category to the speech's short lets.

`checks.csv`: written by `tools/cc-164-report/calc.py`. The yield estimate is a rough bound, not a forecast: it applies
the new rates to 2025 nights, removes an assumed under-18 share (half of NSO's 0-24 age group) and scales to the
speech's 2026 night total; the 8-night caps and the English-language school exemption are not modelled.
