#!/usr/bin/env python3
"""Register a folder of manifesto PDFs against data/manifesto_coverage.csv, changing nothing.

For each PDF in the folder (and its sub-folders) the script records the SHA-256, reads the metadata and the first
pages, decides whether the file is a programme at all, works out which party and which election it is, and compares
it with the coverage table:

  already covered     the same SHA-256 as the copy recorded for that programme (full hash, or the short
                      'c7f65d55…6383' form, prefix and suffix)
  known, not listed   a SHA-256 noted in a coverage row's notes (for example the Maltese edition of a programme
                      whose English edition was listed)
  same text           (with --fetch) a different file with the same text, page for page, as the listed copy: a
                      re-saved or compressed copy, nothing to register
  new edition         a different file for a programme already listed (another print, a later web version,
                      another language); not compared, or compared and the text differs
  new programme       a programme with no listed copy: a party and election logged as 'no programme found' or
                      'not yet listed', or not in the table at all
  unidentified        a programme whose party or election was not found; renaming the file to include the party
                      and year is enough for a re-run
  about a programme   an article, web page or press release that names a programme (news, fact-checks); listed
                      briefly, with a flag when it names a programme logged as not found
  other document      everything else (reports, papers, articles on other subjects): counted; --all lists them

A file is a programme when its name, its metadata or its first pages carry a programme title (PROGRAMMES below) or
the words manifesto, manifest elettorali, programm elettorali, electoral programme, and its first page has none of
the marks of a saved web page, news article or press release (WEB_MARKS). Party and year come from, in order of
weight: the programme's own title, the file name, the PDF metadata, the first pages, and the rest of the text (party
names only, case-sensitive, so 'labour' or 'ilkoll' as ordinary words do not count). Every guess is printed with the
evidence behind it. Last, it lists the coverage rows with no matching file.

--fetch downloads each listed copy that a 'new edition' could be a copy of into a temporary folder outside the
repository (deleted afterwards), checks its SHA-256 against the table and compares the text page by page.

Run from the repository root (needs pdftotext and pdfinfo from poppler, or the pypdf package):
    python scripts/manifesto_register.py PATH [--pages 3] [--fetch] [--all] [--csv OUT.csv]

The PDFs are never copied into the repository: only hashes and source links are recorded, by hand, after review.
"""
import argparse
import csv
import datetime as dt
import difflib
import hashlib
import re
import shutil
import subprocess
import sys
import tempfile
import unicodedata
import urllib.parse
import urllib.request
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
PROGRAMME_WORDS = r"\bmanifest(?:o|os)?\b|\bprogramm\w*\s+elettoral\w*|\belectoral\s+(?:programme|program|manifesto)"
# Marks of a saved web page, news article or press release on the first page: such a file is about a programme, not
# the programme. A party's own web chapters saved as PDF also carry them, so these files are still listed, briefly.
WEB_MARKS = (r"MENU \(/\)|View E-Paper|DIGITAL PAPER|Add as a preferred source|Home\s*>\s*\w|Other factchecks|Ixxerjaha|"
             r"PRESS RELEASE|\bPR\d{6}(?:en|mt)?\b|TVMi\b|\bBy (?:[A-Z][a-z]+ ){1,3}[-–(]")
