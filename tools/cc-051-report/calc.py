#!/usr/bin/env python3
"""CC-051: protected share of Malta's seas under each reference area, where the protected sea lies, and how much of
each depth band is protected. Run fetch_data.py first. Writes data/cc-051/checks.csv and data/cc-051/depth_bands.csv.
Needs shapely, pyproj, numpy and Pillow (for the depth grid)."""
import csv, json, pathlib
import numpy as np
import pyproj
import shapely
from PIL import Image
from shapely import make_valid
from shapely.geometry import shape
from shapely.ops import transform, unary_union

HERE = pathlib.Path(__file__).resolve().parent
D = HERE.parents[1] / "data" / "cc-051"
N = list(csv.DictReader(open(D / "natura2000_marine.csv")))
A = list(csv.DictReader(open(D / "reference_areas.csv")))
REF = {a["reference_area"]: float(a["km2"]) for a in A}
FMZ, EU = REF["Fisheries Management Zone (25 nm)"], REF["Marine waters reported to the EU"]
prot = float(next(r for r in N if r["sitecode"] == "UNION")["sea_km2"])
nsites = sum(1 for r in N if r["sitecode"] != "UNION" and r["sea_km2"] and float(r["sea_km2"]) >= 1)
summed = sum(float(r["sea_km2"]) for r in N if r["sitecode"] != "UNION" and float(r["sea_km2"] or 0) >= 1)
rows = [{"check": "Marine Natura 2000 sites", "value": nsites, "unit": "sites", "source": "EEA", "note": "ERA: 18 sites"},
        {"check": "Protected sea area (union, overlaps counted once)", "value": prot, "unit": "km2", "source": "EEA",
         "note": "ERA: over 4,100 km2"},
        {"check": "Sum of site areas (overlaps double-counted)", "value": round(summed, 1), "unit": "km2", "source": "EEA", "note": ""}]
for a in [x for x in A if "Territorial" not in x["reference_area"]]:
    rows.append({"check": f"Protected share of {a['reference_area']}", "value": round(100 * prot / float(a["km2"]), 1),
                 "unit": "%", "source": "calculated", "note": a["note"]})
rows.append({"check": "Extra protected area needed for 30% of EU-reported marine waters", "value": round(0.3 * EU - prot),
             "unit": "km2", "source": "calculated", "note": ""})
rows.append({"check": "Whole Fisheries Management Zone as a share of EU-reported marine waters",
             "value": round(100 * FMZ / EU, 1), "unit": "%", "source": "calculated",
             "note": "upper limit of protection if every km2 within 25 nm were protected"})
rows.append({"check": "EU-reported marine waters beyond 25 nm", "value": round(EU - FMZ), "unit": "km2",
             "source": "calculated", "note": f"{100 * (EU - FMZ) / EU:.1f}% of the 75,715 km2"})

# ---------------------------------------------------------------- boundaries (data/cc-051/boundaries.geojson)
P = pyproj.Transformer.from_crs(4326, 32633, always_xy=True).transform
Z = {f["properties"]["zone"]: make_valid(transform(P, shape(f["geometry"]))).buffer(0)
     for f in json.load(open(D / "boundaries.geojson"))["features"]}
km2 = lambda g: g.area / 1e6
pz = Z["protected"]
envelope = Z["within_25nm"]
internal = Z["within_25nm"].difference(Z["fmz"])
all_waters = unary_union([Z["eu_marine_waters"], Z["within_25nm"]])
B = [("Territorial sea, 12 nm (Marine Regions v4)", "territorial_sea", "Marine Regions: 3,838 km2"),
     ("Fisheries Management Zone, 25 nm from baselines (rebuilt)", "fmz", "official 11,480 km2"),
     ("Exclusive economic zone (Marine Regions v12)", "eez", "Marine Regions: 52,923 km2"),
     ("Marine waters reported to the EU (EEA map service, simplified)", "eu_marine_waters", "EEA spokesperson: 75,715 km2")]
for label, key, note in B:
    rows.append({"check": f"Boundary area: {label}", "value": round(km2(Z[key]), 1), "unit": "km2",
                 "source": "calculated (UTM 33N)", "note": note})
    rows.append({"check": f"Protected sea inside: {label}", "value": round(km2(pz.intersection(Z[key])), 1),
                 "unit": "km2", "source": "calculated", "note": ""})
rows.append({"check": "Protected sea more than 25 nm from the baselines",
             "value": round(km2(pz.difference(envelope.buffer(0.1 * 1852))), 1), "unit": "km2", "source": "calculated",
             "note": "0.1-nm tolerance for boundary precision"})
