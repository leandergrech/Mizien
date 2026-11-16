#!/usr/bin/env python3
"""CC-162: download the EEA 2026 datasets and extract the Malta rows we use into data/cc-162/.

1. Effort-sharing emissions 2005-2025 (EEA, reporting year 2026): eea_t_esd-2022_p_2005-2025_v01_r00/
   GHG_ESD-ESR_2026_updated01102026.xlsx, sheet GHG_ESD (long format; 2025 is the EEA's approximation, Mt CO2e).
2. GHG projections 2026 dataset: eea_t_ghg-emission-projections_p_2026_v01_r00/GHG_Projections_2026 datahub_dataset.xlsx.
   Sheets Totals and Gas hold a SubmissionYear column. We record which countries have a 2026 submission and Malta's
   rows (submission year, scenario, 2027 ESR totals, 2030 F-gas rows used as a spot check against CC-094).
Public Nextcloud share of the EEA datastore (same route as tools/cc-094-report/fetch.py); raw files go to out/raw/.
"""
import collections, csv, datetime, pathlib, re, subprocess, urllib.parse
import openpyxl

ROOT = pathlib.Path(__file__).resolve().parents[2]
D = ROOT / "data" / "cc-162"
RAW = pathlib.Path(__file__).resolve().parent / "out" / "raw"
DAV = "https://sdi.eea.europa.eu/datashare/public.php/webdav/"
TODAY = datetime.date.today().isoformat()
F = {"esr": "eea_t_esd-2022_p_2005-2025_v01_r00/GHG_ESD-ESR_2026_updated01102026.xlsx",
     "proj": "eea_t_ghg-emission-projections_p_2026_v01_r00/GHG_Projections_2026 datahub_dataset.xlsx"}


def share_id():
    html = subprocess.run(["curl", "-sSL", "https://sdi.eea.europa.eu/datastore/public?path=/" + F["esr"].split("/")[0] + "/"],
                          check=True, capture_output=True, text=True).stdout
    return re.search(r"datashare/s/([A-Za-z0-9]+)/download", html).group(1)


def get(rel):
    RAW.mkdir(parents=True, exist_ok=True)
    out = RAW / rel.split("/")[-1].replace(" ", "_")
    if not out.exists():
        subprocess.run(["curl", "-sS", "-f", "-u", share_id() + ":", "-o", str(out), DAV + urllib.parse.quote(rel)], check=True)
    return out


def write(name, header, rows):
    with open(D / name, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)


esr_url = "https://sdi.eea.europa.eu/catalogue/srv/api/records/be4056d8-9d3e-4cca-b995-3c684637f29e"
wb = openpyxl.load_workbook(get(F["esr"]), read_only=True, data_only=True)
rows = [(r[0], r[1], round(r[2] * 1000, 3), r[3], "kt CO2e", "approximated (proxy)" if (r[0] == "Malta" and r[1] == 2025) else "",
         "EEA GHG_ESD-ESR_2026_updated01102026.xlsx, sheet GHG_ESD", esr_url, TODAY)
        for r in wb["GHG_ESD"].iter_rows(min_row=2, values_only=True) if r[0] == "Malta"]
write("eea_esr_malta_2026.csv", ["country", "year", "value", "series", "unit", "status_note", "source", "url", "retrieved"], rows)

wb = openpyxl.load_workbook(get(F["proj"]), read_only=True, data_only=True)
subs = collections.defaultdict(set)
mt = []
for sheet in ("Totals", "Gas"):
    for r in wb[sheet].iter_rows(min_row=2, values_only=True):
        if r[0] is None:
            continue
        subs[r[0]].add(r[2])
        if r[0] == "MT" and r[2] is not None:
            if (sheet == "Totals" and r[3] == "Total excluding LULUCF") or \
               (sheet == "Gas" and r[3] == "2. Industrial processes" and r[5] == "HFC (kt CO2e)" and r[1] == 2030):
                mt.append((sheet, r[1], r[2], r[3], r[4], r[5], r[8]))
write("eea_projections_2026_submissions.csv", ["country", "submission_years_in_dataset"],
      [(c, "; ".join(str(s) for s in sorted(v))) for c, v in sorted(subs.items())])
write("eea_projections_2026_malta_rows.csv", ["sheet", "year", "submission_year", "category", "scenario", "gas", "gapfilled_value"], mt)
print("written to", D)
