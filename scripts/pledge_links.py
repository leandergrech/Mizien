#!/usr/bin/env python3
"""Candidate links between manifesto pledges of different elections (data/manifesto_pledges.csv), for review.

For each pledge, the best candidates in the other election, so that a person can decide which earlier pledge a later
one carries forward (`follows`) and which earlier pledges have no follow-up. Nothing here is a link: the output is a
review list (data/review/pledge_link_candidates.csv), and a link goes into `follows` only when the maintainer
confirms it (methodology/verdict-scale.md: similar wording found automatically is never shown as a link).

Score of a candidate, about 0 to 1.4:
  text      TF-IDF cosine of the two pledges, with the tokens of scripts/similarity.py less PLEDGE_STOP (timing and
            process words such as 'next legislature', 'complete'), on our summary and target; plus, each at half
            weight, adjacent word pairs ('national park'), the section heading and CONCEPTS: synonym groups, so that
            'solar', 'PV' and 'photovoltaic', or 'offshore', 'floating' and 'deep-sea', count as the same idea. Plain
            TF-IDF gives pledges that say the same thing in other words a low score (the offshore-wind pair 2026 16.1 /
            2022 397: 0.16 by the maintainer's count, 0.24 with the site's tokens).
  numbers   shared quantities (300MW, 100,000, 30%): +0.10 each; shared years (2030, 2050): +0.04 each; at most 0.20.
  topic     same subtopic +0.08, else same topic +0.04 (the topic and subtopic columns, scripts/pledge_topics.py).
  party     same party +0.10.
Ranking (the maintainer's rule: same party first, then same topic): candidates of the same party that score at least
FLOOR come first, then other parties, each by score. The same topic and subtopic raise the score rather than forming a
group of their own, because topics are set by keyword rules and can differ for the same pledge. The best candidate
from another party is added as rank "x" when it scores at least CROSS and is not already listed (one party taking up
another's earlier pledge: ADPD 2022 and Labour 2026 on Manoel Island). Strength: strong >= 0.55, possible >= 0.35,
else weak.

Run from the repository root:
    python scripts/pledge_links.py              # write data/review/pledge_link_candidates.csv and print a summary
    python scripts/pledge_links.py --evaluate   # rank of each pair in data/review/pledge_link_benchmark.csv, against
                                                # plain TF-IDF; the maintainer's confirmed link must come first
"""
import argparse
import csv
import math
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import pledges  # noqa: E402
import similarity  # noqa: E402  (the site's own TF-IDF tokens)

OUT = ROOT / "data" / "review" / "pledge_link_candidates.csv"
BENCH = ROOT / "data" / "review" / "pledge_link_benchmark.csv"
STRONG, POSSIBLE = 0.55, 0.35
TOP, FLOOR, CROSS = 3, 0.15, POSSIBLE
W_SECTION, W_CONCEPT, W_PAIR, W_PARTY, W_SUB, W_TOPIC = 0.5, 0.5, 0.5, 0.10, 0.08, 0.04
# Words of the pledge form, not of its subject (timing, process verbs): left out on top of similarity.STOP.
PLEDGE_STOP = set("""next legislature coming years months phase complete continue continued start started launch work
introduce create strengthen support invest investment carry ensure keep give set draw plan programme scheme schemes
national public project projects pilot further more help including reports report commits aim also already""".split())
W_QTY, W_YEAR, NUM_CAP = 0.10, 0.04, 0.20

