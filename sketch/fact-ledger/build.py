"""Prototype fact ledger for the emissions cluster (sketch: not used by the site build or the validators).

Reads poc/ledger/*.csv (hand-curated facts with references to check rows), the six claims' claim.yml and
checks.csv from the repository, and:
  1. verifies every fact against the check rows it cites (the value must appear in that row);
  2. scans all check rows of the six claims for the same figure stated in more than one report (automatic);
  3. flags near-matches: similar wording, same unit, different value (definitions or vintages to explain);
  4. computes claim-to-claim links through shared facts and compares them with data/edges.csv;
  5. writes ledger.sqlite and graph.json.

    python sketch/fact-ledger/build.py            # writes ledger.sqlite and graph.json next to this file
"""
import csv, json, pathlib, re, sqlite3, sys, itertools, collections
import yaml

HERE = pathlib.Path(__file__).resolve().parent
REPO = pathlib.Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else HERE.parents[1]
CLAIMS = ["CC-003", "CC-025", "CC-026", "CC-031", "CC-109", "CC-114"]
NUM = re.compile(r"[-+−]?\d[\d,]*\.?\d*")
STOP = set("malta the of and in a to by vs as on per with from for its eu-27 eu change same share our".split())


def nums(s):
    out = []
    for m in NUM.findall(str(s).replace("−", "-")):
        try:
            out.append(float(m.replace(",", "")))
        except ValueError:
            pass
    return out


YEARS = re.compile(r"(?:19|20)\d\d")


def years(s):
    return tuple(YEARS.findall(s))


def same_value(x, y):
    """Equal, or equal once the more precise value is rounded to the other's decimals (10.655 and 10.7)."""
    if abs(x - y) <= max(0.051, abs(x) * 0.001):
        return True
    for v, w in ((x, y), (y, x)):
        d = len(repr(w).split(".")[1]) if "." in repr(w) else 0
        if round(v, d) == w:
            return True
    return False


def words(s):
    return {w for w in re.findall(r"[a-z][a-z\-]+", s.lower()) if w not in STOP}


def read(name):
    return list(csv.DictReader(open(HERE / "ledger" / name, encoding="utf-8")))


bases, series, facts, links = read("bases.csv"), read("series.csv"), read("facts.csv"), read("links.csv")
S = {s["id"]: s for s in series}

# ---- the claims and their check rows (line numbers as in the file: header is line 1)
claims, rows = {}, {}
for c in CLAIMS:
    y = yaml.safe_load(open(REPO / "claims" / c / "claim.yml", encoding="utf-8"))
    claims[c] = {"id": c, "title": y["title"], "speaker": y["claim"]["speaker"], "date": str(y["claim"].get("date") or ""),
                 "verdict": y.get("verdict"), "quote": (y["claim"].get("quote") or "").strip(),
                 "subclaims": [{"id": s["id"], "text": s["text"], "rating": s.get("rating"), "tone": s.get("tone"),
                                "finding": s.get("finding")} for s in (y.get("subclaims") or [])]}
    with open(REPO / "data" / c.lower() / "checks.csv", encoding="utf-8") as f:
        for i, r in enumerate(csv.DictReader(f)):
            rows[f"{c}:{i + 2}"] = r

# ---- 1. verify facts against the rows they cite
problems = []
for f in facts:
    v = float(f["value"])
    f["refs"] = f["refs"].split(";")
    for ref in f["refs"]:
        r = rows.get(ref)
        if r is None:
            problems.append(f"{f['id']}: {ref} does not exist")
            continue
        cand = nums(r["value"]) + nums(r.get("note", ""))
        if not any(abs(x - v) <= max(0.051, abs(v) * 0.001) for x in cand):
            problems.append(f"{f['id']}: {ref} value '{r['value']}' does not contain {f['value']} ({r['check'][:60]})")

# ---- 2 and 3. automatic scan across reports
keys = list(rows)
same, near = [], []
for a, b in itertools.combinations(keys, 2):
    ca, cb = a.split(":")[0], b.split(":")[0]
    if ca == cb:
        continue
    ra, rb = rows[a], rows[b]
    if (ra.get("unit") or "").strip() != (rb.get("unit") or "").strip():
        continue
    wa, wb = words(ra["check"]), words(rb["check"])
    if not wa or not wb:
        continue
    sim = len(wa & wb) / len(wa | wb)
    na, nb = nums(ra["value"]), nums(rb["value"])
    if not na or not nb or years(ra["check"]) != years(rb["check"]):
        continue
    eq = any(same_value(x, y) for x in na for y in nb)
    distinctive = any(abs(x) >= 1 and x != round(x) for x in na)
    if eq and (sim >= 0.3 or (distinctive and sim >= 0.15)):
        same.append({"a": a, "b": b, "sim": round(sim, 2), "label_a": ra["check"], "label_b": rb["check"], "value": ra["value"]})
    elif not eq and sim >= 0.6 and ("eu-27" in ra["check"].lower()) == ("eu-27" in rb["check"].lower()):
        x, y = na[0], nb[0]
        if x and y and (x > 0) == (y > 0) and abs(x - y) / max(abs(x), abs(y)) <= 0.12:
            near.append({"a": a, "b": b, "sim": round(sim, 2), "label_a": ra["check"], "label_b": rb["check"],
                         "value_a": ra["value"], "value_b": rb["value"]})

