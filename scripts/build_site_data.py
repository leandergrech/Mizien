#!/usr/bin/env python3
"""Build data/claims.json and docs/data/claims.json from the single source of truth:
claims/*/claim.yml plus data/edges.csv, data/themes.csv and the register of bodies (data/bodies.csv).

Also writes build/site-data.json (git-ignored): the fuller record the Eleventy site
is built from (claim pages, list, feeds), with sources joined to archive/manifest.csv.

Run from the repository root:  python scripts/build_site_data.py
"""
import csv
import json
import pathlib
import re
import shutil
import sys
import unicodedata
from datetime import date, datetime

import yaml

import bodies as register
import connections
import patterns as by_kind
import similarity
import timeline

ROOT = pathlib.Path(__file__).resolve().parent.parent
REPO = "https://github.com/leandergrech/Mizien"

CATEGORY_COLORS = {
    "Land & Trees": "#3d8b5a",
    "Climate & Energy": "#d9772b",
    "Waste": "#9a7b45",
    "Water": "#3c8fbf",
    "Nature & Wildlife": "#9a76c8",
    "Air": "#9fb3c0",
    "Transport": "#c85a3a",
    "Governance & Promises": "#e3a72f",
    "Planning & Housing": "#d16ba5",
    "Noise": "#e8836b",
}
THEME_COLORS = {
    "T1": "#e3a72f", "T2": "#6fcf97", "T3": "#56b4e9", "T4": "#f2994a", "T5": "#bdbdbd", "T6": "#bb86fc", "T7": "#4fc3c8",
    "T8": "#f06292", "T9": "#9fa8da",
}


# colours for topics and themes added later (by the weekly intake routine)
SPARE = ["#4db6ac", "#ff8a65", "#9575cd", "#aed581", "#f48fb1", "#4fc3f7", "#ffd54f", "#a1887f", "#90a4ae", "#ce93d8"]


def spare_colour(key: str) -> str:
    return SPARE[sum(map(ord, key)) % len(SPARE)]


