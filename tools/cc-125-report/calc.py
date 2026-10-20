#!/usr/bin/env python3
"""CC-125: recompute the funding split, the payout schedule and the retrofit scale of Malta's Social Climate Plan from
data/cc-125/payouts.csv and data/cc-125/plan_figures.csv (Decision C(2026) 5266 and the plan, retrieved 20 Oct 2026).
Writes data/cc-125/checks.csv."""
import csv, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[2]
D = ROOT / "data" / "cc-125"
SRC = "data/cc-125/payouts.csv, plan_figures.csv; Decision C(2026) 5266 Annex II/IV; Plan s.2.5.2, s.3.1.2.4; retrieved 20 Oct 2026"
pay = list(csv.DictReader(open(D / "payouts.csv")))
fig = {r["item"]: float(r["value"]) for r in csv.DictReader(open(D / "plan_figures.csv"))}
total, fund, nat = 60599503, 45410023, 15189480
rows = []
def add(check, value, unit, note=""):
    rows.append({"check": check, "value": value, "unit": unit, "source": SRC, "note": note})
add("Fund + national contribution", total - (fund + nat), "EUR", "0 means it equals the stated total 60,599,503")
add("Claimed 'EUR 60.6 million' (rounded from 60,599,503)", round(total / 1e6, 2), "EUR million")
add("Claimed 'EUR 45.4 million' (rounded from 45,410,023)", round(fund / 1e6, 2), "EUR million")
add("National share of total cost", round(100 * nat / total, 2), "%", "claim says at least 25%")
add("Sum of 16 payout values (Annex II)", sum(int(r["payout_eur"]) for r in pay), "EUR", "equals the Fund allocation if 45,410,023")
add("Annex II payouts minus Fund allocation", sum(int(r["payout_eur"]) for r in pay) - fund, "EUR")
for comp in ("C1 Buildings", "C2 Road transport", "C4 Technical assistance"):
    s = sum(int(r["payout_eur"]) for r in pay if r["component"] == comp)
    add(f"Payout value, {comp}", s, "EUR", f"{100*s/fund:.1f}% of the Fund allocation")
cost_sum = fig["Component C1 buildings total cost"] + fig["Component C2 road transport total cost"] + fig["Component C4 technical assistance total cost"]
add("Component costs C1+C2+C4 minus total", cost_sum - total, "EUR", "0 means components add to 60,599,503")
add("Retrofitted units as share of social housing stock (236 / 5,031)", round(100 * 236 / 5031, 2), "%", "plan says approximately 4%")
add("Retrofit cost per unit (I2 total EUR 15,513,057 / 236)", round(15513057 / 236), "EUR/unit", "I2 cost from plan s.2.1.3; includes EPCs")
add("Stated saving per retrofitted unit (1,563,195 kWh / 236)", round(1563195 / 236), "kWh/yr/unit", "no pre-renovation consumption is stated, so a percentage cannot be computed")
add("Energy-saving totals: Section 2 minus Section 3 figure", int(fig["Total energy saving stated (Section 2)"] - fig["Total energy saving stated (Section 3)"]), "kWh/yr", "the plan states two totals")
add("Buildings CO2 check: 5,220,644 kWh x 0.1249 kg/kWh", round(5220644 * 0.1249 / 1e6, 3), "ktCO2/yr", "plan: 0.65")
add("Plan CO2 total check: 0.65 + 2.89", round(0.65 + 2.89, 2), "ktCO2/yr", "plan: 3.54 'annual ... by the year 2032'")
add("Funds tied to targets/milestones due 2027-2029", sum(int(r["payout_eur"]) for r in pay if int(r["year"]) <= 2029), "EUR")
add("Funds tied to targets/milestones due 2030-2032", sum(int(r["payout_eur"]) for r in pay if int(r["year"]) >= 2030), "EUR")
add("Alternative total if Art. 30k applies, as share of baseline total", round(100 * 50878285 / total, 1), "%", "plan s.2.5.2")
with open(D / "checks.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
for r in rows: print(f"{r['check'][:78]:78s} {r['value']:>12} {r['unit']}  {r['note']}")
