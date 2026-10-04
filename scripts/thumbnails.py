"""Thumbnails for claims: one illustration per topic and subtopic, and a specific one for every researched claim.

Each subtopic has a small scene: a setting (hills, sea or town) in its topic's colour, one large line drawing and two
smaller ones from a shared icon set. A claim with a verdict gets its own thumbnail on that scene, with its ID, the
headline figure and caption from `thumbnail:` in its claim.yml (taken from its flyer's results), and its verdict.
Claims not yet checked use their subtopic's thumbnail.

Output is SVG (a few KB each) in build/thumbs/, copied into the site as /claim-files/thumbs/. Called by
scripts/build_site_data.py.
"""
import html
import pathlib
import re
import textwrap

# ------------------------------------------------------------------ line icons, 24x24, drawn with round strokes
ICONS = {
    "tree": "M12 21v-6M12 15c-4.2 0-6.5-2.6-6.5-5.7S8.2 3.6 12 3c3.8.6 6.5 3.3 6.5 6.3S16.2 15 12 15zM12 12l-2.2-2M12 10.5l2.4-2",
    "pine": "M12 3l-5.5 8h3.5l-4.5 6.5h13L14 11h3.5zM12 17.5V21",
    "sapling": "M12 21v-7M12 14c0-3.2 2.1-5.3 5.4-5.3 0 3.2-2.1 5.3-5.4 5.3zM12 16.5c0-2.6-1.9-4.3-4.7-4.3 0 2.6 1.9 4.3 4.7 4.3zM8 21h8",
    "bench": "M3 13h18M5 13v5M19 13v5M4 9.5h16V13H4zM7 9.5V7.5M17 9.5V7.5",
    "grass": "M2 21c2-3 3-5.5 3-8.5M6.5 21c0-3 1.2-5.5 3.2-7.5M11 21c0-4 1.4-6.8 4.4-8.6M15.5 21c.2-3 1.5-5.2 3.4-6.4M20 21c0-2.2.8-3.8 2-5",
    "field": "M2 20h20M3.5 20l4.5-8M8.5 20l3-8M13.5 20l1.5-8M18.5 20l.3-8M2 12h20M5 12c0-2 1.3-3.5 3-4M16 12c0-2.4 1.6-4 4-4.5",
    "crane": "M6 21V4.5h2.2V21M4 21h8M8.2 5.5H21M8.2 5.5l3.8 3.8M18.5 5.5V10M17.4 10h2.2v2.2h-2.2zM6 4.5L8.2 2.5 10 4.5",
    "building": "M5 21V8l7-4 7 4v13M9.5 21v-5h5v5M8.3 11h1.8M13.9 11h1.8M8.3 14h1.8M13.9 14h1.8",
    "house": "M3 11.5L12 4l9 7.5M5.5 10v11h13V10M10 21v-6h4v6",
    "euro": "M17 6.6A7 7 0 1 0 17 17.4M4.5 10.2h9M4.5 13.8h9",
    "document": "M7 3h7l5 5v13H7zM14 3v5h5M10 12h6M10 15.5h6M10 19h3.5",
    "stamp": "M9.5 3h5v5.5l3 3V14h-11v-2.5l3-3zM5 17h14v3.2H5z",
    "megaphone": "M3 10v4l11.5 5V5zM14.5 9a3 3 0 0 1 0 6M6 15l1.2 5h3l-1.2-4.2M18 7.5l2.5-1.5M18.5 12H21M18 16.5l2.5 1.5",
    "ballot": "M4 11h16v10H4zM8 11l2-8h4l2 8M9.4 6.8h5.2M10.5 15.5l1.3 1.3 2.7-2.7",
    "scales": "M12 4v16M8 20h8M4 8h16M4 8l-2.5 5h5zM20 8l-2.5 5h5zM12 2.5v1.5",
    "thermometer": "M12 3a2 2 0 0 1 2 2v9.2a4 4 0 1 1-4 0V5a2 2 0 0 1 2-2zM12 10v6.5M16.5 6h2M16.5 9h2",
    "sun": "M12 8a4 4 0 1 0 0 8a4 4 0 1 0 0-8M12 2v2M12 20v2M2 12h2M20 12h2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4",
    "hardhat": "M3 17.5h18M5 17.5a7 7 0 0 1 14 0M10 10.5V7h4v3.5M12 7V5",
    "moon": "M20 14.5A8 8 0 1 1 9.5 4a6.2 6.2 0 0 0 10.5 10.5z",
    "star": "M12 3.5l2.4 4.9 5.4.8-3.9 3.8.9 5.3-4.8-2.5-4.8 2.5.9-5.3-3.9-3.8 5.4-.8z",
    "bird": "M2 11c2.8-.4 5 .8 7 3.2C10.3 9.6 13.6 7 18 7l3.5 1.2-3.2 1.2c-.3 4.6-3.8 7.6-8.6 7.6H5.5M14.5 9.5h.01",
    "gull": "M3 12c2.5-2.8 5.5-2.8 9 0c3.5-2.8 6.5-2.8 9 0",
    "fish": "M3 12c3-4.2 8.2-5 13-2l4.5-3.2v10.4L16 14c-4.8 3-10 2.2-13-2zM14.5 11v.01",
    "wave": "M2 9c2.5 0 2.5 2 5 2s2.5-2 5-2 2.5 2 5 2 2.5-2 5-2M2 15c2.5 0 2.5 2 5 2s2.5-2 5-2 2.5 2 5 2 2.5-2 5-2",
    "shield": "M12 3l8 3v6c0 5-3.4 8-8 9-4.6-1-8-4-8-9V6zM8.8 12l2.2 2.2 4.2-4.2",
    "speaker": "M3 10v4h4l5 4V6L7 10zM15.5 9a4 4 0 0 1 0 6M18.5 6a8 8 0 0 1 0 12",
    "people": "M8 11a3 3 0 1 0 0-6a3 3 0 1 0 0 6M2 20c0-3.3 2.7-6 6-6s6 2.7 6 6M16.5 11a2.6 2.6 0 1 0 0-5.2M16 14c3.2 0 6 2.4 6 6",
    "key": "M7.5 16a4 4 0 1 0 0-8a4 4 0 1 0 0 8M11.5 12H21M17.5 12v3.2M20.5 12v2.4M6.2 12h.01",
    "suitcase": "M4 8h16v12H4zM9 8V5h6v3M4 13h16M8 20v1M16 20v1",
    "plane": "M10.5 21l1.8-1.6v-5.6l8.7 2.8v-2l-8.7-5.7V4a1.3 1.3 0 0 0-2.6 0v4.9L1 14.6v2l8.7-2.8v5.6l1.8 1.6",
    "car": "M3 13.5l2-5.5h14l2 5.5v5h-2v2h-3v-2H8v2H5v-2H3zM3 13.5h18M6.5 16h.01M17.5 16h.01",
    "road": "M8 21L10.2 3M16 21L13.8 3M12 5v2M12 10v2.2M12 15.5v2.5",
    "bus": "M5 4h14v13H5zM5 12h14M5 7h14M8 17v3M16 17v3M8 14.5h.01M16 14.5h.01",
    "busstop": "M6.5 21V3M6.5 3h6.5v5H6.5M4.5 21h4",
    "ferry": "M3 15h18l-2.2 4H5.2zM6 15v-4h12v4M9 11V8h5v3M2 21.5c2 0 2-1 4-1s2 1 4 1 2-1 4-1 2 1 4 1 2-1 4-1",
    "ship": "M3 15h18l-3 5H6zM5.5 15V9.5h11L19 15M8.5 9.5V5.5h4v4M14 5.5v4M2 22.5c2 0 2-1 4-1s2 1 4 1 2-1 4-1 2 1 4 1 2-1 4-1",
    "bridge": "M2 11h20M4 11v9M20 11v9M2 11c3 0 5-3.2 10-3.2S19 11 22 11M8.5 11v3.5M15.5 11v3.5M12 7.8V11",
    "train": "M6 3.5h12V16H6zM6 10.5h12M9 19.5l-2 2M15 19.5l2 2M9 13.5h.01M15 13.5h.01M6 16h12",
    "truck": "M2 7h11v9.5H2zM13 10h4l4 3.5v3h-8zM6 18.5a2 2 0 1 0 0-.01M17 18.5a2 2 0 1 0 0-.01",
    "rubble": "M3 20l3-5.2 4 2.2 3-6.5 4 4.3 4-1.2V20zM10 17l-.5 3M15 15.5l.8 4.5",
    "bin": "M5 7h14M9.5 7V4.5h5V7M6.5 7l1 13h9l1-13M10 11v6M14 11v6",
    "recycle": "M10.2 6L12 3l4.4 7.6M14.4 10.8l2 .1.8-1.8M18.4 13.8L21 18.2H11.6M13.5 16.4l-1.9 1.8 1.9 1.8M7.4 18.2H3l4.5-7.8M5.6 11.5l1.9-1.1 1.1 1.9",
    "mound": "M2 20c2.6-5.4 5.8-8.4 10-8.4s7.4 3 10 8.4zM5.5 16.5c2-1.3 4-1.8 6.5-1.8s4.6.6 6.6 1.8M8 12.4c1.3-.7 2.6-1 4-1M15.5 6.5c1-1 2-1 3 0M17 4.5c.7-.7 1.4-.7 2.1 0",
    "droplet": "M12 3c3 4 6 7.2 6 11a6 6 0 0 1-12 0c0-3.8 3-7 6-11zM9.2 14.5a2.8 2.8 0 0 0 2.8 2.8",
    "tap": "M4 9.5h9a3 3 0 0 1 3 3v2h2.5v-2a5.5 5.5 0 0 0-5.5-5.5H4zM8.5 7V4.5M5.5 4.5h6M17.3 18v.01M17.3 21v.01",
    "layers": "M2 15.5h20M2 19h20M2 12c3 0 4-1 6-1s3 1 6 1 4-1 8-1M2 8.5c3 0 4-1 6-1s3 1 6 1 4-1 8-1",
    "swimmer": "M2 17c2.5 0 2.5 1.5 5 1.5S9.5 17 12 17s2.5 1.5 5 1.5 2.5-1.5 5-1.5M6.5 13.5l4.2-3 3 3 3.2-2M16 6a2 2 0 1 0 0 4a2 2 0 1 0 0-4",
    "pipe": "M3 9h8v6H3zM11 11h6v8.5M15 19.5h4.5",
    "cloudrain": "M7 15.5a4 4 0 0 1 0-8a6 6 0 0 1 11.2 2.2A3 3 0 0 1 18 15.5zM8 18.5l-1 2.5M12 18.5l-1 2.5M16 18.5l-1 2.5",
    "factory": "M3 21V11l5 3V11l5 3V7.5h3V21zM16 7.5V3h3v18M6 17.5h2M10 17.5h2",
    "smoke": "M7 9a3 3 0 0 1 5-2.2A3 3 0 0 1 17 9a2.6 2.6 0 0 1 0 5.2H7A2.6 2.6 0 0 1 7 9z",
    "plug": "M9 3v5M15 3v5M7 8h10v4a5 5 0 0 1-10 0zM12 17v4",
    "pylon": "M12 2l-5 20M12 2l5 20M7.8 9h8.4M6.4 15h11.2M9 9l6.2 6M15 9l-6.2 6M4 5.5h16",
    "bolt": "M13 2L4 14h7l-1 8 9-12h-7z",
    "solar": "M3 15l3-8h12l3 8zM8.5 7l-1 8M15.5 7l1 8M4.5 11h15M12 15v4M8 19h8",
    "turbine": "M12 11v10.5M12 11L11.2 2.5M12 11l7.6 3.8M12 11l-7.2 4.6M9.5 21.5h5M12 9.8a1.2 1.2 0 1 0 .01 0",
    "chartdown": "M3 3v18h18M7 7l4 5 3-3 6 7M17 16h3v-3",
    "bastion": "M3 21V9h3v2h2V9h3v2h2V9h3v2h2V9h3v12zM10 21v-4.5a2 2 0 0 1 4 0V21",
    "binoculars": "M7 9a4 4 0 1 0 .01 0M17 9a4 4 0 1 0 .01 0M7 9V5h3v4M14 9V5h3v4M10 13h4",
}