def main() -> int:
    claims, records = [], []
    reg = register.load()
    alias = register.alias_index(reg)
    claim_bodies = {}
    for path in sorted((ROOT / "claims").glob("CC-*/claim.yml")):
        d = yaml.safe_load(path.read_text(encoding="utf-8"))
        records.append(d)
        claim_bodies[d["id"]] = register.resolve(d, reg, alias)[0]
        claims.append({
            "id": d["id"],
            "title": d["title"],
            "category": d["category"],
            "claim": d["claim"]["text"],
            "counter": d.get("counter_evidence", ""),
            "status": d.get("status", "Not started"),
            **({"reply": reply_state(d)} if reply_state(d) in ("not-needed", "not-sought") else {}),
            "verdict": d.get("verdict"),
            "tags": d.get("tags", []),
            **({"subtopic": d["subtopic"]} if d.get("subtopic") else {}),
            **({"location": d["location"]} if d.get("location") else {}),
            "priority": d.get("priority", ""),
            "wording_status": d["claim"].get("wording_status", ""),
            "confidence": d.get("verdict_confidence"),
            "speaker": d["claim"].get("speaker", ""),
            "bodies": claim_bodies[d["id"]],
            **({"subclaims": [{k: s.get(k) for k in ("id", "text", "finding", "rating", "tone")} for s in d["subclaims"]]}
               if d.get("subclaims") else {}),
            **({"pledge": pledge_view(d, reg)} if d.get("pledge") else {}),
            "date": str(d["claim"].get("date") or ""),
            "quote": d["claim"].get("quote", ""),
            "version": d.get("version"),
            **({"last_reviewed": str(d["last_reviewed"])} if d.get("last_reviewed") else {}),
            "outputs": {k: f"claim-files/{d['id']}/{pathlib.Path(v).name}" for k, v in (d.get("outputs") or {}).items()},
            "record": f"{REPO}/blob/main/claims/{d['id']}/claim.yml",
        })
    # Claims with similar wording (scripts/similarity.py), with the shared words, for the site's "Find related".
    for cid, near in similarity.similar(claims).items():
        next(c for c in claims if c["id"] == cid)["similar"] = near
    cats = []
    for c in claims:
        if c["category"] not in [x["name"] for x in cats]:
            cats.append({"name": c["category"], "color": CATEGORY_COLORS.get(c["category"]) or spare_colour(c["category"])})

    with open(ROOT / "data" / "edges.csv", newline="", encoding="utf-8") as f:
        edges = [{"from": r["From"], "to": r["To"], "theme": r["Theme ID"], "link_type": r["Link type"],
                  "strength": r["Strength"]} for r in csv.DictReader(f)]
    with open(ROOT / "data" / "themes.csv", newline="", encoding="utf-8") as f:
        themes = [{"id": r["Theme ID"], "name": r["Theme"], "color": THEME_COLORS.get(r["Theme ID"]) or spare_colour(r["Theme ID"]),
                   "dashed": r["Strength"].startswith(("Weak", "Pattern")), "link_type": r["Link type"],
                   "strength": r["Strength"], "description": r["What connects them"],
                   "members": [x.strip() for x in r["Linked claim IDs"].split(",")]} for r in csv.DictReader(f)]

    profiles = connections.profiles(claim_bodies, reg, edges, records)
    # The map needs each body's place in the register and its links to other bodies (see scripts/connections.py).
    map_bodies = [{**{k: p[k] for k in ("id", "name", "kind", "type", "parent", "role")},
                   "links": [{"id": l["id"], "named": len(l["named_with"]), "pairs": l["pairs"], "themes": list(l["themes"])}
                             for l in p["links"]]} for p in profiles.values()]
    body_types = [{"id": k, "label": v, "colour": register.TYPE_COLOURS[k]} for k, v in register.TYPES.items()]
    pledge_labels = [{"name": n, "meaning": m, "slug": "pledge-" + slug(n), "colour": PLEDGE_COLOURS.get(n, "#716f8d")}
                     for n, m in pledge_label_list()]
    # Overlapping pledges, for the map's pledge network (each pair once, with the reasons).
    pledge_links = [{"a": x["id"], "b": o["id"], "why": o["why"]}
                    for x in pledge_network(records, reg, connections.adjacency(edges)) for o in x["overlaps"] if x["id"] < o["id"]]
    out = {"categories": cats, "claims": claims, "edges": edges, "themes": themes, "bodies": map_bodies,
           "body_types": body_types, "pledge_labels": pledge_labels, "pledge_links": pledge_links}
    text = json.dumps(out, ensure_ascii=False, indent=2)
    for target in (ROOT / "data" / "claims.json", ROOT / "docs" / "data" / "claims.json"):
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8")
    preview = ROOT / "docs" / "design-preview.html"
    if preview.is_file():
        page = preview.read_text(encoding="utf-8")
        page, count = re.subn(
            r'(<script id="map-data" type="application/json">).*?(</script>)',
            lambda m: m.group(1) + text.replace("<", "\\u003c") + m.group(2),
            page, count=1, flags=re.S,
        )
        if count:
            preview.write_text(page, encoding="utf-8")
    # GitHub Pages publishes only /docs. Copy claim deliverables there so the
    # same-page viewer and explicit downloads use the same-origin site files.
    files_root = ROOT / "docs" / "claim-files"
    for row in claims:
        claim_path = ROOT / "claims" / row["id"]
        for value in (row.get("outputs") or {}).values():
            filename = pathlib.Path(value).name
            source = claim_path / filename
            if source.is_file():
                dest = files_root / row["id"] / filename
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source, dest)
    write_site_data(records, out, reg, claim_bodies, profiles)
    print(f"Wrote {len(claims)} claims, {len(edges)} edges, {len(themes)} themes.")
    return 0


# ---------------------------------------------------------------- build/site-data.json for the Eleventy site

