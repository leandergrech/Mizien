#!/usr/bin/env python3
"""Publish each claim's report as web HTML, from the same content as its PDF.

Runs a claim's tools/cc-NNN-report/build_report.py with the PDF step intercepted, takes the report content
(the reportlab "story") and writes:

    claims/CC-NNN/report.html          semantic HTML fragment, shown on the claim page
    claims/CC-NNN/report-figures/      the report's figures, taken from the published report.pdf

Figures come from the committed PDF (pdfimages), so the web version shows exactly what the PDF shows and
the figure scripts (some need satellite data or GIS libraries) do not have to be re-run. A check compares the
PDF's words with the HTML's and fails if more than a few are missing.

Usage, from the repository root:
    python tools/report_html.py CC-003 CC-004      # selected claims
    python tools/report_html.py --all              # every claim with tools/cc-NNN-report/build_report.py
    python tools/report_html.py --all --warn       # as CI runs it: problems are warnings, exit code 0
Needs poppler-utils (pdfimages, pdftotext) and the report fonts (Liberation, DejaVu). The outputs are build
products (git-ignored); CI regenerates them on every build, and `npm run build` does too.
"""
import html
import io
import os
import pathlib
import re
import runpy
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
TOOLS = ROOT / "tools"
sys.path.insert(0, str(TOOLS))

import PIL.Image  # noqa: E402
from reportlab.platypus import (BaseDocTemplate, CondPageBreak, Flowable, Image, KeepTogether,  # noqa: E402
                                PageBreak, Paragraph, Spacer, Table)

import mizien_report  # noqa: E402

VERDICTS = ["Supported", "Largely supported", "Not substantiated", "Misleading", "Contradicted"]

# Report palette (tools/mizien_report.py) -> CSS class suffix; the site stylesheet defines the colours.
PALETTE = {"#14452f": "green", "#7fa88b": "sage", "#e6efe8": "pale", "#e3a72f": "amber", "#fbf1d9": "amberpale",
           "#b5483a": "red", "#f7e4e0": "redpale", "#2b3a42": "slate", "#8a9399": "grey", "#eef0f1": "greypale",
           "#f6f4ee": "cream", "#d9772b": "orange", "#fbe9da": "orangepale", "#3c6e8f": "blue", "#e3edf3": "bluepale",
           "#2e7d4f": "greenc", "#bfd6c5": "lightgreen", "#8db36b": "lime", "#c85a3a": "brick", "#8e2f25": "maroon",
           "#ffffff": "white", "#5f6b71": "grey"}   # #5f6b71: the PDF's darker grey (pledge "Not measurable", default chip)


PLEDGE_HEX = {"#" + c.hexval()[2:].upper() for c in mizien_report.PLEDGE_COLS}


def kc(hexcol):
    return PALETTE.get((hexcol or "").lower(), "other")


# ------------------------------------------------------------------ capture the story without building the PDF
class Captured(Exception):
    pass


CAPTURE = {}


def _capture_report(R):
    CAPTURE["story"], CAPTURE["report"] = R.story, R
    raise Captured


def _capture_build(self, flowables, *a, **k):
    CAPTURE["story"] = flowables
    raise Captured


_open = PIL.Image.open


def _lenient_open(fp, *a, **k):
    """Figure scripts write tools/*/out/*.png, which is not committed; fig() only needs a size here."""
    if isinstance(fp, (str, os.PathLike)) and not os.path.exists(fp):
        return PIL.Image.new("RGB", (1600, 900), "white")
    return _open(fp, *a, **k)


def capture(claim_id):
    script = TOOLS / f"{claim_id.lower()}-report" / "build_report.py"
    if not script.is_file():
        raise SystemExit(f"{claim_id}: no {script.relative_to(ROOT)}")
    CAPTURE.clear()
    saved = (mizien_report.build_report, BaseDocTemplate.build, PIL.Image.open)
    mizien_report.build_report, BaseDocTemplate.build, PIL.Image.open = _capture_report, _capture_build, _lenient_open
    cwd = os.getcwd()
    try:
        os.chdir(script.parent)
        sys.path.insert(0, str(script.parent))
        runpy.run_path(str(script), run_name="__main__")
    except Captured:
        pass
    finally:
        os.chdir(cwd)
        sys.path.remove(str(script.parent))
        mizien_report.build_report, BaseDocTemplate.build, PIL.Image.open = saved
    if "story" not in CAPTURE:
        raise SystemExit(f"{claim_id}: the build script did not reach the PDF step")
    return CAPTURE["story"], CAPTURE.get("report")


