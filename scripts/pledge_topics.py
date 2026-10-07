#!/usr/bin/env python3
"""Topic and subtopic for the manifesto list (data/manifesto_pledges.csv), by keyword rules.

The vocabulary is the site's own: the topics (`category`) and subtopics used in the claim records, so a pledge sits
in the same place as the claims on the same subject. A pledge gets the topic of what it is about, not
"Governance & Promises / Manifestos & pledges" (every row is a pledge; that subtopic is for claims about pledges).

How a row is placed:
  1. A row checked as a claim (`claim` column) takes that claim's topic and subtopic, unless the claim is filed under
     Governance & Promises (pledge claims are), in which case the rules decide.
  2. Otherwise each rule below is a regular expression with the topic and subtopic it points to. Rules are matched
     against the English `summary`: a rule that matches counts 1, plus 0.5 for each further match (at most 2), times
     its weight if it is marked as a weak signal; a rule for the topic alone (generic words such as "water" or "energy") counts half. Rules are also matched
     against the `section` heading without the chapter name in brackets (0.75 each: the programme's own grouping helps,
     but the pledge's own words decide; a heading votes once per topic). The topic named first in the summary gets 0.25, which settles near-ties in
     favour of the pledge's main subject. A topic's score is the sum of its rules; the highest topic wins, then the
     highest subtopic inside it (summary first, the section counting half). Phrases that protect land from development
     ("instead of development", "outside the development zone") do not count as development.
  3. Some subjects have no subtopic yet (THEMES with subtopic ""): the row gets the topic and an empty subtopic, and is
     listed for a decision. Some have no topic at all (topic None, e.g. animal welfare): the row stays unassigned and
     is listed with the theme, so the maintainer can decide whether to add a topic or subtopic.
  4. A row with no rule matching is unassigned and listed.

Run from the repository root:
    python scripts/pledge_topics.py             # report only: counts, unassigned rows, rows without a subtopic,
                                                # close calls, and rows where the rules differ from the file
    python scripts/pledge_topics.py --write     # also fill empty topic/subtopic cells (never overwrites a value)
    python scripts/pledge_topics.py --write --force   # recompute every row from the rules (overwrites hand edits)

A value set by hand is kept by --write, so a person can correct a row in the CSV and the next run leaves it alone.
"""
import argparse
import csv
import re
import sys
import unicodedata
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import pledges  # noqa: E402  (the topic vocabulary, shared with the checks)
CSV = ROOT / "data" / "manifesto_pledges.csv"
AFTER = "section"   # the new columns go after this one

CE, TR, WA, PH, LT, TP, NW, AI, WS, GP, HS, NO = ("Climate & Energy", "Transport", "Water", "Planning & Housing",
                                                   "Land & Trees", "Tourism & Population", "Nature & Wildlife", "Air",
                                                   "Waste", "Governance & Promises", "Health & Safety", "Noise")
# Subjects with no subtopic (or no topic) in the claims yet: (topic or None, theme label). Rows placed here are listed.
THEMES = {
    "energy efficiency": CE, "climate adaptation": CE, "biodiversity on land": NW, "litter and cleanliness": WS,
    "local councils": GP, "animal welfare": None,
}

