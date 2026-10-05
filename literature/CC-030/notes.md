# CC-030 notes

**Primary text:** MIA press release, 25 May 2026 (read in full on maltairport.com) for the programme and the 1,000 t.
The release does not mention carbon neutrality or ACA; MIA's neutrality wording comes from its Facts and Figures page
(modified 18 Aug 2025: "Reaching carbon neutral status in 2025", a target), its At a Glance page (modified 2 Sep 2026)
and company announcements (e.g. 495/2026, 24 Aug 2026: "...to Level 3+ (neutrality)"), and the Sustainability Report
2025, p. 31 (Level 3+ "having satisfied criteria related to the reduction of direct emissions and the offsetting of
residual emissions, namely 5,450 tonnes"). The report itself never says "carbon neutral". PDF not committed (company
copyright).

| Item | Result | Access |
|---|---|---|
| 1,000 t a year, EUR 12.5m, 35 hatch pits, EU grant EUR 5.4m | As in the release | Full text |
| AFIF project 24-MT-TC-AE-MIA | CINEA list (13 Nov 2025): eligible EUR 10,783,000; grant EUR 5,391,500; power at all 35 stands; charging for 20 eGPUs, 15 electric airside buses and other eGSE; 5 substations; 7.5 MVA. No CO2 estimate in the list | Full text |
| Level 3+ in 2025, 5,450 t credits | SR p.31; certificate pp.140-141 (Removall Carbon): Canada (Igloo Cellulose) 1,670, France (Chemin du Roi) 2,160, Uganda 1,620 | Full text |
| ACA directory entry | MIA at level term 17 = "Level 3+"; entry modified 20 Nov 2025 (WordPress REST API, `/wp-json/wp/v2/accredited-airport?slug=malta`, read 5 Oct 2026; later requests hit a captcha) | Full record |
| ACA notice, 18 Dec 2025 | "upgraded to Level 3+ ... achieving carbon neutrality for emissions under its direct control"; "In 2024, residual emissions were addressed through the purchase of highly verified emission avoidance credits"; -32% vs 2015 | Full text |
| Gold Standard block 585497 | 1,620 credits, Uganda safe water and cookstoves VPA (GS2296), vintage 2024, retired for MIA 4 Jun 2026 | Registry API |
| Rainbow transaction 9e16ced5-... | 2,160 credits, Chemin du Roi biogas (Oise, France), vintage 2022, retired on behalf of MIA 4 Jun 2026 (owner Removall Carbon) | Registry GraphQL API |
| Third block (Canada, 1,670 t) | Not found: the SR prints the Gold Standard link for 585497 twice | Gap |
| Scope 1/2/3 2015, 2024, 2025 | GRI 102-5 to 102-8, pp.124-125; GRI 103 pp.126-127 | Full text |
| Scope 3 "use of sold products" | Full-flight aircraft, APU, GPU (fuel from ground handlers), engine tests, tenants' Scope 1, passengers' landside traffic (pp.96-97) | Full text |
| Scope 1 sources | Fuel, refrigerant top-ups (counted as purchased), CO2 extinguisher refills (pp.90-91). Litres x MIA's factors give ~408 t of 813 t in 2025 | Full text |
| PwC Malta limited assurance (ISAE 3000) | Covers 102-5, 102-6, 103-2 etc.; not Scope 3 or credits (pp.112-113) | Full text |
| ACA Level 3+ rules | Scope 1, 2 and staff business travel offset | ACA website (read) |
| Aircraft movements 2025 | 65,470: MIA company announcement 461/2026 (14 Jan 2026), read in full (v1.0 had it second-hand) | Full text |
| Net Zero Carbon Plan (2024) | 2025 ACA Level 3+ Neutrality; 2030 -65%; 2050 net zero; -31% by 2023 | Full text |
| Ground power literature | Padhra (2018): accepted manuscript read in full (see below) | Full text |
| Malta Development Bank release (29 May 2026) | Repeats "approximately 1,000 tonnes" with no method; MDB lends EUR 5.4m. Not cited in the report | Read |

## Padhra (2018), what the report uses

Accepted manuscript (University of West London repository, eprint 5214, CC BY-NC-ND), read in full 5 Oct 2026.

- 25,195 intraday turnarounds of short-haul narrow-body jets at 125 European airports, June 2015 (flight data recorders).
- APU fuel flow, duration-weighted: 99.6 kg/h (arrival cycle), 104.4 kg/h (departure), 103.2 kg/h (single-cycle) (section 3.3).
- In double-cycle events the APU was off for an average of 22 min 28 s between arrival and departure (section 3.4).
- Fixed ground power for that period would cut APU emissions of CO, NOx and THC by an average of 47.6%; a mobile
  diesel GPU instead cuts net CO by 40% and NOx by 30% and roughly doubles THC (section 3.4). **Pollutants, not CO2.**
- Mobile diesel GPU fuel use 7.74 kg/h: a Zurich Airport 2004 average from Fleuti (2006), **second-hand** (Fleuti not
  read), section 2.2.

## Our calculations (tools/cc-030-report/calc.py; inputs in data/cc-030/ground_power_inputs.csv)

- Diesel 74,100 kg CO2/TJ x 43.0 TJ/Gg = 3.186 kg CO2/kg (IPCC 2006 defaults); GPU 7.74 kg/h -> 24.7 kg CO2/h.
- APU 103.2 kg/h x 3.163 kg CO2/kg (MIA's own Jet A-1 factor) = 326 kg CO2/h.
- Turnarounds = 65,470 / 2 = 32,735.
- 1,000 t / 24.7 kg/h = ~40,500 GPU-hours = 74.3 min per turnaround (every turnaround).
- GPU at every turnaround for 22.47 min: 9.2 kg per turnaround, ~302 t a year gross (before grid electricity at 0.389 kg/kWh).
- 1,000 t / 326 kg/h = 3,064 APU-hours = 5.6 min per turnaround; after the 302 t GPU case, ~3.9 min.
- Reviewer's independent check (3.19 and 3.16 kg/kg): 24.7 and 325 kg/h; 40,501 h, 74 min; 303 t; 5.6 min. Agrees.

## Gaps
- Method behind the 1,000 t (baseline, hours, APU, vehicles, grid electricity): not published. Ask MIA.
- The GPU and APU parts of Category 11 (MIA collects GPU fuel and APU times from ground handlers): not published.
- Any CO2 estimate in MIA's AFIF application: not public.
- The third credit block (Canada, 1,670 t): registry record not found; credit quality not assessed.
- Which footprint year the 5,450 t were retired against: ACA says 2024 residual emissions; retirements dated 4 Jun 2026.
- A Scope 1 breakdown (fuel vs refrigerants vs extinguishers) for 2024 and 2025.
- The Malta Independent article (Cloudflare challenge from the cloud network) was not read.

## Open-access copies

| File | Licence | SHA-256 |
|---|---|---|
| open-access/Padhra-2018-TRD-accepted-manuscript.docx | CC BY-NC-ND (University of West London repository record, eprint 5214); author's accepted manuscript, unchanged | 4b887c8625a3cb724dac47608c3c5b7ecb8bd8dd7be4920dadd0ac0e4fbe630f |