# ------------------------------------------------------------------ scenes per subtopic: setting, large icon, two small ones
SCENES = {
    ("Land & Trees", "Open spaces & parks"): ("hills", "bench", ["tree", "grass"]),
    ("Land & Trees", "Trees & planting"): ("hills", "tree", ["sapling", "pine"]),
    ("Land & Trees", "Land take & agriculture"): ("hills", "field", ["crane", "building"]),
    ("Climate & Energy", "Electricity & grid"): ("town", "pylon", ["bolt", "plug"]),
    ("Climate & Energy", "Emissions & targets"): ("town", "factory", ["chartdown", "smoke"]),
    ("Climate & Energy", "Renewables"): ("hills", "turbine", ["solar", "sun"]),
    ("Governance & Promises", "Manifestos & pledges"): ("town", "megaphone", ["ballot", "document"]),
    ("Governance & Promises", "Accountability"): ("town", "scales", ["document", "stamp"]),
    ("Health & Safety", "Heat & health"): ("town", "thermometer", ["sun", "people"]),
    ("Health & Safety", "Workplace safety"): ("town", "hardhat", ["crane", "building"]),
    ("Nature & Wildlife", "Dark skies"): ("hills", "moon", ["star", "binoculars"]),
    ("Nature & Wildlife", "Hunting & birds"): ("hills", "bird", ["gull", "gull"]),
    ("Nature & Wildlife", "Marine protection"): ("sea", "fish", ["shield", "wave"]),
    ("Noise", None): ("town", "speaker", ["car", "plane"]),
    ("Planning & Housing", "Development & construction"): ("town", "crane", ["building", "truck"]),
    ("Planning & Housing", "Heritage & character"): ("sea", "bastion", ["building", "shield"]),
    ("Planning & Housing", "Housing & affordability"): ("town", "house", ["euro", "key"]),
    ("Planning & Housing", "Permits & enforcement"): ("town", "document", ["stamp", "house"]),
    ("Tourism & Population", "Population & labour"): ("town", "people", ["hardhat", "house"]),
    ("Tourism & Population", "Short lets & concessions"): ("sea", "key", ["suitcase", "house"]),
    ("Tourism & Population", "Tourism numbers & capacity"): ("sea", "plane", ["suitcase", "people"]),
    ("Transport", "Cars & traffic"): ("town", "car", ["road", "car"]),
    ("Transport", "Ferries & Gozo links"): ("sea", "ferry", ["wave", "sun"]),
    ("Transport", "Public transport"): ("town", "bus", ["busstop", "people"]),
    ("Transport", "Roads & mass transit"): ("town", "bridge", ["train", "car"]),
    ("Waste", "Construction waste"): ("hills", "truck", ["rubble", "crane"]),
    ("Waste", "Landfill & treatment"): ("hills", "mound", ["bin", "truck"]),
    ("Waste", "Recycling & separation"): ("town", "recycle", ["bin", "bin"]),
    ("Water", "Bathing water & sewage"): ("sea", "swimmer", ["droplet", "wave"]),
    ("Water", "Flood relief"): ("town", "cloudrain", ["droplet", "pipe"]),
    ("Water", "Water supply & groundwater"): ("hills", "droplet", ["tap", "layers"]),
    ("Air", "Air quality & health"): ("town", "smoke", ["car", "factory"]),
    ("Air", "Port & power emissions"): ("sea", "ship", ["factory", "plug"]),
}
TOPIC_SCENES = {   # topics without a subtopic, and new topics or subtopics until they get their own scene
    "Land & Trees": ("hills", "tree", ["sapling", "grass"]), "Climate & Energy": ("town", "factory", ["bolt", "sun"]),
    "Waste": ("town", "bin", ["recycle", "truck"]), "Water": ("sea", "droplet", ["wave", "tap"]),
    "Nature & Wildlife": ("hills", "bird", ["fish", "tree"]), "Air": ("town", "smoke", ["factory", "car"]),
    "Transport": ("town", "car", ["bus", "road"]), "Governance & Promises": ("town", "scales", ["megaphone", "document"]),
    "Planning & Housing": ("town", "building", ["crane", "house"]), "Noise": ("town", "speaker", ["car", "plane"]),
    "Tourism & Population": ("sea", "plane", ["people", "suitcase"]), "Health & Safety": ("town", "thermometer", ["hardhat", "sun"]),
}
DEFAULT_SCENE = ("hills", "scales", ["document", "star"])

