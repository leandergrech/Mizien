#!/usr/bin/env python3
"""Register a folder of manifesto PDFs against data/manifesto_coverage.csv, changing nothing.

For each PDF in the folder (and its sub-folders) the script records the SHA-256, reads the metadata and the first
pages, works out which party and which election it is, and compares it with the coverage table:

  already covered     the same SHA-256 as the copy recorded for that programme (full hash, or the short
                      'c7f65d55…6383' form, prefix and suffix)
  known, not listed   a SHA-256 noted in a coverage row's notes (for example the Maltese edition of a programme
                      whose English edition was listed)
  new edition         a different file for a programme already listed (another print, a later web version,
                      another language)
  new programme       a programme with no listed copy: a party and election logged as 'no programme found' or
                      'not yet listed', or not in the table at all
  unidentified        party or election not found in the file; the report shows what was read, so a person can
                      decide (renaming the file to include the party and year is enough for a re-run)

Then it lists the coverage rows with no matching PDF in the folder. Party and year come from, in order of weight:
the programme's own title (from the coverage table and PROGRAMMES below), the file name, the PDF metadata, the
first pages, and the rest of the text (party names only, case-sensitive, so 'labour' or 'ilkoll' as ordinary words
do not count). Every guess is printed with the evidence behind it.

Run from the repository root (needs pdftotext and pdfinfo from poppler, or the pypdf package):
    python scripts/manifesto_register.py PATH [--pages 3] [--csv OUT.csv]

The PDFs are never copied into the repository: only hashes and source links are recorded, by hand, after review.
"""
import argparse
import csv
import datetime as dt
import hashlib
import re
import shutil
import subprocess
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
import pledges  # noqa: E402  (data/cycles.csv and data/manifesto_coverage.csv)

# Names that identify a party: matched case-sensitively on word boundaries, and also with spaces removed, so that
# letter-spaced covers ('PA R T I T L A B U R I S TA') are read. The coverage table's party_name is added to these.
# Acronyms that are ordinary words in Maltese or English ('abba', 'volt') only count in capitals or in a name.
PARTY_NAMES = {
    "pl": ["Partit Laburista", "Labour Party", "Partit tal-Labour"],
    "pn": ["Partit Nazzjonalista", "Nationalist Party"],
    "adpd": ["ADPD", "Alternattiva Demokratika", "Partit Demokratiku", "Green Party"],
    "abba": ["ABBA"],
    "volt": ["Volt Malta", "Volt Europa"],
    "pp": ["Partit Popolari", "People's Party", "People’s Party"],
    "momentum": ["Momentum", "MOMENTUM"],
    "ahwa": ["Aħwa Maltin", "AĦWA MALTIN", "Ahwa Maltin"],
    "imperium": ["Imperium Europa", "IMPERIUM EUROPA"],
}
# Programme titles: a title names both the party and the election. Generic words in a title ('Ilkoll' is also
# 'all of us') only count together with the year.
PROGRAMMES = [
    ("pl", "2022", r"Malta\s+Flimkien"),
    ("pl", "2026", r"\bInt\s+Malta\b"),
    ("pn", "2022", r"Vi[żz]joni\s+G[ħh]al\s+Malta\s+2030"),
    ("pn", "2026", r"Nifs\s+[ĠG]did"),
    ("adpd", "2026", r"\b[Ii]lkoll\b\s+Manifest\s+Elettorali\s+2026"),
    ("abba", "2022", r"Everyone\s+Counts"),
    ("volt", "2022", r"Volt\s+Malta\s+Manifesto\s+2022"),
    ("momentum", "2026", r"Bidla\s+ta['’]\s*Vera"),
    ("ahwa", "2026", r"Malta\s+g[ħh]all-Maltin"),
]
ELECTION_WORDS = r"(?:manifest\w*|elettoral\w*|elezzjoni|election\w*|programm\w*|ġenerali|generali|general)"
HASH = re.compile(r"\b([0-9a-f]{64})\b|\b([0-9a-f]{6,63})(?:…|\.\.\.)([0-9a-f]{3,63})\b")
W = {"title": 6, "filename": 4, "metadata": 4, "first pages": 2, "text": 1}   # weight of a match by where it was found


def fold(s: str) -> str:
    """Lower case, ASCII only, letters only: for names printed letter-spaced or with Maltese letters dropped."""
    return re.sub(r"[^a-z0-9]", "", unicodedata.normalize("NFD", s).encode("ascii", "ignore").decode().lower())


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def hashes_in(text: str) -> list:
    """Every SHA-256 written in a field, full or short ('c7f65d55…6383'): [(prefix, suffix)], full ones with suffix ''."""
    return [(m.group(1), "") if m.group(1) else (m.group(2), m.group(3)) for m in HASH.finditer(text or "")]


