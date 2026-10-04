"""The register of bodies and people (data/bodies.csv) and how claims are matched to it.

Each row is an organisation or a person (a person sits under the body they spoke for, with the role named in the
claim). Claims are matched by their speaker text: claim.speaker is split on ";" and each part is looked up in the
register's aliases (case and spacing ignored, then without anything in brackets). A claim may instead list
`bodies: [id, ...]` in its claim.yml. Speakers that match nothing are reported by scripts/validate_claims.py.
"""
import csv
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
TYPES = {   # type -> label, in the order the constellation shows them
    "government": "Government & ministers", "agency": "Public agencies & companies", "regulator": "Regulators & authorities",
    "oversight": "Courts, tribunals & oversight", "party": "Political parties", "civil_society": "NGOs & unions",
    "business": "Business & industry", "media": "Media", "eu": "EU & international", "research": "Research & statistics",
}
KINDS = {"organisation", "person"}


def _norm(s):
    return re.sub(r"\s+", " ", str(s or "").replace("–", "-").replace("’", "'")).strip().lower()


def load():
    path = ROOT / "data" / "bodies.csv"
    if not path.is_file():
        return {}
    with open(path, newline="", encoding="utf-8") as f:
        return {r["ID"]: {"id": r["ID"], "name": r["Name"], "kind": r["Kind"], "type": r["Type"], "parent": r["Parent"] or None,
                          "role": r["Role"] or None, "aliases": [a for a in r["Aliases"].split("|") if a.strip()],
                          "note": r["Note"] or None} for r in csv.DictReader(f)}


def alias_index(reg):
    idx = {}
    for b in reg.values():
        for a in b["aliases"] + [b["name"]]:
            idx.setdefault(_norm(a), []).append(b["id"])
    return idx


def resolve(claim, reg, idx):
    """Body IDs for a claim (explicit `bodies:` wins), plus speaker parts that matched nothing."""
    if claim.get("bodies"):
        return [b for b in claim["bodies"] if b in reg], [b for b in claim["bodies"] if b not in reg]
    found, unknown = [], []
    for part in str((claim.get("claim") or {}).get("speaker") or "").split(";"):
        if not part.strip():
            continue
        hits = idx.get(_norm(part)) or idx.get(_norm(re.sub(r"\(.*?\)", "", part)))
        if hits:
            found += [h for h in hits if h not in found]
        else:
            unknown.append(part.strip())
    return found, unknown


def org_of(bid, reg):
    """The organisation a body or person speaks for (a person's parent; an organisation itself)."""
    b = reg.get(bid)
    return b["parent"] if b and b["kind"] == "person" and b["parent"] else bid
