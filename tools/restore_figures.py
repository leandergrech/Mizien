#!/usr/bin/env python3
"""Put a report's figures back in tools/cc-NNN-report/out/ from the committed claims/CC-NNN/report.pdf.

The figure PNGs in tools/*/out/ are not committed, and some figure scripts need satellite data, GIS services or API
downloads. To rebuild a report after a text-only correction, restore the figures the published PDF already contains
instead of re-running those pipelines. The script reads the report's story (as tools/report_html.py does) to learn
which figure files build_report.py expects, in order, and writes the PDF's embedded images to those paths.

Usage, from the repository root:
    python tools/restore_figures.py CC-014            # only fills figures that are missing
    python tools/restore_figures.py CC-014 --force    # overwrite existing figures too
Re-run a claim's own figure script instead whenever a figure itself must change.
"""
import pathlib
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

import PIL.Image  # noqa: E402
import report_html  # noqa: E402


def fig_paths(story):
    """Figure file paths in story order (fig() tags its Image with ('fig', path))."""
    out = []

    def walk(x):
        mz = getattr(x, "_mz", None)
        if isinstance(mz, tuple) and mz and mz[0] == "fig":
            out.append(pathlib.Path(mz[1]))
            return
        for attr in ("_content", "_flowables", "_cellvalues"):
            v = getattr(x, attr, None)
            if v is not None:
                for i in (v if isinstance(v, (list, tuple)) else [v]):
                    walk(i) if not isinstance(i, (list, tuple)) else [walk(j) for j in i]

    for f in story:
        walk(f)
    return out


def pdf_images(pdf):
    """The PDF's images in page order, with soft masks flattened onto white."""
    listing = subprocess.run(["pdfimages", "-list", str(pdf)], capture_output=True, text=True, check=True).stdout
    kinds = [ln.split()[2] for ln in listing.splitlines()[2:] if ln.strip()]
    ims = []
    with tempfile.TemporaryDirectory() as tmp:
        subprocess.run(["pdfimages", "-png", str(pdf), f"{tmp}/x"], check=True)
        files = sorted(pathlib.Path(tmp).glob("x-*.png"))
        i = 0
        while i < len(kinds):
            if kinds[i] != "image":
                i += 1
                continue
            im = PIL.Image.open(files[i]).convert("RGB")
            if i + 1 < len(kinds) and kinds[i + 1] == "smask":
                mask = PIL.Image.open(files[i + 1]).convert("L").resize(im.size)
                flat = PIL.Image.new("RGB", im.size, "white")
                flat.paste(im, mask=mask)
                im = flat
                i += 1
            ims.append(im)
            i += 1
    return ims


def main(argv):
    if not argv or argv[0].startswith("-"):
        raise SystemExit(__doc__)
    cid, force = argv[0].upper(), "--force" in argv
    story, _ = report_html.capture(cid)
    paths = fig_paths(story)
    ims = pdf_images(ROOT / "claims" / cid / "report.pdf")
    if len(paths) != len(ims):
        raise SystemExit(f"{cid}: {len(paths)} figures in the story but {len(ims)} images in the PDF; "
                         "run the figure script instead")
    script_dir = ROOT / "tools" / f"{cid.lower()}-report"
    for p, im in zip(paths, ims):
        p = p if p.is_absolute() else script_dir / p
        if p.exists() and not force:
            print(f"{cid}: kept {p.relative_to(ROOT)}")
            continue
        p.parent.mkdir(parents=True, exist_ok=True)
        im.save(p)
        print(f"{cid}: restored {p.relative_to(ROOT)} ({im.width}x{im.height})")


if __name__ == "__main__":
    main(sys.argv[1:])