VERDICT_STYLE = {   # background, text: the site's accessible verdict colours
    "Supported": ("#2e7d4f", "#ffffff"), "Largely supported": ("#8db36b", "#13301f"),
    "Not substantiated": ("#d9772b", "#13301f"), "Misleading": ("#b5483a", "#ffffff"), "Contradicted": ("#8e2f25", "#ffffff"),
}
W, H = 640, 400


def _hex(c):
    c = c.lstrip("#")
    return tuple(int(c[i:i + 2], 16) for i in (0, 2, 4))


def _mix(a, b, t):
    ra, rb = _hex(a), _hex(b)
    return "#" + "".join(f"{round(x + (y - x) * t):02x}" for x, y in zip(ra, rb))


def _esc(s):
    return html.escape(str(s or ""), quote=True)


def _slug(s):
    return re.sub(r"[^a-z0-9]+", "-", str(s or "").lower().replace("&", "and")).strip("-")


def _icon(name, x, y, size, colour, width):
    """A line icon centred at (x, y), `size` pixels across, strokes `width` pixels wide whatever the scale."""
    k = size / 24
    return (f'<g transform="translate({x - size / 2:.1f} {y - size / 2:.1f}) scale({k:.3f})" fill="none" stroke="{colour}" '
            f'stroke-width="{width / k:.3f}" stroke-linecap="round" stroke-linejoin="round"><path d="{ICONS[name]}"/></g>')


