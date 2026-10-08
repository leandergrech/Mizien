"""Toy pre-check: given the wording of a new claim, list what the prototype ledger already holds (brainstorm only).

No language model: a small vocabulary maps words to concepts, numbers are compared with fact values, and the
direction (rise or fall) must agree. Every match is shown with the fact, the reports that used it and their ratings.

    python sketch/fact-ledger/precheck.py "Malta has almost halved emissions per person since 2005."

Run build.py first (it writes graph.json). With no argument it runs the four test sentences and writes precheck.json.
"""
import json, pathlib, re, sys

HERE = pathlib.Path(__file__).resolve().parent
G = json.load(open(HERE / "graph.json", encoding="utf-8"))

VOCAB = {
    "per-person": ["per person", "per capita", "per head", "each resident"],
    "intensity": ["intensity", "intensive", "per euro", "per unit of gdp", "gdp", "economy"],
    "air": ["flight", "aviation", "air transport", "airline", "aircraft", "planes"],
    "transport": ["transport", "cars", "traffic", "road", "buses", "vehicles"],
    "effort-sharing": ["effort sharing", "effort-sharing", "must cut", "binding", "2030"],
    "renewables": ["renewable", "solar", "wind"],
    "population": ["population", "residents"],
    "gozo": ["gozo"],
}
WORD_NUMBERS = {"halved": -50, "half": 50, "tripled": 200, "triple": 200, "doubled": 100, "double": 100, "a quarter": 25, "a third": 33}
RISE = ["rise", "rose", "increase", "grew", "tripled", "doubled", "soared", "highest", "worst", "more"]
FALL = ["fall", "fell", "cut", "down", "reduced", "decrease", "halved", "lower", "less", "cleaner"]


def concepts(text):
    t = text.lower()
    return {c for c, ws in VOCAB.items() if any(w in t for w in ws)}


def direction(text):
    t = " " + text.lower() + " "
    r = any(re.search(rf"\b{w}", t) for w in RISE)
    f = any(re.search(rf"\b{w}", t) for w in FALL)
    return "rise" if r and not f else "fall" if f and not r else None


def numbers(text):
    t = text.lower()
    out = [float(x) for x in re.findall(r"(\d+(?:\.\d+)?)\s*(?:%|per ?cent)", t)]
    out += [v for w, v in WORD_NUMBERS.items() if w in t]
    return out


SER = {s["id"]: s for s in G["series"]}
SUB = {s["id"]: (c, s) for c in G["claims"] for s in c["subclaims"]}
CLAIM = {c["id"]: c for c in G["claims"]}


def fact_concepts(f):
    s = SER[f["series"]]
    text = " ".join([f["statement"], f["measure"], s["label"], s["measure"], s["basis"]])
    c = concepts(text)
    if s["basis"] == "effort-sharing":
        c.add("effort-sharing")
    if s["basis"] == "residence" or "air" in f["measure"]:
        c.add("air")
    return c


