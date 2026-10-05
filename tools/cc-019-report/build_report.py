"""Claim Check 019 report. Run fetch_data.py, crosscheck.py, spotcheck.py, calc.py and figures.py first.
Output: out/report.pdf"""
import csv
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import *  # noqa: E402,F401

FIG = HERE / "out"
DATA = HERE.parents[1] / "data" / "cc-019"
S = []
LG = colors.HexColor("#8DB36B")

# ================================================================== TL;DR
S += [SectionHeading(None, "TL;DR"), Spacer(1, 1 * mm),
      P("In September 2026 Amphora Media, an investigative newsroom, reported that <b>“nearly 830,000 square metres of "
        "nature and cropland have been built up in Malta between 2018 and 2023”</b>, and that in “nearly 95% of the "
        "take-up, farmland rather than natural area was affected”. The press is held to the same standard as everyone "
        "else here. We checked the arithmetic, the map Amphora published, a random sample of it against high-resolution "
        "satellite images, an independent land-cover product and the EEA’s land-change maps.", lead)]
S.append(key_points([
    ("Amphora’s own map adds up.",
     "The 397 change polygons behind Amphora’s map cover 828,429 m², so “nearly 830,000” is exact; the headline’s "
     "“over” is not. The arithmetic and the EEA figures it quotes check out."),
    ("Imagery confirms most of it.",
     "In 40 random draws from Amphora’s area checked against satellite images, 72.5% (95% interval 57–84%) went from "
     "open or green land to grey and 2.5% was already grey. But 15% was already being developed in September 2018, "
     "and 17.5% turned grey only after May 2023."),
    ("An independent model gets these parcels wrong.",
     "Impact Observatory’s 10 m maps show 68% of Amphora’s area as built-up already in 2018, which the imagery "
     "contradicts; only 2–3% of the model’s new built-up land lies inside the polygons. It can neither confirm nor "
     "rule out 0.83 km²."),
    ("The 95% farmland share is overstated.",
     "Amphora’s own data reach 96% only by counting all “grass” as farmland and leaving out the 37% with no 2018 "
     "class. In our imagery sample, fields were 59% of the land before (64% with orchards)."),
    ("Verdict: largely supported (moderate confidence).",
     "The total is Amphora’s own map, the sums are right and imagery confirms most of a sample; but the years are "
     "looser than “2018 to 2023” and the farmland share is overstated."),
]))
S += [Spacer(1, 4 * mm), VerdictMeter(1), Spacer(1, 3 * mm),
      tiles([("0.83", ORANGE, "km² in Amphora’s 397 published polygons (828,429 m²)"),
             ("72.5%", GREEN, "of a random sample of that area went from green to grey in imagery (95%: 57–84%)"),
             ("59%", AMBER, "of the sampled land was fields before; Amphora says nearly 95% farmland"),
             ("2–3%", RED, "of an independent model’s new built-up land lies inside the polygons")]),
      Spacer(1, 4 * mm),
      up_down("Amphora’s basis for the 95% and the imagery dates it used; imagery from 2017 to mid-2018; a larger "
              "imagery sample with a similar result.",
              "Evidence that much more of the area changed before 2018 or after 2023 than in our sample, or a larger "
              "sample confirming less than half of it."),
      Spacer(1, 5 * mm)]
S += toc([("1", "The claim and what we could verify"), ("2", "Method"), ("3", "How the satellite data work"),
          ("4", "What the data show"), ("5", "Where the evidence points different ways"),
          ("6", "Testing the claim"), ("7", "Verdict and requests for evidence"), ("8", "Limitations")])
S.append(PageBreak())

# ================================================================== 1
S.append(SectionHeading(1, "The claim and what we could verify"))
S.append(P("Amphora Media published the investigation on 11 September 2026 [1] with a companion piece on agricultural "
           "land the next day [2], in collaboration with Arena for Journalism in Europe and supported by The Malta "
           "Environment Foundation. We read both in full. The change polygons behind the article’s interactive map are a "
           "public file on Amphora’s website [8]; we downloaded it on 5 October 2026."))
