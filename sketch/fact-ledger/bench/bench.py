"""Small, laptop-sized benchmark of claim and fact matching on Miżien's own data (brainstorm only).

Tasks (ground truth from the repository, not invented):
  A. claim -> related claims: data/edges.csv links (curated themes) as the answer key.
  B. sub-claim -> facts: the prototype ledger's hand links for the six emissions claims.
  C. Maltese -> English: 6 manifesto rows with Maltese wording -> their own English summary among 625;
     CC-114's Maltese press-release title -> CC-114 among 116 claims.
  D. speed: texts per second on this CPU.

    pip install model2vec fastembed pyyaml        # in a virtual environment; models download on first run
    python sketch/fact-ledger/build.py && python sketch/fact-ledger/bench/bench.py
"""
import csv, json, math, re, sys, time, pathlib, collections
import numpy as np
import yaml

HERE = pathlib.Path(__file__).resolve().parent
REPO = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else HERE.parents[2]
GRAPH = json.load(open(sys.argv[2] if len(sys.argv) > 2 else HERE.parent / "graph.json", encoding="utf-8"))
NUM = re.compile(r"\d+(?:\.\d+)?")

# ---------------- data
claims = {}
for p in sorted((REPO / "claims").glob("CC-*/claim.yml")):
    y = yaml.safe_load(open(p, encoding="utf-8"))
    c = y.get("claim") or {}
    claims[y["id"]] = " ".join(str(x) for x in [y.get("title"), c.get("text"), c.get("quote")] if x)
ids = list(claims)
gold_edges = collections.defaultdict(set)
for r in csv.DictReader(open(REPO / "data" / "edges.csv", encoding="utf-8")):
    a, b = r["From"], r["To"]
    if a in claims and b in claims and a != b:
        gold_edges[a].add(b); gold_edges[b].add(a)

facts = GRAPH["facts"]
SER = {s["id"]: s for s in GRAPH["series"]}
fact_text = [f"{f['statement']} ({f['measure']}, {SER[f['series']]['label']}, {f['period']})" for f in facts]
subs = {s["id"]: s["text"] for c in GRAPH["claims"] for s in c["subclaims"]}
gold_facts = collections.defaultdict(set)
for l in GRAPH["links"]:
    gold_facts[l["subclaim"]].add(l["fact"])

pledges = list(csv.DictReader(open(REPO / "data" / "manifesto_pledges.csv", encoding="utf-8")))
mt_rows = [p for p in pledges if re.search(r"[ħġżċ]", p.get("wording") or "")]
cc114_mt = "Malta l-uniku Stat Membru tal-UE li żied l-intensità tal-emissjonijiet tiegħu mill-2013 'l hawn"

checks = []
for p in sorted((REPO / "data").glob("cc-*/checks.csv")):
    try:
        for r in csv.DictReader(open(p, encoding="utf-8")):
            checks.append(f"{r.get('check', '')} {r.get('value', '')} {r.get('unit', '')}")
    except Exception:
        pass

# ---------------- methods
STOP = set("the of and in a to by is was for on as with from at that this be are has have it its an or not per cent".split())
def toks(s):
    return [w for w in re.findall(r"[a-zà-žħġżċ0-9]+", s.lower()) if w not in STOP and len(w) > 1]

class TFIDF:
    name = "TF-IDF (what similarity.py does)"
    def fit(self, corpus):
        df = collections.Counter(w for d in corpus for w in set(toks(d)))
        self.idf = {w: math.log((1 + len(corpus)) / (1 + n)) + 1 for w, n in df.items()}
    def enc(self, texts):
        vocab = {w: i for i, w in enumerate(self.idf)}
        M = np.zeros((len(texts), len(vocab) + 1))
        for i, t in enumerate(texts):
            for w, n in collections.Counter(toks(t)).items():
                M[i, vocab.get(w, len(vocab))] += n * self.idf.get(w, 0)
        return M / (np.linalg.norm(M, axis=1, keepdims=True) + 1e-9)

