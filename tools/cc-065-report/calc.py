#!/usr/bin/env python3
"""CC-065: date arithmetic and a map measurement for the Ġgantija buffer-zone permit.
Writes data/cc-065/checks.csv and data/cc-065/margins.csv.

Inputs (all sourced):
- Megalithic Temples of Malta Management Plan 2012-2017 (Nov 2011), Heritage Malta PDF, Figure 2 'Buffer Zone around Ġgantija'
  (printed p. 17, PDF page 18; MEPA map, GN 357/98). Downloaded here, not committed; SHA-256 below. Needs curl, pdftoppm.
  Scale: the map's scale bar (0 to 0.4 km) and its bounding co-ordinates (E33594-E34520 = 926 m) calibrate pixels to metres.
- Dates: Newsbook (30 Apr 2026, vote 10 to 1; 13 Jun 2026), TVM News (7 Mar 2024), ADPD statement on adpd.mt (2 May 2026).
- Distances from the temples reported for the site: TVM News 7 Mar 2024 'approximately 157 meters'; The Shift 12 Mar 2026 'roughly 150
  metres'; Gozo Regional Council 15 Dec 2023 'less than 200 meters'. The management plan states a minimum 100 m radius for the buffer
  zone of a Grade A site."""
import csv, datetime, hashlib, math, pathlib, subprocess, sys, tempfile
import numpy as np
from PIL import Image
from scipy import ndimage as ndi

ROOT = pathlib.Path(__file__).resolve().parents[2]
D = ROOT / "data" / "cc-065"
URL = "https://heritagemalta.mt/app/uploads/2024/02/Megalithic-Temples-Management-Plan-2012-17.pdf"
SHA = "eb5f9899dc03763848aa5d220c11f7eaa6102a82580b8405b80789ddfd68f8b8"
RETRIEVED = "2026-10-09"
SRC = "Newsbook 30 Apr and 13 Jun 2026; TVM News 7 Mar 2024; adpd.mt 2 May 2026; Shift 12 Mar 2026; retrieved 9 Oct 2026"
rows = []
def add(check, value, unit, source=SRC, note=""):
    rows.append({"check": check, "value": value, "unit": unit, "source": source, "note": note})
d = lambda a, b: (datetime.date.fromisoformat(b) - datetime.date.fromisoformat(a)).days

add("Days from the Planning Board vote (30 Apr 2026) to the ADPD statement as dated on adpd.mt (2 May 2026)", d("2026-04-30", "2026-05-02"), "days",
    note="ADPD's text says the PA decided 'ilbieraħ' (yesterday); a post written on 1 May and stamped 2 May fits; not material to the claim")
add("Planning Board vote 10 to 1: share in favour", round(100 * 10 / 11, 1), "%", note="Newsbook 30 Apr 2026; dissent: Romano Cassar (NGO representative)")
add("Days from first approval (9 Nov 2023) to revocation (7 Mar 2024)", d("2023-11-09", "2024-03-07"), "days",
    "Gozo Regional Council 15 Dec 2023 (approval date); TVM News 7 Mar 2024 (revocation)")
add("Days from final approval (30 Apr 2026) to demolition footage (13 Jun 2026)", d("2026-04-30", "2026-06-13"), "days",
    note="Newsbook says 'six weeks' (6.3 weeks); permit conditions and the monitor's presence not independently confirmed")
add("Reported distance of the site from the temples: lowest and highest figure", "150 to 157", "m",
    "The Shift 12 Mar 2026 (roughly 150); TVM News 7 Mar 2024 (approximately 157)", "Gozo Regional Council: 'less than 200'. Measured from which point of the temple is not stated")
add("Minimum radius of the buffer zone of a Grade A archaeological site", 100, "m", "Management Plan 2012-17, section 2.1.3",
    "A minimum: the Ġgantija zone is irregular and larger (see margins.csv)")

# ---------- map measurement
pdf = pathlib.Path(tempfile.gettempdir()) / "mizien_cc065_mp.pdf"
if not pdf.exists():
    subprocess.run(["curl", "-sS", "-L", "-m", "120", "-o", str(pdf), URL], check=True)
h = hashlib.sha256(pdf.read_bytes()).hexdigest()
if h != SHA:
    print("WARNING: management plan PDF hash differs from the one read on", RETRIEVED, h)