def _setting(kind, colour):
    """Background shapes along the bottom: hills, sea or a town skyline."""
    c1, c2 = _mix(colour, "#0b2419", 0.45), _mix(colour, "#0b2419", 0.65)
    if kind == "sea":
        lines = "".join(
            f'<path d="M0 {y} ' + " ".join(f"q 20 -{6 + i % 2 * 2} 40 0 t 40 0" for _ in range(8)) +
            f'" fill="none" stroke="{colour}" stroke-opacity="{0.42 - i * 0.07:.2f}" stroke-width="3"/>'
            for i, y in enumerate((318, 344, 370, 396)))
        return f'<rect y="300" width="{W}" height="{H - 300}" fill="{c2}" opacity=".7"/>' + lines
    if kind == "town":
        blocks, x = [], 0
        heights = [70, 46, 92, 58, 34, 80, 52, 104, 62, 40, 86, 54, 74, 44, 96, 60]
        for i, h in enumerate(heights):
            w = 40 + (i * 13) % 24
            blocks.append(f'<rect x="{x}" y="{H - h}" width="{w - 4}" height="{h}" rx="3" fill="{c1 if i % 2 else c2}"/>')
            x += w
            if x > W:
                break
        return "".join(blocks)
    return (f'<path d="M0 312 C 110 262, 220 282, 330 300 S 530 256, {W} 290 V {H} H 0 Z" fill="{c2}"/>'
            f'<path d="M0 350 C 140 318, 260 336, 380 352 S 560 320, {W} 340 V {H} H 0 Z" fill="{c1}"/>')


