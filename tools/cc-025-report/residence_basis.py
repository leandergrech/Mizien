#!/usr/bin/env python3
"""CC-025 (v1.2): residence-basis greenhouse gas emissions per person, 2013-2024, Malta, the EU-27 member states and the EU-27.
Emissions: Eurostat env_ac_ainah_r2 (air emissions accounts, residence principle; airpol GHG, THS_T). Headline = nace_r2 TOTAL_HH (all
economic activities plus households; the total CC-114 used). nace_r2 TOTAL (activities without households) is also saved
and reported as a sensitivity (it is not a per-person measure of residents' emissions).
Population: nama_10_pe (POP_NC, THS_PER; the series used in CC-025 and CC-114) and, as a check, demo_pjan (1 Jan, total).
Writes data/cc-025/residence_basis_raw.csv (values, flags, query URLs, retrieval date) and
data/cc-025/residence_basis_per_person.csv, and prints Malta's figures and rank. Needs network unless --offline."""
import csv, json, pathlib, sys, urllib.request, datetime
ROOT = pathlib.Path(__file__).resolve().parents[2]
D = ROOT / "data/cc-025"
B = "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/"
GEOS = "BE BG CZ DK DE EE IE EL ES FR HR IT CY LV LT LU HU MT NL AT PL PT RO SI SK FI SE".split()
G = "&".join("geo=" + g for g in GEOS + ["EU27_2020"])
Q = {"env_ac_ainah_r2": f"env_ac_ainah_r2?{G}&airpol=GHG&unit=THS_T&nace_r2=TOTAL&nace_r2=TOTAL_HH&sinceTimePeriod=2013",
     "nama_10_pe": f"nama_10_pe?{G}&na_item=POP_NC&unit=THS_PER&sinceTimePeriod=2013",
     "demo_pjan": f"demo_pjan?{G}&sex=T&age=TOTAL&unit=NR&sinceTimePeriod=2013"}
RAW = D / "residence_basis_raw.csv"


def fetch():
    out, today = [], datetime.date.today().isoformat()
    for ds, q in Q.items():
        d = json.load(urllib.request.urlopen(B + q))
        dims, size = d["id"], d["size"]
        idx = [{v: k for k, v in d["dimension"][n]["category"]["index"].items()} for n in dims]
        st = d.get("status", {})
        for k, val in d["value"].items():
            pos, co = int(k), []
            for s in reversed(size):
                co.append(pos % s)
                pos //= s
            co = co[::-1]
            c = {n: idx[i][co[i]] for i, n in enumerate(dims)}
            out.append([ds + (":" + c["nace_r2"] if "nace_r2" in c else ""), c["geo"], c["time"], val, st.get(k, ""), d["updated"], B + q, today])
    with open(RAW, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["dataset", "geo", "year", "value", "flag", "eurostat_updated", "query_url", "retrieved"])
        w.writerows(sorted(out))


if "--offline" not in sys.argv:
    fetch()
V, FL = {}, {}
for r in csv.DictReader(open(RAW)):
    key = (r["dataset"], r["geo"], int(r["year"]))
    V[key] = float(r["value"])
    FL[key] = r["flag"]
E, P, J = "env_ac_ainah_r2:TOTAL_HH","nama_10_pe", "demo_pjan"
rows = []
for g in GEOS + ["EU27_2020"]:
    try:
        e13, e24, p13, p24 = V[(E, g, 2013)], V[(E, g, 2024)], V[(P, g, 2013)], V[(P, g, 2024)]
    except KeyError:
        continue
    alt = None
    if (J, g, 2013) in V and (J, g, 2024) in V:
        alt = round(100 * ((e24 / V[(J, g, 2024)]) / (e13 / V[(J, g, 2013)]) - 1), 1)
    flags = "; ".join(f"{k[0]} {k[2]}: {v}" for k, v in sorted(FL.items()) if k[1] == g and v and k[2] in (2013, 2024))
    rows.append(dict(geo=g, t_per_person_2013=round(e13 / p13, 2), t_per_person_2024=round(e24 / p24, 2),
                     change_pct=round(100 * ((e24 / p24) / (e13 / p13) - 1), 1),
                     total_change_pct=round(100 * (e24 / e13 - 1), 1), pop_change_pct=round(100 * (p24 / p13 - 1), 1),
                     change_pct_with_demo_pjan=alt, flags=flags))
ms = sorted([r for r in rows if r["geo"] != "EU27_2020"], key=lambda r: r["change_pct"])
for i, r in enumerate(ms, 1):
    r["rank_1_is_largest_fall"] = i
for r in rows:
    r.setdefault("rank_1_is_largest_fall", "")
with open(D / "residence_basis_per_person.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
    w.writeheader()
    w.writerows(rows)
for r in rows:
    if r["geo"] in ("MT", "EU27_2020"):
        print(r)
mt = next(r for r in rows if r["geo"] == "MT")
print("Malta rank (1 = largest fall):", mt["rank_1_is_largest_fall"], "of", len(ms))
print("Next-highest rise:", ms[-2]["geo"], ms[-2]["change_pct"], "| members with a rise:", [r["geo"] for r in ms if r["change_pct"] > 0])
print("members with any flag in 2013/2024:", [(r["geo"], r["flags"]) for r in rows if r["flags"]])
