"""Claim Check 138 report. Run calc.py and figures.py first. Output: out/report.pdf"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import *  # noqa: E402,F401

FIG = HERE / "out"
S = []
S += [SectionHeading(None, "TL;DR"), Spacer(1, 1 * mm),
      P("On 29 July 2026 the Office of the Prime Minister (OPM) announced that Cabinet had approved a legal notice "
        "establishing White Rocks, Pembroke, as a national park. Its statement, in Maltese, said the step would let the "
        "site be protected and safeguarded, with Project Green administering the park, and that it <b>“continues the "
        "pledge” that parks and public gardens be given protection through legal amendments, “to be safeguarded from "
        "any future development”</b>. MaltaToday reported this as the site receiving “legal protection to safeguard it "
        "against future development”.", lead)]
S.append(key_points([
    ("The notice exists and was published two days later.",
     "L.N. 209 of 2026 appeared in the Gazette on 31 July 2026. It establishes the park within a mapped boundary."),
    ("It contains no protection against development.",
     "None of its five regulations restricts building, works or any other activity. Regulation 4 keeps existing "
     "permits, authorisations, access rights and farming."),
    ("It does not name Project Green or any manager.",
     "Nor does it say what the park is for. The Majjistral park’s regulations do both and list banned activities."),
    ("Protection is possible but has not been done.",
     "The Environment Protection Act lets works in a protected area be restricted by regulations or a conservation "
     "order. No 2026 legal notice up to L.N. 309 does so for White Rocks. We could not read the site’s planning zoning."),
    ("Verdict: not substantiated (moderate confidence). The pledge is not yet due.",
     "Nothing in the notice protects the site from development, so the OPM’s link to that pledge goes beyond what it "
     "does. The manifesto pledge runs to the end of the legislature."),
]))
S += [Spacer(1, 2.5 * mm), VerdictMeter(2), Spacer(1, 3 * mm),
      tiles([("5", AMBER, "regulations in L.N. 209 of 2026: title, definitions, establishment and two savings clauses"),
             ("0", RED, "of them restrict building, works or any other activity in the park"),
             ("0", RED, "mentions of Project Green, or of any manager, in the notice"),
             ("100", GREY, "later 2026 legal notices searched (L.N. 210–309): none concerns White Rocks")]),
      Spacer(1, 4 * mm),
      up_down("A regulation, conservation order or local plan change that restricts development inside the park, or "
              "a document showing the site is already zoned so that development cannot be permitted.",
              "Evidence of development being planned or permitted inside the park boundary after the notice."),
      Spacer(1, 3 * mm)]
S += toc([("1", "The claim and what we could verify"), ("2", "Method"), ("3", "What the notice does"),
          ("4", "What protects a site from development"), ("5", "Where the evidence points different ways"),
          ("6", "Testing the claim"), ("7", "Verdict, pledge label and requests for evidence"), ("8", "Limitations")])
S.append(PageBreak())

S.append(SectionHeading(1, "The claim and what we could verify"))
S.append(P("The OPM’s statement was issued in Maltese by the Department of Information as press release PR261268, "
           "dated 29 July 2026 [1]. The two sentences on White Rocks say, in our translation: “This will mean that the "
           "site can be protected and safeguarded, with the aim of giving public access, recreational use and "
           "conservation the highest priority, with the Project Green agency responsible for administering the Park. "
           "This continues the pledge that the parks and public gardens made in recent years be given protection "
           "through legal amendments so that they are safeguarded from any future development.” The statement calls "
           "the step “the beginning of the fulfilment” of another manifesto pledge. MaltaToday’s report the same day "
           "turned this into a direct statement about the site [2]. The legal notice was gazetted on 31 July [3]."))
S.append(std_table([
    [C("Source", cellh), C("What it says", cellh), C("Our access", cellh), C("Status", cellh)],
    [C("<b>OPM</b>, press release PR261268, 29 Jul 2026 [1]"),
     C("“…jingħataw il-protezzjoni permess [sic] ta’ emendi legali biex jiġu mħarsa minn kwalunkwe żvilupp fil-futur” "
       "(protection through legal amendments, safeguarded from any future development); Project Green to administer."),
     C("Read in full in a browser, 17 Nov 2026 (doi.gov.mt refuses scripts)."), C("<b>The claim</b>")],
    [C("<b>MaltaToday</b>, 29 Jul 2026 [2]"),
     C("“will receive legal protection to safeguard it against future development” (outlet’s paraphrase)."),
     C("Browser copy supplied by the maintainer, read in full."), C("<b>Restatement</b>")],
    [C("<b>L.N. 209 of 2026</b> [3]"),
     C("Five regulations and a boundary map."), C("PDF from legislation.mt, read in full."), C("<b>Primary law</b>")],
    [C("<b>Environment Protection Act</b>, Cap. 549 [4]"),
     C("Powers to make regulations (arts 54–55) and to restrict works in protected areas (art. 69)."),
     C("Consolidated PDF, relevant articles read."), C("<b>Primary law</b>")],
    [C("<b>Labour manifesto 2026</b> [5]"),
     C("White Rocks to become a natural park and to be protected “once and for all” from development (p. 162); legal "
       "amendments to protect parks from development (p. 164)."),
     C("PDF, pages read; sha256 matches the project’s pledge list."), C("<b>Pledge</b>")],
    [C("<b>Ċirkewwa and Majjistral park instruments</b> [6–8]"),
     C("For comparison: what other park instruments under the same Act contain."),
     C("PDFs from legislation.mt, read in full."), C("<b>Primary law</b>")],
], [38 * mm, 66 * mm, 40 * mm, 26 * mm]))
S.append(Spacer(1, 2 * mm))
S.append(P("<b>Fairness note.</b> Establishing the park is a real step, and the White Rocks site was earlier offered for "
           "private development. This check asks only whether the notice gives the legal protection against "
           "development that the statement links it to. It does not question the Government’s intentions.", small))

S += [Spacer(1, 4 * mm), SectionHeading(2, "Method")]
S.append(P("<b>Questions.</b> (A) Was the notice approved and published? (B) Does it put Project Green in charge? "
           "(C) Does it protect the site, and set conservation and public access as priorities? (D) Does it give, or "
           "continue towards, legal protection against development?"))
S.append(P("<b>Evidence.</b> We read L.N. 209 of 2026 in full and the articles of the Environment Protection Act it "
           "cites. We compared it with the 2026 Ċirkewwa Marine Park notice and the Majjistral park regulations, "
           "recording which of nine provisions each contains (<i>data/cc-138/park_instruments.csv</i>). We read the "
           "full text of every later 2026 legal notice available on legislation.mt (L.N. 210–309) for any mention of "
           "White Rocks, Pembroke or a national park. Counts are in <i>data/cc-138/checks.csv</i>."))
S.append(P("<b>Grades.</b> The legal texts and the manifesto are primary documents (grade C, official). "
           "<b>Verdicts</b> follow the five-point scale in Appendix A; the pledge label follows the project’s pledge "
           "rules."))

S.append(CondPageBreak(120 * mm))
S.append(SectionHeading(3, "What the notice does"))
S.append(fig(FIG / "fig1_instruments.png", width=CW * 0.98))
S.append(P("Figure 1. Nine provisions in three park instruments made under the Environment Protection Act. Green: "
           "the provision is in the text.", cap))
S.append(P("L.N. 209 of 2026 was made by the Minister for the environment under articles 54 and 55 of the Act, after "
           "consulting the Environment and Resources Authority (ERA) [3]. Regulation 1 gives its title and its purpose, "
           "“to establish the White Rocks as a national park”. Regulation 2 defines terms. Regulation 3 establishes the "
           "park “as delineated in the site map” in the Schedule. Regulation 4 says the designation “shall not of itself "
           "prejudice” lawful existing farming, access rights, servitudes, permits or authorisations. Regulation 5 keeps "
           "any stricter protection under the Act or other law. That is the whole notice."))
S.append(P("Other park instruments made under the same Act go further. The Majjistral regulations declare the area "
           "protected, state that the designation is to protect its ecological processes, species and habitats, set "
           "up a management board, and require the board’s approval for any works [7]. Separate site regulations list "
           "banned and restricted activities, including temporary installations [8]. The Ċirkewwa Marine Park notice "
           "of 2026 is almost as short as White Rocks’, but it states that the park is to “promote and conserve” its "
           "natural features [6]. The White Rocks notice does none of these things, and Project Green does not appear "
           "in it."))

S.append(CondPageBreak(95 * mm))
S.append(SectionHeading(4, "What protects a site from development"))
S.append(fig(FIG / "fig2_timeline.png", width=CW * 0.98))
S.append(P("Figure 2. The pledge, the announcement and the notice.", cap))
S.append(P("The Act allows activities and works in a protected area to be “prohibited or restricted as provided in "
           "relevant regulations or in a conservation order” (art. 69(3)) [4]. Either route would give the park "
           "protection in law. Neither has been used for White Rocks: the notice restricts nothing, and none of the "
           "100 later legal notices we read mentions the site. ERA conservation orders are published separately, and "
           "we did not search those."))
S.append(P("Building in Malta needs a Planning Authority permit, judged against the local plan and planning policy. "
           "The manifesto itself treats the two as different steps. For Manoel Island it pledges to “change the local "
           "plan” so that no development can take place. For White Rocks it pledges the “necessary change” so the site "
           "is protected “once and for all” from development (p. 162). It also pledges legal amendments to protect "
           "parks generally (p. 164) [5]. The Planning Authority’s site refuses automated access and shows a security "
           "check, so we could not read the site’s current zoning. Whether it already blocks development is an open "
           "question, and it affects the verdict (Section 8)."))

S.append(CondPageBreak(80 * mm))
S.append(SectionHeading(5, "Where the evidence points different ways"))
S.append(contested("Is White Rocks now legally protected from development?", "NOT BY THIS NOTICE", ORANGE,
                   "The site is now a national park in law, with a mapped boundary. A park made under the "
                   "Environment Protection Act can be given restrictions by later regulations or a conservation order. "
                   "The OPM said the site “can be” protected, which is true, and called the step the “beginning” of "
                   "fulfilling a pledge [1].",
                   "The notice restricts nothing and keeps existing permits and authorisations (reg. 4). The statement "
                   "links it to protection “from any future development”, and MaltaToday reported that the site “will "
                   "receive legal protection” against development [1, 2]. No instrument that does this has been "
                   "published.",
                   "The OPM’s wording is hedged, but a reader would take from it that the notice protects the site from "
                   "development. The notice does not. Protection may come later, or may already exist in planning "
                   "policy we could not read.",
                   label_a="FOR THE CLAIM", label_b="AGAINST"))

S.append(CondPageBreak(120 * mm))
S.append(SectionHeading(6, "Testing the claim"))
verd = lambda t, c: chip(t, c, w=29 * mm)
S.append(std_table([
    [C("Sub-claim", cellh), C("Said by", cellh), C("What the evidence shows", cellh), C("Rating", cellh)],
    [C("<b>A.</b> Cabinet approved a legal notice establishing White Rocks as a national park"), C("OPM [1]"),
     C("L.N. 209 of 2026 was gazetted on 31 July 2026 and establishes the park within a mapped boundary."),
     verd("ACCURATE", GREENC)],
    [C("<b>B.</b> Project Green will be responsible for administering the park"), C("OPM [1]"),
     C("The notice names no manager. An administrative arrangement may exist, but it is not in law. The Majjistral "
       "regulations set up their park’s management in law."), verd("NOT IN THE NOTICE", AMBER)],
    [C("<b>C.</b> The site can be protected, with public access, recreation and conservation the highest priority"),
     C("OPM [1]"),
     C("The Act allows restrictions by regulation or conservation order, so protection is possible. The notice sets "
       "no priorities and restricts nothing."), verd("POSSIBLE, NOT DONE", AMBER)],
    [C("<b>D.</b> The step continues the pledge to protect parks “from any future development”; the site “will receive "
       "legal protection” against development"), C("OPM [1]; MaltaToday [2]"),
     C("No regulation restricts development, and regulation 4 keeps existing permits. No later 2026 notice concerns "
       "the site. Planning zoning not read."), verd("NOT SHOWN", ORANGE)],
], [42 * mm, 18 * mm, 76 * mm, 34 * mm], valign="MIDDLE"))

S += [Spacer(1, 6 * mm), SectionHeading(7, "Verdict, pledge label and requests for evidence"),
      verdict_box("Not substantiated", "The notice is real, but it does not protect White Rocks from development, and "
                  "it does not name Project Green. Confidence: moderate."), Spacer(1, 4 * mm)]
S.append(P("<b>Why.</b> The OPM linked the notice to legal protection against development. The text of the notice does "
           "not provide it. It establishes a park and expressly preserves existing permits and rights. The OPM’s own "
           "wording was careful (“can be protected”, “the beginning of the fulfilment”), so we do not rate it "
           "misleading. But the link to protection “from any future development” is stated more strongly than the "
           "notice supports. MaltaToday’s version, that the site “will receive legal protection”, goes further still. "
           "Confidence is moderate because the site’s planning zoning, which could already restrict development, was "
           "not read. <b>What this verdict does not say.</b> It does not say White Rocks will be developed, or that "
           "the park is without value."))
S.append(P("<b>Pledge label: not yet due (as of 17 November 2026).</b> The 2026 manifesto pledged the “necessary "
           "change” so that White Rocks is protected “once and for all” from development [5]. No deadline is stated, "
           "so the term of the legislature that began in 2026 applies. The pledge can be checked: it is met when an "
           "instrument in force prevents development on the site. The notice is not that instrument.", small))
S.append(P("Evidence we are asking for", h2))
S.append(requests_list(["From the OPM or the Ministry for the Environment: which legal instrument, made or planned, "
                        "will protect White Rocks from development, and when.",
                        "From Project Green: the legal basis on which it administers the park.",
                        "From the Planning Authority: the current local plan zoning of the White Rocks site, and "
                        "whether any development permit or application inside the park boundary is outstanding.",
                        "From ERA: whether a conservation order or management plan for the park is being prepared."]))
S += [Spacer(1, 4 * mm),
      callout([P("RIGHT OF REPLY", tag),
               P("Draft, pending right of reply to the Office of the Prime Minister. Not yet sent; the maintainer "
                 "decides when.", small)], bg=AMBER_PALE, bar=AMBER)]
S += [Spacer(1, 6 * mm), SectionHeading(8, "Limitations")]
for l in ["The Planning Authority’s site shows a security check to automated browsers, so the site’s local plan zoning "
          "and any permits were not read. If the zoning already prevents development, sub-claim D would move towards "
          "supported for the site, though not because of the notice.",
          "We searched legal notices only, up to L.N. 309 of 2026 (17 Nov 2026). ERA conservation orders, Government "
          "Notices and Bills before Parliament were not searched.",
          "The OPM statement is in Maltese; the translations are ours. doi.gov.mt refuses scripts, so the page was read "
          "in a browser and needs archiving by hand.",
          "The park’s area was not measured from the Schedule map. The manifesto gives 369,000 m²."]:
    S.append(P("• " + l, bul))
S += [Spacer(1, 6 * mm), SectionHeading(None, "References")]
S += references([
    ("1", "Department of Information. Stqarrija mill-Uffiċċju tal-Prim Ministru: Pass eqreb biex il-White Rocks isir "
          "Park Nazzjonali, PR261268, 29 July 2026 (read in a browser 17 Nov 2026).",
     "https://departmentofinformation.gov.mt/press-release/2026/pr261268"),
    ("2", "MaltaToday. Cabinet approves legal notice classifying White Rocks as national park, 29 July 2026 (maintainer "
          "copy, read 17 Nov 2026).",
     "https://www.maltatoday.com.mt/news/national/143517/cabinet_approves_legal_notice_classifying_white_rocks_as_national_park"),
    ("3", "L.N. 209 of 2026. Establishment of the White Rocks National Park Regulations, 2026. Government Gazette "
          "No. 21,695, 31 July 2026.", "https://legislation.mt/eli/ln/2026/209/eng"),
    ("4", "Environment Protection Act (Cap. 549), consolidated; articles 54, 55 and 69.",
     "https://legislation.mt/eli/cap/549/eng"),
    ("5", "Partit Laburista. Int Malta: Manifest Elettorali 2026, PDF pp. 162 and 164 (retrieved 17 Nov 2026; sha256 "
          "466a60f9…1ceb).",
     "https://partitlaburista.org/wp-content/uploads/2026/08/Manifest_Elettorali_INT_MALTA_2026.pdf"),
    ("6", "L.N. 51 of 2026. Establishment of the Ċirkewwa Marine Park Regulations, 2026.",
     "https://legislation.mt/eli/ln/2026/51/eng"),
    ("7", "S.L. 549.48. Establishment of the Majjistral, Nature and History Park Regulations (L.N. 251 of 2007, as "
          "amended to L.N. 184 of 2025).", "https://legislation.mt/eli/sl/549.48/eng"),
    ("8", "S.L. 549.83. Majjistral Nature and History Park Site Regulations (L.N. 217 of 2013, as amended to L.N. 134 "
          "of 2021).", "https://legislation.mt/eli/sl/549.83/eng"),
    ("9", "MiŻien. Data and scripts: data/cc-138/park_instruments.csv; tools/cc-138-report/calc.py; "
          "data/cc-138/checks.csv.", ""),
])
S.append(PageBreak())
S += appendix_a("A experiment · B observational study with a control or gradient · C review, guidance or "
                "official statistics · D assertion or anecdote. ◆ marks a source known only second-hand.")
S += [Spacer(1, 5 * mm)]
S += revision_log([("1.0", "17 Nov 2026", "First issue. Verdict Not substantiated (moderate confidence); pledge not yet "
                    "due. Draft pending right of reply.")])

build_report(Report(
    number="138", out=str(FIG / "report.pdf"), kicker="Parks and open space",
    title_lines=["Protected from", "development?"],
    subtitle_lines=["Testing the Office of the Prime Minister’s statement", "on the White Rocks national park notice"],
    quote_lines=["“…biex jiġu mħarsa minn kwalunkwe", "żvilupp fil-futur.”"], quote_size=15,
    attribution="Office of the Prime Minister, 29 July 2026 (“…so that they are safeguarded from any future development”).",
    context="On Cabinet’s approval of the legal notice establishing White Rocks as a national park.",
    verdict="Not substantiated", verdict_note="The notice establishes the park but restricts no development",
    footer_lines=["Version 1.0  ·  17 November 2026", "Status: draft, pending right of reply",
                  "Prepared from public sources and open data.", "Repository: github.com/leandergrech/Mizien"],
    running_head="White Rocks national park – OPM, July 2026", version="1.0", date="17 November 2026",
    pdf_title="Protected from development? Claim Check 138",
    pdf_subject="Tests the OPM's statement linking the White Rocks national park notice to protection from development",
    pledge_label="Not yet due", story=S))
