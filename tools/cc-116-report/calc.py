#!/usr/bin/env python3
"""CC-116: test what UNESCO's World Heritage Committee decided on the City of Valletta (Decision 47 COM 7B.114).

Fetches (1) the adopted decision page and (2) the Committee's state-of-conservation document WHC/25/47.COM/7B.Add.3
(which holds the draft decision and the Advisory Bodies' analysis), then checks by string comparison:
  - each phrase of the claim against the adopted decision text;
  - that the adopted paragraphs 3-8 are identical to the draft in the document;
  - that the decision text contains no request to inscribe the property on the List of World Heritage in Danger.
Downloads go to tools/cc-116-report/out/ (git-ignored). Results: data/cc-116/checks.csv (source URL, SHA-256,
retrieval date). Run from the repository root. Needs network access and `pdftotext` (poppler-utils).
"""
import csv, datetime as dt, hashlib, html, pathlib, re, subprocess, urllib.request

ROOT = pathlib.Path(__file__).resolve().parents[2]
OUT = pathlib.Path(__file__).resolve().parent / "out"
OUT.mkdir(exist_ok=True)
UA = {"User-Agent": "Mozilla/5.0"}
URL_DEC = "https://whc.unesco.org/en/decisions/8838"
URL_SOC = "https://whc.unesco.org/archive/2025/whc25-47com-7BAdd3-en.pdf"
TODAY = dt.date.today().isoformat()


def get(url, name):
    p = OUT / name
    if not p.exists():
        p.write_bytes(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=120).read())
    return p


def norm(s):
    s = re.sub(r"\s+", " ", s.replace("’", "'").replace("‘", "'").replace("-\n", "-")).strip()
    return re.sub(r"\s+([,;:.])", r"\1", s)


squash = lambda s: re.sub(r"\s+", "", s).lower()
squash_nc = lambda s: squash(s).replace(",", "")


dec_p = get(URL_DEC, "decision_8838.html")
soc_p = get(URL_SOC, "whc25-47com-7BAdd3-en.pdf")
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
raw = dec_p.read_text(errors="ignore")
raw = re.sub(r"<(script|style)[\s\S]*?</\1>", "", raw)
txt = html.unescape(re.sub(r"<[^>]+>", " ", raw))
i = txt.index("The World Heritage Committee,")
j = txt.index("Decision Code", i)
adopted = norm(txt[i:j])
soc = subprocess.run(["pdftotext", "-layout", str(soc_p), "-"], capture_output=True, text=True).stdout
k = soc.index("Draft Decision: 47 COM 7B.114")
m = soc.index("115. Natural and Culturo-Historical Region of Kotor", k)
draft = norm(re.sub(r"State of conservation of properties\s+WHC/25/47\.COM/7B\.Add\.3, p\. \d+\s+inscribed on the World Heritage List", " ",
                    soc[k:m]))
draft = re.sub(r"(?<=[;,:.]) (\d)\. ", r" \1. ", draft)
# draft numbers its paragraphs; the web page does not. Strip the numbers for comparison.
draft_body = norm(re.sub(r"(?<=\s)\d\.\s{2,}|(?<=\s)\d\.\s", " ", draft[draft.index("The World Heritage Committee,"):]))

rows = []
SRC = f"{URL_DEC} ; {URL_SOC}"


def add(check, value, note=""):
    rows.append({"check": check, "value": value, "source": SRC, "retrieved": TODAY, "note": note})


add("SHA-256 of adopted decision page (HTML)", sha(dec_p), URL_DEC)
add("SHA-256 of WHC/25/47.COM/7B.Add.3 (PDF)", sha(soc_p), URL_SOC)
phrases = [
    ("claim: 'do not sufficiently safeguard the setting of the property'",
     "the current planning policies and regulations do not sufficiently safeguard the setting of the property"),
    ("claim: effective height controls within and around the property",
     "to establish effective height controls within and around the property"),
    ("claim: revise the Views and Vistas Analysis (VVA)", "revise the VVA"),
    ("claim: revise the 2006 North Harbour Local Plan", "the 2006 North Harbour Local Plan"),
    ("claim: revise the 2014 Floor Area Ratio policy guide",
     "the 2014 Planning Policy Guide on the Use and Applicability of the Floor Area Ratio"),
    ("claim: revise the 2022 Grand Harbour Local Plan", "the 2022 Grand Harbour Local Plan"),
    ("claim: buffer zone proposal to be further developed", "the draft proposal for the buffer zone be further developed"),
    ("claim: northern boundary across Marsamxett Harbour",
     "delineation of its northern boundary, especially in the area north of the property across Marsamxett Harbour"),
    ("claim: updated report by 1 December 2026",
     "to submit to the World Heritage Centre, by 1 December 2026, an updated report on the state of conservation"),
    ("claim: for the 49th session", "at its 49th session"),
]
for lab, ph in phrases:
    add(lab, "found" if norm(ph) in adopted else "NOT FOUND", f"phrase: {ph}")
add("Committee 'welcomes' the buffer zone proposal's submission (decision para 3)",
    "found" if "Welcomes the submission of the draft Management Plan, the Views and Vistas Analysis (VVA), and a proposal for a buffer zone" in adopted else "NOT FOUND")
paras = re.split(r"(?=\b(?:Having examined|Recalling|Welcomes|Notes with concern|Also requests|Encourages|Finally requests)\b)", adopted)
same = all(squash_nc(p) in squash_nc(draft_body) for p in paras if len(p) > 20)
add("Every paragraph of the adopted decision appears in the draft in WHC/25/47.COM/7B.Add.3 (ignoring commas)",
    "yes" if same else "NO", "string comparison after normalising spaces, commas and paragraph numbers")
add("Adopted text identical to the draft, ignoring spacing and commas", "yes" if squash_nc(adopted) == squash_nc(draft_body) else "no",
    "exact comparison differs by one comma (after 'COM 7B.190' in the recalling paragraph)")
add("Adopted text identical to the draft, exact (ignoring spacing)", "yes" if squash(adopted) == squash(draft_body) else "no",
    "see the previous row")
for term in ("in Danger", "endanger", "delist", "removal", "Danger"):
    add(f"Occurrences of '{term}' in the adopted decision text", len(re.findall(term, adopted, flags=re.I)))
add("Number of planning documents named for revision (VVA + three plans)", 4)
add("Characters in adopted decision text", len(adopted))
with open(ROOT / "data/cc-116/checks.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\r\n"); w.writeheader(); w.writerows(rows)
for r in rows:
    print(f"{r['check'][:95]:95s} {str(r['value'])[:20]}")
