#!/usr/bin/env python3
"""CC-076: read NSO news release NR 085/2026 (Motor Vehicles: Q1/2026, released 13 May 2026), Table 1 (stock of licensed
motor vehicles, quarterly, Q1 2023 to Q1 2026) -> data/cc-076/nso_stock_by_quarter.csv.

data/cc-076/nso_nr085_table1_q1_2026.xlsx is NSO's own Table 1 workbook. nso.gov.mt refuses automated requests, so it was
fetched on 5 Oct 2026 from the Internet Archive copy of the release page (captured 13 May 2026):
https://web.archive.org/web/20260513093411/https://nso.gov.mt/wp-content/uploads/NR-085-2026_XTYC2Xun_Table1.xlsx
Only the standard library is used to read the workbook."""
import csv, pathlib, re, zipfile
ROOT = pathlib.Path(__file__).resolve().parents[2]
D = ROOT / "data" / "cc-076"
z = zipfile.ZipFile(D / "nso_nr085_table1_q1_2026.xlsx")
ss = [re.sub(r"<[^>]+>", "", s) for s in re.findall(r"<si>(.*?)</si>", z.read("xl/sharedStrings.xml").decode(), flags=re.S)]
x = z.read("xl/worksheets/sheet1.xml").decode()
year, out = None, []
for row in re.findall(r"<row.*?</row>", x, flags=re.S):
    cells = []
    for a, b in re.findall(r"<c ([^>]*?)(?:/>|>(.*?)</c>)", row, flags=re.S):
        m = re.search(r"<v>(.*?)</v>", b or "")
        if m:
            cells.append(ss[int(m.group(1))] if 't="s"' in a else m.group(1))
    if len(cells) == 1 and re.fullmatch(r"20\d\d", cells[0]):
        year = cells[0]
    elif cells and re.fullmatch(r"Q[1-4]", cells[0]):
        vals = [int(c) if c.isdigit() else 0 for c in cells[1:]]
        out.append({"year": year, "quarter": cells[0], "sum_of_columns": sum(vals[:-1]), "total": vals[-1]})
with open(D / "nso_stock_by_quarter.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["year", "quarter", "sum_of_columns", "total", "source", "retrieved"])
    w.writeheader()
    for r in out:
        w.writerow({**r, "source": "NSO NR 085/2026 Table 1 (Internet Archive copy of 13 May 2026)", "retrieved": "2026-10-05"})
print(len(out), "quarters", out[0], out[-1])