# ------------------------------------------------------------------ reportlab paragraph markup -> HTML
def inline(text):
    """Reportlab paragraph markup to HTML inline markup."""
    t = text or ""
    t = re.sub(r"</?font\b[^>]*>", "", t)
    t = re.sub(r"<link\s+href=\"([^\"]*)\"[^>]*>", r'<a href="\1">', t)
    t = t.replace("</link>", "</a>")
    t = re.sub(r"<a\s+href=\"([^\"]*)\"[^>]*>", r'<a href="\1">', t)
    t = t.replace("<super>", "<sup>").replace("</super>", "</sup>")
    t = t.replace("<strike>", "<s>").replace("</strike>", "</s>")
    t = re.sub(r"<br\s*/?>", "<br>", t)
    t = re.sub(r"</?(para|span)\b[^>]*>", "", t)
    t = re.sub(r"<(seq|onDraw|index|img)\b[^>]*/?>", "", t)
    t = re.sub(r"&(?!#?\w+;)", "&amp;", t)      # reportlab tolerates a bare "&"; HTML does not
    return t.strip()


def text_of(x):
    """Inline HTML for a cell value: Paragraph, string, or list of them."""
    if x is None:
        return ""
    if isinstance(x, str):
        return html.escape(x)
    if isinstance(x, Paragraph):
        return inline(x.text)
    if isinstance(x, (list, tuple)):
        return " ".join(filter(None, (text_of(i) for i in x)))
    return Renderer().block(x)


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", re.sub(r"<[^>]+>", "", s).lower()).strip("-")


def verdict_slug(v):
    return slug(v) if v else "none"


def pledge_style(label):
    """Inline colours for a pledge label (the PDF's PLEDGE_COLS), as the --v / --v-ink pair the site styles use."""
    col = "#" + mizien_report.PLEDGE_COLS[mizien_report.PLEDGES.index(label)].hexval()[2:].upper()
    ink = "#ffffff"
    return f"--v: {col}; --v-ink: {ink}"


