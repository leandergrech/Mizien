"""How claims and bodies connect, for the claim pages, the body pages and the map.

Direct links come from data/edges.csv: two claims that share a theme in data/themes.csv. Indirect connections are
found by following those links one or two steps further (second and third degree). They are computed, not curated,
so they are weaker the further they go: a reason to read two checks together, never evidence about either.

Bodies come from the register (scripts/bodies.py). A body's record covers the claims it made directly and those of
the people and offices listed under it. Two bodies are linked when they are named in the same claim, or when their
claims share a theme.
"""
from collections import defaultdict

import bodies as register


def adjacency(edges):
    """{claim: {other claim: [theme ids]}} from the undirected edge list."""
    adj = defaultdict(lambda: defaultdict(list))
    for e in edges:
        a, b, t = e["from"], e["to"], e["theme"]
        if a == b:
            continue
        if t not in adj[a][b]:
            adj[a][b].append(t)
            adj[b][a].append(t)
    return adj


def indirect(cid, adj, depth=3, max_paths=3):
    """Claims two or three links away that are not linked directly, with example paths.

    Each path is a list of steps [claim, theme] from the start: [[B, T1], [C, T2]] reads
    "linked to B by T1, and B is linked to C by T2". Paths list the shortest routes only.
    """
    dist, paths = {cid: 0}, {cid: [[]]}
    frontier = [cid]
    for d in range(1, depth + 1):
        nxt = []
        for u in frontier:
            for v, themes in sorted(adj[u].items()):
                if dist.get(v, d) < d:
                    continue
                if v not in dist:
                    dist[v], paths[v] = d, []
                    nxt.append(v)
                for p in paths[u]:
                    if len(paths[v]) < max_paths:
                        paths[v].append(p + [[v, themes[0]]])
        frontier = nxt
    out = {2: [], 3: []}
    for v, d in dist.items():
        if d in out:
            out[d].append({"id": v, "paths": paths[v]})
    for d in out:
        out[d].sort(key=lambda x: x["id"])
    return out


def bridges(themes):
    """Pairs of themes that share at least one claim: the claims that bridge them."""
    out = []
    for i, a in enumerate(themes):
        for b in themes[i + 1:]:
            shared = sorted(set(a["members"]) & set(b["members"]))
            if shared:
                out.append({"a": a["id"], "b": b["id"], "claims": shared})
    return sorted(out, key=lambda x: (-len(x["claims"]), x["a"], x["b"]))


def units(ids, reg):
    """The bodies a claim is placed under: an office named together with one of its people is implied by the person."""
    parents = {reg[i]["parent"] for i in ids if reg[i]["kind"] == "person"}
    return [i for i in ids if i not in parents]


def descendants(bid, reg):
    """A body and everything below it in the register (its offices and people)."""
    out, todo = [], [bid]
    while todo:
        x = todo.pop()
        out.append(x)
        todo += [b["id"] for b in reg.values() if b["parent"] == x]
    return out


def lineage(bid, reg):
    """A body and everything above it in the register."""
    out = []
    while bid and bid not in out:
        out.append(bid)
        bid = reg[bid]["parent"]
    return out


def profiles(claim_bodies, reg, edges, records):
    """Per body: its claims (direct, and through the people and offices under it), people, and linked bodies.

    claim_bodies: {claim id: [body ids]} as resolved for each claim.
    Only bodies with at least one claim are returned. Linked bodies are counted at office level (a person's
    links count for the office they spoke for), and never between a body and the bodies above or below it.
    """
    by_id = {d["id"]: d for d in records}
    children = defaultdict(list)
    for b in reg.values():
        if b["parent"]:
            children[b["parent"]].append(b["id"])

    def below(bid):
        out, todo = [], [bid]
        while todo:
            x = todo.pop()
            out.append(x)
            todo += children[x]
        return out

    direct = defaultdict(list)
    for cid, ids in claim_bodies.items():
        for b in ids:
            direct[b].append(cid)
    office = {cid: {register.org_of(b, reg) for b in ids} for cid, ids in claim_bodies.items()}
    out = {}
    for bid, b in reg.items():
        tree = below(bid)
        claims = sorted({c for x in tree for c in direct[x]})
        if not claims:
            continue
        related = set(tree) | set(lineage(bid, reg))
        linked = defaultdict(lambda: {"named_with": set(), "themes": defaultdict(set)})
        mine = set(claims)
        for c in claims:
            for o in office[c]:
                if o not in related:
                    linked[o]["named_with"].add(c)
        for e in edges:
            for a, z in ((e["from"], e["to"]), (e["to"], e["from"])):
                if a in mine and z not in mine:
                    for o in office.get(z, ()):
                        if o not in related and not (set(lineage(o, reg)) & set(tree)):
                            linked[o]["themes"][e["theme"]].add((a, z))
        links = []
        for o, v in linked.items():
            pairs = sorted({p for s in v["themes"].values() for p in s})
            links.append({"id": o, "named_with": sorted(v["named_with"]),
                          "themes": {t: sorted(map(list, s)) for t, s in sorted(v["themes"].items())},
                          "pairs": len(pairs), "weight": 3 * len(v["named_with"]) + len(pairs)})
        links.sort(key=lambda x: (-x["weight"], x["id"]))
        verdicts, topics, patterns = defaultdict(int), defaultdict(int), defaultdict(int)
        for c in claims:
            d = by_id[c]
            verdicts[d.get("verdict") or (d.get("pledge") or {}).get("status") or "Not yet checked"] += 1
            topics[d["category"]] += 1
            for t in d.get("tags") or []:
                patterns[t] += 1
        out[bid] = {
            **{k: b[k] for k in ("id", "name", "kind", "type", "parent", "role", "note")},
            "claims": claims, "direct": sorted(direct[bid]),
            "people": sorted(x for x in children[bid] if reg[x]["kind"] == "person" and any(direct[y] for y in below(x))),
            "offices": sorted(x for x in children[bid] if reg[x]["kind"] == "organisation" and any(direct[y] for y in below(x))),
            "verdicts": dict(verdicts), "topics": dict(sorted(topics.items(), key=lambda kv: -kv[1])),
            "patterns": dict(sorted(patterns.items(), key=lambda kv: -kv[1])), "links": links,
        }
    return out
