#!/usr/bin/env python3
"""Topic and subtopic for the manifesto list (data/manifesto_pledges.csv): the taxonomy, keyword rules, and a report.

The pledges have their own taxonomy, data/pledge_topics.csv (maintainer's request, 7 Oct 2026: organise the pledges
"in the most meaningful and semantic way, so that they fit"). It was drawn up from the 625 pledges themselves, so that
every pledge has a topic and a subtopic: 12 topics, 49 subtopics, each with a code (EN-S), a scope note saying what
belongs there, and the nearest topic and subtopic of the claims (`site_topic`, `site_subtopic`), so that pledges and
claims can still be shown together. The claims' own topics are not changed.

The topic and subtopic of each row are a person's reading of the pledge (all 625 placed by hand on 7 Oct 2026). The
keyword rules below suggest a placement for new rows (--write fills empty cells only) and check the hand placements:
the report lists every row where the rules read the pledge differently, which is where a second look is worth having.

How the rules place a row: each rule is a regular expression pointing to a subtopic code, or to a topic name for
generic words (SUBTOPIC_HINTS only choose between the subtopics of a topic already chosen). Rules are matched
against the English `summary`: a rule that matches counts 1, plus 0.5 for each
further match (at most 2), times its weight when it is marked as a weak signal; a topic-only rule counts half. Rules
are also matched against the `section` heading without the chapter name in brackets (0.75, once per topic). The
topic named first in the summary gets 0.25. A topic's score is the sum of its rules; the highest topic wins, then
the highest subtopic inside it (summary first, the heading counting half; ties go to the one named first). Phrases
that protect land from development ("instead of development") do not count as development.

Run from the repository root:
    python scripts/pledge_topics.py                   # report: the taxonomy with counts, rows the rules read
                                                      # differently, rows the rules cannot place
    python scripts/pledge_topics.py --write           # also fill empty topic/subtopic cells from the rules
    python scripts/pledge_topics.py --write --force   # recompute every row from the rules (overwrites hand placements)
"""
import argparse
import csv
import re
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import pledges  # noqa: E402  (the taxonomy, shared with the checks)
CSV = ROOT / "data" / "manifesto_pledges.csv"
AFTER = "section"   # the topic and subtopic columns go after this one