def hash_matches(full: str, written: tuple) -> bool:
    pre, suf = written
    return full == pre if not suf else full.startswith(pre) and full.endswith(suf)


def pdf_info(path: Path) -> dict:
    """Pages, title, author, subject, keywords and creation date from the PDF metadata ({} if unreadable)."""
    if shutil.which("pdfinfo"):
        out = subprocess.run(["pdfinfo", str(path)], capture_output=True, text=True, errors="replace").stdout
        info = {k.strip().lower(): v.strip() for k, _, v in (l.partition(":") for l in out.splitlines()) if v}
        created = ""
        if info.get("creationdate"):
            try:
                created = dt.datetime.strptime(" ".join(info["creationdate"].split()[:5]), "%a %b %d %H:%M:%S %Y").date().isoformat()
            except ValueError:
                created = ""
        return {"pages": int(info.get("pages", "0") or 0), "created": created,
                **{k: info.get(k, "") for k in ("title", "author", "subject", "keywords")}}
    try:
        import pypdf
        r = pypdf.PdfReader(str(path))
        m = r.metadata or {}
        c = m.get("/CreationDate", "") or ""
        created = f"{c[2:6]}-{c[6:8]}-{c[8:10]}" if re.match(r"D:\d{8}", c) else ""
        return {"pages": len(r.pages), "created": created, "title": m.get("/Title", "") or "",
                "author": m.get("/Author", "") or "", "subject": m.get("/Subject", "") or "", "keywords": m.get("/Keywords", "") or ""}
    except Exception:
        return {}


def pdf_text(path: Path, first: int = 0, last: int = 0) -> str:
    """Text of pages first..last (1-based; 0 = from the start / to the end)."""
    if shutil.which("pdftotext"):
        cmd = ["pdftotext", "-q"] + (["-f", str(first)] if first else []) + (["-l", str(last)] if last else []) + [str(path), "-"]
        return subprocess.run(cmd, capture_output=True, text=True, errors="replace").stdout
    try:
        import pypdf
        pages = pypdf.PdfReader(str(path)).pages
        lo, hi = (first or 1) - 1, (last or len(pages))
        return "\n".join((p.extract_text() or "") for p in pages[lo:hi])
    except Exception:
        return ""


def party_patterns(coverage: dict) -> dict:
    names = {p: list(v) for p, v in PARTY_NAMES.items()}
    for (_, party), row in coverage.items():
        for n in re.split(r"\s*[()–]\s*", row.get("party_name") or ""):   # 'Partit Laburista (Labour Party)' -> both
            if len(n) > 3 and n not in names.setdefault(party, []):
                names[party].append(n)
    return {p: [(n, re.compile(r"(?<!\w)" + re.escape(n) + r"(?!\w)"), fold(n)) for n in v] for p, v in names.items()}


def score_parties(where: dict, pats: dict) -> tuple:
    """{party: score} and the evidence, from the texts in `where` ({place: text}). Long names also count with the
    spaces taken out ('PA R T I T L A B U R I S TA'); the rest of the text counts at most 5 hits per name."""
    score, evidence = {}, {}
    for place, text in where.items():
        if not text:
            continue
        flat = fold(text)
        for party, plist in pats.items():
            for name, rx, folded in plist:
                n = len(rx.findall(text))
                if not n and len(folded) >= 10 and place != "text":
                    n = flat.count(folded)
                if n:
                    n = min(n, 5) if place == "text" else 1
                    score[party] = score.get(party, 0) + W[place] * n
                    evidence.setdefault(party, []).append(f"'{name}' in {place}" + (f" ×{n}" if n > 1 else ""))
    return score, evidence


def years_near_election_words(text: str, years: set) -> dict:
    """{year: count} for the election years in `years` printed within 60 characters of an election word."""
    out = {}
    for m in re.finditer(r"\b(20\d\d)\b", text):
        y = m.group(1)
        ctx = text[max(0, m.start() - 60):m.end() + 60]
        if y in years and re.search(ELECTION_WORDS, ctx, re.I):
            out[y] = out.get(y, 0) + 1
    return out


def first_election_on_or_after(day: str, cycles: list) -> str:
    for c in cycles:
        if c["election_date"] >= day:
            return c["id"]
    return ""


def language(text: str) -> str:
    """'Maltese', 'English' or '' from the letters ħ ġ ż ċ and the commonest small words."""
    words = re.findall(r"\w+", text.lower())
    if len(words) < 50:
        return ""
    mt = sum(w in {"il", "u", "li", "ta", "tal", "għal", "biex", "fil", "huwa", "dan"} for w in words) + 2 * len(re.findall(r"[ħġżċ]", text.lower()))
    en = sum(w in {"the", "and", "of", "to", "will", "for", "is", "that", "we", "our"} for w in words)
    return "Maltese" if mt > en * 1.5 else "English" if en > mt * 1.5 else "mixed"


