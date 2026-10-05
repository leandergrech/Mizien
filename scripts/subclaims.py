#!/usr/bin/env python3
"""The parts of a claim (sub-claims), kept in step with its report.

Each report generator (tools/cc-NNN-report/build_report.py) may hold a sub-claim table: a header row starting
"Sub-claim", then rows "<b>A.</b> wording", the finding, and a rating chip such as verd("SUPPORTED", GREENC). The
table is where the research writes them; claim.yml carries the same parts as `subclaims:` (ids CC-NNNA, CC-NNNB...)
so the site can show and link them. This script reads a report's table and writes the block into claim.yml, just
after the `location:` block.

    python scripts/subclaims.py CC-017          # sync one claim from its report
    python scripts/subclaims.py --all           # sync every claim whose report has a sub-claim table
    python scripts/subclaims.py --check         # report claims whose subclaims differ from their report

scripts/validate_claims.py fails when a claim's subclaims differ from its report's table, and names this script.
"""
import ast
import json
import pathlib
import re
import sys

import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
TONE_BY_COLOUR = {"GREENC": "green", "LG": "lime", "AMBER": "amber", "ORANGE": "orange", "RED": "red", "BRICK": "red",
                  "MAROON": "maroon", "GREY": "grey"}
FIELDS = ("id", "text", "said_by", "finding", "rating", "tone")
HEAD = ("subclaims:   # parts of the claim tested separately (the report's sub-claim table), numbered parent + letter;\n"
        "             # kept in step with the report by scripts/subclaims.py; tone is the colour of the report's chip")


def _strip(s):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", s or "")).strip()


def _text(node):
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value
    if isinstance(node, ast.Call) and node.args:
        return _text(node.args[0])
    return None


def _colour(node):
    if isinstance(node, ast.Call) and len(node.args) > 1 and isinstance(node.args[1], ast.Name):
        return node.args[1].id
    return None


def _tone_from_words(t):
    t = t.lower()
    for words, tone in (("misleading", "red"), ("contradict", "maroon"), ("not substantiated", "orange"),
                        ("largely", "lime"), ("supported", "green"), ("accurate", "green")):
        if words in t:
            return tone
    return "grey"


def _sentence(t):
    s = re.sub(r"\bcc-(\d{3})\b", lambda m: "CC-" + m.group(1), t.lower())
    return s[:1].upper() + s[1:]


def from_report(cid):
    """The report's sub-claim table as subclaims, or None if the report has none."""
    path = ROOT / "tools" / f"cc-{cid[3:]}-report" / "build_report.py"
    if not path.is_file():
        return None
    for node in ast.walk(ast.parse(path.read_text(encoding="utf-8"))):
        if not isinstance(node, ast.List) or not node.elts or not isinstance(node.elts[0], ast.List):
            continue
        head = [_strip(_text(c)) for c in node.elts[0].elts]
        if not head or not re.match(r"(?i)sub-?claim", head[0]):
            continue
        rows = []
        for r in node.elts[1:]:
            if not isinstance(r, ast.List) or not r.elts:
                continue
            m = re.match(r"^([A-Z])[.)]\s*(.+)$", _strip(_text(r.elts[0])))
            if not m:
                continue
            row = {"id": cid + m.group(1), "text": m.group(2)}
            for h, c in zip(head[1:], r.elts[1:]):
                t = _strip(_text(c))
                if re.match(r"(?i)said by", h):
                    row["said_by"] = t
                elif re.match(r"(?i)what the evidence|evidence|finding", h):
                    row["finding"] = t
                elif re.match(r"(?i)rating|verdict|result", h):
                    row["rating"] = _sentence(t)
                    row["tone"] = TONE_BY_COLOUR.get(_colour(c)) or _tone_from_words(t)
            rows.append(row)
        return rows or None
    return None


def same(record_parts, report_parts):
    norm = lambda xs: [{k: str(x.get(k) or "") for k in FIELDS} for x in xs or []]
    return norm(record_parts) == norm(report_parts)


def block(parts):
    q = lambda s: json.dumps(s, ensure_ascii=False)   # a JSON string is a valid double-quoted YAML scalar
    lines = [HEAD]
    for x in parts:
        lines.append(f"  - id: {x['id']}")
        for k in ("text", "said_by", "finding", "rating"):
            if x.get(k):
                lines.append(f"    {k}: {q(x[k])}")
        if x.get("tone"):
            lines.append(f"    tone: {x['tone']}")
    return "\n".join(lines) + "\n"


def _slot(s):
    """Where the block goes: right after the location block, which other edits rarely touch (so merges stay clean)."""
    if "\nlocation:" not in s:
        return s.index("\nhistory:") + 1 if "\nhistory:" in s else len(s)
    i = s.index("\nlocation:") + 1
    m = re.search(r"\n(?=[a-z_]+:)", s[i:])
    return i + m.start() + 1 if m else len(s)


def sync(cid):
    """Write the report's sub-claims into claim.yml. Returns True if the file changed."""
    parts = from_report(cid)
    p = ROOT / "claims" / cid / "claim.yml"
    s = p.read_text(encoding="utf-8")
    current = (yaml.safe_load(s) or {}).get("subclaims")
    if parts is None or same(current, parts):
        return False
    if "\nsubclaims:" in s:   # drop the old block: from "subclaims:" to the next top-level key
        i = s.index("\nsubclaims:") + 1
        m = re.search(r"\n(?=[a-z_]+:)", s[i:])
        s = s[:i] + s[i + m.start() + 1:]
    s = s[:_slot(s)] + block(parts) + s[_slot(s):]
    p.write_text(s, encoding="utf-8")
    return True


def main(argv):
    ids = sorted(p.parent.name for p in (ROOT / "claims").glob("CC-*/claim.yml"))
    if "--check" in argv:
        bad = [c for c in ids if from_report(c) is not None
               and not same((yaml.safe_load((ROOT / "claims" / c / "claim.yml").read_text(encoding="utf-8")) or {}).get("subclaims"), from_report(c))]
        print("\n".join(f"{c}: subclaims differ from the report's table" for c in bad) or "All subclaims match their reports.")
        return 1 if bad else 0
    targets = ids if "--all" in argv else [a for a in argv if re.fullmatch(r"CC-\d{3}", a)]
    if not targets:
        print(__doc__)
        return 2
    for c in targets:
        if sync(c):
            print(f"{c}: subclaims updated from its report")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