WEB_LINKS = 3        # or at least this many '(https://…)' links printed on the first page
WEB_NAME = r"fact-?check|press release|\bnews\b"
COPY_SUFFIX = re.compile(r"(?:[-_ ]+(?:compressed|copy|final|ocr|small|web)|\s*\(\d+\))$", re.I)
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
    page1 = pdf_text(path, 1, 1)
    prog = bool(title_hits) or any(re.search(PROGRAMME_WORDS, places[k], re.I) for k in ("filename", "metadata", "first pages"))
    web = re.search(WEB_MARKS, page1[:3000]) or len(re.findall(r"\(https?://[^)\s]*\)", page1)) >= WEB_LINKS \
        or re.search(WEB_NAME, path.stem.replace("_", " "), re.I)
    kind = "other" if not prog else "about" if web else "programme"
    kind_why = (f"web or press marks: '{web.group(0) if hasattr(web, 'group') else 'links'}'" if web else "") if prog else ""
    past = {y for y in re.findall(r"\b(20[0-3]\d)\b", head) if int(y) <= dt.date.today().year}   # target years such as 2030 are not elections
    other = sorted(y for y in past if y not in years and years_near_election_words(head, {y}))
    yr = sorted(ys.items(), key=lambda kv: -kv[1])
    cycle = yr[0][0] if yr and (len(yr) == 1 or yr[0][1] > yr[1][1]) else ""
    return {"file": str(path), "name": path.name, "sha256": sha256(path), "bytes": path.stat().st_size, **info, "kind": kind, "kind_why": kind_why,
            "language": language(full[:20000]), "party": party, "party_note": party_note,
            "party_evidence": "; ".join(evidence.get(party, [])[:4]) if party else "",
            "cycle": cycle, "cycle_evidence": "; ".join(year_why[:4]),
            "other_years": ", ".join(other), "first_line": " ".join(head.split())[:160]}


def stem(name: str) -> str:
    """A file name without its extension, copy suffixes ('-compressed', ' (1)') and punctuation, for comparing names."""
    n = Path(urllib.parse.unquote(urllib.parse.urlparse(name).path if "://" in name else name)).stem
    while COPY_SUFFIX.search(n):
        n = COPY_SUFFIX.sub("", n)
    return fold(n)


def classify(r: dict, coverage: dict, cycles: list) -> tuple:
    """(category, explanation) for one PDF against the coverage table."""
    for (cyc, party), row in coverage.items():
        if any(hash_matches(r["sha256"], h) for h in hashes_in(row.get("sha256"))):
            return "already covered", f"{party} {cyc}: {row.get('document') or row.get('party_name')} ({row['status']}, {row.get('rows')} rows)"
    for (cyc, party), row in coverage.items():
        if any(hash_matches(r["sha256"], h) for h in hashes_in(row.get("notes"))):
            return "known, not listed", f"{party} {cyc}: noted in the coverage notes but not extracted: \"{row['notes'][:140]}\""
    row = coverage.get((r["cycle"], r["party"])) if r["party"] and r["cycle"] else None
    if r["kind"] == "other":
        return "other document", "no programme title or programme words in the name, metadata or first pages"
    if r["kind"] == "about":
        gap = row is not None and row["status"] != "listed"
        return "about a programme", (r["kind_why"] + (f"; NOTE: {r['party']} {r['cycle']} is logged as '{row['status']}': check whether "
                                                       f"this is the programme itself" if gap else ""))
    if not r["party"] or not r["cycle"]:
        missing = " and ".join(x for x, v in (("party", r["party"]), ("election", r["cycle"])) if not v)
        return "unidentified", f"{missing} not found in the file" + (f" ({r['party_note']})" if r["party_note"] else "")
    contested = {c["id"]: {x.strip() for x in (c.get("contested") or "").split(";")} for c in cycles}
    if row is None:
        if r["party"] not in contested.get(r["cycle"], set()):
            return "new programme", f"{r['party']} is not listed as contesting {r['cycle']} in data/cycles.csv: check the party and year"
        return "new programme", f"no coverage row for {r['party']} {r['cycle']}"
    if row["status"] == "listed":
        held = row.get("sha256") or "no hash recorded"
        hint = ("; same file name as the listed copy, so probably a re-saved or compressed copy (--fetch compares the text)"
                if stem(r["name"]) == stem(row.get("source_url") or "") else "")
        return "new edition", (f"{r['party']} {r['cycle']} is listed from {row.get('document')} (sha256 {held}; {row.get('source_url')}); "
                               f"this file differs" + hint)
    return "new programme", f"{r['party']} {r['cycle']} is logged as '{row['status']}': {(row.get('notes') or row.get('searched') or '')[:160]}"