def identify(path: Path, pages: int, cycles: list, coverage: dict, pats: dict) -> dict:
    info = pdf_info(path)
    head = pdf_text(path, 1, pages)
    full = pdf_text(path)
    rest = full[len(head):] if full.startswith(head) else full
    meta = " ".join(info.get(k, "") for k in ("title", "author", "subject", "keywords"))
    places = {"filename": path.stem.replace("_", " ").replace("-", " "), "metadata": meta, "first pages": head, "text": rest}
    years = {c["id"] for c in cycles}

    # 1. A programme title names party and election together.
    title_hits = []
    for party, cyc, rx in PROGRAMMES:
        for place in ("filename", "metadata", "first pages"):
            if re.search(rx, places[place]) or (place == "filename" and re.search(rx, path.stem.replace("_", " "), re.I)):
                title_hits.append((party, cyc, f"title '{rx}' in {place}"))
                break
    # 2. Party names.
    score, evidence = score_parties(places, pats)
    for party, _, why in title_hits:
        score[party] = score.get(party, 0) + W["title"]
        evidence.setdefault(party, []).insert(0, why)
    ranked = sorted(score.items(), key=lambda kv: -kv[1])
    party, party_note = "", ""
    if ranked and (len(ranked) == 1 or ranked[0][1] >= 2 * ranked[1][1]):
        party = ranked[0][0]
    elif ranked:
        party_note = "unclear: " + ", ".join(f"{p} {s}" for p, s in ranked[:3])
    # 3. Election year: title, then file name, metadata and first pages near election words, then the creation date.
    ys, year_why = {}, []
    for p, c, _ in title_hits:
        if p == party:
            ys[c] = ys.get(c, 0) + W["title"]; year_why.append(f"{c} from the programme title")
    for place in ("filename", "metadata", "first pages"):
        txt = places[place]
        found = years_near_election_words(txt, years) if place == "first pages" else {y: 1 for y in re.findall(r"\b(20\d\d)\b", txt) if y in years}
        for y, n in found.items():
            ys[y] = ys.get(y, 0) + W[place] * min(n, 3); year_why.append(f"{y} in {place}" + (f" ×{n}" if n > 1 else ""))
    if info.get("created"):
        y = first_election_on_or_after(info["created"], cycles)
        if y:
            ys[y] = ys.get(y, 0) + 1; year_why.append(f"{y}: first election after the file was made ({info['created']})")
    past = {y for y in re.findall(r"\b(20[0-3]\d)\b", head) if int(y) <= dt.date.today().year}   # target years such as 2030 are not elections
    other = sorted(y for y in past if y not in years and years_near_election_words(head, {y}))
    yr = sorted(ys.items(), key=lambda kv: -kv[1])
    cycle = yr[0][0] if yr and (len(yr) == 1 or yr[0][1] > yr[1][1]) else ""
    return {"file": str(path), "name": path.name, "sha256": sha256(path), "bytes": path.stat().st_size, **info,
            "language": language(full[:20000]), "party": party, "party_note": party_note,
            "party_evidence": "; ".join(evidence.get(party, [])[:4]) if party else "",
            "cycle": cycle, "cycle_evidence": "; ".join(year_why[:4]),
            "other_years": ", ".join(other), "first_line": " ".join(head.split())[:160]}


def classify(r: dict, coverage: dict, cycles: list) -> tuple:
    """(category, explanation) for one PDF against the coverage table."""
    for (cyc, party), row in coverage.items():
        if any(hash_matches(r["sha256"], h) for h in hashes_in(row.get("sha256"))):
            return "already covered", f"{party} {cyc}: {row.get('document') or row.get('party_name')} ({row['status']}, {row.get('rows')} rows)"
    for (cyc, party), row in coverage.items():
        if any(hash_matches(r["sha256"], h) for h in hashes_in(row.get("notes"))):
            return "known, not listed", f"{party} {cyc}: noted in the coverage notes but not extracted: \"{row['notes'][:140]}\""
    if not r["party"] or not r["cycle"]:
        missing = " and ".join(x for x, v in (("party", r["party"]), ("election", r["cycle"])) if not v)
        return "unidentified", f"{missing} not found in the file" + (f" ({r['party_note']})" if r["party_note"] else "")
    row = coverage.get((r["cycle"], r["party"]))
    contested = {c["id"]: {x.strip() for x in (c.get("contested") or "").split(";")} for c in cycles}
    if row is None:
        if r["party"] not in contested.get(r["cycle"], set()):
            return "new programme", f"{r['party']} is not listed as contesting {r['cycle']} in data/cycles.csv: check the party and year"
        return "new programme", f"no coverage row for {r['party']} {r['cycle']}"
    if row["status"] == "listed":
        held = row.get("sha256") or "no hash recorded"
        return "new edition", (f"{r['party']} {r['cycle']} is listed from {row.get('document')} (sha256 {held}; {row.get('source_url')}); "
                               f"this file differs")
    return "new programme", f"{r['party']} {r['cycle']} is logged as '{row['status']}': {(row.get('notes') or row.get('searched') or '')[:160]}"