def _scene(setting, primary, secondary, colour, uid):
    """The illustration: glow, rings, setting, one large icon and two small ones (right-hand side)."""
    dark = _mix(colour, "#0b2419", 0.78)
    mid = _mix(colour, "#14452f", 0.55)
    rings = "".join(f'<circle cx="470" cy="170" r="{r}" fill="none" stroke="{colour}" stroke-opacity="{0.20 - i * 0.03:.2f}" stroke-width="2"/>'
                    for i, r in enumerate((122, 158, 196, 236)))
    return (f'<defs><linearGradient id="bg{uid}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{dark}"/>'
            f'<stop offset="1" stop-color="{mid}"/></linearGradient>'
            f'<radialGradient id="gl{uid}" cx=".73" cy=".43" r=".5"><stop offset="0" stop-color="{colour}" stop-opacity=".55"/>'
            f'<stop offset="1" stop-color="{colour}" stop-opacity="0"/></radialGradient></defs>'
            f'<rect width="{W}" height="{H}" fill="url(#bg{uid})"/><rect width="{W}" height="{H}" fill="url(#gl{uid})"/>{rings}'
            + _setting(setting, colour)
            + f'<circle cx="470" cy="170" r="104" fill="{colour}" fill-opacity=".22"/>'
            + _icon(primary, 470, 170, 176, "#f6f4ee", 7)
            + _icon(secondary[0], 586, 76, 70, "#e3a72f", 4.5)
            + _icon(secondary[1], 590, 270, 64, "#e3a72f", 4.5))


def scene_for(category, subtopic):
    return SCENES.get((category, subtopic)) or TOPIC_SCENES.get(category) or DEFAULT_SCENE


def _lines(text, width, max_lines):
    lines = textwrap.wrap(str(text or ""), width=width)
    if len(lines) > max_lines:
        lines = lines[:max_lines]
        lines[-1] = lines[-1].rstrip(" ,;:") + "…"
    return lines