SITE_DATA = ROOT / "build" / "site-data.json"
PREVIEWS = ROOT / "build" / "claim-previews"     # small flyer previews, copied into the site as claim-files/
VERDICT_RATING = {"Supported": 5, "Largely supported": 4, "Not substantiated": 3, "Misleading": 2, "Contradicted": 1}
STATUS_LABELS = {
    "Not started": "Not yet checked",
    "In progress": "Check in progress",
    "Drafted": "Draft: right of reply pending",
    "Right of reply": "Sent to the body concerned for reply",
    "Published": "Published",
}
OUTPUT_LABELS = {"report": "Full report", "report_pdf": "Full report", "flyer_pdf": "Flyer", "flyer_png": "Flyer image",
                 "document": "Document", "appendix": "Appendix"}


def slug(text: str) -> str:
    """ASCII slug that keeps Maltese letters readable: ħ -> h, ż -> z, għ -> gh."""
    text = (text or "").replace("ħ", "h").replace("Ħ", "H").replace("&", " and ")
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def jsonable(x):
    """YAML gives dates as date objects; the site wants plain strings."""
    if isinstance(x, dict):
        return {k: jsonable(v) for k, v in x.items()}
    if isinstance(x, list):
        return [jsonable(v) for v in x]
    if isinstance(x, (date, datetime)):
        return x.isoformat()
    return x


def norm_url(url: str) -> str:
    url = re.sub(r"^https?://(www\.)?", "", (url or "").strip(), flags=re.I)
    host, _, rest = url.partition("/")
    return (host.lower() + ("/" + rest if rest else "")).rstrip("/")


def load_archive() -> dict:
    rows = {}
    path = ROOT / "archive" / "manifest.csv"
    if path.is_file():
        with open(path, newline="", encoding="utf-8") as f:
            for r in csv.DictReader(f):
                key = norm_url(r.get("url"))
                if key and (key not in rows or (r.get("archived_url") and not rows[key].get("archived_url"))):
                    rows[key] = r
    return rows


def archive_entry(url: str, manifest: dict) -> dict:
    """How a cited source is preserved: archived (snapshot link), hashed (fetched and hashed, no
    snapshot), offline (no public URL, e.g. a PDF supplied by the maintainer) or missing."""
    if not (url or "").lower().startswith("http"):
        return {"state": "offline"}
    r = manifest.get(norm_url(url))
    if not r:
        return {"state": "missing"}
    snapshot = (r.get("archived_url") or "").strip()
    if snapshot.startswith("http://"):
        snapshot = "https://" + snapshot[len("http://"):]
    return {
        "state": "archived" if snapshot else ("hashed" if r.get("sha256") else "missing"),
        "url": snapshot or None,
        "sha256": r.get("sha256") or None,
        "retrieved_utc": r.get("retrieved_utc") or None,
    }


PROCESS_NOTE = re.compile(r"right of reply|must not be published|maintainer", re.I)


def public_limitations(caveats: str) -> str:
    """claim.yml 'caveats' mixes the check's limitations with editorial process notes (right-of-reply
    status, publication holds). The site shows the limitations; right of reply has its own section.
    Until claim.yml has a separate 'limitations' field, sentences about process are left out here."""
    sentences = re.split(r"(?<=[.!?])\s+(?=[A-Z'\u2018\u201c(])", (caveats or "").strip())
    return " ".join(s for s in sentences if s and not PROCESS_NOTE.search(s))


def bold_table(md_file: str) -> list:
    """Rows of a methodology table whose first cell is bold: [(name, meaning), ...]."""
    text = (ROOT / "methodology" / md_file).read_text(encoding="utf-8")
    return re.findall(r"^\|\s*\*\*(.+?)\*\*\s*\|\s*(.+?)\s*\|\s*$", text, flags=re.M)


def pledge_label_list() -> list:
    """[(label, meaning)] from the 'Pledges' section of methodology/verdict-scale.md (maintainer decision, 5 Oct 2026)."""
    return [(m.group(1), m.group(2)) for m in (re.match(r"\*\*(.+?)\*\*:\s*(.+)", x) for x in section_items("verdict-scale.md", "Pledges")) if m]


