#!/usr/bin/env python3
"""CC-157: read Malta's projected heat-related GDP loss off Fig. 4b of García-León et al. (2021).

The paper gives no table of country values and the Supplementary Information has none for Malta (checked: MOESM1 lists
Malta only as region MT00 in the NUTS list). Fig. 4b is a dot plot, so values are measured from the published image
(Nature Communications 12:5807, CC BY 4.0; image downloaded 10 Nov 2026 from media.springernature.com, saved as
data/cc-157/fig4_source_image.png). Axis calibration: tick marks at x=1230.5 (-4.0 %) and x=1962 (0 %) in the 2000-px-wide image.
Writes data/cc-157/fig4b_readings.csv and data/cc-157/checks.csv.
"""
import csv, pathlib
import numpy as np
from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parents[2]
D = ROOT / "data" / "cc-157"
im = np.array(Image.open(D / "fig4_source_image.png").convert("RGB")).astype(int)
X0, X4 = 1962.0, 1230.5  # pixel of 0 % and -4.0 %
PX = (X0 - X4) / 4.0      # pixels per percentage point
ROWS = ["Cyprus", "Croatia", "Portugal", "Malta", "Spain", "Romania", "Greece", "Italy", "Bulgaria", "France", "EFTA",
        "Slovenia", "Hungary", "Austria", "Slovakia", "Latvia", "Czechia", "Germany", "Poland", "Lithuania", "Estonia",
        "Denmark", "Finland", "Luxembourg", "Netherlands", "Sweden", "Belgium", "Ireland", "United Kingdom"]
Y0, DY = 89, (927 - 89) / (len(ROWS) - 1)
COLS = {"2055-2064": ((130, 35), (0, 50)), "1981-2000": ((90, 40), None)}


def dark_red_centre(y):
    """x-centre (pixels) of the left-most dark-red dot (the 2055-64 decade) on the row at y."""
    band = im[int(y) - 8:int(y) + 9, 1000:2000]
    m = (abs(band[:, :, 0] - 130) < 35) & (band[:, :, 1] < 50) & (band[:, :, 2] < 50)
    xs = np.where(m.any(axis=0))[0] + 1000
    if not len(xs):
        return None
    left = xs.min()
    blob = xs[xs < left + 12]       # one dot is about 11 px wide
    return (blob.min() + blob.max()) / 2.0


out, byname = [], {}
for k, name in enumerate(ROWS):
    c = dark_red_centre(Y0 + k * DY)
    if c is None:
        continue
    v = (c - X0) / PX
    byname[name] = v
    out.append({"country": name, "period": "2055-2064", "pixel_x": c, "gdp_impact_pct_read_from_figure": round(v, 2)})
with open(D / "fig4b_readings.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(out[0]))
    w.writeheader(); w.writerows(out)

mt = byname["Malta"]
rank = sorted(byname.values()).index(mt) + 1  # 1 = largest loss
checks = [
    ("Malta, GDP impact of heatwaves, 2055-2064 (read from Fig. 4b)", round(mt, 2), "% of GDP",
     "García-León et al. 2021 Fig. 4b", "dot-plot reading, uncertainty about +/-0.1 pp; multi-model average, RCP8.5 climate, no further adaptation"),
    ("Claim threshold", -2.5, "% of GDP", "Business Now / Euronews wording", "'exceeding -2.5 per cent'"),
    ("Margin of Malta's reading beyond the threshold", round(mt - (-2.5), 2), "pp", "calc", "negative = larger loss than 2.5%"),
    ("Malta's rank among plotted entries (1 = largest loss), 2055-2064", rank, "of %d" % len(byname),
     "Fig. 4b", "plotted entries include 'EFTA' as one group"),
    ("Cyprus (largest loss), 2055-2064", round(byname["Cyprus"], 2), "% of GDP", "Fig. 4b", ""),
    ("Median plotted entry, 2055-2064", round(float(np.median(list(byname.values()))), 2), "% of GDP", "Fig. 4b", ""),
    ("Europe aggregate, 2055-2064 (stated in the paper)", -1.14, "% of GDP", "García-León et al. 2021 text, p. 5",
     "'beyond 1.14% (s.d. 0.25%) in the 2060's'; average 1981-2010 0.21%"),
]
with open(D / "checks.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["check", "value", "unit", "source", "note"])
    w.writerows(checks)
for c in checks:
    print(c)
