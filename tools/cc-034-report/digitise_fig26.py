"""Claim Check 034: digitise Figure 26 of ERA's Air Quality Plan for Malta (NO2 diurnal curves at Msida, summer and
winter, 2014-17 vs 2018-19; plan p. 60) so that calc.py can compare the plan's own curves with the EEA hourly data.

Usage:  python digitise_fig26.py /path/to/DIGITAL-Air-Quality-Plan.pdf
The plan PDF (SHA-256 56b99ee8c0d4ea56f7b7ffa55c2d72be991f6e13a48064e20da8fcff56cf11c4) is not committed; it is read
from ERA's website (era.org.mt/wp-content/uploads/2025/02/DIGITAL-Air-Quality-Plan.pdf). Needs pdftoppm (poppler) and
Pillow. Output: data/cc-034/plan_fig26_digitised.csv (series, point, value).

Method: page 60 rendered at 300 dpi; the y-axis is calibrated on the axis labels (80 at the top of the axis line, 10 at
the x-axis line: 13.4 pixels per µg/m³); each of the four lines is picked out by its flat colour, and its height is read
at the 24 vertices (x = 595.5 + 63.5 i pixels, i = 0..23; the series have 24 points). A vertex hidden under another
line is left blank. Reading error: about ±0.5 µg/m³ on slopes and up to ±1 µg/m³ at sharp peaks (the line is about
8 pixels thick). The plan's x-axis labels are spaced 60.6 pixels apart while its points are 63.5 apart; point i is
taken as label i, which is how the curves are numbered here ("label").
"""
import csv
import pathlib
import subprocess
import sys
import tempfile

from PIL import Image

D = pathlib.Path(__file__).resolve().parents[2] / "data" / "cc-034"
COLOURS = {"winter_2014-17": (147, 149, 152), "winter_2018-19": (209, 211, 212),
           "summer_2014-17": (238, 178, 65), "summer_2018-19": (246, 213, 156)}
Y_BOTTOM, PX_PER_UNIT = 3004.5, 13.4   # pixel row of 10 µg/m³ (centre of the x-axis line); pixels per µg/m³
X0, DX = 595.5, 63.5


def close(p, c, tol=6):
    return all(abs(a - b) <= tol for a, b in zip(p, c))


def main(pdf):
    with tempfile.TemporaryDirectory() as tmp:
        subprocess.run(["pdftoppm", "-r", "300", "-f", "60", "-l", "60", "-png", pdf, str(pathlib.Path(tmp) / "p")],
                       check=True)
        im = Image.open(next(pathlib.Path(tmp).glob("p-*.png"))).convert("RGB")
    rows = []
    for name, col in COLOURS.items():
        for i in range(24):
            x = round(X0 + DX * i)
            ys = [y for xx in (x - 1, x, x + 1) for y in range(2040, 3003) if close(im.getpixel((xx, y)), col)]
            val = 10 + (Y_BOTTOM - sum(ys) / len(ys)) / PX_PER_UNIT if ys else None
            rows.append({"series": name, "label": f"{i:02d}", "no2_ugm3": "" if val is None else f"{val:.1f}"})
    with open(D / "plan_fig26_digitised.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["series", "label", "no2_ugm3"])
        w.writeheader()
        w.writerows(rows)
    print("wrote plan_fig26_digitised.csv", len(rows))


if __name__ == "__main__":
    main(sys.argv[1])