# (subtopic code or topic name, pattern[, weight]) on the English summary, case-insensitive.
SUMMARY_RULES = [
    # Climate
    ("CL-T", r"climate[- ]neutral|net[- ]zero|zero[- ]carbon|carbon[- ]neutral"),
    ("CL-T", r"\bemission|greenhouse|climate[- ](?:change |related\)? )?targets?|drastic cut"),
    ("CL-G", r"climate (?:change |action )?(?:authority|agency|plan|strategy|education|initiatives|polic)|climate-vulnerable|low-carbon transition|conference"),
    ("CL-B", r"\bcompan(?:y|ies)\b|enterprises|\bindustr(?:y|ial)\b|firms|manufactur|\bSMEs?\b|state aid|aid to (?:companies|industry)|start-ups|\bESG\b|Corporate Sustainability|tour operators|operators|Climate Action Fund|decarbonisation while"),
    ("CL-A", r"\badapt(?:ation)?\b|urban heat|cool (?:and white )?roofs|street shade|erosion|coastal protection|resilient infrastructure|preparing the economy|nature-based"),
    ("Climate", r"\bclimate\b"),
    # Energy
    ("EN-S", r"rooftop|on every (?:public |feasible )?(?:roof|building)|public (?:buildings?|roof)|schools|factories|solar water heaters?|household|homes?\b|apartment|condominium|without (?:a )?roof"),
    ("EN-S", r"community (?:projects|battery|batteries|energy)|energy[- ]sharing|share renewable|cooperatives|solar (?:canopies|car ?ports?|rights)|micro wind|batteries for|home and business batteries|\bPV\b|photovoltaic"),
    ("EN-L", r"offshore|floating|\bwave\b|solar farms?|wind farm|large-scale|\d+% of (?:electricity|its energy)|renewable sources by|feed-in|geothermal|methane|biogas|cooperation with Sicily|agricultur\w* (?:projects|and electricity)|reservoir owners"),
    ("EN-L", r"renewabl|\bsolar\b|\bwind\b", 0.5),
    ("EN-G", r"interconnector|electricity (?:link|connection)|undersea cables?|connection with mainland|distribution (?:network|centre|centres|system|link)|substations?|feeders|transformers"),
    ("EN-G", r"\bgrid\b|blackouts?|power cuts|interruptions|low[- ]voltage|poor voltage|smart meters|control room|network monitoring|energy storage|battery (?:energy )?storage|\bstorage\b"),
    ("EN-F", r"Electrogas|\bgas\b(?! emissions| price)|pipeline|hydrogen|energy contracts|clean-energy contracts|energy sovereignty|energy autonomy|secures supply|cheapest|to competition|biodiesel|store as much"),
    ("EN-B", r"tariffs?|\bbills?\b|subsid|price stability|energy prices|meter (?:rent|charges)|eco-reduction|charging rate|overcharged|rebate|decoupled"),
    ("EN-E", r"insulat|energy[- ]efficien|heat[- ]pump|passive|double glazing|air conditioners|Energy Performance|energy audits|energy use intensity|Irrinova|building sustainably|sustainable new and renovated|carbon neutral and generate|sustainability upgrades"),
    ("Energy", r"\benergy\b|\belectricity\b"),
    # Transport
    ("TR-V", r"electric[- ](?:vehicle|bus|cars?)|\bEVs?\b|electric or hybrid|bus fleet|goods vehicles|clean-fuel"),
    ("TR-C", r"park[- ]and[- ]ride|traffic|sustainable mobility|streets for people|reasonable distance|cut travel|\bcars\b|used by cars"),
    # Air & noise
    ("AN-A", r"air[- ]quality|air pollution|emission filters|Air Quality Index"),
    ("AN-S", r"shore[- ]to[- ]ship|\bships\b(?! from)|parked aircraft|aviation|Single European Sky"),
    ("AN-S", r"Grand Harbour|International Airport"),
    ("AN-N", r"\bnoise\b"),
    # Water
    ("WA-S", r"reverse osmosis|desalination|potable|tap[- ]?water|drinking[- ]water|water (?:production|distribution|dispensers|filters|fountains)|reservoirs? (?:at|works)|water tanks|blue bonds"),
    ("WA-C", r"rainwater|rain water|water (?:catchment|storage|conservation|management|consumption)|groundwater|aquifer|grey[- ]?water|effluent|collect water|harvest"),
    ("WA-W", r"(?<!treated )sewage(?! effluent)|sewerage|wastewater"),
    ("Water", r"\bwater\b"),
    # Waste
    ("WS-P", r"single[- ]use|plastic|packaging|refill|repair|\breuse\b|food waste|zero[- ]waste|circular economy|waste minimi|waste[- ]reduction|cut(?:ting)? (?:the )?waste|excess consumption|raw materials|resource-use|material efficiency|brine|waste glass"),
    ("WS-R", r"(?<!non-)recycl|separat|refund scheme|return machines|bulky[- ]waste|civic amenity|skip facility|clothes"),
    ("WS-T", r"incinerat|waste[- ]to[- ]energy|Ecohive|landfill|organic-waste plant|waste mining|waste (?:management|plan|strategy|policy)"),
    ("WS-C", r"construction (?:and demolition )?waste|construction materials|building materials|excavation[- ]waste|dismantl|demolished buildings|virgin stone|quarr\w+ for (?:dispos|construction|storage)"),
    ("WS-L", r"litter|cleanliness|cleaning|smart bins|refuse collection|Clean Malta"),
    ("Waste", r"\bwaste\b"),
    # Nature & Wildlife
    ("NW-H", r"biodiversity|habitats?|species|ecological|Natura 2000|pollinators?|flora|fauna|invasive species|valleys?\b|genetic|nature network|natural areas|(?<!marine )protected areas|conservation programmes|wild rabbit|barn owl"),
    ("NW-M", r"\bmarine\b|seagrass|Posidonia|moorings|at sea\b|maritime|coastal erosion|Hurd's Bank|berthing"),
    ("NW-F", r"\bfish(?:ing|ers|eries)?\b|fish[- ]farms?|trawling|lampuki|tuna|mrejkba|fishing-net"),
    ("NW-B", r"\bhunt\w*|\btrap(?:ping|pers)?\b|turtle dove|finch|\bbirds?\b|bird-ringing|birdwatch"),
    ("NW-D", r"light pollution|artificial lighting"),
    # Animal welfare
    ("AW-V", r"veterinar|\bvets?\b|animal hospital|ambulance|neuter|sterilis|pet insurance"),
    ("AW-S", r"sanctuar|shelters?|rehoming|re-homing|adopt(?:ion|ing)?\b|\bstray|feeders"),
    ("AW-L", r"animal welfare (?:strategy|Directorate)|Commissioner for Animal|portfolio for animal|Animal Police|animal abus|cruelty|microchip|licensing for|positive list|farm animals|animal wardens|remove animals"),
    ("AW-P", r"dog (?:parks?|swimming)|beaches for dogs|cat caf|cafés|cemeter|equestrian|responsibility towards animals"),
    ("Animal welfare", r"\banimals?\b|\bpets?\b|\bdogs?\b|\bcats?\b"),
    # Parks & trees
    ("PT-U", r"\bparks?\b(?![- ]and[- ]ride)|gardens?\b|open spaces?|green space|\bsquares?\b(?! metres)|pedestrian"),
    ("PT-G", r"every locality|per locality|every (?:town|village)|near homes|ten minutes|Parks Act|standards for parks|map of parks|greening grant|green[- ]infrastructure|green cities|façades|roof gardens|community gardens|green lungs|protected from development|urban green"),
    ("PT-N", r"national park|natur(?:e|al) park|natural (?:areas|state)|Manoel Island|White Rocks|\bWied\b|woodland|Chadwick|Inwadar|Salina|Ta.? Qali|regenerat\w+ (?:works|abandoned)"),
    ("PT-T", r"\btrees?\b|afforest|seedlings|tree-planting|planting"),
    # Countryside & coast
    ("CC-A", r"footpaths?|trails?\b|walking (?:trails|routes)|hiking|trekking|picnic|camping|caravanning|countryside|rural (?:areas|places)|country pathways"),
    ("CC-C", r"\bbeach(?:es)?\b|concessions?|public domain|coastline|shoreline|bathing bays|swimming zones|carrying-capacity|Comino"),
    ("CC-F", r"\bfarm(?:ers|ing)\b|agricultur|herders|livestock|\bproduce\b|Pitkalija|abattoir|ecological economy"),
    # Land use & planning
    ("LP-S", r"planning (?:law|reform|strategy|framework|decisions|criteria)|Planning Authority|local plans?|masterplan|Strategic Plan|land[- ]use|impact assessments?|consultation|Bills 143|White Paper|CMEPA|excessive development|commercial development|geological surveys|planning"),
    ("LP-O", r"\bODZ\b|outside[- ](?:the[- ])?development[- ]zones?|rationali[sz]ation|public land|not (?:be )?developed|undeveloped|agricultural land|race track|marina|football campus"),
    ("LP-H", r"high[- ]rise|building heights?|height limits|ten or more floors|skyline|aesthetic|design styles?|scoring system"),
    ("LP-P", r"\bpermits?\b|appeal|tribunal|illegal|sanctioning|Environmental Protection Unit"),
    ("LP-C", r"construction|building codes|contractors?|Building and Construction Authority|excavation|building works|unfinished|collapse|expropriation|block of flats|neighbours"),
    ("LP-T", r"heritage|UNESCO|scheduled|urban conservation|\bUCAs?\b|village cores?|historic|walled cities|landscape|overhead (?:service )?wires|Lazzaretto|Fort Manoel|demolition of buildings|adaptive reuse"),
    # Environmental governance
    ("EG-R", r"Environment and Resources Authority|\bERA\b|regulators?|\bboards?\b|KPIs|agencies tied"),
    ("EG-P", r"Constitution|\bNGOs?\b|Ombudsman|Guardian of Future Generations|legal aid|environmental data|Civic Service"),
    ("EG-L", r"local councils?|localities receive|revenue sharing|council funding|council services"),
    ("EG-S", r"Sustainability Agenda|environmental alliance|top priority when drafting|tax framework|serious offence|environmental impact, both"),
]