S.append(std_table([
    [C("What was said", cellh), C("Where", cellh), C("Access", cellh)],
    [C("“nearly 830,000 square metres of nature and cropland have been built up in Malta between 2018 and 2023” "
       "(headline: “over 830,000”)"), C("Amphora [1]"), C("Read in full")],
    [C("Total land loss 0.26%, “among the top 5 countries”; “a conservative estimate”"), C("Amphora [1]"),
     C("Read in full")],
    [C("EEA: 920,000 m² (2012–2018) and 190,000 m² (2006–2012); “at least 1.94 square kilometres” since 2006"),
     C("Amphora [1]"), C("Checked [7, 9]")],
    [C("“in nearly 95% of the take-up, farmland rather than natural area was affected”"), C("Amphora [2]"),
     C("Read in full")],
    [C("The map: 397 change polygons, each with its 2018 class (Dynamic World) and its status (“Built / developed”)"),
     C("Amphora [8]"), C("Downloaded")],
], [104 * mm, 34 * mm, 32 * mm]))

# ================================================================== 2
S.append(Spacer(1, 4 * mm))
S.append(SectionHeading(2, "Method"))
S.append(P("<b>Questions.</b> Does Amphora’s map add up to 830,000 m², does independent data confirm the land it "
           "flags, are the comparisons right, and was the land mostly farmland?"))
S.append(P("<b>Evidence.</b> Amphora’s method [1] uses Google and WRI’s Dynamic World [3], with each flagged area "
           "checked by eye. We measured its published polygons in UTM 33N [8]; the file has no stated licence, so we do "
           "not redistribute it and record its SHA-256 instead. For an independent check we used a different model, "
           "Impact Observatory and Esri’s 10 m annual land cover [4, 5]: 2017–2023 through Microsoft Planetary Computer "
           "and, new in version 1.2, 2024 and 2025 from Esri’s image service [10], whose 2017–2023 maps are identical "
           "to the first set pixel for pixel. We laid Amphora’s polygons over these maps (pixel centres, with a 20 m "
           "tolerance as a check). The EEA’s CORINE Land Cover change maps [9] test the EEA figures. Island areas are "
           "from OpenStreetMap. At the maintainer’s request we also checked a random sample of Amphora’s polygons "
           "against high-resolution satellite imagery in Esri’s World Imagery Wayback archive [11, 12] (section 4). Scripts "
           "and data: <i>tools/cc-019-report/</i> and <i>data/cc-019/</i>."))
S.append(P("<b>Grades.</b> Satellite land cover is a direct, model-classified measurement (grade B), and so is our "
           "visual check of a random sample of imagery; CORINE and the EEA chart are official statistics (grade C). "
           "◆ marks a source known second-hand."))

# ================================================================== 3
S.append(CondPageBreak(70 * mm))
S.append(SectionHeading(3, "How the satellite data work"))
S.append(P("Both products classify every 10 m pixel with a deep-learning model trained on Sentinel-2 imagery [3, 4]. "
           "Single-year maps are noisy: in the Impact Observatory data Malta’s built-up area changes by 3 to 27 km² "
           "from one year to the next (−21 km² from 2023 to 2024, +23 km² from 2024 to 2025); the largest swing is over "
           "thirty times the 0.83 km² being measured. Comparing the 2018 and 2023 maps directly gives 24 km² of newly "
           "built-up pixels, or 18.9 km² net, which is not credible. We therefore counted only pixels that changed "
           "consistently: not built up in each of several early maps and built up in each of several later ones, and "
           "subtracted the reverse change as a gauge of noise. Each rule sees only land first mapped as built in a "
           "particular window: 2020–21 (3-year rule, maps 2017–19 against 2021–23), 2019–22 (2-year rule), and, with the "
           "2024 and 2025 maps, 2020–23 and 2019–24. Amphora handled the same problem by checking each flagged area by "
           "eye, which removes false alarms but can miss developments, as it notes."))

# ================================================================== 4
S.append(CondPageBreak(150 * mm))
S.append(SectionHeading(4, "What the data show"))
S.append(fig(FIG / "fig1_overlap.png"))
S.append(P("Figure 1. Amphora’s polygons (orange) over the land the independent model maps as newly built-up, first "
           "mapped in 2019–24 (blue). Close-ups: grey is land the model already mapped as built-up in 2018. The two "
           "rarely coincide. Polygons: Amphora Media [8].", cap))
