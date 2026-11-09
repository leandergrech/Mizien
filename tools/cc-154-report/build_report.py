"""Claim Check 154 report. Run calc.py and figures.py first. Output: out/report.pdf"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import *  # noqa: E402,F401

FIG = HERE / "out"
S = []

# ================================================================== TL;DR
S += [SectionHeading(None, "TL;DR"), Spacer(1, 1 * mm),
      P("In late October 2025 the European Commission wrote to BirdLife Malta about Malta’s finch-trapping “research derogation”. "
        "Italpress (MNA) reported on 2 November 2025 that the Commission had “reaffirmed” that the derogation “remains in breach of "
        "European Union law”. We found the letter itself, published by BirdLife Malta, and compared it with that report.", lead)]
S.append(key_points([
    ("The letter says less than the headline.",
     "Italpress’s words “remains in breach of European Union law” do not appear in the letter. The Commission wrote that it "
     "“did not endorse” the framework, that the new derogation “seems similar” to the 2024 one, and that its services are "
     "“currently assessing” the new one."),
    ("What the Commission did say is accurately reported.",
     "The February 2025 letter of formal notice: “That request still stands.” And, if EU law is not complied with, the Commission "
     "“may decide to take additional enforcement steps such as referring Malta back to the Court of Justice”."),
    ("The underlying legal position is on the record.",
     "On 19 September 2024 the Court of Justice declared in case C-23/23 that Malta’s derogation scheme for seven finch species breached the "
     "Birds Directive. Whether the 17 October 2025 rules do the same is for the Commission’s assessment; BirdLife Malta reports a new "
     "formal notice of 21 November 2025 ◆, which we have not read."),
    ("What we cannot tell.",
     "We did not read the 17 October 2025 rules, the Government’s reasoning, or the new notice. The letter’s date is "
     "24 October 2025 on its signature line; Italpress gives 27 October."),
]))
S += [Spacer(1, 2.5 * mm), VerdictMeter(1), Spacer(1, 3 * mm),
      tiles([("0", GREY, "Occurrences of “in breach” or “remains valid” in the Commission’s letter"),
             ("Still stands", GREEN, "The Commission’s words on the February 2025 formal notice"),
             ("393 days", BLUE, "From the CJEU judgment (19 Sep 2024) to the new derogation (17 Oct 2025)"),
             ("Not read", GREY, "The 17 Oct 2025 rules and the new formal notice")]),
      Spacer(1, 4 * mm),
      up_down("Nothing: Supported is the top of the scale. Moving from Largely supported to Supported would need the "
              "Commission’s own wording that the new derogation is in breach, for example the formal notice INFR(2025)2128 as issued.",
              "A Commission or Court finding that the 17 October 2025 rules meet Article 9 of the Birds Directive, or a letter "
              "withdrawing the February 2025 notice."),
      Spacer(1, 3 * mm)]
S.append(PageBreak())

# ================================================================== 1
S.append(SectionHeading(1, "The claim and what we could verify"))
S.append(P("The claim record put three phrases in quotation marks: “remains in breach of European Union law”, “remains valid” and "
           "“may refer the case back to the ECJ”. They come from Italpress’s own text [1]; the only words Italpress puts "
           "in quotation marks are “research derogation” and “illegal practice” (the latter is BirdLife’s). We therefore restate the claim "
           "from the Commission’s letter [2] and rate what the Commission wrote, not the outlet’s wording."))
S.append(std_table([
    [C("Source", cellh), C("What it says", cellh), C("Our access", cellh), C("Status", cellh)],
    [C("<b>European Commission</b>, DG Environment, letter to BirdLife Malta, Ref. Ares(2025)8980114, signed by Nicola Notaro, Head of Unit [2]"),
     C("“Commissioner Roswall did not endorse the Maltese derogation framework”; a new ‘research derogation’ was adopted on 17 October, "
       "“which seems similar” to the 2024 one; the February 2025 letter of formal notice: “That request still stands.” "
       "The Commission services “are currently assessing” the new derogation; “the Commission may decide to take additional "
       "enforcement steps such as referring Malta back to the Court of Justice”."),
     C("Full text of the PDF read, 9 Nov 2026 (BirdLife Malta’s copy). Electronic signature 24 Oct 2025."), C("<b>The claim</b> (speaker’s own words)")],
    [C("<b>Italpress (MNA)</b>, 2 Nov 2025 [1]"),
     C("Headline and text: the Commission “has reaffirmed” the derogation “remains in breach of European Union law”; the formal "
       "notice “remains valid”; may refer the case back to the ECJ. Dates the letter 27 October."),
     C("Full text read."), C("Outlet’s account; locates the claim")],
    [C("<b>BirdLife Malta</b>, 1 Nov 2025 [3]"),
     C("Reports the letter: the Commission did not endorse the framework, the February 2025 notice “still stands”, it is assessing the new "
       "derogation and may refer Malta back to the Court."),
     C("Full text read."), C("Advocacy source; agrees with the letter")],
    [C("<b>Court of Justice</b>, judgment of 19 Sep 2024, C-23/23, <i>Commission v Malta</i> [4]"),
     C("Declares that, by adopting a derogation scheme allowing live-capturing of seven finch species, Malta failed to fulfil obligations under "
       "Articles 5 and 8(1) of Directive 2009/147/EC, read with Article 9(1)."),
     C("Operative part read on EUR-Lex."), C("<b>Primary (court)</b>")],
    [C("<b>BirdLife Malta</b>, 21 Nov 2025 [5]"),
     C("Says the Commission opened a new infringement procedure, letter of formal notice INFR(2025)2128, stating that the 17 Oct 2025 "
       "derogation mirrors the system previously annulled; Malta has two months to reply."),
     C("BirdLife’s post read; the notice itself not read ◆."), C("Second-hand ◆")],
], [40 * mm, 74 * mm, 30 * mm, 26 * mm]))
S += [Spacer(1, 4 * mm),
      callout([P("WHAT WE COULD NOT READ", tag),
               P("The text of the 17 October 2025 rules; the Government’s explanation of them; the Commission’s letter of formal notice "
                 "INFR(2025)2128 or an infringement-register entry; any reply from the Minister. The PDF’s file name carries a different Ares "
                 "number (Ares20259162948) from the reference printed in the letter (Ares(2025)8980114); we cannot say why. Routes tried are in "
                 "<i>literature/CC-154/README.md</i>.", small)],
              bg=AMBER_PALE, bar=AMBER), Spacer(1, 4 * mm)]

# ================================================================== 2
S.append(SectionHeading(2, "Method"))
S.append(P("<b>Questions.</b> (A) Did the Commission say that its February 2025 formal notice still stands? (B) Did it say it is assessing "
           "the new derogation and may refer Malta back to the Court? (C) Did it say the derogation “remains in breach of EU law”?"))
S.append(P("<b>Evidence.</b> We read the letter word for word and searched it for the phrases in the claim record, then compared it with "
           "Italpress and BirdLife Malta. We read the operative part of the judgment for the legal background. Dates are in "
           "<i>data/cc-154/checks.csv</i>. We did not test the 17 October 2025 rules against the judgment: the rules were not read and the "
           "claim is about the Commission’s statement, not about the legality of the rules."))
S.append(P("<b>Grades.</b> The letter and the judgment are grade C (official documents); news and NGO posts are grade D. "
           "<b>Verdicts</b> follow Appendix A."))

# ================================================================== 3
S.append(CondPageBreak(110 * mm))
S.append(SectionHeading(3, "What the evidence shows"))
S.append(P("<b>The letter.</b> It answers an email of 16 October from BirdLife Malta’s chief executive and is signed by a head of unit at the request of "
           "the Commissioner’s Cabinet [2]. It states that the Commissioner “did not endorse” the framework and asked how the national "
           "authorities plan to ensure “full implementation” of the ruling in C-23/23; that the 2024 derogation led to a letter of formal notice in February "
           "2025 and “That request still stands”; that derogations must be “strictly applied and enforced” under Article 9; and that the services are "
           "“currently assessing” the new derogation, with referral to the Court named as one possible further step [2]."))
S.append(fig(FIG / "fig1_timeline.png", width=CW * 0.98))
S.append(P("Figure 1. Public record, 15 October to 21 November 2025. Sources: letter [2], BirdLife Malta [3, 5], Italpress [1]. "
           "The 21 November entry is second-hand.", cap))
S.append(P("<b>What the letter does not say.</b> The phrases “remains in breach”, “in breach” and “remains valid” do not occur in it. "
           "“Still stands” is the Commission’s phrase for the February 2025 request. The Commission’s only judgement on the new "
           "derogation is that it “seems similar” to the 2024 one, which was the subject of the notice; it describes its own assessment as ongoing [2]. "
           "Italpress’s “remains in breach” is therefore the outlet’s characterisation of the letter, not the Commission’s sentence [1]."))
S.append(P("<b>The legal background.</b> The Court’s operative part is about the scheme Malta had adopted before the judgment [4]. Whether the "
           "17 October 2025 rules cure that is the question the Commission says it is assessing [2]. BirdLife Malta reports that, on "
           "21 November 2025, the Commission concluded they do not and opened a new procedure [5]. We read BirdLife’s post only, so we treat this as "
           "context ◆ and do not rely on it for the verdict. We did not read the Government’s position."))
S.append(callout([P("WHAT THIS DOES AND DOES NOT SHOW", tag),
                  P("It shows that the Commission’s statements on the formal notice and on possible referral are as reported, and that the report’s "
                    "headline wording is stronger than the letter’s. It does not show whether the 17 October 2025 rules comply with the "
                    "Birds Directive; that is for the Commission and, if referred, the Court.", small)],
                 bg=BLUE_PALE, bar=BLUE))

# ================================================================== 4
S.append(CondPageBreak(70 * mm))
S.append(SectionHeading(4, "Where the evidence points different ways"))
S.append(contested("Does the Commission say the derogation “remains in breach”?", "REPORT STRONGER THAN LETTER", AMBER,
                   "Italpress’s headline and first sentence say the Commission “reaffirmed” the derogation “remains in breach of European Union "
                   "law” [1]. The Court found Malta’s earlier scheme in breach in 2024 [4]; the letter calls the new derogation “similar” to the 2024 one [2]; "
                   "BirdLife Malta reports a new formal notice in November ◆ [5].",
                   "The letter itself withholds endorsement and says the new derogation is under assessment; it makes no finding of breach "
                   "on it [2]. The Government’s reasoning for the 17 October 2025 rules was not read.",
                   "On 24 October 2025 the Commission’s own words are “assessing”, not “in breach”. The stronger reading is supported by the "
                   "judgment and, second-hand, by the later notice, but not by the letter.",
                   label_a="EVIDENCE FOR ‘IN BREACH’", label_b="WHAT THE LETTER SAYS"))

# ================================================================== 5
S.append(CondPageBreak(120 * mm))
S.append(SectionHeading(5, "Testing the claim"))
verd = lambda t, c: chip(t, c, w=29 * mm)
S.append(std_table([
    [C("Sub-claim", cellh), C("Said by", cellh), C("What the evidence shows", cellh), C("Rating", cellh)],
    [C("<b>A.</b> The formal notice sent to Malta in February 2025 still stands"),
     C("European Commission [2]"),
     C("Letter: “That request still stands.” BirdLife Malta’s report agrees [3]. The record’s “remains valid” is Italpress’s paraphrase [1]."),
     verd("ACCURATE", GREENC)],
    [C("<b>B.</b> The Commission is assessing the new derogation and may refer Malta back to the Court"),
     C("European Commission [2]"),
     C("Letter: services “currently assessing”; the Commission “may decide to take additional enforcement steps such as referring Malta back "
       "to the Court of Justice”. The record’s “may refer the case back to the ECJ” is Italpress’s wording [1]."),
     verd("ACCURATE", GREENC)],
    [C("<b>C.</b> The derogation “remains in breach of European Union law”"),
     C("Italpress headline [1]; not in the letter [2]"),
     C("Headline wording, not rated as the Commission’s. Background: CJEU 2024 judgment [4]; later formal notice reported by BirdLife Malta ◆ [5]."),
     verd("NOT RATED", GREY)],
], [46 * mm, 24 * mm, 66 * mm, 28 * mm], valign="MIDDLE"))

# ================================================================== 6
S += [Spacer(1, 6 * mm), SectionHeading(6, "Verdict and requests for evidence"),
      verdict_box("Largely supported", "What the Commission wrote is as reported on the formal notice and possible referral; the "
                  "“in breach” wording is the outlet’s and goes beyond the letter. Confidence: moderate."), Spacer(1, 4 * mm)]
S.append(P("<b>Why.</b> (1) The two statements that are the Commission’s own, that the February 2025 request “still stands” and that it may "
           "refer Malta back to the Court, are in the letter as reported. (2) We rate <i>Largely supported</i> rather than <i>Supported</i> "
           "because the claim record’s central quotation, “remains in breach of European Union law”, is not in the letter, which says the "
           "new derogation is being assessed. (3) Confidence is moderate: we read the letter in BirdLife Malta’s copy, not from the Commission, and we did "
           "not read the 17 October 2025 rules or the later notice. The rating applies to the statement as reported, not to any person or body."))
S.append(CondPageBreak(60 * mm))
S.append(P("Evidence we are asking for", h2))
S.append(requests_list([
    "The Commission’s letter of formal notice INFR(2025)2128 (November 2025) or its infringement-register entry.",
    "The text of the 17 October 2025 finch-trapping rules and the Government’s explanation of how they implement C-23/23.",
    "The Commission’s own copy of the letter of October 2025, to settle the date (24 or 27 October) and the Ares reference.",
]))
S += [Spacer(1, 4 * mm),
      callout([P("RIGHT OF REPLY", tag),
               P("No right of reply is needed for this verdict (maintainer rule of 5 October 2026). Corrections and further evidence are welcome "
                 "through the contest form.", small)], bg=PALE, bar=GREEN)]

# ================================================================== 7
S += [Spacer(1, 6 * mm), SectionHeading(7, "Limitations")]
for l in ["We read the Commission’s letter in a copy published by BirdLife Malta, an interested party. The text is a Commission-signed PDF, "
          "but we have not confirmed it against a Commission copy, and its file name carries a different Ares number from the reference printed in it.",
          "The letter’s signature line gives 24 October 2025; Italpress says 27 October. The three-day difference is unexplained; it does not affect the rating.",
          "The statement that the phrases “in breach” and “remains valid” are absent from the letter covers this one PDF, read in full on 9 November 2026.",
          "The November 2025 formal notice is known only from BirdLife Malta’s post ◆. We use it as context, not as evidence for the verdict.",
          "We did not read the 17 October 2025 rules or the Government’s position, and we offer no view on whether they comply with the Birds Directive."]:
    S.append(P("• " + l, bul))

S += [Spacer(1, 6 * mm), SectionHeading(None, "References")]
S += references([
    ("1", "Italpress/MNA (2 Nov 2025). EU Commission, Malta’s finch trapping still breaches EU law.", "https://www.italpress.com/?p=598716"),
    ("2", "European Commission, DG Environment (Nicola Notaro) to Mark Sultana, BirdLife Malta. Ref. Ares(2025)8980114, e-signed 24 Oct 2025. "
          "Copy published by BirdLife Malta, retrieved 9 Nov 2026.", "https://birdlifemalta.org/wp-content/uploads/2025/10/Ares20259162948.pdf"),
    ("3", "BirdLife Malta (1 Nov 2025). European Commission confirms that finch-trapping derogation is not in line with the European Court of Justice ruling.",
     "https://birdlifemalta.org/2025/11/european-commission-clarifies-it-has-not-endorsed-maltas-finch-trapping-derogation/"),
    ("4", "Court of Justice of the EU (19 Sep 2024). Case C-23/23, European Commission v Republic of Malta, judgment (First Chamber). EUR-Lex CELEX 62023CJ0023.",
     "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:62023CJ0023"),
    ("5", "BirdLife Malta (21 Nov 2025). BirdLife Malta welcomes new infringement action as Commission calls on Malta to comply with EU Birds Directive ◆ (second-hand).",
     "https://birdlifemalta.org/2025/11/birdlife-malta-welcomes-new-infringement-action-as-commission-calls-on-malta-to-comply-with-eu-birds-directive/"),
    ("6", "Miżien. Calculation script and outputs: tools/cc-154-report/calc.py; data/cc-154/checks.csv.", ""),
])

S.append(PageBreak())
S += appendix_a("A experiment · B observational study with a control or gradient · C review, guidance or "
                "official statistics · D assertion or anecdote. ◆ marks a source known only second-hand.")
S += [Spacer(1, 5 * mm)]
S += revision_log([("1.0", "9 Nov 2026", "First issue. Verdict Largely supported (moderate confidence); no right of reply needed.")])

build_report(Report(
    number="154", out=str(FIG / "report.pdf"), kicker="Nature and wildlife",
    title_lines=["Finch trapping:", "what did the", "Commission write?"],
    subtitle_lines=["Testing a report of the Commission’s October 2025", "letter against the letter itself"],
    quote_lines=["“That request still stands.”"], quote_size=16,
    attribution="European Commission, DG Environment, letter to BirdLife Malta, October 2025.",
    context="Speaker’s own words (the letter, Ref. Ares(2025)8980114).",
    verdict="Largely supported", verdict_note="Letter as reported; “in breach” wording is the outlet’s",
    footer_lines=["Version 1.0  ·  9 November 2026", "Status: no right of reply needed",
                  "Prepared from public sources and EU documents.", "Repository: github.com/leandergrech/Mizien"],
    running_head="Finch trapping: what did the Commission write?", version="1.0", date="9 November 2026",
    pdf_title="Finch trapping: what did the Commission write? Claim Check 154",
    pdf_subject="Tests Italpress's report of the Commission's October 2025 letter on Malta's finch-trapping derogation",
    story=S))