def pages_text(path: Path) -> list:
    """The text of every page, as lists of lower-case words."""
    if shutil.which("pdftotext"):
        out = subprocess.run(["pdftotext", "-q", str(path), "-"], capture_output=True, text=True, errors="replace").stdout
        pages = out.split("\f")
        if pages and not pages[-1].strip():
            pages = pages[:-1]
    else:
        import pypdf
        pages = [(p.extract_text() or "") for p in pypdf.PdfReader(str(path)).pages]
    return [re.findall(r"\w+", t.lower()) for t in pages]


def compare_text(copy: Path, listed: Path) -> dict:
    """Page-by-page comparison: pages with the same text (95% of words in order), pages whose text the copy lost
    (empty in the copy, e.g. turned into images by a compressor), and pages that differ."""
    a, b = pages_text(copy), pages_text(listed)
    same = lost = 0
    differ = []
    for i, (x, y) in enumerate(zip(a, b), 1):
        if x == y or difflib.SequenceMatcher(None, x, y, autojunk=False).ratio() >= 0.95:
            same += 1
        elif not x and y:
            lost += 1
        else:
            differ.append(i)
    n = max(len(a), len(b))
    verdict = len(a) == len(b) and same + lost >= 0.95 * n and same >= 0.5 * n
    extra = (f", {len(b) - len(a)} pages only in the listed copy" if len(b) > len(a) else
             f", {len(a) - len(b)} pages only in this file" if len(a) > len(b) else "")
    return {"same_text": verdict, "summary": f"{len(a)} pages here, {len(b)} in the listed copy; same text on {same}"
            + (f", text lost in this copy on {lost}" if lost else "") + (f", different on {len(differ)} (pp. {', '.join(map(str, differ[:8]))}"
            + ("…" if len(differ) > 8 else "") + ")" if differ else "") + extra + " (pages compared in order)"}


def fetch(url: str, folder: Path) -> Path:
    """Download a listed copy into `folder` (a temporary folder outside the repository). Google Drive view links are
    turned into their download form."""
    m = re.search(r"drive\.google\.com/file/d/([^/]+)", url)
    if m:
        url = f"https://drive.google.com/uc?export=download&id={m.group(1)}"
    out = folder / f"listed-{hashlib.sha1(url.encode()).hexdigest()[:10]}.pdf"
    if not out.exists():
        req = urllib.request.Request(url, headers={"User-Agent": "Mizien-manifesto-register/1.0 (public claim-checking project)"})
        with urllib.request.urlopen(req, timeout=120) as resp, out.open("wb") as f:
            shutil.copyfileobj(resp, f)
    return out


def compare_with_listed(r: dict, row: dict, folder: Path) -> tuple:
    """For a 'new edition': fetch the listed copy and compare. Returns (category, extra detail)."""
    url = row.get("source_url") or ""
    if not (urllib.parse.urlparse(url).path.lower().endswith(".pdf") or "drive.google.com/file/d/" in url):
        return "new edition", "the listed copy is not a PDF (web chapters): not compared"
    try:
        listed = fetch(url, folder)
    except Exception as e:  # network, 403, timeout: say so and leave the category as it is
        return "new edition", f"could not fetch the listed copy ({e.__class__.__name__}: {e}): not compared"
    if open(listed, "rb").read(5) != b"%PDF-":
        return "new edition", "the listed URL did not return a PDF: not compared"
    h = sha256(listed)
    held = hashes_in(row.get("sha256"))
    note = "" if any(hash_matches(h, x) for x in held) else f"; NOTE: the URL now serves a different file (sha256 {h[:8]}…{h[-4:]}) from the one listed"
    c = compare_text(Path(r["file"]), listed)
    return ("same text" if c["same_text"] else "new edition"), c["summary"] + note


