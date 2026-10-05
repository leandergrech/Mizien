"""Patterns by kind of body: which pattern tags, verdicts and topics turn up in claims made by each kind of body
(government, agencies, regulators, parties, NGOs, business, media, EU, research), and who said what, when, on each
issue (theme).

This describes the claims Miżien has picked up. It does not measure how accurate any kind of body is: claims are
chosen because they can be checked, tags are provisional until a report is finished, and the numbers are small.
A claim made jointly by bodies of two kinds counts once for each kind.
"""
from collections import OrderedDict

import bodies as register
import connections
import timeline

MIN_FOR_OBSERVATION = 3     # fewer tagged claims than this: no sentence about where a tag turns up
DOMINANT_SHARE = 0.6        # one kind of body accounts for at least this share: say so


def claim_types(ids, reg):
    """The kinds of body that made a claim, in register order; the first is the kind of the first body named."""
    units = connections.units(ids, reg)
    first = [reg[u]["type"] for u in units[:1]]
    rest = [t for t in register.TYPES if any(reg[u]["type"] == t for u in units)]
    return first + [t for t in rest if t not in first]


def build(records, claim_bodies, reg, themes, pattern_names, verdict_names, categories, claim_ref):
    by_id = {d["id"]: d for d in records}
    types_of = {cid: claim_types(ids, reg) for cid, ids in claim_bodies.items()}
    present = [t for t in register.TYPES if any(t in ts for ts in types_of.values())]
    kinds = []
    for t in present:
        mine = [by_id[c] for c in sorted(types_of) if t in types_of[c]]
        kinds.append({"id": t, "label": register.TYPES[t], "colour": register.TYPE_COLOURS[t], "claims": len(mine),
                      "checked": sum(1 for d in mine if d.get("verdict")),
                      "tagged": sum(1 for d in mine if d.get("tags"))})

    def matrix(rows, test):
        out = []
        for r in rows:
            cells = OrderedDict((t, [claim_ref(by_id[c]) for c in sorted(types_of) if t in types_of[c] and test(by_id[c], r)])
                                for t in present)
            total = sorted({x["id"] for v in cells.values() for x in v})
            out.append({"name": r, "cells": [{"type": t, "claims": v} for t, v in cells.items()], "total": len(total)})
        return out

    pattern_rows = matrix(pattern_names, lambda d, r: r in (d.get("tags") or []))
    verdict_rows = matrix(verdict_names + ["Not yet checked"], lambda d, r: (d.get("verdict") or "Not yet checked") == r)
    topic_rows = matrix(categories, lambda d, r: d["category"] == r)
    observations = []
    for row in pattern_rows:
        n = row["total"]
        if n < MIN_FOR_OBSERVATION:
            observations.append({"tag": row["name"], "n": n, "text": f"Only {n} claim{'' if n == 1 else 's'} carr{'ies' if n == 1 else 'y'} this tag so far: too few to say where it turns up."})
            continue
        top = max(row["cells"], key=lambda c: len(c["claims"]))
        k = len(top["claims"])
        spread = sum(1 for c in row["cells"] if c["claims"])
        if k / n >= DOMINANT_SHARE:
            text = (f"{k} of the {n} claims tagged so far involve {register.TYPE_PROSE[top['type']]}"
                    f"{'' if spread == 1 else f'; the rest are spread over {spread - 1} other kind' + ('' if spread == 2 else 's') + ' of body'}.")
        else:
            text = f"The {n} claims tagged so far are spread over {spread} kinds of body, with no one kind accounting for most."
        observations.append({"tag": row["name"], "n": n, "text": text})

    # Issues over time: the claims in each theme, placed by the date of the statement and coloured by who made it.
    items, undated = {}, {}
    for th in themes:
        for cid in th["members"]:
            d = by_id.get(cid)
            if not d:
                continue
            when = timeline.parse_date((d.get("claim") or {}).get("date"))
            ref = {**claim_ref(d), "type": (types_of.get(cid) or ["other"])[0]}
            if when:
                items.setdefault(th["id"], []).append({**ref, "mid": when["mid"], "date": when["label"],
                                                       "rough": when["precision"] == "year" or when["approx"]})
            else:
                undated.setdefault(th["id"], []).append(ref)
    ax = timeline.axis([i["mid"] for v in items.values() for i in v])
    issues = []
    for th in themes:
        placed, rows = timeline.place(items.get(th["id"], []), ax) if ax else ([], 0)
        kinds_here = sorted({i["type"] for i in placed} | {i["type"] for i in undated.get(th["id"], [])},
                            key=lambda t: list(register.TYPES).index(t) if t in register.TYPES else 99)
        issues.append({"id": th["id"], "name": th["name"], "color": th["color"], "description": th["description"],
                       "strength": th["strength"], "items": placed, "rows": max(rows, 1),
                       "undated": undated.get(th["id"], []), "kinds": kinds_here})
    chart = {"axis": ax, "lanes": [{"topic": i["name"], "items": i["items"], "rows": i["rows"]} for i in issues if i["items"]]}
    return {"kinds": kinds, "patterns": pattern_rows, "verdicts": verdict_rows, "topics": topic_rows,
            "observations": observations, "issues": issues, "axis": ax, "chart": chart,
            "min_for_observation": MIN_FOR_OBSERVATION, "dominant_share": DOMINANT_SHARE}