# (topic, subtopic or "" for the topic alone, or a THEMES label, pattern[, weight]) on the English summary,
# case-insensitive. The optional weight (default 1) marks a weak signal.
SUMMARY_RULES = [
    # Climate & Energy
    (CE, "Emissions & targets", r"climate[- ]neutral|net[- ]zero|zero[- ]carbon|carbon[- ]neutral"),
    (CE, "Emissions & targets", r"\bemission|greenhouse|low[- ]carbon"),
    (CE, "Emissions & targets", r"decarboni[sz]"),
    (CE, "Emissions & targets", r"climate[- ](?:change |action |related\)? )?(?:plan|strategy|authority|agency|target|polic|initiative|goal|education|fund)"),
    (CE, "Electricity & grid", r"interconnector|electricity (?:link|connection)|undersea cables?"),
    (CE, "Electricity & grid", r"\bgrid\b|distribution (?:network|centre|system|link)|substation|feeders|transformers|low-voltage network|network monitoring"),
    (CE, "Electricity & grid", r"blackout|power cuts?|interruption|low[- ]voltage|poor voltage"),
    (CE, "Electricity & grid", r"\bbills?\b|tariff|meter|subsid|energy (?:prices?|contracts?)|price stability|charging rate|eco-reduction"),
    (CE, "Electricity & grid", r"Enemalta|Electrogas|hydrogen-ready|gas pipeline|pipeline|(?<!greenhouse )\bgas\b|energy (?:sovereignty|security|autonomy)|secure(?:s)? supply|supply security|transmission|electricity (?:markets?|generation)"),
    (CE, "Electricity & grid", r"battery|batteries|energy storage|storage of energy"),
    (CE, "Renewables", r"renewabl|clean[- ]energy|clean sources|cleaner energy"),
    (CE, "Renewables", r"\bsolar\b|\bPV\b|photovoltaic"),
    (CE, "Renewables", r"\bwind\b|wave[- ](?:energy|farm)|geothermal|biogas|biodiesel|methane"),
    (CE, "Renewables", r"\bhydrogen\b(?!-ready)"),
    (CE, "Renewables", r"feed-in|energy[- ]sharing|community energy|energy cooperatives"),
    (CE, "", r"\benergy\b|\belectricity\b|\bclimate\b"),
    (CE, "energy efficiency", r"insulat|energy[- ](?:efficien|performance|audit|use intensity)|heat[- ]pump|passive|double glazing|air conditioners|retrofit|EPC\b|sustainab\w+ upgrades|sustainable (?:new )?(?:and renovated )?buildings|building sustainably|Irrinova"),
    (CE, "climate adaptation", r"\badapt(?:ation)?\b|climate[- ]vulnerable|resilient infrastructure|prepar\w+ (?:the economy )?for climate change|coastal protection|erosion"),
    # Transport
    (TR, "Cars & traffic", r"\bcars?\b|traffic|electric[- ]vehicle|\bEVs?\b|electric or hybrid|vehicles?\b|park[- ]and[- ]ride"),
    (TR, "Cars & traffic", r"mobility|\btravel\b|heavy goods|logistics"),
    (TR, "Public transport", r"\bbus(?:es)?\b|public transport"),
    (TR, "Roads & mass transit", r"\broads?\b|road maintenance|metro|mass transit"),
    (TR, "Ferries & Gozo links", r"\bferr(?:y|ies)\b|Gozo Channel"),
    # Water
    (WA, "Bathing water & sewage", r"sewage|sewerage|wastewater|effluent"),
    (WA, "Bathing water & sewage", r"bathing|swimming zones?|swimmers|Blue Flag|\bbeach(?:es)?\b(?! concessions)"),
    (WA, "Water supply & groundwater", r"reverse osmosis|desalination|brine"),
    (WA, "Water supply & groundwater", r"reservoirs?|groundwater|aquifer|underground water"),
    (WA, "Water supply & groundwater", r"rainwater|rain water|water catchment|water[- ]storage|collect water|water tanks"),
    (WA, "Water supply & groundwater", r"tap[- ]?water|potable|drinking[- ]water|water (?:conservation|consumption|production|distribution|management|supply|shortages?|dispensers|filters)|grey[- ]?water"),
    (WA, "Flood relief", r"flood|storm ?water"),
    (WA, "", r"\bwater\b"),
    # Planning & Housing
    (PH, "Housing & affordability", r"\bhousing\b|\brent(?:al|ed|als)?\b|landlords?|rented"),
    (PH, "Permits & enforcement", r"\bpermits?\b|permitting|\bappeals?\b|tribunal|Planning Authority"),
    (PH, "Permits & enforcement", r"illegal(?:ly built| develop\w*| ODZ| structures| buildings)|sanction|enforcement notices?|Environmental Protection Unit"),
    (PH, "Permits & enforcement", r"enforce", 0.5),     # enforcement is promised on every subject: a weak signal
    (PH, "Development & construction", r"construction|\bdevelop(?:ment|ments|ers?|ed)\b(?![- ]zones?)|building projects?|excavation|demolition"),
    (PH, "Development & construction", r"high[- ]rise|building heights?|height limits|ten or more floors|floors\b|storeys"),
    (PH, "Development & construction", r"local plans?|masterplan|planning (?:law|strategy|framework|reform|policy|decisions|criteria)|national planning|land[- ]use"),
    (PH, "Development & construction", r"building codes?|contractors?|Building and Construction Authority|marina|race track|motor-racing|land reclamation|expropriation|blocks? of flats"),
    (PH, "Heritage & character", r"heritage|UNESCO|scheduled|Grade [12]|urban conservation|\bUCAs?\b|village cores?|old village|historic|walled cities|aesthetic|skyline|design styles?|conservation of buildings|landscape|restor\w+ (?:fort|the lazzaretto)"),
    # Land & Trees
    (LT, "Open spaces & parks", r"\bparks?\b(?![- ]and[- ]ride)|Manoel Island"),
    (LT, "Open spaces & parks", r"national park|natur(?:e|al) park|eco-parks|regenerat"),
    (LT, "Open spaces & parks", r"gardens?\b|open spaces?|green spaces?|green areas?|green lungs|green networks?|green[- ]infrastructure|greening|green cities|pocket parks|\bsquares?\b(?! metres)|pedestrian"),
    (LT, "Open spaces & parks", r"trails?\b|walking|footpaths?|\bpaths?\b|trekking|hiking|running tracks|cycling track"),
    (LT, "Open spaces & parks", r"picnic|camping|caravanning|recreation|family spaces?|countryside access|access to the countryside|countryside paths|country pathways|rural (?:areas|places)"),
    (LT, "Trees & planting", r"\btrees?\b|afforest|woodlands?|seedlings|shrubs|planting"),
    (LT, "Land take & agriculture", r"\bODZ\b|outside[- ](?:the[- ])?development[- ]zones?"),
    (LT, "Land take & agriculture", r"rationali[sz]ation|land take|no-net land"),
    (LT, "Land take & agriculture", r"\bfarm(?:ers?|land|ing)?\b|agricultur|herders|livestock|\bproduce\b|Pitkalija|abattoir"),
    (LT, "Land take & agriculture", r"public land|agricultural land|private countryside"),
    # Tourism & Population
    (TP, "Tourism numbers & capacity", r"touris|carrying[- ]capacity|\bhotels?\b|tour operators"),
    (TP, "Short lets & concessions", r"concession|public domain|coastline|shoreline|coastal access|access to the shoreline|commerciali[sz]ation|private (?:pools|development)"),
    (TP, "Population & labour", r"population|foreign workers"),
    # Nature & Wildlife
    (NW, "Hunting & birds", r"\bhunt|\btrap(?:ping|pers)?\b|turtle dove|finch|\bbirds?\b|bird-ringing|birdwatch"),
    (NW, "Marine protection", r"\bmarine\b|seagrass|Posidonia|sea-?bed|under ?water|the sea\b|at sea\b"),
    (NW, "Marine protection", r"\bfish(?:ing|ers|eries)?\b|fish[- ]farms?|trawling|lampuki|tuna|fishing-net"),
    (NW, "Marine protection", r"moorings?|anchor|berthing|diving"),
    (NW, "Dark skies", r"light pollution|artificial lighting"),
    (NW, "biodiversity on land", r"biodiversity|habitats?|species|ecological|ecosystems?|Natura 2000|pollinators?|flora|fauna|invasive|valleys?\b|genetic|rubble walls|garrigue|nature network|natural (?:areas|state)|wild rabbit|barn owl|conservation(?! areas)"),
    # Air
    (AI, "Air quality & health", r"air[- ]quality|air pollution|pollution from|emission filters?|\bdust\b|Air Quality Index"),
    (AI, "Port & power emissions", r"shore[- ]to[- ]ship|\bships?\b|aircraft|aviation|\bairport\b|power station"),
    # Waste
    (WS, "Recycling & separation", r"(?<!non-)recycl|separat|\breuse|repair|refill|refund scheme|return machines|deposit"),
    (WS, "Recycling & separation", r"single[- ]use|plastic|packaging|containers?|circular economy|organic[- ]waste|food waste|compost|anaerobic|digesters|zero[- ]waste|waste minimi[sz]ation|waste[- ]reduction|cut(?:ting)? (?:the )?waste|reduce waste"),
    (WS, "Construction waste", r"construction (?:and demolition )?waste|construction materials|building materials|excavation[- ]waste|dismantl\w* (?:rather|buildings)|dismantled rather|virgin stone|disposing of construction|quarr\w+ for (?:dispos|construction)"),
    (WS, "Landfill & treatment", r"landfill|incinerat|waste[- ]to[- ]energy|Ecohive|EcoHive|bulky[- ]waste|civic amenity|skips?\b|waste (?:plant|mining|treatment)|WasteServ"),
    (WS, "", r"\bwaste\b"),
    (WS, "litter and cleanliness", r"litter|cleanliness|cleaning|smart bins|refuse collection|waste collection|clean malta"),
    # Governance & Promises
    (GP, "Accountability", r"independen(?:ce|t)\b|autonomy and independence|accountab|regulators?\b|\bboards?\b|Ombudsman"),
    (GP, "Accountability", r"parliamentary (?:scrutiny|oversight|committees?|vote)|standing committees|KPIs?|performance standards|benchmarking|Guardian of Future Generations"),
    (GP, "Accountability", r"Constitution|\bNGOs?\b|transparen|conduct rules|register of their assets|environmental data|legal aid|Environment and Resources Authority|\bERA\b"),
    (GP, "local councils", r"local council (?:funding|services)|to local councils|local councils a right|consultation with local councils|revenue sharing|localities receive"),
    # Health & Safety
    (HS, "Heat & health", r"urban heat|heatwave|\bheat\b|cool (?:and white )?roofs|street shade|\bshade\b"),
    (HS, "Workplace safety", r"health and safety|collapse|injur|dangerous structures|protect workers"),
    # Noise
    (NO, "", r"\bnoise\b|nuisance|Sundays and public holidays|8am"),
    # No topic yet
    (None, "animal welfare", r"animal welfare|animal police|animal abuse|animal hospital"),
    (None, "animal welfare", r"\banimals?\b|\bpets?\b|\bdogs?\b|\bcats?\b|\bstray|neuter|sterilis|veterinar|\bvets?\b|microchip|adopt(?:ion|ing)\b|rehoming|sanctuar|equestrian|horses|cruelty"),
]