# ------------------------------------------------------------------ story -> HTML
class Renderer:
    def __init__(self, figures=None):
        self.figures = figures if figures is not None else []   # web paths, in PDF order
        self.fig_n = 0
        self.out = []

    # blocks that need grouping (bullets, references)
    def render(self, story):
        out, group, kind = [], [], None

        def flush():
            nonlocal group, kind
            if group:
                tag = "ol" if kind == "ref" else "ul"
                cls = "refs" if kind == "ref" else "bullets"
                out.append(f'<{tag} class="{cls}">' + "".join(group) + f"</{tag}>")
            group, kind = [], None

        story = list(story)
        i = 0
        while i < len(story):
            f = story[i]
            i += 1
            if self.is_figure(f):                       # a figure and the caption paragraph after it
                j = i
                while j < len(story) and isinstance(story[j], Spacer):
                    j += 1
                cap = story[j] if j < len(story) and isinstance(story[j], Paragraph) and story[j].style.name == "cap" else None
                if cap is not None:
                    i = j + 1
                flush()
                out.append(self.figure(inline(cap.text) if cap is not None else None))
                continue
            k, item = self.list_item(f)
            if k:
                if kind != k:
                    flush()
                kind = k
                group.append(item)
                continue
            flush()
            h = self.block(f)
            if h:
                out.append(h)
        flush()
        return "\n".join(out)

    @staticmethod
    def is_figure(f):
        mz = getattr(f, "_mz", None)
        return (mz and mz[0] == "fig") or (isinstance(f, Image) and not mz)

    def list_item(self, f):
        mz = getattr(f, "_mz", None)
        if mz and mz[0] == "ref":
            _, n, t, u = mz
            link = f' <a href="{html.escape(u)}">{html.escape(u)}</a>' if u else ""
            return "ref", f'<li id="ref-{html.escape(str(n))}"><span class="ref-n">[{n}]</span> {inline(t)}{link}</li>'
        if isinstance(f, Paragraph) and f.style.name == "bul":
            return "bul", "<li>" + re.sub(r"^\s*(•|&bull;)\s*", "", inline(f.text)) + "</li>"
        return None, None

    def block(self, f):
        if f is None or isinstance(f, (Spacer, PageBreak, CondPageBreak)):
            return ""
        if isinstance(f, (list, tuple)):
            return self.render(f)
        mz = getattr(f, "_mz", None)
        if mz:
            return getattr(self, "mz_" + mz[0])(*mz[1:])
        name = type(f).__name__
        if name == "SectionHeading":
            num, title = getattr(f, "num", None), getattr(f, "title", "")
            hid = f"section-{num}" if num else slug(title)
            n = f'<span class="sec-n">{num}</span> ' if num else ""
            return f'<h2 id="{hid}">{n}{html.escape(title)}</h2>'
        if name == "VerdictMeter":
            return self.meter(getattr(f, "active", None), getattr(f, "scale", "verdict"))
        if isinstance(f, Paragraph):
            return self.para(f)
        if isinstance(f, KeepTogether):
            return self.render(getattr(f, "_content", []))
        if isinstance(f, Image):
            return self.figure()
        if isinstance(f, Table):
            return self.table_generic(f)
        if isinstance(f, Flowable) and type(f).__name__ in ("NextPageTemplate", "ActionFlowable", "Indenter"):
            return ""
        return ""   # decorative custom flowables carry no text

    def para(self, f):
        style, body = f.style.name, inline(f.text)
        if not body:
            return ""
        if style == "h2":
            return f"<h3>{body}</h3>"
        cls = {"lead": "lead", "small": "small", "cap": "caption", "tag": "tag", "ref": "ref"}.get(style)
        return f'<p class="{cls}">{body}</p>' if cls else f"<p>{body}</p>"

    def figure(self, caption=None):
        self.fig_n += 1
        if self.fig_n > len(self.figures):
            return f'<p class="small">[Figure {self.fig_n}: see the PDF report.]</p>'
        src, w, h = self.figures[self.fig_n - 1]
        alt = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", caption or ""))).strip() or f"Figure {self.fig_n} of the report"
        cap = f'<figcaption>{caption}</figcaption>' if caption else ""
        return (f'<figure class="report-figure"><img src="{src}" width="{w}" height="{h}" alt="{html.escape(alt[:300])}" '
                f'loading="lazy">{cap}</figure>')

    def meter(self, active, scale="verdict"):
        segs = []
        if scale == "pledge":   # pledge labels: colours inline, so the page does not depend on stylesheet classes
            for i, v in enumerate(mizien_report.PLEDGES):
                on = ' class="on" aria-current="true"' if i == active else ""
                segs.append(f'<li{on}><span class="badge v-{verdict_slug(v)}" style="{pledge_style(v)}">{v}</span></li>')
            return ('<ol class="report-meter pledge-meter" aria-label="Pledge labels" '
                    'style="grid-template-columns: repeat(auto-fit, minmax(96px, 1fr))">' + "".join(segs) + "</ol>")
        for i, v in enumerate(VERDICTS):
            on = ' class="on" aria-current="true"' if i == active else ""
            segs.append(f'<li{on}><span class="badge v-{verdict_slug(v)}">{v}</span></li>')
        return '<ol class="report-meter" aria-label="Verdict scale">' + "".join(segs) + "</ol>"

    def cell(self, c):
        mz = getattr(c, "_mz", None)
        if mz and mz[0] in ("chip", "grade"):
            return getattr(self, "mz_" + mz[0])(*mz[1:])
        if isinstance(c, Table) and not mz:
            return self.table_generic(c)
        if isinstance(c, (list, tuple)):
            parts = [self.cell(x) for x in c]
            return "".join(p if p.startswith("<") and not p.startswith(("<b>", "<i>", "<a ")) else f"<p>{p}</p>"
                           for p in parts if p)
        if isinstance(c, Paragraph):
            return inline(c.text)
        if isinstance(c, Image):
            return self.figure()
        if isinstance(c, str):
            return html.escape(c)
        return self.block(c) if c is not None else ""

    # ---------------------------------------------------------------- untagged tables (CC-001, custom blocks)
    @staticmethod
    def _hex(c):
        try:
            return c.hexval().replace("0x", "#").lower()
        except Exception:
            return None

    def _bg(self, t, row=None):
        """Background colour of a table (or of one row), from its style commands."""
        for cmd in getattr(t, "_bkgrndcmds", []):
            try:
                op, (sc, sr), (ec, er), arg = cmd[0], cmd[1], cmd[2], cmd[3]
            except Exception:
                continue
            if op != "BACKGROUND":
                continue
            if row is None or (sr == row and er in (row, row - len(t._cellvalues))):
                return self._hex(arg)
        return None

    def _bar(self, t):
        for cmd in getattr(t, "_linecmds", []):
            if cmd and cmd[0] == "LINEBEFORE" and len(cmd) >= 5:
                return self._hex(cmd[4])
        return None

    @staticmethod
    def _paras(cell):
        cell = cell if isinstance(cell, (list, tuple)) else [cell]
        return [x for x in cell if isinstance(x, Paragraph)]

    def _keypoints(self, content):
        items = content if isinstance(content, (list, tuple)) else [content]
        if len(items) != 1 or not isinstance(items[0], Table):
            return None
        rows = items[0]._cellvalues
        if not rows or any(len(r) != 2 or not isinstance(r[0], Table) or not isinstance(r[1], Paragraph) for r in rows):
            return None
        if not all(re.fullmatch(r"\d+", re.sub(r"<[^>]+>", "", getattr(r[0]._cellvalues[0][0], "text", "")).strip())
                   for r in rows):
            return None
        return '<ol class="key-points">' + "".join(f"<li>{inline(r[1].text)}</li>" for r in rows) + "</ol>"

    def table_generic(self, t):
        rows = getattr(t, "_cellvalues", [])
        if len(rows) == 1 and len(rows[0]) == 1:        # a one-cell box: a chip, key points or a callout
            only = rows[0][0]
            if isinstance(only, Paragraph) and only.style.name in ("chip", "g"):
                if only.style.name == "g":
                    return self.mz_grade(re.sub(r"<[^>]+>", "", only.text).strip())
                return self.mz_chip(only.text, self._bg(t) or "#5f6b71", "#ffffff")
            kp = self._keypoints(rows[0][0])
            if kp:
                return kp
            bg, bar = self._bg(t), self._bar(t)
            if bg or bar:
                return self.mz_callout(rows[0][0], bg or "#ffffff", bar or "#ffffff")
            return f'<div class="report-box">{self.cell(rows[0][0])}</div>'
        flat = [c for r in rows for c in r]
        if len(rows) == 2 and all(isinstance(c, Paragraph) for c in flat) and \
                all(c.style.fontSize >= 16 for c in rows[0]) and all(c.style.fontSize < 10 for c in rows[1]):
            return self.mz_tiles([(c0.text, self._hex(c0.style.textColor), c1.text) for c0, c1 in zip(rows[0], rows[1])])
        if len(rows) == 1 and len(rows[0]) == 2:
            a, b = self._paras(rows[0][0]), self._paras(rows[0][1])
            if len(a) >= 2 and len(b) >= 2 and "MOVE" in a[0].text.upper() and "MOVE" in b[0].text.upper():
                return self.mz_updown(a[1].text, b[1].text)
        if flat and all(isinstance(c, Paragraph) and c.style.name == "toc" for c in flat if c is not None):
            items = []
            for c in flat:
                m = re.match(r"^(\S+)(?:&nbsp;|\s)+(.*)$", re.sub(r"</?font\b[^>]*>", "", c.text).strip())
                if m:
                    items.append((m.group(1), m.group(2)))
            items.sort(key=lambda x: (len(x[0]), x[0]))
            return self.mz_toc(items)
        if self._bg(t, row=0) == "#14452f":                 # green header row: a data table
            return self.mz_table(rows, True)
        body = "".join("<tr>" + "".join(f"<td>{self.cell(c)}</td>" for c in r) + "</tr>" for r in rows)
        return f'<div class="table-wrap"><table class="report-table layout"><tbody>{body}</tbody></table></div>'

    # ---------------------------------------------------------------- tagged helpers
    def mz_callout(self, paras, bg, bar):
        inner = self.render(paras if isinstance(paras, (list, tuple)) else [paras])
        return f'<div class="callout bg-{kc(bg)} bar-{kc(bar)}">{inner}</div>'

    def mz_chip(self, text, bg, fg):
        if (bg or "").upper() in PLEDGE_HEX:   # pledge labels: the site has no chip classes for them
            return f'<span class="chip" style="background: {bg}; color: #fff">{inline(text)}</span>'
        return f'<span class="chip bg-{kc(bg)}">{inline(text)}</span>'

    def mz_grade(self, g):
        return f'<span class="grade grade-{html.escape(g.lower())}" title="Evidence grade {html.escape(g)}">{html.escape(g)}</span>'

    def mz_fig(self, path):
        return self.figure()

    def mz_table(self, rows, header):
        head, body = (rows[0], rows[1:]) if header else (None, rows)
        th = "<thead><tr>" + "".join(f'<th scope="col">{self.cell(c)}</th>' for c in head) + "</tr></thead>" if head else ""
        tb = "".join("<tr>" + "".join(f"<td>{self.cell(c)}</td>" for c in r) + "</tr>" for r in body)
        return f'<div class="table-wrap"><table class="report-table">{th}<tbody>{tb}</tbody></table></div>'

    def mz_contested(self, title, status, status_col, side_a, side_b, why, label_a, label_b, label_why):
        return (f'<section class="contested"><header><h3>{inline(title)}</h3>'
                f'<span class="chip bg-{kc(status_col)}">{inline(status)}</span></header>'
                f'<div class="sides"><div class="side-a"><p class="tag">{inline(label_a)}</p><p>{inline(side_a)}</p></div>'
                f'<div class="side-b"><p class="tag">{inline(label_b)}</p><p>{inline(side_b)}</p></div></div>'
                f'<footer><p class="tag">{inline(label_why)}</p><p>{inline(why)}</p></footer></section>')

    def mz_keypoints(self, kp):
        items = "".join(f"<li><strong>{inline(a)}</strong> {inline(b)}</li>" for a, b in kp)
        return f'<ol class="key-points">{items}</ol>'

    def mz_tiles(self, items):
        tiles = "".join(f'<div class="tile"><span class="tile-big fg-{kc(col)}">{inline(b)}</span>'
                        f'<span class="tile-cap">{inline(cp)}</span></div>' for b, col, cp in items)
        return f'<div class="tiles">{tiles}</div>'

    def mz_updown(self, up, down, up_head="What would move the verdict up", down_head="What would move it down"):
        return (f'<div class="updown"><div class="up"><p class="tag">{html.escape(up_head)}</p>'
                f"<p>{inline(up)}</p></div><div class=\"down\"><p class=\"tag\">{html.escape(down_head)}</p>"
                f"<p>{inline(down)}</p></div></div>")

    def mz_toc(self, items):
        li = "".join(f'<li><a href="#section-{html.escape(str(n))}"><span class="sec-n">{n}</span> {inline(t)}</a></li>'
                     for n, t in items)
        return f'<nav class="report-toc" aria-label="In this report"><ol>{li}</ol></nav>'

    def mz_verdictbox(self, verdict, subline):
        if verdict in mizien_report.PLEDGES:
            return (f'<div class="verdict-box pledge-box v-{verdict_slug(verdict)}" style="{pledge_style(verdict)}">'
                    f'<span class="vb-label">Pledge</span><strong>{html.escape(verdict)}</strong><p>{inline(subline)}</p></div>')
        return (f'<div class="verdict-box v-{verdict_slug(verdict)}"><span class="vb-label">Verdict</span>'
                f"<strong>{html.escape(verdict)}</strong><p>{inline(subline)}</p></div>")

    def mz_requests(self, reqs):
        return '<ul class="requests">' + "".join(f"<li>{inline(r)}</li>" for r in reqs) + "</ul>"

    def mz_ref(self, n, t, u):          # only reached outside a list context
        return self.list_item(type("R", (), {"_mz": ("ref", n, t, u)})())[1]


