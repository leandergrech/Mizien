#!/usr/bin/env python3
"""CC-079: fetch the Eurostat data used to test WasteServ's '192,000 tonnes ... around 4.5% of Malta's total energy
needs' -> data/cc-079/. Needs network. Each CSV keeps the status flags, Eurostat's update stamp, the query URL and the
retrieval date.

  eurostat_nrg_bal_c.csv   Complete energy balances, Malta, GWh and ktoe: the denominators (gross available energy,
                           gross inland consumption, primary and final energy consumption, final energy use)
  eurostat_nrg_cb_e.csv    Supply, transformation and consumption of electricity, Malta, GWh (all flows)
  eurostat_nrg_bal_peh.csv Electricity and heat production by fuel, Malta, GWh (waste and total)
  eurostat_env_wasmun.csv  Municipal waste by waste management operations, Malta, thousand tonnes and kg per person
  eurostat_env_wastrt.csv  Treatment of all waste by category and operation, Malta, tonnes (biennial)
  eurostat_env_wasgen.csv  Generation of all waste by category, Malta, tonnes (biennial)
"""
import csv, datetime, json, pathlib, urllib.request

ROOT = pathlib.Path(__file__).resolve().parents[2]
OUT = ROOT / "data" / "cc-079"
API = "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/"
BAL = ["PPRD", "IMP", "EXP", "GAE", "INTMARB", "GIC", "INTAVI", "NRGSUP", "GIC2020-2030", "PEC2020-2030",
       "FEC2020-2030", "PEC_EED", "FEC_EED", "FC_E", "AFC", "DL", "TI_EHG_E", "TO_EHG"]
QUERIES = {
    "eurostat_nrg_bal_c.csv": "nrg_bal_c?geo=MT&unit=GWH&unit=KTOE&siec=TOTAL&siec=E7000&siec=W6210&siec=W6220"
                              "&siec=RA000&" + "&".join("nrg_bal=" + b for b in BAL) + "&sinceTimePeriod=2010",
    "eurostat_nrg_cb_e.csv": "nrg_cb_e?geo=MT&siec=E7000&unit=GWH&sinceTimePeriod=2010",
    "eurostat_nrg_bal_peh.csv": "nrg_bal_peh?geo=MT&unit=GWH&siec=TOTAL&siec=W6210&siec=W6220&siec=RA000"
                                "&nrg_bal=GEP&nrg_bal=GHP&sinceTimePeriod=2010",
    "eurostat_env_wasmun.csv": "env_wasmun?geo=MT&unit=THS_T&unit=KG_HAB&sinceTimePeriod=2010",
    # all waste (not only municipal), excluding major mineral wastes, which cannot be burnt: treated and generated
    "eurostat_env_wastrt.csv": "env_wastrt?geo=MT&unit=T&hazard=HAZ_NHAZ&waste=TOT_X_MIN&waste=TOTAL&waste=W101"
                               "&waste=W103&sinceTimePeriod=2014",
    "eurostat_env_wasgen.csv": "env_wasgen?geo=MT&unit=T&hazard=HAZ_NHAZ&nace_r2=TOTAL_HH&waste=TOT_X_MIN&waste=TOTAL"
                               "&waste=W101&waste=W103&sinceTimePeriod=2014",
}


def rows(d):
    """Flatten Eurostat JSON-stat: yields ({dim: code}, {dim: label}, value, flag)."""
    dims, size = d["id"], d["size"]
    idx = [{v: k for k, v in d["dimension"][n]["category"]["index"].items()} for n in dims]
    for k, val in d["value"].items():
        pos, c = int(k), []
        for s in reversed(size):
            c.append(pos % s); pos //= s
        code = {n: idx[i][p] for i, (n, p) in enumerate(zip(dims, c[::-1]))}
        lab = {n: d["dimension"][n]["category"]["label"].get(code[n], "") for n in dims}
        yield code, lab, val, d.get("status", {}).get(k, "")


LABELLED = ("nrg_bal", "siec", "wst_oper", "waste")
today = datetime.date.today().isoformat()
OUT.mkdir(parents=True, exist_ok=True)
for name, q in QUERIES.items():
    url = API + q
    d = json.load(urllib.request.urlopen(url, timeout=120))
    keys = [n for n in d["id"] if n not in ("freq", "time")]
    out = []
    for code, lab, val, fl in rows(d):
        out.append([d["label"]] + [code[k] for k in keys] + [lab[k] for k in keys if k in LABELLED]
                   + [code["time"], val, fl, d["updated"], url, today])
    out.sort(key=lambda r: tuple(str(x) for x in r[1:len(keys) + 2]))
    labcols = [k + "_label" for k in keys if k in LABELLED]
    with open(OUT / name, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["dataset"] + keys + labcols + ["year", "value", "flag", "eurostat_updated", "query_url", "retrieved"])
        w.writerows(out)
    print(name, len(out), "rows; Eurostat updated", d["updated"])