# (topic, subtopic/theme, pattern) on the section heading without its chapter, case-insensitive; each counts 1.5.
SECTION_RULES = [
    (LT, "Trees & planting", r"afforestazzjoni"),
    (None, "animal welfare", r"annimali"),
    (NW, "Hunting & birds", r"kaċċa|insib"),
    (NW, "Marine protection", r"\bsajd\b|ibħra|taħt il-baħar|marine"),
    (NW, "biodiversity on land", r"bijodiversità|biodiversity|natura\b|ambjent naturali"),
    (LT, "Land take & agriculture", r"biedja|agrikol|\bODZ\b"),
    (LT, "Open spaces & parks", r"spazji miftuħa|open spaces|\bparks?\b|green cities|jgawdi l-kampanja|aċċess għall-kampanja|widien"),
    (WS, "", r"skart|\bwaste\b"),
    (WS, "Recycling & separation", r"ċirkolari|circular"),
    (WS, "litter and cleanliness", r"ambjent nadif"),
    (WA, "", r"\bilma\b|\bwater\b"),
    (CE, "", r"enerġija|energy|dikarbonizzazzjoni"),   # not 'climate': those sections mix heat, nature and waste
    (CE, "Electricity & grid", r"elettriku|kontijiet|distribuzzjoni tal-enerġija|sigurtà tal-enerġija"),
    (CE, "Renewables", r"rinnovabbli|renewable"),
    (AI, "Air quality & health", r"arja\b|\bair\b"),
    (PH, "", r"ippjanar|planning|kostruzzjoni|construction|development|żvilupp|pjani lokali|użu tal-art|\bart,"),
    (PH, "Heritage & character", r"qalba tal-irħula|heritage"),
    (GP, "Accountability", r"bordijiet|governanza"),
    (GP, "local councils", r"kunsilli lokali"),
]
SUMMARY_W, SECTION_W, GENERIC, FIRST = 1.0, 0.75, 0.5, 0.25
# Phrases about protecting land from development: the pledge is about the land, not about building.
PROTECT = re.compile(r"\b(?:instead of|from|against|free of|no|of commercial|for commercial|sustainable|unnecessary)\s+"
                     r"(?:further |commercial |private |unnecessary |inappropriate urban |large-scale )?develop\w*", re.I)