out = pathlib.Path(tempfile.gettempdir()) / "mizien_cc065_p"
subprocess.run(["pdftoppm", "-r", "200", "-f", "18", "-l", "18", "-png", str(pdf), str(out)], check=True)
png = sorted(pathlib.Path(tempfile.gettempdir()).glob("mizien_cc065_p-*18.png"))[0]
im = np.array(Image.open(png).convert("RGB")).astype(int)
r, g, b = im[..., 0], im[..., 1], im[..., 2]
X0, X1, Y0, Y1 = 340, 1680, 300, 1300           # map frame, excluding the legend
sub = np.zeros(r.shape, bool); sub[Y0:Y1, X0:X1] = True
red = (r > 200) & (g < 140) & (b < 140) & sub
blue = (b > 170) & (b - r > 40) & (b - g > 20) & sub
cyan = (g > 180) & (b > 180) & (r < 150) & sub
lab, n = ndi.label(ndi.binary_closing(red, iterations=3))
k = 1 + int(np.argmax(ndi.sum(red, lab, range(1, n + 1))))
temple = ndi.binary_fill_holes(lab == k)
buf = ndi.binary_fill_holes(ndi.binary_closing(blue | cyan | temple, iterations=4))
# scale bar: dark run on the bar row, 0 to 0.4 km
dark = (r < 70) & (g < 70) & (b < 70)
row = np.nonzero(dark[1330])[0]
bar0, bar1 = int(row.min()), 998                 # left end of bar; right end read from the 0.4 km tick
pxm = (bar1 - bar0) / 400.0
frame_m = (1677 - 369) / pxm                     # width of the map frame in metres
add("Map calibration: width of the map frame from the scale bar, against the printed bounding co-ordinates (E33594 to E34520 = 926 m)",
    round(frame_m), "m", "Management Plan 2012-17, Figure 2", f"{pxm:.3f} px per metre at 200 dpi; difference {100*(frame_m-926)/926:+.1f}%")
add("Area of the plotted Ġgantija buffer zone (from the map, including the temple)", round(buf.sum() / pxm**2 / 1e4, 1), "ha",
    "Management Plan 2012-17, Figure 2", "pixel count on the map; approximate")
dist = ndi.distance_transform_edt(buf)
edge = temple & ~ndi.binary_erosion(temple)
m = dist[edge] / pxm
cy, cx = ndi.center_of_mass(temple)
dirs = [("North", 90), ("North-east", 45), ("East", 0), ("South-east", -45), ("South", -90), ("South-west", -135), ("West", 180), ("North-west", 135)]
mrows = []
for name, ang in dirs:
    dx, dy = math.cos(math.radians(ang)), -math.sin(math.radians(ang))
    t0 = t1 = None
    for t in np.arange(0, 1500, 0.5):
        x, y = int(round(cx + dx * t)), int(round(cy + dy * t))
        if not (0 <= x < r.shape[1] and 0 <= y < r.shape[0]): break
        if t0 is None and not temple[y, x]: t0 = t
        if not buf[y, x]: t1 = t; break
    mrows.append({"direction": name, "margin_m": round((t1 - t0) / pxm)})
add("Shortest distance from the temple polygon's edge to the buffer-zone boundary (any direction)", round(m.min()), "m",
    "Management Plan 2012-17, Figure 2", f"median {np.median(m):.0f} m, longest {m.max():.0f} m over the edge pixels")
inside = [x["direction"] for x in mrows if x["margin_m"] >= 157]
outside = [f'{x["direction"]} ({x["margin_m"]} m)' for x in mrows if x["margin_m"] < 157]
add("Of eight compass directions, those where the buffer zone extends at least 157 m from the temple edge", len(inside), "of 8",
    "Management Plan 2012-17, Figure 2", "shorter margin in: " + "; ".join(outside) + ". Distance alone does not settle whether the site is inside the zone")
with open(D / "margins.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["direction", "margin_m"]); w.writeheader(); w.writerows(mrows)
with open(D / "checks.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
for x in rows: print(f"{x['check'][:100]:100s} {str(x['value']):>10} {x['unit']}  {x['note'][:90]}")
for x in mrows: print(x)