S.append(fig(FIG / "fig2_estimates.png"))
S.append(P("Figure 2. Left: Amphora’s figure against the independent model’s net totals under four rules; the result "
           "swings from 3.0 to below zero with the years used. Right: what the land was in 2018, in Amphora’s own "
           "classes and in the model’s.", cap))
S.append(CondPageBreak(110 * mm))
S.append(std_table([
    [C("Check", cellh), C("Result", cellh), C("Amphora", cellh), C("Grade", cellh)],
    [C("Area of Amphora’s 397 polygons [8]"), C("<b>828,429 m²</b>"), C("nearly (headline: over) 830,000 m²"),
     C("–")],
    [C("830,000 m² as a share of Malta’s land (314 km²)"), C("0.264%"), C("0.26%"), grade_tag("C")],
    [C("In FIFA pitches; vs Comino; vs Manoel Island"), C("116; 0.24–0.30; 2.7"), C("116; roughly a quarter; two"),
     grade_tag("C")],
    [C("Cropland + grass, of the area with a known 2018 class [8]"), C("96% (95.3–95.7%)"),
     C("nearly 95% farmland"), C("–")],
    [C("Area with no 2018 class; polygons that were sea in 2018 [8]"), C("37%; 2 (4,429 m²)"), C("–"), C("–")],
    [C("Imagery: Amphora’s area confirmed green to grey, 40 draws [11]"), C("<b>72.5%</b> (57–84%)"), C("–"),
     grade_tag("B")],
    [C("Imagery: fields, share of the land before [11]"), C("59% (64% with orchards)"), C("nearly 95% farmland"),
     grade_tag("B")],
    [C("Amphora’s area already built-up in the 2018 map [5]"), C("68% (61% in all of 2017–19)"), C("–"),
     grade_tag("B")],
    [C("Amphora’s area the model maps as newly built [5]"), C("6–14%"), C("–"), grade_tag("B")],
    [C("Model’s new built-up land inside Amphora’s polygons [5]"), C("<b>2–3%</b> (5–7% within 20 m)"), C("–"),
     grade_tag("B")],
    [C("Model’s net new built-up, four rules [5, 10]"), C("−0.06 to 2.96 km²"), C("0.83 km²"), grade_tag("B")],
    [C("Model: new built-up was crops / rangeland / bare (3-year rule)"), C("65% / 31% / 4%"),
     C("nearly 95% farmland"), grade_tag("B")],
    [C("CORINE: new artificial land 2006–12 / 2012–18 [9]"), C("20.6 ha / 93.7 ha"), C("19 ha / 92 ha"),
     grade_tag("C")],
    [C("EEA chart, land take 2012–18 [7]"), C("0.91–0.94 km²; highest of 39"), C("0.92 km²"), grade_tag("C")],
    [C("EEA 2006–12 + 2012–18 + Amphora 2018–23"), C("1.94 km²"), C("at least 1.94 km²"), grade_tag("C")],
], [70 * mm, 40 * mm, 46 * mm, 14 * mm]))
S.append(P("All values in <i>data/cc-019/checks.csv</i>, <i>amphora_classes.csv</i>, <i>amphora_io_overlap.csv</i> and "
           "<i>imagery_spotcheck_summary.csv</i>. Comino: 0.30 of its 2.8 km² OpenStreetMap outline, 0.24 of the 3.5 km² "
           "often quoted. Amphora’s figures have no grade: they are the claim being tested.", cap))

# ------------------------------------------------------------------ 4, imagery spot-check (maintainer decision)
SS = {(r["group"], r["item"]): r for r in csv.DictReader(open(DATA / "imagery_spotcheck_summary.csv"))}
SP = list(csv.DictReader(open(DATA / "imagery_spotcheck.csv")))
nd = sum(int(r["draws"]) for r in SP)
nt = sum(int(r["draws"]) for r in SP if r["class"] == "unclear" and r["state_sep_2018"] == "mostly cleared or built")
gr = [r for r in SP if r["amphora_lc2018"] == "grass"]
gf = sum(r["before_land_type"] in ("cultivated field", "fallow field") for r in gr)
na = sum(int(r["draws"]) for r in SP if r["class"] == "confirmed" and r["grey_by_may_2023"] != "yes")
assert (round(100 * nt / nd, 1), round(100 * na / nd, 1)) == (15.0, 17.5)  # quoted in the prose: keep in step


