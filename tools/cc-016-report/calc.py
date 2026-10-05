#!/usr/bin/env python3
"""CC-016: test 'shore-to-ship slashes 90% of air pollution in the Grand Harbour' with formulas, not by eye.

Reads data/cc-016/ (retrieved 3 Oct 2026) and writes data/cc-016/checks.csv. The emission estimate is a simple
upper bound: it assumes a connected ship emits nothing locally while plugged in, and ignores other harbour sources.
"""
import csv, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
D = ROOT / "data" / "cc-016"
U = {r["item"]: float(r["value"]) for r in csv.DictReader(open(D / "ops_uptake.csv"))}
CALLS = {int(r["year"]): int(r["calls"]) for r in csv.DictReader(open(D / "cruise_calls.csv"))}
rows = []


def add(check, value, unit, source, note=""):
    rows.append({"check": check, "value": value, "unit": unit, "source": source, "note": note})


berths, conn = U["Cruise berths at Valletta Cruise Port"], U["Berths connected to onshore power (OPS)"]
add("Share of cruise berths that connected, Jul 2024-Jul 2025", round(100 * conn / berths, 1), "%",
    "Transport Malta FOI via Amphora", f"{int(conn)} of {int(berths)}")
t = U["Share of berth time connected"]
add("Share of berth time connected", t, "%", "Amphora Media")
add("Connections by one ship (MSC World Europa)", round(100 * U["Connections by MSC World Europa"] / conn), "% of all",
    "Transport Malta FOI via Amphora")
add("Carnival Corporation calls connected", round(100 * U["Carnival Corporation calls connected"] /
    U["Carnival Corporation calls"]), "%", "Transport Malta FOI via Amphora", "6 of 58")
# Upper bound on the cut in at-berth emissions: connected time x 100% local removal
add("Upper bound: cut in cruise at-berth emissions, year one", t, "%", "calculated",
    "if a plugged-in ship emits nothing locally")
add("Claimed cut", 90, "%", "Infrastructure Malta")
add("Connected berth time needed for a 90% cut (at 100% removal while plugged in)", 90, "%", "calculated")
hot = U["Hotelling share of cruise CO2 at Istanbul Galataport 2024"]
add("Upper bound on cut in all cruise emissions in port (hotelling >90% of CO2)", round(t * hot / 100, 1), "%",
    "calculated", "manoeuvring emissions are not touched by OPS")
add("Cruise calls 2024 -> 2025", f"{CALLS[2024]} -> {CALLS[2025]}", "calls", "Valletta Cruise Port",
    f"{100 * (CALLS[2025] / CALLS[2024] - 1):+.0f}%")
add("Cruise calls 2019 -> 2025", f"{CALLS[2019]} -> {CALLS[2025]}", "calls",
    "VCP; 2019 second-hand (Amphora; IM citing NSO)",
    f"{100 * (CALLS[2025] / CALLS[2019] - 1):+.0f}%")
# Indicative only: unplugged berth time at 2025 calls (year-one uptake) against 2024 calls with no OPS, same stay
# lengths assumed. The periods do not match: calls are calendar years, uptake is Jul 2024-Jul 2025, and OPS was
# already available from Jul 2024, so 2024 is not a no-OPS baseline.
g = CALLS[2025] / CALLS[2024]
add("Unplugged berth time at 2025 calls and year-one uptake vs 2024 calls with no OPS (indicative)",
    round(100 * (g * (1 - t / 100) - 1), 1), "%", "calculated",
    "periods differ (calendar-year calls; Jul-Jul uptake; OPS from Jul 2024): growth of the same order as uptake")
for k in ["nitrogen dioxide", "particulate matter", "sulphur dioxide", "carbon dioxide"]:
    add(f"Infrastructure Malta: per-liner cut on shore power, {k}", U[f"Per-liner cut on shore power: {k}"], "%",
        "Infrastructure Malta, 30 Nov 2020", "stated by IM; underlying study not cited")
add("Project cost figures stated", " / ".join(f"{U[k]:g}" for k in ["Project cost (stated at launch)",
    "Project cost, phase 1 (budget)", "Project cost, whole Grand Harbour Clean Air Project"]), "EUR million",
    "TVM 10 Jul 2024; IM 2020; IM 2020-2022", "launch / phase 1 budget / whole project: figures vary by phase and date")

with open(D / "checks.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\r\n")
    w.writeheader()
    w.writerows(rows)
for x in rows:
    print(f"{x['check']:84s} {str(x['value']):>12} {x['unit']:10s} {x['note']}")