def section_items(md_file: str, heading: str) -> list:
    """Bulleted or numbered items under '## heading' in a methodology file, inline Markdown kept."""
    text = (ROOT / "methodology" / md_file).read_text(encoding="utf-8")
    m = re.search(r"^## " + re.escape(heading) + r"\s*$(.*?)(?=^## |\Z)", text, flags=re.M | re.S)
    if not m:
        return []
    items = re.findall(r"^(?:- |\d+\. )(.+(?:\n(?!- |\d+\. )[^\n]+)*)", m.group(1), flags=re.M)
    return [re.sub(r"\s+", " ", x).strip() for x in items]


def flyer_preview(cid: str, outputs: dict):
    """A 600 px wide WebP of the flyer for the claim page (the full PNG stays a download). Returns its site path."""
    name = outputs.get("flyer_png")
    src = ROOT / "claims" / cid / pathlib.Path(name).name if name else None
    if not src or not src.is_file():
        return None
    from PIL import Image  # Pillow is installed with reportlab
    dest = PREVIEWS / cid / "flyer-preview.webp"
    if not dest.is_file() or dest.stat().st_mtime < src.stat().st_mtime:
        dest.parent.mkdir(parents=True, exist_ok=True)
        im = Image.open(src).convert("RGB")
        im.thumbnail((600, 1000))
        im.save(dest, "WEBP", quality=82, method=6)
    w, h = Image.open(dest).size
    return {"url": f"/claim-files/{cid}/flyer-preview.webp", "width": w, "height": h}


def label_of(d: dict):
    """What a claim is rated: its verdict, or for a pure pledge (no verdict) its pledge label. (label, slug, kind)"""
    if d.get("verdict"):
        return d["verdict"], slug(d["verdict"]), "verdict"
    status = (d.get("pledge") or {}).get("status")
    if status:
        return status, "pledge-" + slug(status), "pledge"
    return None, None, None


# Right of reply (maintainer decision, 5 October 2026): sought only when a check finds a claim Not substantiated,
# Misleading or Contradicted (for pledges: Not measurable, Off track or Missed). A check that supports a claim needs
# none, and says so even if its record also says sought: false. right_of_reply.sought: false records a decision not
# to seek one where it would otherwise apply.
REPLY_VERDICTS = {"Not substantiated", "Misleading", "Contradicted"}
REPLY_PLEDGES = {"Not measurable", "Off track", "Missed"}


def reply_state(d: dict):
    """Where a check's right of reply stands: received, sent, not-sought, on-hold, pending, not-needed, or None (no verdict).
    on-hold: a reply would be needed but rests on a document not yet read (right_of_reply.on_hold says which)."""
    ror = d.get("right_of_reply") or {}
    if ror.get("response") or ror.get("response_date"):
        return "received"
    if ror.get("sent"):
        return "sent"
    verdict, pledge = d.get("verdict"), (d.get("pledge") or {}).get("status")
    if not (verdict or pledge):
        return "not-sought" if ror.get("sought") is False else None
    if not (verdict in REPLY_VERDICTS or pledge in REPLY_PLEDGES):
        return "not-needed"
    if ror.get("sought") is False:
        return "not-sought"
    return "on-hold" if ror.get("on_hold") else "pending"


def status_label(d: dict) -> str:
    if d.get("status") == "Drafted":
        return {"not-sought": "Draft: right of reply not sought", "on-hold": "Draft: right of reply on hold",
                "not-needed": "Draft: no right of reply needed"}.get(reply_state(d), STATUS_LABELS["Drafted"])
    return STATUS_LABELS.get(d.get("status"), d.get("status"))


def claim_ref(d: dict) -> dict:
    """The few fields a list of claims needs: number, title and verdict (or pledge label)."""
    label, label_slug, kind = label_of(d)
    return {"id": d["id"], "title": d["title"], "path": f"/claims/{d['id']}/", "verdict": d.get("verdict"),
            "verdict_slug": slug(d["verdict"]) if d.get("verdict") else None, "category": d["category"],
            "status": d.get("status"), "date": str(d["claim"].get("date") or ""),
            "label": label, "label_slug": label_slug, "label_kind": kind, "reply": reply_state(d)}