def pct(v):
    """Shares that are whole draws out of 40 are exact (steps of 2.5); others are rounded to whole numbers."""
    v = float(v)
    return f"{v:g}" if round(v * 10) % 25 == 0 else f"{round(v)}"


def share(r, ci=True):
    return f"{pct(r['share_of_draws_pct'])}%" + (
        f" ({float(r['wilson95_lo_pct']):.0f}–{float(r['wilson95_hi_pct']):.0f}%)" if ci and r["wilson95_lo_pct"] != ""
        else "")


cls = lambda k: SS[("class", k)]
S.append(CondPageBreak(90 * mm))
S.append(P("Imagery spot-check of Amphora’s polygons", h2))
S.append(P("<b>Method.</b> We drew 40 points on Amphora’s 828,429 m² by systematic sampling with probability "
           "proportional to polygon area (random order and start, seed 20261005), so each draw stands for an equal "
           "slice of the area; they fell in 39 polygons. For each we laid the outline over Esri Wayback imagery [11] from "
           "before July 2018, 4 September 2018, 6 May 2023 and June to September 2025, dated from Esri’s metadata [12], "
           "and classed it by eye: <i>confirmed</i> if most of it was open or green before and built, paved, quarried, a "
           "yard or a construction site in 2025. The archive has no image of these spots from August 2016 to September "
           "2018, so every “before” image dates from July 2015 to August 2016; where most of a polygon was already under "
           "construction, built or quarried by September 2018 we class it <i>unclear</i>. The imagery is not reproduced "
           "(Esri’s terms); the class and a note for every polygon are in <i>data/cc-019/imagery_spotcheck.csv</i>."))
S.append(std_table([
    [C("Class (draws)", cellh), C("Share of Amphora’s area (95% interval)", cellh), C("What we saw", cellh)],
    [C(f"Confirmed ({cls('confirmed')['draws']})"), C(f"<b>{share(cls('confirmed'))}</b>"),
     C("Fields, scrub or garrigue before; buildings, roads, yards, quarry or works by 2025")],
    [C(f"Partial ({cls('partial')['draws']})"), C(share(cls("partial"))),
     C("Part already a yard or spoil before, or an unsealed boat yard after")],
    [C(f"Unclear ({cls('unclear')['draws']})"), C(share(cls("unclear"))),
     C(f"{nt} open in 2015–16 but mostly being developed by September 2018; 1 surface not visible")],
    [C(f"Already grey ({cls('already grey')['draws']})"), C(share(cls("already grey"))),
     C("A graded development platform before 2016")],
    [C(f"Still open ({cls('still open')['draws']})"), C(share(cls("still open"))), C("None")],
], [34 * mm, 52 * mm, 84 * mm]))
S.append(Spacer(1, 3 * mm))
r23 = SS[("rule", "confirmed and mostly grey by 6 May 2023 (article's 2018-2023)")]
grp = "before land type (draws open in the before image)"
fo = pct(SS[(grp, "farmland (fields + orchards)")]["share_of_draws_pct"])
ag = cls("already grey")["share_of_draws_pct"]
S.append(P(f"<b>Result.</b> {share(cls('confirmed'))} of the sampled area went from open or green land to built-up or "
           f"grey; {pct(SS[('rule', 'confirmed + half of partial')]['share_of_draws_pct'])}% if partial polygons count as "
           f"half. Only one draw was already grey and none was still open. Counting only land that was mostly grey by "
           f"May 2023, the article’s window, the share is {share(r23)}: 17.5% of the area turned grey later, in line "
           f"with the map file’s 2018–2025. Before the change, {share(SS[(grp, 'fields (cultivated + fallow)')])} of the "
           f"sampled land was fields, cultivated or fallow, and {fo}% "
           f"with orchards; the rest was scrub, garrigue or rough grass, often on vacant plots beside built-up land. Of "
           f"the {len(gr)} sampled polygons Amphora classes as “grass”, {gf} were fields and {len(gr) - gf} scrub or "
           f"garrigue."))