ORDER = ["already covered", "known, not listed", "same text", "new edition", "new programme", "unidentified", "about a programme",
         "other document"]


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("path", help="folder of manifesto PDFs (searched recursively)")
    ap.add_argument("--pages", type=int, default=3, help="first pages read for the title and year (default 3)")
    ap.add_argument("--fetch", action="store_true", help="download the listed copy of each 'new edition' (to a temporary "
                    "folder outside the repository) and compare the text page by page")
    ap.add_argument("--all", action="store_true", help="also list every 'other document' by name")
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
    with tempfile.TemporaryDirectory(prefix="mizien-listed-") as tmp:
        for p in files:
            r = identify(p, a.pages, cycles, coverage, pats)
            r["category"], r["detail"] = classify(r, coverage, cycles)
            if a.fetch and r["category"] == "new edition":
                r["category"], r["compared"] = compare_with_listed(r, coverage[(r["cycle"], r["party"])], Path(tmp))
                r["detail"] = r["detail"].replace(" (--fetch compares the text)", "")
            rows.append(r)
    seen = {}
    for r in rows:
        seen.setdefault(r["sha256"], []).append(r["name"])

    counts = ", ".join(f"{c} {sum(r['category'] == c for r in rows)}" for c in ORDER if any(r["category"] == c for r in rows))
    print(f"{len(files)} PDF(s) in {folder}: {counts}.\ndata/manifesto_coverage.csv has {len(coverage)} rows. Nothing was changed.\n")
    for cat in ORDER:
        group = [r for r in rows if r["category"] == cat]
        print(f"== {cat}: {len(group)}")
        if cat == "other document" and not a.all:
            if group:
                print("  not programmes (no programme title or programme words); --all lists them, the CSV has them")
            print()
            continue
        for r in group:
            dup = [n for n in seen[r["sha256"]] if n != r["name"]]
            print(f"  {r['name']}  sha256 {r['sha256'][:8]}…{r['sha256'][-4:]}  {r.get('pages', '?')} pages"
                  + (f", {r['language']}" if r["language"] else "") + (f"  (same file as {', '.join(dup)})" if dup else ""))
            if cat in ("about a programme", "other document"):
                print(f"    party {r['party'] or '?'}; election {r['cycle'] or '?'}" + (f"; {r['detail']}" if cat != "other document" else ""))
                continue
            print(f"    party {r['party'] or '?'}"
                  + (f" ({r['party_evidence']})" if r["party_evidence"] else f" ({r['party_note']})" if r["party_note"] else "")
                  + f"; election {r['cycle'] or '?'}" + (f" ({r['cycle_evidence']})" if r["cycle_evidence"] else ""))
            if r["other_years"]:
                print(f"    also near election words: {r['other_years']} (not in data/cycles.csv)")
            print(f"    {r['detail']}")
            if r.get("compared"):
                print(f"    compared with the listed copy: {r['compared']}")
            if cat in ("new edition", "new programme", "unidentified"):
                print(f"    title: {r.get('title') or '-'}; made {r.get('created') or '?'}; first words: {r['first_line'][:120]}")
        print()

    matched = {(c, p) for (c, p), row in coverage.items() for r in rows
               if r["category"] in ("already covered", "known, not listed")
               and any(hash_matches(r["sha256"], h) for h in hashes_in((row.get("sha256") or "") + " " + (row.get("notes") or "")))}
    matched |= {(r["cycle"], r["party"]) for r in rows if r["category"] == "same text"}
    offered = {(r["cycle"], r["party"]) for r in rows if r["category"] in ("new edition", "new programme")}
    about = {(r["cycle"], r["party"]) for r in rows if r["category"] == "about a programme"}
    print("== coverage rows with no matching PDF in the folder")
    for (c, p), row in sorted(coverage.items()):
        if (c, p) in matched:
            continue
        note = ("a candidate file is listed above" if (c, p) in offered else
                "only articles or web pages about it here" if (c, p) in about else "no file found here")
        kind = "listed from web chapters" if "web chapters" in (row.get("document") or "") and row["status"] == "listed" else row["status"]
        print(f"  {c} {p} ({row['party_name']}): {kind}; {note}")

    if a.csv:
        fields = ["category", "detail", "compared", "name", "sha256", "bytes", "pages", "language", "kind_why", "party", "party_evidence",
                  "party_note", "cycle", "cycle_evidence", "other_years", "title", "author", "created", "first_line", "file"]
        with open(a.csv, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
            w.writeheader()
            w.writerows(sorted(rows, key=lambda r: (ORDER.index(r["category"]), r["name"])))
        print(f"\nWrote {a.csv}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