PLEDGE_COLOURS = {   # pledge labels (methodology/verdict-scale.md, Pledges): a family of their own, apart from the verdict hues
    "Not measurable": "#716f8d", "Not yet due": "#5c7689", "On track": "#337f71", "Off track": "#ae5d33",
    "Met": "#23705f", "Missed": "#7c2d4a",
}


def pledge_view(d: dict, reg: dict) -> dict | None:
    """A pledge block ready to show: the label with its as-of date, who made it, when, in what, and by when."""
    p = d.get("pledge")
    if not p:
        return None
    fmt = lambda v: (timeline.parse_date(v) or {}).get("label") if v is not None else None
    occasion = p.get("occasion") or str(p.get("vehicle") or "").split(",")[0].strip()
    return {"status": p.get("status"), "slug": "pledge-" + slug(p.get("status") or ""), "colour": PLEDGE_COLOURS.get(p.get("status")),
            "as_of": fmt(p.get("as_of")), "as_of_iso": str(p.get("as_of") or ""), "made_on": fmt(p.get("made_on")),
            "deadline": fmt(p.get("deadline")), "term_end": fmt(p.get("term_end")), "target": p.get("target"),
            "vehicle": p.get("vehicle"), "occasion": occasion, "note": p.get("note"),
            "made_by": [body_ref(reg[b]) for b in p.get("made_by") or [] if b in reg],
            "made_by_ids": [b for b in p.get("made_by") or [] if b in reg],
            "pure": not d.get("verdict"), "overlaps": [str(x) for x in p.get("overlaps") or []]}


def pledge_network(records: list, reg: dict, adj) -> list:
    """Every pledge with what links it: who made it, when (the occasion), what (topic), and overlapping pledges."""
    pledges = {d["id"]: d for d in records if d.get("pledge")}
    out = []
    for cid, d in pledges.items():
        v = pledge_view(d, reg)
        overlaps = {}
        for o in v["overlaps"]:
            if o in pledges and o != cid:
                overlaps.setdefault(o, []).append("listed as overlapping")
        for o, themes in adj.get(cid, {}).items():
            if o in pledges:
                overlaps.setdefault(o, []).append("share a theme")
        for o, x in pledges.items():
            if o != cid and x["category"] == d["category"] and x.get("subtopic") and x.get("subtopic") == d.get("subtopic"):
                overlaps.setdefault(o, []).append(f"same subtopic ({d['subtopic']})")
        for o in [o for o, x in pledges.items() if o != cid and cid in [str(y) for y in (x["pledge"].get("overlaps") or [])]]:
            overlaps.setdefault(o, []).append("listed as overlapping")
        out.append({**claim_ref(d), "pledge": v, "subtopic": d.get("subtopic"),
                    "overlaps": [{**claim_ref(pledges[o]), "why": sorted(set(w))} for o, w in sorted(overlaps.items())]})
    return sorted(out, key=lambda x: x["id"])


def body_ref(b: dict) -> dict:
    return {"id": b["id"], "name": b["name"], "kind": b["kind"], "role": b["role"], "path": f"/bodies/{b['id']}/"}