S.append(P("<b>What it means.</b> More than half of the sampled area is confirmed, so by the maintainer’s rule, set "
           "before the check, confidence stays moderate. On what stood there before, the imagery sides with Amphora: "
           f"the model maps 68% of this area as built-up in 2018, the imagery {pct(ag)}% "
           f"({float(ag) + 100 * nt / nd:.1f}% counting land being "
           "developed by September 2018). We did not check the model’s new built-up land outside Amphora’s polygons, so "
           "whether Amphora missed developments is untested. The farmland share is well below 95%, even at the top of "
           "its interval, unless scrub and rough grass are counted as farmland."))

# ================================================================== 5
S.append(CondPageBreak(80 * mm))
S.append(SectionHeading(5, "Where the evidence points different ways"))
S.append(contested(
    "Q1  Is 830,000 m² right?", "MOSTLY CONFIRMED", LG,
    "Amphora’s polygons add up to 828,429 m², and it says each area was checked by eye. In imagery, 72.5% of a "
    "random sample of that area (57–84%) went from open or green land to grey; only 2.5% was already grey. The "
    "model agrees that 88% of the area was built-up by 2023 and 92% by 2025.",
    "The model maps 68% of the area as built-up already in 2018, and only 2–3% of its own new built-up land lies "
    "inside Amphora’s polygons. In the imagery sample 15% of the area was already being developed by September "
    "2018, and 17.5% turned grey only after May 2023.",
    "<b>For this claim:</b> the imagery settles the main disagreement in Amphora’s favour: these parcels were "
    "mostly green before. The figure fits 2018–2025, the map file’s years, better than the article’s 2018–2023, and "
    "no check here looks for developments Amphora missed."))
S.append(contested(
    "Q2  Was 95% of it farmland?", "OVERSTATED", AMBER,
    "In Amphora’s own data, cropland and grass make up 96% of the area with a known 2018 class. Amphora may count "
    "grassland as farmland; it has not said. Abandoned fields can look like scrub from above.",
    "Dynamic World’s “grass” includes natural meadows and excludes plotted fields, which it calls crops [3]; 37% of "
    "the area has no 2018 class. In our imagery sample fields were 59% of the land before (43–73%), 64% with "
    "orchards; the rest was scrub, garrigue or rough grass.",
    "<b>For this claim:</b> most of the land was farmland, but “nearly 95%” holds only if scrub and rough grass on "
    "vacant plots are counted as farmland."))
S.append(contested(
    "Q3  Over or nearly 830,000?", "HEADLINE ROUNDS UP", GREY,
    "The text says “nearly”, and the polygons add up to 828,429 m².",
    "The headline says “over” 830,000.",
    "<b>For this claim:</b> a minor point that does not change the finding."))

# ================================================================== 6
S.append(CondPageBreak(100 * mm))
S.append(SectionHeading(6, "Testing the claim"))
verd = lambda t, c: chip(t, c, w=29 * mm)
S.append(std_table([
    [C("Sub-claim", cellh), C("What the evidence shows", cellh), C("Rating", cellh)],
    [C("<b>A.</b> About 830,000 m² of green land built up 2018–2023"),
     C("Amphora’s polygons add up to 828,429 m² (two, 4,429 m², were sea in 2018). Imagery confirms green to grey "
       "for 72.5% of a random sample of the area (57–84%), 55% by May 2023; 15% was being developed by September "
       "2018. An independent model flags largely different land."), verd("LARGELY SUPPORTED", LG)],
    [C("<b>B.</b> 0.26% of land; comparisons (pitches, Comino, Manoel)"), C("Arithmetic checks out (Comino: 0.24 of the "
       "3.5 km² often quoted, 0.30 of the OSM outline; Manoel: 2.7, not two)."), verd("SUPPORTED", GREENC)],
    [C("<b>C.</b> Nearly 95% of take-up was farmland"),
     C("Cropland + grass = 96% of the area with a known 2018 class (our reading of the basis), but only if all grass is "
       "farmland; 37% has no class. In imagery, fields were 59% of the sampled land, 64% with orchards."),
     verd("PARTLY SUPPORTED", AMBER)],
    [C("<b>D.</b> EEA figures and the 1.94 km² total"), C("CORINE change maps: 20.6 ha (2006–12) and 93.7 ha (2012–18) "
       "[9]; EEA chart 0.91–0.94 km² [7]; sum correct."), verd("SUPPORTED", GREENC)],
], [52 * mm, 88 * mm, 30 * mm], valign="MIDDLE"))