def norm(s: str) -> str:
    """Typographic hyphens and apostrophes to plain ones, NFC (PN 2026 headings use U+2010)."""
    s = unicodedata.normalize("NFC", s or "")
    return s.replace("‐", "-").replace("‑", "-").replace("’", "'")


def section_of(row: dict) -> str:
    return re.sub(r"\s*\(chapter[^)]*\)", "", norm(row.get("section")))


def vocabulary() -> dict:
    """{topic: set of subtopics} from the claim records (the site's own topics; scripts/pledges.py)."""
    return pledges.topic_vocabulary()


def claim_topics() -> dict:
    out = {}
    for p in sorted((ROOT / "claims").glob("CC-*/claim.yml")):
        d = yaml.safe_load(p.read_text(encoding="utf-8"))
        out[d["id"]] = (d["category"], d.get("subtopic") or "")
    return out


def check_rules(vocab: dict) -> list:
    errs = []
    for topic, sub, rx, *_ in SUMMARY_RULES + SECTION_RULES:
        re.compile(rx)
        if topic is None:
            if sub not in THEMES or THEMES[sub] is not None:
                errs.append(f"rule {rx!r}: theme '{sub}' with no topic must be in THEMES with topic None")
        elif topic not in vocab:
            errs.append(f"rule {rx!r}: topic '{topic}' is not used by any claim")
        elif sub and sub not in vocab[topic] and THEMES.get(sub) != topic:
            errs.append(f"rule {rx!r}: '{sub}' is neither a subtopic of '{topic}' in the claims nor a theme of that topic")
    return errs