# ------------------------------------------------------------------ figures from the published PDF
def extract_figures(pdf, dest_dir, claim_id):
    """Write the PDF's figures (in page order) as PNG, with their transparency flattened onto white."""
    listing = subprocess.run(["pdfimages", "-list", str(pdf)], capture_output=True, text=True, check=True).stdout
    rows = [ln.split() for ln in listing.splitlines()[2:] if ln.strip()]
    kinds = [r[2] for r in rows]            # image | smask | ...
    for old in dest_dir.glob("fig-*"):
        old.unlink()
    if "image" not in kinds:
        return []
    with tempfile.TemporaryDirectory() as tmp:
        subprocess.run(["pdfimages", "-png", str(pdf), f"{tmp}/x"], check=True)
        files = sorted(pathlib.Path(tmp).glob("x-*.png"))
        out, i = [], 0
        while i < len(kinds):
            if kinds[i] != "image":
                i += 1
                continue
            im = _open(files[i]).convert("RGB")
            if i + 1 < len(kinds) and kinds[i + 1] == "smask":
                mask = _open(files[i + 1]).convert("L").resize(im.size)
                flat = PIL.Image.new("RGB", im.size, "white")
                flat.paste(im, mask=mask)
                im = flat
                i += 1
            n = len(out) + 1
            dest_dir.mkdir(parents=True, exist_ok=True)
            name = f"fig-{n}.png"
            im.save(dest_dir / name, optimize=True)
            out.append((f"/claim-files/{claim_id}/report-figures/{name}", im.width, im.height))
            i += 1
    return out