# (subtopic code, pattern): hints that choose between the subtopics of a topic already chosen, without adding to the
# topic's score (policy words such as "strategy" say which kind of parks pledge it is, not that it is about parks).
SUBTOPIC_HINTS = [
    ("PT-G", r"\b(?:policy|strategy|programme|schemes?|guarantee|law|standards|national map|investment|funds)\b|open spaces first|reintroduce nature|buy (?:land|them)|lease or buy|public land into parks"),
]

# (subtopic code or topic name, pattern) on the section heading (without its chapter), case-insensitive; 0.75 each.
SECTION_RULES = [
    ("PT-T", r"afforestazzjoni"),
    ("Animal welfare", r"annimali"),
    ("NW-B", r"kaċċa|insib"),
    ("NW-F", r"\bsajd\b"),
    ("NW-M", r"ibħra|taħt il-baħar|marine"),
    ("NW-H", r"bijodiversità|biodiversity|natura\b"),
    ("CC-F", r"biedja|agrikol"),
    ("LP-O", r"\bODZ\b"),
    ("PT-U", r"spazji miftuħa|open spaces|\bparks?\b|green cities"),
    ("CC-A", r"jgawdi l-kampanja|aċċess għall-kampanja|rikreazzjoni"),
    ("PT-N", r"widien|manoel island"),
    ("Waste", r"skart|\bwaste\b"),
    ("WS-P", r"ċirkolari|circular"),
    ("WS-L", r"ambjent nadif"),
    ("Water", r"\bilma\b|\bwater\b"),
    ("Energy", r"enerġija|energy|elettriku|dikarbonizzazzjoni"),
    ("EN-B", r"kontijiet"),
    ("EN-G", r"distribuzzjoni tal-enerġija|sigurtà tal-enerġija|provvista sigura"),
    ("EN-L", r"rinnovabbli|renewable"),
    ("CL-B", r"industrija|industrijali"),
    ("Air & noise", r"arja\b|\bair\b"),
    ("Land use & planning", r"ippjanar|planning|kostruzzjoni|construction|development|żvilupp|pjani lokali|użu tal-art|\bart,"),
    ("LP-T", r"qalba tal-irħula|heritage"),
    ("EG-R", r"bordijiet|governanza"),
    ("EG-L", r"kunsilli lokali"),
    ("Climate", r"klima|klimatika|climate"),
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


def taxonomy() -> dict:
    """{code: (topic, subtopic)} from data/pledge_topics.csv."""
    return {t["code"]: (t["topic"], t["subtopic"]) for t in pledges.load_pledge_topics()}


def check_rules(tax: dict) -> list:
    topics = {t for t, _ in tax.values()}
    errs = []
    for key, rx, *_ in SUMMARY_RULES + SECTION_RULES + SUBTOPIC_HINTS:
        re.compile(rx)
        if key not in tax and key not in topics:
            errs.append(f"rule {rx!r}: '{key}' is neither a subtopic code nor a topic in data/pledge_topics.csv")
    return errs


def score(row: dict, tax: dict) -> tuple:
    """({topic: score}, {(topic, code): (summary score, section score)}, {(topic, code): first position}, {topic: summary score})."""
    summary, section = PROTECT.sub(" protected ", norm(row.get("summary"))), section_of(row)
    tops, subs, first, pos, summ, voted = {}, {}, {}, {}, {}, set()
    for rules, text, where in ((SUMMARY_RULES, summary, "summary"), (SECTION_RULES, section, "section")):
        for key, rx, *wt in rules:
            found = list(re.finditer(rx, text, re.I))
            if not found:
                continue
            topic, code = (tax[key][0], key) if key in tax else (key, "")
            if where == "summary":
                w = min(2.0, SUMMARY_W + 0.5 * (len(found) - 1)) * (GENERIC if not code else 1) * (wt[0] if wt else 1)
                summ[topic] = summ.get(topic, 0) + w
                first[topic] = min(first.get(topic, 10 ** 6), found[0].start())
                pos[(topic, code)] = min(pos.get((topic, code), 10 ** 6), found[0].start())
            else:   # a heading votes once per topic, however many of its rules match
                w = 0 if topic in voted else SECTION_W
                voted.add(topic)
            tops[topic] = tops.get(topic, 0) + w
            a, b = subs.get((topic, code), (0, 0))
            subs[(topic, code)] = (a + w, b) if where == "summary" else (a, b + SECTION_W)
    if first:   # the subject named first in the summary
        tops[min(first, key=first.get)] += FIRST
    return tops, subs, pos, summ


def assign(row: dict, tax: dict) -> dict:
    """{topic, subtopic, code, margin, runner_up} as the rules read one row."""
    tops, subs, pos, summ = score(row, tax)
    if not tops:
        return {"topic": "", "subtopic": "", "code": "", "margin": 0, "runner_up": ""}
    ranked = sorted(tops.items(), key=lambda kv: (-kv[1], -summ.get(kv[0], 0)))   # ties: more from the summary
    best, best_score = ranked[0]
    runner = ranked[1] if len(ranked) > 1 else ("", 0)
    for code, rx in SUBTOPIC_HINTS:   # within the chosen topic only
        if tax[code][0] == best and re.search(rx, norm(row.get("summary")), re.I):
            a, b = subs.get((best, code), (0, 0))
            subs[(best, code)] = (a + SUMMARY_W, b)
            pos.setdefault((best, code), 10 ** 6)
    inside = sorted(((c, a + 0.5 * b) for (t, c), (a, b) in subs.items() if t == best and c),
                    key=lambda kv: (-kv[1], pos.get((best, kv[0]), 10 ** 6)))   # ties: the one named first
    code = inside[0][0] if inside else ""
    return {"topic": best, "subtopic": tax[code][1] if code else "", "code": code, "margin": best_score - runner[1],
            "runner_up": runner[0]}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--write", action="store_true", help="fill empty topic/subtopic cells in data/manifesto_pledges.csv from the rules")
    ap.add_argument("--force", action="store_true", help="with --write: recompute every row, overwriting hand placements")
    a = ap.parse_args(argv)
    tax = taxonomy()
    errs = check_rules(tax)
    if errs:
        print("\n".join("FAIL " + e for e in errs))
        return 1
    with CSV.open(encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        fields, rows = list(reader.fieldnames), list(reader)
    for col in ("subtopic", "topic"):
        if col not in fields:
            fields.insert(fields.index(AFTER) + 1, col)
    rules = {r["id"]: assign(r, tax) for r in rows}
    changed = 0
    for r in rows:
        x, have = rules[r["id"]], ((r.get("topic") or "").strip(), (r.get("subtopic") or "").strip())
        if a.write and (a.force or have == ("", "")) and (x["topic"], x["subtopic"]) != have:
            r["topic"], r["subtopic"] = x["topic"], x["subtopic"]
            changed += 1
        r.setdefault("topic", ""); r.setdefault("subtopic", "")

    n = len(rows)
    count = {}
    for r in rows:
        count[(r["topic"], r["subtopic"])] = count.get((r["topic"], r["subtopic"]), 0) + 1
    order = list(dict.fromkeys(t for t, _ in tax.values()))
    print(f"{n} manifesto rows; data/pledge_topics.csv: {len(order)} topics, {len(tax)} subtopics.\n")
    print("== the taxonomy, with the rows in each")
    for t in order:
        print(f"  {t}: {sum(v for (tt, _), v in count.items() if tt == t)}")
        for code, (tt, s) in tax.items():
            if tt == t:
                print(f"      {code}  {s}: {count.get((t, s), 0)}")
    loose = [r for r in rows if not r["topic"] or not r["subtopic"]]
    print(f"\n== rows without a topic and subtopic: {len(loose)}")
    for r in loose:
        x = rules[r["id"]]
        print(f"     {r['id']}: rules suggest {x['code'] or '-'} ({x['topic'] or 'nothing matched'})  |  {r['summary'][:90]}")
    agree_t = sum(1 for r in rows if r["topic"] and rules[r["id"]]["topic"] == r["topic"])
    agree_s = sum(1 for r in rows if r["subtopic"] and rules[r["id"]]["subtopic"] == r["subtopic"])
    placed = sum(1 for r in rows if r["subtopic"])
    print(f"\n== the rules read {agree_t} of {placed} placed rows into the same topic and {agree_s} into the same subtopic")
    differ = [r for r in rows if r["subtopic"] and rules[r["id"]]["subtopic"] != r["subtopic"]]
    print(f"   rows the rules read differently (the file is kept; worth a second look): {len(differ)}")
    code_of = {v: k for k, v in tax.items()}
    for r in differ:
        x = rules[r["id"]]
        print(f"     {r['id']}: file {code_of.get((r['topic'], r['subtopic']), '?')} {r['subtopic']}; rules {x['code'] or '-'} {x['subtopic'] or x['topic'] or 'nothing'}"
              f"  |  {r['summary'][:80]}")
    if a.write:
        with CSV.open("w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=fields)
            w.writeheader()
            w.writerows(rows)
        print(f"\nWrote {CSV.relative_to(ROOT)}: {changed} rows changed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