# Synonym groups: a pledge that names any of the words also carries the concept token, so that two pledges using
# different words for the same thing meet. Kept to things manifestos name in different words.
CONCEPTS = {
    "solar": r"solar|\bPV\b|photovoltaic",
    "wind": r"\bwind\b|turbines?",
    "offshore": r"offshore|floating|deep-sea|sea-surface|at sea\b|in maltese waters",
    "interconnector": r"interconnector|electricity (?:link|connection)|undersea cables?|connection with (?:mainland )?europe",
    "storage": r"batter(?:y|ies)|energy storage|storage",
    "distribution": r"distribution (?:network|centre|centres|system|link)|substations?|feeders|transformers",
    "hydrogen": r"hydrogen",
    "gas": r"\bgas\b(?! emissions)|pipeline|Electrogas|LNG",
    "bills": r"\bbills?\b|tariffs?|energy prices|price stability|subsid|meter rent|\brates?\b",
    "trees": r"\btrees?\b|afforest|woodland|seedlings|planting",
    "park": r"\bparks?\b(?![- ]and[- ]ride)|gardens?\b|open spaces?|green spaces?|green areas?",
    "trail": r"trails?\b|footpaths?|walking (?:paths|routes)|hiking|trekking",
    "valley": r"valleys?\b|\bwied\b",
    "desal": r"reverse osmosis|desalination",
    "reservoir": r"reservoirs?|rainwater|water storage|water catchment",
    "sewage": r"sewage|sewerage|wastewater|effluent",
    "wte": r"waste-to-energy|incinerat|Ecohive",
    "bulky": r"bulky[- ]waste|civic amenity",
    "recycling": r"(?<!non-)recycl|separation|refund scheme|return machines",
    "plastic": r"single-use|plastic|packaging",
    "hunting": r"\bhunt\w*|trapp\w*|turtle dove|finch",
    "mpa": r"marine protected|protected marine|marine park",
    "fishfarm": r"fish[- ]farms?",
    "natura": r"Natura 2000",
    "odz": r"\bODZ\b|outside[- ](?:the[- ])?development[- ]zones?|rationali[sz]ation",
    "height": r"high-rise|building heights?|height limits|floors\b|storeys",
    "localplan": r"local plans?|masterplans?",
    "regulator": r"Environment and Resources Authority|\bERA\b|regulators?|Planning Authority",
    "boards": r"\bboards?\b",
    "neutral": r"climate[- ]neutral|net[- ]zero|zero[- ]carbon|carbon[- ]neutral",
    "airquality": r"air[- ]quality|air pollution",
    "shoreside": r"shore-to-ship|grid electricity to parked|ships at the Grand Harbour",
    "animals": r"\banimals?\b|\bpets?\b|\bdogs?\b|\bcats?\b|\bstray|neuter|veterinar|sanctuar",
    "efficiency": r"insulat\w*|energy[- ]efficien\w*|heat[- ]pump|energy performance",
}
QTY = re.compile(r"(\d{1,3}(?:,\d{3})+|\d+(?:\.\d+)?)\s*(%|per ?cent|mw|gw|kw|m2|km2?|million|billion|units|trees|tonnes|hectares|tomna)?", re.I)


def words(text: str, pairs: bool = False, stop: bool = True) -> Counter:
    """Stems of the subject words; with pairs, also adjacent pairs ('national park', 'offshore wind') at W_PAIR.
    stop=False keeps the pledge-form words (plain TF-IDF, for comparison)."""
    stems = [s for s, w in similarity.tokens(text) if not stop or (w not in PLEDGE_STOP and s not in PLEDGE_STOP)]
    out = Counter(stems)
    if pairs:
        for a, b in zip(stems, stems[1:]):
            out[a + "_" + b] += W_PAIR
    return out


def concepts(text: str) -> Counter:
    return Counter({"~" + k: 1 for k, rx in CONCEPTS.items() if re.search(rx, text or "", re.I)})


def numbers(row: dict) -> set:
    """Quantities and years in the summary and target: {'q:300mw', 'q:100000', 'y:2030', ...}. Bare small numbers
    without a unit (item numbers, 'two') are left out."""
    out = set()
    for m in QTY.finditer(f"{row.get('summary', '')} {row.get('target', '')}"):
        n, unit = m.group(1).replace(",", ""), (m.group(2) or "").lower().replace(" ", "").replace("percent", "%").replace("per cent", "%")
        if re.fullmatch(r"(19|20)\d\d", n) and not unit:
            out.add("y:" + n)
        elif unit or float(n) >= 100:
            out.add(f"q:{float(n):g}{unit}")
    return out


