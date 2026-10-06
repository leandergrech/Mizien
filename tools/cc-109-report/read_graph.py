#!/usr/bin/env python3
"""CC-109: read the bar values of Graph 3.1 in the Commission's 2026 Country Report - Malta from the PDF's vector paths.

Graph 3.1 ("Greenhouse gas emissions in the effort sharing sectors, 2005, 2023, and 2024", source: European Environment
Agency) is drawn as filled rectangles, one path per sector with one rectangle per year. The y-axis tick labels (0 to 1.6
MtCO2e) give the scale: points per Mt is the slope of label position against label value (least squares over the nine
labels); each bar segment's value is its height divided by that slope. Values are read from the Commission's own PDF.
The Council's copy (document 10135/26 ADD 1) draws the same graph with outlined tick labels and line-built bars, so
there we check only that each sector's drawing has the same extent as in the Commission copy (within 0.01 pt).
The PDFs are downloaded to out/ (not committed).

Writes data/cc-109/graph31_bars.csv. Needs PyMuPDF (pip install pymupdf).
"""
import csv, datetime, hashlib, pathlib, urllib.request

import pymupdf

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[1]
OUT = HERE / "out"
OUT.mkdir(exist_ok=True)
COPIES = {
    "Commission": "https://economy-finance.ec.europa.eu/document/download/b0bb0c3b-1b52-4ac5-8090-ee21edf1e039_en"
                  "?filename=MT_SWD_2026_218_1_EN_autre_document_travail_service_part1_v1.pdf",
    "Council": "https://data.consilium.europa.eu/doc/document/ST-10135-2026-ADD-1/en/pdf",
}
SECTORS = {(0.0, 0.69, 0.941): "Domestic transport (excl. aviation)", (0.816, 0.808, 0.808): "Buildings (under ESR)",
           (0.573, 0.816, 0.314): "Agriculture", (1.0, 0.753, 0.0): "Small industry", (0.753, 0.0, 0.0): "Waste"}
YEARS = ("2005", "2023", "2024")
UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"}


def pdf(copy):
    p = OUT / f"country_report_2026_mt_{copy.lower()}.pdf"
    if not p.exists():
        p.write_bytes(urllib.request.urlopen(urllib.request.Request(COPIES[copy], headers=UA), timeout=120).read())
    return p


def sector_extents(page, region):
    """Bounding box of each sector's drawing (all three bars together)."""
    out = {}
    for d in page.get_drawings():
        name = SECTORS.get(tuple(round(c, 3) for c in d["fill"])) if d.get("fill") else None
        if name and region.intersects(d["rect"]) and d["rect"].width > 50:
            out[name] = d["rect"]
    return out


rows, extents = [], {}
for copy in ("Commission",):
    path = pdf(copy)
    sha = hashlib.sha256(path.read_bytes()).hexdigest()
    doc = pymupdf.open(path)
    pno = next(i for i, pg in enumerate(doc) if "effort sharing sectors, 2005, 2023, and 2024" in pg.get_text())
    page = doc[pno]
    title = page.search_for("effort sharing sectors, 2005, 2023, and 2024")[0]
    src = page.search_for("Source:")
    src = min((r for r in src if r.y0 > title.y1), key=lambda r: r.y0)
    region = pymupdf.Rect(title.x0 - 5, title.y1, title.x0 + 230, src.y0)
    # y-axis labels -> scale
    labels = []
    for b in page.get_text("dict", clip=region)["blocks"]:
        for l in b.get("lines", []):
            for s in l["spans"]:
                t = s["text"].strip()
                if t in ("0", "0.2", "0.4", "0.6", "0.8", "1", "1.2", "1.4", "1.6"):
                    labels.append((float(t), (s["bbox"][1] + s["bbox"][3]) / 2))
    n = len(labels)
    mx, my = sum(v for v, _ in labels) / n, sum(y for _, y in labels) / n
    slope = sum((v - mx) * (y - my) for v, y in labels) / sum((v - mx) ** 2 for v, _ in labels)   # pt per Mt (<0)
    segs = {}
    for d in page.get_drawings():
        if d.get("fill") is None or not region.intersects(d["rect"]) or len(d["items"]) != 3:
            continue
        name = SECTORS.get(tuple(round(c, 3) for c in d["fill"]))
        if not name:
            continue
        for it in d["items"]:
            r = it[1] if it[0] == "re" else it[1].rect
            segs.setdefault(round(r.x0), {})[name] = r
    for x, year in zip(sorted(segs), YEARS):
        base = max(r.y1 for r in segs[x].values())          # bottom of the stack = zero line
        top = min(r.y0 for r in segs[x].values())
        total = (base - top) / -slope
        for name, r in segs[x].items():
            v = r.height / -slope
            rows.append({"copy": copy, "pdf_page": pno + 1, "year": year, "sector": name, "value_mt": round(v, 4),
                         "share_of_bar_pct": round(100 * v / total, 2), "bar_total_mt": round(total, 4),
                         "scale_pt_per_mt": round(-slope, 3), "pdf_sha256": sha, "source_url": COPIES[copy],
                         "method": "vector path heights / least-squares axis scale (tools/cc-109-report/read_graph.py)",
                         "retrieved": datetime.date.today().isoformat()})
    print(copy, "page", pno + 1, "scale", round(-slope, 3), "pt/Mt")
    extents[copy] = sector_extents(page, region)

# Council copy: same drawing?
doc = pymupdf.open(pdf("Council"))
cno = next(i for i, pg in enumerate(doc) if "effort sharing sectors, 2005, 2023, and 2024" in pg.get_text())
cpage = doc[cno]
ct = cpage.search_for("effort sharing sectors, 2005, 2023, and 2024")[0]
cext = sector_extents(cpage, pymupdf.Rect(ct.x0 - 5, ct.y1, ct.x0 + 230, ct.y1 + 160))
same = all(abs(cext[k].height - extents["Commission"][k].height) < 0.01 and
           abs(cext[k].width - extents["Commission"][k].width) < 0.01 for k in SECTORS.values())
print("Council copy page", cno + 1, "same drawing as the Commission copy:", same)
assert same
for r in rows:
    r["council_copy_check"] = f"Council PDF page {cno + 1}: same sector extents (within 0.01 pt)"

with open(ROOT / "data" / "cc-109" / "graph31_bars.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0]))
    w.writeheader()
    w.writerows(rows)
for r in rows:
    print(r["copy"], r["year"], f'{r["sector"]:38s}', r["value_mt"], f'{r["share_of_bar_pct"]}%', r["bar_total_mt"])