def run(text):
    want, nums, d = concepts(text), numbers(text), direction(text)
    scored = []
    for f in G["facts"]:
        v = float(f["value"])
        fc = fact_concepts(f)
        score = 2 * len(want & fc)
        why = sorted(want & fc)
        loose = re.search(r"\b(almost|nearly|about|around|roughly|over|more than)\b", text.lower())
        if f["unit"] == "%" and nums and want & fc:
            if any(abs(abs(v) - abs(n)) <= max(3, (0.2 if loose else 0.12) * abs(n)) for n in nums):
                score += 3
                why.append("number")
        if d and f["unit"] == "%" and "change" in f["measure"]:
            if (d == "rise") == (v > 0):
                score += 1
            else:
                score -= 2
        since = re.search(r"since (\d{4})", text.lower())
        span = 10 if re.search(r"ten years|decade", text.lower()) else None
        a, _, b = f["period"].partition("-")
        if since and a == since.group(1):
            score += 1
            why.append("period")
        if span and b and int(b) - int(a) == span:
            score += 1
            why.append("period")
        if "emission" in text.lower() and f["series"].startswith(("S-GHG", "S-AIR", "S-INT", "S-ESR", "S-TRA")):
            score += 1
        if score >= 4:
            scored.append((score, f, why))
    scored.sort(key=lambda x: -x[0])
    top = [x for x in scored[:5] if x[0] >= scored[0][0] - 2] if scored else []
    bases = sorted({SER[f["series"]]["basis"] for _, f, _ in top} - {"context"})
    prior = {}
    for _, f, _ in top:
        for l in G["links"]:
            if l["fact"] == f["id"] and l["subclaim"] in SUB:
                c, s = SUB[l["subclaim"]]
                prior.setdefault(s["id"], {"claim": c["id"], "speaker": c["speaker"], "verdict": c["verdict"],
                                           "subclaim": s["text"], "rating": s["rating"], "tone": s["tone"], "via": []})["via"].append(f["id"])
    top_ids = {f["id"] for _, f, _ in top}
    FACT = {f["id"]: f for f in G["facts"]}
    counterparts = []
    for p in prior.values():
        sub = next(k for k, (c, s) in SUB.items() if s["text"] == p["subclaim"])
        for l in G["links"]:
            if l["subclaim"] == sub and l["fact"] not in top_ids and l["role"] in ("contradicts", "context"):
                g = FACT[l["fact"]]
                gb = SER[g["series"]]["basis"]
                if gb not in bases and gb != "context" and g["id"] not in [c["id"] for c in counterparts]:
                    counterparts.append({"id": g["id"], "statement": g["statement"], "basis": gb, "via": sub})
    close = [c for c in counterparts if want & fact_concepts(FACT[c["id"]])]
    counterparts = (close or counterparts)[:2]
    flags = [t for t in G["tensions"] if any(t["a"] == f["id"] or t["b"] == f["id"] for _, f, _ in top)]
    notes = []
    if len(bases) > 1:
        notes.append("The matching facts sit on more than one basis (" + ", ".join(bases) + "). Ask which one the claim means before checking it.")
    if "per-person" in want:
        notes.append("A per-person figure: population grew 40.9% over 2005-2024 (F06), which explains about half of the per-person fall (F07).")
    if any(f["id"] in ("F08", "F09") for _, f, _ in top):
        notes.append("Intensity per euro of GDP differs by price basis: -72.2% in volumes, -83.8% at current prices (F08, F09).")
    return {"text": text, "concepts": sorted(want), "numbers": nums, "direction": d,
            "facts": [{"id": f["id"], "score": s, "why": w, "statement": f["statement"], "value": f["value"], "unit": f["unit"],
                       "period": f["period"], "basis": SER[f["series"]]["basis"]} for s, f, w in top],
            "prior": list(prior.values()), "counterparts": counterparts, "flags": flags, "notes": notes}


EXAMPLES = [
    "Malta has almost halved its emissions per person since 2005.",
    "Because of flights, Malta's emissions nearly tripled in ten years.",
    "Transport makes up half of the emissions Malta must cut by 2030.",
    "Malta's economy is now 80% less carbon intensive than in 2005.",
]

if __name__ == "__main__":
    texts = sys.argv[1:] or EXAMPLES
    results = [run(t) for t in texts]
    json.dump(results, open(HERE / "precheck.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    for r in results:
        print("\n»", r["text"], "| concepts:", r["concepts"], "| numbers:", r["numbers"], "| direction:", r["direction"])
        for f in r["facts"]:
            print(f"   {f['id']} ({f['score']}) {f['basis']:>14}  {f['statement'][:80]}  [{', '.join(f['why'])}]")
        for p in r["prior"]:
            print(f"   earlier: {p['claim']} {p['speaker'][:30]} — {p['subclaim'][:50]} → {p['rating']}")
        for c in r["counterparts"]:
            print(f"   other basis: {c['id']} {c['basis']}: {c['statement'][:70]} (from {c['via']})")
        for n in r["notes"]:
            print("   note:", n)
        for t in r["flags"]:
            print("   flag:", t["a"], t["b"], t["status"])
