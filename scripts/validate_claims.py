#!/usr/bin/env python3
"""Validate every claims/CC-*/claim.yml against the project's rules.

Run from the repository root:  python scripts/validate_claims.py
Exit code is non-zero if any record is invalid.
"""
import pathlib
import re
import sys

import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent

STATUSES = {"Not started", "In progress", "Drafted", "Right of reply", "Published"}
VERDICTS = {None, "Supported", "Largely supported", "Not substantiated", "Misleading", "Contradicted"}
CONFIDENCE = {None, "High", "Moderate", "Low"}
WORDING = {"Verbatim found", "Paraphrase: locate quote"}
TAGS = {"Selective metric", "Input-as-outcome", "Compliance-not-health",
        "Conditional-turned-unconditional", "Promise-without-baseline"}
REQUIRED = ["id", "title", "category", "status", "claim", "tags"]
STRICT_VERDICTS = {"Misleading", "Contradicted"}


def check(path: pathlib.Path) -> list:
    errs = []
    d = yaml.safe_load(path.read_text(encoding="utf-8"))
    for k in REQUIRED:
        if k not in d:
            errs.append(f"missing field: {k}")
    if errs:
        return errs
    if not re.fullmatch(r"CC-\d{3}", d["id"]):
        errs.append(f"bad id format: {d['id']}")
    if path.parent.name != d["id"]:
        errs.append(f"folder name {path.parent.name} does not match id {d['id']}")
    if d["status"] not in STATUSES:
        errs.append(f"unknown status: {d['status']}")
    if d.get("verdict") not in VERDICTS:
        errs.append(f"unknown verdict: {d.get('verdict')}")
    if d.get("verdict_confidence") not in CONFIDENCE:
        errs.append(f"unknown confidence: {d.get('verdict_confidence')}")
    c = d["claim"]
    if c.get("wording_status") not in WORDING:
        errs.append(f"unknown wording_status: {c.get('wording_status')}")
    for t in d["tags"]:
        if t not in TAGS:
            errs.append(f"unknown tag: {t}")
    if d.get("verdict") in STRICT_VERDICTS and not d.get("evidence_shown"):
        errs.append("Misleading/Contradicted requires 'evidence_shown' (documents or data that can be shown)")
    if d["status"] in {"Right of reply", "Published"} and not (d.get("right_of_reply") or {}).get("sent"):
        errs.append("status needs right_of_reply.sent date")
    if d["status"] == "Published" and c.get("wording_status") != "Verbatim found":
        errs.append("cannot publish without a verbatim, archived claim wording")
    return errs


def main() -> int:
    bad = 0
    files = sorted((ROOT / "claims").glob("CC-*/claim.yml"))
    for p in files:
        errs = check(p)
        if errs:
            bad += 1
            print(f"FAIL {p.relative_to(ROOT)}")
            for e in errs:
                print(f"   - {e}")
    print(f"{len(files) - bad}/{len(files)} claim records valid.")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