def score(row: dict, vocab: dict | None = None) -> tuple:
    """({topic or ('none', theme): score}, {(topic, sub): (summary score, section score)}, [why]) for one row."""
    summary, section = PROTECT.sub(" protected ", norm(row.get("summary"))), section_of(row)
    tops, subs, why, first, pos, summ, voted = {}, {}, [], {}, {}, {}, set()
    for rules, text, where in ((SUMMARY_RULES, summary, "summary"), (SECTION_RULES, section, "section")):
        for topic, sub, rx, *wt in rules:
            found = [m for m in re.finditer(rx, text, re.I)]
            if not found:
                continue
            key = topic if topic is not None else ("none", sub)
            if where == "summary":
                generic = sub == "" and (vocab is None or vocab.get(topic))   # Noise has no subtopics: not generic
                w = min(2.0, SUMMARY_W + 0.5 * (len(found) - 1)) * (GENERIC if generic else 1) * (wt[0] if wt else 1)
                summ[key] = summ.get(key, 0) + w
                first[key] = min(first.get(key, 10 ** 6), found[0].start())
                pos[(key, sub)] = min(pos.get((key, sub), 10 ** 6), found[0].start())
            else:   # a heading votes once per topic, however many of its rules match
                w = 0 if key in voted else SECTION_W
                voted.add(key)
            tops[key] = tops.get(key, 0) + w
            a, b = subs.get((key, sub), (0, 0))
            subs[(key, sub)] = (a + w, b) if where == "summary" else (a, b + SECTION_W)
            why.append(f"{where} '{found[0].group(0)}' → {topic or 'no topic'}{' / ' + sub if sub else ''}")
    if first:   # the subject named first in the summary
        lead = min(first, key=first.get)
        tops[lead] += FIRST
    return tops, subs, why, pos, summ


