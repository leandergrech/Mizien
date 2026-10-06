"""Claims with similar wording, computed when the site data is built (scripts/build_site_data.py).

Each claim's own words (its title, the claim as summarised and the verbatim quote; not our counter-evidence) are
turned into a TF-IDF vector: words that are frequent in the claim but rare across all claims weigh most. Two claims
are similar when the cosine of their vectors reaches THRESHOLD and they share at least MIN_SHARED words; each claim
keeps its TOP most similar, with the shared words that contribute most, so the site can say *why* two claims are
listed together.

Nothing here is a judgement: similar wording is a lead for a reader, like a shared body or theme, and the site
always shows the words behind it. No external library or service is used, and the result is the same on every run.
"""
import math
import re
import unicodedata
from collections import Counter

THRESHOLD = 0.25
MIN_SHARED = 2     # one shared word ("Gozo", "blue") is not enough
TOP = 5
STOP = set("""a about above after again against all also am an and any are as at be because been before being below
between both but by can could did do does doing down during each few for from further had has have having he her here
hers him his how i if in into is it its itself just me more most my no nor not now of off on once only or other our out
over own same she should so some such than that the their them then there these they this those through to too under
until up very was we were what when where which while who whom why will with would you your yours said says say says
per cent percent year years new one two three first last will would may might must shall since within without
according also around including including made make makes many much number among across already still yet even well
malta maltese government minister ministry claim claims become becomes became five six seven ten
lovin times today maltatoday newsbook shift independent reporting reported reports report told statement stated
quoted quote article interview post""".split())   # words of the reporting, not of the claim


def plain(text: str) -> str:
    t = unicodedata.normalize("NFD", str(text or "")).encode("ascii", "ignore").decode().lower()
    return t.replace("’", "'")


def tokens(text: str) -> list:
    out = []
    for w in re.findall(r"[a-z][a-z0-9]+", plain(text)):
        if len(w) < 3 or w in STOP:
            continue
        stem = w[:-1] if len(w) > 4 and w.endswith("s") and not w.endswith("ss") else w   # buses -> buse is fine: both forms meet
        out.append((stem, w))
    return out


def similar(claims: list) -> dict:
    """{claim id: [{"id", "score", "terms"}]} for claims given as dicts with id, title, claim, quote."""
    docs, shown = {}, {}
    for c in claims:
        toks = tokens(" ".join([c.get("title", ""), c.get("claim", ""), c.get("quote", "")]))
        docs[c["id"]] = Counter(s for s, _ in toks)
        for s, w in toks:
            shown.setdefault(s, Counter())[w] += 1
    n = len(docs)
    df = Counter(s for d in docs.values() for s in d)
    vec = {}
    for cid, d in docs.items():
        v = {s: (1 + math.log(tf)) * math.log((1 + n) / (1 + df[s])) for s, tf in d.items() if df[s] > 1}   # a word in one claim only links nothing
        norm = math.sqrt(sum(x * x for x in v.values())) or 1
        vec[cid] = {s: x / norm for s, x in v.items()}
    ids = sorted(vec)
    pairs = {cid: [] for cid in ids}
    for i, a in enumerate(ids):
        va = vec[a]
        for b in ids[i + 1:]:
            vb = vec[b]
            shared = [(va[s] * vb[s], s) for s in va.keys() & vb.keys()]
            score = sum(x for x, _ in shared)
            if score < THRESHOLD or len(shared) < MIN_SHARED:
                continue
            terms = [shown[s].most_common(1)[0][0] for _, s in sorted(shared, reverse=True)[:3]]
            pairs[a].append({"id": b, "score": round(score, 2), "terms": terms})
            pairs[b].append({"id": a, "score": round(score, 2), "terms": terms})
    return {cid: sorted(p, key=lambda x: (-x["score"], x["id"]))[:TOP] for cid, p in pairs.items() if p}
