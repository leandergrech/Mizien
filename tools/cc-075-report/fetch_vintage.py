#!/usr/bin/env python3
"""CC-075: what Eurostat had published before the Lovin Malta article of 21 Sep 2024.

Eurostat's API serves only the current data, so the earlier vintages come from Eurostat's own publications:
- Statistics Explained "Passenger cars in the EU", through its MediaWiki API (api.php works for scripts):
  the revision list for Oct 2023 - Mar 2025; revision 627098 (31 Jan 2024; data extracted Dec 2023; 2022 figures) and
  revision 647912 (19 Aug 2024; data extracted Jul 2024; 2023 figures), which was the live revision from 19 Aug to
  5 Nov 2024, so on the article's date;
- the two "Motorisation rate" Figure 3 image files those revisions show (with upload time and sha1 from imageinfo);
- the infographic in Eurostat's news release of 17 Jan 2024 (ddn-20240117-1), "Motorisation rate of passenger cars in
  the EU, 2012 and 2022".
Files go to data/cc-075/ (es_*, news_*); vintage_sources.csv lists each with URL, sha1 and retrieval date."""
import csv, datetime, hashlib, json, pathlib, urllib.parse, urllib.request

ROOT = pathlib.Path(__file__).resolve().parents[2]
D = ROOT / "data" / "cc-075"
UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"}
API = "https://ec.europa.eu/eurostat/statistics-explained/api.php"
TODAY = datetime.date.today().isoformat()
rows = []


def get(url):
    return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=120).read()


def save(name, url, note, extra=None):
    data = get(url)
    (D / name).write_bytes(data)
    rows.append({"file": name, "url": url, "sha1": hashlib.sha1(data).hexdigest(), "bytes": len(data),
                 "retrieved": TODAY, "note": note} | (extra or {}))
    return data


q = lambda **kw: API + "?" + urllib.parse.urlencode(kw | {"format": "json"}, safe="|:,")
save("es_passenger_cars_revisions_2023-2025.json",
     q(action="query", prop="revisions", titles="Passenger_cars_in_the_EU", rvprop="ids|timestamp|comment",
       rvlimit="100", rvstart="2025-03-01T00:00:00Z", rvend="2023-10-01T00:00:00Z"),
     "Revision list: 647912 (2024-08-19) is followed by 655141 (2024-11-05), so it was live on 2024-09-21.")
for rid, note in ((627098, "Revision of 31 Jan 2024: 'Data extracted in December 2023'; Figure 3 'Motorisation rate, 2022'."),
                  (647912, "Revision of 19 Aug 2024, live until 5 Nov 2024: 'Data extracted in July 2024'; Figure 3 "
                           "'Motorisation rate, 2023'; text: Italy 694, Luxembourg 675, Cyprus 665, Finland 664, "
                           "Estonia 630, Latvia 418, EU average 571; Table 2: Malta 317,234 (2022), 323,852 (2023).")):
    save(f"es_passenger_cars_rev{rid}.json",
         q(action="query", prop="revisions", revids=str(rid), rvprop="ids|timestamp|content", rvslots="main"), note)

for title, name, note in (
        ("File:Motorisation_rate,_2023_Figure_3.png", "es_fig3_motorisation_2023.png",
         "Figure 3 of revision 647912 (2023 data, all 27 Member States)."),
        ("File:Motorisation_rate,_2022_figure_3.png", "es_fig3_motorisation_2022_jan2024.png",
         "Figure 3 of revision 627098 (2022 data as published in January 2024).")):
    info = json.loads(get(q(action="query", titles=title, prop="imageinfo", iiprop="url|sha1|timestamp|size")))
    ii = list(info["query"]["pages"].values())[0]["imageinfo"][0]
    data = save(name, ii["url"], note, {"uploaded": ii["timestamp"], "sha1_api": ii["sha1"]})
    assert hashlib.sha1(data).hexdigest() == ii["sha1"], title

save("news_20240117_infographic.png",
     "https://ec.europa.eu/eurostat/documents/4187653/18057933/Transport-equipment-passenger-cars.png/"
     "49ac26b9-94c8-9c35-a073-faa0cf8ed5eb?t=1705416759660",
     "Infographic of Eurostat news ddn-20240117-1 (17 Jan 2024): 'Motorisation rate of passenger cars in the EU, "
     "2012 and 2022' (full size, linked from the release page).")

fields = ["file", "url", "sha1", "bytes", "retrieved", "uploaded", "sha1_api", "note"]
with open(D / "vintage_sources.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=fields); w.writeheader()
    for r in rows:
        w.writerow({k: r.get(k, "") for k in fields})
for r in rows:
    print(r["file"], r["sha1"], r["bytes"], r.get("uploaded", ""))