# ---- 3b. ledger rule: two facts on the same series, measure, period and unit with different values
explained = {tuple(sorted((r["a"], r["b"]))): r for r in read("explained.csv")}
tensions = []
for f, g in itertools.combinations(facts, 2):
    if (f["series"], f["measure"], f["period"], f["unit"]) == (g["series"], g["measure"], g["period"], g["unit"]) and not same_value(float(f["value"]), float(g["value"])):
        e = explained.get(tuple(sorted((f["id"], g["id"]))), {})
        tensions.append({"a": f["id"], "b": g["id"], "status": e.get("status", "unreviewed"), "explanation": e.get("explanation", "")})

# ---- 4. claim-to-claim links through shared facts
fact_claims = collections.defaultdict(set)
for l in links:
    fact_claims[l["fact"]].add(l["subclaim"][:6])
for f in facts:                      # a fact cited by a claim's check rows also belongs to that claim
    for ref in f["refs"]:
        fact_claims[f["id"]].add(ref.split(":")[0])
pair_facts = collections.defaultdict(set)
for fid, cs in fact_claims.items():
    for a, b in itertools.combinations(sorted(cs), 2):
        pair_facts[(a, b)].add(fid)
edges = set()
for r in csv.DictReader(open(REPO / "data" / "edges.csv", encoding="utf-8")):
    edges.add(tuple(sorted((r["From"], r["To"]))))
pairs = [{"a": a, "b": b, "facts": sorted(fs), "in_edges_csv": (a, b) in edges} for (a, b), fs in sorted(pair_facts.items())]
missing_in_edges = [p for p in pairs if not p["in_edges_csv"]]

# ---- 5. outputs
db = sqlite3.connect(HERE / "ledger.sqlite")
db.executescript("""
drop table if exists bases; drop table if exists series; drop table if exists facts; drop table if exists fact_refs;
drop table if exists claims; drop table if exists subclaims; drop table if exists links;
create table bases(id text primary key, name text, definition text);
create table series(id text primary key, basis text references bases, dataset text, filter text, measure text, unit text, label text);
create table facts(id text primary key, series text references series, measure text, period text, statement text, value real, unit text, vintage text, note text);
create table fact_refs(fact text references facts, ref text, check_label text, check_value text);
create table claims(id text primary key, title text, speaker text, date text, verdict text);
create table subclaims(id text primary key, claim text references claims, text text, rating text, tone text);
create table links(subclaim text references subclaims, fact text references facts, role text);
""")
db.executemany("insert into bases values (?,?,?)", [(b["id"], b["name"], b["definition"]) for b in bases])
db.executemany("insert into series values (?,?,?,?,?,?,?)", [tuple(s[k] for k in ("id", "basis", "dataset", "filter", "measure", "unit", "label")) for s in series])
db.executemany("insert into facts values (?,?,?,?,?,?,?,?,?)", [(f["id"], f["series"], f["measure"], f["period"], f["statement"], float(f["value"]), f["unit"], f["vintage"], f["note"]) for f in facts])
db.executemany("insert into fact_refs values (?,?,?,?)", [(f["id"], r, rows.get(r, {}).get("check"), rows.get(r, {}).get("value")) for f in facts for r in f["refs"]])
db.executemany("insert into claims values (?,?,?,?,?)", [(c["id"], c["title"], c["speaker"], c["date"], c["verdict"]) for c in claims.values()])
db.executemany("insert into subclaims values (?,?,?,?,?)", [(s["id"], c["id"], s["text"], s["rating"], s["tone"]) for c in claims.values() for s in c["subclaims"]])
db.executemany("insert into links values (?,?,?)", [(l["subclaim"], l["fact"], l["role"]) for l in links])
db.commit()

for f in facts:
    f["claims"] = sorted(fact_claims[f["id"]])
    f["checks"] = [{"ref": r, "label": rows[r]["check"], "value": rows[r]["value"]} for r in f["refs"] if r in rows]
graph = {"bases": bases, "series": series, "facts": facts, "links": links, "claims": list(claims.values()),
         "pairs": pairs, "auto_same": same, "auto_near": near, "problems": problems, "tensions": tensions,
         "stats": {"check_rows": len(rows), "facts": len(facts), "links": len(links), "auto_same": len(same), "auto_near": len(near),
                   "pairs": len(pairs), "pairs_missing_in_edges": len(missing_in_edges)}}
json.dump(graph, open(HERE / "graph.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)

print(f"check rows read: {len(rows)}  facts: {len(facts)}  links: {len(links)}")
print(f"reference problems: {len(problems)}")
for p in problems:
    print("  !", p)
print(f"automatic: same figure in two reports: {len(same)}; near-matches to explain: {len(near)}")
for s in same:
    print(f"  = {s['a']:>10} {s['b']:>10}  {s['value'][:16]:>16}  {s['label_a'][:55]}  |  {s['label_b'][:55]}")
for n in near:
    print(f"  ~ {n['a']:>10} {n['b']:>10}  {n['value_a'][:14]} vs {n['value_b'][:14]}  {n['label_a'][:50]}  |  {n['label_b'][:50]}")
print(f"ledger rule, same series/measure/period/unit but different value: {len(tensions)}")
for t in tensions:
    print(f"  ! {t['a']} vs {t['b']}: {t['status']}")
print(f"claim pairs sharing facts: {len(pairs)}; not in edges.csv: {len(missing_in_edges)}")
for p in pairs:
    print(f"  {p['a']}–{p['b']}  {'edges.csv' if p['in_edges_csv'] else 'NEW      '}  {','.join(p['facts'])}")