# ------------------------------------------------------------------ cover block and page
def cover_html(R, claim_id):
    if R is None:
        return ""
    title = " ".join(R.title_lines)
    subtitle = " ".join(R.subtitle_lines)
    quote = " ".join(R.quote_lines)
    return (f'<div class="report-cover"><p class="kicker">Claim Check {html.escape(R.number)} · '
            f"{html.escape(R.kicker)}</p><h2 class=\"report-title\">{html.escape(title)}</h2>"
            f'<p class="report-subtitle">{html.escape(subtitle)}</p>'
            f'<blockquote class="report-quote"><p>{html.escape(quote)}</p>'
            f'</blockquote><p class="quote-source">{html.escape(R.attribution)}<br>{html.escape(R.context)}</p>'
            f'<p class="report-verdict"><span class="badge v-{verdict_slug(R.verdict)}">Verdict: {html.escape(R.verdict)}</span> '
            f"<em>{html.escape(R.verdict_note)}</em></p>"
            f'<p class="small">Version {html.escape(R.version)} · {html.escape(R.date)}</p></div>')


def words(s):
    return re.findall(r"[a-z0-9]+", s.lower().replace("’", "'"))


def check_text(pdf, html_text):
    """Share of the PDF's body words (cover and running heads excluded) that also appear in the HTML."""
    txt = subprocess.run(["pdftotext", "-f", "2", "-layout", str(pdf), "-"], capture_output=True, text=True).stdout
    txt = re.sub(r"MIŻIEN\s+·\s+CLAIM CHECK.*|v\d+\.\d+ draft.*", " ", txt)
    have = set(words(html.unescape(re.sub(r"<[^>]+>", " ", html_text))))
    pdf_words = [w for w in words(txt) if len(w) > 2]
    missing = [w for w in pdf_words if w not in have]
    return 1 - len(missing) / max(1, len(pdf_words)), sorted(set(missing))[:25]


