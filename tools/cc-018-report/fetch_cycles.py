#!/usr/bin/env python3
"""CC-018 v1.2: the IMF Article IV consultation cycle of each EU member, from its latest staff report.

For each EU member, finds its latest IMF Staff Country Report (Crossref, prefix 10.5089, published from June 2024)
and reads the staff report and informational annex on the IMF eLibrary (imf.org itself returns 403 to scripts),
keeping the sentence that states the consultation cycle. Two historical Luxembourg reports (2000, 2002), read the
same way, are appended. Writes data/cc-018/imf_consultation_cycles.csv. Network needed; slow (polite delays).
"""
import csv, datetime, html, json, pathlib, re, time, urllib.parse, urllib.request

OUT = pathlib.Path(__file__).resolve().parents[2] / "data" / "cc-018" / "imf_consultation_cycles.csv"
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36"
EU = ["Austria", "Belgium", "Bulgaria", "Croatia", "Cyprus", "Czech Republic", "Denmark", "Estonia", "Finland",
      "France", "Germany", "Greece", "Hungary", "Ireland", "Italy", "Latvia", "Lithuania", "Luxembourg", "Malta",
      "Netherlands", "Poland", "Portugal", "Romania", "Slovak Republic", "Slovenia", "Spain", "Sweden"]
PAT = (r"((?:It is|The next|Staff|[A-Z][a-z]+ is|The [A-Z][a-z]+ Republic is|Malta has)[^.]*?"
       r"(?:\d+[-–]month|within \d+ months)[^.]*\.)")
ELIB = "https://www.elibrary.imf.org/view/journals/002/{}/{}/article-{}-en.xml"
HIST = [("Luxembourg (2000)", "2000", "065", "IMF Staff Country Report No. 00/65 (doi:10.5089/9781451824254.002)"),
        ("Luxembourg (2002)", "2002", "118", "IMF Country Report No. 02/118 (doi:10.5089/9781451824339.002)")]
today = datetime.date.today().isoformat()


def get(url):
    return urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA}), timeout=90).read() \
        .decode("utf-8", "replace")


def text(h):
    h = re.sub(r"(?s)<script.*?</script>|<style.*?</style>", "", h)
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", h)))


def cycle_sentence(vol, iss):
    for art in ("A001", "A002", "A003"):
        try:
            m = re.search(PAT, text(get(ELIB.format(vol, iss, art))))
        except Exception:  # noqa: BLE001
            m = None
        time.sleep(1.5)
        if m:
            return art, re.sub(r"\s+\.", ".", m.group(1).strip())
    return None, None


rows = []
for c in EU:
    q = urllib.parse.quote(f"{c} Article IV Consultation Staff Report")
    items = json.loads(get(f"https://api.crossref.org/works?query.bibliographic={q}&filter=from-pub-date:2024-06,"
                           f"prefix:10.5089&rows=15&select=DOI,title,issued,volume,issue,container-title"))
    cand = [i for i in items["message"]["items"] if i.get("container-title") == ["IMF Staff Country Reports"]
            and c.split()[0].lower() in " ".join(i.get("title", [])).lower()]
    cand.sort(key=lambda i: i["issued"]["date-parts"][0], reverse=True)
    for it in cand[:3]:
        art, s = cycle_sentence(it["volume"], it["issue"])
        if s:
            rows.append({"member": c, "cycle_months": "24" if "24" in s else "12",
                         "report": f"IMF Country Report No. {it['volume'][2:]}/{int(it['issue'])}", "statement": s,
                         "part": "staff appraisal" if art == "A001" else "informational annex",
                         "url": ELIB.format(it["volume"], it["issue"], art), "retrieved": today})
            break
    time.sleep(4)
rows.sort(key=lambda x: x["member"])
for member, vol, iss, rep in HIST:
    t = text(get(ELIB.format(vol, iss, "A001")))
    s = re.search(r"\d+\. [^.]*24[- ]month[^.]*\.|\d+\. [^.]*within 24 months\.", t).group(0)
    last = re.search(r"The last Article IV consultation was concluded at [^)]*\)\s*\([^)]*\)\.", t)
    part = "staff appraisal"
    if last:  # 2002 report: date of the previous (2000) consultation, from Appendix I (Fund relations)
        s, part = f"{s} (Appendix I: {last.group(0)})", "staff appraisal; Fund relations"
    rows.append({"member": member, "cycle_months": "24", "report": rep, "statement": s,
                 "part": part, "url": ELIB.format(vol, iss, "A001"), "retrieved": today})
with open(OUT, "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\r\n")
    w.writeheader()
    w.writerows(rows)
print(len(rows), "rows ->", OUT)