# ================================================================== 7
S += [Spacer(1, 6 * mm), SectionHeading(7, "Verdict and requests for evidence"),
      verdict_box("Largely supported", "Amphora’s map adds up and imagery confirms most of a random sample of it; "
                  "the years are looser than stated and the 95% farmland share is overstated. Confidence: moderate."),
      Spacer(1, 4 * mm)]
S.append(P("<b>Why.</b> (1) The figure is the area of Amphora’s published polygons, and the arithmetic, comparisons "
           "and EEA figures are right. (2) Imagery of a random sample confirms green-to-grey change on 72.5% of the "
           "area (57–84%) and finds almost none already built; the independent model’s contrary reading of 2018 does "
           "not hold on these parcels, so the model’s failure to confirm the figure weighs little. (3) The years are "
           "looser than “2018 to 2023”: 15% of the sampled area was already being "
           "developed by September 2018 and 17.5% turned grey only after May 2023, in line with the map file’s "
           "2018–2025. (4) The 95% farmland share is overstated: fields were 59% of the sampled land, 64% with "
           "orchards; and the headline rounds up a number the text rounds down. These limit how exactly the figure fits "
           "its stated period and land type, not whether the land was built over. Confidence is moderate by the rule "
           "the maintainer set before the check: more than half of the sampled area confirmed."))
S.append(P("Evidence we are asking for", h2))
S.append(requests_list([
    "Amphora: the basis and period of the 95% farmland figure, and how “grass” was counted.",
    "Amphora: whether the polygons cover 2018–2023 or 2018–2025 (the map file says 2018–2025; in our sample 17.5% "
    "of the area turned grey after May 2023), and the 2018 class of the 162 polygons marked unknown.",
    "Anyone: imagery of Malta from 2017 to mid-2018, to date the 15% of the sampled area already being developed by "
    "September 2018; and a check for developments Amphora’s map missed.",
]))

# ================================================================== 8
S += [Spacer(1, 6 * mm), SectionHeading(8, "Limitations")]
for l in ["Land-cover models misclassify pixels; our rules reduce but do not remove this.",
          "The imagery check is by eye, by us, on 40 draws in 39 polygons, so its 95% interval spans about ±13 "
          "points. The “before” images are from July 2015 to August 2016 and the next from 4 September 2018, so "
          "changes in between cannot be dated. Small polygons and unsealed yards are hard to judge, and fallow fields "
          "and scrub are hard to tell apart. The check does not look for developments Amphora missed.",
          "Amphora’s polygons are small (median 504 m², about five pixels); a 20 m tolerance raises the overlap only "
          "to 5–7%, so misalignment does not explain it.",
          "The persistence rules only see land first mapped as built in set windows (2019–24 at most), not exactly "
          "2018–2023.",
          "Amphora’s map file gives its years as 2018–2025 and each polygon’s status as of 2025; the article says "
          "2018–2023.",
          "CORINE maps only changes of 5 ha or more; every one of Amphora’s polygons (the largest is 3.3 ha) is "
          "below that.",
          "Built-up land includes roads, car parks and quarries as well as buildings; so does Amphora’s. Neither "
          "estimate says whether development was inside or outside the development zone.",
          "Class names differ between the two models; ‘rangeland’ in IO is not the same as ‘natural’."]:
    S.append(P("• " + l, bul))

