#!/usr/bin/env python3
"""CC-075: read three Eurostat bar charts by pixel measurement (files fetched by fetch_vintage.py into data/cc-075/).

1. es_fig3_motorisation_2023.png: Statistics Explained "Passenger cars in the EU", Figure 3 "Motorisation rate,
   2023", in revision 647912 (live 19 Aug - 5 Nov 2024). Horizontal bars, sorted.
2. es_fig3_motorisation_2022_jan2024.png: the same article's Figure 3 "Motorisation rate, 2022" (uploaded
   16 Jan 2024, shown in revision 627098).
3. news_20240117_infographic.png: Eurostat news of 17 Jan 2024, "Motorisation rate of passenger cars in the EU, 2012
   and 2022"; vertical bars, the 2022 bars (gold) are read.

Method: bars are found by their colour; the value scale is calibrated on the chart's own gridlines (every 100 cars per
1,000) and axis, then checked against the values Eurostat prints in the accompanying text. Labels are listed in the
order printed on each chart (read from the images). Ranks among the 27 Member States are by measured value.
Writes data/cc-075/chart_reads.csv."""
import csv, pathlib
from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parents[2]
D = ROOT / "data" / "cc-075"
EU27 = ["Belgium", "Bulgaria", "Czechia", "Denmark", "Germany", "Estonia", "Ireland", "Greece", "Spain", "France",
        "Croatia", "Italy", "Cyprus", "Latvia", "Lithuania", "Luxembourg", "Hungary", "Malta", "Netherlands", "Austria",
        "Poland", "Portugal", "Romania", "Slovenia", "Slovakia", "Finland", "Sweden"]

CHARTS = [
    dict(file="es_fig3_motorisation_2023.png", chart="Statistics Explained Figure 3, 2023 data (rev 647912)",
         kind="h", colour=(38, 68, 167),
         labels=["EU", "Italy", "Luxembourg", "Cyprus", "Finland", "Estonia", "Poland", "Czechia", "Lithuania", "Germany",
                 "Slovenia", "France", "Malta", "Austria", "Greece", "Portugal", "Spain", "Belgium", "Netherlands",
                 "Croatia", "Slovakia", "Denmark", "Sweden", "Bulgaria", "Ireland", "Hungary", "Romania", "Latvia",
                 "Liechtenstein", "Iceland", "Switzerland", "Norway", "Montenegro", "Georgia", "Serbia", "Moldova",
                 "Bosnia and Herzegovina", "North Macedonia", "Albania", "Türkiye", "Kosovo"],
         printed={"Italy": 694, "Luxembourg": 675, "Cyprus": 665, "Finland": 664, "Estonia": 630, "Latvia": 418,
                  "EU": 571},
         printed_src="text of revision 647912"),
    dict(file="es_fig3_motorisation_2022_jan2024.png", chart="Statistics Explained Figure 3, 2022 data (Jan 2024)",
         kind="h", colour=(38, 68, 167),
         labels=["EU", "Italy", "Luxembourg", "Finland", "Cyprus", "Estonia", "Malta", "Czechia", "Lithuania", "Germany",
                 "Slovenia", "Poland", "Austria", "France", "Spain", "Portugal", "Greece", "Belgium", "Netherlands",
                 "Croatia", "Denmark", "Sweden", "Slovakia", "Ireland", "Bulgaria", "Hungary", "Romania", "Latvia",
                 "Liechtenstein", "Iceland", "Norway", "Switzerland", "Montenegro", "Georgia", "Serbia",
                 "North Macedonia", "Bosnia and Herzegovina", "Albania", "Türkiye", "Kosovo"],
         printed={"Italy": 684, "Luxembourg": 678, "Finland": 661, "Cyprus": 658, "Latvia": 414, "Romania": 417,
                  "Hungary": 424, "EU": 560},
         printed_src="Eurostat news of 17 Jan 2024"),
    dict(file="news_20240117_infographic.png", chart="Eurostat news infographic, 17 Jan 2024, 2022 bars",
         kind="v", colour=(176, 145, 33),
         labels=["EU", "Italy", "Luxembourg", "Finland", "Cyprus", "Estonia", "Malta", "Czechia", "Lithuania", "Germany",
                 "Slovenia", "Poland", "France", "Austria", "Spain", "Portugal", "Greece", "Belgium", "Netherlands",
                 "Croatia", "Denmark", "Sweden", "Slovakia", "Ireland", "Bulgaria", "Hungary", "Romania", "Latvia"],
         printed={"Italy": 684, "Luxembourg": 678, "Finland": 661, "Cyprus": 658, "Latvia": 414, "Romania": 417,
                  "Hungary": 424, "EU": 560},
         printed_src="Eurostat news of 17 Jan 2024"),
]