def vectors(rows: list, section: bool = True, concept: bool = True, stop: bool = True) -> dict:
    """TF-IDF vectors {id: {token: weight}}, unit length."""
    docs = {}
    for r in rows:
        tf = words(f"{r.get('summary', '')} {r.get('target', '')}", pairs=concept, stop=stop)
        if concept:
            for t in concepts(r.get("summary", "")):
                tf[t] += W_CONCEPT
        if section:
            sec = re.sub(r"\s*\(chapter[^)]*\)", "", r.get("section", ""))
            for t, c in words(sec).items():
                tf["§" + t] += c * W_SECTION   # heading words kept apart from summary words: half weight
        docs[r["id"]] = tf
    n = len(docs)
    df = Counter(t for d in docs.values() for t in d)
    out = {}
    for mid, d in docs.items():
        v = {t: ((1 + math.log(c)) if c >= 1 else c) * math.log((1 + n) / (1 + df[t])) for t, c in d.items() if df[t] > 1}
        norm = math.sqrt(sum(x * x for x in v.values())) or 1
        out[mid] = {t: x / norm for t, x in v.items()}
    return out


def cosine(a: dict, b: dict) -> tuple:
    shared = sorted(((a[t] * b[t], t) for t in a.keys() & b.keys()), reverse=True)
    return sum(x for x, _ in shared), [t for _, t in shared]


def label(t: str) -> str:
    return (t[1:] + " (concept)" if t.startswith("~") else "heading: " + t[1:] if t.startswith("§")
            else t.replace("_", " ") if "_" in t else t)


def score(a: dict, b: dict, va: dict, vb: dict, na: set, nb: set) -> dict:
    text, terms = cosine(va, vb)
    shared_n = sorted(na & nb)
    num = min(NUM_CAP, sum(W_YEAR if x.startswith("y:") else W_QTY for x in shared_n))
    same_party = a["party"] == b["party"]
    same_topic = bool(a.get("topic")) and a.get("topic") == b.get("topic")
    same_sub = same_topic and bool(a.get("subtopic")) and a.get("subtopic") == b.get("subtopic")
    total = text + num + (W_PARTY if same_party else 0) + (W_SUB if same_sub else W_TOPIC if same_topic else 0)
    why = []
    if terms:
        why.append("shared: " + ", ".join(label(t) for t in terms[:5]))
    if shared_n:
        why.append("same figures: " + ", ".join(x[2:] for x in shared_n))
    why.append(("same party" if same_party else "other party") + "; "
               + (f"same subtopic ({a['subtopic']})" if same_sub else f"same topic ({a['topic']})" if same_topic else "other topic"))
    return {"score": total, "text": text, "same_party": same_party, "same_topic": same_topic, "why": "; ".join(why)}


def tier(s: dict) -> int:
    """Same party first (when the candidate reaches FLOOR), then other parties, each by score. A better match from
    another party is still shown, as rank "x" (CROSS). The topic counts through the score only, because topics are set
    by keyword rules and can differ for the same pledge (ADPD 2026 item 9 and 2022 item 4 are word for word the same
    but filed under Renewables and under Development & construction)."""
    if s["score"] < FLOOR:
        return 2
    return 0 if s["same_party"] else 1


def candidates(rows: list, vec: dict, nums: dict) -> dict:
    """{pledge id: [(candidate id, score dict, rank label)]}: TOP by the ranking rule, plus a strong other-party one."""
    other = {}
    for r in rows:
        other.setdefault(r["cycle"], []).append(r)
    cycles = sorted(other)
    out = {}
    for a in rows:
        pool = [b for c in cycles if c != a["cycle"] for b in other[c]]
        scored = [(b["id"], score(a, b, vec[a["id"]], vec[b["id"]], nums[a["id"]], nums[b["id"]])) for b in pool]
        ranked = sorted(scored, key=lambda x: (tier(x[1]), -x[1]["score"], x[0]))
        top = [(bid, s, str(i + 1)) for i, (bid, s) in enumerate(ranked[:TOP])]
        listed = {bid for bid, _, _ in top}
        cross = max(((bid, s) for bid, s in scored if not s["same_party"] and bid not in listed), key=lambda x: x[1]["score"], default=None)
        if cross and cross[1]["score"] >= CROSS:
            top.append((cross[0], cross[1], "x"))
        out[a["id"]] = top
    return out


def strength(x: float) -> str:
    return "strong" if x >= STRONG else "possible" if x >= POSSIBLE else "weak"


def load() -> list:
    return list(pledges.load_manifesto().values())