def _text(lines, x, y, size, leading, fill, weight="400", family="'Liberation Sans', Arial, sans-serif", extra=""):
    spans = "".join(f'<tspan x="{x}" dy="{0 if i == 0 else leading}">{_esc(ln)}</tspan>' for i, ln in enumerate(lines))
    return f'<text x="{x}" y="{y}" font-family="{family}" font-size="{size}" font-weight="{weight}" fill="{fill}"{extra}>{spans}</text>'


def _shade(uid, width):
    """A dark panel behind the text that fades into the illustration (no hard edge)."""
    return (f'<defs><linearGradient id="sh{uid}" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#06180f" stop-opacity=".72"/>'
            f'<stop offset=".72" stop-color="#06180f" stop-opacity=".5"/><stop offset="1" stop-color="#06180f" stop-opacity="0"/>'
            f'</linearGradient></defs><rect width="{width}" height="{H}" fill="url(#sh{uid})"/>')


def subtopic_svg(category, subtopic, colour):
    setting, primary, secondary = scene_for(category, subtopic)
    uid = _slug(f"{category}-{subtopic}")
    shade = _shade(uid, 340)
    kicker = _text([category.upper()], 30, 64, 15, 0, "#cfe2d4", "700", extra=' letter-spacing="1.6"')
    title = _text(_lines(subtopic or category, 15, 3), 30, 126, 40, 46, "#ffffff", "700", "'Liberation Serif', Georgia, serif")
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">'
            + _scene(setting, primary, secondary, colour, uid) + shade + kicker + title + "</svg>")


def claim_svg(c, colour):
    setting, primary, secondary = scene_for(c["category"], c.get("subtopic"))
    uid = _slug(c["id"])
    th = c.get("thumbnail") or {}
    figure, caption = str(th.get("figure") or ""), str(th.get("caption") or c.get("title") or "")
    bg, ink = VERDICT_STYLE.get(c.get("verdict"), ("#5d7468", "#ffffff"))
    size = 96 if len(figure) <= 4 else 78 if len(figure) <= 7 else 58
    shade = _shade(uid, 380)
    kicker = _text([f'{c["id"]} · {(c.get("subtopic") or c["category"]).upper()}'], 30, 54, 16, 0, "#cfe2d4", "700",
                   extra=' letter-spacing="1.2"')
    fig = _text([figure], 28, 64 + size, size, 0, "#ffffff", "700") if figure else ""
    cap = _text(_lines(caption, 24, 3), 30, 100 + size, 24, 30, "#eef3ef")
    label = (c.get("verdict") or "Not yet checked").upper()
    pw = 32 + len(label) * 12.6
    pill = (f'<rect x="28" y="{H - 72}" width="{pw:.0f}" height="46" rx="23" fill="{bg}"/>'
            f'<text x="{28 + pw / 2:.0f}" y="{H - 42}" text-anchor="middle" font-family="\'Liberation Sans\', Arial, sans-serif" '
            f'font-size="18" font-weight="700" letter-spacing="1" fill="{ink}">{_esc(label)}</text>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">'
            + _scene(setting, primary, secondary, colour, uid) + shade + kicker + fig + cap + pill + "</svg>")


def render_all(records, colours, out_dir):
    """Write the thumbnails; return {claim_id: {"url", "specific", "alt"}} for the site data."""
    out_dir = pathlib.Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    result, done = {}, set()
    for c in records:
        colour = colours.get(c["category"], "#7fa88b")
        key = (c["category"], c.get("subtopic"))
        name = f"sub-{_slug(c['category'])}--{_slug(c.get('subtopic') or 'all')}.svg"
        if key not in done:
            (out_dir / name).write_text(subtopic_svg(c["category"], c.get("subtopic"), colour), encoding="utf-8")
            done.add(key)
        if c.get("verdict"):
            own = f"{c['id']}.svg"
            (out_dir / own).write_text(claim_svg(c, colour), encoding="utf-8")
            th = c.get("thumbnail") or {}
            alt = f"{th.get('figure', '')} {th.get('caption', '')}".strip() or c["title"]
            result[c["id"]] = {"url": f"/claim-files/thumbs/{own}", "specific": True, "alt": alt}
        else:
            result[c["id"]] = {"url": f"/claim-files/thumbs/{name}", "specific": False, "alt": ""}
    return result
