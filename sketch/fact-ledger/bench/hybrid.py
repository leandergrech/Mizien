"""TF-IDF combined with an embedding model (z-scored sum), on tasks A and B of bench.py. Same setup as bench.py."""
import numpy as np
# reuse data loading and classes from bench.py without running its loop
src = open(__file__.replace("hybrid.py", "bench.py")).read().split("# ---------------- run")[0]
g = {"__file__": __file__.replace("hybrid.py", "bench.py")}; exec(src, g)
T = g["TFIDF"](); T.fit(list(g["claims"].values()) + g["fact_text"] + [p["summary"] for p in g["pledges"]])
for name, model, kind in [("bge-small-en-v1.5", "BAAI/bge-small-en-v1.5", "fe"), ("multilingual-MiniLM", "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2", "fe")]:
    M = g["Embed"](name, model, kind)
    def z(S): return (S - S.mean(axis=1, keepdims=True)) / (S.std(axis=1, keepdims=True) + 1e-9)
    ids, claims, gold = g["ids"], g["claims"], g["gold_edges"]
    texts = [claims[i] for i in ids]
    S = z(T.enc(texts) @ T.enc(texts).T) + z(M.enc(texts) @ M.enc(texts).T); np.fill_diagonal(S, -99)
    rec, rr = [], []
    for i, c in enumerate(ids):
        if not gold.get(c): continue
        order = [ids[j] for j in np.argsort(-S[i])]
        rec.append(len(set(order[:5]) & gold[c]) / min(5, len(gold[c]))); rr.append(1 / (1 + min(order.index(x) for x in gold[c])))
    subs, gf, facts, ft = g["subs"], g["gold_facts"], g["facts"], g["fact_text"]
    q = [s for s in subs if gf.get(s)]
    S2 = z(T.enc([subs[s] for s in q]) @ T.enc(ft).T) + z(M.enc([subs[s] for s in q]) @ M.enc(ft).T)
    rb = [len({facts[j]["id"] for j in np.argsort(-S2[i])[:5]} & gf[s]) / min(5, len(gf[s])) for i, s in enumerate(q)]
    print(f"TF-IDF + {name}: A recall@5 {np.mean(rec):.3f} MRR {np.mean(rr):.3f} | B recall@5 {np.mean(rb):.3f}")