def evaluate(rows: list) -> int:
    by = {r["id"]: r for r in rows}
    bench = list(csv.DictReader(BENCH.open(encoding="utf-8")))
    full = candidates(rows, vectors(rows), {r["id"]: numbers(r) for r in rows})
    plain_vec = vectors(rows, section=False, concept=False, stop=False)   # plain TF-IDF: the site's tokens only
    print(f"{len(bench)} pairs in {BENCH.relative_to(ROOT)} (later pledge -> earlier pledge)\n")
    print(f"  {'pair':<52} {'plain TF-IDF':>13} {'score':>6}  rank later->earlier, earlier->later")
    res = {}
    for p in bench:
        a, e = p["pledge"], p["earlier"]
        plain = cosine(plain_vec[a], plain_vec[e])[0]
        fwd = next((rk for bid, _, rk in full[a] if bid == e), "-")
        back = next((rk for bid, _, rk in full[e] if bid == a), "-")
        sc = next((s["score"] for bid, s, _ in full[a] if bid == e), None)
        # rank by plain TF-IDF among the same candidates (all of the other election)
        pool = [r["id"] for r in rows if r["cycle"] != by[a]["cycle"]]
        plain_rank = 1 + sum(1 for bid in pool if cosine(plain_vec[a], plain_vec[bid])[0] > plain)
        res.setdefault(p["basis"], []).append((fwd, back, plain_rank))
        print(f"  {a + ' -> ' + e:<52} {plain:>6.2f} (#{plain_rank:<3}) {sc if sc is None else round(sc, 2)!s:>6}  {fwd:>2}, {back:>2}   {p['basis']}")
    print("\n  basis       pairs  found 1st  in top 3   (both directions)   plain TF-IDF: 1st, top 3")
    for basis, xs in res.items():
        n = len(xs)
        first = sum(f == "1" for f, _, _ in xs)
        top3 = sum(f in ("1", "2", "3", "x") for f, _, _ in xs)
        both = sum(f in ("1", "2", "3", "x") and b in ("1", "2", "3", "x") for f, b, _ in xs)
        print(f"  {basis:<11} {n:>5}  {first:>9}  {top3:>8}   {both:>8}            {sum(pr == 1 for *_, pr in xs):>4}, {sum(pr <= 3 for *_, pr in xs):>4}")
    known = [x for x in bench if x["basis"] == "maintainer"]
    ok = all(next((rk for bid, _, rk in full[k["pledge"]] if bid == k["earlier"]), "-") == "1" for k in known)
    print("\nMaintainer-confirmed links ranked first: " + ("yes" if ok else "NO"))
    return 0 if ok else 1


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--evaluate", action="store_true", help="rank the pairs in data/review/pledge_link_benchmark.csv")
    a = ap.parse_args(argv)
    rows = load()
    if a.evaluate:
        return evaluate(rows)
    by = {r["id"]: r for r in rows}
    cand = candidates(rows, vectors(rows), {r["id"]: numbers(r) for r in rows})
    party = {(c["cycle"], c["party"]): c["party_name"] for c in pledges.load_coverage().values()}
    fields = ["pledge", "party", "election", "pledge_summary", "rank", "candidate", "candidate_party", "candidate_election",
              "candidate_summary", "score", "strength", "text_similarity", "why", "decision"]
    OUT.parent.mkdir(parents=True, exist_ok=True)
    n_rows, bands = 0, Counter()
    with OUT.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for r in sorted(rows, key=lambda r: (r["cycle"], r["party"], r["id"])):
            for bid, s, rk in cand[r["id"]]:
                b = by[bid]
                w.writerow({"pledge": r["id"], "party": r["party"], "election": r["cycle"], "pledge_summary": r["summary"],
                            "rank": rk, "candidate": bid, "candidate_party": b["party"], "candidate_election": b["cycle"],
                            "candidate_summary": b["summary"], "score": f"{s['score']:.2f}", "strength": strength(s["score"]),
                            "text_similarity": f"{s['text']:.2f}", "why": s["why"], "decision": ""})
                n_rows += 1
                if rk == "1":
                    bands[strength(s["score"])] += 1
    print(f"Wrote {OUT.relative_to(ROOT)}: {n_rows} rows for {len(rows)} pledges (top {TOP}, plus the best other-party "
          f"candidate where it is at least possible). Best candidate per pledge: " + ", ".join(f"{k} {bands[k]}" for k in ("strong", "possible", "weak")) + ".")
    print("Fill `decision` (yes / no) for the pairs to link; nothing goes into `follows` until then.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
