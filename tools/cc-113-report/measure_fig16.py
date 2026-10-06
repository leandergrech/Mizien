#!/usr/bin/env python3
"""CC-113: read Figure 16 of COM(2025) 17 ("Fossil fuel subsidies compared to GDP (%, 2015 and 2023)") by pixel.

COM(2025) 17 final (28 Jan 2025) publishes the 2023 shares only as a bar chart. This script downloads the report's
XHTML from the EU Publications Office (Cellar), extracts the figure's embedded image, finds the 0% and 4% gridlines and
measures each 2023 bar from the baseline up (allowing short gaps where the 2015 diamond or the EU-27 dashed line
crosses the bar). Output: data/cc-113/com2025_17_fig16_measured.csv. Accuracy is about +/-0.01 percentage points
(one gridline step is about 693 pixels per percentage point) for bars that rise clear of the EU-27 dashed line (about
0.66%); the tops of lower bars are crossed by that line and by the 2015 markers and are under-measured (Belgium reads
0.65 against 0.76 by eye), so the output marks them reliable = no and calc.py does not use them.
"""
import base64, csv, datetime, hashlib, pathlib, re, urllib.request
import numpy as np
from PIL import Image
import io

ROOT = pathlib.Path(__file__).resolve().parents[2]
OUT = pathlib.Path(__file__).resolve().parent / "out" / "raw"
OUT.mkdir(parents=True, exist_ok=True)
URL = "http://publications.europa.eu/resource/cellar/7150e5a9-dd6f-11ef-be2a-01aa75ed71a1.0017.03/DOC_1"
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
LABELS = "AT BE BG CY CZ DE DK EE ES FI FR EL HR HU IE IT LT LU LV MT NL PL PT RO SE SI SK EU27".split()  # chart: GR

page = urllib.request.urlopen(urllib.request.Request(URL, headers={"User-Agent": UA}), timeout=180).read().decode("utf-8")
(OUT / "com2025_17.xhtml").write_text(page, encoding="utf-8")

# record the file's SHA-256 beside fetch.py's hashes (run this script after fetch.py, which rewrites that file)
HASHES = ROOT / "data" / "cc-113" / "raw_files_sha256.csv"
hrows = [r for r in csv.DictReader(open(HASHES)) if r["file"] != "com2025_17.xhtml"]
raw = page.encode("utf-8")
hrows.append({"file": "com2025_17.xhtml", "url": URL, "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest(),
              "retrieved": datetime.date.today().isoformat()})
with open(HASHES, "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["file", "url", "bytes", "sha256", "retrieved"])
    w.writeheader()
    w.writerows(hrows)
cap = page.index("Fossil fuel subsidies compared to GDP")   # Figure 16 caption (the number is split by tags)
imgs = [(m.start(), m.group(1)) for m in re.finditer(r'src="data:image/[a-z]+;base64,([^"]+)"', page)]
pos, b64 = [im for im in imgs if im[0] < cap][-1]          # the image just before the caption
im = np.asarray(Image.open(io.BytesIO(base64.b64decode(b64))).convert("RGB")).astype(int)
H, W, _ = im.shape
r, g, b = im[..., 0], im[..., 1], im[..., 2]
bar = (b > 200) & (r < 190) & (r > 100) & (g > 190)                    # light-blue bar fill
grey = (abs(r - g) < 8) & (abs(g - b) < 8) & (r > 200) & (r < 235)      # light-grey gridlines
rows = [y for y in range(H) if grey[y].sum() > W * 0.5]
lines = []
for y in rows:
    if lines and y - lines[-1][-1] <= 2:
        lines[-1].append(y)
    else:
        lines.append([y])
grid = sorted(sum(l) / len(l) for l in lines)
assert len(grid) == 5, grid                                             # 4%, 3%, 2%, 1%, 0%
y4, y0 = grid[0], grid[-1]
pp = (y0 - y4) / 4


def height(x, max_gap=130):
    """Climb from the baseline through bar pixels, crossing gaps up to max_gap (diamonds, dashed line)."""
    y, top, gap = int(y0) - 6, None, 0
    while y > 0:
        if bar[y, x]:
            top, gap = y, 0
        else:
            gap += 1
            if gap > max_gap:
                break
        y -= 1
    return (y0 - top) / pp if top is not None else 0.0


foot = bar[int(y0) - 25:int(y0) - 5].sum(axis=0) > 10
groups, cur = [], []
for x in range(W):
    if foot[x]:
        cur.append(x)
    elif cur:
        groups.append(cur); cur = []
if cur:
    groups.append(cur)
merged = []                                       # a diamond at the foot can split a low bar in two: rejoin
for gr in groups:
    if merged and len(gr) < 120 and len(merged[-1]) < 120 and gr[-1] - merged[-1][0] < 200:   # two narrow halves
        merged[-1] = list(range(merged[-1][0], gr[-1] + 1))
    else:
        merged.append(gr)
bars = [gr for gr in merged if len(gr) > 100]
assert len(bars) == len(LABELS), len(bars)
rows = []
for lab, gr in zip(LABELS, bars):
    xs = gr[len(gr) // 5: 4 * len(gr) // 5]
    v = float(np.median([height(x) for x in xs]))
    rows.append({"geo": lab, "year": 2023, "ffs_share_of_gdp_pct_measured": round(v, 3),
                 "reliable": "yes" if v >= 0.8 else "no (bar top crossed by the EU-27 line or a 2015 marker)",
                 "method": "pixel measurement of the 2023 bar against the 0% and 4% gridlines (about +/-0.01 pp)",
                 "source": "European Commission, COM(2025) 17 final, 28 Jan 2025, Figure 16", "url": URL,
                 "retrieved": datetime.date.today().isoformat()})
with open(ROOT / "data" / "cc-113" / "com2025_17_fig16_measured.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0]))
    w.writeheader()
    w.writerows(rows)
for r_ in sorted(rows, key=lambda r_: -r_["ffs_share_of_gdp_pct_measured"])[:6]:
    print(r_["geo"], r_["ffs_share_of_gdp_pct_measured"])