def claim_connections(cid: str, d: dict, by_id: dict, adj, out: dict, reg: dict, claim_bodies: dict, profiles: dict,
                      patterns: dict) -> dict:
    """Everything that connects one claim to others: pattern tags, indirect links (second and third degree) and
    other claims by the same bodies. Direct links are the claim's `links`."""
    ind = connections.indirect(cid, adj)
    names = {t["id"]: t["name"] for t in out["themes"]}
    step = lambda p: [{"id": x, "title": by_id[x]["title"], "theme": t, "theme_name": names.get(t, t)} for x, t in p]
    second = [{**claim_ref(by_id[x["id"]]), "via": [step(p) for p in x["paths"]]} for x in ind[2]]
    third = [{**claim_ref(by_id[x["id"]]), "via": [step(x["paths"][0])]} for x in ind[3]]
    same, listed = [], {cid}
    for u in connections.units(claim_bodies[cid], reg):
        for b in [u] + ([reg[u]["parent"]] if reg[u]["kind"] == "person" and reg[u]["parent"] else []):
            others = [x for x in profiles[b]["claims"] if x not in listed] if b in profiles else []
            if others:
                same.append({"body": body_ref(reg[b]), "claims": [claim_ref(by_id[x]) for x in others]})
                listed.update(others)
    tags = []
    for t in d.get("tags") or []:
        others = [x for x in by_id.values() if x["id"] != cid and t in (x.get("tags") or [])]
        tags.append({"tag": t, "meaning": patterns.get(t), "claims": [claim_ref(x) for x in others]})
    return {"second": second, "third": third, "same_body": same, "patterns": tags}


def claim_timeline(cid, d, by_id, reg, claim_bodies, profiles, sources, intake, today):
    """The claim's dated events (scripts/timeline.py), with statements by the same body on the same topic."""
    ev = timeline.claim_events(d, sources, intake.get(cid))
    said = timeline.parse_date(d["claim"].get("date"))
    offices, seen = [], set()
    for u in connections.units(claim_bodies[cid], reg):
        o = register.org_of(u, reg)
        if o not in offices:
            offices.append(o)
    for o in offices:
        for x in (profiles.get(o) or {}).get("claims", []):
            other = by_id[x]
            when = timeline.parse_date(other["claim"].get("date"))
            if x == cid or x in seen or other["category"] != d["category"] or not when:
                continue
            seen.add(x)
            rel = ("Statement" if not said or when["mid"] == said["mid"]
                   else "Earlier statement" if when["mid"] < said["mid"] else "Later statement")
            tree = set(connections.descendants(o, reg))
            who = [reg[u]["name"] for u in connections.units(claim_bodies[x], reg) if u in tree] or [reg[o]["name"]]
            ev.append({"when": when, "kind": "same-body", "label": f"{rel} by {' and '.join(who)} on {d['category']}",
                       "text": "", "url": None, "claim": claim_ref(other)})
    return [{**{k: v for k, v in e.items() if k != "when"}, "date": e["when"]["label"], "iso": e["when"]["iso"],
             "year": e["when"]["iso"][:4], "mid": e["when"]["mid"], "future": e["when"]["mid"] > today}
            for e in timeline.sort_events(ev)]


def lanes(claims: list, by_id: dict) -> dict:
    """A body's statements on a time axis, one lane per topic, plus the undated ones and the topics it returned to."""
    dated, undated = {}, []
    for c in claims:
        when = timeline.parse_date(by_id[c]["claim"].get("date"))
        ref = claim_ref(by_id[c])
        if when:
            dated.setdefault(by_id[c]["category"], []).append({**ref, "mid": when["mid"], "date": when["label"],
                                                               "rough": when["precision"] == "year" or when["approx"]})
        else:
            undated.append(ref)
    ax = timeline.axis([i["mid"] for v in dated.values() for i in v])
    out = []
    for topic in sorted(dated, key=lambda t: (-len(dated[t]), t)):
        placed, rows = timeline.place(dated[topic], ax)
        out.append({"topic": topic, "items": placed, "rows": rows})
    threads = [{"topic": l["topic"], "claims": sorted(l["items"], key=lambda i: i["mid"])} for l in out if len(l["items"]) > 1]
    return {"axis": ax, "lanes": out, "undated": undated, "threads": threads}