class Embed:
    def __init__(self, name, model, kind):
        self.name, self.kind = name, kind
        if kind == "m2v":
            from model2vec import StaticModel
            self.m = StaticModel.from_pretrained(model)
        else:
            from fastembed import TextEmbedding
            self.m = TextEmbedding(model)
    def fit(self, corpus):
        pass
    def enc(self, texts):
        E = np.asarray(self.m.encode(texts) if self.kind == "m2v" else list(self.m.embed(texts)), dtype=float)
        return E / (np.linalg.norm(E, axis=1, keepdims=True) + 1e-9)

def rank_scores(Q, D):
    return Q @ D.T

def number_bonus(q, d):
    nq, nd = {float(x) for x in NUM.findall(q)}, {float(x) for x in NUM.findall(d)}
    return 0.15 if any(abs(a - b) <= max(1.0, 0.08 * a) for a in nq for b in nd if a >= 2) else 0.0

# ---------------- run
methods = [
    TFIDF(),
    Embed("model2vec potion-base-8M (8 MB, English)", "minishlab/potion-base-8M", "m2v"),
    Embed("model2vec potion-multilingual-128M", "minishlab/potion-multilingual-128M", "m2v"),
    Embed("bge-small-en-v1.5 (67 MB, English)", "BAAI/bge-small-en-v1.5", "fe"),
    Embed("paraphrase-multilingual-MiniLM-L12 (220 MB)", "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2", "fe"),
]
results = []
for m in methods:
    row = {"method": m.name}
    # A
    m.fit(list(claims.values()) + fact_text + [p["summary"] for p in pledges])
    E = m.enc([claims[i] for i in ids]); S = rank_scores(E, E); np.fill_diagonal(S, -9)
    rec, rr = [], []
    for i, cid in enumerate(ids):
        g = gold_edges.get(cid)
        if not g:
            continue
        order = [ids[j] for j in np.argsort(-S[i])]
        rec.append(len(set(order[:5]) & g) / min(5, len(g)))
        rr.append(1 / (1 + min(order.index(x) for x in g)))
    row["A_recall@5"], row["A_mrr"], row["A_n"] = np.mean(rec), np.mean(rr), len(rec)
    # B
    q_ids = [s for s in subs if gold_facts.get(s)]
    Q, D = m.enc([subs[s] for s in q_ids]), m.enc(fact_text)
    S = rank_scores(Q, D)
    for hybrid in (False, True):
        rec = []
        for i, s in enumerate(q_ids):
            sc = S[i] + (np.array([number_bonus(subs[s], t) for t in fact_text]) if hybrid else 0)
            top = {facts[j]["id"] for j in np.argsort(-sc)[:5]}
            rec.append(len(top & gold_facts[s]) / min(5, len(gold_facts[s])))
        row["B_recall@5" + ("_numbers" if hybrid else "")] = np.mean(rec)
    row["B_n"] = len(q_ids)
    # C
    summ = [p["summary"] for p in pledges]
    D = m.enc(summ); Q = m.enc([p["wording"] for p in mt_rows])
    ranks = [1 + int(np.sum(D @ Q[i] > D[pledges.index(p)] @ Q[i])) for i, p in enumerate(mt_rows)]
    E = m.enc([claims[i] for i in ids]); q = m.enc([cc114_mt])[0]
    ranks.append(1 + int(np.sum(E @ q > E[ids.index("CC-114")] @ q)))
    row["C_ranks"] = ranks
    # D
    t = time.perf_counter(); m.enc(checks); dt = time.perf_counter() - t
    row["D_texts_per_s"] = len(checks) / dt
    results.append(row)
    print(json.dumps({k: (round(v, 3) if isinstance(v, float) else v) for k, v in row.items()}, ensure_ascii=False), flush=True)
json.dump(results, open(pathlib.Path(__file__).with_name("results.json"), "w"), indent=1, default=float)
print("check rows embedded:", len(checks), "| Maltese test rows:", len(mt_rows) + 1)