def near(c, ref, tol=18):
    return all(abs(a - b) <= tol for a, b in zip(c, ref))


def runs(idx):
    out, cur = [], [idx[0]]
    for i in idx[1:]:
        if i == cur[-1] + 1:
            cur.append(i)
        else:
            out.append(cur); cur = [i]
    out.append(cur)
    return out


def grey(c):
    return c[0] == c[1] == c[2] and 150 < c[0] < 235


def read(ch):
    im = Image.open(D / ch["file"]).convert("RGB")
    W, H = im.size
    px = im.load()
    if ch["kind"] == "h":
        rows = [y for y in range(H) if sum(near(px[x, y], ch["colour"]) for x in range(W)) > 20]
        bars = runs(rows)
        ends = []
        for b in bars:
            y = b[len(b) // 2]
            xs = [x for x in range(W) if near(px[x, y], ch["colour"])]
            ends.append((y, min(xs), max(xs)))
        starts = [e[1] for e in ends]
        axis = max(set(starts), key=starts.count)              # bars all start at the axis
        ends = [e for e in ends if abs(e[1] - axis) <= 3]       # drops the logo's flag and other blue marks
        bars = [b for b in bars if any(b[len(b) // 2] == e[0] for e in ends)]
        top, bot = bars[0][0], bars[-1][-1]
        cols = [x for x in range(axis + 5, W) if sum(grey(px[x, y]) for y in range(top, bot)) > 0.25 * (bot - top)]
        grid = [sum(r) / len(r) for r in runs(cols)]
        pos = [e[2] for e in ends]
    else:
        cols = [x for x in range(W) if sum(near(px[x, y], ch["colour"]) for y in range(H)) > 20]
        bars = runs(cols)
        ends = []
        for b in bars:
            x = b[len(b) // 2]
            ys = [y for y in range(H) if near(px[x, y], ch["colour"])]
            ends.append((x, min(ys), max(ys)))
        bottoms = [e[2] for e in ends]
        base = max(set(bottoms), key=bottoms.count)              # bars all stand on the axis
        ends = [e for e in ends if abs(e[2] - base) <= 3]
        bars = [b for b in bars if any(b[len(b) // 2] == e[0] for e in ends)]
        axis = base + 1
        left, right = bars[0][0], bars[-1][-1]
        rws = [y for y in range(0, axis - 5) if sum(grey(px[x, y]) for x in range(left, right)) > 0.12 * (right - left)]
        grid = sorted((sum(r) / len(r) for r in runs(rws)), reverse=True)   # nearest the axis first
        pos = [e[1] for e in ends]
    assert len(ends) == len(ch["labels"]), (ch["file"], len(ends), len(ch["labels"]))
    # gridlines are at 100, 200, ...; fit value = a + b * pixel through the axis (0) and every gridline
    pts = [(axis, 0.0)] + [(g, 100.0 * (i + 1)) for i, g in enumerate(grid)]
    n = len(pts); mx = sum(p for p, _ in pts) / n; my = sum(v for _, v in pts) / n
    b = sum((p - mx) * (v - my) for p, v in pts) / sum((p - mx) ** 2 for p, _ in pts)
    a = my - b * mx
    vals = {lab: round(a + b * p, 1) for lab, p in zip(ch["labels"], pos)}
    resid = {k: round(vals[k] - v, 1) for k, v in ch["printed"].items()}
    eu = sorted(((v, k) for k, v in vals.items() if k in EU27), reverse=True)
    rank = {k: i + 1 for i, (_, k) in enumerate(eu)}
    return vals, resid, rank, len(eu), len(grid)


out = []
for ch in CHARTS:
    vals, resid, rank, n, ng = read(ch)
    worst = max(abs(r) for r in resid.values())
    print(f"{ch['file']}: {ng} gridlines; EU-27 bars {n}; residuals on printed values ({ch['printed_src']}): {resid}")
    print("   Malta", vals["Malta"], "rank", rank["Malta"], "of", n, "| neighbours:",
          [(k, vals[k], rank[k]) for k in sorted(rank, key=rank.get) if abs(rank[k] - rank["Malta"]) <= 1])
    for i, lab in enumerate(ch["labels"]):
        out.append({"chart": ch["chart"], "file": ch["file"], "order": i, "label": lab, "value_read": vals[lab],
                    "eu27_rank_by_value": rank.get(lab, ""), "printed_value": ch["printed"].get(lab, ""),
                    "max_abs_residual_on_printed": worst})
with open(D / "chart_reads.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(out[0])); w.writeheader(); w.writerows(out)