def assign(row: dict, vocab: dict, by_claim: dict) -> dict:
    """{topic, subtopic, theme, basis, margin, runner_up, why} for one row."""
    cid = (row.get("claim") or "").strip()
    if cid in by_claim and by_claim[cid][0] != GP:
        t, s = by_claim[cid]
        return {"topic": t, "subtopic": s, "theme": "", "basis": f"from {cid}", "margin": 99, "runner_up": "", "why": []}
    tops, subs, why, pos, summ = score(row, vocab)
    if not tops:
        return {"topic": "", "subtopic": "", "theme": "", "basis": "no rule matched", "margin": 0, "runner_up": "", "why": []}
    ranked = sorted(tops.items(), key=lambda kv: (-kv[1], -summ.get(kv[0], 0)))   # ties: more from the summary
    best, best_score = ranked[0]
    runner = ranked[1] if len(ranked) > 1 else (None, 0)
    margin = best_score - runner[1]
    label = lambda k: k[1] + " (no topic)" if isinstance(k, tuple) else k
    if isinstance(best, tuple):            # a theme with no topic (animal welfare)
        return {"topic": "", "subtopic": "", "theme": best[1], "basis": "theme with no topic", "margin": margin,
                "runner_up": label(runner[0]) if runner[0] else "", "why": why}
    inside = sorted(((s, a + 0.5 * b) for (k, s), (a, b) in subs.items() if k == best and s),
                    key=lambda kv: (-kv[1], pos.get((best, kv[0]), 10 ** 6)))   # ties: the one named first
    real = [(s, v) for s, v in inside if s in vocab.get(best, set())]
    themes = [(s, v) for s, v in inside if THEMES.get(s) == best]
    named = {s for (k, s), (a, _) in subs.items() if k == best and a > 0}   # named in the summary itself
    sub, theme = "", ""
    # An existing subtopic named in the summary wins over a theme with no subtopic (use what exists when it fits).
    if real and (not themes or real[0][1] >= themes[0][1] or real[0][0] in named):
        sub = real[0][0]
    elif themes:
        theme = themes[0][0]
    return {"topic": best, "subtopic": sub, "theme": theme, "basis": "rules", "margin": margin,
            "runner_up": label(runner[0]) if runner[0] else "", "why": why}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--write", action="store_true", help="fill empty topic/subtopic cells in data/manifesto_pledges.csv")
    ap.add_argument("--force", action="store_true", help="with --write: recompute every row, overwriting values set by hand")
    ap.add_argument("--close", type=float, default=0.5, help="list rows whose best topic leads by this much or less (default 0.5)")
    a = ap.parse_args(argv)
    vocab, by_claim = vocabulary(), claim_topics()
    errs = check_rules(vocab)
    if errs:
        print("\n".join("FAIL " + e for e in errs))
        return 1
    with CSV.open(encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        fields, rows = list(reader.fieldnames), list(reader)
    for col in ("subtopic", "topic"):
        if col not in fields:
            fields.insert(fields.index(AFTER) + 1, col)
    res = {r["id"]: assign(r, vocab, by_claim) for r in rows}

    changed, differ = 0, []
    for r in rows:
        x = res[r["id"]]
        have = ((r.get("topic") or "").strip(), (r.get("subtopic") or "").strip())
        if have != ("", "") and have != (x["topic"], x["subtopic"]):
            differ.append((r["id"], have, (x["topic"], x["subtopic"])))
        if a.write and (a.force or have == ("", "")):
            if ((r.get("topic") or ""), (r.get("subtopic") or "")) != (x["topic"], x["subtopic"]):
                changed += 1
            r["topic"], r["subtopic"] = x["topic"], x["subtopic"]
        r.setdefault("topic", ""); r.setdefault("subtopic", "")

    # Report: counts, then what needs a person.
    final = {r["id"]: (r["topic"], r["subtopic"]) if a.write else (res[r["id"]]["topic"], res[r["id"]]["subtopic"]) for r in rows}
    n = len(rows)
    print(f"{n} manifesto rows. Topics and subtopics from the claims: {len(vocab)} topics, {sum(map(len, vocab.values()))} subtopics.\n")
    counts = {}
    for t, s in final.values():
        counts[(t, s)] = counts.get((t, s), 0) + 1
    print("== placed")
    for t in sorted({t for t, _ in counts if t}):
        tot = sum(v for (tt, _), v in counts.items() if tt == t)
        print(f"  {t}: {tot}  (" + ", ".join(f"{s or 'no subtopic'} {v}" for (tt, s), v in sorted(counts.items()) if tt == t) + ")")
    by = lambda pred: [r for r in rows if pred(r)]
    loose = by(lambda r: not final[r["id"]][0])
    nosub = by(lambda r: final[r["id"]][0] and not final[r["id"]][1] and vocab.get(final[r["id"]][0]))
    print(f"\n== no topic: {len(loose)}")
    groups = {}
    for r in loose:
        groups.setdefault(res[r["id"]]["theme"] or "no rule matched", []).append(r)
    for g, rs in sorted(groups.items(), key=lambda kv: -len(kv[1])):
        print(f"  -- {g}: {len(rs)}")
        for r in rs:
            print(f"     {r['id']}: {r['summary'][:110]}")
    print(f"\n== topic but no subtopic (no existing subtopic fits): {len(nosub)}")
    groups = {}
    for r in nosub:
        groups.setdefault(f"{final[r['id']][0]}: {res[r['id']]['theme'] or 'general'}", []).append(r)
    for g, rs in sorted(groups.items(), key=lambda kv: -len(kv[1])):
        print(f"  -- {g}: {len(rs)}")
        for r in rs:
            print(f"     {r['id']}: {r['summary'][:110]}")
    close = [r for r in rows if res[r["id"]]["basis"] == "rules" and res[r["id"]]["topic"] and res[r["id"]]["margin"] <= a.close]
    print(f"\n== close calls (best topic leads by {a.close} or less; placed, worth a look): {len(close)}")
    for r in close:
        x = res[r["id"]]
        print(f"     {r['id']}: {x['topic']} / {x['subtopic'] or x['theme'] or '-'} over {x['runner_up']}  |  {r['summary'][:90]}")
    if differ:
        print(f"\n== in the file but different from the rules (kept unless --force): {len(differ)}")
        for mid, have, rule in differ:
            print(f"     {mid}: file {have[0]} / {have[1] or '-'}; rules {rule[0] or '-'} / {rule[1] or '-'}")
    if a.write:
        with CSV.open("w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=fields)
            w.writeheader()
            w.writerows(rows)
        print(f"\nWrote {CSV.relative_to(ROOT)}: {changed} rows changed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