ORDER = ["already covered", "known, not listed", "new edition", "new programme", "unidentified"]


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("path", help="folder of manifesto PDFs (searched recursively)")
    ap.add_argument("--pages", type=int, default=3, help="first pages read for the title and year (default 3)")
    ap.add_argument("--csv", help="also write the register to this CSV file (keep it outside the repository or in scratch)")
    a = ap.parse_args(argv)
    folder = Path(a.path).expanduser()
    if not folder.is_dir():
        print(f"{folder}: not a folder", file=sys.stderr)
        return 2
    if not (shutil.which("pdftotext") and shutil.which("pdfinfo")):
        try:
            import pypdf  # noqa: F401
        except ImportError:
            print("needs pdftotext and pdfinfo (poppler-utils) or the pypdf package", file=sys.stderr)
            return 2
    cycles, coverage = pledges.load_cycles(), pledges.load_coverage()
    pats = party_patterns(coverage)
    files = sorted(p for p in folder.rglob("*") if p.is_file() and p.suffix.lower() == ".pdf")
    rows = []
    for p in files:
        r = identify(p, a.pages, cycles, coverage, pats)
        r["category"], r["detail"] = classify(r, coverage, cycles)
        rows.append(r)
    seen = {}
    for r in rows:
        seen.setdefault(r["sha256"], []).append(r["name"])

    print(f"{len(files)} PDF(s) in {folder}; data/manifesto_coverage.csv has {len(coverage)} rows. Nothing was changed.\n")
    for cat in ORDER:
        group = [r for r in rows if r["category"] == cat]
        print(f"== {cat}: {len(group)}")
        for r in group:
            dup = [n for n in seen[r["sha256"]] if n != r["name"]]
            print(f"  {r['name']}  sha256 {r['sha256'][:8]}…{r['sha256'][-4:]}  {r.get('pages', '?')} pages"
                  + (f", {r['language']}" if r["language"] else "") + (f"  (same file as {', '.join(dup)})" if dup else ""))
            print(f"    party {r['party'] or '?'}"
                  + (f" ({r['party_evidence']})" if r["party_evidence"] else f" ({r['party_note']})" if r["party_note"] else "")
                  + f"; election {r['cycle'] or '?'}" + (f" ({r['cycle_evidence']})" if r["cycle_evidence"] else ""))
            if r["other_years"]:
                print(f"    also near election words: {r['other_years']} (not in data/cycles.csv)")
            print(f"    {r['detail']}")
            if cat in ("new edition", "new programme", "unidentified"):
                print(f"    title: {r.get('title') or '-'}; made {r.get('created') or '?'}; first words: {r['first_line'][:120]}")
        print()

    matched = {(c, p) for (c, p), row in coverage.items() for r in rows
               if r["category"] in ("already covered", "known, not listed")
               and any(hash_matches(r["sha256"], h) for h in hashes_in((row.get("sha256") or "") + " " + (row.get("notes") or "")))}
    offered = {(r["cycle"], r["party"]) for r in rows if r["category"] in ("new edition", "new programme")}
    print("== coverage rows with no matching PDF in the folder")
    for (c, p), row in sorted(coverage.items()):
        if (c, p) in matched:
            continue
        note = "a candidate file is listed above" if (c, p) in offered else "no file found here"
        kind = "listed from web chapters" if "web chapters" in (row.get("document") or "") and row["status"] == "listed" else row["status"]
        print(f"  {c} {p} ({row['party_name']}): {kind}; {note}")

    if a.csv:
        fields = ["category", "detail", "name", "sha256", "bytes", "pages", "language", "party", "party_evidence", "party_note",
                  "cycle", "cycle_evidence", "other_years", "title", "author", "created", "first_line", "file"]
        with open(a.csv, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
            w.writeheader()
            w.writerows(sorted(rows, key=lambda r: (ORDER.index(r["category"]), r["name"])))
        print(f"\nWrote {a.csv}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
