#!/usr/bin/env python3
"""CC-063: fetch Eurostat series -> data/cc-063/ (with query URL and retrieval date). Needs network.
 env_wasgen: construction (NACE F) waste, total and mineral C&D (W121), tonnes, Malta (biennial).
 env_wastrt: treatment of mineral C&D waste (W121), Malta, tonnes, by operation.
 sts_copr_a: production in construction, annual volume index 2015=100, Malta."""
import csv, datetime, json, pathlib, urllib.request
ROOT = pathlib.Path(__file__).resolve().parents[2]
B = "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/"
Q = {
 "eurostat_env_wasgen.csv": B + "env_wasgen?geo=MT&nace_r2=F&nace_r2=TOTAL_HH&waste=W121&waste=TOTAL&hazard=HAZ_NHAZ&unit=T&sinceTimePeriod=2010&format=JSON",
 "eurostat_env_wastrt.csv": B + "env_wastrt?geo=MT&waste=W121&hazard=NHAZ&unit=T&sinceTimePeriod=2010&format=JSON",
 "eurostat_sts_copr_a.csv": B + "sts_copr_a?geo=MT&nace_r2=F&indic_bt=PRD&s_adj=CA&unit=I15&sinceTimePeriod=2010&format=JSON",
}
today = datetime.date.today().isoformat()
for name, url in Q.items():
    d = json.load(urllib.request.urlopen(url))
    dims, size = d["id"], d["size"]
    cats = [list(d["dimension"][n]["category"]["index"]) for n in dims]
    lab = [d["dimension"][n]["category"].get("label", {}) for n in dims]
    with open(ROOT / "data/cc-063" / name, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(dims + ["label_waste_or_oper", "value", "flag", "eurostat_updated", "query_url", "retrieved"])
        for k, v in sorted(d["value"].items(), key=lambda kv: int(kv[0])):
            pos, c = int(k), []
            for s in reversed(size):
                c.append(pos % s)
                pos //= s
            c = c[::-1]
            codes = [cats[i][j] for i, j in enumerate(c)]
            l = [lab[i].get(codes[i], "") for i in range(len(dims)) if dims[i] in ("waste", "wst_oper")]
            w.writerow(codes + ["; ".join(l), v, d.get("status", {}).get(k, ""), d["updated"], url, today])
    print(name, "ok", d["updated"])