S += [Spacer(1, 6 * mm), SectionHeading(None, "References")]
S += references([
    ("1", "Amphora Media (11 Sep 2026). Green To Grey: Malta lost over 830,000 square metres of land to development in "
          "five years.", "https://www.amphora.media/2026/09/green-to-grey-malta-land-loss-development-construction"),
    ("2", "Amphora Media (12 Sep 2026). Green to Grey: when development creeps up on agricultural land.",
     "https://www.amphora.media/2026/09/green-to-grey-development-agricutlural-land"),
    ("3", "Brown C.F. et al. (2022). Dynamic World, near real-time global 10 m land use land cover mapping. "
          "<i>Scientific Data</i> 9:251. doi:10.1038/s41597-022-01307-4. (Class definitions, Table 1, read.)",
     "https://doi.org/10.1038/s41597-022-01307-4"),
    ("4", "Karra K. et al. (2021). Global land use / land cover with Sentinel 2 and deep learning. <i>IGARSS 2021</i>, "
          "4704–4707. doi:10.1109/IGARSS47720.2021.9553499.", "https://doi.org/10.1109/IGARSS47720.2021.9553499"),
    ("5", "Impact Observatory and Esri. 10 m Annual Land Use Land Cover (9-class) V2, 2017–2023; Microsoft Planetary "
          "Computer; retrieved 4 Oct 2026.", "https://planetarycomputer.microsoft.com/dataset/io-lulc-annual-v02"),
    ("6", "MiŻien. Data and calculations: data/cc-019/; tools/cc-019-report/.", ""),
    ("7", "European Environment Agency (2019, modified 2024). Country comparison: land take and land recultivation in "
          "EEA39 in the period 2012–2018 (in proportion of country area). Value read from the chart.",
     "https://www.eea.europa.eu/en/analysis/maps-and-charts/country-comparison-land-take-and"),
    ("8", "Amphora Media (2026). Green to Grey change polygons for Malta, malta-change.geojson (generated 30 Aug 2026; "
          "retrieved 5 Oct 2026; SHA-256 cf250ece…fcf320). Not redistributed.",
     "https://www.amphora.media/greentogrey/data/malta-change.geojson"),
    ("9", "European Environment Agency. CORINE Land Cover change layers 2006–2012 and 2012–2018 (CHA0612, CHA1218), "
          "discomap map service; queried 5 Oct 2026.", "https://image.discomap.eea.europa.eu/arcgis/rest/services/Corine"),
    ("10", "Impact Observatory, Microsoft and Esri. Sentinel-2 10m Land Cover time series, 2017–2025 (Esri Living "
           "Atlas image service); retrieved 5 Oct 2026.",
     "https://ic.imagery1.arcgis.com/arcgis/rest/services/Sentinel2_10m_LandCover/ImageServer"),
    ("11", "Esri. World Imagery Wayback, releases of 18 Jan 2018, 30 Oct 2019, 7 Mar 2024 and 26 Mar 2026 (imagery "
           "acquired Jul 2015–Aug 2016, 4 Sep 2018, 6 May 2023 and Jun–Sep 2025 by Maxar/Vantor satellites, 0.3–0.5 m); "
           "viewed 5 Oct 2026. Not reproduced.",
     "https://wayback.maptiles.arcgis.com/arcgis/rest/services/World_Imagery"),
    ("12", "Esri. World Imagery metadata layers for each Wayback release (acquisition date SRC_DATE, sensor, "
           "resolution); queried 5 Oct 2026.", "https://metadata.maptiles.arcgis.com/arcgis/rest/services"),
])

S.append(PageBreak())
S += appendix_a("A experiment · B observational study with a control or gradient, or direct measurement · C review, "
                "guidance or official statistics · D assertion or anecdote. ◆ marks a source known only second-hand.")