def write_site_data(records: list, out: dict, reg: dict, claim_bodies: dict, profiles: dict) -> None:
    import thumbnails  # scripts/thumbnails.py: one scene per subtopic, a specific thumbnail per researched claim
    manifest = load_archive()
    thumbs = thumbnails.render_all(records, {c["name"]: c["color"] for c in out["categories"]}, ROOT / "build" / "thumbs")
    titles = {d["id"]: d["title"] for d in records}
    by_id = {d["id"]: d for d in records}
    theme_names = {t["id"]: t["name"] for t in out["themes"]}
    adj = connections.adjacency(out["edges"])
    pattern_meanings = dict(bold_table("pattern-tags.md"))
    sources_ev, intake = timeline.source_events(), timeline.intake_dates()
    today = date.today().isoformat()
    sims = {c["id"]: c.get("similar", []) for c in out["claims"]}   # similar wording (scripts/similarity.py)
    site_claims = []
    for d in records:
        cid, rec = d["id"], jsonable(d)
        files = []
        for key, value in (d.get("outputs") or {}).items():
            name = pathlib.Path(value).name
            src = ROOT / "claims" / cid / name
            files.append({"key": key, "label": OUTPUT_LABELS.get(key, key.replace("_", " ").capitalize()), "name": name,
                          "url": f"/claim-files/{cid}/{name}", "type": src.suffix.lstrip(".").upper(),
                          "bytes": src.stat().st_size if src.is_file() else None})
        links = []
        for e in out["edges"]:
            if cid in (e["from"], e["to"]):
                other = e["to"] if e["from"] == cid else e["from"]
                links.append({"id": other, "title": titles.get(other, other), "theme_id": e["theme"],
                              "theme": theme_names.get(e["theme"], e["theme"]), "link_type": e["link_type"],
                              "strength": e["strength"]})
        report = ROOT / "claims" / cid / "report.html"   # web version of the report (tools/report_html.py)
        preview = flyer_preview(cid, d.get("outputs") or {})
        site_claims.append({
            **rec,
            "path": f"/claims/{cid}/",
            "status_label": status_label(d),
            "reply": reply_state(d),
            "is_draft": d.get("status") != "Published",
            "limitations": public_limitations(d.get("caveats")),
            "rating": VERDICT_RATING.get(d.get("verdict")),
            **dict(zip(("label", "label_slug", "label_kind"), label_of(d))),
            "pledge_view": pledge_view(d, reg),
            "verdict_slug": slug(d["verdict"]) if d.get("verdict") else None,
            "category_slug": slug(d["category"]),
            "sources": [{**jsonable(s), "archive": archive_entry(s.get("url"), manifest)}
                        for s in (d["claim"].get("sources") or [])],
            "files": files,
            "report_html": report.read_text(encoding="utf-8") if report.is_file() else None,
            "flyer_preview": preview,
            "thumb": thumbs.get(cid),
            "links": links,
            "similar": [{**claim_ref(by_id[x["id"]]), "score": x["score"], "terms": x["terms"]} for x in sims.get(cid, []) if x["id"] in by_id],
            "bodies": [{**body_ref(reg[b]), "parent": body_ref(reg[reg[b]["parent"]]) if reg[b]["parent"] else None}
                       for b in connections.units(claim_bodies[cid], reg)],
            "connections": claim_connections(cid, d, by_id, adj, out, reg, claim_bodies, profiles, pattern_meanings),
            "timeline": claim_timeline(cid, d, by_id, reg, claim_bodies, profiles, sources_ev, intake, today),
            "corrections": [{"date": e["when"]["label"], "iso": e["when"]["iso"], "label": e["label"], "text": e["text"],
                             "step": e["step"], "version": e["version"]}
                            for e in timeline.history_events(d) if e["kind"] == "correction"],
            "record_url": f"{REPO}/blob/main/claims/{cid}/claim.yml",
        })
    # Updates for the feeds: steps of each check, replies and curated events, newest first.
    updates = sorted(({**{k: e[k] for k in ("label", "text", "url", "date", "iso", "mid", "kind")}, "claim": claim_ref(by_id[c["id"]])}
                      for c in site_claims for e in c["timeline"]
                      if e["kind"] in ("check", "correction", "reply", "curated") and not e["future"]),
                     key=lambda u: (u["mid"], u["claim"]["id"]), reverse=True)
    body_pages = []
    for bid, p in profiles.items():
        b = reg[bid]
        links = [{**body_ref(reg[l["id"]]), "type": reg[l["id"]]["type"], "named_with": [claim_ref(by_id[x]) for x in l["named_with"]],
                  "themes": [{"id": t, "name": theme_names.get(t, t),
                              "pairs": [[claim_ref(by_id[a]), claim_ref(by_id[z])] for a, z in pairs]}
                             for t, pairs in l["themes"].items()], "pairs": l["pairs"]} for l in p["links"]]
        body_pages.append({
            **body_ref(b), "type": b["type"], "type_label": register.TYPES[b["type"]], "note": b["note"],
            "parent": body_ref(reg[b["parent"]]) if b["parent"] else None,
            "ancestors": [body_ref(reg[x]) for x in reversed(connections.lineage(bid, reg)[1:])],
            "people": [body_ref(reg[x]) for x in p["people"]], "offices": [body_ref(reg[x]) for x in p["offices"]],
            "claims": [{**claim_ref(by_id[c]), "by": [body_ref(reg[x]) for x in connections.units(claim_bodies[c], reg)]}
                       for c in p["claims"]],
            "direct": p["direct"], "verdicts": p["verdicts"], "topics": p["topics"], "patterns": p["patterns"],
            "links": links,
            "time": lanes(p["claims"], by_id),
            "updates": [u for u in updates if u["claim"]["id"] in set(p["claims"])][:50],
        })
    body_order = list(register.TYPES)
    body_pages.sort(key=lambda b: (body_order.index(b["type"]), b["kind"] == "person", b["name"].lower()))
    data = {
        "claims": site_claims,
        "bodies": body_pages,
        "body_types": out["body_types"],
        "updates": updates[:100],
        # The public log of changes to checks (the Corrections page): every version, correction and clarification,
        # dated when the research was done.
        "changes": sorted(({"date": e["when"]["label"], "iso": e["when"]["iso"], "step": e["step"], "label": e["label"],
                            "text": e["text"], "claim": claim_ref(d), "fix": e["kind"] == "correction",
                            "verdict": e["verdict"]}
                           for d in records for e in timeline.history_events(d) if e["step"] in ("version", "correction", "clarification")),
                          key=lambda x: (x["iso"], x["claim"]["id"], x["label"]), reverse=True),
        "by_kind": by_kind.build(records, claim_bodies, reg, out["themes"], [n for n, _ in bold_table("pattern-tags.md")],
                                 [n for n, _ in bold_table("verdict-scale.md")], [c["name"] for c in out["categories"]], claim_ref,
                                 [n for n, _ in pledge_label_list()]),
        "pledges": pledge_network(records, reg, adj),
        "pledge_labels": out["pledge_labels"],
        "theme_bridges": [{**x, "a_name": theme_names.get(x["a"]), "b_name": theme_names.get(x["b"]),
                           "claims": [claim_ref(by_id[c]) for c in x["claims"]]} for x in connections.bridges(out["themes"])],
        "categories": [{**c, "slug": slug(c["name"])} for c in out["categories"]],
        "themes": out["themes"],
        "verdicts": [{"name": n, "meaning": m, "rating": VERDICT_RATING.get(n), "slug": slug(n)}
                     for n, m in bold_table("verdict-scale.md")],
        "grades": [{"grade": g, "meaning": m} for g, m in bold_table("evidence-grades.md")],
        "patterns": [{"name": n, "meaning": m} for n, m in bold_table("pattern-tags.md")],
        "confidence": [{"level": m.group(1), "meaning": m.group(2)} for m in
                       (re.match(r"\*\*(.+?)\*\*:\s*(.+)", x) for x in section_items("verdict-scale.md", "Confidence")) if m],
        "verdict_rules": section_items("verdict-scale.md", "Rules"),
        "source_order": section_items("evidence-grades.md", "Source order"),
    }
    SITE_DATA.parent.mkdir(parents=True, exist_ok=True)
    SITE_DATA.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")


if __name__ == "__main__":
    sys.exit(main())
