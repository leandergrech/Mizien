#!/usr/bin/env python3
"""CC-092: search log for the PN 2026 programme (Nifs Ġdid). Fetches every chapter's web page and chapter PDF from
pn.org.mt (browser User-Agent; scripts get 403 without one on some days), extracts the text (pdftotext for the PDFs)
and counts the words this check depends on. Writes data/cc-092/pn_programme_search.csv: one row per document with
its URL, retrieval date, SHA-256 and the count of each term (the web pages carry each item twice, in two
layouts, so their counts are doubled). The documents themselves are not committed (copyright).
Needs network and poppler-utils."""
import csv, datetime, hashlib, html, pathlib, re, subprocess, tempfile, unicodedata, urllib.request

ROOT = pathlib.Path(__file__).resolve().parents[2]
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/124.0 Safari/537.36"}
WEB = ["ghawdex", "ambjent", "agrikoltura-u-sajd", "energija-u-ilma", "edukazzjoni-u-hiliet", "ekonomija", "governanza",
       "is-settur-privat", "kultura-u-arti", "malta-fid%e2%80%90dinja", "mobbilta-infrastruttura-u-ppjanar",
       "politika-socjali", "sahha-u-sport", "tnaqqis-fit-taxxi", "turizmu", "zghazagh"]
PDF = ["1-Ekonomija-1", "2-Settur-Privat", "3-Tnaqqis-fit-taxxi", "4-Sahha-u-Sport", "5-Edukazzjoni-u-Hiliet",
       "6-Politika-Socjali", "7-Zghazagh", "8-Trasport-", "9-Energija-u-Ilma", "10-Ghawdex", "11-Turizmu",
       "12-Kultura", "13-Ambjent", "14-Agrikoltura", "15-Governanza", "16-Malta-fid-Dinja"]
# term -> regular expression on NFC text with every hyphen-like character turned into "-"
TERMS = {"afforestazzjoni": r"afforestazzjoni", "siġar/siġra (trees/tree)": r"\bsi[ġg](?:ar|ra)\b",
         "indiġen* (indigenous)": r"indi[ġg]en", "nattiv*/endemi* (native/endemic)": r"\bnattiv|\bendemi",
         "net-zero": r"net-?\s?zero", "xagħri (garrigue)": r"xag[ħh]ri", "karbonju/carbon": r"karbonju|carbon",
         "strateġija (strategy)": r"strate[ġg]ija"}


def norm(t):
    t = unicodedata.normalize("NFC", t)
    return re.sub(r"[‐‑‒–­−]", "-", t).lower()


def web_text(b):
    s = b.decode("utf-8", "replace")
    s = re.sub(r"(?is)<(script|style|noscript|svg)[^>]*>.*?</\1>", " ", s)
    return html.unescape(re.sub(r"<[^>]+>", " ", s))


def pdf_text(b):
    with tempfile.TemporaryDirectory() as td:
        p = pathlib.Path(td) / "c.pdf"
        p.write_bytes(b)
        subprocess.run(["pdftotext", "-layout", str(p), str(p.with_suffix(".txt"))], check=True)
        return p.with_suffix(".txt").read_text(encoding="utf-8", errors="replace")


rows = []
docs = [("web", f"https://pn.org.mt/nifsgdid/{c}/") for c in WEB] + \
       [("pdf", f"https://pn.org.mt/wp-content/uploads/2026/05/{c}.pdf") for c in PDF]
for kind, url in docs:
    b = urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=120).read()
    t = norm(web_text(b) if kind == "web" else pdf_text(b))
    row = {"kind": kind, "url": url, "retrieved": datetime.date.today().isoformat(),
           "sha256": hashlib.sha256(b).hexdigest(), "bytes": len(b)}
    for name, rx in TERMS.items():
        row[name] = len(re.findall(rx, t))
    rows.append(row)
    print(kind, url.rsplit("/", 2)[-2 if kind == "web" else -1], {k: row[k] for k in TERMS})
with open(ROOT / "data" / "cc-092" / "pn_programme_search.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0]))
    w.writeheader()
    w.writerows(rows)
