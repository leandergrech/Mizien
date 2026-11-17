"""Claim Check 164: rough yield of the 2027 eco-contribution rates from NSO guest nights. Output: data/cc-164/checks.csv"""
import csv
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
D = ROOT / "data/cc-164"
v = {r["item"]: float(r["value"]) for r in csv.DictReader(open(D / "nso_inbound_2025.csv"))}
SRC = "NSO NR 020/2026 Tables 1-2; Budget Speech 2027 p. 26-27"
gross = v["nights_collective_2025"] * 8 + v["nights_other_rented_2025"] * 10
minors = 0.5 * v["tourists_age_0_24_2025"] / v["tourists_total_2025"]
adult = gross * (1 - minors)
growth = v["nights_2026_speech"] / v["nights_total_2025"]
scaled = adult * growth
out = [
    ("New rates x 2025 nights, all ages, no cap", round(gross / 1e6, 1), "EUR million", SRC,
     "collective EUR 8, other rented EUR 10"),
    ("Assumed under-18 share (half of NSO 0-24 group)", round(100 * minors, 1), "%", SRC, "assumption"),
    ("Adults only, 2025 nights, no cap", round(adult / 1e6, 1), "EUR million", SRC, ""),
    ("Growth in nights 2025 to 2026 (speech: 28 million)", round(100 * (growth - 1), 1), "%", SRC, ""),
    ("Adults only, scaled to 2026 nights, no cap", round(scaled / 1e6, 1), "EUR million", SRC,
     "caps of 8 nights and the English-school exemption lower this"),
    ("Tourists staying 7 nights or more, 2025", round(100 * v["tourists_stay_7plus_2025"] / v["tourists_total_2025"], 1), "%",
     SRC, "only stays over 8 nights are affected by the cap"),
    ("Speech projection", 182, "EUR million", "Budget Speech 2027 p. 27", "'madwar EUR 182 miljun'"),
    ("Estimates 2027 eco-contribution (as reported)", 213, "EUR million", "Amphora Media, 13 Nov 2026 (second-hand)",
     "against EUR 21 million for 2026; may include cruise and Comino fees"),
    ("Estimates 2027 minus 2026 (as reported)", 213 - 21, "EUR million", "Amphora Media (second-hand)", ""),
]
with open(D / "checks.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["check", "value", "unit", "source", "note"])
    w.writerows(out)
for o in out:
    print(o[0], o[1], o[4])