rows.append({"check": "Protected sea in internal waters (landward of the baselines)",
             "value": round(km2(pz.intersection(internal)), 1), "unit": "km2", "source": "calculated",
             "note": "the official FMZ area excludes internal waters"})
rows.append({"check": "Protected share of FMZ, internal waters excluded from both",
             "value": round(100 * km2(pz.intersection(Z["fmz"])) / FMZ, 1), "unit": "%", "source": "calculated", "note": ""})
rows.append({"check": "Protected share of the sea within 25 nm, internal waters included in both",
             "value": round(100 * prot / km2(envelope), 1), "unit": "%", "source": "calculated", "note": ""})
rows.append({"check": "EU-reported marine waters beyond 25 nm (boundaries)",
             "value": round(km2(Z["eu_marine_waters"].difference(envelope))), "unit": "km2", "source": "calculated",
             "note": f"{100 * km2(Z['eu_marine_waters'].difference(envelope)) / km2(Z['eu_marine_waters']):.1f}% of the polygon"})
rows.append({"check": "EU-reported marine waters outside the EEZ as mapped by Marine Regions",
             "value": round(km2(Z["eu_marine_waters"].difference(Z["eez"]))), "unit": "km2", "source": "calculated", "note": ""})

# ---------------------------------------------------------------- depth bands (EMODnet grid from fetch_data.py)
BANDS = [("Shelf, 0-200 m", 0, 200), ("Slope, 200-1,000 m", 200, 1000), ("Deep sea, over 1,000 m", 1000, 1e5)]
X0, Y0, X1, Y1 = 12.4, 34.0, 18.3, 36.8
grid = np.array(Image.open(HERE / "out" / "bathymetry.tif")).astype("float64")
H, Wd = grid.shape
lon = X0 + (X1 - X0) / Wd * (np.arange(Wd) + 0.5)
lat = Y1 - (Y1 - Y0) / H * (np.arange(H) + 0.5)
LON, LAT = np.meshgrid(lon, lat)
GX, GY = pyproj.Transformer.from_crs(4326, 32633, always_xy=True).transform(LON, LAT)
cell = ((X1 - X0) / Wd * 111.320 * np.cos(np.radians(LAT))) * ((Y1 - Y0) / H * 110.574)  # km2 per cell
sea = grid < 1e9                       # land is no-data
depth = np.where(sea, -grid, np.nan)   # metres, positive down


def inside(g):
    shapely.prepare(g)
    return shapely.contains_xy(g, GX, GY) & sea


mp = inside(pz)
drows = []
for zone, g in [("Within 25 nm (incl. internal waters)", envelope),
                ("All waters reported to the EU (incl. internal waters)", all_waters)]:
    m = inside(g)
    tot = cell[m].sum()
    for band, lo, hi in BANDS:
        b = m & (depth < hi) & ((depth >= lo) if lo else True)
        a, ap = cell[b].sum(), cell[b & mp].sum()
        drows.append({"zone": zone, "depth_band": band, "area_km2": round(a), "share_of_zone_pct": round(100 * a / tot, 1),
                      "protected_km2": round(ap), "protected_pct": round(100 * ap / a, 1)})
for band, lo, hi in BANDS:
    b = mp & (depth < hi) & ((depth >= lo) if lo else True)
    drows.append({"zone": "Protected sea (18 sites)", "depth_band": band, "area_km2": round(cell[b].sum()),
                  "share_of_zone_pct": round(100 * cell[b].sum() / cell[mp].sum(), 1), "protected_km2": round(cell[b].sum()),
                  "protected_pct": 100.0})
with open(D / "depth_bands.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(drows[0]), lineterminator="\r\n")
    w.writeheader()
    w.writerows(drows)
rows.append({"check": "Deepest point inside a protected site", "value": round(float(np.nanmax(depth[mp]))), "unit": "m",
             "source": "EMODnet via EEA", "note": "grid cells of about 200 m"})

with open(D / "checks.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\r\n")
    w.writeheader()
    w.writerows(rows)
for r in rows:
    print(f"{r['check']:86s} {str(r['value']):>9} {r['unit']:4s} {r['note']}")
for r in drows:
    print(f"{r['zone']:54s} {r['depth_band']:24s} {r['area_km2']:>7} km2 ({r['share_of_zone_pct']:>5}%)  "
          f"protected {r['protected_km2']:>6} ({r['protected_pct']}%)")