def publish(claim_id):
    claim_dir = ROOT / "claims" / claim_id
    pdf = claim_dir / "report.pdf"
    if not pdf.is_file():
        raise SystemExit(f"{claim_id}: no claims/{claim_id}/report.pdf")
    story, R = capture(claim_id)
    figures = extract_figures(pdf, claim_dir / "report-figures", claim_id)
    r = Renderer(figures)
    body = r.render(story)
    page = (f'<article class="report" data-claim="{claim_id}">\n{cover_html(R, claim_id)}\n{body}\n</article>\n')
    (claim_dir / "report.html").write_text(page, encoding="utf-8")
    share, missing = check_text(pdf, page)
    status = "ok" if share >= 0.98 and r.fig_n == len(figures) else "CHECK"
    print(f"{claim_id}: {status} · {share:.1%} of PDF words present · figures {r.fig_n} in story, {len(figures)} in PDF"
          + (f" · missing e.g. {missing[:12]}" if share < 0.995 else ""))
    return status == "ok"


def main(argv):
    warn = "--warn" in argv
    argv = [a for a in argv if a != "--warn"]
    ids = sorted(p.name.split("-report")[0].upper() for p in TOOLS.glob("cc-*-report")) if argv == ["--all"] else argv
    if not ids:
        raise SystemExit(__doc__)
    bad = []
    for i in ids:
        try:
            ok = publish(i)
        except (Exception, SystemExit) as e:          # one broken script must not stop the site build
            if not warn:
                raise
            print(f"{i}: FAILED · {e}")
            ok = False
        if not ok:
            bad.append(i)
    if bad:
        msg = "Report web version needs a look: " + ", ".join(bad) + " (the claim page falls back to its summary)."
        print(f"::warning::{msg}" if warn else msg)
    return 0 if warn or not bad else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