S += [Spacer(1, 5 * mm)]
S += revision_log([("1.0", "4 Oct 2026", "First issue. Right of reply to Amphora Media not yet sent."),
                   ("1.1", "5 Oct 2026", "Corrections. (1) Periods of the independent estimates: “2018–2023” → land "
                    "first mapped as built in 2020–21 (3-year rule) and 2019–22 (2-year rule), which is what the rules "
                    "can detect (TL;DR, tile, sections 3, 4, 5 and 6, limitations, Figure 2 labels and caption). "
                    "(2) Comino: “about 0.3 of Comino, as stated” → Amphora says “roughly a quarter”; 830,000 m² is 0.24 "
                    "of the 3.5 km² often quoted and 0.30 of the 2.8 km² OpenStreetMap outline. (3) Simple comparison: "
                    "“would give 24 km²” → 24 km² of newly built-up pixels, 18.9 km² net (now saved in "
                    "<i>data/cc-019/io_lulc_change.csv</i>). (4) Year-to-year noise: “more than 15 km², twenty times the "
                    "change” → 3 to 27 km², the largest over thirty times 0.83 km²; flyer “15 km² a year” → “up to "
                    "27 km² from year to year”. (5) The TL;DR now says the two estimates are not like for like. Verdict and "
                    "confidence unchanged."),
                   ("1.2", "5 Oct 2026", "Upgrade. (1) Amphora’s published change polygons [8] measured: 397 polygons, "
                    "828,429 m², so “nearly 830,000” is reproduced and the headline’s “over” is not. (2) Spatial "
                    "cross-check with the independent model: “an independent measurement finds more, not less” and "
                    "“plausible and conservative” → the model already maps 68% of Amphora’s area as built-up in 2018, "
                    "6–14% as new, and only 2–3% of its new built-up land lies inside Amphora’s polygons, so it neither "
                    "confirms nor rules out the figure (TL;DR, tiles, sections 2–8, flyer). (3) The 2024 and 2025 maps "
                    "added from Esri’s service (identical to the earlier maps for 2017–2023): net totals −0.06 to "
                    "2.96 km² by rule. (4) Sub-claim A “supported” → “plausible”; sub-claim C “not shown” → “needs "
                    "context”: cropland + grass = 96% of the area with a known 2018 class (our reading of the basis of "
                    "“nearly 95%”). (5) Sub-claim D: the 2006–2012 EEA figure checked with the CORINE change map "
                    "(20.6 ha; 93.7 ha for 2012–2018). (6) New Figure 1 (Amphora’s polygons over the model’s new "
                    "built-up land), replacing the map of new built-up pixels; Figure 2 redrawn with four rules and "
                    "Amphora’s own 2018 classes. Verdict and confidence unchanged."),
                   ("1.2", "5 Oct 2026", "Maintainer decision (5 Oct 2026): imagery spot-check of Amphora’s polygons, "
                    "with confidence set by a rule fixed beforehand (moderate if more than half of the sampled area is "
                    "confirmed, low otherwise). 40 draws by systematic sampling proportional to area (seed 20261005; 39 "
                    "polygons) checked by eye against Esri World Imagery Wayback [11, 12] from 2015–16, 2018, 2023 and "
                    "2025: 72.5% of the sampled area confirmed green to grey (95% interval 57–84%), 7.5% partial, 2.5% "
                    "already grey, 17.5% unclear (15% being developed by September 2018); 55% grey by May 2023; fields "
                    "59% of the land before (64% with orchards). Confidence: moderate. New subsection and table rows in "
                    "section 4; TL;DR (key points, tiles, what would move the verdict), sections 2, 5 to 8 and the flyer "
                    "updated; Q1 “plausible, unconfirmed” → “mostly confirmed”; Q2 “depends on definitions” → "
                    "“overstated”; sub-claim A “plausible” → “largely supported”; sub-claim C “needs context” → "
                    "“partly supported”. Verdict unchanged.")])

build_report(Report(
    number="019", out=str(FIG / "report.pdf"), kicker="Land and trees",
    title_lines=["830,000 m² of", "green land", "built over?"],
    subtitle_lines=["Testing a newsroom’s satellite estimate of land lost to development in Malta",
                    "against its own map, satellite images, an independent land-cover model and EEA data"],
    quote_lines=["“Nearly 830,000 square metres of nature", "and cropland have been built up in Malta",
                 "between 2018 and 2023.”"], quote_size=15,
    attribution="Amphora Media, Green to Grey, 11 September 2026.",
    context="Companion piece: nearly 95% of the take-up was farmland.",
    verdict="Largely supported", verdict_note="Matches Amphora’s own map; imagery confirms most of a sample",
    footer_lines=["Version 1.2  ·  5 October 2026", "Status: draft (right of reply: Amphora Media)",
                  "Prepared from public sources, Amphora’s map, high-resolution images and land cover.",
                  "Repository: github.com/leandergrech/Mizien"],
    running_head="Green to grey – Malta", version="1.2", date="5 October 2026",
    pdf_title="830,000 m2 of green land built over? Claim Check 019",
    pdf_subject="Tests Amphora Media's estimate of green land built up in Malta, 2018-2023",
    story=S))
